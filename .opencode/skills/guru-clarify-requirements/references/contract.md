# `guru-clarify-requirements` Contract

All GitHub reads and confirmed writes use the shared authenticated, repo-bound
`gh` adapter in `.trellis/spec/workflow/workflow-contract.md`; there is no App,
MCP, connector, or browser fallback.

## Ownership And Modes

The global workflow owns mandatory invocation and unique exit consumers. This
package declares `judgment_mode=semantic` and owns:

```text
forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit
```

Workflow and standalone modes use identical preconditions and freshness.
Standalone removes only global routing; it does not remove the complete Guru
Team runtime or current-evidence requirement. Load `trellis-brainstorm` as the
questioning method, while this Skill retains every semantic decision.

Before a newly observed scenario can become a proposal, user question, scope
decision, task update, or new-task draft, this owner supplies only candidate
refs and live locators to
`guru-qualify-normal-scenario:requirements_scope_set`. `classified` returns to
this owner, `mechanism_revision_required` returns for remove/replace and fresh
qualification, `scope_confirmation_required` re-enters through the closed
`normal_scenario_scope_confirmation` profile, and `blocked` stops. Rejected
candidates cannot be escalated into dialogue or authority mutation.

`normal_scenario_scope_confirmation` is a target-owned consumer input, not a
second qualification route. It accepts exactly `profile`, `source_exit`,
`mode`, `target_locator`, `resume_target`, `continuation_id`, and a non-empty
unique `candidate_refs` set. It accepts no classification decisions, reasons,
severity, authorization, result/checkpoint locator, or worker report. The
qualifier output is projected directly into these fields. After the real scope
choice, this owner updates live authority through its existing rules and returns
to the exact closed `resume_target`; changed authority or candidates require the
original owner to run fresh qualification.

## Current Executing Owner

The current executing AI is this Skill's semantic owner in both workflow and
standalone modes. `owner_not_yet_executed` means continue the current review;
it is not a typed exit and does not require an external owner, agent ID,
subagent evidence, or pre-existing owner result. The restriction on runtime
semantic judgment does not restrict the current AI from authoring that judgment.

Read the complete contract, real Discovery public output, and current authority.
You resolve repository-answerable questions from evidence, review duplicate
disposition and scope, and ask only the real product choices required by this
contract. Author the current clarification result and Gate before running
record-requirements-clarification.sh, check-requirements-clarification.sh, and
invoke.sh with their declared inputs. Never invent an answer to an unresolved
load-bearing question merely to obtain clear.

Keep this owner's authoring and recorded result in call-local memory for its
own record/check/invoke sequence. Pass only actual public invoke stdout through
the declared thin projection to the next consumer; never read or reconstruct
producer-private results. This responsibility does not waive missing authority,
freshness, schema, prerequisite, or unresolved-choice checks: use the existing
declared blocker or re-entry route when a real gap remains. Do not bypass the
workspace gate or ask for a corrective Prompt merely because your review has
not run yet.

## Forward Behavior

For repository-answerable questions, duplicate evidence, and recalled
decisions, first read `.trellis/spec/workflow/semantic-retrieval.md`. The AI
constructs the minimal applicable concept family and assesses coverage inside
the existing clarification gate; the recorder and public outputs receive no
query transcript, keyword list, or search-process field. Negative conclusions
must meet the shared contract's multilingual, literal, and legacy-alias bar.

Execute in this order:

1. validate invocation, review target, current context and authority;
2. classify input into confirmed facts, repository-answerable questions,
   product-intent questions, scope-risk decisions and out-of-scope facts;
3. consume Discovery's checker-passed `duplicate_snapshot` on the current
   initial path and author one mutually exclusive
   target disposition, including a selected/rejected decision for every
   candidate;
4. inspect current Docs/code/tests/history/GitHub/Git evidence until every
   repository-answerable question is `answered` with checked evidence or
   `not_answerable` with checked evidence and a missing reason;
5. ask exactly one highest-value user question per round. Use one
   `atomic_group` only for an indivisible product choice and record why it
   cannot be split. A partial answer closes no question. Classify each answer
   as `load_bearing` or `non_load_bearing` and bind its authority actions;
6. propose exact scope decisions and source-of-truth actions;
7. execute the AI Review Gate;
8. when required, show the exact target, target disposition, payload, scope
   delta, affected contracts and executor action, then obtain dedicated human
   confirmation in the current dialogue;
