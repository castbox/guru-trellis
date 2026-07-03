# Overlay Guidelines

## Canonical Relationship

Overlay files are small platform entrypoints. They should point the AI back to
`.trellis/workflow.md` and the Guru Team companion scripts instead of
duplicating the full workflow.

Reference overlay groups:

- `.agents/skills/trellis-start/SKILL.md`
- `.agents/skills/trellis-continue/SKILL.md`
- `.agents/skills/trellis-finish-work/SKILL.md`
- `.codex/prompts/trellis-start.md`
- `.codex/skills/trellis-continue/SKILL.md`
- `.claude/commands/trellis/continue.md`
- `.cursor/commands/trellis-finish-work.md`

## Required Content

All Guru Team overlays should include the marker:

```markdown
<!-- guru-team-overlay: v1 -->
```

Continue entries must:

- run `python3 ./.trellis/scripts/get_context.py`
- run `python3 ./.trellis/scripts/get_context.py --mode phase`
- route by task status
- keep planning artifacts and review fields in Chinese
- run Branch Review Gate before finish-work
- avoid adding a separate user-facing publish step

Finish entries must:

- call `.trellis/guru-team/scripts/bash/finish-work.sh --json`
- explain that finish-work archives the task, records journal metadata, and
  publishes a non-draft PR
- state that only `close_issues` may use close keywords

Start entries must:

- identify themselves as fallback/explicit orientation
- support natural-language issue-backed intake when no active task exists
- ask for consent before creating GitHub issues, worktrees, branches, or Trellis
  tasks unless explicitly requested
- treat `handoff.json` as intake provenance only

## Cross-Platform Consistency

When changing one overlay, search all copies:

```bash
find trellis/presets/guru-team/overlays -type f | sort
rg "Branch Review Gate|finish-work|handoff.json|guru-team-overlay" trellis/presets/guru-team/overlays
```

After canonical overlay edits, re-apply the preset to this source repository and
run the dogfood drift check:

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

The drift check is read-only and only verifies file presence/content equality.
It does not decide whether an overlay change is semantically correct.

Keep platform-specific command names only where needed, such as
`/trellis:finish-work` for Claude and `/trellis-finish-work` for Cursor.

## Anti-Patterns

- Pasting the entire workflow into every overlay.
- Creating platform-only semantics that do not exist in
  `trellis/workflows/guru-team/workflow.md`.
- Omitting the overlay marker, which makes installer conflict detection weaker.
- Mentioning publish as a separate user-facing step.
