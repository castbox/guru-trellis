---
name: guru-check-task
description: Check a complete task through scope-first semantic review, full validation evidence, Docs SSOT reconciliation, finding reruns, and four typed exits.
---

# Guru Check Task

Use this Skill after implementation and repository-defined check evidence exist,
and before
`guru-create-task-commit`. Load
[references/contract.md](references/contract.md) before acting.

Validate all ten entry preconditions in workflow or standalone mode. Read
the complete approved task scope, implementation terminal result, current diff,
code/tests/docs/spec, repository-defined commands, Docs SSOT Plan, and issue
ledger. Classify every candidate issue
before assigning severity, complete all adequacy dimensions, and perform the AI
Review Gate. Current-scope findings require implementation and a later full
rerun; scope-changing findings route back to planning or clarification.

The public input id `implementation_handoff` is retained for compatibility. It
is an embedded evidence collection that this semantic owner assembles from the
terminal result plus live repository facts; it does not require a separate
`implementation-handoff.md`.

Call the recorder and checker only after the semantic result exists. They
validate objective schema, linkage, digests, repository snapshot, full-round,
and exit/consumer facts; they never decide scope, severity,
adequacy, Docs SSOT consistency, pass, or route. Return exactly one of
`passed`, `implementation_required`, `planning_stale`, or `blocked`. Fail
closed when evidence or the complete compatible Guru Team preset is missing.
Routine agent assignment, liveness, handoff, and recovery bookkeeping are not
entry evidence and are not written into `phase2-check.json`. Existing schema
2.0 artifacts remain read-only compatible; new records use schema 2.1.
This package is not self-contained or portable.
