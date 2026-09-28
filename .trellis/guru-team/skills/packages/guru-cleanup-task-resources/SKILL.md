---
name: guru-cleanup-task-resources
description: Clean sealed Guru-owned resources or explicitly selected manual and machine-handoff targets.
---

# Guru Cleanup Task Resources

Normal Cleanup consumes only ResourceSealRefDTO and resolves Guru-owned
incarnations from the common-dir ledger. It preserves caller-owned and unknown
resources. Missing terminal ownership returns `manual_cleanup_required` with
call-local live candidates; it does not reconstruct or persist ownership.
`select_explicit_cleanup_targets` first accepts an empty
`selected_candidate_ids` list with the exact terminal Finish identity and
returns the live candidates. Its next call accepts only selected candidate IDs
from that result.
Machine handoff has a separate profile.

For #454, the former public `manual` profile and `manual_selection_required`
exit are retired without aliases. Callers replace `selected_targets` with
`selected_candidate_ids` from the current `manual_cleanup_required` output.
The changed input, semantic-result and aggregate-output schema IDs are 3.0;
the unchanged normal and machine-handoff output shapes retain their IDs.
Invoke from a retained checkout of the same Git common-dir that is outside
the selected deletion set (`--root` may name that checkout). After Finish in a
linked task worktree, first move the Cleanup invocation to the retained
checkout. If none is available, stop for manual disposition; do not attempt
to remove the invoking checkout.

Every deletion checks exact Git ref/HEAD and registered worktree state again.
An absent resource converges through the same ledger resolution. Normal cleanup
removes linked worktrees, then local branches, then remote branches under exact
HEAD checks. A moved or dirty target blocks the affected action. The shared
ledger resolves the complete Guru-owned pending set only after deletion.
Caller-owned retained resources are never included in normal deletion. An exact
common-dir result receipt lets the same Finish seal input recover the same
`cleaned` output after successful deletion and lost output; an unrelated stale
inventory still blocks.

Candidate IDs bind repository common-dir, resource kind/ref, registered checkout
path where applicable, and live HEAD. The AI reviews the selected IDs and
rediscovers every resource, requiring the same repository, identity, HEAD,
registered worktree state, clean worktree and current non-use. It then shows
an exact deletion plan naming each selected branch, worktree path or remote ref,
and gets a fresh confirmation in the current dialogue before invoking deletion.
Unselected candidates remain untouched. A stale candidate, dirty worktree or
current resource returns `blocked`. A retained caller-owned resource can be
selected explicitly, but normal Cleanup never deletes it. Selection does not
assign Guru ownership or create historical ownership. Current branch bindings
in the Git common-dir block deletion even if the invoking checkout contains
only an older archived task generation. Machine handoff reads a released source inventory and resolves only
its Guru-owned pending local resources. Both require independent deletion
confirmation and can reread a recorded result after output loss. The active
#434 workflow invokes normal Cleanup after Finish; this package does not
choose the global consumer route.
