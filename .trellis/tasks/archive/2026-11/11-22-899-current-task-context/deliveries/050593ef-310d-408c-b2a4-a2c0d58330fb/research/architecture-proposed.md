# #899 D1 Architecture 贡献

本提案属于 Task `899-current-task-context` generation `0` 和 Delivery `050593ef-310d-408c-b2a4-a2c0d58330fb`。候选路径为 `target_native`，承接 ADR-035 和 ADR-STEP-CONTEXT-LOADING。

## Workflow Context 拟议条款

拟整合到 `docs/architecture/03-domains/workflow-context.md` 的责任范围、正常上下文和分发章节。

标准续接通过一次 Guru 公开只读调用组合当前 Task、C4/C5、会话及上游 Delivery 读事实。查询返回 TaskId、generation、TaskRef、已核验 checkout 及当前义务所需的 Delivery 定位。区分当前、无当前 Delivery、终态、无 Task、需要绑定及原查询错误。显式读取只在原合同允许时执行，返回的目标不成为会话选择。需要写入的绑定、重绑、选择、终态与维护操作各由原 owner 执行。查询不写 Task、session、Git、缓存或 workflow 状态。

会话内的前次结果只在对应当前依赖匹配时复用。Task 分片依赖同一仓库及 context、绑定、TaskId、generation 和当前来源。checkout 分片还依赖当前 C4/C5 与活 Git 登记和 checkout 事实。Delivery 分片还依赖当前选择、精确记录和 workflow 支持声明。变化只使依赖它的复用结果失效。缺失、错误和关系不符保留原诊断及恢复职责。

唯一 Workflow continuation 按当前请求消费定位。相邻既有 typed exit 仍按原出口发现处理。无当前 Task 进入原 No-Task 入口。已绑定且无当前 Delivery 消费原 Task 义务。对返回的精确 Delivery，先读取它的官方 record 和 gate applicability。存在 Publication PR 时，按精确 repo/PR 读回原实时状态。真实 MERGED 优先进入原 Merge recovery，显式合并对象的 adopt 仍使用原前置。只有原 delivered 结果进入 Completion。其余路径按真实适用结果和原 phase 责任承接。

匹配 workflow、Guru runtime 和实际受影响的平台投影同步更新。旧受支持版本继续使用其完整匹配入口。查询结果只作为本次流程定位和同会话事实复用的输入，不是状态或流程决定的权威。验证覆盖标准入口一次解析及原后继选择、查询前后状态、正常变化刷新和受影响的公开分发。

## 整合

原 Architecture owner 在 final_integration 核对实际目标和拟写条款，对照真实实现与定向验证，整合完整当前定义并读回。提交后审核绑定实际 before/after。
