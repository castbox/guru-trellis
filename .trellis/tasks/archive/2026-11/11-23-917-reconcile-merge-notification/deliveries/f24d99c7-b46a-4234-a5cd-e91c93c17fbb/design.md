# D1 合并通知的 Reconcile 路由设计

## 1. 设计目标、需求承接与内容基线

本方案交付本批 [PRD](prd.md) 的 S1、S2、S3 及 AC1、AC2、AC3。D1 覆盖 [Task 的整体需求](../../prd.md)。开发基线 B 取 Intake 选定的 main@8604558695dfd9d8ea2181406a87ece70d9eea63。Planning H0 为同一提交。实施候选由原 owner 按固定 B 与实际 HEAD 构造。PR 目标是 castbox/guru-trellis 的 origin/main，实时目标不改写 B。

适用架构为 guru-trellis-architecture、guru-trellis-design-constitution-v1 和 guru-trellis-architecture-change-contract-v1。独立候选审核认定本次在原 owner 内落实 ADR-028，结果为 baseline_current / no_architecture_impact。

## 2. 当前系统、边界与目标差额

共享编排正文供 DAG 和 Sequence 调用。Minimal Child Prompt 要求子会话整合当前选定基底。Fresh Merge Gate And Integration 在同仓其他 PR 合并后再次要求整合。当前仓库 workflow 已限制实际触发条件，但通知的在途接收与工作接回入口没有直接引用该条件。本批替换两条无条件指令，并在接收点承接当前 owner 的判断。D1 尚无前序结果。

## 3. 来源设计处置

| 来源与承诺 | 处置与本方案落点 | 理由与影响 |
| --- | --- | --- |
| #567 第 7–9 条：在途候选和仍适用证据保持稳定，内容审核与实际合并资格分别核对 | retain → §4 接收、§6 第 3 步 | 同步观察不改变既有审核对象。 |
| #567 第 10–12 条：五类实际触发，原 Merge 确认服务端要求，不加规则查询 | retain → §6 第 4 步 | 继续由各原阶段获取本阶段适用的事实。 |
| #567 第 13–15 条：仅固定一次目标，范围内处理和原恢复 | retain → §5 原 Reconcile 输入，§7 恢复 | 原 Reconcile 消费固定目标。后继工作保持原阶段和审批边界。 |
| #567 第 18、20 条：受控 consumer 同步、Markdown 判断与脚本执行分层 | retain → §4 投影职责，§8 验证设计 | 原安装机制分发同一合同，测试只供事实和动作轨迹。 |

承诺均在现行范围内承接。无需上游重新选择条件。

## 4. 模块、职责与设计取舍

- **协调派发**由 trellis/presets/guru-team/spec/workflow/issue-orchestration.md 负责。在派发正文保留用户给出的同步条件原文，以及已核对的仓库、目标、通知和实际阻塞事实。创建、发送、继续等待及合并资格仍由原协调合同处理。对同仓后继节点，保留单一集成负责人及结果回读，依据实际影响安排下一动作。
- **原阶段接收**由 trellis/workflows/guru-team/workflow.md 负责。在途处理和接回入口定位当前 Task、Delivery、阶段和固定候选，并引用唯一 Fixed content and actual integration 规则。收到通知后，由原阶段负责人核查适用事实，保留仍适用结果并完成原步骤，或者进入原 Reconcile。
- **受管投影**沿原工具更新入口将两份 canonical 正文投影到 dogfood 和适用安装。DAG、Sequence 通过现有引用读取共享正文。已有明确入口只做定位，触发定义保留在原 workflow。

直接替换既有指令可同时覆盖派发和接收。仅修改 Reconcile 无法修正派发输入，且会推迟原本应由阶段负责人作出的判断。独立 watcher 或脚本判断会复制当前事实判定并增加额外查询。采用两个原入口的局部修订。

## 5. 接口与数据

