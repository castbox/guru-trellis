# Issue #118 最终实现交接

## 1. 身份与证据边界

- Repository：`castbox/guru-trellis`。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- 已审实现 HEAD：`4847bfb8763483b4648915ce1da918cdfb24a678`。
- 已审 committed range：`origin/main...4847bfb`，467 个路径。

本文件独立汇总 approved planning、三份历史 implementation handoff、post-finding Phase 2、
Branch Review、Issue Scope Ledger 与当前 publication/finalizer contracts。它只是一份
human-readable task-history handoff，不替代任何 owner recorder/checker，也不授权 semantic
pass、publication readiness、recovery route 或外部副作用。

当前证据绑定如下：

- `planning-approval.json`：`typed_exit=approved`，
  `facts_sha256=9d0d14bada5d4990a3f62402bdb5b28275fd1c7bf20476cdd01f1145defbeb70`。当前
  `prd.md`、`design.md`、`implement.md` SHA-256 分别为
  `770e27527c6b65496d6a68380d42addcc5dc39d3ad5b5161d0172a15aac19bd9`、
  `a9d8777afeaa5a880b8bcdba016bd7981be0286fe130d577c4ef6f8a9b39d4b5`、
  `d26bb6137afa4ae8a5b8b1e3859d74ecb312b03975043f09013712e3261e09a8`，与批准记录一致。
- `phase2-check.json`：artifact SHA-256
  `18ee2866f3b7f4fd361f6cc5b8f5be4b32cd5919f8606f91fa74b37f49cb18e9`，
  `typed_exit=passed`，
  `facts_sha256=59520187e1d1c95da2ca63759779bedfc6d9348640f6968d19af368e8cd93aca`。该 gate 的
  repository snapshot 如实记录 `5695f7a` 加未提交 finding fix；fix 随后作为 `4847bfb`
  提交，不能把 Phase 2 snapshot 误述为直接生成于 `4847bfb`。
- `review-gate.json`：绑定 `head=4847bfb8763483b4648915ce1da918cdfb24a678`，
  `review_intent=fresh_final_review`，`typed_exit=passed`，`findings=[]`，
  `facts_sha256=802d213f494b981d2174e337006c18dcbbda4113e23f87ad56c803d9e6101974`。

## 2. 最终实现

### 2.1 公共 Skill 与 I/O

- 新增 active 公共 closed-loop Skill `guru-finalize-task`，
  `judgment_mode=semantic`，使用 forward behavior、AI Review Gate、条件式精确 human
  confirmation、recorder/validator、single typed exit 五阶段 profile。
- Interface 1.3 使用六个 distinct public input profiles：`publication_ready`、
  `verification_verified`、`verification_not_required`、`same_plan_resume`、
  `reprepare_preview`、`standalone_finalization`。
- 六个 public outputs 统一使用 `exit_id`：`verification_required`、
  `publication_review_stale`、`resume_finalization`、`reprepare_required`、
  `published`、`blocked`。每个 exit 使用独立 closed schema、example、唯一 consumer 与
  thin deterministic projection。
- #116 `ready` 与 #117 `verified|not_required` 只投影 target 直接消费的最小 seed。
  `reprepare_required` self re-entry 的 producer seed 精确为 `task_ref`、`reason_code`；
  fresh intent/context 只来自 target-owned authoring fields，runtime 不合成 AI intent。
- Package closure 为 13 active Skills / 52 external exits；验证后的 global marker closure
  保持 12 invokes / 46 exits / 27 targets。Finalizer package 已 active，但 registry 的
  `workflow_integration_state=deferred`；#119 仍独占 global Finish invocation/order。

### 2.2 语义与确定性边界

- `guru-finalize-task` 独占 plan、scope、readiness、recovery route、finding、revision action
  与 confirmation 充分性判断。
- #105 closeout engine 仍是唯一 deterministic transaction substrate，负责 immutable plan、
  reviewed content push、verification boundary、唯一 Draft PR、final projection、official
  archive transaction、三方 HEAD equality 与 draft-to-ready。
- Package scripts 只做 executor、validator、recorder；不判断 publication readiness、Issue
  close scope、Docs SSOT、安全/部署结论或 semantic pass。
- `closeout-plan.json`、publication/verification evidence、PR/archive/recovery facts、
  digest/path/blob/HEAD facts 与内部 transaction states 全部 owner-private。内部
  `prepared`、`content_pushed`、`evidence_pushed`、`draft_bound`、
  `projection_validated`、`archive_moved`、`archive_pushed` 没有暴露为公共 Skill、
  public DTO 或用户命令。
- Production eval 执行真实 public wrapper，先从 actual `exit_id` 选择 per-exit schema，再
  断言 `expected_exit`；`expected_exit` 不进入 adapter/native request。

### 2.3 事务与 recovery

- 第一次副作用或 plan 改变前，side-effect-free preview 展示 immutable plan bytes、完整
  side effects 与 `closeout_plan_digest`；formal execution 在副作用前重建并校验相同
  bytes/digest。
