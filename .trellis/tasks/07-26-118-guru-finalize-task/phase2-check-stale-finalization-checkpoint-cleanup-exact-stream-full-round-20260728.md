# Issue #118 stale finalization checkpoint cleanup Phase 2 exact-stream 全量检查

## 检查完成

### 检查身份与边界

- 角色：独立 Phase 2 `trellis-check` reviewer。
- Reviewer：`/root/issue118_phase2_stale_checkpoint_exact_stream`。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Checked HEAD：`362f8cd62c62621e892b46e68763ae4323460871` 加 current task-local working tree。
- Finding inventory：P0=`0`、P1=`0`、P2=`0`、P3=`0`。
- 建议 typed exit：`passed`，consumer=`skill:guru-create-task-commit`。

Workspace boundary 通过：expected workspace 与 actual repo root 都是上述 task
worktree；source checkout 为
`/Users/wumengye/Documents/GoProjects/guru-trellis`，状态 clean，且没有
suspicious source artifacts。Planning approval checker 返回
`typed_exit=approved`，规划、ambiguity/provenance/fixed-scope scanner、Docs SSOT 与
三份 planning document digest 均 current。

`check.jsonl` 只有 seed row，因此本轮按 fallback 读取 task `prd.md`、`design.md`、
`implement.md`，并读取 `docs`、`preset`、`workflow` 适用 spec，以及
`trellis-check`、`guru-check-task` 的 Phase 2 exact-command/stream 合同。

本 reviewer 未修改 runtime、public contract、API、schema、tests、workflow、preset、
overlay、README、平台分发、旧 Phase 2/Branch Review/publication/finalization gate；未调用
Phase 2 recorder，未 stage、commit、push、创建/修改 PR、archive、Ready、merge、deploy
或执行 GitHub Issue mutation。本轮只新增本报告与配套 exact-stream JSON。

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
- Live authority：GitHub #118、#115、#119、#132、#105、#118 accepted-current
  comment、task branch open PR identity、remote main/feature refs、Trellis 官方 docs。

### Exact-stream evidence

- Formal commands：`72`；unique command ids：`72`；raw streams：`144`。
- 每条 command 都记录 exact `argv[]`、cwd、exit code、result summary、stdout/stderr
  locator、SHA-256 与 byte size。
- Retained-capture readback 重算：command `72/72`、unique ids `72/72`、streams
  `144/144`；所有 stdout/stderr digest/size 与 record digest/size 匹配；无 duplicate
  id、空 argv、缺失 nonzero rationale 或 integrity error。
- Status：`passed=65`、`expected_nonzero=5`、`passed_superseding=1`、
  `setup_error=1`。
- Reviewer setup error：
  `capture-readback-inline-attempt` 因 Python f-string quoting exit 1；原始
  stdout/stderr identity 已记录，并由唯一
  `capture-readback-script` supersede。文件化 verifier 及最终 JSON-vs-manifest
  readback 均通过。
- Capture manifest：SHA-256
  `d9b609253283de90cab832ceb185aa8fb7a3c814f09a58dc748363c5b3899248`，
  `118298` bytes。
- Raw captures 保留至 JSON readback/recompute 完成后才清理；capture、native runs、
  throwaway 与 reviewer-generated `__pycache__` roots 最终均验证 absent。

配套 evidence：

`phase2-command-evidence-stale-finalization-checkpoint-cleanup-exact-stream-full-round-20260728.json`

- SHA-256：
  `c69424befc6367c9f10a528e4fcfdb5a46f1956f891edbdd4d7255c5e7e3b948`
- `153412` bytes
- `3223` lines

### Normal-path finding 与修复复核

被删除的 `closeout-plan.json` 和 `task-finalization-gate.json` 是 finalizer
owner-private active checkpoint，但绑定旧 identity：

- reviewed work HEAD：`d420a6842eca05bd0bf7472bdf06e3b519bace5f`
- plan digest：
  `59ce5a04a6e9470d7d5e99ab76f8821af0b1ae8cc0448f0ded08b205021d88f6`
- typed route：`verification_required`

Current task-work HEAD 已是 `362f8cd...`。旧 plan 后由正常 task workflow 形成七个合法
evidence path，且本轮逐文件重算保持以下 exact identity：

