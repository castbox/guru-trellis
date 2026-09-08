# Change Request Readiness Review Contract

## Ownership And Boundary

`guru-review-change-request` is the only semantic owner of pre-task change
request readiness. The global workflow owns mandatory invocation, five unique
consumers, and the fail-closed stop. The package runtime owns prerequisite
projection, linkage, recording and checking; the shared runtime provides only
neutral schema, hash and dispatch primitives.

The Skill rereads current target authority and the Docs/code/tests/history
needed by its own readiness gate. It never chooses duplicate reuse, runs the
clarification loop, scans wording independently, or
creates an issue, branch, worktree, or Trellis task. It reuses the current
outputs of `guru-clarify-requirements` and `guru-review-contract-wording`;
Discovery cognition is not reopened through a private artifact. Issue #112's
`guru-create-task-workspace` consumer owns every task-creation side effect and
consumes the checked typed exit directly. It does not persist the private
`issue-review.json`-shaped result under the task.

Before any newly observed scenario participates in readiness, scope conclusion,
finding, requested test, clarification, or blocking route, the owner forms a
candidate-only set and invokes
`guru-qualify-normal-scenario:change_request_candidate_set`. Candidate inputs
contain no decision, scenario class, severity, route, or caller assertion of a
normal path. `classified` returns to this owner;
`scope_confirmation_required` routes to requirements clarification;
`mechanism_revision_required` returns here for remove/replace and full fresh
review; `blocked` stops. Rejected candidates do not become findings, tests,
clarification, or follow-up work. This review stores no qualification artifact,
checkpoint, result locator, or cross-round ledger.

Workflow and standalone modes have identical entry preconditions. Both require
the complete compatible Guru Team preset, extension manifest, dispatcher,
runtime, installed inventory, and selected discovery copy. A copied package is
not portable. This contract covers normal honest workflow operation and
ordinary stale, mismatch, omission, and implementation-error cases. It does
not expand into malicious artifact forgery, adversarial bypass, locking,
TOCTOU, stress, fault-injection, or cross-OS hardening.

## Target Identity

Exactly one target kind is reviewed:

- `existing_issue`: normalized repository, positive issue number, canonical
  issue URL, current authority update time, and title/body SHA-256 values;
- `proposed_draft`: reviewed draft id, source-request digest, title/body
  SHA-256 values, and `side_effect_free=true`;
- `standalone_request`: explicit caller locator, request id, source-request
  digest, title/body SHA-256 values, and `side_effect_free=true`.

The recorder derives `identity_sha256` from the variant's authority fields and
`content_sha256` from the title/body hashes in `owner_context.change_request`.
It compares that target with the public prerequisite transition and rejects any title/body,
source kind, repository, issue number, URL, draft id, or target digest mismatch.
For `proposed_draft` and `standalone_request`, `source_request_sha256` is not a
caller label. The recorder reuses #113's current draft `review_target` authority
projection exactly: `kind=draft`, normalized `repo`, null `issue_number`/`url`/
`updated_at`, `state=draft`, and the SHA-256 of the reviewed body bytes. It
canonical-digests that projection and rejects a missing, wrong, or stale
`source_request_sha256`. The reviewed title bytes remain independently bound by
`title_sha256`; `draft_id` or `request_id` plus `caller_locator` remain the
variant identity rather than being folded into the #113 authority projection.

## Prerequisite Projection

The only prerequisite input is the independent, schema-validated public
transition from the actual producer. `wording_current` supplies clarity and
wording. Original `clarity_current` supports a missing-wording reroute; original
`context_current` supports a missing-clarity reroute. Neither full upstream
owner results nor handwritten projections are accepted. Wrong/absent stages,
unsupported shape, or inconsistent duplicate fields return `schema_mismatch`,
not a request to repeatedly refresh unchanged live content.

The owner-private 2.0 result contains only status and the public identities:
clarity facts/target/disposition/content/scope, and wording facts/scope/scan/
target-content. Missing stages become `status=missing` with null identities;
present stages become `status=current`. Callers never author these statuses.
The runtime validates public mode, continuation, target locator and source
profile. Current target matching uses the public target locator (including
repository and issue identity), Wording's public title/body identity, and the
checker's authoritative issue reread. For `context_current`, the public
`authority_content_sha256` must match the source body hash. Readiness does not
reconstruct Clarification's private review target, facts digest, or serialization
format. Clarity target/content/disposition hashes are opaque checker-bound
identities, preserved unchanged in the local result and receipt linkage.
The existing draft `source_request_sha256` normalization remains Readiness's
explicit source contract, not an interpretation of clarity target identity.
Wording's top-level and nested content
identities must agree and match current title/body combination. Real content
or target drift returns `stale_identity`.

Clarity `content_sha256` is the semantic review content identity, not the
title/body combination. Clarity's disposition hash covers the full reviewed
disposition object; `target_disposition.disposition_sha256` carries the
producer's distinct disposition digest. They are preserved, not equated.
Clarity facts must match `clarity_result_sha256`, and wording facts must match
`wording_facts_sha256`. In `clarity_current` only, top-level content equals
clarity's semantic content; Wording replaces that top-level value with its
title/body combination. The full transition, including both disposition
domains, is bound by the checker's receipt.

`evidence_linkage` binds target identity/content, clarity facts, wording facts,
and one canonical
`linkage_sha256`. The clarification disposition digest is an independent
linkage member, so a retained/selected target decision cannot drift while a
previous readiness pass remains reusable. Checker invocation supplies the same
public transition and source snapshot, rebuilds this projection, and compares
it byte-for-byte with the recorded result. The AI still owns every route;
scripts never turn missing evidence into an automatically chosen exit.

## Semantic Review

