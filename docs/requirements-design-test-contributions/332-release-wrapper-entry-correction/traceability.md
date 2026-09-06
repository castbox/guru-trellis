# #332 Original-entry correction Traceability

| Requirement | Design | Test | Architecture / acceptance |
| --- | --- | --- | --- |
| `R332-ENTRY-01` | `D332-ENTRY-01..02` | `T332-ENTRY-01` | original public identity; AC1 |
| `R332-ENTRY-02` | `D332-ENTRY-03..04` | `T332-ENTRY-02`, `T332-ENTRY-06` | invocation-local transaction; AC3-5 |
| `R332-ENTRY-03` | `D332-ENTRY-02..03` | `T332-ENTRY-02`, `T332-ENTRY-06` | compatibility branch exit; AC3, AC6 |
| `R332-ENTRY-04` | `D332-ENTRY-04`, `D332-ENTRY-07` | `T332-ENTRY-01` | single public entry; AC2 |
| `R332-ENTRY-05` | `D332-ENTRY-01`, `D332-ENTRY-05` | `T332-ENTRY-01`, `T332-ENTRY-04` | package-private/public boundary; AC2, AC7 |
| `R332-ENTRY-06` | `D332-ENTRY-05..06` | `T332-ENTRY-04` | Interface wrapper authority; AC7-8 |
| `R332-ENTRY-07` | `D332-ENTRY-08` | `T332-ENTRY-04` | non-`invoke.sh` regression; AC7 |
| `R332-ENTRY-08` | `D332-ENTRY-07` | `T332-ENTRY-05` | shared asset ownership; AC9 |
| `R332-ENTRY-09` | `D332-ENTRY-03`, `D332-ENTRY-11` | `T332-ENTRY-03` | preserved semantic/mutation boundaries; AC10 |
| `R332-ENTRY-10` | `D332-ENTRY-09..10` | `T332-ENTRY-07..08` | `.44 -> .45`, fresh candidate; AC11-12 |
| `R332-ENTRY-11` | `D332-ENTRY-13` | `T332-ENTRY-09` | exclusive Guru finish and incomplete-closeout fail closed; AC13 |
| `R332-ENTRY-12` | `D332-ENTRY-14` | `T332-ENTRY-10` | review visibility and pass announcement timing; AC14 |
| `R332-ENTRY-13` | `D332-ENTRY-15` | `T332-ENTRY-11` | displayed-action confirmation continuity; AC15 |

Current authority locators are `docs/{requirements,design,test}/README.md` and
`docs/architecture/README.md` at `current-main-0.6.5-guru.45`; `.44` remains the immutable predecessor. The
Architecture delta is owned by `docs/architecture/contributions/332-release-wrapper-entry-correction.md`.
The reviewed promotion records no dynamic publication, release, time, Gate checkpoint, or user authorization.
