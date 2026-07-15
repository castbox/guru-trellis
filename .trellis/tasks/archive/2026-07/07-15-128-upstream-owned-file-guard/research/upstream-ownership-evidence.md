# Upstream ownership 规划证据

## 官方 Trellis 文档

- https://docs.trytrellis.app/index.md
- https://docs.trytrellis.app/advanced/custom-workflow.md
- https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md
- https://docs.trytrellis.app/advanced/configuration.md
- https://docs.trytrellis.app/start/everyday-use.md

结论：`.trellis/workflow.md` 是 AI phase/routing 控制面；`trellis update` 使用 `.trellis/.template-hashes.json` 识别 generated template 与用户修改，并通过 overwrite、keep、`.new` 处理冲突；spec marketplace 不承载 platform entry 或 task runtime state。

## Issue 链

- #127：最终架构与五个子 issue 顺序。
- #128：本 task，只建立 inventory/validator，不迁移行为。
- #112：Intake `guru-*` owners 与 task workspace integration。
- #119：Finish `guru-*` owners 与 explicit finish integration。
- #129：`guru-approve-task-plan`。
- #130：`guru-check-task`。
- #131：`guru-review-branch`。
- #132：thin routing 集成与 43 个 legacy overlay 删除。

## Current generated files

环境：`trellis 0.6.5`。

命令：

```bash
trellis init -y -u ownership-audit --claude --codex --cursor
```

结果：43 个 canonical overlay 目标中，37 个由 clean init 生成；以下 6 个路径未由当前 `0.6.5` clean init 生成：

- `.codex/prompts/trellis-continue.md`
- `.codex/prompts/trellis-finish-work.md`
- `.codex/prompts/trellis-start.md`
- `.codex/skills/trellis-continue/SKILL.md`
- `.codex/skills/trellis-finish-work/SKILL.md`
- `.codex/skills/trellis-start/SKILL.md`

这 6 个路径属于历史 Codex entry namespace。Inventory 必须把 `generated_in_clean_init=false` 作为事实记录，不能把它们描述成当前 init 产物。

## Installer facts

- `apply_guru_team_trellis_preset.py::looks_like_trellis_generated_entry()` 使用 path/content signals 识别 upstream-generated entry。
- `copy_overlay()` 对识别出的 entry 直接替换；未知本地改动写 `.new`。
- `MANAGED_ASSET_PATHS` 全部映射到 `.trellis/guru-team/**`。
- Skill package canonical root 是 `trellis/skills/guru-team/**`，active ids 当前为 `guru-sync-base` 与 `guru-create-task-commit`。
- `trellis/guru-team-extension.json.public_api.managed_paths` 同时声明 Guru namespace 与 legacy upstream namespace。
- `check-dogfood-overlay-drift.sh` 当前只比较 canonical/dogfood bytes。
- `verify-throwaway-install.sh` 当前覆盖 initial apply、workflow preview/switch、`trellis update --force`、preset reapply、dogfood drift 与 zero-sidecar scan。

## Base identity

- Base branch：`main`
- Base commit：`291b57b6c02872320a4dce0626a2f718399b8f56`
- Overlay count：`43`
- Workflow 与 overlay payload 在 #128 中属于 immutable non-regression surface。
