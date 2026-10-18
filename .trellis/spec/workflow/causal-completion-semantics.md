# Causal Completion Semantics

Semantic identity: `guru-causal-completion-semantics`.
`causal_semantics_version=1`.
Canonical locator: `trellis/presets/guru-team/spec/workflow/causal-completion-semantics.md`.
Installed locator: `.trellis/spec/workflow/causal-completion-semantics.md`.
Content identity is the canonical locator, declared version and exact current
UTF-8 bytes. A reader may calculate SHA-256 for its local consistency consumer;
the document contains no self-referential digest. Identity is neither approval
nor a new cross-stage freshness protocol.

## Ownership and applicability

This is the sole common authority for causal evidence dimensions and semantic
dispositions. It owns no stage route, Skill invocation, public DTO, recorder,
or Completion decision. Qualification owns candidate admission; each existing
stage owner reads this authority and judges its current work and evidence;
Task Completion alone judges the whole accepted completion definition.
Publish executes Delivery Review's reviewed payload. Closure owns source Issue
actions, and Finish owns bookkeeping after Closure.

Determine goals from current accepted scope and actual behavior: ordinary
feature, diagnosis, mitigation, root-cause repair, or a combination. Apply
repair proof only to the goals or claims that require it. For mixed work, judge
each goal and slice, then judge the entire task against all accepted scope.
An unknown cause alone does not invalidate a satisfied diagnosis or mitigation.
It does not excuse work whose accepted goal requires finding or repairing it.

Consume still-applicable qualification for an unchanged mechanism. A stage
change alone is no reason to repeat it; current stage review remains necessary.
Changed mechanism, authority, conditions or causal evidence goes back to the
existing qualification owner. Lost conclusions must be obtained from live
sources, never reconstructed from green tests or a persisted causal ledger.

## Evidence dimensions

Keep the following observations distinct in review and public claims. Their
presence is not a checklist-based proof, and they are not new schema fields.

| Dimension | What the evidence can establish |
| --- | --- |
| diagnosis | Bounded investigation, observations, hypotheses, known first failure, causal gaps and competing explanations. |
| implementation | The actual change to state, data, algorithm, resource behavior or external interaction and its real consumers. |
| static evidence | What inspection, type/schema checks and other static validation establish about the inspected candidate. |
| integration evidence | What the exercised component interactions establish, at the actual test layer. |
| external evidence | Observed effects at an external dependency, with current source and applicability. |
| production effect | Observations under the accepted production conditions, including original failure conditions and final business outcome. |
| root-cause resolution | Applicable first-failure, causal-chain and counterfactual evidence connects the changed cause to the resolved original failure. |
| mitigation | Its observed effect, legitimate-input and consumer impact, risks, applicability, direct owner, expiry and exit conditions, and remaining known or unknown cause. |
| remaining risk | Unfinished work, evidence gaps, residual failures and uncertainty that the accepted scope still leaves. |

For the applicable goal, separately inspect admission, failure stage,
classification, business outcome, owner, time window and completeness.
Compare the original object and path with the current observation. Improvement
in one dimension does not prove the others: renamed errors, deferred failure,
owner transfer, an excluded legitimate input, incomplete fallback output or a
lower failure count cannot alone prove cause removal. Inspect redistribution
across stage, component, operation, time window and classification; preserve
known first failure and failed samples instead of observing only the last retry.

Admission/config/limit/retry/fallback/normalization/error mapping is judged by
actual behavior and authority. A supported mitigation stays a mitigation.
A mechanism that merely hides or transfers failure without the required
repair, mitigation or protection basis is symptom suppression. Test fixtures,
filters, defaults and assertions must expose the required behavior rather than
manufacture success by excluding it.

Keep legitimate protection with current RDT/Architecture authority, protected
object, real harm without blocking, direct owner and current-layer necessity.
Credential, permission, tenant isolation, identity/integrity, idempotency,
ownership/lease/fence, transaction/error-fact blocking and stable terminal
errors are not removed merely because they block. This retains existing normal
correctness boundaries; it adds no attack model or concurrency/crash hardening.

## Semantic dispositions

These describe evidence and claims; they are not cross-owner success exits.
A stage's existing pass/ready/approved additionally requires every applicable
condition of that stage. Several dispositions may truthfully coexist.

| Disposition | Applicable meaning |
| --- | --- |
| `diagnosis_incomplete` | Some causal facts remain unknown. Bounded diagnosis may still meet its own scope; a goal that requires locating the cause remains unfinished. |
| `root_cause_identified` | Applicable first-failure and causal evidence supports the cause and addresses competing explanations; identification alone does not establish repair. |
| `mitigation_applied` | The bounded mechanism and its scope-required effect/risk evidence are established, with owner, expiry/exit and residual cause/gaps retained; it does not assert root-cause repair. |
| `implementation_validated` | Implementation meets its accepted code/test requirements at the stated validation layer; it does not establish production effect. |
| `external_effect_unverified` | The required external effect has not been established; report the concrete gap. Use `production_effect_unverified` when the unverified claim specifically concerns production. |
| `production_effect_verified` | Applicable production observations establish the stated effect; cause resolution still requires its own causal basis. |
| `root_cause_fixed` | The applicable qualified repair, implementation and scope-required causal/production evidence support removal of the original cause and failure, without mere suppression or redistribution. |

Green tests, complete diffs, recorder/checker success, PR publication, merge,
deploy, smoke, fallback output and lower failure rates establish only their
actual observation layer. None alone establishes `root_cause_fixed`.

## Completion evidence and equivalence

Ordinary features meet their accepted RDT scope without an incident questionnaire
or mandatory production proof. Diagnosis-only and mitigation-only work can
finish when their own accepted work and evidence are complete, including honest
unknowns; they cannot close a source/parent still requiring root-cause repair.
An implementation-only repair can finish its code/test scope while explicitly
reporting `production_effect_unverified`; it cannot close a parent still
requiring production causal closure. If diagnosis itself must locate the cause,
an unknown cause means that accepted work remains incomplete.

When the accepted whole task requires production root-cause repair, use the
same input or justified strictly equivalent production evidence. Completion
judges equivalence against the original failure's critical input conditions,
state, processing path, operating conditions and observed outcome. Equal sample
counts, green tests and lower failure rates alone are not equivalence. Do not
add a universal threshold, equivalence field table or evidence ledger.
Fixtures/mocks can test workflow judgment but cannot prove business production
effects.

One-time or unsafe-to-replay inputs do not require dangerous replay. Existing
observations or lawfully obtained equivalent evidence can suffice. If they do
not, retain the concrete missing evidence, its existing acquisition owner and
re-entry condition. Evidence acquisition obeys the business repository's
permissions and side-effect boundaries; this authority grants no production
access or write. Delivery requirements concern its independent slice; effects
obtainable only after merge/deploy remain whole-task Completion obligations,
so they do not create a circular delivery prerequisite.

## Semantic changes

Revise this same authority and affected behavior evals when common semantics
change. Each existing owner judges its actual dependency impact and re-enters
the earliest affected owner with fresh authority/evidence. Unrelated byte
changes do not automatically invalidate the whole chain. Do not auto-upgrade a
version, use a digest as approval, duplicate this prose in stage packages, or
create permanent incident state, review history or authorization artifacts.
