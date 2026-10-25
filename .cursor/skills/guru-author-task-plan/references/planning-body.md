# 规划正文合同

## 1. 使用与职责

这是四类规划正文的唯一共享规则源。Author 在每次写作前实际读取本文件、当前 profile 的模板、完整当前来源及其关联条件。先完整读取安装的 `.trellis/spec/workflow/clear-technical-writing.md`；语言规则只由该规范定义。本文件和模板不改变 Skill Interface、原 owner、接受出口或 freshness 规则。

| 正文 | 模板（相对本文件） | 职责与完成边界 |
| --- | --- | --- |
| Task `prd.md` | [task-prd.md](../templates/task-prd.md) | 整体问题、来源、需求和验收责任；`scope_requirements_ready` 前完成，由原 Clarify 审查后 `accept_scope`。此时不要求 Delivery 方案。 |
| 所选 Delivery `prd.md` | [delivery-prd.md](../templates/delivery-prd.md) | 本批完整需求与上下文；当前 requirements 阶段返回 `requirements_ready` 前完成。此时不要求尚未开始的方案。 |
| 所选 Delivery `design.md` | [delivery-design.md](../templates/delivery-design.md) | 本批实际设计和唯一来源设计处置；`plan_ready` 前完成适用内容。 |
| 所选 Delivery `implement.md` | [delivery-implement.md](../templates/delivery-implement.md) | 本批执行、验证、Policy 和 Docs Plan；`plan_ready` 前完成适用内容，再经原 Wording、Architecture、Approval。 |

整体范围仍由公共 `accepted_scope` 承载。Delivery 写作先解析本次实际 DeliveryKey、`scope_ref/planning_root`，另读整体 PRD 和真实前序事实。scope-only Task PRD 写作不要求存在 Delivery。不得从目录盘点猜选切片，不创建 Task 根 design/implement，不覆盖历史 Delivery。原生 seed 是合法起点，不代表正文已完成。

## 2. 从来源到正文

1. 读取完整当前请求、选定 Issue/评论、相关仓库事实及 canonical authority。不要先把详细来源缩成摘要，再只从摘要推导。
2. 在来源表区分要求、已约定设计、建议、候选、历史事实和原始证据。每项给出可解析 locator、章节/条款和用途。较新或较短的来源不能自行覆盖旧承诺。
3. 详细来源可原文保留或等义组织到模板章节。核对背景、场景、行为、完整条件、否定、例外、执行顺序、义务强度、约束、依赖、非目标和验收。技术内容只有经原 owner 选为规范性约束或已接受方案时才是必须保留的来源设计。
4. 简略来源和无 Issue 请求先由 Discovery 调查代码、文档、调用方和历史可回答的事实。Clarify 处理剩余的需求、来源角色、范围或真实产品选择。未知事实和未回答的问题如实保留；不得编造用户答复或用默认值补成已确认要求。
5. 需求明确而机制未定时，由 Author/Architecture 细化技术方案。不要把技术未定变成要求用户提供实现。真正冲突回原 owner；范围变化回 Clarify。普通正文遗漏回最早受影响的写作阶段。

必要引用须能定位到已接受本地内容或明确 canonical authority，并写明章节/条款及本批用途。共享定义、完整接口规格可以引用；本批行为、条件、约束、验收、设计差额与执行安排仍在对应正文展开。实施和审核前实际加载引用及必要关联条件，链接存在不能证明已读。引用失效或来源变化时，沿原 owner 判断影响并刷新受影响阶段；不制造摘要缓存、第二范围权威或跨阶段审计链。

## 3. 结构、字段与深度

按各模板的编号和章节顺序写 Markdown。模板中的“填写”提示是写作指令，完成正文用实际内容替换；不用空表或占位符冒充结果。需要逐项核对的要求、场景、接口和验收保留稳定 ID；已有来源编号可沿用。ID 和矩阵只帮助定位，不能替代行为说明。

始终适用的内容包括来源、问题、目标/非目标、真实调用方和场景、行为、范围、可观察验收及实际未决项。场景填写调用方、前置条件、触发动作、处理行为、可观察结果。存在真实业务角色与价值时写用户故事及验收场景；工程变更使用真实调用方，不编造最终用户。各验收对应需求和验证方式，说明输入、入口及可观察结果，不预填通过。

