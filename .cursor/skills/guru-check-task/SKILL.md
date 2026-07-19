---
name: guru-check-task
description: Check a complete task through scope-first semantic review, full validation evidence, Docs SSOT reconciliation, finding reruns, and four typed exits.
---

# Guru Check Task

Use this Skill after implementation handoff and official unchanged
`trellis-check` evidence exist, and before `guru-create-task-commit`. Load
[references/contract.md](references/contract.md) before acting.

Validate all eleven entry preconditions in workflow or standalone mode. Read
the complete approved task scope, implementation handoff, current diff,
code/tests/docs/spec, repository-defined commands, worker evidence, Docs SSOT
Plan, issue ledger, and agent recovery chain. Classify every candidate issue
before assigning severity, complete all adequacy dimensions, and perform the AI
Review Gate. Current-scope findings require implementation and a later full
rerun; scope-changing findings route back to planning or clarification.

Call the recorder and checker only after the semantic result exists. They
validate objective schema, linkage, digests, repository snapshot, recovery,
full-round, and exit/consumer facts; they never decide scope, severity,
adequacy, Docs SSOT consistency, pass, or route. Return exactly one of
`passed`, `implementation_required`, `planning_stale`, or `blocked`. Fail
closed when evidence or the complete compatible Guru Team preset is missing.
This package is not self-contained or portable.
