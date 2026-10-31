---
name: guru-review-task-completion
description: Judge formal Task-wide Completion when invoked by the workflow or requested as a formal stage result, covering all Deliveries and evidence under existing prerequisites and routes. 检查需求是否做完 or 审核需求完成度 alone does not select formal Completion; independent read-only assessment belongs to guru-review-change even when a Task exists.
---

# Guru Review Task Completion

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Enter this Skill for formal whole-Task Completion under the workflow's review
entry. An independent read-only assessment of requirement coverage retains its
requested scope even with a bound Task and enters `guru-review-change` in
standalone mode.

Apply `.trellis/spec/workflow/quality-guidelines.md#specialist-review-standards`
within this owner's whole-task evidence review. Read applicable specialist
evidence against current accepted obligations and actual Delivery results;
identify uncovered work and required evidence gaps. Preserve this Skill's
formal Task entry and completion routes; specialist or individual Delivery
passes never establish whole-task Completion.

Use this semantic owner for Task-wide completion, including Delivery merge,
withdrawal, evidence-only refresh or Reactivate validation with no current
Delivery. Current profiles are `delivery_completion`,
`delivery_evidence_refresh`, and `delivery_reactivation_validation`.
All consume `task_ref` and public `task_key`; evidence refresh additionally
consumes the concrete source exit/reason, and Reactivate validation consumes
its actual preceding archive anchor. Reread current accepted scope and every
actual Delivery result across generations. The semantic result binds those
exact scope/fact identities, minimum current evidence and remaining work.
Do not infer completion from all known Deliveries being terminal: unallocated
scope, changed acceptance or missing causal evidence remains this owner's
whole-task judgment. A fresh public `complete_task` writes only the actual
completed conclusion after the full semantic review. Recover lost output from
the identical result; do not synthesize another result or require an empty
Delivery. `completed` emits the existing minimum ResultRef to Closure; other
continuation exits emit `task_ref`, `task_key`, and the concrete ReasonDTO.

For a manual merge recorded by original Merge, read the actual DeliveryFact
candidate/head and original Publication separately. Upstream `reviewed_head`
in the terminal fact identifies actual content; it is not a new Check/Review
pass. Compare the full published-to-actual and PR delta, including paths beyond
the original candidate, current accepted authority, actual CI/reviews and
scope-required evidence. Old gate applicability against the original candidate
alone cannot establish that the actual head was reviewed. Reuse still-applicable
same/equivalent evidence; changed content returns through affected original
owners. Required evidence gaps select `evidence_pending`, actual unfinished
work selects its applicable remaining/revision route, and changed authority
selects `requirements_revision_required`. Non-required CI does not add scope.
Pending/cancelled/missing/failed remains its real state even when MERGED is
reliable. Never demand another merge, invent pass, or infer `completed` from
the recovered fact. Public aggregate facts remain readable without trailers;
history discovery is not a Completion prerequisite.

Consume the actual current Architecture
`task_impact_sync(stage=acceptance_finish)` result before completion. That
owner applies its Downstream eligibility entry to still-applicable independent
conclusions and live facts; this caller neither relabels a Branch Review DTO
nor repeats the assessment merely because the caller changed. Changed facts
needing a new conclusion return through the existing independent assessment
route; missing committed review/promotion keeps its existing blocking route.
The Completion owner still judges whole-task scope and evidence separately.
An already reviewed and promoted contribution is not promoted again at
Completion. Missing or changed Architecture facts return to that original
owner; knowledge acceptance does not establish merge, deployment or adoption.
Read the one Direct Source from `source.repo_ref + number`, or the legal
`no_issue` relation. Coordination/Related/Follow-up links neither add Closure
targets nor change the published `exact_source`, `reference_only`, `follow_up`
or `parent` meanings. Necessary external dependencies/evidence count only when
accepted scope uses them: missing evidence uses `evidence_pending`, unfinished
work uses the applicable remaining/revision route. Informational or out-of-scope
Follow-up changes do not block completion. Verify necessary updates to the
repository's actual long-term authority, or a reasoned non-applicability;
do not impose one Baseline type on every repository.

## Stage facts, gaps and current results

