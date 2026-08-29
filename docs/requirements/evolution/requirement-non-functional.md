# Guru Trellis Evolution 非功能需求

版本：`evolution-requirements-revision-2026-08-29`；状态：
`requirements_ready_for_design`。

本文件是 Evolution Requirements 非功能约束的唯一主定义。功能范围与场景见
[`requirement-main.md`](./requirement-main.md)，验收 fixture 与执行成本证据规则见该文件第 5 章。

## 1. 执行效率、安静性与上下文治理

`requirement-main.md` 的 `EVO-REQ-044..050` 是执行连续性功能行为的唯一主定义；本节只拥有
质量门槛与计数口径，不重新定义允许的消息类别、handoff 内容、resume route 或状态转换。
以下约束以 `requirement-main.md` 第 5.2 节的 action/consumer 与 correctness trace 为依据。
流程耗时、rounds、bytes、compression 次数及相对 baseline 改善比例可用于诊断，不作为
Requirements、candidate 或 Release 的验收门槛；不得通过删减能力、隐藏失败或跳过 gate 获得
表面上的短路径。

- `EVO-NFR-001`：对 `EVO-REQ-044..050` 定义的正常行为，没有新 authority、finding、选择或
  副作用变化时，重复 semantic gate、重复阶段往返和同一 owner 可合并却拆开的重复动作计数均为
  0；额外的 human-style assignment、approval/signoff chain 与 transaction handoff 计数也为 0，
  不设置相对耗时或轮次阈值。
- `EVO-NFR-002`：同一 exact unchanged source 在相邻阶段的重复正文/累计输出/private evidence
  注入计数为 0。适用 repository RDT、Architecture Baseline 与 task `prd.md`/`design.md`/
  `implement.md` 必须保持稳定 locator/identity/order，形成可由 host/model/provider 自然复用的稳定
  context prefix；decision-relevant live facts、current delta 与未解决项位于最小变化 tail。cache hit/miss、
  cached-token 数与 cache provider 只作诊断，不是 correctness 或 Release 门槛；具体允许传递的最小
  信息由 `EVO-REQ-045..048` 主定义，本条不维护第二份字段集合。
- `EVO-NFR-003`：正常路径保留动作的 direct-consumer 或 correctness/freshness coverage 为 100%；
  无 consumer 的脚本、validator、recorder、文档重读和外部状态查询计数为 0。
- `EVO-NFR-004`：`EVO-FIX-FULL-NORMAL` 必须覆盖 request-to-cleanup 的完整正常生命周期，并为
  每项保留的 handoff、读取、脚本、gate、validation 和 transition 说明不可替代的责任；无法说明
  直接 consumer 或 correctness 价值的动作必须删除。该 trace 必须证明每个 semantic owner 直接从
  current RDT/Architecture/task projection 与最小 live delta 作出判断，而不是消费前一 owner 的事务型
  交接或事实复述；不设置相对耗时或交互轮次门槛。
- `EVO-NFR-005`：正常 Planning 主动生成 continuation capsule 或非 durable 中间交接文件的计数为
  0；repository RDT、Architecture Baseline、task 三件套及其 current locator 不属于中间交接文件，
  但不得复制成第二份 cache/handoff authority。平台自动 context compression 只作为诊断信号，不作为
  PASS/FAIL 条件。发生
  compression/resume 时仍须按 `EVO-NFR-009` 恢复 current 工作，具体恢复行为由
  `EVO-REQ-046..047` 主定义。
- `EVO-NFR-006`：对 `EVO-REQ-049` 定义的 clear/no-finding 路径，暴露内部读取、projection、
  recorder、validator、locator 搬运、human-style assignment/signoff/transaction handoff 或
  already-current fact restatement 的用户可见消息计数为 0；允许展示的业务消息类别只由
  `EVO-REQ-049` 主定义。
- `EVO-NFR-007`：任一 public handoff/result 的字段都必须有唯一直接 consumer；无 consumer
  字段、可 live 重建事实、process metadata、授权和完整 evidence 不进入 public output。
- `EVO-NFR-008`：本条是执行连续性异常计数的唯一主定义。每个支持的 exact normal fixture/run
  中，invalid handle wait、decision-relevant truncation、duplicate cumulative stdout、
  unconsumed user intent、duplicate current-fact narration、human-style transaction handoff 和 orphan
  artifact 均为 0；workflow 主动生成但没有直接恢复 consumer 的 continuation capsule 计入 orphan
  artifact。术语对应的正向行为与 route 只引用
  `EVO-REQ-044..050`，不得在本文件另起一套功能合同。

## 2. 可靠性、恢复与可用性

`EVO-NFR-012..017` 按兼容、维护与安全语义定义在第 3、4 节；稳定编号不表示本节缺号或
重复定义，`EVO-NFR-018..033` 继续承接本节后新增的 submodule/stock 与 Evolution prerequisite 边界。