- Verification route 严格位于 reviewed content push 之后、PR/archive 之前；re-entry 只消费
  同 task/plan/reviewed HEAD 的 #117 owner-checker current evidence。
- Draft identity、final summary、single archive metadata transaction、local/remote/PR HEAD
  equality 与 ready 后零 repository write 均由同一 engine 保持。
- Recovery 对外只使用六个 public exits；same-plan continuation、cross-month reprepare、
  stale publication review、terminal published 与 blocked identity/path/HEAD 情形保持封闭。

## 3. Finding 闭环

### 3.1 Round 2

- `F-ROUTE-01`：pre-archive `published` 必须拥有同 task/plan/reviewed HEAD 的 #117
  `verified|not_required` owner evidence；只有 objective committed recovery state 可以使用
  已继承证据继续。
- `F-DTO-02`：移除空 `route.output` truthiness bypass。只有 pre-executor `published` 可以
  保存 exact private marker；executor 完成后重新按 public schema 校验内存 DTO。

### 3.2 Round 3

- 关闭 `F-RECOVERY-03`、`F-MATERIALIZATION-04`、`F-LOCATOR-05`、
  `F-IDENTITY-06`、`F-STATE-07`。
- Finalizer-only #117 augmentation 绑定 immutable plan、active/archive locator、repository、
  evidence allowlist/commit 与 exact archive transaction；generic #117 checker 未放宽。
- `published` gate 从 pre-executor 到 archive 只持久化 private marker；public wrapper 只在
  terminal archive + ready PR facts current 时在内存物化 DTO，`task_ref` 使用 immutable
  archive locator。
- `verification_required.repo_ref` 绑定 immutable plan repository；same-plan resume 的合法
  objective states 收敛，`prepared`、reprepare、stale 与 terminal ready 不得误入。

### 3.3 Round 4 与最终 HEAD

- 历史 P1 `F-FINAL-LEGACY-01` 已由 commit
  `4847bfb8763483b4648915ce1da918cdfb24a678` 关闭。
- 对 #105 engine 合法持久化的同月 partial plan，finalizer 可执行一次 exact、plan-bound、
  owner-private gate takeover。Preview/recorder/checker 在 formal transition 前保持 predecessor
  plan bytes；formal transition 重新校验 predecessor plan/state、同月、HEAD/commit state、
  augmented digest 与 exact gate 后，才替换 plan/readiness。
- Takeover 只运行一次；generic #105 对该 gate 和任意额外 artifact 继续 fail closed。
  Cross-month reprepare、public DTO、#105 既有 transaction ordering/failure matrix 未改变。
- Ownership stable-facts acceptance assertion 已同步；validator、registry ownership、frozen
  overlay inventory 与 #132 migration semantics 未改变。

## 4. Docs SSOT

- 批准策略为 `ssot_first`。
- Durable implementation inputs 为 finalizer step-local contract，以及
  `.trellis/spec/workflow/skill-package-contract.md`、`workflow-contract.md`、
  `companion-scripts.md`、`quality-guidelines.md`；task `prd.md`、`design.md`、
  `implement.md` 提供 approved task delta。
- Durable delta 已合并：active package 13/52、target-owned authoring handoff 12、deferred
  global marker closure 12/46/27、owner-private state、single #105 engine、verification/
  materialization/recovery contracts 与 #119/#132 ownership boundary。
- Round 3 先更新 finalizer-specific durable contracts 再同步 code/tests。Round 4 same-month
  takeover 实现既有 partial-recovery、private-gate ownership、generic strictness 与 extra-path
  fail-closed 合同，没有改变 public I/O、global route、install inventory 或 navigation；
  post-finding Docs SSOT 结论为 `no_docs_update_needed`。
- Finding 复现、fixture 调整、sidecar 处置、各轮 transcript 与本文件属于 task history，
  不复制到 durable behavior SSOT。

## 5. 验证汇总

Post-finding Phase 2 typed exit 为 `passed`，open P0/P1/P2/P3 均为 0：

- Focused takeover 4 passed；`CloseoutTransactionContractTest` 93 passed。
- Runtime full 615 passed、13 skipped；Skill packages 178 passed；preset 45 passed；
  finalizer package 4 passed；ownership regression 9 passed。
- Installed shared real-wrapper production eval 8/8 passed，覆盖六 exits 与 verified/
  not-required branches。
- Source/installed package validation 为 13 active、0 planned、0 legacy；installed 2644
  managed files，0 removal/conflict/sidecar。
- 隔离的 production-dispatch probe 按 preview -> record -> check -> execute 顺序通过；formal
  takeover 后 state=`content_pushed`，重复 takeover 不再触发。该 fixture 证据不是目标仓库
  的真实 publication side effect。
