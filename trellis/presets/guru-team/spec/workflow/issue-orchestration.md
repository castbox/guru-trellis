# Issue Orchestration Method

This is the shared semantic contract for `guru-orchestrate-issue-dag` and
`guru-orchestrate-issue-sequence`. Their package-local contracts own scheduling,
serial advancement, and typed exits. This method owns selected-base continuity,
endpoint interpretation,
current-dialogue authority, overall completion responsibility, active unblocking,
native child operation, progress decisions, merge proof, completion proof,
native observation, quiet notifications, and supported recovery.

## Provider And Scope

Load this method and `clear-technical-writing.md` from the same provider as the
selected package. In a complete source checkout the spec root is
`trellis/presets/guru-team/spec/workflow`; in a complete installation it is
`.trellis/spec/workflow`. Package roots are respectively
`trellis/skills/guru-team/packages` and `.trellis/guru-team/skills/packages`.
A platform projection locates that provider; it is not another semantic owner.
Do not combine personal historical copies with current managed packages.
If a personal discovery entry is a filesystem link, resolve its real path before
locating the containing provider. The target project or current working directory
does not establish which provider supplied the Skill.

Each target business repository may be elsewhere, independently of the
coordinator and provider. It supplies its own current
AGENTS.md, workflow, Skills, accepted Issue scope, and live Git/GitHub facts.
The coordinator does not install or replace its workflow. These Skills are
Codex-only, explicitly invoked, instruction-only standalone operations. They
are not mandatory phases of a single-Issue workflow and create no coordinator
Task, scheduler script, database, status file, checkpoint, or journal.

`judgment_mode=semantic`: perform the requested work, conduct the AI Review
Gate, consume only necessary current-dialogue confirmation, use native tools
to validate objective facts, and return one package-declared typed exit.
Native tool results do not prove semantic sufficiency or authorize a route.
No dummy recorder, JSON permission input, or persisted gate is required.

## Current Human Endpoint And Authority

Before the first child is created, read the actual human messages
for this run in the coordinator conversation. The goal is full Issue completion
under the completion proof below. A request to process the selected Issues does
not need another endpoint choice. Planning, PR publication, a child turn ending
and a Delivery merge are intermediate results, not alternative completion goals.
Resolve whether the actions needed to reach completion, including merge where
applicable, are delegated. Use the human's meaning, not a required phrase or an
assistant plan. `auto` continues after preflight within the current action
boundary; it grants no unlimited merge permission.

An explicit human request to pause or perform only an earlier stage limits the
current execution segment. Respect that boundary and state the remaining Issue
obligations. The existing stage-completed exits report only that requested
segment; they never mean the Issue goal is complete. Missing permission for an
action holds that action and prompts its concrete plan when needed. It does not
turn the run into PR-only work or remove subsequent completion obligations.

After read-only preflight, show precise prospective effects. If current human
instructions already cover them, start directly without another launch question.
If a necessary launch action boundary remains unresolved, ask only the concrete
missing action choice before child creation. Return `dry_run_blocked`
until that choice is resolved. Do not ask whether to aim for completion, silently
select PR readiness, or defer a known missing merge decision until every PR is
ready. A later action gap holds only dependent work; keep permitted work moving.

Only this run's actual human instructions establish or change its execution
limits and delegated scope. Assistant plans or scope statements, child requests,
summaries,
automation configuration, and another run's permission cannot independently
authorize or restrict this run. A scheduler wakeup is automation input even
when delivered as `role=user`. These sources may locate relevant conversation;
read the original human text before relying on it.

At each observation cycle, use still-current human instructions already read
in this conversation. After context loss, changed scope, or uncertain summaries,
recover the necessary original messages and distinguish automated wakeups. If
recovery is impossible or ambiguous, hold only the affected mutations and
report the missing source or choice. Do not ask the human to repeat an already
recoverable current delegation. Keep permitted inspection and bounded work moving.

Keep execution authorization, the human's execution limits, and their origin
and process in the current conversation only. Never serialize them as permission
or approval records in public inputs/outputs, schemas, checkpoints, journals,
archive, child prompts, or automation configuration. Ordinary operation inputs
such as model settings or accepted gates remain usable, and the conversation
result may state the actual stage reached and remaining work. A child's minimal
operational work segment and stop-before instruction do not record or prove
permission. Send a later concrete instruction such as `合并PR`
within actual delegation without attaching “the user already authorized this.”
Repository rules expressly requiring direct human confirmation still apply.

## DAG Action Authorization And Handoff

Apply this section to actions for nodes in the selected DAG. The coordinator
first identifies the exact action and target. Read the current proposal,
actual delegation, target rules, and the original step's prerequisites.
If delegation covers the action, the prerequisites pass, and the target rules
do not require direct human confirmation, send the exact instruction to the
original owner and read back its actual result. A child's “awaiting approval”
label alone does not require another user question.

