# Evolution Design Decisions

状态：`design_ready_for_delivery_planning` / `fresh_design_review_passed` / `evolution_refactor_eligible`。这些decision已从current
`requirements_ready_for_design` identity重审并补入#311/#312 prerequisite、`EVO-REQ-082..083`、
installed publication、verifier failure evidence与original-worktree continuity；它们仍不是current runtime
或accepted ADR。

- `EVO-DDEC-001`（accepted）：采用 `target_native`。最终 candidate 只运行新合同；不保留旧 route、
  dual-read/write、legacy schema selector、compatibility wrapper 或 fallback。
- `EVO-DDEC-002`（accepted）：保留 marketplace workflow id `guru-team`，通过新的 extension contract
  identity、完整 existing-migration 合同和原子 activation 做破坏性升级；不同时发布第二个可运行
  legacy workflow id。该选择满足“stable id 或明确迁移合同”的公共 API 规则。
- `EVO-DDEC-003`（accepted）：global workflow 只拥有 invocation/phase 顺序、mandatory Skill id、
  typed-exit consumer 和 fail-closed stop；每项 semantic responsibility 由一个 closed-loop Skill 独占。
- `EVO-DDEC-004`（accepted）：每个 independent invocation 只建立一个 owner-private
  `context_envelope`。RDT、Architecture、stock 与 provider facts 只由各 section owner首次读取和定向
  refresh，consumer经owner runtime取得authorized minimal projection，不形成第二条authority读取链；
  无依赖变化时不得全文重读。public edge 只允许 selected exit 的
  `direct|select|rename|normalize` projection；runtime-derived facts由exact consumer owner解析而不进入
  caller-authored input，禁止generic frame、implicit pass-through、producer checkpoint或ambient lookup补字段。
- `EVO-DDEC-005`（accepted）：`docs/requirements/evolution/`、本 Design 与
  `docs/test/evolution/` 是 target RDT authority；selected-base `.41` 继续是 current as-built authority，
  `.40`只作historical comparison。实施 task
  通过 contribution/promotion 推进 current，不从 task 三件套反推 repository RDT。
- `EVO-DDEC-006`（accepted）：standard Planning 新增唯一 author `guru-plan-task`，并保留一次
  `guru-approve-task-plan` semantic approval；normal path 删除 mandatory wording review、normal-scenario
  qualification 和 upstream brainstorm wrapper。
- `EVO-DDEC-007`（accepted）：standard Phase 2 的唯一 implementation owner 是新公共 Skill
  `guru-implement-task`。task-free 仍由 `guru-execute-task-free-change` 独占；每个 worker invocation
  恰好绑定两者之一。
- `EVO-DDEC-008`（accepted）：官方 Trellis package/source 继续由 upstream 独占。Guru preset 新增
  “post-projection policy” ownership，只管理 pinned source 生成后的精确 allowlist target；不修改
  upstream repo、全局 npm、package cache 或 `node_modules`。current ownership contract/schema 3.0 继续
  禁止 Guru 处理 official `trellis-*` paths；future transaction 必须先安装并验证 ownership 4.0/schema/
  validator 与 exact policy claim，再允许 selected stock mutation。该 handoff 不取得 upstream source
  ownership，也不提前激活 target workflow。
- `EVO-DDEC-009`（accepted）：九项 `suppressed_semantic_route` 选择 managed absence，不做内容 patch。
  删除前必须证明 Guru successor current；未知/用户修改/sidecar/identity mismatch 保留原文件并返回
  `upstream_suppression_blocked`。
- `EVO-DDEC-010`（accepted）：`trellis-channel`、`trellis-session-insight`、`trellis-break-loop` 的
  discoverable raw surface 选择 managed quarantine；caller 只通过 Guru-owned non-auto adapter 使用
  pinned CLI/reference。explicit-only 写入意图在 raw provider 调用前返回 Guru change owner。
- `EVO-DDEC-011`（accepted）：五项 stock worker projection 由 Guru-owned caller-bound worker
  definitions 替代；raw platform/channel worker 不进入 target dispatch inventory。worker 只返回
  observation/execution/evidence，不能决定 scope、finding、approval 或 route。platform implement 与
  channel implement 分别使用独立 adapter identity；两者各自闭合 `task_free|standard_phase2` profiles，
  不共享一个模糊 transport-neutral worker contract。
- `EVO-DDEC-012`（accepted）：stock policy 的 canonical source位于 Guru preset namespace，安装态
  provenance 位于 `.trellis/guru-team/extension.json` 的 closed stock-policy domain；pre-semantic
  admission guard 不执行 mutation。
