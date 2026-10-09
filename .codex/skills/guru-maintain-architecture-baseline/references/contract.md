# Architecture Baseline Contract 2.0

## Authority model

The business repository Architecture Baseline is the only shared architecture
SSOT. It owns current/target state, decisions, GAPs, owners, compatibility
exits, ADRs, history, evidence, and the design constitution or its unique
locator. Guru Team owns the mandatory lifecycle and typed routes, not the
project's architecture answer.

The constitution projection contains one explicit `current` or
`pending_reviewed_promotion` authority status, one authority locator, one
version or content identity, and exactly these five stable identity/name pairs:

- `mature-practice-applicability` / `成熟实践与适用性`
- `concept-semantic-completeness` / `概念与语义完整性`
- `cohesion-change-isolation` / `职责内聚与变化隔离`
- `minimum-necessary-complexity` / `最小必要复杂度`
- `debt-one-way-convergence` / `技术债务单向收敛`

Principle prose, scores, per-principle verdicts, and mechanical checklists are
not public Skill data.

## Constitution applicability and existing revision owners

Read the project's unique current constitution authority and apply
`minimum-necessary-complexity` to the complete proposed change at Planning,
implementation discovery, Phase 2, and independently at Branch Review. Consume
its task-applicable conclusion and evidence for every added capability, including
public contracts and abstractions; do not limit the review to task-local
persistence. This package does not own or restate principle prose.

Distinguish a current requirement whose mechanism needs revision from a
requirement-authority conflict. For the former, the current stage's qualification
owner consumes `mechanism_revision_required` through its existing mechanism
router to remove/replace the mechanism while preserving accepted scope.
For the latter, select `architecture_conflict` with the concrete authority
conflict; `guru-architecture-baseline-planning-router` returns to the current
Planning owner and, when source scope must change, existing requirements
clarification. Review again against the revised current authority. Missing
applicable necessity evidence uses `contract_incomplete` and the same Planning
router; a real intent choice or unresolved dependency uses existing
clarification or blocked handling. An approved requirement alone cannot replace
this judgment, and this owner never silently deletes accepted scope.

Use existing impact, evidence, finding and route fields only for applicable
conclusions. Do not introduce per-capability records, scores, keyword
classifiers, public fields, or a second constitution checklist.

## Public and owner boundary

The 2.0 public input is a caller-owned route and authority DTO. Every profile
identifies the profile, stage, task, current baseline, constitution, project
change contract, requirement/behavior authority, and freshness. Branch Review
task impact and promotion also carry the exact structured committed range.
Public input never carries an impact decision, change path, contribution
decision, project-check descriptor or result, review conclusion, semantic pass,
or typed route.

After rereading those live locators, the AI-owned semantic result records the
reviewed impact kind and reason. Architecture-impact results additionally bind
exactly one change path, the task-owned contribution, the current descriptors
reread from project authority, exactly one result for every descriptor
identity, and the stage-specific review state. The semantic result records the
current owner review; it never becomes a second project descriptor authority.
The deterministic runtime only validates this separation, identity/freshness
and committed-range binding, and route consistency.
A no-impact `baseline_current` projection includes its concise reviewed reason
so the direct stage consumer can audit the lightweight result without creating
a contribution or ADR. Every current projection also carries the producing
profile and `constitution_status=current`; the current authority locator must
resolve component-by-component to an existing regular repository file without
a symlink-backed component.

The Architecture Skill owns the reviewer method; the contract-selected AI
executor performs its semantic judgment. The caller owns delivery coordination,
not the review conclusion. Baseline maintenance and promotion retain their
existing owner. A wrapper's refusal to generate judgment is not a missing
external approval and does not authorize caller self-assessment.

The owner execution sequence is public input validation, the profile-specific
read order below, applicable project-check execution/evidence review,
semantic Architecture or current eligibility judgment, result authoring against
`schemas/semantic-result.schema.json`, one `scripts/invoke.sh --invocation -`
call, and consumption of its single typed exit. Routine confirmation is not an
authoring prerequisite and no confirmation wording or state belongs in the
result.

