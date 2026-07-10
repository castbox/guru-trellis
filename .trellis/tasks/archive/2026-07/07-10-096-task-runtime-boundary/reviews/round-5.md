# Round 5 问题闭环审查报告

## 审查范围

- 角色：问题闭环审查代理；仅审查并写 raw report，不修改实现、commit、push、PR 或 gate。
- Reviewed HEAD：`f48abcf1f73da439efc68f7342dde562c4c9c452`。
- Diff 范围：`origin/main...HEAD`，覆盖完整五提交：`a84e5720d0ea18482b46b165062930e50cf54b34`、`90a2d45c823775ff0eaa485ef10640d8b4aa96f5`、`f05cd662e852984f7f07cf6336d0867eb6532302`、`9c542783cd1c99819ebd70fd77134c4b07febd7e`、`f48abcf1f73da439efc68f7342dde562c4c9c452`。
- Round 5 增量确认：`f48abcf1f73da439efc68f7342dde562c4c9c452` 仅从 `reviews/round-4.md` 删除主会话追加的“实现后 Finding 生命周期补充”，未改变实现或测试。
- Workspace boundary：expected workspace 与 actual repo root 均为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/096-task-runtime-boundary`；source checkout clean、无 suspicious source artifacts。审查开始时仅 task-local `agent-assignment.json` 存在主会话 recorder dirty，本 reviewer 未修改该文件。

## 历史 Finding 闭环

- Round 1 SHA / runtime mapping、clean clone obsolete fixture、workflow managed file 同步、finish-work boundary、developer identity 残留等 findings：代码、测试与 clean clone 证据保持闭环。
- Round 2 remote marketplace verifier / ledger / failed payload / exact metadata tail / publish 顺序 findings：实现与定向 contract tests 保持闭环；当前 ledger 仍正确记录 required remote evidence 为 `pending`，未伪造 passed artifact。
- Round 4 active workspace contract P1 的内容修复：当前 canonical workflow、README、requirements、workflow specs、preset overlays、dogfood start/continue/finish 入口及三平台 implement/check agents 均未发现 `handoff.workspace_path`、`task-start-context.workspace_path`、`task_start_context.workspace_path` 或旧 fixed `.trellis/guru-team/handoff.json` active 引用；workspace 定位正文已统一为 portable ids + current checkout / `.trellis/.runtime/guru-team/**` / `git worktree list` + `check-workspace-boundary.sh --task`。

## Findings

### Finding 1 — P1：active-reference scanner 漏扫三平台 dogfood implement/check agents，无法阻止本轮要求的回归

- 文件：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:7008`。
- 问题：`ActivePublicReferenceContractTest.active_public_files()` 扫描 canonical preset overlays、dogfood start/continue/finish skills/prompts/commands、`.trellis/agents`，但没有扫描 dogfood `.codex/agents/**`、`.claude/agents/**`、`.cursor/agents/**`。这些文件正是 Round 4 P1 明确要求闭环的 active implement/check agent copies，也是 `implementation-handoff.md` 声称 scanner 已覆盖的 “dogfood ... agent copies”。
- 可复现证据：在 `.codex/agents/trellis-check.toml` 临时注入 `task-start-context.workspace_path` 后，仅运行 `ActivePublicReferenceContractTest`，结果仍为 exit `0` / `OK`；恢复文件后 working tree 无该变异。说明测试对目标 active surface 存在真实 false negative，不是推测性覆盖建议。
- 影响：当前文件内容虽然已经清理，但后续任一 dogfood implement/check agent 单独回流旧 workspace API 时，240 项 suite 仍可能全绿；因此“active-reference scanner 能阻止回归”和 AC7 的确定性保护尚未成立。`phase2-check.json` 与 `implementation-handoff.md` 对 scanner 覆盖范围的声明也不够准确。
- 修复要求：把 `.codex/agents`、`.claude/agents`、`.cursor/agents` 纳入 active public file set，或改为从 canonical overlay managed paths / 明确 allowlist 派生 canonical 与 dogfood 扫描集合；增加至少一个针对 dogfood implement/check agent 的回归用例，并确认 `.trellis/tasks/**`、`.trellis/tasks/archive/**` 等历史 artifact 仍不在扫描范围。
- 状态：未修复。Branch Review 模式不得修改实现，应返回主会话修复并生成新 HEAD 后由新的独立 reviewer 复审。

## 验证结果

- Core tests：`python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`，240 tests passed。
- Preset tests：`python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`，30 tests passed。
- Clean clone：使用 `git clone --no-local` 并 checkout 固定 Reviewed HEAD，240+30 tests 通过，dogfood overlay drift 通过，clone 工作树 clean。
- 定向 verifier/ledger：`PublishBoundaryTest`、`MarketplaceVerificationContractTest`、`ActivePublicReferenceContractTest` 共 41 tests passed；pending evidence、failed payload、ledger digest、metadata tail 与 publish fail-closed 路径保持有效。
- 静态检查：Python compile、全部 managed shell `bash -n`、task JSONL validation、phase context、dogfood overlay drift、`git diff --check origin/main...HEAD` 均通过。
- Commit messages：五提交均通过 `check-commit-messages.sh --base-ref origin/main`。
- Canonical/dogfood：workflow、Python helper、task-start-context schema、marketplace-verification schema byte equality 通过；无 `.new` / `.bak`。
- Active 内容独立扫描：补入 `.codex/agents`、`.claude/agents`、`.cursor/agents` 后，当前实际内容无 forbidden reference；finding 针对 scanner 回归保护范围，而非当前正文仍有旧引用。
- Lint：通过（Python compile、shell syntax、`git diff --check`）。
- TypeCheck：不适用；仓库无独立静态类型检查配置。
- Tests：通过，但存在上述可复现测试覆盖 finding。

## Docs SSOT 与任务证据

- Plan strategy：`ssot_first`。durable docs（README、requirements、canonical workflow/README、preset README、`.trellis/spec/workflow/**`）与当前代码、schema、overlay 和运行时边界正文一致。
- Durable docs / task artifacts：Round 4 P1 的语义修复已同步；但 `implementation-handoff.md` 和 `phase2-check.json` 声称 active scanner 覆盖 dogfood agent copies，与实际 `active_public_files()` 不一致，因此当前 evidence 不能支持“回归已被完全阻止”的结论。
- Task delta：当前范围无需 reviewer 首次合并 durable docs；历史 task report 被 scanner 排除是正确方向。修复 scanner 时应保持历史 artifact 不参与 active contract 扫描。
- Remote marketplace：任务目录无 `marketplace-verification.json`；ledger 的 required evidence 状态为 `pending`。正式 publish 前必须按既定顺序 push reviewed/fixed content HEAD、运行真实远端 verifier、生成 schema-valid passed artifact、回写 ledger 并提交精确 metadata tail。

## 安全、部署与 Issue Scope

- 安全：完整 diff 未发现 token、private key、`.env`、数据库 URL、签名 URL或客户数据；verifier 仍只记录 digest/size，未发现新增敏感输出路径。
- 部署：无业务服务、DB migration、容器、Kubernetes、CI/CD、Makefile 或依赖锁文件影响；变更限于 Guru Team workflow/preset/runtime metadata 与发布门禁。
- Issue scope：`close_issues` 仅 #96；#53 为 related；#97/#98/#99/#100 为 followup。未发现错误 close keyword 或范围扩张。

## 证据交接

- Branch Review diff：`origin/main...f48abcf1f73da439efc68f7342dde562c4c9c452`，完整五提交。
- Findings：P0 0、P1 1、P2 0、P3 0。
- 历史 findings：Round 1/2 保持闭环；Round 4 内容修复有效，但其 deterministic regression scanner 闭环不完整。
- Gate 适用性：本报告可作为 Round 5 raw Branch Review evidence，但因存在 P1 finding，不可用于通过 Branch Review Gate 或最终放行。

## 结论

Reviewed HEAD `f48abcf1f73da439efc68f7342dde562c4c9c452` 当前 active workspace 文案和实现合同已清理，但 active-reference scanner 无法覆盖三平台 dogfood implement/check agents，不能满足“阻止回归”的明确验收要求。当前不是零 finding，**不建议进入新的最终放行审查，不建议通过 Branch Review Gate**。修复 scanner 覆盖并生成新 HEAD 后，应重新执行变异验证、240+30 clean clone 和独立闭环审查；只有零 findings 才建议进入新的最终放行审查。
