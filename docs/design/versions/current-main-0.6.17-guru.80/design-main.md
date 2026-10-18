# #383 因果完成语义与阶段承接

版本：`current-main-0.6.17-guru.80`；状态：`active`；predecessor：`current-main-0.6.17-guru.79`。薄继承[不可变前驱](../current-main-0.6.17-guru.79/design-main.md)全部有效合同及原对象证据。本版承接已独立审查的 #383 增量；Architecture 当前继承 `docs/architecture/README.md` / `current-main-0.6.17-guru.80` / `active`，晋升 preimage 为 `.79`。知识晋升不表示软件发布、业务生产根因修复或任务完成；晋升产生的差异须 fresh Phase 2、Task Commit 与独立完整 Branch Review。

[设计增量](../../../requirements-design-test-contributions/383-causal-completion-semantics/design.md)拥有 D383-01..04。单一 canonical causal spec 服务七个现有 owner；stage-local contract 拥有本阶段证据与路由，runtime 仅确定性校验和投影。原 Check 对已选 reapprove_plan 承接 current_scope proposal refs，公开 I/O/schema/exit 不变。
