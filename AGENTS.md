# 维护指南（给后续 agent）

本仓库是本地维护的 Loon 去广告插件集合，通过 GitHub Pages 分发。这份文件记录**改动的固定流程**和**已经踩过的坑**，动手前请先读完。

## 一、先搞清楚谁在用

| 使用方 | 导入什么 | 说明 |
| --- | --- | --- |
| 手机（唯一真实用户） | 只导入 `lite/Splash-Only.lpx` 与 `lite/InApp-Ads.lpx` | 其它 `plugins/*.lpx` 不参与日常使用 |
| 已停用 | `lite/X-Ads-Test.lpx` | 无 Rewrite、Script 或 MitM 的撤回提示；X 原生 App 无法可靠通过 Loon 安全过滤 |
| 仓库读者 | 全部文件 | 完整版 27 个插件 + `scripts/` 远程脚本 |

推论：

- **日常规则改动默认落在 `lite/` 两份聚合插件里**；X 这类证书固定或响应结构高风险的 App 不加入 MITM 聚合，只在 `plugins/` 里改，用户手机看不到效果。
- `plugins/` 与多数 `scripts/` 是历史资产，不要为了“保持一致”顺手大改；确需同步时说明理由。
- `scripts/*.js|*.jq` 是**运行时从 Pages 拉取**的资源，不是本地依赖；删了会导致对应完整版插件失效。精简版当前只引用 `NeteaseCloudMusicAdOnly.js`。

## 二、目录

```
lite/          两份日常插件、一个 X 停用提示文件及其文档、清单、校验和
plugins/       27 个完整版插件（部分依赖 scripts/）
scripts/       远程脚本资源；精简版只引用网易云活动广告窄脚本
docs/          审计文档与历史 App 说明
catalog.json   完整版索引
AGENTS.md      本文件
```

`lite/` 内：`manifest.json`（逐条规则来源）、`inventory.json`、`verification.json`、`SHA256SUMS`、`README.md`、`AUDIT.md`。

## 三、改一份 `.lpx` 的固定流程

按顺序做，**不要跳步**：

1. **改规则**（`lite/Splash-Only.lpx` 或 `lite/InApp-Ads.lpx`）。
2. **同步 `#!date`，格式 `YYYY-MM-DD HH:MM`**。Loon 插件详情页原样显示该字段（官方文档：“该值会按原样显示”，不做解析），带时分才能区分同一天内的多次改动；只写日期会让用户以为没更新（真实发生过）。
3. **同步 `lite/manifest.json`**：新增/修改的规则要有一条对应记录（`mode`/`app`/`hosts`/`pattern`/`action`/`phase`/`note`/`source`）。域名规则用 `mode: "rule"`、`phase: "dns"`。
4. **重新生成校验和**（`lite/SHA256SUMS` 覆盖 10 个文件）：
   ```bash
   cd lite && shasum -a 256 Splash-Only.lpx InApp-Ads.lpx X-Ads-Test.lpx README.md AUDIT.md \
     manifest.json inventory.json verification.json NOTICE.md LICENSE-Bilibili-GPL-3.0.txt > SHA256SUMS
   shasum -a 256 -c SHA256SUMS | grep -c ': OK'   # 应为 10
   ```
5. **本地校验**（见第五节的脚本），确认开关无未定义、无重复规则、MitM 覆盖所有 URL 主机。
6. **若改动 `scripts/NeteaseCloudMusicAdOnly.js`**：运行 `node --check`，用用户抓包做加解密/保留内容回放，并更新 `manifest.json` 里的脚本 SHA-256。
7. **提交并推送**到 `main`。
8. **确认线上状态**。看一次即可，不要轮询（见第十三节）；线上还是旧版本属正常，不代表失败。

`lite/X-Ads-Test.lpx` 是已撤回实验的占位文件，必须保持零 Rewrite、零 Script、零 MitM。X 原生 iOS 客户端不适合由 Loon 过滤：启用 MITM 会破坏时间线加载，而关闭内部开关不会撤销静态 MitM。需要 X 去广告时只建议使用 Safari 网页版扩展，不能重新把 X 主机加入日常聚合插件。