- Clean throwaway exit 0，覆盖 marketplace discovery、preset install/reapply、official
  `trellis update`、managed hash、`.new/.bak` recovery、all-platform distribution、contract/
  eval/wrapper discovery 与 installed closeout recovery。
- Canonical/installed/shared/Agents/Codex/Claude/Cursor package bytes 与 modes 一致，scripts
  executable；Shared/Codex/Claude/Cursor corpus byte-identical。Codex trusted-root、Claude
  input protocol、Cursor documented unsupported/unavailable 与 shared parsing 均有覆盖。
- Bash syntax、Python compile、JSON/schema validators、task validation、ownership、dogfood
  overlay drift、`git diff --check`、no-write assertion 与 final cache/sidecar hygiene 通过。

Branch Review 覆盖 `origin/main...4847bfb`：

- Round 5 从 Round 1/2 original finding owner 建立 direct fresh-agent closure。
- Round 6 是最后、current、fresh、zero-finding final review；focused takeover/cross-month
  6/6、transaction 93/93、finalizer 4/4、wrapper 8/8、platform protocol 2/2 通过。
- Round 6 raw report SHA-256 为
  `f2cbca7694d3bacdb4339103b8847a32839de4d49a3c0ac3426ee1dae821b689`；最终 gate
  `typed_exit=passed` 且 `findings=[]`。

## 6. Scope、安全与部署

- `close_issues` 只有 #118；#81、#115 只为 related；#119、#132 为 follow-up。
- #115 仍由 #119 combined acceptance 关闭；#119 拥有 global Finish family workflow/
  platform integration；#132 拥有 upstream overlay cleanup。
- Global workflow、dogfood workflow、upstream `trellis-finish-work` Skill/Command/Prompt、
  preset overlays 与 official `.trellis/scripts/task.py` 相对 base 无 diff；已完成 #105 的通用
  transaction semantics 未改变。
- 未纳入恶意 actor、伪造 artifact、攻击模型、并发 finalizer、锁、TOCTOU、额外 fault
  injection、偶发 crash consistency 或跨 OS 原子性。
- 未发现 token、credential、private key、`.env`、数据库 URL、签名 URL、客户数据或敏感
  provider payload 泄漏。
- 无 dependency、CI/CD、container、Compose、Kubernetes、Helm/Kustomize、DB migration、
  Makefile、服务部署或 production data write 变化；存在 additive package/runtime/schema/
  preset 安装升级影响，已由 clean install/update/reapply/all-platform evidence 覆盖。

## 7. Publication 与 finalization 当前状态

截至本文件生成时：

- 远端不存在 `feat/118-guru-finalize-task` branch，GitHub 不存在该 head 的 PR；#118、#115、
  #119、#132 均仍为 OPEN。
- `pr-body.md` 与 `finish-summary-index.json` 是尚未经过
  `guru-review-task-publication` semantic gate 的 Phase 3.6 初始候选；`pr-readiness.json`
  不存在，不能声称 `guru-review-task-publication:ready`。
- Issue Scope Ledger 只关闭 #118，但
  `remote_marketplace_verification.status=pending`、`commands_passed=false`；local unpublished
  throwaway 不替代 required pushed feature-ref verification。
- 未 push `4847bfb` 或 publication metadata tail，未创建/复用/更新真实 Draft PR，未执行
  task archive move、archive metadata commit/push、三方 HEAD equality、draft-to-ready、Issue
  mutation、deploy、production write、tag/release 或全局 npm/`node_modules` mutation。

`implementation-handoff.md` 本身是 `4847bfb` 之后新增的 task-history metadata，当前不在
已审 committed range 内，也不是 publication contract 的 closed metadata-revision allowlist
成员。若下游保留并提交本文件，HEAD、Phase 2、task commit、Branch Review 与 publication
binding 必须按各 owner contract 重新取得 current evidence；在该路径被正式处理前，不得以
既有 `4847bfb` gate 直接推导 publication `ready`。

## 8. 下游规则

1. 先把本 handoff 的 repository-status/HEAD 影响纳入 task-work 生命周期，并重新取得所需的
   current Phase 2、task commit 与 Branch Review evidence。
2. 仅以当前 `pr-body.md`、`finish-summary-index.json` 候选调用
   `guru-review-task-publication`；由该 Skill 独占十维 semantic review、metadata-only
   revision、recorder/checker 与 `ready|return_to_task_work|blocked` route。
3. 只有 current `ready` 才能进入 `guru-finalize-task`。第一次副作用或 plan 改变前必须展示
   immutable closeout plan、exact human digest 与完整副作用，并取得 mandatory confirmation。
4. 若 actual exit 为 `verification_required`，必须在 content push 后、Draft PR/archive 前由
   #117 owner 完成 pushed feature-ref verification；不得用本地 throwaway 代替。
5. 任何 task path、HEAD、diff、publication metadata、remote state、plan 或 owner evidence
   变化都必须由对应 owner checker 重新验证；本文件不能用于选择 semantic pass 或 recovery
   route。