| Path | SHA-256 | Bytes |
| --- | --- | ---: |
| `implementation-handoff-live-wrapper-namespace-fix.md` | `2154f3ee9ffdafeb61d0a254c78437eec5a91744657e37ab8bc803c877514b6c` | 3826 |
| `phase2-check-live-wrapper-namespace-fix-exact-stream-full-round.md` | `2a74ae2f84742b75c126cccf0bd77c06cc22d16f0d8faa5b9cf498acb85fae30` | 13876 |
| `phase2-check-live-wrapper-namespace-fix-full-round.md` | `d6f594a610cddd857c7a8e221ede26744ab90c79fd48ed68e31294eeb4de6830` | 12593 |
| `phase2-command-evidence-live-wrapper-namespace-fix-exact-stream-full-round.json` | `6bf7d3f77d235b4d712a854969c5ff976c3d950787753595c7dc3761153086a1` | 281289 |
| `phase2-command-evidence-live-wrapper-namespace-fix-full-round.json` | `de1e29c39de44663b35a6bc9f6c6065cff4beb5e36c141f9b361080b9b3c5d88` | 12794 |
| `reviews/round-016-final-release.md` | `a9bb25dba2ccce44fc6e2d175ea7739b18f0ff6023f3b25ef440d6c26f34a651` | 15214 |
| `task-commit-plans/008.json` | `be4175c6c79b825b670f44b10ff78124f6841d7e2efe5460bd0513fb147aa69f` | 37348 |

旧 immutable projection 不能吸收这些 paths；真实 side-effect-free preview 因
`unexpected_task_files` fail closed。旧 gate 已存在，又不能进入 legacy takeover。
该问题无需伪造或恶意篡改即可在支持的 normal path 复现，属于 current-scope
correctness。

Current cleanup 删除两个 active copies，使后续完整 task-work/publication gates 重新
通过后，finalizer 可消费 current #116 `ready` evidence 重新 preview、生成新 immutable
plan，并取得新的 exact digest confirmation。它没有放宽 #116 owner checker、plan
digest、HEAD、path、#117 或 recovery 校验。

旧 bytes 仍由 checked commit 精确保留：

- `HEAD:closeout-plan.json`：
  SHA-256=`d26f1f9ba335c83c6c9af17ce197688a2e78075f1dddee42deb497e457307f13`，
  `208175` bytes。
- `HEAD:task-finalization-gate.json`：
  SHA-256=`711042c6d1ad9db7c6d8ea89bf036a1bda3b80b5cf393466d0a449e4e1f11876`，
  `3085` bytes。

### 已修复问题

- 文件：`.trellis/tasks/07-26-118-guru-finalize-task/closeout-plan.json`、
  `.trellis/tasks/07-26-118-guru-finalize-task/task-finalization-gate.json`。
- 问题：两个 reserved active checkpoint 绑定旧 HEAD/plan/route，immutable projection
  不含后续七个合法 task-work evidence path，导致 current preview 稳定返回
  `unexpected_task_files`。
- 修复：Implementation agent 删除两个 stale active checkpoint；后续 finalization 必须
  从 current #116 `ready` evidence 重新 preview 并重新确认新 digest。
- Reviewer 复核：删除范围只含 task-local private state，不修改 public API、runtime、
  schema、test、workflow、preset、overlay、deploy surface 或 protected upstream path。

本 reviewer 没有新增 implementation self-fix。

### 未修复问题

没有 open current-scope P0-P3 finding，`implementation_required=false`。

以下是预期 downstream stale state，不是未修复实现缺陷：

- `check-phase2-check` exit 2：旧 assignment、HEAD、dirty snapshot 与 reviewed
  `closeout-plan.json` binding stale。
- `check-review-gate` exit 2：旧 Phase 2、task commit/ledger、assignment 与 current
  working tree binding stale。
- `check-task-publication-review --expected-exit ready` exit 2：旧 Branch Review、
  Phase 2、repository/publication bindings stale。

三条结果均有 exact stderr digest/size 和 expected-nonzero rationale。它们证明旧 gate
没有被 cleanup 错误复用。主会话必须在本报告后重新运行 fresh `guru-check-task`
semantic Gate/recorder/checker、task commit、独立 Branch Review 与 publication review。

完整 committed `git diff --check origin/main...HEAD` 仍 exit 2，只命中 immutable
`reviews/round-009-finding-closure.md:203` 的历史 trailing whitespace。Current dirty
diff 通过；本轮不改写历史 raw review evidence。

### Docs SSOT

Approved task strategy 是 `ssot_first`：主实现已把 finalizer ownership、Interface 1.3、
transaction semantics、installation 与 #119/#132 边界写回 durable
package/spec/README SSOT。

本 cleanup 的 reconciliation result 是 `no_docs_update_needed`，不改变 approved
strategy：

- cleanup 只删除两个 stale task-local private checkpoint；
- immutable plan、owner-private state、#116 checker、same-plan recovery 与
  fail-closed preview 的 durable contract 无变化；
- runtime、API、schema、test、workflow、preset、overlay、README 与平台 copy 均无
  dirty delta；
- cleanup handoff、本报告与 JSON 只保留 task-history/recovery provenance。

因此 durable docs、task artifacts、code/test 与 approved Docs SSOT Plan 一致。

### 验证结果

