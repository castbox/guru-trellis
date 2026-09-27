---
name: guru-cleanup-task-resources
description: Clean sealed Guru-owned resources or explicitly selected manual and machine-handoff targets.
---

# Guru Cleanup Task Resources

Normal Cleanup consumes only ResourceSealRefDTO and resolves Guru-owned
incarnations from the common-dir ledger. It preserves caller-owned and unknown
resources. Manual cleanup requires explicit target selection, fresh validation
and its own deletion confirmation; machine handoff has a separate profile.
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

Manual cleanup records the exact selected result without assigning Guru
ownership. A retained caller-owned resource is identified by the ledger's
resource ID, kind and portable ref; its newly reviewed selected HEAD is the
deletion lease, not the historical Finish HEAD. Current branch bindings in the
Git common-dir block deletion even if the invoking checkout contains only an
older archived task generation. Machine handoff reads a released source inventory and resolves only
its Guru-owned pending local resources. Both require independent deletion
confirmation and can reread a recorded result after output loss. The active
#434 workflow invokes normal Cleanup after Finish; this package does not
choose the global consumer route.
