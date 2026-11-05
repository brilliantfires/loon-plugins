#!/usr/bin/env python3
"""Offline regression tests; does not emulate the Loon parser or iPhone network stack."""
import copy, importlib.util, json, re, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('build',HERE/'build.py'); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
count=0

def check(condition, message):
    global count
    assert condition,message
    count+=1

def expression(r):
    m=re.fullmatch(r'response\.json\.jq\(`(.*)`\)',r['action'])
    return m[1] if m else None

def run(r,obj):
    p=subprocess.run(['jq','-c',expression(r)],input=json.dumps(obj),text=True,capture_output=True)
    check(p.returncode==0, f'{r["app"]}: {p.stderr}')
    return json.loads(p.stdout)

def rule(mode,app,part):
    found=[r for r in b.RULES if r['mode']==mode and r['app']==app and part in r['pattern']]
    assert len(found)==1,(mode,app,part,len(found))
    return found[0]

for mode,filename in [('splash','Splash-Only.lpx'),('inapp','InApp-Ads.lpx')]:
    text,summary=b.build(mode)
    check(text==(HERE/filename).read_text(),'generated artifact drift')
    check('[Script]' not in text and 'jq_file(' not in text and 'mock_file(' not in text,'external dependency')
    check('[Rule]' not in text,'uncontrolled domain/QUIC rejection')
    lines=[l for l in text.splitlines() if l.startswith(('request if','response if'))]
    check(len(lines)==len(set(lines)),'duplicate rule')
    declared=set(re.findall(r'^(app_\w+) = switch,',text,re.M))
    for line in lines:
        m=re.match(r'(request|response) if \$\{(app_\w+)\} == true && \$\{url\} ~= ',line)
        check(m is not None and m[2] in declared,'missing App guard: '+line)
    if mode=='inapp': check('= switch,true' not in text,'in-app must default off')
    # Physical pruning must remove hosts as well as rules, without modifying the full artifact.
    limited,stats=b.build(mode,{'Zhihu'},True)
    check(stats['hosts']==['api.zhihu.com'] and stats['apps']==['Zhihu'],'hostname pruning failed')
    check('weibo' not in limited.lower(),'unselected App remains')

# Native jq execution, malformed schema protection and idempotence for every expression.
for r in b.RULES:
    if not expression(r): continue
    for obj in [{},None,[],{'data':None},{'data':[]},{'data':{'items':None}},{'data':'unexpected'}, {'keep':{'nested':[1,2,3]}}]:
        out=run(r,obj)
        check(run(r,out)==out,'not idempotent: '+r['app'])
        if isinstance(obj,dict) and 'keep' in obj: check(out['keep']==obj['keep'],'unrelated data changed')

r=rule('splash','Zhihu','real_time')
s={'launch':json.dumps({'ads':[{'id':'ad'}],'request_id':'normal'}),'float_layer':json.dumps({'ads':[1]}),'keep':42}
o=run(r,s); check(json.loads(o['launch'])=={'ads':[],'request_id':'normal'},'splash failed'); check(o['float_layer']==s['float_layer'],'splash changed in-app ads')
check(run(r,{'launch':'broken JSON'})=={'launch':'broken JSON'},'invalid embedded JSON not preserved')
r2=rule('inapp','Zhihu','app_float')
check(run(r,run(r2,s))==run(r2,run(r,s)),'shared endpoint plugins do not commute')
r=rule('inapp','Zhihu','next-render'); s={'data':[{'type':'answer','id':1},{'type':'ad','id':2},{'type':'article','id':3}],'paging':{'next':'keep'}}
o=run(r,s); check([v['id'] for v in o['data']]==[1,3] and o['paging']==s['paging'],'answer/pagination loss')
r=rule('splash','Coolapk','main'); s={'data':[{'entityId':944},{'entityId':20131,'entities':[{'title':'酷品'}]},{'extraDataArr':{'SplashAd.Type':'tanx','SplashAd.timeout':'4000','normal':'keep'}}]}
o=run(r,s); check(len(o['data'])==3 and o['data'][0]==s['data'][0] and o['data'][1]==s['data'][1],'init cards removed'); check(o['data'][2]['extraDataArr']['SplashAd.timeout']=='1','timeout lost'); check(o['data'][2]['extraDataArr']['normal']=='keep','normal config lost')
r=rule('inapp','Coolapk','dataList'); s={'data':[{'entityTemplate':'sponsorCard'},{'entityTemplate':'imageScaleCard','title':'酷安热搜'},{'entityTemplate':'feed','title':'值得买|红包'}]}; check(run(r,s)['data']==s['data'][1:],'normal cards incorrectly removed')
r=rule('inapp','Xiaohongshu','homefeed'); s={'data':[{'id':1,'ads_info':{}},{'id':2,'model_type':'live_v2'},{'id':3,'has_related_goods':True,'card_icon':{},'related_ques':[1]},{'id':4,'model_type':'note'}],'cursor':'keep'}; o=run(r,s); check(o=={'data':s['data'][1:],'cursor':'keep'},'non-ad live/shopping content changed')
r=rule('inapp','Weibo','container_timeline'); s={'statuses':[{'id':1,'mblogtypename':'广告'},{'id':2,'mblogtypename':'热推','user':{'mbtype':2},'buttons':[1]},{'id':3,'readtimetype':'adMblog'},{'id':4,'text':'我讨论广告技术','promotion':{'type':'normal'}}],'cards':[{'mblog':{'is_ad':1}},{'mblog':{'id':5,'mblogtypename':'热推'}}],'groups':[{'title':'最新微博'},{'title':'全部关注'}]}; o=run(r,s); check(o['statuses']==[s['statuses'][1],s['statuses'][3]],'Weibo normal content changed'); check(o['groups']==s['groups'] and o['cards']==s['cards'][1:],'Weibo groups changed')
r=rule('splash','Xiaohongshu','system_service\\/config'); s={'data':{'splash':[1],'store':{'keep':1},'app_theme':'normal','loading_img':'normal'}}; o=run(r,s); check(o['data']=={k:v for k,v in s['data'].items() if k!='splash'},'XHS config overfiltered')
r=rule('splash','Taobao','awesome'); item={'imgUrl':'ad','videoUrl':'ad','normal':9}; s={'data':{'containers':{'splash_home_base':{'base':{'sections':[{'bizData':{'taobao-splash':{'data':[item]}}}]}}}},'other':'keep'}; o=run(r,s); got=o['data']['containers']['splash_home_base']['base']['sections'][0]['bizData']['taobao-splash']['data'][0]; check(got['waitTime']=='0' and got['normal']==9 and got['imgUrl']=='' and o['other']=='keep','Taobao scope')

