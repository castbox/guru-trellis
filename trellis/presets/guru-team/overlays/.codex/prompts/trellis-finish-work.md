<!-- guru-team-overlay: v1 -->
# Guru Team Finish Work

Finish-work archives the task, records the journal, then automatically publishes a non-draft PR. There is no separate user-facing publish command.

Before running the helper, generate or review the PR body for GitHub reviewers
who do not know the Trellis task. The body must be Chinese and self-explanatory:
`变更摘要`, `影响范围`, `验证结果`, `Review Gate`, `Issue 关闭范围`, and
`安全说明` must contain concrete content. Do not use low-information summaries
such as `当前 Trellis task`, `已提交实现与文档更新`, or `详见 artifact`.
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

The `--from-trellis-finish-work` marker is required proof that this explicit finish entrypoint was invoked; do not add it to `trellis-continue`. The helper verifies the passed Branch Review Gate, allowing only Trellis metadata such as `review.md`, `reviews/*.md`, `agent-assignment.json`, `review-gate.json`, and PR readiness files after the reviewed HEAD; rejects uncommitted non-metadata changes; runs the normal Trellis archive and journal commands; commits any remaining Trellis metadata-only changes; then internally pushes and creates the PR. Direct `publish-pr` is not the normal path and is reserved for explicit recovery/debug after finish-work. It does not perform review itself; the gate must already record task-local `review.md` as `review_report` digest evidence, raw `review_reports[]` digest evidence for every review round, and when sub-agents were used it should already record `agent-assignment.json` digest/roles evidence; Docs SSOT reconciliation and any required Middle-platform Knowledge Gate evidence must also be present.

PR title, section headings, and body must be Chinese. Only `close_issues` from `issue-scope-ledger.json` may use `Closes #xx`.
