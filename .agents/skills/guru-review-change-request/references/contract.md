# Change Request Readiness Review Contract

## Ownership And Boundary

`guru-review-change-request` is the only semantic owner of pre-task change
request readiness. The global workflow owns mandatory invocation, five unique
consumers, and the fail-closed stop. The shared runtime owns only schema,
hash, digest, evidence linkage, existing prerequisite objective checks,
recording, and checking.

The Skill never fetches base context, searches Docs/code/tests/history, chooses
duplicate reuse, runs the clarification loop, scans wording independently, or
creates an issue, branch, worktree, or Trellis task. It reuses the current
outputs of `guru-discover-change-context`, `guru-clarify-requirements`, and
`guru-review-contract-wording`. Issue #112's
`guru-create-task-workspace` consumer owns every task-creation side effect and
any later task-local persistence of the byte-identical checker-passed
`issue-review.json` result.

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
`content_sha256` from the title/body hashes. It rebuilds the fixed wording
change-request scope from `--change-request-input` and rejects any title/body,
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

The recorder accepts one closed `prerequisite_payloads` object with `context`,
`clarity`, and `wording` members. Each member is either the complete upstream
result or `null` when the AI is recording an explicit missing-evidence reroute.
The runtime calls the existing objective structural/live helpers for each
present payload. It does not copy or reimplement current/history discovery,
clarification reduction, or wording scan/classification.

The durable result stores only portable projections and error codes:

- context: schema/exit, snapshot/base/query/live/current/history/duplicate
  identities;
- clarity: schema/exit, result/target/content/scope identities;
- wording: schema/profile/exit, facts/scope/scan and target-content identities.

Each projection has `status=current`, `missing`, or `invalid`. Only `current`
is eligible for `ready`. Missing/stale/mismatched evidence remains objective
input to the AI's reroute judgment; scripts never map an error code to an exit.

`evidence_linkage` binds target identity/content, base/current/history/
duplicate identities, clarity facts, wording facts, and one canonical
`linkage_sha256`. Checker invocation supplies the same current prerequisite
payloads and change-request input, rebuilds this projection, and compares it
byte-for-byte with the recorded result.

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
`reroute` pairs with one of the three prerequisite exits, and `blocked` pairs
with `blocked`. A missing or incomplete Gate fails closed. Zero scanner errors,
successful prerequisite checkers, or ten structurally present dimensions never
generate or imply a semantic pass.

Human confirmation is normally `not_required`. If the AI identifies a proposal
that would change confirmed product semantics, #101 does not absorb that
decision: it records `required` with the proposal digest and returns
`clarify_requirements`, where `guru-clarify-requirements` owns the exact user
decision.

## Five Typed Exits

- `ready` -> Skill `guru-create-task-workspace`
- `clarify_requirements` -> Skill `guru-clarify-requirements`
- `review_wording` -> Skill `guru-review-contract-wording`
- `refresh_context` -> Skill `guru-sync-base`
- `blocked` -> stop `change-request-review-blocked`

The result carries one scalar exit and its exact consumer. Unknown, multiple,
missing, unmapped, or consumer-mismatched exits fail closed. `ready` requires
all ten dimensions passed, no blocking finding, all three prerequisites
current, complete linkage, a passed Gate, and `human_confirmation=not_required`.
The runtime validates these objective invariants but returns the AI-authored
exit unchanged.

## Artifact Lifecycle

Schema `guru-change-request-review-1.0` defines the portable result and
`issue-review.json` is its stable artifact basename. The #101 recorder and
checker are pre-task/standalone stdout-only and reject any output or task
locator. They do not create repository caches, workspace journals, history
indexes, sidecars, or task artifacts. Only #112 may later persist the exact
checker-passed bytes to the direct active task's tracked `issue-review.json`.

Examples and tests use fictional repositories, issues, hashes, and findings.
They contain no active task state, workspace journal, credential, private
business data, or machine-local absolute path.

Production linkage regression tests create a real clean Git repository, run
current context, clarification, and wording payloads through their production
record/check commands, then run the resulting full prerequisite set through
the change-request production recorder/checker to `ready`. Negative cases cover
wrong prerequisite exits, consumer and target/content mismatch, base/current/
history/duplicate drift, and both draft variants' source-authority digest
mismatch. They do not replace producers with handwritten portable projections.
