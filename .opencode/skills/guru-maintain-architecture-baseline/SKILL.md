---
name: guru-maintain-architecture-baseline
description: Maintain a repository Architecture Baseline through semantic bootstrap, task impact synchronization, promotion, and repair profiles.
---

# Guru Maintain Architecture Baseline

`judgment_mode=semantic`. This Skill is the reusable Architecture Baseline
owner for exactly four profiles: `bootstrap_foundation`, `task_impact_sync`,
`promotion`, and `repair`.

Load [references/contract.md](references/contract.md) completely before acting.
The AI executing this Skill is the semantic owner selected by this contract; it
must not wait for or invent a second external Architecture owner merely because
the deterministic runtime cannot make semantic decisions.

Execute one profile in this order:

1. validate the caller/profile and read the exact public input;
2. reread the complete contract, live task and planning scope, Architecture
   Baseline, design constitution, project change contract, and current project-
   check descriptors and evidence;
3. run or inspect every applicable project check and judge its applicability,
   blocking effect, and before/after meaning;
4. make the Architecture impact, change-path, contribution/ADR, finding, and
   route judgments as the current AI owner;
5. author one complete result matching `schemas/semantic-result.schema.json`;
6. submit `public_input` plus that `owner_result` once through the formal
   `scripts/invoke.sh --invocation -` boundary; and
7. consume exactly one declared typed exit.

`owner_not_yet_executed` is an internal prompt to finish steps 2-6, not a typed
stop and not a reason to ask for routine confirmation. Map genuinely missing
authority or project-check facts to the existing incomplete or blocked routes.
On deterministic schema, identity, freshness, consumer, or route validation
failure, report the exact error and stop the current invocation. Any correction
requires fresh Skill re-entry with reread facts and a newly authored envelope;
it is not a retry within the same semantic round. Report execution capability
as missing only when the platform truly cannot provide the contract-required
AI review, reads, result authoring, or formal invocation. User confirmation is
required only for a real choice or side effect; it never supplies the semantic
result and is never recorded in the owner result or another authorization
artifact.

Every standard task enters `task_impact_sync` at Planning. The AI rereads the
project Architecture Baseline, design-constitution authority, project
change-contract identity, task scope, and applicable project-check protocol.
It returns either a reviewed `no_architecture_impact` result or exactly one of
`target_native`, `legacy_boundary_convergence`, and
`dedicated_refactor_slice`.

Implementation discovery invalidates the prior result when scope, risk,
authority, persistence, SDK, external, owner, or architecture boundaries
expand. Phase 2 and Branch Review are independent semantic judgments: Phase 2
reviews the candidate before/after state; Branch Review recomputes it from the
complete committed diff. Publication and Acceptance/Finish may consume only a
fresh no-change result or a reviewed and promoted contribution.

The project authority owns all architecture and constitution prose. This
package consumes only authority status, locators, verifiable identities, the
five stable principle identities/short names, and task-local change/evidence
contracts. It does not turn principles into a scorecard and does not encode
language, framework, or business-specific checks.

Only task-owned contributions may be written before independent Branch Review.
Shared current Architecture authority changes only through serialized
`promotion` bound to the expected current identity. A promotion diff re-enters
Phase 2 and committed full-diff Branch Review before Publication.

The AI owns applicability, sufficiency, conflict, regression, contribution,
ADR, promotion, and route judgment. The deterministic runtime validates only
the closed 2.0 input/result/output contracts, exact identity/freshness binding,
project-check shape, unique consumer, and minimal typed projection. Missing or
1.0 input is rejected; it is never upgraded or dual-read.

Author the smallest result valid for the selected branch. In particular, a
`no_architecture_impact` owner result uses `promotion_state=no_change` and omits
`change_path`, contribution fields, project-check descriptor/result fields,
and `review`; optional schema properties are not universally valid across
semantic branches.

The public input carries only caller route and live authority identities, plus
the exact committed range when the stage needs one. The AI rereads the project
Architecture change-contract authority and records its current project-check
descriptors together with descriptor-identity-bound results in the owner
result. A no-impact current output projects its concise reviewed reason but no
contribution, descriptor, check, or ADR fields.

Bootstrap may project `baseline_current` only from an active successor at the
same locator with a distinct identity. Repair always starts from an active
baseline. Branch Review and promotion bind their nested reviewed range exactly
to the caller-supplied structured committed range.

Every `baseline_current` requires `authority_status=current`, an existing
regular repository file at the constitution locator, and carries its exact
`source_profile`. Only `task_impact_sync` may resume its matching lifecycle
stage. Bootstrap and repair current results rerun that affected
`task_impact_sync` stage; promotion current results return through fresh Phase
2, Task Commit, and independent committed full-diff Branch Review.

Public exits are `baseline_current`, `sync_required`, `baseline_incomplete`,
`architecture_conflict`, `contract_incomplete`, `fitness_regression`, and
`blocked`. Unknown, multiple, stale, or unmapped exits fail closed.

Archived read-only callers still invoke this owner independently at each stage:
`review_refresh_required` selects `branch_review`, `archived_review_passed`
selects `publication`, and `archived_ready` selects `acceptance_finish` through
the existing `source_exit` input. For these exact sources, judge within the
read-only scope and return only `baseline_current` with current/no-change or
already-promoted authority, or `blocked` with the actual missing prerequisite.
Do not write a contribution, promote, repair, or start implementation to make
this invocation pass. Runtime rejects an incompatible stage or writing route;
it never changes an AI-selected route. Ordinary sources retain all seven exits.
