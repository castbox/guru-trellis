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
Task-local recording/checking must also prove that the exact artifact target is
not ignored by Git; pre-task mode remains stdout-only. A caller-authored
`refresh_base` result records the observed stale codes and superseded digests,
then re-enters the complete Skill through `guru-sync-base`.

Fail closed on stale base/live/blob/query/archive identity, invalid evidence,
unknown exits, or missing compatible runtime. This package is not
self-contained or portable.

After the semantic gate and owner recorder/checker complete, invoke
`scripts/invoke.sh --input <declared-profile.json> --owner-result <repo-relative-context-result>`
to serialize the minimal handoff. The runtime reruns the existing checker and
derives the route from its checked `typed_exit`; callers never name the expected
exit. Consumers receive caller-owned continuation only, never the private
context snapshot body.
