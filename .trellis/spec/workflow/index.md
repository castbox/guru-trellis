# Guru Trellis Workflow Specs

This repository is the public source for the reusable `guru-team` Trellis
workflow and preset. It is not a product backend/frontend application.

## Scope

Use these specs when changing:

- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/config-template.yml`
- `trellis/workflows/guru-team/schemas/`
- `trellis/workflows/guru-team/scripts/`
- `.trellis/workflow.md` when dogfooding the marketplace workflow in this repo

## Pre-Development Checklist

Before editing workflow behavior:

1. Read [workflow-contract.md](./workflow-contract.md).
2. Read [companion-scripts.md](./companion-scripts.md) when changing Bash or Python helpers.
3. Read [data-contracts.md](./data-contracts.md) when changing config, task-start-context, runtime boundary, review-gate, issue ledger, or PR payload data.
4. Read [skill-package-contract.md](./skill-package-contract.md) when changing public workflow skills, registry/interface schemas, workflow markers, installation, or typed exits.
5. Read [quality-guidelines.md](./quality-guidelines.md) before validation or commit.
6. Read shared guides under `.trellis/spec/guides/` when the change touches multiple generated surfaces or payload contracts.

## Local Architecture

- `trellis/index.json` publishes the marketplace template id `guru-team`.
- `trellis/workflows/guru-team/workflow.md` is the canonical workflow contract.
- `.trellis/workflow.md` is this repository's dogfooded active copy and must stay synchronized when runtime parsing or local validation depends on the updated workflow.
- `trellis/workflows/guru-team/config-template.yml` defines default Guru Team behavior.
- `trellis/workflows/guru-team/scripts/bash/*.sh` are thin executable wrappers.
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` owns companion behavior.
- Phase 0 base selection/sync is owned by the active `guru-sync-base` package plus
  shared `sync-base` / `check-base-sync` runtime commands; `prepare-task` reuses
  that core and does not define a second resolver.
- `trellis/skills/guru-team/` owns the public workflow skill registry, interface schemas, packages, and test-only fixtures.
- Interface 1.2 remains the frozen legacy contract. Registry 1.1 selects exact
  `interface_schema_id` plus `io_contract_state`; interface 1.3 is
  production-active for all thirteen active workflow packages and 52 external
  exits. Global workflow markers are 13 invokes, 52 exits, and 29 targets. The frozen
  `stage0-minimal-handoff-v1` manifest owns its original six packages and 24
  exits, while `production-minimal-handoff-v1` independently owns planning,
  check, and commit with 11 exits. The mixed fixture remains test-only.
- `discover-skill-contract` is the stable deterministic public discovery
  command. It returns a closed legacy/minimal variant and portable errors; the
  exact package invocation remains package-owned and callers do not import the
  companion Python source.
- `guru-discover-change-context` owns the semantic Phase 0 current-state/history discovery loop; its deterministic runtime reads only archived `finish-summary.json:index.*` and persists no repo-level cache.
- `guru-create-task-workspace` owns the final Intake mutation closed loop. Its
  recorder/executor/checker publish stdout plan/result contracts, create either
  one exact reviewed issue or one exact workspace/task invocation, persist only
  four portable task-local Intake artifacts, and use only ignored
  `.trellis/.runtime/guru-team/**` mappings.
- `guru-approve-task-plan` owns the Phase 1 semantic planning approval closed
  loop. Its shared recorder/checker consume AI-reviewed input and validate only
  schema, repository/planning facts, digests, freshness, and the typed-exit
  union for the single task-local `planning-approval.json` artifact.
- `guru-check-task` owns the complete Phase 2 semantic check, scope-before-
  severity classification, Docs SSOT review, finding full rerun, four typed
  exits, and the single `phase2-check.json`; unchanged official `trellis-check`
  workers provide evidence only.
- `guru-review-branch` is the sole Phase 3.5 semantic owner. Global workflow
  and platform entries only invoke its six-field public input and consume its
  four typed exits; review scripts are package-owned deterministic
  recorder/validator implementation details.
- `guru-review-task-publication` is the sole publication semantic owner after
  Branch Review. The workflow caller first authors the two current task-local
  publication content candidates, then invokes this owner; the caller does not
  judge readiness. The Skill owns two target-authored profiles, the single layered
  `pr-readiness.json`, metadata-only internal revision, ten-dimension review,
  and `ready` / `return_to_task_work` / `blocked`; workflow owns only routes.
- `guru-verify-extension-installation` is the sole semantic owner of extension
  installation applicability, closed capability selection, adequacy, findings,
  and the four verification exits. It owns the active
  `verification_required` target profile; standalone calls use the distinct
  `standalone_verification` profile.
- `guru-finalize-task` is the active semantic owner of immutable closeout-plan
  review, exact digest confirmation, seven distinct input profiles, six public
  exits, and the owner-private recovery loop. It reuses the existing #105
  deterministic transaction engine. Package discovery, global invocation after
  publication `ready`, five thin finish entries, and automatic machine recovery
  routing are active. Issue #119 adds the canonical `guru-finish-work` entry and
  combined Finish-family route while preserving the package contracts.
- `trellis/workflows/guru-team/schemas/task-start-context.schema.json` documents the portable task-start context JSON shape.

## Required Validation

Run the narrowest reliable set for your change, and include the result in the task record:

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
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

- `skill-package-contract.md`: public Interface 1.3 I/O, active publication
  bridge, private state and routing discriminator;
- `workflow-contract.md`: thin Phase 3.5 invocation and typed consumers;
- `data-contracts.md`: scenario/disposition/finding artifact shapes;
- `companion-scripts.md`: deterministic recorder/checker boundary;
- `quality-guidelines.md`: lifecycle, eval, distribution and upgrade coverage.

## Task Publication Review Closed-Loop Owner

The durable contracts for `guru-review-task-publication` are split across
`skill-package-contract.md`, `workflow-contract.md`, `data-contracts.md`,
`companion-scripts.md`, and `quality-guidelines.md`. Together they own the two
Interface 1.3 profiles, minimal exits, layered private gate, semantic/runtime
boundary, thin routing, real-wrapper eval, participation in the current
thirteen-Skill/52-exit package closure, and install/update checks. The global
workflow projection is 13 invokes, 52 exits, and 29 targets.

## Extension Installation Verification Closed-Loop Owner

The durable contracts for `guru-verify-extension-installation` are split
across `skill-package-contract.md`, `workflow-contract.md`,
`companion-scripts.md`, `quality-guidelines.md`, `preset/installer.md`, and
`docs/public-docs.md`. Together they own its two structurally distinct inputs,
four minimal exits, one task-local-or-session private owner result, remote
clean-install executor, retry/stale/redaction rules, real-wrapper production
eval, and canonical/installed/platform/update/reapply verification.

## Task Finalization Closed-Loop Owner

The durable contracts for active `guru-finalize-task` are split across
`skill-package-contract.md`, `workflow-contract.md`, `companion-scripts.md`,
`quality-guidelines.md`, `preset/installer.md`, `preset/upstream-ownership.md`,
and `docs/public-docs.md`. Together they own its seven profiles, six external
exits, immutable closeout plan, exact digest confirmation, owner-private
recovery facts, real-wrapper eval, and additive distribution.

The current package graph contains thirteen active Skills and 52 external exits
with twelve target-owned `skill_input_authoring_seed` handoffs. Global workflow
markers are 13 invokes, 52 exits, and 29 targets. Issue #119 closes combined
Finish-family acceptance and umbrella Issue #115. Issue #132 remains the
follow-up owner for physical upstream overlay cleanup.
