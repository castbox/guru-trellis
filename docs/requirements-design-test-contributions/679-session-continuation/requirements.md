# #679 需求增量

来源为 [live Issue #679](https://github.com/castbox/guru-trellis/issues/679) 的 R1–R4 和 AC1–AC6。整体当前范围由本 Task 根 PRD 承载；此贡献维护 repository RDT，不替代 Planning、Check 或 Completion。

固定前驱为 `e6c3b8276d62ac174ab42cba5bca4d5784be2ca3`。完整拟写定义见 [requirements proposed target](proposed/docs/requirements/current/task-delivery-lifecycle.md)，目标为 `docs/requirements/current/task-delivery-lifecycle.md`，保持 RDT-REQ-LIFECYCLE identity。该 proposed 正文的相对引用按目标文件位置解释。

- R679-01 / BEH679-RECEIVE：明确接收者自己的缺绑定/缺选择，由原 owners 补缺并继续原未完义务。
- R679-02 / BEH679-FIRST-FAILURE：区分真实 current 状态与失配，保首失败及原 owner，不减校验。
- R679-03 / BEH679-STANDALONE：真实 producer 身份和 mode 投影，合法不同 caller_locator，普通错误后完整重建 consumer。
- R679-04 / BEH679-ARTIFACTS：真实 key 展示、Task-only 根 PRD 和实际 archive ref/key。

R531/R657 的公共模型、现有原 writer、no-context 边界、阶段及门禁责任保持。#666 通用停顿、业务仓/生产、完整 Release/Upgrade 矩阵不进入本贡献。历史 #548/#443/#396 的实际观察保持原意；新增证据不追溯改写旧结论。