| 生产方 | 已有输入或输出 | 消费方 |
| --- | --- | --- |
| 用户、通知和事实读取 | 现有自然语言同步条件，已核对的目标提交、通知和实际阻塞事实 | 协调派发。原样保留同步条件的限制语。 |
| 协调派发或直接通知 | 当前工作和原条件，已核对事实 | 原阶段负责人按既有入口校验当前事实。 |
| 原阶段负责人 | 具体触发依据，适用的原 Reconcile profile，固定目标 OID | guru-reconcile-task-base。按原 profile 向 selected_base_ref 或该 profile 对应的精确新基底输入传递实际目标。 |

继续使用现有 Task/Delivery identity、候选和证据。产品 schema、字段、持久状态和公开出口沿用现有合同。

## 6. 状态、顺序、正常与失败流程

1. 协调会话收到 sibling merge 通知时核实所属仓库、目标和实际合并结果。如果要派发后续执行，将已核对的事实和原条件交给该节点当前阶段。关注合并与「必要时同步」按原条件执行。
2. 执行会话直接收到通知，或接回包含通知的未完工作时，按原阶段入口核对同一 Task、Delivery、阶段、候选和适用证据。通知进入当前原步骤。已有合并事实可以用于核对，缺失事实留给原入口处理。
3. 如果只观察到通知、目标 SHA 前进、behind 或同文件路径重叠，继续原步骤并使用仍适用的证据。无需运行额外集成检查、轮询或候选同步。原阶段可继续完成其必要的证据核查。
4. 如果出现实际 Git 冲突、必需检查发现具体集成失败、原 Merge 确认既有服务端分支更新要求、明确需要纳入依赖或需求，或用户明确请求同步，原阶段负责人指出依据，选择一次目标提交，并调用原 Reconcile。
5. 原入口遇到真实身份、状态或事实缺口时，按原 owner 的恢复或停点处置。适用证据的变化由原阶段负责人处理。冲突验收停在真实调用，后继冲突处置与交付不在此场景的观察范围。

## 7. 恢复、兼容、迁移与集成

在途会话从原阶段适用合同接续，先核自身绑定和实际阶段。协调者的转述不提供绑定、授权或审核结果。结果丢失依旧交原操作恢复。当前安装通过同源成套 workflow/preset 更新采用该变化，保留 Task/session 和用户本地修改，冲突 sidecar 沿安装 owner 处置。历史契约通过固定已有 provider 读取。无需公共 DTO 迁移或第二套 consumer。

## 8. 验证设计

| 验证 | 真实入口与输入 | 观察 |
| --- | --- | --- |
| V1 / AC1 | 原 DAG 协调入口。使用临时仓库中目标正常推进的真实 Git 事实和条件式通知，由隔离 native Agent 执行。 | 记录实际派发输入。保留原条件和核对事实，派发继续原阶段且没有追赶请求。 |
| V2 / AC2 | 实际执行会话在审核途中接收同类通知。隔离目标与候选修改同一路径的不同位置。 | 核起点、候选、适用证据及实际继续动作。读取完整所用工具轨迹，确认没有调用 Reconcile。 |
| V3 / AC3 | 使用同一固定候选与正常提交造成的真实 Git 冲突，保持执行会话当前阶段入口。 | 保存具体冲突、一次固定目标、原 Reconcile Step 的首次命令和原始结果。到此停止。 |
| V4 / 投影 | 受管 workflow/preset 的受影响源码、dogfood、声明的安装入口与重应用。 | 核受管字节、适用加载、权限和 sidecar，记录定向覆盖。 |

V1–V3 使用真实 Agent 选择动作。隔离工具记录 Git 原始事实、派发和命令结果，不输出预设路线。验证独立区分计划、实际工具动作与现场效果。当前证据门槛是临时仓库的实际运行。

## 9. Canonical 引用、本轮差额与实际未决项

RDT 归 [需求当前单元](../../../../../docs/requirements/current/issue-orchestration.md)、[设计当前单元](../../../../../docs/design/current/issue-orchestration.md) 和 [测试当前单元](../../../../../docs/test/current/issue-orchestration.md)。仅纳入本次通知入口的完整行为差额和定向验证方法。既有 #567 的定义及历史事实继续由其原来源维护。Architecture 采用既有 [ADR-028](../../../../../docs/architecture/adr/028-fixed-content-baseline.md)。候选审核认为无新增架构决定，本方案没有 Architecture contribution 或 ADR 候选。当前没有需协调选择的需求。
