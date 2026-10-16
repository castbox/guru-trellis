# Current requirements and Delivery planning authoring contract

## Identity, input and authority

This is the sole planning writer. Before each write batch resolve the same
TaskId/generation, Direct Source, registered checkout and current session
through their original owners. Read live source, selected comments, current
requirement/design authorities and actual repository files. Ordinary dirty
work is valid. Missing identity returns to its original resolution owner;
never reset a branch, infer source selection from metadata, or create another
Task. Source selection retains locator/section/authority_kind. Normative design
is a constraint; advisory design remains advisory.

Current aggregate 2.0 has nine independent profiles and five exits. The old
Task-root development profiles and outputs remain validation assets for fixed
old installations; they are not current runtime fallbacks. Migration must
apply the complete matching workflow, consumers and package set after public
and private migration. A missing old gate re-enters its original semantic owner;
mechanically adding a DeliveryKey does not create a current pass.

## Whole-Task requirements, without Task Planning

`task_scope_requirements` consumes original Clarify source_selection and
revision_refs with mode/task_ref. It writes only root `prd.md`: overall
requirements, acceptance responsibilities and concrete source locators. It
never writes root design, implement or context, does not require a Delivery,
and does not assess an implementation mechanism or approve/activate a plan.
Public accepted_scope remains the single acceptance relation; a PRD seed or
file presence cannot establish it.

Review requirement completeness and source commitments, qualify genuine scope
questions with the original requirements_scope_set owner, and return exactly:
`scope_requirements_ready` with task_ref/requirements_locator to the original
Clarify scope continuation; `clarify_scope` for a real unresolved scope choice;
or `blocked` for named missing authority. No candidate qualification cache,
Task Planning state, or second requirements writer is introduced. Clarify
freshly reviews this actual output and original source selection before its
public accept_scope operation. On output loss, rerun this read-only validation
against the current whole requirements; on source-selection loss, refresh
Clarify rather than reconstructing its judgment from the PRD.

## Eight Delivery profiles

Every profile carries the exact opaque upstream DeliveryKey and task_ref.
Resolve its public planning_root/current selection through the installed API;
read the Task's overall scope separately. All three documents and two JSONL
files belong to that Delivery. D2 never overwrites D1's plan. Delivered/stopped
or historical keys are read as facts, not accepted as current Author entries.
The current stage owner performs legal rework to planning before writing here.
When the official context resolver has no key, pass this profile's explicit
DeliveryKey to the original projection for current-generation/C4/public-record
validation; no session selection is required or written. With context, retain
official current-selection matching, including missing/stale/conflicting stops.
After a successful delivery_initial_review requirements_ready, invoke Creation's
retire_creation_result port with task_ref/key. Only that producer validates and
retires its matching pending operation; Author never reads its private input.

| Profile | Actual producer and positive behavior |
| --- | --- |
| delivery_initial_review | Explicit Creation result plus original source_selection; converge slice requirements and actual candidate. |
| delivery_active_task_scope_change | Original Clarify published scope_ready plus selection/revision_refs and affected key; revise only affected slice requirements/candidate after root requirements publication. |
| delivery_wording_reentry | Actual Wording content_changed/change_refs; equivalent wording returns plan_ready; changed mechanism returns requirements_ready. |
| delivery_approval_revision | Actual Approval revision_actions; execution-plan-only fixes may return plan_ready; requirements/design fixes re-enter candidate assessment. |
| delivery_delivery_plan_revision | Delivery Review delivery_policy_gap/revision_refs; revise the same key's actual slice policy. Completion next_independent_delivery goes to Creation first, then delivery_initial_review on its new UUID. |
| delivery_requirements_revision | Original Clarify source_selection/revision_refs; converge the current slice without a caller-preselected decision. |
| delivery_solution_planning | Actual current Architecture candidate_assessment; write design/implement/context using its thin assessment. |
| delivery_architecture_conflict_resolution | Actual Architecture purpose/conflict_refs; revise the mechanism, returning to fresh candidate assessment or Clarify for a real requirement choice. |

All profiles can return clarify_scope or blocked with their precise refs and
same key. Missing/stale producer output refreshes that original owner. Routine
technical re-entry or missing ephemeral output requires no planning consent.

## Requirements and candidate before substantive solution writing

