# #116 需求：实现 guru-review-task-publication 闭环 Skill

## 1. 目标

实现并激活稳定公共 Skill：

```text
guru-review-task-publication
```

该 Skill 是 Branch Review Gate 通过后、进入不可逆发布事务前的唯一 publication
semantic review owner。它负责审查当前 task 的交付结果、Issue 关闭范围、PR body、
Docs SSOT、安全与部署影响、验证声明、finish summary 语义索引以及 metadata tail，
并在 AI 已完成判断后记录和校验唯一的 `pr-readiness.json`。

该 Skill 不执行 commit、push、GitHub PR mutation、archive、draft-to-ready、remote
marketplace verification 或 finalization transaction。

## 2. 权威与优先级

### 2.1 当前权威

需求按以下优先级解释：

1. GitHub Issue [#116](https://github.com/castbox/guru-trellis/issues/116) 正文；
2. #116 的 2026-07-22 additive `accepted_current` 评论；
3. 已完成 #131、#144、#146 的 current Interface 1.3 合同；
4. 仓库当前 durable SSOT：
   `.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、
   `docs/requirements/**`、canonical workflow、registry 与 runtime；
5. 本 task 的 checker-passed Phase 0 artifacts。

2026-07-22 评论替代正文中与其冲突的 `exit` 字段、consumer input 与 eval
表述：所有 typed DTO 统一使用 `exit_id`，并新增双入口 authoring-seed 与真实
public-wrapper production eval 要求。其余 publication review、metadata revision
loop、`pr-readiness.json` ownership 与非目标保持有效。

### 2.2 Live baseline

- Intake base：`main` @ `bdc8f50bcd1e325aed331d4b01107b83ed8ee940`。
- Registry 当前为 10 个 active Skills、39 个 exits；
  `guru-review-task-publication` 仅是 planned row，canonical package 尚不存在。
- `guru-review-branch:passed` 已固定输出
  `exit_id`、`task_ref`、`reviewed_head`、`review_ref`，并以
  `planned_skill_input_seed` 暂存后三个业务字段。
- `guru-finalize-task` 尚未进入 registry；#118 后续拥有 finalization producer 与
  `publication_review_stale` output。
- 当前 `build_pr_readiness_snapshot()` 确定性写入 `ready=true`，并把
  `pr-readiness.json` 仅视为 publish-input snapshot；这不能证明 AI 已完成
  publication semantic review。
- `pr-body.md`、`finish-summary-index.json`、Issue Scope Ledger、Docs SSOT、
  Branch Review 与 finish-work deterministic publish bindings 已有可复用实现，
  本任务不得重建平行 artifact 或把它们放进 public DTO。

## 3. 功能需求

### R1. Active semantic Skill 与稳定身份

- 新增 active `guru-review-task-publication` package。
- Interface 使用 `schema_version=1.3`、`judgment_mode=semantic`，阶段固定为：

  ```text
  forward_behavior
    -> ai_review_gate
    -> conditional_human_confirmation
    -> recorder_validator
    -> typed_exit
  ```

- Workflow 与 standalone 使用相同 entry preconditions、review dimensions、
  artifact、pass 条件与 stale behavior；standalone 只改变入口来源。
- Skill id、profile id、exit id、schema id、runtime command 与 consumer id
  都是公共 API，不得由 runtime 推断或静默改名。

### R2. 双入口 public input 与 target-owned authoring seed

Package 独立拥有两个 closed structured profiles。

#### R2.1 `publication_review`

完整必填字段：

```text
profile
mode
task_ref
reviewed_head
review_ref
review_intent
```

- #131 `passed` 只提供 `task_ref`、`reviewed_head`、`review_ref`。
- #116 以 `skill_input_authoring_seed` 声明剩余字段
  `profile`、`mode`、`review_intent`。
- `seed_fields` 与 `authoring_fields` 交集为空，union 与 profile
  top-level required fields，merge 禁止覆盖。

#### R2.2 `publication_review_stale`

完整必填字段：

```text
profile
mode
task_ref
stale_reason
review_intent
reentry_context
```

- #118 后续只提供 `task_ref`、`stale_reason`。
- #116 本任务先发布 target schema、完整 input example、authoring example 与 eval
  fixture；#118 后续激活 producer edge。
- Runtime 不得代写 `mode`、`review_intent` 或 `reentry_context`，也不得从
  `stale_reason` 推断 semantic judgment。

`mode` 的 closed enum 为 `workflow|standalone`。`review_intent` 使用
package-owned closed enum，值固定为 `initial_review`、
`metadata_revision_review` 与 `stale_reentry_review`。

### R3. Private entry evidence

Runtime 按 `task_ref` 读取并客观校验以下 owner-private evidence：

- active task identity、task status、portable workspace boundary；
- intake repo/base/head/branch 与 current reviewed HEAD；
- `prd.md`、`design.md`、`implement.md`、`planning-approval.json`；
- `phase2-check.json`；
- `review.md`、raw review reports、`agent-assignment.json`、
  `review-gate.json`；
- `issue-scope-ledger.json`；
- approved Docs SSOT Plan 与实施后的 reconciliation outcome；
- current base-to-HEAD diff、working tree 与 metadata-tail facts；
- task-local `pr-body.md`；
- task-local `finish-summary-index.json`；
- current `pr-readiness.json`（仅在 re-entry 或 replacement 时）。

缺失、failed、stale、HEAD/hash/scope/workspace mismatch、Branch Review 后出现非
allowlisted metadata drift 时失败关闭。Public input 不携带这些 artifact bodies、
absolute paths、digest bundles 或 recorder state。

### R4. Publication semantic review dimensions

AI Review Gate 必须逐项审查：

1. `diff_outcome_consistency`：problem、outcome、changed behavior、affected surfaces
   与实际 diff 一致。
2. `issue_scope_closure`：primary/close/related/followup 与 delivery unit、
   acceptance、review coverage 一致；只有完整验收的 issue 才能 close。
3. `pr_body_quality`：标题与 body 为中文、具体、自包含、无占位或
   Trellis-session 依赖。
4. `validation_claims`：真实列出验证命令、结果、失败与未验证项，不泛化声称完整链路。
5. `branch_review_summary`：准确说明 review range、reviewer、findings 与 closure。
6. `docs_ssot_reconciliation`：strategy、updated authorities、merged delta、
   task-history-only、follow-up/限制真实一致。
7. `safety_deployment_impact`：secret、安全、配置、schema、CI/CD、容器、K8s、
   DB migration、Makefile、部署、回滚与兼容性判断完整。
8. `finish_summary_semantics`：future history search 所需语义字段完整，不混入由
   recorder 注入的 Git/GitHub/path/time facts。
9. `metadata_tail_integrity`：Branch Review 后仅有 allowlisted task metadata tail。
10. `artifact_binding_freshness`：task、ledger、gate、HEAD、body/index digest 与
    current invocation 完整绑定。

零 scanner error、changed-files 分类或空 findings 不能自动生成通过结论。

### R5. Finding 与内部 metadata revision loop

- 每个 finding 必须记录 stable ref、dimension、summary、scope basis、affected
  artifact/evidence、route class、status 与 closure evidence。
- 只需要修改 task-local `pr-body.md`、`finish-summary-index.json` 或 contract-listed
  `issue-scope-ledger.json` publication metadata 时，Skill 在内部完成：

  ```text
  finding -> AI revision -> reread/rescan -> fresh semantic review -> recorder/checker
  ```

- PR body、ledger、index 的 metadata-only revision 不形成 workflow exit。
- 修复需要改 code、test、durable docs、spec、workflow、schema、config、preset、
  CI/CD、deployment 或使 Branch Review stale 时，必须返回 task work。
- 外部条件、缺失权限或需要用户决策且不能由当前 task work 解决时返回 blocked。
- 任何 current-scope finding 不得降级成 observation 或 follow-up 来获取 ready。

### R6. 唯一 `pr-readiness.json` 与分层 ownership

- `pr-readiness.json` 是唯一 publication readiness gate/checkpoint；不得新增
  第二个 pass artifact。
- Artifact 必须分层保存：
  - AI-reviewed dimensions、findings、scope/impact conclusion、revision history、
    reviewer process evidence 与 typed conclusion；
  - deterministic task/HEAD/artifact/content bindings；
  - 由后续 finalization owner 写入的 optional deterministic publish-input layer。
- `pr-body.md` 与 `finish-summary-index.json` 仍是独立 task-local content artifacts，
  但不是 public handoff。
- Recorder 只能在 AI review 与所需 confirmation 已发生后记录结论；
  validator 只能验证 schema、hash、HEAD、allowlist、content binding、exit 与 freshness。
- 移除“deterministic builder 直接生成 `ready=true` 即代表语义审查通过”的语义。
- 现有 finish-work compatibility helper 只能在 checker-passed `ready` gate 上追加或
  校验 deterministic publish inputs，必须保留 semantic gate，不得覆盖它。
- `publication_ref` 是 ready DTO 中唯一 opaque identity/freshness token；它不得包含
  review narrative、findings、artifact path 或完整 digest bundle。

### R7. 三个 typed exits 与唯一 consumers

每个 exit 使用独立 schema 与完整 example：

- `ready`：

  ```json
  {
    "exit_id": "ready",
    "task_ref": "<task>",
    "reviewed_head": "<sha>",
    "publication_ref": "<opaque-current-ref>"
  }
  ```

  Consumer 为 planned `guru-finalize-task`。本任务需要在 registry 增加其 planned
  identity，并只发布 minimal seed；不定义 #118 的 target schema。

- `return_to_task_work`：

  ```json
  {
    "exit_id": "return_to_task_work",
    "task_ref": "<task>",
    "finding_refs": ["PUB-001"],
    "resume_target": "phase-2"
  }
  ```

  Consumer 为 `trellis-continue` 所属 workflow router。Router 必须要求 fresh
  implementation、Phase 2、commit 与 Branch Review 后再进入 publication review。

- `blocked`：

  ```json
  {
    "exit_id": "blocked",
    "reason_code": "<stable-code>",
    "remediation": "<next-action>"
  }
  ```

  Consumer 为显式 stop。

Unknown、missing、multiple、unmapped、schema/consumer mismatch 一律失败关闭。

### R8. Stale、replacement 与 re-entry

- `publication_review_stale` 不得绕过完整十维 semantic review。
- Current non-ready 或 stale owner evidence 的 replacement 必须绑定当前 task、
  current reviewed HEAD、旧 publication identity 与本轮 fresh content。
- Metadata-only re-entry 可在同一 Skill 内闭环；任何非 metadata drift 先返回 task work。
- Re-entry 不新增 parallel artifact、全局 journal、lock、transaction log 或
  adversarial tamper protocol。
- 普通正常流程中 recorder 生成错误 digest、executor 写错 payload 或 consumer 接受
  stale state 仍是有效 correctness bug；仅排除故意伪造/欺骗场景。

### R9. Script 边界

Script 职责限定为：

- 读取 Git、task 与 artifact facts；
- 校验 schema、required fields、hash、HEAD、path、allowlist、close/ref syntax；
- 记录 AI 已给出的 findings、conclusion、revision 与 confirmation；
- 检查 forbidden placeholder 与 deterministic structure；
- 基于 checker-passed owner result 选择实际 output schema 并做薄 projection。

Script 不得：

- 决定 close/related/followup；
- 判断 PR body、Docs SSOT、安全、部署或验证声明是否充分；
- 分类 finding 应内部修订、返回 task work 或 blocked；
- 根据 changed files 自动设置 ready；
- 用空 findings、预置模板、`--pass` 或测试成功冒充 AI review。

### R10. Real public wrapper 与 production eval

- Package 发布 dispatcher-only `scripts/invoke.sh`。
- Semantic case 使用 repo-local checker-passed owner result，真实执行 public wrapper。
- Actual exit 决定 per-exit schema；`expected_exit` 仅在 wrapper 返回后断言，
  不进入 adapter/native request、owner result 或 route selector。
- Canonical corpus 固定覆盖：
  - workflow initial ready；
  - standalone initial ready；
  - `return_to_task_work`；
  - blocked；
  - `publication_review_stale` re-entry；
  - PR body/ledger/index metadata revision 后 fresh pass；
  - metadata revision 后发现非 metadata drift 的 return path。
- Shared、Codex、Claude、Cursor 使用 byte-identical corpus，并验证 Codex trusted
  Git root、Claude input protocol、Cursor unavailable/unsupported 与 shared parsing。
- Eval 不替代 semantic review、metadata revision loop、transaction failure matrix
  或 clean installation verification。

### R11. Workflow、registry、distribution 与 upgrade

- 将 `guru-review-task-publication` 从 planned 激活为 Interface 1.3 active row。
- 将 #131 `passed` 的 `planned_skill_input_seed` 替换为 target-owned
  `skill_input_authoring_seed`，#131 output DTO bytes 不变。
- 新增 planned `guru-finalize-task` row，`ready` 只向它投影 minimal seed。
- Canonical workflow 只增加 mandatory invocation、三 exits、唯一 consumers、
  re-entry 与 fail-closed route；不得复制 Skill 内部十维审查或 revision loop。
- Existing `production-minimal-handoff-v1` 保持 3 Skills/11 exits 与原 activation
  identity，不把 #116 加入该 manifest。
- Active closure 更新为 11 active Skills、42 exits；每个 active profile/exit
  必须有 current eval binding。
- Canonical package、installed shared package、`.agents`、`.codex`、`.claude`、
  `.cursor` copies 必须由 preset 同步且 byte-identical。
- 不修改或 overlay upstream `trellis-finish-work` Skill/Command/Prompt；
  #119 继续拥有 finish-family integration，#132 继续拥有最终 overlay 收敛。
- Clean install、workflow marketplace、`trellis update`、preset reapply、executable
  mode、`.new/.bak`、dogfood drift 与 upstream ownership 都必须验证。

### R12. 正常运行边界与非目标

本任务只覆盖 honest-but-fallible 正常路径、常见操作失误、stale/mismatch 与普通
correctness/compatibility。Hash、digest 与 freshness 只用于版本绑定和过期检测。

明确不做：

- push、GitHub PR mutation、archive、commit、draft-to-ready、finalization；
- remote marketplace verifier 的远端执行；
- #118 `guru-finalize-task` 实现；
- #119 finish family integration；
- #132 upstream overlay removal/收敛；
- 修改 upstream Trellis、全局 npm、`node_modules`；
- 恶意伪造、对抗性输入、锁、TOCTOU、压力、额外 fault injection、偶发 crash
  consistency 或跨 OS 原子性加固。

## 4. Issue scope ledger

- `close_issues`：#116。
- `related_issues`：#115、#131、#144、#146。
- `followup_issues`：#81、#117、#118、#119、#132。

当前 task 不关闭任何 related/followup issue。后续 PR 只有 #116 可使用
`Closes #116`。

## 5. Docs 状态

- Docs state：`partial_docs`。
- 证据：durable workflow/preset/requirements docs 已完整描述 Interface 1.3、
  Branch Review、finish-work 与 planned publication boundary，但尚未定义 active
  `guru-review-task-publication`、双入口、三 exits、semantic gate schema 与
  `pr-readiness.json` 分层迁移。
- Strategy：`ssot_first`。完整 Docs SSOT Plan 由 `design.md` 唯一拥有。
- Middle-platform Knowledge Gate：不适用；本任务不涉及 go-guru、Unity/Flutter Guru
  SDK 或业务中台框架。

## 6. 验收标准

- [ ] AC1：`guru-review-task-publication` 以 Interface 1.3 semantic package 激活，
  workflow/standalone preconditions 与 pass 条件一致。
- [ ] AC2：`publication_review` 与 `publication_review_stale` 各有 closed schema、
  aggregate schema、完整 input example 与 authoring example。
- [ ] AC3：#131 seed 精确为 `task_ref/reviewed_head/review_ref`；stale seed 精确为
  `task_ref/stale_reason`；两个 authoring partition 均 disjoint、complete、no-overwrite。
- [ ] AC4：Runtime 能校验 planning、Phase 2、Branch Review、ledger、Docs SSOT、
  diff/working tree、body/index 与 workspace/current HEAD。
- [ ] AC5：十个 semantic dimensions、finding 分类、metadata revision loop 与
  AI Review Gate 均由 Agent 完成；script trace 不替代判断。
- [ ] AC6：`pr-readiness.json` 是唯一 gate；passing artifact 含真实 AI review、
  findings closure 与 current task/HEAD/content bindings，不再由 deterministic
  builder 无条件写 `ready=true`。
- [ ] AC7：现有 finalization compatibility helper 只在 passing gate 上追加 deterministic
  publish inputs，保留 semantic conclusion 与 opaque `publication_ref`。
- [ ] AC8：Metadata-only body/ledger/index revision 能内部闭环；任何 code/test/docs/
  spec/workflow/config/schema drift 返回 task work，并使旧 gate stale。
- [ ] AC9：`ready`、`return_to_task_work`、`blocked` 均使用 `exit_id`、独立
  schema/example、最小字段与唯一 consumer。
- [ ] AC10：`ready` 只向 planned #118 提供
  `task_ref/reviewed_head/publication_ref`；#116 不发布 #118 target schema。
- [ ] AC11：Stale re-entry 执行完整十维 review，不能复用旧 pass 或绕过 metadata
  freshness。
- [ ] AC12：Real-wrapper corpus 覆盖两 profiles、两 modes、三 exits、stale re-entry、
  metadata fresh pass 与 return path；actual exit 决定 schema。
- [ ] AC13：Shared/Codex/Claude/Cursor corpus byte-identical，且 native adapter
  不向 Agent 暴露 eval corpus或 private runtime source。
- [ ] AC14：Workflow 只保留 invocation/routes；#131 bridge 激活；
  `production-minimal-handoff-v1` 保持 3/11；live closure 为 11 Skills/42 exits。
- [ ] AC15：Canonical/installed/platform package、registry、extension inventories、
  managed assets、executable mode 与 public schema inventories一致。
- [ ] AC16：Package、runtime、source/installed validators、preset installer、
  upstream ownership 与 dogfood drift tests通过。
- [ ] AC17：Clean throwaway init/switch/install、`trellis update`、preset reapply、
  zero unresolved `.new/.bak` 与 standalone wrapper smoke通过。
- [ ] AC18：Docs SSOT reconciliation完成，task delta合并到 durable docs；
  remote verifier明确保留给 finish/publish gate且本任务不虚报已执行。
- [ ] AC19：独立 Phase 2 与 Branch Review覆盖需求、设计、runtime、schema、workflow、
  eval、distribution、docs、compatibility、安全/部署影响，current-scope finding为零。

## 7. 完成条件

AC1-AC19 均有代码、schema、测试、命令或独立语义审查证据；Docs SSOT
reconciliation 完成；task work commit 通过 `guru-create-task-commit`；当前完整
`origin/main...HEAD` 通过 `guru-review-branch`。随后由显式 finish entry 才能进入
publication review/finalization 链；本任务本身不执行发布副作用。
