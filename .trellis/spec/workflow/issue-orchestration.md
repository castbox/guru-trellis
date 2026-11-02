# Issue Orchestration Method

This is the shared semantic contract for `guru-orchestrate-issue-dag` and
`guru-orchestrate-issue-sequence`. Their package-local contracts own scheduling,
serial advancement, and typed exits. This method owns endpoint interpretation,
current-dialogue authority, native child operation, progress decisions, merge
proof, completion proof, heartbeat supervision, and supported recovery.

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

The target business repository may be elsewhere. It supplies its own current
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

Before the first child or heartbeat is created, read the actual human messages
for this run in the coordinator conversation. Resolve the requested endpoint:
full Issue completion under the completion proof below, or an explicitly
requested earlier stage such as planning or reviewed PR publication. Resolve
whether the actions needed to reach it, including merge where applicable,
are delegated. Use the human's meaning, not a required phrase or an assistant
plan. `auto` continues after preflight within this scope; it neither selects
an endpoint nor grants unlimited merge permission.

After read-only preflight, show precise prospective effects. If current human
instructions already cover them, start directly without another launch question.
If the endpoint or a necessary action boundary remains unresolved, ask only
the real choice that resolves it, before child or heartbeat creation. Return
`dry_run_blocked` until that choice is resolved. Do not silently select PR
readiness or defer a missing merge decision until every PR is ready.

Only this run's actual human instructions establish or change its endpoint and
delegated scope. Assistant plans or scope statements, child requests, summaries,
heartbeat configuration, and another run's permission cannot independently
authorize or restrict this run. A scheduler wakeup is automation input even
when delivered as `role=user`. These sources may locate relevant conversation;
read the original human text before relying on it.

At each observation cycle, use still-current human instructions already read
in this conversation. After context loss, changed scope, or uncertain summaries,
recover the necessary original messages and distinguish automated wakeups. If
recovery is impossible or ambiguous, hold only the affected mutations and
report the missing source or choice. Do not ask the human to repeat an already
recoverable current delegation. Keep permitted inspection and bounded work moving.

Keep execution authorization, the human's endpoint choice, and their origin
and process in the current conversation only. Never serialize them as permission
or approval records in public inputs/outputs, schemas, checkpoints, journals,
archive, child prompts, or heartbeat configuration. Ordinary operation inputs
such as model settings or accepted gates remain usable, and the conversation
result may state the actual stage reached and remaining work. A child's minimal
operational work segment and stop-before instruction do not record or prove
permission. Send a later concrete instruction such as `合并PR`
within actual delegation without attaching “the user already authorized this.”
Repository rules expressly requiring direct human confirmation still apply.

## Public Inputs And Model Settings

Each package owns its concise conversation input contract. Resolve one exact
repository, saved local project, and selected Issue identities. Do not put the
endpoint or authorization in a normalized data object; resolve those from the
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
| Provider/tools | Same-provider package and shared method; current native project, chat, message, wait, heartbeat and live-read capabilities. |
| Repository/project | Authenticated exact `owner/repo`; one current saved project matching its path and repository remote. |
| Initial base | Live default branch is known; local default, local tracking ref and remote default OIDs agree. Report all three without fetching. |
| Initial checkout | Clean and suitable for the target repository's normal intake; no unrelated work is reset or moved. |
| Issues | Selected identities are accessible and open initially, with sufficient current scope and completion criteria. Explicit resume can adopt completed nodes only after fresh full proof. |
| Dependencies | Package scheduling rules and live hard prerequisites are compatible with the requested endpoint. |
| Existing owners | No competing coordinator, heartbeat, pending creation, child or Task for a selected `repository + Issue`; exact resume bindings are recovered instead. |
| Gates | Accepted validation, normal closeout and explicit completion overrides are concrete. |
| Effects/endpoint | Exact prospective app and Git/GitHub effects fit the current human endpoint and delegation. |

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
affected gate freshness. Reconcile through original repository owners.

The AI reviews scope, completeness, dependencies, isolation, tool capability,
current human boundary and truthful evidence before entering live execution.
For `dry-run`, return its one ready/blocked exit and stop. Auto/live enter
execution only when ready and covered; an intermediate preflight is not a
second final exit.

## Native Children And Async Ownership

Use current native Codex tools. Separate user-visible Issue chats are intended
execution carriers, rather than in-turn implementation subagents. Resolve the
saved project afresh. Create each child with `target.type=project`, its actual
`projectId`, and `environment.type=worktree`. Start from the project default
branch unless the human explicitly chose another starting state. The child's
workflow establishes formal Task and branch binding. Do not invent a ref from
an Issue title.

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
Coordinator: <current formal chat identity>
Position/prerequisites: <only this child's sequence position or prerequisite refs>
Completion overrides: <only this Issue's additional accepted gates>
Current execution segment: <work to do, then where to stop and report>

