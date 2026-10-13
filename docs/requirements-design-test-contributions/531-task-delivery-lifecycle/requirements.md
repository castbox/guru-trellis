# #531 需求增量

状态：draft，未晋升 shared current。来源是 [Issue #531](https://github.com/castbox/guru-trellis/issues/531)
当前 accepted scope；继承 RDT current-main-0.6.17-guru.89 / active，
Architecture current-main-0.6.17-guru.86 / active。

| Requirement / behavior | 需求差额 |
| --- | --- |
| R531-01 / BEH531-OWNERS | Task 保留整体责任；所有 Delivery 包括 D1 独立规划和生命周期；公共状态唯一归上游 |
| R531-02 / BEH531-PLAN | 每次首次 Planning 前建立稳定 identity；D2 不覆盖 D1；唯一 Author 和独立语义 gates 保留 |
| R531-03 / BEH531-REWORK | 同 Delivery 返工，整体 authority 先修订；全撤回合法停止/unbind，退出不冒充交付 |
| R531-04 / BEH531-CANDIDATE | dirty 精确提交；clean 既有候选 fresh Check 后完整 Review，零重复提交 |
| R531-05 / BEH531-FACT | 原事务恢复真实远端成功后投影，零重复副作用；历史事实不等于当前 gate pass |
| R531-06 / BEH531-COMPLETION | 整体 Completion、Closure、Finish、Cleanup、Reactivate 独立；证据或收尾无需空 Delivery |
| R531-07 / BEH531-MIGRATION | 公共/私有迁移分 owner，支持组合应用前诊断，canonical/installed/native/reapply 一致 |
| R531-08 / BEH531-DEPENDENCY | 局部 provider 缺口只阻塞真实依赖；独立必要 consumer 继续，不接管 provider |

旧 #468 能力由 R531-02/03 迁移并退役 Task 激活分叉；#530 clean 接续由 R531-04
承接；#292 的九 profiles/五 exits 唯一 Author 已交付，本 Issue 按整体 scope-only
与八 Delivery profiles 显式迁移，不建立第二 Author。#530 的实际 public Check
适用性与 stable committed identity 已交付；旧 Phase2 capture 不成为新的 authority。
不承接业务实现、部署、完整 Release 矩阵或原业务树自动恢复。
