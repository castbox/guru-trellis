# GOVERNANCE

- `ARCH-GOV-001`：Architecture 变化按 `bootstrap_foundation`、`task_impact_sync`、`promotion` 或 `repair` 进入唯一 semantic owner。
- `ARCH-GOV-002`：CURRENT 条目必须有 current code/config/test/release evidence；`inferred`/`unverified` 不能晋升为 CURRENT。
- `ARCH-GOV-003`：每次 gate 重读 live authority、locator/version/status 与 task delta；unknown/multiple/stale exit fail closed。
- `ARCH-GOV-004`：Architecture/RDT/projection 三者 locator 与 traceability 必须一致；projection 只能包含读取规则、identity 与 freshness。
- `ARCH-GOV-005`：普通并行 task 使用隔离 contribution，不共同写 shared current；这是 ownership 规则，不引入锁、TOCTOU 或 shared ledger。
- `ARCH-GOV-006`：每个标准 task mandatory 进入 Architecture semantic owner；`architecture_impact` 恰好选择 `target_native`、`legacy_boundary_convergence` 或 `dedicated_refactor_slice`，`no_architecture_impact` 只返回 current identity 与可审核理由。
- `ARCH-GOV-007`：Guru public identity 与项目 baseline/change-contract identity 只在 task-local Architecture change contract 相交。适用 concern、owner、GAP、before/after、project check、evidence、review 或 freshness 缺失、过期或冲突时 fail closed。
- `ARCH-GOV-008`：普通 task 只写 task-owned contribution；shared current 仅由 Architecture owner 在 independent committed-diff review 后按 expected current identity 串行 promotion。live current 推进使旧 task 返回 `sync_required`，promotion diff 必须重新通过 Phase 2、task commit 与独立 Branch Review。

完整项目 change contract 与 project-check descriptor 见 [`change-contract.md`](./change-contract.md)。
