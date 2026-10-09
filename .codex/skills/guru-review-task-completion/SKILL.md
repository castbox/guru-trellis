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