- `EVO-DDEC-013`（accepted）：fresh install 顺序固定为 official Trellis projection -> Guru workflow
  -> Guru preset/stock policy -> validation；existing migration 使用 Requirements 指定的五个 substep、
  唯一 workflow cutover、mandatory preset reapply 和一次 final validation。UPDATE dry-run 含
  `MIGRATION REQUIRED` 时只走 `--migrate --skip-all`，否则只走 `--skip-all`；force/create-new 不替代该
  canonical 分支。
- `EVO-DDEC-014`（accepted）：invocation/task/provider recovery 使用可消费的短生命周期 private state；
  durable history只保留 cleanup 后仍不可重建的 terminal identity/result。授权、完整 stdout、完整 review
  history与 live 可重建 facts 永不持久化。
- `EVO-DDEC-015`（accepted）：Architecture impact 为 `architecture_impact/target_native`，因为本设计
  改变 entry owner、single writer、compatibility exit 与 distribution ownership；因此需要 task-owned
  contribution 与 ADR candidate，但本任务不 promotion shared current。
- `EVO-DDEC-016`（accepted）：普通 delivery slice 只运行 scope-targeted checks；完整三平台
  clean/existing matrix 与 exact-candidate Release 由末端专项 Issue 独占。
- `EVO-DDEC-017`（accepted）：parent repository workflow 永久默认排除 submodule；相关 Gitlink 仅在
  explicit independent repository scope 下进入新 invocation。
- `EVO-DDEC-018`（accepted）：流程优化以重复 gate/read/action、无 consumer artifact、intent loss 等
  correctness 零计数验收；耗时、rounds、bytes 与 compression 只作诊断，不设相对改善门槛。
- `EVO-DDEC-019`（accepted）：副作用确认不是独立 Skill、public DTO 或 digest challenge。每个 owning
  semantic Skill 先 live 判断是否仍有 action；no-mutation current exit 直接收敛，plan display、confirmation
  wait、refusal branch 与 mutation 均为 0。只有 action pending 时，owner 才私有生成并展示 current exact
  action plan，由 AI 在当前对话判断“确认继续”“可以，继续”等清晰肯定；确认只覆盖刚展示 action，
  material drift 后失效。READY PR merge 使用同一合同，不要求
  固定 `合并PR`。固定 prompt、口令、hash、digest、task id、path、branch、SHA、identity、摘要、规定句式
  或 `确认执行 <hash>` 均不得成为 challenge；脚本、validator、recorder 不解析、匹配、验证或持久化
  用户确认。每个明确拒绝进入该owner命名的zero-side-effect refusal output；Merge、manual Issue closure、
  Finish/archive、delivery-terminal Cleanup与active-lifecycle disposition cleanup互不继承确认，refusal不得
  伪装成blocked/provider defect。Stock action-required/partial/unknown continuation 只能先进入同一 owner 的
  `stock-policy-action-confirmation-wait`；确认后才进入 profile-fixed action re-entry，不能直接成为 mutation authority。
- `EVO-DDEC-020`（accepted）：standalone projection/stock、retained-host 与 embedded/reapply 使用互斥
  profile/exit schema。embedded child 只能返回 exact caller；不得取得 standalone blocked/current、
  workflow completion 或 caller terminal。reapply caller固定为Existing Migrator的ordered
  UPDATE/PRESET-REAPPLY cell；embedded Stock的current、required、partial、unknown、refusal与caller-finding
  `returned_to_caller` variants字段互斥，只有action-state variant携带action continuation；该 continuation
  经 exact caller 的 fixed edge 返回 Stock owner，并在需要 mutation 时先经过命名 confirmation wait，才可
  投影到 standalone/embedded/reapply 的 profile-fixed action re-entry。Release publication
  的zero-completed/unknown progress与true partial也使用互斥 re-entry/block schema。
- `EVO-DDEC-021`（accepted）：`EVO-DEL-01..08` 完成全部 39 个 public Skill 与 activation candidate 后才
  冻结 immutable matrix candidate。`EVO-DEL-09` 只对该 identity 执行完整矩阵；任一实现/合同修订都使
  matrix stale并从新 candidate 重跑。`EVO-DEL-10` 只调用已实现、已评审的 Release Skill 对同一 candidate
  发布与验证，不得在 Release slice 修改 candidate。
- `EVO-DDEC-022`（accepted）：跨 Skill wording/qualification clarification 与 repository Bootstrap只携带
  producer-profile固定、原caller拥有且中间owner不可展开的continuation。wording只允许一个standalone与
  四个active content owner的closed caller profiles；qualification scope必须由唯一Clarification owner取得
  真实choice，再回原caller重建完整candidate并fresh qualification；RDT/Architecture incomplete分别通过
  `rdt_request|architecture_request`进入Bootstrap，并只回对应authority owner的`bootstrap_reentry`。
  standalone qualification caller不是mechanism owner，不能产生mechanism-revision result/profile。router不得
  从task、producer checkpoint、envelope file或ambient state推断return owner。
