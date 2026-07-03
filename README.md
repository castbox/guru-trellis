# Guru Trellis

Guru Team Trellis 的公开 marketplace 与 preset 资产仓库。

本仓库是可复用 `guru-team` Trellis workflow 的 canonical 来源，用于让团队成员在业务仓库中开箱即用地安装统一的 Trellis 工作流、companion scripts 和多平台入口 overlay。

## 仓库内容

- `trellis/index.json`：Trellis marketplace 入口，提供 `guru-team` workflow。
- `trellis/workflows/guru-team/`：workflow 主合同、配置模板、schema 和 companion scripts。
- `trellis/presets/guru-team/`：把 companion scripts 和平台入口 overlay 安装到目标业务仓库的 preset installer。

## 新项目安装

在目标业务仓库中初始化 Trellis，并直接选择 Guru Team workflow：

```bash
trellis init -u <name> --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis
```

然后安装 Guru Team companion assets：

```bash
git clone https://github.com/castbox/guru-trellis.git /path/to/guru-trellis
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project
```

## 已有 Trellis 项目切换

先生成预览，不直接覆盖 active workflow：

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis \
  --template guru-team \
  --create-new
```

人工确认 `.trellis/workflow.md.new` 后，再切换 workflow 并重新应用 preset：

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis \
  --template guru-team
git clone https://github.com/castbox/guru-trellis.git /path/to/guru-trellis
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project
```

## 升级方式

Trellis 官方 CLI、项目内 Trellis 模板、Guru Team workflow/preset 是三层不同来源，推荐分开升级：

```bash
trellis upgrade
trellis update --dry-run
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis \
  --template guru-team \
  --create-new
```

确认 `.trellis/workflow.md.new` 后再切换 workflow，并重新运行 preset installer。

preset installer 是幂等的：

- 内容相同的文件会跳过。
- 缺失文件会安装。
- 已识别的上游 Trellis 生成入口会替换为 Guru Team overlay。
- 未识别的本地改动会保留，并生成 `.new` 文件供人工对比。

## 用户主流程

安装后，用户仍然只需要记住三个主入口：

- `trellis-start`
- `trellis-continue`
- `trellis-finish-work`

`review-branch`、`check-review-gate`、`publish-pr` 是 workflow 内部 companion script，不是需要用户日常手动记忆的新主流程。

## 维护原则

- 不修改 Trellis npm 全局包、`node_modules` 或上游 Trellis 源码。
- 不把业务仓库的私有规则写入通用 workflow。
- 长期规则维护在本仓库的 marketplace workflow、preset、companion scripts 和 overlay 中。
- 目标业务仓库中的 generated copy 只是安装结果，不作为长期维护源。
