# D1：独立 final_plan 完整显式对象接入

## 1. 整体来源与术语

整体需求为 [Task PRD](../../prd.md)，公开 accepted_scope 为该文件的 `sha256:c8b6b2475e82802452387ac90810790971d1702b76471ef3c403dd62ee5abc53`。本批 scope_ref 选中 R694-01..07 和 AC694-01..05，覆盖全部 #694 要求。DeliveryKey 为 Task `694-architecture-final-plan-object` / generation `0` / UUID `0982ab15-61b8-41d3-9639-85049e61719e`；公开 planning_root 为 `deliveries/0982ab15-61b8-41d3-9639-85049e61719e`。

| 来源 | 章节、角色及本批用途 |
| --- | --- |
| [live #694](https://github.com/castbox/guru-trellis/issues/694) | 完整正文；七项行为为要求，来源/关联/非目标为约定兼容边界。 |
| `docs/requirements/current/task-delivery-lifecycle.md` R679、`docs/design/current/task-delivery-lifecycle.md` D531/D679、`docs/test/current/task-delivery-lifecycle.md` T679 | 当前行为、单writer与接收隔离；本批改变独立final_plan接入，保留其余路径。 |
| `docs/architecture/README.md`、constitution、change-contract | 架构authority、原则与原检查/晋升职责，限制本批机制及写入。 |

完整显式对象定位本次评审的 Task、generation、Delivery、planning_root 与设计；它不授予会话执行选择。final_plan 是 Wording-current 方案之后、相邻 Approval 之前的原 Architecture 目的。

## 2. 整体与本批目标、非目标

本批独立交付目标是让新的独立 reviewer 用完整对象通过原正式 final_plan 评审，而无需为一次性评审持久绑定/选择。对象的当前 C4/checkout、公开关系、scope/stage/root 和设计 freshness 必须保留；实际 stdout 与相邻consumer仍正确。

本批与整体均只处理 #694。保留 Author、Wording、Approval、Activation、实施及其他 Architecture stage 的原绑定/选择；普通恢复仍由原 owner 写其必要runtime。不修后端#961、不碰其会话、不部署或写业务数据；不开始#693/#692、不重做#695；不新增通用框架/审批链/台账、跨Skill digest authority、release/tag或额外Issue；不恢复专项回放/A-B/native eval/固定案例数/耗时统计、额外安装或完整矩阵，不扩攻击、并发或crash场景。

## 3. 本批起点、前序结果、依赖与剩余责任

本Task尚无前序Delivery。本批从 `2dbaf308e6d5137bf640cfe546a078497c1c713a` 开始，交付目标main；D1是全量pull_request切片，当前phase为planning，尚无Planning/Check/Review结果。#695 PR699/700已经合并，是当前基线事实，非本Task前序切片，也不新增依赖gate。

现有共享 `current(key)` 仅无context按显式key投影；有context读取本会话。现有Architecture planning guard要求Task和Delivery选择，原恢复能力有效。需要在这个兼容起点承接窄入口及派发差额，不用全局fallback改变其他consumer。

本批合并后没有预定后续实现切片，但整体Completion仍审全部R01..07与AC01..05，再由Closure、Finish和Cleanup原owner完成收尾。源码变更、安装投影或单元通过不等于整体完成。

## 4. 本批调用方、场景与流程

| 场景 | 前置与触发 | 必须观察的行为 |
| --- | --- | --- |
| DS01 | fresh generic reviewer有真实context、无Task/Delivery选择，收到完整对象并进入独立final_plan | 核完整对象后正式评审；不产生持久绑定/选择，不改规划、生命周期、baseline或资源。 |
| DS02 | 同对象已有合法绑定，或resolver确认无context；进入既有合法入口 | 合法事实可复用；无context显式入口继续可用，不删改环境或借主会话身份。 |
| DS03 | 其他合法选择、损坏绑定、错generation/C4/checkout/profile、终态/非planning、scope/root/design freshness错配 | 报实际首失败并回原owner，不覆盖选择，不改报成功，不用文件存在冒充关系有效。 |
| DS04 | 独立评审返回typed stdout，主执行会话已有自己的合法选择 | 只有原允许的成功结果进入Approval，其余走原consumer；key/root/purpose/freshness一致，Approval不获得无绑定入口。 |
| DS05 | 普通执行会话需要恢复绑定/选择 | 原Identity/Ensure/Bind/Selection恢复同对象，在原职责明确runtime写入；此路径不成为DS01前置或阶段pass。 |

## 5. 完整行为、条件与约束

- **DR01（R694-01/DS01）**：完整显式对象是独立final_plan校验和评审的直接输入。评审者不再独立拼装Identity/Ensure/Bind/Selection取得资格，也不先写无后续consumer的执行选择；wrapper形式不能替代这一行为。
- **DR02（R694-02/DS01/03）**：保留TaskId/generation、C4分支、唯一注册checkout、Task/Delivery公开关系、适用profile、非终态且planning、accepted_scope/scope_ref关系、planning_root和实际设计内容freshness的完整校验。失败定位真实条件并回原owner，不能因提供key或文件存在放行。
- **DR03（R694-03/DS02/03）**：本次对象不成为会话执行选择。同对象合法绑定可复用；其他选择、损坏绑定或真实身份/阶段冲突保原处理，不覆盖、不借主会话身份。保无context原显式入口，禁止通过环境修改制造该状态。
- **DR04（R694-04/DS02/05）**：接入只对独立final_plan生效。共享substrate实际consumers须盘点；普通Author/Wording/Approval/Activation/实施及其他Architecture stage保原语义。公共I/O如变，必须最小且明确兼容/迁移，不能新增大optional总入口。唯一来源设计处置将在design第3节维护。
- **DR05（R694-05/DS01/05）**：一次性评审不改业务代码、规划、共享baseline、生命周期、session选择及资源。正式invoke仍返回原typed result。原执行恢复保原owner及必要runtime写范围，不能搬回DS01作前置。
- **DR06（R694-06/DS01/04）**：fresh generic reviewer空任务历史；先constitution/baseline/change-contract，再核对象、读设计事实/实际consumers/必要源码，最后解释性归属。不加载PRD、验收叙事、实现总结或前序pass；AI自行形成impact/出口。实际stdout保同key/root/purpose/design freshness与声明consumer。只将原可进入Approval的成功出口交其原合法选择consumer；architecture_conflict、sync_required、contract_incomplete、fitness_regression及阻塞保原路由。
- **DR07（R694-07/全场景）**：维护实际命中的RDT/Architecture完整authority、canonical Skill/workflow/派发，同步dogfood和受影响平台。实现前核最新合同；Markdown拥有语义判断，脚本仅校验客观事实。不改上游Trellis、全局npm或node_modules。沿现行Check、独立完整Branch Review、PR readiness及升级流程。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 验证输入与预期结果 |
| --- | --- | --- |
| DAC01 | DR01/02/05；DS01 | 从原正式final_plan给完整当前对象，未选择接收者可执行校验/评审并返回真实typed stdout，所列状态无写入。 |
| DAC02 | DR02/03；DS02/03 | 沿原公共API形成合法选择、无context和普通失配，成功兼容、首失败/原owner、非覆盖与保拒绝强度均正确。 |
| DAC03 | DR04/05；DS02/05 | 原共享consumer回归保持；普通恢复仍使用原writer和明确runtime写入，不扩新入口。 |
| DAC04 | DR06；DS01/04 | 原独立派发按指定顺序执行并自行形成结果；实际aggregate output、所选分支、薄projection与相邻Approval input组合正确，非成功路由保持。 |
| DAC05 | DR07；全场景 | 当前受影响package/runtime、canonical/dogfood/installed/声明平台、reapply/drift、sidecar/mode定向检查及完整Check/独立committed Review。分层报告实际证据，不预填安装或行为通过。 |

当前没有产品未决项。具体接口表示与机制取舍由Author/Architecture完成；真实authority冲突回原owner。实现、运行和质量gate均尚未验证。本批不另造专项验收协议或额外矩阵。

## 7. Canonical 引用与本轮差额

R679/D679/T679的完整接收单元是本轮窄修订对象：独立final_plan去掉无consumer持久选择，其余接收路径保留。Architecture `01-current/system.md`、`03-domains/ownership.md`、`06-governance/change-contract.md` 中相关对象/owner/规划职责按真实设计差额由原owner承接，不先改shared current。

canonical Architecture package的Skill/contract/invoke/Interface聚合与分支schema、shared DeliveryProjection和workflow的实际consumer是实现/兼容依据。任何命中源码、安装或指导差额须在同一切片保持一致；同内容分发不证明真实Agent行为。具体设计、Docs策略与验证安排在独立candidate_assessment后写入本批design/implement。
