#!/usr/bin/env python3
"""Build two ad-only, self-contained Loon plugins from reviewed endpoint rules.
No publishing or modifications to the existing 27 plugins.
"""
from pathlib import Path
import argparse, hashlib, json, re
ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
RULES = []
NAMES = {p.stem: re.search(r'^#!name=(.*)', p.read_text(), re.M)[1] for p in (ROOT/'plugins').glob('*.lpx')}

def add(mode, app, hosts, pattern, action, note, phase='response', source=None):
    # Native jq still parses bodies; guard unexpected shapes and roll back on errors.
    match = re.fullmatch(r'response\.json\.jq\((.*)\)', action)
    if match:
        token = match[1]
        expr = token[1:-1] if token.startswith('`') else json.loads(token)
        expr = 'if type=="object" then . as $original | try (' + expr + ') catch $original else . end'
        action = 'response.json.jq(`' + expr + '`)'
    RULES.append(dict(mode=mode, app=app, hosts=hosts.split(','), pattern=pattern, action=action, phase=phase, note=note, source=source or f'plugins/{app}.lpx'))

def jq(mode, app, hosts, pattern, expr, note, source=None):
    add(mode,app,hosts,pattern,'response.json.jq(`'+expr+'`)',note,source=source)

def req(mode, app, hosts, pattern, note):
    add(mode,app,hosts,pattern,'reject_dict(200)',note,'request')

def copy(mode,app,hosts,needle,note):
    lines=[s for s in (ROOT/'plugins'/f'{app}.lpx').read_text().splitlines() if s.startswith(('request if','response if')) and needle in s and 'then script(' not in s]
    assert len(lines)==1,(app,needle,len(lines))
    line=lines[0]
    # Remove old per-feature conditions. Each generated rule receives its App switch.
    condition,action=line.split(' then ',1)
    condition=condition[condition.index('${url}'):]
    add(mode,app,hosts,condition.removeprefix('${url} ~= '),action,note,line.split(' ',1)[0])