- `EVO-NFR-009`：本条只拥有 `EVO-REQ-010,041,047,076` 与对应 fixture 的可测质量门槛；preclassification、invocation identity/envelope、receipt、entry route、pending、owner、re-entry 和 terminal 的行为、字段与顺序均以 `requirement-main.md` 为唯一主定义，本条不重述。
  `EVO-FIX-ENTRY-ROUTING` 中，所有通过 pre-entry admission 的适用 independent invocation（包括无
  active lifecycle、active-wait、shared-scope-pending 与已证明隔离的输入）的 invocation-level route、
  new-change mode（仅对有明确文件变更目标的 new change）和 distribution/release action 覆盖率必须为
  100%；pre-entry redirect/blocked 单独归属 admission owner，不计作 route 缺失或成功；无 active
  lifecycle 的 independent input 必须立即进入唯一 receipt/isolation/guard 链，不得因没有旧 owner
  而被漏测或等待。
  `EVO-FIX-LATEST-INTENT` 必须按主定义枚举的输入/结果组合覆盖 owner-local、material、override、lifecycle-bound、independent、binding-blocked 与 isolation-pending/blocked，并记录对应的 exact owner、唯一 consumer、identity/freshness 与 re-entry evidence；覆盖率必须为 100%。对 `independent_request_isolation_pending`，还必须覆盖 progress-refresh、safe-clear/re-entry 与 no-progress/invalid-handle/non-consumable-owner -> `independent_request_isolation_blocked` 三类 liveness 分支；每次 re-evaluation 的三选一结果覆盖率必须为 100%，无界 pending、重复 pending、重复 receipt 或用相对耗时/轮次阈值替代事件/状态进展的计数均为 0。重复、遗漏、重排、提前消费、错误 owner/re-entry、错误默认 new change、绕过 entry selection、旧 candidate 改写和无 consumer pending 的计数均为 0。该条只度量 fixture/evidence，不建立第二份 route 或 receipt 合同。
  `EVO-FIX-REQUEST-STOP` 与 `EVO-FIX-HISTORY-RESUME` 的合法 stop、唯一 current recovery、equivalent-stale recovery、not-found/multiple/material-mismatch blocked 及 exact re-entry 覆盖率必须为 100%；stop 的新增/修改/cleanup/发布副作用为 0，blocked 不得猜测 current 或激活 history。通用只读请求的 direct-answer 分类、最小 live-fact 读取、unavailable/unverified 边界和 `direct_answer_completed -> workflow_completed` 覆盖率必须为 100%；只有 `REQ-UC-EVO-037..038` 可进入 top-level specialist，错误进入 mode/lifecycle、创建资源、修改被审对象或把 durable history query 隐藏为 direct answer 的计数均为 0。
  正向行为、状态转换和字段合同均回指上述 `EVO-REQ`，本条不维护第二份功能路线。
  对 `EVO-FIX-CHANGE-REQUEST`，ready、active duplicate、completed duplicate、scope clarification、
  linked-prerequisite blocked 与 resolution blocked 的分类、唯一 consumer、terminal/re-entry 覆盖率
  必须为 100%；重复资源/authoring、completed task 重启、scope choice 后未 fresh 重建 candidate、
  prerequisite/resolution 恢复后进入错误阶段的计数均为 0。
  对 `EVO-FIX-ACTIVE-DISPOSITION`，exact current-work resolution、无不可逆远端副作用时的
  retain/suspend/abandon 分类、未决“取消”意图的一次 choice 与 choice 前零 cleanup、deletable resource
  为 0 的 no-op abandonment、存在 deletable resource 的 cleanup plan、missing/stale/current
  confirmation、refused confirmation 的唯一 retain/suspend choice、唯一 resume/
  disposition/cleanup/history-query owner、cleanup 后可发现的最小 durable disposition/history、
  disposition completion 与 blocked exact re-entry 覆盖率必须为 100%；已有不可逆远端副作用时，原
  route 正常 terminal、forward-recovered terminal、terminal block 及其后无 local cleanup/
  eligible local cleanup 两类结果覆盖率必须为 100%。
  未确认 cleanup、拒绝后产生 `retained | suspended` 多终点、零资源 abandonment 仍要求副作用确认、
  unrelated/retained/durable resource 被删除、已完成删除重放、owner 扩张、cleanup 后 history
  不可查询或被隐藏、远端结果被删除/回滚/移动/重建、不可逆 outcome 被冒充
  cancelled/abandoned、terminal block
  被冒充成功，或 disposition/recovery 重新顶层分流的计数均为 0；正向行为只由
  `EVO-REQ-010,042..043,047,067` 主定义。
  对 `EVO-FIX-HISTORY-RESUME`，archive/finish 与 disposition durable result 的唯一 query owner、
  `durable_history_result_current`/blocked 分类、cleanup 后 discoverability 和只读 terminal 覆盖率
  必须为 100%；history query 重入、恢复或激活被查询 lifecycle，以及把 retained/suspended resume
  意图误作只读 history query 的计数均为 0。
  对 `EVO-FIX-WORDING-EXPLICIT`，review-only scope 必须覆盖 `pass`、route-level
  `specialist_revision_required`、`blocked`，
  change-scoped scope 必须覆盖 `pass`、`content_changed`、`blocked`；对
  `EVO-FIX-QUALIFY-EXPLICIT`，必须覆盖 `classified`、`scope_confirmation_required`、
  `mechanism_revision_required`、`blocked`，并覆盖 scope clarification 或 mechanism revision
  前提失败向 route-local `qualification_blocked` 的投影。各自的 active caller、standalone caller
  或指定 recovery owner 的唯一 consumer/re-entry/terminal 覆盖率必须为 100%；standalone `pass`、
  revision findings 与 qualification `classified` 都必须到达 `workflow_completed`，额外“修改或 stop”
  选择计数为 0。丢失、重复、提前消费、错误终止 active caller、把 review-only revision 静默变成
  new change 或把 qualification 非 classified 结果投影为 acceptance 的计数均为 0。
  对 `EVO-FIX-FINISH-RECOVERY`，单 task 的 archive/history/finish-summary 与 partial Cleanup failure
  attribution、live reread、exact-boundary re-entry 和 retained-ref/history reachability 覆盖率必须为
  100%；Delivery/archive/已 current Finish/已完成删除重放、cleanup owner 扩张、partial Finish 误报成功
  或 durable history 被隐藏的计数均为 0。
- `EVO-NFR-010`：`EVO-REQ-039,053..054,056,083` 覆盖的 Delivery、distribution、clean install、
  existing migration 与 Release 外部 provider failure，以及 `EVO-REQ-032,060` 覆盖的 base
  movement/refresh failure，必须产生明确 current blocked/recovery 边界。provider 场景必须可解释
  current contract/capability、source owner/contract locator、target/action 与 unknown-outcome
  classification；base 场景必须可查询 invocation checkout 的刷新前 identity/HEAD/dirty-untracked
  状态、selected base/ref/commit/diff identity、实际 refresh action、刷新结果与 checkout 未修改
  证明，并可解释 exact upstream identity 与影响范围。两类
  结果都必须解释最后确认的 live state、已完成与待执行副作用、权限/错误/可重试/幂等/停止分类、
  当前尝试是否仍在 Design 声明的有限等待/尝试策略内，以及唯一恢复入口；不得把 `unverified`、
  `skipped` 或历史结果冒充 PASS。
  每个 blocked、recovery、active wait、partial 或 unknown result 都必须由其 owning caller/route
  owner 提供一个可查询的最小 current result（durable history query 由 history owner 提供），至少
  包含 exact invocation/candidate/action identity、current state/phase/owner、适用时的
  RDT/Architecture identity 与片段、provider contract/source identity、最后确认的 live state、
  已完成/待执行/未知动作、错误或权限/配额分类、重试/停止分类与有限边界、唯一 re-entry 输入和
  unverified boundary。具体使用日志、指标、trace 或 public result 的哪种载体由 Design 决定，但
  查询入口、直接 consumer 和上述最小字段不能省略；没有常驻服务时，owner result/history query
  即为可查询入口。
  timeout/unavailable、认证或权限拒绝、限流/配额、不可重试拒绝、unknown/partial、stale identity、
  invalid handle、重复不可逆动作、未消费 intent 或 orphan artifact 一旦观察到，必须在下一动作前
  形成对应事件并进入既定 recovery/blocked/terminal 边界；不能以继续等待或历史结果掩盖。相同事实
  不得重复产生语义 gate。该事件阈值只约束 correctness/可解释性，不引入耗时、rounds、bytes 或
  相对 baseline 的 PASS/FAIL 门槛。
  对 standalone verifier execution failure，事件形成必须先于 temporary workspace cleanup，且
  `EVO-FIX-VERIFIER-FAILURE-EVIDENCE` 中 matrix-command failure 与 matrix 外
  `postcheck_failure` 的 structured evidence、owner attribution、blocked result 与 exact re-entry
  覆盖率均为 100%；`failed + null failure`、cleanup 后补录、错误 stage/cell、Finalizer consumer 或
  内嵌 caller finding 夺取 standalone ownership 的计数均为 0。
