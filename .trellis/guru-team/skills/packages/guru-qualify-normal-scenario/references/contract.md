# Normal-Scenario Qualification Contract

## Contents

1. Ownership and boundary
2. Closed profiles and callers
3. Scope-first review
4. Candidate decisions
5. AI Review Gate and exits
6. Process-local runtime
7. Re-entry and callers

## 1. Ownership And Boundary

`guru-qualify-normal-scenario` is the only semantic owner of normal-scenario qualification. It decides whether a newly proposed behavior scenario is eligible to enter a caller's own scope, acceptance, test, finding, implementation, or publication judgment. It does not decide severity, planning sufficiency, implementation design, publication readiness, or the caller's final route.

The global workflow owns conditional mandatory invocation and typed-exit routing.
[Applicability](applicability.md) owns the loading, adoption and refresh
conditions. The caller reads it before this full contract and judges whether
dedicated admission is needed, without assigning a qualification verdict.
Each caller owns its profile-specific candidate set and post-qualification stage
judgment. Workers and reviewers may report a candidate reference, observed
behavior, locators and a minimal reproduction hint; they do not assign severity,
scenario class, qualification or an implementation route.

## 2. Closed Profiles And Callers

Use exactly one profile and its fixed caller/semantic owner:

| Profile | Caller and semantic owner |
| --- | --- |
| `task_free_pre_write` | `guru-execute-task-free-change` |
| `task_free_evolution` | `guru-execute-task-free-change` |
| `requirements_scope_set` | `guru-clarify-requirements` |
| `change_request_candidate_set` | `guru-review-change-request` |
| `planning_scenario_set` | `guru-approve-task-plan` |
| `implementation_discovery` | `guru-phase2-implementation-coordinator` |
| `base_impact_candidate_set` | `guru-reconcile-task-base` |
| `phase2_candidate_set` | `guru-check-task` |
| `branch_review_candidate_set` | `guru-review-branch` |
| `publication_candidate_set` | `guru-review-task-delivery` |

The deterministic resume target is a separate workflow mapping. In particular,
`implementation_discovery` remains owned by
`guru-phase2-implementation-coordinator`, while clarification and typed-output
re-entry resume through the existing `guru-resume-implementation` workflow
target.
`publication_candidate_set` returns to `guru-review-task-delivery` after
classification, scope clarification, or mechanism revision.

Workflow and standalone modes use the same evidence and judgment. Each input is a closed profile contract containing its fixed profile and caller, one current target identity, a non-empty unique `candidate_refs` set, and the minimum locators needed for live reread. Do not accept severity, scenario class, a proposed decision or exit, authorization text, an earlier qualification result, a shared artifact locator, a raw worker report, a search transcript, or a caller assertion that a path is normal.

## Explicit Task/Delivery target

The seven Task/Delivery profiles (`author_candidate_set`, `planning_scenario_set`,
`implementation_discovery`, `base_impact_candidate_set`, `phase2_candidate_set`,
`branch_review_candidate_set`, `publication_candidate_set`) select input 2.0 through
aggregate 3.0. Each requires opaque `target.delivery_key` from the original caller's
actual Identity/Ensure/Bind/Delivery selection or current query. The key carries
TaskId, current generation and Delivery identity. The installed public API owns
its parsing; callers do not infer it from inventory, paths or digests.

Before invocation, the caller retains its own TaskRef/key/profile and stage
purpose in the current call. The original identity owners must agree on the
current generation, branch binding, ownership and registered checkout. When the
official resolver has no context key, `current(key)` validates that explicit
object without writing a session. With an available context, its official current
selection must match the complete key. Missing, stale, terminal, erroneous or
conflicting context facts return to their original owner; explicit parameters
never replace that selection.

The shared factual checker resolves the selected key's real `planning_root`.
For `planning_scenario_set`, `planning_paths` must equal its three planning files;
for other planning-identity profiles those paths come from that same root.
`author_candidate_set` checks only its existing `author_paths` and identity, not
future design/implementation bodies. Existing HEAD, path, file-set and candidate
checks continue. The four non-Delivery profiles retain their existing inputs.
`phase2_candidate_set` retains its declared pinned-old/recovery boundary; this
input evolution does not restore a retired current Check stage.

