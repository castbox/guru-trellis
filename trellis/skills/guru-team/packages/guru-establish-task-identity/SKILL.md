---
name: guru-establish-task-identity
description: Resolve an immutable TaskId and its current source relation, requesting fresh review for ambiguous legacy source.
---

# Establish Task Identity

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Use `delivery_active_task`. Read the exact TaskId, generation and artifact
through the installed upstream Task schema-2 parser. Current `task.json.source`
is authoritative; this owner never changes overall scope or Delivery stage.
Old Task headers reserve identity and are migration/history diagnostics only.
Do not infer a new public generation or Delivery identity from legacy status,
cycle, path or source hints. Missing or mixed schema stops for the original
migration owner; no tracked Task or runtime mapping is written.

Use `scripts/invoke.sh --root <task-checkout> --input -`. Return exactly one
typed exit; invalid or duplicate task identities fail closed.

For `task_not_found`, identify the missing TaskRef and stop dependent identity
consumers. A branch name or candidate scan cannot restore the carrier. When
the current request selects same-identity recovery, use the original Branch
owner's [complete recovery contract](../guru-establish-task-branch-binding/references/task-carrier-recovery.md):
fix one retrievable Git commit and inspect its TaskId/generation, source/scope,
Delivery, full planning files and actual historical gaps before a reviewed
exact file restore. An ambiguous identity/source or unsupported schema remains
with this Identity or the original migration owner; do not create a replacement
Task, increment generation or manufacture missing gates.

After the original Git/file and base-branch writers finish, reread the restored
workspace through this same public entry. Identity can read the workspace
Task even when an unbound branch's HEAD tree lacks it. That success proves
identity only; the original Branch/Ensure owners still establish and validate
the current environment's resource relationship before receiving-session Bind.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
