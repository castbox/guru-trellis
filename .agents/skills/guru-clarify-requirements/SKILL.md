---
name: guru-clarify-requirements
description: Clarify initial requirements, active-task scope changes, or explicit review requests through an evidence-first semantic loop with exact confirmation and typed exits.
---

# Guru Clarify Requirements

Use this Skill after `guru-discover-change-context:context_ready`, when an
active task receives scope-changing input, or for an explicit standalone
requirements review.

Load [references/contract.md](references/contract.md) and
`trellis-brainstorm`. Execute the semantic closed loop in its declared order,
ask at most one highest-value question per round, complete the AI Review Gate
and any exact action/proposal confirmation before calling recorder/checker,
then return exactly one declared typed exit.

Use only the dispatcher wrappers for deterministic recording and checking.
Pre-task and standalone results are stdout-only. This Skill has no mutation
executor and no dedicated tracked clarification artifact. GitHub writes remain
AI-owned and require exact confirmed payloads plus a live reread.

Fail closed on missing/current-context drift, open load-bearing questions,
confirmation or digest mismatch, stale active-task evidence, unknown exits, or
missing compatible runtime. This package is not self-contained or portable.
