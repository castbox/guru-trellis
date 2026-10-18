# #295 contribution traceability

| Requirement | Design | Test | Current/Architecture inheritance |
| --- | --- | --- | --- |
| `R295-01` | `D295-01` | `T295-01` | `BEH-001`, `CON-001..003`, `DES-004`, `DES-008`, `ARCH-DOM-001/004` |
| `R295-02` | `D295-02` | `T295-01`, `T295-09` | `REQ-006`, `DES-006`, `ARCH-INT-001` |
| `R295-03` | `D295-01..02`, `D295-04` | `T295-01..02` | `REQ-007`, `DES-007`, `CON-001..003`, `ARCH-GOV-006..008` |
| `R295-04` | `D295-03`, `D295-06..07` | `T295-03` | `REQ-008`, `DES-008`, `ARCH-DOM-004`, `ARCH-INT-001` |
| `R295-05` | `D295-04..05` | `T295-03..05` | `BEH-001`, `REQ-001`, `DES-004`, `SCN-024/025/030/031` |
| `R295-06` | `D295-05..07` | `T295-04..05` | `REQ-009`, `DES-010`, `SCN-033`, `SCN-036..040` |
| `R295-07` | `D295-01`, `D295-08` | `T295-02`, `T295-06` | `CON-001..003`, `DES-006..008`, `CASE-001/002` |
| `R295-08` | `D295-07..08` | `T295-05..07` | `BEH-001`, `DES-004`, `SCN-024/025/030/031/033` |
| `R295-09` | `D295-09` | `T295-08` | `REQ-006`, `DES-006`, `ARCH-DOM-004` |
| `R295-10` | `D295-09` | `T295-08` | `REQ-008/009`, `DES-008/010`, `SCN-036..040` |
| `R295-11` | `D295-10..11` | `T295-09..11` | `REQ-006/007`, `DES-006/007`, `ARCH-INT-001` |
| `R295-12` | `D295-11..12` | `T295-11..12` | `DES-008`, `ARCH-GOV-006..008` |

Architecture impact: `architecture_impact`; change path: `target_native`; expected
current: `current-main-0.6.5-guru.39`. 本 contribution 与对应 Architecture
contribution保持 task-owned candidate，只有 independent committed full-diff review 后的
serialized promotion才能分配 successor shared identities并更新 current authority。
