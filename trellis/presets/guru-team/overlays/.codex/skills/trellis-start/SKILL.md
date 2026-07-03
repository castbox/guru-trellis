---
name: trellis-start
description: "Guru Team Trellis session entry. Use when beginning a new task or re-establishing Trellis context; keeps user-facing workflow on start / continue / finish-work."
---

<!-- guru-team-overlay: v1 -->

# Guru Team Trellis Start

Initialize context through the normal Trellis start entry point. Do not introduce a new user-facing command.

1. Run:

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode phase
```

2. If there is no active task and durable work is needed, follow `.trellis/workflow.md` Phase 0:

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json "<user request, issue number, or issue URL>"
```

3. Keep planning artifacts in Chinese: `prd.md`, `design.md`, `implement.md`, and human-readable review fields.

4. Treat `.trellis/guru-team/handoff.json` as intake provenance only. Final close/ref/followup scope belongs in the task-level `issue-scope-ledger.json`.

Full contract lives in `.trellis/workflow.md`.
