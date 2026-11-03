# 审核充分性能力

导航别名：`R717/D717/T717`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/requirements/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

Identity：`RDT-REQ-REVIEW-SUFFICIENCY`；状态：`current`。来源：[Issue #717](https://github.com/castbox/guru-trellis/issues/717)。

## R717-01 / BEH717-OWNER：共同规则的唯一来源

Guru 为自己的现有审核职责提供一份可加载的共同充分性规范。规范正文由 `trellis/presets/guru-team/spec/workflow/review-sufficiency.md` 唯一维护；原 owner 在其实际审查范围内读取并执行，旧重复正文迁出后删除或引用。审查对象的范围、覆盖、调查、发现判断、结束、局限和后继承接的完整条件只由该源定义，本单元不再建立平行定义。

该要求在原 owner 接到明确当前对象/目的/版本的审查时生效。审核完成、对象通过、修复/验收完成分开；各阶段的独立性、顺序、通过条件、typed exits、恢复和副作用仍由原 Skill 持有。工程方法组合不得依赖 Check/Branch 的私有阶段方法；不能以新文件、优先级声明或机器通过代替旧定义退出和真实执行。

## R717-02 / BEH717-BOUNDARY：provider 与目标独立

框架方法来自完整 Guru provider；受审仓库提供自己的实际 authority。Guru 按专业来源及版本消费证据，不复制独立专业标准。外部专业 Skill 的独立调用不能因为本项而隐含要求 target 安装 Trellis；本项不实现外部仓库接入，也不批量升级业务项目。

不存在新的公共 Skill、I/O、schema、出口、长期覆盖台账、评分器或充分性 gate。题目外的攻击、竞态压力、业务修复和完整发布矩阵不进入该能力。原 Task/Delivery 与修复调度责任保持。

## R717-03 / BEH717-ADOPTION：实际执行与采用证据

仓库交付须使固定 source 上承担审查的必要消费者真正加载唯一源，保留合法阶段差异，并通过真实生产 owner 入口观察代表性 Issue、代码和规划/设计审核。验收方在运行前确定问题、合法对照和必要缺口，保留首轮 old/new 实际结果，不把预期 findings 或当前判断注入被测 Agent。逐例判断行为和局限，机械分发、命令通过或问题数量不替代该证据。

受管 canonical/dogfood/installed、声明平台及适用 reapply/drift 是独立采用义务。普通任务不承担完整 installer/Release Gate 矩阵。源码变更、模型行为和实际项目安装分别表达；任何未完成责任不能改称已经采用。

## 关系与完整定义

[设计职责](../../design/current/review-sufficiency.md) 与 [测试策略](../../test/current/review-sufficiency.md) 承接本能力。共同审核行为只读取唯一 managed spec；现有检索、测试价值、因果、完整知识和专业标准保持原 owner。Architecture 的 owner/依赖决定见 `ARCH-REVIEW-SUFFICIENCY` 与 ADR-REVIEW-SUFFICIENCY。
