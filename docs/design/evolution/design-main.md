# Guru Trellis Evolution Target Design

版本：`evolution-design-candidate-2026-08-29`；状态：`design_ready_for_delivery_planning` /
`fresh_design_review_passed` / `evolution_refactor_eligible`。本文件已从 current `requirements_ready_for_design` identity 重新承接
`REQ-REV-011..138`、`EVO-001..007`、`EVO-CAP-001..004`、`EVO-REQ-001..083`、
`EVO-NFR-001..033` 与 `TARGET-DELTA-001..013`。`EVO-DES-070..073` 分别拥有两阶段
Evolution eligibility、#312 original-worktree/base continuity、#311 installed publication terminal
continuity 与 standalone verifier failure evidence；它们与既有 `EVO-DES-001..069` 共同构成本轮 fresh
Design review candidate。该 target Design 不改变 selected-base current `.41` runtime 事实，也不授权实现或
发布；`.40` 仅为历史 comparison evidence。

## 1. System Boundary

- `EVO-DES-001`：产品边界是一次用户 invocation 从 admission 到唯一 terminal 的完整 lifecycle，
  包括 direct answer、new change、resume/history/disposition、distribution/release、两类 specialist
  与 stop；standard change 的 request-to-cleanup 是其中一条 route，不再冒充所有请求入口。
- `EVO-DES-002`：authority 分为三层：repository RDT/Architecture durable authority、task-owned
  contribution/planning projection、owner-private invocation/runtime state。三层只交换 identity、locator、
  version/status 与直接 consumer 所需的最小 result。
- `EVO-DES-003`：global workflow 是稳定 owner graph；Markdown 决定顺序与 route，semantic Skill
  完成判断，deterministic runtime 只执行/记录/校验客观事实。
- `EVO-DES-004`：官方 Trellis 提供 workflow/spec/skill/agent/hook/update provider；Guru Team 通过
  marketplace workflow、preset、Guru namespace packages 与精确 post-projection policy 扩展，不改
  upstream package source。
- `EVO-DES-005`：current as-built、target Design、implementation candidate 与 released candidate
  四种状态不可互相冒充。Design ready 不表示 runtime implemented；implemented 不表示 reviewed；
  reviewed 不表示 released。

## 2. Runtime Planes

| Plane | Unique owner | Durable boundary | Forbidden responsibility |
| --- | --- | --- | --- |
| Invocation admission | `guru-admit-invocation` | 默认 call/host-session-local；pending/blocked/resume 只使用 producer-owned host continuation，repository checkpoint 为 0 | 产品 route、文件 mutation、approval |
| Request routing | `guru-route-request` | 不持久化 route history | downstream semantic work、副作用 |
| Stock policy | `guru-maintain-stock-projection` | canonical policy + installed provenance；action recovery 使用 host continuation，或仅在 task current 时使用 same-Skill checkpoint | 产品 scope、finding、publication |
| Standard change | Phase-specific Guru Skills | task RDT contribution、task planning、必要 terminal history | parallel authority、legacy route |
| Repository RDT | `guru-maintain-requirements-design-test-ssot` | repository current/target/contribution | task planning 成为 repository authority |
| Architecture | `guru-maintain-architecture-baseline` | baseline/current + task contribution/ADR | schema/runtime 决定架构答案 |
| Provider/worker | caller-bound adapter/worker | 默认 result 直接返回 caller | scope、sufficiency、severity、route |
| Delivery/Release | exact route owner | provider terminal facts与最小 durable history | child gate 改选 route |
| Cleanup/history | cleanup/history owner | cleanup 后仍不可重建的 terminal identity/result | 删除 unrelated/retained authority |

## 3. Invocation Admission And Context

- `EVO-DES-006`：每条可能启动顶层 invocation 的 user event 先进入
  `guru-admit-invocation`。该 owner 以 host user-event identity、active lifecycle/owner/scope/candidate、
  wait/continuation facts 和 arrival sequence 判定 `lifecycle_bound`、`independent` 或
  `binding_blocked`。`binding_blocked` 只表示 lifecycle causality/identity 无法判定；已经建立独立
  invocation/envelope/receipt 后的 scope/owner/isolation boundary 无法判定，必须使用不同的
  `independent_request_isolation_blocked`。`lifecycle_bound` 必须产生 consumer-minimal
  `bound_event_ref`，它绑定该 host event 的 identity/session、current event content 与单调 arrival
  sequence；不得只传 sequence 后要求 current owner 从 host/ambient state 重新寻找这条消息。
- `EVO-DES-007`：bound event 不建立新 envelope/receipt。它由 current/earliest owner 分类为
  owner-local additive、material additive 或 override；Admission 只把
  `lifecycle_ref,current_owner_id,bound_event_ref,event_sequence` 交给 closed owner router，router再把
  `lifecycle_ref,bound_event_ref,event_sequence` 直接投影到该 owner 的 `lifecycle_intent_reentry`。
  只有旧 owner按 Requirements 完成停止、suspend 或远端收敛后，后续独立 invocation 才取得新
  identity/envelope/receipt。
- `EVO-DES-008`：independent event 先分配 `invocation_id`，建立一个 `context_envelope`，写入恰好一次
  admission receipt，再执行 isolation gate。无 active 或安全隔离直接继续；共享可变 scope/不可逆边界
  只有存在可观察下一进展时才 pending。每次 pending re-evaluation 恰好得到 progress refresh、safe clear
  或 `independent_request_isolation_blocked`；scope/owner/boundary 无法唯一解析、无进展、handle 失效或
  owner 不再可消费时也必须进入该独立 block。stop 只把 `continuation_ref,repair_input` 投影到 Admission
  的 `isolation_repair_reentry`，复用原 envelope/receipt 并重新判定 isolation，不得压入
  lifecycle `binding_blocked` 或重复 receipt。
- `EVO-DES-009`：`context_envelope` 是 owner-private closed object，逻辑 section 只有：
  `request`, `lifecycle_binding`, `authority_context`, `stock_policy_context`, `provider_context`,
  `implementation_context`, `dependency_versions`, `continuation`。section 按需产生；N/A 不读取正文。
- `EVO-DES-010`：envelope 在 admission、pre-route、pre-task、task-free 与 standalone 边界只能存在于
  当前调用栈或 host 的 current session/continuation 中；这些边界在 `.trellis/tasks/**`、
  `.trellis/workspace/**` 与 `.trellis/.runtime/**` 的 file mutation 均为 0。跨 user turn、provider unknown、
  isolation pending 或 exact recovery 只由 producer-owned host continuation 携带
  `invocation_id,context_revision,continuation_ref,repair_input` 中该 re-entry 必需的最小子集，并由 exact
  owner 结合 live authority 重建自己的 authorized view；continuation 缺失、stale 或不可唯一解析时进入
  既有 owner block/re-entry，不得静默创建 generic repository envelope file。只有 task 已存在且 exact
  Skill owner 的不可重建状态具有同 owner public-wrapper 这一直接 consumer 时，才可按该 Skill 既有合同
  使用 task-local ignored owner-private checkpoint；它不是 `context_envelope`，不得跨 Skill 共享或由下游
  consumer 读取，并在 current consumption、stale replacement 或 terminal 后由 owner 删除。任何载体均
  禁止写 authorization、完整 stdout/review history、可 live 重建的 Git/GitHub/Trellis facts 或全文 RDT。
