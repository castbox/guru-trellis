# #578 design-main

版本：`current-main-0.6.17-guru.101`；状态：`active`；predecessor：`current-main-0.6.17-guru.100`。完整继承[不可变前驱](../current-main-0.6.17-guru.100/design-main.md)的有效合同；[#578 唯一增量](../../../requirements-design-test-contributions/578-cross-owner-validation-facts/traceability.md)连接 R578-01..05 / BEH578-01..05 / D578-01..03 / T578-01..04。需求、机制与实际结果分别由该根 requirements.md、design.md、test.md 单写，不复制历史正文。

继承 Architecture `current-main-0.6.17-guru.94/active` 与 ADR-029；只窄替代 #464 same-owner-only 和 ADR-019 无条件本人命令重跑的冲突解释，保留当前完整独立判断、真实依赖适用性、来源说明、当前绑定、typed routes 与 private checkpoint 退休。#575 S1 及其余前驱有效合同保持；不因本晋升改变软件版本或完成来源采用后续阶段。

首次独立完整 committed Review 为 `404d3f4d7635b19fb2c9f0d6aa642e2f1bf925b4...5ba72ba9ca40d990d8250fbc0c174475bc3d98f4`。[唯一 Test](../../../requirements-design-test-contributions/578-cross-owner-validation-facts/test.md)保留真实命令、失败/skip/incomplete和未验证边界；晋升新差额仍须 fresh Phase2/TaskCommit/不同 reviewer 完整 BranchReview。不证明 Delivery/Completion、Release/Upgrade矩阵、source-lock精确安装或业务采用。
