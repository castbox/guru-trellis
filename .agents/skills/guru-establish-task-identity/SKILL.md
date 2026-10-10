---
name: guru-establish-task-identity
description: Resolve an immutable TaskId and its current source relation, requesting fresh review for ambiguous legacy source.
---

# Establish Task Identity

Read the exact active TaskId, generation and task artifact. Current
`task.json.source` wins; only the canonical legacy Issue scope may be
normalized automatically. For other legacy tasks, review the source relation
from fresh authority before supplying `reviewed_source`; that judgment cannot
be made by the script. No tracked task or runtime mapping is written.

Use `scripts/invoke.sh --root <task-checkout> --input -`. Return exactly one
typed exit; invalid or duplicate task identities fail closed.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
