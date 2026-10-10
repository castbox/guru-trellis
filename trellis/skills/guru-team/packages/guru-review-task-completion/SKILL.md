---
name: guru-review-task-completion
description: Review all current task Delivery and evidence facts and select one bounded completion route.
---

# Guru Review Task Completion

Use this semantic owner after an exact Delivery merge result, or after a
normally finished task is Reactivated to its next generation and only fresh
validation is needed, without a new business Delivery. In that case use
`reactivation_validation` with the current active TaskLifecycleKey, the
preceding generation's unique committed terminal archive identity, and
current `reactivation` and `validation` evidence slots. The archive is historical
context, not a current Completion or Delivery result. Verify it against Git and
the Reactivate transaction before the AI gate; no old Finish/Cleanup receipt
proves the new generation complete. Old closeout/restore lineages remain
pinned-old or require individual manual disposition; they are not current
standalone inputs. Freshly resolve accepted scope, all historical Delivery
facts, the selected basis and its current evidence slots. Review remaining
work before authoring `semantic-result.json`. The wrapper binds the reviewed
identities and records the AI-owned route; a merge or passing test alone does
not establish Completion. `completed` requires no remaining work and emits a
`ResultRefDTO`. Other routes emit `TaskArtifactDTO` and `ReasonDTO`, or only
`ReasonDTO` for `blocked`.

Consume the actual current Architecture
`task_impact_sync(stage=acceptance_finish)` result before completion. That
owner applies its Downstream eligibility entry to still-applicable independent
conclusions and live facts; this caller neither relabels a Branch Review DTO
nor repeats the assessment merely because the caller changed. Changed facts
needing a new conclusion return through the existing independent assessment
route; missing committed review/promotion keeps its existing blocking route.
The Completion owner still judges whole-task scope and evidence separately.
Read the one Direct Source from `source.repo_ref + number`, or the legal
`no_issue` relation. Coordination/Related/Follow-up links neither add Closure
targets nor change the published `exact_source`, `reference_only`, `follow_up`
or `parent` meanings. Necessary external dependencies/evidence count only when
accepted scope uses them: missing evidence uses `evidence_pending`, unfinished
work uses the applicable remaining/revision route. Informational or out-of-scope
Follow-up changes do not block completion. Verify necessary updates to the
repository's actual long-term authority, or a reasoned non-applicability;
do not impose one Baseline type on every repository.

## Causal whole-task judgment

Before the semantic gate, read
`.trellis/spec/workflow/causal-completion-semantics.md`, current accepted
completion definition, live source Issue authority, all business Deliveries
and current evidence from their normal sources. Judge the entire scope using
the common evidence/dispositions, rather than this merge alone or a prior
stage pass. Preserve the actual observation layer and residual uncertainty.
No fixed evidence-field checklist or recorder output proves cause removal.

Ordinary features complete their accepted RDT scope. Diagnosis, mitigation and
implementation-only repairs may complete their own requirements without
claiming production root-cause closure. Inspect source/parent requirements
before selecting a closure disposition: do not choose `close_source` for one
still requiring root-cause repair or production closure. If the accepted
source scope truly needs revision, use `requirements_revision_required`;
Closure executes the current reviewed disposition rather than inventing one.
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
With no new evidence, wait for that condition instead of immediately invoking
another review. On arrival, reread applicable authority, whole scope and current
evidence: Delivery-based refresh retains the exact same-generation
`merge_result`; Reactivate-only refresh retains the current
`reactivation_anchor` and this generation's evidence. Historical merge,
Completion or Finish does not substitute for that anchor or new evidence.
Keep Delivery slots `planning`, `delivery_review`, `delivery_publication`
and Reactivate slots `reactivation`, `validation` unchanged; read production
facts from their existing source and bind the current evidence identity using
existing fields, without a production/global causal slot.

After merge/deploy, new facts may require `requirements_revision_required`,
`implementation_revision_required` or `additional_delivery_required` in the
same active task. Normal unfinished work remains `remaining_work`. Use
`blocked` only for a concrete missing authority/dependency or inability to form
a reliable judgment, not ordinary pending evidence. Only the whole accepted
scope with all required evidence complete can return `completed` to the sole
`guru-complete-task-closure` consumer, then Finish; Finalizer stays historical.

```bash
scripts/invoke.sh --input <completion-input.json> \
  --semantic-result <semantic-result.json> --json
```

Only `completed` projects to Closure. All other exits preserve the active task
and route to their declared owner. `evidence_pending` on the Reactivate-only
path re-enters `evidence_refresh` with `reactivation_anchor`, not `merge_result`;
author the same current-generation identity and fresh evidence using
`examples/reactivation-evidence-refresh-authoring.json`. Delivery-based
`evidence_refresh` retains its exact same-generation merge result.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
