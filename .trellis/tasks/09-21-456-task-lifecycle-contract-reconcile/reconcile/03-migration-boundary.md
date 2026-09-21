# Migration Boundary

## 1. Fixed Sequence

Exact dependency: `#454@b695adc928c2064bd27f07e2bb3bbbd034540571`.

The target sequence is fixed:

1. Phase C: implement #454 substrate.
2. Phase D443: migrate `guru-bind-task-session` package/schema/runtime/projections.
3. Phase D436: migrate Reactivate, Completion, Closure, Finish, and Cleanup packages.
4. Phase E434: fresh reconcile and atomically activate #434 workflow graph.

## 2. Replace/Retire Boundary

| Item ID | Affected package/files | Unique migration owner | #454 dependency | Forbidden before completion | Blocking | Successor task | Completion proof |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `443-INPUT-SCHEMA` | Bind `schemas/input*`, interface/examples | Bind package owner | TaskId/generation/session resolution | Bind major activation | yes | Phase D443 Bind migration | New input schemas validate TaskId/generation profiles and contain no workspace/path authority. |
| `443-SESSION-PAYLOAD` | common-dir session store/schema | #454 substrate owner | Session Association design 08 | Any new Bind/Create/Reactivate session write | yes | Phase C substrate implementation | Substrate tests show the stored association is exactly `task_id + lifecycle_generation`. |
| `443-SUCCESS-DTO` | Bind output/consumer schemas | Bind package owner | Public I/O design 11 Bind rows | Bind routers and #434 graph | yes | Phase D443 Bind migration | All five success outputs and consumer schemas validate the same `TaskLifecycleDTO + resume_target` shape. |
| `443-EXPLICIT-MODE` | Bind interface/schema/runtime; workflow router | Bind package owner | Session explicit-task contract | Context-less create/resume route | yes | Phase D443 then Phase E434 | Interface/runtime tests emit `explicit_task_mode` and the #434 router consumes it. |
| `443-BLOCKED-DTO` | Bind blocked output schema and interface wiring | Bind package owner | `ReasonDTO` family | Bind major activation | yes | Phase D443 Bind migration | Interface path/id and blocked consumer schema agree on the target `ReasonDTO` output. |
| `443-MANUAL-RECOVERY` | Bind runtime/Skill/examples | Bind package owner | pointer-only recovery | Manual recovery route | yes | Phase D443 Bind migration | Recovery tests update only the session pointer and never reconstruct workspace mappings. |
| `443-MAPPING-DEPENDENCY` | Bind runtime and legacy mapping readers/writers | #454 substrate owner | retired mapping model | Any target Bind runtime | yes | Phase C + Phase D443 | Repository search and tests show no active Bind reader/writer depends on task/workspace mappings or path/branch/HEAD fields. |
| `443-CONSUMER-ROUTERS` | canonical/dogfood workflow | #434 workflow owner | new Bind interface | Production routing | yes | Phase E434 graph activation | Canonical and dogfood workflows contain every declared Bind router with one mapped consumer. |
| `443-REGISTRY-SELECTOR` | registry Bind selector | #434 activation owner | Phase D443 package-ready identity | Selector flip/integrated state | yes | Phase E434 graph activation | The activation transaction selects only the reviewed Phase D443 package identity. |
| `443-PROJECTIONS` | installed/platform Bind package files | Bind package owner | migrated canonical package | Installer/platform publication | yes | Phase D443 Bind migration | Canonical, installed, manifest, and declared-platform Bind bytes pass parity/drift checks. |
| `436-REACTIVATE-INPUT` | Reactivate input/private transaction schemas/runtime | Reactivate package owner | archive/generation/acquisition/ledger substrate | Reactivate major activation | yes | Phase D436 Reactivate migration | Reactivate inputs validate the target archive/generation/acquisition refs and omit retired workspace authority. |
| `436-REACTIVATE-PLANNING` | Reactivate planning output/schema | Reactivate package owner | target DTO/branch/session outcome | Planning router activation | yes | Phase D436 then Phase E434 | Planning output validates the target DTO and is consumed by the declared planning router. |
| `436-REACTIVATE-LEGACY-EXITS` | Reactivate interface/schemas/consumers | Reactivate package owner | target exit closure | Any alias or old route | yes | Phase D436 Reactivate migration | Interface, schemas, runtime, tests, and workflow contain no legacy direct requirements/implementation/evidence-refresh exits. |
| `436-REACTIVATE-NEW-EXITS` | Reactivate interface/output schemas | Reactivate package owner | design 11 Reactivate rows | New graph routing | yes | Phase D436 then Phase E434 | All target Reactivate exits validate and have exactly one declared #434 consumer. |
| `436-REACTIVATE-BLOCKED` | Reactivate blocked schema | Reactivate package owner | `ReasonDTO` | Reactivate activation | yes | Phase D436 Reactivate migration | Blocked output and consumer schemas validate the same target `ReasonDTO`. |
| `436-COMPLETION-INPUT` | Completion input/schema/Skill | Completion package owner | scope/evidence/merge-lineage substrate | Completion production invoke | yes | Phase D436 Completion migration | Completion input tests resolve target scope, evidence, and merge-lineage refs without free-form legacy authority. |
| `436-COMPLETION-DTO` | Completion output/consumer schemas | Completion package owner | design 11 Completion rows | Downstream Closure and revision routes | yes | Phase D436 Completion migration | Every Completion exit validates its target DTO and unique consumer. |
| `436-CLOSURE-INPUT` | Closure input/transaction/runtime schemas | Closure package owner | frozen action-set/source contracts | Closure production invoke | yes | Phase D436 Closure migration | Closure tests consume the frozen action-set/source refs and no longer accept the legacy direct field bundle. |
| `436-CLOSURE-EXITS` | Closure output/consumer schemas | Closure package owner | Result/Transaction/Reason DTOs | Finish route | yes | Phase D436 Closure migration | All Closure exits validate target Result/Transaction/Reason DTOs and their declared consumers. |
| `436-CLOSURE-NEW-CONFLICT` | Closure interface/workflow consumer | Closure package owner | external-change conflict contract | Conflict recovery route | yes | Phase D436 then Phase E434 | External-change conflict is emitted by live-state mismatch tests and returns to Closure semantic re-entry. |
| `436-FINISH-INPUT` | Finish input/transaction/runtime schemas | Finish package owner | Closure result and terminal state | Finish production invoke | yes | Phase D436 Finish migration | Finish consumes only the target Closure result/transaction refs and terminal lifecycle state. |
| `436-FINISH-EXITS` | Finish interface/output schemas/consumers | Finish package owner | design 11 Finish rows | Closure refresh/manual cleanup routes | yes | Phase D436 then Phase E434 | Target Finish exits validate and each route has one declared consumer. |
| `436-FINISH-SEAL` | Finish result and resource seal schemas | Finish package owner | resource ledger/terminal seal | Normal Cleanup | yes | Phase C + Phase D436 Finish | Finish tests seal the terminal archive projection and exact generation inventory into `ResourceSealRefDTO`. |
| `436-CLEANUP-INPUT` | Cleanup input/runtime/schema | Cleanup package owner | ResourceSeal and ledger resolution | Normal Cleanup | yes | Phase D436 Cleanup migration | Cleanup resolves owned resources only from the target seal and lifecycle ledger. |
| `436-CLEANUP-EXITS` | Cleanup output/consumer schemas | Cleanup package owner | CleanupResult/Reason DTOs | Cleanup terminal/self routes | yes | Phase D436 Cleanup migration | Cleanup terminal, remaining-resource, and blocked outputs validate their target DTOs and consumers. |
| `436-CLEANUP-PROFILES` | Cleanup Skill/interface/runtime | Cleanup package owner | normal/manual/handoff contracts | Manual/handoff Cleanup | yes | Phase D436 Cleanup migration | Normal, manual, and machine-handoff profiles pass package tests with their complete target exit closure. |
| `436-RESOURCE-OWNERSHIP` | Reactivate/Finish/Cleanup legacy resource logic | #454 substrate owner | single common-dir ledger | Any package-local second ledger | yes | Phase C + Phase D436 | Repository search and integration tests show one common-dir lifecycle ledger and no package-local competing ledger. |
| `434-WORKFLOW` | canonical/dogfood workflow | #434 workflow owner | all migrated package interfaces | Partial production graph | yes | Phase E434 graph activation | One reviewed activation diff adds the complete mandatory invocation chain without partial live edges. |
| `434-TARGETS` | workflow target markers/routers | #434 workflow owner | declared target consumers | Any target activation | yes | Phase E434 graph activation | Workflow validation maps every migrated exit to exactly one declared target consumer. |
| `434-STOPS` | workflow stop markers | #434 workflow owner | declared blocked/terminal exits | Any producer activation | yes | Phase E434 graph activation | Workflow validation maps every blocked/terminal exit to its declared stop and rejects unknown exits. |
| `434-REGISTRY-SELECTORS` | registry interfaces/integration state | #434 activation owner | package-ready gate | Integrated state or selector flip | yes | Phase E434 graph activation | The single activation transaction flips all package selectors only after package-ready identities pass. |
| `434-MANIFEST` | extension manifest schemas/files | #434 activation owner | migrated package inventory | Publishing mixed manifest | yes | Phase E434 graph activation | Manifest validation publishes exactly the reviewed migrated package inventory and command/schema identities. |
| `434-PROJECTION-BYTES` | installed/platform package projections | #434 activation owner | migrated canonical bytes from Phase D packages | Installer/overlay publication | yes | Phase E434 graph activation | Reapply, parity, drift, sidecar, and declared-platform checks prove projections match the activated canonical bytes. |

## 3. Out-Of-Scope Boundary

`434-DIRTY-WORKTREE` remains untouched. Its historical dirty files are neither migrated nor used as proof. Phase E434 must
start from a fresh selected base, reread live package interfaces, and build a new atomic activation candidate.

## 4. Owner Boundaries

- #454 substrate owns identity, generation, source/target relations, branch association/rebind, live checkout resolution,
  session storage, resource ledger, and shared DTO definitions.
- #443 owns Bind semantic behavior and package contract, not branch/checkout/resource authority.
- #436 package owners retain their semantic judgments and consume substrate; Finish seals inventory, Cleanup deletes resources.
- #434 owns only mandatory invocation, typed-exit routing, targets/stops, selectors, projection wiring, and atomic activation.
- Phase D package owners produce package-ready canonical contracts. The single #434 activation owner alone flips registry
  selectors, rewrites the active manifest inventory, and publishes active installed/platform projection bytes; this keeps
  each boundary row under one mutation owner while preserving the fixed predecessor dependency.
