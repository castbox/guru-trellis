<!-- guru-team-overlay: v1 -->
# Guru Team Finish Work

`trellis-finish-work` is the only user-facing closeout and recovery entry. Do not expose a separate publish command, `--skip-archive`, or `--recovery-after-finish-work`.

Validate the portable worktree boundary before reading or writing task-local artifacts:

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>
```

Create and AI-review task-local `pr-body.md` and `finish-summary-index.json`. The Chinese body must contain concrete `变更摘要`, `影响范围`, `验证结果`, `Review Gate`, `Issue 关闭范围`, `安全说明`, and `Docs SSOT` / `文档同步`; only ledger `close_issues` may use `Closes #xx`.

Run dry-run first:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file "{TASK_DIR}/finish-summary-index.json" \
  --body-file "{TASK_DIR}/pr-body.md" \
  --dry-run
```

Review the complete `closeout_plan` and pass its digest unchanged:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file "{TASK_DIR}/finish-summary-index.json" \
  --body-file "{TASK_DIR}/pr-body.md" \
  --expected-plan-digest "<closeout_plan_digest>"
```

Dry-run and formal use the same prepare validators. Formal finish pushes the reviewed content HEAD, records deterministic marketplace evidence, commits plan/readiness/evidence, binds one exact draft PR, builds the only final summary before archive, validates the future archive projection, calls official `task.py archive --no-commit`, creates and pushes one exact archive metadata commit, checks local/remote/PR HEAD equality, then marks the PR ready. It never rewrites repo artifacts after archive.

Prepare accepts only missing/empty official `hooks.after_archive` and rejects non-empty or unparsable config without executing it. Immediately before official move it rechecks the live archive month, regular-file/mode/blob continuity, empty index, and exact planned untracked outputs.

On failure, rerun this same entry with the same digest. Recovery derives the unique next transition from committed plan/readiness, active/archive locators, Git/remote facts, and PR identity. Multiple PR matches, input drift, unexpected metadata paths, and HEAD mismatch fail closed.
The exception is `archive-month-preflight`: keep the active task/draft PR, rerun dry-run, review the new digest, and formalize that digest. This may append only a plan/readiness supersession evidence commit; it never rewrites history or migrates an archive directory.

Run `resolve-human-artifacts.sh --json --task <task-path>` and show the active-task `Markdown 产物 review 表` after dry-run, then rerun it for the archived-task table after success. The table lists only `prd.md`, `design.md`, `implement.md`, `review.md`, and `pr-body.md`. Guru Team never calls `add_session.py` or reads/writes `.trellis/workspace/**`.