- `EVO-DDEC-023`（accepted）：普通recoverable block使用`contracts.md`第7.1节的closed same-owner
  continuation/profile inventory；terminal/new-invocation结果不伪造continuation。Clean、Migration与standalone
  Stock的局部mutation refusal保留truthful action state并只从原owner action-reentry恢复；其它显式terminal
  refusal仍通过新invocation/current-work resolution继续。Admission的lifecycle-binding与independent-isolation
  block相互独立，Answer把adapter block提升为自己的recoverable result。bound intent/current-work resume使用
  exact owner/profile registry；remote disposition经named convergence wait回Disposition，post-owner/post-remote
  pending intent只能进入两个fresh Admission profiles。retained-host由R01..R09 profile固定到九个exact host
  context owner，suppressed guard success只到Route Request；controlled adapter由profile固定caller并同步返回，
  public output不携带generic caller id/ref。
- `EVO-DDEC-024`（accepted）：raw `trellis-meta` managed absence不以描述性“lazy reference”作为能力
  successor。Guru preset transaction单写`guru-trellis-reference-manifest-1.0`，source precedence固定为official
  docs解释扩展语义、local runtime解释installed facts、pinned package snapshot解释shipped-template facts；
  `guru-trellis-reference-read-adapter-1.0`只按standalone Answer或七个embedded caller profiles读取并同步返回。
  所有写入意图在adapter前进入active/new-change owner，raw matcher、semantic owner与write surface均不保留。
- `EVO-DDEC-025`（accepted）：raw `trellis-update-spec`的能力由现有public
  `guru-bootstrap-repository-ssot`新增`projection_refresh` profile承接，而不新增第40个public Skill。它是
  `.trellis/spec`唯一编排/写入owner；Branch Review独立选择`promotion_kind`与
  `projection_kind=none|authority_only|with_code_spec`；两个discriminator只选择相对live target identity尚未
  current的工作，不按complete diff中贡献的历史存在性重复选择。所有selected RDT/Architecture promotion
  （如有）current后，后两种生成`guru-code-spec-projection-1.0` locator/usage/freshness projection。
  `authority_only`在current projection缺失或持有stale authority locator/usage/freshness时选中，禁止code-spec
  ref，并允许与任一promotion kind组合，包括shared authority已经current时的`promotion_kind=none`；
  `with_code_spec`必须携带same-range、current projection尚未包含的reviewed contribution ref。
  `projection_kind=none`只允许没有outstanding promotion且没有任何missing/stale authority或code-spec projection；回程后的fresh
  Branch Review即使仍看见原贡献diff，也在promotion/projection target identities精确current时输出
  `promotion_kind=none,projection_kind=none`。material drift重新打开对应工作。成功只回fresh Check，再经
  新Commit与Branch Review；preset/reapply只验证identity/reachability，不能代写projection。
- `EVO-DDEC-026`（accepted）：metadata provenance preparation、branch push与Draft PR creation是
  `guru-publish-task-pr`内三个独立exact actions，分别使用
  `provenance_prepare -> task-publication-provenance-confirmation-wait -> provenance_confirmation_reentry`、
  `push_prepare -> task-branch-push-confirmation-wait -> push_confirmation_reentry`和
  `pr_create_prepare -> task-pr-creation-confirmation-wait -> pr_creation_confirmation_reentry`。三者拥有不同
  continuation、refusal、provider recovery；三个拒绝分别闭合为
  `publication_preparation_not_executed -> task-publication-preparation-not-executed`、
  `branch_push_not_executed -> task-branch-push-not-executed`和
  `pr_creation_not_executed -> task-pr-creation-not-executed`，每个output只携带该action的最小task/acceptance/head identity。
  每个prepare/re-entry先live-reread，exact tail、bound HEAD或
  exact base/head Draft/READY PR已current时分别无写入产生`publication_head_current`、`branch_published`或
  `draft_pr_current`，不得重复确认、commit、push或创建duplicate PR。任一confirmation永不授权下一action；
  PR current只进入Finish，不能直接Merge。
- `EVO-DDEC-027`（accepted）：causally bound user event必须以`bound_event_ref,event_sequence`直达closed
  lifecycle owner；ref绑定host event identity/session/content，sequence只负责arrival order，不能单独承担事件
  语义或触发ambient host-history lookup。`authority_context`的Clarification requirement-delta、repository RDT与
  Architecture subprojection各有唯一owner；适用semantic owner直接消费同一stable bound authority content，
  minimal public DTO不替代authority正文。`provider_context`的direct-consumer inventory必须覆盖每个已声明
  Git/GitHub/Trellis/preset/Release action owner，而不是只列delivery子集。
