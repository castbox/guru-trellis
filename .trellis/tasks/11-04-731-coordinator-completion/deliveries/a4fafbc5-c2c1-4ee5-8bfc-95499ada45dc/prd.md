# D1 协调责任与主动解阻需求

## 1. 整体来源与术语

整体 authority：.trellis/tasks/11-04-731-coordinator-completion/prd.md@sha256:b8df92fe7acf36ab2328d799444cc5b2261125ebc188b39de6d62cb7805f87a9。当前 Delivery：a4fafbc5-c2c1-4ee5-8bfc-95499ada45dc，planning_root=deliveries/a4fafbc5-c2c1-4ee5-8bfc-95499ada45dc。已完整读取整体 PRD 及 Direct Source https://github.com/castbox/guru-trellis/issues/731；本文终点、节点等待和终局阻塞含义与整体第1节相同。共享方法和两 package 是现行合同，源码约束按 design 第3节处置。

## 2. 整体与本批目标、非目标

本批是全量 D1，承担整体 R1..R9/AC1..AC9。现有观察与建议转发不足以保证主动解阻，D1 补齐持续判断、实际动作和终点核证。不操作原业务会话、生产、版本发布或完整多平台矩阵；不新增协调存储或脚本决策器。

## 3. 本批起点、前序结果、依赖与剩余责任

无前序 Delivery。开发基线 main@1d32c9c8044ed12fce54ab991545ab0cfde0993c；PR 目标 main。现有共享方法、调度差异、原 owner 与受管安装可复用。D1 必须同时交付合同、隔离真实 Agent 验证和投影；全部验收完成后仍须原 Task Completion/Closure/Finish，不以一次 merge 代替。无预分配 D2；若验收未满足则继续本 D1。

## 4. 本批调用方、场景与流程

两显式 Skill 的协调 Agent 为真实 caller。S1 顺利推进：轻量观察并核终点。S2 blocked/无建议且仍有方向：调查/商讨/协调并持续接收处置结果。S3 声明不足：质疑证据、要求原 owner 修正并验证。S4 普通输入/路径/前置错误或旧事务失败：保留首失败及同身份，从支持入口恢复或合法后续执行，未知副作用不重复。S5 外部等待：责任方、对象、复查条件明确；实际条件变化或失效时重新安排。S6 真无路：核支持路径及范围内修复后最小请求、安全停妥并停止心跳，条件补齐原 run 恢复。DAG 按真实依赖及 failure policy 继续独立工作；Sequence 完成当前项前不推进后项。

## 5. 完整行为、条件与约束

R1 持续维护全部目标和剩余义务；指令/单轮观察/子会话结束/单 Delivery merge 均不等于整体完成。R2 按真实缺口提醒、调研、商讨、资源协调、质疑及适用独立 review，原正式 gate 不被代填。R3 无现成建议仍识别有依据调查方向；追踪到实际结果再判断，不无限重试、实验或反复审计。R4 保留旧失败，区分原事务恢复和同身份合法后续执行；明确停止条件有效。R5 实际复查等待而非文字变化；超时、结束、无人承接或复查条件失效即重新处置，静默不替判断。R6 无可推进工作才终局阻塞，说明目标缺口、已核方向及原因、最小责任条件、恢复条件和受影响节点，不穷举理论方案，不修范围外框架或替代必需 producer。R7 保留调度、身份、资源、集成 owner、语义 gate、确认和公开出口；原 owner 同步投影。R8 隔离真实 Agent 从正常公开入口作多轮事实/动作闭环，输入和工具不代选动作。R9 实施前刷新采用历史现场，保留可移植去敏首处置/修复对照或准确缺证、不复现说明。

## 6. 本批验收、验证方式与未决项

AC1 两入口持续推进至终点；AC2 可解阻场景真实调查并追踪到终点；AC3 不足阻塞/推荐/完成声明被核证并交原 owner 修正；AC4 保留首失败与身份、区分事务恢复/合法后续、无不确定重复；AC5 最小外部请求、等待失效复查与安全终局收口、调度约束保持；AC6 顺利和不变等待轻量；AC7 用最小充分组合观察多轮真实 Agent 工具闭环，成功至终点、等待至变化承接、阻塞至安全收口；AC8 历史首处置与修复行为或准确缺证说明，三层证据独立；AC9 定向回归、原安装 reapply/drift 与实际平台/mode 边界。以上按整体第7节输入和可观察结果逐项验收，不预填通过。

需求无未决产品选择。验证载体与最小写集由本批原 Planning/Architecture 决定；无法运行不降格为静态通过。

## 7. Canonical 引用与本轮差额

现行行为定义为 trellis/presets/guru-team/spec/workflow/issue-orchestration.md，差额是主动解阻和等待失效后的持续判断。两 package contracts 保留 DAG/严格串行责任。现行 RDT Codex 分发定义为 docs/requirements/current/codex-skill-distribution.md 及对应 design/test；本轮不改变发现机制，新增行为知识由原 RDT owner 形成隔离 proposed 后晋升。Architecture authority 为 docs/architecture/README.md、00-foundation/design-constitution.md、06-governance/change-contract.md；本轮机制影响交独立 Architecture 判断，不能由本文预判。无 API/schema 字段变化。
