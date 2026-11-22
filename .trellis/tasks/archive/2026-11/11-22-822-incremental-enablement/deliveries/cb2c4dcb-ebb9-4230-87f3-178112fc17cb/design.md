# #822 D1 增量启用接续设计

## 1. 设计目标、需求承接与内容基线

本批覆盖 Delivery PRD 的 DS1、DS2、DAC1 和 DAC2。开发基线 B 和 Planning H0 均为 `ffbc25e32e65fa843c0ff0d75a9f16f0e0f0ea8f`。该提交为 Intake 固定的 origin/main。实际交付范围按原 Candidate constructor 读取 B 到交付候选，Pull Request 目标为 `castbox/guru-trellis:main`。独立 Architecture 候选评估返回 `baseline_current` 和 `no_architecture_impact`，沿用项目 Architecture Baseline、设计宪法和变更合同。

## 2. 当前系统、边界与目标差额

本 Task 的 D1 无前序切片。验收样本有一项由现有 Task 与 Delivery API 承载的已交付计费实现。样本的配置加载、预算条件以及前序证据都可读。前序证据覆盖固定 writer 精度和物理索引。模型预算与本批配置加载需要定向补验。

当前 `guru-create-delivery:created` 有唯一 router。router 读公共阶段和实际义务，Author 已有增量写作和相邻证据要求。基线的固定范围检查与新会话绑定/选回检查已通过。现存恢复测试还执行已退役的 `chain.wording()`，故不能证明当前 final Architecture、Approval 和 Activation 链。将该检查对齐 #850 已交付的链路，并保留原同切片和规划文件不变断言。正常 Agent 样本若暴露当前导航缺口，补在发现该缺口的原入口。

## 3. 来源设计处置（唯一）

没有必须采纳的外部方案。#822 要求在原 continuation、Creation、Author、验证及交付职责内采用现有 `discover-skill-contract`。此约束在 §4–§7 承接。业务 PR #1468 和 #1281 只提供去敏案例与依赖背景。

## 4. 模块、职责与设计取舍

- 续接入口只读取实际 Task、Delivery、阶段、适用结果，并把当前对象交给原 owner。前序切片已交付且有明确后续目标时，原 Creation 创建当前 slice。切片已存在时，原 Selection 保留 key，原阶段 owner 接续工作。
- Author 读取前序 Delivery 可引用结果及当前配置差额，形成实际影响与补验。资金精度、索引、模型预算和配置加载各自对照条件。评估后只补当前未覆盖的内容。
- 验证层使用已受管的 CLI/API 和现有测试。原 `guru-author-task-plan/tests/test_receiving_session.py` 保留当前 final Architecture → Approval → Activation 和同切片断言。隔离样本用于观察 Agent 分支判断、取证与停止条件。
- 若原入口已经足以承接某一情况，采用其行为证据。若完成当前义务所需的实际入口无法通过已声明合同定位，只补原 owner 的说明或路由承接。语义判断由原 owner 完成。

## 5. 接口与数据

API/数据形状保持。公共 TaskKey、DeliveryKey、ScopeRef、Planning root、阶段和结果按原 owner 查询。实际 `created` DTO 进入其唯一 consumer，使用有效 `source_selection` 进入 `delivery_initial_review`，已推进的切片从原阶段接续。Approval 的实际 `planning_result_id` 交 Activation。运行不依赖短期输入文件路径。

## 6. 状态、顺序、正常与失败流程

读取准确当前对象和已有结果。当前义务确需后续交付时，按实际 Task scope 创建后续切片。已选同一切片则根据现行阶段和适用前置进入 Author、Architecture、Approval、Activation 或验证。缺失或失效的必要结果返回其 producer。完成适用证据判断和配置补验后进入当前可交付步骤。进度描述读取到的实际阶段和剩余门禁。

## 7. 恢复、兼容、迁移与集成

恢复编排保留实际 key、规划正文及仍适用结果。后续 slice 引用前序而不覆盖前序。当前方案不调整公共合同，安装态若受说明修订影响则通过原 tools owner 同步对应投影。README、配置或公共契约仅在存在实际差额时维护，无 schema 或业务配置迁移。

## 8. 验证设计

- V1 使用隔离的已交付样本，从 Codex 与当前安装的 `trellis-continue` 取得前序、后续切片和实际接续。记录可观察的 owner/profile、重用和剩余义务。案例前序 GitHub 数据在隔离环境提供，原 Task/Delivery owner 调用来自实际安装。
- V2 核对当前接续公开入口及对应测试，保留后续候选采用前序提交、恢复后相同 key 和原规划字节。修复历史测试断言链后验证当前 Approval 与 Activation。组件的模拟评审证据范围止于 transport。
- V3 在样本确认 writer/index 证据仍适用后，验证目标模型容量、预留和两版本标识，以及五字段被样本配置加载路径读取。必须区分已通过的本地检查与待执行审核、合并或实际部署。本样本验证范围止于本地交付准备。
- V4 涉及受管说明差额时执行当前匹配安装与声明平台投影、sidecar/drift 定向检查。只有源码测试修复时验证包和安装态行为；分发没有增量即不重跑安装矩阵。

## 9. Canonical 引用、本轮差额与实际未决项

采用 `docs/design/current/task-delivery-lifecycle.md` 的续接和阶段 owner 定义、`docs/test/current/task-delivery-lifecycle.md` 的 T679、T792、T850-03、`docs/test/current/behavior-validation-method.md` 的 T747 和 `docs/architecture/README.md` 的职责边界。检测与配置演练的证据将由原 Test SSOT owner 承接。候选没有架构变化，不增加 ADR。若实测需要改变状态所有权或公共契约，暂停该改动并返回 Author 与 Architecture。
