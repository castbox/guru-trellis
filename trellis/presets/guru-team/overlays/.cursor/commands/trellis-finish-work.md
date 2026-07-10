<!-- guru-team-overlay: v1 -->
# Guru Team Finish Work

Finish-work archives the task, records the journal, then automatically publishes a non-draft PR. There is no separate user-facing publish command.

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

Run the internal Guru Team finish helper as a dry-run readiness preview first:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --body-file "{TASK_DIR}/pr-body.md" \
  --dry-run
```

Only after reviewing the dry-run output, run the formal finish:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
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

The `--from-trellis-finish-work` marker is required proof that this explicit finish entrypoint was invoked; do not add it to `/trellis-continue`. The helper verifies the passed Branch Review Gate, allowing only Trellis metadata such as `review.md`, `reviews/*.md`, `agent-assignment.json`, `review-gate.json`, and PR readiness files after the reviewed HEAD; rejects uncommitted non-metadata changes; runs the normal Trellis archive and journal commands; commits any remaining Trellis metadata-only changes; then internally pushes the reviewed content branch, runs deterministic remote marketplace init/preview/switch/preset-reapply verification, records schema-valid task-local `marketplace-verification.json`, replaces required structured pending evidence in primary/close Issue Scope Ledger entries with real verifier facts, commits exactly the artifact plus ledger as the metadata-only tail, pushes it, cross-validates artifact SHA-256/content HEAD/remote HEAD against the ledger, rechecks the exact two-path tail and Branch Review Gate, and only then creates the PR. Missing, pending, failed, tampered, or stale verification blocks before `gh pr create`; no tag is created. Durable docs, `.trellis/spec/`, source, tests, schema, config, scripts, preset, overlay, CI/CD, deployment, migration, or Makefile drift after the gate must return to Phase 2/3; finish-work/archive must not first merge durable docs or patch missing Docs SSOT work. Direct `publish-pr` is not the normal path and is reserved for explicit recovery/debug after finish-work. It does not perform review itself; the gate must already record task-local `review.md` as `review_report` digest evidence and raw `review_reports[]` digest evidence for every review round, and those Markdown reports must already be Chinese human-readable task artifacts except for literal command/path/JSON/HEAD/API/code tokens; when sub-agents were used it should already record `agent-assignment.json` digest/roles evidence. Docs SSOT reconciliation and any required Middle-platform Knowledge Gate evidence must also be present.

PR title, section headings, and body must be Chinese. Only `close_issues` from `issue-scope-ledger.json` may use `Closes #xx`.
