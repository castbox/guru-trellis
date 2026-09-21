# Current Contract Inventory

## 1. Authority And Status

- Issue authority: `castbox/guru-trellis#456`, updated `2026-09-21T06:17:54Z`.
- Current consumer baseline: `main@9d541be35a0cb4c6bef60a0c19b9c8eac39e6690`.
- Exact target: `#454@b695adc928c2064bd27f07e2bb3bbbd034540571`.
- Scope: #443 Bind/session, #436 Reactivate/Completion/Closure/Finish/Cleanup, and #434 graph consumers only.

Canonical package roots are under `trellis/skills/guru-team/packages/`; installed copies are under
`.trellis/guru-team/skills/packages/`. Platform projections are the declared Shared, Claude, Codex, and Cursor package
surfaces. Canonical and installed current bytes are aligned, but alignment to the old contract is not target compliance.

### 1.1 Exact locator and projection closure

For every package row below, the locator set is closed as follows:

- canonical package: `trellis/skills/guru-team/packages/<package>/`;
- installed package: `.trellis/guru-team/skills/packages/<package>/`;
- registry selectors: `trellis/skills/guru-team/registry.json` and `.trellis/guru-team/skills/registry.json`;
- extension manifest: `.trellis/guru-team/extension.json`;
- workflow consumers: `trellis/workflows/guru-team/workflow.md` and `.trellis/workflow.md`;
- current selected public projections: `.agents/skills/<package>/`, `.claude/skills/<package>/`,
  `.codex/skills/<package>/`, and `.cursor/skills/<package>/`.

Every current interface declares the same 23 destination identifiers:
`shared, claude, cursor, opencode, codex, kilo, kiro, gemini, antigravity, devin, qoder, codebuddy, copilot, droid,
dsh, pi, reasonix, zcode, trae, omp, grok, kimi, snow`. The current repository materializes the selected
Shared/Claude/Codex/Cursor projections above. `443-PROJECTIONS`, `434-PROJECTION-MECHANISM`, and
`434-PROJECTION-BYTES` cover this complete declared set; no platform-specific contract has an independent disposition.

### 1.2 Exact package, command, registry, and manifest members

| Package | Interface / command | Registry route and state | Manifest member | Inventory Item IDs |
| --- | --- | --- | --- | --- |
| `guru-bind-task-session` | Interface `1.4`; `invoke-guru-bind-task-session` | `task-session-binding`; `deferred` | package id plus current interface/tree digests | `443-PKG-ID`, `443-COMMAND`, `443-REGISTRY-SELECTOR`, `443-PROJECTIONS` |
| `guru-reactivate-task` | Interface `1.4`; `invoke-guru-reactivate-task` | `task-reactivation`; `deferred` | package id plus current interface/tree digests | `436-REACTIVATE-PKG`, `434-COMMANDS`, `434-REGISTRY-DEFERRED`, `434-REGISTRY-SELECTORS`, `434-MANIFEST`, `434-PROJECTION-BYTES` |
| `guru-review-task-completion` | Interface `1.4`; `invoke-guru-review-task-completion` | `task-completion-review`; `deferred` | package id plus current interface/tree digests | `436-COMPLETION-PKG`, `434-COMMANDS`, `434-REGISTRY-DEFERRED`, `434-REGISTRY-SELECTORS`, `434-MANIFEST`, `434-PROJECTION-BYTES` |
| `guru-complete-task-closure` | Interface `1.4`; `invoke-guru-complete-task-closure` | `task-closure`; `deferred` | package id plus current interface/tree digests | `436-CLOSURE-PKG`, `434-COMMANDS`, `434-REGISTRY-DEFERRED`, `434-REGISTRY-SELECTORS`, `434-MANIFEST`, `434-PROJECTION-BYTES` |
| `guru-finish-task` | Interface `1.4`; `invoke-guru-finish-task` | `task-finish`; `deferred` | package id plus current interface/tree digests | `436-FINISH-PKG`, `434-COMMANDS`, `434-REGISTRY-DEFERRED`, `434-REGISTRY-SELECTORS`, `434-MANIFEST`, `434-PROJECTION-BYTES` |
| `guru-cleanup-task-resources` | Interface `1.4`; `invoke-guru-cleanup-task-resources` | `task-resource-cleanup`; `deferred` | package id plus current interface/tree digests | `436-CLEANUP-PKG`, `434-COMMANDS`, `434-REGISTRY-DEFERRED`, `434-REGISTRY-SELECTORS`, `434-MANIFEST`, `434-PROJECTION-BYTES` |

## 2. #443 Session Binding

