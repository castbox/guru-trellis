# #247 Issue Scope Ledger retirement Traceability

状态：`reviewed_promoted`；promotion input：`current-main-0.6.5-guru.49`；current successor：
`current-main-0.6.5-guru.50`。稳定 ID 已合并到三层 versioned current authority；本 contribution只保留
provenance，不是第二 current authority。

| Requirement | Design | Test / Scenario | Architecture refs |
| --- | --- | --- | --- |
| `R247-01..02` | `D247-01`, `D247-06` | `T247-01`, `T247-07`, `SCN-090` | `ARCH-CUR-027`, `ARCH-INT-017`, `ARCH-GAP-008`, `ADR-009` |
| `R247-03` | `D247-01` | `T247-02` | `ARCH-CUR-027`, `ARCH-DOM-015` |
| `R247-04` | `D247-02` | `T247-03`, `SCN-087` | `ARCH-GOV-006..009`, `EVD-026` |
| `R247-05..06` | `D247-03..05` | `T247-04`, `SCN-085..087`, `SCN-090` | `ARCH-DOM-015`, `ARCH-INT-017`, `ARCH-GOV-009`, `ADR-009` |
| `R247-07` | `D247-05` | `T247-05`, `SCN-089` | `ARCH-DOM-015`, `ARCH-GOV-009` |
| `R247-08..09` | `D247-08` | `T247-06..07`, `SCN-088` | `ARCH-CUR-027`, `ARCH-GAP-008`, `ADR-009` |
| `R247-10` | `D247-06..08` | `T247-08`, `SCN-090` | `ARCH-CUR-027`, `EVD-026` |

`BEH-019` 由 `D247-08` / `T247-06` / `SCN-088` 承接；`BEH-020` 由
`D247-03..05` / `T247-04` / `SCN-085..087` / `SCN-090` 承接，其中 `SCN-090` 同时验证
Finalizer-to-Merge body identity continuity。旧 task migration明确不进入 traceability。

Architecture contribution locator：
[`docs/architecture/contributions/247-remove-issue-scope-ledger.md`](../../architecture/contributions/247-remove-issue-scope-ledger.md)，
identity：`architecture-contribution-247-remove-issue-scope-ledger-v1`。
Accepted ADR locator：
[`docs/architecture/adr/009-issue-reference-closure-ownership.md`](../../architecture/adr/009-issue-reference-closure-ownership.md)，
identity：`ADR-009`。

## Fresh Phase 2 Evidence And Remaining Gates

- `R247-01..10` 已由 `D247-01..08`、`T247-01..08` 与 `SCN-085..090` 覆盖；没有旧 task migration、
  ledger compatibility或替代 Issue aggregate进入 accepted traceability。
- 原 Phase 2 Architecture 曾按 `dedicated_refactor_slice` 审查；2026-09-13 committed Branch Review
  发现该 path 与 ADR contract 不完整后，该结论及其 downstream gate 已 stale。Planning 随后改为
  `target_native` / `ADR-009-CANDIDATE`，并已由本次 promotion 接受为 `ADR-009`。
- 2026-09-13 fresh Phase 2 已重新执行：Architecture 官方 invoke 返回
  `baseline_current / architecture_impact / target_native / reviewed_candidate`，`ADR required=true`；两个
  qualifier 均返回 `classified / qualified_current`，`guru-check-task` 返回 `passed`。
- 本次 fresh round 的相关 package/runtime/integration 共 `392` tests 通过；active ledger
  writer/reader/precondition/schema registration/aggregate DTO consumer为零，upstream ownership 与
  dogfood overlay drift 均为 `status=ok`，canonical/installed/platform projection保持一致。
- 此前完整 preset Python suite `203 tests / OK (skipped=1)`、parallel finish `2/2`、installed closeout
  `3/3` 与 routing `42/42` 仍是同一实现候选的较早完整回归事实，但不是本次 fresh Phase 2 的唯一 gate，
  也不替代新的 Architecture、qualification、freshness checker 或 public wrapper结果。
- independent committed full-diff Branch Review 已绑定 exact range
  `ec016827fac81d33faeacb307b0db76d5259dc28...9c3c00908446ac0fa86974cb9886f37917ac40ca`
  并返回候选 `none`、P0-P3 findings zero；serialized Architecture/RDT promotion 已建立唯一 active `.50`。
- 完整 Release matrix、tag、GitHub Release与生产业务仓验证继续作为明确 deferred boundary；promotion-created
  combined diff仍须fresh Phase 2、Task Commit与独立完整Branch Review，不证明Publication或远端结果。
