# #311 contribution traceability

| Requirement | Design | Test | Current/Architecture inheritance |
| --- | --- | --- | --- |
| `R311-01` | `D311-01..04`, `D311-08` | `T311-01`, `T311-02` | `BEH-008`, `DES-012`, ADR-007 |
| `R311-02` | `D311-01..03` | `T311-02`, `T311-03` | installer manifest contract, ADR-007 |
| `R311-03` | `D311-02..04` | `T311-01`, `T311-05` | #191 clean provenance-tail contract, ADR-007 |
| `R311-04` | `D311-02..04` | `T311-02`, `T311-03` | preset installer source provenance, ADR-007 |
| `R311-05` | `D311-04`, `D311-05`, `D311-08` | `T311-01`, `T311-02`, `T311-04` | `BEH-008`, ADR-007 |
| `R311-06` | `D311-05..07` | `T311-05`, `T311-06` | reviewed/publication two-head contract, #191 |
| `R311-07` | `D311-01`, `D311-05..07` | `T311-05`, `T311-06` | installer source provenance, ADR-007 |
| `R311-08` | `D311-06..08` | `T311-07`, `T311-08` | `REQ-014`, `BEH-010`, `DES-012`, `TST-012`, `SCN-009` |
| `R311-09` | `D311-01`, `D311-09`, `D311-10` | `T311-08`, `T311-09` | #195 package-local runtime, standalone verifier boundary |
| `R311-10` | `D311-03..08` | `T311-03`, `T311-04`, `T311-07` | Finalizer fail-close and diagnostic contract |
| `R311-11` | `D311-09..11` | `T311-09`, `T311-10` | `ARCH-CUR-002`, `ARCH-CUR-006`, `DES-015` |
| `R311-12` | `D311-09..11` | `T311-11`, `T311-12` | Validation Scope Ownership, `ARCH-GAP-001..005` |
| `R311-13` | `D311-12` | `T311-13` | standalone verifier evidence and cleanup boundary |

Architecture impact：`architecture_impact`；change path：`target_native`。本 contribution 与 Architecture
contribution/ADR-007 已通过 independent committed full-diff review，并由 expected `.40` serialized
promotion 提升到 `.41` 的 `reviewed_promoted`。promotion-created diff 仍须 fresh 重新进入 Phase 2、
task commit 与 Branch Review。

当前实现证据覆盖 `R311-01..11` 对应的 `T311-01..10` 与 `R311-13/T311-13`。distinct fresh-final
Branch Review 绑定
`origin/main@d907fcc5e17f23b6499648e5e9a208457f2d6f8b...651defee871d4bb07683547df09d1e0ac62b4a49`
的 7 commits / 85 paths；`BR-311-FIXTURE-001` 与 `BR-311-SOURCE-001..006` 全部闭环，P0-P3 open
findings 为零。

`R311-12/T311-11` 仍为 `unverified`：current `651defee` 尚未在现有真实 fixture 上完成 fresh
reinstall、GitHub Publication/Finalizer、Ready 与 terminal flow；local fake-GitHub 第 3 次且最后一次
完整 integration 通过不替代该外部证据，且禁止第 4 次完整 integration或创建新的真实 throwaway repo。
#267 release-wide matrix/tag/Release、生产发布与错误文件重试同样保持 `unverified`，Issue #311 保持
OPEN，直至复跑证明最大根因已修复。
