---
name: guru-finalize-task
description: Finalize a reviewed Trellis task through one semantic closeout loop, one deterministic transaction engine, and six typed exits.
---

# Guru Finalize Task

Use only after `guru-review-task-publication:ready`, or for one declared
same-owner resume/reprepare profile. Read `references/contract.md` before use.

The current business closeout graph never invokes
`guru-verify-extension-installation`, never requests a `not_required` result,
and never reads verifier DTOs, checkpoints, refs, or task artifacts. Ordinary
publication continues through a new Draft PR. A separately previewed
`existing_pr_recovery` may adopt only the unique same-repository Open PR whose
remote/PR HEAD is a strict ancestor of the publication HEAD. Equality is
accepted only after that exact pre-push HEAD is transaction-bound, then converge
the current Publication title/body, archive, preserve Ready or mark Draft
Ready, and hand off to `guru-merge-task-pr`.

Execute the semantic profile in order: preview, AI review, one exact bounded
side-effect confirmation when required, gate record/check, deterministic
transition, and exactly one typed exit. Unknown, multiple, retired, stale, or
unmapped inputs and exits fail closed. Retired verification re-entry input
requires a fresh current Publication result and full Finalizer reprepare.
An already Ready same-plan transaction is a terminal read-only recovery: live
facts are revalidated and the current Merge DTO is materialized without
repeating any Git or GitHub mutation.
