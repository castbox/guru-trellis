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
accepted only after that exact pre-push HEAD is transaction-bound, or when the
current exact `ordinary_publication/push_content` transaction is still unbound
and remote/PR/Publication HEAD already equal. The latter path rereads exact PR,
scope, Draft/Ready and metadata bytes, converts the same owner transaction to
`existing_pr_recovery/bind_pr` before any remaining external mutation, and
never repeats publication push or PR creation. Both paths then converge the
current Publication title/body, archive, preserve Ready or mark Draft Ready,
and hand off to `guru-merge-task-pr`.

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

The unique recommended Happy Path is:

1. Run `preview-finalization` once and present its exact side-effect plan.
2. Complete the AI review and obtain a clear dialogue-local confirmation for
   that preview's `confirmation_identity`; do not persist the reply.
3. Run `finalize-task-happy-path --input ... --review-input ...
   --confirmed-preview-sha256 ...` once.

The facade records and checks the completed AI review, executes the current
transaction, and internally continues only mapped same-plan provenance/archive
reprepare, existing-PR adoption, resumable transaction recovery, and terminal
output-loss recovery. A scope, repository/base/head authority, reviewed commit,
PR title/body, close-Issue set, publication mode, or side-effect-set change
returns a stable exit and requires a new preview and confirmation. The digest
identifies the plan only; it is not authorization and is never persisted.

`record-finalization-gate`, `check-finalization-gate`,
`execute-finalization-transition`, and `invoke-guru-finalize-task` remain
compatibility, focused-test, diagnostic, and recovery commands. Unknown,
multiple, retired, stale, or unmapped inputs and exits fail closed. Retired
verification re-entry input requires a fresh current Publication result and
full Finalizer reprepare.
An already Ready same-plan transaction is a terminal read-only recovery: live
facts are revalidated and the current Merge DTO is materialized without
repeating any Git or GitHub mutation.