9. after confirmation only, the AI may execute a GitHub write, reread live
   facts, and provide objective mutation evidence without serializing the
   authorization;
10. call recorder/checker and return one typed exit.

AI owns question selection, clarity, scope classification, action selection,
confirmation necessity, semantic pass/block and route intent. Scripts never
perform those judgments.

## Questions And Convergence

Record only clarification rounds and answers that actually occurred. Unknown,
unasked, or unanswered choices are not refused, deferred, or answered. In
particular, `answer_status=refused` requires an actual user refusal; absence of
a response is not that evidence. Never invent a question, reply, refusal, or
deferral to satisfy required schema fields, and never claim the user explicitly
declined a choice without that actual response.

When current authority contains an unresolved load-bearing conflict and no real
choice can be obtained, return the existing `blocked` exit with
`ai_review_gate.status=blocked`. Describe the conflicting requirements, missing
choice, and actual evidence in the Gate finding, summary, and result `reason`.
If no clarification round with an actual answer occurred, use
`clarification_rounds=[]`; do not synthesize a round to express the conflict.
Keep `open_questions` consistent with the recorded lifecycle (empty when there
are no recorded rounds), and do not treat that empty array as semantic clarity.
An asked but unanswered question can be described truthfully in the blocked
Gate without assigning it a fictional answer status. Preserve actual prior
rounds and partial answers when present; do not erase them to use the empty
shape. The existing blocker requires no new schema field or runtime judgment.

Every clarification round contains one `question_id` that must be opened in
that round or already belong to the current open set. The reducer enforces
`open_questions = opened - closed`, rejects close-before-open and
reopen-after-close, and does not allow an empty lifecycle to hide a partial
answer. `answer_status=partial` cannot close its own or another question. An
unresolved load-bearing decision can produce `blocked`; a rejected/deferred
expansion that leaves current confirmed
scope complete is classified as related, followup, new task or out-of-scope and
does not block that current scope. During an active task, an expansion cannot
receive any of those five scope classifications until the AI has completed the
required dialogue decision.

`clear` is valid only when `open_questions=[]`, the AI Review Gate passed,
source/context authority is current, all proposals have final decisions, and
no successful GitHub mutation remains unrefreshed.

## Target Disposition

Every initial issue/draft review records exactly one disposition:

- `keep_current_open_issue`: retain the current open issue;
- `keep_current_draft`: retain the side-effect-free proposed draft;
- `retarget_existing_issue`: select one different open duplicate candidate;

Initial-change-request input schema 2.0 replaces 1.0 in the current graph. Its
required snapshot is accepted only when target locator, authority body digest,
query, checked time, candidates and aggregate digest match the current context
transition and the owner disposition. Policy staleness, authority mutation,
retarget or explicit refresh invalidates the projection and routes through the
existing context refresh owner; Clarification never reads Discovery private
state and never performs the normal initial search again.
- `reopen_closed_issue`: retain and reopen the closed source issue;
- `create_followup_draft`: retain the closed issue only as related/reference
  and produce a new side-effect-free issue draft;
- `block_target_complete`: record evidence that the target is complete and no
  independently deliverable gap remains.

Scope/product conflict and target disposition are independent judgments. A
conflict does not make a known issue identity or Discovery duplicate facts
unknown. When current target facts suffice, complete the target disposition
even with a blocked semantic Gate: for example, retain the known open issue
when the reviewed duplicate evidence supports it, while recording the unresolved
product choice as the blocker. This is a fresh AI judgment, not a default keep
decision or a default pass. Preserve the actual Discovery `duplicate_snapshot`,
including its candidate facts and opaque tokens.

`target_disposition=null` is not a blocked shortcut. `needs_context` or a
blocked incomplete target decision may carry no disposition only when the target
decision itself is genuinely missing and the selected invocation permits it.
In particular, initial `source_exit=context_ready` still requires a disposition
matching its snapshot, including on blocked; null does not satisfy that public
invocation. Do not drop the snapshot, change the source exit, or invent a target
decision to bypass the binding. Handle genuine missing target evidence through
the existing context/error route. Every progressing `clear`,
`refresh_context`, `retarget_context`, or `new_task` result requires one current
disposition. In particular, an issue comment/body edit or proposed-draft update
cannot use `target_disposition=null` while returning `refresh_context`.