The two cases below need no separate confirmation when all their conditions
hold. Apply them only to the current node and keep any explicit execution
limit or target rule requiring direct human confirmation. The coordinator
arranges the work; the original owner checks live facts and executes it.

### Stale worktree registrations

Use this disposition when a node's original step is blocked by stale worktree
registrations in its shared Git repository. The original executor uses Git to
preview the exact set its supported cleanup command would remove. For each
entry, verify that the worktree directory is absent and that no Task or running
operation needs that registration. Apply the same checks to registrations left
by other completed Issues.

Execute only if the command would remove exactly the verified set. If the
preview includes an extra entry, or any required fact is unknown, stop the
cleanup and recheck. Do not delete an existing worktree, branch, commit, Task
record, or remote resource under this rule. Read the registrations again and
verify that only the reviewed set was removed. Then resume the same node at
its original blocked step and observe the result.

### Converged Issue body revisions

Use this disposition when the original reviewer of a selected node proposes
the exact revised body for its Issue. Verify the Issue identity, the full text
to write, and the authority and repository evidence that establish the
editorial correction. The user's goal, scope, acceptance, and execution limits
must remain the same. Evidence that an identifier has no collision does not
establish a decision on an open option.

Send the exact amendment to the original Issue owner. That owner rereads the
live body, checks the text to be replaced, uses the existing body-edit entry,
and verifies the written body by reading it back. If the live body changed,
review the new body before any write. On success the original owner refreshes
the affected Intake and review conclusions for the same node. An unresolved
product or technical choice, material change, or direct-human rule stays at
the original confirmation boundary.

### Confirmation While Independent Work Remains

When the coordinator knows the exact action and determines that human
confirmation is required, hold that action and the work that depends on it.
If independent work can advance or has an owned bounded wait, send the exact
confirmation request in a user-visible message that leaves this turn active.
Send it as soon as the proposal and confirmation boundary are established,
before another event wait or continuation instruction. Then immediately
continue the existing native observation cycle. After each wait, reread the
original independent operation, even if its owner sent no new message.
Use the current result to keep waiting or direct the original owner to the next
permitted step. Read the actual result before reporting its status. While the
request is unanswered, leave the affected action on hold.

Use a nonterminal user-facing confirmation channel that the current host
supports and permits for this action. Include the affected node, the exact
proposed effect, and an explicit request for confirmation. A progress message
that reports the hold does not ask for confirmation. In a Codex CLI session
that permits confirmation questions in assistant commentary, use that
channel. If the current host forbids questions in commentary, use another
supported and permitted nonterminal confirmation channel only when one exists.

