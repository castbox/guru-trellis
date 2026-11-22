# #908 requirements 拟写

状态：integrated_pending_review。完整拟写见 `proposed/docs/requirements/current/task-delivery-lifecycle.md`，其相对引用按最终 current 位置解析。适用前驱为 Git `2acab7fadebf57c2f2560451b9ff2a050d8811f5` 的 `docs/requirements/current/task-delivery-lifecycle.md`。

差额只同步已经生效的 R900 行为：独立完整 Review 通过后由 `guru-publication-entry-router` 获取发布 Architecture 资格，再由 `guru-publish-task-delivery` 判断 readiness、形成预览并执行发布。原 R531、R636、R637、R794、R856、R899、R900 的未替代条件、历史身份、Refs-only、Closure、Merge 和整体 Completion 责任保持。

本拟写不改变产品要求、公共 Skill、profile、schema、typed exit 或状态机；它仅修正 current 正文中仍使用已退役独立 Delivery Review 名称的过期表述。

原 RDT owner 已在工程验证后把完整拟写整合到 current 并逐字节读回；尚未发生独立 committed Review。
