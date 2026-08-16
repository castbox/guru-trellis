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

Before this owner creates a scope proposal, asks a scope question, or assigns a
terminal scope disposition to a newly observed scenario, form only candidate
refs and live locators and invoke `guru-qualify-normal-scenario` with
`requirements_scope_set`. Rejected candidates are final for the current
invocation and must not become clarification questions. The
`normal_scenario_scope_confirmation` public profile instead consumes only the
qualifier's minimal `scope_confirmation_required` projection and asks the exact
authority choice before returning to the declared original owner. It does not
repeat or reinterpret qualification and accepts no decision, reason, severity,
authorization, result locator, or qualification artifact.

Before answering repository-searchable questions or evaluating duplicate and
prior-decision evidence, read `.trellis/spec/workflow/semantic-retrieval.md` and
apply it in this Skill's semantic gate. Do not infer absence from a
single-language zero result or expose the query process through the public DTO.

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
stale planning content, missing scope-only Ledger binding, missing compact
owner-result `decision_trail`, or missing live GitHub-visible scope authority,
load-bearing clarification without a current issue/draft
authority action, authority/context/task-update order mismatch, invalid caller
resume, stale active-task evidence, non-current artifact input, unknown exits,
or missing current runtime. This package is not self-contained or portable.

After the semantic gate and owner recorder/checker complete, invoke
`scripts/invoke.sh --invocation -` with the closed call-local public input,
`context_current` transition, and checked owner result on stdin to serialize
the minimal handoff. The runtime reruns the existing checker and
derives the route from its checked `typed_exit`; callers cannot select the
route. Private clarification evidence is not a public input or output template.