- `EVO-NFR-011`：本条只拥有 `EVO-REQ-033` 并行隔离行为的质量门槛，并在同一 fixture 中验证
  `EVO-REQ-076` 的独立请求隔离 liveness；产品行为与状态顺序仍只由 `requirement-main.md` 主定义。
  对同一 exact base 上 A=`github_pr`、B=`none` 的双 task fixture，两种 completion/merge order 中
  task-local resource、provider、archive、Finish、cleanup、history 与 retained-ref 的交叉写入、错误
  归属、副作用重放和 failure propagation 均为 0；B 的 GitHub I/O 为 0，两个 task 各自 recovery 后
  的 history/current result 与 cleanup 前后 retained-ref reachability 覆盖率均为 100%。在两个
  completion order 中分别注入一个与旧 lifecycle 共享可变 scope/不可逆边界的 independent request：
  只有存在可观察下一进展事件时才允许 pending；每次 re-evaluation 必须得到 progress-refresh、
  safe-clear/re-entry 或 no-progress/invalid-handle/non-consumable-owner ->
  `independent_request_isolation_blocked`，独立请求不得被旧 owner 吞并且 admission receipt 不得重复。
  无界 pending、饥饿、重复 receipt、相对耗时/轮次阈值替代 liveness 判断及跨 task failure propagation
  的计数均为 0。shared authority 仍只经 serialized promotion 前进。
- `EVO-NFR-018`：parent repository 的正常 mode selection、Intake、RDT/Architecture Planning、
  Implementation、validation、Finish 与 Cleanup 不得依赖无关 Git submodule 的初始化、可访问性、
  clean/branch 状态或命令成功；默认路径的 submodule I/O 与 validation 为 0。显式 submodule
  repository scope 必须隔离运行，不能扩大 parent task 的 authority、artifact 或验证集合。

- `EVO-NFR-019`：`current-capability-inventory.md` 中绑定的 17 个 logical stock asset 必须恰好
  落入 `suppressed_semantic_route=9`、`provider_only=1`、`explicit_only=2` 或
  `controlled_worker_provider=5`，每行有一个 Guru successor/保留理由、一个 policy binding、
  一个 projection cell 集合、一个 Design handoff/status 与一个直接验证 fixture；其 consumer
  栏必须明确记录“真实 current direct consumer”，或在尚未绑定时记录可审计的
  `consumer_unbound/current_drift` 与 Design handoff projection。后者不是 current closure，不能
  冒充 active consumer。三类 `retained_nonsemantic` surface 必须拆为九个 host-bound row（每类三
  host），并各自有真实 host/policy consumer 或 `retained_context_blocked` repair handoff。
  覆盖维度是一次 shared `.agents/skills` projection layer 加上 Codex、Claude、Cursor 三个
  supported host；shared layer 不作为第四个 host 重复计数。未知、重复、同一 asset 的多重 role、
  未声明 successor/保留理由/consumer-or-handoff 的数量均为 0；官方其它平台只能作为 source-only
  boundary，不计入 Guru supported projection coverage。Requirements closure 只在真实 consumer
  或明确的 handoff projection、owner、re-entry 和 blocked contract 均可追踪时成立；handoff 本身
  不等于 current closure。
- `EVO-NFR-020`：对 `EVO-REQ-069` 的 shared-layer/host/context 每个支持 cell，stock semantic
  auto-dispatch 与 Guru entry/lifecycle owner 必须恰好选择一个；九项 `suppressed_semantic_route`
  在第一项 semantic 行为前必须由 admission guard intercept、redirect 或 fail closed。admission
  guard 不得在 route/action 选择前执行 patch、absence/quarantine、delete 或其它 mutation；这些
  action 只有在已选且 caller/scope/target 绑定的 maintenance/provider action 中才可发生。第二个 `entry_route_selected`、
  第二次 semantic approval、重复 requirement/full-document read、重复 routine question、重复副作用
  或 stock route 改写已选 Guru route 的计数均为 0；stock matcher 不得因普通自然语言直接恢复任何 suppressed raw asset，
  包括 raw `trellis-spec-bootstrap`。该零计数与 context matrix 只在
  `EVO-FIX-STOCK-COEXISTENCE` 中判定，不由 workflow marker 单独证明。
- `EVO-NFR-021`：`provider_only`、`controlled_worker_provider` 和 `explicit_only` 的每次调用
  必须可回指真实 Guru caller 或明确的 `design_handoff`、current scope、source identity、调用
  profile、输入范围、最小 result/typed exit、回程和 consumer。当前不存在的
  `guru-phase2-implementation-coordinator` 必须标为 `current_drift`，不能作为 active caller
  计数；`STOCK-CONSUMER-*` 也不能作为真实 consumer 计数。唯一 provider 只能返回 caller-bound
  channel transport；五项 worker 只能返回 caller-bound research observation、implementation execution
  或 check evidence，不能触发 intent/scope/sufficiency/finding/severity/
  approval/revision/route/publication/merge/Finish/cleanup 判断。`explicit_only` 只允许
  `trellis-session-insight` 的显式历史检索与 `trellis-break-loop` 的显式诊断；任何 spec/Issue/文档/
  代码 follow-up 写入意图必须在 raw explicit invocation 前回到 Guru `new change` 或已绑定 active
  caller；实际写入由该 caller 绑定 exact scope/action/target/consumer，raw explicit write 调用数为 0，
  不得改写 Requirements/Design/Test、Architecture、product 或 route authority。
  raw `trellis-before-dev`、raw `trellis-update-spec` 与 raw `trellis-meta` 均属于 suppressed：其可观察
  能力必须分别由同一 envelope 派生的 Guru-owned `implementation_context`、受治理的 RDT/
  Architecture/code-spec contribution-to-projection、lazy read-only Trellis reference + Guru change
  lifecycle 承接；raw 调用、auto-match 与独立全文读取/写入链计数均为 0。
  provider 自行提问、第二 gate、越权继续下游、把 provider result 当 semantic pass，或显式写入
  越界 authority 的计数均为 0。raw `trellis-spec-bootstrap` 不属于 provider；若未来 adapter 只能
  证明 observation，必须用独立 Guru identity，raw asset 仍按 suppressed 验收。九项
  `suppressed_semantic_route` 的 stock auto-trigger guard 或任一 Guru successor 无损承接无法证明时，
  必须得到 `upstream_suppression_blocked`；其它 role 的 caller/profile/guard binding 无法证明时才得到
  `provider_boundary_blocked`；任一分支都不得直接调用风险 surface。standalone exact explicit-only 的
  history/diagnostic 只读请求必须覆盖 `explicit_provider_result_current -> direct_answer_completed ->
  workflow_completed`，其中 unavailable/unverified 是答案边界而不是 provider success；要求
  follow-up 写入的请求必须在 raw explicit invocation 前重新归类为 `new change` 或回到 active caller，
  不能由 stock-policy owner 形成 standalone terminal。direct-answer caller 内部的 channel/research/check
  provider 与 active caller 内嵌的 provider/worker/explicit read-only result 必须先形成
  `provider_result_current`，再投影为 `returned_to_unique_caller`；caller/target/consumer 不唯一时才得到
  `provider_boundary_blocked`。
