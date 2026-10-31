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
Its current upstream contract supplies requirement exploration only; Guru's
task creation, activation and completion owners remain separate. Clarification
does not require or establish a task personnel identity.

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

On fresh Intake after Issue creation or a same-scope context return, read the
formal target identity, complete current authority and actual Discovery public
output first. Compare the new target/body and scope with the investigation
already available in this conversation. Reuse facts only where their sources
and conditions still apply; resolve evidence-answerable gaps from those facts
before asking another product question. Do not repeat an interview for an
already clear same-scope fact or rebuild Discovery's private result. This owner
still personally judges current intent, source roles, duplicate disposition
and scope, then produces its own result for Wording or the original Author.
Changed or unavailable authority returns to the affected original context or
scope owner; an old-target pass cannot supply the current judgment.

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

The independent `standard_intake` and `reviewed_plan_intake` input schemas
replace the retired `initial_change_request` profile. Both require a checked
duplicate snapshot; reviewed-plan input additionally carries explicitly selected
source locators. The snapshot is accepted only when target locator, authority body digest,
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

For Issue/draft writing, revision, and requirements review, actually read
[the shared Issue content specification](issue-content.md) and the installed
writing specification before the applicable work. That body owns content
organization; this contract retains source actions and their execution order.
When the user requests creation or improvement, organize necessary confirmed
content into the final body under that specification. Ordinary discussion may
still use comments; a comment alone does not complete requested body editing.
Review-only requests do not acquire mutation authority. Apply the shared
complete-body and local-revision rules within this owner's existing gate.

Historical 3.0 actions are exactly `none`, `issue_comment`, `issue_body_edit`,
`proposed_draft_update`, `new_issue_draft`, `select_existing_issue`,
`reopen_issue`, and `active_task_scope_update`. There is no mutation executor
in this package. Current active 4.0 excludes active_task_scope_update;
its independent scope_ready boundary is defined below.

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

## Historical Active-Task Scope Change — private 4.0 / scope_ready 1.0

This section preserves the pinned-old contract for validation and migration
evidence. Current schema2 installations must use the independent whole-scope
writer and publication migration below; do not invoke this Task-status route.

Pause implementation/check/commit/review progression. Reread the same live
TaskId/generation, Direct Source or legal no_issue relation and current scope.
Classify new input as current task scope, related, followup, new task or
out-of-scope. Current inclusion requires the same delivery unit and the actual
scope choice where required. Clarify judges scope before planning is written;
it never requires complete updated planning or writes planning itself.

Current active calls use `requirements-clarification-active-task-4.0.schema.json`.
The private result retains current context/authority, terminal proposals, the
compact owner-result `decision_trail`, source selection and AI-selected
`revision_refs`. Active evidence contains only task_locator,
github_authority_facts_sha256 and nullable decision_trail. The trail contains
final classification decisions plus the remote authority locator and content
checksum; no authorization, planning hashes or reentry_owners are recorded.
Mechanism dispositions require optional_mechanism_origin=true and remain outside
the classification trail. Legal no_issue and no-classification cases may have
null trail; an external authority classification uses the actual remote facts.

`scope_ready` requires current context, zero open questions, a passed AI Gate,
a nonempty terminal proposal set containing accepted_current and nonempty
revision_refs chosen by this AI from the actual revised sources. The seven
terminal decisions retain their meanings: accepted_current, related, followup,
new_task, out_of_scope, mechanism_removed and mechanism_replaced. Do not derive
revision_refs from every selected source or let a script choose the scope.
`scope_ready` means scope is ready for Author; it is not planning approval,
activation, task mutation or permission to resume execution.

The new public output contains exactly exit_id, mode, task_ref,
source_selection and revision_refs. Its one consumer is the existing
`guru-requirements-clear-router`, whose new independent 1.0 input receives the
output directly. That router drops exit_id, adds fixed
profile=active_task_scope_change and passes the other four fields unchanged to
`guru-author-task-plan`. No transition, digest, planning identity, private
result, caller-selected route or resume_target crosses this boundary.

Active `clear` remains for terminal non-current/mechanism-only decisions and
returns to the exact interrupted consumer; it cannot contain accepted_current.
Active `new_task` requires an actual terminal new_task proposal and reviewed
side-effect-free draft; original intake still owns new resource creation.
Neither route requires planning hashes or an active_task_scope_update action.

A GitHub comment/body/reopen mutation still returns refresh_context before
current scope can proceed. The AI rereads authority kind/URL/content and update
time directly, then fresh Sync/Discovery returns current context to this same
profile. Missing context returns needs_context and the original caller-aware
Discovery return. Runtime validates supplied schema/digest/context/task bindings;
it does not perform the AI's live GitHub read or task-local write.

