---
name: guru-establish-task-identity
description: Resolve an immutable TaskId and its current source relation, requesting fresh review for ambiguous legacy source.
---

# Establish Task Identity

Use `delivery_active_task`. Read the exact TaskId, generation and artifact
through the installed upstream Task schema-2 parser. Current `task.json.source`
is authoritative; this owner never changes overall scope or Delivery stage.
Old Task headers reserve identity and are migration/history diagnostics only.
Do not infer a new public generation or Delivery identity from legacy status,
cycle, path or source hints. Missing or mixed schema stops for the original
migration owner; no tracked Task or runtime mapping is written.

Use `scripts/invoke.sh --root <task-checkout> --input -`. Return exactly one
typed exit; invalid or duplicate task identities fail closed.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