# ------------------- Only splash -------------------
copy('splash','12306','ad.12306.cn',r'getAdList','仅开屏广告接口')
copy('splash','Amap','m5.amap.com',r'splash_screen','仅开屏接口')
jq('splash','Amap','m5.amap.com',r'/^https:\/\/m5\.amap\.com\/ws\/shield\/frogserver\/aocs\/updatable\/1(?:\?|$)/i','del(.data.splashscreen, .data.SplashScreenControl, .data.splashview_config)','只移除启动配置内三个开屏字段')
copy('splash','Bilibili','app.bilibili.com',r'show|event','保留原开屏列表清理')
copy('splash','Bilibili','app.bilibili.com',r'splash\/list','保留原开屏模拟响应；不处理视频播放')
jq('splash','Coolapk','api.coolapk.com',r'/^https:\/\/api\.coolapk\.com\/v6\/main\/init(?:\?|$)/i','if (.data|type)=="array" then .data |= map(if type=="object" and (.extraDataArr|type)=="object" then .extraDataArr |= (if has("SplashAd.Type") then .["SplashAd.Type"]="" | .["SplashAd.resumeType"]="" | .["SplashAd.hType"]="" | .["SplashAd.onResume"]=0 | if has("SplashAd.timeout") then .["SplashAd.timeout"]="1" else . end else . end) else . end) else . end','保留所有初始化卡片；仅修改旧版已有开屏字段和等待参数；新组合待实测')
copy('splash','Douban','api.douban.com',r'app_ads','仅开屏广告接口；沿用原插件签名版限制')
copy('splash','Douban','frodo.douban.com',r'feature_switch','保留三个开屏 SDK 配置字段处理')
copy('splash','Goofish','acs.m.goofish.com',r'idlecommerce','仅明确开屏接口；排除 scene.restore 全场景拦截')
copy('splash','JD','api.m.jd.com',r'(?:start)','仅 start 开屏图片和展示次数')
copy('splash','McDonalds','api.mcd.cn',r'home\/splash','沿用开屏投放过期方案')
# Taobao: target only explicit splash configuration; generic cloudvideo/poplayer not safe as splash-only.
jq('splash','Taobao','guide-acs.m.taobao.com',r'/^https:\/\/guide-acs\.m\.taobao\.com\/gw\/mtop\.taobao\.wireless\.home\.splash\.awesome\.get(?:\/|\?|$)/i','if (.data.containers.splash_home_base.base.sections|type)=="array" then (.data.containers.splash_home_base.base.sections[] | select(type=="object") | .bizData["taobao-splash"].data | select(type=="array")) |= map(if type=="object" then . + {waitTime:"0",times:"0",hotStart:"false",haveVoice:"false",hideTBLogo:"false",enable4G:"false",coldStart:"false",startTime:"3818332800000",endTime:"3818419199000",gmtStart:"2090-12-31 00:00:00",gmtEnd:"2090-12-31 23:59:59",gmtStartMs:"3818332800000",gmtEndMs:"3818419199000"} | (if .imgUrl then .imgUrl="" else . end) | (if .videoUrl then .videoUrl="" else . end) else . end) else . end','从原 JS 迁移开屏配置分支；不拦截普通视频或通用活动模板',source='scripts/Taobao.js')
jq('splash','Tieba','tiebac.baidu.com',r'/^https?:\/\/tiebac\.baidu\.com\/c\/s\/sync(?:\?|$)/i','del(.home_screen_ad)','仅已知 home_screen_ad 字段；不保证覆盖其他 SDK 开屏')
jq('splash','Xiaohongshu','edith.xiaohongshu.com',r'/^https:\/\/edith\.xiaohongshu\.com\/api\/sns\/v1\/system_service\/config(?:\?|$)/','del(.data.splash)','不删除商店、主题和加载图片等非广告配置',source='scripts/Xiaohongshu.js')
jq('splash','Xiaohongshu','edith.xiaohongshu.com',r'/^https:\/\/edith\.xiaohongshu\.com\/api\/sns\/v2\/system_service\/splash_config(?:\?|$)/','if (.data.ads_groups|type)=="array" then .data.ads_groups |= map(if type=="object" then .start_time=3818332800 | .end_time=3818419199 | if (.ads|type)=="array" then .ads |= map(if type=="object" then .start_time=3818332800 | .end_time=3818419199 else . end) else . end else . end) else . end','沿用原开屏投放时间处理，无媒体缓存',source='scripts/Xiaohongshu.js')
copy('splash','Xiaoxiang','mall.meituan.com',r'homepage\/splash','仅开屏广告接口')
# try/catch must preserve the input string on parse error, not the jq error text.
JLAUNCH='if (.launch|type)=="string" then .launch |= (. as $original | try (fromjson | .ads=[] | tojson) catch $original) elif (.launch|type)=="object" then .launch.ads=[] else . end'
jq('splash','Zhihu','api.zhihu.com',r'/^https:\/\/api\.zhihu\.com\/commercial_api\/(?:real_time_launch_v2|launch_v2)(?:\?|$)/',JLAUNCH,'只清空 launch.ads，保留其他浮层和原字符串格式')
copy('splash','Zhuanzhuan','app.zhuanzhuan.com',r'getOpenScreen','仅开屏接口')
jq('splash','Weibo','bootpreload.uve.weibo.com',r'/^https:\/\/bootpreload\.uve\.weibo\.com\/v[12]\/ad\/preload(?:\?|$)/i','if (.ads|type)=="array" then .ads |= map(if type=="object" then .start_time=3818332800 | .end_time=3818419199 | .daily_display_cnt=50 | .display_duration=0 else . end) else . end','迁移原开屏预加载分支',source='scripts/Weibo.js')
jq('splash','Weibo','wbapp.uve.weibo.com',r'/^https:\/\/wbapp\.uve\.weibo\.com\/(?:preload\/get_ad|wbapplua\/wbpullad\.lua)(?:\?|$)/i','if (.cached_ad.ads|type)=="array" then .cached_ad.ads |= map(if type=="object" then .show_count=50 | .duration=0 | .start_date=3818332800 | .end_date=3818419199 else . end) else . end','迁移原开屏缓存分支',source='scripts/Weibo.js')
# SDK response can be JSON followed by OK. Numeric/Boolean field replacements preserve that framing.
replacements=[(r'"show_push_splash_ad"\s*:\s*true',r'"show_push_splash_ad":false'),(r'"background_delay_display_time"\s*:\s*\d+',r'"background_delay_display_time":31536000'),(r'"lastAdShow_delay_display_time"\s*:\s*\d+',r'"lastAdShow_delay_display_time":31536000'),(r'"realtime_ad_video_stall_time"\s*:\s*\d+',r'"realtime_ad_video_stall_time":0'),(r'"realtime_ad_timeout_duration"\s*:\s*\d+',r'"realtime_ad_timeout_duration":0'),(r'"displaytime"\s*:\s*\d+',r'"displaytime":0'),(r'"displayintervel"\s*:\s*\d+',r'"displayintervel":31536000'),(r'"allowdaydisplaynum"\s*:\s*\d+',r'"allowdaydisplaynum":0')]
add('splash','Weibo','sdkapp.uve.weibo.com',r'/^https:\/\/sdkapp\.uve\.weibo\.com\/interface\/sdk\/sdkad\.php(?:\?|$)/i',' | '.join('response.body.replace(/'+p+'/, `'+v+'`)' for p,v in replacements),'定点替换已知开屏标量字段；兼容 JSON+OK；不对广告数组做正则删除',source='scripts/Weibo.js')

