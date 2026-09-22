# Phase C Migration And Retirement Ledger

## 1. Rule

Phase C builds target-native substrate and package-ready contracts while the
current production predecessor remains the sole active graph. Phase D443 and
D436 migrate package owners; E434 later performs the atomic activation and
retirement transaction.

`retain_until_phase_e` is not compatibility support. It prevents a partial
production cutover. New substrate must keep zero reads and zero writes against
the retained predecessor mappings.

## 2. Current Slice State

| Slice | State on September 22, 2026 | Authority meaning |
| --- | --- | --- |
| C2 shared lifecycle kernel | `reviewed_promoted` in `.59` | Current contract/runtime substrate only. |
| D0 stage-evidence correction | `reviewed_promoted` in `.59` | Current Reconcile/Task Commit/Branch Review lineage only. |
| C3 checkout acquisition/resolution | `reviewed_candidate` | Canonical runtime, DTOs, tests and inactive package are present in the current worktree; fresh gates remain. |
| C4-C7 | `not_started` | No authority or completion may be inferred from C3. |
| D443 / D436 | `not_started` | Existing active packages remain unchanged. |
| E434 / #434 activation | `not_started` | Active registry selector, active graph, workflow and projections remain on the predecessor. |

## 3. Closed Disposition

| Asset/capability | Current disposition | Later owner | Exit condition |
| --- | --- | --- | --- |
| C3 `guru-ensure-task-checkout` canonical package | `candidate_inactive` | C6 validates composition; E434 activates | Required later packages complete and atomic selector/workflow activation passes. |
| C3 planned registry/manifest metadata | `candidate_planned_metadata` | C3 records package readiness; E434 owns later activation | Registry state is exactly `planned`, canonical `planned_skill_ids` contains the ID, and no active selector or projection consumes it. |
| C3 checkout DTO/runtime | `candidate_target_native` | C4-C7 consume without copying authority | Fresh C3 gates and later consumer contracts pass. |
| `guru-create-task-workspace` package/id/command | `retain_until_phase_e` | new `guru-create-task` package in C6 | Selector switches atomically, then old ID/command exits. |
| task-workspace plan/result/recovery schemas | `retain_until_phase_e` | no new owner reuses old IDs | Old consumer count reaches zero. |
| task/workspace mapping writers | `retain_until_phase_e` | D443/D436 remove dependencies | Global writer count reaches zero. |
| task/workspace mapping readers/repair | `retain_until_phase_e` | D443/D436 remove dependencies | Global reader count reaches zero. |
| path-bearing session payload | `replace_in_fork_then_d443` | D443 Bind major | New Bind selector is active and old schema consumer count is zero. |
| `task.json.worktree_path/meta.worktree_path` authority | `stop_reading_in_new_code` | D443/D436 consumers | All production consumers stop reading it; tracked legacy bytes remain. |
| `task.json.branch/meta.branch` authority | `stop_reading_in_new_code` | C4 plus D443/D436 consumers | Branch association is active and legacy fields are non-authoritative history. |
| `base_head/entry_head/source_checkout` authority | `stop_reading_in_new_code` | affected package owners | Operation-local consumers replace all old readers. |
| Bind Interface current major | `out_of_phase_c3` | D443 | New major selector and routers activate atomically. |
| Reactivate/Completion/Closure/Finish/Cleanup majors | `out_of_phase_c3` | D436 | Migrated interfaces and routers activate atomically. |
| #434 workflow graph/targets/stops | `forbidden_in_phase_c` | E434 | Fresh E434 reconcile and complete graph validation pass. |
| active/integrated registry selectors | `forbidden_in_phase_c` | E434 | Package-ready gate passes. |
| `active_skill_ids` and active graph manifest | `forbidden_in_phase_c` | E434 | Complete active inventory passes. |
| installed/platform projection bytes | `forbidden_in_phase_c` | E434 | Atomic publication and parity pass. |

## 4. Unsupported Intermediate States

Phase C does not support:

- old packages reading the new substrate;
- new packages reading old mappings;
- session dual-read or dual-write;
- old/new public-ID aliases;
- registry selecting a new package while workflow still uses an old edge;
- installed/platform bytes preceding manifest and selector activation;
- a Guru overlay modifying Fork-generated official task/session files.

The task branch may contain inactive new canonical bytes beside the active old
predecessor only because production selection still has one owner.

## 5. Verification Queries

C3 verification maintains these bounded facts:

- new runtime mapping reader/writer count is zero;
- new runtime references to `worktree_path`, `source_checkout` and
  `.trellis/workspace` authority are zero;
- planned registry/manifest metadata names exactly the C3 package-ready ID;
- active registry selector, `active_skill_ids`, workflow, active graph and
  installed projection changes are zero;
- C4-C7 and D/E surface changes are zero;
- call-local checkout DTO fields do not enter durable lifecycle DTOs;
- every C3 package exit has one declared consumer;
- touched non-generated runtime files remain below 3000 lines.

Phase E, not C3, owns proof that all old and mixed production counts reach
zero.
