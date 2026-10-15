# ADR-567-CANDIDATE 固定内容对象与实际阻塞整合

状态：proposed / task-owned。来源 #567；尚未接受或晋升。关联 contribution：architecture-contribution.md。承接并在接受后替代 ADR-005/012/013/024 中与本决策冲突的默认base/freshness规则；历史正文不改写。

## 背景

开发基线、每轮Delivery未交付内容与PR目标是不同对象。以target最新SHA、整体CURRENT版本或祖先关系作全链资格，导致隔离任务被动整合和重审；原source范围、候选和事务检查不能因此一起删除。

## 选择

内容审查绑定固定完整候选与阶段适用authority，由原semantic owners决定适用性。每轮范围使用实际未交付事实，后续Delivery不重复前序已交付内容。PR能否合并由原merge流程的实际GitHub状态、必需检查和既有服务端规则决定；分支是否包含最新base是独立事实，不成为通用资格。

Reconcile只响应真实冲突/具体集成问题/原merge已确认的服务端更新要求/明确依赖或需求/主动同步；一次固定目标，局部变化沿原owner审查差额和依赖。保留全部原子能力和同操作恢复；不以空提交、tree等价、旧pass重标签或伪造gate推进。

authority版本与fixed candidate不是忽略实际需求变更。显式适用规则、scope、方案、实现语义和依赖变化仍回原owner。共享CURRENT promotion保留真实写前expected-current，不能变成所有在途Task的重规划义务。Completion仍核验全部scope和真实交付，查询截点不冒充截点后新增事实，#569独占查询准备。

## 取舍与退出

删除默认pair guard、无consumer的同步状态及全链freshness耦合；不增加bypass、并行协调器、长期证明库或兼容分支。内部API直接演进，MIGRATION-567同步producer/consumer并覆盖正常在途恢复；实际安装与旧数据迁移沿#566原owner。真实mutation的expected-head/payload/身份一致性保留。

本决策须经final_plan、实现、项目检查与独立完整committed Review后，由原Architecture owner决定接受及正式ADR编号/导航，随后promotion新diff重新验证。未达到该边界前只有candidate地位，不改变shared CURRENT或声称安装/发布通过。
