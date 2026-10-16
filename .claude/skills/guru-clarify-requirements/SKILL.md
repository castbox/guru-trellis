---
name: guru-clarify-requirements
description: Clarify initial requirements, active-task scope changes, or explicit review requests through an evidence-first semantic loop with dialogue-local choices and typed exits.
---

# Guru Clarify Requirements

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

The current executing AI is this Skill's semantic owner. Read the complete
contract and perform its review yourself before authoring the current owner
result and calling record, check, and invoke. `owner_not_yet_executed` is an
internal state to continue this review, not a typed stop or a missing external
owner. Do not wait for another agent, agent ID, subagent evidence, or a
pre-existing owner result. Real missing authority or prerequisites still
follow this Skill's declared routes; runtime cannot supply your judgment.

Use this Skill after `guru-discover-change-context:context_ready`, when an
active task receives scope-changing input, or for an explicit standalone
requirements review.

For an initial proposed-change discussion, the actual current Discovery
`context_ready` remains this Skill's entry prerequisite. If this Skill or
brainstorm is loaded before that result exists, follow the current workflow's
mandatory initial mode/base/context graph first. Deferring file writes or
resource creation does not waive that entry. Method loading alone cannot end
the turn with a product question outside this owner's formal closed loop.

For active-task scope change, the canonical workflow mandatory invokes this
same Skill with an exact caller-aware `resume_target`; no caller may duplicate
classification or planning-update semantics.
Reread the task's one Direct Source (`source.repo_ref + number`), or its legal
`no_issue` relation, and current accepted scope. A Coordination Issue changing
without a Direct Source/scope change does not automatically change this task.
Once an external process has revised Direct Source, judge that live revision
through the existing scope-change routes. Related Work affects this round only
through its explicit necessary dependency/evidence/completion use; information
and out-of-scope Follow-up do not add obligations. Repository location and link
direction never select a source or topology. Preserve TaskId/generation when
the existing active-task route returns to Planning.

Before this owner creates a scope proposal, asks a scope question, or assigns a
terminal scope disposition to a newly observed scenario, form only candidate
refs and live locators and invoke `guru-qualify-normal-scenario` with
`requirements_scope_set`. Rejected candidates are final for the current
invocation and must not become clarification questions. The
`normal_scenario_scope_confirmation` public profile instead consumes only the
qualifier's minimal `scope_confirmation_required` projection and asks the exact
authority choice before returning to the declared original owner. It does not
repeat or reinterpret qualification and accepts no decision, reason, severity,
authorization, result locator, or qualification artifact.

Before a proposed clarification mechanism can affect scope, questions, or an
authority action, invoke `guru-qualify-solution-mechanism` with the same
profile. A `mechanism_revision_required` result removes or replaces only that
mechanism and returns here for fresh qualification; it is not a scope
confirmation route.

Before answering repository-searchable questions or evaluating duplicate and
prior-decision evidence, read `.trellis/spec/workflow/semantic-retrieval.md` and
apply it in this Skill's semantic gate. Do not infer absence from a
single-language zero result or expose the query process through the public DTO.

From the repository root, load
`.trellis/guru-team/skills/packages/guru-clarify-requirements/references/contract.md`;
when brainstorm is loaded, apply the current owner/stage/return constraint in that contract. Execute the semantic closed loop in its declared order,
ask at most one highest-value question per round, complete the AI Review Gate
and any real action/proposal choice before calling recorder/checker,
keep that authorization in the current dialogue, then return exactly one
declared typed exit.

Record only clarification rounds and answers that actually occurred. Unknown,
unasked, or unanswered choices are not refused, deferred, or answered; never
invent an interaction to fill the schema. When a required real choice cannot
be obtained, express the unresolved conflict through the existing blocked Gate,
not a fabricated round, answer, or pass. Follow Questions And Convergence in
the contract for the no-answer blocked shape.

A scope/product conflict does not erase known target identity or duplicate
facts. Complete the independent target disposition when the facts suffice,
even for blocked, and preserve the real Discovery snapshot. Null disposition
is not a blocked shortcut; it applies only where the target decision itself
is genuinely missing and the existing invocation contract permits it.
Return only successful public invoke stdout as the final DTO. Record/check
`typed_exit` is not a public exit; handle an invoke error truthfully through
the existing repair/re-entry rules, never by hand-writing a blocked DTO.

Use only the dispatcher wrappers for deterministic recording and checking.
Pre-task and standalone results are stdout-only. This Skill has no mutation
executor and no dedicated tracked clarification artifact. GitHub writes remain
AI-owned and require an exact current payload plus a live reread; the result
records only objective action and mutation facts.

