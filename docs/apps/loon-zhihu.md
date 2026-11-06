# 去广告插件保留清单

整理日期为 2026-11-04。每个应用保留一个版本，共 21 个 Loon 插件。

用户已确认酷安、12306、麦当劳、菜鸟的最新测试版实机有效。其他插件沿用目录内最新版本，本次未重新进行手机测试。文件中的测试版名称及历史验证说明保持原样，当前确认记录以本清单为准。

| 应用 | 保留文件 | 说明 |
| --- | --- | --- |
| 知乎 | [Zhihu-Splash.lpx](Zhihu-Splash.lpx) | 内容为 v3，与原 Zhihu-Ads-v3.lpx 完全相同。 |
| 豆瓣 | [Douban-Splash-Fix.lpx](Douban-Splash-Fix.lpx) | 开屏 SDK 配置补丁，需配合原有豆瓣规则。 |
| 酷安 | [Coolapk-Splash-Timeout-Test.lpx](Coolapk-Splash-Timeout-Test.lpx) | 最新整合版，含等待时长调整。 |
| 闲鱼 | [Goofish-Integrated-Test.lpx](Goofish-Integrated-Test.lpx) | 整合版，已包含 scene.restore 补丁。 |
| 京东 | [JD-Integrated.lpx](JD-Integrated.lpx) | 本地整合版。 |
| 麦当劳 | [McDonalds-Ads-v2-Test.lpx](McDonalds-Ads-v2-Test.lpx) | v2 过期配置方案。 |
| 菜鸟 | [Cainiao-Daily-Task-v2.lpx](Cainiao-Daily-Task-v2.lpx) | v2 每日现金任务过滤补丁，需配合原有去广告插件。 |
| 微博 | [Weibo.lpx](Weibo.lpx) | 本地脚本及12项功能开关，待实机验证。 |
| 网易云音乐 | [NeteaseCloudMusic.lpx](NeteaseCloudMusic.lpx) | 本地脚本及17项开关，待实机验证。 |
| 微信公众号 | [WeChat.lpx](WeChat.lpx) | 本地维护版，原生规则，待实机验证。 |
| 小红书 | [Xiaohongshu.lpx](Xiaohongshu.lpx) | 本地规则及脚本，待实机验证。 |
| 小象超市 | [Xiaoxiang.lpx](Xiaoxiang.lpx) | 本地维护版，原生复写，待实机验证。 |
| 百度贴吧 | [Tieba.lpx](Tieba.lpx) | 本地ProtoBuf脚本及视频帖过滤开关，待实机验证。 |
| 百度网盘 | [BaiduNetdisk.lpx](BaiduNetdisk.lpx) | 8条原生复写，待实机验证。 |
| YouTube | [YouTube.lpx](YouTube.lpx) | 纯去广告本地版，播放回退兼容性待实机验证。 |
| 瑞幸咖啡 | [LuckinCoffee.lpx](LuckinCoffee.lpx) | 7条原生请求过滤，待实机验证。 |
| 淘宝 | [Taobao.lpx](Taobao.lpx) | 本地规则与脚本，待实机验证。 |
| 顺丰速运 | [SFExpress.lpx](SFExpress.lpx) | 3条规则，module-config模拟响应不完整，此项暂缺。 |
| 淘票票 | [Taopiaopiao.lpx](Taopiaopiao.lpx) | 本地维护版，原生复写，待实机验证。 |
| 转转 | [Zhuanzhuan.lpx](Zhuanzhuan.lpx) | 本地维护版，待实机验证。 |
| 12306 | [12306-Reject-JSON-Test.lpx](12306-Reject-JSON-Test.lpx) | 原生复写版，无脚本依赖；应用内请求改为空 JSON 响应，待复测。 |

## 转转本地维护

