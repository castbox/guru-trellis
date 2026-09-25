---
name: guru-review-task-completion
description: Review all current task Delivery and evidence facts and select one bounded completion route.
---

# Guru Review Task Completion

Use this semantic owner after an exact closeout/Delivery merge result or an
evidence-refresh request. Freshly resolve the TaskLifecycleKey, accepted scope,
the selected merge lineage and its current evidence slots. Review remaining
work before authoring `semantic-result.json`. The wrapper binds the reviewed
identities and records the AI-owned route; a merge or passing test alone does
not establish Completion. `completed` requires no remaining work and emits a
`ResultRefDTO`. Other routes emit `TaskArtifactDTO` and `ReasonDTO`, or only
`ReasonDTO` for `blocked`.

```bash
scripts/invoke.sh --input <completion-input.json> \
  --semantic-result <semantic-result.json> --json
```

Only `completed` projects to Closure. All other exits preserve the active task
and route to their declared owner.
