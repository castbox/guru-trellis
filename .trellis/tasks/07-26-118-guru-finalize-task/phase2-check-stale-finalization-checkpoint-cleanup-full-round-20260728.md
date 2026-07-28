# Issue #118 stale finalization checkpoint cleanup Phase 2 全量检查

## 检查完成

### 检查身份与边界

- 角色：独立 Phase 2 `trellis-check` reviewer。
- Reviewer：`/root/issue118_phase2_stale_checkpoint_cleanup`。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Checked HEAD：`362f8cd62c62621e892b46e68763ae4323460871` 加 current task-local working tree。
- Finding inventory：P0=`0`、P1=`0`、P2=`0`、P3=`0`。
- 建议 typed exit：`passed`，consumer=`skill:guru-create-task-commit`。

Workspace boundary 通过：expected workspace 与 actual repo root 都是上述 task worktree；
source checkout 为 `/Users/wumengye/Documents/GoProjects/guru-trellis`，状态 clean，且没有
suspicious source artifacts。Planning approval checker 返回 `typed_exit=approved`，schema 2.0
规划、ambiguity/provenance/fixed-scope scanner、Docs SSOT 与三份 planning document digest
均 current。

`check.jsonl` 只有 seed row，因此本轮按 fallback 读取 task `prd.md`、`design.md`、
`implement.md`，并读取 `docs`、`preset`、`workflow` 三个适用 spec layer。

本 reviewer 未修改 runtime、public contract、schema、tests、workflow、preset、overlay、
README、平台分发、旧 gate 或 publication/finalization artifact；未调用 Phase 2 recorder，
未 commit、push、创建/修改 PR、archive、Ready、merge、deploy 或执行 GitHub Issue mutation。
本轮只新增本报告及同轮 command evidence。

### 已检查文件

- Planning：`prd.md`、`design.md`、`implement.md`、`planning-approval.json`。
- Cleanup handoff：
  `implementation-handoff-stale-finalization-checkpoint-cleanup.md`。
- 删除目标：`closeout-plan.json`、`task-finalization-gate.json`。
- Current task evidence：`agent-assignment.json`、`phase2-check.json`、
  `review-gate.json`、`review.md`、`pr-readiness.json`、`pr-body.md`、
  `finish-summary-index.json`、`issue-scope-ledger.json`、
  `task-commit-plans/008.json`、`reviews/round-016-final-release.md`。
- 完整实现：`origin/main...HEAD` 的 committed diff、canonical/dogfood runtime、
  `guru-finalize-task` package、#116/#117 producer-consumer edges、Interface 1.3、
  registry、schemas、examples、eval corpus、preset installer 与平台 copies。
- Durable Docs SSOT：`.trellis/spec/docs/**`、`.trellis/spec/preset/**`、
  `.trellis/spec/workflow/**`、repository/workflow/preset README。
- Protected/deployment surfaces：global workflow、upstream `trellis-finish-work`
  family、preset overlays、official `.trellis/scripts/task.py`、CI/CD、container、
  K8s/Helm、DB migration、Terraform、Makefile 与 deploy paths。

### Normal-path finding 与修复复核

被删除的 `closeout-plan.json` 和 `task-finalization-gate.json` 是 finalizer owner-private
active checkpoint，但它们绑定的是旧 identity：

- reviewed work HEAD：`d420a6842eca05bd0bf7472bdf06e3b519bace5f`
- plan digest：`59ce5a04a6e9470d7d5e99ab76f8821af0b1ae8cc0448f0ded08b205021d88f6`
- typed route：`verification_required`

Current task-work HEAD 已是 `362f8cd...`。旧 plan 之后，正常 task workflow 又产生七个
合法 evidence path：