2026-11-04 根据用户提供的网络版规则整理。原标题简化为“转转”，原规则作者为可莉。文件为 `Zhuanzhuan.lpx`。接口匹配统一支持带查询参数及无查询参数的 URL，合并 getmyprofilev3 的两项处理，为三个 JQ 处理补充缺失数组保护。共 15 条复写，无外部脚本依赖。保留原规则的过滤范围和模拟响应内容。已完成本地匹配及 JSON 样例检查，尚未实机验证。

## 12306 原生复写优化

2026-11-04 将脚本替换为按请求头匹配的原生复写，保留开屏规则及五项 operation-type 筛选。需要支持请求头条件的新式复写语法。

应用内过滤的响应行为由脚本的断开连接改为 HTTP 200 和 `{}`，此次优化版尚未实机验证。已移除局域网脚本依赖及开屏域名 DIRECT 规则，开屏命中后由 Loon 本地返回空 JSON。

原插件和脚本备份于 `/Users/Mac/.Trash/12306脚本版备份-20261104-162838`，可恢复。原描述中“仍停留蓝屏可确认固定等待”的判断过强，现已删除，该现象本身无法确定原因。

## 清理记录

11 个旧版、重复文件或独立测试补丁已移入系统废纸篓，可恢复。

备份位置为 `/Users/Mac/.Trash/去广告插件旧版-20261104-162351`。

- `zhihu-analysis/Zhihu-Splash-before-popup.lpx`
- `loon-zhihu/12306-Splash-Wait-Test.lpx`
- `loon-zhihu/Cainiao-Daily-Task.lpx`
- `loon-zhihu/Zhihu-Ads-v3.lpx`
- `loon-zhihu/McDonalds-Ads.lpx`
- `loon-zhihu/Goofish-Scene-Restore-Test.lpx`
- `loon-zhihu/Coolapk-Integrated-Fix.lpx`
- `loon-zhihu/12306-Integrated.lpx`
- `loon-zhihu/Coolapk-Splash-Config-v2.lpx`
- `loon-zhihu/Coolapk-Splash-Test.lpx`
- `loon-zhihu/Coolapk-Splash-Config-v3.lpx`

## 小象超市本地维护

2026-11-04 根据用户提供的7条请求过滤、脚本正文及补充的匹配地址整理。标题为“小象超市”，原规则作者为可莉。文件为 `Xiaoxiang.lpx`，保留原请求过滤的正则匹配范围。

将 `portal-portm.meituan.com/horn_ios/mergeRequest` 响应脚本替换为原生 JSON 字段删除，清理 `aidata_dd_resource_config.data.customer.feature_src_list.ad`。原脚本仅在 ad 为 JavaScript 真值时删除，原生版对存在的该字段直接删除，包括 false、0、空字符串和 null。无外部脚本依赖。已完成本地正则与 JSON 路径样例检查，尚未实机验证。

## 小红书本地维护

2026-11-04 根据用户提供的规则、12份脚本附件及截图整理。11份附件相同，另1份缺少末尾右括号，采用完整附件。标题为“小红书”，保留作者 RuCu6、fmz200 署名。

文件为 `Xiaohongshu.lpx` 和 `Xiaohongshu.js`。9条原生复写、1条QUIC规则及4条按域名区分的脚本入口，共用一份本地脚本。搜索响应的空数组及空对象改用JSON类型，banner_list、hot_list和trending地址支持有无查询参数。

原始完整脚本匹配行只提供了 imagefeed/live_photo/save，其余入口根据脚本内17个路径分支和截图域名补齐。edith对应脚本全部分支，rec对应homefeed和视频保存，so对应搜索，www对应视频保存。这些补齐的匹配条件尚未实机验证。

脚本修正包括空响应和未知接口只结束一次、持久化缓存损坏时容错、v4视频列表全部被过滤时正确返回空数组、子评论使用自身字段处理。实况照片和视频保存保留原有跨请求缓存逻辑，因此继续使用JS。脚本由 `http://192.168.3.35:18765/Xiaohongshu.js` 本地托管，手机首次下载或刷新脚本时需能访问电脑。后续局域网地址改变时需要调整脚本URL。