| Item ID | Surface | Current live fact |
| --- | --- | --- |
| `443-PKG-ID` | package/Skill | `guru-bind-task-session` is the semantic owner for resume, missing-session rebind, switch, Reactivate rebind, and manual recovery. |
| `443-COMMAND` | command | `invoke-guru-bind-task-session` is the public launcher and currently binds Interface `1.4` schemas/runtime. |
| `443-INPUT-SCHEMA` | schema | `guru-bind-task-session-input-1.0` uses TaskRef, continuation, current/target task refs, workspace-derived resolution, and generation rules from the old model. |
| `443-SESSION-PAYLOAD` | runtime state | Current runtime persists/reads TaskRef and workspace-related session authority rather than only TaskId + generation. |
| `443-SUCCESS-EXIT-IDS` | exits | `session_resumed`, `session_rebound`, `task_switched`, `reactivate_rebound`, and `session_manually_recovered` exist with five declared routers. |
| `443-SUCCESS-DTO` | output/consumer schema | All five success exits use a route payload containing `task_ref + lifecycle_generation + resume_target`. |
| `443-EXPLICIT-MODE` | missing exit | No `explicit_task_mode` exit exists; missing context identity currently fails closed. |
| `443-BLOCKED-EXIT-ID` | exit/stop | `binding_blocked -> task-session-binding-blocked` exists. |
| `443-BLOCKED-DTO` | output/interface wiring | The standalone blocked schema is exit-only and does not carry `ReasonDTO`, but `interface.json` declares its schema id while incorrectly pointing `binding_blocked` to the generic success `schemas/public-output.schema.json`; the live public contract is internally inconsistent. |
| `443-MANUAL-RECOVERY` | behavior | Manual recovery can reconstruct task/workspace mappings instead of limiting itself to the session pointer. |
| `443-MAPPING-DEPENDENCY` | private/runtime dependency | Runtime scans worktrees/mappings and reads path, branch, HEAD, base HEAD, task/workspace mappings, and legacy metadata. |
| `443-CONSUMER-ROUTERS` | workflow consumer | Five routers are declared in the interface, but they are not present as production targets in the current workflow. |
| `443-REGISTRY-SELECTOR` | registry | Registry route `task-session-binding` selects the current Interface `1.4` package and marks workflow integration deferred. |
| `443-PROJECTIONS` | manifest/platform | Manifest and platform projections publish the old public package subset consistently. |

## 3. #436 Post-Delivery Lifecycle

| Item ID | Surface | Current live fact |
| --- | --- | --- |
| `436-REACTIVATE-PKG` | package/Skill | `guru-reactivate-task` owns Reactivate semantics. |
| `436-REACTIVATE-INPUT` | input schema | `guru-reactivate-task-input-1.0` consumes `task_ref`, `archive_ref`, `task_id`, workspace/base/resource assumptions, and old generation handling. |
| `436-REACTIVATE-PLANNING` | exit | `reactivated_to_planning -> task-planning-router` exists, with old TaskRef-bearing output. |
| `436-REACTIVATE-LEGACY-EXITS` | exits | Direct exits to requirements, implementation, and evidence refresh exist. |
| `436-REACTIVATE-NEW-EXITS` | missing exits | `session_binding_recovery_required`, `resume_reactivation`, and `source_correction_required` do not exist. |
| `436-REACTIVATE-BLOCKED` | exit/output | `reactivate_blocked -> task-reactivate-blocked` exists with old blocked payload semantics. |
| `436-COMPLETION-PKG` | package/Skill | `guru-review-task-completion` owns Completion judgment. |
| `436-COMPLETION-INPUT` | input schema | `guru-review-task-completion-input-1.0` uses free-form `authority_refs`, `delivery_facts`, and `evidence_refs`; evidence refresh adds source/resume fields. |
| `436-COMPLETION-EXITS` | exits/consumers | Seven target exit IDs and consumer directions already match the target closure. |
| `436-COMPLETION-DTO` | outputs | Non-completed routes use TaskRef/resume payloads; `completed` is not the target `ResultRefDTO`. |
| `436-CLOSURE-PKG` | package/Skill | `guru-complete-task-closure` owns source Issue closure/no-mutation semantics. |
| `436-CLOSURE-INPUT` | input/schema | Current input is `completion_ref + source_issue`; outputs carry `task_ref`, source snapshot, and closure fields across owners. |
| `436-CLOSURE-EXITS` | exits | `closed`, `no_mutation`, `resume_closure`, and `blocked` exist with the target consumer directions. |
| `436-CLOSURE-NEW-CONFLICT` | missing exit | `external_change_conflict -> Closure semantic re-entry` is absent. |
| `436-FINISH-PKG` | package/Skill | `guru-finish-task` owns terminal archive/Finish semantics. |
| `436-FINISH-INPUT` | input/schema | Current input carries Closure fields directly; recovery does not use `TransactionRefDTO`. |
| `436-FINISH-EXITS` | exits | `success`, `resume_finish`, and `blocked` exist; `closure_refresh_required` and `manual_cleanup_required` are absent. |
| `436-FINISH-SEAL` | output/authority | Success outputs task/archive/finish/generation fields; there is no sealed inventory `ResourceSealRefDTO`. |
| `436-CLEANUP-PKG` | package/Skill | `guru-cleanup-task-resources` owns deletion and Cleanup result. |
| `436-CLEANUP-INPUT` | input/schema | Caller may provide `resources`; semantic result derives `owned_resources` from old workspace/runtime assumptions. |
| `436-CLEANUP-EXITS` | exits | `cleaned`, `remaining_resources`, and `blocked` exist; cleaned is zero-payload and remaining carries old continuation fields. |
| `436-CLEANUP-PROFILES` | profiles/exits | Normal/manual/machine-handoff profiles and manual/handoff exits are absent. |
| `436-RESOURCE-OWNERSHIP` | authority | No unified common-dir ledger is the single authority; Reactivate, Finish, and Cleanup retain overlapping resource assumptions. |