- `EVO-NFR-022`：对 `EVO-REQ-071..080` 已选的 suppression/provider/explicit/retained action，
  每个 asset 必须可观察地绑定恰好一个 current action identity；action 的语义选择仍只由
  `EVO-REQ-071` 拥有，本条不重新选择或排序 action。
  只需在同一 invocation `context_envelope` 中建立一次最小 `stock_policy_context`（含 provenance）
  即可绑定 package name/version、source version/path、目标 projection cell、必要 template
  hash/manifest、用户修改/删除状态和 `.new`/`.bak` 或等价 sidecar 状态；该 projection 与适用的
  `authority_context`/`provider_context` 必须共用同一 envelope，不得各自启动第二次完整读取。
  registry integrity/tarball identity 仅在 source snapshot 变化或该 action 无法唯一确认时读取，不得
  为每个内部 Skill/worker 重复扫描。action 的选择、兼容性优先级、successor 证明与未选方案的否决
  只由 `EVO-REQ-071` 主定义；本条只校验已选 action 的 identity/provenance 与执行质量，不再规定
  “精确移除优先”或 patch/quarantine/provider 的选择顺序。重复人工 patch loop、宽泛 glob 删除、
  用户修改误判为 stock、来源/hash/路径不唯一、未处理 sidecar 或无法证明 successor 时不得覆盖、删除
  或激活 target contract。对 raw before-dev/update-spec/meta，successor proof 必须分别绑定
  `implementation_context` 两个 profile、governed code-spec contribution-to-projection 与 lazy
  reference/new-change lifecycle；raw absence 但 successor 不可达仍是阻断性
  capability-preservation/consistency finding，按 suppressed role 必须得到
  `upstream_suppression_blocked`；它不属于 `EVO-NFR-012` 的 capability-loss gate，也不能成为
  `stock_policy_current`。standalone policy/projection
  校验按 role 分别保留现状并得到 `upstream_suppression_blocked` 或 `provider_boundary_blocked`；
  嵌入 clean-install、migration 或 Release pre-publish 时只回传最小 caller finding。只有 Design
  选定的 action 需要 completed/pending/unknown、已完成/待执行动作、独立 state、不可逆边界和唯一
  恢复 owner；首次全 pending 必须得到 `stock_policy_action_required`，unknown 不得当作成功，已完成
  或不可逆动作不得重放。pre-entry admission 不得执行所选 mutation；未选 action 不要求单独验证。retained row 失败必须得到
  `retained_context_blocked`；用户授权过程不得写入 artifact、checkpoint 或 public result。
- `EVO-NFR-023`：fresh init 只适用于 `EVO-REQ-010` 判定的 `clean_target`；existing migration
  只适用于 `existing_migration_target`。可唯一归属的 official Trellis managed installation footprint
  即使 active workflow 与 Guru projection 均缺失，也必须按 existing migration 处理；partial/legacy Guru
  surface 即使 workflow 缺失同样不得按 clean 处理，mixed/unknown/unowned/multiple identity 只能得到
  `distribution_state_blocked`。fresh init、
  existing migration、`trellis update`、`upgrade`、workflow switch、preset reapply、`--force` 与
  `--create-new` 只作为一个已选 top-level distribution/maintenance invocation 下的 provider action
  或 control subcell；启动该 top-level invocation 的独立用户输入必须在进入 route/caller 前经过一次最小
  `pre_semantic_dispatch_guard`。正常 clear/redirect 路径只执行一次，只有 role-local blocked 的修复
  前提 current 后才可按同一 invocation/envelope/receipt 精确重入，不得新建第二个 guard。该 guard
  只能 redirect 或 fail closed，不执行 mutation。通过该
  admission guard 后，只有已选 route/caller 且实际触及 stock surface 的 cell 才进入一次
  `stock_policy_evaluation`；同一 invocation 的后续 migration/provider substep、caller 或 worker
  以及已绑定 provider/worker return、upstream CLI stimulus 或 native event 都复用这次 guard 与
  caller-owned policy 结果，不生成新的 `request_received`、不重新顶层分流，也不重复执行 guard。
  每个 concrete host policy fixture 恰好绑定 `EVO-REQ-080` 一个适用 setup discriminator；七个 cell
  作为 per-host partition 汇总覆盖，不与高层 hook configuration 做交叉乘积。setup unknown、
  emission 与配置不一致或 hook absence 被误判为 suppression 时，只能返回 role-local blocked。
  同一 invocation 内
  后续 caller/worker 复用同一 `context_envelope` 中已经建立的 policy/authority projection；只有 package/source/projection/
  file/sidecar identity 或 decision-relevant live facts 变化时才定向 fresh reread。首次全 pending、
  部分完成或未知分别落入 recovery-required 的
  `stock_policy_action_required`/`stock_policy_action_partial`/`stock_policy_action_unknown`
  （优先级 `unknown > partial > action_required`，三者都不是成功/终端），随后只能得到
  `stock_policy_current`、对应 role-local blocked 或调用方拥有的 blocked/re-entry；不得使用未定义
  的“用户保留状态”。无 stock surface 的 direct answer、非 stock stop/history/specialist 不得
  承担完整 inventory/provenance scan。role-local 结果为：
  suppressed 使用 `upstream_suppression_blocked`，provider/explicit/worker 使用
  `provider_boundary_blocked`，retained host context 使用 `retained_context_blocked`；
  clean-install 为 `clean_install_blocked`，existing migration 按 live cutover state 为
  `pre_migration_current_preserved | migration_blocked`，Release pre-publish 为
  `release_pre_publish_blocked`，standalone policy/projection 才使用上述 role-specific stock
  blocked 结果。官方 update 的 user deletion preservation、modified-file decision、force overwrite、
  `.new` copy、backup 与重新生成文件不得留下第二 semantic owner、mixed semantic graph、未处理
  sidecar 或 stale policy。任何 partial/unknown 状态在 recovery 前必须复用同一 invocation 中仍
  current 的 `context_envelope` policy/authority projection；只有 package/source/projection identity、file/context/sidecar
  state 或 decision-relevant live facts 变化、过期或未知时，才定向 fresh reread 受影响 state，
  只能从对应 exact policy/caller owner 重入未完成或可安全重试的 action；无法证明安全重试时保持
  同一 role-local blocked，未经所需 identity/decision-relevant state fresh reread 的“自动恢复成功”
  计数为 0。
  `trellis update --dry-run` 包含 `MIGRATION REQUIRED` 时必须执行
  `trellis update --migrate --skip-all`，否则必须执行 `trellis update --skip-all`；两条分支都必须
  验证 `--skip-all` 保留 user modification，且 `.new`/backup/sidecar 状态被重新读取。命令语义
  仍属于 upstream provider facts。
  上述 Trellis CLI 命令只作为 provider test stimulus；若 Guru 改变命令/参数/输出/退出码语义，必须
  重新分类为 CLI contract 并建立 `CLI-INTENT-*`，不得沿用本矩阵的“不适用 CLI”结论。
