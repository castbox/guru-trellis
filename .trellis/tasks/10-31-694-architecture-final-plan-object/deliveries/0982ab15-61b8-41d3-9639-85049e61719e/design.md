# D1：独立 final_plan 显式对象设计

## 1. 设计目标、需求承接与内容基线

本设计承接本批PRD的DR01..07、DS01..05和DAC01..05，覆盖整体R694-01..07及AC694-01..05。目标是在原Architecture final_plan中分开“本次评审对象”和“会话执行选择”，保完整对象校验、独立AI判断、正式typed结果和相邻consumer。

固定内容B为 `2dbaf308e6d5137bf640cfe546a078497c1c713a`：原 `DeliveryProjection.content_base(key, development_base=B, observed_target=main)` 实际返回该值。首次D1无前序Delivery；Planning H0也是B，最终实现H尚不存在。PR目标为main，目标推进不自动重选B或构成整合义务。

阶段适用authority为B下 `docs/architecture/README.md`（`guru-trellis-architecture`）、`00-foundation/design-constitution.md`（`guru-trellis-design-constitution-v1`）和`06-governance/change-contract.md`（`guru-trellis-architecture-change-contract-v1`）。独立candidate_assessment实际stdout为 `baseline_current / architecture_impact / target_native`，purpose=candidate_assessment，freshness=`sha256:7623f76c07e30a5ea824d2dc6cf7372a2e9bff9784043b31644a8a5f05f2c6d9`，decision refs为ARCH-DOM-019/043/045、ADR-024/035。该结果不代替本设计的final_plan或实现/晋升结果。

## 2. 当前系统、边界与目标差额

原workflow Explicit receiving-session continuation和Architecture Skill对所有Planning接收者要求Identity/Ensure及必要Bind/Selection。原Architecture invoke在Delivery planning guard调用`projection.current(key)`；有context时无绑定/选择被拒绝。原共享adapter只有无context时使用`_explicit_current(key)`，其`_require_explicit_task`承接原当前generation/C4/注册checkout检查。官方public record/session API拥有Task/Delivery事实和session选择，Guru不另建状态。

本批只在Architecture包本地选择final_plan的接入规则。共享`DeliveryProjection.current(key)`、原Creation/Bind writer及普通Planning consumers不变。原对象解析、scope/phase/root/design内容freshness及owner-result/output校验继续执行。对应Markdown编排先识别本次为独立final_plan对象评审，再由该Skill完成只读entry；其他接收仍按原跨Skill恢复。

没有前序本Task实现。当前代码尚未支持新接入；本设计中的方法和变化均为待实现。

## 3. 来源设计处置（唯一）

