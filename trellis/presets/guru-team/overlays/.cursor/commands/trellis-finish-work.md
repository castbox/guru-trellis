<!-- guru-team-overlay: v1 -->
# Guru Team Finish Work

Finish-work archives the task, records the journal, then automatically publishes a non-draft PR. There is no separate user-facing publish command.

Run the internal Guru Team finish helper:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json
```

The helper verifies the Branch Review Gate for the current HEAD, rejects uncommitted non-metadata changes, runs the normal Trellis archive and journal commands, commits any remaining Trellis metadata-only changes, then pushes and creates the PR.

PR title, section headings, and body must be Chinese. Only `close_issues` from `issue-scope-ledger.json` may use `Closes #xx`.