- `EVO-NFR-024`：suppression 或 provider 化不得造成 current 用户能力损失。九项 suppressed
  asset 必须由 Guru successor/fixture 证明相同可观察结果仍可达；唯一 provider 必须证明 caller-bound
  channel transport，五项 worker 必须证明 caller-bound research/implementation/check result，两项
  explicit 必须证明 history query 与只读 diagnosis/recommendation；raw break-loop 的 follow-up 写入
  能力必须由 Guru `new change`/active caller successor 无损承接，而不是由 explicit raw action 保留。
  九个 retained host row
  必须由 host/policy consumer 证明 context preserve/reconcile 可达，失败时可发现为
  `retained_context_blocked`。任何因删除/absence/patch
  导致的 active lifecycle、archive/finish/disposition history、RDT/Architecture authority、clean
  install/migration 或 Release capability 不可恢复/不可查询，均为阻断性差集，不得以“旧 Skill 不
  保留”豁免；`EVO-FIX-STOCK-COEXISTENCE` 与 `EVO-FIX-STOCK-MAINTENANCE` 必须共同覆盖该差集。
- `EVO-NFR-025`：stock policy 的例外恢复必须绑定精确 asset、scope、action、caller、source
  version、projection cell 和有效时点，并证明不会与 Guru semantic owner 重叠。exact explicit-only
  只允许 read-only history/diagnostic action；关联请求出现写入意图时必须在 raw invocation 前回到
  Guru `new change` 或 exact active caller，route/target/consumer 不能唯一绑定时 fail closed。
  普通自然语言触发的例外恢复、legacy fallback、dual-read、dual-write 或 dual-gate 计数均为 0。

- `EVO-NFR-026`：17 个 stock role row 的 successor/policy/projection/action/blocked binding 与九个
  retained row 的 host/policy handoff 覆盖率必须为 100%；其中一项 provider、两项 logical explicit
  asset（各自的 standalone/embedded profile）与五项 worker row 的 caller/profile/input/minimal
  result/typed-exit/consumer/re-entry 覆盖率必须为 100%，
  九项 suppressed row 则必须证明 raw caller 为 0、Guru successor 可达且 suppression failure 只回
  `upstream_suppression_blocked`。真实 active caller 不存在时必须明确标记 `current_drift`/
  `design_handoff`，Requirements gate 不得把该行声明为 current closure。provider/worker 与 channel
  worker 必须分别证明 platform-agent、channel-runtime 和 spawning-caller 的边界；platform
  `trellis-implement` 与 channel `implement` 都必须分别覆盖 task-free/标准 Phase 2 profile，每次
  invocation 恰好绑定一个 implementation owner，不能以同一泛称 worker 或固定 task-free owner
  代替三者。
- `EVO-NFR-027`：首次全 pending、partial、unknown 三种 action 状态的优先级、owner、独立
  `file_state`/`context_state`/`sidecar_state`、不可逆边界与 exact re-entry 覆盖率必须为 100%；
  每个需要确认的 next stock mutation 必须经唯一 `stock-policy-action-confirmation-wait`，正常清晰肯定进入
  standalone/embedded/reapply 的 profile-fixed action re-entry，缺少确认保持 wait，明确拒绝进入对应
  action-not-executed，material drift 零副作用重建 current plan；从 action-state continuation 直接执行待确认
  mutation 或要求固定确认字符串的计数均为 0。
  `stock_policy_action_required` 被误报为 current、unknown 被猜测成功、已完成 action 被重放或
  在 identity/state/decision-relevant facts 已变化、过期或未知时未执行所需 fresh reread 的计数均为 0。
- `EVO-NFR-028`：source-stimulus 的适用范围、六类 stimulus、固定优先级、句中提及负例、passive context 隔离和 source-class collision 均以 `requirement-main.md` 的 `EVO-REQ-076` 与 `EVO-FIX-LATEST-INTENT` 为唯一行为主定义。本条只验证：适用 fixture 的分类、exact binding、唯一 owner/consumer 与固定 rank 覆盖率为 100%；lifecycle-bound/passive context 不进入统计，unknown/multiple class、ordinary 误触 stock、internal return 重新顶层分流、explicit/ordinary 双匹配和被动 context 抢占请求的计数为 0。
- `EVO-NFR-029`：官方 update dry-run 的 migration/non-migration discriminator 与两条 exact
  command 分支覆盖率必须为 100%；`--skip-all` 保留用户修改、`.new`/backup/sidecar 可解释，
  `--force` 冒充分支成功或 generic update 代替 exact command 的计数均为 0。
- `EVO-NFR-030`：无 stock surface 的 direct answer、非 stock stop/history/specialist 跳过完整
  stock policy scan 的覆盖率必须为 100%；pre-semantic guard 读取超出 source/matcher 最小 facts、
  在 route/action 选择前执行 mutation、改变 semantic route、制造 routine question 或让无关请求
  进入 `stock_policy_current` 的计数均为 0。pre-entry redirect/blocked 必须由 admission owner
  可查询并可精确 re-entry，但不计为 top-level route。
