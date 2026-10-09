# #464 正常修订与恢复需求贡献

`REQ-464-LOCAL` 的唯一源为 [Issue #464](https://github.com/castbox/guru-trellis/issues/464)，accepted contract `2026-10-09-r11`。本贡献继承 `current-main-0.6.17-guru.77 / active`，不替代 shared current。

行为 `BEH-464-CHECK`：当前 Check owner 完整语义复核时，只重跑实际依赖改变或事实不可用的检查，并为当前候选绑定结果。行为 `BEH-464-RECOVERY`：Delivery 局部输出丢失保留仍适用的 checked Branch Review anchor；缺失结果回原 owner，新 committed content 完整审查。

其余验收使用既有 identity、Reconcile、Task Commit、Publish、Completion 与 continuation owners；不改变公开 I/O、候选一致性算法或生命周期定义。13项映射见 [traceability.md](./traceability.md)，实际证据及未验证边界只由 [test.md](./test.md)拥有。