For the whole accepted scope and every actual Delivery, separately express the
applicable contract authority, source implementation, artifact deployment/entry
reachability, initialization or enablement, consumer adoption, and original-request
end-to-end acceptance in existing reason/evidence/summary fields. Name the actual
capability, object, environment and basis. Explain non-applicability; add no DTO
fields. One dimension does not prove another. Contract, source and deployment
facts remain established when the capability is not enabled; initialization, adoption
and end-to-end claims retain their own evidence gaps. Partial implementation does
not satisfy unrelated or still-unimplemented accepted scope.

For a corrected decision, apply Migration and retirement in
`.trellis/guru-team/skills/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md`.
Distinguish the new decision taking effect, the new entry or requirement being
delivered, old implementations migrating and environment cutover. Inspect the
same decision's remaining adopters and the actual coexistence basis or necessary
adaptation/exit. Promotion and delivery of a new entry alone do not complete
that correction. Migration within accepted Task scope remains unfinished when
assigned to a later Delivery; justified existing implementations outside that
scope do not
automatically block completion. Use the actual remaining/revision route for
missing implementation and reserve `evidence_pending` for a real evidence gap.

Locate each unsatisfied requirement and its dependent operation before routing:

- Necessary code or a consumer is unimplemented: identify the actual Delivery
  that can legally carry the change before choosing the continuation below.
  More observation cannot implement it.
- The mechanism adds an unsupported enablement/migration prerequisite: consume
  the original qualification's basis, necessity and operation scope; return to
  the original mechanism/Planning owner and Architecture as applicable. Do not
  ask for evidence of that unsupported prerequisite. A real source/scope conflict
  instead uses the original requirements revision owner.
- An authoritative prerequisite is necessary for the claimed operation, but its
  external evidence has not arrived: retain `evidence_pending` and its original
  `evidence_refresh` consumer, concrete acquisition owner and refresh condition.
- An unknown environment or effect is unrelated to accepted completion: state
  that unverified boundary and continue the lawful completion judgment.

Missing activation or switch evidence blocks only dependent enablement, adoption,
acceptance or completion claims. It does not retract established facts or block
unrelated operations. Mixed gaps keep their actual responsibilities; do not label
all missing work as external evidence or turn technical elaboration into scope
revision. Only fully satisfied accepted scope with necessary evidence can complete.

Read Stage limits and result observations in
`.trellis/guru-team/skills/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md`.
Check that current result entries state their observation cutoff and accurately
reference later original public results and Git/PR facts. Retain raw commands,
old failures and then-unknown facts; do not require prose to record its own final
pass/HEAD or archived result. Genuine missing current content returns to its
original writer and normal affected-coverage review. Completion does not write
shared current, replay completed promotion or create an empty Delivery/extra
commit for a terminal-result update. Closure and Finish retain their own boundary.

## Causal whole-task judgment

Before the whole-task judgment, actually load
`.trellis/guru-team/skills/packages/guru-author-task-plan/references/planning-body.md`
and that package's `templates/task-prd.md`, `templates/delivery-prd.md`,
`templates/delivery-design.md`, and `templates/delivery-implement.md`.
Read the whole Task PRD/accepted scope, applicable Delivery bodies and all actual
Delivery results across generations. Load necessary planning references and
their associated conditions; a link or prior approval cannot replace the read.
Apply the contract within this owner's whole-task scope. Preserve each
Delivery's historical identity and distinguish its old acceptance from current
obligations. Check remaining responsibility and the actual Completion
conditions across full, partial and later Deliveries.

Judge required actual Agent writing/review evidence separately from
deterministic and installation checks. Missing required evidence retains
`evidence_pending`; actual writing or implementation omissions use the
existing revision/remaining-work routes to the earliest affected owner, while
changed requirement authority uses `requirements_revision_required`.
Technical elaboration alone does not revise product scope. Completion never
writes planning or accepts a batch result as proof of the entire Task.

Before the semantic gate, read
`.trellis/spec/workflow/causal-completion-semantics.md`, current accepted
completion definition, live source Issue authority, all business Deliveries
and current evidence from their normal sources. Judge the entire scope using
the common evidence/dispositions, rather than this merge alone or a prior
stage pass. Preserve the actual observation layer and residual uncertainty.
No fixed evidence-field checklist or recorder output proves cause removal.