# Compile every regex with Node, check known URL positives and hostname lookalikes.
patterns=[]
for r in b.RULES:
    m=re.match(r'^/(.*?)(?<!\\)/([i]*)',r['pattern'])
    check(m is not None,'regex missing')
    patterns.append({'pattern':m[1],'flags':m[2],'app':r['app']})
node='''const fs=require('fs'); const p=JSON.parse(fs.readFileSync(0,'utf8')); for(const x of p){ const r=new RegExp(x.pattern,x.flags); if(r.test('https://evil.example/path')) throw Error(x.app); } console.log(p.length);'''
p=subprocess.run(['node','-e',node],input=json.dumps(patterns),text=True,capture_output=True); check(p.returncode==0,p.stderr)
# SDK JSON and JSON+OK framing, multiple advertisements and normal fields preserved.
r=rule('splash','Weibo','sdkad')
repls=re.findall(r'response\.body\.replace\(/(.*?)(?<!\\)/, `(.*?)`\)',r['action'])
for suffix in ['', 'OK']:
    s=json.dumps({'show_push_splash_ad':True,'background_delay_display_time':10,'ads':[{'displaytime':5,'allowdaydisplaynum':3,'id':1},{'displaytime':6,'allowdaydisplaynum':4,'id':2}],'normal':'keep'})+suffix
    out=s
    for pattern,value in repls: out=re.sub(pattern,lambda _:value,out)
    check(out.endswith('OK') if suffix else out.endswith('}'),'SDK framing changed')
    obj=json.loads(out[:-2] if suffix else out)
    check(obj['normal']=='keep' and obj['show_push_splash_ad'] is False and all(a['displaytime']==0 and a['allowdaydisplaynum']==0 for a in obj['ads']),'SDK rewrite failed')

# Recheck existing private captures without distributing or printing their contents.
import zipfile
capture_results={}
base=b.ROOT.parent
cool=base/'coolapk-analysis/capture-42.zip'
if cool.exists():
    with zipfile.ZipFile(cool) as z: before=json.loads(z.read('68726_96457_1793332637627/response_body_raw'))
    after=run(rule('splash','Coolapk','main'),before)
    check(len(after['data'])==len(before['data']),'captured init card loss')
    restored=copy.deepcopy(after)
    keys=['SplashAd.Type','SplashAd.resumeType','SplashAd.hType','SplashAd.onResume','SplashAd.timeout']
    for old,new in zip(before['data'],restored['data']):
        if isinstance(old.get('extraDataArr'),dict) and 'SplashAd.Type' in old['extraDataArr']:
            for key in keys:
                if key in old['extraDataArr']: new['extraDataArr'][key]=old['extraDataArr'][key]
                else: new['extraDataArr'].pop(key,None)
    check(restored==before,'captured non-splash field changed')
    capture_results['Coolapk_init']=1
for filename,record in [('capture-57.zip','59767_88745_1793457905397'),('capture-58.zip','59839_89119_1793458065253')]:
    path=base/'mcd-analysis'/filename
    if not path.exists(): continue
    with zipfile.ZipFile(path) as z: before=json.loads(z.read(record+'/response_body_raw'))
    after=run(rule('splash','McDonalds','splash'),before)
    check(len(after['data']['list'])==len(before['data']['list'])==8,'captured McD records lost')
    check(all(x['countDown']==0 and x['endTime'].startswith('2000-') for x in after['data']['list']),'captured McD expiry failure')
    check([x['id'] for x in before['data']['list']]==[x['id'] for x in after['data']['list']],'captured McD ID changed')
    capture_results['McDonalds_splash']=capture_results.get('McDonalds_splash',0)+1

result={'offline_assertions':count,'rule_count':len(b.RULES),'jq_count':sum(expression(r) is not None for r in b.RULES),'status':'passed','private_capture_responses':capture_results,'limitations':['Not a Loon parser test','Not a real app network test','No measured energy savings','Native regex replacement framing tested with Python; Loon runtime still requires device validation']}
(HERE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,indent=2))