## Independent assessment entry

New `task_impact_sync` conclusions at `planning`, applicable
`implementation_discovery`, `phase2`, and `branch_review` are executed by a
fresh independent subagent, including a proposed no-impact change. The reviewer
has not authored or implemented the current candidate and has not read its PRD,
acceptance criteria, implementation summary, completion claims, prior pass, or
scope defense. Use empty task history, not a full-history fork of the caller.
Necessary AGENTS, engineering specs, this Skill, Architecture authorities and
operating instructions may load; they must not embed a task pass narrative.

The caller supplies exact repository/task locators, stage, current candidate
design locator or full-diff base/head, necessary long-term authority locators
and real constraint sources. These locate the object; they do not preselect
impact, change path, finding, pass or exit. Do not leak task narratives through
a dispatch summary. Planning reviews actual design facts and affected existing
implementation; `design.md` is a design object, not compliance authority. A
call-local design candidate is also valid. No real candidate means no candidate
pass; reading baseline authority alone is not design assessment.

Use the platform's supported fresh Task/Agent/subagent facility and inspect its
actual prelude. For Codex, use a fresh generic worker rather than an official
`trellis-check`, `trellis-implement` or `trellis-research` role whose task
context injection would preload narratives. A changed role name or different
worker id alone does not prove isolation. Do not patch upstream hooks or agent
definitions. If compliant dispatch is unavailable, the worker did not execute
or finish, or its result is missing/mismatched, stop through the existing
blocked/re-entry route; never degrade to the caller authoring the assessment.
Do not add a reviewer ledger, public reviewer fields or another state machine.

The reviewer reads and judges in this order:

1. current project constitution, Architecture Baseline and change contract;
2. actual Planning design facts, or the complete implementation candidate:
   Phase 2 includes tracked and untracked work; Branch Review binds the exact
   committed base/head/full diff;
3. changed decisions, defaults, state, rejection conditions, dependencies and
   responsibilities;
4. actual affected consumers, including unchanged callers, state reads/writes
   and runtime assembly;
5. comparable capabilities and their real constraints;
6. form an independent Architecture judgment, then inspect necessary design
   explanations/contribution for accurate attribution and responsibility.

Prefer durable requirement/design/operations authority for business constraints.
When a necessary new constraint exists only in the task, obtain only that fact
and its source; do not import the whole task narrative. Missing constraints or
evidence remain conditional or use the existing incomplete/blocked route.

The reviewer personally executes applicable project checks, authors the
semantic result and invokes the formal wrapper. It returns the actual declared
exit/output and current identity to the caller. Structure/schema/green commands,
prefilled owner results, worker labels, and caller self-filled Architecture
results are not evidence of this execution. Normal caller self-authoring can
pass objective validation while failing this Markdown method; re-enter with a
compliant fresh reviewer, not a new authenticity mechanism or hostile fixture.

A compliant fresh worker may finish Architecture first, then read task
narratives and execute Check or Branch Review. Each Skill still performs its
own complete review and produces its own actual result and freshness. A worker
already exposed to narratives or implementation cannot retroactively supply
the independent first round. Committed Branch Review always reassesses its
candidate independently; Phase 2 pass cannot substitute. New facts that change
Architecture judgment return to the corresponding fresh assessment stage.
Review and validation commands are read-only evidence collection; they do not
authorize product fixes, scope changes or promotion.

## Responsibility and change causality

Determine actual responsibility from the changed decisions, consumer graph,
state ownership, assembly and dependency direction. Check whether a generic
capability interprets business semantics or treats protocol/model/endpoint/
default configuration as business authority. Compare similar capabilities with
their real constraints; existing implementation is evidence, not an approved
precedent. Evaluate a more direct alternative that preserves every affected
current contract. Technical keywords and utility paths are not classifiers;
do not audit unrelated exported symbols or invent future consumers. A controlled
extension example may exercise an existing extension point.

