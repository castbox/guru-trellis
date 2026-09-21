# Contract Mapping

## 1. Target

Exact target: `#454@b695adc928c2064bd27f07e2bb3bbbd034540571`.

`TaskLifecycleDTO` is the fixed Bind success payload. It contains only `task_id + lifecycle_generation`; Bind consumers
freshly derive TaskRef. Other owners may use `TaskArtifactDTO` only where their direct consumer must read the artifact.

## 2. #443 Mapping

| Item ID | Target contract | Disposition | Target owner/consumer |
| --- | --- | --- | --- |
| `443-PKG-ID` | Session pointer semantic owner remains `guru-bind-task-session`. | `retain` | `guru-bind-task-session` |
| `443-COMMAND` | Keep `invoke-guru-bind-task-session`; bind it to the new major schemas/runtime. | `retain` | Bind package |
| `443-INPUT-SCHEMA` | TaskId/TaskLifecycleKey profiles; generation supports `0`; no workspace locator authority. | `replace` | #443 package migration |
| `443-SESSION-PAYLOAD` | Stored association exactly `task_id + lifecycle_generation`. | `replace` | #454 session substrate |
| `443-SUCCESS-EXIT-IDS` | Preserve all five exit IDs and router IDs. | `retain` | #434 routers |
| `443-SUCCESS-DTO` | All five exits output `TaskLifecycleDTO + resume_target`. | `replace` | #443 package migration |
| `443-EXPLICIT-MODE` | Add `explicit_task_mode(TaskLifecycleDTO) -> guru-current-phase-router`. | `replace` | #443 package migration / #434 router |
| `443-BLOCKED-EXIT-ID` | Preserve exit and stop IDs. | `retain` | `task-session-binding-blocked` |
| `443-BLOCKED-DTO` | Output `ReasonDTO`. | `replace` | #443 package migration |
| `443-MANUAL-RECOVERY` | Recover only session pointer; never reconstruct mappings. | `replace` | #443 package migration |
| `443-MAPPING-DEPENDENCY` | Remove all task/workspace mapping and path/branch/HEAD authority from Bind. | `retire` | #454 substrate + #443 migration |
| `443-CONSUMER-ROUTERS` | Materialize six target routers in workflow, validating DTO then routing only. | `replace` | #434 graph activation |
| `443-REGISTRY-SELECTOR` | Select the new major contract only during atomic graph activation after Phase D443 is package-ready. | `replace` | #434 activation |
| `443-PROJECTIONS` | Produce package-ready canonical schemas/interface/consumer contracts and package-owned projection sources; active installed/platform publication remains deferred. | `replace` | #443 package migration |

## 3. #436 Mapping

