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

The global workflow owns mandatory invocation and typed-exit routing. Each caller owns only its profile-specific candidate set and its post-qualification stage judgment. Workers and reviewers may report a candidate reference, observed behavior, locators, and a minimal reproduction hint; they do not assign severity, scenario class, qualification, or an implementation route.

## 2. Closed Profiles And Callers

Use exactly one profile and its fixed caller/resume owner:

| Profile | Caller and resume owner |
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
| `publication_candidate_set` | `guru-review-task-publication` |

Workflow and standalone modes use the same evidence and judgment. Each input is a closed profile contract containing its fixed profile and caller, one current target identity, a non-empty unique `candidate_refs` set, and the minimum locators needed for live reread. Do not accept severity, scenario class, a proposed decision or exit, authorization text, an earlier qualification result, a shared artifact locator, a raw worker report, a search transcript, or a caller assertion that a path is normal.

## 3. Scope-First Review

Reread the live requirement authority, current planning, actual caller and consumer, relevant code and diff or base range, applicable tests, and repository contracts. Do not substitute a worker summary, an existing implementation, an existing test, or a prior invocation.

For every candidate, judge in this fixed order:

1. Identify exact current requirement authority.
2. Prove the real supported entry, caller, and consumer.
3. Reproduce an honest normal action sequence without falsification, attack behavior, or deliberate workflow bypass.
4. Observe that current required behavior actually fails.
5. Establish scope provenance only after the first four steps pass.

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

The deterministic runtime validates only closed shape, identities, freshness facts, enums, exact candidate coverage, and the declared consumer binding. It must not derive the exit from decision words, judge scope or witness sufficiency, interpret severity, or choose a route.

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

Never create or request an output path, result locator, checkpoint path, temporary result file, tracked file, ignored `.trellis/.runtime/**` qualification state, cross-process locator, report, candidate or rejection ledger, approval, signoff, assignment, handoff, or transcript. `artifacts` and `private_artifacts` are empty. This Skill and its runtime never write a Phase 2, Branch Review, or Publication gate. After consuming the process-local stdout, the corresponding stage Owner performs its own direct review and directly authors only the minimal classification and witness required by that stage's existing owner-private gate. The stage Owner does not copy, cite, or reread a Skill result or artifact.

## 7. Re-entry And Callers

The result is valid only for its current authority, planning, target, caller graph, candidate set, diff/range/HEAD or base pair, tests, and publication payload. Any relevant change requires a complete fresh invocation. A mechanism revision, scope choice, or finding fix also requires a full rerun.

The classified and mechanism routers route only by validator-confirmed profile and its fixed resume owner. They do not parse reasons or witnesses and do not repeat qualification. After scope clarification, the original Owner rereads live context, reconstructs the appropriate profile input, and invokes this Skill again. Unknown, missing, duplicate, multiple, unmapped, or consumer-mismatched results fail closed.