| Path | SHA-256 | Bytes |
| --- | --- | ---: |
| `implementation-handoff-live-wrapper-namespace-fix.md` | `2154f3ee9ffdafeb61d0a254c78437eec5a91744657e37ab8bc803c877514b6c` | 3826 |
| `phase2-check-live-wrapper-namespace-fix-exact-stream-full-round.md` | `2a74ae2f84742b75c126cccf0bd77c06cc22d16f0d8faa5b9cf498acb85fae30` | 13876 |
| `phase2-check-live-wrapper-namespace-fix-full-round.md` | `d6f594a610cddd857c7a8e221ede26744ab90c79fd48ed68e31294eeb4de6830` | 12593 |
| `phase2-command-evidence-live-wrapper-namespace-fix-exact-stream-full-round.json` | `6bf7d3f77d235b4d712a854969c5ff976c3d950787753595c7dc3761153086a1` | 281289 |
| `phase2-command-evidence-live-wrapper-namespace-fix-full-round.json` | `de1e29c39de44663b35a6bc9f6c6065cff4beb5e36c141f9b361080b9b3c5d88` | 12794 |
| `reviews/round-016-final-release.md` | `a9bb25dba2ccce44fc6e2d175ea7739b18f0ff6023f3b25ef440d6c26f34a651` | 15214 |
| `task-commit-plans/008.json` | `be4175c6c79b825b670f44b10ff78124f6841d7e2efe5460bd0513fb147aa69f` | 37348 |

旧 immutable projection 不能吸收这七个新 path；真实 side-effect-free preview 因
`unexpected_task_files` fail closed。旧 gate 已存在，又不能进入 legacy takeover。
因此继续保留两个 reserved checkpoint names 会稳定阻断 current publication entry，
无需人为伪造、篡改 artifact 或引入异常场景即可复现，属于 current normal-path correctness。

Current cleanup 删除两个 active copies，使后续完整 gate 重新通过后能够以 current
publication evidence 重新 preview、生成新 immutable plan，并取得新的 exact digest
confirmation。它没有放宽 #116 owner checker、plan digest、HEAD、path 或 recovery 校验。

旧 bytes 仍由 checked commit 精确保留：

- `HEAD:closeout-plan.json` SHA-256=`d26f1f9ba335c83c6c9af17ce197688a2e78075f1dddee42deb497e457307f13`，
  208175 bytes。
- `HEAD:task-finalization-gate.json`
  SHA-256=`711042c6d1ad9db7c6d8ea89bf036a1bda3b80b5cf393466d0a449e4e1f11876`，
  3085 bytes。

删除工作树 active copies 不抹除 Git audit history，也不把 private checkpoint body
泄露到 public DTO、runtime cache 或 durable docs。

### 已修复问题

- 文件：`.trellis/tasks/07-26-118-guru-finalize-task/closeout-plan.json`、
  `.trellis/tasks/07-26-118-guru-finalize-task/task-finalization-gate.json`。
- 问题：两个 reserved active checkpoint 绑定旧 HEAD/plan/route，且 immutable projection
  不含后续七个合法 task-work evidence path，导致 current preview 稳定返回
  `unexpected_task_files`。
- 修复：Implementation agent 删除两个 stale active checkpoint；后续 finalization 必须
  从 current #116 `ready` evidence 重新 preview 并重新确认新 digest。
- Reviewer 复核：删除范围只含 task-local private state，不修改 public API、runtime、
  schema、test、workflow、preset、overlay、deploy surface 或 protected upstream path。

本 reviewer 没有新增机械 self-fix。

### 未修复问题

没有 open current-scope P0-P3 finding。

以下是预期 downstream stale state，不是未修复实现缺陷：

- `check-phase2-check` 返回 exit 2：旧 evidence 的 assignment、HEAD、dirty snapshot stale，
  且 reviewed path 中的旧 `closeout-plan.json` 已删除。
- `check-review-gate` 返回 exit 2：Phase 2、assignment、task commit/ledger 与 current
  working tree binding stale。
- `check-task-publication-review --expected-exit ready` 返回 exit 2：Branch Review、
  Phase 2、repository/publication bindings stale。

这些 fail-closed 结果证明旧 gate 没有被删除操作错误复用。主会话必须在本报告之后重新执行
`guru-check-task` recorder/checker、task commit、独立 Branch Review 与 publication review。

完整 committed `git diff --check origin/main...HEAD` 仍只命中 immutable
`reviews/round-009-finding-closure.md:203` 的历史 trailing whitespace。Current dirty diff
与排除 raw review history 的 effective diff check 通过；本轮不改写历史 raw review evidence。

### Docs SSOT

Approved task strategy 仍是 `ssot_first`：主实现已把 finalizer ownership、Interface 1.3、
transaction semantics、installation 与 #119/#132 边界写回 durable package/spec/README SSOT。

本 cleanup 的 reconciliation result 是 `no_docs_update_needed`，不改变 approved strategy：

- cleanup 只删除两个 stale task-local private checkpoint；
- immutable plan、owner-private state、#116 checker、same-plan recovery 与 fail-closed preview
  的 durable contract 无变化；
