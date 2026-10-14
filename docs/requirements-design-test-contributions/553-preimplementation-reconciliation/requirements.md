# #553 实施前基线整合增量

来源：[Issue #553](https://github.com/castbox/guru-trellis/issues/553)，当前accepted验收1-7。前驱R531的Task/Delivery身份与R530的实施后接续责任保持。状态：candidate；未晋升shared current。

| Requirement / behavior | 必须观察的行为 |
| --- | --- |
| R553-01 / BEH553-PREPLAN | 已批准同Delivery规划修订后，合法基线文档冲突经原Reconcile审查并精确整合，原Activation恢复实施；不要求未实施业务Check |
| R553-02 / BEH553-EVIDENCE | 基线验证与完整业务Phase2分离，不创建Check/TaskCommit/BranchReview/Delivery批准 |
| R553-03 / BEH553-IDENTITY | TaskId/gen/DeliveryKey与规划、原consumer保持；base-only推进不自动扩大scope或全链重规划 |
| R553-04 / BEH553-PENDING | 只commit受审integration tree；无关staged/unstaged/untracked及并行内容保持 |
| R553-05 / BEH553-FRESH | actual HEAD/base/MERGE_HEAD、resolved entries、tree和父序绑定；普通stale/mismatch/unresolved及真实authority变化返回原owner |
| R553-06 / BEH553-RECOVERY | 同操作结果丢失恢复原commit，不duplicate；既有实施后resolved和无冲突路径保持 |
| R553-07 / BEH553-DISTRIBUTION | canonical与适用完整managed投影一致，定向runtime/installed接续/reapply/drift分层验证，未验证边界明确 |

不改backend #148或其它业务资源，不改上游/全局/node_modules，不增加攻击、锁/TOCTOU或完整Release矩阵。原业务手动恢复只作历史来源，不作当前闭环证据。
