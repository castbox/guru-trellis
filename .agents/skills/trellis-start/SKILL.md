---
name: trellis-start
description: "Guru Team Trellis fallback orientation entry. Use when automatic startup context is unavailable, hooks did not run, or the user explicitly asks to reload current Trellis context."
---

<!-- guru-team-overlay: v1 -->

# Guru Team Trellis Start Fallback

This is a thin fallback loader, not an intake or task-mutation workflow.

1. Read `.trellis/workflow.md` and use it as the only global route contract.
2. Before repository, GitHub, Docs, code, test, history, or task reads, classify
   the request from already injected state. A new repo-changing route performs
   the mandatory invoke `guru-sync-base`; consume only its declared workflow
   exit. Let the
   workflow invoke every later owner Skill. Do not call `prepare-task` or copy
   any Skill's review, confirmation, recorder, recovery, or mutation steps here.
3. For active-task orientation or a non-new-work route, load the fixed Guru Team
   no-workspace context set:

```bash
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode packages
python3 ./.trellis/scripts/task.py current --source
git branch --show-current
git status --short --branch
```

Do not open, enumerate, read, summarize, or infer from `.trellis/workspace/`.

4. Report the current task/status, the next workflow-owned Skill or the real
   blocker. Apply the workflow's global interaction contract: automatically
   consume mapped exits and ask `确认继续` only for one fully displayed current,
   unique, unambiguous proposal or side effect. Never require a SHA, digest, or
   fixed reply text.

This entry does not create or update an Issue, task, worktree, branch, runtime
checkpoint, handoff, commit, push, PR, archive, or cleanup resource.
