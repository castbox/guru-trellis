# D1 协调责任与主动解阻设计

## 1. 设计目标、需求承接与内容基线

本批承接 PRD R1..R9、S1..S6、AC1..AC9。开发和内容基线 B=1d32c9c8044ed12fce54ab991545ab0cfde0993c，来源为本轮 main 固定 Git 对象；Planning H0 同 B，PR 目标 main，最终实现 H 另由原 candidate owner 建立。独立 Architecture candidate_assessment 实际返回 baseline_current/no_architecture_impact：沿既有职责，不新增 authority、状态或脚本决策器，无 contribution/ADR。当前 authority 为 docs/architecture/README.md、00-foundation/design-constitution.md、06-governance/change-contract.md。final_plan 尚待完整方案和 Wording 后执行。

## 2. 当前系统、边界与目标差额

现有共享 issue-orchestration.md 定义终点、授权、原生子会话、心跳、进度、合并及完成证明。DAG contract 拥有依赖、slot、failure policy；chain contract 拥有严格串行。两 Skill 均显式加载共享方法，Codex-only 且 instruction-only。

本批直接修改共享判断：将整体完成责任、障碍调查与结果追踪、外部等待有效性、真正无路的终局阻塞连成闭环。原 progress 表和恢复/settlement 改为该方法的具体消费，不另建一套审批步骤。无前序 Delivery。

## 3. 来源设计处置（唯一）

| 来源承诺 | 处置和落点 | 理由与影响 |
| --- | --- | --- |
| Issue #731 修改范围：优先共享方法 | retain，第4/6节共享判断；两 Skill 只定位和调用 | 单一职责来源，避免副本分叉 |
| 两 canonical Skill、DAG/chain、心跳和必要案例同步 | retain，第4/8节具体消费及验证 | public 路由不变，旧案例改为补充当前闭环 |
| 原调度、身份/资源、单集成 owner、gate/确认/出口 | retain，第5/7节 | 原 contract 为调度 authority，不用新语义覆盖边界 |
| Markdown/AI 判断，工具只提供确定性事实 | retain，第4/8节 | 无生产调度脚本、机械分类器或持久协调台账 |
| 原安装 owner 同步、定向 reapply/drift | retain，第7/8节 | 不手工覆盖受管投影，不接完整发布矩阵 |
| 真实 Agent 隔离正常入口，不预填下一步 | retain，第8节 | 事实 provider 与评估答案分离，静态验证不替行为 |

无 change/reject，未偏离上游承诺。PRD 与 implement 只引用本节。

## 4. 模块、职责与设计取舍

共享方法增加“整体责任与主动解阻”正文，整合原 Progress Decision 与 Supported Workflow Recovery；定义有依据调查、讨论、质疑、原 owner 修正及跟进结果。终点、授权、merge proof 等既有规则仍由原段落拥有，使用引用衔接。

两 Skill 的观察步骤明确消费该闭环；DAG failure/settlement 说明局部受影响范围，Sequence 说明步骤失败不释放当前位置。共享心跳强调实际外部条件及剩余工作，静默仅控制通知。必要 examples/forward cases 增补多轮输入与 host-only 审核观察，避免把教学案例当行为证据。

直接修改优于新增协调 Skill、脚本、台账或固定问答链：这些替代会重复现有 owner，增加维护成本且不能替代 AI 判断。新测试代码只作隔离事实载体，不装入公开 package。

## 5. 接口与数据

沿用显式 Skill 的原 conversation input → same-provider 方法/本地调度合同 → 原 typed exit/consumer。无新增 public 字段、schema、exit、持久存储或平台授权记录。临时 test provider 的资源是合成场景事实；不影响生产 app。

观察可保留目标、剩余义务、责任方/等待对象/复查条件的会话上下文，不形成新规范化 DTO、ledger 或 digest。子会话输入保持最小工作段，不复制用户授权过程。

## 6. 状态、顺序、正常与失败流程

每轮先核原人类终点与最新真实事实，再判断未完成义务。顺利工作继续轻量观察。遇 blocked/失败/无建议/不足完成声明时，区分本步失败、节点障碍、真实外部等待与整体无路；核具体缺口和影响范围，按证据选择调查、商讨、资源协调、适用审核或原 owner 修正。发出指令后接收实际结果，再更新缺口和下一步，不能把消息发送当完成。

