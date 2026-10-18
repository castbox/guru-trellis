# #331 设计差额与责任

状态：`promoted_source`。完整当前设计由三份 [lifecycle](../../design/current/task-delivery-lifecycle.md)、[completion](../../design/current/completion-closure.md)、[knowledge](../../design/current/knowledge-maintenance.md) 拥有；本贡献定位差额，不再复制正文。前驱 RDT `.109` 和 Architecture `.100` 适用本迁移比较，晋升关系由本目录 manifest 拥有，执行证据仍以唯一 Test 为准。

| Responsibility / contract | 唯一责任与实际落点 | Requirement / test |
| --- | --- | --- |
| D331-01 / CON331-01 | 原RDT package的current-knowledge合同；三层完整current单元和只含identity/status/locator/关系的导航；接口继续canonical单写。 | R331-01/04 → T331-01/04/05 |
| D331-02 / CON331-02 | 原task_impact_sync/promotion/repair处理R/D/T/Architecture关联与稳定身份；独立Task contribution；完整目标及前后继关系。 | R331-02 → T331-02/03/05 |
| D331-03 / CON331-03 | 原Architecture owner分别在generic版本源与project stack-selection边界维护；project只拥有选择/约束/差异，公开引用不复制正文。 | R331-03 → T331-04/05 |
| D331-04 / CON331-04 | 原Phase2独立before/after、串行expected-current晋升、实际写入适用性、最终Check/commit/committed Review；旧Task阶段适用性与工程事实采用保持。 | R331-01/02/04 → T331-01/03/05 |
| D331-05 / CON331-05 | 显式migration inventory/切换恢复/legacy退出；canonical/dogfood/installed及匹配更新/reapply无漂移；不改旧snapshot。 | R331-05 → T331-03/04/05/06 |
| D331-06 / CON331-06 | Test owner冻结对照，脚本只采真实events/bytes/usage/paths，AI逐次判完整性；临时raw trace与唯一长期Test结果分开。 | R331-06 → T331-01..06 |

原四profiles和public DTO/exit/schema保持。只有原owners可晋升共享README；candidate正文与本贡献不独立生效。实际Architecture contribution是 [331-current-effective-knowledge](../../architecture/contributions/331-current-effective-knowledge.md)，项目治理和ADR决定由Architecture authority拥有，不由本RDT复制。

迁移前后内容、稳定trace及被窄替代执行片段见 [traceability](./traceability.md)。唯一实际结果和未验证边界见 [test](./test.md)，不将写出目录或文档作为行为完成证据。
