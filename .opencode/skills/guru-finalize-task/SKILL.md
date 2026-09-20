---
name: guru-finalize-task
description: Finalize a reviewed Trellis task through one semantic finalization loop, one deterministic transaction engine, and six typed exits.
---

# Guru Finalize Task

Use only after `guru-review-task-publication:ready`, or for one declared
same-owner resume/reprepare profile, or after `archived_ready` for the dedicated
`archived_review_refresh` profile. Read `references/contract.md` before use.

## Archived Review Refresh

For this profile only, consume the workflow's fresh Architecture
`acceptance_finish` result and Publication's `archived_ready` projection.
Validate the completed committed archive, current A/B and exact existing Ready
PR bytes. Derive original H from the summary commit set using ancestry, then
validate original archive continuity with H, never A. Review these facts and
the current Publication authority semantically. Record/check the current
review through `invoke.sh --input ... --review-input ...`; do not supply
`--confirmed-preview-sha256` or invoke the transaction executor.
Return only original `ready_for_merge` or `blocked`. This path does not archive,
push, edit PR/Issue, repair mappings, restore tasks, or reuse an old gate.
Missing/stale mapping or an in-flight original transaction stops for the
existing Finalizer recovery; it is not repaired by this profile. The invocation
retires only its short-lived review checkpoint after terminal consumption.

The remaining sections describe the unchanged original transaction profiles.

The current business finalization graph never invokes
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

One additional current-plan recovery is allowed before generic transaction
base-evolution handling: an unbound predecessor
`ordinary_publication/push_content` transaction may advance only across one
validated direct-child provenance metadata tail while its old Publication HEAD
still equals the unique PR and remote HEAD. Preview classifies that topology as
`strict_ancestor` with `push_required=true`. Execute rereads the same facts and
persists one current-plan `existing_pr_recovery/push_content` transaction before
pushing the new Publication HEAD exactly once. This path reuses the existing
recovery engine and does not widen the equal-HEAD no-push conversion.

That same recovery also accepts one legal composition where base evolution
precedes the current provenance tail. The current Publication HEAD must first
pass `provenance_tail_commit_errors()` against its direct parent; the existing
exact base-evolution binary-delta comparison then uses that validated parent as
its endpoint. The direct-tail and pure-base-evolution paths remain unchanged,
and no path filtering, permissive business-drift classification, or multi-tail
sequence is introduced.

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

The unique public Happy Path is:

1. Run `preview-finalization` once and present its exact side-effect plan.
2. Complete the AI review and obtain a clear dialogue-local confirmation for
   that preview's `confirmation_identity`; do not persist the reply.
3. Run `invoke-guru-finalize-task --input ... --review-input ...
   --confirmed-preview-sha256 ...` once.

The original `scripts/invoke.sh` public entry records and checks the completed
AI review, executes the current
transaction, and internally continues only mapped same-plan provenance/archive
reprepare, existing-PR adoption, resumable transaction recovery, and terminal
output-loss recovery. A scope, repository/base/head authority, reviewed commit,
PR title/body external-work-item effect, publication mode, or side-effect-set change
returns a stable exit and requires a new preview and confirmation. The digest
identifies the plan only; it is not authorization and is never persisted.

`ready_for_merge` carries the SHA-256 identity of the exact Publication-reviewed
PR body bytes as `publication_body_sha256`. This is the minimal handoff required
by Merge to reject a later body-only edit before it derives closing keywords or
performs any remote mutation; it does not restore Issue arrays or transfer the
Publication decision itself.

`record-finalization-gate`, `check-finalization-gate`, and
`execute-finalization-transition` remain package-private focused-test,
diagnostic, and recovery commands. `invoke-guru-finalize-task` accepts the
current semantic review input and never consumes a prebuilt owner result.
Unknown,
multiple, retired, stale, or unmapped inputs and exits fail closed.
For an explicit independent manual operation after an automatic stop, read
`.trellis/workflow.md#manual-gitgithub-operations` (Manual Git/GitHub Operations).
That global boundary does not relax this Skill's entry or completion contract.

An already Ready same-plan transaction revalidates live facts and materializes
the current Merge DTO without repeating any Git or GitHub mutation. Finalizer
alone converges the exact task's existing source/target mapping projections
to the committed archive locator when needed; it never rebuilds an unknown
mapping or lets a read-only boundary checker repair identity.
