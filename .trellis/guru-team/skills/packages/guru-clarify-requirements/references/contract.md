# `guru-clarify-requirements` Contract

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

## Forward Behavior

Execute in this order:

1. validate invocation, review target, current context and authority;
2. classify input into confirmed facts, repository-answerable questions,
   product-intent questions, scope-risk decisions and out-of-scope facts;
3. search current open issues for duplicates and author one mutually exclusive
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
8. when required, show exact target, target disposition, payload, scope delta,
   affected contracts,
   executor command and derived action/proposal digests, then obtain dedicated
   human confirmation;
9. after confirmation only, the AI may execute a GitHub write, reread live
   facts, and provide mutation evidence;
10. call recorder/checker and return one typed exit.

AI owns question selection, clarity, scope classification, action selection,
confirmation necessity, semantic pass/block and route intent. Scripts never
perform those judgments.

## Questions And Convergence

Every clarification round contains one `question_id` that must be opened in
that round or already belong to the current open set. The reducer enforces
`open_questions = opened - closed`, rejects close-before-open and
reopen-after-close, and does not allow an empty lifecycle to hide a partial
answer. `answer_status=partial` cannot close its own or another question. A refused load-bearing decision can
produce `blocked`; a rejected/deferred expansion that leaves current confirmed
scope complete is classified as related, followup, new task or out-of-scope and
does not block that current scope. During an active task, an unconfirmed
expansion cannot receive any of those five scope classifications without dedicated
proposal-digest-bound user decision evidence.

`clear` is valid only when `open_questions=[]`, the AI Review Gate passed,
source/context authority is current, all accepted proposals have exact
confirmation when required, and no successful GitHub mutation remains
unrefreshed.

## Target Disposition

Every initial issue/draft review records exactly one disposition:

- `keep_current_open_issue`: retain the current open issue;
- `keep_current_draft`: retain the side-effect-free proposed draft;
- `retarget_existing_issue`: select one different open duplicate candidate;
- `reopen_closed_issue`: retain and reopen the closed source issue;
- `create_followup_draft`: retain the closed issue only as related/reference
  and produce a new side-effect-free issue draft;
- `block_target_complete`: record evidence that the target is complete and no
  independently deliverable gap remains.

`needs_context` or a blocked incomplete decision may carry no disposition only
because it cannot advance downstream. Every progressing `clear`,
`refresh_context`, `retarget_context`, or `new_task` result requires one current
disposition. In particular, an issue comment/body edit or proposed-draft update
cannot use `target_disposition=null` while returning `refresh_context`.

Duplicate search is mandatory even when its candidate set is empty. Every
candidate binds live repo/number/state/URL/updated-at facts and one `selected`
or `rejected` AI decision. Non-empty candidate sets require exact human
confirmation for both a keep decision and a selected replacement; empty sets
do not manufacture confirmation for `keep_current_*`.

`retarget_existing_issue` owns one exactly confirmed
`select_existing_issue` action and returns `retarget_context`. Its unique
consumer is `guru-sync-base`; the complete sync, context discovery,
clarification, wording and change-request review chain reruns for the selected
issue. No target-specific evidence from the old target transfers.

`reopen_closed_issue` owns one exactly confirmed `reopen_issue` GitHub
mutation and returns `refresh_context`. `create_followup_draft` owns a
`new_issue_draft`, returns `new_task`, and cannot place the original closed
issue in the future task's close set. `block_target_complete` requires a
blocked AI gate and returns `blocked`. Closed issues cannot reach `clear`.

## Scope Proposals

Every proposal binds exact scenario, trigger evidence, proposed contracts,
cost, alternatives, omission consequence, origin status, decision and derived
digest. `unconfirmed_expansion + accepted_current` requires a dedicated
proposal-digest-bound confirmation. A generic continuation, task creation,
planning approval or review confirmation never qualifies.

When `optional_mechanism_origin=true`, decision cannot be `accepted_current`.
Remove or replace that mechanism; if independent product value remains, form a
new proposal and confirm it separately. Unrequested threat, attack, TOCTOU,
race, fault-injection or cross-OS hardening follows this same rule.

## Source Actions And Mutation Boundary

Actions are exactly `none`, `issue_comment`, `issue_body_edit`,
`proposed_draft_update`, `new_issue_draft`, `select_existing_issue`,
`reopen_issue`, and `active_task_scope_update`. There is no mutation executor
in this package.

For `issue_comment` or `issue_body_edit`, the AI must reread the live preimage,
match repo/issue/action/payload/confirmation digests, execute the exact existing
connector action or reviewed `gh` command, reread live facts, then pass only
normalized mutation facts to recorder/checker. Success returns
`refresh_context`, never `clear`. Checker requires exact equality among the
human-confirmed action payload body, canonical payload digest, mutation result
content digest, and reread live body/comment bytes. `new_issue_draft` performs no issue creation
and returns `new_task`; #112 owns the complete intake mutation route.

Every clarification round carries an AI-authored `authority_impact` and
`authority_action_ids`. `load_bearing` covers any answer that changes problem,
scope, acceptance, non-goals, issue disposition, risk/test boundary, or another
contract future implementation must consume. For an issue target it requires
a confirmed `issue_comment` or `issue_body_edit`, followed by live reread and
`refresh_context`; for a draft target it requires a confirmed and validated
`proposed_draft_update` bound to current draft bytes. `none + clear` is invalid
for a load-bearing round. `non_load_bearing` does not require or permit an
authority action merely to satisfy the contract.

