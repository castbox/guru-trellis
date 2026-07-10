---
name: trellis-finish-work
description: "Guru Team Trellis finish entry. Use after task work is committed and Branch Review Gate passed; archives task, records finish-summary, then publishes a non-draft PR."
---

<!-- guru-team-overlay: v1 -->

# Guru Team Trellis Finish Work

Finish-work is the only user-facing closeout entry. Do not ask the user to remember a separate publish command.

Before reading or writing task-local closeout artifacts, treat `task-start-context.json` as portable identifiers only (`workspace_slug`, `task_workspace_id`, and repo-relative `task_artifact_dir`). Resolve the machine-local task worktree from the current checkout, `.trellis/.runtime/guru-team/**`, and `git worktree list`, then require `.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>` to confirm it. Never read an absolute `workspace_path` from committed task context.

Before running the helper, generate or review the PR body for GitHub reviewers
who do not know the Trellis task. The body must be Chinese and self-explanatory:
`变更摘要`, `影响范围`, `验证结果`, `Review Gate`, `Issue 关闭范围`, and
`安全说明` must contain concrete content. It must also include a `Docs SSOT` /
`文档同步` result with the plan strategy, durable docs updates or no-update
reason, task delta merged back, task-history-only content, and any follow-up or
current PR limitation. Do not use low-information summaries such as
`当前 Trellis task`, `已提交实现与文档更新`, or `详见 artifact`.
Write the reviewed Markdown body to the task-local file
`{TASK_DIR}/pr-body.md` and pass it with `--body-file "{TASK_DIR}/pr-body.md"`.
A task-local JSON readiness artifact passed with `--body-artifact <path>` is
also accepted, but the main flow should use the reviewed Markdown file.
Non-draft publish requires one of these reviewed sources; script-generated
`generated` bodies are preview/draft-only and do not count as readiness
evidence. The readiness/body files are Trellis task metadata and publish reads
the final body from the archived task artifact after archive.

Create and AI-review `{TASK_DIR}/finish-summary-index.json` before dry-run. It
contains semantic problem/outcome/behavior/surface/contract judgment plus
non-factual command/config/schema/symbol/phrase search terms; the companion
injects issue, PR, branch, path, commit, artifact, and time facts.
The AI input accepts at most 19 `contract_changes`; the final summary accepts
20 so the recorder can append the fixed protected-path filtering fact.

Run the internal Guru Team finish helper as a dry-run readiness preview first:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file "{TASK_DIR}/finish-summary-index.json" \
  --body-file "{TASK_DIR}/pr-body.md" \
  --dry-run
```

Only after reviewing the dry-run output, run the formal finish:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file "{TASK_DIR}/finish-summary-index.json" \
  --body-file "{TASK_DIR}/pr-body.md"
```

After dry-run, run `resolve-human-artifacts.sh` against the active task and
include an active-task `Markdown 产物 review 表`:

```bash
.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh --json --task <task-path>
```

After the formal finish archives the task, run the resolver again against the
archived task name or archive path and include the archive-path
`Markdown 产物 review 表` in the final reply. The table lists only `prd.md`,
`design.md`, `implement.md`, `review.md`, and `pr-body.md`; missing files must
not be rendered as Markdown links, and JSON artifacts stay out of the standard
table.

The `--from-trellis-finish-work` marker proves this explicit entrypoint was invoked; do not add it to `trellis-continue`. The helper validates the gate and AI index, archives the task, writes schema-valid initial `finish-summary.json`, commits task metadata, verifies any remote marketplace change, and creates the PR. It never calls `add_session.py` or reads/writes `.trellis/workspace/**`. Initial and final summaries sort and deduplicate raw Git paths, filter workspace/runtime protected prefixes, write the safe set to both path arrays, and add exactly one fixed non-disclosing contract fact only when filtering occurred; schema/validator path fields have no protected-prefix exception. After PR creation it rewrites URL and PR ref, then commits and pushes exactly the archived summary path without reopening Branch Review Gate. Any non-task metadata path fails. A post-PR failure preserves the URL and executable recovery command. Recovery revalidates repo/base/head, reviewed body/readiness, gate, and current/remote HEAD, then queries the current repo/head/base before create: one open PR is reused, zero triggers one same-input create retry, and multiple fail closed without create. A failed retry keeps the initial empty URL/refs and returns the same recovery command. Normal marketplace publish executes the verifier; recovery validates and reuses existing passed verifier evidence instead of rerunning it against a dirty/staged summary. Missing/stale marketplace or review evidence blocks, and no tag is created. Durable docs, source, tests, schema, config, scripts, preset, overlay, CI/CD, deployment, migration, or Makefile drift must return to Phase 2/3.
