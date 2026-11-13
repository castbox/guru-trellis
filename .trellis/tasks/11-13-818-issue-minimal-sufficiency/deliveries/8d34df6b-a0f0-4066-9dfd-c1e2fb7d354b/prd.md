# #818 D1：收敛 Issue 内容方法

## 1. 整体来源与术语

整体 authority 为[Task PRD](../../prd.md)，公共 accepted_scope revision 为 `sha256:065383064cb34c9454364a6082852cccdbf993f713cb5eaadbad9f34c626fe20`。本 DeliveryKey 为 `818-issue-minimal-sufficiency / 0 / 8d34df6b-a0f0-4066-9dfd-c1e2fb7d354b`，planning_root 为 `deliveries/8d34df6b-a0f0-4066-9dfd-c1e2fb7d354b`；scope_ref 选择整体 R1–R4、AC1、AC2。

Direct Source 为 [#818 全文](https://github.com/castbox/guru-trellis/issues/818)，当前无评论。整体 PRD 第1节列出的四份固定外仓来源已完整读取，只提供可迁入 Guru 的方法。当前 `issue-content.md`、四原 owner、共同审核充分性规范及 #153 RDT 贡献提供既有职责与实现事实；不能自行升级为新增需求。没有额外规范性来源设计。

## 2. 整体与本批目标、非目标

本批完整交付 #818：让四原 owner 在 Issue 创建、修订和审核中，先判断要求必要性，再检查表达充分性。读者能连续理解触发、执行者、核心行为、结果及必要例外；验收先证明主要结果，保留有来源的保护和真实适配。

本批覆盖整体 R1–R4、AC1/AC2。范围包括唯一共享内容方法、必要 owner 引用、受影响投影和真实 Agent/定向分发验证。不新增 Skill、轮次、评分、证明表、资格账本、脚本语义判断或评测平台；不改 #819 的评论复用/Intake 路由，不继承 #747/#736 整项，不关联发布版本或执行完整安装发布矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

这是本 Task 首个 Delivery，尚无前序 Delivery。开发起点为 `fd0ee32618433a92ae934e29afb5b72e7136b4f7`；#815 的交付及归档已在该 main 中。当前共享规范已实现来源保留、正文裁剪和四 owner 同源读取，现有分发测试及去敏示例可复用。

本批输入是当前 Issue、整体需求、现有内容与审核合同及四份方法原文。公共扩展交付后不依赖外仓运行时读取。当前没有需要交给后继 Delivery 的独立责任；整体 Completion 仍须确认本批真实行为与采用证据，Delivery 合并本身不代表 Task 完成。

## 4. 本批调用方、场景与流程

- **D1-S1 写作/修订：**Clarify 接收原始需求和现有正文。它检查新增要求的实际用途，删除无依据扩张及其派生义务，保留必要保护和现有入口适配。随后用连续规则说明主要行为，再组织例外和验收。
- **D1-S2 原审核：**Wording、Readiness、Create Issue 分别在原门禁内读取完整正文和必要来源。审核者独立说明适用场景、主要结果和必要例外，再核对来源、消费者与验收；同时识别冗余和遗漏。遗漏及真实范围选择仍回原 owner，不新增审核节点。
- **D1-S3 采用/验证：**原安装 owner 从 canonical 同步受影响 dogfood 和声明平台。原有执行能力观察实际写作及审核输出；原分发工具检查字节、引用、reapply、drift 和 sidecar。两类结论分别报告。

## 5. 完整行为、条件与约束

1. **必要性（整体 R1）：**新增要求、机制、验证义务必须对应原始需求、受支持场景、真实消费者和当前结果。说明省去该项会使哪项原始需求无法完成。结果必要与整套机制必要分别判断；历史实现/测试/审核不能自行授权要求。
2. **扩张收敛（整体 R2）：**无依据或已排除的扩张不转成确认问题、测试、Finding、依赖、后续任务或放行条件。收敛要求及其派生链，不改名或迁往其它阶段。原始需求明确的安全、权限、敏感数据及真实兼容责任保留。
3. **规则与审核（整体 R3）：**先连续说明触发、执行者、行为和结果，再展开必要例外与技术约束；同一规则只有一个完整定义。审核独立还原规则，反查真实入口；发现入口不自动增加交付项，必要适配也不能误排。摘要、关键词命中或作者解释不能替代正文可理解性。
4. **验收（整体 R4）：**主目标先于必要保护，不逐项复述功能规则，不追加无来源的固定样本数、设备数、测试方法或完整矩阵。验收深度与当前成果一致，下游准备由下游阶段负责。

四原 owner 的职责、Skill I/O、typed exits、扫描范围、确认、刷新及恢复不变。Markdown/AI 判断语义；脚本只执行确定性动作。具体共同正文组织由本批 design 承接，不在各入口复制第二份规则。没有新增持久化字段或数据迁移。

## 6. 本批验收、验证方式与未决项

- **D1-AC1 / 整体 AC1：**复用现有过程示例及执行能力，通过原写作和审核入口观察实际输出。用包含普通过度要求、派生验收及同源必要保护/入口的输入，检查是否删除扩张、突出主要结果，并保留必要语义。记录实际覆盖和局限；不以静态分发结果宣称行为通过，不为验证擅自发布 GitHub 对象。
- **D1-AC2 / 整体 AC2：**使用原分发、引用、安装/reapply 和 drift 能力核对受影响 canonical、dogfood、installed 与声明平台投影一致；执行与真实差额匹配的定向验证，报告未执行项。完整安装或发布矩阵不属于本批。

暂无阻塞本批 requirements 阶段的范围或产品选择。当前只完成需求规划；行为验证、受管采用及本批交付均未完成。

## 7. Canonical 引用与本轮差额

| 既有 authority/合同 | 本批用途与实际差额 |
| --- | --- |
| `trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md` 全文 | 唯一 Issue 内容规范；承接必要性、派生义务、完整规则组织和主目标验收差额 |
| `trellis/presets/guru-team/spec/workflow/review-sufficiency.md` 全文及 `docs/requirements/current/review-sufficiency.md` | 保留共同审核充分性职责；核对 Issue-specific 方法的唯一定义和引用，不把本项扩成所有审核阶段重构 |
| `docs/requirements-design-test-contributions/153-issue-content-ssot/{requirements,design,test}.md`，经 RDT `.109` 未迁移入口承接 | 保留四原 owner、来源整理、原创建/修订和分层验证责任；历史 T153 结果不作本批通过 |
| `trellis/presets/guru-team/scripts/python/test_issue_content_distribution.py` 与 `test_review_sufficiency_distribution.py` | 复用真实 writer 的分发/reapply/引用检查；不增加文本自证或以其替代 Agent 观察 |
| `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md` | 独立 Architecture 按原权威读取并评估当前候选；本 PRD 不预选其影响结论或晋升结果 |

本批真实 Architecture/RDT 差额及 Docs Plan 在原 owner 评估后写入设计与实施规划。Planning 不直接修改共享 current、全局导航或安装副本。