## 4. #434 Graph Consumer

| Item ID | Surface | Current live fact |
| --- | --- | --- |
| `434-COMMANDS` | commands | Six package invoke command IDs exist and point to current Interface `1.4` contracts. |
| `434-WORKFLOW` | workflow graph | Canonical/dogfood workflow still runs the old Branch Review -> Publication -> Finalizer -> Merge -> Restore graph; the six packages have no production mandatory invocation. |
| `434-TARGETS` | workflow targets | Bind routers and target Completion/Closure/Finish/Cleanup/Reactivate routers are absent or incomplete. |
| `434-STOPS` | workflow stops | Target blocked/terminal stops are absent or incomplete in the production graph. |
| `434-REGISTRY-DEFERRED` | registry state | All six packages are `active` with `workflow_integration_state=deferred`. |
| `434-REGISTRY-SELECTORS` | registry selector | Selectors point to the old Interface `1.4` schemas and package contracts. |
| `434-MANIFEST` | extension manifest | Manifest enumerates old input/output schema IDs and projected package files. |
| `434-PROJECTION-MECHANISM` | projection mechanism | Canonical -> installed -> Shared/Claude/Codex/Cursor projection and parity checking exist. |
| `434-PROJECTION-BYTES` | projected contract | Projected bytes consistently expose the old DTOs, exits, schemas, and consumers. |
| `434-DIRTY-WORKTREE` | historical workspace | The separate #434 dirty worktree is behind current main, contains stale planning/schema work, and has no target graph activation. It was not modified. |

## 5. Inventory Closure

- Inventory Item ID count: 47.
- Every Item ID appears exactly once in `02-contract-mapping.md`.
- Sections 6 and 7 enumerate every current public schema field and every external exit/consumer member. Each member is
  assigned to exactly one inventory Item ID or one explicitly named graph Item ID set; the corresponding mapping row is
  its sole disposition.
- Current package/interface facts are inputs only; no current deferred declaration is treated as activated workflow proof.

## 6. Exact Current Public Schema Fields

The following field sets are read from the current canonical public schemas. Aggregate schemas and per-exit schemas are
listed under the same Item ID only when all members have the same target disposition.

