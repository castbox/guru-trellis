# #908 test 拟写

状态：integrated_pending_review。完整拟写见 `proposed/docs/test/current/task-delivery-lifecycle.md`，其相对引用按最终 current 位置解析。适用前驱为 Git `2acab7fadebf57c2f2560451b9ff2a050d8811f5` 的 `docs/test/current/task-delivery-lifecycle.md`。

受影响场景 T531、T635、T636、T637、T794 和 T900 只更新当前 owner 和阶段措辞。必须保持：

- Branch Review `passed` 进入 `guru-publication-entry-router`；
- Publication 准备判断 readiness 并产出准确预览；
- 确认前无远端写入，确认后执行同一预览；
- 失效、部分完成和已合并恢复仍由原 owner 处理；
- Merge、Refs-only、Completion、Closure 和 Finish 责任不变。

本拟写不把文档更新当作测试通过。实际 source/package、private release regression、来源样本和正式分支审查分别提供工程证据。

原 RDT owner 已在 RDT promotion 中整合并读回三份 current 正文；该状态只表示 integrated_pending_review，独立 committed Review 仍未发生。