Ordinary features complete their accepted RDT scope. Diagnosis, mitigation and
implementation-only repairs may complete their own requirements without
claiming production root-cause closure. Read source/parent requirements and
retain their remaining responsibilities in the completion evidence. Completion
judges the accepted Task scope; it does not select an Issue disposition or
author Closure's action set. A satisfied Task may return `completed` while its
source still has repair responsibility. Closure independently reviews that
source and decides its actual action, including `retain_open`, under its own
contract. If the accepted Task scope truly needs revision, use
`requirements_revision_required`.
A diagnosis that itself requires identifying the cause remains unfinished
while the cause is unknown. Required investigation/work uses `remaining_work`
or the actual existing revision owner, not automatic production pending.

For production repair requirements, judge same-input or strictly equivalent
production evidence under the common authority. Sufficient lawfully obtained
evidence can support `completed` even when original inputs cannot safely be
replayed. Insufficient evidence uses `evidence_pending`, with the concrete gap,
existing acquisition owner and condition for refresh in existing reason/evidence
fields. Preserve the active task; do not archive, create a replacement task,
force dangerous replay or request business production access.

`evidence_pending` has exactly the existing `evidence_refresh` consumer.
With no new evidence, wait for its acquisition condition. On arrival, reread
current scope and all actual Delivery facts. Historical Completion/Finish never
substitutes for fresh evidence. The refresh profile does not require a current
Delivery or reuse an old merge DTO as current approval.

After merge/deploy or Reactivate validation, new facts may require further work
in the same active Task. Choose the implementation continuation from the actual
current public Delivery facts:

- Use `implementation_revision_required` only when an actual current nonterminal
  Delivery owns that work and can legally rework through its original phase
  owner. Identify that Delivery and its reviewed planning in the existing
  reason/evidence fields; the consumer resolves its real continuation before
  Phase 2.
- If the implementation needs a new slice, or no current nonterminal Delivery
  can legally carry it, use `additional_delivery_required`. Its existing
  consumer enters original Delivery Creation and Planning before implementation.
  A merged or stopped Delivery is historical; do not reopen it, manufacture a
  selection, or implement before the new slice's required planning and activation.
- Changed accepted authority uses `requirements_revision_required`. Ordinary
  unfinished investigation or other work that needs no new implementation slice
  retains `remaining_work`; required external evidence retains `evidence_pending`.

Use `blocked` only for a concrete missing authority/dependency or inability to form
a reliable judgment, not ordinary pending evidence. Only the whole accepted
scope with all required evidence complete can return `completed` to the sole
`guru-complete-task-closure` consumer, then Finish; Finalizer stays historical.

```bash
scripts/invoke.sh --input <completion-input.json> \
  --semantic-result <semantic-result.json> --json
```

Only `completed` projects to Closure. All other exits preserve the Task and
route to their declared owner. Evidence-only recovery preserves Task identity,
while implementation/new business work uses a genuine same/new Delivery.
Completion, Closure, Finish archive persistence and Cleanup are distinct facts.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.

## Bounded history consumption

Read all current Task/generation scope and actual Delivery/evidence facts. A
history result proves only its explicit cutoff; later unrelated Task or
bookkeeping commits do not require a requery, integration or business gate
refresh. If this Task has a new Delivery or changed required evidence, obtain
only missing facts and rejudge affected Completion conclusions. Never use the
old cutoff to claim current completeness. When history is actually needed,
call the original Merge `discover-task-deliveries` owner with query1 (historical
trailer-only callers) or query2 (public recorded facts). Consume its result3.0
`task_identity`, `repo_ref`, `base_ref`, `cutoff_commit` and `deliveries` with
the explicit query context; no producer-private state is needed. Preparation
belongs to that owner and never requires a caller fetch or Task integration.
On lost output, reenter the original query and read its newly explicit cutoff;
do not infer an unobserved former cutoff. Obtain a bounded new result only for
known missing same-Task facts/evidence, then rejudge affected conclusions. No
remote SHA equality qualifies Completion, and history is not a new mandatory
prerequisite when public Task facts already suffice. Adopt the matching
result/consumer combination described in MIGRATION-569.