| Item ID | Target contract | Disposition | Target owner/consumer |
| --- | --- | --- | --- |
| `436-REACTIVATE-PKG` | Reactivate semantic owner remains unchanged. | `retain` | `guru-reactivate-task` |
| `436-REACTIVATE-INPUT` | Archived TaskLifecycleKey, source correction, checkout acquisition, branch binding, ledger and transaction contract. | `replace` | #436 Reactivate migration |
| `436-REACTIVATE-PLANNING` | Keep exit ID; output new `TaskArtifactDTO + BranchBindingRefDTO + session_outcome`. | `replace` | `task-planning-router` |
| `436-REACTIVATE-LEGACY-EXITS` | Remove direct requirements/implementation/evidence-refresh exits without aliases. | `retire` | #436 Reactivate migration |
| `436-REACTIVATE-NEW-EXITS` | Add session recovery, same-transaction resume, and source-correction exits from #454. | `replace` | Bind / Reactivate / Source Reconcile |
| `436-REACTIVATE-BLOCKED` | Keep IDs; replace output with `ReasonDTO`. | `replace` | `task-reactivate-blocked` |
| `436-COMPLETION-PKG` | Completion semantic owner remains unchanged. | `retain` | `guru-review-task-completion` |
| `436-COMPLETION-INPUT` | Consume TaskLifecycleKey, AcceptedScopeIdentity, exact merge lineage, and current evidence slots. | `replace` | #436 Completion migration |
| `436-COMPLETION-EXITS` | Preserve seven exit IDs and unique consumer directions. | `retain` | declared consumers |
| `436-COMPLETION-DTO` | Non-complete exits use `TaskArtifactDTO + ReasonDTO`; completed uses `ResultRefDTO`. | `replace` | #436 Completion migration |
| `436-CLOSURE-PKG` | Closure semantic owner remains unchanged. | `retain` | `guru-complete-task-closure` |
| `436-CLOSURE-INPUT` | Frozen transaction over lifecycle, Completion, source, scope, target, binding, evidence, and action set; outputs are Result/Transaction refs. | `replace` | #436 Closure migration |
| `436-CLOSURE-EXITS` | Preserve four current exit IDs and consumers with target DTOs. | `replace` | #436 Closure migration |
| `436-CLOSURE-NEW-CONFLICT` | Add `external_change_conflict -> Closure semantic re-entry`. | `replace` | #436 Closure migration |
| `436-FINISH-PKG` | Finish remains terminal archive and inventory-sealing owner. | `retain` | `guru-finish-task` |
| `436-FINISH-INPUT` | Consume Closure result/ref and use same-owner `TransactionRefDTO` recovery. | `replace` | #436 Finish migration |
| `436-FINISH-EXITS` | Keep current exits; add `closure_refresh_required` and `manual_cleanup_required`. | `replace` | Closure / Finish / Cleanup |
| `436-FINISH-SEAL` | Success outputs `ResourceSealRefDTO`; Finish seals but never deletes resources. | `replace` | #436 Finish migration |
| `436-CLEANUP-PKG` | Cleanup remains deletion/result owner. | `retain` | `guru-cleanup-task-resources` |
| `436-CLEANUP-INPUT` | Normal profile consumes only `ResourceSealRefDTO` and reads the ledger; no caller resource list. | `replace` | #436 Cleanup migration |
| `436-CLEANUP-EXITS` | Current exits use `CleanupResultRefDTO`; blocked uses `ReasonDTO`. | `replace` | #436 Cleanup migration |
| `436-CLEANUP-PROFILES` | Add normal/manual/machine-handoff profiles and target manual/handoff exits. | `replace` | #436 Cleanup migration |
| `436-RESOURCE-OWNERSHIP` | Retire package-local/derived ownership assumptions; use the single common-dir ledger, Finish seal, and Cleanup result owners. | `retire` | #454 substrate + #436 migration |

## 4. #434 Mapping

| Item ID | Target contract | Disposition | Target owner/consumer |
| --- | --- | --- | --- |
| `434-COMMANDS` | Preserve six invoke command IDs; bind to migrated package contracts. | `retain` | package owners |
| `434-WORKFLOW` | Atomically replace old closeout graph with mandatory invokes and target exit routing after dependencies pass. | `replace` | #434 graph task |
| `434-TARGETS` | Add every target router declared by the new package interfaces. | `replace` | #434 graph task |
| `434-STOPS` | Add all named blocked/terminal stops with one producer route each. | `replace` | #434 graph task |
| `434-REGISTRY-DEFERRED` | Keep deferred state until package migration and graph activation are jointly ready. | `retain` | #434 activation gate |
| `434-REGISTRY-SELECTORS` | Switch selectors to migrated major contracts only during atomic activation. | `replace` | #434 graph task |
| `434-MANIFEST` | Replace old schema/package references with the reviewed package-ready interface and projection inventory during activation. | `replace` | #434 activation |
| `434-PROJECTION-MECHANISM` | Keep projection/parity mechanism. | `retain` | installer/overlay owner |
| `434-PROJECTION-BYTES` | Publish the reviewed package-ready contracts atomically to active installed/platform bytes; no mixed old/new platform state. | `replace` | #434 activation |
| `434-DIRTY-WORKTREE` | Historical/stale planning input; not target authority or activation evidence. | `out_of_scope` | none |

## 5. Mapping Closure

- Mapping Item ID count: 47.
- Every Item ID has exactly one disposition.
- Inventory sections 6 and 7 bind every exact current schema field, exit, and consumer to one Item ID. A grouped row is
  valid only because every listed member shares that row's single disposition; no member is partly retained and partly
  replaced inside one Item ID.
- No alias, dual-read, dual-write, compatibility shim, or long-lived adapter is permitted.
