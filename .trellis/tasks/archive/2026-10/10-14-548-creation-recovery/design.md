# #548 验证方案

## 单一机制

正式 current 创建与真实 Codex context Task恢复成立；后续无key D1路径已实际失败：原Creation创建D1后select要求context，原Planning current读取也阻塞。修复原DeliveryProjection接受caller已有明确DeliveryKey：只有官方context resolver确实无key时，经原C4注册checkout、当前TaskId/generation、官方parse/applicability与workflow profile验证，返回call-local current/terminal事实；不写session。无明确key的query仍保留官方no-current，不从inventory推断。有key仍只读取官方current；missing/stale/不同current不能fallback。有keyselection不得静默替换其它Task/Delivery的合法current，普通missing selection可由原Creation恢复。

Author/Wording/Architecture/Approval/Activation均透传原输入已带的key，保留本阶段phase/scope检查；qualification使用原planning_paths/planning_identity，无新增public字段。Creation无key返回created时保留原pending operation/UUID；recover_creation以同continuation/原operation恢复原D1。实际Author成功消费后只调用原Creation退休端口，端口复核exact key/当前scope/原operation后删除自身pending；Author不读取其private格式。有key沿官方session恢复，原成功退休行为保持。

## 来源设计承接

| 来源约束 | 处置 | 落点和理由 |
| --- | --- | --- |
| #548 当前事实与定位要求：当前组合先验证，不预断旧 bug | retain | 定向baseline、正式native样本和联合测试；失败与环境缺口分开 |
| #548 AC1/2：正式创建与 Task/session 或 explicit-task、D1接续 | retain | Create Task 包的联合回归从真正 Guru 创建器开始，使用当前官方公共API；Planning/Activation结果必须来自其原正式wrapper |
| #548 AC3/4/6：同一创建恢复、missing/new session、冲突保护和内容保留 | retain | 原Create/Bind包与TaskLifecycle测试；联合链额外保留规划、普通dirty/untracked、Git和公共slot，恢复不授新gate |
| #548 AC5：旧nonterminal/untracked缺HEAD identity逐记录处置 | retain | 升级包的隔离public Plan2 dryRun样本；明确defer/manual/pinned-old及所缺输入；不会删除重建 |
| #548 AC7：installed/native/projection/reapply/drift分层 | retain | 一份成套current安装复用本次真实Codex context，正式current/continuation读回；平台静态投影与安装字节核验单列 |
| #531当前架构：Task整体scope与所有Delivery独立规划 | retain | D1实际创建后用同一planning_root与原Author/Wording/Architecture/Approval/Activation；测试fixture语义只证明transport层 |
| #548非目标：不改业务树、不扩矩阵、不恢复旧workspace模型 | retain | 验证仅本仓源及/tmp隔离sample，旧主dogfood完整保留，不半升级 |

## 联合回归职责

在 `guru-create-task/tests/` 添加一个包级联合回归。前置由现有正式fixture提供固定上游资产与真实Git linked checkout。执行当前正式Create及原result recovery，再显式whole-scope Author/Clarify和D1 Create，调用真实Planning wrappers直到Approved/Activation及current implementing读回。覆盖有key和无key两条路由；模拟key只记包级事实。保留TaskId/gen、只有一个Delivery、原计划、无额外Git资源，当前公共phase不替代gate。

在 `guru-upgrade-installation/tests/` 补一个旧未提交Task的public Plan2处置回归。用官方前驱安装/Task writer产生旧nonterminal样本并建立可审查inventory；Task不在HEAD时不伪造HEAD/source map或planning pass。实际preview的convert拒绝或defer可执行事实，与原文件字节/mode、HEAD/refs/worktrees保留分别断言。该用例不证明原业务迁移成功。

支持证据文件记录固定CLI/Core资产、当前Guru source、正式和fixture层结果、首个失败、native同Task接续及逐记录停止。已有独立单包测试不复制；普通负例只覆盖AC要求的stale/mismatch/conflict。

## Architecture / Docs

独立实际candidate评估为 architecture_impact / target_native，继承 .88与constitution v1。任务专属贡献为 .trellis/tasks/10-14-548-creation-recovery/architecture-contribution.md；ADR-024仍适用，无新ADR。RDT使用delta_first，原owner拥有 docs/requirements-design-test-contributions/548-creation-recovery/。最终Phase2前完成RDT reconciliation；首次完整committed独立Review后再由原Architecture/RDT owners按expected-current晋升，新增diff重跑Check/commit/完整Review。支持证据只有一个Test SSOT，docs/testing仅导航，避免复制结果。

产品落点为原adapter、Creation runtime及其退休端口、五个已有key的Planning consumer和各自step-local合同。旧root开发API、public DTO、workflow routing和当前完整legacy dogfood不改；成套current隔离安装通过preset重应用验证。匹配前驱不可取得时，旧官方0.6.17 writer + public Plan2的legacy/defer仍只证明受控逐记录保留，不能声称Task1 castbox3转换通过。

## 风险和边界

主/此checkout保留完整legacy运行副本；它们只执行本Task开发生命周期，不证明current Task2组合。current样本成套安装。真实context证据绑定本次隔离sample，不证明CMS原会话。完整Release/multi-platform矩阵、业务安装/部署仍排除。
