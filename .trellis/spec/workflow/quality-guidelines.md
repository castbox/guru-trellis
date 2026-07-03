# Workflow Quality Guidelines

## Source-Backed Changes

Every workflow behavior change should update the canonical source and the
surfaces that expose it:

- reusable workflow: `trellis/workflows/guru-team/workflow.md`
- dogfooded active workflow when needed: `.trellis/workflow.md`
- preset overlay entries under `trellis/presets/guru-team/overlays/`
- README docs for installation, upgrade, and daily entrypoints
- companion scripts and schemas when behavior is executable

Search before editing a phrase, command, marker, or config key:

```bash
rg "review-branch|finish-work|publish-pr|issue-scope-ledger|middle_platform_knowledge|guru-team-overlay"
```

## Required Checks

Use these checks before committing workflow or preset changes:

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate <task-dir>
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

Add targeted script invocations when changing phase parsing, intake, review,
finish, publish, installer behavior, or source-repo dogfood overlay sync.

## Review Focus

Before Branch Review Gate, review the full branch diff from the task's intake
base branch. Include:

- marketplace index and docs
- workflow and dogfood copy
- companion scripts
- schemas and config templates
- preset installer and overlays
- Trellis task artifacts
- generated or installed-copy expectations
- deployment asset impact

## Anti-Patterns

- Adding project-private business policy to the reusable `guru-team` workflow.
- Making shell scripts detect AI runtime capabilities such as MCP availability.
  Treat those as AI runtime/tool capabilities and express the decision in
  workflow or prompt text.
- Relying on chat memory for issue close scope, base branch, or reviewed head.
- Leaving `.new` or `.bak` installer outputs unresolved in committed changes.
- Committing local identity files, `.env`, tokens, signed URLs, or private
  provider output.