# ------------------- In-app ads only -------------------
# No generic layout, recommendation, account, media saving or networking changes.
req('inapp','12306','mobile.12306.cn',r"/^https:\/\/mobile\.12306\.cn\/otsmobile\/app\/mgs\// && ${request.header['operation-type']} == \"com.cars.otsmobile.integration.activityBanner\"".replace('\\"','"'),'仅 activityBanner；不拦整个首页、会员问答或支付完成入口')
jq('inapp','Amap','m5.amap.com',r'/^https:\/\/m5\.amap\.com\/ws\/shield\/frogserver\/aocs\/updatable\/1(?:\?|$)/i','del(.data.adStatementConfig, .data.adCustomerRetainArchitecture, .data.adImEntryConfig, .data.adVenueConfig, .data.EndNaviC3AdCard)','只保留原配置中的明确广告字段；删除远程 jq 依赖')
copy('inapp','Amap','m5-zb.amap.com',r'promotion-web','广告推广资源接口')
copy('inapp','BaiduNetdisk','pan.baidu.com',r'pcs\/adv','仅广告接口；恢复 getconfig/getsyscfg 和页面入口')
for needle in [r'large_card_material',r'get_shopping_info',r'index\/feed',r'getInfoBy',r'feed\/index\?',r'feed\/index\/story',r'ads\/materials',r'activity\/deliver']:
    # feedVideoOnly/cardExtra rules match same URL; select original pure-ad gate explicitly.
    if needle in [r'feed\/index\?',r'feed\/index\/story']:
        lines=[l for l in (ROOT/'plugins/Bilibili.lpx').read_text().splitlines() if '${feedAds}' in l and needle in l]
        assert len(lines)==1
        l=lines[0]; c,a=l.split(' then ',1); add('inapp','Bilibili','app.bilibili.com',c[c.index('${url} ~= ')+10:],a,'只按明确 ad_info/广告卡类型过滤')
    else:
        host='line3-h5-mobile-api.biligame.com' if 'large_card' in needle else ('api.bilibili.com' if needle in [r'ads\/materials',r'activity\/deliver'] else 'api.live.bilibili.com')
        copy('inapp','Bilibili',host,needle,'保留原生广告与直播购物浮层过滤；无 Protobuf 脚本')
for needle,host in [(r'ads\.index','netflow-mtop.cainiao.com'),(r'adkeyword','cn-acs.m.cainiao.com'),(r'ads\.m?show','cn-acs.m.cainiao.com')]: copy('inapp','Cainiao',host,needle,'仅独立广告接口；不改每日现金任务、会员或首页推荐')
jq('inapp','Coolapk','api.coolapk.com',r'/^https:\/\/api\.coolapk\.com\/v6\/(?:main\/(?:dataList|indexV8)|page\/dataList)(?:\?|$)/i','if (.data|type)=="array" then .data |= map(select(if type=="object" then .entityTemplate != "sponsorCard" else true end)) else . end','只移除 sponsorCard，保留热搜、普通图片卡和推荐')
jq('inapp','Coolapk','api.coolapk.com',r'/^https:\/\/api\.coolapk\.com\/v6\/feed\/detail(?:\?|$)/i','if (.data|type)=="object" and (.data|has("detailSponsorCard")) then .data.detailSponsorCard=[] else . end','仅详情赞助卡；不筛评论 id 或删正常商品内容')
copy('inapp','Dewu','app.dewu.com',r'app\/advertisement','广告接口可能兼含开屏；不虚称为独立开屏接口')
copy('inapp','Didi','res.xiaojukeji.com',r'activity\/mget','活动广告接口；不改证书校验、网络连通性或行程布局')
for needle in [r'movie\/ad',r'home_banner']: copy('inapp','Douban','frodo.douban.com',needle,'仅电影广告与首页广告横幅；沿用原签名版限制')
for endpoint in ['mtop.taobao.idlehome.home.nextfresh','mtop.taobao.idlehome.home.newitem.page']:
    jq('inapp','Goofish','acs.m.goofish.com','/^https:\/\/acs\.m\.goofish\.com\/gw\/'+re.escape(endpoint).replace('/','\\/')+'\//i','if (.data.sections|type)=="array" then .data.sections |= map(select(if type=="object" then .data.clickParam.args.cardType != "mamaAD" else true end)) else . end','只移除 mamaAD；保留正常推荐和首页其他卡片')
