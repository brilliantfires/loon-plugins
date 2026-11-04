# 原始来源归档

`original/` 保存迁移前的本地文件，内容基本保持原样，便于比较、回滚和追溯作者信息。

其中的部分旧文件仍包含已失效的局域网脚本地址或旧版 `[Mitm]` 写法。它们不参与最终导入；可导入版本统一位于仓库根目录的 `plugins/`。

如只修改归档来源，请运行：

```bash
python3 tools/render_plugins.py
./tools/validate.sh
```

重新生成最终插件。
