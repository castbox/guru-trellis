---
name: guru-discover-change-context
description: Discover fresh current and archived change context, run the semantic evidence gate, and produce a portable snapshot before Guru Team requirement clarification.
---

# Guru Discover Change Context

Use this Skill after `guru-sync-base:synced`, or when a standalone caller asks
to discover change context from a fresh base with explicit issue, request,
path, command, config, schema, or symbol clues.

Load [references/contract.md](references/contract.md). Execute its semantic
closed loop in the declared order, complete the AI Review Gate before any
recorder/validator, then return exactly one declared typed exit.

Use the dispatcher-only wrappers for history preview, snapshot recording, and
snapshot checking. Pre-task recording is stdout-only. Post-task recording may
write only the exact expected snapshot to task-local `context-discovery.json`.
For `refresh_base`, pass one repeatable `--prior-snapshot-input` /
`--expected-prior-snapshot-sha256` pair for every refresh-history entry, ordered
from the oldest `context_ready` ancestor through the direct prior. For `N`
entries also pass `N-1` independently retained
`--prior-refresh-receipt-input` /
`--expected-prior-refresh-receipt-sha256` pairs in hop order. A single refresh
keeps the existing one-ancestor-pair CLI form without a receipt. Never embed
external evidence bytes in the new artifact. Task-local recording/checking must
also prove that the exact artifact target is not ignored by Git; pre-task mode
remains stdout-only.

Fail closed on stale base/live/blob/query/archive identity, unsafe evidence,
unknown exits, or missing compatible runtime. This package is not
self-contained or portable.
