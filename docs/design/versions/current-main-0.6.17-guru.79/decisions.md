# #382 目标感知根因候选资格

版本：`current-main-0.6.17-guru.79`；状态：`active`；predecessor：`current-main-0.6.17-guru.78`。薄继承[不可变前驱](../current-main-0.6.17-guru.78/decisions.md)全部有效合同及原对象证据。本版承接已独立审查的 #382 根因候选资格增量；Architecture 当前继承 `docs/architecture/README.md` / `current-main-0.6.17-guru.79` / `active`，晋升 preimage 为 `.78`。知识晋升不表示软件发布、业务故障修复或任务完成；晋升产生的差异须重新通过 fresh Phase 2、Task Commit 与独立完整 Branch Review。

[ADR-020](../../../architecture/adr/020-root-cause-qualification.md)记录独立根因候选 owner；ADR-019 的独立新评估与原 owner 下游 eligibility/promotion 合同继续有效。受控 consumers 同步演进，normal/solution 既有公开 API 保持，无新 compatibility adapter 或 completion SSOT。