jq('inapp','Goofish','acs.m.goofish.com',r'/^https:\/\/acs\.m\.goofish\.com\/gw\/mtop\.taobao\.idle\.local\.home\//i','if (.data.sections|type)=="array" then .data.sections |= map(select(if type=="object" then .template.cardEnum != "ads" else true end)) else . end','只移除 cardEnum=ads')
jq('inapp','Goofish','g-acs.m.goofish.com',r'/^https:\/\/g-acs\.m\.goofish\.com\/gw\/mtop\.taobao\.idlemtopsearch\.search\//i','if (.data.resultList|type)=="array" then .data.resultList |= map(select(if type=="object" then .data.item.main.exContent.dislikeFeedback.clickParam.args.bizType != "ad" else true end)) else . end','只移除搜索明确广告，保留搜索前缀栏')
copy('inapp','JD','api.m.jd.com',r'(?:deliverLayer|orderTrackBusiness)','仅物流页面横幅；不拦推荐、不改 HTTPDNS')
copy('inapp','LuckinCoffee','capi.lkcoffee.com',r'adposNew','仅广告位接口；恢复公共模块、礼品卡与成长日历')
copy('inapp','McDonalds','api.mcd.cn',r'richpop','仅推广弹窗')
copy('inapp','NeteaseCloudMusic','interface*.music.163.com',r'(ocpc\/)?ad','仅独立广告响应；移除 AES/gzip 脚本及页面白名单')
jq('inapp','Pinduoduo','api.pinduoduo.com',r'/^https:\/\/api\.pinduoduo\.com\/order\//i','del(.marketing_banner_vo, .shipping.banner_above_recommend)','仅订单营销横幅；不封 titan 长连接和日志域名，不动底栏')
copy('inapp','SFExpress','ccsp-egmas.sf-express.com',r'app\/ad','仅广告接口；恢复积分商城及首页模块')
copy('inapp','Taopiaopiao','acs.m.taobao.com',r'popup','推广弹窗')
copy('inapp','Taopiaopiao','acs.m.taobao.com',r'mtopitemadvertiseapi','广告接口')
jq('inapp','Taopiaopiao','acs.m.taobao.com',r'/^https:\/\/acs\.m\.taobao\.com\/gw\/mtop\.film\.mtopintegrationapi\.homeconfig\//i','del(.data.returnValue.floatingBanner)','只移除悬浮横幅；保留搜索和顶部标签')
jq('inapp','Tieba','tiebac.baidu.com',r'/^https?:\/\/tiebac\.baidu\.com\/c\/s\/sync(?:\?|$)/i','del(.advertisement_config, .ad_adsense, .ad_config, .ad_sdk_priority) | if (.wl_config|type)=="object" then .wl_config |= (if has("home_ad_num") then .home_ad_num=0 else . end | if has("frs_ad_num") then .frs_ad_num=0 else . end | if has("pb_comment_ad_num") then .pb_comment_ad_num=0 else . end) else . end','仅广告配置；无 Protobuf 处理，不删视频帖和直播帖；覆盖有限')
req('inapp','WeChat','mp.weixin.qq.com',r'/^https:\/\/mp\.weixin\.qq\.com\/mp\/getappmsgad(?:\?|$)/i','仅公众号广告接口；移除 90 多个小程序主机与 wxs.qq.com 泛拦截')
# Microblog: inspect only known content arrays, never recursive keyword deletion of user content.
WBAD='def isad: if type != "object" then false else (.mblogtypename == "广告" or .readtimetype == "adMblog" or .promotion.recommend == "广告" or .content_auth_info.content_auth_title == "广告" or .ads_material_info.is_ads == true or .is_ad == 1) end; '
WBARRAY='def clean: map(select((isad or (if type=="object" then (.mblog|isad) else false end))|not)); '
wbexpr=WBAD+WBARRAY+'reduce ["statuses","cards","items","reposts","hot_reposts"][] as $key (.; if (.[$key]|type)=="array" then .[$key] |= clean else . end) | if (.cards|type)=="array" then (.cards[] | select(type=="object") | .card_group | select(type=="array")) |= clean else . end'
jq('inapp','Weibo','api.weibo.cn',r'/^https:\/\/api\.weibo\.cn\/2\/(?:statuses\/(?:container_timeline(?:_hot|_topic|_topicpage|_unread)?|unread_hot_timeline|repost_timeline)|video\/full_screen_stream|searchall|cardlist)(?:\?|$)/i',wbexpr,'原 isAd 中仅保留明确广告标志；保留快转、非关注内容、热推、头像、菜单、连播和默认分组',source='scripts/Weibo.js')
req('inapp','Weibo','card.weibo.com,weibo.com',r'/^https:\/\/(?:card\.weibo\.com\/article\/m\/aj|weibo\.com\/ttarticle\/x\/m\/aj)\/uvead(?:\?|$)/i','仅文章广告；不拦赞赏和投票')
jq('inapp','Xiaohongshu','edith.xiaohongshu.com,rec.xiaohongshu.com',r'/^https:\/\/(?:edith|rec)\.xiaohongshu\.com\/api\/sns\/v6\/homefeed(?:\?|$)/','if (.data|type)=="array" then .data |= map(select(if type=="object" then (has("ads_info")|not) else true end)) else . end','只移除原广告标记 ads_info；保留直播、带货笔记、相关推荐',source='scripts/Xiaohongshu.js')
jq('inapp','Xiaohongshu','edith.xiaohongshu.com',r'/^https:\/\/edith\.xiaohongshu\.com\/api\/sns\/v4\/note\/videofeed(?:\?|$)/','if (.data|type)=="array" then .data |= map(select(if type=="object" then (has("ad")|not) else true end)) else . end','只移除原 ad 标记；不修改视频保存或缓存',source='scripts/Xiaohongshu.js')
req('inapp','Xiaohongshu','www.xiaohongshu.com',r'/^https:\/\/www\.xiaohongshu\.com\/api\/sns\/v1\/ads\/resource(?:\?|$)/i','独立广告资源接口')
for needle in [r'bubble\/operate',r'category-banner',r'api\/c\/banner']:
    copy('inapp','Xiaoxiang','mall.meituan.com',needle,'只保留广告横幅和浮层；不拦订单/个人页推荐')