复杂度决定展开深度。存在服务/API、持久化、状态转换、分支或跨 Delivery 集成时，写出实际名称、方向、字段/值、职责、顺序、失败结果和必要恢复。接口表应能让实施者定位生产者和消费者；流程应能让审核者分辨成功、失败及例外。图表辅助正文，不代替行为。

简单工程变更可以短写，但保留必要章节。workflow 的接口可以是“原 profile/输入 → 加载对象 → 原出口/consumer”；说明公共数据是否变化，不为填表创造 API 或状态。没有状态转换时写执行顺序。条件内容逐项说明真实的不适用理由或等效章节位置：例如“没有持久化字段变化，因此没有数据迁移”；不得把适用内容统写“不适用”。

草稿和返工允许有具体缺口；写明缺什么、待哪个原 owner 处理、阻塞哪一阶段。到第1节对应接受边界前补齐当前阶段。空标题、TBD、“沿用原方案”、宽泛编号及预填 pass 不算完成。确实没有必要未决问题时如实说明；后续非阻塞观察不能混为当前缺口。

## 4. Delivery 与来源设计

全量 D1、部分、后续及同批返工都要写本批独立目标、覆盖项、排除项、起点、输入/依赖、边界、剩余责任和整体 Completion 关系。首次明确没有前序；后续实际读取前序交付结果，区分已交付事实和当前待实现要求。设计写清已有能力、目标状态、本轮差额、前后交付接口及适用兼容/集成。复制整体 PRD 或只列编号不能替代这些内容。

存在规范性来源设计时，由当前 Delivery design 第3节维护唯一处置矩阵：来源、原承诺、retain/change/reject、具体设计落点、理由、影响、上游处置。逐项核对，不用“R1–R7 已保留”代替实际落点。PRD 和 implement 只引用该矩阵。无规范性来源设计时说明已读来源及判断依据，不建空矩阵；实际方案仍须展开。偏离必须回真实上游 owner，不得通过模板静默改变承诺。

implement 保留唯一 Delivery Policy 和唯一 Docs SSOT Plan，具体策略含义沿 [authoring.md](authoring.md#solution-writing-and-complete-positive-capability)。三份 Delivery 文档各保留命中的 requirement/behavior、design、test、Architecture canonical 引用及本轮差额。模板填充只生成所选规划；不直接写共享 README/index/manifest、Architecture Baseline 或 spec projection，不预建空 contribution/ledger。原 Author 的真实 task-owned Architecture contribution/必要 ADR 候选与原 RDT/Architecture 晋升职责保持。

本批存在真实临时限制时，在现有 Policy、步骤和 Docs Plan 内说明限制的能力／对象、原因、解除条件、当前阶段边界和直接后继责任。后继 Delivery 实际读取前序结果，核对解除条件；条件满足后，实施 owner 更新行为和适用断言，原 RDT／Architecture owner 在自己的合法边界维护当前规范、指南及派生说明。历史正文保留原观察。局部限制不等于整个 Task 冻结，局部实现也不等于整体完成。没有真实限制或变化时，不增加空文档、状态字段或验证义务。

## 5. 写作自检、原审核与示例

输出前由 Author 对照完整来源、适用模板和实际正文自检：当前阶段是否完成，场景→要求→设计→实施→验证→验收能否对应，引用是否实际读取，来源角色、条件与历史身份是否保持。原审核 owners 只在原范围判断；不新增通用 reviewer。脚本只检查分发、引用、投影及既定机器条件，不能凭章节数、关键词或文件存在证明充分性。

[详细来源示例](../examples/planning-body/detailed/process.md) 展示技术约束、全量正文、部分及后续切片和具体修订。[简略来源示例](../examples/planning-body/brief/process.md) 展示事实调查、真实问题待答分支、无来源设计和简单任务裁剪。示例是去敏教学材料，不能当作当前需求、真实用户答复或测试证据。只有当前 accepted scope 要求实际 Agent 行为验证时，才由原 owners 经正常入口执行并单独报告；本次 #154 的 V1–V7 不成为所有业务 Task 的固定验证义务。