Outputs and routers retain their existing shapes and meanings. The original
caller consumes the returned profile and candidate disposition against its own
current invocation, then continues its original stage. Root's profile-only
return uses that same caller-owned context. No key is added to output and no
qualification state, binding writer or second authority is introduced.

Old published profile/aggregate schemas and public-input examples remain
historical validation assets. Current invocation selects only the versioned
inputs. Pending old inputs return to their original caller for fresh assembly;
completed conclusions follow applicability. See the complete provider's
`MIGRATION-812.md` for adoption, recovery and rollback boundaries.

## 3. Scope-First Review

Reread the live requirement authority, current planning, actual caller and consumer, relevant code and diff or base range, applicable tests, and repository contracts. Do not substitute a worker summary, an existing implementation, an existing test, or a prior invocation.

For every candidate, judge in this fixed order:

1. Identify exact current requirement authority.
2. Prove the real supported entry, caller, and consumer.
3. Reproduce an honest normal action sequence without falsification, attack behavior, or deliberate workflow bypass.
4. Observe that current required behavior actually fails. An evidenced actual
   responsibility/Architecture contract violation qualifies without requiring
   a functional failure or a task acceptance clause naming that violation;
   tests and implementation agreeing does not disprove it.
5. Establish scope provenance and current-task necessity only after the first
   four steps pass: where would the current goal or an affected current
   contract fail if this work were omitted? Separate an inherited problem from
   its new expansion/solidification. Include necessary local refactoring,
   consumer adaptation and old-path exit, but do not automatically turn an
   unrelated historical defect into current work, a finding, gate or follow-up.

Problem validity does not alone prove task necessity or mechanism suitability.
Return qualified inputs to the original owner; it independently applies
solution-mechanism applicability before accepting a mechanism. Never qualify only
because a plan was approved, implementation exists, tests are green, a reviewer
recommended it or the user said continue. Legal non-default inputs/configuration
remain legal under current authority; defaults and missing diagnostic tags do
not justify inventing a stronger rejection rule. For red tests use bounded
causal evidence, stop on proven unrelatedness, and keep unresolved attribution
explicit rather than assuming a historical failure.

Quarantine severity, reviewer pressure, an existing patch or test, coverage arguments, best-practice claims, and theoretical bypass framing until those five questions are answered. These narratives never establish authority by themselves.

For a candidate framed as security, attack, forgery, tampering, hostile input, bypass, defense in depth, TOCTOU, locking, fault injection, or unrequested hardening, begin with no current-scope qualification. Qualify it only when an exact current requirement locator, a real supported entry, an honest action sequence, and a reproducible current defect all exist. Secret and credential redaction, explicit permission boundaries, destructive-action confirmation, ordinary stale or mismatch behavior, incorrect recorder or executor output, and a real caller selecting the wrong runtime remain legitimate when current authority requires them.

If the repository contract already excludes the scenario, return `rejected_out_of_scope`. Never upgrade that candidate into user confirmation, a negative test, implementation, a finding, a follow-up, or a publication blocker. If the current task introduced a mechanism that serves only an excluded scenario, select `mechanism_removed` or `mechanism_replaced`; existing code, tests, or reviewer severity do not grandfather it.

## 4. Candidate Decisions

Give every candidate exactly one current decision:

- `qualified_current`: explicit current authority and the supported normal path reproduce a current required-behavior defect.
- `qualified_explicit_nonstandard`: current authority explicitly requires the nonstandard but supported scenario.
- `qualified_approved_expansion`: a current user scope choice explicitly added the scenario.
- `scope_confirmation_required`: the first four scope-first checks pass and a real unresolved scope choice remains. Do not use this for a scenario already excluded by repository authority.
- `rejected_no_authority`: no current requirement authorizes the behavior.
- `rejected_unsupported_entry`: the proposed entry, caller, or consumer is not supported.
- `rejected_not_reproduced`: an honest supported action sequence does not reproduce the claimed current defect.
- `rejected_out_of_scope`: current repository or task authority explicitly excludes the scenario.
- `mechanism_removed`: remove a task-introduced mechanism whose only purpose is an excluded scenario.
- `mechanism_replaced`: replace such a mechanism with one serving a qualified current scenario.
- `blocked`: live authority, target identity, candidate evidence, or caller/consumer state is too incomplete or stale for a reliable decision.

