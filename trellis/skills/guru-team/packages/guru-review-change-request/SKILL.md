---
name: guru-review-change-request
description: Review whether a current change request is one independently deliverable unit through linked prerequisite evidence, an AI readiness gate, and five typed exits.
---

# Guru Review Change Request

Use this Skill after `guru-review-contract-wording:change_request:pass` and
before task workspace creation. Load
[references/contract.md](references/contract.md) before acting.

Reread the current target authority, then validate clarity and wording evidence. Review all
ten readiness dimensions, record findings and one scope conclusion, complete
the AI Review Gate, and call the recorder and checker only after the semantic
judgment exists. Return exactly one declared typed exit.

The recorder and checker validate only closed JSON shape, hashes, linkage,
freshness, fixed consumers, and objective exit invariants. They never generate
findings, select a delivery unit, decide readiness, or choose a route. Pre-task
and standalone execution is stdout-only. `ready` declares
`guru-create-task-workspace` as its consumer but does not create or persist a
task workspace. Fail closed when evidence is missing, stale, mismatched, or the
compatible Guru Team preset runtime is unavailable. This package is not
self-contained or portable.

After the semantic gate and owner recorder/checker complete, invoke
`scripts/invoke.sh --invocation -` with the closed call-local public input,
`wording_current` transition, and checked owner result on stdin to serialize the
readiness handoff. The transition carries the checker-bound clarity, wording,
and target projections; the runtime reruns the existing readiness checker and
derives the Agent-owned route from its checked result. It does not decide
readiness or expose the private review artifact.
