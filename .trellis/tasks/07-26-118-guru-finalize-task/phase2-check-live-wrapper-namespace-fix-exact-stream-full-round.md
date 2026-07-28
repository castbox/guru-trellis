# Issue #118 live public-wrapper Namespace 修复 Phase 2 exact-stream 全量检查

## 检查完成

### 检查身份与边界

- 角色：独立 Phase 2 `trellis-check` reviewer。
- Reviewer：`/root/issue118_phase2_exact_stream_check`；未参与本轮 implementation。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Checked HEAD：`d420a6842eca05bd0bf7472bdf06e3b519bace5f` 加 current working tree。
- Full committed range：`origin/main...HEAD`，541 paths，81273 insertions，4767 deletions。
- Current Namespace fix：3 paths，150 insertions，3 deletions。
- 正式 command evidence：128 records，128 份 exact argv，256 份 stdout/stderr
  digest+size；原始 streams retained。
- Finding inventory：P0=`0`、P1=`0`、P2=`0`、P3=`0`。
- 建议 typed exit：`passed`，consumer=`skill:guru-create-task-commit`。

Workspace boundary 通过：expected workspace 与 actual repo root 均为上述 task worktree；
source checkout 为 `/Users/wumengye/Documents/GoProjects/guru-trellis`，无 suspicious source
artifact。Planning approval checker 在检查前后均返回 `approved`，批准的 planning document
digests 与 `ssot_first` Docs SSOT Plan current。`check.jsonl` 只有 seed row，因此按合同 fallback
读取完整 planning、handoff、workflow/preset/docs specs、live authority、repository diff 与 tests。

本 reviewer 未修改 implementation、tests、spec、planning、ledger、agent assignment、旧 evidence、
publication/review/finalization artifacts；未调用 Phase 2 recorder，未 commit、push、创建/修改 PR、
archive、Ready、merge、deploy、production write 或修改 GitHub Issue。除本报告与同轮 JSON 外，
只在 `.trellis/.runtime/guru-team/issue118-live-wrapper-namespace-exact-stream-full-round/` 保留
gitignored exact capture streams/manifest/native transcript copy。

### Live authority 与 agent chain

- Issue #118 live state 为 OPEN；accepted-current authority comment `5045036678` 可读取且未漂移。
- #105 为 CLOSED；#115、#119、#132 为 OPEN。Close scope 只含 #118；#115 保持 related，
  #119/#132 保持 follow-up，#105 transaction semantics 保持 completed。
- Remote `main` 为 `7820a9ee...`；remote feature branch 为 `d420a684...`。当前 Namespace fix
  仍为未提交 working delta，本 reviewer 没有 push。
- 当前 feature branch 无 open PR；没有新 Draft PR、archive、Ready 或 Issue mutation。
- `agent-assignment.json` 的 schema/current HEAD/recovery chain validator 前后均通过；implementation
  agent与前一轮 checker均 completed，本 exact-stream reviewer 已 assigned，主会话应在收到本报告后
  记录其 completed event。
- 原 owner 输入
  `.trellis/.runtime/guru-team/finalization-inputs/issue118-publication-ready-d420.json`
  的 context digest 精确匹配 old finalization gate invocation identity，旧 gate probe 未使用人工近似输入。

### 已检查文件

- Planning：`prd.md`、`design.md`、`implement.md`、planning approval、provenance、live issue/comment。
- Handoff：全部 `implementation-handoff*.md`，重点为
  `implementation-handoff-live-wrapper-namespace-fix.md`；完整 implementation/check recovery chain。
- Current fix：canonical/dogfood `guru_team_trellis.py` 与 canonical runtime tests。
- Complete implementation：完整 541-path committed diff、12 个 current tracked dirty paths、5 个
  pre-artifact untracked paths、task metadata/review/publication/finalization历史。
- Runtime：完整 Guru runtime、#105 closeout transaction matrix、fresh exact wrapper fixture、
  owner package与 expected-exit boundary。
- Package graph：`guru-finalize-task`、#116/#117 producer-consumer edges、Interface 1.3、registry、
  schemas/examples/projections/private artifacts、production adapter/eval corpus。
- Distribution：canonical/installed/shared/Codex/Claude/Cursor parity、preset installer、ownership、
  overlay drift、repo-external replica apply 与 clean throwaway install/update/reapply/sidecar recovery。
- Durable docs：finalizer package contract、approved `.trellis/spec/workflow/**`、preset/docs specs、
  repository/workflow/preset README 与唯一 Docs SSOT Plan。