- Lint：通过。Current diff check、changed existing JSON、Bash syntax、Python compile、
  source/installed validators、ownership、overlay drift、protected/deploy no-diff 与
  sensitive-material scan 均符合预期。
- TypeCheck：通过适用检查。仓库没有 configured ruff/mypy/pyright gate；Python compile、
  closed schema/interface validators 与完整 tests 提供适用静态覆盖。
- Task validation：通过。
- Runtime full：`627 passed, 13 skipped`。
- #105 transaction matrix：`105 passed`。
- Skill/package graph：`180 passed`。
- Finalizer owner contract：`5 passed`。
- #116/#117 owner contracts：`28 passed`。
- Preset installer：`45 passed`。
- Upstream ownership：`9 passed`。
- 四平台 focused corpus/parsing/isolation：`5 passed`。
- Shared adapter parsing：`2 passed`。
- Expected-exit boundary：`3 passed`。
- Source/installed package：13 active Skills、52 external exits closure；
  workflow markers `12/46/27`。
- Installed managed files：`2659`；sidecar/removal/conflict=`0/0/0`。
- Source/installed shared real wrapper：各 `8/8` cases 通过，覆盖六 exits 及
  `verified`/`not_required` re-entry。
- Canonical/shared/Codex/Claude/Cursor package 与 corpus parity：通过。
- Runtime canonical/dogfood parity 与 dogfood overlay drift：通过。
- Clean throwaway：通过；覆盖 marketplace init/preview/switch、initial install、
  official update、preset reapply、managed hash、`.new/.bak`、五个 package copies、
  source/installed wrapper 与 OOTB；终态 sidecar/conflict=`0/0`。
- Live issue scope：#118/#115/#119/#132 `OPEN`；#105
  `CLOSED/COMPLETED`。
- Live task branch open PR：无；remote feature HEAD=`d420a684...`，
  remote main=`7820a9ee...`，本轮未执行任何 remote mutation。
- Issue ledger/PR body：只关闭 `#118`；`#115` related；`#119/#132` follow-up；
  PR body 只含 `Closes #118`。
- Security/deploy：未发现 secret/credential pattern；无 CI/CD、container、K8s、
  DB migration、Terraform、Makefile、deploy 或 production-write 影响。

### 证据交接

- 阶段二：完整覆盖 planning/provenance/workspace、cleanup normal path、旧 plan/gate
  identity、七个 preserved evidence path、Docs SSOT、627/13、#105 105、Skill graph、
  finalizer、#116/#117、preset/ownership、source/installed real wrapper、四平台
  corpus/parsing、canonical/dogfood/parity/drift、clean throwaway
  install/update/reapply/`.new`/`.bak`/OOTB、protected/deploy/sensitive scope、live
  GitHub #118/#115/#119/#132/#105 与三个预期 stale gate。P0/P1/P2/P3=`0/0/0/0`。
- Exact streams：JSON 内含全部 72 条 exact argv、exit、summary、stdout/stderr
  SHA-256/size、nonzero rationale、setup supersession 与 144-stream integrity
  readback，可支撑 fresh `phase2-check.json` 的 command facts。
- Guru boundary：本报告不替代 `guru-check-task` semantic Gate；本 reviewer 未调用
  recorder。主会话需先记录本 checker completed event，再运行 recorder/checker。
- Docs SSOT：approved strategy=`ssot_first`；cleanup result=
  `no_docs_update_needed`；durable docs / task artifacts / code / tests 一致，cleanup
  artifacts 仅为 task history。
- Branch Review：本轮不是 Branch Review。Fresh task commit 后必须由独立 reviewer
  覆盖完整 `origin/main...HEAD`，再执行 publication review 和新的 immutable
  plan/digest 确认。
- 安全与部署：无 secret/credential/customer data/raw provider payload；无 deploy 或
  production-write 影响。

### 结论

Stale finalization checkpoint cleanup 在支持的 normal path 上成立：删除两个旧 active
checkpoint 释放 reserved owner-private names，同时保留 Git 历史与七个正常 task-work
evidence paths，并强制所有 downstream evidence 按 current task-work 重新建立。实现与
Issue #118、approved planning、Docs SSOT、Interface 1.3 private-state boundary、#105
transaction semantics、#116/#117 ownership、#119/#132 scope 边界一致。

未发现 open current-scope finding，Lint、适用 TypeCheck、完整 tests、package/eval、
distribution/OOTB 与 exact-stream integrity 均通过。建议 Phase 2
typed exit=`passed`，`implementation_required=false`。

下一步必须由主会话记录本 checker completed event，运行 fresh `guru-check-task`
recorder/checker，创建新 task commit，执行独立完整 Branch Review，重新取得 #116
`ready`，再生成并展示新的 immutable closeout plan/digest。新 confirmation 前禁止
push、PR mutation、archive、Ready、merge 或 Issue mutation。