- `EVO-DDEC-028`（accepted）：`phase-1-task-activation`是`guru-approve-task-plan`在current semantic
  confirmation后的确定性substep，不是router或terminal。只有task transition current后才产生
  `approved -> guru-implement-task:initial`；transition failure留在Approval owner的recoverable block，避免
  planning approval与implementation之间出现unmapped result。
- `EVO-DDEC-029`（accepted）：39个public Skill中恰好37个可持有lifecycle，并全部进入Section 3.1
  registry；Admission、Route Request、Answer、Current Work resolution与History query不得因位于入口/查询
  边界而遗漏。Wording与Qualification两个specialist不接管lifecycle，fixed original caller在specialist
  wait/block期间继续拥有continuation与re-entry，避免额外specialist owner或generic resume route。
- `EVO-DDEC-030`（accepted）：standalone stock maintenance不增加第五个distribution action。
  `guru-validate-extension-projection:standalone`是`guru-maintain-stock-projection:standalone`的唯一caller；
  Stock action只在该route内执行，`stock_policy_current`绑定同一candidate/target并只回Projection的
  `stock_policy_reentry`，随后fresh完整projection validation才可完成workflow。Stock owner不能直接产生
  standalone workflow terminal。
- `EVO-DDEC-031`（accepted）：Planning唯一confirmation展示并授权一个compound next action：task status
  activation加立即进入approved `guru-implement-task:initial` scope/allowed-write boundary。它不形成第二个
  routine implementation-entry confirmation，也不授权Commit、push、PR、merge、Release或cleanup；activation
  transition失败时implementation write为0并留在Approval recovery。
- `EVO-DDEC-032`（accepted）：Workspace先解析exact current resource state，再决定是否存在待执行 action。
  repo/Issue/base/branch/worktree/task/path与ownership/isolation全部匹配current change identity时，直接产生
  `workspace_current`并进入RDT task impact，plan display、confirmation wait、refusal branch与mutation均为0；
  只有creation、transfer或isolation待执行时才按`EVO-REQ-081`展示计划并等待dialogue-local确认。
- `EVO-DDEC-033`（accepted）：#311/#312使用两阶段eligibility而不新增runtime wrapper Skill。
  `requirements_ready_for_design`只放行Design；83/33/23/13/50 Design successor与fixture mapping差集为0且fresh
  full review通过后，closed planning projection才产生`evolution_refactor_eligible`供未来delivery intake消费。
  Material drift回最早authority owner，等价identity refresh不重放unchanged review。
- `EVO-DDEC-034`（accepted）：#312 successor留在`guru-reconcile-task-base`。owner以original active
  worktree identity和per-path状态判定；current-base tracked/path-clean same-task继续，unrelated dirty保持原owner
  且不被修改，真实same-task dirty/untracked/review metadata/identity blocker继续fail closed。不得新增一个
  source-clean wrapper或通过source checkout cleanliness绕过task-worktree blocker。
- `EVO-DDEC-035`（accepted）：#311 publication不恢复旧Finalizer aggregate，也不把全部行为塞进Publish。
  Publish拥有immutable extension source/target reviewed checkout、metadata tail、branch push与Draft PR；Finish
  拥有summary、official archive、archive commit/push、Ready和archive-bound`ready_for_merge`；Merge只消费该
  identity，Closure与Cleanup继续分离。这样保留current terminal continuity，同时维持one owner per action。
- `EVO-DDEC-036`（accepted）：standalone verifier failure lifecycle归
  `guru-validate-extension-projection`，其private structured failure必须先于temporary cleanup；public block只
  增加direct-consumer需要的`failure_ref`，stop展示后只投影continuation/repair回same owner。Embedded
  clean/migration/Release保持caller-owned finding，Finish/Finalizer对verifier state零edge。

## Rejected Directions

- 为每个平台手工维护一套 workflow 或复制 step-local语义到 command/hook；会产生多个 owner。
- 只靠 frontmatter、workflow marker、hook absence 或自然语言提示抑制 stock；无法证明 auto-match 不冲突。
- patch upstream package/global install；不满足官方扩展与可恢复 update 边界。
- 保留所有 raw stock surface 再叠加 Guru guard；会继续产生双匹配和重复上下文。
- 为了避免 breaking migration 保留 legacy adapter；与 single-contract target 冲突。
- 将完整 invocation envelope、review artifact 或 authorization 搬进 public DTO；没有直接 consumer。
- 把 `确认执行 <hash>`、固定 prompt/口令、hash/digest/task/path/branch/SHA/identity/摘要复述、规定句式
  或 `合并PR` 词法匹配作为继续条件；这会把 AI 语义判断错误下放给字符串协议并把 freshness token
  误作授权 authority。
- 在一个 Issue 同时完成全部实现与 Release；无法建立可审核的串行 gate 和 exact-candidate evidence。
