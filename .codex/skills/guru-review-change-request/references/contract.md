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
the `guru-task-intake-router` consumes the checked ready exit, dispatching
`proposed_draft` to Issue creation and `existing_issue | standalone_request`
to task creation after their own fresh gates. It does not persist the private
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
checkpoint, result locator, or cross-round state store.

Workflow and standalone modes have identical entry preconditions. Both require
the complete compatible Guru Team preset, extension manifest, dispatcher,
runtime, installed inventory, and selected discovery copy. A copied package is
not portable. This contract covers normal honest workflow operation and
ordinary stale, mismatch, omission, and implementation-error cases. It does
not expand into malicious artifact forgery, adversarial bypass, locking,
TOCTOU, stress, fault-injection, or cross-OS hardening.

## Current Executing Owner

The current executing AI is this Skill's semantic owner in both workflow and
standalone modes. `owner_not_yet_executed` means continue the current review;
it is not a typed exit and does not require an external owner, agent ID,
subagent evidence, or pre-existing owner result. The restriction on runtime
semantic judgment does not restrict the current AI from authoring that judgment.

Read the complete contract, current target authority, real prerequisite public
outputs, and the Docs/code/tests/history needed for all ten readiness dimensions.
You author the findings, scope conclusion, readiness Gate, and route before
running record-change-request-review.sh, check-change-request-review.sh, and
invoke.sh. Neither structurally present dimensions nor successful prerequisite
checkers decide readiness; ready still requires the complete declared review.

Keep this owner's authoring and recorded result in call-local memory for its
own record/check/invoke sequence. Pass only actual public invoke stdout through
the declared thin projection to the next consumer; never read or reconstruct
producer-private results. This responsibility does not waive missing authority,
freshness, schema, prerequisite, or unresolved-choice checks: use the existing
declared blocker or re-entry route when a real gap remains. Do not bypass the
workspace gate or ask for a corrective Prompt merely because your review has
not run yet.

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

For `current_issue`, copy public `target_locator` from the real producer
stdout's `transition.target_locator`, preserving the transition unchanged.
Both must equal the canonical source issue URL (`target.url`), carried from
Discovery's `live_change.identity` through Clarification and Wording. `#N` is
only a search clue or display label here; it is not an equivalent chain binding
and returns `stale_identity` at `public_input.target_locator`. Use the captured
live source snapshot and actual recorder/checker receipt `result`; never manually rebuild
producer transitions, duplicate snapshots or validation receipts from examples.

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

`scope_conclusion` records requirement/scope basis, delivery unit,
duplicate/reuse conclusion,
implementation target and current gap, archived constraints, risk boundary,
and excluded scope.

The AI authors Gate `status`, `reviewer`, and `summary`. After that semantic
judgment, the recorder derives `reviewed_linkage_sha256` from the current
source/transition linkage, `scope_conclusion_sha256` from the authored scope
conclusion, and `findings_count` from the explicit findings list. If any of
these derived fields is supplied, it must equal the current derivation; it is
not silently overwritten. No second version or compatibility reader is used.
Checker and invoke still require and validate the complete recorded Gate.
`passed` pairs with `ready`,
`reroute` pairs with one of the mapped prerequisite or live-context exits, and `blocked` pairs
with `blocked`. A missing or incomplete Gate fails closed. Zero scanner errors,
successful prerequisite checkers, or ten structurally present dimensions never
generate or imply a semantic pass.

If the AI identifies a proposal that would change confirmed product semantics,
#101 does not absorb that decision: it returns `clarify_requirements`, where
`guru-clarify-requirements` owns the exact dialogue decision. The review result
records the route and objective evidence only, never authorization state.

## Five Typed Exits

- `ready` -> workflow `guru-task-intake-router`
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
public readiness transition directly.

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
the completed AI review, check consumes record receipt `result`, and invoke consumes the
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

## Installed Authoring

Use the target repository root as cwd. The actual runtime package is
`.trellis/guru-team/skills/packages/guru-review-change-request/`; platform
discovery copies do not contain the command runtime. Run these existing managed
launchers with the appropriate envelope on stdin:

```bash
bash .trellis/guru-team/skills/packages/guru-review-change-request/scripts/record-change-request-review.sh --root . --invocation - --json
bash .trellis/guru-team/skills/packages/guru-review-change-request/scripts/check-change-request-review.sh --root . --invocation - --json
bash .trellis/guru-team/skills/packages/guru-review-change-request/scripts/invoke.sh --root . --invocation - --json
```