- `EVO-DES-011`：public consumer 只接收 `invocation_id`、`context_revision` 与该 exit 的最小业务
  projection，不接收 envelope path/body/digest bundle。normal workflow 的 call-local
  `authority_context` 按 applicable repository RDT、Architecture Baseline/constitution/change contract、active
  task `prd.md`/`design.md`/`implement.md` 的稳定 locator/identity/order组织同一份已绑定 authority content，
  形成主要稳定 prefix；task 三件套只承载 task-local delta/projection，decision-relevant live facts、current
  delta 与 unresolved items 只进入最小变化 tail。Clarification 独占其中的 current requirement-delta/
  reviewed-design subprojection，RDT owner独占 repository RDT subprojection，Architecture owner独占 baseline/
  constitution/change-contract subprojection；Plan/Approval/Implementation/Check/Review/Readiness/Acceptance
  直接使用适用的同一 bound content view，而不是消费前一 owner 的摘要或 handoff。每个 source family只由其
  section owner完成一次首次 live content read；后续 semantic owner从 current stable prefix判断，不再次用
  tool全文读取同一 source。跨 turn host continuation 与允许的 active-task same-owner checkpoint 仍只保存
  可恢复 locator/identity 与最小 continuation，绝不保存 envelope 正文或全文 RDT。public edge与provider
  consumer只取得自己的 authorized minimal projection；这条最小 DTO
  规则不得把 semantic owner实际需要的 current authority正文替换成 producer summary。host/model/provider
  cache 命中、缺失或不可用都不得改变 authority、freshness、route 或 result。每个 semantic owner 直接据
  current prefix/tail 判断并执行，不消费 human-style assignment/signoff/transaction handoff 或
  already-current fact restatement。equivalent identity drift只刷新 projection，不重放 unchanged semantic
  review；dependency/material facts 变化才返回最早受影响 section 定向 reread，并只使该 section 与
  下游失效。consumer 的每个 required public input 必须由 selected exit 的
  `direct|select|rename|normalize` projection满足；repo/provider/checkout/plan/RDT/Architecture live facts
  若由该 consumer 自己拥有，则从 public input 删除并由 exact section owner提供。禁止 generic current
  frame、implicit pass-through、producer checkpoint、envelope file、ambient Git state或runtime-source lookup
  补造缺失字段；same-Skill wait 必须经过命名 pause，以 closed continuation加后续新 event/choice构造
  re-entry，不能重新要求 producer 没有输出的原始字段。每个 public output 字段也必须有 direct consumer；
  仅用于审计、显示方便或恢复猜测的字段不能进入 output。跨Skill clarification只可携带由原caller拥有、
  profile固定且仅由该caller re-entry消费的`caller_continuation_ref`；Clarification与router原样返回但不读取，
  不存在任意`return_stage`或可展开的generic frame。普通recoverable blocked result必须携带producer-owned
  `continuation_ref,repair_input`并落入`contracts.md`第7.1节唯一same-owner profile；stop只消费诊断字段并
  投影closed re-entry input。wording/qualification是唯一cross-Skill例外，必须原样返回caller-owned token；
  明确terminal/new-invocation结果不得为形式闭环伪造continuation。
- `EVO-DES-012`：pre-semantic dispatch guard 是 admission owner 内的 deterministic substep；它只
  判定 source stimulus、exact stock collision 与 current policy manifest。suppressed 命中在第一项
  semantic action 前 redirect 或 blocked，不执行 patch/delete/quarantine。blocked 结果按 role 恰好分为
  `upstream_suppression_blocked`、`provider_boundary_blocked` 与 `retained_context_blocked`，分别只重入
  Admission的`suppression_reentry`、`provider_boundary_reentry`或`retained_context_reentry`重新验证对应
  policy/provider/host边界；不得压成 generic stock collision，也不得由stop直接调用mutation owner。九项
  suppressed guard 的成功 consumer 统一且唯一为 `request_admitted -> guru-route-request:top_level`；各自
  Guru successor 只描述 Route Request 后的能力，不得由 guard 直接调用。

```text
user event
  -> guru-admit-invocation
     |-> bound -> current/earliest lifecycle owner
     |-> binding_blocked -> binding_reentry -> preclassification again
     `-> independent -> new envelope + one receipt -> isolation
         |-> pending -> progress refresh | safe clear | independent_request_isolation_blocked
         |-> independent_request_isolation_blocked -> isolation_repair_reentry -> isolation
         `-> clear -> stock admission guard -> guru-route-request
```

## 4. Exactly-One Top-Level Route

- `EVO-DES-013`：`guru-admit-invocation:request_admitted` 必须输出 consumer-minimal `request_ref`；
  `guru-route-request` 只消费该 admitted request projection，并恰好返回
  `direct_answer`、`new_change`、`resume_or_history`、`distribution_or_release`,
  `specialist_review` 或 `stopped`。`direct_answer` 同时固定
  `answer_profile=ordinary|trellis_reference|explicit_history|explicit_diagnosis`，由 Answer owner 按 profile 读取零项或最小
  facts/provider observation；`stopped`必须把`stop_reason_ref,unexecuted_boundary_ref`交给terminal consumer；
  route 未唯一时只返回一个最高价值问题或 blocked。
- `EVO-DES-014`：direct answer 由 `guru-answer-request` 完成；它读取答案所需的最小 live facts。
  `trellis_reference` profile只通过`guru-trellis-reference-read-adapter-1.0`读取
  `guru-trellis-reference-manifest-1.0`选定的official-doc/local-runtime/package-snapshot locator；standalone
  result只回Answer，写入意图在adapter调用前进入active/new-change owner，绝不调用raw `trellis-meta`。
  provider unavailable/access/incomplete 是带 unverified boundary 的正常完成，不创建 lifecycle；只有
  `answer_scope_ref`、fixed profile 或唯一 consumer 绑定 stale/mismatched 且当前 invocation 无法修复时，
  才返回 terminal `answer_binding_blocked`。controlled adapter 的 `provider_boundary_blocked` 必须由 Answer
  owner 提升为 recoverable `answer_provider_blocked -> direct-answer-provider-blocked`，并只用 Answer-owned
  continuation 从 `provider_reentry` 重调相同 adapter profile。availability/incomplete 结果选择任一 blocked
  exit 的计数必须为 0。
- `EVO-DES-015`：new change 才调用 `guru-select-workflow-mode`，且只有明确文件变更目标适用。
  task-free 继续由 `guru-execute-task-free-change` 独占；standard 进入 base/context/requirements/
  readiness/workspace chain。task-free scope/risk 扩大时，escalation router 保留 `partial_work_ref` 并从
  `guru-sync-base:task_free_escalation` 重新经过完整 Discovery/Clarification/Readiness，再到 Workspace；
  不得直接创建 Workspace 或跳过 standard 前置判断。
- `EVO-DES-016`：resume/history 先由 `guru-resolve-current-work` 区分 continue、disposition 与 durable
  history。三个结果分别进入 current owner、`guru-dispose-lifecycle`、`guru-query-lifecycle-history`；
  history query 永不激活旧 lifecycle。bound-intent 与 current-work router 只能使用 `contracts.md` 第 3.1
  节列出的 37 个 exact owner ids，并分别进入该 Skill 的 `lifecycle_intent_reentry` 或
  `current_work_resume`。该集合显式包含 Admission、Route Request、Answer、Current Work resolution 与
  History query；wording/qualification 两个 specialist Skill 不接管 lifecycle，其 fixed original caller 在
  specialist wait/block 期间继续持有 owner identity。unknown/multiple/stale owner 在 producer 处 blocked，
  不存在 generic “matching Skill/profile”、task scan、private checkpoint 或 ambient lookup。
- `EVO-DES-017`：distribution/release 由 `guru-route-distribution` 按 terminal intent、exact candidate
  与 target live state选择 standalone projection、clean install、existing migration 或 exact Release。
- `EVO-DES-018`：specialist 顶层只允许 wording review-only 与 normal-scenario qualification；wording
  使用contract表的九个closed caller profile：standalone只固定Route Request；active只允许task-free、
  Clarification、Plan与Implementation四个content owner分别选择review-only或change-scoped。review-only只允许
  pass/revision-findings/blocked，change-scoped只允许pass/content-changed/blocked；每个original caller创建
  opaque`caller_continuation_ref`，wording owner/router原样返回，pass/revision/content-changed/block只进入该
  caller的closed re-entry。其它active owner先回earliest applicable content owner，不能传任意caller id。
  qualification 使用 contract 表枚举的十一组 fixed profile/caller，未知caller/profile fail closed。每个
  qualification caller 提供自己的 opaque `caller_continuation_ref`；
  `scope_confirmation_required` 只进入该 profile 对应的 Clarification owner，取得一次真实 scope choice 后
  原样返回 token 给原 caller。只有原 caller 可打开 token、重建完整 current candidate set并 fresh 调用
  同一 qualification profile；Clarification/router 不读取 token，也不得把未决 scope 投影为
  `classified`。scope clarification blocked 只回原 caller 的 qualification-scope repair，再重入同一
  Clarification profile；mechanism revision同样只回原机制 owner并在修订后 fresh qualification。十个 active
  profile 可以产生该结果；standalone Route Request 不是原机制 owner，故
  `standalone_specialist:mechanism_revision_required` 与其 mechanism re-entry 都 schema-invalid。
  wording blocked同样只回原caller修复scope/authority/semantic prerequisite后重建scope/rescan并fresh review；
  standalone revision完整报告后直接完成，不产生modify/stop选择。
  active workflow 内的同类调用复用原 caller，不重新 top-level route。stop只适用于没有待处置 active
  lifecycle且本 invocation 尚无副作用的场景。

