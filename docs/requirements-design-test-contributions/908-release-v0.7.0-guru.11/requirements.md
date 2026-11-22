# #908 requirements 拟写

状态：integrated_pending_review。独立 committed Review 尚未发生，本状态不表示质量通过。适用前驱为 Git `2acab7fadebf57c2f2560451b9ff2a050d8811f5` 的 requirements current units。

Architecture assessment 为 `baseline_current / architecture_impact`，change path 为 `target_native`。Task-owned Architecture relation 见 [908 Architecture contribution](../../architecture/contributions/908-release-v0.7.0-guru.11.md)，决定 authority 为 [ADR-POSTCOMMIT-INDEPENDENT-REVIEW](../../architecture/adr/postcommit-independent-review.md)。Architecture current targets 已写入并 readback；独立 committed Review 仍待执行。

本贡献的所有实际 requirements current targets 及其完整 after 如下：

- [task-delivery-lifecycle](proposed/docs/requirements/current/task-delivery-lifecycle.md) -> [current](../../requirements/current/task-delivery-lifecycle.md)
- [knowledge-maintenance](proposed/docs/requirements/current/knowledge-maintenance.md) -> [current](../../requirements/current/knowledge-maintenance.md)
- [completion-closure](proposed/docs/requirements/current/completion-closure.md) -> [current](../../requirements/current/completion-closure.md)

差额只同步已经生效的 R900 行为：独立完整 Review 通过后由 `guru-publication-entry-router` 获取发布 Architecture 资格，再由 `guru-publish-task-delivery` 判断 readiness、形成预览并执行发布。Requirements 当前正文同时把 knowledge maintenance 与 Completion 的旧 Delivery Review 阶段名改为 Publication readiness/execute；原 R531、R636、R637、R794、R856、R899、R900 的未替代条件、历史身份、Refs-only、Closure、Merge 和整体 Completion 责任保持。

本拟写不新增产品要求、公共 Skill、profile、schema、typed exit 或状态机。原 RDT owner 已在工程验证后把上述完整 after 整合到 current、逐文件读回并核对字节；独立 committed Review 尚未发生。