## 四、GitHub Pages 有延迟，但只需要看一次

push 成功 ≠ 立刻生效，实测延迟 **1～3 分钟**，`raw.githubusercontent.com` 也可能返回旧内容。所以不要凭 push 输出就说“已上线”。但也**不要为了等构建反复轮询**——看一次，旧版本就如实说“已推送，构建中”。

单次检查：

```bash
cd lite && curl -sS -o /tmp/check.lpx \
  "https://brilliantfires.github.io/loon-plugins/lite/InApp-Ads.lpx?cb=$RANDOM"
grep -m1 '^#!date' /tmp/check.lpx
shasum -a 256 /tmp/check.lpx InApp-Ads.lpx | cut -c1-12
```

要点：

- 必须带 `?cb=<随机数>` 绕过 CDN 缓存。
- 用 **SHA-256 相等**判断，不要用文件大小或 `grep` 关键字（大小可能恰好相同，例如只改日期）。
- 同时确认 `#!date` 是预期值（含时分）。

## 五、本地校验脚本

仓库里没有 `tools/`（曾有一个依赖 `rg` 的脚本，本机没装 `rg` 跑不通，已删除）。用这段内联脚本代替：

```bash
cd lite && python3 - <<'PY'
import re, pathlib
for f in ['Splash-Only.lpx', 'InApp-Ads.lpx']:
    raw = pathlib.Path(f).read_text()
    t = raw.replace('\\/', '/').replace('\\.', '.')
    lines = t.splitlines()
    args = set(re.findall(r'^(\w+)\s*=', t.split('[Rewrite]')[0], re.M))
    used = set(re.findall(r'\$\{(\w+)\}', t)) - {'url'}
    mitm = set(x.strip() for x in re.search(r'hostname\s*=\s*(.*)', t).group(1).split(','))
    hosts = set(re.findall(r'https://([a-z0-9.*-]+)', t)) - {'github.com'}
    rew = [l for l in lines if l.startswith(('request if', 'response if'))]
    print(f, '| 复写', len(rew), '| 重复', len(rew) - len(set(rew)),
          '| 未定义开关', sorted(used - args) or '无',
          '| MitM 未覆盖', sorted(h for h in hosts if h not in mitm) or '无')
PY
```

## 六、Loon 语法与本仓库约定

```ini
[Argument]  app_X = switch,true,tag=显示名        # InApp 版默认 false
[Rule]      DOMAIN-SUFFIX,example.com,REJECT      # 域名层拒绝，不需要 MitM
[Rewrite]   request if ${app_X} == true && ${url} ~= /.../i then reject_dict(200)
            response if ... then response.json.jq(`...`)
[MitM]      hostname = a.com, b.com
```

约定：

- 可选 query 用 `(\?|$)`；`lite/` 内也有用 `(?:\?|$)` 的写法，同一文件内保持就近一致即可。
- 想排除“只在 query 里出现关键字”的误伤，用 `[^?]*` 限定路径部分。
- 正则写在 `.lpx` 里要转义 `/` 与 `.`（`https:\/\/api\.zhihu\.com`），改完用 Python 按同样规则还原测试。
- `[MitM]` 与 `[Rule]` 都是**静态**的，App 开关关掉也不会撤销；文档里必须写明这一点。
- 能用 `response.json.jq` 原生产生的，不要引脚本；`lite/` 默认保持零 JS。目前唯一例外是 `scripts/NeteaseCloudMusicAdOnly.js`：网易云两个活动接口的响应是 AES/gzip，普通 JQ 无法处理。不得借用该例外恢复完整版首页、评论、底栏和其他加解密入口。

## 七、正则踩过的坑（务必回看）

**路径分隔符不一定是你以为的那个。** 闲鱼开屏接口是：

```
/gw/mtop.taobao.idlecommerce.splash.ads/1.0/
```

第一版按 `/splash` 写（`[^?]*\/splash`），7 个用例挂了 4 个——因为 `idlecommerce` 与 `splash` 之间是**点号**，不是斜杠。修正为同时接受两种分隔：

```
[^?]*[\/.]splash[a-z0-9_.\/-]*(\?|$)
```

