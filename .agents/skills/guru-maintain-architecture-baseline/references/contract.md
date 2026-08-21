# Architecture Baseline Contract 2.0

## Authority model

The business repository Architecture Baseline is the only shared architecture
SSOT. It owns current/target state, decisions, GAPs, owners, compatibility
exits, ADRs, history, evidence, and the design constitution or its unique
locator. Guru Team owns the mandatory lifecycle and typed routes, not the
project's architecture answer.

The constitution projection contains one authority locator, one version or
content identity, and exactly these five stable identity/name pairs:

- `mature-practice-applicability` / `成熟实践与适用性`
- `concept-semantic-completeness` / `概念与语义完整性`
- `cohesion-change-isolation` / `职责内聚与变化隔离`
- `minimum-necessary-complexity` / `最小必要复杂度`
- `debt-one-way-convergence` / `技术债务单向收敛`

Principle prose, scores, per-principle verdicts, and mechanical checklists are
not public Skill data.

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
a contribution or ADR.

## Task-local change contract

Every standard task binds the Guru public contract identity and the project's
baseline/change-contract identities. `no_architecture_impact` is a lightweight
reviewed result and creates neither contribution nor ADR. An architecture
impact selects exactly one path: `target_native`,
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

Bootstrap activates only a successor with the same baseline locator,
`status=active`, and an identity distinct from the missing, draft, or
superseded predecessor. Repair accepts only an already active baseline; it
cannot relabel a draft or superseded baseline as current.

## Project architecture checks

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
