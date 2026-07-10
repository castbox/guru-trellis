# 分支审查第一轮：问题发现审查

## 审查元数据

- 审查角色：问题发现审查代理（全新独立 reviewer）
- 审查范围：`origin/main...HEAD`
- Reviewed HEAD：`a84e5720d0ea18482b46b165062930e50cf54b34`
- Base：`origin/main`，审查时指向 `59d6c0caf404c4c927fe8aada92811d1ced907d5`
- 提交：`a84e572 feat(workflow): #96 重建任务启动上下文与本机运行态边界`
- 工作区：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/096-task-runtime-boundary`
- 边界校验：通过；expected workspace 与 actual repo root 一致，source checkout 无可疑 task artifact。
- 审查方式：独立读取 Issue #96、`prd.md`、`design.md`、`implement.md`、`implementation-handoff.md`、`planning-approval.json`、`phase2-check.json`、`issue-scope-ledger.json`、`agent-assignment.json`、`check.jsonl` 引用的 spec/research，以及完整 committed diff；未复用 Phase 2 结论代替 Branch Review。

## Diff 概览

- 完整 diff：48 files changed，2440 insertions，1499 deletions。
- 主要范围：任务启动上下文 schema/writer/loader、local runtime mapping、workspace boundary、prepare/planning/check/review/finish/publish 调用链、obsolete managed artifact cleanup、canonical/dogfood/overlay/docs/spec、单元测试与任务证据。
- 提交规范：`check-commit-messages.sh` 通过，commit subject 和 body 满足 Issue #96 work commit 合同。

## 问题清单

### Finding 1 — P1：任务启动上下文的 base/remote SHA 映射读取错误，正常新建任务会静默写空

- 状态：阻塞
- 文件：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:6293`
- 证据：
  - `refresh_base_freshness_for_planner()` 和 `ensure_base_freshness()` 返回的字段是 `local_head_after` 与 `remote_head`，见同文件 `1278-1279`、`1343-1347`。
  - `build_task_start_context()` 却读取不存在的 `local_sha` 与 `remote_sha`，因此 fallback 为 `""`。
  - 最小复现用 producer 真实字段构造 payload 后，`base_head_sha` 与 `remote_head_sha` 均输出空行。
  - 现有测试只验证 schema 接受空 SHA，没有断言正常成功路径必须写入 producer 提供的 40 位 SHA，因此 220 项 core tests 未发现该错误。
- 影响：
  - Issue #96 要求任务启动上下文保存可移植的 base/task 启动事实；SHA 字段虽然存在，但实际创建路径丢失值，削弱 base freshness、审计与后续 stale 判断证据。
  - schema 允许空字符串只适合无法确认 remote 的受控路径，不应掩盖成功 fetch/create-worktree 路径的字段映射错误。
- 建议修复：将读取键改为 `local_head_after` / `remote_head`，并新增成功 fetch、remote-only、fetch-failed 三类测试，明确何时允许空值。

### Finding 2 — P1：preset installer 测试在 committed HEAD 上失败，Phase 2 的“30 tests passed”结论不可复现

- 状态：阻塞
- 文件：`trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py:803`
- 证据：
  - `test_install_removes_unmodified_obsolete_schema` 运行 `git show HEAD:trellis/workflows/guru-team/schemas/intake-handoff.schema.json` 取得旧 managed 内容。
  - 当前提交已按需求删除该 path，因此 `git show HEAD:...` 返回 fatal，测试 suite 结果为 `FAILED (errors=1)`，退出码 1。
  - 独立重跑结果：30 项中 1 error；失败发生于测试 fixture 构造，不是 installer 正确拒绝或接受 obsolete 文件的行为断言。
  - `phase2-check.json` 记录该命令为 “30 tests passed”，但该结论只对 pre-commit working tree 快照成立，不能在 reviewed committed HEAD 上复现。
- 影响：
  - Issue #96 明确要求 obsolete managed schema 的未修改删除与用户修改保留双路径验证；当前 committed branch 的关键回归测试自身不可执行。
  - Branch Review 不能在测试失败时放行。
- 建议修复：把旧 schema fixture 固化为测试内常量/fixture 文件，或从明确的 base ref（而非 `HEAD`）读取并处理不可用场景；测试必须对任意 clone 的当前提交可重复运行。

### Finding 3 — P1：远端 marketplace push 后硬门禁没有真实执行点，`finish-work` 会 push 后立即创建 PR

