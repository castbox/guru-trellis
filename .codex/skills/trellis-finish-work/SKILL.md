---
name: trellis-finish-work
description: "Guru Team Trellis finish entry. Use after task work is committed and Branch Review Gate passed; binds an immutable closeout plan, creates a draft PR, archives once, then marks the PR ready."
---

<!-- guru-team-overlay: v1 -->

# Guru Team Trellis Finish Work

`trellis-finish-work` is the only user-facing closeout and recovery entry. Do
not ask the user to choose a publish command, `--skip-archive`, or
`--recovery-after-finish-work`.

Before reading or writing task artifacts, resolve the portable worktree identity
from the current checkout, `.trellis/.runtime/guru-team/**`, and
`git worktree list`, then require:

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>
```

Create and AI-review task-local `pr-body.md` and
`finish-summary-index.json`. The Chinese PR body must contain concrete
`变更摘要`, `影响范围`, `验证结果`, `Review Gate`,
`Issue 关闭范围`, `安全说明`, and `Docs SSOT` / `文档同步`.
Only `close_issues` may use `Closes #xx`. The semantic summary index contains
judgment and non-factual search terms; the companion injects GitHub, Git, path,
artifact, and time facts.

Run the side-effect-free prepare pipeline first:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file "{TASK_DIR}/finish-summary-index.json" \
  --body-file "{TASK_DIR}/pr-body.md" \
  --dry-run
```

Review the complete `closeout_plan` and save its
`closeout_plan_digest`. Formal finish must pass that digest unchanged:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file "{TASK_DIR}/finish-summary-index.json" \
  --body-file "{TASK_DIR}/pr-body.md" \
  --expected-plan-digest "<closeout_plan_digest>"
```

Dry-run and formal execution share `prepare_closeout()`. Formal finish compares
the digest before its first side effect, pushes the reviewed content HEAD,
records deterministic pending/passed marketplace evidence, commits and pushes
plan/readiness/evidence, creates or reuses one exact draft PR, builds the only
final summary with canonical PR URL and one `PR #<number>` ref, validates the
future archive projection, then calls official `task.py archive --no-commit`.
It creates one exact archive metadata commit, pushes it, requires local/remote/PR
HEAD equality, and only then runs draft to ready. After archive it must not
rebuild or rewrite repo artifacts.

If any stage fails, rerun this same entry with the same expected digest. The
state machine resumes from committed plan/readiness, active/archive locators,
Git/remote facts, and the unique PR identity. Multiple matching PRs, protected
input drift, unexpected metadata paths, or HEAD mismatch fail closed.

After dry-run, run `resolve-human-artifacts.sh --json --task <task-path>`
against the active task and show the `Markdown 产物 review 表`. After formal finish, run the same resolver against the archived task and include its archived table. The resolver lists only `prd.md`, `design.md`,
`implement.md`, `review.md`, and `pr-body.md`. Guru Team never calls
`add_session.py` and never reads or writes `.trellis/workspace/**`.
