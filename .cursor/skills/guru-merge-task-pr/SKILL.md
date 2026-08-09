---
name: guru-merge-task-pr
description: Merge one Ready task PR through a semantic live gate, expected-head mutation, and post-merge closure verification.
---

# Guru Merge Task PR

Use this Skill only for the remote post-publication merge boundary. In workflow
mode consume `guru-finalize-task:ready_for_merge`; in standalone mode accept one
repo-bound PR identity and rebuild the same live evidence.

Read [references/contract.md](references/contract.md), run the preview, perform
the semantic gate, and ask once for the exact merge action. After confirmation,
record/check the gate, execute with the expected head, and return exactly one of
`merged`, `merge_blocked`, or `closure_mismatch`.

Fail closed on stale head, Draft/Open/readiness drift, unknown policy, missing
close scope, incomplete GitHub response, or unmapped output. Never enter Phase
0, sync a base, update/rebase the PR branch, close Issues directly, synchronize
local `main`, or clean task resources.