Historical private 3.0, public clear 3.0 and workflow clear consumer 2.0 retain
original bytes. Other profiles keep 3.0. A historical successful active 3.0
result fails with fresh original-producer re-entry; it is never converted into
scope_ready or a new pass. Historical blocked is preserved as evidence, not
replayed as progress. Existing activate/resume_execution owners retain lifecycle
status; an in_progress replan does not rerun initial activation.

## Recorder, Checker, And Exits

Recorder derives proposal/action/payload/content/result SHA-256 values from the
AI-reviewed payload and emits canonical result bytes. Checker recomputes
them and validates supplied schema and content bindings. The AI owns live
GitHub/context reads; public invoke validates the current active task identity. Both are deterministic,
perform no GitHub write, and cannot synthesize a semantic pass.

- `scope_ready` -> the same workflow target `guru-requirements-clear-router`,
  then its fixed active-task Author input projection;
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

The recorder accepts the closed Schema 3.0 non-active or Schema 4.0 active semantic shape with only the derived
fields listed below omitted. It validates that shape before calculating values
and validates the complete selected-version result before returning it. Checker and
invoke require the complete result and independently recompute the same fields.
Supplied derived values are consistency assertions, never silently replaced.
No schema version, Skill id, decision, target, consumer or gate is defaulted.

### Minimal Recorder Authoring

The current public profiles and successor outputs are declared in the Interface. This table describes
only the transient private owner JSON consumed by record, not public input.

| Required semantic fields | Source |
| --- | --- |
| `schema_version`, `skill_id`, `generated_at`, `mode` | Explicit current result metadata; `3.0` for non-active profiles, `4.0` for active and `guru-clarify-requirements` |
| `typed_exit`, `consumer`, `invocation_context`, `reason`, `error` | Completed AI route and caller decision, with explicit nullable fields |
| `review_target`, `target_disposition`, `context_evidence` | Current reviewed facts and final target decision; null disposition only where already allowed |
| `confirmed_facts`, `repository_answerable_questions`, `clarification_rounds`, `open_questions`, `scope_proposals`, `affected_contracts` | AI-reviewed content and final proposal decisions; explicit arrays even when empty |
| `source_actions`, `mutation_results`, `active_task_evidence` | Explicit selected actions, preimages, external receipts and task evidence; no-action still requires the existing `none` row |
| `revision_refs` (4.0 only) | AI-selected changed source references; nonempty for scope_ready |
| `ai_review_gate` | Complete explicit AI judgment; missing gate/status/decision never means passed |

All nested semantic fields remain required by the profile-selected private
schema declared above; historical 3.0 remains immutable.
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
mutation receipts, authority checksums and decision-trail references
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
`--expected-result-sha256` from record receipt `result`. Full result examples live at
`.trellis/guru-team/skills/packages/guru-clarify-requirements/examples/requirements-clarification.json`,
not under an Agent discovery projection. Scripts use the managed interpreter;
do not import an eval helper or run a package module with system Python.

