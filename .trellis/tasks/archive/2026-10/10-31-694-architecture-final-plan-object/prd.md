# 独立 Architecture final_plan 显式对象接入整体需求

## 1. 来源与术语

| 来源 | 章节、角色与用途 |
| --- | --- |
| [Direct Source #694](https://github.com/castbox/guru-trellis/issues/694) | 完整正文；目标与行为要求为需求，来源、关联与非目标为兼容和范围约束。2026-10-31 读取，Issue OPEN，无评论。 |
| `docs/requirements/current/task-delivery-lifecycle.md` R679 | 现有接收者行为 authority；本项只窄演进独立 final_plan 接入。 |
| `docs/design/current/task-delivery-lifecycle.md` D531/D679 | 当前对象、会话选择和原 owner 的职责边界。 |
| `docs/test/current/task-delivery-lifecycle.md` T679 | 现有回归边界；本项沿原验证流程更新受影响预期。 |
| `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md` | 当前 Architecture、五原则及原检查/晋升职责。 |

“显式对象”是本次评审目标的 Task locator、TaskId/generation、DeliveryKey、planning_root 与设计 locator；它不等于会话执行选择。`final_plan` 指原 Architecture `delivery_task_impact_sync / planning` 的最终规划评审目的。Task 承担全部需求；Delivery 承担所选交付范围。

## 2. 背景与问题

来源记录的后端 #961 是历史诊断案例：准确对象已传给独立接收会话，但初始查询为 no_current_task。原 Identity/Ensure/Bind 和 Delivery Selection 能恢复同对象，故不是 Task 丢失或会话隔离失效。

当前 `trellis/workflows/guru-team/workflow.md` 的 Explicit receiving-session continuation 与 Architecture invoke guard 要求有 context 的接收者先补 Task 绑定和 Delivery 选择。`DeliveryProjection.current(key)` 仅在无 context 时按明确对象读取；有 context 时保留实际会话事实。一次性评审因而必须写没有后续执行 consumer 的选择；派发同时要求“不写文件”和“恢复绑定”也会产生冲突。

## 3. 目标与非目标

目标是让收到完整对象、尚未建立 Task/Delivery 选择的新独立会话，直接完成对象校验和正式 final_plan 评审，不为此次评审创建持久 session 绑定或选择。保留原身份、校验、独立性、typed result 和错误 consumer。

仅改变该 final_plan 接入与对应派发。普通 Author、Wording、Approval、Activation、实施和其他 Architecture stage 保留原绑定/选择语义。普通执行会话的缺绑定恢复仍由原 owner 执行。

不处理后端 #961，不改变其会话，不部署或写业务数据；不开始 #693/#692，不重做 #695 JSON 读取器；不新增通用派发框架、审批阶段、reviewer 台账、跨 Skill digest authority、release/tag 或额外 Issue。不恢复专项回放、A/B、native eval、固定案例数、耗时统计、额外安装或完整多平台矩阵。不增加攻击模型、并发压力或 crash 矩阵。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置条件与触发 | 行为及可观察结果 |
| --- | --- | --- |
| S694-01 | fresh generic reviewer 具有真实 context，收到完整当前对象，尚无 Task/Delivery 选择；调用独立 final_plan | 校验对象后正式评审，返回原 typed result；评审前后不产生绑定、选择、生命周期或资源写入。 |
| S694-02 | 同对象已有合法绑定/选择，或原 resolver 确认无 context；调用现有合法 final_plan | 复用合法事实，保留原显式入口；不通过改环境制造无 context。 |
| S694-03 | 已有其他合法选择、损坏绑定，或身份、checkout、scope、阶段、root、内容 freshness 真实冲突 | 指出实际首失败条件并交原 owner，不覆盖选择、不借主会话身份、不重开终态。 |
| S694-04 | final_plan 完成；主执行会话持有自己的合法 Task/Delivery 选择 | 仅原合同可进入 Approval 的成功出口进入该 consumer；其余出口按各自原 consumer 处理。Approval 不取得无绑定入口。 |
| S694-05 | 普通执行会话确实缺失绑定，沿原接续入口恢复 | 原 Bind/Selection owner 在明确 runtime 写入边界内恢复；恢复不是评审通过，也不是一次性评审的前置。 |

## 5. 行为要求

- **R694-01 → S694-01**：完整显式对象必须足以进入一次性独立 final_plan 的对象校验及正式评审。评审者无需独立调用 Identity/Ensure/Bind/Selection 取得执行资格。不得只封装原多步后仍先写无 consumer 的执行选择。
- **R694-02 → S694-01/03**：校验覆盖 TaskId/generation、当前 C4 分支关系、唯一注册 checkout、Task/Delivery 公开关系、适用 profile、非终态和 planning 阶段、accepted scope 与 scope_ref 的关系、planning_root 和设计实际内容 freshness。不得用 key 或文件存在替代校验；真实失败回原 owner。
- **R694-03 → S694-02/03**：对象不自动成为会话选择。同对象合法绑定可复用；其他合法选择、损坏绑定和真实身份/阶段冲突保留原处理。无 context 的既有合法入口继续可用；不得删改环境变量或借用主会话身份。
- **R694-04 → S694-01/02/05**：首次交付仅改变独立 final_plan 与对应派发。复用 substrate 时盘点实际 consumers，保持其他 Planning/实施/Architecture stage 的绑定和选择语义。公共 I/O 如需变化，采用最小明确合同，保合法调用或明确迁移；不新增大量 optional 字段的总入口。
- **R694-05 → S694-01/05**：一次性评审不改业务代码、规划、共享 Architecture Baseline、Task/Delivery 生命周期、session 选择或资源记录；正式 invoke 仍返回原 typed result。普通恢复保原 owner，并在原职责内明确 runtime 写入范围，不将其例外搬回一次性评审。
- **R694-06 → S694-01/04**：fresh generic reviewer 使用空任务历史。依次读取 constitution、baseline、change contract，核对象，再读设计事实、实际 consumers 和必要源码，最后读解释性归属；不加载 PRD、验收叙事、实施总结或前序 pass。AI 自行形成 impact 与出口。实际 stdout 保同一 DeliveryKey/planning_root、purpose、design freshness 和声明 consumer；不得预填或改报成功。仅原可进入相邻 Approval 的成功出口交给 Approval，接收者仍按自己的合法选择承接。architecture_conflict、sync_required、contract_incomplete、fitness_regression 和阻塞结果保原 consumer。
- **R694-07 → 全场景**：依实际差额维护原 Architecture/RDT authority、canonical Skill、workflow 和派发指导，同步 dogfood 和受影响声明平台。实现前核当时最新合同。沿原开发、Check、独立 Branch Review、PR readiness 和升级流程，验证声明限于实际证据。

## 6. 约束与依赖

当前开发基线及交付目标为 main，起点 `2dbaf308e6d5137bf640cfe546a078497c1c713a`。本 Task 保持唯一 TaskId、generation 和既有会话隔离，不修改上游 Trellis、全局 npm 或 node_modules。Markdown 拥有流程和语义判断；脚本只校验客观对象事实并执行明确动作。

来源指定的 canonical Architecture package、`runtime/invoke.py`、shared `delivery_projection/adapter.py` 与 workflow 是兼容起点。必须核对实际 Interface 聚合 output、所选 final_plan 分支和相邻 Approval input；只改独立 schema 不足。具体接入表示与兼容方案由 Author/独立 Architecture owner 确定，不是待决产品选择。

#695 的输入载体能力已交付，按现有接口复用；串行安排不新增功能依赖 gate。#693 拥有后续合同承接方法，#692 拥有 Intake 效率和诊断；不将这些责任并入本项。没有服务、数据库或业务数据迁移需求。

## 7. 可观察验收与验证方式

| 验收 | 对应要求/场景 | 入口、输入与预期结果 |
| --- | --- | --- |
| AC694-01 | R01/02/05；S01 | 在原正式 Architecture final_plan 入口使用完整当前对象和未绑定接收会话；完成校验、语义评审与实际 stdout，保持对象身份且无所列写入。 |
| AC694-02 | R02/03；S02/03 | 通过原 API 形成合法同对象/其他选择、无 context 和普通 stale/mismatch；合法入口保持，真实冲突保原 owner 与首失败，不覆盖身份或弱化校验。 |
| AC694-03 | R04；S02/05 | 原共享 consumers 和其他 Planning/Architecture stage 的适用回归保持；普通恢复仍由原 writer 执行并明确 runtime 边界。 |
| AC694-04 | R06；S01/04 | 独立 reviewer 按原入口和读取顺序自行形成结果；核实际 public output→声明 projection→相邻 Approval input，成功/非成功路由、key/root/purpose/freshness 均正确。 |
| AC694-05 | R07；全场景 | 受影响原 package/runtime、canonical/dogfood/installed/声明平台、reapply/drift、sidecar/mode 的现行定向验证与完整 Check/独立 committed Review 通过。源码、集成和实际行为证据分别报告；不将本项扩为专门安装/Release矩阵。 |

上述是验收定义，当前尚未实施或验证通过。依原 Task 全范围完成责任，Delivery 合并后仍须 Completion、Closure、Finish 和明确资源处置；局部 gate 不能替代整体完成。

## 8. 实际未决项

没有待决产品范围选择。接入的具体 public 表示、最小只读校验复用和兼容迁移由 D1 Author/Architecture 确定；若出现真实 authority 冲突，回原 owner。实现与运行、Check、独立 Review 和安装投影证据尚待后续原流程形成。
