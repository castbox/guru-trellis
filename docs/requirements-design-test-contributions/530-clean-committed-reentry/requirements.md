# #530 增量需求

状态：implementation_candidate；Direct Source：[Guru #530](https://github.com/castbox/guru-trellis/issues/530)。原 TaskId `issue-530-clean-committed-reentry` / generation 0。此增量尚未晋升共享 authority。

| Requirement / behavior | 必须行为 |
| --- | --- |
| R530-01 / BEH530-CONTINUE | post_commit Reconcile、fresh Phase 2、unchanged post_check 后，无待提交增量的正式候选能够进入首次独立完整 Branch Review。 |
| R530-02 / BEH530-IDENTITY | 原 owner 从当前 Task、HEAD、selected base 和 Check 事实正式投影现有 Branch Review 输入，不复用整合前 commit。 |
| R530-03 / BEH530-READONLY | 接续不制造空提交、相同内容提交或 tracked 推进文件；只读核验已有候选。 |
| R530-04 / BEH530-RECOVER | 真实增量仍执行原 exact commit；base 再演进和正常 stale 经原 owners 恢复，不携带旧证据。 |
| R530-05 / BEH530-FULLREVIEW | fresh Phase 2、fresh Branch Architecture 和首次独立完整 Branch Review 均必需，finding-fix/fresh-final intent 保持。 |
| R530-06 / BEH530-DISTRIBUTE | 同步 canonical/runtime/schema/consumer/平台投影，并运行正常链路和定向安装回归。 |

[设计](design.md)、[测试结果](test.md)、[双向 trace](traceability.md)分别拥有对应层。Backend #444、安装目标、软件发布和完整多平台矩阵保留独立边界。