Choose among the three qualified decisions by the scenario's relationship to the
repository normal-operation boundary, not by the entry through which the defect
was observed. Ordinary stale or mismatch behavior, incorrect recorder or executor
output, maintenance omissions, and a real caller selecting the wrong runtime are
`qualified_current`. Secret or credential redaction and explicit permission or
destructive-action confirmation are `qualified_explicit_nonstandard` when current
authority preserves them as supported exceptions to that ordinary boundary. A
supported normal entry does not turn such an explicit nonstandard obligation into
`qualified_current`. Use `qualified_approved_expansion` only when a current user
scope choice added the scenario; the mere presence of explicit authority is not an
approved expansion.

Apply one fail-closed precedence rule to the rejected decisions. When current
repository or task authority explicitly excludes the scenario or an assumption it
requires, choose `rejected_out_of_scope` even if the candidate also lacks a
supported entry or reproducible defect. Do not downgrade an explicit exclusion to
`rejected_unsupported_entry` or `rejected_not_reproduced`. Only when no explicit
exclusion applies, use `rejected_no_authority` for a missing current requirement,
`rejected_unsupported_entry` when authority exists but the proposed entry, caller,
or consumer is unsupported, and `rejected_not_reproduced` when authority and a
supported entry exist but the honest action sequence does not reproduce the defect.

For each decision, keep a concise reason and a six-part witness in the current semantic result: `requirement_refs`, `supported_entry_refs`, `existing_caller_refs`, `honest_action_sequence`, `defect_observation`, and `excluded_assumptions`. These are AI-authored semantic evidence, not facts a script may judge for sufficiency.

## 5. AI Review Gate And Exits

Before emitting an exit, review the complete candidate set and confirm that:

- every input candidate has exactly one decision and no extra decision exists;
- the fixed scope-first order was applied to each candidate;
- safety and attack framing was reverse-proved instead of assumed;
- severity and implementation pressure did not become authority;
- an excluded candidate was not promoted to clarification, finding, implementation, test, follow-up, or blocker;
- qualified candidates remain inputs to the original Owner rather than pre-deciding that Owner's stage judgment;
- the typed exit and its unique consumer express the AI's current semantic conclusion.

Return exactly one exit:

- `classified`: all candidates are qualified or rejected, with no unresolved scope choice, mechanism revision, or blocked decision. The classified router returns the decisions and witnesses to the fixed original Owner.
- `scope_confirmation_required`: a real unresolved scope choice remains and no candidate is blocked. Project only candidate refs and current continuation identity to `guru-clarify-requirements:normal_scenario_scope_confirmation`; do not project decisions, reasons, severity, authorization, or a result locator.
- `mechanism_revision_required`: at least one task-introduced mechanism must be removed or replaced and no candidate is blocked. The mechanism router returns the current decisions and witnesses to the fixed original Owner.
- `blocked`: live evidence cannot support a reliable current judgment. Stop at `normal-scenario-qualification-blocked`.

The deterministic runtime validates only closed shape, identities, freshness facts, enums, exact candidate coverage, the fixed cross-field aggregation of the AI-selected candidate decisions and typed exit, and the declared consumer binding. It must not author a candidate decision, judge scope or witness sufficiency, interpret severity, or choose a route.

## 6. Process-Local Runtime

Author one invocation envelope:

```json
{"schema_version":"1.0","semantic_result":{"schema_version":"1.0","skill_id":"guru-qualify-normal-scenario","public_input":{},"candidate_results":[],"ai_review_gate":{},"typed_exit":"classified","consumer":{"kind":"workflow","id":"guru-normal-scenario-classified-router"}}}
```

Supply it only through stdin:

```bash
scripts/invoke.sh --invocation -
```

The invocation process validates and serializes the semantic result in memory, performs current structural and freshness checks, and emits one typed result on stdout. The separate record and check commands exist for deterministic tests and explicit same-pipeline composition; they also require stdin and emit stdout only.

