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
| `TST-012`, `SCN-009` | `REQ-014`, `BEH-010` | `DES-012`, `CON-004` | Finalizer focused package + Throwaway closeout evidence |
| `TST-013`, `SCN-010` | `REQ-015` | `DES-013` | source/installed registry-derived inventory validation |
| `TST-014`, `SCN-011..012` | `REQ-016`, `REQ-017`, `BEH-011` | `DES-014`, `DES-015`, `DES-017` | six-cell matrix summary + cell results |
| `TST-015`, `SCN-013` | `REQ-018` | `DES-016`, `DES-019` | three-group capability comparison + independent consistency/installation comparison |
| `TST-016`, `SCN-014` | `REQ-019` | `DES-007`, `DES-014` | installed RDT/Architecture/Bootstrap evals + docs projection checks |
| `TST-017`, `SCN-015..016` | `REQ-020` | `DES-018` | local A/B lifecycle + real GitHub A merge/closure/cleanup evidence |
| `TST-018`, `SCN-028`, `SCN-031..032` | `REQ-027`, `REQ-028` | `DES-026`, `DES-027`, `DES-032` | workflow stage routes + exact Phase 2/Branch Review/promotion re-entry |
| `TST-019`, `SCN-024` | `REQ-029` | `DES-028` | current design constitution locator/identity + public projection separation |
| `TST-020`, `SCN-024..027` | `REQ-030` | `DES-029` | schema/eval path exclusivity and no-impact contract |
| `TST-021`, `SCN-025..028` | `REQ-031` | `DES-026`, `DES-029`, `DES-030`, `DES-033` | task-local Architecture contribution + project change contract |
| `TST-022`, `SCN-029`, `SCN-033` | `REQ-032` | `DES-030..032` | project-check descriptor/result binding + route fixtures |
| `TST-023`, `SCN-031..032` | `REQ-033` | `DES-027`, `DES-033` | reviewed contribution、ADR-005与 serialized promotion |
| `TST-024`, `SCN-030` | `REQ-034` | `DES-033` | parallel stale and shared-current single-writer fixtures |
| `TST-025..026`, `SCN-024..033` | `REQ-035` | `DES-034` | source/installed projections、evals、reapply/drift与 representative clean install |
| `TST-027`, `SCN-034..037` | `REQ-036..040` | `DES-035..039` | canonical/installed sync-base 15/15 and exact authority fixtures |
| `TST-028..029`, `SCN-038..039` | `REQ-038`, `REQ-041..042` | `DES-037`, `DES-039..041` | post-sync transition and workspace freshness continuity tests |
| `TST-030`, `SCN-040` | `REQ-043` | `DES-042` | validators、projection equality、reapply/drift/sidecar-zero and representative detached wrapper |