## 5. Standard Change Lifecycle

### 5.1 Intake And Workspace

- `EVO-DES-019`：standard route 顺序为 `guru-sync-base -> guru-discover-change-context ->
  guru-clarify-requirements -> guru-review-change-request -> guru-create-task-workspace`。Mode 只把
  `change_scope_ref` 投影给 Sync；Sync 自行解析 base selector并输出
  `change_scope_ref,base_ref,authority_checkout_ref`；Discovery输出 `change_scope_ref,change_context_ref`，
  才构成 Clarification initial input。normal chain 不再 mandatory 调用 wording reviewer；reviewed-design
  commitment由 clarification/plan author保真承接。Clarification 的 `requirements_current` 不固定直达
  change-readiness，而是按selected profile进入`guru-requirements-current-router`：initial/escalation返回
  change-readiness；后续scope/requirement修订把`requirements_result_ref`与原caller独占的
  `caller_continuation_ref`原样返回Change Readiness、Plan、Commit、Reconcile、Branch Review、Delivery
  Readiness或Acceptance的精确re-entry。Approval scope clarification不直接回Approval，而是携带
  `plan_revision_ref`回Plan修订，随后再fresh approval。Clarification/router不读取caller token；active
  revision只消费`revision_ref,caller_continuation_ref`，retarget只消费自身continuation和新`target_ref`。
  十一组 qualification-scope Clarification profile则只消费`scope_candidate_refs,caller_continuation_ref`，
  并按`EVO-DES-018`回原caller。Discovery/Sync refresh同样只使用各自owner的continuation；Discovery的
  context-refresh output只返回Clarification直接消费的`change_context_ref,continuation_ref`，不重复输出
  已由Clarification continuation绑定的`change_scope_ref`，也不传播return-stage frame。Workspace
  readiness refresh只把其已校验的`change_identity`及suspended profile的`partial_work_ref`投影给专用
  readiness re-entry，由Readiness owner定向live reread；不得重建initial三字段或使用hidden frame。
- `EVO-DES-020`：Phase 0 的 `authority_context` 只含 current Requirements/Design/Test 及适用
  authoring/review/lifecycle contracts；Architecture section 明确 N/A。detached invocation 可以只读
  exact base authority，base sync 使用已选 authority checkout而不修改 invocation checkout。
- `EVO-DES-021`：change-readiness 独占 duplicate、prerequisite、scope overlap 与 independently
  deliverable 判断。只有 ready 进入 workspace；active/completed duplicate、clarification、prerequisite、
  resolution blocked 各回唯一 consumer。
- `EVO-DES-022`：`guru-create-task-workspace` 在读取 ready `change_identity` 后先 live 解析 exact
  repo/Issue/base/branch/worktree/task/path 与 ownership/isolation state；public input 不接收无 producer 的
  `resource_plan_ref`。若全部 required resource 已精确匹配 current change identity，且无 creation、transfer
  或 isolation action 待执行，则直接产生 `workspace_current -> task_impact_sync`，user-visible plan、确认
  wait、refusal branch 与 mutation 均为 0。否则 Workspace owner 自行生成、语义审查并只在 current call/
  host-session continuation 中 owner-private 保存 exact resource/transfer-or-isolation plan；确认前 generic
  repository plan/envelope/checkpoint write 为 0。owner 按 `EVO-DES-069` 展示 current 计划并取得 dialogue-local 语义
  确认。task-free escalation 已先经过 Sync/Discovery/Clarification/Readiness；suspended profile 仍必须由
  Workspace owner 生成并确认 transfer/isolation plan，资源建立后在 Planning 前验证唯一 owner。明确拒绝
  只返回 `workspace_not_created -> task-workspace-not-created`，保持 source/partial work 可发现且资源副作用
  为 0；它不得伪装成 readiness/Workspace defect。

### 5.2 RDT- And Architecture-Aware Planning

- `EVO-DES-023`：Planning 的第一个实质步骤是
  `guru-maintain-requirements-design-test-ssot:task_impact_sync`。其public input只有common `task_ref`；RDT
  owner在当前 envelope 中读取自己拥有的 repository RDT subprojection，并消费 Clarification-owned、只供
  本轮 RDT impact与Plan直接使用的 `requirement_delta_ref,reviewed_design_binding_ref`；它不从尚未写作的
  task artifacts、Workspace private plan或ambient state猜测 task delta，也不接受caller复制的
  locator/version/status。
  current结果按no-impact/aligned或contribution-current的disjoint schema输出`rdt_result_ref,impact_kind`及
  仅适用的`contribution_ref`，由RDT router消费并只把Architecture/Plan直接需要的result identity继续投影。
  task-local contribution的形成与修订留在该impact owner内，不得从Planning直接调用shared promotion。
  `baseline_incomplete` 只把`missing_layer_refs`与RDT owner创建的opaque
  `authority_caller_continuation_ref`交给Bootstrap的`rdt_request`；Bootstrap返回authority identity与同一
  token后只进入RDT `bootstrap_reentry`，由RDT owner打开并fresh验证原stage，不从task、private state或
  ambient lookup推断origin。
- `EVO-DES-024`：RDT current 后立即调用
  `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`；其public input只有
  `task_ref,rdt_result_ref`，这时才由Architecture owner加载 baseline、constitution、change contract 与适用
  片段，不接受caller复制的live Architecture fields。`baseline_current` 使用三个 disjoint output：no-impact
  禁止 change path/contribution，aligned 必须有 change path 且禁止 contribution，contribution-current 同时
  要求 change path 与 contribution ref；三者都输出`rdt_result_ref,architecture_result_ref,impact_kind`，供
  router校验后把两个result ref投影给Plan，不使用 nullable union。no-impact 不创建 contribution/ADR；
  impact 选择唯一 change path。task-local Architecture contribution同样不在Planning阶段调用shared
  promotion。Architecture `baseline_incomplete` 使用独立`architecture_request`与Architecture owner的
  `authority_caller_continuation_ref`；Bootstrap只原样返回token到Architecture `bootstrap_reentry`。Bootstrap
  自己的repair/blocked recovery只打开Bootstrap-owned continuation，不读取或替换caller token。
- `EVO-DES-025`：`guru-plan-task` 是三份 task planning artifact 的唯一 author。initial public input精确为
  `task_ref,rdt_result_ref,architecture_result_ref`；current requirement delta/reviewed-design projection由Plan
  owner从同一 `authority_context` 的 Clarification-owned subprojection取得，且直接使用稳定 prefix 中适用的
  repository RDT/Architecture正文；不得通过undeclared authoring seed、task runtime snapshot、producer summary
  或ambient Docs lookup补造。revision/finding re-entry分别只消费`task_ref,revision_ref`或
  `task_ref,finding_refs`并定向重读受影响owner；Clarification、authority与base返回分别消费closed
  `requirements_result_ref`/caller token、`authority_result_ref`或`base_result_ref`。`prd.md` 只拥有 requirement locator/delta/acceptance mapping；
  `design.md` 只拥有 Design locator/reconciliation/Architecture alignment；`implement.md` 只拥有 Test locator、
  approved execution/validation/delivery mapping 与 Docs SSOT Plan。
- `EVO-DES-026`：`guru-approve-task-plan` 是 normal Planning 唯一 sufficiency reviewer。它实际消费
  stable prefix中的current RDT/Architecture authority content、对应result与三份 task projection，返回
  approved/revision/scope/block；文件存在性、
  checker PASS或 author boolean 不能替代判断。revision只回Plan；scope clarification经Requirements owner
  后也先回Plan修订，不能通过无producer的approval revision/clarification profile直接复核stale plan。
- `EVO-DES-027`：AI semantic approval 通过后只展示一次完整 compound next-action plan：它同时明确 task
  status activation，以及立即进入 `guru-implement-task:initial` 的 approved implementation scope、allowed
  writes 与 stop boundary，并显式排除 Commit、push、PR、merge、Release、cleanup 等后续副作用。当前清晰
  语义肯定只授权该复合行动，不产生第二个 routine implementation-entry confirmation；
  `phase-1-task-activation` 是 Approval owner 内、semantic confirmation后的确定性 substep，不是 public router
  或 terminal。只有 transition current 后 Approval 才输出 `approved -> task_ref`，并直接进入
  `guru-implement-task:initial`；客观 transition failure返回 Approval自己的recoverable block且 implementation
  write为0，不得留下 unmapped activation result。不写授权 artifact，也不再做第二次 approval；确认缺失保持
  等待，明确拒绝保留 planning task并完成当前 invocation。material plan/authority change使private approval
  checkpoint stale并fresh review；同一未变 plan不重复semantic approval或确认。