已通过JS语法、本地模拟请求、脚本各分支URL覆盖、JSON类型及下载文件一致性检查，尚未在手机验证广告过滤和保存效果。

### 小红书功能开关

2026-11-04 增加11项独立插件开关，默认全部开启以沿用此前行为。

开屏广告、信息流广告、隐藏直播卡片、隐藏带货卡片、推广弹窗、搜索精简、页面精简、关注推荐精简、图片与实况保存、视频保存、评论图片与实况保存。

脚本按新式Script对象参数读取开关，旧入口缺少参数时按全部开启处理。图片和视频共有的function_switch保存按钮配置在任一保存功能开启时生效。评论媒体处理沿用原脚本的red_id改名等行为。开屏开关也涵盖原脚本删除app_theme/loading_img/store的启动配置处理。

已通过17个脚本路径回归、16种响应全部关闭、信息流/直播/带货各自独立控制、视频保存与广告过滤分离测试。全部关闭时响应保持原状且不写媒体缓存，QUIC基础规则仍启用。手机开关UI及真实流量效果待实测。开关前文件已备份到系统废纸篓。

手机更新插件和脚本后，在插件参数中调整开关。首次下载及刷新JS需访问电脑本地服务。

## 微博本地维护

2026-11-04 根据用户提供的18条请求复写、3条分流规则、20个脚本入口及20份脚本附件整理。20份附件完全相同。去除1条重复的tiny_video_info_show复写，最终保留17条请求复写。

文件为 `Weibo.lpx` 和 `Weibo.js`，标题为“微博”，保留 RuCu6、zmqcherish 署名。20个脚本匹配条件沿用用户补充的原配置，共用本地脚本 `http://192.168.3.35:18765/Weibo.js`。首次下载或刷新脚本需要手机可访问电脑此地址。

沿用小红书的方式添加12个功能开关，默认全部开启。按响应所在页面分组，页面开关控制该分支的广告过滤与原脚本内容精简行为。

- 开屏广告。调整开屏投放与等待配置。
- 首页与关注流精简。过滤广告及原规则中的关注推荐快转等内容。
- 评论区精简。过滤评论推广气泡弹幕及提示。
- 搜索与发现精简。过滤热搜推广搜索推荐及发现页模块。
- 个人主页精简。清理博主主页推荐皮肤及关注弹窗。
- 我的页面精简。按原规则保留个人页指定入口。
- 消息页精简。清理活动通知闪聊及动态广告。
- 微博详情精简。清理商品投票赞赏模块并调整详情菜单。
- 视频页精简。清理视频广告商品悬浮窗及红包。
- 关闭视频连播。清空自动连播列表。
- 超话页精简。清理超话推荐热词及广场入口。
- 首页推广精简。清理签到红包悬浮窗和发布入口。

原脚本的应用图标分支未包含在原插件匹配入口中，未暴露无效图标开关。三个原始域名分流规则独立保留，不受页面参数控制。要停用全部规则可禁用整个插件。

脚本增加空响应返回、异常时保留原响应及缺失data字段的保护。SDK开屏兼容纯JSON和JSON加OK后缀，保留原后缀格式。其他业务过滤逻辑沿用原脚本，包括关注流中的非关注博主/快转过滤、个人页入口白名单以及关闭视频连播。

已完成JS语法、默认行为与原脚本对照、全部关闭及单项开启隔离、开屏响应格式和无效输入测试。实际脚本匹配URL覆盖检查通过，尚未在手机验证。

## 微信公众号本地维护

