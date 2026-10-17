# GOVERNANCE

- `ARCH-GOV-001`：Architecture 变化按 `bootstrap_foundation`、`task_impact_sync`、`promotion` 或 `repair` 进入唯一 semantic owner。
- `ARCH-GOV-002`：CURRENT 条目必须有 current code/config/test/release evidence；`inferred`/`unverified` 不能晋升为 CURRENT。
- `ARCH-GOV-003`：每次 gate 读取 live authority，由原语义 owner 选择并重读明确阶段适用的 locator/version/status 与真实 task delta。无关整体 CURRENT/ref/version 前进不改变已选适用性；真实立即适用规则变化须明确对象和承接要求并回原 owner。unknown/multiple/真正 stale exit 继续 fail closed；ADR-028 定义本条的适用边界。
- `ARCH-GOV-004`：Architecture/RDT/projection 三者 locator 与 traceability 必须一致；projection 只能包含读取规则、identity 与 freshness。
- `ARCH-GOV-005`：普通并行 task 使用隔离 contribution，不共同写 shared current；这是 ownership 规则，不引入锁、TOCTOU 或共享协调状态。
- `ARCH-GOV-006`：每个标准 task mandatory 进入 Architecture semantic owner；`architecture_impact` 恰好选择 `target_native`、`legacy_boundary_convergence` 或 `dedicated_refactor_slice`，`no_architecture_impact` 只返回 current identity 与可审核理由。
- `ARCH-GOV-007`：Guru public identity 与项目 baseline/change-contract identity 只在 task-local Architecture change contract 相交。明确阶段适用的 concern、owner、GAP、before/after、project check、evidence、review 或 freshness 缺失、过期或冲突时 fail closed。digest/ref 只服务本地事实一致性；无关整体版本推进不代替适用性判断，也不使旧 pass 自动适用于真实新候选。
- `ARCH-GOV-008`：普通 task 只写 task-owned contribution；shared current 仅由 Architecture owner 在 independent committed-diff review 后按 expected current identity 串行 promotion。该写操作的 live current 与 expected-current 错配由原 promotion owner 返回 `sync_required` 并处理实际差额，不扩大为全部在途 task 的开发资格。真实 promotion diff 必须重新通过 Phase 2、task commit 与独立完整 Branch Review；未晋升贡献仍不能进入 Publication/Finish。
- `ARCH-GOV-009`：Issue reference 与 closure intent 由 Publication 唯一语义判断；Finalizer保留current push/PR/archive/Ready/handoff/recovery但不重判closure，GitHub按进入默认分支的closing keyword执行关闭。Merge 保留原四个操作/恢复出口与独立 readiness/expected-head/live result 验证，并增加只读 `review_refresh_required`，完整出口集合以 current Interface 为准。新增只读复审不改变任何关闭责任。no-Issue不制造Issue identity，reference-only与non-default-base路径绑定current authority，其它owner不得补偿调用Issue close API。
- `ARCH-GOV-010`：active-task continuation先消费current adjacent DTO；output丢失时回最近合法原owner。任何status、Git shape、旧摘要、旧确认或retired checkpoint都不能重建semantic pass。确认仅存在于当前对话，新的副作用或authority变化必须重新展示。
- `ARCH-GOV-011`：一个active task可以产生多个独立Delivery；每次Delivery只使用`Refs`并在merge后保持task active。`delivered`唯一交给#436 Completion，不得表达或触发task completion、Issue closure、archive、Finish、Cleanup或Reactivate。#435只建立additive packages，#434之前不得形成第二个active production graph或兼容adapter。

完整项目 change contract 与 project-check descriptor 见 [`change-contract.md`](./change-contract.md)。

## #600 晋升时机后继

[ADR-030](../adr/030-promotion-before-final-check.md)替代本文件及继承 authority 中“完整 committed Review 后例行晋升并重做完整 Review”的顺序片段。最终 Check 前完成受审分支晋升；不为补最终 Review pass 或最终 SHA 循环写正文。原 authority、独立性、finding lifecycle 和最终正式结果要求保持。实际完成状态只按当前事实与[唯一 Test](../../requirements-design-test-contributions/600-promotion-before-check/test.md)读取。
