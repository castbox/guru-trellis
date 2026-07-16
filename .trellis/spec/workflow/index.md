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
- `guru-discover-change-context` owns the semantic Phase 0 current-state/history discovery loop; its deterministic runtime reads only archived `finish-summary.json:index.*` and persists no repo-level cache.
- `trellis/workflows/guru-team/schemas/task-start-context.schema.json` documents the portable task-start context JSON shape.

## Required Validation

Run the narrowest reliable set for your change, and include the result in the task record:

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate <task-dir>
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