If no permitted nonterminal confirmation channel is available, report that
limit and keep observing permitted independent work. When the original
settlement rules allow a handback, give the exact remaining confirmation
request. A final response ends the turn, so do not use it just to wait for an
answer while independent work remains observable.
Deduplicate the request without skipping observations. The original settlement
conditions and [interruption recovery](#observation-after-an-interruption)
still apply.

## Selected Base

Resolve one selected base branch per target repository from the human's explicit choice;
only when that repository has no explicit base, use its live default branch.
For DAG, use its repository map; Sequence resolves its one repository. Never
apply the coordinator’s base or one target’s choice to all repositories. Keep
the exact repository, remote and branch consistent through initial preflight,
child creation/instructions, observation recovery, base reconciliation, PR target,
merge and completion proof. A separately requested starting state does not
silently change the integration target; resolve a real conflict before launch.

Read local branch, tracking ref and live remote OIDs for that selected base.
Do not require equality, fast-forward, fetching or any other mutation of an
unrelated branch outside it. A stale local `main` cannot block a run explicitly based on
current `dev`; no exemption or permission to update `main` is needed. The live
default branch remains relevant to GitHub closure semantics or an accepted
release requirement, not as an extra synchronization or delivery target.

If selected-base synchronization is actually needed, keep dry-run read-only and
use the target repository's original base owner for the exact selected branch.
A branch mismatch is not permission to switch or reset unrelated work. On
resume, recover the selection from this run's original messages and actual
child/Task/PR facts; do not replace it with a newer project default. A genuine
change to the target follows the original scope/base owners and affected gates.

## Public Inputs And Model Settings

Each package owns its concise conversation input contract. Resolve every
selected Issue’s canonical repository, saved local project and primary repository,
selected base and exact identity. DAG may span repositories; Sequence keeps its
one-repository input and strict complete-before-next rule. Their scheduling
contracts remain package-owned.
Do not put the endpoint or authorization in a normalized data object; resolve those from the
human conversation. Optional completion overrides identify concrete accepted
extra gates, not new release, deployment, cleanup, or publication permission.

Resolve exact `child_model` and `child_thinking` before live side effects.
Use the current tool schema and supported model/effort choices; do not copy a
fixed or outdated model list. Reuse an explicit selection already present in
this run. If either value remains absent, ask one concise current supported
model/reasoning choice before launch. Read-only analysis can continue while
that choice remains pending; do not force it merely to draw or dry-run a graph.

Pass the selected values as structured native creation parameters. Prompt text,
parent inheritance and platform defaults do not substitute for the resolved
selection. Unsupported explicit settings block dependent creation and require
a human-selected supported replacement, never silent fallback. Once a child
exists, preserve its settings on ordinary continuation and temporary capacity
recovery. Model names in examples are illustrative rather than defaults.

## Read-Only Preflight And AI Gate

Dry-run is strictly read-only. It may inspect authenticated GitHub data, local
Git status/refs, `git ls-remote`, saved projects, actual chat output and existing
automation configuration. It must not fetch, update refs, edit files, create
chats/worktrees/Tasks, send messages, or mutate GitHub or automations.

Before a live launch, verify the whole selected run:

| Check | Required proof |
| --- | --- |
| Provider/tools | Same-provider package and shared method; current native project, chat, message, wait and live-read capabilities. |
| Repository/project | For every target `owner/repo`, authenticate access and resolve its current saved local project, actual primary folder and repository remote. A coordinator/provider project or an added secondary folder is not proof of the target primary repository. |
| Initial base | Each repository’s selected base is resolved under the rule above; its local branch, tracking ref and live remote OIDs agree. Report those facts without fetching. Unrelated branches add no equality or update requirement. |
| Initial checkout | Clean and suitable for each target repository's normal intake; no unrelated work is reset or moved. |
| Issues | Selected identities are accessible and open initially, with sufficient current scope and completion criteria. Explicit resume can adopt completed nodes only after fresh full proof. |
| Dependencies | Package scheduling rules and live hard prerequisites are compatible with the requested endpoint. |
| Existing owners | No competing coordinator, pending creation, child or Task for a selected `repository + Issue`; exact resume bindings are recovered instead. Inspect any existing matching old-run automation under the migration rule. |
| Gates | Accepted validation, normal closeout and explicit completion overrides are concrete. |
| Effects/endpoint | Exact prospective app and Git/GitHub effects, including any environment provisioning, fit the current human endpoint and delegation. |
| Environment | Current supported creation/UI capabilities, permissions, actual trust and necessary setup are known per repository. Missing conditions use Environment Readiness below; directory creation alone does not pass. |

Inspect actual context behind a title or preview before asserting duplicate
ownership. A different graph/order can still overlap; an unrelated active Task
is not a conflict. Existing incomplete closeout or archived Task identity stays
with its original repository owner. Do not create replacement identities.

Accepted Issue scope determines required results. Repository instructions and
stage owners determine valid execution and gates. Live PR/check/remote state
supplies facts. None of these replaces the current human's execution boundary.
A newer Issue comment does not automatically waive repository rules. Resolve
real contradictions from their original sources; ask only an unresolved real
product or authority choice.

On resume, legitimate prior work may have changed the base or dirtied child
worktrees. Do not rerun initial clean/equal-OID requirements against an active
run. Recover exact owners, candidate/base identities, current remote state and
the applicability of existing gate results. Apply the target workflow's actual
integration conditions through the original stage owner.

The AI reviews scope, completeness, dependencies, isolation, tool capability,
current human boundary and truthful evidence before entering live execution.
For `dry-run`, return its one ready/blocked exit and stop. Auto/live enter
execution only for covered ready nodes. A repository-local environment gap uses
the selected package’s failure rules; a whole-run gap holds all dependent work.
An intermediate preflight is not a second final exit.

## Environment Readiness

Inspect the current native tool schemas and supported App UI before declaring
that a missing environment can or cannot be created. Check the target repository,
local checkout/remote, saved project and primary folder, permissions, selected
base/source, app trust requirements and actual execution prerequisites. Do not
infer capability from an old tool list or treat a cloud/LaTeX project operation
or a projectless chat as local repository-project registration.

Dry-run only reports these facts, supported actions and remaining conditions.
It creates no checkout, project, setup, child or automation. In live execution,
show exact repositories, paths, project changes, source/base and necessary
setup effects. Consume the current action boundary; when it already covers
these effects, do not ask again. Otherwise obtain only the missing action choice.

When a supported entry and permissions exist, establish the missing prerequisite
through that entry. A checkout may be cloned from its verified remote into a
nonexistent intended path; never overwrite existing local work. Register or edit
a local App project only through its actual supported tool or UI. Afterwards,
reread the saved project and its primary folder, Git remote, selected local/
tracking/live base and checkout suitability. Correct repository binding is a
separate condition from creation success. Preserve existing project folders,
settings and unrelated work.

App trust is a user review boundary. If the App requires project, prompt or
hooks trust, tell the user the exact target and displayed review action and
hold this environment until the user completes it. Never edit private App
state or trust configuration, or click a trust confirmation for the user.
A successfully created directory/project does not establish trust. Use actual
App evidence or the user’s completed review; do not invent a trust API or require
an unavailable status field when the supported UI is the source of that fact.

Setup serves actual missing execution prerequisites, such as required dependencies
or untracked runtime files in new worktrees. Inspect existing local-environment
settings and target-repository instructions first. Configure only what those
facts require, through a supported entry and its ordinary action boundary.
Do not require new hooks/scripts or an environment file for every repository.

If no supported creation entry or permission is available, name the exact
repository, missing prerequisite and responsible party. Give concrete current
user steps: obtain its checkout when absent; add/edit that local project in
Codex; verify the repository folder is primary; review any App-displayed trust
request; and use local-environment setup settings only for actual prerequisites.
Adapt these steps to the current UI/tool help or official Projects and Local
environments documentation rather than inventing buttons. State what to reread
before resume. In the blocked response, give each affected repository’s exact
checkout path/remote and actionable user steps, including the supported local
project/primary-folder action and displayed trust review when applicable. These
steps are the user’s direct means to resolve the reported gap.
An unsupported generic project-registration API is a present
capability gap, not a permanent prohibition on supported UI creation.

Retain this environment block with its affected nodes and descendants in the
same conversation. DAG `continue_independent` may progress other ready nodes;
`stop_dispatch` stops new admissions. Sequence holds its current position.
Observe admitted children to safe boundaries; do not discard their owners.
When no permitted work remains, use normal terminal-block settlement, including any old-run timer stop, with the exact missing condition. Once the condition changes,
reread project/primary remote/base/trust and affected dependencies, then resume
the same run and existing children. Unadmitted nodes receive their first child;
environment recovery never creates replacement owners or reapplies initial
clean/equal checks to already active worktrees.

Official documentation locators: [Projects](https://learn.chatgpt.com/docs/projects)
(primary folder controls Git/worktree operations) and
[Local environments](https://learn.chatgpt.com/docs/environments/local-environment)
(setup for new worktrees). Read the current applicable documentation when the
actual capability or UI requires clarification; these links do not prove runtime
availability.

## Native Children And Async Ownership

Use current native Codex tools. Separate user-visible Issue chats are intended
execution carriers, rather than in-turn implementation subagents. Resolve the
node’s saved project and primary repository afresh. Create each child with `target.type=project`, its actual
`projectId`, and `environment.type=worktree`. Start from the selected base
unless the human explicitly requested a separate starting state. The original
repository owners must verify that such a state fits the selected target and
current dependencies; preserve both identities and resolve an actual conflict
through those owners. A valid separate source never changes the PR target.

Pass an explicit existing source branch/ref through the tool's supported
starting-state parameter, such as branch `dev`; a prompt alone does not select
the worktree source. Preserve an explicitly requested working-tree source under
the same suitability and unrelated-change rules. Omit the override only when
the tool's actual default matches the resolved source. If the capability cannot
express that source, hold creation and report the specific gap rather than
creating from another branch. The child's workflow establishes formal Task and
branch binding. Do not invent a ref from an Issue title.

Before each creation, inspect existing active/pending owners. Bind one logical
creation to repository, current run, Issue and requested settings, plus the
sequence position when applicable. A formal `threadId` and `hostId` identify
the child. `clientThreadId`, pending, missing formal ID or an unknown outcome
reserves that Issue and its package-defined slot. Never pass a client ID where
a formal ID is required or repeat creation while its result is unresolved.

Recover the exact operation through app-returned identities and actual chat
context. Titles alone cannot bind it. A verified failed creation with no owning
child may retry the same Issue after its cause is corrected. Ambiguous ownership
stops affected dispatch. Immediately observe each newly formal child with
`wait_threads` and `timeoutMs: 0`, including after pending resolution. Preserve
its returned cursor for later waits. Emit the app-required created-chat directive
for each newly created chat.

### Minimal Child Prompt

Project only execution inputs into the child:

```text
Repository: <owner/repo>
Issue: #<number>
Selected base: <remote>/<branch> (PR and completion target)
Starting state: <actual source, only if separately specified>
Synchronization condition: <the user's exact condition, when supplied>
Confirmed facts: <relevant live facts already checked, when available>
Coordinator: <current formal chat identity>
Position/prerequisites: <only this child's sequence position or repository-qualified prerequisite refs>
Completion overrides: <only this Issue's additional accepted gates>
Current execution segment: <work to do, then where to stop and report>

Use this repository's complete current Trellis workflow. Read live Issue body,
accepted comments, linked delivery, AGENTS.md, workflow and relevant specs.
Read the installed clear-technical-writing.md in full where required. Recover
existing Task/Delivery identity through its original owner. Use this dedicated
worktree and independent branch binding. Verify required predecessor results
before implementation. Apply the user's synchronization condition through
the target workflow's original stage owner. Keep PRs and merge proof on the
selected target.

Own only this Issue. Preserve other agents' changes, resources and evidence.
Do not write shared journals or unrelated Task metadata. Stop at the specified
execution boundary even when later phases are available. Always stop for a
coordinator disposition before merge. Report other precise side-effect plans
under the repository workflow; do not infer permission from this prompt.

When stopping, state the current phase, actual completed gates, exact next
operation and targets, prerequisites and recommendation. Report workflow
errors with the original owner's supported recovery. Keep acceptance, truthful
validation, semantic review, readiness, whole-Task and release gates. Do not
start other Issues or message other chats.
```

Do not copy human approval text/status/provenance or large historical evidence
into the prompt. Child-local implementation/check delegation stays with its
repository workflow. The coordinator never implements the Issue itself.

Project prerequisites according to the selected package's dependency kinds.
For a DAG contract-only prerequisite, include its provider, live contract
locator, consuming work and any precise current hold; the DAG package owns
readiness and Mock-development scheduling. Do not turn that input into a
full-provider-completion wait. Sequence retains its strict complete-before-next
rule; this projection adds no alternative scheduling mode to it.

## Native Waiting And Observation

Apply [Quiet Notifications](#quiet-notifications) throughout the run. The
coordinator stays active in this conversation and uses native child observation
and event waits to supervise the selected work. Do not create, restart or update
an automation to track these Issues to a milestone, failure or completion.
A timer is not a launch prerequisite or proof of supervision. Native project,
chat, message, wait and live-read capabilities remain required; an unavailable
required capability retains its concrete preflight or recovery gap.

Immediately snapshot each newly formal child with `wait_threads` and
`timeoutMs: 0`. Before a multi-child disposition, obtain current coverage of
all admitted unfinished children without blocking one behind another. DAG may
reuse native batch coverage; Sequence takes a snapshot. Preserve each child's
formal identity, `hostId` and returned cursor in this conversation. For later
observation, use a bounded native event wait with the current cursors, at most
60 seconds per call, within the tool's actual supported limits. When an event
arrives or the wait times out, apply the observation steps below. DAG applies
its local `DAG Observation` profile to coverage, result reads and condition
checks. Sequence performs the complete cycle and rechecks current facts on
timeout. A timeout does not prove failure or completion.
Do not substitute a two-second polling loop, shell scheduler, watchdog or new
persistent coordination store.

Every cycle:

1. Resolve pending creations and observe every formal unfinished child. Respect
   the native target limit and rotate batches fairly; one busy child, merge or
   repair must not starve siblings.
2. Preserve each returned cursor. One returned event does not prove all targets
   were observed; obtain snapshots for uncovered targets.
3. Read the newest actual assistant output when changed, idle or terminal and
   the wait result did not provide it. Summaries, previews and status labels
   are discovery hints.
4. Judge all remaining obligations. For a DAG action that requires human
   confirmation, apply [Confirmation While Independent Work Remains](#confirmation-while-independent-work-remains).
   Give each actionable idle child one useful valid continuation within
   current execution limits. Recheck actual
   external wait conditions even without new text. Follow the chosen action
   to its result; a sent instruction does not resolve the obligation.
5. Verify candidate stage/completion results, apply package scheduling and fill
   eligible slots. Retain an observation error and retry that same binding;
   never claim healthy supervision for an unobserved child.

Stay in this loop while permitted work or an owned bounded wait remains. Do
not end the active turn with `auto_started` or `progressing` merely to wait for
an automation, another child message or a human reminder. Those existing exits
remain concise conversation results for their original next-observation
consumer when a native interruption or necessary handback ends execution; they
are not terminal success and do not remove continuation responsibility. Native
created-chat directives retain their own reporting contract.

### Conversation Recovery Inputs

Qualify each node, pending reservation, child/host/cursor, Task/Delivery and PR
with its repository. Keep the selected run inputs, current sequence position,
consumed events, pending operations and each repository's integration owner in
this conversation. After admission or a carrier change, reconcile these facts
with the actual native result before continuing. No checkpoint, ledger,
authorization record or automation prompt is introduced.

On resume, recover original messages and existing formal or pending owners,
then recheck live child facts. A stale summary does not retake ownership, roll
back the sequence position or permit duplicate creation. A lost cursor requires
a fresh snapshot of the same child; an unknown send or mutation outcome first
requires exact-operation recovery.

### Observation After An Interruption

On every resumed execution, first observe all admitted unfinished children.
For DAG, read decision-relevant results or recover any missing result. For
Sequence, read changed or idle results. Act on each actionable idle child in this cycle
under its current gates. Do not wait for another timer or human reminder.

Compare the current time with the last actual observation available in this
conversation or native history. Preserve any gap as unobserved time. If the
previous observation is unavailable, state that limit. Do not claim background
supervision while this coordinator was stopped, interrupted, or not executing.
An idle child or elapsed interval alone proves no native scheduler fault.

Perform one current catch-up cycle. Preserve owners and unknown-operation
recovery; do not replay an instruction for each missed interval, restart from
a fresh base, or relax a gate to compensate for delay. The same observation,
active-unblocking and quiet-output rules then resume.

### Migration From Timer-Based Supervision

This contract directly replaces mandatory two-minute automation heartbeat with
current-conversation native waits. Skill ids, graph/chain inputs, scheduling,
stable exit ids and their consumers remain. `auto_started` now hands the next
observation consumer the verified initial child bindings and observation
condition, rather than a heartbeat identity. Terminal outputs prove safe child
and operation settlement, rather than requiring a timer that was never created.
Apply the complete matching provider through the existing installation owner;
do not combine old timer instructions with these packages.

For a resumed old run, inspect any already existing matching heartbeat only to
recover its original identities and stop it through the supported native owner.
Verify the stop without recreating or reactivating it. An unknown stop result
requires recovery of that operation. A stop failure retains the precise
settlement gap; known children still receive permitted observation and
continuation. It does not justify a replacement timer or duplicate child.
After verified stop, keep observing the same run through native waits.

## Quiet Notifications

Both orchestrators operate quietly by default. During active supervision,
continue tool observation and original-owner actions without routine commentary
or a progress-only final response. Phase changes, PR publication or merge,
individual Issue completion, successor admission, supported retry and an
unchanged valid wait do not themselves require a human notification. No
heartbeat XML envelope or invented notification API is used.

Notify the human when a real choice, missing action permission or expressly
direct-human step is required; when active unblocking establishes an unresolved
condition needing human action; or when the whole selected run reaches a
verified terminal result. Give the exact affected work, action or minimum
condition. Deduplicate an unchanged request while preserving observations and
useful continuations. A necessary human handback retains the remaining work
and exact resume condition; it is not a completion claim. For DAG confirmations, apply
[Confirmation While Independent Work Remains](#confirmation-while-independent-work-remains).

Show the initial precise prospective effects and necessary setup choices under
preflight. Answer an explicit status question directly, then continue permitted
supervision. Follow higher-priority host requirements for progress reporting;
quiet operation does not suppress a required human interaction or excuse an
observation gap. Do not create an automation or custom delivery mechanism to
silence routine progress.

## Progress Decision

### Overall Responsibility And Active Unblocking

Keep full Issue completion and all remaining accepted obligations in view until
completion, an explicit human stop boundary, or a genuinely unresolved block.
An explicit earlier-stage boundary may settle only that segment. A stage result
or a missing permission never removes the unfinished Issue obligations. Sending
an instruction, observing one turn, a child ending, or one Delivery merging does
not discharge that responsibility. Keep lightweight conversation context about
the actual gap, its owner and the next result to observe; create no coordinator
ledger or additional gate artifact.

When a child reports blocked, failure, no recommendation, or completion without
sufficient proof, first identify the unmet requirement and affected work from
current facts. A child statement is evidence to examine, not the coordinator's
conclusion. Distinguish a failed step from a node obstacle, a valid external
wait and a whole-run block. Check relevant inputs, paths, prerequisites, current
supported entries, available capabilities and the original owner's actual
result. The absence of a recommendation does not establish that no route exists.
Follow a concrete supported investigation direction when the facts provide one.

Choose useful action for that gap: remind the owner of a missed obligation,
inspect facts, research the relevant capability, discuss alternatives with the
owner, coordinate an available resource, challenge unsupported claims, or use
the applicable independent review. Require the original owner to correct its
implementation, finding, gate or closeout result when needed. These are tools
for judgment, not a fixed sequence of questions or approvals on every cycle.
Smooth progress needs only its normal observation and endpoint verification.
Do not implement the Issue yourself or fill in another owner's formal pass.

After a disposition, observe its actual execution and result, compare that
result with the gap, and decide the next supported action. A sent suggestion,
accepted recommendation or investigation request is not evidence that the
obstacle is resolved. Continue while an in-scope direction has a factual basis.
Do not repeat a failed configuration without a changed premise, experiment
indefinitely, or reopen satisfied gates without a relevant change. Preserve
real human stop conditions and all existing side-effect boundaries.

### External Waits

A valid wait names a responsible owner, the actual operation or missing
condition, and a bounded recheck condition. Inspect the underlying status or
evidence on subsequent observations; child text need not change. An operation
ending, timeout, absent responsible owner, or invalidated recheck condition
requires a new progress decision, including after failure. Do not carry a
stale waiting label forward or treat silence as proof that a wait remains valid.
When the condition changes, pursue the now-valid action and observe its result.
For an unchanged valid wait, keep the existing owner and stay quiet after the
check. Genuine missing external conditions use the terminal-block test below
when no permitted work remains; they do not justify an ownerless endless wait.

### Current Disposition

The coordinator judges the latest real child message, last relevant instruction,
workflow phase, Issue scope, actual current gates and human boundary. When
several conditions apply, choose the earliest unmet prerequisite. A child need
not request fixed wording before receiving a useful next instruction.

| Evidence | Disposition |
| --- | --- |
| Requested earlier stage is reached | Verify its original-owner result and safe inactive disposition; apply package stage rules without advancing further. |
| Phase finished and completion obligations remain | Send the next valid mapped phase instruction within current execution limits; resolve only the missing action permission when necessary. |
| One precise current in-scope operation has passing prerequisites | Send `确认继续` if that is the target workflow's signal, only for that action. |
| One unique current safe recommendation fits scope | Evaluate consequences and adopt it, for example `按建议方案执行`; unresolved real choices return to the human. |
| Delegated merge passes the fresh merge gate | Send `合并PR` for the selected integration owner, subject to direct-human exceptions. |
| Missing, stale or failed gate has an in-scope route | Request original-owner refresh, finding repair and affected re-review; never send generic approval. |
| Block, failure, absent recommendation or insufficient claim | Apply active unblocking above; inspect and challenge the actual gap, then follow the selected owner action to its result. |
| Next mutation is unclear | Inspect or request scoped read-only investigation of the concrete uncertainty and its prerequisites. |
| Supported workflow recovery exists | Select its original-owner route below and verify its result. |
| CI or another required operation is genuinely running | Keep one bounded wait with exact operation, owner and recheck condition. |
| Owned wait changes, ends, expires or loses its owner | Reevaluate the actual condition and remaining gap, then take the supported action without waiting for new child text. |
| Local completion is reported | Verify the requested endpoint; request any missing applicable closeout, release or evidence. |
| Unblocking has established no supported in-scope continuation | Apply the terminal-block test and selected package's failure/settlement rules. |

Before messaging, verify the formal destination, inactive relevant turn, current
evidence and actual human messaging delegation. Do not broadcast a generic
approval. Deduplicate by child, turn/message, live gate state and the last
instruction's expected result. A wait timeout alone creates no new event.
A material prerequisite change does. Never use a coordinator message as a
substitute for a direct-human confirmation expressly required by the repository.

For a newly observed temporary capacity/overload event, including the tool's
current 429 retry-limit or model-at-capacity messages, preserve the same child,
Task, worktree, branch, model and reasoning. Within continuation scope, send
exactly `确认继续` once for that error event. If a new attempt fails likewise,
retry after the next bounded wait and observation; no repeat within one cycle, model switch or replacement
child. Actual exhausted quota, missing credentials and unsupported models retain
their concrete blocker. Other admitted DAG children still receive observation.

## Fresh Merge Gate And Integration

For each repository, choose one integration owner among its ready children in
package order. Keep the global execution slot limit and actual cross-repository
dependencies/resource constraints. Independent repositories can integrate under
their own passing gates while another repository’s result remains pending.
First
recover whether merge is inside this run's current human delegation. Then
freshly read that node’s exact repository/PR, target branch, current head and reviewed
candidate; current selected-base head, mergeability and merge policy; required
checks/reviews at that candidate with no unresolved required finding; truthful
PR title/body, closure intent, validation and deployment/release claims; and
the exact current operation displayed by the child. Verify that the PR targets
the selected base. Read the default branch only where actual closure or release
rules require it; do not add another branch's freshness as a merge gate.

When delegation and these gates pass, send `合并PR` without a repeated human
confirmation for each node. A child request alone proves neither. Preserve the
original Merge Skill, semantic confirmation gate, expected-head transaction and
any explicit direct-human-only exception. `auto` and a previous `确认继续`
neither establish merge scope nor waive readiness.

After a same-repository sibling merge, verify the repository, target and
actual merge facts. When dispatching to a waiting child, pass the user's
synchronization condition verbatim and relay only the facts already checked.
Keep requests to watch for a merge or to synchronize if needed conditional.
Have the original stage owner continue its step and apply the target
workflow's actual integration conditions. A merge notice, changed target SHA
or overlapping paths alone give no instruction to reconcile or refresh
still-applicable gate results.

Retain that repository’s integration owner until its live result and
immediately required shared-base closeout have known dispositions. Do not
send another merge in that repository while its original transaction is
unresolved. Keep observing
and advancing other independent repositories; a pending result does not create
a dependency or shared resource constraint between them.
Recover original transaction and GitHub state after lost results; do not repeat
remote mutation on an uncertain response. Then re-read the next owner’s own repository/base. A merge in a different
repository does not advance or prove this node’s base; refresh only actually
affected shared prerequisites and gates. A supported auto-merge/queue still needs its current original gates.
An Issue's release/Task closeout may remain pending after its integration turn
ends; package execution-slot rules remain separate.

## Stage And Full Completion Proof

For a human-requested earlier stage, verify that original owner's current
result, candidate, target and applicable checks. Draft PR publication, reviewed
Ready PR and merged Delivery differ. Preserve actual unfinished Issue/Task
work. Stage proof never satisfies a hard full-completion dependency. Each
package owns whether that stage permits another child or a terminal result.

Full Issue completion requires fresh proof of every applicable item:

1. The Issue is closed with the intended completed resolution. Duplicate,
   superseded or not-planned closure does not prove delivery.
2. All PRs required to deliver its scope are merged. Identify the reviewed
   candidate and the platform's actual merge result.
3. The actual merge result is reachable from the live selected base. For
   squash/rebase, verify the resulting commits and candidate association;
   do not require ancestry of the former feature HEAD. A run targeting `dev`
   does not also require delivery to `main` unless accepted Issue scope says so.
   Issue closure still uses the repository's original Closure owner; do not
   assume GitHub auto-closes an Issue for a non-default-branch merge.
4. The repository's semantic Check, full-range Review, readiness and whole-Task
   completion pass under their current contracts. A merged Delivery is not
   whole-Task completion.
5. Validation evidence names what ran and its result. Skipped/unavailable tests
   remain explicit limits. Accepted docs/SSOT, Architecture and installation or
   platform projections have been covered where applicable.
6. Required closure/archive/resource work is complete or has a repository-valid
   nonblocking disposition. Never clean another node's resources incidentally.
7. Every accepted per-Issue completion override passes.

Bind each proof to the node’s canonical repository/Issue, exact Task/Delivery,
PR and selected base. A same-number Issue or successful merge in another
repository is no evidence for this node.
Use live GitHub and remote Git reads. During dry-run, use read-only compare or
commit APIs if local objects cannot prove ancestry without fetch; report an
actual proof gap if neither source suffices. Authorized execution may synchronize
only through its original repository owner.

Release scope additionally requires the exact version/tag and peeled commit,
published non-draft Release with the accepted prerelease policy, corresponding
packages/assets/checksums and required published-version smoke. Deployments or
downstream upgrades gate only the accepted scope that requires them. Ordinary
Issues do not inherit a separate release/installer matrix.

## Supported Workflow Recovery

Diagnose from actual errors and live state before reporting a terminal block.
A coordinator's invented endpoint is an interpretation error, not a Merge
transaction failure. Recover the current human source and correct the reading.

Use the current original owner's supported route: underlying entry for an
unavailable overlay, original-producer refresh for stale evidence, semantic
applicability assessment for a mismatched gate, existing transaction recovery
for a lost mutation result, or an explicitly supported equivalent for a broken
recorder/validator/executor. A manual equivalent must preserve the exact current
action and prove equivalent pre/postconditions under repository rules.

An unknown side-effect result first requires recovery of that exact operation;
never repeat it merely to obtain a clearer response. Once facts establish that
an earlier transaction failed and cannot be recovered, preserve that failure
and the same Issue/Task/Delivery identity. That transaction's end alone does not
prove the Issue cannot continue. Ask the original owner to assess whether a
supported subsequent operation can meet the remaining requirement, for example
after correcting an ordinary input, path or prerequisite error. Verify that
operation's own preconditions and result. This is not permission to replay an
uncertain mutation, erase the failed transaction, bypass its stop condition or
create replacement identities.

Do not waive fail-closed rules, edit artifacts to manufacture acceptance,
suppress test failures, invent semantic pass, or substitute direct evidence
where the original contract requires its unavailable producer. A required
producer with no supported equivalent remains a concrete gap; direct evidence
cannot substitute for it. Use the terminal-block test below after assessing
the remaining work. Do not detour into repairing Guru Trellis or filing
a defect Issue unless that work is explicitly in scope.

If the chat carrier cannot continue, use an app-supported same-directory
continuation/fork only within current instructions. Preserve Issue, Task/Delivery,
worktree, branch, PR, findings and gates. Verify the old carrier is inactive and
the new formal carrier owns that same state before replacing the binding and
immediately observing it. This changes a carrier, not Issue ownership or slot
count. Do not restart from a fresh base or create parallel owners. Temporary
capacity errors use same-child retry instead.

Handle normal async creation, base movement, stale/mismatch and expressly
supported transaction recovery. Do not add adversarial artifact cases, stress
locks, crash protocols or fault-injection mechanisms.

## Settlement And Resume

Before a terminal blocked exit, establish through the active-unblocking method
that the requested endpoint is unmet and no permitted in-scope work can advance.
Report the specific target gap, supported directions actually checked and why
they cannot continue, the minimum missing condition and responsible party or
real human choice, the resume condition, and affected nodes. Preserve completed
results and validation limits. This requires a reasoned judgment from relevant
facts, not exhaustive theoretical options or a child's unsupported assertion.
Apply the package's failure policy to unaffected work before whole-run settlement.

A terminal result requires no pending creation or unresolved operation and all
admitted children inactive at verified safe boundaries. Any matching timer from
an old run must have a verified stopped disposition under the migration rule.
Do not blindly interrupt a merge. If safe disposition or an old timer stop
remains unproven, retain `progressing` with that exact incomplete settlement
and recover it while continuing permitted observations.

Use a stage-completed exit only under the selected package's declared stage
conditions. State unfinished Issue/Task work without inventing a merge blocker.
A genuine blocked exit requires the terminal-block judgment above. Completed
exits require full proof.
Do not archive chats, remove worktrees or perform other incidental cleanup.

Resume the same run after its concrete blocker is resolved or the human resumes
a limited segment. Recover children, the selected base and unfinished completion
obligations, revalidate affected proofs and resume native observation of those same owners.
No new Task or fresh-base restart. Membership, dependency, completion-gate or resource changes
need fresh semantic impact review and only their real human choices. Do not
persist authorization during recovery.
