# Guru Team Trellis Preset

The preset installs companion assets and Guru Team entry overlays for the
`guru-team` Trellis workflow into an existing Trellis project.

It does not run `trellis init` and does not modify Trellis upstream files.
It is idempotent: identical files are skipped, missing files are installed,
Guru-managed companion assets are upgraded in place with `.bak` backups,
existing `.trellis/guru-team/config.yml` is preserved, known upstream
Trellis-generated entry files are replaced with Guru Team overlays, and unknown
local modifications are preserved by writing `.new` copies.

## Apply

```bash
git clone https://github.com/castbox/guru-trellis.git /path/to/guru-trellis
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project
```

## Installed Files

- `.trellis/guru-team/config.yml`
- `.trellis/guru-team/schemas/intake-handoff.schema.json`
- `.trellis/guru-team/scripts/bash/check-env.sh`
- `.trellis/guru-team/scripts/bash/prepare-task.sh`
- `.trellis/guru-team/scripts/bash/review-branch.sh`
- `.trellis/guru-team/scripts/bash/check-review-gate.sh`
- `.trellis/guru-team/scripts/bash/publish-pr.sh`
- `.trellis/guru-team/scripts/bash/finish-work.sh`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `.agents/skills/trellis-start/SKILL.md`
- `.agents/skills/trellis-continue/SKILL.md`
- `.agents/skills/trellis-finish-work/SKILL.md`
- `.codex/prompts/trellis-start.md`
- `.codex/prompts/trellis-continue.md`
- `.codex/prompts/trellis-finish-work.md`
- `.codex/skills/trellis-start/SKILL.md`
- `.codex/skills/trellis-continue/SKILL.md`
- `.codex/skills/trellis-finish-work/SKILL.md`
- `.claude/commands/trellis/continue.md`
- `.claude/commands/trellis/finish-work.md`
- `.cursor/commands/trellis-continue.md`
- `.cursor/commands/trellis-finish-work.md`

The active `.trellis/workflow.md` is installed or switched through the official
Trellis workflow marketplace:

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis \
  --template guru-team
```

The daily user-facing entry points are natural-language task requests, issue
URLs or issue numbers, `trellis-continue`, and `trellis-finish-work`. The
`trellis-start` overlay remains installed as a fallback / explicit orientation
entry for platforms without automatic startup injection, disabled or unapproved
hooks, suspected bootstrap failures, or manual context reloads.

Review and publish helpers are internal companion script subcommands used by
the workflow; they are not daily user-facing entries.
