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
does not block that current scope.

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

Bind live GitHub-visible authority, current `issue-scope-ledger.json` digest,
all three planning document digests, stale planning/Phase-2/Branch-Review
identities, and re-entry owners `guru-approve-task-plan`, `guru-check-task`, and
`guru-review-branch`. This Skill records no dedicated task artifact; it
validates the existing updated artifacts and legal re-entry contract. The
canonical active-task Scope Change Gate mandatory invokes this Skill and does
not duplicate these steps.

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