Design/code/tests/contribution consistency, green acceptance, declared owner
agreement, approved plans or user continuation do not establish architectural
correctness. An evidenced current responsibility violation is itself a defect
without first requiring a functional failure. Distinguish an inherited error
from its new expansion or solidification with concrete before/after causality.
New/worsened deviations and necessary local boundary convergence belong to the
current change. Unrelated historical debt may be reported truthfully but does
not automatically become a current P0-P3 finding, release gate, required
follow-up or Issue. Insufficient evidence stays uncertain.

For an evidenced responsibility deviation, use the existing gate evidence to
state the concrete before/after causal delta and a more direct alternative.
Identify the actual owning boundary, necessary affected-caller adaptations and
obsolete-path exit, or explain from the current graph why any of these is not
needed. Preserve supported behavior and legal configuration, and stop at
causally unrelated debt. A generic "revise the mechanism" conclusion alone does
not explain the necessary local convergence. This is a causal correction
explanation for the delivery owner, not severity, a repair authorization, or a
new acceptance contract; no additional result fields or artifact are required.

The reviewer reports Architecture facts and causal effects; delivery owners
separately determine current work and qualification before edits/tests/severity.
Neither scope defense nor discovery alone settles that responsibility or
authorizes changes. If a necessary correction changes product goals or
Architecture authority, stop the affected work through the existing owner route.

## Downstream eligibility entry

`publication` and `acceptance_finish` retain fresh matching-stage invocations
by the Architecture owner. Consume the still-applicable independent conclusion,
reviewed contribution and live authority, candidate, committed-review and
promotion facts; judge this stage's eligibility and personally invoke the same
2.0 wrapper. A caller change alone does not repeat the same assessment or create
another reviewer. Do not relabel a Branch Review DTO as a downstream result,
use Phase 2 in place of committed review, or transfer promotion ownership.
Missing committed review or promotion follows its existing route. Changed
candidate or applicable Architecture facts needing a new conclusion return to
the corresponding fresh assessment stage; a shared authority update first uses
the existing owner's applicability judgment. Bootstrap, repair and promotion
are not automatically extra independent assessments; new assessment conclusions
still obey the entry above. No new Skill, profile, exit or private state is added.

## Task-local change contract

Every standard task binds the Guru public contract identity and the project's
baseline/change-contract identities. `no_architecture_impact` is a lightweight
reviewed result and creates neither contribution nor ADR. Its owner result uses
`promotion_state=no_change` and omits `change_path`, contribution fields,
`project_check_descriptors`, `project_checks`, and `review`; those optional
schema properties belong only to the architecture-impact branches that require
them. An architecture impact selects exactly one path: `target_native`,
`legacy_boundary_convergence`, or `dedicated_refactor_slice`.

The project task-local contract owns requirement/behavior authority, boundary,
decision and GAP refs, required concerns with explicit applicability, current
and target owners, one writer, compatibility exit, allowed/forbidden parallel
scope, deviation lifecycle, deletion conditions, design responsibilities,
before/after state, project checks, evidence, contribution, ADR, review,
promotion, and expected current identity.

An ADR candidate is necessary only when the task changes an architecture
decision, principle tradeoff/exception, GAP lifecycle, owner/single-writer, or
compatibility exit. Current-conforming work does not create an ADR.
`adr.required=true` therefore carries a non-empty locator, while `false` carries
an empty locator. `reviewed_promoted` carries a non-empty promoted identity and
is valid only after the contribution has an independent reviewed state.

## Stage lifecycle

Planning creates the current impact result. Implementation discovery re-enters
when a material boundary expands. Phase 2 performs applicable project checks
and a first before/after semantic judgment. Branch Review independently
recomputes the same concerns from the committed full diff. Publication rejects
missing, stale, conflicting, incomplete, regressing, or unpromoted state.
Acceptance/Finish accepts only fresh no-change or reviewed+promoted state.

Promotion is serialized by the Architecture owner and binds the expected live
current identity. If live current advanced, `sync_required` returns to the same
owner without overwriting. The promotion diff must receive a fresh Phase 2 and
independent Branch Review. The resulting current identity is the only identity
the next task may consume.