copy('inapp','Xiaoxiang','portal-portm.meituan.com',r'horn_ios','只删除广告配置字段')
jq('inapp','Zhihu','api.zhihu.com',r'/^https:\/\/api\.zhihu\.com\/commercial_api\/answer\/[0-9]+\/bottom-v2(?:\?|$)/','if (.adjson|type)=="string" then .adjson |= (. as $original | try (fromjson | .ads=[] | tojson) catch $original) elif (.adjson|type)=="object" then .adjson.ads=[] else . end','保留嵌套 JSON 的字符串类型')
jq('inapp','Zhihu','api.zhihu.com',r'/^https:\/\/api\.zhihu\.com\/next-render(?:\?|$)/','if (.data|type)=="array" then .data |= map(select(if type=="object" then .type!="ad" else true end)) else . end','只移除明确广告；保留回答与分页')
# launch_v2 can contain both splash and in-app preloads: disjoint field sets in the two plugins.
jq('inapp','Zhihu','api.zhihu.com',r'/^https:\/\/api\.zhihu\.com\/commercial_api\/(?:app_float_layer|launch_v2)(?:\?|$)/','reduce ["app_float_video","float_layer","search_middle_page"][] as $k (.; if has($k) then .[$k] |= (if type=="string" then . as $original | try (fromjson | .ads=[] | tojson) catch $original elif type=="object" then .ads=[] else . end) else . end)','只处理应用内三个广告字段，不改 launch')
for needle in [r'getallpopwin',r'queryFrontPageWindowInfo']:
    copy('inapp','Zhuanzhuan','app.zhuanzhuan.com',needle,'只保留推广弹窗，不改商品推荐和我的页面')

