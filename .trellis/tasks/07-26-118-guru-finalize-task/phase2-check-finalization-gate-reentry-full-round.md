# Issue #118 finalization gate re-entry 修复 Phase 2 全量检查报告

## 检查完成

### 检查身份与边界

- 角色：独立 Phase 2 `trellis-check` reviewer。
- Agent：`/root/issue118_phase2_finalization_gate_reentry_check`。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Checked HEAD：`c04ed1d7a816ac80217953bcf52f7a2a44b645d2` 加当前未提交
  finalization-gate re-entry runtime、tests、task evidence 与 handoff delta。
- Full committed range：`origin/main...c04ed1d7a816ac80217953bcf52f7a2a44b645d2`，
  532 paths，74550 insertions，4753 deletions。
- Current tracked delta：12 paths，1359 insertions，433 deletions；另有 3 个 task-local
  untracked handoff/review reports。本报告写入后只再增加本报告本身。
- Authority：live Issue #118 与 accepted-current comment `5045036678`；close scope 仍只包含
  #118。
- Finding inventory：P0=`0`、P1=`0`、P2=`0`、P3=`0`。
- Phase 2 semantic recommendation：typed exit=`passed`，consumer=
  `skill:guru-create-task-commit`。

Workspace boundary validator 通过：expected workspace 与 actual repo root 均为上述 worktree；
source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` clean，
`suspicious_source_artifacts=[]`。Planning approval checker 返回 `status=ok`、
`typed_exit=approved`，planning document digests current。

本 reviewer 未修改 product、durable docs、spec、runtime、tests、planning 或现有 gate；只新增
本 raw report。未调用 Phase 2 recorder/checker，未 commit、push、创建/修改 PR、archive、
Ready、merge、deploy 或修改 GitHub Issue。主会话必须在收到 terminal handoff 后记录本 checker
的 completed lifecycle event，随后才能生成新的 `phase2-check.json`。

### Live authority 复核

- Issue #118 当前仍为 open，正文继续要求 `guru-finalize-task` 独占 immutable plan、exact
  confirmation、content push、verification routing、唯一 Draft PR、projection、archive
  metadata transaction、三方 HEAD equality、Ready 与封闭 recovery matrix。
- accepted-current comment `5045036678` 继续要求 Interface 1.3、六个 `exit_id`、
  `reprepare_required` 的 `task_ref`/`reason_code` seed 与 target-owned authoring fields 分离、
  真实 public wrapper eval 及 actual-exit-first schema selection。
- #109、#112、#116、#117、#131、#144、#146 当前为 closed；#115、#119、#132 当前为
  open。远端 `main` 仍指向 `7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- `close_issues=[118]`；#115 只为 related umbrella；#119 持有 Finish family integration、
  combined acceptance 与 #115 closure；#132 持有 upstream overlay cleanup；#105 已完成事务
  语义不变。

### 已检查文件

- Planning 与 authority：`prd.md`、`design.md`、`implement.md`、`planning-approval.json`、
  live Issue/comment、issue dependency state 与 current ledger。
- Handoff/lifecycle：完整 implementation handoff/recovery chain、
  `implementation-handoff-finalization-gate-reentry-fix.md`、`agent-assignment.json`、Round 13/14
  raw review reports。
- 当前实现：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- Dogfood runtime：`.trellis/guru-team/scripts/python/guru_team_trellis.py`。
- Tests：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 与 finalizer、
  verifier、publication、Skill graph、preset、ownership suites。
- Public package：`trellis/skills/guru-team/packages/guru-finalize-task/**`、#116/#117 producer
  contracts、consumer bindings、schemas、examples、real wrapper 与 eval corpus。
- Distribution：canonical、`.trellis/guru-team`、Agents、Codex、Claude、Cursor package copies，
  preset installer、registry/manifest、ownership inventory、overlay drift 与 executable scripts。
