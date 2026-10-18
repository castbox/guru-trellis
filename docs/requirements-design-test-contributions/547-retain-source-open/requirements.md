# #547 Requirements 增量

来源：[Issue #547](https://github.com/castbox/guru-trellis/issues/547) 当前目标、范围与 AC1..7；前驱是 RDT `.90/active` 的 R531-06、#436 收尾能力。Architecture 继承 `.87/active`。本增量由原 RDT owner reconciliation；source prose不复制。

| Requirement / behavior | 本版增量目标 |
| --- | --- |
| R547-01 / BEH547-SCOPE | 同 TaskId/generation/exact_source 正常 scope 修订后的 whole-task Completion |
| R547-02 / BEH547-DISPOSITION | 来源资格与本次保留 OPEN 的处置分开 |
| R547-03 / BEH547-RESULT | 零 close 的有效 no_mutation ResultRef 接续 Finish |
| R547-04 / BEH547-ARCHIVE | 归档 scope、交付历史与未验证界限，Cleanup 独立 |
| R547-05 / BEH547-COMPLETION | 当前必要工作或证据不足仍回原 Completion owner |
| R547-06 / BEH547-PROJECTION | 旧动作、blocked 原因与多 Issue 源事实投影保持正确 |
| R547-07 / BEH547-RECOVERY | 输出丢失复用原结果，正常状态漂移回原处置 owner |
| R547-08 / BEH547-ADOPTION | additive enum 与 matching consumer；受控采用和真实旧安装分开 |

原 CMS 现场恢复、联调/产品 #59 联合验收、业务升级和完整 Release 矩阵不属于本增量；其 OPEN 责任不能被受控绿色证明抹除。#548 不承接于本 Task。
