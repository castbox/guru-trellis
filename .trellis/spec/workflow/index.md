# Guru Trellis Workflow Specs

This repository is the public source for the reusable `guru-team` Trellis
workflow and preset. It is not a product backend/frontend application.

## Scope

Use these specs when changing:

- [Guru Trellis evolution requirements](../../../docs/requirements/evolution/requirement-main.md) for the user-confirmed product outcomes and the current target Requirements draft; the document status controls which detailed requirements are approved.
- [architecture-baseline.md](./architecture-baseline.md) for the Architecture Baseline owner and authority projection.
- [requirements-design-test-ssot.md](./requirements-design-test-ssot.md) for the atomic Requirements, Design, and Test authority, contribution, and traceability contract.
- [bootstrap-repository-ssot.md](./bootstrap-repository-ssot.md) for the one-time Bootstrap orchestration, cross-SSOT alignment, and minimal spec projection.

- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/config-template.yml`
- `trellis/workflows/guru-team/schemas/`
- `trellis/workflows/guru-team/scripts/`
- `.trellis/workflow.md` when dogfooding the marketplace workflow in this repo

## Pre-Development Checklist

Before editing workflow behavior:

1. Read the [Guru Trellis evolution requirements](../../../docs/requirements/evolution/requirement-main.md), map the proposed refactor to `EVO-001..007`, and identify any unaffected goals before choosing implementation boundaries.
2. Read [workflow-contract.md](./workflow-contract.md).
3. Read [companion-scripts.md](./companion-scripts.md) when changing Bash or Python helpers.
4. Read [data-contracts.md](./data-contracts.md) when changing config, current task identity, runtime boundary, review-gate, external-work-item references, or PR payload data.
5. Read [skill-package-contract.md](./skill-package-contract.md) when changing public workflow skills, registry/interface schemas, workflow markers, installation, or typed exits.
6. Read [quality-guidelines.md](./quality-guidelines.md) before validation or commit.
7. Read shared guides under `.trellis/spec/guides/` when the change touches multiple generated surfaces or payload contracts.
8. Read [semantic-retrieval.md](./semantic-retrieval.md) before an owner searches
   Docs, code, tests, history, duplicate candidates, or consumers and may form a
   negative existence conclusion.
9. Read [subtraction-first-compatibility.md](./subtraction-first-compatibility.md)
   when planning, implementing, checking, or reviewing delete/replace/merge
   work or a proposed compatibility exception.
   This also governs complexity restraint, long-term decoupling, and the
   3000-line review trigger for touched non-generated code files.

## Local Architecture

- `trellis/index.json` publishes the marketplace template id `guru-team`.
- `trellis/workflows/guru-team/workflow.md` is the canonical workflow contract.
- `.trellis/workflow.md` is this repository's dogfooded active copy and must stay synchronized when runtime parsing or local validation depends on the updated workflow.
- `trellis/workflows/guru-team/config-template.yml` defines default Guru Team behavior.
- `trellis/workflows/guru-team/scripts/bash/*.sh` are thin executable wrappers.
- `trellis/skills/guru-team/packages/*/runtime/` owns Skill-specific deterministic behavior; `trellis/skills/guru-team/runtime/` is a closed inventory containing only shared command dispatch, schema, discovery, installation validation, eval, and I/O primitives.
- Phase 0 base selection/sync is owned by `guru-sync-base`; the current Intake
  route carries checked call-local transitions through discovery, clarification,
  wording, and change-request review. A proposed draft enters the separate
  `guru-create-issue` owner and fresh Intake; an existing Issue or standalone
  request enters `guru-create-task`.
- `trellis/skills/guru-team/` owns the public workflow skill registry, interface schemas, packages, and test-only fixtures.
- The live registry and selected Interfaces, not old cardinalities, define the
  active packages. This #434 candidate has 34 active packages, 155 exits, and
  104 commands; the business workflow has 33 mandatory invokes and 153 exits.
  `production-current-v4` remains a four-package submanifest, not the complete
  Delivery/Completion lifecycle selector. The standalone extension verifier
  does not enter a business task.
- `discover-skill-contract` is the stable deterministic public discovery
  command. It returns the selected current Interface contract and portable errors; the
  exact package invocation remains package-owned and callers do not import the
  companion Python source.
- `guru-discover-change-context` owns the semantic Phase 0 current-state/history discovery loop; its deterministic runtime reads only archived `finish-summary.json:index.*` and persists no repo-level cache.
- Task creation, immutable identity, branch binding, checkout resolution,
  session binding, and Planning activation are separate current owners. TaskId
  and lifecycle generation, live Git checkout facts, and their selected
  branch/resource contracts replace old task/workspace mapping authority.
- `guru-approve-task-plan` owns the Phase 1 semantic planning approval closed
  loop. Its shared recorder/checker validate the compact schema 3.0 semantic
  projection in ignored owner-private runtime; consumers receive only one
  minimal typed exit and never parse `planning-approval.json`.
- `guru-check-task` owns the complete Phase 2 semantic check, scope-before-
  severity classification, Docs SSOT review, finding full rerun, four typed
  exits, and the ignored current schema 5.0 `phase2-check.json` owner checkpoint;
  unchanged official `trellis-check` workers provide ephemeral evidence only.
- `guru-review-branch` owns the independent committed full-diff review and
  bounded continuity. Its current `passed` exit enters Delivery Review;
  historical archived-review output stops for explicit legacy disposition.
- `guru-review-task-delivery` reviews one slice and its Refs-only PR payload;
  `guru-publish-task-delivery` owns push/PR recovery and
  `guru-merge-task-delivery` returns a Delivery result, not Task Completion.
- `guru-review-task-completion` judges the entire accepted task scope across
  Deliveries. Only `completed` enters `guru-complete-task-closure`, the separate
  source Issue disposition owner. `guru-finish-task` archives the current
  generation through a bookkeeping-only PR after Closure; only verified Finish
  enters `guru-cleanup-task-resources`. Normally finished archives may enter
  `guru-reactivate-task` under a new generation of the same TaskId.
- `guru-verify-extension-installation` is the source-repository-owned semantic
  verifier for clean throwaway installation adequacy. It is standalone-only,
  accepts `source_repository_verification`, returns `verified|blocked`, and is
  unreachable from business-task Delivery, Completion, Closure, and Finish.
- The old `guru-create-task-workspace`, `guru-review-task-publication`,
  `guru-finalize-task`, `guru-merge-task-pr`, and `guru-restore-archived-task`
  contracts and their 32/142, 22/98 snapshots are pinned-old history only.
  Old in-flight transactions require a compatible pinned version or reviewed
  manual disposition, never an adapter into the current lifecycle.

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

- `skill-package-contract.md`: selected public I/O, current Delivery Review
  handoff, private state and routing discriminator;
- `workflow-contract.md`: thin Phase 3.5 invocation and typed consumers;
- `data-contracts.md`: scenario/disposition/finding artifact shapes;
- `companion-scripts.md`: deterministic recorder/checker boundary;
- `quality-guidelines.md`: lifecycle, eval, distribution and upgrade coverage.

## Delivery And Task Closeout Owners

The current Delivery Review, Publish, Merge, Completion, Closure, Finish,
Cleanup, and Reactivate contracts are split across `skill-package-contract.md`,
`workflow-contract.md`, `data-contracts.md`, `companion-scripts.md`, and
`quality-guidelines.md`. The workflow invokes each stable Skill id and consumes
its typed exits; entry conditions, semantic judgments, recovery, and private
state remain with the owning package. Each Delivery PR is Refs-only. Completion
alone decides whole-task adequacy, Closure owns source Issue disposition, and
Finish's bookkeeping PR is not a business Delivery.

## Extension Installation Verification Closed-Loop Owner

The durable contracts for `guru-verify-extension-installation` are split
across `skill-package-contract.md`, `workflow-contract.md`,
`companion-scripts.md`, `quality-guidelines.md`, `preset/installer.md`, and
`docs/public-docs.md`. Together they own its single source-repository input,
two minimal exits, one ignored source-session private result, clean-throwaway
executor, retry/stale/redaction rules, and
canonical/installed/platform/update/reapply verification. Business tasks and
their closeout owners do not consume this Skill.

The retired Publication/Finalizer/PR Merge/Restore contracts in those specs are
explicitly historical. Their old evals and DTOs do not authorize current
Delivery or Finish, and old in-flight state is not auto-migrated.
