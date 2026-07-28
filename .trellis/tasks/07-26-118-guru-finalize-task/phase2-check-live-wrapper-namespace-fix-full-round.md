# Issue #118 live public wrapper Namespace 修复 Phase 2 全量检查报告

## 检查完成

### 检查身份与边界

- 角色：独立 Phase 2 `trellis-check` reviewer。
- Reviewer：`/root/issue118_live_wrapper_fix_phase2_check`，未参与本轮实现。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Checked HEAD：`d420a6842eca05bd0bf7472bdf06e3b519bace5f` 加当前完整 dirty/untracked task delta。
- Full committed range：`origin/main...d420a6842eca05bd0bf7472bdf06e3b519bace5f`，
  541 paths，81273 insertions，4767 deletions。
- 当前修复 delta：3 files，150 insertions，3 deletions。
- Finding inventory：P0=`0`、P1=`0`、P2=`0`、P3=`0`。
- Phase 2 semantic recommendation：typed exit=`passed`，consumer=
  `skill:guru-create-task-commit`。

Workspace boundary validator 通过：expected workspace 与 actual repo root 均为上述 worktree；
source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` clean，
`suspicious_source_artifacts=[]`。Planning approval checker exit `0`，typed exit=`approved`，
planning approval artifact SHA-256 为
`1bcc7712aa1c8a74f72ecfa4a90d8384d77fbd7a6ed95f65714737ffa600c9c6`。
`check.jsonl` 只有 seed row；按合同 fallback 使用批准的 planning artifacts、匹配的
workflow/preset/docs specs 与完整实现证据，该缺口不阻断。

本 reviewer 未修改 implementation、durable docs、spec、planning、ledger、publication、
review 或 finalization gate；只新增本报告与同轮 command evidence。未调用
`record-phase2-check`，未 commit、push、创建/修改 PR、archive、Ready、merge、deploy、
production write 或修改 GitHub Issue。

### Live authority 与 scope 复核

- Issue #118 为 OPEN；accepted-current authority 仍为 comment `5045036678`。
- #115、#119、#132 为 OPEN；#105 为 CLOSED/COMPLETED。
- Close scope 仅为 #118；#115 保持 related，#119/#132 保持 follow-up，#105 transaction
  semantics 保持不变。
- 本轮没有修改 Finish-family global entry/order、upstream overlay、官方 `task.py` 或 Issue
  mutation 行为。
- 恶意伪造/篡改、并发 finalizer、锁、TOCTOU、新 fault injection、crash consistency 与跨
  OS atomicity 仍为明确 out of scope。

### 已检查文件

- Planning：`prd.md`、`design.md`、`implement.md`、planning approval、live authority 与 issue
  scope ledger。
- Handoff：`implementation-handoff-live-wrapper-namespace-fix.md`、完整 implementation/check
  assignment recovery chain 与既有 review/gate 历史。
- 当前实现：canonical/dogfood `guru_team_trellis.py` 与 canonical
  `test_guru_team_trellis.py`。
- Runtime：完整 Guru runtime suite、#105 `CloseoutTransactionContractTest`、fresh isolated
  wrapper fixture、expected-exit boundary。
- Public package：`guru-finalize-task`、#116/#117 consumer edges、Interface 1.3 graph、source/
  installed public wrappers、shared/Codex/Claude/Cursor packages 与 corpora。
- Distribution：registry、manifest、preset installer、ownership、overlay drift、canonical/
  dogfood/platform parity 与 clean throwaway install/update/reapply chain。
- Durable SSOT：package contract、`.trellis/spec/workflow/**`、repository/preset/workflow
  README，以及 `design.md` 的唯一 Docs SSOT Plan。
- Protected surfaces：workflow Markdown、upstream `trellis-finish-work` family、preset overlay、
  official `.trellis/scripts/task.py`、CI/CD、container、K8s、DB migration、Makefile 与 deploy
  paths。
- Complete scope：完整 committed range 与全部 current dirty/untracked paths，不限于最新三文件。

### 实现语义复核

原 normal-path defect 是 public wrapper parser 生成的 `argparse.Namespace` 不含 private
closeout 字段，而 owner checker 复用 `prepare_closeout()` 时直接访问
`finish_summary_index_file`，导致 `AttributeError`，无法形成合法 typed exit。

当前实现新增 `finalization_public_wrapper_checker_args()`。该 helper 复制 public args，先把
checker-private 参数设为空；仅当 exact task-local `closeout-plan.json` 是安全 regular file 且
通过 immutable plan validator 时，才从 plan 与固定 task-local
`finish-summary-index.json`、`pr-body.md` 重建 repo/base/remote/title 与内容 locator。Public
CLI、input schema、public DTO 与跨 Skill projection 均未新增 private 字段。

`cmd_invoke_stage0_skill()` 只把该 private Namespace 传给 finalization owner checker。真实旧
gate probe 不再出现 `AttributeError`，而是返回结构化 `owner_result_not_checked`。Direct checker
明确报告 `plan identity mismatch`、`current facts mismatch` 与 route `plan_ref` mismatch；这是
source drift 后旧 plan/gate 的预期 freshness fail-closed，当前修复没有放宽旧 gate。

Fresh isolated fixture 覆盖 verified/not-required re-entry 正向路径、arbitrary metadata 拒绝，
以及 initial no-plan 时 index/body 仍必须显式提供。4 tests 全部通过。因此修复同时关闭正常
re-entry crash，并保留 initial preview/recorder 与 stale-gate 边界。

### 十项 adequacy review

1. `requirements`：passed。Live authority、approved planning 与 close-only-#118 ledger 一致。
2. `design`：passed。Private Namespace reconstruction 符合 single engine 与 owner-private state
   设计，没有建立第二套 transaction implementation。
3. `implementation`：passed。Canonical/dogfood runtime byte-identical；helper 只从 validated
   plan 与固定 task-local files 重建 checker 输入。
4. `tests`：passed。Fresh fixture、runtime、transaction、Skill graph、packages、wrappers、preset、
   ownership 与 throwaway chain 完成。
5. `docs_ssot`：passed。Strategy=`ssot_first`；本补丁恢复现有 owner-private wrapper contract，
   `no_docs_update_needed`。
6. `cross_layer`：passed。Public I/O、consumer projections、actual-exit selection 与 owner-private
   boundary 不变。
7. `compatibility`：passed。#105 ordering、Interface 1.3 profiles/exits、#116/#117 edges、workflow
   markers `12/46/27` 与 protected surfaces 不变。
8. `deployment_and_operations`：passed。无 dependency、CI/CD、container、K8s/Kustomize、DB
   migration、Makefile、deploy 或 production-write 影响。
9. `agent_recovery`：passed for semantic handoff。Implementation agent completed；主会话应在
   terminal handoff 后记录本 checker completed event。
10. `verification_completeness`：passed。完整 scope、normal-path reproduction、fresh positive/
    negative fixture、full regressions、distribution 与 clean installation 均已覆盖；Claude 401
    被明确保留为外部 residual，没有冒充 pass。

### 已修复问题

- 文件：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、
  `.trellis/guru-team/scripts/python/guru_team_trellis.py`、
  `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
- 问题：Public wrapper 把缺少 checker-private closeout 字段的 parser Namespace 直接交给 owner
  checker，真实 content-pushed re-entry 触发 `AttributeError`。
- 修复：当前 implementation diff 通过 validated immutable plan 重建 checker-private Namespace，
  并增加 real wrapper re-entry 与 initial-no-plan fail-closed regressions。本 reviewer 未修改这些
  文件；全量复核确认问题已关闭。

本轮未发现需要 reviewer 自修复的额外 code、schema、config、docs 或 test 问题。

### 未修复问题

- Claude live native case 返回 `execution_error`，transcript 为本机 CLI HTTP 401
  `Invalid API key`。这是外部认证 residual；input protocol 与 package graph 有自动验证，但
  Claude live semantic case不得描述为通过。
- Cursor live case返回预期 stable `unsupported`，未声明 semantic pass。
- 旧 plan `closeout-plan:59ce5a04...`、旧 finalization gate、旧 Phase 2、commit/review/
  publication/finalization evidence 均已因当前 source/task delta stale，不得复用。
- Exact pushed-ref verification 及后续副作用仍由 #117/#118 owner gate执行，本 reviewer 未获得
  push/publication authority。

以上均不是 current-scope P0-P3 finding。

### 验证结果

- Lint：通过。JSON/schema/validator、Bash syntax、`py_compile`、overlay drift、ownership、
  parity、protected/deploy no-diff、`git diff --check HEAD` 与 task validate 均通过。
- TypeCheck：通过适用检查。仓库无独立 configured static type checker；changed Python
  `py_compile`、schema/interface validators 与 full runtime tests 通过。
- Tests：通过。Runtime full `627 passed, 13 skipped`；#105 transaction matrix `105 passed`；
  Skill/package graph `180 passed`；#116/#117/#118 contract set `33 passed`；expected-exit
  boundary `3 passed`；preset `45 passed`；ownership `9 passed`。
- Fresh focused fixture：`4 passed`，覆盖 verified/not-required、arbitrary metadata rejection 与
  initial no-plan explicit-input gate。
- Source/installed validators：通过；13 active Skills、52 external exits、workflow markers
  `12/46/27`、sidecars/conflicts `0`。
- Source/installed shared real wrapper：各 `8/8 passed`，六 exits 与 verified/not-required
  re-entry 全覆盖。
- Codex live：trusted-root case passed；Cursor live：预期 `unsupported`；Claude live：外部 401
  residual，未计为通过。
- Package parity：shared/installed/Codex/Claude/Cursor bytes 一致；corpus SHA-256
  `07603a307748e067ea316a03b0dcb6ecf128b114fea680ea2b3e5dd21df4dfb4`。
- Clean throwaway：terminal rc=`0`。使用 exact branch workflow source 与 current local
  canonical preset payload，覆盖 initial install/reapply、official `trellis update`、managed
  hashes、`.new/.bak` recovery、零 sidecar、四平台分发、installed wrapper 与 closeout recovery。
- 临时 root `/tmp/guru-118-phase2.3qVvl2` 已用 exact depth-first delete 清除并确认不存在。

### 证据交接

- 阶段二：覆盖 live authority、approved planning、完整 committed range、全部 current delta、
  implementation handoff、normal-path reproduction/closure、runtime、tests、public wrappers、
  platform packages、distribution、install/update/reapply、ownership、protected boundaries、
  security/deploy 与 hygiene。P0/P1/P2/P3=`0/0/0/0`，十项 adequacy 全部 passed。本报告与
  同轮 JSON 可支撑主会话生成 fresh `phase2-check.json`；recorder 必须绑定届时 current
  artifacts、completed checker lifecycle 与 repository snapshot。
- Docs SSOT：plan strategy=`ssot_first`，task durable delta 已合并且 current；本修复为
  `no_docs_update_needed`，handoff/Phase 2 reports 属于 task-history-only content。#119/#132 与
  exact pushed-ref verification 保持 follow-up/current-finalization limitation。
- Branch Review：本轮不是 Branch Review，且未修改 `review.md` / `review-gate.json`。Fresh
  task commit 后必须重新执行完整 `origin/main...HEAD` independent Branch Review，再执行
  publication review 与新 immutable closeout plan/digest confirmation。
- 安全与部署：未发现 secret、credential、signed URL、客户数据或 raw provider payload；无
  dependency、CI/CD、container、K8s、DB migration、Makefile、deploy 或 production write 影响。
- Structured residuals：Claude 401、Cursor unsupported、旧 evidence stale、exact pushed-ref
  verification pending；均已分类为非当前 finding，且未夸大验证状态。

### 结论

Live public wrapper Namespace defect 已在受支持的正常 re-entry 路径上关闭；stale owner gate
仍按 objective identity/current facts/route binding fail closed。实现与 Issue #118 authority、
approved Docs SSOT、Interface 1.3 private/public boundary、#105 transaction semantics 以及
#119/#132 ownership 一致，完整回归与安装/更新链通过，没有 open P0-P3 finding。建议 Phase 2
typed exit=`passed`。

主会话下一步必须先记录本 checker completed event，再运行 Phase 2 recorder/checker、fresh task
commit、独立 Branch Review、publication review 与新的 immutable finalization confirmation；旧
plan、gate、confirmation 和后续 evidence 均不得复用。

本报告和 command evidence 的最终 SHA-256、bytes 与 lines 由 terminal handoff 提供，避免正文
自引用。