Converge PRD without lowering accepted scope to fit current Architecture.
Identify interfaces, mechanisms, ordering, compatibility and semantic owners.
Form only the current call-local design_locator, or design_facts with source
constraint_refs when no substantive design exists. Facts describe mechanisms,
not PRD narrative, approval or acceptance claims. Do not persist a parallel
candidate/proposal/cache. Invoke original normal-scenario and solution owners
with author_candidate_set, then applicable root-cause qualification. Feature
work retains not_incident_applicable; other exits follow their unique owners.
The actual requirements_ready output reaches independent Architecture
candidate_assessment before the first substantive design/implement write.

## Solution writing and complete positive capability

Consume only the actual candidate_assessment from this same candidate/key.
Use current constitution, baseline, required concerns and project checks, and
its impact/change path/decision refs, to author a genuine contribution and
necessary ADR candidate. Shared promotion remains with its original owner
after first committed full-diff independent Review, then fresh Check/commit/
Review. Planning cannot promote shared authority.

Delivery design owns one source-design disposition matrix: concrete source,
original commitment, retain/change/reject, real landing point, rationale,
impact and upstream handling. Check every normative commitment. Scope choices
return Clarify; Architecture conflicts return its owner; other technical
constraints require their real upstream disposition. With no normative design,
state that evidence rather than inventing an empty matrix. PRD/implement only
reference this sole matrix.

Implement owns one Delivery Policy: full by default; partial requires an
independent slice, remaining work and whole Completion conditions; staged
requires ordered/current stage, entry/exit, remaining stages and final conditions.
Delivery Review and Completion inspect policy, never write it. Select one
Docs SSOT strategy (ssot_first, delta_first, bootstrap_or_repair_docs,
no_docs_update_needed) and name the original RDT writer/direct consumer.
Reconcile a delta before final Phase 2. Preserve truthful causal and completion
semantics; package checks are not incident or remote-success proof.

Select business context for the installed official `task.py add-context
<task_ref> <implement|check> <file> <reason> --delivery <actual UUID>`.
Official scripts execute, while Author judges context relevance. Context JSONL
entries must name actual file/reason; no brainstorm second writer or hook patch.
An existing empty official context JSONL is a valid empty selection, including
byte-preserving migration. Require both regular files, validate every actual
entry, and let Author judge sufficiency; do not add entries solely to pass a
nonempty-file check or force a migrated clean candidate to be recommitted.

## Gate, typed exits and recovery

Review the complete current profile: source disposition, requirements,
mechanism/Architecture dependency, policy/Docs plan, official context, scope and
validation boundary. Invoke scripts/invoke.sh with the exact input and current
call-local owner result. The validator checks identity/files/minimal handoff;
it does not write planning, decide routes, or replace Approval. No persistent
Author checkpoint or authorization record is created.

requirements_ready.key/candidate -> Architecture candidate_assessment -> this
same key's solution_planning; plan_ready.key -> Wording -> fresh final_plan ->
adjacent Approval. Candidate assessment cannot substitute for final_plan.
clarify_scope -> original Clarify; blocked -> declared fail-closed stop.
scope_requirements_ready goes only to whole-scope Clarify, never Architecture.

No-PRD, PRD-only, seed, design-only, partial or stale documents are normal
states to read and converge; document count does not establish readiness.
Source/scope changes go through Clarify/root requirements before affected
Delivery writing. Mechanism changes refresh candidate assessment; equivalent
wording refreshes dependent gates only. Informational Related Work alone does
not replan. Approval does not write planning; Activation alone writes the public
Planning acceptance after current presentation/acceptance. Lost semantic
outputs fresh re-enter their producers; historical commits/PR/merge facts
remain facts. Byte-equivalent Plan2 path migration does not force a new commit.
Ordinary implementation repair/evidence completion stays with its existing
Phase 2/Completion owner unless actual planning authority changed.

## Fixed Delivery range

Select the development baseline, Delivery content range and PR target separately.
Use the existing `DeliveryProjection.content_base(key, development_base=...,
observed_target=...)` fact projection: recover the same Delivery candidate
first; otherwise use the unique greatest actual prior delivered head ancestral
to current HEAD, then the explicitly selected development baseline or unique
merge base of one observed target commit. Missing/incomparable facts return
to this owner; range selection never fetches or integrates. Record B and its
source in the existing Delivery design. Planning H0 is an observation, not the
final implementation head. Do not repeat D1 in D2 or add a Task baseline field.