2026-11-04 根据用户提供的1条域名规则、2条请求复写及截图整理。文件为 `WeChat.lpx`，标题为“微信公众号”，保留 RuCu6 署名及原始匹配范围。包括 wxs.qq.com 域名后缀拦截和 mp.weixin.qq.com 指定接口过滤，无脚本依赖。原规则也包含相关推荐和监测请求过滤。已通过本地正则正反例及局域网下载内容一致性检查，尚未实机验证。

## 网易云音乐本地维护

2026-11-04 根据用户提供的6条域名规则、7条原生复写、6条脚本配置及Keywos脚本正文整理。原脚本时间为2025-02-19，截图插件日期为2026-10-02，两者日期不同，本次依据附件实际内容处理，尚未确认当前App响应结构是否仍一致。

文件为 `NeteaseCloudMusic.lpx` 和 `NeteaseCloudMusic.js`，标题为“网易云音乐”。保留RuCu6及Keywos署名。去除重复的首页脚本入口，按脚本分支补上底栏标签接口。关注列表入口限定为脚本实际支持的get/v2。脚本路径增加接口结束边界，搜索默认词域名正则补全转义点。6条域名规则和7条原生复写沿用原有过滤范围，其中也含版本检查、推荐和页面入口过滤，独立于脚本参数。

附件存在旧版首页case缺少开头斜线、问候模块commonResourceList被赋成forEach返回值、未知接口重复调用done、评论缺失tag或user时报错等问题。新版修正路径与缺失字段处理，保留显示中的问候模块列表，所有响应只结束一次，异常时保留原响应。

新版移除会员等级与到期时间伪装，移除把评论用户followed强制设为true的处理。评论会员图标和挂件清理继续由评论区精简控制。未加入原配置中没有入口的音效排序和会员中心处理。未互关提示仍按原脚本mutualFollowDay为null的启发式判断，准确性未确认，默认关闭。

提供17项开关。首页精简、评论区精简、发现页精简、我的页面精简默认开启。隐藏问候语默认开启。漫游、笔记、发现三个底栏隐藏开关和其余八个首页模块隐藏开关默认关闭，未互关提示默认关闭。首页精简开启时沿用原脚本模块白名单，关闭时保留整个首页响应。底栏入口根据脚本路径补齐，真实App是否调用该接口仍需手机验证。

使用Loon原生AES-ECB/PKCS7与gzip API，最低版本沿用3.5.1(998)。密钥和AES输出已与用户附件内嵌库交叉比对，处理后的加密负载保留输入的gzip状态。无需下载远端加密库。官方API依据为 https://nsloon.app/en/docs/Script/script_api/ 。

已通过80项加解密、gzip、功能开关与回归检查，以及72种接口URL组合匹配和局域网下载一致性检查。以上为Node模拟Loon API的本地测试，Loon运行时及真实接口尚未验证。脚本由 `http://192.168.3.35:18765/NeteaseCloudMusic.js` 托管，手机首次下载和刷新脚本时需能访问电脑。

## 淘票票本地维护

2026-11-04 根据用户提供的规则及补充的queryadvertise接口整理。文件为 `Taopiaopiao.lpx`，标题为“淘票票”，保留可莉署名。合并homeconfig两项响应处理，去除重复的aristotle递归过滤，最终为2条请求过滤和2条响应JQ处理，无脚本依赖。

保留原URL匹配范围。homeconfig移除floatingBanner和searchShadeList，按原规则移除activeImage为真值的顶部标签并删除其余标签的backgroundColor。aristotle逐层清除componentId包含tpp_banner或等于tpp_guess_like的节点。增加缺失字段及非数组保护，避免向无子节点的对象添加nodes为null的字段。

已通过本地jq嵌套样例、正常内容保留、缺失及非标准字段、幂等性、接口匹配边界和局域网下载一致性检查。尚未在手机验证，截图宣称的开屏效果也需实机确认。

## 淘宝本地维护

