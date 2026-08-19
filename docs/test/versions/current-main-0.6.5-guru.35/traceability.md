# Test Traceability

| Strategy / Scenario | Requirements | Design | Evidence |
| --- | --- | --- | --- |
| `TST-001` | `NFR-004` | `DES-008` | #266 docs/spec checks |
| `TST-002`, `CASE-001` | `REQ-003`, `REQ-008` | `DES-002`, `CON-001` | package tests / registry-interface graph |
| `TST-003`, `CASE-002` | `REQ-004`, `REQ-010` | `DES-003`, `CON-002` | semantic eval + independent review |
| `TST-004`, `SCN-001..004` | `REQ-001`, `REQ-005`, `BEH-001..006` | `DES-004`, `DES-005` | integration/task history |
| `TST-005`, `SCN-005` | `REQ-006`, `NFR-001` | `DES-001`, `DES-006` | throwaway/reapply/platform parity |
| `TST-006`, `SCN-006` | `REQ-007`, `BEH-007` | `DES-007` | RDT/Architecture/Bootstrap validation |
| `TST-007` | `REQ-008`, `NFR-003` | `CON-001..003` | schema/exit/consumer closure |
| `TST-008` | `REQ-009`, `NFR-004` | `DES-008` | GitHub/release/exact candidate owner evidence |
| `TST-009`, `SCN-007` | `REQ-005`, `REQ-011`, `REQ-012`, `REQ-013` | `DES-005`, `DES-009`, `DES-010`, `DES-011` | business parallel matrix owner evidence |
| `TST-010` | `REQ-011`, `BEH-008` | `DES-005`, `DES-009` | task index/archive/finish-summary query evidence |
| `TST-011`, `SCN-008` | `REQ-012` | `DES-011` | provider/base/partial recovery evidence |
