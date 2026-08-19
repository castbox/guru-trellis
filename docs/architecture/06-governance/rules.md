# GOVERNANCE

- `ARCH-GOV-001`：Architecture 变化按 `bootstrap_foundation`、`task_impact_sync`、`promotion` 或 `repair` 进入唯一 semantic owner。
- `ARCH-GOV-002`：CURRENT 条目必须有 current code/config/test/release evidence；`inferred`/`unverified` 不能晋升为 CURRENT。
- `ARCH-GOV-003`：每次 gate 重读 live authority、locator/version/status 与 task delta；unknown/multiple/stale exit fail closed。
- `ARCH-GOV-004`：Architecture/RDT/projection 三者 locator 与 traceability 必须一致；projection 只能包含读取规则、identity 与 freshness。
- `ARCH-GOV-005`：普通并行 task 使用隔离 contribution，不共同写 shared current；这是 ownership 规则，不引入锁、TOCTOU 或 shared ledger。
