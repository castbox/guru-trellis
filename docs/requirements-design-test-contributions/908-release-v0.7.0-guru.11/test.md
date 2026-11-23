# #908 test 拟写

状态：integrated_pending_review。独立 committed Review 尚未发生，本状态不表示测试或质量通过。适用前驱为 Git `2acab7fadebf57c2f2560451b9ff2a050d8811f5` 的 test current units。

Architecture assessment 为 `baseline_current / architecture_impact`，change path 为 `target_native`。验证关系引用 [908 Architecture contribution](../../architecture/contributions/908-release-v0.7.0-guru.11.md) 与 [ADR-POSTCOMMIT-INDEPENDENT-REVIEW](../../architecture/adr/postcommit-independent-review.md)。Verification 需观察 RDT proposed/current 字节一致、Architecture current relation、ADR accepted 状态和未审边界，不以字符串或文档存在替代独立 Review。

本贡献的所有实际 test current targets 及其完整 after 如下：

- [task-delivery-lifecycle](proposed/docs/test/current/task-delivery-lifecycle.md) -> [current](../../test/current/task-delivery-lifecycle.md)
- [completion-closure](proposed/docs/test/current/completion-closure.md) -> [current](../../test/current/completion-closure.md)
- [runtime-location](proposed/docs/test/current/runtime-location.md) -> [current](../../test/current/runtime-location.md)

受影响场景 T531、T635、T636、T637、T794 和 T900 只更新当前 owner 和阶段措辞。必须保持：

- Branch Review `passed` 进入 `guru-publication-entry-router`；
- Publication 准备判断 readiness 并产出准确预览；
- 确认前无远端写入，确认后执行同一预览；
- 失效、部分完成和已合并恢复仍由原 owner 处理；
- Merge、Refs-only、Completion、Closure 和 Finish 责任不变。

`T669-06` 只把未预填的当前阶段名改为 Publication readiness/result；`#813` 的 `runtime-location` 只同步当前阶段名并保留原观察截止、安装限制和未验证结论。`test/current/knowledge-maintenance.md` 复核后没有旧 current owner 命中，因此不进入本贡献 target 集。

本拟写不把文档更新当作测试通过。原 RDT owner 已在 RDT promotion 中整合并逐字节读回上述完整 current 正文；该状态只表示 integrated_pending_review，独立 committed Review 仍未发生。