2026-11-04 根据用户提供的6条域名规则、11条请求复写、2条脚本入口及两份相同的RuCu6脚本正文整理。脚本原始时间为2024-01-12。文件为 `Taobao.lpx` 与 `Taobao.js`，标题为“淘宝”。去除getadv、mtopadvertiseapi.queryadvertise、idle.home.welcome各1条重复规则，最终保留8条请求过滤及2条脚本入口。

保留原接口匹配范围及开屏字段设置，包括未来时间戳和字符串类型的布尔配置。原规则也会命中飞猪、闲鱼、一淘等应用使用的指定接口，继续沿用此范围。脚本补充缺失字段和数组类型保护，未知接口、空响应、解析失败均保持原响应，所有路径只调用一次done。移除重复的waitTime赋值。按外层入口的大小写不敏感匹配统一脚本匹配。MITM仅保留实际使用的3个主机，截图中没有对应规则的heic.alicdn.com未加入。

已通过53次响应模拟、缺失字段、异常输入和幂等性运行，以及接口匹配和局域网下载一致性检查，尚未在手机验证。首次下载及刷新本地脚本时需要手机能访问 `http://192.168.3.35:18765/Taobao.js`。

## 顺丰速运本地维护

2026-11-04 根据用户提供的规则整理为 `SFExpress.lpx`，标题为“顺丰速运”。包含广告接口拦截、积分商城商品列表拦截和appHomeConfig中position等于数值2的模块过滤。原始URL匹配范围保持不变，首页过滤增加缺失数组及非标准元素保护。纯原生复写，无脚本。

用户两次提供的module-config模拟响应均在url内嵌“快速寄件”配置处结束，缺少JSON闭合结构。无法还原原始完整页面配置，该项未纳入插件。保留其他3条规则，尚不能覆盖原插件全部页面精简。MITM仅包含这3条规则使用的ccsp-egmas和ucmp主机。

已通过本地jq样例、URL匹配和局域网下载一致性检查，实际效果待手机验证。完整module-config JSON或原lpx仍是补齐该项所需的信息。

## 瑞幸咖啡本地维护

2026-11-04 根据用户提供的8条请求复写及截图整理，原作者Sliverkiss。文件为 `LuckinCoffee.lpx`，标题为“瑞幸咖啡”。移除1条重复的modules规则，最终保留7条原生请求过滤，均沿用原来的URL前缀匹配和HTTP 404返回方式。MITM为capi.lkcoffee.com，无脚本依赖。

原规则范围也包含成长日历、礼品卡页面及公共模块接口，本地版保持该范围。已检查匹配样例、其他主机与普通接口不命中，以及局域网下载内容一致性，真实广告过滤与页面功能待实机验证。

## YouTube纯去广告本地维护

2026-11-04 按用户“只需要去广告”要求整理。用户提供的请求脚本Build为2026/7/12，后续补充响应脚本Build为2026/7/19。响应脚本与作者公开文件的构建日期一致，保留原protobuf实现与消息定义，在其后实现独立、可读的广告清理入口。文件为 `YouTube.lpx` 和 `YouTube.js`，标题为“YouTube”，脚本内保留作者及Apache 2.0许可证文本。

处理6类响应接口，browse、next、search清理广告卡片，player清理adPlacements、adSlots和pageadViewthroughconversion，reel_watch_sequence只移除isAd为真的条目，get_watch对其player和next做同样的广告处理。原始协议未知字段继续保留，生成代码中两个空消息读取器改为调用通用读取器，使其正确消费并保留未知字段。无广告变化时保留原始响应字节。

未保留字幕或歌词翻译、后台播放与画中画开启、上传/Shorts/选段/升级按钮隐藏、设置入口注入，以及按shorts布局名称过滤普通内容。响应匹配移除guide和account/get_setting。原广告识别中基于字段编号及布局的持久化白名单/黑名单未复用，避免沿用旧配置中的内容过滤结果。广告识别仍沿用原脚本pagead字节标记及最小1000字节阈值和inline_injection_entrypoint_layout.eml布局判据。