Duplicate search is mandatory even when its candidate set is empty. Every
candidate binds live repo/number/state/URL/updated-at facts and one `selected`
or `rejected` AI decision. Non-empty candidate sets require exact human
confirmation for both a keep decision and a selected replacement, but the
result stores only the final disposition and objective candidate facts.

`retarget_existing_issue` owns one validated `select_existing_issue` action
and returns `retarget_context`. Its unique
consumer is `guru-sync-base`; the complete sync, context discovery,
clarification, wording and change-request review chain reruns for the selected
issue. No target-specific evidence from the old target transfers.

`reopen_closed_issue` owns one completed `reopen_issue` GitHub
mutation and returns `refresh_context`. `create_followup_draft` owns a
`new_issue_draft`, returns `new_task`, and cannot place the original closed
issue in the future task's close set. `block_target_complete` requires a
blocked AI gate and returns `blocked`. Closed issues cannot reach `clear`.

## Scope Proposals

Every proposal binds exact scenario, trigger evidence, proposed contracts,
cost, alternatives, omission consequence, origin status, decision and one
derived digest used only by recorder/checker to validate those current bytes.
The digest is neither workflow authority nor authorization evidence.
`unconfirmed_expansion + accepted_current` requires one dedicated dialogue-local
choice before the decision is finalized. That choice is not copied into the
result or decision trail.

When `optional_mechanism_origin=true`, decision cannot be `accepted_current`.
Remove or replace that mechanism; if independent product value remains, form a
new proposal and decide it separately. Unrequested threat, attack, TOCTOU,
race, fault-injection or cross-OS hardening follows this same rule.

## Source Actions And Mutation Boundary

Actions are exactly `none`, `issue_comment`, `issue_body_edit`,
`proposed_draft_update`, `new_issue_draft`, `select_existing_issue`,
`reopen_issue`, and `active_task_scope_update`. There is no mutation executor
in this package.

For `issue_comment` or `issue_body_edit`, the AI must reread the live preimage,
match repo/issue/action/payload facts, execute the exact existing
shared repo-bound `gh` action, reread live facts, then pass only
normalized mutation facts to recorder/checker. Success returns
`refresh_context`, never `clear`. Checker requires exact equality among the
action payload body, canonical payload digest, mutation result
content digest, and reread live body/comment bytes. `new_issue_draft` performs no issue creation
and returns `new_task`; #112 owns the complete intake mutation route.

Every clarification round carries an AI-authored `authority_impact` and
`authority_action_ids`. `load_bearing` covers any answer that changes problem,
scope, acceptance, non-goals, issue disposition, risk/test boundary, or another
contract future implementation must consume. For an issue target it requires
a completed `issue_comment` or `issue_body_edit`, followed by live reread and
`refresh_context`; for a draft target it requires a validated
`proposed_draft_update` bound to current draft bytes. `none + clear` is invalid
for a load-bearing round. `non_load_bearing` does not require or permit an
authority action merely to satisfy the contract.

## Active-Task Scope Change

Pause implementation/check/commit/review progression. Classify new input as
current task scope, related, followup, new task or out-of-scope. Current
inclusion requires the same delivery unit, no material boundary/risk/test
expansion, complete updated planning and the required dialogue decision.

Active-task `clear` and `new_task` require a non-empty set containing only the
seven terminal decisions: the five scope classifications `accepted_current`,
`related`, `followup`, `new_task`, and `out_of_scope`, plus the mechanism
dispositions `mechanism_removed` and `mechanism_replaced`. `new_task` must
contain at least one `decision=new_task` classification. Every scope
classification is finalized only after the required dialogue decision and
binds one compact owner-result `decision_trail`. It is not a process trail: it
contains only the final proposal decisions plus the remote authority locator
and content checksum. It
contains no user identity, wording, timestamp, confirmation reference,
authorization digest, planning identity, review state, context snapshot,
resume target or re-entry routing. Mechanism
dispositions instead require `optional_mechanism_origin=true`; they never enter
the trail or trigger GitHub/task authority mutation. A mechanism-only payload
may return `clear`, and a mixed payload places only its five-classification
subset in the trail.
Mechanism-only still carries all three planning documents, re-entry owners,
and current context evidence in the owner-private
result; only `decision_trail` is null. Every
terminal active-task path receives the same live task/context freshness check.
The checker independently validates the owner-result trail against the current
proposal set and live GitHub authority. Current planning, context, task action
and re-entry facts are reread from their owning sources. Those rederivable
bindings and the trail stay in the transient owner result.