Use this repository's complete current Trellis workflow. Read live Issue body,
accepted comments, linked delivery, AGENTS.md, workflow and relevant specs.
Read the installed clear-technical-writing.md in full where required. Recover
existing Task/Delivery identity through its original owner. Use this dedicated
worktree and independent branch binding; reconcile the current default branch
and verify predecessor results before implementation.

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

## Heartbeat And Observation

Use one native thread heartbeat attached to the current coordinator. Inspect
existing automations and reuse the matching heartbeat on resume. **The default
heartbeat interval is two minutes.** Apply another current human-selected
interval only when the native tool supports it. Inspect the current schedule
contract and use its supported representation; do not invent a secondly rule,
raw automation directive, cron fallback, or shell scheduler. A missing scheduling
capability blocks live launch before children are dispatched. After creation
or update, read back the actual heartbeat and verify the interval is two minutes,
or the currently selected supported value, and that it targets this coordinator.
A failed write or mismatched configuration blocks dispatch until corrected;
a requested setting or successful-looking card alone is not verification.

A heartbeat interval is independent of child wait timeouts. Preserve immediate
zero-timeout snapshots after binding and before multi-child disposition. Later
bounded native waits may use their supported event-wait behavior and cursors;
do not replace the two-minute heartbeat with a two-second polling loop.

The heartbeat prompt identifies the managed Skill/provider, normalized Issue
selection/dependencies, project, concurrency/resources, selected model settings,
failure policy and accepted completion gates. It contains no selected endpoint
or authorization record. Include this supervision instruction:

```text
Resume this same Issue run as its AI coordinator. Load the selected managed
Skill, its local contract and the shared issue-orchestration.md from the same
provider. Recover this run's endpoint from original human messages in this chat.
Observe every admitted unfinished Issue chat and read its newest real assistant
output when changed or idle. Judge the actual phase, recommendation, blockers
and fresh gates. Give each actionable idle child below the endpoint one useful
continuation in this cycle. Use 确认继续, 按建议方案执行 or 合并PR only when
their current conditions pass; otherwise request precise remediation, inspection
or supported owner recovery. Recheck owned external waits and deduplicate
unchanged events. Apply this Skill's scheduling and advancement rules. Stay
quiet while work or a handled wait is unchanged. Stop the heartbeat only after
a verified settled outcome.
```

Keep bindings, pending operations, cursors, consumed events and the integration
owner in conversation context. App-owned configuration carries only minimum
replayable run inputs. No new persistent coordination or authorization store.
After context loss, recover original identities and live facts before dispatch.

Every wake performs one complete observation cycle:

1. Resolve pending creations and observe every formal unfinished child. For a
   multi-child run start with nonblocking snapshots, so one busy child cannot
   starve siblings. Respect the tool target limit and rotate batches fairly.
2. Preserve each child's `hostId` and cursor. One returned event does not prove
   other targets were observed; obtain snapshots for any uncovered targets.
3. Read newest actual assistant output when changed or terminal and the wait
   result did not provide it. Summaries, previews and status labels are hints.
4. Apply the progress decision below to every actionable idle child within the
   endpoint. Recheck external waits against live facts even without new text.
5. Verify candidate stage/completion results, apply package scheduling and fill
   eligible slots. State an observation error and retry that same binding;
   never advertise healthy monitoring for an unobserved child.

A failed gate changes the requested remedy; it does not justify abandoning an
idle incomplete child. `ACTIVE` configuration alone proves no observation.
An unknown send result requires reading the child's actual conversation before
retry; do not duplicate a possibly delivered instruction. Stay quiet only after
successful observation of running work, an already-handled unchanged event, or
an unchanged owned bounded wait.

## Progress Decision

The coordinator judges the latest real child message, last relevant instruction,
workflow phase, Issue scope, actual current gates and human boundary. When
several conditions apply, choose the earliest unmet prerequisite. A child need
not request fixed wording before receiving a useful next instruction.

