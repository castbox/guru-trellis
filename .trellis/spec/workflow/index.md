# Guru Trellis Workflow Specs

This repository is the public source for the reusable `guru-team` Trellis
workflow and preset. It is not a product backend/frontend application.

## Scope

Use these specs when changing:

- [architecture-baseline.md](./architecture-baseline.md) for the Architecture Baseline owner and authority projection.
- [requirements-design-test-ssot.md](./requirements-design-test-ssot.md) for the atomic Requirements, Design, and Test authority, contribution, and traceability contract.

- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/config-template.yml`
- `trellis/workflows/guru-team/schemas/`
- `trellis/workflows/guru-team/scripts/`
- `.trellis/workflow.md` when dogfooding the marketplace workflow in this repo

## Pre-Development Checklist

Before editing workflow behavior:

1. Read [workflow-contract.md](./workflow-contract.md).
2. Read [companion-scripts.md](./companion-scripts.md) when changing Bash or Python helpers.
3. Read [data-contracts.md](./data-contracts.md) when changing config, current task identity, runtime boundary, review-gate, issue ledger, or PR payload data.
4. Read [skill-package-contract.md](./skill-package-contract.md) when changing public workflow skills, registry/interface schemas, workflow markers, installation, or typed exits.
5. Read [quality-guidelines.md](./quality-guidelines.md) before validation or commit.
6. Read shared guides under `.trellis/spec/guides/` when the change touches multiple generated surfaces or payload contracts.
7. Read [semantic-retrieval.md](./semantic-retrieval.md) before an owner searches
   Docs, code, tests, history, duplicate candidates, or consumers and may form a
   negative existence conclusion.

## Local Architecture

- `trellis/index.json` publishes the marketplace template id `guru-team`.
- `trellis/workflows/guru-team/workflow.md` is the canonical workflow contract.
- `.trellis/workflow.md` is this repository's dogfooded active copy and must stay synchronized when runtime parsing or local validation depends on the updated workflow.
- `trellis/workflows/guru-team/config-template.yml` defines default Guru Team behavior.
- `trellis/workflows/guru-team/scripts/bash/*.sh` are thin executable wrappers.
- `trellis/skills/guru-team/packages/*/runtime/` owns Skill-specific deterministic behavior; `trellis/skills/guru-team/runtime/` is a closed inventory containing only shared command dispatch, schema, discovery, installation validation, eval, and I/O primitives.
- Phase 0 base selection/sync is owned by the active `guru-sync-base` package plus
  shared `sync-base` / `check-base-sync` runtime commands; `prepare-task` reuses
  that core and does not define a second resolver.
- The six-package/23-exit Phase 0 graph uses the workflow-owned five-stage
  `base_current` -> `context_current` -> `clarity_current` ->
  `wording_current` -> `readiness_current` transition family and versioned
  call-local invocation envelopes. `guru-sync-base` public invocation is the
  only authoritative sync; normal pre-task transport is stdin/stdout only and
  writes no owner/prerequisite/transition repository files. Compatibility
  `prepare-task` is a local diagnostic, not a workflow hop.
- `trellis/skills/guru-team/` owns the public workflow skill registry, interface schemas, packages, and test-only fixtures.
- Registry 1.4 accepts integrated, deferred, and standalone-only active rows.
  Integrated packages select Interface 1.4, normal-scenario qualification selects
  Interface 1.6, and the source-only verifier selects Interface 1.5. The registry
  contains twenty active packages and 85 exits; global business workflow markers
  are 19 invokes, 83 exits, 31 workflow targets, and 20 stop targets. Registry,
  discovery, invocation, installation, and validation read only the live
  current package graph. The planning/check/commit/qualification closure is
  defined only by `contracts/production-current.json` with contract id
  `production-current-v4`; it contains four packages, 20 profiles, 15 exits,
  authoring seeds, schemas, examples, production control, and eval bindings
  without an alternate execution path. Versioned v2/v3 files are immutable
  legacy assets.
- `discover-skill-contract` is the stable deterministic public discovery
  command. It returns the closed current Interface 1.4 contract and portable errors; the
  exact package invocation remains package-owned and callers do not import the
  companion Python source.
- `guru-discover-change-context` owns the semantic Phase 0 current-state/history discovery loop; its deterministic runtime reads only archived `finish-summary.json:index.*` and persists no repo-level cache.
- `guru-create-task-workspace` owns the final Intake mutation closed loop. Its
  recorder/executor/checker publish stdout plan/result contracts, create either
  one exact reviewed issue or one exact workspace/task invocation, persist only
  one Guru-owned portable task-local Intake artifact
  (`issue-scope-ledger.json`), and use only ignored
  `.trellis/.runtime/guru-team/**` mappings.
- `guru-approve-task-plan` owns the Phase 1 semantic planning approval closed
  loop. Its shared recorder/checker validate the compact schema 3.0 semantic
  projection in ignored owner-private runtime; consumers receive only one
  minimal typed exit and never parse `planning-approval.json`.
- `guru-check-task` owns the complete Phase 2 semantic check, scope-before-
  severity classification, Docs SSOT review, finding full rerun, four typed
  exits, and the ignored current schema 5.0 `phase2-check.json` owner checkpoint;
  unchanged official `trellis-check` workers provide ephemeral evidence only.
- `guru-review-branch` is the sole Phase 3.5 semantic owner. Global workflow
  and platform entries only invoke its six-field public input and consume its
  four typed exits; review scripts are package-owned deterministic
  recorder/validator implementation details.
- `guru-review-task-publication` is the sole publication semantic owner after
  Branch Review. The owner reads approved scope, the complete current diff,
  validation results, and live issue state, then authors and reviews the current
  PR title/body in memory. Its checked `ready` DTO carries that exact payload
  directly to Finalizer without task-local publication content artifacts. The
  Skill owns two target-authored profiles, the single layered ignored schema 3.0
  `pr-readiness.json` checkpoint, metadata-only internal revision, shared
  Finalizer preflight, ten-dimension review, and `ready` /
  `return_to_task_work` / `blocked`; workflow owns only routes.
- `guru-verify-extension-installation` is the source-repository-owned semantic
  verifier for clean throwaway installation adequacy. It is standalone-only,
  accepts `source_repository_verification`, returns `verified|blocked`, and is
  unreachable from business tasks, Publication, Finalizer, and finish-work.
- `guru-finalize-task` is the active semantic owner of the exact closeout plan
  review, current-conversation Finalizer confirmation, four distinct input profiles,
  six public exits, and the owner-private transaction/recovery loop. Current
  re-entry uses ignored `finalization-transaction.json`; current preparation and
  archives never select `closeout-plan.json`. Package discovery, global invocation
  after publication `ready`, three Guru-owned daily entries, and automatic machine
  recovery routing are active. Terminal `ready_for_merge` evals feed
  `guru-merge-task-pr`. Upstream
  `trellis-finish-work` entries are owned only by official Trellis and are not
  installed or managed by the Guru preset.
- Current task and worktree identity comes only from official `task.json`, the
  ignored runtime mapping, the current checkout, and live `git worktree list`
  facts. Missing or mismatched current identity fails closed; no alternate task
  identity artifact participates in resolution.

## Required Validation

Run the narrowest reliable set for your change, and include the result in the task record:

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate <task-dir>
.trellis/guru-team/scripts/bash/discover-skill-contract.sh --root . --mode installed --skill guru-sync-base --json
git diff --check
```

For workflow phase behavior, also run representative context reads:

```bash
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 1.1
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5
```

## Non-Applicable Template Areas

There is no app frontend, database, API server, or ORM in this repository. Do
not add React, database, route-handler, or service-layer guidance unless the
repository actually grows those assets.

## Branch Review Closed-Loop Owner

The durable contracts for `guru-review-branch` are split across:

- `skill-package-contract.md`: public Interface 1.4 I/O, active publication
  bridge, private state and routing discriminator;
- `workflow-contract.md`: thin Phase 3.5 invocation and typed consumers;
- `data-contracts.md`: scenario/disposition/finding artifact shapes;
- `companion-scripts.md`: deterministic recorder/checker boundary;
- `quality-guidelines.md`: lifecycle, eval, distribution and upgrade coverage.

## Task Publication Review Closed-Loop Owner

The durable contracts for `guru-review-task-publication` are split across
`skill-package-contract.md`, `workflow-contract.md`, `data-contracts.md`,
`companion-scripts.md`, and `quality-guidelines.md`. Together they own the two
Interface 1.4 profiles, minimal exits, layered private gate, semantic/runtime
boundary, thin routing, real-wrapper eval, participation in the current
twenty-Skill/85-exit package closure, and install/update checks. The global
business workflow projection is 19 invokes, 83 exits, 31 workflow targets, and
20 stop targets.

## Extension Installation Verification Closed-Loop Owner

The durable contracts for `guru-verify-extension-installation` are split
across `skill-package-contract.md`, `workflow-contract.md`,
`companion-scripts.md`, `quality-guidelines.md`, `preset/installer.md`, and
`docs/public-docs.md`. Together they own its single source-repository input,
two minimal exits, one ignored source-session private result, clean-throwaway
executor, retry/stale/redaction rules, and
canonical/installed/platform/update/reapply verification. Business tasks and
Finalizer do not consume this Skill.

## Task Finalization Closed-Loop Owner

The durable contracts for active `guru-finalize-task` are split across
`skill-package-contract.md`, `workflow-contract.md`, `companion-scripts.md`,
`quality-guidelines.md`, `preset/installer.md`, `preset/upstream-ownership.md`,
and `docs/public-docs.md`. Together they own its four profiles, six external
exits, dialogue-only side-effect confirmation, owner-private minimal transaction,
six-core archive, real-wrapper eval, and additive distribution.

The current package graph contains twenty active Skills and 85 external exits
with fourteen target-owned `skill_input_authoring_seed` handoffs. Global workflow
markers are 19 invokes, 83 exits, 31 workflow targets, and 20 stop targets. Issue #119 combined acceptance
additionally requires the three Guru-owned daily entries, terminal
`ready_for_merge` and Merge evals, current ownership
validation, and installed integration coverage.
