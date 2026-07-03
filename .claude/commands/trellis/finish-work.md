<!-- guru-team-overlay: v1 -->
# Guru Team Finish Work

Finish-work archives the task, records the journal, then automatically publishes a non-draft PR. There is no separate user-facing publish command.

Run the internal Guru Team finish helper:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json
```

The helper verifies the Branch Review Gate for the current HEAD, rejects uncommitted non-metadata changes, runs the normal Trellis archive and journal commands, commits any remaining Trellis metadata-only changes, then pushes and creates the PR. It does not perform review itself; the gate must already record reviewer or review-report evidence, Docs SSOT reconciliation, and any required Middle-platform Knowledge Gate evidence.

PR title, section headings, and body must be Chinese. Only `close_issues` from `issue-scope-ledger.json` may use `Closes #xx`.
