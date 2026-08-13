---
name: guru-finalize-task
description: Finalize a reviewed Trellis task through one semantic closeout loop, one deterministic transaction engine, and six typed exits.
---

# Guru Finalize Task

Use only after `guru-review-task-publication:ready`, or for one declared
same-owner resume/reprepare profile. Read `references/contract.md` before use.

The current business closeout graph never invokes
`guru-verify-extension-installation`, never requests a `not_required` result,
and never reads verifier DTOs, checkpoints, refs, or task artifacts. After the
reviewed content push, continue directly through Draft PR binding, archive,
archive push, Ready transition, and `guru-merge-task-pr` handoff.

Execute the semantic profile in order: preview, AI review, one exact bounded
side-effect confirmation when required, gate record/check, deterministic
transition, and exactly one typed exit. Unknown, multiple, retired, stale, or
unmapped inputs and exits fail closed. Retired verification re-entry input
requires a fresh current Publication result and full Finalizer reprepare.
