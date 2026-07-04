<!-- guru-team-overlay: v1 -->
# Guru Team Finish Work

Finish-work archives the task, records the journal, then automatically publishes a non-draft PR. There is no separate user-facing publish command.

Run the internal Guru Team finish helper:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work
```

The `--from-trellis-finish-work` marker is required proof that this explicit finish entrypoint was invoked; do not add it to `/trellis-continue`. The helper verifies the passed Branch Review Gate, allowing only Trellis metadata such as `review.md` / `review-gate.json` after the reviewed HEAD; rejects uncommitted non-metadata changes; runs the normal Trellis archive and journal commands; commits any remaining Trellis metadata-only changes; then internally pushes and creates the PR. Direct `publish-pr` is not the normal path and is reserved for explicit recovery/debug after finish-work. It does not perform review itself; the gate must already record task-local `review.md` as `review_report` digest evidence, Docs SSOT reconciliation, and any required Middle-platform Knowledge Gate evidence.

PR title, section headings, and body must be Chinese. Only `close_issues` from `issue-scope-ledger.json` may use `Closes #xx`.
