# Guru Check Task Contract

## Ownership And Profile

`guru-check-task` is the only semantic owner of the complete Phase 2 task check
and the single task-local `phase2-check.json`. It uses
`judgment_mode=semantic` and the exact stage order `forward_behavior ->
ai_review_gate -> conditional_human_confirmation -> recorder_validator ->
typed_exit`. The global workflow owns one mandatory invocation and the four
unique consumers. Official unchanged `trellis-check` workers provide raw
evidence only and cannot produce a Guru pass.

Workflow and standalone modes use the same eleven ordered preconditions from
`interface.json`. Standalone discovers the direct active task and expected
worktree, then performs the same planning, authority, ledger, agent, repository,
and freshness checks. Neither mode is self-contained outside the complete
compatible Guru Team preset.

## Semantic Closed Loop

1. Validate runtime/workspace and current checker-passed
   `guru-planning-approval-2.0:approved` evidence. Normal implementation HEAD
   and dirty drift after activation does not alone stale planning; changes to
   planning documents, Docs SSOT locator, authority, scope categories, task,
   base identity, or branch do.
2. Read the complete task scope, implementation handoff, code, tests, docs,
   specs, current `origin/<base>...HEAD` diff, full dirty state, repository
   validation commands, worker report, and unresolved verification.
3. Execute every applicable repository-defined check. Record exact argv,
   exit code, stdout/stderr SHA-256 and size, and a concrete result summary.
   Record each omitted check with a specific reason and impact.
   Bind the non-empty implementation/check agent id sets exactly to effective
   completed events for those roles, and bind worker evidence to the exact
   completed check agent set.
4. Classify each candidate before severity. Record its requirement/planning
   trigger, supported normal-path reproduction, disposition, and route basis.
5. Assign P0/P1/P2/P3 only to `current_scope`; every such candidate must link
   exactly one finding with the same candidate id and severity.
   `scope_change_required` routes to planning, while
   `followup_proposal` and `out_of_scope` do not block or authorize work.
   Untriggered malicious/hostile, TOCTOU/race, locking, fault-injection,
   crash-consistency, stress, or cross-OS proposals are out of scope.
6. Review requirements, design, implementation, tests, Docs SSOT, cross-layer
   contracts, compatibility, deployment/operations, agent recovery, and
   verification completeness. Link every finding and unverified item from at
   least one adequacy dimension; reject unknown, duplicate, missing, or
   dangling ids. Include CI/CD, container, K8s/Kustomize, DB
   migration and Makefile impact, including an evidence-based no-impact result.
7. Complete the AI Review Gate. Any open current-scope finding returns
   `implementation_required`; a scope/authority/planning change returns
   `planning_stale`; unavailable reliable evidence returns `blocked`.
8. After any implementation fix, start a new full round over the entire scope,
   current diff, all applicable commands, Docs SSOT status, and recovery chain.
   A partial or latest-chunk-only rerun cannot pass.
9. Send the AI-authored closed input to `record-phase2-check`, run
   `check-phase2-check`, and return exactly one typed exit.

## Artifact And Deterministic Boundary

New active evidence has `schema_version=2.0`, `skill_id=guru-check-task`, and
closed schema id `guru-phase2-check-2.0`. It binds task, planning, provenance,
Docs SSOT, handoff, agent assignment, repository snapshot, command and worker
evidence, scope qualification, adequacy, findings, unverified items, Gate,
human confirmation, exit, route, consumer, full-round identity and
`facts_sha256`.

The agent projection binds the task-local locator plus a digest of the stable
implementation/check assignment state: their agent records, status/liveness,
corrections, recovery links, exact completed id sets, and recovery closure. It
does not bind the complete file digest, so legal post-commit Branch Review
assignment/status/round/reuse metadata may append. Phase 2 agent or recovery
drift still fails closed, and Branch Review independently validates and digests
the complete current assignment artifact.

Recorder/checker may validate schema, paths, references, hashes, sizes, HEAD,
diff, dirty state, planning/ledger/agent linkage, recovery closure, full-round
identity and exit/consumer invariants. They never infer scope disposition,
severity, command sufficiency, semantic adequacy, Docs SSOT consistency, Gate
status, confirmation need, pass, or route. Legacy `--pass --coverage` is a
stable migration error. Active schema 1.0 requires complete semantic re-entry;
archived artifacts remain byte-for-byte historical.

Post-commit consumers may accept the recorded HEAD as an ancestor only when
every later committed non-metadata path was covered by recorded dirty paths and
the current worktree has no unreviewed non-metadata dirty path. They never
re-record a pass solely to match the commit HEAD.

## Typed Exits

- `passed` requires all ten adequacy dimensions passed, zero open current-scope
  finding, zero blocking unverified item, a completed agent recovery chain, a
  current full-round identity, passed AI Gate, null route discriminator, and
  consumer `skill:guru-create-task-commit`.
- `implementation_required` requires an open current-scope finding and
  consumer `workflow:guru-resume-implementation`.
- `planning_stale` requires stale planning or a scope-changing candidate. Route
  discriminator `reapprove_plan` maps only to `guru-approve-task-plan`, while
  `clarify_requirements` maps only to `guru-clarify-requirements`, through
  workflow target `guru-task-check-planning-router`.
- `blocked` requires a concrete blocker and consumer
  `stop:task-check-blocked`.

Unknown, multiple, ambiguous, unmapped, Gate-inconsistent, or
consumer-mismatched results fail closed.