Only a `baseline_current` produced by `task_impact_sync` may resume the exact
matching stage. A current result from bootstrap or repair reruns the affected
`task_impact_sync` stage; it does not resume that stage directly. A current
promotion result always re-enters fresh Phase 2, Task Commit, and independent
committed full-diff Branch Review before any downstream reuse.

Bootstrap activates only a successor with the same baseline locator,
`status=active`, and an identity distinct from the missing, draft, or
superseded predecessor. Repair accepts only an already active baseline; it
cannot relabel a draft or superseded baseline as current.

## Project architecture checks

### Archived Read-Only Sources

The existing `task_impact_sync` input binds three additional closed
source/stage pairs: `review_refresh_required/branch_review`,
`archived_review_passed/publication`, and `archived_ready/acceptance_finish`.
Each is a fresh matching-stage semantic invocation. Downstream eligibility may
consume a still-applicable independent conclusion as defined above; an earlier
stage DTO never replaces this stage's actual output.
The caller supplies the exact current range or A/B identity for that stage.

For these sources the AI reviews only the existing current project authority
and evidence. It selects `baseline_current` only with `no_change` or
`reviewed_promoted` state. If a prerequisite is missing/stale or satisfying it
needs a contribution, promotion, repair, implementation or other write, the
AI selects the existing `blocked` exit and explains the actual limitation.
It does not relabel that need as fulfilled. No writing recovery is executed
inside this invocation. The validator checks source/stage and exit/state
compatibility without choosing, converting or repairing an owner result.
An invalid writable result fails before projection. Other source exits and
profiles retain their current behavior and consumers.

Projects declare their own check descriptor, command, and semantics. The AI
owner rereads current descriptor authority and records one `descriptor_identity`, check
identity/version, entrypoint, applicable scope,
rule/decision/GAP refs, result-contract identity, and freshness source. The generic result
contains the same descriptor identity and check identity/version,
applicability, rule/decision/GAP refs,
before/after state, `pass|fail|unverified`, evidence or an unavailable reason,
freshness, and the AI-reviewed `blocking` result derived from applicability and
the task's real dependency. The owner result carries the descriptors and
results. Runtime maps each result to the owner-reread descriptor set by
`descriptor_identity`, requires exact
check id/version and a one-to-one match,
rejects missing, duplicate, unregistered, or extra descriptors/results, binds
applicable scope plus rule/decision/GAP refs exactly, validates the descriptor
entrypoint locator and result-contract identity, and binds every result
freshness to the current invocation. It does not execute the project command
or interpret its semantics. Every descriptor/result binds at least one current rule,
decision, or GAP identity. A blocking failed or unverified check cannot support
`baseline_current`. `not_applicable` requires non-blocking passed evidence that
proves the current applicability decision; fail or unverified cannot use that
label to bypass an applicable concern. A non-blocking evidence gap remains
explicit and cannot be used to close a GAP, approve an exception, or claim
architecture completion.

## Stable routes

- `contract_incomplete`: return to Planning or repair for missing applicable
  contract, authority, decision, constitution, or check facts.
- `architecture_conflict`: return to Planning for an authority conflict.
- `fitness_regression`: return to implementation/check for a new or worsened
  deviation, owner expansion, dual writer, or closed-GAP recurrence.
- `sync_required`: return to promotion/repair for stale baseline,
  constitution, contribution, or expected-current identity.

The deterministic invocation records no authorization and makes no semantic
decision. It validates the AI-authored result and serializes exactly one closed
typed output.

`owner_not_yet_executed` is only an internal execution state: the current AI
owner continues the sequence above. Missing authority, constitution, project
contract, descriptor, or required check evidence uses the existing
`contract_incomplete`, `baseline_incomplete`, or `blocked` route as applicable.
A deterministic validation error is repaired by correcting the authored result
or freshly rereading stale identity/freshness facts only after the current
invocation reports the exact error and stops. That correction starts a new
semantic owner round with a newly authored envelope; it is not a retry within
the prior round and the failed invocation is never converted into an
Architecture judgment. Only a platform that cannot perform the required AI
review, public/live reads, result authoring, or formal invocation may report a
true execution-capability gap.
