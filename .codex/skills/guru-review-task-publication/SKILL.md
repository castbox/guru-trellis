---
name: guru-review-task-publication
description: Review task publication readiness through ten semantic dimensions, metadata-only revision, one private gate, and three typed exits.
---

# Guru Review Task Publication

Use after `guru-review-branch:passed`, or for a checker-declared stale
finalization handback. Read `references/contract.md`, author the selected public
input profile, complete the semantic review, then call the package recorder and
checker through the shared dispatcher.

Never treat scanner success, empty findings, changed-file classification, a
legacy `ready=true` snapshot, or script success as semantic pass. Metadata-only
revision remains inside this Skill and requires a fresh complete review.

Emit exactly one declared typed exit. Missing, stale, ambiguous, multiple,
unmapped, or checker-failed evidence fails closed.
