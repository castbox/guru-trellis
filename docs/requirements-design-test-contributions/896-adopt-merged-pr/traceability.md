# #896 关系

来源为 [Issue #896](https://github.com/castbox/guru-trellis/issues/896) 的「行为要求」与「验收」。架构决定见 [ADR-026](../../architecture/adr/026-manual-merged-delivery-recovery.md)。当前定义位于需求、设计、测试各自的 Task 与 Delivery 生命周期单元。

| 当前要求 | 设计职责 | 验证 |
| --- | --- | --- |
| R896-01 / BEH896-ADOPT | D896-01 | T896-01、T896-02 |
| R896-02 / BEH896-CLOSEOUT | D896-02 | T896-01、T896-02 |
| R896-03 / BEH896-REENTRY | D896-01、D896-02 | T896-03、T896-04 |
