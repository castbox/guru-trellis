# 审核充分性的测试策略

导航别名：`R717/D717/T717`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/test/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

Identity：`RDT-TST-REVIEW-SUFFICIENCY`；状态：`current`。关联 [R717](../../requirements/current/review-sufficiency.md) 与 [D717](../../design/current/review-sufficiency.md)。

## T717-01 / SC717-RULES：规则和真实 consumer

比较固定 source 与完整候选，逐条核共同定义的唯一源、旧段删除、合法阶段特例与专题 owner。定向 contract/runtime 验证原公开 I/O 和出口保持；检查 actual provider 读取、目标 authority 分开及共享组合不再反向读取阶段私有方法。文件存在、维度齐全或关键词通过不能证明语义完整。

## T717-02 / SC717-NATIVE：真实 Agent 行为

验收方在执行前固定正常案例、已知问题、合法对照、必要证据缺口和可比条件，不向被测 Agent 注入期待 findings、当前语义结论或入口外纠偏。通过完整 provider 的实际 owner 入口执行 Issue、代码和规划/设计对象，保留首次实际运行及必要重入。原入口需要的独立视角与前置保持，不能用方法片段试验替代。

案例覆盖分散问题、同机制多入口、未修复 findings/失败测试下完成只读审查、正确实现/合法差异、必要证据缺口、后继候选承接，以及充分覆盖后停止。AI 读取实际调查和报告逐例判断遗漏、误报、早停、重复调查及结论局限。原始失败不隐藏；不以总 finding 数、统计改善或绿测代替正确性，也不承诺所有未知缺陷一次发现。

## T717-03 / SC717-DISTRIBUTE：分发和安装

用原受管 writer 安装/reapply 后实际读取新 spec 和命中 packages/平台投影，核用户内容保留及 sidecar；实际 dogfood tools 更新再运行 installed validation 与 overlay drift。普通本项不扩大为完整多平台 installer/Release Gate，local-candidate 结果也不证明 formal source lock 或其它业务仓库采用。

## 观察状态与证据限制

本批实际观察定位为 TaskId=`717-review-sufficiency`、generation=`0`、DeliveryId=`a55b1bd3-718a-42aa-a77a-dc9387abc2b9` 的 `validation/review-sufficiency.md` 与 `validation/implementation.md`。前者唯一承接真实 old/new 案例、首轮失败、合法控制、原入口与恢复后的逐例判断；后者承接定向机械、分发与实际 tools 采用。Task 活动或归档路径由原 Task 身份解析，不依靠本单元复制运行摘要。

已取得的证据是本地候选源码、实际安装和受控案例中的 Agent 行为，不推出统计改善、任意审核一次发现全部缺陷、外部专业 Skill 接入或业务生产效果。首次失败及原独立入口 bootstrap 的未验证边界保持原观察；正式 Check/Review/Delivery/Completion 读取各原公共结果与 Git/PR 事实，知识晋升本身不产生阶段通过。完整多平台 installer/Release 矩阵及 formal Fork source-lock 仍未验证。

## T-JQ-INDEPENDENCE / SC-JQ-INDEPENDENCE：独立推导及裁剪观察

承接 BEH-JQ-INDEPENDENCE → CON-JQ-INDEPENDENCE。来源为 Task `user-journey-quality` generation 0、Delivery `9edfdfc4-9f0b-4a1c-bfc7-88a70f26abad` 的 V1—V4；本次已取得原生 Agent 只读方法执行观察，T717 的历史观察不重写为本轮证据。本次 JQ 定义由该 Delivery 的实际 candidate_checked 后，原 RDT owner 在 final integration 整合并读回；当前定义由包含本文件的精确 Git revision 绑定。方法实现、有限行为观察与受管采用分别判断，最终 Check、Review、Delivery 和 Completion 仍由原 owner 的实际结果建立。

V1/V3 评价原职责入口在未收到缺陷答案时，是否从当前 authority 和真实材料推导连续操作、交接或验证缺口，再对照候选；检查原首读、隔离和资格规则保持。V2 观察已有入口与局部测试事实是否得到适当证明层级和验证顺序。V4 的 trim 纯函数合法对照检查方法不把简单任务扩大为 UI/设备验收。

独立评价者在执行前持有预期，读取完整实际输出、工具调查和局限，区分遗漏、错误扩张与未执行。材料中的教学例子或已知历史答案不能替代原生观察；不以问题数量、关键词或多个 Agent 同意推断充分。适用证据沿原规则复用，不因执行者或阶段更换重跑。

分发采用复用 SC-JQ-05..06；本单元不复制执行记录、固定评分或统计收益。真正阶段通过仍由原 Check/Review 等公共结果建立。


## JQ 当前观察与证明边界

实际结果由 TaskId `user-journey-quality`、generation `0`、DeliveryId `9edfdfc4-9f0b-4a1c-bfc7-88a70f26abad` 的 `validation/behavior-evals.md` 与 `validation/implementation.md` 唯一承接，Task 活动或归档路径由原身份解析。V1—V4 使用完整 canonical provider 和执行前冻结的中性材料，记录实际原生 Agent 的输入、工具及输出。观察支持本组材料中的连续操作与交接推导、真实未决选择保留、局部证据范围限制及纯函数低成本对照；独立预期未提供给被测 Agent。

该执行使用原职责的方法进行只读推导，没有运行四组正式公开 owner 的完整生命周期链或 formal Check/Branch Review，也没有操作真实业务应用。不能将方法观察提升为正式门禁通过、业务验收、任意未知缺陷检出或统计收益。V5/V6 的实际定向分发/reapply 和本 checkout tools 更新支持受管正文采用；`local_candidate` 保留 `formal_fork_source_lock` 未验证，完整 Release 矩阵、业务项目采用和 QA 缺陷率改善也未验证。知识晋升本身不补足这些证据。