- Protected surfaces：global workflow activation、upstream `trellis-finish-work` family、preset overlays、
  official `.trellis/scripts/task.py`、CI/CD、container、K8s/Kustomize、DB migration、Terraform、
  Makefile 与 deploy paths。

### 实现语义复核

原 normal-path defect 是 public parser `argparse.Namespace` 不含 checker-private
`finish_summary_index_file` 等参数，`cmd_invoke_stage0_skill -> check_finalization_gate_result ->
finalization_preview_context -> prepare_closeout` 直接访问时抛出 `AttributeError`，无法形成 typed exit。

Current implementation 新增 `finalization_public_wrapper_checker_args()`：

- 复制 public Namespace，不修改 public input；
- 先把 finish summary/body/repo/remote/title 等 checker-private字段设为 `None`；
- initial no-plan 路径保持 explicit-input fail closed，不猜测 reviewed content；
- 只有 exact task-local `closeout-plan.json` 是非 symlink regular file 且通过 immutable plan
  validator 时，才从 plan 与固定 task-local `finish-summary-index.json`、`pr-body.md` 重建 private args；
- 只把 private copy 传给 owner checker，public schema、DTO、CLI、producer/consumer projection均不变。

使用原 exact D420 input 的 live old-gate probe 现返回结构化
`owner_result_not_checked`，无 `AttributeError`/`Traceback`。Direct checker 的错误集合精确为：

- `task finalization gate plan identity mismatch`
- `task finalization gate current facts mismatch`
- `Task finalization route output plan_ref does not match current facts.`

这证明 Namespace crash 已关闭，current source/task drift 仍使 old plan/gate fail closed，没有放宽
freshness。Fresh focused fixture 5/5 通过，覆盖 prepared gate positive、arbitrary metadata rejection、
workflow `verified`、standalone `not_required` 与 initial no-plan explicit input。

### 十项 adequacy review

1. `requirements`：passed。Live authority、approved planning、close-only-#118 ledger 一致。
2. `design`：passed。Private checker Namespace 复用唯一 #105 engine，不形成第二套 transaction。
3. `implementation`：passed。Canonical/dogfood runtime byte-identical；helper 只消费 validated plan。
4. `tests`：passed。Focused、runtime、#105、package graph、owner edges、eval、preset、ownership、
   replica 与 throwaway 全部覆盖。
5. `docs_ssot`：passed。Strategy=`ssot_first`；latest correction=`no_docs_update_needed`，只恢复
   existing owner-private real-wrapper contract；handoff/report 为 task-history-only。
6. `cross_layer`：passed。7 profiles、6 exits、52 active external exits、actual-exit-first、public/private
   partition 与 #116/#117 projections current。
7. `compatibility`：passed。#105 ordering、legacy wrappers、workflow markers `12/46/27`、global
   Finish boundary 与 official archive script 无回归。
8. `deployment_and_operations`：passed。无 dependency、CI/CD、container、K8s、DB migration、
   Terraform、Makefile、deploy 或 production-write delta。
9. `agent_recovery`：passed。Implementation/check history closed；只待主会话记录本 reviewer terminal event。
10. `verification_completeness`：passed。完整 scope、exact old-gate、fresh positive/negative、full tests、
    source/installed wrappers、platform protocols、install/update/reapply 与 terminal hygiene均有 current streams。

### 已修复问题

