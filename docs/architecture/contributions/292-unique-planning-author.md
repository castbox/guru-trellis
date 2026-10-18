# 唯一 Planning writer contribution

Identity：`architecture-contribution-292-unique-planning-author-v1`；状态：`reviewed_promoted`；predecessor：`current-main-0.6.17-guru.84`；successor：`current-main-0.6.17-guru.85`。来源：[Issue #292](https://github.com/castbox/guru-trellis/issues/292) 的 r27 与 Task `292-unique-planning-author` / generation0 的 design D9/D10；源设计 content identity 为 `sha256:b418acf6f38419717ca9d0cb126dc748ed74c7373afc419674bf79cbd89d1b50`。本文件是已晋升责任与决策的 durable locator，不依赖 active Task 路径长期存在。

## Boundary and decisions

原 Planning 已拥有最终设计处置，但未命名 writer；Architecture 的单一 Planning 输入要求先有 contribution，且只回 Approval；活动 Clarify 与 writer 的前置要求形成先写后判断的循环。当前由 `guru-author-task-plan` 独占规划语义写作及 revision，Clarify/Discovery/Architecture/Wording/Approval 保留各自判断。脚本仅执行确定性 schema、identity、projection 与事实动作，不能替代上述判断。

`target_native` 直接演进当前受控消费者。Architecture planning3.0 的 candidate_assessment 对真实候选进行前置评估，回 Author solution_planning，不要求未来 contribution；final_plan 审 Wording-current design、真实 contribution/必要 ADR，回相邻 Approval。两目的归原 Architecture owner，非 Planning/maintenance2.0 与 project descriptor/result2.0 保持。旧无 purpose Planning2.0 入口退出 runtime，中断调用 fresh Author 重入；不保留 dual reader、第二评估 owner 或长期缓存。

Clarify scope_ready1.0 先完成 scope/来源判断，再经原 clear-router 的独立 consumer1.0 将最小 current refs 投影给同一 Author。Clarify 不写 planning、hash、生命周期或授权状态。旧 private3/clear3/consumer2 保留 pinned 字节但不转换旧成功结果为新 pass；其它 profiles 与正常 context refresh 回程保持。必要决策分别归 [ADR-022](../adr/022-unique-planning-author.md) 与 [ADR-023](../adr/023-scope-ready-before-planning.md)。

Author 的八 profiles/四 exits 对应当前初稿、方案、Wording/Approval revision、Delivery/Completion revision、活动 scope、Architecture conflict 与创建恢复 consumers。前置 normal/solution/root 资格使用当前候选，不要求未来三份文档；Approval 保留独立规划资格。Wording refs、Approval actions 和两种 Delivery/Completion 原因经薄 projection 回同一 writer；原 execution owner 承接批准后的 activate/resume。TaskId、generation、正式 Task writer、source/Closure、Delivery/Completion 与 promotion owners 不变。

## Applicable concerns and convergence

九 concerns 全部适用：authority/constitution 绑定唯一 current 与上述 planning3.0/非 planning2.0 区分；boundary/decision 和 owner/single-writer 由当前具名职责与 ADR-022/023 承接；compatibility/exit 是 matching workflow/preset 的 current-only migration；GAP/deviation 继承 closed ARCH-GAP-006/008/012，不改其生命周期；parallel scope 不允许任务竞争 shared current；evidence/freshness 绑定当前候选和原范围；review/promotion 按原 expected-current single-writer 顺序执行。

Project check 沿 `guru-trellis-architecture-convergence:repository:1` / `guru-trellis-architecture-convergence@1`，使用原 ARCH-GOV-006..009、ADR-005/009 与 ARCH-GAP-006/008。责任与迁移适用性见本文件及 ADR；实际测试、native、安装层次、历史失败与未验证边界仅由[唯一 Test](../../requirements-design-test-contributions/292-unique-planning-author/test.md)拥有。本 contribution 不引入审查流水账或第二 Test authority。

晋升修改共享 authority 后，完整新差异仍须 fresh Phase2、Task Commit 与独立完整 committed Branch Review；此前实现审查不能替代。constitution、软件版本轴与 GAP lifecycle 保持；完整多平台矩阵、软件 Release 与业务安装/部署不因此获得证明。