The AI reviews these ten fixed dimensions in order:

1. `requirement_completeness`
2. `delivery_unit_consistency`
3. `implementation_target_evidence`
4. `claimed_behavior_current`
5. `current_implementation_gap`
6. `docs_code_tests_consistency`
7. `archived_history_constraints`
8. `duplicate_reuse_validity`
9. `target_authority_current`
10. `prerequisite_hash_linkage`

Each dimension records `passed` or `failed`, a non-empty summary, evidence
references, affected hashes, and finding ids. Findings use the closed category
set `requirement_gap`, `delivery_conflict`, `wording_gap`, `context_stale`,
`target_complete`, `current_history_conflict`, `duplicate_reuse_conflict`, and
`prerequisite_mismatch`. Category structure is audit data; it never selects an
exit.

`scope_conclusion` records requirement/scope basis, delivery unit, close/
related/follow-up issue projections, duplicate/reuse conclusion,
implementation target and current gap, archived constraints, risk boundary,
and excluded scope. The public schema does not hard-code issue #101; this
task's Issue Scope Ledger and finish-work gate own its `[101]` close projection.

The AI Review Gate records reviewer, reviewed linkage digest, summary, findings
count, scope-conclusion digest, and status. `passed` pairs with `ready`,
`reroute` pairs with one of the mapped prerequisite or live-context exits, and `blocked` pairs
with `blocked`. A missing or incomplete Gate fails closed. Zero scanner errors,
successful prerequisite checkers, or ten structurally present dimensions never
generate or imply a semantic pass.

If the AI identifies a proposal that would change confirmed product semantics,
#101 does not absorb that decision: it returns `clarify_requirements`, where
`guru-clarify-requirements` owns the exact dialogue decision. The review result
records the route and objective evidence only, never authorization state.

## Five Typed Exits

- `ready` -> Skill `guru-create-task-workspace`
- `clarify_requirements` -> Skill `guru-clarify-requirements`
- `review_wording` -> Skill `guru-review-contract-wording`
- `refresh_context` -> Skill `guru-sync-base`
- `blocked` -> stop `change-request-review-blocked`

The result carries one scalar exit and its exact consumer. Unknown, multiple,
missing, unmapped, or consumer-mismatched exits fail closed. `ready` requires
all ten dimensions passed, no blocking finding, both prerequisites
current, complete linkage, and a passed Gate.
The runtime validates these objective invariants but returns the AI-authored
exit unchanged.

## Artifact Lifecycle

Schema `guru-change-request-review-2.0` defines the owner-private result and
`issue-review.json` is its stable artifact basename. The #101 recorder and
checker are pre-task/standalone stdout-only and reject any output or task
locator. They do not create repository caches, workspace journals, history
indexes, sidecars, or task artifacts. The workspace owner consumes the current
public readiness transition and persists only the task-local issue scope ledger.

Examples and tests use fictional repositories, issues, hashes, and findings.
They contain no active task state, workspace journal, credential, private
business data, or machine-local absolute path.

Production linkage regression tests create a real clean Git repository, run
clarification and wording through their production record/check/invoke
commands, then feed the actual public transition through
the readiness production record/check/invoke commands to `ready`. Negative cases cover
wrong prerequisite exits, consumer and target/content mismatch, live target
drift, and both draft variants' source-authority digest
mismatch. They do not replace producers with handwritten portable projections.

## Single Invocation And Migration

The public target profiles remain `current_issue`, `proposed_draft`, and
`standalone_request`; `source_exit` is entry metadata, not a caller-authored
prerequisite pass. All commands receive one `--invocation -` envelope with
`schema_version=1.0`, `public_input`, independent `transition`,
`owner_context={change_request: source}`, and `owner_result`. Record consumes
the completed AI review, check consumes record stdout, and invoke consumes the
same checked result plus `validation_receipt`. Receipt is forbidden in
record/check and required in invoke. The package-local closed pre-receipt
schema is `review-invocation.schema.json`; invoke reuses the existing shared
semantic-owner schema. All inputs can remain in memory; no input files are
created. A single envelope file locator is also supported by the same parser.

Issue #386 directly retires `--input`, `--mode`, `--change-request-input`,
`--prerequisites-input`, `--expected-facts-sha256`, and authored
`prerequisite_payloads`. Callers migrate to the envelope and fresh public
producer transitions, not adapters for old private artifacts. Owner schema
2.0 removes unconsumed upstream payload/schema/exit/profile/error fields.
Old 1.0 private results and receipts must be regenerated by fresh review;
there is no dual reader or backfill of invented upstream hashes.

Each public output keeps its existing schema and consumer. Ready carries the
declared readiness transition and workspace profile. Clarification re-entry
requires the original `context_current`; wording re-entry requires the original
`clarity_current`. Pass that original transition to all three commands. Keep
the upstream public output in call-local context while reviewing so re-entry
does not reconstruct Discovery private state or fabricate hashes. Missing
original context fails closed. Refresh and blocked remain AI-authored exits.
# Invocation-Local Authority Snapshot And Receipt

One readiness invocation captures the target issue authority once. Recorder,
clarity projection, wording projection and target normalization use that same
snapshot; the checker performs the one authoritative validation and returns a
call-local receipt bound to exact result, prerequisites and target snapshot.
The receipt's `prerequisite_sha256` is the canonical digest of
`{prerequisites, transition}`, binding the complete original public transition,
including base, context, continuation and both disposition digest domains.
The serializer rebuilds only local target/prerequisite projections and result,
validates the receipt and public output, and adds zero live Git/GitHub calls.
Any target, prerequisite, transition or result identity change rejects the old
receipt. The digest is a local checker/serializer consistency token, not
cross-Skill semantic approval or authorization.
