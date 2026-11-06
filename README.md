# Loon 去广告插件

本地维护的 Loon 插件集合。插件显示名统一使用应用名称，功能说明放在描述中。

## 只去广告的精简版

新增两套自包含插件，均无 JS 和外部脚本依赖：

| 版本 | 导入地址 | 默认设置 |
| --- | --- | --- |
| 仅去开屏 | https://brilliantfires.github.io/loon-plugins/lite/Splash-Only.lpx | 15 个 App，豆瓣以外默认开启 |
| App 内去广告 | https://brilliantfires.github.io/loon-plugins/lite/InApp-Ads.lpx | 24 个 App 独立开关，默认全部关闭 |

请先停用对应旧插件，避免叠加。精简版缩小了广告覆盖范围，尚未做手机能耗实测；App 开关不动态撤销静态 MitM 域名。不使用内部版时请停用整个插件。

[安装与覆盖说明](lite/README.md) · [逐 App 审计](lite/AUDIT.md)

## 导入

在 Loon 的插件导入文本框中粘贴下面对应应用的地址，不需要添加 `loon://` 前缀。

| 应用 | 导入地址 |
| --- | --- |
| 12306 | `https://brilliantfires.github.io/loon-plugins/plugins/12306.lpx` |
| 百度网盘 | `https://brilliantfires.github.io/loon-plugins/plugins/BaiduNetdisk.lpx` |
| 哔哩哔哩 | `https://brilliantfires.github.io/loon-plugins/plugins/Bilibili.lpx` |
| 菜鸟 | `https://brilliantfires.github.io/loon-plugins/plugins/Cainiao.lpx` |
| 酷安 | `https://brilliantfires.github.io/loon-plugins/plugins/Coolapk.lpx` |
| 豆瓣 | `https://brilliantfires.github.io/loon-plugins/plugins/Douban.lpx` |
| 闲鱼 | `https://brilliantfires.github.io/loon-plugins/plugins/Goofish.lpx` |
| 京东 | `https://brilliantfires.github.io/loon-plugins/plugins/JD.lpx` |
| 瑞幸咖啡 | `https://brilliantfires.github.io/loon-plugins/plugins/LuckinCoffee.lpx` |
| 麦当劳 | `https://brilliantfires.github.io/loon-plugins/plugins/McDonalds.lpx` |
| 网易云音乐 | `https://brilliantfires.github.io/loon-plugins/plugins/NeteaseCloudMusic.lpx` |
| 顺丰速运 | `https://brilliantfires.github.io/loon-plugins/plugins/SFExpress.lpx` |
| 淘宝 | `https://brilliantfires.github.io/loon-plugins/plugins/Taobao.lpx` |
| 淘票票 | `https://brilliantfires.github.io/loon-plugins/plugins/Taopiaopiao.lpx` |
| 百度贴吧 | `https://brilliantfires.github.io/loon-plugins/plugins/Tieba.lpx` |
| 微信 | `https://brilliantfires.github.io/loon-plugins/plugins/WeChat.lpx` |
| 微博 | `https://brilliantfires.github.io/loon-plugins/plugins/Weibo.lpx` |
| 小红书 | `https://brilliantfires.github.io/loon-plugins/plugins/Xiaohongshu.lpx` |
| 小象超市 | `https://brilliantfires.github.io/loon-plugins/plugins/Xiaoxiang.lpx` |
| YouTube | `https://brilliantfires.github.io/loon-plugins/plugins/YouTube.lpx` |
| 知乎 | `https://brilliantfires.github.io/loon-plugins/plugins/Zhihu.lpx` |
| 转转 | `https://brilliantfires.github.io/loon-plugins/plugins/Zhuanzhuan.lpx` |
| 高德地图 | `https://brilliantfires.github.io/loon-plugins/plugins/Amap.lpx` |
| 滴滴 | `https://brilliantfires.github.io/loon-plugins/plugins/Didi.lpx` |
| 得物 | `https://brilliantfires.github.io/loon-plugins/plugins/Dewu.lpx` |
| 京东外卖 | `https://brilliantfires.github.io/loon-plugins/plugins/JD-Takeout.lpx` |
| 拼多多 | `https://brilliantfires.github.io/loon-plugins/plugins/Pinduoduo.lpx` |

GitHub Raw 使用相同路径，例如：

```text
https://raw.githubusercontent.com/brilliantfires/loon-plugins/main/plugins/12306.lpx
```

如果 Raw 地址访问不稳定，可改用 jsDelivr 的固定分支地址：

```text
https://cdn.jsdelivr.net/gh/brilliantfires/loon-plugins@main/plugins/12306.lpx
```

## 使用要求

- Loon 版本不低于 `3.5.1(998)`。
- 安装并信任 Loon 的 HTTPS 证书。
- 开启 MITM 和 HTTPS 解密；YouTube 还需要 HTTP/2 兼容与 QUIC 回退设置。
- 合并后的插件与旧版不能同时启用，否则同一接口可能被重复改写。
- 部分规则仍在等待真机验证，详见 [审计报告](docs/AUDIT.md)。

## 更新流程

最终导入文件位于 `plugins/`，公共地址使用已构建的 GitHub Pages。文件路径不发生变化时，推送更新后无需重新修改导入链接。

直接修改 `plugins/` 下的插件后推送即可：

```bash
cd /Users/Mac/工作区/CodeTemp/Agent/None/loon-plugins
git add -A
git commit -m "Update Loon plugins"
git push
```

需要注意两点：

- 插件通过 GitHub Pages 远程加载 `scripts/` 下的脚本和 jq 文件，修改这些文件必须一并提交，否则手机端会取到旧版本或 404。
- 插件名称必须与 `catalog.json` 中的应用名一致，这是之前出图与导入列表的约定。

`main` 地址用于持续更新。需要固定版本时，可将链接中的 `main` 换成对应提交哈希；升级时再修改链接。

## 目录

- `plugins/`：可直接导入的最终插件，共 27 个
- `lite/`：零 JS 的精简版，`Splash-Only.lpx` 与 `InApp-Ads.lpx` 两份
- `scripts/`：插件远程加载的固定脚本、jq 资源和所需许可证
- `docs/AUDIT.md`：逐项审计、合并结果和待验证事项
- `docs/apps/`：整理前各应用的说明文件与维护记录
- `catalog.json`：机器可读的插件清单，`source` 字段记录规则来源
- `NOTICE.md`：第三方作者与来源说明