- 状态：阻塞
- 文件：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:7364`
- 证据：
  - `phase2-check.json` 将 `remote branch marketplace init/preview/switch` 标记为 “commit+push 后、PR 前硬门禁”。
  - 当前远端尚无 `codex/096-task-runtime-boundary` branch，`git ls-remote --heads origin codex/096-task-runtime-boundary` 无输出，raw branch `trellis/index.json` 返回 HTTP 404，因此本轮无法执行该 gate。
  - Trellis CLI 0.6.5 的 registry parser 支持 `gh:owner/repo/subdir#ref`，所以 branch/tag push 后技术上可验证；问题不在 CLI 能力。
  - 实际 `cmd_publish_pr()` 在 `git push -u` 后紧接着执行 `gh pr create`，见同文件 `7365-7388`；`cmd_finish_work()` 自动调用该 publish 流程，workflow 也规定 finish-work 后自动 publish。
  - 当前 workflow、skill、script、schema 或 gate artifact 中没有要求/验证 marketplace init/preview/switch 成功的字段，也没有 push-only 后暂停点；该“硬门禁”只存在于任务说明和 Phase 2 文字证据中。
- 影响：
  - 用户要求的“远端 marketplace push 后硬门禁设计真实可执行”未满足；正常 `trellis-finish-work` 路径会在 reviewer 无法插入验证的情况下直接建 PR。
  - 当前分支涉及 workflow marketplace、preset、overlay 与 upgrade/update 公共 API，缺少远端 branch 内容验证会使开箱安装结论仍依赖本地 canonical/公开 main 的替代样本。
- 建议修复：定义可审计且 fail-closed 的发布前验证方案。可选方向包括：受控 push-only executor + 远端 marketplace verifier artifact + publish validator，或在 `cmd_publish_pr()` 的 `git push` 与 `gh pr create` 之间执行确定性 marketplace commands 并记录 branch/ref、命令、结果和 digest。AI 仍负责判断结果充分性，脚本只执行/记录/校验事实。

### Finding 4 — P1：`close_issues` 的 Issue #96 验收证据为空，当前 Issue Scope Ledger 无法通过 publish validator

- 状态：阻塞
- 文件：`.trellis/tasks/07-10-096-task-runtime-boundary/issue-scope-ledger.json:12`
- 证据：
  - `close_issues[0].number` 为 96，但 `acceptance_evidence` 是空数组；`primary_issue.acceptance_evidence` 也为空。
  - `validate_ledger_for_publish()` 明确要求每个 close issue 存在验收或验证证据，否则返回 `close_issues 中 issue #96 缺少验收或验证证据。`，见 `guru_team_trellis.py:2422-2425`。
  - close/ref/followup 分类本身正确：仅 #96 在 `close_issues`；#53 在 `related_issues`；#97/#98/#99/#100 在 `followup_issues`，不会被当前 PR 关闭。
- 影响：
  - 当前 artifact 不能支撑 `Closes #96`，也不能进入 publish。
  - 即使后续解决前三项代码/测试问题，仍需把 Issue #96 每项验收的真实命令、文件和结果写入 ledger，并由最终 Branch Review 覆盖。
- 建议修复：修复并复验后，按 Issue #96 验收项补齐 `acceptance_evidence`；对远端 marketplace gate 只能记录真实 push 后结果，不得用 deferred 说明替代 passed evidence。

## Issue #96 验收覆盖

- 固定字段白名单与 schema：已实现；但 Finding 1 表明两个 SHA 字段在正常 producer 路径失真。
- portable context 禁止绝对路径/runtime/preflight/developer path：validator 与测试覆盖，最小扫描未发现当前 tracked context 泄漏。
- local runtime 路径与 gitignore：已实现 `.trellis/.runtime/guru-team/workspaces|tasks/*.json`，`.gitignore` 与 installer idempotent 管理存在。
- cache miss 重建：实现通过 `git worktree list` + branch + task context 重建，core tests 覆盖。
- workspace boundary：prepare 后续 planning/check/review/finish/publish 均迁移到 task context/runtime 推导；finish/publish 在副作用前执行 boundary。
- 普通 task tracked 写入隔离：并行 task fixture 验证 task context/runtime path 不共享固定文件；未发现重新写 `.trellis/guru-team/handoff.json`。
- obsolete cleanup：installer 实现了 hash allowlist 删除与用户修改冲突保留，但 Finding 2 使 committed branch 的删除测试失败。
- handoff public API cleanup：代码公共读取路径、schema、config、manifest、workflow 与公开 docs 已迁移；剩余字符串位于历史 task evidence、obsolete 清理声明、禁键列表和不存在断言，属于允许范围。
- canonical/dogfood/overlay/docs/spec：canonical workflow/script/schema 与 dogfood hashes 一致，overlay drift check 通过，无 `.new` / `.bak`。
- throwaway/update：Phase 2 记录本地 throwaway preset 与 `trellis update --migrate` 通过；本轮未重复破坏性 upgrade 流程。
- 远端 marketplace：未完成，且现有自动 publish 数据流缺少真实门禁，见 Finding 3。

## 数据流审查