有明确调查方向时继续；没有建议也检查现有能力、原入口、路径/输入/前置和独立义务。未知副作用先恢复原操作，不重发；旧事务已知失败不可恢复时保留事实，由原 owner 核是否存在合法后续操作。无依据同配置重试、无限实验或穷举不成立。

等待必须有责任方、对象及复查条件；每轮核实际条件与等待有效性。操作结束、超时、无人承接或条件失效触发重新判断，即使子会话没有新文字。只有有依据解阻判断已完成且无范围内工作可推进，才最小报告缺失条件并走原安全停妥/心跳停止；恢复同一 run。DAG 按原 failure policy 继续独立工作，Sequence 不跳过当前项。真实用户停止条件保留。

## 7. 恢复、兼容、迁移与集成

无 public API 或持久数据迁移。源码与已安装副本由 canonical 和原 guru-upgrade-tools 的 local_candidate 同步维护；本 Task/session 保留。普通 full apply 的历史 Task 拒绝不触发无关迁移。具体 prepare 冻结后按实际文件清单执行，不手工刷新 manifest。

保留 pending create、未知发送/merge结果的原操作恢复和单集成 owner。通知去重不去重实际状态复查。原公开出口及消费者语义不变。未触及上游模板/runtime，因此不修改全局 npm 或 node_modules。

## 8. 验证设计

| ID | 层/输入/入口 | 可观察结果及 AC |
| --- | --- | --- |
| V1 | 修改前相同 provider 的一组隔离 baseline；真实 Codex 显式调用两技能 | 记录首个失当处置或准确不复现，不制造失败；AC8 |
| V2 | DAG 隔离多轮：独立节点、依赖节点；无建议障碍、外部等待失效/变化、未知消息结果 | 实际调查/讨论/原 owner动作/结果再判断，独立工作合法推进、依赖保留，全部节点达到场景终点；AC1..AC7 |
| V3 | Sequence 隔离多轮：两个节点；旧事务已知失败、普通输入/路径错误、依据不足完成声明和顺利项 | 保留旧失败和身份，合法后续/审核至当前项完整结果再推进下一项，最后 chain_completed；AC1..AC4/AC6..AC8 |
| V4 | Sequence 单节点真实外部/必需 producer 缺口及明确停止边界 | 核当前入口/支持修正后准确最小缺失条件，安全 inactive 与心跳停止，chain_blocked；AC5..AC8 |
| V5 | source/installed 公共包验证、JSON、diff-check、已有定向 package/分发回归 | I/O/metadata不变，两包完整可发现且测试私有文件不泄入public；AC9 |
| V6 | 当前 worktree 原 tools owner 同步、同候选定向 reapply、dogfood drift/sidecars/mode | 实际投影及manifest一致，Task/session保留；只报告所选平台，不宣称完整Release矩阵；AC9 |

V2..V4 从显式公开 Skill 入口运行真实 Agent，初始输入仅目标、现场事实和边界；模型不能读取 host-only 预期或评分。事实型 MCP 只提供当前资源、子会话状态及模型实际所选操作的结果，不判断下一路由、不代发指令、不以关键词审批或生成 gate pass。子会话处置若需要理解自然语言，由独立真实 Agent 执行，不由 fixture 以关键词选脚本答案。场景状态和原始 trace 仅外部临时测试空间；最终报告留必要去敏事实和局限。静态 next-action walkthrough 只补辅助判断。成功运行必须到约定终点；等待实际观察复查及变化承接；真阻塞必须核安全收口。模型/工具不可用或缺分支就保留未验证，调查真实支持路径。

历史采用现场见 research/historical-observations.md，包含 provider 比对、实际首观察窗口、SSM 后续事实和 Sequence 限制。它不证明候选通过。真实 app side effects、生产业务闭环、所有客户端与完整多平台矩阵不在本项证明层。

## 9. Canonical 引用、本轮差额与实际未决项

共享 issue-orchestration.md 与两 package 是本轮运行合同修改点；当前 Codex 发现规范不变。原 RDT owner 以 delta_first 形成三个完整独立知识单元候选（requirement/design/test：issue-orchestration.md），在隔离 proposed 下覆盖要求、方法取舍及行为测试层边界，经 candidate review 后原 final_integration晋升。按 #711 的独立subject导航无需改共享根 README/index/manifest。Architecture candidate 无影响，不创建空contribution/ADR。后续若实际机制超出当前事实，回原资格/Architecture。

无待决定产品选择。MCP载体的实际中立性和真实多轮可执行性须由实施、独立Check验证，不能预判通过。
