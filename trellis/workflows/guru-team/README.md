# Guru Team Trellis Workflow

本目录维护 Guru 团队可复用的 Trellis workflow。

这个 workflow 的 marketplace id 固定为通用的 `guru-team`。它承载 GitHub issue
intake、Git base branch/worktree preflight、中文 planning artifact、Issue Scope
Ledger、Branch Review Gate，以及 finish-work 成功后的自动 publish PR 规则。

## Marketplace 安装

```bash
trellis init -u <name> --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis
```

已有 Trellis 项目切换 active workflow：

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis \
  --template guru-team
```

只有在需要生成 `.trellis/workflow.md.new` 做人工 review、且不切换 active
workflow 时，才使用 `--create-new`。

## Companion Assets

Trellis workflow marketplace 只负责安装或切换 `.trellis/workflow.md`。
companion scripts、配置、schema 和团队自有入口 overlay 需要通过 preset installer
写入目标仓库：

```bash
git clone https://github.com/castbox/guru-trellis.git /path/to/guru-trellis
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project
```

installer 会写入 `.trellis/guru-team/`，并可安装 `.agents/skills`、
`.claude/commands`、`.cursor/commands` 下的 Guru Team overlay。它不会修改 Trellis
上游脚本、npm 全局包、`node_modules` 或 `.trellis/scripts/task.py`。

installer 幂等：同内容跳过，缺失文件写入，Guru-managed companion assets 会升级 active
文件并把旧版保存为 `.bak`，已有 `.trellis/guru-team/config.yml` 不覆盖，识别为上游
Trellis 生成入口时替换为 Guru Team overlay；未知本地改动写 `.new`，不静默覆盖。

`prepare-task.sh --json` 默认只执行 intake 和 preflight planning，不创建新的
worktree。只有在用户已经 review 计划中的 base branch 和 workspace path 后，才使用
`--create-worktree` 或 `--create-task`。

Branch Review Gate 与 publish helper 是内部子命令：

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
.trellis/guru-team/scripts/bash/check-review-gate.sh --json
.trellis/guru-team/scripts/bash/finish-work.sh --json
```

用户主流程仍然只有 `trellis-start`、`trellis-continue`、`trellis-finish-work`。

`review-branch.sh --pass` 必须带中文 `--summary` 和至少一条 `--evidence`，避免空白自证通过。
Phase 2 的官方 `trellis-check` sub-agent 负责 commit 前质量检查；Phase 3 Branch
Review Gate 可由 sub-agent 辅助审查，但最终门禁以 `review-gate.json` 为准。