| Package | Current public schema IDs and exact fields | Inventory Item ID |
| --- | --- | --- |
| Bind | `guru-bind-task-session-input-1.0`: required `profile, mode, task_ref, continuation_id`; optional `target_task_ref, lifecycle_generation, resume_target, current_task_ref` | `443-INPUT-SCHEMA` |
| Bind | `guru-bind-task-session-output-1.0`: `exit_id, task_ref, lifecycle_generation, resume_target` | `443-SUCCESS-DTO` |
| Bind | Intended `guru-bind-task-session-output-blocked-1.0`: `exit_id`; live `interface.json` points that id to `schemas/public-output.schema.json`, whose actual id/fields are the success DTO (`exit_id, task_ref, lifecycle_generation, resume_target`) | `443-BLOCKED-DTO` |
| Reactivate | `guru-reactivate-task-input-1.0`: `profile, mode, task_ref, archive_ref, task_id` | `436-REACTIVATE-INPUT` |
| Reactivate | requirements/planning/implementation/evidence output schemas: `exit_id, task_ref, resume_target, lifecycle_generation` | `436-REACTIVATE-PLANNING`, `436-REACTIVATE-LEGACY-EXITS` |
| Reactivate | `guru-reactivate-task-output-blocked-1.0`: `exit_id` | `436-REACTIVATE-BLOCKED` |
| Completion | completion input: `profile, mode, task_ref, authority_refs, delivery_facts, evidence_refs`; evidence-refresh input additionally has `source_exit, resume_target` | `436-COMPLETION-INPUT` |
| Completion | remaining/evidence/additional-delivery/requirements-revision/implementation-revision outputs: `exit_id, task_ref, resume_target`; completed: `exit_id, task_ref, completion_ref`; blocked: `exit_id` | `436-COMPLETION-DTO` |
| Closure | `guru-complete-task-closure-input-1.0`: `profile, source_exit, mode, task_ref, completion_ref, source_issue`; optional `closure_ref` | `436-CLOSURE-INPUT` |
| Closure | no-mutation: `exit_id, task_ref, closure_exit, closure_ref, source_issue`; closed additionally has `issue_ref`; resume has `exit_id, task_ref, completion_ref, closure_ref, source_issue`; blocked: `exit_id` | `436-CLOSURE-EXITS` |
| Finish | `guru-finish-task-input-1.0`: `profile, source_exit, mode, task_ref, closure_exit, closure_ref, source_issue` | `436-FINISH-INPUT` |
| Finish | success: `exit_id, task_ref, archive_ref, finish_ref, lifecycle_generation`; resume: `exit_id, task_ref, closure_exit, closure_ref, source_issue`; blocked: `exit_id` | `436-FINISH-EXITS`, `436-FINISH-SEAL` |
| Cleanup | `guru-cleanup-task-resources-input-1.0`: `profile, source_exit, mode, task_ref, archive_ref, finish_ref, lifecycle_generation` | `436-CLEANUP-INPUT` |
| Cleanup | cleaned: `exit_id`; remaining: `exit_id, task_ref, archive_ref, finish_ref, lifecycle_generation`; blocked: `exit_id` | `436-CLEANUP-EXITS` |

Current private semantic/transaction schemas remain package implementation details, but their old workspace/resource
authority is included in `443-MAPPING-DEPENDENCY` and `436-RESOURCE-OWNERSHIP`; they cannot escape migration through an
unlisted public handoff.

## 7. Exact Current External Exit And Consumer Members

| Package | Current external exit -> unique consumer | Inventory Item ID |
| --- | --- | --- |
| Bind | `session_resumed -> guru-bind-task-session-resume-router`; `session_rebound -> guru-bind-task-session-rebind-router`; `task_switched -> guru-bind-task-session-switch-router`; `reactivate_rebound -> guru-bind-task-session-reactivate-router`; `session_manually_recovered -> guru-bind-task-session-manual-recovery-router` | `443-SUCCESS-EXIT-IDS`, `443-CONSUMER-ROUTERS` |
| Bind | `binding_blocked -> task-session-binding-blocked` stop | `443-BLOCKED-EXIT-ID` |
| Reactivate | `reactivated_to_requirements -> guru-clarify-requirements`; `reactivated_to_implementation -> guru-resume-implementation`; `reactivated_to_evidence_refresh -> guru-review-task-completion` | `436-REACTIVATE-LEGACY-EXITS` |
| Reactivate | `reactivated_to_planning -> task-planning-router` | `436-REACTIVATE-PLANNING` |
| Reactivate | `reactivate_blocked -> task-reactivate-blocked` stop | `436-REACTIVATE-BLOCKED` |
| Completion | `remaining_work -> active-task-continuation`; `evidence_pending -> guru-review-task-completion`; `additional_delivery_required -> task-delivery-planning-router`; `requirements_revision_required -> guru-clarify-requirements`; `implementation_revision_required -> guru-resume-implementation`; `completed -> guru-complete-task-closure`; `blocked -> task-completion-blocked` stop | `436-COMPLETION-EXITS` |
| Closure | `no_mutation -> guru-finish-task`; `closed -> guru-finish-task`; `resume_closure -> guru-complete-task-closure`; `blocked -> task-closure-blocked` stop | `436-CLOSURE-EXITS` |
| Finish | `success -> guru-cleanup-task-resources`; `resume_finish -> guru-finish-task`; `blocked -> task-finish-blocked` stop | `436-FINISH-EXITS` |
| Cleanup | `cleaned -> task-cleanup-complete` stop; `remaining_resources -> guru-cleanup-task-resources`; `blocked -> task-cleanup-blocked` stop | `436-CLEANUP-EXITS` |

Target-only exits absent from current interfaces are inventoried separately by `443-EXPLICIT-MODE`,
`436-REACTIVATE-NEW-EXITS`, `436-CLOSURE-NEW-CONFLICT`, `436-FINISH-EXITS`, and `436-CLEANUP-PROFILES`. Workflow target
and stop materialization for all retained, replaced, and new exits is covered by `434-TARGETS` and `434-STOPS`.
