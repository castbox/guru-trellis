# 当前 pack 用法

这是 #154 隔离验证 fixture 的当前行为说明，不是规划或验收结果。

从 fixture 根目录执行：

```bash
python3 sandbox/pack.py
python3 sandbox/pack.py --output artifacts
python3 sandbox/pack.py --help
```

不传 `--output` 时，命令在当前工作目录的 `dist` 目录中创建 `package.txt`。显式传入 `--output DIR` 时，命令使用该目录。构建成功返回 0。

目标已存在时，命令向 stderr 报告原因并返回 2。命令不覆盖已有目标或其中内容。

`--help` 展示 `--output DIR` 的输出目录用途和实际默认值 `dist`。帮助路径不执行构建，不创建目录或文件。

当前没有 `--dry-run`。预演能力仍由后续 D2 承担。