Fail closed on missing/current-context drift, unresolved load-bearing questions,
invalid actual question lifecycle, stale/mismatched scope or source bindings,
unknown exits or missing runtime. Current schema2 scope calls use the independent
Delivery/whole-scope inputs and scope_ready 2.0 contract below. Non-active
intake and standalone profiles retain their existing contract. Private active
4.0 and scope_ready 1.0 describe pinned-old validation evidence only; current
installations do not invoke their Task-status path. Historical successful
results require fresh original owner re-entry and do not supply a current pass.
This package is not self-contained or portable. See the full contract for
objective checks and routes.

## Installed Commands And Authoring

Run from the repository root through the managed package wrappers:

```bash
bash .trellis/guru-team/skills/packages/guru-clarify-requirements/scripts/record-requirements-clarification.sh --mode workflow --input - --json
bash .trellis/guru-team/skills/packages/guru-clarify-requirements/scripts/check-requirements-clarification.sh --input - --json
bash .trellis/guru-team/skills/packages/guru-clarify-requirements/scripts/invoke.sh --invocation - --json
```

Use `--mode standalone` for standalone recording. Feed the reviewed semantic
owner JSON to record, its stdout result to check, and the complete invocation
envelope to invoke. Keep these values in memory; do not create repository files.
The contract's `Minimal Recorder Authoring` table lists required semantic fields
and the exact omittable fields. The full checked-result example is at
`.trellis/guru-team/skills/packages/guru-clarify-requirements/examples/requirements-clarification.json`;
remove only the listed derived fields when using it as an authoring shape, and
replace every example judgment and fact with the current reviewed result.
Agent discovery projections do not contain the package scripts or examples.

After the semantic gate and owner recorder/checker complete, invoke the command
above with the closed call-local public input,
`context_current` transition, and checked owner result on stdin to serialize
the minimal handoff. The runtime validates the envelope's mode, target, and
transition bindings, reruns the existing checker, and derives the route and
output from the checked `typed_exit` and declared transition. Callers cannot
select the route or provide a separate `typed_output` field. Private
clarification evidence is not a public input or output template.


At this candidate boundary, consume actual normal-scenario and solution-mechanism
outcomes before loading `guru-qualify-root-cause` with `requirements_scope_set`. Supply only eligible
refs. New or materially changed incident/protection mechanisms enter that owner;
ordinary features receive its stable applicability disposition. Consume a
still-applicable same-mechanism conclusion on later stages and independently
review this stage's current work/evidence; caller change alone does not repeat
qualification. Root `classified` continues this stage, retaining diagnosis or
mitigation disposition without claiming repair. `mechanism_revision_required`
removes/replaces that mechanism and reenters; `diagnosis_required` pauses only
the unsupported repair and continues bounded investigation of the returned
gaps through this owner, then resubmits. A concrete `blocked` stops. Do not turn
symptom suppression into unrelated scope confirmation, cache qualifications,
or use qualification as completion. Actual scope changes use existing routes.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.

Use the current declared profiles and caller-aware context returns in the contract.
Preserve selected source locators and their normative/advisory roles for current
Planning; do not decide final design dispositions or create an alternate owner.

## Delivery scope revision

Use delivery_active_task_scope_change with exact DeliveryKey, or
delivery_task_scope_revision with TaskKey when whole-task scope changes and
no current Delivery is needed. Initial whole scope after public Task creation
uses the latter profile with source_exit=created and the Creation resume target.
Read the current source and whole-task authority; if a Delivery exists, also
read its affected plan before the same semantic Clarify gate. Null accepted_scope
is not approval. Return source_selection/revision_refs and scope_action (revised,
no_change or withdrawal_required) to Author task_scope_requirements; do not
publish scope before Author writes the reviewed root PRD.
Partial revision returns to the same Delivery's earliest affected owner after
scope acceptance. Whole withdrawal returns to its current stage owner for legal
public stop and automatic selection release; task_scope must not impersonate
another role. Existing PR/history survives; PR closure/cleanup remain independent.
No-current-Delivery closeout and evidence refresh do not create empty slices.
The old active_task_scope_change activity input requires the pinned old complete
installation; it is not a current fallback or schema-2 writer.

## Current schema2 whole-scope continuation

The new distribution retires legacy active_task_scope_change runtime; its old
schema remains pinned-old validation evidence. delivery_active_task_scope_change
and delivery_task_scope_revision judge current source and overall scope, return
scope_ready 2.0 to the same Author task_scope_requirements, and do not publish
scope or write PRD. They preserve source_selection/revision_refs; files and
metadata cannot reconstruct missing selection.

task_scope_requirements_acceptance consumes only the actual scope-only Author
root requirements_locator plus the adjacent original selection/revision_refs.
Freshly review that whole PRD and scope commitments, then invoke the public
accept_scope operation with its real AuthorityRef. scope_ready 2.0 on this
profile carries TaskKey to Creation/affected Delivery routing, not back to root
writing. Scope_action is route intent; the current Delivery stage owner alone
performs legal rework or full withdrawal stop/release. No current Delivery is
required for whole-scope acceptance. Public operation retries recover the same
accepted authority; they do not create new Task, Delivery, or current gate pass.
