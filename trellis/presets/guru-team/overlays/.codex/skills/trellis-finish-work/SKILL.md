---
name: trellis-finish-work
description: "Guru Team Trellis finish entry. Use after task work is committed and Branch Review Gate passed; archives task, records journal, then publishes a non-draft PR."
---

<!-- guru-team-overlay: v1 -->

# Guru Team Trellis Finish Work

Finish-work is the only user-facing closeout entry. Do not ask the user to remember a separate publish command.

Run the internal Guru Team finish helper:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json
```

The helper verifies the current HEAD has a passed Branch Review Gate, rejects uncommitted non-metadata changes, archives the active task, records the session journal, commits any remaining Trellis metadata-only changes, then internally calls `publish-pr` to push and create a non-draft PR with a Chinese title and body. Direct `publish-pr` is not the normal path and is reserved for explicit recovery/debug after finish-work. The helper does not perform review itself; the gate must already record reviewer or review-report evidence, Docs SSOT reconciliation, and any required Middle-platform Knowledge Gate evidence.