- Durable SSOT：`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`.trellis/spec/docs/**`、
  package contract 与 repository/preset/workflow README surfaces。
- Protected no-diff：canonical/dogfood workflow Markdown、upstream `trellis-finish-work`
  Skill/Command/Prompt family、official `.trellis/scripts/task.py`、preset overlays。
- Complete effective scope：全部 532 个 committed paths与当前 15 个 pre-report dirty/untracked
  paths，而不是只检查最新两行 runtime 变更。

`check.jsonl` 只有 seed row；按 contract fallback 使用已批准 planning artifacts 和匹配的
workflow/preset/docs/quality specs。该缺口不阻断，planning approval 与 Docs SSOT Plan 均有效。

### 实现语义复核

`record-finalization-gate` 在首次 formal transition 前合法写入 exact task-local
`task-finalization-gate.json`。此时 closeout plan 尚未物化，publication readiness 尚无
`publish_inputs`。旧 prepared-state resolver 调用 generic publication checker，导致 honest
recorder -> checker 路径把 finalizer-owned gate 误判为 publication freshness drift。

当前修复只在以下三个条件同时成立时开放 existing finalizer augmentation：

1. plan 尚未 materialize；
2. readiness 不含 `publish_inputs`；
3. direct task-local gate 是 regular non-symlink file。

该路径传入唯一 gate locator 且 `require_plan=False`；gate 缺失仍调用 generic publication
checker，任意 additional/unowned metadata 仍因 exact status delta mismatch fail closed。新增
测试通过真实 `cmd_record_finalization_gate()` -> `cmd_check_finalization_gate()` 验证 exact
gate-only pass，并验证加入 arbitrary metadata 后抛出 `WorkflowError`。

本修复没有新增 public DTO、profile、schema、exit、consumer、route、state 或用户命令；没有
让 script 判断 plan、scope、readiness、recovery route、semantic pass 或 confirmation；没有
改变 verification owner、#105 transaction order、#119 global integration 或 #132 overlay
ownership。

### 十项 adequacy review

1. `requirements`：passed。Live #118 body/comment、approved planning 与 close-only-#118 ledger
   一致，未引入 #119/#132 或 excluded unusual scenarios。
2. `design`：passed。Prepared gate augmentation 复用现有 owner-private finalizer boundary；
   immutable plan、verification ordering、PR/archive/recovery 设计不变。
3. `implementation`：passed。Canonical/dogfood runtime byte-identical，exact gate-only locator、
   `require_plan=False` 与 generic fallback 的条件边界明确。
4. `tests`：passed。Focused、full runtime、Skill graph、package、preset/ownership、wrapper、
   adapter 与 clean throwaway coverage 全部完成；Claude live 401 被诚实保留为 residual。
5. `docs_ssot`：passed。strategy=`ssot_first`，outcome=`no_docs_update_needed`；runtime 修复使
   实现重新符合现有 durable contract，没有新的公共或持久语义。
6. `cross_layer`：passed。#116 `ready` 与 #117 `verified|not_required` 仍使用最小 DTO；
   owner-private gate/plan/readiness/verification/PR/archive/recovery facts 未进入 public handoff。
7. `compatibility`：passed。#105 compatibility behavior、六 exits、七个 distinct profiles、
   actual-exit schema ordering、protected upstream/global surfaces均未改变。
8. `deployment_and_operations`：passed。无 dependency、CI/CD、container、Compose、K8s、
   Helm/Kustomize、DB migration、Makefile、Terraform、production config/data/write 变更。
9. `agent_recovery`：passed for semantic handoff。实现 agent 已 completed；本 checker assignment
   current 且无 replacement/stale gap。主会话必须在 terminal handoff 后追加 completed event，
   recorder 再绑定该闭合 lifecycle。
10. `verification_completeness`：passed。所有 applicable repository checks 与 install/update
    gate 已执行；Claude credential 401 与 unpushed exact-ref verification是已界定、非阻断的
    外部/下游状态，不被误报为 pass。

### 已修复问题

- 文件：无 implementation file。
- 问题：最终上下文 checker 在 repo 内生成 ignored Python `__pycache__`/`.pyc`。
- 修复：只把本 reviewer 生成的 cache 移到 repo-external evidence root；终态扫描仓库内
  `__pycache__`、`.pyc`、`.pyo`、`.new`、`.bak` 为零。

未发现需要自修复的代码、schema、config、docs 或 tests finding。

### 未修复问题

- Claude live native case 返回 structured `execution_error`：HTTP 401 `Invalid API key`，
  input/output tokens 均为 0，`permission_denials=[]`。这是本机外部认证不可用，不是 public
  wrapper、corpus 或 adapter protocol defect；不得在 publication 中描述为 Claude live pass。
- Feature exact ref 尚未 push，remote marketplace/extension verification 尚未发生。这是
  正式 finalization 的预期前置状态；content push 后必须由 #117 owner route 验证 exact
  remote ref/HEAD，当前 Phase 2 不授权 push。
- 旧 `phase2-check.json`、task commit、Branch Review、publication review、immutable plan 与
  finalization confirmation 均早于当前 runtime/test/handoff/report delta。主会话必须重新执行
  这些 owner gates，不得复用旧 freshness 或旧 confirmation。

以上均不是 current-scope P0-P3 finding。

### 验证结果

#### Tests 与合同

- Focused prepared-gate re-entry：2/2 passed。
- Runtime full：626 passed，13 skipped。
- Skill package graph：179/179 passed。
- Preset installer + ownership tests：54/54 passed。
- Finalizer/verifier/publication package tests：33/33 passed。
- Expected-exit boundary：3/3 passed；测试确认 caller-selected `--exit ready` 被 CLI 拒绝，
  `expected_exit` 只在实际 wrapper 返回后断言。
- Source package validator：passed；13 active，0 planned，markers=12/46/27。
- Installed validator：passed；2659 managed，0 sidecar/removal/conflict。
- Source/installed shared real public wrapper：各 8/8 passed，六 exits 与 verified/not_required
  re-entry 均覆盖。
- Codex live trusted-root case：passed，actual exit=`publication_review_stale`。
- Cursor live case：stable `unsupported`，runner terminal exit 0。
- Claude live case：external `execution_error`/401，如未修复问题所述，不计为 pass。
- Task validate：passed，`All validations passed`。

关键 evidence hashes：

- Focused stderr SHA-256：`1dce85386c40491a292edd4f2f827dc57e25ab900f0d9b7f5122e3df9e4a82cf`。
- Runtime stdout/stderr SHA-256：
  `a6542af6fbdbaf4500ec5f371d9b52a88028c25d41c7779cd41b71b8bfe11a01` /
  `17cb6687341d68a75eb64dc8bf8fe40a0e1e1adb56c416575d8e2014e697164f`。
- Skill graph stderr SHA-256：`f2ab90b7c04a659b98436566cf6305876d3d8b58f64829481a4cd3d7c3a970e8`。
- Source/installed wrapper stdout SHA-256：
  `e121d8c561189ee53881b02ea121bd75992787b9882dc55f6cb6cd8e95cf03cf` /
  `91e8f36c235ac13147d4a58ac1b26e6b66a39398a301426a2c74147c33057fdc`。
- Expected-exit-boundary stderr SHA-256：
  `e73cd9d6e0774b6f359d96da37b9d54f7fef447a8e704fbb745a911f5b3495c2`。
- Interface audit stdout SHA-256：
  `43457b0898d792a4b537f4e6a8bfa7b5d7f0260689b712fd1bc87fc28e2afe60`。

#### Lint 与 TypeCheck

- Lint：通过 current dirty product/docs/spec/code/test `git diff --check`、JSON/interface audit、
  Bash syntax、source/installed validator、ownership、overlay drift 与 protected no-diff checks。
- Full committed `git diff --check origin/main...HEAD` exit 2，仅命中 immutable historical raw
  report `reviews/round-009-finding-closure.md:203` 的 trailing whitespace。修改该行会破坏已
  绑定 raw evidence identity；当前实现与本轮 task delta 无 whitespace defect。
- TypeCheck：通过适用门禁。仓库无独立 configured static type checker；canonical/dogfood
  runtime、tests 与 adapter `python3 -m py_compile` 通过。
- Changed Bash `bash -n`：通过；stdout/stderr均为空，SHA-256均为
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。
- Protected surfaces effective diff：空；deployment-impact scan：空；对应 stdout/stderr SHA-256
  均为 empty digest。

#### Distribution、安装与 update

- Canonical/installed/Agents/Codex/Claude/Cursor package `diff -qr` 全部 byte-identical。
- 六份 eval corpus SHA-256 均为
  `07603a307748e067ea316a03b0dcb6ecf128b114fea680ea2b3e5dd21df4dfb4`。
- Dogfood overlay drift：passed。
- Upstream ownership：passed；frozen/active=`43/43`，active Skills=13，planned=0。
- Clean throwaway terminal exit 0，覆盖 public workflow marketplace discovery、local unpublished
  current workflow sample、fresh init、preset install/reapply、official Trellis update、workflow
  preview/reselection、managed `.bak`、unknown edit `.new`、all-platform distribution、wrapper、
  closeout、ownership/drift 与终态 hygiene。
- Throwaway terminal message：
  `Verified public marketplace discovery plus local unpublished workflow sample`。
- Throwaway stdout：4165616 bytes，SHA-256=
  `2cca7aadc2a74ce0d6b4b273e65c4ca6af1116a0ba0854e19d1a725c0fdd6602`。
- Throwaway stderr：930 bytes，SHA-256=
  `d96b72c464e963f7a126772399f81bbf3dd1253eb8b0ad49b22344ab4f5b35e0`；
  仅包含 expected tests 与 Codex hook configuration notice，不是 verification failure。

### 证据交接

- 阶段二：覆盖 live authority、approved planning、完整 committed range、全部 current dirty/
  untracked task delta、implementation handoff、runtime、tests、public wrappers、platform adapters、
  distribution、install/update/reapply、ownership、protected boundaries、安全/部署与 hygiene。
  P0/P1/P2/P3=`0/0/0/0`，十项 adequacy 全部 passed。本报告可支撑主会话生成新的
  `phase2-check.json`；recorder 必须绑定届时 current dirty paths、本报告 digest 与 completed
  checker lifecycle。
- Docs SSOT：strategy=`ssot_first`，outcome=`no_docs_update_needed`。Durable docs 已拥有
  finalizer-private exact metadata augmentation、prepared route、generic checker strictness、
  unexpected-path fail closed 与 public/private boundary；本修复只恢复 runtime conformance。
  Task handoff/report 是 task-history-only content，没有待合并的 durable semantic delta；#119、
  #132 与 exact pushed-ref verification保持明确 follow-up/PR limitation。
- Branch Review：本轮不执行 Branch Review，也不写 `review.md`/`review-gate.json`。主会话完成
  新 task commit 后必须用独立 reviewer 覆盖新的完整 `origin/main...HEAD`，随后重新执行
  publication review 和新的 immutable closeout plan/digest confirmation。
- 安全/部署：无 credential、secret、signed URL、客户数据或原始 provider payload；无
  dependency、CI/CD、container、K8s、DB migration、Makefile、deploy 或 production write 影响。
- 残余：Claude live 401；feature exact ref 尚未 push。两者必须在后续 owner gate 中诚实
  处理，不得夸大为已验证。

### 结论

Finalization-gate prepared-state re-entry 修复与 Issue #118 accepted-current authority、approved
Docs SSOT、Interface 1.3 public/private boundary、#105 transaction semantics 及 #119/#132 ownership
一致。完整 regression、wrapper、distribution、install/update 与静态门禁均通过，没有 open
P0-P3 finding。建议 Phase 2 typed exit=`passed`。

主会话下一步必须先记录本 checker completed event，再重新执行 Phase 2 recorder/checker、
task commit、独立 Branch Review、publication review 与新的 immutable finalization
confirmation；旧 plan、gate 与 confirmation 不得复用。

本报告 SHA-256、bytes 与 lines 由写入后的 terminal handoff提供，避免正文自引用。
