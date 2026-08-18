---
name: guru-maintain-architecture-baseline
description: Maintain a repository Architecture Baseline through semantic bootstrap, task impact synchronization, promotion, and repair profiles.
---

# Guru Maintain Architecture Baseline

`judgment_mode=semantic`. This Skill owns the architecture authority decision:
whether a baseline is current, incomplete, stale, conflicting, accepted, or
ready for promotion. It supports exactly four profiles: `bootstrap_foundation`,
`task_impact_sync`, `promotion`, and `repair`.

The project authority lives in `docs/architecture/`; this package supplies the
reusable contract and does not copy business architecture content. FOUNDATION
selects a versioned horizontal stack baseline. CURRENT is evidence-proven
implementation, TARGET is accepted future state, GAP is an explicit delta,
PLAN is an approved plan, ADR is history, and EVIDENCE supports judgment.

The AI performs authority, conflict, status, finding, revision and route
judgment. The deterministic runtime validates the closed profile input, owner
result identity, baseline locator/version/status/scope, contribution partition,
freshness and the minimal typed projection. It never decides sufficiency.

Public exits are `baseline_current`, `sync_required`, `baseline_incomplete`,
`architecture_conflict`, `contract_incomplete`, `fitness_regression`, and
`blocked`. Each exit has one consumer and a profile-specific output schema.

Run this Skill for every file-changing request that has not already entered an
active-task route. Issue presence, current branch, and task-free wording do not
control entry. The AI owns the semantic decision; scripts only validate a
completed selection and serialize the one typed exit.

Use `task_free` immediately when the user explicitly requests that semantic;
the shortest public expression is `这次走 task-free`. Recognize equivalent
multilingual wording semantically rather than through a keyword table. Neither
`帮我改一下` nor `不要开 Issue` is explicit task-free intent.

Without explicit intent, read only the limited live repository and Issue facts
needed for the decision:

- automatically select `task_free` when the boundary is clear, local,
  reversible, and confidently has no obvious high-risk effect;
- ask one concise mode question when task-free is likely but scope or risk
  evidence is insufficient; an affirmative answer selects `task_free` and a
  refusal selects `standard_intake`, with no repeated question for the same
  scope;
- automatically select `standard_intake` when isolation, planning, complete
  review, or high-risk validation is clearly needed, including material runtime,
  cross-layer contract, public API, schema, CI, install/update, deploy,
  permission, security, or data impact.

An Issue supplies evidence but never decides the mode. File count, paths, and
keywords are weak evidence only and never independent classifiers. Once
selected, mapped exits, ordinary recovery, and same-scope retries reuse the
selection. Material scope, authority, or risk changes require a fresh semantic
decision.

`task_free` is limited to the current checkout and the explicitly bounded
files for this turn. It never authorizes task/worktree/branch creation,
commit, push, PR, merge, tag, release, installation, or cleanup. Preserve all
unrelated dirty and untracked files. `guru-execute-task-free-change` separately
owns checkout suitability, bounded editing, targeted checks, and post-write
risk evolution. It never reads remote branch protection and does not add fields
to this Skill's public DTO.

The execution Skill re-enters this selector only for automatic scope/risk
expansion. Explicit expansion stays in that Skill's interaction re-entry.
Commit, push, PR, merge, release, installation, cleanup, and Issue closure
remain independent later authorizations.

Return exactly one of `standard_intake`, `task_free`, or `blocked`.