- `EVO-NFR-031`：Codex `hooks-enabled`、`hooks-disabled`、`no-hook` 三种配置，以及 Claude/
  Cursor `trellis-start` 的 hooks-enabled 与 hooks-disabled/no-hook 分支必须逐一验证 emission、
  context injection 和 suppression/redirect；这些高层配置必须从每个 supported host 的 setup
  discriminator partition 派生，不得与七个 cell 做交叉乘积。每个 concrete fixture 恰好选择一个
  `EVO-REQ-080` 的 `enabled_approved`、`enabled_pending`、`enabled_denied`、
  `feature_off_config_present`、`feature_on_config_absent`、`feature_off_config_absent`、
  `configuration_unknown` setup discriminator，并记录 `user_feature_flag`、
  `project_hook_config`、`one_time_approval`、`emission`、`context_injection`。
  `enabled_pending`/`enabled_denied` 只在 host 实际存在 one-time approval surface 时适用；无该 surface
  时必须以 host/provider fact 标为 `not_applicable`，enabled success 使用
  `one_time_approval=not_applicable`，N/A 不计作漏测。把 hook
  absence/not-emitted、feature flag off 或 approval 状态当作 suppression、配置缺失但仍 emitted、
  setup 与观察不一致、漏测任一 cell 或在第一项 semantic 行为后才隔离的计数均为 0；unknown 或
  不一致只能得到 role-local blocked 并从精确 setup repair 重入。
- `EVO-NFR-032`：invocation-scoped `context_envelope`、适用性判定、`authority_context`/`stock_policy_context`/`provider_context` projection、reuse 与定向失效均以 `requirement-main.md` 的 `EVO-REQ-026` 为唯一行为主定义。本条只验证：每个适用 normal invocation 的 envelope 建立一次、下游只消费最小 projection、无依赖变化时重复全文回读/authority resolution/注入/gate 为 0，发生依赖变化时从最早受影响 owner 定向刷新并使下游 freshness 失效；task-free 与标准 Phase 2 implementation 都从该 envelope 派生 Guru-owned `implementation_context`，每次恰好绑定一个 implementation owner，raw `trellis-before-dev` 调用与第二套 spec 全文读取链为 0；direct answer、非 stock stop/history/specialist 与 standalone read 不因无关 authority/inventory 扩大读取，RDT/Architecture 不被 stock/task-local artifact 替代，public handoff 不携带可由 projection/live facts 重建的字段。

## 3. 兼容、分发与可维护性

- `EVO-NFR-012`：shared `.agents/skills` projection layer、Codex、Claude、Cursor 与
  canonical/dogfood/installed 的 scenario、
  semantic result 和 re-entry/stop 必须一致。对 `EVO-REQ-053` 的每个 supported projection cell，
  capability-loss gate 只比较 `workflow`、`task_data`、`docs_authority`；独立的
  consistency/installation gate 比较 Skill API/interface/schema/command、distribution、
  managed/installed inventory、mode、template hash、sidecar、声明平台 parity 与 extension
  identity/version binding。shared layer 只计一次，host parity 必须按 Codex、Claude、Cursor 分别
  验证。两类 gate 的 drift 检出、分类、affected-surface 解释和 exact validation
  re-entry 覆盖率均必须为 100%；后一类 drift 仍阻断但不得计为 capability loss。top-level
  standalone mismatch 的 projection-owner attribution 与 `projection_validation_blocked` re-entry
  覆盖率必须为 100%；clean install、existing migration 或 Release pre-publish 内嵌 gate finding 的
  exact-caller return 覆盖率必须为 100%，错误取得 standalone projection ownership 或产生
  `projection_validation_blocked` 的计数为 0。错误 `projection_current`、未分类 projection failure
  和以其它 distribution route 掩盖 failure 的计数为 0。
