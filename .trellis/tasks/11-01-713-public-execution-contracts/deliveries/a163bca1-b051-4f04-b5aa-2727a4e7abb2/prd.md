# D1：公开执行合同与定向交付验收需求

## 1. 整体来源与术语

Direct Source 为 [#713](https://github.com/castbox/guru-trellis/issues/713)，整体需求见 [Task PRD](../../prd.md)。当前根 PRD 已通过原范围接受，D1 已合法退回 planning；本批引用该公共 authority：`sha256:bacc8a5f1a574dd76dc4274dece5bfd14cd27d2ccdef5942046a93683d6667ff`。
D1 保持 TaskId 713-public-execution-contracts / generation 0 / delivery_id a163bca1-b051-4f04-b5aa-2727a4e7abb2。固定 B 为 8378b8d500a974ae1c01bd0571f30149f56541b0。选中 S1–S5、AC1–AC4、缩减后的 AC6–AC8 与 AC9；AC5 取消。
MIGRATION-710 的 authoring/结果兼容和原错误语义保持。历史结果、局部命令、结构、安装及 native 按实际层级使用，取消验收不等于通过。

## 2. 整体与本批目标、非目标

本批交付完整公开执行资料、原生产入口调用闭合、错误/恢复/结果消费、R5 职责收敛和匹配分发。采用仍适用的定向结果，不再追加完整 native 链、非等价 native 代表、旧 fixture 接续或重复安装。
公开支持语义、已知正确性缺陷修复和全部最终质量门禁保持。D1 独占保留后的完整范围；取消项不形成隐藏 D2 或必需补证支线。#711/#712/#363、业务 #994 代码/状态/生产、上游/global/node_modules、攻击/并发加固及完整发布矩阵仍为非目标。

## 3. 本批起点、前序结果、依赖与剩余责任

这是同一 Task 的首次 D1，B/H0 和 main 目标保持。#710 实际前置交付已在 B；其历史证据不替代本项当前 Check。固定声明集合仍为 43 包、127 命令、180 structured profiles。
已有代码、合同、consumer 和安装结果由原 Check 判断适用性。N1 首装配失败、N3 public-only 不充分、F10/H2 非通过、R5 方法不足/resume execution_error/Drift fitness_regression 保留；R3 仅 runtime 准备通过且未启动 native。旧 clean 后续损坏不归因 installer，不称当前可用。
余下责任是同步范围、更新受影响规划和知识贡献、完成当前范围全部质量链及交付，不再续跑取消项。

## 4. 本批调用方、场景与流程

| 场景 | 前置、动作与观察 |
| --- | --- |
| SC1 原公开步骤承接 | 正式安装和真实原 owner 前置下，核公开输入、原命令、producer 输出及 consumer；采用已发生的定向结果，不要求新的 preTask→Finish native 链 |
| SC2 普通错误 | 使用已有 relation/disposition、authoring/result、receipt 等实际错误及公开纠正结果，保留原失败 |
| SC3 变化与恢复 | 采用已有真实 candidate/stale/同结果恢复证据，检查 key/B/适用结果不被覆盖；取消追加完整 native 恢复链 |
| SC4 固定调用族 | 核 F1–F13、mode/profile、当前/旧合同及 consumer，逐项标记现有证据和未验证行为，不追加非等价 native 场景 |
| SC5 执行器真实故障 | 保留 exit/stdout/stderr 和确认范围，已知正确性缺陷交原维护 owner，不将 caller 错误改判产品缺陷 |
| SC6 分发与兼容 | 复用仍匹配的 source/dogfood/平台/代表安装、mode/sidecar/reapply/drift 及旧 consumer 事实，仅刷新真实变更依赖 |


## 5. 完整行为、条件与约束

本批逐项满足整体PRD第5节S1–S5，具体承接如下：

- S1：固定B声明集合逐owner核对完整调用链。补R1既有Issue/no_issue输入域与正向示例；修R2当前/旧合同导航，公开多profile选择条件和真实兼容域。AI字段、producer身份、recorder字段分清，正常authoring不得要求完整结果字段。不得将实现偶然限制提升为新义务。
- S2：先证明既有public CLI/dispatcher能否完成candidate/内容身份/阶段操作及恢复；充分时补原owner调用说明，不新增能力。真实缺额才补原owner最小生产命令。AI选择范围/B/路径/阶段，执行器计算事实；workflow只保留全局顺序和路由。
- S3：机器可判断的输入/合同/stale给具体诊断与原恢复，内部故障只报告确认范围并交维护；完整捕获原退出状态及双输出，显式消费receipt.result/checker receipt/唯一typed exit；原错误不吞掉，不从截断显示补字段，不重算旧摘要。
- S4：R5三辅助逐项对照生产能力，正常所需导航/选择/计算归生产owner，eval复用。隔离/替身/路径/运输/观测可留，单元完整fixture只证明其边界。真实 Agent 的当前语义前置不可由 host 预填。采用已有结果时，必须保留实际读取、输入、命令和承接的证据层级；缺 native 不改记为通过。
- S5：完整matching分发和既有成功consumer显式兼容；原owner处理sidecar与用户修改，保留模式和session/Task；没有旧consumer不能发明长期兼容层。已发布成功语义若变化先形成迁移合同。

规范性来源设计的唯一retain/change/reject矩阵在本批design第3节；PRD不另建第二矩阵。原AI/脚本职责、稳定API、typed exit和freshness保持；本批不持久化授权或新审计链。

## 6. 本批验收、验证方式与未决项

| AC | 要求 | 保留的可观察验收 |
| --- | --- | --- |
| AC1 | S1/S3 | 原 creation Issue/no_issue 正向调用与已观察字段错误的定向证据；公开 schema、例子及诊断与实际入口一致。 |
| AC2 | S1 | 固定 B 和本项差额的 43 active packages、127 commands、180 structured profiles 完成导航、输入/输出及 consumer 核对；保留真实兼容域。 |
| AC3 | S2 | 原 construct/candidate、阶段与恢复入口的定向执行和真实 consumer 结果；公共 token 原样承接，不复制私有算法。 |
| AC4 | S3 | 原命令 exit/stdout/stderr、receipt.result、checker receipt、typed exit 的定向检查和真实错误事实；不吞掉 stale 或已确认故障。 |
| AC5（取消） | S4 | 取消新的首次正确完整 native 链验收；原失败、纠正后结果与未验证范围保留，不作为通过项。 |
| AC6（缩减） | S3/S4 | 复用普通错误、真实 stale、结果丢失/恢复的现有定向或局部命令证据；取消新的独立 native 恢复链及旧 fixture 状态接续。 |
| AC7（缩减） | S1/S4 | 保留 F1–F13 的声明语义和证据层级对应；采用现有结构、命令、安装、synthetic 与局部 native 结果，不再要求追加非等价 native 代表。 |
| AC8（缩减） | S4 | 保留 R5 三辅助职责对照、生产能力归原 owner、合法 fixture 与原入口模块回归；取消 R5 模型方法加载及特殊接续的新增行为补证。 |
| AC9 | S5 | 采用当前匹配 canonical/dogfood/平台/代表安装及兼容恢复的现有实绩；只刷新实际变更依赖，不重复安装或完整矩阵。 |

| 取消项 | 范围 | 结果口径 |
| --- | --- | --- |
| C1 / AC5 | 新的 preTask→Finish 首次正确完整 native 链 | 取消本批验收；已有首装配失败与后续生命周期事实保留，不记全链通过。 |
| C2 / AC6 | 新的独立 N3 public-only 变化/结果恢复链及旧 fixture 接续 | 取消追加 native 和历史状态恢复；已有普通错误、stale、同结果恢复按实际层级采用。 |
| C3 / AC7 | F10、其余非等价 family/profile/caller/goal 的追加 native 代表 | 取消追加模型验收；保留 43/127/180 声明、导航与 consumer 映射和已有定向结果，未验证行为明确列出。 |
| C4 / AC8 | R5 完整方法加载、Planning→同 fixture Activation/resume、Drift 的模型方法补证 | 取消补证及重跑；保留职责对照、生产入口、alias/consumer 模块结果，以及 execution_error、fitness_regression 和方法证据不足。 |
| C5 / AC9 | 为补上述 native 而重复准备环境、恢复损坏 clean 或再次安装 | 取消重复准备与安装；复用完整且仍匹配的安装/投影、reapply/drift/sidecar/mode 实绩。 |

没有未决产品选择。源 Issue、根 PRD 接受和 D1 scope revision 已完成。保留范围须经过候选 Check、原知识 final integration/readback、最终 Check、TaskCommit、完整 committed Review、Delivery Review/readiness、发布/交付和 Task Completion/Closure/Finish；合并前保留 fresh merge gate。

## 7. Canonical 引用与本轮差额

| 当前authority | 命中内容与本轮差额 |
| --- | --- |
| [Requirements lifecycle](../../../../../docs/requirements/current/task-delivery-lifecycle.md)、[Completion](../../../../../docs/requirements/current/completion-closure.md) | 复用Task/Delivery阶段和Completion责任，补正常入口合同及恢复可执行性，不另建生命周期 |
| [Design lifecycle](../../../../../docs/design/current/task-delivery-lifecycle.md)、[Completion](../../../../../docs/design/current/completion-closure.md) | 原owner生产操作与consumer承接，当前导航和候选操作说明差额 |
| [Test lifecycle](../../../../../docs/test/current/task-delivery-lifecycle.md)、[Completion](../../../../../docs/test/current/completion-closure.md) | 现有fixtures/public-wrapper证据只作分层起点，本批按修订后的 AC 采用现有定向证据，取消三族与未覆盖 family 的追加 native 要求 |
| [Architecture](../../../../../docs/architecture/README.md)、[constitution](../../../../../docs/architecture/00-foundation/design-constitution.md)、[change contract](../../../../../docs/architecture/06-governance/change-contract.md) | owner/控制面/执行面、最小必要复杂度、兼容退出；由独立Architecture判断本候选影响，不能以PRD声称符合替代 |
| [知识维护](../../../../../docs/requirements/current/knowledge-maintenance.md)及匹配Design/Test | 修原RDT/Architecture执行合同；不提前实施#711知识组织迁移 |
| [Skill package contract](../../../../spec/workflow/skill-package-contract.md)、[Quality](../../../../spec/workflow/quality-guidelines.md) | public I/O、最小DTO、验证范围与native层级；原writers负责真实知识差额，不预建空贡献或共享索引 |

本批后续方案、Policy和Docs Plan分别由design、implement拥有。后续实施/审核实际加载上述必要正文及关联条件；链接存在本身不作为已读或通过证据。