| Evidence | Disposition |
| --- | --- |
| Requested earlier stage is reached | Verify its original-owner result and safe inactive disposition; apply package stage rules without advancing further. |
| Phase finished below the endpoint | Send the next valid mapped phase instruction. |
| One precise current in-scope operation has passing prerequisites | Send `确认继续` if that is the target workflow's signal, only for that action. |
| One unique current safe recommendation fits scope | Evaluate consequences and adopt it, for example `按建议方案执行`; unresolved real choices return to the human. |
| Delegated merge passes the fresh merge gate | Send `合并PR` for the selected integration owner, subject to direct-human exceptions. |
| Missing, stale or failed gate has an in-scope route | Request original-owner refresh, finding repair and affected re-review; never send generic approval. |
| Next mutation is unclear | Request read-only inspection and one precise next action with prerequisites. |
| Supported workflow recovery exists | Select its original-owner route below and verify its result. |
| CI or another required operation is genuinely running | Keep one bounded wait with exact operation, owner and recheck condition. |
| Owned wait changes | Reevaluate the latest actual output with the new live facts, then send the valid next action without waiting for new child text. |
| Local completion is reported | Verify the requested endpoint; request any missing applicable closeout, release or evidence. |
| Genuine unresolved prerequisite or permission has no supported route | Report the concrete block and apply the selected package's failure/settlement rules. |

Before messaging, verify the formal destination, inactive relevant turn, current
evidence and actual human messaging delegation. Do not broadcast a generic
approval. Deduplicate by child, turn/message, live gate state and the last
instruction's expected result. A new heartbeat alone creates no new event.
A material prerequisite change does. Never use a coordinator message as a
substitute for a direct-human confirmation expressly required by the repository.

For a newly observed temporary capacity/overload event, including the tool's
current 429 retry-limit or model-at-capacity messages, preserve the same child,
Task, worktree, branch, model and reasoning. Within continuation scope, send
exactly `确认继续` once for that error event. If a new attempt fails likewise,
retry on the next heartbeat; no repeat within one wake, model switch or replacement
child. Actual exhausted quota, missing credentials and unsupported models retain
their concrete blocker. Other admitted DAG children still receive observation.

## Fresh Merge Gate And Integration

Choose one integration owner among ready children in package order. First
recover whether merge is inside this run's current human delegation. Then
freshly read the exact repository/PR, target branch, current head and reviewed
candidate; current default branch, mergeability and merge policy; required
checks/reviews at that candidate with no unresolved required finding; truthful
PR title/body, closure intent, validation and deployment/release claims; and
the exact current operation displayed by the child.

When delegation and these gates pass, send `合并PR` without a repeated human
confirmation for each node. A child request alone proves neither. Preserve the
original Merge Skill, semantic confirmation gate, expected-head transaction and
any explicit direct-human-only exception. `auto` and a previous `确认继续`
neither establish merge scope nor waive readiness.

After a sibling merge, reconcile the evolved base and refresh affected gates
through the waiting child's normal owners. Keep one integration owner until
its live result and immediately required shared-base closeout have known
dispositions. Do not send a second merge while that transaction is unresolved.
Recover original transaction and GitHub state after lost results; do not repeat
remote mutation on an uncertain response. Then re-read the base for the next
owner. A supported auto-merge/queue still needs its current original gates.
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
3. The actual merge result is reachable from the live default branch. For
   squash/rebase, verify the resulting commits and candidate association;
   do not require ancestry of the former feature HEAD.
4. The repository's semantic Check, full-range Review, readiness and whole-Task
   completion pass under their current contracts. A merged Delivery is not
   whole-Task completion.
5. Validation evidence names what ran and its result. Skipped/unavailable tests
   remain explicit limits. Accepted docs/SSOT, Architecture and installation or
   platform projections have been covered where applicable.
6. Required closure/archive/resource work is complete or has a repository-valid
   nonblocking disposition. Never clean another node's resources incidentally.
7. Every accepted per-Issue completion override passes.

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

Do not waive fail-closed rules, edit artifacts to manufacture acceptance,
suppress test failures, invent semantic pass, or substitute direct evidence
where the original contract requires its unavailable producer. If no supported
route proves the same claim, report the precise missing evidence/authority and
apply package failure rules. Do not detour into repairing Guru Trellis or filing
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

A terminal result requires no pending creation or unresolved operation, all
admitted children inactive at verified safe boundaries, and verified heartbeat
stop through the native tool. Do not blindly interrupt a merge. If stopping the
heartbeat fails or safe disposition remains unproven, return `progressing`
with that exact incomplete settlement and recover it.

Use a stage-completed exit only under the selected package's declared stage
conditions. State unfinished Issue/Task work without inventing a merge blocker.
A genuine blocked exit requires the requested endpoint still unmet and no
remaining permitted work that can advance. Completed exits require full proof.
Do not archive chats, remove worktrees or perform other incidental cleanup.

Resume the same run after its concrete blocker is resolved. Recover children,
revalidate affected proofs and resume the same heartbeat as needed. No new Task
or fresh-base restart. Membership, dependency, completion-gate or resource changes
need fresh semantic impact review and only their real human choices. Do not
persist authorization during recovery.
