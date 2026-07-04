---
name: trellis-finish-work
description: "Guru Team Trellis finish entry. Use after task work is committed and Branch Review Gate passed; archives task, records journal, then publishes a non-draft PR."
---

<!-- guru-team-overlay: v1 -->

# Guru Team Trellis Finish Work

Finish-work is the only user-facing closeout entry. Do not ask the user to remember a separate publish command.

Before running the helper, generate or review the PR body for GitHub reviewers
who do not know the Trellis task. The body must be Chinese and self-explanatory:
`变更摘要`, `影响范围`, `验证结果`, `Review Gate`, `Issue 关闭范围`, and
`安全说明` must contain concrete content. Do not use low-information summaries
such as `当前 Trellis task`, `已提交实现与文档更新`, or `详见 artifact`.
Write the reviewed Markdown body to a task-local file and pass it with
`--body-file <path>`, or pass a task-local JSON readiness artifact with
`--body-artifact <path>`. Non-draft publish requires one of these reviewed
sources; script-generated `generated` bodies are preview/draft-only and do not
count as readiness evidence. The readiness/body files are Trellis task metadata
and publish reads the final body from the archived task artifact after archive.

Run the internal Guru Team finish helper:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work
```

The `--from-trellis-finish-work` marker is required proof that this explicit finish entrypoint was invoked; do not add it to `trellis-continue`. The helper verifies the passed Branch Review Gate, allowing only Trellis metadata such as `review.md` / `review-gate.json` after the reviewed HEAD; rejects uncommitted non-metadata changes; archives the active task; records the session journal; commits any remaining Trellis metadata-only changes; then internally calls `publish-pr` to push and create a non-draft PR with a Chinese title and body. Direct `publish-pr` is not the normal path and is reserved for explicit recovery/debug after finish-work. The helper does not perform review itself; the gate must already record task-local `review.md` as `review_report` digest evidence, Docs SSOT reconciliation, and any required Middle-platform Knowledge Gate evidence.