- runtime、schema、test、workflow、preset、overlay、README 与平台 copy 均无 dirty delta；
- cleanup handoff、本报告与 JSON 只保留 task-history/recovery provenance。

因此当前 durable docs、task artifacts、code/test 与 approved Docs SSOT Plan 一致。

### 验证结果

- Lint：通过。Current `git diff --check`、changed existing JSON parse、Bash syntax、
  Python compile、source/installed package validator、ownership、overlay drift、
  sensitive-material scan、protected/deploy no-diff 均通过。
- TypeCheck：通过适用检查。仓库没有单独 configured ruff/mypy/pyright gate；
  Python compile、closed schema/interface validators 与完整 tests 提供适用静态覆盖。
- Task validation：通过。
- Runtime full：627 passed，13 skipped。
- #105 transaction matrix：105 passed。
- Skill/package graph：180 passed。
- Finalizer owner contract：5 passed。
- #116/#117 owner contract：28 passed。
- Preset installer：45 passed。
- Upstream ownership tests：9 passed。
- Source/installed package validator：13 active Skills、52 exits，workflow markers
  `12/46/27`；installed managed files=2659，sidecar/removal/conflict=`0/0/0`。
- Source/installed shared real wrapper：各 8/8 passed，覆盖六个 exits 及
  `verified`/`not_required` re-entry。
- Canonical/installed/shared/Codex/Claude/Cursor finalizer package parity：通过。
- Runtime canonical/dogfood parity：通过。
- Clean throwaway：exit 0，覆盖 initial install、installed recovery、official
  `trellis update`、preset reapply、ownership、no-developer path 与 final zero-sidecar。
- Live issue scope：#118 OPEN；#115/#119/#132 OPEN；#105 CLOSED/COMPLETED。
- Issue ledger/PR body：只关闭 `#118`；`#115` related；`#119/#132` follow-up；
  PR body 只含 `Closes #118`。

验证 setup observation：

- 初始 changed-JSON loop 包含两个已删除 JSON；改为只解析 existing changed JSON 后通过。
- 初始相对 `PYTHONPYCACHEPREFIX` 污染临时 Git fixture；改用 repo 内绝对 gitignored prefix
  后 focused 105-case suite 全部通过。

### 证据交接

- 阶段二：覆盖 planning/provenance、workspace、cleanup normal path、旧 plan/gate identity、
  七个 preserved evidence path、完整 runtime/#105/package/eval、install/update/reapply、
  Docs SSOT、安全/部署与下游 stale behavior。P0/P1/P2/P3=`0/0/0/0`。
- 本报告与
  `phase2-command-evidence-stale-finalization-checkpoint-cleanup-full-round-20260728.json`
  可支撑主会话构造 fresh `phase2-check.json`，但不替代 `guru-check-task` semantic Gate，
  本 reviewer 未调用 recorder。
- Docs SSOT：approved strategy=`ssot_first`；cleanup result=`no_docs_update_needed`；
  durable docs / task artifacts / code / tests 一致，cleanup artifacts 仅为 task history。
- Branch Review：本轮不是 Branch Review。Fresh task commit 后必须使用独立 reviewer 覆盖
  完整 `origin/main...HEAD`，再执行 publication review 和新的 immutable plan/digest 确认。
- 安全与部署：未发现 secret、credential、private key、signed URL、customer data 或 raw
  provider payload；无 CI/CD、container、K8s、DB、Terraform、Makefile、deploy 或
  production-write 影响。

### 结论

Stale finalization checkpoint cleanup 在支持的 normal path 上成立：删除两个旧 active
checkpoint 释放 reserved owner-private names，同时保留 Git 历史，并强制所有下游 evidence
按 current task-work 重新建立。实现与 Issue #118、approved planning、Docs SSOT、
Interface 1.3 private-state boundary、#105 transaction semantics、#116/#117 ownership、
#119/#132 scope 边界一致，没有 open current-scope finding。

建议 Phase 2 typed exit=`passed`。下一步必须由主会话记录本 checker completed event，运行
fresh Phase 2 recorder/checker，创建新 task commit，执行独立完整 Branch Review，重新取得
#116 `ready`，再生成并展示新的 immutable closeout plan/digest。新 confirmation 前禁止
push、PR mutation、archive、Ready、merge 或 Issue mutation。
