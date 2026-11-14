# Gen2 来源切片：恢复 Sync 普通输入兼容

## 1. 整体来源与术语

Task `808-release-v070-guru9` / generation 2，Delivery `f6f0708c-9406-4d11-9ab0-4877a18fb3ac`，profile 为 `pull_request`。整体权威为[根 PRD](../../prd.md)，accepted revision 为 `sha256:835586c0c5ca6a22a50a872ce8249a2548dfac4d6f84a4321f78f4d06addb950`。本批选择根 AC-01/03/05/06，不改整体 scope。

| 来源、具体位置 | 角色与本批用途 |
| --- | --- |
| [#808](https://github.com/castbox/guru-trellis/issues/808)：冻结候选与验收、前置与准备范围、完成条件与范围边界 | 要求：完整候选发现合法兼容缺陷时回准备 owner；修复后重新冻结，不把旧候选通过沿用 |
| [Sync 合同](../../../../../trellis/skills/guru-team/packages/guru-sync-base/references/contract.md)：Qualification confirmation refresh、Interface Public Handoff | 既有设计约束：普通 bare/public_input envelope、默认值与字段级诊断保持；结构化 return_identity 使用封闭当前合同 |
| [MIGRATION-811](../../../../../trellis/presets/guru-team/MIGRATION-811.md)：2.1 Consumer 自有输入与 AI 补写 | 既有兼容承诺：新增确认 envelope 不得收紧普通调用 |
| [MIGRATION-819](../../../../../trellis/presets/guru-team/MIGRATION-819.md)：公共选择器与消费者 | 当前迁移约束：Sync current input/envelope 3.0，仍明确引用 2.0 的普通及资格确认分支，不恢复退休 selector 或旧结果 |
| [#813](https://github.com/castbox/guru-trellis/issues/813)：要求4及交付与兼容边界 | 要求依据：旧同步型来源的兼容边界不得静默破坏；其已交付关闭事实不是本批通过 |
| [私有发布合同](../../../../../.agents/skills/release-guru-trellis-version/references/contract.md)：Two-Stage Lifecycle、Complete Source Before Actual Adoption、Stage 2 | 执行约束：来源先独立交付，真实 tools 采用再由后继切片完成；全部后置发布责任保持 |
| 原 Release reviewer 对 C `139626ac1e860ee67c03196ce664c4a2a7145152` 的完整报告及有界复现 | 原始观察：唯一 P2 finding；当前会话保留原输出，不写发布 ledger 或修改失败 C |

“普通调用”指不携 `return_identity` 的既有 Sync read/sync/skipped 调用。“结构化返回”指携该字段的资格确认或 existing_issue_intake 接续；两者的当前专用输入与消费者仍各归原 owner。来源设计的唯一处置将在本批 design 第3节维护。

## 2. 整体与本批目标、非目标

独立审核在上述 C 的真实公开 command 入口发送
`{"public_input":{"source_exit":"start","mode":"workflow","route":"original_request"}}`，
实际 exit 2，字段为 `invocation.schema_version`。仅增加原 `schema_version:"1.0"` 后，同入口实际 exit 0 / skipped。源码在原 mode/route/read/sync 处理前无条件校验新版 envelope 与 public aggregate，dispatcher 不补齐输入。

本批目标是恢复既有普通调用可用性和原默认/诊断，保留当前结构化返回的严格合同、固定 Git-object read 与实际 sync 行为。完整来源、必要回归和自身分发可用性必须在本批交付，不把来源缺陷留给后继采用才修。

不变更六项发布输入：repo `castbox/guru-trellis`、Issue #808、tag `v0.7.0-guru.9`、extension `0.7.0-guru.9`、CLI/Core `0.7.0-castbox.6`、前驱 `v0.7.0-guru.8`。不改 Fork/source lock、公共 shape/selector/exit、AI 判断职责、Task/session 语义或生产部署。不引入兼容 parser、自动猜 profile、状态、缓存或 fallback 体系，不扩攻击、并发、fault 或累计矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

gen0 D1/D2 已经 PR839/840 实际交付；gen1 verifier 修复通过 PR842 合并为 `74f361da28d24e02a797e9a33a97be1fede065ac`，该代 Completion/Closure/Finish/Cleanup 已实际完成，bookkeeping PR843 合并为 `139626ac1e860ee67c03196ce664c4a2a7145152`。原身份、scope、三个 Delivery 和两个 generation 的结果保持。当前 gen2 Reactivate、Identity/Ensure/Bind 和 Creation 均已实际成立。

本 checkout 起点为 C139626ac。固定开发 B 及其来源由原 constructor 在本批规划中实际确定；PR 目标名 main 不等于内容 B。原 C 的安装及其他确定性 gates 已执行，但其独立 Release review 因唯一 Sync finding 不通过，不能重标为 pass。

本批改变受管 runtime，因此当前安装尚不能证明修复已被实际采用。来源切片完整提交、独立 Review/readiness 和实际 delivered 后，原 Completion 应以 additional_delivery_required 接原 Creation，后继 slice 才从完整干净已交付来源执行原 source_locked tools、保留验证及完整质量交付。当前不预建后继 UUID 或安装事务。

全部准备业务后再由原 Completion/Closure no_mutation/Finish/Cleanup 收口；Stage 2 重新冻结唯一 fresh main candidate，执行全部原 gates、tag/smoke/Release、eafc/primary 收敛和 #808 关闭。旧 C 的限定 standalone 接受与其他通过仅保其原观察，不证明新候选。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置与动作 | 可观察结果 |
| --- | --- | --- |
| G2-SC-01 普通输入 | 既有公开 Sync 调用方，给合法 bare public object、无版本 public_input envelope 或正常版本化普通输入 | 按原 mode/route/operation 进入实际 skipped/read/sync，不因新增结构化 envelope 要求被拒绝 |
| G2-SC-02 默认与正常错误 | 普通调用省略原可省字段，或发生普通 mode/route/operation 参数错误 | repo_root、route、operation、source_exit 保原默认；原字段级错误及真实 Git/base 阻塞不被吞并或改成成功 |
| G2-SC-03 结构化返回 | 原资格确认或 existing_issue_intake caller 携真实 return_identity，使用当前 envelope/input | 严格校验与原 read/消费者投影保持；普通入口兼容不能替结构化分支补身份、猜选或绕过前置 |
| G2-SC-04 来源验证 | 原工程/审核 owner 通过公开 wrapper 和合法临时 Git fixture 执行原分支 | 观察真实 parser/route/read/sync 及结果；采用适用原覆盖，只补 bare/default 等真实缺口，不以文本或 mock 自证 |
| G2-SC-05 来源→采用→发布 | 本批实际 delivered 后原 Completion/Creation、tools 和各质量 owner | 来源与实际采用各自成立；本批不宣称已安装或已发布，后继与整体责任不遗漏 |

## 5. 完整行为、条件与约束

**G2-R-01 普通兼容（根 AC-01/05；SC-01/02）**：不携 return_identity 的普通调用保原 bare/public_input envelope 和正常版本化形式。mode 的原合法值保持；route 默认 repo_change，operation 默认 sync，repo_root 默认当前仓库，skipped 的 source_exit 默认 start。不能仅给测试补 schema_version 或放宽断言而保留原拒绝。

**G2-R-02 结构化当前合同（AC-01/05；SC-03）**：return_identity 分支继续使用当前封闭 envelope 3.0、current aggregate 3.0 及匹配专用输入。原资格确认/current Issue 返回的身份、固定 commit、continuation、handoff_profile 和唯一 consumer 不变。不得恢复已替换 selector、读取旧结果充当当前事实或建立另一套兼容 reader。

**G2-R-03 原确定性职责（AC-01/05；SC-01/02/03）**：Sync 仍为 deterministic；原 skipped/read/sync/blocked、固定对象及 authority checkout/fetch/ff-only/validator 行为不变。正常无效 mode/route/operation 按原字段诊断，真实 Git/source mismatch 或 dirty authority 保原阻塞；不把 parser 修复当 AI readiness 或 Completion。

**G2-R-04 必要行为回归（AC-05；SC-04）**：执行受影响普通公开调用与结构化返回覆盖。优先复用既有 skipped、真实临时 Git read/sync、默认和字段级错误用例；仅对真实未覆盖的 bare/无版本/default 入口补独立断言。被测 wrapper/dispatch/validation/route 必须执行，不能 mock 掉拒绝点、预填 producer 输出或镜像实现。组件、临时安装、真实 Agent 与外部发布分别报告。

**G2-R-05 完整来源及采用边界（AC-03/05；SC-04/05）**：本批完成 canonical runtime 与必要回归、source validation、全部受影响平台投影的来源可用性，以及原 RDT/Architecture after 判断。当前 target 的受管差额如实保留，真实 source_locked 采用由后继 slice 承担，不能以样本代替。本批如出现先采用才能满足自身来源验证的依赖，回原 Planning/Architecture，而非延期自身缺陷。

**G2-R-06 原交付与后置责任（AC-06；SC-05）**：全部 after 经原 TaskCommit、固定完整 committed candidate、新独立 Architecture/Check/full_review、publication eligibility、Delivery readiness、Publication 和 expected-head Merge。PR 中文 Refs #808；不关闭 #813 或 #808，不重写历史。整个 Task、终态与 Stage 2 分别由其原 owner 判断。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应要求/场景、入口与输入 | 必须观察及边界 |
| --- | --- | --- |
| G2-AC-01 | R01/03、SC01/02：原 public wrapper，普通三类合法 carrier 与原省略字段，必要临时 Git fixture | 原真实分支与默认可用，原字段级错误及 Git 阻塞保持；不只验证 schema 字面 |
| G2-AC-02 | R02/04、SC03/04：原结构化确认/Issue 返回 wrapper 及其现有有效/普通缺字段覆盖 | 当前严格 envelope/input 和返回身份/消费者保持；补普通兼容不放宽该域 |
| G2-AC-03 | R04/05、SC04：本批 source/受影响回归及一个必要临时目标的完整平台/managed bytes/mode/provenance 检查 | 来源完整可分发；临时目标观察与 dirty/local source 边界明确，不证明本 checkout 已正式采用 |
| G2-AC-04 | R05/06、SC05：必要知识 after、完整提交/独立质量及原 Delivery 交付链 | 本切片无延期来源缺陷，真实 Refs-only delivered；后继采用及整体 Completion、终态/发布责任保留 |

当前没有待用户选择的需求或重大技术取舍。恢复原承诺优先于新增退役普通 API 的迁移；具体最小落点由独立 candidate assessment 后的方案展开。没有实际实现或新候选通过。

## 7. Canonical 引用与本轮差额

- [REQ/DES/TST-811](../../../../../docs/requirements/current/qualifier-applicability.md)、[DES-811](../../../../../docs/design/current/qualifier-applicability.md)、[TST-811](../../../../../docs/test/current/qualifier-applicability.md)：Sync 确认接续与普通读/同步分工，current-knowledge 的原观察截止保持；本批恢复原消费者兼容，不新增资格语义。
- [RDT issue-content](../../../../../docs/requirements/current/issue-content.md)及配对 design/test：current Issue Intake 仍使用 MIGRATION-819 当前接口，本批不改变评审/评论/来源 authority。
- [Architecture](../../../../../docs/architecture/README.md) 的原 constitution/change contract、ownership/distribution：一个原 Sync owner，来源和实际采用分层；是否有真实知识差额由独立原 owner 判断，不预造 contribution/ADR。
- [质量规范](../../../../../.trellis/spec/workflow/quality-guidelines.md)、[因果语义](../../../../../.trellis/spec/workflow/causal-completion-semantics.md)及[减法规则](../../../../../.trellis/spec/workflow/subtraction-first-compatibility.md)：原调用与观察决定验证，直接演进原分支，不制造 fallback、重复测试或发布状态文档。

本 PRD 拥有当前需求；design 将拥有方案及唯一来源设计处置，implement 将拥有执行/验证及唯一 Delivery Policy/Docs Plan。后续原维护 owners 核实际 after；当前正文不替代 Approval、实现或 Release gate。
