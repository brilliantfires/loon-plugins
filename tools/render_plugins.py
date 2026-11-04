#!/usr/bin/env python3
"""Render the normalized public Loon plugin catalog from the archived sources."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources" / "original"
PLUGINS = ROOT / "plugins"
REPO_RAW = "https://raw.githubusercontent.com/brilliantfires/loon-plugins/main"
LOCAL_SCRIPT_PREFIX = "http://192.168.3.35:18765/"

ICONS = {
    "12306": "12306.png",
    "BaiduNetdisk": "BaiduNetDisk.png",
    "Bilibili": "Bilibili.png",
    "Cainiao": "Cainiao.png",
    "Coolapk": "CoolApk.png",
    "Douban": "DouBan.png",
    "Goofish": "FleaMarket.png",
    "JD": "JD.png",
    "LuckinCoffee": "LuckinCoffee.png",
    "NeteaseCloudMusic": "NeteaseCloudMusic.png",
    "SFExpress": "SF-Express.png",
    "Taobao": "Taobao.png",
    "Taopiaopiao": "Taopiaopiao.png",
    "Tieba": "Tieba.png",
    "WeChat": "Weixin.png",
    "Weibo": "Weibo.png",
    "Xiaohongshu": "RedPaper.png",
    "Xiaoxiang": "iMaiCai.png",
    "YouTube": "YouTube.png",
    "Zhihu": "Zhihu.png",
    "Zhuanzhuan": "ZhuanZhuan.png",
    "Amap": "Amap.png",
    "Didi": "DiDi.png",
    "Dewu": "Dewu.png",
    "JD-Takeout": "JDWaimai.png",
    "Pinduoduo": "PinDuoDuo.png",
}

PLUGIN_DEFS = [
    {
        "id": "12306",
        "name": "12306",
        "desc": "过滤开屏广告和应用内推广入口；应用内推广过滤可独立关闭。",
        "source": "loon-zhihu/12306-Reject-JSON-Test.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "本地整理：Codex",
    },
    {
        "id": "BaiduNetdisk",
        "name": "百度网盘",
        "desc": "过滤广告、活动和推荐接口，并精简小说、短剧、打印及求职入口。",
        "source": "loon-zhihu/BaiduNetdisk.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：可莉；本地整理：Codex",
    },
    {
        "id": "Bilibili",
        "name": "哔哩哔哩",
        "desc": "默认仅清理明确广告。评论、动态、视频页扩展、互动弹幕、空降助手、播放增强等高风险功能均由独立开关控制并默认关闭。",
        "source": "Bilibili-Loon/Bilibili-Ads-Full.lpx",
        "homepage": "https://github.com/kokoryh/Sparkle",
        "author": "原脚本：kokoryh；完整开关封装：Codex",
        "open_url": "https://apps.apple.com/app/id736536022",
    },
    {
        "id": "Cainiao",
        "name": "菜鸟",
        "desc": "过滤菜鸟广告并提供每日现金任务隐藏开关；每日任务会清空任务接口，异常时可单独关闭。",
        "source": "Cainiao-Loon/Cainiao-Ads.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：@小白脸、可莉；本地整合：Codex",
    },
    {
        "id": "Coolapk",
        "name": "酷安",
        "desc": "过滤开屏、信息流、评论与热词推广，并缩短开屏等待时间；当前仍属待实机验证版本。",
        "source": "loon-zhihu/Coolapk-Splash-Timeout-Test.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：RuCu6、可莉；本地修改：Codex",
    },
    {
        "id": "Douban",
        "name": "豆瓣",
        "desc": "移除开屏、信息流、首页横幅和搜索填充词，并关闭开屏 SDK 的三个开关字段。仅适用于 IPA 签名版豆瓣。",
        "source": "Douban-Loon/Douban.lpx",
        "homepage": "https://getupnote.com/share/notes/zSn1ShBmzNYISKcTgjXE5oHMrNf2/34bf3aad-7872-497d-b239-198e27e8c84c",
        "author": "原规则：可莉；本地整合：Codex",
    },
    {
        "id": "Goofish",
        "name": "闲鱼",
        "desc": "过滤开屏、推荐、搜索和页面推广。场景恢复候选拦截尚未实机验证，默认关闭。",
        "source": "loon-zhihu/Goofish-Integrated-Test.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：可莉；本地整合：Codex",
    },
    {
        "id": "JD",
        "name": "京东",
        "desc": "过滤开屏、首页、个人页、订单与物流页面推广，并处理京东页面配置。",
        "source": "loon-zhihu/JD-Integrated.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原脚本：RuCu6；本地整合：Codex",
    },
    {
        "id": "LuckinCoffee",
        "name": "瑞幸咖啡",
        "desc": "过滤开屏、弹窗、活动及推广接口。",
        "source": "loon-zhihu/LuckinCoffee.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：Sliverkiss；本地整理：Codex",
    },
    {
        "id": "McDonalds",
        "name": "麦当劳",
        "desc": "通过将开屏投放窗口设为过期并清理推广弹窗来去广告；两个功能可独立关闭。",
        "source": "loon-zhihu/McDonalds-Ads-v2-Test.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "本地整理：Codex",
    },
    {
        "id": "NeteaseCloudMusic",
        "name": "网易云音乐",
        "desc": "过滤首页、发现页、评论与个人页推广；提供首页和底栏等独立开关。",
        "source": "loon-zhihu/NeteaseCloudMusic.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则与脚本：RuCu6、Keywos；本地整理：Codex",
    },
    {
        "id": "SFExpress",
        "name": "顺丰速运",
        "desc": "过滤广告接口、积分商城推荐和首页指定推广模块。",
        "source": "loon-zhihu/SFExpress.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：可莉；本地整理：Codex",
    },
    {
        "id": "Taobao",
        "name": "淘宝",
        "desc": "过滤开屏图片、视频和活动资源，并处理原规则中的相关接口。",
        "source": "loon-zhihu/Taobao.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则与脚本：RuCu6；本地整理：Codex",
    },
    {
        "id": "Taopiaopiao",
        "name": "淘票票",
        "desc": "过滤广告弹窗、悬浮推广、搜索填充词、横幅和猜你喜欢。",
        "source": "loon-zhihu/Taopiaopiao.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：可莉；本地整理：Codex",
    },
    {
        "id": "Tieba",
        "name": "百度贴吧",
        "desc": "过滤开屏、信息流和帖内推广并精简页面；推荐页视频帖过滤可单独关闭。",
        "source": "loon-zhihu/Tieba.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则与脚本：可莉、app2smile；本地整理：Codex",
    },
    {
        "id": "WeChat",
        "name": "微信",
        "desc": "合并微信公众号与常用微信小程序的广告、推荐和推广过滤。",
        "source": "WeChat-MiniPrograms-Loon/WeChat-MiniPrograms.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：可莉、RuCu6；本地整合：Codex",
    },
    {
        "id": "Weibo",
        "name": "微博",
        "desc": "过滤开屏、信息流、评论、搜索、个人页与视频推广；提供多组独立开关。",
        "source": "loon-zhihu/Weibo.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则与脚本：RuCu6、zmqcherish；本地整理：Codex",
    },
    {
        "id": "Xiaohongshu",
        "name": "小红书",
        "desc": "过滤开屏、信息流和搜索推广，并处理图片、实况照片和视频保存；功能可独立控制。",
        "source": "loon-zhihu/Xiaohongshu.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则与脚本：RuCu6、fmz200；本地整理：Codex",
    },
    {
        "id": "Xiaoxiang",
        "name": "小象超市",
        "desc": "过滤开屏、悬浮推广、横幅、商品推荐和广告配置字段。",
        "source": "loon-zhihu/Xiaoxiang.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：可莉；本地整理：Codex",
    },
    {
        "id": "YouTube",
        "name": "YouTube",
        "desc": "过滤视频、信息流、搜索和 Shorts 广告。需要启用 MitM over HTTP/2 与 QUIC 回退保护。",
        "source": "loon-zhihu/YouTube.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则与脚本：Maasea、VirgilClyne、Choler、DivineEngine、app2smile；本地整理：Codex",
        "system": "iOS,iPadOS,macOS",
    },
    {
        "id": "Zhihu",
        "name": "知乎",
        "desc": "过滤开屏、回答广告、回答流广告、首页与搜索浮层推广。",
        "source": "loon-zhihu/Zhihu-Splash.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：可莉；本地整理：Codex",
    },
    {
        "id": "Zhuanzhuan",
        "name": "转转",
        "desc": "过滤开屏、推广弹窗、信息流和商品推荐，并精简“我的”页面。",
        "source": "loon-zhihu/Zhuanzhuan.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：可莉；本地整理：Codex",
    },
    {
        "id": "Amap",
        "name": "高德地图",
        "desc": "移除开屏、首页推荐、搜索推荐、打车广告、地点推荐及广告，并精简“我的”页面。",
        "source": "Amap-Loon/Amap.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：可莉；本地整理：Codex",
    },
    {
        "id": "Didi",
        "name": "滴滴",
        "desc": "移除开屏、弹窗、横幅推广，处理首页与个人页配置并精简页面。",
        "source": "Didi-Loon/Didi.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：可莉；本地整理：Codex",
    },
    {
        "id": "Dewu",
        "name": "得物",
        "desc": "移除开屏、弹窗、搜索词、热搜、推荐信息流，并精简消息与“我的”页面。",
        "source": "Dewu-Loon/Dewu.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：可莉；本地整理：Codex",
    },
    {
        "id": "JD-Takeout",
        "name": "京东外卖",
        "desc": "移除首页、点评、购物车及“我的”页面推荐，精简搜索发现和搜索榜单。",
        "source": "JD-Takeout-Loon/JD-Takeout.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：可莉；本地整理：Codex",
    },
    {
        "id": "Pinduoduo",
        "name": "拼多多",
        "desc": "移除开屏、底栏多多视频、会场入口、聊天推荐及推广，并精简首页和个人中心。",
        "source": "Pinduoduo-Loon/Pinduoduo.lpx",
        "homepage": "https://hub.kelee.one",
        "author": "原规则：ZenmoFeiShi、可莉；本地整理：Codex",
    },
]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise ValueError(f"Missing expected text for {label}: {old[:100]}")
    return text.replace(old, new, 1)


def strip_header(text: str) -> str:
    lines = text.splitlines()
    index = 0
    while index < len(lines) and lines[index].startswith("#!"):
        index += 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    return "\n".join(lines[index:]).rstrip() + "\n"


def add_argument(body: str, argument: str) -> str:
    section = f"[Argument]\n{argument.strip()}\n\n"
    if "[Rule]" in body:
        return body.replace("[Rule]\n", section + "[Rule]\n", 1)
    return body.replace("[Rewrite]\n", section + "[Rewrite]\n", 1)


def render_header(item: dict) -> str:
    lines = [
        f"#!name={item['name']}",
        f"#!desc={item['desc']}",
        f"#!homepage={item['homepage']}",
        "#!tag=去广告",
        f"#!system={item.get('system', 'iOS,iPadOS')}",
        "#!system_version=15",
        "#!loon_version=3.5.1(998)",
    ]
    icon = ICONS.get(item["id"])
    if icon:
        lines.append(
            "#!icon=https://raw.githubusercontent.com/luestr/IconResource/"
            f"main/App_icon/120px/{icon}"
        )
    if item.get("open_url"):
        lines.append(f"#!openUrl={item['open_url']}")
    lines.extend(
        [
            f"#!author={item['author']}",
            "#!date=2026-11-04",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def apply_special_transforms(plugin_id: str, body: str) -> str:
    if plugin_id == "12306":
        body = add_argument(
            body,
            "appPromotions = switch,true,tag=应用内推广过滤,"
            "desc=关闭后仅过滤开屏广告，避免推广入口处理影响其他页面。",
        )
        body = replace_once(
            body,
            "request if ${url} ~= /^https:\\/\\/mobile\\.12306\\.cn\\/otsmobile\\/app\\/mgs\\//",
            "request if ${appPromotions} == true && ${url} ~= /^https:\\/\\/mobile\\.12306\\.cn\\/otsmobile\\/app\\/mgs\\//",
            "12306 app promotion switch",
        )

    if plugin_id == "Cainiao":
        body = add_argument(
            body,
            "dailyTasks = switch,true,tag=隐藏每日现金任务,"
            "desc=会清空每日任务接口的 data；页面异常或需要查看任务时可关闭。",
        )
        daily_rule = (
            "response if ${dailyTasks} == true && ${url} ~= "
            "/^https:\\/\\/guide-acs\\.m\\.taobao\\.com\\/gw\\/mtop\\.cainiao\\."
            "pubaccount\\.daily\\.task\\.activity\\.task\\.query\\/2\\.0\\/?(?:\\?|$)/i "
            'then response.json.jq(".data={}")\n\n'
        )
        body = replace_once(body, "[MitM]\n", daily_rule + "[MitM]\n", "Cainiao daily rule")
        body = replace_once(
            body,
            "hostname = netflow-mtop.cainiao.com, nbcps-mtop.cainiao.com, cn-acs.m.cainiao.com, e2e-mtop.cainiao.com, longquan-mtop.cainiao.com",
            "hostname = netflow-mtop.cainiao.com, nbcps-mtop.cainiao.com, cn-acs.m.cainiao.com, e2e-mtop.cainiao.com, longquan-mtop.cainiao.com, guide-acs.m.taobao.com",
            "Cainiao daily host",
        )

    if plugin_id == "Douban":
        douban_switch_rule = (
            "response if ${url} ~= /^https:\\/\\/frodo\\.douban\\.com\\/api\\/v2\\/"
            "feature_switch(?:\\?|$)/i then response.json.jq("
            '".splash_sdk_info=[] | .enable_splash_client_bid=false | '
            '.splash_client_bid_use_preload=false")\n\n'
        )
        body = replace_once(
            body,
            "[MitM]\n",
            douban_switch_rule + "[MitM]\n",
            "Douban splash SDK switch",
        )

    if plugin_id == "Goofish":
        body = add_argument(
            body,
            "sceneRestore = switch,false,tag=场景恢复候选拦截,"
            "desc=尚未实机验证，默认关闭；启用后会作用于该接口的全部场景。",
        )
        body = replace_once(
            body,
            "request if ${url} ~= /^https:\\/\\/acs\\.m\\.goofish\\.com\\/gw\\/mtop\\.idle\\.idleadv\\.scene\\.restore\\//",
            "request if ${sceneRestore} == true && ${url} ~= /^https:\\/\\/acs\\.m\\.goofish\\.com\\/gw\\/mtop\\.idle\\.idleadv\\.scene\\.restore\\//",
            "Goofish scene restore switch",
        )

    if plugin_id == "McDonalds":
        body = add_argument(
            body,
            "splashConfig = switch,true,tag=开屏投放过期处理\n"
            "popupClean = switch,true,tag=推广弹窗过滤",
        )
        body = replace_once(
            body,
            "response if ${url} ~= /^https:\\/\\/api\\.mcd\\.cn\\/bff\\/portal\\/home\\/splash",
            "response if ${splashConfig} == true && ${url} ~= /^https:\\/\\/api\\.mcd\\.cn\\/bff\\/portal\\/home\\/splash",
            "McDonalds splash switch",
        )
        body = replace_once(
            body,
            "response if ${url} ~= /^https:\\/\\/api\\.mcd\\.cn\\/bff\\/portal\\/richpop\\/v2",
            "response if ${popupClean} == true && ${url} ~= /^https:\\/\\/api\\.mcd\\.cn\\/bff\\/portal\\/richpop\\/v2",
            "McDonalds popup switch",
        )

    if plugin_id == "WeChat":
        body = replace_once(
            body,
            "DOMAIN,wxsnsdy.wxs.qq.com,REJECT\n"
            "DOMAIN,wxsmsdy.video.qq.com,REJECT\n"
            "DOMAIN,wxsnsdythumb.wxs.qq.com,REJECT\n",
            "DOMAIN,wxsmsdy.video.qq.com,REJECT\n",
            "WeChat redundant wxs domain rules",
        )
        body = replace_once(
            body,
            "DOMAIN,e.jparking.cn,REJECT\n",
            "DOMAIN,e.jparking.cn,REJECT\nDOMAIN-SUFFIX,wxs.qq.com,REJECT\n",
            "WeChat official account domain",
        )
        official_rules = (
            "request if ${url} ~= /^https:\\/\\/mp\\.weixin\\.qq\\.com\\/mp\\/"
            "(cps_product_info|getappmsgad|jsmonitor|masonryfeed|relatedarticle)\\?/i "
            "then reject_dict(200)\n"
            "request if ${url} ~= /^https:\\/\\/mp\\.weixin\\.qq\\.com\\/mp\\/"
            "relatedsearchword/i then reject_dict(200)\n\n"
        )
        body = replace_once(body, "[MitM]\n", official_rules + "[MitM]\n", "WeChat official rules")
        body = replace_once(
            body,
            "hostname = 3pp.starbucks.com.cn,",
            "hostname = mp.weixin.qq.com, 3pp.starbucks.com.cn,",
            "WeChat official host",
        )

    return body


def main() -> None:
    PLUGINS.mkdir(parents=True, exist_ok=True)
    catalog = []
    for item in PLUGIN_DEFS:
        source = SOURCES / item["source"]
        body = strip_header(source.read_text(encoding="utf-8"))
        body = body.replace(LOCAL_SCRIPT_PREFIX, f"{REPO_RAW}/scripts/")
        body = body.replace("[Mitm]", "[MitM]")
        body = apply_special_transforms(item["id"], body)
        text = render_header(item) + body
        target = PLUGINS / f"{item['id']}.lpx"
        target.write_text(text, encoding="utf-8")
        catalog.append(
            {
                "id": item["id"],
                "name": item["name"],
                "desc": item["desc"],
                "plugin_url": f"{REPO_RAW}/plugins/{target.name}",
                "source": f"sources/original/{item['source']}",
            }
        )
    (ROOT / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Rendered {len(catalog)} plugins")


if __name__ == "__main__":
    main()