教训：写匹配规则前，先用真实抓包里的完整路径跑一遍回归，别照着函数名猜结构。

## 八、jq 的写法与测试

真实响应常常是**嵌套 JSON 字符串**（`{"banner": "{\"ads\":[...]}"}`），不能直接 `.banner.ads=[]`，要 `fromjson` → 改 → `tojson` 还原。

标准骨架（保留原文、失败不炸）：

```jq
if type=="object" then . as $original
| try ( ...改动... ) catch $original
else . end
```

只动目标字段时，进一步用局部兜底：

```jq
.banner |= (. as $b | try ((fromjson) | if (.ads|type)=="array" then .ads=[] else . end | tojson) catch $b)
```

注意 `try EXP catch .` 里的 `.` 是**错误信息**而不是原输入，会写出 `"Invalid numeric literal..."` 这种脏数据。必须像上面这样显式保存 `$b` / `$original`。

验证方式：用抓包里的真实 body 跑一遍，再补一组异常输入（非法 JSON、字段类型不符、字段缺失、空值、顶层是数组/字符串），全部要求**原样返回**。

## 九、改完要提醒用户的事

- `InApp-Ads` 的 App 开关**默认全部关闭**，新增规则必须让用户手动打开对应 App 的开关。
- 手机上需要**重新导入/更新插件**才会拿到新规则；Loon 不会自动同步。
- `[Rule]` 域名拦截会影响所有同类 App（例如 `tanx.com` 会作用到淘宝、闲鱼、优酷），要提前说清代价与回退方式。

## 十、抓包流程

需要定位未知广告时，**顺序不能错**：

1. Loon 里先开始抓包；
2. 再从后台杀掉目标 App；
3. 冷启动，等开屏/目标页面结束；
4. 停止并导出。

先杀进程再开抓包会漏掉启动早期的请求——曾因此误判为“接口不存在”。另外导出包里响应体可能是明文 JSON，也可能被压缩，先看头部字节再解。

## 十一、本机环境

- 没有 `rg`；用 `grep` 或 Python。
- `jq`、`python3`、`node`、`shasum` 可用；macOS 的 `sed -i` 需要跟空字符串：`sed -i '' 's/a/b/'`。
- 提交信息用中文说明“改了什么 + 依据什么”，一次提交只做一件事。

## 十二、验证边界

仓库文档里的“已验证”仅指离线校验与已保存响应的回放，**没有** iPhone 上的命中率、CPU 或能耗实测。写结论时不要夸大；基于推断的规则（例如按广告上报域名反推开屏链路）要在 `AUDIT.md` 里标明是推断，并写清需要什么证据才能确认。

## 十三、验证的分寸

本地验证只能证明**规则没写错**，不能证明“手机上广告没了”。把两者混为一谈，就会浪费大量时间。

**确实有用的部分**（都是真实拦下的错误）：

- 用抓包里的真实响应跑 jq，发现 `try EXP catch .` 会把错误信息写进 body；
- 用抓包里的真实 URL 跑正则，发现闲鱼 `idlecommerce.splash.ads` 是点号不是斜杠；
- 用抓包比对接口主机，发现菜鸟广告接口已从 `cn-acs.m.cainiao.com` 迁到 `netflow-mtop.cainiao.com`。

**没用的部分（不要做）**：

- 反复 `sleep` + `curl` + 哈希对比的轮询循环。构建要 1～3 分钟，等它没有意义；看一次，回答“已推送”即可。
- 为改日期、改注释、改文档、改文案跑任何测试。
- 把“本地通过”写成“已生效”。没有看到线上内容，就只能说“已推送”。
- 拿本地回放结果反驳用户真机上的反馈。真机为准。

**改动类型与验证要求**：

| 改动 | 要求 |
| --- | --- |
| 正则 / jq / 接口路径 | 用对应抓包样本跑一次，只为抓写法错误，不做第二轮 |
| `#!date`、注释、文档、README | 无 |
| 推送之后 | 最多一次 `curl` 看一眼，或直接交给用户手机上验证 |
| 不确定是否覆盖真机场景 | 说明边界，让用户实测，不要自己编造结论 |