- `EVO-NFR-013`：本条只拥有 `EVO-REQ-053` clean install、`EVO-REQ-054` existing migration，以及
  `EVO-REQ-056` Release pre-publish、publication 与 post-publish failure 的质量门槛，不重新定义
  phase、cutover 或 terminal categories。clean/migration 的入口分类覆盖率必须先证明
  `distribution_state_preclassification`：active workflow 缺失、且无任何可归属 official Trellis/Guru
  managed installation state 的 target 100% 判为 `clean_target`；存在可唯一归属的 official Trellis
  config/template-hash/scripts/spec/task/workspace/manifest（即使 workflow 与 Guru projection 缺失）、
  可识别 Guru current、可唯一归属的 partial/legacy Guru managed surface/sidecar/lifecycle/history/ref
  （即使 workflow 缺失），或已识别 non-Guru active workflow 的
  identity/provenance/owner 与当前安全 transition plan 已唯一收敛时，100% 判为
  `existing_migration_target`；non-Guru workflow 的 plan 尚未 current，以及
  mixed/unknown/unowned/multiple identity 100% 判为 `distribution_state_blocked`，且在 clarification/
  live repair 前 route 副作用为 0。foreign-workflow repair 后必须先重入 preclassification，正向分支
  不得要求预先 mutation，且 source workflow 保留到唯一 cutover。clean install 的每个 supported cell 都必须能够查询并解释 current
  install status，且 100% 落入 `new_contract_current` 或 `clean_install_blocked`；existing repository
  的五个 supported migration cell 是覆盖矩阵而非每次 invocation 的五个必执行动作，必须在一个
  composite invocation 中按 `MIG-CELL-INSTALL -> MIG-CELL-UPGRADE -> MIG-CELL-UPDATE -> MIG-CELL-WORKFLOW-SWITCH -> MIG-CELL-PRESET-REAPPLY`
  的顺序覆盖所有适用 substep。每个 invocation 只执行适用 cell；每个 `not_applicable` 必须有
  provider/help 或 live-state 依据，五项全 `not_applicable` 仍须形成 composite current 并执行一次
  final validation。五个 cell 共享一次 migration preflight、唯一 cutover 和一次 composite final
  validation；每个 cell 只额外绑定自己的 applicability、provider stimulus、step-local live delta、
  phase 与 exact-step blocked/re-entry，不能把 step-local current 当作完整 migration terminal，也
  不能以“同上”或其它 cell 结果代替该 step 的 provider evidence。所有适用的 INSTALL/UPGRADE/UPDATE
  与 WORKFLOW-SWITCH preview/preflight current（或在该有序 boundary 对 byte-equal target 的
  `not_applicable` current observation）后才进入 `migration_cutover_current`；invocation entry 即使已
  读取到 byte-equal target，也不得跳过前序适用 substep 或提前改变 cutover/failure 分类；随后必须形成
  `migration_preset_reapply_current`（适用 step current，或有 provider/live-state 依据的
  `not_applicable` current observation），并只在全部适用 substep current 后执行一次
  `migration_final_validation_current`。
  每个 cell 的 provider flag/profile
  discriminator 也必须逐一可复核：INSTALL 的完整 preservation profile 是
  `trellis init -y --skip-existing --claude --codex --cursor`，不声称 `--workflow guru-team` 会替换
  existing workflow；`trellis init --force` 只能是独立 overwrite control subcell，`--create-new` 对
  `trellis init` 为有依据的 N/A；UPDATE 以 `trellis update --dry-run` 后的
  `trellis update --migrate --skip-all` 或 `trellis update --skip-all` 分支为成功口径，
  `trellis update --force`/`trellis update --create-new` 只能是独立 control subcell；UPGRADE 只使用
  `trellis upgrade --tag <npm-dist-tag-or-version>`，PRESET-REAPPLY 两项均为 provider-help 依据的
  N/A；WORKFLOW-SWITCH 在 workflow 非字节相等时必须是 `trellis workflow ... --create-new` preview
  后显式 `trellis workflow ... --force` application；workflow 已与 target 字节相等时记录
  live-state `not_applicable`；该观察只能在固定顺序抵达 WORKFLOW-SWITCH boundary 后与 force write 一样
  形成唯一 migration cutover。flag 变体未绑定、
  用 no-flag workflow replacement 冒充确认、或以
  其它 cell 代替该 step 的计数均为 0。migration owner 必须按实际 live cutover state
  分类 composite terminal：cutover 前的
  preflight/application finding 可以在未执行 final validation 时直接落入
  `pre_migration_current_preserved` 并停止；进入 `migration_cutover_current` 后的 WORKFLOW-SWITCH、
  PRESET-REAPPLY 或 final validation finding 只允许按 live state forward recover，并分别重入
  `migration_cutover_current`、`migration_preset_reapply_current` 或
  `migration_final_validation_current`，最终只收敛为 `new_contract_current` 或
  `migration_blocked`；在 final
  validation current 前不得派发 target consumer。
  三类是唯一 composite terminal，substep 不产生独立 terminal。对迁移前可发现的 active/resumable work 与
  archived finish/history result，100% 必须在 cutover 前得到可解释的 preservation/migration 判定：
  能由新合同承接的，在 `new_contract_current` 后保持可恢复/可查询；不能承接的，只能在 cutover
  前保留 pre-migration current 并阻塞。Release pre-publish finding 的 Release-owner attribution、
  `release_pre_publish_blocked` 结果、新 candidate identity 与完整 gate rerun 覆盖率必须为 100%。三类
  caller 路径中的错误 projection terminal、历史静默丢失、legacy runtime consumer、可运行旧新混合
  graph、静默 authority 丢失、未分类 terminal、旧 candidate evidence 复用和发布后 legacy fallback
  均为 0。Release confirmation 缺失、明确拒绝、candidate identity/content 变化与 decision-relevant
  provider/target/gate facts 变化的分类覆盖率必须为 100%：缺失只保持 current wait，明确拒绝必须以
  `release_not_published` 零 publication 副作用完成，candidate/关键 facts 变化必须使旧 wait/确认失效并
  返回 pre-publish owner；stale wait 进入 publication、拒绝后仍保持 active wait、未重新验证受影响 gate、
  超时推断确认或持久化授权状态的计数均为 0。Release publication partial/blocked、post-publish
  recoverable blocked 与 semantic-defect
  `release_published_unverified` 的 exact-state classification、identity binding、唯一 re-entry/terminal
  覆盖率必须为 100%；publication/post-publish 返回 pre-publish、重新 publication、删除/移动/重建原
  tag/Release、把 published-unverified 冒充 verified、或在原 identity 上修订语义 defect 的计数均为
  0。post-publish defect follow-up 必须按 `requirement-main.md` 的 `EVO-REQ-056` 重新分类；若需
  文件/合同/产品修改，先完成独立 `new change` lifecycle，只有后续 `distribution/release` 的
  exact-candidate Release action 才允许创建新 candidate，其它分类创建 candidate 的计数必须为 0。
  用户本地修改与 current Requirements/Design/Test/Architecture authority 按官方语义保留。
- `EVO-NFR-033`：`EVO-REQ-082..083` 的 prerequisite freshness 与 capability-preservation gate 必须采用
  exact、可复核且不复用旧结论的质量口径。六个维度必须分别记录
  `accepted_implementation_scope`、`exact_merge_identity`、`merge_reachability`、
  `accepted_scope_findings`、`issue_lifecycle` 与 `open_followup_only`；`OPEN/CLOSED` 只属于
  lifecycle fact，不能替代其它五项。accepted scope 未完成、accepted-scope finding 未解决、exact
  merge identity 不可验证、merge 不可从 selected base 到达、或 `OPEN` 但 follow-up 边界不清时，
  Requirements-stage `evolution_prerequisite_blocked` 分类覆盖率必须为 100%，Evolution
  Design/runtime/delivery/activation/cutover/Release 副作用为 0。当前 selected base 已包含 #311
  PR #313/merge `21c7da1…` 与 #312 PR #314/merge `3efcce7…`；#311 的 `OPEN` 仅表示明确的
  production release、错误文件重试和 Issue closure follow-up，#312 为 `CLOSED`。这些 lifecycle
  结果不解除后续 fresh rebind、merged behavior reconciliation、requirement/normal-path fixture
  zero-loss 或 Requirements review gate。

  Requirements-stage prerequisite 成功样本必须在同一 exact selected-base identity 下证明：六维
  classification 可追溯率 100%；RDT、Architecture 与 inventory rebind coverage 100%；`CUR-CAP-*`、
  merged prerequisite capability 与 `TARGET-DELTA-001..013` 的 requirement/normal-path fixture successor
  coverage 100%；`EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION`、`EVO-FIX-BASE-EVOLUTION` 与
  `EVO-FIX-VERIFIER-FAILURE-EVIDENCE`、`EVO-FIX-EVOLUTION-PREREQUISITE` 的 Requirements-stage
  assertions 全部 current；23 个 current capability、13 个 target delta、83 个 requirement 与 50 个
  fixture 的 set closure 均 exact；capability
  requirement/fixture 差集、旧 snapshot/review 复用、installed extension source/target reviewed checkout
  混淆、base-tracked clean same-task false blocker、installed 路径未继续到唯一 Draft PR/archive/Ready/
  `ready_for_merge` 或重放 completed mutation、verifier failure 为 null/cleanup 先于 evidence/
  `postcheck_failure` 错误分类、source/task worktree unrelated dirty 误分类、
  dirty/untracked/review-metadata/identity blocker 漏检，以及 Requirements gate current 前启动 Design
  的计数均为 0。installed 与 self-hosted publication、clean-tracked continue、unrelated-dirty isolation
  与真实 workspace blocker 的正反向覆盖率均为 100%。这些断言通过并完成 fresh Requirements 全稿审核后
  只产生 `requirements_ready_for_design`；Design successor 不得成为该结果的前置。

  Design/refactor-stage 成功样本必须继续绑定同一 exact selected-base capability set，证明全部 current/
  merged capability 与 target delta 的 Design successor 和 fixture mapping coverage 100%、fresh Design
  full-review finding 为 0，才产生 `evolution_refactor_eligible`；此前 runtime/delivery/activation/cutover/
  Release 动作为 0。任何 merge/base/authority/behavior/requirement/fixture/Design-successor identity 的
  material change 必须使对应较晚 eligibility stale，并从最早受影响 gate 重做 fresh Requirements 或
  fresh Design 全稿审核；Requirements 阶段不得以满足本质量门槛为由预选 #311 的未来 owner、Skill、
  DTO 或实现机制。
