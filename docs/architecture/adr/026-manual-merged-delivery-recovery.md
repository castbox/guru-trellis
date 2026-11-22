# ADR-026：手动合并事实由原 Merge 归属

状态为 `accepted`，补充 ADR-024。#557 的首次独立完整 committed Review 范围为 `ccf67ff157dc006f236870049dda9cba0fafa73f...6bba4880362a2e0ff31b535809e4895b7fa1a84d`，原 Architecture owner 随 .90 晋升。#896 补充缺少 Publication 时的归属路径。

公开Task/Delivery模型是唯一身份authority。普通用户合并已有正式Delivery PR是正常外部事实，不保证Guru merge message、trailers、pre-merge gate或receipt存在。只以这些生成副产物识别结果，会丢失实际已发布/合入的正式Delivery。

## 合并归属与内容

原 Merge owner 根据公开 Task/Delivery 关系与真实 GitHub 和 Git 事实认定归属。两个入口均核对同仓 PR 的实际目标、head、双父合并和目标分支的第一父历史。合并提交的第二父须等于 PR head。归属不足、歧义或不匹配时，保留原 Delivery 状态。支持范围是普通双父合并。

- 有 Publication 时，`delivery_merged_recovery` 沿 #557 核对原 Task、generation、Delivery 和唯一 Publication 的关联。
- 缺少 Publication 时，`delivery_adopt_merged_pr` 处理用户明确选择的仓库、PR 与原 Task/Delivery。PR head 与合并树中的 Task、Delivery 和接受范围须与当前公开记录一致。相对实际共同基点，PR 须新增选定 Delivery，或改变其关系或相关规划证据。仅继承 Task 元数据时，归属不成立。首次记录使用原 Task 的登记 checkout。已归档 Task 可重读已存在的结果。

原 Merge owner 通过现有 `record_delivery(historical_success=true)` 记录实际交付。缺少 Publication 的入口按唯一共同基点到 PR head 的受支持路径构造 Candidate，沿用现有元数据排除规则。DeliveryFact 的 `merge_commit` 及其经核对的第一父提交固定实际合入范围。Merge 审查两段完整差异，并按实际 PR head 读取 CI。PR head 和实际合入内容可以不同。

## 验收与恢复

原 Completion 独立审核整体接受范围、实际合入内容和仍适用的验证证据。它将实际合入范围和适用的独立证据交给原 Architecture 验收资格入口。实际 CI 保留原状态。缺少必要证据时，沿原证据缺口路线继续。Completion 通过后，原 Closure 和 Finish 按现有职责收尾。Closure 遇到已关闭的源 Issue 时重新读取其状态。

输出丢失后，重入读取同一公开 DeliveryFact。新远端 Guru 合并继续沿用 expected-head、消息和 trailers 合同。

公开历史 query2 读取 DeliveryFact。既有 trailer schema 1/2 和 query1 保持各自的历史职责。旧完整安装的退出继续由原迁移 owner 负责。

#557 的实现、验证、兼容和未验证边界由原 RDT 贡献与 Test 承接。边界覆盖旧完整载体与新匹配安装。实际晋升依据见[已晋升贡献](../contributions/557-manual-merged-delivery-recovery.md)。

#896 使用完整匹配的 workflow 与 preset，沿用公开 Task2/API 1.0、DeliveryFact 和 Completion handoff。采用边界见 [MIGRATION-896](../../../trellis/presets/guru-team/MIGRATION-896.md)。隔离旅程、回归和实际 GitHub 读取见 [#896 验证记录](../../requirements-design-test-contributions/896-adopt-merged-pr/test.md)。