For `planning_scenario_set`, `implementation_discovery`, and
`phase2_candidate_set`, compute `planning_identity` with the
[File-set identity](#file-set-identity) format below over the actual planning
owner's selected `prd.md`, `design.md`, and `implement.md` paths. The checker
recomputes it from current regular, non-symlink repository files before emitting
a typed result.

## File-set identity

This is the shared public format for qualification `author_identity` and
`planning_identity`. The original caller chooses the current evidence paths;
the identity neither selects scope nor establishes semantic qualification.
For `author_candidate_set`, use exactly `target.author_paths` and place the
result in `target.author_identity`. Include only existing source/candidate
files; future design or implementation files are not prerequisites.

1. Sort the supplied repository-relative path strings with Python `sorted`.
   Preserve each original string in the rows; do not resolve it to an absolute
   path, add `path:`, normalize it, or deduplicate the input while computing.
2. For each sorted path, read the file's original bytes. Construct one object
   with exactly `path` (the original path string) and `content_sha256` (the
   lowercase hexadecimal SHA-256 of those bytes). Do not decode or normalize
   file content, line endings, a UTF-8 BOM, or Unicode text.
3. Serialize the complete rows array with
   `json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(',', ':'))`,
   then encode that JSON text as UTF-8. Hash those bytes with SHA-256.
   No newline is added to the hashed JSON.
4. Use the resulting 64 lowercase hexadecimal characters directly, without a
   `sha256:` prefix. It is not a hash of file concatenation or of a path-to-hash
   object. Its meaning and schema remain the existing file-set identity.

The following recipe uses only Python's standard library and writes only
stdout. Run it from the repository root after replacing the example list with
the exact current `target.author_paths`. The first argument is the repository
root; the second is the JSON path list. The final printed newline is not part
of the digest.

```sh
python3 - . '["docs/来源设计.md",".trellis/tasks/current/prd.md"]' <<'PY'
import hashlib
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1])
paths = json.loads(sys.argv[2])
rows = [
    {"path": path, "content_sha256": hashlib.sha256((repo / path).read_bytes()).hexdigest()}
    for path in sorted(paths)
]
encoded = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
print(hashlib.sha256(encoded).hexdigest())
PY
```

If a selected file changes, reread its source/candidate evidence and apply
[applicability](applicability.md) to the affected judgment. A new invocation
recomputes the identity from current files; adoption of a still-applicable
semantic conclusion does not replay an old invocation. Never patch an earlier
identity or recorded result to make it current.

Never create or request an output path, result locator, checkpoint path, temporary result file, tracked file, ignored `.trellis/.runtime/**` qualification state, cross-process locator, report, candidate or rejection state store, approval, signoff, assignment, handoff, or transcript. `artifacts` and `private_artifacts` are empty. This Skill and its runtime never write a Phase 2, Branch Review, or Publication gate. After consuming the process-local stdout, the corresponding stage Owner performs its own direct review and directly authors only the minimal classification and witness required by that stage's existing owner-private gate. The stage Owner does not copy, cite, or reread a Skill result or artifact.

## 7. Re-entry And Callers

Each invocation binds its current authority, planning, target, caller graph,
candidate set, diff/range/HEAD or base pair, tests and publication payload.
Adoption and material-change refresh follow [applicability](applicability.md).
Stage/caller or unrelated byte changes alone do not repeat semantic admission;
a new invocation still supplies current facts and cannot replay an old envelope.
Revisions refresh the judgments whose actual premises changed.

The classified and mechanism routers route only by validator-confirmed profile
and its fixed resume owner. They do not parse reasons or witnesses or repeat
qualification. After scope clarification, the original Owner rereads live
context and refreshes the affected admission through this same Skill. Unknown,
missing, duplicate, multiple, unmapped or consumer-mismatched results from an
entered invocation fail closed. A legitimately untriggered qualifier has no
result to consume and is not a missing-result error.

## Author candidate set

Author owns `author_candidate_set` (caller `guru-author-task-plan`), binding
current source/candidate locators and existing author_paths with author_identity.
Load [File-set identity](#file-set-identity) before constructing that target.
It does not require future design/implement files. Original planning_scenario_set
remains Approval-only and requires three current docs. Return classified and
mechanism results to Author; scope/diagnosis/blocked retain original owners.