- `EVO-NFR-014`：正常路径的 semantic owner 数量、持久 artifact 数量和 public data volume
  必须由直接业务责任/consumer 证明；不得为了“合同完整”新增 wrapper、schema 或 checkpoint。
  top-level specialist invocation 只允许 `REQ-UC-EVO-037` wording review-only 与
  `REQ-UC-EVO-038` qualification；不得用“有界 semantic review”扩张第三个 profile。对这两个显式
  specialist invocation，wording 的 review-only/change-scoped 两种 scope 与 qualification
  的四类 typed result 必须各有一个可追踪 owner 和唯一 result consumer；active caller、standalone
  caller、scope clarification、mechanism revision 与 blocked/re-entry 不得通过组合 wrapper、重复
  reviewer 或无 consumer checkpoint 拼接。standalone review-only 的 pass/revision result 报告后直接
  完成当前 invocation，不得新增只为等待“修改或 stop”选择的 wrapper/state/checkpoint。normal
  Planning 的 routine wording/qualification wrapper 调用计数仍为 0。
- `EVO-NFR-015`：同一事实在 Requirements/Design/Test/Architecture/workflow/Skill 中只有一个
  semantic owner；projection 只引用 identity/locator/version/status，不复制正文。specialist 的
  review-only/change-scoped 边界、各 profile result 的 caller ownership 与 re-entry 只由
  `requirement-main.md` 的 `EVO-REQ-010,057..058` 和对应 Skill contract 分层承接；通用只读 semantic
  review 属于 direct answer，不建立 specialist result graph。状态图、return
  matrix、fixture 与 inventory 只能引用该主定义，不能再定义一套 pass/content-change/blocked 或
  qualification route 语义。任何 result 无 owner、多个 consumer、active/standalone 混用或由 child
  validator 抢占 caller ownership 的计数均为 0。

## 4. 安全与隐私

- `EVO-NFR-016`：prompt、log、artifact、Issue、PR、history 与测试证据不得泄露 secret、token、
  private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。`EVO-REQ-083` 的 verifier
  error tail 必须 bounded 且 credential-safe：在保留定位 stage/cell/command/exit 所需错误语义的同时，
  对 credential、token、签名 URL 与敏感原始记录执行 redaction；tail 无界、包含 secret，或因过度
  redaction 而无法判断实际 failure boundary 的计数均为 0。stdout/stderr 只持久化 hash/size，不因本
  合同新增完整原始输出 artifact。
- `EVO-NFR-017`：Git/GitHub/Trellis、Release 与 cleanup 副作用只能发生在 `EVO-REQ-081`
  已完整展示并取得 dialogue-local semantic confirmation 的 exact target/scope/action，且 provider live
  permission/visibility 与全部 decision-relevant facts current 的边界上；认证、权限、target identity 或
  current plan 不可证明时必须保持零副作用并进入对应 owner blocked/recovery，不得降级到其它 route。
  `EVO-FIX-SEMANTIC-CONFIRMATION` 对完整 current 计划后的“确认继续”“可以，继续”及其它清晰语义
  肯定的接受覆盖率必须为 100%，并证明每次只推进刚展示 action；READY PR merge 不得要求固定
  `合并PR`。未完整展示计划、疑问/限制/条件/修改/部分选择/拒绝、material plan/live-fact drift 的
  零副作用与重新展示/route-local 收敛覆盖率必须为 100%。固定 prompt/口令要求、
  `确认执行 <hash>`、hash/digest challenge、task/path/branch/SHA 重复、摘要复述、规定句式、
  script/validator/recorder 对用户确认的解析/匹配/验证，以及 confirmation/authorization 在 schema、DTO、
  gate、checkpoint、artifact、history 中的持久化计数均为 0。plan/live-fact digest 可服务局部确定性
  freshness，但不得成为用户 challenge 或授权 authority。Stock pending mutation 同样必须由命名的
  `stock-policy-action-confirmation-wait` 承接，不能把 action-state continuation 直接当作 confirmation 或
  mutation authority。unrelated dirty/untracked files、worktree、
  branch、task 和远程资源必须保持不变。

## 5. 非功能范围豁免

| `waived_item` | `scope_refs` | `waiver_reason` | `risk_statement` |
| --- | --- | --- | --- |
| 服务端 QPS/并发吞吐 | 全局 | 本产品是本地/Agent 驱动的交互 workflow，无常驻服务端 API；本轮只治理 workflow 内无 consumer 动作、重复读取/注入和不必要交接，不设置替代性的吞吐或相对性能指标 | 不代表外部 GitHub/Trellis 服务性能；流程耗时与工具量可用于诊断，但不决定 PASS/FAIL |
| 恶意 actor、对抗输入、artifact 人为伪造、额外锁/TOCTOU | 全局 | 产品假设 honest-but-fallible 协作，按仓库 current 安全边界执行 | 普通 stale/mismatch、错误 recorder/validator 和 secret/副作用边界仍必须处理 |
| 旧 Guru workflow 合同兼容 | `REQ-UC-EVO-034..035` | 用户明确要求重构后只保留新合同 | existing repository 仍必须通过一次受支持迁移进入新合同；不能静默留在旧路径 |
