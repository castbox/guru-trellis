# Root-Cause Candidate Qualification Contract

## Owner and entry

This semantic owner owns candidate admission, applicability and return routes.
Caller first consumes actual normal-scenario outcomes for real/current/supported
scope and solution-mechanism outcomes for authority placement, supplying only
eligible refs and current evidence locators. Root owner does not recursively
invoke them, duplicate their judgment, classify severity or decide completion.
Workflow and standalone have identical preconditions and review.

Read accepted scope, current Issue/RDT/Architecture, code/tests, available
failure evidence and actual proposed behavior. Public input has ten closed
caller profiles, current targets, refs and locators; it accepts no goal,
classification, pass, prior root result or private checkpoint. Infer actual
goal from scope and behavior, never labels, paths or keywords. A repair with
side effects cannot escape review by naming itself diagnosis. Existing code,
green tests, independent review, best practice and security pressure are not
causal authority. Only supported honest normal paths enter findings.

## Forward behavior and AI Review Gate

Review the entire candidate set using goal-specific dimensions. Unknowns are
honest gaps, never invented evidence. The call-local result has one goal,
classification, reason and goal-specific evidence object per ref. This is not
a persisted questionnaire or public handoff.

- **Ordinary feature:** inspect applicability and actual behavior. With no
  incident-resolution or protection mechanism, return `not_incident_applicable`
  and continue the original stage without an incident questionnaire.
- **Diagnosis:** real failure and bounded investigation allow observation,
  collection and hypothesis testing. Review action impact. Unknown first
  failure/causal chain stays in evidence gaps. `diagnosis_incomplete` returns
  `classified` and continues diagnosis; never require proof of the conclusion
  as investigation entry.
- **Mitigation:** review actual effect evidence, risks, legitimate input and
  consumer impact, conditions, direct owner, expiry/exit, and remaining known
  or unknown cause. Supported bounded mitigation yields `mitigation_only`.
  Unknown cause alone is no blocker. Emergency mitigation retains existing
  production permissions and side-effect boundaries; qualification grants no write.
- **Root-cause fix:** locate the first deviation on the original object/stage,
  causal chain, hypothesis and competing explanations. Identify changed state,
  algorithm, resource behavior or external interaction. Reverse-prove the
  counterfactual: without changing cause does failure persist, move earlier,
  change name, become delayed or transfer owner? What happens without the
  mechanism? Keep the same input or strictly equivalent sample in the original
  path and plan separate admission, failure stage, classification and final
  outcome observations. Consider a smaller mechanism nearer the cause.
  Supported evidence and plan yield `root_cause_mechanism_eligible`.
  Missing causal/counterfactual basis yields `diagnosis_incomplete`, precise
  evidence gaps and `diagnosis_required`; pause this repair while allowing
  legitimate investigation and independently qualified mitigation.
- **Protection:** bind protected object, real harm without blocking, direct
  owner, current RDT/Architecture authority, current-layer necessity and
  legitimate input impact. Credential/permission/integrity/ownership/identity/
  idempotency/lease/fence mechanisms yield `protection_invariant_eligible` when
  these facts support them. Generic safety or recommended defaults cannot
  create rejection authority.

Range/configuration gates, retry/backoff/budget increases, partial fallback,
normalization/truncation, error mapping, last-error-only observation and sample
exclusion are not classified by their technical names. Without supported
repair, bounded mitigation or independent protection basis, behavior that only
hides/transfers failure is `symptom_suppression_rejected`. Return remove/replace
of that mechanism, retain failed samples and accepted scope, and do not divert
to unrelated scope confirmation. Green tests/lower counts alone are no proof.
Distinguish an unproved repair hypothesis from demonstrated suppression.
Concrete unavailable authority/entry/external evidence preventing the current
goal review is `blocked`. Unknown root cause does not itself block diagnosis
or mitigation. Confirmation cannot override failed semantic judgment.

AI reviews all refs and selects exactly one exit. Human interaction serves
only real scope/authority choice or side effects through the existing owner.
Mapped exits, mechanism revision, same-scope diagnosis and stale reentry proceed
automatically. Then invoke `scripts/invoke.sh --invocation -` with
`{"schema_version":"1.0","semantic_result":<AI-authored result>}` on stdin.
Recorder/checker validate schemas, exact coverage, current Git/planning/locator
facts, local digests, enum aggregation and unique consumer. They cannot choose
goals or judge sufficiency. No qualification output path, artifact, cache,
checkpoint, authorization or investigation history is written to tracked or
ignored storage. Commands are process-local stdin/stdout.

## Typed exits and consumers

Aggregation validates AI-selected results: blocked before mechanism revision
before diagnosis required before classified. A mixed set pauses promotion until
the existing owner revises/reviews the complete set. This is not a classifier.

| Exit | Output beyond exit_id | Unique consumer |
| --- | --- | --- |
| classified | profile, continuation_id, candidate_dispositions(ref, classification) | guru-root-cause-classified-router |
| mechanism_revision_required | profile, continuation_id, revision_candidates(ref, reason) | guru-root-cause-mechanism-router |
| diagnosis_required | profile, continuation_id, diagnosis_candidates(ref, evidence_gaps) | guru-root-cause-diagnosis-router |
| blocked | reason | root-cause-qualification-blocked |

Consumer owns its input schema under `consumers/`; projection is direct.
Profile selects the existing owner/resume mapping in the workflow table.
Refs/classification distinguish continuing diagnosis, mitigation, protection,
repair or ordinary feature. Revision refs/reason identify remove/replace.
Diagnosis refs/gaps identify paused repairs and bounded investigation.
Continuation identifies only the call-local context, never authorization,
approval or a cross-stage cache. No full result crosses the public boundary.
Unknown, multiple, stale or unmapped exits stop closed.

## Stage reuse and completion boundary

An unchanged mechanism with still-applicable scope, authority, conditions and
causal evidence consumes the earlier minimal conclusion in the conversation,
or an existing owner gate already requiring it. Next stage independently
reviews current implementation/evidence. Stage/caller change alone does not
repeat qualification. New/materially changed behavior, conditions, authority
or causal evidence, stale facts or lost conclusions reenter from live sources.
Never reconstruct pass or create a qualification database.

Diagnosis route pauses only unsupported repair, continues bounded collection
through the existing stage owner and then resubmits. Branch Review changes use
its existing implementation route. Delivery owns its planning/implementation/
scope/blocked routing; no new task-work exit is invented.

Read `.trellis/spec/workflow/causal-completion-semantics.md` for the common
evidence/disposition authority. This owner continues to judge candidate
admission under the goal-specific contract above; it does not judge completion
or duplicate the common semantics. Each subsequent stage applies that same
authority to its own actual work/evidence and retains its existing routes.
Qualification alone establishes neither a stage pass nor whole-task completion.
