# D2 需求、设计与测试隔离提案

本提案对应 #747 的 D2，Task `747-user-journey-method` generation 0，Delivery `e8681e3c-8935-499e-9183-fd249710b846`。当前适用的 RDT 和 Architecture 前像以固定开发基线 `e74a4b0d9d5bc8ad29d00c41839a703ba6380aef` 定位。PR #888 的 main 合并提交 `37f3d29c76ef5fe2a35597e38661c37f38b2df9f` 含相同的目标前像。D2 已接受 `delta_first`。

| 验收关系 | Requirement | Design | Test |
| --- | --- | --- | --- |
| 最小完整旅程优先与单入口裁剪 | R747-D2-01 | D747-D2-01 | T747-D2-01 |
| 真实入口、替身、样本与独立审核 | R747-D2-02 | D747-D2-02 | T747-D2-02 |
| 受影响分发和实际本地采用 | R747-D2-01、R747-D2-02 | D747-D2-01、D747-D2-02 | T747-D2-03 |

本目录中的三份正文是现有 `behavior-validation-method.md` 各层目标的完整拟稿。链接按最终目标解析。原 RDT owner 在本批工程验证后对照真实目标整合并回读。提交后的独立 Review 核对实际前后内容。V2 至 V6 的执行记录由原实施和审核负责人承接。