### 5.3 Implementation, Check And Promotion

- `EVO-DES-028`：`guru-implement-task` 是 standard Phase 2唯一 implementation owner。initial public input
  只有`task_ref`；它从自己的 envelope section派生 `implementation_context`，解析approved plan、current
  RDT/Architecture result projection、适用 specs 与 code，而不要求Planning caller复制live plan/authority
  fields。它可调用 caller-bound worker，但 worker不能继续 phase或决定 pass；`implementation_current`只把
  `candidate_ref`投影给Check，finding/discovery re-entry只消费对应ref，planning revision明确投影到
  `guru-plan-task:revision_reentry`；authority/base返回只消费`authority_result_ref`或`base_result_ref`并由
  Implementation owner定向重建current implementation context。
- `EVO-DES-029`：implementation discovery 发现 scope、RDT、Architecture、provider、persistence、SDK、
  owner或外部边界扩大时，停止新写入并回 earliest affected owner；普通实现事实持续回写 task-owned
  RDT/Architecture contribution，不等到 Finish。
- `EVO-DES-030`：Phase 2 由 `guru-check-task` 完成一次 semantic check；finding 返回 implementation
  owner，修订后只重跑依赖 affected 的验证与 gate。之后 `guru-create-task-commit` 精确提交 task scope，
  `guru-review-branch` 独立审核 committed full diff。Commit owner单独展示 exact staged-path/commit plan；
  明确拒绝得到 `commit_not_created -> task-commit-not-created`，不提交、不进入 Branch Review。
- `EVO-DES-031`：RDT/Architecture contribution只有 independent full-diff review 后可 serialized
  promotion。Branch Review pass 必须进入 post-review authority router，并在每次 fresh review 中先把完整
  committed diff 内的 contribution/projection 与 live shared current identity 比较；两个 discriminator只描述
  尚未current的工作，不重复描述该range中已经current的历史贡献。`promotion_kind`只选择尚未以reviewed
  target identity成为current、且expected-current precondition仍成立的RDT/Architecture contribution；已精确
  current的contribution不再产生promotion ref，material current/contribution/expected-identity drift则返回对应
  authority owner，不能降为`none`。`projection_kind`只选择当前`guru-code-spec-projection-1.0`仍缺失的
  authority locator/usage/freshness或same-range code-spec contribution；已精确包含current authority与reviewed
  code-spec identities的projection不再产生refresh工作，material projection/contribution drift返回Bootstrap或
  affected owner。pass output按`promotion_kind=none|rdt|architecture|rdt_then_architecture`与
  `projection_kind=none|authority_only|with_code_spec`选择closed schema；每个outstanding
  `rdt_promotion_ref|architecture_promotion_ref`绑定contribution content、该reviewed committed range与
  expected-current identity，`with_code_spec`额外要求同range的outstanding `code_spec_contribution_ref`。
  `projection_kind=none`表示既无outstanding authority promotion，也无current projection尚缺或stale的
  authority locator/usage/freshness与code-spec contribution；它只与`promotion_kind=none`组合。
  `authority_only`表示current projection只缺失或持有stale authority locator/usage/freshness，禁止code-spec
  ref，并可与任一promotion kind组合，包括shared authority已经current时的`promotion_kind=none`正常repair；
  `with_code_spec`可与任一promotion kind组合且必须携带same-range outstanding code-spec ref。router按 RDT ->
  Architecture 的稳定顺序调用selected
  `promotion` profile；所有selected promotion current后，非none projection调用`.trellis/spec`唯一编排/写入
  owner `guru-bootstrap-repository-ssot:projection_refresh`的closed variant。该owner live-reread已promote的
  RDT/Architecture与current projection，仅在`with_code_spec`额外回读同range contribution；若目标projection
  已current则无写入返回，否则审核并只写`guru-code-spec-projection-1.0` locator/usage/freshness projection，
  禁止raw `trellis-update-spec` result或authority正文。`spec_projection_ref`重命名为
  `authority_result_ref`只回`guru-check-task:authority_reentry`，随后必须新Commit和committed full-diff Branch
  Review。该fresh full-diff review即使仍看见原始contribution/projection diff，也必须在live target identities
  已current时输出精确double-none并进入delivery；任一material drift重新打开对应promotion/projection工作。
- `EVO-DES-032`：base advance 由 `guru-reconcile-task-base` 按 actual diff 分成 no-impact、planning、
  implementation、review continuity、scope choice或 blocked；no-impact/reconciled输出closed
  `resume_target,base_result_ref`，router只把该ref交给allowlisted exact `base_reentry`，不读取旧caller frame；
  不得重新创建 task或回 Phase 0。

### 5.4 Delivery, Finish And Cleanup

- `EVO-DES-033`：`guru-select-delivery-route` 在 reviewed candidate上恰好选择 `github_pr` 或 `none`。
  route 绑定后不能因 provider失败 fallback。
- `EVO-DES-034`：两条 route 都先完成 delivery readiness 与 pre-delivery acceptance。GitHub route随后按
  publication provenance prepare -> publication-head push -> Draft PR -> official Finish/archive + archive push +
  Ready -> archive-bound `ready_for_merge` -> expected-head merge -> issue closure -> delivery terminal -> owned
  cleanup 的固定顺序执行。none route按 local Finish/archive -> issue closure not applicable -> delivery
  terminal -> owned cleanup 执行，GitHub I/O 为 0。Finish 前后的 chained identity直接绑定 route、acceptance、
  reviewed content、publication/archive head 与 durable result；Closure、Merge或Cleanup不得从ambient provider/
  archive facts猜测前序结果。
- `EVO-DES-035`：`guru-accept-task` 是两条 route共享的 pre-delivery semantic acceptance owner，按 route
  profile消费 current RDT/Architecture/validation/diff，不重复 Branch Review。GitHub publication先由
  `guru-publish-task-pr:provenance_prepare`绑定 `reviewed_content_ref` 并选择closed `self_hosted|installed`
  mode：self-hosted source固定为target reviewed HEAD；installed source只从current installation manifest/
  managed-byte/source-commit identity解析canonical repository immutable full OID，在独立clean detached
  `extension_source_checkout`读取apply bytes；业务mutation、metadata-tail lineage与commit只发生在独立
  `target_reviewed_checkout`。source/target lineage、cleanliness、source immutability、allowlisted provenance
  fields、normalized reviewed-content equality、direct parent与single metadata tail任一不current，都在remote
  mutation前进入publication owner recovery。缺tail时owner展示且只确认该metadata-only preparation；精确tail
  current时零mutation产生`publication_head_current`。其后`push_prepare` live-reread exact remote branch，
  bound publication HEAD已current时零push/确认产生`branch_published`，否则只确认branch push；
  `pr_create_prepare`再live-rereadexact base/head PR，已存在的exact Draft/READY PR零creation/确认产生
  `draft_pr_current`，否则只确认创建Draft PR。provenance prepare、push与PR creation使用三个互不兼容的
  continuation/refusal/provider recovery；任一确认不授权下一action，re-entry均先live-reread并禁止重放。
- `EVO-DES-036`：`guru-finalize-task` 在GitHub route只消费exact Draft/READY PR与publication head，在none
  route只消费local acceptance；none Acceptance只输出`acceptance_ref`，不提前形成或传入delivery fact。它
  live-reread task/archive/summary/remote/PR facts；已存在且精确匹配的official
  archive、archive commit/push、Ready state与schema-valid `ready_for_merge`直接无mutation收敛。否则它展示一个
  exact Finish transaction，确认后只生成compact summary、official archive与archive commit，安全push该
  archive head并把同一PR转为Ready；partial/unknown/provider failure保留已完成/待执行action并只重入Finish，
  不重放archive、push或Ready mutation。GitHub success输出archive-bound `ready_for_merge_ref`给Merge；none
  success才作为该route唯一producer输出绑定durable result的`delivery_fact_ref`给Closure-N/A。Finish refusal为
  `finish_not_executed`，不能
  继承publication或其它确认。
  `guru-merge-task-pr`只接受`ready_for_merge_ref`，重新验证PR live READY、base、archive expected head、summary/
  scope binding后展示exact merge plan；清晰语义肯定即可expected-head merge，不要求固定`合并PR`。merge
  refusal/repair只回Merge，merge确认不授权manual Issue closure。Closure读取Merge或none Finish产生的
  `delivery_fact_ref`，只读current/N/A无需确认；exact manual close另行展示，拒绝得到
  `issue_closure_not_applied`。delivery-terminal router从closure chained identity生成绑定durable result的
  `delivery_terminal_ref`并直接进入Cleanup，不再调用第二次Finish。
  `guru-clean-task-resources`自行live-read owned/unrelated/retained resources并审查private cleanup plan；无
  deletable resource时确定性完成，有删除项时经owner-local confirmation re-entry执行，拒绝得到
  `resources_retained -> workflow-completed`。Cleanup只凭自身continuation或delivery terminal恢复，不重放
  publication、Finish、Merge或Closure。
