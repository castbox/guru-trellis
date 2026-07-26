---
name: guru-finalize-task
description: Finalize a reviewed Trellis task through one semantic closeout loop, one deterministic transaction engine, and six typed exits.
---

# Guru Finalize Task

Use this Skill only after publication review is current, or when explicitly
resuming a previously prepared finalization.

1. Read `references/contract.md` completely.
2. Validate the selected public input profile and every owner precondition.
3. Run the side-effect-free preview or current-state discovery.
4. Perform the AI Review Gate and obtain exact plan-digest confirmation when
   the contract requires it.
5. Record and check the private gate before any deterministic transition.
6. Emit exactly one declared typed exit.

`judgment_mode=semantic`. Scripts execute, record, and validate deterministic
facts; they never choose scope, readiness, recovery intent, or semantic pass.
Unknown, missing, multiple, stale, or consumer-mismatched results stop fail
closed.
