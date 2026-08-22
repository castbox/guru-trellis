# #295 Architecture contribution

## Candidate identity and authority boundary

- candidate identity: `architecture-contribution-295-sync-discovery-public-handoff-v1`.
- requirement authority: GitHub Issue #295 and task `prd.md`.
- behavior authority: task `design.md` and `implement.md`.
- current baseline: `docs/architecture/README.md` /
  `current-main-0.6.5-guru.39` / `active`.
- design constitution: `docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` /
  `guru-trellis-architecture-change-concerns-v1`.
- change path: `target_native`; promotion state: `reviewed_candidate`.
- expected current identity: `current-main-0.6.5-guru.39`. Shared current remains
  owned by the serialized Architecture promotion step after independent full-diff
  review.

## Boundary and decision

Current Sync correctly owns its private `guru-base-sync-result-1.0` and exports
only `base_current`, but mandatory Discovery still requires that private result
and its digests. The installed Phase 0 transcript compensates by reconstructing
producer-private state, so the declared public workflow graph is not executable
by an honest caller.

The target boundary preserves Sync's current public shape and makes Discovery
consume only its independent public input plus `base_current`. Discovery owns a
fresh live `base_observation` and its semantic result. The deterministic runtime
checks Git identity, freshness, schema closure, and typed routes without taking
over semantic context review. No compatibility layer, second authority, private
result projection, or dual-read is retained.

This is current-conforming work under `ARCH-DOM-001`, `ARCH-DOM-004`, and
`ARCH-INT-001`; it does not change an architecture decision, owner topology,
single-writer rule, GAP lifecycle, or compatibility exit. No new ADR is required.

## Required concern review

| Concern | Applicability | #295 contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | Bind the Guru 2.0 contract, active `.39` baseline, and project change contract v1. |
| `constitution-binding` | `applicable` | Apply concept completeness, cohesion/change isolation, minimum complexity, and one-way convergence without copying principle prose into public DTOs. |
| `boundary-and-decision` | `applicable` | `target_native` preserves `base_current` as the only Sync transition and moves live observation to Discovery ownership. |
| `owner-and-single-writer` | `applicable` | Sync owns private sync state; Discovery owns context semantics and live observation; the #295 task is the candidate writer; promotion remains the only shared-current writer. |
| `compatibility-and-exit` | `applicable` | Stable Skill ids, Sync output 2.0, base-current 1.0, typed exits, and Clarify consumer remain; old Discovery schemas remain immutable legacy assets but are not dual-read by the active graph. |
| `gap-and-deviation` | `applicable` | Close only Issue #295's public handoff gap; retain current Architecture GAP state and introduce no new deviation. |
| `parallel-scope` | `applicable` | Allow the #295 task, canonical package, generated projections, and task-owned contributions; forbid direct shared-current edits and the excluded downstream Issues. |
| `evidence-and-freshness` | `applicable` | Bind Planning to the current task content; later stages use targeted package/runtime, public transcript, managed Python, projection/drift, and one clean throwaway evidence. |
| `review-and-promotion` | `applicable` | Keep this contribution candidate until independent committed full-diff review, then promote only against expected `.39` and rerun post-promotion gates. |

## Before and after

- before: Discovery cannot consume Sync's public `synced` output without a caller
  reconstructing Sync-private result and digest fields.
- after: the actual Sync wrapper output projects `base_current` into Discovery;
  Discovery live-reads its authority checkout, records only Discovery-owned
  observation, and projects `context_ready` to Clarify.
- preserved: Sync public output and transition shapes, AI semantic ownership,
  stable typed exits, zero pre-task repository mutation, installer protection,
  and managed package runtime.

## Project check

- descriptor: `guru-trellis-architecture-convergence:repository:1` /
  `guru-trellis-architecture-convergence@1`.
- refs: `ARCH-GOV-006..008`, `ADR-005`, and `ARCH-GAP-006`.
- Planning evidence: live Issue #295; current task `prd.md`, `design.md`, and
  `implement.md`; current Architecture baseline, constitution, and change contract;
  this contribution.
- Planning result: `pass`. The plan selects one path, preserves one semantic owner
  per private state, keeps one task writer and one promotion writer, and introduces
  no compatibility authority or worsened deviation.
- Phase 2, Branch Review, Publication, and Acceptance/Finish must rerun from their
  own fresh candidate or committed-range evidence.

## Promotion contract

Promotion is required only after the complete #295 committed diff has passed
independent Branch Review. It must bind expected current identity
`current-main-0.6.5-guru.39`; a live-current advance returns `sync_required`.
Promotion does not authorize a tag, Release, or any excluded downstream Issue.
