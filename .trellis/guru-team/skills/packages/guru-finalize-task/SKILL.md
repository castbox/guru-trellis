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

When ordinary pre-PR reprepare requires a provenance metadata tail, keep the
business target and Guru Trellis implementation in separate temporary
checkouts. The detached target checkout at `reviewed_content_head` is the only
`--repo` apply target and tail-commit owner. A second detached clean source
checkout supplies the canonical preset entry: self-hosted mode binds it to the
same repository at reviewed HEAD, while installed mode resolves the current
manifest's canonical immutable repo/ref/commit through exact-OID fetch. Validate
source and target identity and clean state independently, permit only the
binding-aware manifest tail, and stop before publication side effects on any
resolution, checkout, apply, or validation failure. This package-local source
binding never invokes or substitutes for extension verification.
Initial `publication_ready` preview first classifies an exact existing PR. When
no PR and no remote branch exist, a missing installed metadata tail maps the
still-prepared plan directly to `reprepare_required` before push, PR creation,
archive, Ready, or Issue mutation.

Execute the semantic profile in order: preview, AI review, one exact bounded
side-effect confirmation when required, gate record/check, deterministic
transition, and exactly one typed exit. Unknown, multiple, retired, stale, or
unmapped inputs and exits fail closed. Retired verification re-entry input
requires a fresh current Publication result and full Finalizer reprepare.
An already Ready same-plan transaction is a terminal read-only recovery: live
facts are revalidated and the current Merge DTO is materialized without
repeating any Git or GitHub mutation.
