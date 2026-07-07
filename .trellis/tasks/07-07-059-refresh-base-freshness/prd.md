# #59 prepare-task 应在 planner 阶段刷新 base 分支远程状态

## Goal

修正 Guru Team `prepare-task` 的 Phase 0 handoff preflight：默认 planner-only 输出必须基于已刷新或已明确确认的远端 base 状态，不能在未刷新 `origin/<base>` 时把本地 remote-tracking 缓存报告为 `fresh: true`。

本任务关闭 [castbox/guru-trellis#59](https://github.com/castbox/guru-trellis/issues/59)。

## 背景与证据

- Issue #59 记录了 #55 intake 时的缺陷：planner-only `prepare-task.sh --json` 曾在 `fetch_performed: false` 时报告 `fresh: true`，但随后发现本地 `main` 落后 `origin/main` 7 个提交。
- 当前源码中 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 的 `cmd_prepare()` 在 `should_create_worktree=false` 时调用 `inspect_base_freshness()`；该函数只比较本地 base 与本地 `origin/<base>` 缓存。
- executor 路径已经通过 `ensure_base_freshness()` 执行 `git fetch` 并覆盖了工作区创建前刷新 base 的测试；缺口在 planner-only 路径。
- 本仓库存在 durable docs/spec SSOT：`.trellis/spec/workflow/*`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`trellis/workflows/guru-team/workflow.md`。本任务需要同步可复用 workflow/preset 文档与 dogfood 安装副本。
- Middle-platform Knowledge Gate 不适用：本任务修改 Trellis workflow companion scripts 与文档，不涉及 go-guru、proto-guru、ORM、Unity3D/Flutter Guru SDK 等中台框架。

## Requirements

- R1: 默认 planner-only `prepare-task.sh --json "<issue or request>"` 必须刷新或等价确认选中 base 的远端状态，再生成 `preflight.base_freshness`。
- R2: `base_freshness.remote_head` 必须来自刷新后的 `origin/<base>` 或明确标注无法确认；不得静默使用 stale remote-tracking ref 并报告 `fresh: true`。
- R3: 当本地 base 落后远端且可 fast-forward 时，planner-only 不应修改本地 base，但必须输出可审计状态，供 handoff review 判断；executor 路径仍负责安全 fast-forward 或 fail closed。
- R4: 当本地 base 与远端分叉或远端无法确认时，planner-only 应 fail closed 或输出明确阻塞状态；executor 路径不得从 stale/diverged base 创建 task branch。
- R5: 更新 workflow/README/schema 文案，明确只有已刷新或远端确认过的 freshness 才能作为 handoff 证据，`fetch_performed: false` 不应被展示为“fresh”证据。
- R6: 增加测试或可复现验证，覆盖 local base 落后 remote 的 planner-only 场景。
- R7: canonical 源头与 dogfood 安装副本必须同步：优先修改 `trellis/workflows/guru-team/`、`trellis/presets/guru-team/`，再同步 `.trellis/guru-team/` 和 `.trellis/workflow.md` 等运行副本。

## Acceptance Criteria

- [ ] 在一个本地 `main` 落后 `origin/main` 的复现仓库中，默认 `prepare-task.sh --json` 不再报告未刷新的 `fresh: true`。
- [ ] `preflight.base_freshness.fetch_performed` 或等价字段能证明远端状态已刷新；若无法刷新，输出不得伪装成 fresh。
- [ ] `prepare-task --create-worktree --create-task` 仍会在创建 worktree/task 前刷新 base，并在分叉或无法确认时 fail closed。
- [ ] 单元测试覆盖 planner-only 刷新远端 remote-tracking ref 的场景，以及 local behind remote 时不快进本地 base 但报告非 fresh/stale 的行为。
- [ ] `trellis/workflows/guru-team/workflow.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、schema 描述与实现语义一致；必要时同步 `.trellis/workflow.md` 与 `.trellis/guru-team/` dogfood 副本。
- [ ] 通过 targeted Python tests、shell syntax/compile checks、task validation、dogfood overlay drift check 和 `git diff --check`。
- [ ] 最终报告明确哪些 throwaway install / upgrade-update 门禁已覆盖，哪些因范围或环境未完整执行。

## Out Of Scope

- 不修改 Trellis 官方 CLI、全局 npm 包或 `node_modules`。
- 不创建新的 workflow id、template id、preset id 或 spec template marketplace 内容。
- 不改变 issue intake、duplicate search、naming quality、developer identity、PR publish 等无关流程语义。
- 不在脚本中加入 AI 判断；脚本仅执行 Git/GitHub 状态读取、刷新、校验与 artifact 记录。

## Notes

- 当前无阻塞性开放问题；issue #59 的验收口径足够进入实现。
