---
name: guru-discover-change-context
description: Discover fresh current and archived change context, run the semantic evidence gate, and hand minimal current identity to Guru Team requirement clarification.
---

# Guru Discover Change Context

Use this Skill after `guru-sync-base:synced`, or when a standalone caller asks
to discover change context from a fresh base with explicit issue, request,
path, command, config, schema, or symbol clues.

Load [references/contract.md](references/contract.md). Execute its semantic
closed loop in the declared order, complete the AI Review Gate before any
recorder/validator, then return exactly one declared typed exit.

Use the dispatcher-only wrappers for history preview, owner-result recording,
and owner-result checking. Normal recording/checking is stdin/stdout-only and
does not create a repository artifact. A caller-authored `refresh_base` result
records only the observed current stale codes, then reruns the complete Skill
through `guru-sync-base` and live authority.

Only when this same owner is genuinely interrupted for an active task, record
the validated result with `--recovery-task <task> --recovery-continuation-id
<id>`. This lazily creates one minimal ignored checkpoint. On recovery, rerun
the complete owner from live authority, check with the same two arguments, and
invoke the public wrapper with `--owner-task <task>
--owner-continuation-id <id>` so successful DTO validation consumes it.

Fail closed on stale base/live/blob/query/archive identity, invalid evidence,
unknown exits, or missing compatible runtime. This package is not
self-contained or portable.

After the semantic gate and owner recorder/checker complete, invoke
`scripts/invoke.sh --input <declared-profile.json> --owner-result -` with the
checked owner result on stdin
to serialize the minimal handoff. The runtime reruns the existing checker and
derives the route from its checked `typed_exit`; callers never name the expected
exit. Consumers receive caller-owned continuation only, never the private
owner-result body.