- 文件：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、
  `.trellis/guru-team/scripts/python/guru_team_trellis.py`、
  `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
- 问题：Public wrapper 把缺少 checker-private closeout字段的 Namespace 直接交给 owner checker，
  content-pushed normal re-entry 抛出 `AttributeError`。
- 修复：Implementation agent 通过 safe validated immutable plan 重建 private Namespace，并增加
  positive/negative wrapper regressions。本 reviewer 未修改这些文件；独立复核确认 finding 已关闭。

本轮没有新增 reviewer self-fix，也没有 open current-scope finding。

### 未修复问题

- Claude live native representative case 的 runner rc=`0`，structured status=`execution_error`；transcript
  显示本机 CLI HTTP 401、0 input/output tokens、无 permission denial。Input protocol 已验证，但该外部
  authentication residual 不描述为 semantic pass。
- Cursor live representative case稳定返回 declared `unsupported`；不描述为 semantic pass。
- Exact pushed feature-ref marketplace verification仍是后续 #117 owner gate。当前 fix 未 commit/push，
  因此 local current-candidate throwaway不能替代 future pushed-ref verification。
- Old plan `59ce5a04...`、old finalization gate、旧 Phase 2/commit/review/publication/finalization evidence
  因 current source/task delta stale，不得复用。
- 完整 committed `git diff --check` 仍只命中 immutable Round 9 raw report line 203 trailing whitespace；
  current effective product/docs/spec/code/test/metadata diff check通过。该历史 raw evidence observation 已按
  current authority 资格化为 nonblocking `out_of_scope`，本轮不改写。

以上均不是 open P0-P3 current-scope finding。

### 验证结果

- Lint：通过。JSON parse、Bash syntax、Python compile、schema/interface/package validators、ownership、
  overlay drift、effective diff check、sensitive material scan与 protected/deploy no-diff均通过。
- TypeCheck：通过适用检查。仓库没有独立 configured ruff/mypy/pyright命令；changed Python compile、
  Interface 1.3 closed schemas、runtime/full tests提供适用静态覆盖。
- Focused Namespace fixture：5/5 passed。
- Runtime full：627 passed，13 skipped。
- #105 transaction matrix：105 passed。
- Skill/package graph：180 passed。
- Finalizer owner package：5 passed；#116/#117 owner packages：28 passed。
- Expected-exit boundary：3 passed；shared adapter parsing：2 passed。
- Preset installer：45 passed；upstream ownership：9 passed。
- Source/installed validators：13 active Skills、52 external exits、workflow markers `12/46/27`；installed
  managed files 2659，sidecar/conflict/removal=`0/0/0`。
- Source/installed shared real wrapper：各 8/8 passed，六 exits 与 verified/not_required均覆盖。
- Codex live：passed，trusted Git root 与 repo-external execution root精确授权，trace 末事件为真实
  `invoke.sh` 且 rc=`0`，native request不含 `expected_exit`。
- Claude live：外部 401 residual；Cursor live：预期 unsupported。
- Package parity：canonical/installed/shared/Codex/Claude/Cursor bytes 与 corpus一致。
- Dogfood replica：`--all-platforms` apply、installed validator、overlay drift、runtime/package parity通过，
  sidecars=`0`。
- Clean throwaway：rc=`0`，804518 ms；覆盖 exact feature branch workflow source、local current payload、
  initial install、official update、reapply、managed hashes、`.new/.bak` recovery、platform distribution、
  installed wrapper/recovery；terminal managed/sidecar/conflict=`2659/0/0`，Namespace runtime installed parity通过。
- Exact stream：128 command records的原始 stdout/stderr全部 retained；逐条 records携带 exact argv、
  exit code、SHA-256与字节数。10 条 probe/setup错误均有 superseding command并已关闭。
- Hygiene：repo-external native/throwaway/replica roots已精确删除；repo caches/sidecars清零；source checkout clean。

### 证据交接

- 阶段二：覆盖 planning/provenance、live authority、完整 diff/dirty scope、handoff/agent recovery、
  Namespace normal path、runtime/#105/package/eval、platform、distribution、Docs SSOT、安全/部署与 hygiene。
  P0/P1/P2/P3=`0/0/0/0`，十项 adequacy passed；本报告与同轮 exact-stream JSON可支撑 fresh
  `phase2-check.json`，但本 reviewer没有调用 recorder。
- Docs SSOT：plan strategy=`ssot_first`；durable package/spec/README delta已在 committed scope；本次
  correction=`no_docs_update_needed`，task handoff/check artifacts只保留历史。#119/#132 与 pushed-ref
  verification保持 follow-up/current-finalization limitation。
- Branch Review：本轮不是 Branch Review。Fresh task commit后必须对完整 `origin/main...HEAD` 重新执行
  independent Branch Review，再执行 publication review与新的 immutable finalization plan/digest确认。
- 安全与部署：未发现 secret、credential、signed URL、customer data 或 raw provider payload；无 CI/CD、
  container、K8s、DB、Terraform、Makefile、deploy或 production write影响。

### 结论

Live public-wrapper Namespace defect 已在支持的 normal re-entry path上关闭；原 exact old gate 现在只因
plan/current facts/route binding stale而结构化 fail closed。Current implementation与 Issue #118 authority、
approved Docs SSOT、Interface 1.3 public/private boundary、#105 transaction semantics、#116/#117 edges、
#119/#132 ownership以及 clean install/update/reapply合同一致，没有 open P0-P3 finding。

建议 Phase 2 typed exit=`passed`。主会话下一步必须先记录本 checker completed event，再运行 Phase 2
recorder/checker、fresh task commit、独立 Branch Review、publication review与新的 immutable closeout
plan/digest confirmation；old plan/gate/confirmation/evidence不得复用。
