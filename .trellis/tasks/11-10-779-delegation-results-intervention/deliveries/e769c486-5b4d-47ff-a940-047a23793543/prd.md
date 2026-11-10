# #779 D1 委托结果承接与介入方法

## 1. 整体来源与术语

TaskId 为 `779-delegation-results-intervention`，generation 为 `0`；本批 DeliveryId 为 `e769c486-5b4d-47ff-a940-047a23793543`，profile 为 `pull_request`，公共 phase 为 `planning`。公共 scope_ref 选择 [整体 PRD](../../prd.md) 的 R779-01..06，authority revision 为 `sha256:4136971246785e9c3c1dea9b536cb6c23a55af54024012ef169aa5e74c328884`。planning_root 为公共创建返回的 `deliveries/e769c486-5b4d-47ff-a940-047a23793543`。

| 来源 | 角色与用途 |
| --- | --- |
| [#779](https://github.com/castbox/guru-trellis/issues/779) 完整正文 | Direct Source；六项修复要求、范围及最小验收为当前要求；事故调查是历史证据 |
| [整体 PRD](../../prd.md) 第1至8节 | 已接受整体范围；本批覆盖全部行为，保留所有条件与非目标 |
| `trellis/presets/guru-team/spec/workflow/workflow-contract.md` Phase 2 | 现有派工/终态事实承接约束及本轮候选落点 |
| `trellis/workflows/guru-team/workflow.md` Phase 2 | 现有主协调者、计划外候选与正式审查路由 |
| [#734](https://github.com/castbox/guru-trellis/issues/734) R3/R4 | 关联背景；不作为前置、预算或设备验收来源 |

执行者、主协调者和执行事实沿整体 PRD 第1节定义。命令终态指该命令真实结束状态，不由日志片段或页面 PASS 推断；工作包完成仍须满足原工作包要求。

## 2. 整体与本批目标、非目标

当前已有唯一执行者和终态承接原则，但仍缺委托后的协作方法。D1 的独立交付目标是把自主执行、介入条件、冲突写入交接和结果适用性统一放入原派工合同，并同步实际受影响投影。本批覆盖整体 R779-01..06 与 AC779-01/02，不拆出后继能力。

保留整体 PRD 第3节的全部非目标：不承接消息/批次预算、规模阈值、设备矩阵或事故重放；不新增 Skill/步骤、DTO/状态、台账、持久 handoff、授权记录、强制汇报表、额度、锁或调度平台；不强制换代理重派，不 patch 上游或业务工具，不自动修改或关闭 #734，不承诺节省比例。

## 3. 本批起点、前序结果、依赖与剩余责任

本批是首次 Delivery，没有前序交付事实。开发起点为 `221f74caef372414a1c7d700575742eb1e075af4`，在当前专属工作树的 `codex/779-delegation-results-intervention` 分支执行；PR 目标为 main，开发基线与实际 PR 集成目标分开。

现有 canonical Phase 2 已要求采用 worker 终态和 live facts、不建 implementation handoff artifact。全局 workflow 已保留主协调者对计划外候选的判断。拟补差额不会改变公共生命周期或这些语义职责。

依赖是当前匹配的 workflow/preset、原安装或 tools-upgrade owner 和受管同步检查。规则不依赖 #734 或设备能力。完整切片交付后，Task 仍须由原 Completion 判断整体六项要求和全部必要证据；本节点在 PR 发布后停下，不把 PR 或单个 gate 视为 Task 已完成。当前未分配责任为空，实际未完成项仍包括方案、实现、同步、检查、独立审核和发布。

## 4. 本批调用方、场景与流程

| 场景 | 起点与触发 | 本批期望行为与观察 |
| --- | --- | --- |
| SC779-01 正常推进 | 工作包已委托，执行者可自行继续 | 执行者完成原命令等待、环境诊断、断言、产物与终态；主会话做独立工作或按平台能力有界等待，不默认同日志双重跟踪或连续补发过程指令 |
| SC779-02 介入/接管 | 具体阻塞需原 owner 决策、范围/机制变化、冲突写入、用户停止或执行者无法继续 | 先核当前运行与缺口，再采取原职责内动作；接管沿可用原句柄继续，未知终态明确为未知 |
| SC779-03 写入窗口 | 主会话拟写内容与执行者当前工作冲突 | 请求自然边界暂停→执行者确认当前终态且不启动下一轮→主会话写入→通知恢复；无冲突工作继续并行，无写入需求不逐轮审批 |
| SC779-04 承接/交叠 | 收到终态汇报，或发现已交叠写入 | 核要求和适用性，区分日志、页面、命令、产物、工作包层次；交叠披露失效证据并补实际必要验证，正式 Check/Review 继续由原 owner 判断 |

## 5. 完整行为、条件与约束

- **R779-01 / SC779-01**：执行者自主完成已委托工作包内的命令等待、常规环境诊断、原断言、产物取回及终态汇总。计划外范围、机制或风险变化仍按现有 discovery 合同返回主协调者，不借自主执行扩大范围。
- **R779-02 / SC779-01/04**：正常推进时主会话不默认并行跟踪同一日志并连续下发 poll、继续或下一步指令。主会话可做互不影响的工作或按平台能力有界等待。日志片段、页面 PASS、命令终态、产物通过和工作包完成分别判断。
- **R779-03 / SC779-02**：仅针对真实原 owner 决策阻塞、范围/机制变化、冲突写入、用户停止或执行者确实无法继续而介入。先核本次实际运行和具体缺口，再处理；猜测不直接成为重启、重建或修改要求。必要进度查询、证据读取和主会话 adb 使用继续允许。
- **R779-04 / SC779-02/04**：执行者在当前对话提供最少的完成内容、实际终态、结果位置及未完成项。诊断先核本次进程/日志/产物对应关系，未知终态如实说明。接管先查现有工作、沿可用原句柄继续，不默认重启；正常协作不要求逐命令上报 PID、句柄或 hash。
- **R779-05 / SC779-03/04**：冲突写入按场景中的自然边界顺序交接。执行者确认终态且暂不启动下一轮前，主会话不进入冲突写入。无冲突路径继续并行，无写入需求继续原委托。已交叠则按实际影响披露失效证据并补必要验证，不一律重跑。
- **R779-06 / SC779-04**：主协调者仍核结果是否满足当前要求、识别新缺陷并交原 owner；正式 Check/独立 Review 保持职责。可验证执行事实经适用性判断后采用，只有具体缺口或不一致才补查/重跑。新增要求作为明确差额，不用零碎消息改变隐含完成条件。

来源约定设计的唯一逐项处置由本批 `design.md` 第3节维护；本 PRD 不另建处置矩阵。规则优先归 canonical workflow-contract Phase 2，全局 workflow 仅必要引用；不把主协调者虚构成独立 implementation Skill。受管副本通过原安装/升级 owner 同步并保留 Task/session，不手工覆盖。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 入口、输入与预期观察 |
| --- | --- | --- |
| AC779-01 | R779-01..06 / SC779-01..04 | 原 Check 与独立 Review 读取修订后的完整派工段、实际引用及计划外处理/正式审核关系。判断自主执行、介入、事实层次、接管、交接及结果采用条件均完整，没有逐轮审批、持久运行状态或隐含完成条件 |
| AC779-02 | 全部要求/场景 | 原安装或 tools-upgrade owner 对当前 Task checkout 同步实际受影响 canonical/dogfood/声明平台投影，并执行必要 drift/mode/sidecar 检查；真实结果与保留的 Task/session 可核，不把源码检查扩大为全平台实际 Agent 或业务采用 |

验证选择遵循 `.trellis/spec/workflow/quality-guidelines.md#test-and-validation-value`。本批不新增仅冻结文字的测试，不强制设备、Agent 评测框架、事故重放或消息计数测试，不执行完整多平台安装/升级/Release 矩阵。实际节省效果未验证。没有必要产品问题；具体方案、安装写集与命中命令由原 Author/Architecture 展开，完整方案前不进入实施。

## 7. Canonical 引用与本轮差额

| Authority | 本批用途与差额 |
| --- | --- |
| `docs/requirements/current/task-delivery-lifecycle.md` 固定内容范围、实施与返工；候选适用性 | 保留原实施与事实采用责任；本轮补委托后协作方法，不改生命周期 |
| `docs/design/current/task-delivery-lifecycle.md` Authority/调用责任、最终 Check/Review、候选适用性职责 | 保留 Markdown/AI 与 runtime 的边界及正式 owner；精确方法继续由 canonical workflow-contract 单写 |
| `docs/test/current/task-delivery-lifecycle.md` 策略与完整性、候选适用性场景 | 采用分层证据边界；本轮只增加真实方法差额所需语义和同步验证，不复制历史矩阵 |
| `docs/architecture/README.md` scope/status 与维护关系 | Architecture 原 owner 独立判断实际候选影响；当前 PRD 不预判无影响或晋升通过 |
| `trellis/presets/guru-team/spec/workflow/workflow-contract.md` Phase 2；`trellis/workflows/guru-team/workflow.md` 2.1 | 本轮候选是现有控制面方法修订和必要引用；实际方案待独立 candidate_assessment 后写入 |

RDT/Architecture 的具体更新必要性与目标由原维护 owner 判断；Planning 不直接写共享 authority 或登记全局导航。