- Prepare：planner 输出仍可包含本机 preflight；仅 `--create-worktree` 写 local runtime workspace mapping，仅 `--create-task` 写 task-local context/ledger/runtime task mapping，分层方向正确。
- Boundary：从当前 checkout、task-local context、runtime cache、`git worktree list` 推导 expected workspace；source checkout suspicious artifacts fail closed。
- Planning / Check / Review：均以 task dir + task-start context 为输入；Branch Review 预检使用 `allow_committed_head=True` 审计 Phase 2 祖先 HEAD 之后的 committed paths，设计合理。
- Finish / Publish：workspace boundary 检查已前移到 archive/push 前；但远端 marketplace gate 未进入该链路。
- Schema / Runtime 安全：schema `additionalProperties=false`，validator 递归拒绝禁键、绝对路径和 `.trellis/.runtime/` 路径；当前 task context 未包含本机绝对路径。

## Docs SSOT 判断

- Plan strategy：`ssot_first`。
- Durable primary inputs：canonical workflow 与 task-start-context schema。
- 同步结果：workflow、companion specs、requirements docs、README、preset docs、canonical overlays 与 dogfood copies 已同步。
- Task delta merge：任务启动上下文、本机运行态、workspace boundary、obsolete cleanup 合同已进入 durable docs。
- Task-history-only：planning/research/approval/check/assignment artifacts 保留在 task 目录，未写入公共 marketplace/spec template。
- 结论：Docs SSOT 的当前文本与实现大体一致，但“remote branch marketplace hard gate”只记录在 task evidence，没有落成可执行 durable workflow/script contract；因此 Docs SSOT/执行合同仍不完整，对应 Finding 3。

## 验证命令与结果

- `git diff --name-status origin/main...HEAD`：通过，审查 48 个 changed files。
- `git diff --check origin/main...HEAD`：通过。
- `.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task ...`：通过。
- `.trellis/guru-team/scripts/bash/check-commit-messages.sh --json --task ...`：通过。
- `.trellis/guru-team/scripts/bash/check-agent-assignment.sh --json --task ...`：通过；独立 reviewer assignment 已记录在 working tree metadata。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：通过，220 tests。
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：失败，30 tests 中 1 error，见 Finding 2。
- `python3 -m py_compile ...`：通过。
- `python3 ./.trellis/scripts/task.py validate ...`：通过，9 implement + 10 check entries。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- changed JSON/JSONL parse：通过。
- `git ls-remote --heads origin codex/096-task-runtime-boundary`：无远端 branch。
- remote raw branch `trellis/index.json`：HTTP 404。
- Trellis CLI：`0.6.5`；安装代码确认 `gh:...#ref` 支持 branch/tag ref。
- `check-phase2-check.sh` 普通模式：因 Phase 2 记录 pre-commit HEAD/dirty snapshot 而报告 stale；Branch Review 代码路径使用 `allow_committed_head=True`，会审计祖先 HEAD 后提交是否完全被 Phase 2 dirty paths 覆盖，因此该普通模式结果本身不是额外 finding。

## 安全与部署影响

- 安全：未发现 secret、token、private key、`.env`、签名 URL 或客户数据进入 diff。task context 当前无绝对路径泄漏。
- 部署：不涉及业务服务、容器、Kubernetes、数据库 migration、CI/CD 或 Makefile；影响集中在开发工作流、marketplace/preset 安装、task metadata 与发布门禁。
- 升级风险：obsolete cleanup 对用户修改副本采用保留并报告冲突，方向正确；但 committed 测试失败，尚不能作为 release 级升级证据。

## 观察项

- `agent-assignment.json` 当前 dirty 仅因为主会话在 commit 后记录本轮 reviewer；属于 Branch Review metadata，不是实现越界。
- source checkout 状态为空，未发现 task artifact 错写源 checkout。
- 当前 extension stable tag `v0.6.5-guru.3` 尚未出现在 origin；稳定 tag 验证应在合并/release 后执行，不应冒充当前 branch gate。

## 后续候选

- 为 `task-start-context.json` 增加 JSON Schema runtime validation 测试，确保 Python validator 与 schema 不漂移。
- 把 marketplace branch/ref 验证结果定义为结构化 artifact，并在 publish validator 中校验 ref、HEAD/digest 与命令结果，避免仅靠文字 checklist。
- 修复后新增一个从 clean clone 运行 preset tests 的 CI 场景，防止测试依赖被本提交删除的 `HEAD:path`。

## 最终结论

- Findings：4 个，均为 P1 阻塞项。
- 当前 Branch Review Round 1 不通过，不可生成通过型 `review-gate.json`，不可执行 finish/publish，也不可使用 `Closes #96`。
- 修复前三项实现/测试/发布门禁问题并补齐 Issue Scope Ledger 验收证据后，应重新提交并由新的问题闭环审查代理覆盖新的 `origin/main...HEAD` 完整 diff。
