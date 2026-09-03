# Solution-Mechanism Qualification Contract

## Ownership

`guru-qualify-solution-mechanism` is the only semantic owner for deciding
whether a proposed solution mechanism can carry business correctness, identity,
concurrency, cancellation, recovery, inspection, monitoring, publication
gates, or business evidence. `guru-qualify-solution-mechanism` remains the separate
owner of whether a scenario itself is in scope. Neither owner substitutes for
the caller's planning, implementation, test, review, or publication judgment.

## Closed callers

The supported profiles are the ten existing lifecycle profiles:
`task_free_pre_write`, `task_free_evolution`, `requirements_scope_set`,
`change_request_candidate_set`, `planning_scenario_set`,
`implementation_discovery`, `base_impact_candidate_set`, `phase2_candidate_set`,
`branch_review_candidate_set`, and `publication_candidate_set`. Each profile
fixes one caller and return owner. The caller supplies only the current target,
candidate references, and live locators; it does not supply a decision, severity,
approval, prior result, worker report, or mechanism classification.

## Semantic review

For every candidate, reread current authority and the real dependency/caller
graph, then answer in order:

1. Identify exact current requirement authority and architecture/spec authority.
2. Prove the real supported entry and consumer that exercise the mechanism.
3. What business authority is the mechanism carrying, and where is that authority
   supposed to live?
4. Reproduce an honest normal action sequence and observe whether it preserves
   required terminal and recovery semantics without relying on OS/kernel/process/
   descriptor identity.
5. Establish scope provenance only after the first four checks pass; otherwise
   qualification is blocked.

This review is based on the relationship to the repository normal-operation
boundary. Observe that current required behavior actually fails before treating
the mechanism as a qualified defect.

The prohibition is semantic, not lexical. A helper, test, framework, shared
library, deployment utility, monitor, validator, recovery path, or evidence
producer is equally covered when it delegates business authority to a forbidden
primitive. Conversely, normal file/directory I/O is qualified when it only
persists or reads ordinary state. Passing tests, fail-closed behavior, race or
TOCTOU claims, production pressure, security best-practice claims, and an
already-implemented framing do not create an exception.

## Candidate decisions

Use exactly one decision per candidate. For compatibility with the shared
qualification schema, `qualified_current` is the wire name for the semantic
`qualified_application_mechanism` outcome:

- `qualified_current` (`qualified_application_mechanism`): current authority and the real supported
  graph show an appropriate application-level authority.
- `qualified_explicit_nonstandard`: current authority explicitly requires a
  supported nonstandard mechanism without delegating business authority to OS.
- `qualified_approved_expansion`: a current user scope choice explicitly adds it.
- `scope_confirmation_required`: authority and graph are current, but a genuine
  unresolved mechanism scope choice remains. A forbidden primitive never uses it.
- `rejected_no_authority`, `rejected_unsupported_entry`,
  `rejected_not_reproduced`, `rejected_out_of_scope`: the candidate cannot be
  promoted for the stated reason.
- `mechanism_removed`: a task-introduced forbidden mechanism has no qualified
  purpose and must be removed.
- `mechanism_replaced`: a task-introduced forbidden mechanism must be replaced
  with an application-level mechanism serving a qualified requirement.
- `blocked`: authority, graph, target identity, or candidate evidence is
  missing, stale, or incomplete.

Any use of OS lock, `/proc`, process identity/liveness, FD identity/inheritance,
signals, or an equivalent primitive as business authority must produce the
`mechanism_revision_required` exit, never ordinary scope confirmation. Existing
violations are reported only with repository, owner layer, consumer, and
business capability; this Issue does not migrate another repository or perform
production operations.

If repository authority explicitly excludes a candidate, choose `rejected_out_of_scope` even if the candidate also lacks a supported entry or reproduction;
Do not downgrade an explicit exclusion. Quarantine severity, implementation
pressure, test coverage, best-practice claims, and theoretical bypass framing.

Only when no explicit exclusion applies may a supported normal entry qualify the
mechanism; A supported normal entry does not turn an excluded mechanism into a
current requirement. Only when no explicit exclusion applies should a caller
promote the mechanism. the mere presence of explicit authority is not an approved expansion.
Reverse-prove security or attack framing against the supported honest path; do
not treat a scanner or keyword match as a decision.

## Gate, exits, and state

The AI must review every candidate exactly once in the current invocation. The
four exits are `classified` (all candidates qualified or rejected),
`scope_confirmation_required` (only a genuine unresolved scope choice),
`mechanism_revision_required` (a forbidden task-introduced mechanism), and
`blocked` (reliable semantic judgment is impossible). The latter two route to
their dedicated mechanism owner and blocked stop respectively.

Recorder/checker commands are stdin/stdout only. They may verify schema shape,
fixed profile/caller identity, current Git and planning identities, safe
locators, exact candidate coverage, digests, and consumer binding. They may not
inspect mechanism meaning, select a route, persist authorization, or create a
qualification report, ledger, checkpoint, handoff, or result file. Any material
authority, dependency graph, mechanism, candidate, diff, test, or target change
requires a complete fresh invocation.