来源为[完整live #694](https://github.com/castbox/guru-trellis/issues/694)。下列技术承诺为规范性约束，不降为建议。

| 来源条款与原承诺 | 处置 | 设计落点、理由、影响和上游处置 |
| --- | --- | --- |
| 目标1：完整对象的新独立会话无需外部拼Bind/Selection，也不先写执行选择 | retain | §4/6在原final_plan本地只读entry中核对象，无新writer或wrapper；实现目标本身，不改来源。 |
| 目标2：Task/gen、C4、唯一checkout、公开关系/profile、非终态planning、scope/root/design freshness完整 | retain | §4/5保原校验并对final_plan所有入口核原显式Task/C4事实；§8正常失配验证。 |
| 目标3：对象不是选择，同对象复用，其他选择/损坏/冲突回原owner，无context原入口保持 | retain | §6按真实current kind和key处理；不改环境或全局current。 |
| 目标4：仅独立final_plan及派发；其他consumers保持；最小I/O或明确迁移 | retain | §4列实际共享consumers；§5不新增public字段/profile，§7成套采用指导。 |
| 目标5：一次性评审不改业务/规划/baseline/生命周期/session/资源；普通恢复保必要runtime写 | retain | §4只读边界及Markdown中两类职责；原正式invoke负责结果校验，无自动Bind/Selection。 |
| 目标6：fresh generic reviewer空历史，authority→对象→设计/consumers→解释；不预载PRD或pass | retain | §6派发读取合同不变，明确新entry发生在authority首读后；实际评审由独立AI，caller不填结论。 |
| 目标6：实际stdout保key/root/purpose/design freshness，只有合法成功到相邻Approval | retain | §5核原Interface当前aggregate/final_plan/consumer组合；Approval自身guard保持。错误consumer不改报成功。 |
| 目标7：原Architecture/RDT authority、canonical/workflow/派发、dogfood/声明平台同步 | retain | §9真实贡献/拟写完整单元，implement Docs Plan定位唯一owners和原晋升时点。 |
| 来源/非目标：不重做#695或#693方法，不改后端#961，不加专项/安装/矩阵、框架或OS加固 | retain | §7/8限定采用和定向验证；不新增产品范围、provider或安装组合。 |

没有change/reject项，也没有需改变source scope的决定。

## 4. 模块、职责与设计取舍

**D694-01：Architecture包本地entry。** 在`trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/runtime/invoke.py`提取小型Planning对象接入helper。唯一调用方是该原invoke的Delivery planning分支；helper根据已有`planning_purpose`判断：candidate_assessment使用原current规则，final_plan执行下节只读对象规则。它只选择客观校验路径，不判断impact、充分性或出口。正式AI gate/owner-result/invoke保持。

final_plan复用共享projection的原显式对象校验（当前Task/generation、C4及注册checkout），而不改变`current(key)`或新增全局fallback。原`resolve`/`planning_directory`、workflow profile和official public facts继续拥有公开关系。阶段、scope authority、root和design freshness继续在原Architecture validator核对。若抽取共享只读原子校验确有必要，仅暴露原职责的事实读取，不把“缺选择也可评审”的策略移入共享consumer；任何此类差额须由原独立owner判断。

**D694-02：保留选择错误。** helper先读取真实current；error/terminal/不同Task或Delivery保原错误事实，不用显式对象隐藏。只有无Task选择、同Task同generation无Delivery选择、匹配的已选对象，或原无context入口可继续目标对象检查。缺选择的对象视图仅为此次调用期评审事实，不写session，也不宣称session已current。

**D694-03：Markdown单写编排。** 修改canonical workflow的Explicit receiving-session continuation及Planning dispatch，使独立final_plan直接进入原Architecture Skill的对象entry；其余原步骤仍显式Identity/Ensure及必要Bind/Selection。Architecture Skill/contract独占该步骤内分支、读序、只读边界和失败owner；入口只路由、不复制步骤。普通执行恢复的runtime写入沿原Bind/Selection职责明确，不扩大到业务/规划/shared authority。

**D694-04：实际consumer核对。** 当前使用shared current的直接Planning consumers为Author、Wording、Approval、Activation和Architecture；前四者及Architecture candidate_assessment/非Planning stages保原选择语义。原Interface selected baseline_current aggregate为`public-output-baseline-current-index-5.0.schema.json`，直接projection到`consumers/workflow/current-5.0.schema.json`；selected Delivery planning分支由`public-output-delivery-baseline-current-1.0.schema.json`校验。current router按purpose将final_plan交相邻Approval，candidate交Author。实现测试组合实际invoke stdout及被选合同，不能只验证孤立schema。

取舍：拒绝全局把current(key)改为显式对象读取，它会改变未授权consumers；拒绝自动Bind/Selection wrapper，它仍写无consumer选择；拒绝新Skill/profile/大optional DTO、持久reviewer状态和第二选择writer。原Architecture包本地的小型差额有一个当前consumer，复用已有身份事实，职责和维护成本低于上述替代。

## 5. 接口与数据

不新增公共Skill id、profile、typed exit、schema字段、配置或Task/Delivery/session持久格式。现有`delivery_task_impact_sync` Planning input已带Task locator、完整DeliveryKey、公开planning_root、planning_purpose、design locator/design facts和freshness及authority。该原输入足以定位一次评审对象；不新增“授权/通过/调用者身份”字段。

| 生产者→消费者 | 本批行为与约束 |
| --- | --- |
| Wording-current caller→原Architecture final_plan | 完整既有input进入该Skill；先authority再对象/设计，缺选择不要求写选择。 |
| 原Architecture invoke→原current router | 原typed DTO、source_profile、key/root/purpose/freshness及所选分支字段保持；逐一核对当前引用链，发现引用缺项时在本批修正，保持原投影语义。 |
| current router final_plan成功→原Approval | 薄projection使用实际相邻stdout，Approval input的architecture_assessment/原合法current guard保持；不能以reviewer无选择入口给Approval放行。 |
| 非成功Architecture出口→原consumer | architecture_conflict/contract_incomplete回原Planning owner，sync_required回原维护/同purpose，fitness_regression回原纠正，blocked停止；不伪装成功。 |

公开输出不是session写入receipt；没有新缓存、绑定、资源记录或生命周期operation。普通执行恢复仍使用原session schema3与原writer。

## 6. 状态、顺序、正常与失败流程

本次评审不改变Task/Delivery阶段。原Planning仍为candidate_assessment→Author solution→Wording→final_plan→Approval→展示/接受→Activation。

final_plan步骤：fresh generic reviewer空任务历史→读constitution/baseline/change-contract→读真实current并核完整显式对象→读设计实际内容和consumers/必要源码→独立形成判断→读必要解释及真实贡献/必要ADR→构造owner result→原正式invoke→唯一typed consumer。

| 真实接收事实 | final_plan对象entry |
| --- | --- |
| resolver无context | 沿原显式对象校验，不改环境，不写session。 |
| no_current_task | 直接核显式对象的原Task/gen/C4/checkout/public关系及后续stage/scope/root/freshness，不调用Bind/Selection。 |
| no_current_delivery且TaskKey匹配 | 同上，调用期评审不写选择。 |
| current且完整key匹配 | 复用选择事实，仍核目标C4/checkout及原后续条件，不重写绑定。 |
| no_current_delivery但TaskKey不同，或current为其他key | 原选择/身份冲突，不覆盖。 |
| error、terminal或真实generation/checkout/profile/stage/scope/root/content冲突 | 原实际首失败及owner；普通错误不变成缺绑定或成功。 |

candidate_assessment与其他stage继续原接续，不通过此helper引入无选择执行。对象entry不能自行决定AI semantic pass；结构通过也可能产生原conflict/incomplete/regression/sync/blocked。

## 7. 恢复、兼容、迁移与集成

直接演进既有final_plan接入，现有合法带绑定与无context调用保持；没有第二版本reader、别名、双写或新compatibility layer。改变的是受限评审资格，不改变Task/Delivery身份、phase或Approval输入。原读序/错误consumer不退役。

普通执行会话恢复仍由原Identity/Ensure/Bind/Creation Selection执行必要runtime写入；一旦恢复，回原未完成义务，不重启已有Planning。一次性final_plan无此副作用或recovery checkpoint。调用错误沿原Skill新轮fresh re-entry，不手补owner/digest或转换失败结果。

新增`trellis/presets/guru-team/MIGRATION-694.md`描述同源workflow、Architecture package/runtime和受影响平台成套采用；现有安装继续原合同，成套采用后按同key/root/实际义务续接。无数据迁移，不能热patch已安装guard或改manifest/hash。source/dogfood同步沿原preset；若历史数据阻止plain apply，报告实际诊断并由原tools-only owner审清写集后恢复，保Task/Delivery/session与用户内容。此指导不是额外安装/矩阵要求。

## 8. 验证设计

| 验证 | 设计/验收 | 入口、输入、预期与证据限制 |
| --- | --- | --- |
| V694-01 | D01/02；DAC01/02 | 原Architecture package tests通过真实installed upstream public API形成新context缺绑定、同Task无选择、匹配绑定与无context；正式final_plan invoke成功且Task、session、planning、baseline和resource写集无新增。fixture语义输入只证明集成层，不冒充AI评审。 |
| V694-02 | D01/02；DAC02/03 | 原公共API产生其他选择、真实stage/scope/gen/root错配与原读取error边界，断言首失败/原owner及拒绝强度；不手改artifact制造攻击案例。其他目的和Author/Wording/Approval/Activation原回归保持。 |
| V694-03 | D04；DAC04 | 实际invoke stdout逐一进入Interface当前aggregate、final_plan分支、declared projection/current consumer与相邻Approval input；保key/root/purpose/design freshness及成功/非成功原consumer。不能只断言字符串或孤立schema。 |
| V694-04 | D03；DAC05 | 原workflow/skill contract与分发检查核路由、读序、普通恢复runtime写边界；独立Architecture/Check/Review实际读改动及未改consumers。静态parity不证明所有平台Agent行为。 |
| V694-05 | §7；DAC05 | 当前受影响canonical/dogfood/installed/声明平台、reapply/drift、可执行mode与递归sidecar定向检查，使用原安装/升级owner。无额外clean安装、专项回放、A-B、native eval、案例数/耗时或完整矩阵。 |

原候选Architecture/Check先审实现和完整隔离拟写，再由原owners final_integration/readback，重绑实际candidate并最终Check/commit/独立完整committed Review。没有部署/业务数据效果声明；各层未验证边界单列。

## 9. Canonical 引用、本轮差额与实际未决项

RDT原owner维护R679/D679/T679完整接收单元及必要关系：把独立final_plan对象entry与普通恢复分开，原条件存续。Architecture原owner维护实际命中的ARCH-DOM-019/043/045、CURRENT相关接收事实和change-contract的原规划职责。task-owned真实贡献为`docs/architecture/contributions/694-final-plan-object.md`，必要ADR候选为同名目录`adr-explicit-review-object.md`；拟目标ADR为`docs/architecture/adr/explicit-review-object.md`，只解释普遍接收前置的窄替代，不改其他owner。

shared current先保持B下内容；完整proposed单元由原owners在实施时生成，原独立candidate评审与Check后才final_integration。普通导航只在必要关系变化时写，不递增全局版本。该批具体职责和晋升见implement唯一Docs Plan。

当前没有产品范围未决。具体代码与边界需final_plan确认；正式实现、集成、分发、Check/Review及整体收尾仍未验证。若独立Architecture发现机制不足或source冲突，沿其真实出口回原owner，不以candidate pass覆盖。
