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
| `TST-029`, `SCN-039` | `REQ-044..045` | `DES-043..044` | Sync-to-Discovery public transition、live observation与 source-aware freshness |
| `TST-005`, `TST-007`, `TST-030`, `SCN-005`, `SCN-040` | `REQ-046` | `DES-006`, `DES-010`, `DES-042` | #295 canonical/installed/platform/preset contract closure |
| `TST-031`, `SCN-041..043` | `REQ-047`, `REQ-049` | `DES-045..046` | Finalizer canonical/installed 59/59 + binding/tail negative fixtures |
| `TST-032`, `SCN-044` | `REQ-048`, `REQ-049`, `BEH-008`, `BEH-010` | `DES-046` | prepared-state/existing-PR/absent-remote focused regression |
| `TST-033`, `SCN-045` | `REQ-049..050` | `DES-047` | verifier-zero dependency + source/installed/platform/reapply/drift checks |
| `TST-034`, `SCN-047` | `REQ-050` | `DES-047` | current real fixture `unverified`; local fake-GitHub integration only |
| `TST-035`, `SCN-046` | `REQ-051` | `DES-048` | verifier 17/17、routing 44/44、closed failure schema/postcheck evidence |
| `TST-036`, `SCN-048` | `REQ-052`, `REQ-055` | `DES-049..050`, `DES-052` | historical #267 unique active `.42` / superseded `.41` / expected-current checks；current successor `.43` |
| `TST-037` | `REQ-052..053` | `DES-051` | historical `.3/.39/CLI 0.6.15` mapping and release-boundary review |
| `TST-038` | `REQ-054` | `DES-049..051` | historical #267 `.41...42` semantic diff and no-ADR/no-runtime-change review |
| `TST-039`, `SCN-048` | `REQ-053`, `REQ-055` | `DES-049`, `DES-052` | historical #267 contribution review + serialized owners + post-promotion fresh lifecycle |
| `TST-040`, `SCN-053` | `REQ-056` | `DES-053`, `CON-005` | four project-local projections + public/installed inventory exclusion |
| `TST-041`, `CASE-003` | `REQ-057..058`, `REQ-061`, `BEH-012` | `DES-054..056`, `CON-006` | invocation, owner-composition and fail-closed contract guards |
| `TST-042`, `SCN-049..050` | `REQ-058`, `REQ-060`, `BEH-012`, `NFR-006` | `DES-055`, `DES-058`, `CON-006` | honest-path temporary Git fixture + planless reconciliation regression |
| `TST-043`, `SCN-051..052` | `REQ-060`, `NFR-006` | `DES-057..058` | reviewed-content checkpoint/drift table tests |
| `TST-044`, `CASE-004` | `REQ-059`, `REQ-062`, `NFR-006` | `DES-057`, `DES-059`, `CON-006` | live payload, forbidden artifact and independent confirmation checks |
| `TST-045`, `CASE-003` | `REQ-057`, `REQ-061..062`, `BEH-012` | `DES-054`, `DES-056`, `DES-059` | post-merge minimum gate scope and stop-before-mutation guard |
| `TST-046`, `SCN-054` | `REQ-063`, `REQ-065` | `DES-060`, `DES-062` | `.44` unique current、latest stable `.4/.39`、target `.5/.40/CLI 0.6.15` mapping review |
| `TST-047`, `SCN-054` | `REQ-064`, `REQ-066` | `DES-061` | fresh #311/#333/#339/#358/#361 merged prerequisite consumption |
| `TST-048`, `SCN-054` | `REQ-065..066` | `DES-060`, `DES-062` | expected `.43` serialized RDT promotion、Architecture `.44` inheritance and navigation closure |
| `TST-049`, `SCN-054`, `CASE-003` | `REQ-066..067`, `BEH-013` | `DES-061`, `DES-063` | same-candidate predecessor diff、version/distribution/platform/install gates and fail-closed routes |
| `TST-050`, `SCN-054`, `CASE-004` | `REQ-067..068`, `BEH-013` | `DES-063..064`, `CON-006` | installed business chain、secret/residue、tag/smoke/Release/closure/cleanup independent transactions |
| `TST-051` | `REQ-073` | `DES-065`, `DES-067` | current registry/interface/workflow/preset graph closure |
| `TST-052`, `SCN-055..056` | `REQ-069..070`, `BEH-014` | `DES-065..066` | #240 package/evals + PR #346 review + ADR-008 |
| `TST-053`, `SCN-057..058` | `REQ-071`, `BEH-015` | `DES-067`, `CON-007` | Merge/Restore routing tests + PR #351 review |
| `TST-054`, `SCN-057..058` | `REQ-072`, `BEH-015` | `DES-068`, `CON-007` | restore package success/idempotent/zero-write negative tests |
| `TST-055` | `REQ-069..073` | `DES-065..068` | EVD-019/EVD-020 + `.44` serialized promotion and fresh re-entry boundary |