Author `owner_result` with `generated_at`, `mode`, the current variant's
`target` authority fields, `semantic_review`, `typed_exit`, `reason`,
`affected_evidence`, and the selected `consumer`. `semantic_review` explicitly
contains all ten `dimensions`, `findings` (use `[]` when none), the complete
`scope_conclusion`, and `ai_review_gate`. The minimum Gate is:

```json
{"status": "passed", "reviewer": "readiness-owner", "summary": "Completed the ten-dimension review against current authority."}
```

This is a shape example, not a supplied readiness judgment. The AI must choose
the actual status and route. Missing status, reviewer, summary, dimensions,
findings, scope conclusion or route is rejected, never defaulted to pass.
For dimension/finding `affected_hashes`, use the existing public transition
evidence or source evidence actually reviewed, with matching `evidence_refs`
(for example `transition.context_result_sha256`). Do not precompute private
linkage or import eval runtime. Target hashes and prerequisites are derived by
the recorder; draft `source_request_sha256` remains the existing source
authority input described above. `examples/issue-review.json` is a complete
recorded-result example, not the minimal authoring input. Replace owner_result
with record receipt `result` for check, then add only check receipt `result.validation_receipt` for
invoke. No repository file is needed for this call-local exchange.

### Producer-Bound Draft Recipe

For `proposed_draft`, take `draft_id` from the actual producer public
`transition.target_locator`. Bind the current source snapshot's `draft_id`,
the authored `target.draft_id`, and `public_input.target_locator` to that exact
value. Preserve the entire transition, including mode and continuation id.
An example's locator is fictional shape data: never substitute it, an Issue
label such as `#145`, or a newly invented id for the producer's locator.
`examples/change-request.json` and `examples/public-proposed-draft-input.json`
illustrate the same draft identity; they supply no real prerequisite output.

`source_request_sha256` hashes the complete authority projection below using
UTF-8 canonical JSON (`ensure_ascii=False`, sorted keys, separators `,` and
`:`). `body_sha256` hashes only the current UTF-8 body bytes. These are distinct
values; title bytes remain independently bound by the recorder. Use the
reviewed normalized repository identity, not a draft name, as `repo`.

```json
{"kind":"draft","repo":"example/guru-extension","issue_number":null,"url":null,"state":"draft","updated_at":null,"body_sha256":"<current body SHA-256>"}
```

The following executable recipe uses standard-library JSON/hash/transport only.
Call it in the target repository with the actual Wording `pass` stdout, current
draft source, reviewed repository identity, and this AI's freshly completed
owner review. `completed_review` supplies `generated_at`, `semantic_review`,
`typed_exit`, `reason`, `affected_evidence`, and `consumer`, as described above;
it supplies no target or recorder-derived fields. It must contain the real ten
dimension judgments and evidence, explicit findings (`[]` only when none),
scope conclusion and minimum Gate `status/reviewer/summary`. Nothing here
creates a semantic review, defaults a pass, or calculates private linkage.

```python
import copy
import hashlib
import json
import subprocess

def draft_envelope(draft_source, wording_output, repo_ref, completed_review):
    transition = copy.deepcopy(wording_output["transition"])
    assert wording_output["exit_id"] == "pass"
    assert transition["stage"] == "wording_current"
    locator = transition["target_locator"]
    source = copy.deepcopy(draft_source)
    assert source["kind"] == "draft" and source["draft_id"] == locator
    body_sha256 = hashlib.sha256(source["body"].encode("utf-8")).hexdigest()
    authority = {
        "kind": "draft", "repo": repo_ref, "issue_number": None,
        "url": None, "state": "draft", "updated_at": None,
        "body_sha256": body_sha256,
    }
    authority_sha256 = hashlib.sha256(json.dumps(
        authority, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()
    owner = copy.deepcopy(completed_review)
    owner["mode"] = transition["mode"]
    owner["target"] = {
        "kind": "proposed_draft", "repo": repo_ref, "draft_id": locator,
        "source_request_sha256": authority_sha256,
    }
    return {
        "schema_version": "1.0",
        "public_input": {
            "profile": "proposed_draft", "source_exit": wording_output["exit_id"],
            "mode": transition["mode"], "target_locator": locator,
            "continuation_id": transition["continuation_id"],
        },
        "transition": transition,
        "owner_context": {"change_request": source}, "owner_result": owner,
    }

def record_check_invoke(envelope):
    envelope = copy.deepcopy(envelope)
    scripts = ".trellis/guru-team/skills/packages/guru-review-change-request/scripts/"
    def command(name):
        result = subprocess.run(
            ["bash", scripts + name, "--root", ".", "--invocation", "-", "--json"],
            input=json.dumps(envelope, ensure_ascii=False), text=True,
            capture_output=True, check=True,
        )
        return json.loads(result.stdout)
    recorded = command("record-change-request-review.sh")
    assert recorded["formal_exit"] is False
    envelope["owner_result"] = recorded["result"]  # replace the whole result
    checked = command("check-change-request-review.sh")
    assert checked["formal_exit"] is False
    envelope["validation_receipt"] = checked["result"]["validation_receipt"]
    return command("invoke.sh")  # actual formal exit; consume its declared route
```

