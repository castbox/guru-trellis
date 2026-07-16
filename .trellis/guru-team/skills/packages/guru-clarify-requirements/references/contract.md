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
3. inspect current Docs/code/tests/history/GitHub/Git evidence until every
   repository-answerable question is `answered` with checked evidence or
   `not_answerable` with checked evidence and a missing reason;
4. ask exactly one highest-value user question per round. Use one
   `atomic_group` only for an indivisible product choice and record why it
   cannot be split. A partial answer closes no question;
5. propose exact scope decisions and source-of-truth actions;
6. execute the AI Review Gate;
7. when required, show exact target, payload, scope delta, affected contracts,
   executor command and derived action/proposal digests, then obtain dedicated
   human confirmation;
8. after confirmation only, the AI may execute a GitHub write, reread live
   facts, and provide mutation evidence;
9. call recorder/checker and return one typed exit.

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
`proposed_draft_update`, `new_issue_draft`, and
`active_task_scope_update`. There is no mutation executor in this package.

For `issue_comment` or `issue_body_edit`, the AI must reread the live preimage,
match repo/issue/action/payload/confirmation digests, execute the exact existing
connector action or reviewed `gh` command, reread live facts, then pass only
normalized mutation facts to recorder/checker. Success returns
`refresh_context`, never `clear`. Checker requires exact equality among the
human-confirmed action payload body, canonical payload digest, mutation result
content digest, and reread live body/comment bytes. `new_issue_draft` performs no issue creation
and returns `new_task`; #112 owns the complete intake mutation route.

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
parses the ledger and requires one exact trail match. It reuses the shared
schema 1.2 planning-approval validator, including explicit post-planning
confirmation, passed ambiguity review, controlled-term scan, all seven checked
dimensions, exact reviewed/approved aliases, and the three path/hash/size
bindings; an old ledger hash, two-line planning placeholder, or minimal
approval/review JSON is insufficient.

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
- `new_task` -> workflow target `guru-full-task-intake-chain` (staged #112);
- `blocked` -> stop `requirements-clarification-blocked`.

`blocked` if and only if `ai_review_gate.status=blocked`. Unknown, multiple or
unmapped exits fail closed. Pre-task/standalone results remain stdout-only and
never write a repo cache, workspace journal or fixed handoff. The package
requires the complete compatible Guru Team preset and is not self-contained or
portable.

The clear router validates `invocation_context.resume_target` without making a
new semantic decision: initial issue/draft uses `guru-review-contract-wording`
(staged #114), standalone uses `guru-standalone-caller`, accepted-current
active scope uses `guru-active-task-planning-review`, and a non-current active
classification uses the exact declared interrupted Phase 1/2/3/Branch Review
target. Any kind/target mismatch fails closed.