UNSUPPORTED_SPLASH = {'BaiduNetdisk':'旧版 getconfig/getsyscfg 为通用配置，未证明是开屏专用','Cainiao':'现有 ads 接口无法可靠区分开屏与应用内','Dewu':'advertisement 为通用广告接口','Didi':'现有活动投放和通用域名拦截不能证明仅影响开屏','JD-Takeout':'现有规则主要是推荐/页面精简','LuckinCoffee':'adposNew 为通用广告位','NeteaseCloudMusic':'现有广告域名和 /ad/ 为共享广告资源','Pinduoduo':'旧版没有明确开屏专用接口，不保留 titan 等通用封锁','SFExpress':'/app/ad/ 为通用广告接口','Taopiaopiao':'queryadvertise 为通用广告接口','WeChat':'公众号与小程序广告，不能视为微信本体开屏','YouTube':'现有实现为视频/信息流去广告，非开屏'}
UNSUPPORTED_INAPP={'Taobao':'现有 JS 是开屏和通用活动模板，跨 App 的拦截不纳入淘宝内部去广告','JD-Takeout':'现有规则以推荐、钱包、页面入口删除为主，缺少明确广告判据','YouTube':'需要 Protobuf 脚本及视频域名解密；本轮以零 JS 原生版为基线，不纳入。需要时单独启用原 YouTube 插件并测量开销。'}

def build(mode, selected=None, enable_inapp=False):
    rules=[r for r in RULES if r['mode']==mode and (selected is None or r['app'] in selected)]
    apps=sorted({r['app'] for r in rules})
    if not apps: raise ValueError('没有选中受支持的 App')
    title='开屏广告' if mode=='splash' else '应用内广告'
    desc=('仅处理明确开屏入口；不保证覆盖所有 App 的所有开屏。' if mode=='splash' else '只保留广告过滤；默认全部关闭，请按需打开 App 开关。')+'无 JS、无定时任务、无外部资源。关闭开关不移除静态 MitM 域名；不用时停用整个插件。'
    if mode=='inapp' and enable_inapp: desc=desc.replace('默认全部关闭，请按需打开 App 开关。','所选 App 默认开启（豆瓣除外），可逐项关闭。')
    lines=[f'#!name={title}',f'#!desc={desc}','#!author=原规则：可莉、RuCu6、fmz200、zmqcherish、Sliverkiss、kokoryh、Keywos、app2smile；精简整理：Codex','#!homepage=https://github.com/brilliantfires/loon-plugins','#!tag=去广告','#!system=iOS,iPadOS','#!system_version=15','#!loon_version=3.5.1(998)','#!date=2026-11-05','','[Argument]']
    for app in apps:
        default=(mode=='splash' or enable_inapp) and app!='Douban'
        extra=',desc=沿用原插件限制仅适用兼容的签名版豆瓣' if app=='Douban' else ''
        lines.append(f'app_{app.replace("-","_")} = switch,{str(default).lower()},tag={NAMES[app]}{extra}')
    lines+=['','[Rewrite]']
    for app in apps:
        lines+=['',f'# {NAMES[app]}']
        for r in rules:
            if r['app']!=app: continue
            lines+=['# '+r['note'],f'{r["phase"]} if ${{app_{app.replace("-","_")}}} == true && ${{url}} ~= {r["pattern"]} then {r["action"]}']
    hosts=sorted({h for r in rules for h in r['hosts']})
    lines+=['','[MitM]','# 静态名单。开关仅关闭复写，不动态撤销 TLS 解密。','hostname = '+', '.join(hosts),'']
    return '\n'.join(lines),dict(apps=apps,hosts=hosts,rules=len(rules),scripts=0)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--apps',help='Comma-separated App IDs; physically removes all other rules and MitM hosts')
    parser.add_argument('--output',type=Path,default=OUT)
    parser.add_argument('--enable-inapp',action='store_true')
    args=parser.parse_args()
    selected=set(args.apps.split(',')) if args.apps else None
    if selected and selected-set(NAMES): raise ValueError(f'Unknown apps: {selected-set(NAMES)}')
    args.output.mkdir(parents=True,exist_ok=True)
    summary={}
    for mode,filename in [('splash','Splash-Only.lpx'),('inapp','InApp-Ads.lpx')]:
        if selected and not any(r['mode']==mode and r['app'] in selected for r in RULES): continue
        content,summary[mode]=build(mode,selected,args.enable_inapp)
        (args.output/filename).write_text(content)
    if selected is None:
        files=sorted({r['source'] for r in RULES})
        manifest={'date':'2026-11-05','summary':summary,'rules':RULES,'unsupported_splash':UNSUPPORTED_SPLASH,'unsupported_inapp':UNSUPPORTED_INAPP,'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}}
        (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
