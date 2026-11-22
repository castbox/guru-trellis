# #900 实施与验证计划

## 1. 输入与引用

从本批 [PRD](prd.md) 的 AC1/AC2 和[设计](design.md)的唯一来源设计处置执行。基线 B 为 `f06eddb6ccf97ddd2d1a41c117692f5957cb2dc7`。没有前序 Delivery。使用固定候选、原 Architecture 资格、实际发布条件及既有事务事实。

## 2. 有依赖顺序的步骤与文件责任

1. 在 `trellis/skills/guru-team/packages/guru-publish-task-delivery/` 整合语义准备合同与现有确定性 gate 和事务。将旧 readiness 的合法 rework、scope 命中和 payload 校验归入该 owner。以实际预览内容和动作绑定确认，按设计 §6–7 实现两种恢复。对记录 readiness 后丢失预览的调用，沿原 rework 重新执行一次准备。对尚未完成的事务，用同一引用回读原 preimage/postimage，再用当前 readiness 绑定待执行部分。
2. 在 canonical workflow、routing、registry、Review、Architecture、Publish、Merge interfaces 同步正常、失效、already MERGED、scope 和回程 consumers。沿现有公共 API 来回传递实际 key 和结果。同步 README、例子和 MIGRATION-900。完成退役入口的引用与注册清理。
3. 在定向测试中驱动真实 public wrappers、受控 Git/gh、受影响消费者和原事务 recovery。先覆盖 V1，再补 V2/V3 中有独立风险的分支。
4. 用原 `guru-upgrade-tools` 在匹配且隔离的安装边界同步声明平台、dogfood 和 managed spec。处理实际 sidecar 并检查更新后的收敛。待工程事实齐备，原 RDT/Architecture 做实际知识整合与读回。然后由原 TaskCommit 和独立 Branch Review 处理固定候选。

## 3. 验证入口、输入与预期观察

| ID | 可执行入口及观察 |
| --- | --- |
| V1 | 新 Publication 准备与执行 wrapper，在既有 Publication tests 的真实仓库/受控 gh 设施运行。检查 preview、确认边界、精确动作、远端 readback、PublicationFact 和 Merge 接收。 |
| V2 | 同一包装入口，用已审候选的合法依赖缺失、AI 未通过的 readiness 及正常远端变化。比对原 owner 回程、无新远端动作，以及具体重复预览。 |
| V3 | 定向运行 `guru-publish-task-delivery/tests/` 下受影响的 transaction、remote_recovery 和 migration 用例，及 `guru-merge-task-delivery/tests/test_manual_recovery.py` 中受影响的接续。新增新入口转接断言。分别截断正常调用于 readiness 落盘后且事务建立前，以及事务已经完成 push 或绑定 PR 但仍有后续动作时。前者验证同一 key 的合法退回和一次新的 readiness，确认前远端保持原状态。后者验证实质预览变化触发新确认，保留同 PR 与已完成动作，仅执行重新确认的待执行动作。 |
| V4 | 运行 `.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source` 及 installed 模式和 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。检查实际 reapply、Task/session 状态和 sidecar。受控 Agent 通过正常入口完成一次实际判断和预览。完整安装矩阵由专门任务承担。 |

运行仓库质量规范的定向语法、public graph、Task 校验及 diff 检查。所列均为计划验证。生产采用及本 Task 实际 GitHub 交付由后续有权限的流程记录。

## 4. 停止条件与适用回退点

缺候选、Architecture 资格、同一事务或来源证据时回其原职责。计划外机制、兼容或 owner 变化先暂停受影响写入并重新评估。真实冲突与需要结合新基线的依赖交原 Reconcile。保留已存在的 PR、已经完成的远端事实和原恢复入口。

验证设施无法到达目标路径时报告缺口。只有实际独立覆盖足以支撑 AC1/AC2 才停止补测。已获确认的操作按同一事务恢复。发布预览实质变化时取得新的确认。

## 5. Delivery Policy

`full`。本切片实现并验证 #900 的 AC1 和 AC2，无后继工程切片。合并后由 Completion 核对整个 Task 范围及最终证据，再按原 Closure、Finish 处理来源和归档。

## 6. Docs SSOT Plan

`delta_first`。原 RDT owner 维护 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 的完整命中条款与必要关系，保留历史记录。原 Architecture owner 用隔离贡献和 ADR 候选更新 ARCH-DOM-017、ARCH-CUR-075 及实际命中的 GOV、INTEGRATION 条款。两 owner 在工程自检后按 live target 和 expected-current 整合并读回。精确 TaskCommit 包含全部实际结果，由独立 Branch Review 核对进入准备入口及其消费者。
