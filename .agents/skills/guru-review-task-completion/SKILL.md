---
name: guru-review-task-completion
description: Review all current task Delivery and evidence facts and select one bounded completion route.
---

# Guru Review Task Completion

Use this semantic owner after a reviewed Delivery result or an evidence-refresh
request. Read the current task scope, requirements, Delivery history and
validation evidence before authoring `semantic-result.json`. The wrapper only
records and validates the AI-owned route; it never infers completion from a
merge, test, Issue state or archive.

```bash
scripts/invoke.sh --input <completion-input.json> \
  --semantic-result <semantic-result.json> --json
```

Only `completed` projects to Closure. All other exits preserve the active task
and route to their declared owner.
