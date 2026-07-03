---
name: trellis-start
description: "Guru Team Trellis fallback orientation entry. Use when automatic startup context is unavailable, hooks did not run, or the user explicitly asks to reload full Trellis context."
---

<!-- guru-team-overlay: v1 -->

# Guru Team Trellis Start Fallback

Use this entry as fallback / explicit orientation. In normal auto-bootstrap platforms, users can describe the task, paste an issue URL, or say "handle issue #123"; the AI should classify that request from injected Trellis context, workflow-state, startup context, hook breadcrumbs, or skill matching.

Run this start entry when the platform has no automatic session/startup injection, hooks are disabled or unapproved, bootstrap appears not to have run, or the user asks for a full context report / reload.

1. Run:

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode phase
```

2. If there is no active task and the user's natural-language request is issue-backed, task-like, or requires file changes, follow `.trellis/workflow.md` Phase 0:

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json "<user request, issue number, or issue URL>"
```

3. Ask for consent before creating a GitHub issue, worktree, branch, or Trellis task unless the user explicitly requested that side effect.

4. Keep planning artifacts in Chinese: `prd.md`, `design.md`, `implement.md`, and human-readable review fields.

5. During planning, follow `.trellis/workflow.md` for Middle-platform Knowledge Gate and Repo Docs SSOT discovery. MCP availability is checked from current AI tools/capabilities, not shell scripts.

6. Treat `.trellis/guru-team/handoff.json` as intake provenance only. Final close/ref/followup scope belongs in the task-level `issue-scope-ledger.json`.

Full contract lives in `.trellis/workflow.md`.
