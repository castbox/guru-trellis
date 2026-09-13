# #247 Issue Scope Ledger retirement Traceability

状态：`contribution_candidate`；expected current：`current-main-0.6.5-guru.49`；candidate successor
由 reviewed serialized promotion 分配。本 contribution 不写 shared current。

| Requirement | Design | Test / Scenario | Architecture refs |
| --- | --- | --- | --- |
| `R247-01..02` | `D247-01`, `D247-06` | `T247-01`, `T247-07`, `SCN-090` | `ARCH-INT-016`, `ARCH-GAP-006` |
| `R247-03` | `D247-01` | `T247-02` | `ARCH-INT-016` |
| `R247-04` | `D247-02` | `T247-03`, `SCN-087` | `ARCH-GOV-006..008` |
| `R247-05..06` | `D247-03..05` | `T247-04`, `SCN-085..087` | `ARCH-GOV-006..008` |
| `R247-07` | `D247-05` | `T247-05`, `SCN-089` | `ARCH-GOV-006..008` |
| `R247-08..09` | `D247-08` | `T247-06..07`, `SCN-088` | `ARCH-GAP-006` |
| `R247-10` | `D247-06..08` | `T247-08`, `SCN-090` | `ARCH-INT-016` |

`BEH-019` 由 `D247-08` / `T247-06` / `SCN-088` 承接；`BEH-020` 由
`D247-03..05` / `T247-04` / `SCN-085..087` 承接。旧 task migration明确不进入 traceability。

Architecture contribution locator：
[`docs/architecture/contributions/247-remove-issue-scope-ledger.md`](../../architecture/contributions/247-remove-issue-scope-ledger.md)，
identity：`architecture-contribution-247-remove-issue-scope-ledger-v1`。

## Phase 2 Closure

- `R247-01..10` 已由 `D247-01..08`、`T247-01..08` 与 `SCN-085..090` 覆盖；没有旧 task migration、
  ledger compatibility或替代 Issue aggregate进入 accepted traceability。
- current candidate 的完整 preset Python suite为 `203 tests / OK (skipped=1)`；parallel finish `2/2`、
  workspace invocation `1/1`、installed closeout `3/3`、routing `42/42` 与 live inventory均通过。
- canonical reapply、dogfood/source-installed validation、recursive sidecar/conflict scan与静态卫生通过；
  ledger active writer/reader/registration/public DTO consumer为零。
- Architecture Phase 2按 `dedicated_refactor_slice` 审查为 `reviewed_candidate`，expected shared current仍为
  `current-main-0.6.5-guru.49`；本 task不写 shared current。
- 完整 Release matrix、tag、GitHub Release与生产业务仓验证继续作为明确 deferred boundary，不改变
  current-version task 的 requirement/design/test闭环结论。
