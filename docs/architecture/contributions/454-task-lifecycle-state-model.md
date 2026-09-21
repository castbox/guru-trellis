# #454 Task Lifecycle State Model Architecture Contribution

## Identity And Review State

- candidate identity: `architecture-contribution-454-task-lifecycle-state-model-v1`.
- lifecycle state: `candidate_pending_independent_review`.
- source authority: live Issue #454 and approved task planning.
- task locator: `.trellis/tasks/09-20-454-task-lifecycle-state-model`.
- related RDT contribution: `docs/requirements-design-test-contributions/454-task-lifecycle-state-model/`.
- expected current baseline: `current-main-0.6.17-guru.58` / `active`.
- design constitution: `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `guru-trellis-architecture-change-contract-v1`.
- change path: `target_native`.

This contribution is task-owned and does not update shared CURRENT. Promotion
requires independent committed full-diff review and an expected-current-bound
Architecture owner action. C2 records only the shared lifecycle kernel and DTO
substrate; C3-C6 package/runtime slices and #434 production activation remain
pending.

## Boundary And Decision

Before this candidate, task identity, mutable locator, checkout path, branch,
session, Git state and ownership are mixed across tracked metadata and runtime
mappings. The target boundary has one framework/extension split:

1. `castbox/Trellis` owns immutable TaskId, lifecycle generation, TaskId-to-
   TaskRef resolution and path-free session primitives.
2. Guru owns one shared lifecycle contract catalog and deterministic adapters,
   then later branch, checkout and resource substrates.
3. Phase D package owners consume the substrate without copying its authority.
4. #434 alone activates registry, workflow, manifest, installed and platform
   projections.

C2 implements only item 2's contract/identity/source/result primitives. It
does not add a durable identity index, second session store, workspace mapping
reader, compatibility alias, dual-read, dual-write or production route.

## Ownership And Source Identity

- official framework primitive source:
  `castbox/Trellis@eb370008c7689d4e272ae626bd002190ecbb3296`;
- reviewed parent: `43fffc170927c85d9f7fc106cc5a059e80d4530b`;
- reviewed tree: `bd1f133cc55d0562ad9ec5f426bca70d1584194b`;
- successful CI run: `35621578090`;
- Guru canonical contract: `trellis/skills/guru-team/contracts/task-lifecycle/`;
- Guru canonical runtime: `trellis/skills/guru-team/runtime/task_lifecycle/`.

Guru does not modify or copy `.trellis/scripts/**`. Invalid official facts fail
closed; the runtime does not repair task metadata or select semantic routes.

## Required Concerns

| Concern | Applicability | Candidate contract |
| --- | --- | --- |
| authority-binding | applicable | Bind Issue #454, Architecture `.58`, constitution v1 and change contract v1. |
| constitution-binding | applicable | Preserve official extension surfaces, owner isolation, minimum complexity and one-way convergence. |
| boundary-and-decision | applicable | Select `target_native` and keep Fork primitive ownership separate from Guru substrate and #434 activation. |
| owner-and-single-writer | applicable | Fork writes official task/session primitives; Guru writes shared substrate; later owners write packages and activation. |
| compatibility-and-exit | applicable | No compatibility layer; old production readers retire only in the later atomic activation. |
| gap-and-deviation | applicable | C2 removes the need for a new duplicate identity/session substrate but does not claim the complete lifecycle gap closed. |
| parallel-scope | applicable | This task writes only canonical substrate and task-owned contributions, not shared current or another task's package. |
| evidence-and-freshness | applicable | Bind exact Fork source, focused tests, source/README consistency, SSOT parity, task validation and zero upstream-script diff. |
| review-and-promotion | applicable | Candidate remains pending until Phase 2, committed full-diff review and serialized expected-current promotion. |

## Contract Shape

The Draft 2020-12 catalog declares 35 named DTOs. Stable TaskId, mutable
TaskRef and lifecycle generation remain separate. Source is the closed
`IssueSource | NoIssueSource` union; Delivery target is portable repository/ref
identity. Public DTOs contain only direct-consumer fields and reject machine
paths, session/authorization state, generic evidence and undeclared Git facts.
TaskId remains safe as the suffix of the reserved machine-handoff control ref;
repository and branch primitives share one schema/runtime value domain. Handoff
receipts use only that control namespace, and lifecycle state fields use closed
consumer-owned enums.

Identity resolution scans current active/archive artifacts, validates exact
TaskId plus case-fold uniqueness, preserves TaskId across rename/archive, and
maps missing legacy generation to zero without tracked rewrite. Schema loading
is local-only and rejects remote/parent refs, nested resource identities and
symlink escape.

## Validation And Promotion Boundary

C2 focused validation covers the lifecycle unit suite, Fork preparation/source
mapping, task validation, schema/compile checks, canonical/preset SSOT equality,
forbidden-field and legacy-reader scans, line limits, zero
`.trellis/scripts/**` diff and `git diff --check`.

The complete installer/upgrade/release matrix, registry closure, production
workflow cardinality, installed/platform projection, C3-C6 behavior and live
business operations are not C2 evidence. ADR is required at serialized
promotion because the final task changes framework/extension ownership and
state authority; no shared ADR is created by this candidate.
