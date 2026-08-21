# #290 contribution traceability

| Requirement | Design | Test | Current/Architecture inheritance |
| --- | --- | --- | --- |
| `R290-01` | `D290-01`, `D290-02`, `D290-08` | `T290-01`, `T290-02`, `T290-11..14` | `BEH-001`, `DES-004`, ADR-006 |
| `R290-02` | `D290-02`, `D290-03`, `D290-08` | `T290-03`, `T290-04`, `T290-11`, `T290-12` | `BEH-001`, Architecture contribution #290 |
| `R290-03` | `D290-04..07` | `T290-03`, `T290-05`, `T290-06` | `DES-004`, ADR-006 |
| `R290-04` | `D290-02`, `D290-03`, `D290-05` | `T290-02`, `T290-04`, `T290-06` | design constitution, target-native path |
| `R290-05` | `D290-05`, `D290-06` | `T290-05`, `T290-06` | `BEH-001`, `DES-004` |
| `R290-06` | `D290-04`, `D290-06..08` | `T290-07`, `T290-12..14` | public Skill I/O contract |
| `R290-07` | `D290-07` | `T290-08`, `T290-10` | `DES-008`, current `SCN-005` |
| `R290-08` | `D290-04..08` | `T290-09`, `T290-12..14` | `DES-008`, #267 boundary |

Architecture impact：`architecture_impact`，change path：`target_native`。本 contribution
与 Architecture contribution/ADR-006 在 independent review 和 serialized promotion
前均不是 shared current authority；若 expected `.38` identity 已推进，必须返回
`sync_required`，不得覆盖新 current。