The clear router validates `invocation_context.resume_target` without making a
new semantic decision: initial issue/draft uses `guru-review-contract-wording`
(staged #114), standalone uses `guru-standalone-caller`, scope_ready uses the fixed Author projection above, and a non-current active
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

The six current public profiles are `standard_intake`, `reviewed_plan_intake`,
`active_task_scope_change`, `standalone_review`,
`normal_scenario_scope_confirmation`, and `solution_mechanism_scope_confirmation`. After the owner loop,
`.trellis/guru-team/skills/packages/guru-clarify-requirements/scripts/invoke.sh --invocation -`
validates the closed call-local public input,
`context_current` transition, and current owner result, reruns the existing
checker, validates mode/target/continuation freshness, derives the Agent-owned
typed route and minimal output from the checked result, and serializes only the
declared continuation; clarification evidence remains private and is never
imported by the next Skill. The envelope has no top-level `typed_output` input:
callers cannot provide or select the route. Locator arguments remain only for
explicitly documented compatibility consumers and are not the normal route.

Only successful public invoke stdout is the final DTO. A record/check receipt
`result.typed_exit` is owner-private evidence, not a public exit. If invoke returns
an error, preserve and report that actual failure, correct ordinary authoring
omissions from already reviewed facts or follow the declared context re-entry,
then rerun the affected record/check/invoke sequence. Never hand-write a blocked
DTO, copy an example output, or present a planned semantic exit as successfully
emitted. An unresolved invocation error remains an execution failure, even when
the AI correctly judged that the product conflict should block.

## Intake semantic ownership and source selection (#250)

Clarify alone owns user intent, requirement authority, source classification,
Issue intent and real unresolved choices. Discovery supplies repository/history
evidence and coverage; Wording and readiness retain their independent judgments.
Read Direct Source, explicitly selected comments and introduced requirements or
design sections fresh. Distinguish normative interfaces, mechanisms, order and
compatibility constraints from advisory candidates; the presence of a design
does not make its normative clauses optional. Clear technical sources need zero
questions. Answer repository-searchable questions from evidence first. Ask at
most one highest-value unresolved question per round, with evidence, options,
a recommendation and trade-offs. An actual partial answer stays unresolved.

`standard_intake` is the ordinary initial owner. `reviewed_plan_intake` requires
`source_locators` for the selected existing requirements/design; its name never
substitutes for fresh review. Both retain Discovery's checked duplicate snapshot.
`active_task_scope_change` preserves TaskId/generation and the interrupted
consumer; `standalone_review` preserves its declared `resume_target`.
The two qualification confirmation profiles are distinct: consume actual
qualifier stdout, ask only its unresolved authority choice, and return to its
original owner. Context repair returns to that qualification owner, rather than
entering the four-profile Discovery loop.

When load-bearing context is missing in any of the four context-capable
profiles, emit `needs_context` with `handoff_profile=context_request`. The
discriminated `return_identity` contains only profile, target and continuation,
plus selected source locators, active task identity/interrupted consumer, or
standalone consumer as required by that profile. Discovery returns that exact
profile and identity with new context. Freshly project its actual stdout into
the independently owned input; never reuse an old invocation object, owner
result or stale duplicate snapshot on a repeated return.

The AI authors `source_selection` in the selected 3.0/active 4.0 owner result. Each selected
entry is only `locator`, `section`, and `authority_kind` (`requirement`,
`design_constraint`, or `advisory`). The selection itself carries the
irreducible choice of which comment/section and its authority role. Empty is
legal when there is no introduced source. No full text, final design disposition,
history, source matrix or authorization belongs here. `clear` or `scope_ready` hands it to the
clear router; the transition relays it through current Wording/readiness to
current Planning. Planning rereads sources and owns final retain/change/reject
only in `design.md`. A lost selection re-enters this owner instead of guessing
from task metadata or introducing a persistent cache.

Upstream `trellis-brainstorm` remains discoverable. It may be unselected,
automatically selected, or deliberately reused for a method. In every case
this Skill remains the semantic owner: constrain any loaded method to the
current stage, input, exact return consumer and question policy above. Method
reuse never creates a second interview, separate planning owner, Issue/task
mutation path or exemption from current Guru gates.

See [MIGRATION-250.md](./MIGRATION-250.md) for the synchronized public API
replacement and current caller re-entry.

## Delivery scope revision

Use delivery_active_task_scope_change with exact DeliveryKey, or
delivery_task_scope_revision with TaskKey when whole-task scope changes and
no current Delivery is needed. Initial whole-Task scope after public Task
creation uses the latter profile with source_exit=created and the Creation
resume target. Null accepted_scope is not approval. Review current source,
whole-task authority and the affected Delivery plan when present. Return the
original source_selection/revision_refs and scope_action (revised, no_change
or withdrawal_required) to Author task_scope_requirements. This pre-Author
judgment does not accept_scope or write PRD.
Partial revision returns to the same Delivery's earliest affected owner after
post-Author scope acceptance. Whole withdrawal returns to its current stage
owner for legal public stop and automatic selection release: task_scope must
not impersonate another role. Existing PR/history survives; PR closure/cleanup
remain independent. No-current-Delivery closeout and evidence refresh do not
create empty slices. Legacy active_task_scope_change requires the pinned old
complete installation; it is not a current fallback or schema-2 writer.

## Whole-scope writer and publication migration (schema2)

The single Author owns root whole requirements, while this same Clarify owner
owns the initial source/scope judgment and the post-Author scope publication.
New Delivery scope profiles emit scope_ready2.0 before authoring with original
source_selection/revision_refs and scope_action; they perform no accept_scope.
The task_scope_requirements_acceptance profile consumes the actual Author
scope_requirements_ready requirements_locator plus the original current source
selection. After fresh semantic review it binds the root PRD real revision and
calls installed accept_scope using the declared task_scope owner. It returns
scope_ready2.0 with TaskKey to Creation or affected-stage routing. Missing source
selection refreshes Clarify; it is not recovered from PRD/metadata. Scope-only
writing is not Task Planning and cannot reach Architecture/Approval/Activation.

Legacy active_task_scope_change and missing-key gate results are pinned-old
validation only; current migrated installations fresh re-enter the proper
scope/Delivery owner. Do not convert an old pass by appending a key. History
and committed clean content remain facts. This complete installation migration
is the only switch; no old status writer or reader fallback is added.