- `EVO-DES-037`：durable history由 `guru-query-lifecycle-history` 从 archive/finish/disposition 的
  compact terminal records解析；cleanup必须保留查询所需identity与retained ref reachability。

```text
standard change
  -> base/context/requirements/readiness/workspace
  -> RDT impact -> Architecture impact -> one plan author -> one approval
  -> implementation owner -> Phase 2 -> commit -> committed full-diff review
  -> contribution review/promotion/recheck when applicable
  -> github_pr | none -> readiness -> acceptance
     |-> github_pr -> provenance prepare -> push -> Draft PR -> Finish/archive/Ready
     |               -> ready_for_merge -> merge -> closure
     `-> none -> local Finish/archive -> closure N/A
  -> delivery terminal -> owned cleanup -> workflow completed
```

## 6. Resume, Latest Intent And Disposition

- `EVO-DES-038`：current-work resolution使用 live task/worktree/branch/provider/archive facts恢复唯一
  owner；equivalent stale刷新identity后继续，not-found/multiple/material mismatch blocked。causally bound
  latest event只通过 Admission 产生的 `bound_event_ref,event_sequence` 进入registered owner，current owner
  不得从host session、task scan或ambient message history补找该事件。
- `EVO-DES-039`：owner-local additive只使受影响判断失效；remote boundary前 material additive回
  earliest owner；boundary后形成有唯一 consumer的 `additive_change_pending`，旧 route收敛后启动新
  invocation。无副作用 stop/本地 suspend current 后只允许 producer 的
  `successor_invocation_required -> guru-admit-invocation:post_owner_pending`；四个 remote owner 的 normal、
  forward-recovered 或 terminal-block outcome current 后，只允许
  `post_remote_intent_ready -> guru-admit-invocation:post_remote_pending`。两种 fresh-entry profile 都从
  producer output直接构造输入，再建立新 identity/envelope/receipt；不得复用旧 frame 或让 router猜入口。
- `EVO-DES-040`：override在无副作用时停止旧 route；可逆本地副作用形成 `suspended_current_work`；
  不可逆远端动作由原 owner先正常/forward-recovery/terminal-block收敛。任何后续请求都获得新
  identity/envelope/receipt并重新六类 route，不默认 new change。
- `EVO-DES-041`：`guru-dispose-lifecycle` 区分 retain、suspend、no-resource abandon、confirmed cleanup
  与 irreversible remote boundary。只在有 exact deletable owned resources 时输出
  `cleanup_confirmation_required -> active-lifecycle-cleanup-confirmation-wait`；清晰肯定只凭continuation进入
  cleanup confirmation re-entry。明确拒绝时，
  若同一回复已包含唯一 retain 或 suspend choice，cleanup-confirmation owner把
  `continuation_ref,disposition_intent`直接投影到`cleanup_refusal_choice_reentry`并完成对应disposition；否则只
  输出`active_lifecycle_disposition_choice_required -> active-lifecycle-disposition-choice-wait`，询问一次真实
  retain/suspend choice。缺失、疑问或歧义回复保持同一wait；choice current后以
  `continuation_ref,disposition_intent`进入`choice_reentry`。choice current前cleanup/delete count为0；不得
  产生`disposition_cleanup_not_executed`/`lifecycle-cleanup-not-executed` terminal、generic blocked或
  `retained|suspended`双结果。`choice_reentry`只接受后一个 named choice wait，绝不消费原 cleanup refusal。
  irreversible remote 分支输出`current_owner_id,remote_boundary_ref,continuation_ref`到
  `active-lifecycle-remote-convergence-wait`；wait只调用四个registered remote owner之一的
  `remote_disposition_resume`，观察三类current outcome并把`remote_outcome_ref,continuation_ref`投影到
  Disposition `remote_reentry`。remote owner不接触Disposition continuation，也不存在generic remote router。
- `EVO-DES-042`：disposition success写最小 durable result，使 cleanup后仍可查询；不删除 unrelated、
  durable authority、retained refs或不可逆 remote outcome。

## 7. Distribution And Release

- `EVO-DES-043`：standalone projection由 `guru-validate-extension-projection` 拥有；capability-loss只
  比较 `workflow/task_data/docs_authority`，Skill API/distribution/installed parity属于独立 consistency
  gate。需要执行已选 stock policy action 时，该 owner 是
  `guru-maintain-stock-projection:standalone` 的唯一 caller：只通过
  `stock_maintenance_required`进入 Stock owner，`stock_policy_current` 以绑定同一 candidate/target 的
  `policy_ref`只返回 Projection的`stock_policy_reentry`，再fresh验证完整surface后才能得到
  `projection_current|projection_validation_blocked`。这不是第五个顶层 distribution action，Stock owner也
  不取得workflow terminal。embedded clean/migration/Release profile只允许`returned_to_caller`，child finding
  只能成为caller-local finding，不能取得standalone terminal。
- `EVO-DES-044`：clean install只有 `clean_target` 可进入，顺序为 official init/projection -> Guru
  workflow -> preset/stock policy -> installed validation；结果只有 new-contract-current 或 caller-owned
  blocked/re-entry。每个待执行 external mutation 单独展示 next exact action；拒绝返回
  `clean_install_not_executed` 并保留 created/current resource facts 与continuation；之后只有新的明确继续
  意图可把`step_ref,continuation_ref`投影到Clean owner的`action_reentry`。blocked recovery只把
  `step_ref,continuation_ref,repair_input`投影回Clean owner；continuation绑定candidate/target，caller不重传。
- `EVO-DES-045`：existing migration只从 `existing_migration_target` 进入，按 INSTALL -> UPGRADE ->
  UPDATE -> WORKFLOW-SWITCH -> PRESET-REAPPLY判定并执行 applicable cell；共享一次 preflight、唯一
  cutover、一次 final validation。UPDATE 先读取 `trellis update --dry-run`：包含 `MIGRATION REQUIRED` 时
  只执行 `trellis update --migrate --skip-all`，否则只执行 `trellis update --skip-all`；`--force` 与
  `--create-new` 仅属于独立 control subcell。foreign/mixed/unknown先 blocked并回 preclassification。每个
  待执行 external mutation 单独确认；cutover 前拒绝返回 `pre_migration_action_not_executed` 并携带
  preserved identity/step/continuation，cutover 后拒绝返回 `post_migration_action_not_executed` 并携带真实
  cutover/step/continuation；两者互斥，新明确继续意图只把continuation投影到原Migrator的`action_reentry`。
  pre/post blocked stop分别消费truthful
  preserved/cutover display field，re-entry只把`continuation_ref,repair_input`投影回Migrator；continuation
  绑定candidate/target、ordered cell与live cutover phase，不靠ambient installation state重建。
- `EVO-DES-046`：workflow switch的 explicit force write或有序 boundary的 byte-equal observation是
  唯一 cutover；其后必须形成 preset-reapply current，再 final validate。cutover前 finding保留旧
  current，cutover后只 forward recover到 new current或 migration blocked。
- `EVO-DES-047`：Release由 `guru-release-candidate` 独占 pre-publish、confirmation wait、immutable
  publication与 tag-pinned post-publish四段。confirmation遵循 `EVO-DES-069` 的完整 prohibited-challenge
  集合：current 清晰语义肯定直接进入 publication，缺失确认保持 wait，明确拒绝返回
  `release_not_published`，candidate/decision-relevant facts 变化使旧 wait 失效并回 pre-publish 重建；
  authorization 不持久化。publication首个动作零完成或 outcome unknown 时使用
  `publication_progress_ref,continuation_ref,repair_input` 的 pending re-entry/block，不重复candidate/stage；
  至少一项完成且一项 pending 时才允许`published_partial_ref,continuation_ref`的retryable partial re-entry，
  blocked partial修复才额外携带`repair_input`。publication current以`published_ref,continuation_ref`进入
  post-publish，post-publish repair只回传continuation与repair；各output schema互斥。semantic defect终止为
  published-unverified，后续修订是新 invocation。
- `EVO-DES-048`：provider自动重试上限由每个 action contract声明为“同一 action最多一次自动安全重试”；
  只有 live reread证明未完成、provider明确可重复且没有不可逆重复风险时执行。否则立即 partial/unknown/
  blocked并要求唯一恢复输入；不以时间或轮次阈值判定业务成功。每个 action 的 private
  `provider_context.provider_action_contract` 完整承载 source owner、contract locator/version、caller
  scope、target/action、input/output/effective boundary、permission/quota/error/partial/unknown、
  idempotency、live reread、retry/stop，并从 `contracts.md` 的 Git、GitHub、Trellis upstream、Guru preset
  与 Release closed action profile 中恰好选择一项；variant 字段不得用“as applicable”省略。单个 action
  state 只允许 `completed|pending|unknown`；`partial` 仅是 completed+pending 的 aggregate，优先级固定为
  `unknown > partial > action_required`。public DTO只投影当前 consumer 必需的 result/continuation。

## 8. Stock Projection Control Plane

- `EVO-DES-049`：stock source inventory绑定 package name/version/integrity/tarball identity和相对模板
  locator。source owner仍是 official Trellis；Guru `stock-policy owner`拥有 exact target projection
  action与provenance，但不拥有产品 route。current ownership contract/schema 3.0 明确禁止 Guru claim/
  patch/delete upstream paths，因此任何 future stock mutation 前，preset transaction 必须先安装并验证
  `guru-extension-ownership-contract-4.0`、其 schema/validator 与 exact post-projection policy claim；该
  ownership handoff current 前 mutation count 为 0，且它不取得 upstream source ownership或提前激活
  target workflow。
- `EVO-DES-050`：preset新增 closed `stock_projection` manifest domain，记录 selected platform、asset、
  source identity、target path、action、before/after identity、successor、file/context/sidecar state、
  action status与reapply result。它不记录 authorization或完整 scan。
- `EVO-DES-051`：九项 suppressed asset在 official projection完成后按 exact allowlist做 managed absence。
  只有 bytes等于 pinned upstream template或previous-managed identity且Guru successor current时才删除；
  user edit/unknown/sidecar/missing successor保持原状并 blocked。raw `trellis-update-spec`的successor current
  还要求`guru-bootstrap-repository-ssot:projection_refresh`与`guru-code-spec-projection-1.0`的post-review
  trigger/fresh-Check回程可达；raw `trellis-meta`的successor current还要求
  `guru-trellis-reference-manifest-1.0`、caller-fixed
  `guru-trellis-reference-read-adapter-1.0`以及active/new-change写入route全部可达。
- `EVO-DES-052`：channel/explicit asset先把 pinned source复制到 non-discoverable
  `.trellis/guru-team/stock-providers/<asset>/`，再移除 discoverable projection；Guru adapter显式读取
  reference或调用 CLI。每个 adapter具有caller-fixed closed standalone/embedded/transport profile、一个窄
  success result、统一 `provider_boundary_blocked` 与 caller-owned evidence ref/return shape；adapter output
  不携带generic `caller_ref`。blocked同步回profile-fixed caller，由caller在本step修复或产生自己的第7.1节
  recoverable block，re-entry后只重调同一adapter profile；Answer必须使用自己的
  `answer_provider_blocked/provider_reentry`，不能把 adapter block误投terminal binding block。quarantine不是
  第二semantic route，也不进入平台auto-match。
  Trellis reference不是quarantined raw provider：preset transaction单写
  `guru-trellis-reference-manifest-1.0`，以official docs优先解释扩展语义、local runtime解释安装事实、pinned
  package snapshot解释shipped-template事实；独立reference adapter只按standalone-answer或七个embedded
  caller profile懒读取选定locator并同步返回，不能继承`trellis-meta` matcher、semantic owner或写入权。
- `EVO-DES-053`：platform/channel workers由 Guru-owned agent definitions替换；platform implement 只经
  `guru-platform-implementation-worker-adapter-1.0`，channel implement 只经
  `guru-channel-implementation-worker-adapter-1.0`，两者各自具有互斥的 `task_free|standard_phase2`
  profiles。spawning caller把
  profile、scope、source/candidate、allowed writes与consumer写入 invocation payload，worker只返回
  profile-specific `research_observation_current`、`implementation_worker_current` 或
  `check_observation_current` 及 caller-owned evidence ref。task-free/standard implementation 与
  platform/channel check profiles互斥；raw worker path从 target dispatch inventory移除。
- `EVO-DES-054`：pre-semantic guard只读 manifest与source stimulus。完整 policy evaluation只在
  stock-touching caller发生；首次全 pending、partial、unknown分别返回 action-required/partial/unknown，
  复用 current call/host-session envelope并只重入未完成或可安全重试 action；standalone profile不得为此写
  repository envelope/checkpoint。action-state resolver 可先做零副作用 live
  resolution；一旦 next pending mutation 唯一且需要确认，Stock owner 必须展示 current exact plan 并进入
  `stock-policy-action-confirmation-wait`，只有 current 清晰肯定才可投影 continuation 到 profile-fixed action
  re-entry；missing/refusal/material drift 分别保持 wait、进入 owner-specific action-not-executed、或零副作用
  返回同一 profile 重新读取和展示。每个 atomic action 只记录
  `completed|pending|unknown`；partial只由 action set 聚合得出。`retained_host` profile拥有独立
  `retained_context_current|retained_context_blocked` public contract；R01..R09各由profile固定host/cell/action
  及唯一hook-policy/session/workflow-breadcrumb context owner，后者再向Admission/worker/current-owner提供
  authorized minimal projection；这些later caller不直接消费retained result，public input不接受caller id。
  standalone 与 embedded/reapply exit set
  互斥，embedded/reapply 永远只回 exact caller。standalone caller固定为
  `guru-validate-extension-projection:standalone`；`stock_policy_current`只回其`stock_policy_reentry`，不得直接
  `workflow-completed`。standalone suppression/provider failure分别进入
  `stock-suppression-maintenance-blocked`与`stock-provider-maintenance-blocked`，不使用未命名role-local block；
  pending mutation拒绝得到携带同一continuation的`stock_policy_action_not_executed`；新明确继续意图只把
  该 token 交回 `stock-policy-action-confirmation-wait` 所属的 exact owner，重新 live-reread 后才可进入
  `standalone_action_reentry`，embedded/reapply则以
  `returned_to_caller(policy_result=action_not_executed)`回profile-fixed caller。
  `reapply` profile 只固定回 `guru-migrate-existing-repository` 的 ordered update/preset-reapply cell，
  不存在未命名 standalone reapply caller。standalone action-required/partial/unknown各只输出closed
  `continuation_ref`给同一 Stock owner 的 action-state resolver；需要确认的 mutation 必须先进入
  `stock-policy-action-confirmation-wait`，肯定后才到`standalone_action_reentry`。exact Stock owner从自己的
  policy/continuation section解析 bound candidate/target与action state，caller不重复传入原始字段。embedded/reapply 的
  `returned_to_caller`使用互斥closed variants：current只携带policy ref；required/partial/unknown各携带
  `action_state_ref,continuation_ref`；refusal携带同形state/continuation；caller finding只携带finding refs。
  另一variant字段一律非法，只有action state variant可经 exact caller 的 fixed stock-action edge 返回 Stock
  resolver，并在命名 wait 取得 current 肯定后把 continuation 投影到对应 profile-fixed
  `embedded_clean_action_reentry`、`embedded_migration_action_reentry`、`embedded_release_action_reentry` 或
  `reapply_action_reentry`；
  continuation 本身不构成 mutation authority。
- `EVO-DES-055`：official update/upgrade/init重新生成 stock path不是成功。preset reapply重建inventory、
  对 Design选定action执行current/blocked判断、处理`.new/.bak`，最后要求active semantic graph唯一、
  no unresolved sidecar、all successors reachable。update reapply 必须保留 dry-run discriminator 与所选
  `--migrate --skip-all|--skip-all` 分支，不得把 `--force`/`--create-new` 当 canonical update。

详尽逐 asset选择见 [`stock-and-distribution.md`](./stock-and-distribution.md)。

## 9. Platform Projection

- `EVO-DES-056`：canonical authority为 `trellis/workflows/guru-team/`、
  `trellis/skills/guru-team/`、`trellis/presets/guru-team/`。dogfood与installed copies不是authoritative。
- `EVO-DES-057`：Shared是一次`.agents/skills` projection layer；supported hosts只有Codex、Claude、
  Cursor。每个平台从同一 registry/interface生成Guru Skills与worker/explicit entries，不复制业务语义。
- `EVO-DES-058`：hooks只注入短 workflow-state、host-session continuation handle或caller-bound context，
  不注入或解析 repository envelope path/body；passive startup/session/subagent/channel context不得消费请求或
  生成route。hooks-disabled/no-hook仍由main-session Guru
  entry执行相同contract。per-host setup 使用 Requirements 的七个 exact cells：
  `enabled_approved|enabled_pending|enabled_denied|feature_off_config_present|feature_on_config_absent|
  feature_off_config_absent|configuration_unknown`；高层 enabled/disabled/no-hook 仅为派生视图。
- `EVO-DES-059`：activation manifest将workflow、registry/interfaces/runtime、stock policy、workers、
  ownership contract 4.0、Trellis reference manifest/adapter、code-spec projection contract、platform entries与
  installed provenance绑定为一个candidate。缺项、mixed version或unknown sidecar
  在任何target consumer运行前fail closed。

## 10. RDT And Architecture Evolution

- `EVO-DES-060`：本Design与Evolution Test当前是 target contribution candidate；只有完整
  Design/Test/Architecture/task-planning fresh gate通过后才可称 reviewed/ready。未来implementation Issue
  必须同时读取 selected-base `.41` current 与 target delta，通过 task-local contribution 说明本 slice 的
  before/after；`.40` 只作为历史 comparison evidence。
- `EVO-DES-061`：每个requirement/behavior必须到达一个Design responsibility/contract和至少一个
  Test strategy/scenario/case。replacement/split/merge保留predecessor/successor；删除必须说明subtraction。
- `EVO-DES-062`：Architecture task impact选择`target_native`，命中
  `concept-semantic-completeness`、`cohesion-change-isolation`、`minimum-necessary-complexity`与
  `debt-one-way-convergence`。task contribution拥有新owner graph、stock projection ownership、
  compatibility exit与promotion conditions。
- `EVO-DES-063`：shared Architecture/RDT current只有在实现candidate independent review后由各自
  owner serialized promotion；本planning task只维护task-owned contribution，不修改shared current
  Architecture、shared current RDT或ADR index。
- `EVO-DES-064`：`.trellis/spec`只投影target contract的reading/usage rules、authority locators与定向
  freshness，不复制本Design、Requirements或Architecture正文。其唯一owner是
  `guru-bootstrap-repository-ssot:projection_refresh`，trigger恰好是fresh full-diff review确认仍存在尚未current
  的shared promotion、authority locator/usage/freshness projection repair或code-spec projection工作；调用前
  所有selected shared promotion（如有）必须current，`authority_only`与`with_code_spec`输入互斥，前者允许
  `promotion_kind=none`且禁止code-spec ref，后者必须携带same-range outstanding contribution ref。owner先将
  current projection与selected authority/code-spec target identities比较，精确current时不得重写。其唯一成功回程是
  `spec_projection_ref -> guru-check-task:authority_reentry -> fresh Commit -> fresh Branch Review`。其它Skill、
  raw `trellis-update-spec`、hook、worker或preset reapply不得成为第二projection writer；回程后的fresh Branch
  Review必须把已经current的promotion/projection排除出outstanding set并允许精确double-none，material drift则
  重新打开affected work。

## 11. Observability And Evidence

- `EVO-DES-065`：每个normal fixture输出invocation/candidate/fixture identity、observed action、direct
  consumer/correctness responsibility、typed result与unverified boundary；不保存累计stdout或全量上下文。
- `EVO-DES-066`：provider blocked/recovery result至少可查询action identity、phase/owner、last live state、
  completed/pending/unknown actions、error/retry classification、re-entry input与unverified boundary。
  全部普通recoverable block还必须命中`contracts.md`第7.1节恰好一个producer/profile/input row；wording/
  qualification caller-owned block、direct-answer terminal binding block与published-unverified terminal分别按
  其显式例外验证，不能被generic blocked recovery吞并；Answer adapter block必须命中自己的Section 7.1 row。
- `EVO-DES-067`：正常path中重复semantic gate、unchanged全文read、无consumer script/artifact、重复
  question/side effect、invalid wait、unconsumed intent、human-style assignment/signoff/transaction handoff、
  already-current fact restatement均为0；cache hit/miss、diagnostic时间/round/byte不决定pass，cache 不可用时
  同一stable authority content仍只完成一次live read并对每个适用semantic owner可用，semantic result 与
  fresh authority resolution必须等价。bound event只传sequence而丢失event identity/content、或通过ambient
  lookup恢复的计数同样为0。
- `EVO-DES-068`：secret/credential/raw sensitive records不得进入prompt/log/artifact/Issue/PR/history/test。
  Git/GitHub/Trellis mutation只在exact target/current permission与dialogue-local confirmation边界发生。
- `EVO-DES-069`：每个可能拥有副作用的 semantic Skill 先解析 current action state；若已是 no-mutation
  current result，则不展示 action plan、不进入确认 wait/refusal branch，直接按该 current exit 收敛。只有
  真实选择或副作用待执行时，owner 才生成并审查 owner-private exact action plan，向用户完整展示 current
  action、repo/target、scope、副作用、保留/不包含边界与 decision-relevant facts；展示后未 material drift
  时，AI 接受“确认继续”“可以，继续”或任一清晰语义肯定，并只执行刚展示 action。疑问、限制、条件、
  修改、部分选择、拒绝或 material target/scope/permission/candidate/HEAD/
  fact 变化均保持零副作用，返回同一 owner 重建并重新展示或 route-local 收敛。READY PR merge 使用
  同一边界，不存在固定 `合并PR` gate。不得要求用户复制固定 prompt、口令、hash、digest、task id、
  path、branch、SHA、identity、摘要或规定句式；`确认执行 <hash>` 不得成为继续条件。确认只由 AI 根据
  current 对话语义判断；hash/digest 只可校验 owner-private plan freshness，script/validator/recorder
  不解析、匹配、验证或持久化回复，schema/DTO/gate/checkpoint/history 也不含 confirmation/authorization
  字段。明确拒绝必须选择该owner声明的zero-side-effect result；至少闭合base sync、Workspace、plan
  activation、Commit、publication provenance-tail preparation、branch push、PR creation、READY merge、manual Issue closure、Finish/archive、delivery-terminal
  Cleanup、active-lifecycle disposition cleanup、clean install、migration、stock maintenance与Release，且
  不得把refusal误报为blocked/provider defect。Publish三个action分别使用
  `publication_preparation_not_executed -> task-publication-preparation-not-executed`、
  `branch_push_not_executed -> task-branch-push-not-executed`和
  `pr_creation_not_executed -> task-pr-creation-not-executed`，output只携带对应action的最小identity且互不兼容。
  Stock maintenance 的需要确认 mutation 统一进入 `stock-policy-action-confirmation-wait`：normal affirmative
  只进入 standalone/embedded/reapply 的 profile-fixed action re-entry，missing 保持 wait，refusal 使用各自
  action-not-executed，material drift 零副作用返回 exact Stock owner 重建计划；不得从 action-state
  continuation 直接执行 mutation。
  active-lifecycle disposition cleanup是唯一特殊形状：回复
  已含唯一retain/suspend choice时直接消费，否则只能得到
  `active_lifecycle_disposition_choice_required`并进入
  `active-lifecycle-disposition-choice-wait`；choice current前删除为0，不能制造not-executed terminal或双结果。
  disposition cleanup与delivery-terminal Cleanup分别通过自己命名的dialogue-local wait及continuation re-entry；
  confirmation reply/authorization永不进入DTO、checkpoint、gate、history或durable result。

## 12. Merged Capability Preservation And Eligibility

- `EVO-DES-070`：Evolution prerequisite采用两道不可互换的gate。Design入口只消费同一exact selected-base
  identity下current `prerequisite_merge_identity_current`、`requirements_ready_for_design`与
  `requirements_trace_ready_for_design`，不得重新把Design successor当作Requirements readiness前置。
  Design owner展开83个Requirement、33个NFR、23个current capability、13个target delta与50个fixture，
  验证每项至少到达一个语义充分的Design responsibility/contract和fixture mapping，并执行fresh full review；
  只有Design差集、P1/P2/P3 finding和high-risk question均为0，才产生
  `design_ready_for_delivery_planning` / `fresh_design_review_passed`，并由closed gate projection形成
  `evolution_prerequisite_current -> evolution_refactor_eligible`。该projection只允许未来Evolution delivery
  intake读取，不创建runtime resource或副作用，也不预选新的public Skill。selected base、merge、RDT/
  Architecture、capability、Requirements、fixture或Design identity material drift使较晚gate stale并返回最早
  受影响owner；等价identity refresh不重放unchanged semantic review。
- `EVO-DES-071`：`guru-reconcile-task-base`在任何base/current-work continuation前，以live common-dir、cwd、
  runtime mapping、task/worktree/branch identity和per-path ownership/state恢复唯一original active worktree。
  current-base tracked且逐路径clean的same-task文件继续原worktree，不因路径存在或通用source-clean开关误阻断；
  dirty/untracked same-task文件、`review.md`/`reviews/**`、review/check metadata或identity mismatch仍进入exact
  Reconcile blocker。source checkout与task worktree的unrelated dirty状态保持原owner、原bytes/index/worktree
  state，不被归为same-task blocker，也不得被本owner修改、stage、清理或忽略。该判断只改变
  `reconciled|blocked`分类，不扩张allowed writes或绕过真实artifact/identity blocker。
- `EVO-DES-072`：#311 installed publication preservation由现有owner分层承接而不增加public Skill：
  `guru-publish-task-pr`拥有closed source/target binding、metadata-only publication preparation、branch push与
  Draft PR；`guru-finalize-task`拥有summary、official archive、archive commit/push、Ready与schema-valid
  `ready_for_merge`；`guru-merge-task-pr`只消费archive-bound expected head；Cleanup只在delivery terminal后运行。
  Publish的三个拒绝输出分别终止于`task-publication-preparation-not-executed`、
  `task-branch-push-not-executed`与`task-pr-creation-not-executed`，不得共享缺省terminal或遗漏consumer。
  reviewed-content identity通过allowlisted provenance normalization保持不变，publication/archive head分别绑定
  direct-parent lineage与exact generated bytes。self-hosted与installed均可达同一terminal；missing/mutable/
  mismatched source、target-as-source、额外managed/task/sidecar/config diff与partial remote state各由exact owner
  fail closed/recover。terminal reinvoke对metadata tail、branch push、PR、archive、archive push、Ready、merge和
  cleanup的completed mutation replay均为0，Finalizer不读取verifier evidence。
- `EVO-DES-073`：standalone extension verifier由
  `guru-validate-extension-projection:standalone|standalone_reentry`拥有failure lifecycle。deterministic runner在
  pre-matrix、matrix-cell或post-matrix真实failure边界先构造schema-valid non-null private failure result，字段
  至少包含actual stage、applicable matrix cell、stable command label、exit code、bounded credential-safe tail与
  stdout/stderr hash/size；matrix外command/asset inventory/ownership/sidecar/capability failure统一为
  `postcheck_failure`。Projection owner校验并绑定`failure_ref`后才允许temporary cleanup，再输出
  `projection_validation_blocked`到named stop；stop可展示current failure/unverified boundary，只把
  `continuation_ref,repair_input`投影回`standalone_reentry`。raw stdout/stderr、authorization与完整lifecycle不进入
  public DTO或durable history。embedded clean/migration/Release只返回caller-owned finding，不创建/读取
  standalone failure state；Finish/Finalizer消费verifier lifecycle/gate/artifact/exit的edge为0。

## 13. Terminal Design Gate

Current `design_ready_for_delivery_planning` / `fresh_design_review_passed` candidate requires：

1. 本目录与Evolution Test全稿完成且导航/链接/manifest current；
2. `EVO-REQ-001..083`、`EVO-NFR-001..033`、`CUR-CAP-001..023`、`TARGET-DELTA-001..013`均有
   Design/Test successor，差集为0；
3. 50个`EVO-FIX-*`均有owner、candidate kind、evidence layer、blocked/re-entry和验收结果；其中Evolution
   prerequisite命中`EVO-DES-070`，base evolution命中`EVO-DES-071`，installed publication命中
   `EVO-DES-072`，verifier failure命中`EVO-DES-073`；
4. 17个stock asset action与9个retained host rows无unknown/duplicate/unbound consumer；
5. every required public consumer input的来源恰好是common invocation binding、selected exit的
   `direct|select|rename|normalize` projection或该consumer exact section owner；缺失producer、generic frame、
   hidden seed、private checkpoint/envelope-file、ambient/runtime lookup均为0。every public output字段有direct
   consumer；caller-owned clarification、authority repair、bootstrap、base reconciliation与post-review
   promotion均有profile-fixed producer/consumer；普通recoverable block必须命中第7.1节唯一same-owner
   profile；Admission lifecycle binding、post-receipt isolation与Answer provider block必须三者独立，前两者
   分别从自己的re-entry恢复且Answer provider可重入；bound event必须以
   `bound_event_ref,event_sequence`直达exact owner，不得只传sequence或ambient lookup；stable
   `authority_context`必须给Clarification/RDT/Architecture subprojection各自唯一owner，并让Plan/Approval及
   后续semantic owner直接使用同一bound authority content而不是summary handoff；wording的九个closed caller
   profile与四类return、qualification scope choice必须经profile-fixed Clarification返回原caller fresh重建
   candidate，standalone qualification不得产生mechanism revision；RDT/Architecture Bootstrap必须原样返回
   各自caller continuation；bound-intent/current-work只使用closed owner/profile registry，post-owner/post-remote
   fresh Admission与remote disposition wait都必须由selected output构造；closed registry必须恰好覆盖37个
   lifecycle owner，并显式包含Admission/Route Request/Answer/Current Work/History；wording/qualification必须
   保持原caller ownership。Trellis reference必须由独立manifest/
   caller-fixed adapter承接且raw meta write surface为0；authority-promotion/code-spec触发的projection必须由Bootstrap唯一
   owner写入并回fresh Check/Commit/Review；clean/migration/standalone-stock拒绝后的same-owner action re-entry必须
   可构造，Stock action-required/partial/unknown 还必须经唯一 `stock-policy-action-confirmation-wait` 闭合
   normal affirmative、missing、refusal、material drift 与 standalone/embedded/reapply profile-fixed re-entry，
   action-state continuation 直接执行待确认 mutation 的路径为0；adapter output不得携带generic caller ref；R01..R09分别只交给exact host context owner，suppressed
   admission success只交给Route Request；standalone Stock只能由Projection owner调用，current只回Projection
   `stock_policy_reentry`并fresh validation，embedded Stock variants字段互斥；publication provenance、branch
   push与Draft PR creation必须有三个互不兼容的prepare/wait/confirmation re-entry/refusal/recovery，且任一确认
   不能构造下一action；三个refusal必须分别投影到`task-publication-preparation-not-executed`、
   `task-branch-push-not-executed`与`task-pr-creation-not-executed`，每个output/consumer唯一且可构造；
   Finish必须在Merge前形成official archive/archive push/Ready与archive-bound
   `ready_for_merge`，Merge后不得再次Finish；
   active-disposition cleanup拒绝在无唯一choice时恰好得到
   `active_lifecycle_disposition_choice_required`并进入一个choice wait，choice前删除为0；
   Workspace必须先live解析exact resource与ownership/isolation state；exact-current reuse必须直接
   `workspace_current -> task_impact_sync`，plan display、confirmation wait、refusal branch与mutation均为0，
   只有pending creation/transfer/isolation才进入确认边界；
   Approval的精确计划必须同时展示activation与进入approved implementation scope，确认只授权该复合行动；
   确定性activation必须在owner内收敛，并以`approved -> guru-implement-task:initial`闭合，transition failure时
   implementation write为0；
6. migration/projection/Release没有legacy consumer或断链；
7. `EVO-DES-001..073` fresh independent Design review未解决P1、blocking P2、P3与high-risk open question均为0；
8. 只形成delivery Issue建议，不创建Issue、不实现、不激活task、不commit/push/PR/merge/release。

Current gate passed against this revised candidate. #311/#312 merge, exact `.41` authority rebind, 83/13/50
Requirements-stage successor zero-loss and the merge-bound fresh Requirements gate remain current. The complete
Design/Test/Architecture/task projection closed `DES-REV-001..048`; the final fresh semantic review reported open
P1=0, blocking P2=0, P3=0 and high-risk question=0, and deterministic closure passed. The closed gate therefore
projects `design_ready_for_delivery_planning`, `fresh_design_review_passed` and `evolution_refactor_eligible`.
This continuation remains in Phase 1 and stops at that completed Design gate; no implementation or delivery action
is authorized.
