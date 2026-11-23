# #908 追踪与整合边界

原完整来源为 Git `2acab7fadebf57c2f2560451b9ff2a050d8811f5` 的 RDT/Test current units。原 owner 为 `guru-maintain-requirements-design-test-ssot`，authority identity 为 `guru-trellis-rdt`，状态 active。当前整合状态为 `integrated_pending_review`；独立 committed Review 尚未发生。

Architecture assessment 为 `baseline_current / architecture_impact`，change path 为 `target_native`。Task-owned relation 为 [908 Architecture contribution](../../architecture/contributions/908-release-v0.7.0-guru.11.md)，decision authority 为 [ADR-POSTCOMMIT-INDEPENDENT-REVIEW](../../architecture/adr/postcommit-independent-review.md)。该 contribution 覆盖七个 Architecture current units、11 个 necessary consumers 和 ADR promotion；本 RDT 贡献继承其 authority，不复制 Architecture 正文。

| 当前行为 | 要求 | 设计责任 | 验证 |
| --- | --- | --- | --- |
| Publication preparation 链 | R531-05、R636-04/05、R794-05、R900-01/02 | D531-05、D636-04/05、D794-02、D900-01/02 | T531、T636-05、T794-01/02、T900-01/02 |
| 子切片成果与 readiness | R649-03、R657-04、R713-05 | D649-02、D679、D713-05 | T649-02、T657-06、T713-03 |
| 旧 Draft、same-PR 和已合并恢复 | R636、R635-03、R637-06、R794-06 | D636-02、D635-03、D637、D794-04 | T636-02/07、T635-03、T637-06、T794-04 |

R856 的错误边界、R899 的续接读取和 R900 的完整发布入口保持 current。RDT 与 Architecture 使用同一 `architecture_impact / target_native` relation：RDT 维护 Requirements/Design/Test 完整 current after，Architecture owner 维护 current units 与 ADR accepted 状态。两者都只表示实际写入/readback，不表示 independent Review 通过。

## RDT/Test targets

以下九份完整 proposed after 均与对应 current bytes 一致：

| Layer | Complete proposed after | Current target |
| --- | --- | --- |
| Requirements | [task-delivery-lifecycle](proposed/docs/requirements/current/task-delivery-lifecycle.md) | [current](../../requirements/current/task-delivery-lifecycle.md) |
| Requirements | [knowledge-maintenance](proposed/docs/requirements/current/knowledge-maintenance.md) | [current](../../requirements/current/knowledge-maintenance.md) |
| Requirements | [completion-closure](proposed/docs/requirements/current/completion-closure.md) | [current](../../requirements/current/completion-closure.md) |
| Design | [task-delivery-lifecycle](proposed/docs/design/current/task-delivery-lifecycle.md) | [current](../../design/current/task-delivery-lifecycle.md) |
| Design | [knowledge-maintenance](proposed/docs/design/current/knowledge-maintenance.md) | [current](../../design/current/knowledge-maintenance.md) |
| Design | [completion-closure](proposed/docs/design/current/completion-closure.md) | [current](../../design/current/completion-closure.md) |
| Test | [task-delivery-lifecycle](proposed/docs/test/current/task-delivery-lifecycle.md) | [current](../../test/current/task-delivery-lifecycle.md) |
| Test | [completion-closure](proposed/docs/test/current/completion-closure.md) | [current](../../test/current/completion-closure.md) |
| Test | [runtime-location](proposed/docs/test/current/runtime-location.md) | [current](../../test/current/runtime-location.md) |

Planning 批准且工程验证完成后，原 RDT owner 重读 live current、完整 proposed、实际实施结果和必要关系，将完整 after 写入 current、逐文件 readback，并记录 `integrated_pending_review`。当前 private release regression 11/11、upgrade installation contract 35/35、source/platform validators 和 focused Codex 来源样本均通过。随后 TaskCommit 纳入实际 after，固定 committed candidate 的独立 Review 审核真实 before/after。本文不预先声明 Review、Publication、Release 或 Task Completion 通过。