GitHub comment/body mutation returns `refresh_context` before any task-local
update. On re-entry, live authority kind/URL/content and update time are reread
directly. The task-update action preimage must equal the current transient
`context_evidence` digest. The AI then validates the current planning identities and
one `active_task_scope_update` action. After the dialogue decision, the
task-local write binds that action to the same five-class proposal set and the
current preimage. Recorder/checker retain only the objective action and result
facts; each component writes no authorization fields. A task-only update does not require a
second Discovery result or a changed digest before `clear` or active-task
`new_task` resumes the exact interrupted progression. `new_task` then carries only a reviewed
side-effect-free draft; #112 still owns issue/task creation. This Skill records
no dedicated clarification artifact and never writes another task directory.

## Recorder, Checker, And Exits

Recorder derives proposal/action/payload/content/result SHA-256 values from the
AI-reviewed payload and emits canonical result bytes. Checker recomputes
them and validates current live GitHub/Git/task facts. Both are deterministic,
perform no GitHub write, and cannot synthesize a semantic pass.

- `clear` -> workflow target `guru-requirements-clear-router`;
- `needs_context` -> Skill `guru-discover-change-context`;
- `refresh_context` -> Skill `guru-sync-base`;
- `retarget_context` -> Skill `guru-sync-base` and complete initial-intake rerun;
- `new_task` -> workflow target `guru-full-task-intake-chain` (staged #112);
- `blocked` -> stop `requirements-clarification-blocked`.

`blocked` if and only if `ai_review_gate.status=blocked`. Unknown, multiple or
unmapped exits fail closed. Pre-task/standalone results remain stdout-only and
never write a repo cache, workspace journal or fixed handoff. The package
requires the complete current Guru Team preset and is not self-contained or
portable.

The recorder accepts the closed Schema 2.0 semantic shape with only the derived
fields listed below omitted. It validates that shape before calculating values
and validates the complete Schema 2.0 result before returning it. Checker and
invoke require the complete result and independently recompute the same fields.
Supplied derived values are consistency assertions, never silently replaced.
No schema version, Skill id, decision, target, consumer or gate is defaulted.

### Minimal Recorder Authoring

Public input profiles and output schemas are unchanged. This table describes
only the transient private owner JSON consumed by record, not public input.

| Required semantic fields | Source |
| --- | --- |
| `schema_version`, `skill_id`, `generated_at`, `mode` | Explicit current result metadata; `2.0` and `guru-clarify-requirements` |
| `typed_exit`, `consumer`, `invocation_context`, `reason`, `error` | Completed AI route and caller decision, with explicit nullable fields |
| `review_target`, `target_disposition`, `context_evidence` | Current reviewed facts and final target decision; null disposition only where already allowed |
| `confirmed_facts`, `repository_answerable_questions`, `clarification_rounds`, `open_questions`, `scope_proposals`, `affected_contracts` | AI-reviewed content and final proposal decisions; explicit arrays even when empty |
| `source_actions`, `mutation_results`, `active_task_evidence` | Explicit selected actions, preimages, external receipts and task evidence; no-action still requires the existing `none` row |
| `ai_review_gate` | Complete explicit AI judgment; missing gate/status/decision never means passed |

All nested semantic fields remain required by
`.trellis/guru-team/skills/packages/guru-clarify-requirements/schemas/requirements-clarification.schema.json`.
The exact fields that normal authoring may omit are:

| Omittable field | Deterministic derivation |
| --- | --- |
| `review_target.facts_sha256` | Facts digest of the remaining review-target fields |
| `target_disposition.disposition_digest` | Facts digest excluding this field and the upstream `duplicate_facts_sha256` |
| `scope_proposals[].proposal_digest` | Facts digest of the remaining proposal fields, including the AI decision |
| `source_actions[].payload_sha256` | Compact digest of the explicit payload object; null for null payload |
| `source_actions[].action_digest` | Compact digest of `action_id`, `kind`, `target`, `payload`, `preimage_sha256`, `payload_sha256` |
| `content_identity` (whole object) | The eight complete bindings below, after deriving the fields above |

Both encodings use UTF-8 JSON with sorted keys, compact separators, unescaped
Unicode and unchanged array order. Facts digests retain a trailing LF; compact
digests have no trailing LF. Target/proposal/disposition use their established
facts projections; action/content/result use the current compact encoding.
There is one rule per field, not a version reader or alternate accepted digest.

The eight `content_identity` fields are compact digests: `target_sha256` hashes
`review_target`; `disposition_sha256` hashes `target_disposition` (including its
upstream token); `context_sha256` hashes `context_evidence`; `scope_sha256`
hashes `scope_proposals`; `action_sha256` hashes `source_actions`;
`payload_sha256` hashes the ordered action payload list. `content_sha256`
hashes the object containing `confirmed_facts`, `repository_answerable_questions`,
`clarification_rounds`, `open_questions`, `affected_contracts`, and `reason`.
`result_sha256` hashes the whole completed result except `content_identity`.

Do not omit or recalculate upstream `duplicate_snapshot.facts_sha256`, its
candidate `facts_sha256`, or disposition `duplicate_facts_sha256`. Copy these
opaque values unchanged from Discovery. Invoke checks exact token and candidate
fact equality plus target/query/time/authority bindings, without implementing
Discovery's hash algorithm. Selected-issue facts, body/preimage checksums,
mutation receipts, planning/authority checksums and decision-trail references
remain explicitly supplied evidence; this recorder does not select, reconstruct,
or execute them. Changed content with old bindings is rejected by record,
checker and invoke; after a fresh AI review, omit the listed fields to record
the new content. Binding validation is not proof of a live external read.

From the repository root, use the actual installed wrappers:

```bash
bash .trellis/guru-team/skills/packages/guru-clarify-requirements/scripts/record-requirements-clarification.sh --mode workflow --input - --json
bash .trellis/guru-team/skills/packages/guru-clarify-requirements/scripts/check-requirements-clarification.sh --input - --json
bash .trellis/guru-team/skills/packages/guru-clarify-requirements/scripts/invoke.sh --invocation - --json
```

Standalone recording uses `--mode standalone`; checker optionally accepts
`--expected-result-sha256` from record stdout. Full result examples live at
`.trellis/guru-team/skills/packages/guru-clarify-requirements/examples/requirements-clarification.json`,
not under an Agent discovery projection. Scripts use the managed interpreter;
do not import an eval helper or run a package module with system Python.

The clear router validates `invocation_context.resume_target` without making a
new semantic decision: initial issue/draft uses `guru-review-contract-wording`
(staged #114), standalone uses `guru-standalone-caller`, accepted-current
active scope uses `guru-active-task-planning-review`, and a non-current active
classification uses the exact declared interrupted Phase 1/2/3/Branch Review
target. Any kind/target mismatch fails closed.

## Interface 1.4 Public Handoff

For the normal initial Issue path, copy Discovery's actual invoke stdout:
`handoff_target_locator` becomes public `target_locator`, and `transition` and
`duplicate_snapshot` are retained unchanged. All three target locators must
equal the canonical issue URL originating in `live_change.identity`; do not
replace it with `#N`. Copy the complete snapshot, including its opaque digest,
rather than manually rebuilding it from an example. This also preserves the
target identity for the next Wording consumer.

The public profiles are `initial_change_request`, `active_task_scope_change`,
`standalone_review`, and `normal_scenario_scope_confirmation`. After the owner loop,
`.trellis/guru-team/skills/packages/guru-clarify-requirements/scripts/invoke.sh --invocation -`
validates the closed call-local public input,
`context_current` transition, and current owner result, reruns the existing
checker, validates mode/target/continuation freshness, derives the Agent-owned
typed route and minimal output from the checked result, and serializes only the
declared continuation; clarification evidence remains private and is never
imported by the next Skill. The envelope has no top-level `typed_output` input:
callers cannot provide or select the route. Locator arguments remain only for
explicitly documented compatibility consumers and are not the normal route.

Only successful public invoke stdout is the final DTO. A record/check
`typed_exit` is owner-private evidence, not a public exit. If invoke returns
an error, preserve and report that actual failure, correct ordinary authoring
omissions from already reviewed facts or follow the declared context re-entry,
then rerun the affected record/check/invoke sequence. Never hand-write a blocked
DTO, copy an example output, or present a planned semantic exit as successfully
emitted. An unresolved invocation error remains an execution failure, even when
the AI correctly judged that the product conflict should block.
