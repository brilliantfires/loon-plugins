# 高德地图 Loon 本地版

本地插件：[Amap.lpx](./Amap.lpx)

插件显示名为“高德地图”。按截图补全来源信息，并按你提供的规则整理，完全重复的条目已去重。

整理结果：

- MitM 主机：6 个
- 有效 Rewrite：22 条
- 覆盖范围：开屏广告、首页推荐、搜索推荐、打车广告、地点推荐与广告，以及“我的”页面精简

有两个规则使用远程 jq 脚本：

- `https://kelee.one/Resource/JQLang/Amap/updatable.jq`
- `https://kelee.one/Resource/JQLang/Amap/search_poi_detail.jq`

当前环境直接请求这两个脚本返回 HTTP 403，可能是 Cloudflare 防护；插件保留了你提供的原地址，尚未完成 Loon 设备端执行验证。

当前文件地址：

```text
http://192.168.3.35:18772/Amap.lpx
```

手机与 Mac 需要在同一 Wi-Fi。若 IP 变化，双击 `serve-local.command`，使用它打印的新地址。
