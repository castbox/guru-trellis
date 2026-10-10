# #468 Traceability

状态：`candidate`；current inheritance：`current-main-0.6.17-guru.80 / active`。不改变 shared current。

| Requirement / behavior | Design responsibility | Validation / source scenarios |
| --- | --- | --- |
| R468-01 / BEH468-SOURCE | D468-01 | T468-01 / SC468-SOURCE：1/2/11/15；portable source、信息链接、执行仓库和 source 仓库分离。dispositions 与 no-Issue 另见 T468-04。 |
| R468-02 / BEH468-DEPENDENCY | D468-01 | T468-02 / SC468-DEPENDENCY：3..10；current Direct Source、必要依赖/证据、信息/Follow-up、earliest-owner 与原 Completion 回程。原 #464 BEH-464-CHECK/RECOVERY 继承，不重设计。 |
| R468-03 / BEH468-REPLAN | D468-02/03 | T468-03 / SC468-REPLAN：16；首次/活动/真实输出丢失区分、same TaskId/generation、零重复 status mutation、current producer/continuation、Phase2 retirement。 |
| R468-04 / BEH468-LIFECYCLE | D468-01/04 | T468-01/04 / SC468-LIFECYCLE：12/13/14；no-Issue/no-close、active/unfinished/finished 分流与 current repository 适用 SSOT。 |
| R468-05 / BEH468-DISTRIBUTION | D468-04 | T468-05 / SC468-DISTRIBUTION：canonical/installed/platform、reapply/drift/sidecar/mode、task/hygiene；不承接完整 Release 矩阵。 |

[Requirement](./requirement.md)拥有本任务增量与来源，[Design](./design.md)拥有职责引用，[Test](./test.md)独占实际 pass/fail、首次失败和未验证边界。Architecture inheritance 与 task-owned贡献由 [Architecture current entry](../../architecture/README.md)及 [candidate contribution](../../architecture/contributions/468-direct-source-replanning-compatibility.md)承接，不从 test pass 推导 promotion、完整架构 gate 或任务完成。
