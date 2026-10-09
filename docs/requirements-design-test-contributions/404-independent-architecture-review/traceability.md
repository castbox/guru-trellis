# #404 双向追踪

状态：RDT 合同已晋升至 `current-main-0.6.17-guru.78`，不表示实现或 Architecture promotion 完成。继承 RDT/Architecture `current-main-0.6.17-guru.77` / `active`；source 为 Issue #404 `2026-10-09-r4`。本表连接本任务最小增量，实际结果唯一引用 [Test](./test.md)。

| Requirement | Design | Acceptance / Test |
| --- | --- | --- |
| R404-01 | D404-01, D404-05 | A404-06..08 / T404-06..08 |
| R404-02 | D404-01, D404-02 | A404-01, A404-02, A404-06, A404-07 / T404-01, T404-02, T404-06, T404-07 |
| R404-03 | D404-02, D404-03 | A404-01..03 / T404-01..03 |
| R404-04 | D404-03 | A404-03, A404-04 / T404-03, T404-04 |
| R404-05 | D404-04 | A404-04, A404-05 / T404-04, T404-05 |
| R404-06 | D404-01, D404-05, D404-07 | A404-07, A404-08 / T404-07, T404-08 |
| R404-07 | D404-05, D404-06 | A404-08, A404-09 / T404-08, T404-09 |
| R404-08 | D404-07, D404-08 | A404-01..10 / T404-01..10 |

反向引用：D404-01..08 和 T404-01..10 均通过上述行追溯 R404-01..08；A404 只标识 task acceptance，不另建测试结果 authority。Architecture inheritance 由 [public locator](../../architecture/README.md) 和 [task-owned contribution](../../architecture/contributions/404-independent-architecture-review.md) 承接，不复制其私有结果或 Constitution 正文。shared current 晋升由原 owner 重新读取 live expected-current 决定，不能由本表预定版本或推定后续 gate 通过。
