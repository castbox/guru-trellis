---
name: guru-clarify-requirements
description: Clarify initial requirements, active-task scope changes, or explicit review requests through an evidence-first semantic loop with dialogue-local choices and typed exits.
---

# Guru Clarify Requirements

Use this Skill after `guru-discover-change-context:context_ready`, when an
active task receives scope-changing input, or for an explicit standalone
requirements review.

For active-task scope change, the canonical workflow mandatory invokes this
same Skill with an exact caller-aware `resume_target`; no caller may duplicate
classification, ledger, or planning-update semantics.

Load [references/contract.md](references/contract.md) and
`trellis-brainstorm`. Execute the semantic closed loop in its declared order,
ask at most one highest-value question per round, complete the AI Review Gate
and any real action/proposal choice before calling recorder/checker,
keep that authorization in the current dialogue, then return exactly one
declared typed exit.

Use only the dispatcher wrappers for deterministic recording and checking.
Pre-task and standalone results are stdout-only. This Skill has no mutation
executor and no dedicated tracked clarification artifact. GitHub writes remain
AI-owned and require an exact current payload plus a live reread; the result
records only objective action and mutation facts.

Fail closed on missing/current-context drift, repository `answered` without
checked evidence, invalid question
lifecycle, open load-bearing questions, payload/live mutation or
digest mismatch, missing/stale/multiple target disposition, unresolved or
stale duplicate-candidate decisions, closed targets without an explicit legal
disposition, empty/non-final active-task proposal sets on `clear`/`new_task`,
any unresolved scope classification, any classification task update not bound
to the same current proposal set,
mechanism disposition with a classification trail or mutation, incomplete or
stale planning content, missing compact `decision_trail` ledger authority or live
GitHub-visible scope authority,
load-bearing clarification without a current issue/draft
authority action, authority/context/task-update order mismatch, invalid caller
resume, stale active-task evidence, legacy 1.0 artifact input, unknown exits,
or missing compatible runtime. This package is not self-contained or portable.

After the semantic gate and owner recorder/checker complete, invoke
`scripts/invoke.sh --input <declared-profile.json> --owner-result <repo-relative-clarification-result>`
to serialize the minimal handoff. The runtime reruns the existing checker and
derives the route from its checked `typed_exit`; callers cannot select the
route. Private clarification evidence is not a public input or output template.