The recorder receives minimal authoring, not the old complete
`examples/issue-review.json` result. Omit `reviewed_linkage_sha256`,
`scope_conclusion_sha256`, and `findings_count` from the authored Gate. Do not
import eval/private runtime or hash `evidence_linkage` to supply them. Record
derivation and target normalization are existing capabilities, not a new
review or recovery mechanism. Keep source/public input/transition unchanged
through this same-owner sequence. Record/check receipts have
`formal_exit=false`; only `invoke.sh` supplies a formal exit, and only its
actual `ready` may enter the ready consumer. Stop on a command error, inspect
its actual diagnostic, and follow the recovery below instead of using a
partial stdout as a pass or inventing a validation receipt.

### Same-Scope Authoring Recovery

An ordinary construction error in this side-effect-free review is handled by
the current AI. Reread the current source and actual prerequisite public
output, explain the mistake, and rebuild the entire minimal consumer envelope
with the recipe above. Reassess the ten dimensions against those current facts;
unchanged evidence can remain applicable, but a previously authored `passed`
is not a substitute for that judgment. Do not ask for repeated confirmation
when scope/authority and side effects are unchanged. Real scope choices and
external or Git side effects retain their existing owner boundaries.

| Ordinary mistake | Existing behavior and consumer reconstruction |
| --- | --- |
| Draft target copied from standalone authoring with `caller_locator`/`request_id` | Target normalization may ignore these variant extras; their presence alone does not establish rejection. The public input is still its closed draft profile. Rebuild the draft target using only `kind/repo/draft_id/source_request_sha256`; preserve legal normalization and diagnose actual identity/digest errors separately. |
| Body SHA used as `source_request_sha256` | The wrong authority digest is rejected. Recompute only the complete public authority projection from the same reviewed body and repository. |
| Invented or inconsistent `draft_id` | Source, target and public locator must bind to the actual producer locator. Rebuild this consumer from that same real draft source/output; never change the producer to accommodate the invented id. |
| Gate linkage computed by hashing a linkage object containing `linkage_sha256` itself | An explicitly supplied wrong derived Gate value is rejected. Discard it and omit all three Gate-derived fields; let the existing recorder derive its fixed projection. |
| Old complete owner result partly patched or recomputed | It may retain stale target/Gate bindings and fail; patching a field does not refresh the whole review. Discard this consumer result, reconstruct fresh minimal authoring, then replace it with the actual whole record `result` before check. Do not patch recorded prerequisites, private linkage, facts digest or receipt. |

These are normal authoring mistakes, not a new rejection policy or hostile-input
model. Preserve the original producer transition throughout same-source
recovery. If the source snapshot is actually for another draft, do not relabel
it to force a match; obtain the current matching source/upstream output first.

A real body or authority revision requires the existing upstream refresh:
Sync/Discovery, Clarification, and Wording run against the revised content
before a new readiness review. Consume their new actual outputs; the locator
may legitimately change. The old source-authority digest and old receipt do
not stand in for revised content. Do not edit an old transition's hashes or
locator to make it appear refreshed.

Missing prerequisites are distinct from consumer construction errors.
With an actual original `clarity_current`, author a real missing-wording
finding and `review_wording` decision using that original transition. With
an actual original `context_current`, the corresponding missing-clarity route
is `clarify_requirements`. Perform the declared review and record/check/invoke
for that route; never downgrade a later transition or synthesize an earlier
one. If the required original public output or current authority is absent,
stop and identify exactly what its owner must supply. Do not manufacture
producer passes, hashes, receipts or `ready` to continue.

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
