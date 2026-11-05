#!/usr/bin/env python3
"""Create a smaller pair of plugins from the bundled manifest, without network access."""
import argparse,json,re
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--apps',required=True,help='Comma-separated App IDs, such as Bilibili,Zhihu')
p.add_argument('--output',type=Path,default=Path('selected'))
p.add_argument('--enable-inapp',action='store_true')
a=p.parse_args(); here=Path(__file__).resolve().parent
m=json.loads((here/'manifest.json').read_text()); chosen=set(a.apps.split(','))
known=set(m['summary']['splash']['apps'])|set(m['summary']['inapp']['apps'])
if chosen-known: p.error('Unsupported App IDs: '+','.join(sorted(chosen-known)))
a.output.mkdir(parents=True,exist_ok=True)
if a.output.resolve()==here: p.error('Choose a different output folder to preserve the original files')
for mode,filename in [('splash','Splash-Only.lpx'),('inapp','InApp-Ads.lpx')]:
    rules=[r for r in m['rules'] if r['mode']==mode and r['app'] in chosen]
    apps=sorted({r['app'] for r in rules})
    if not apps: continue
    text=(here/filename).read_text(); header=text.split('[Argument]')[0]
    if mode=='inapp' and a.enable_inapp: header=header.replace('默认全部关闭，请按需打开 App 开关。','所选 App 默认开启（豆瓣除外），可逐项关闭。')
    declarations={l.split(' = ',1)[0]:l for l in text.splitlines() if ' = switch,' in l}
    lines=[header.rstrip(),'','[Argument]'];names={}
    for app in apps:
        variable='app_'+app.replace('-','_');line=declarations[variable]
        if mode=='inapp' and a.enable_inapp and app!='Douban':line=line.replace('switch,false','switch,true',1)
        names[app]=line.split('tag=',1)[1].split(',desc=',1)[0];lines.append(line)
    lines+=['','[Rewrite]']
    for app in apps:
        lines+=['','# '+names[app]]
        for r in rules:
            if r['app']==app:
                lines+=['# '+r['note'],f'{r["phase"]} if ${{app_{app.replace("-","_")}}} == true && ${{url}} ~= {r["pattern"]} then {r["action"]}']
    hosts=sorted({h for r in rules for h in r['hosts']})
    lines+=['','[MitM]','# 静态名单。开关仅关闭复写，不动态撤销 TLS 解密。','hostname = '+', '.join(hosts),'']
    target=a.output/filename;target.write_text('\n'.join(lines))
    print(f'{target}: {len(apps)} apps, {len(rules)} rules, {len(hosts)} MitM patterns')
