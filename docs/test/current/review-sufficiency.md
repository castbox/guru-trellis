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
