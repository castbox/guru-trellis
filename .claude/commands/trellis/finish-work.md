<!-- guru-team-overlay: v1 -->
# Guru Team Finish Work

Finish-work archives the task, records the journal, then automatically publishes a non-draft PR. There is no separate user-facing publish command.

Run the internal Guru Team finish helper:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work
```

The `--from-trellis-finish-work` marker is required proof that this explicit finish entrypoint was invoked; do not add it to `/trellis:continue`. The helper verifies the Branch Review Gate for the current HEAD, rejects uncommitted non-metadata changes, runs the normal Trellis archive and journal commands, commits any remaining Trellis metadata-only changes, then internally pushes and creates the PR. Direct `publish-pr` is not the normal path and is reserved for explicit recovery/debug after finish-work. It does not perform review itself; the gate must already record reviewer or review-report evidence, Docs SSOT reconciliation, and any required Middle-platform Knowledge Gate evidence.

PR title, section headings, and body must be Chinese. Only `close_issues` from `issue-scope-ledger.json` may use `Closes #xx`.