原请求脚本在缓存密钥命中时会将initplayback重定向到作者的init-stream.maasea.workers.dev，由远端处理UMP，且其能力开关无法完全限定为只去广告。本地版采用原脚本密钥未命中时已有的空HTTP 200回退，使用原生response.body.mock实现，促使客户端尝试普通播放接口。没有远端Worker依赖、没有密钥缓存和log_event/config收集入口。这个回退路径在当前YouTube版本上的播放兼容性尚未确认，不能据本地测试承诺视频广告全部去除。

加入youtubei.googleapis.com和googlevideo.com的QUIC拒绝规则，配合HTTP路径处理。MITM为youtubei.googleapis.com和*.googlevideo.com。按用户截图的要求需启用MitM over HTTP/2及QUIC回退保护。

已通过41次protobuf响应运行，覆盖视频广告、信息流与搜索广告、Shorts广告、普通Shorts保留、字幕与播放能力不变、未知字段保留、无广告响应及无效输入，并检查URL范围和局域网下载一致性。以上为本地模拟，手机广告效果和播放兼容性待实测。首次安装或刷新脚本时手机需能访问 `http://192.168.3.35:18765/YouTube.js`。

## 百度网盘本地维护

2026-11-04 根据用户提供的7条请求过滤及1条响应过滤整理。文件为 `BaiduNetdisk.lpx`，标题为“百度网盘”，保留可莉署名。清除复制文本中的Markdown加粗标记及额外转义，将语法还原为正常Loon新式复写。保留原URL范围，包括要求查询参数、pcs单数字版本号和api/plugin/get拦截。无脚本依赖。

入口列表过滤删除type为novel、shortplay、print和job_hunt的项目，其余内容保留。增加缺失字段、非数组及非对象列表元素保护。原规则也拦截getconfig、getsyscfg及plugin/get等通用配置接口，本地版沿用原范围，具体页面功能影响待手机验证。

已通过本地jq样例、幂等性、缺失字段、正反例接口匹配和局域网下载一致性检查。尚未实机验证。

## 百度贴吧本地维护

2026-11-04 根据用户提供的规则和app2smile脚本正文整理。文件为 `Tieba.lpx` 与 `Tieba.js`，标题为“百度贴吧”，保留可莉及app2smile署名。原脚本日期为2025-11-18。

删除getInterestClassList和个人主页字段删除各1条重复规则，sync的3项处理合为同一条动作链，个人主页删除与JQ过滤合为同一条动作链。最终保留2条分流规则、11条原生复写和1条ProtoBuf脚本入口。所有URL匹配范围沿用原配置。

同步配置中的广告数值继续使用数字类型。sync导航、个人主页custom_grid、zone_info及common_func_noraml列表增加缺失字段和类型保护，沿用原页面精简范围。两个针对180.76.76.200的分流规则继续保留。

保留原ProtoBuf实现和业务过滤逻辑，增加空/异常响应及缺少data时的保护，解析失败保持原响应，所有路径只结束一次。帖子页按cmd参数区分302001和309751，避免查询参数其他位置出现相同数字时选错解析器。视频帖过滤参数读取补充布尔值规范化，兼容对象参数、JSON字符串及原key=value参数形式。

“过滤推荐页视频帖”使用独立switch，默认true，沿用用户截图。关闭后保留普通视频帖，原直播及广告过滤和页面精简继续生效。未额外引入原配置中没有匹配入口的frs/threadlist规则。

已通过53次ProtoBuf运行，覆盖与原脚本正常输入结果对照、推荐视频过滤开关、帖内两类cmd、错误响应、缺失data及未知字段保留，并通过原生JQ样例、幂等性、数值类型、URL匹配和局域网下载一致性检查。真实手机广告效果尚未验证。手机首次下载或刷新脚本需访问 `http://192.168.3.35:18765/Tieba.js`。