## Active-Task Scope Change

Pause implementation/check/commit/review progression. Classify new input as
current close scope, related, followup, new task or out-of-scope. Current
inclusion requires the same delivery unit, no material boundary/risk/test
expansion, complete updated planning and dedicated confirmation.

Active-task `clear` and `new_task` require a non-empty set containing only the
seven terminal decisions: the five scope classifications `accepted_current`,
`related`, `followup`, `new_task`, and `out_of_scope`, plus the mechanism
dispositions `mechanism_removed` and `mechanism_replaced`. `new_task` must
contain at least one `decision=new_task` classification. Every scope
classification requires proposal-digest-bound exact user-decision evidence,
regardless of its origin status, and binds one structured `decision_trail`.
Mechanism dispositions instead require `optional_mechanism_origin=true` and
`confirmation_ref=null`; they never enter the trail or trigger GitHub/task
authority mutation. A mechanism-only payload may return `clear`, and a mixed
payload projects only its five-classification subset into confirmation/trail.
Mechanism-only still carries the current task-local ledger, all three planning
documents, complete planning approval, review/stale identities, re-entry
owners, and current context evidence; only `decision_trail` is null. Every
terminal active-task path receives the same live task/context freshness check.
The exact trail is stored in current
`issue-scope-ledger.json.scope_decisions[]` and contains proposal decisions,
user-decision evidence, live GitHub comment/body authority including
`updated_at`, the `context_before_task_update_sha256`, all three planning
document digests, planning approval,
Branch-Review state, interrupted resume target and re-entry owners
`guru-approve-task-plan`, `guru-check-task`, and `guru-review-branch`. Checker
parses the ledger and requires one exact trail match. It reuses the complete
shared `check-planning-approval --require-exit approved` validator for the
Skill-owned `guru-planning-approval-2.0` artifact. That validation covers the
current task and requirement authorities, wording evidence, Docs SSOT Plan,
four-class provenance, unusual-scenario dispositions, AI Gate, facts digest,
typed exit/consumer, exact reviewed/approved aliases, and all three current
planning-document bindings. The ordinary planning confirmation must have
`user_confirmation.kind=post-planning-approval`, `status=confirmed`, and
non-null prompt/confirmation timestamps; generic continuation or a legacy
confirmation source cannot substitute. An old ledger hash, two-line planning
placeholder, active legacy approval, or minimal approval/review JSON is
insufficient.

If `review-gate.json` exists, re-entry requires
`review_evidence.status=stale` and the exact artifact path/content digest.
`not_started` is valid only when that file is absent, its artifact is null, and
the stale downstream Branch Review digest is null. `current` is never valid
during active-task re-entry.

GitHub comment/body mutation returns `refresh_context` before any task-local
update. On re-entry, live authority kind/URL/content/`updated_at` must match,
current `context-discovery.json.generated_at` must be at least that authority
time, and its snapshot digest must equal `context_before_task_update_sha256`.
The AI then validates the current ledger/planning/review/stale identities and
one `active_task_scope_update` action. The same exact confirmation that covers
the five-class proposal set must use
`confirmation_kind=exact_source_action_and_scope`, list that task-update action
id in `confirmed_actions[]`, and bind the canonical digest of the confirmed
action set before the task-local source-of-truth write. Proposal-only
confirmation, planning approval, or `status=validated` cannot substitute for
this action confirmation. A task-only update does not require a
second context snapshot or a changed digest before `clear` or active-task
`new_task` resumes the exact interrupted progression. `new_task` then carries only a reviewed
side-effect-free draft; #112 still owns issue/task creation. This Skill records
no dedicated clarification artifact and never writes another task directory.

## Recorder, Checker, And Exits

Recorder derives proposal/action/payload/content/result SHA-256 values from the
AI/human-reviewed payload and emits canonical result bytes. Checker recomputes
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
requires the complete compatible Guru Team preset and is not self-contained or
portable.

Schema 2.0 is a breaking artifact-contract version. Schema 1.0 callers and
artifacts cannot express required target disposition, duplicate decisions,
authority impact, `select_existing_issue`, `reopen_issue`, or
`retarget_context`; recorder/checker reject them with
`requirements_clarification_legacy_schema_requires_refresh`. There is no
semantic auto-migration. The caller reruns from `guru-sync-base` and produces a
fresh 2.0 result.

The clear router validates `invocation_context.resume_target` without making a
new semantic decision: initial issue/draft uses `guru-review-contract-wording`
(staged #114), standalone uses `guru-standalone-caller`, accepted-current
active scope uses `guru-active-task-planning-review`, and a non-current active
classification uses the exact declared interrupted Phase 1/2/3/Branch Review
target. Any kind/target mismatch fails closed.

## Interface 1.3 Public Handoff

The public profiles are `initial_change_request`, `active_task_scope_change`,
and `standalone_review`. After the owner loop,
`scripts/invoke.sh --input ... --owner-result ...` reruns the existing checker,
derives the Agent-owned typed route from its checked result, and serializes only
the declared continuation; clarification evidence remains private and is never
imported by the next Skill.
