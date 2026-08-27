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
contribution/ADR-007 在 independent committed full-diff review 和 expected `.40` serialized promotion前
均保持 candidate；promotion-created diff仍须 fresh重新进入 Phase 2、task commit 与 Branch Review。

当前实现证据已覆盖 `R311-01..11` 对应的 `T311-01..10`，并覆盖 `R311-13/T311-13`；
`R311-12/T311-11` 的 representative
GitHub closeout 已获授权并执行到 independent Branch Review，但旧 candidate 因
`BR-311-FIXTURE-001`（首次 Publication 无 existing plan 时 target repo 绑定变量未初始化）被 P1
阻断；后续 validation candidate `8138e3dd355f088ad6d4b43548243134f7bbe7d5` 又证明首次无 remote
branch/PR 的 `prepared` state 未进入 provenance inference。两个 source finding-fix 当前均通过
canonical/installed `58/58` regression、source/installed validator、reapply、parity 与 sidecar-zero。
candidate `cdc55ca93bc28934bfaa1c4ba48aeef83baf3277` 的第 3 次且最后一次 throwaway 已进入 default
matrix，但 exact failure facts 在 cleanup 后丢失；`R311-13/T311-13` 现已用 focused fixtures 完成
structured failure、stable helper label、outer parsing、closed schema、bounded credential-safe tail 与
unparseable fallback 验证。必须形成不同 candidate object，才可在现有 fixture 上 fresh 重试完整
closeout。该未验证项不被 local package validator、旧
candidate 的 false green 或 #267 release-wide evidence 替代。
