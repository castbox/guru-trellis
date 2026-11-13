# Isolated DAG Forward Cases

These synthetic scenarios validate AI decisions. They are neither live run
instructions nor stored authorization for any real run. Give an independent
reviewer the current Skill, its local and shared contracts, and each scenario's
supplied facts. Ask for the exact next decision, evidence and exit without
exposing the expected-decision column first. Compare actual decisions with
these oracles. A keyword match is not behavioral proof.
The expected observations below stay host-only. These walkthroughs supplement
real isolated multi-turn Agent execution; they do not prove its tool behavior.

Do not launch chats/automations, send messages, modify Git/GitHub or create
coordinator state during the walkthrough. All listed human statements are
synthetic scenario input. Exact model/effort settings are supported and explicit
unless a scenario says otherwise. All unspecified access/tool facts pass.

## Review Scenarios

Use these ordinary scenarios for a static walkthrough or an isolated simulation.
Do not launch live chats, automations, or GitHub writes just to validate a skill.

| Scenario | Required observable decision |
| --- | --- |
| One Issue; no edges | One child; completion stops heartbeat. |
| Fork, fast left branch, slow right branch | Left successor starts as soon as its own predecessors complete and a slot is free. |
| Join with one incomplete predecessor | Join child is not created. |
| Two free slots; first creation pending | Pending node consumes one slot; another independent ready node can use the second. |
| Replayed pending/idle event | No duplicate chat or duplicate disposition. |
| Temporary capacity error in one child | Same child/model retries on a later heartbeat; siblings remain observed. |
| One child blocks | Descendants wait; independent work follows the chosen failure policy. |
| Two PRs ready; first merges | Second passes current-base reconciliation before its separate merge disposition. |
| Squash merge completes | Verify actual resulting commit and candidate mapping, not ancestry of the old feature HEAD. |
| Resume after legitimate base movement | Recover existing children and reconcile; do not require initial OIDs or clean active worktrees. |
| Graph has cycle or missing hard edge | Read-only blocked result, no launch. |
| More children than one wait batch | Every child receives an observation or an explicit observation error in the cycle. |
| Human requested only a graph/dry-run | No child, heartbeat, ref, or file mutation. |
| Child finishes a phase without asking for a fixed continuation phrase | Heartbeat infers and sends the next valid phase instruction in the same cycle. |
| Latest completed turn recommends one bounded solution | Heartbeat evaluates it and may send `按建议方案执行` without another human nudge. |
| Child says blocked by stale evidence with a supported refresh route | Heartbeat requests original-owner refresh and continuation, not terminal blocking. |
| Child requests merge but required checks failed | Heartbeat requests remediation; it does not send `合并PR`. |
| Idle child waits on CI; CI turns green without new child text | Heartbeat rechecks live prerequisites and sends the newly valid continuation. |
| Chat-message send returns an unknown outcome | Read actual child conversation before retrying; no blind duplicate prompt. |

## Endpoint And Delegation Regressions

These are synthetic regression inputs and expected observations, not live run
instructions or retained authorization. Exercise them through an isolated AI
walkthrough using the current Skill and contracts. Do not create chats,
automations, Git mutations or a state file for these checks. Judge the actual
next action and its evidence; matching a phrase or exit alone is insufficient.

| Case and supplied conversation/live facts | Required observable decision |
| --- | --- |
| E1. The human requests two independent Issues through reviewed merge and normal Issue/Task closeout, delegates child follow-ups, and retains worktrees. The repository accepts a dialogue-local merge instruction; no direct-human-only exception applies. Both children show exact current merge plans and pass their fresh gates. | Within each repository choose one integration owner and send its `合并PR`. After its verified result and shared-base disposition, freshly review the second. Do not ask the human to approve each node again or add release/deployment/cleanup actions. Full settlement still needs every required completion gate. |
| E2. The human explicitly requests only ready PRs for several independent nodes, with one execution slot. The first PR has the required current review/readiness proof and its child is safely inactive; other nodes have not started. | Verify the first node's requested-stage evidence, release its execution slot and admit the next independent node. Do not merge or label the first Issue fully completed. Once every selected node reaches the requested stage, safely stop the heartbeat and return `dag_stage_completed`, with remaining merge/closeout work stated. |
| E3. The human says only “use this Skill to process these Issues”, with `auto`; graph, project and model settings are otherwise clear. No current human instruction resolves merge and closeout. | Keep full Issue completion as the goal. Show the concrete prospective effects and resolve only missing action delegation before launch. Do not ask the human to choose completion versus PR-only, assume merge permission, or invent a PR-only restriction. An unanswered necessary launch-action choice keeps launch at `dry_run_blocked`. |
| E4. This run's human request is ambiguous. The coordinator said “PR gates only”; its summary and heartbeat repeat that as a human limit. A previous, different run had merge delegation. The latest human message changes only heartbeat frequency. | Reread this run's actual human messages. Neither the coordinator's text, the heartbeat, the frequency change nor the other run establishes a PR-only limit or action delegation. Keep the completion goal and resolve the missing concrete action choice; do not report that the human restricted this run to PRs or claim a Merge transaction failed. |
| E5. On recovery, this run's original human message clearly delegates reviewed merges and normal closeout. A summary says “ask for merge confirmation”; the idle child has displayed one exact fresh merge plan, all required gates pass, and no direct-human-only exception applies. | Recover that same-run human instruction, preserve the existing child and integration ordering, and send the valid merge instruction. Do not ask the human to repeat delegation or copy its text/status into a child prompt, heartbeat or checkpoint. |
| E6. E1 applies, but the repository explicitly reserves this particular merge confirmation to the human directly. | Preserve that exception and request the exact required human action. Do not represent a coordinator message as the human's direct confirmation, and do not waive any merge gate. |
| E7. End-to-end work is delegated, but one PR's required check failed and its original owner has a supported repair. | Request that repair and re-review affected evidence. Keep monitoring permitted work as `progressing`; do not merge, ask for redundant approval, or declare a terminal block before attempting the supported route. A genuine unresolved prerequisite still uses the normal blocked route. |
| E8. The human requests PR-only work for A then B, while B's live hard prerequisite requires A's merged completed result and A is not complete. | Surface the endpoint/dependency conflict at preflight. Do not weaken the edge, start B from A's unmerged branch, or treat A's PR readiness as full predecessor proof. Resolve the actual scope choice or report the concrete blocked prerequisite. |
| E9. The human requests planning only. The child would normally continue from accepted planning into implementation during the same turn. | Give that child the narrow execution instruction to finish planning, stop before implementation and report the actual result. Do not copy human approval text, status or provenance. Verify only the requested planning result and safe disposition before stage settlement; do not wait until after the child has implemented. |

## Managed Entry And Timing Cases

| Case and supplied facts | Required observable decision |
| --- | --- |
| M1. A user explicitly invokes this managed Skill for a fully delegated run. The source package/shared spec agree; target business repository is elsewhere and has its own complete workflow. The only matching personal copy is historical. | Load the same-provider managed method and target workflow; do not use the personal copy or install orchestration into the target to proceed. |
| M2. E1 applies and no heartbeat interval is mentioned. Native heartbeat supports minute intervals. A child was just created with a formal ID. | Configure the one native current-chat heartbeat for two minutes; immediately snapshot the child with timeout 0. Do not use a 2000ms polling loop or treat the interval as merge permission. |
| M3. Models were not selected, but all other preflight facts and endpoint are clear. Current tool exposes supported model/effort combinations. | Complete read-only findings and ask one concise supported model/effort choice before live effects; do not use stale enumerations or silently inherit defaults. |
| M4. One child reports a broken required validator; its original repository owner has no supported equivalent or recovery. The business evidence looks plausible. | Report the precise missing supported route and apply affected-node failure rules; do not replace a mandatory producer with direct evidence or claim pass. |

## Multi-Turn Coordination Walkthroughs

Supply only the current round's facts to the Agent. For each subsequent round,
obtain its action and observe the result before disclosing new facts. Keep the
required observations private; do not turn them into hints, tool routing rules
or claimed real execution evidence.

| Case and supplied facts across rounds | Required observable behavior across rounds |
| --- | --- |
| U1. A and B are independent; C depends on A. A's idle child reports a failed external check and no recommendation. The diagnostic service's current capability listing includes access to that operation's detailed failure. B is progressing. If inspected, the operation shows an ordinary input-path error that the original owner can correct through its existing entry. Later owner output supplies its corrected execution and gates. | Investigate the available direction and discuss/request the scoped correction from A's owner, then observe the actual result and complete missing obligations. Do not call lack of a recommendation terminal, count the request as a fix, or start C before A's full completion proof. Continue observing B under the original failure policy. |
| U2. A waits on a check with a named owner and recheck condition. Its text stays unchanged. A later observation finds that the operation ended unsuccessfully; the owner's supported correction is available. Another observation after correction finds the new check passed, still without new child text. | Check real operation status each round. Reassess the ended wait, arrange the original-owner correction, then use the passing result for the next valid action. Quiet notification handling does not skip these judgments or cause duplicate sends. |
| U3. A's required producer is unavailable after current capability and original-owner route inspection; no supported equivalent exists. B is independent with remaining permitted work. C depends on A. B later reaches full completion and safe disposition. | Establish the actual gap without manufacturing pass or repairing an out-of-scope framework. Hold C, continue B under continue_independent, and only after remaining permitted work and safe settlement are complete return dag_blocked with checked directions, minimum missing producer condition, responsible party, affected nodes and resume condition. For stop_dispatch, preserve its existing safe-hold rules instead. |

## Selected Base And Completion Goal Regressions

Use the same isolated walkthrough boundary above. Supply facts without the
required-decision column first; these cases do not run live Git operations.

| Case and supplied conversation/live facts | Required observable decision |
| --- | --- |
| B1. The human explicitly selects dev and delegates the concrete completion actions. Local dev, origin/dev and remote dev agree. The repository default is main; local main is behind, in another clean worktree. Two independent nodes are ready. | Preflight is ready without updating main or asking for an exemption. Create children from the supported explicit dev starting state and send dev as the PR/completion target. Preserve the unrelated main worktree. |
| B2. B1 applies, but local dev is behind remote dev. | Report the actual selected-base mismatch read-only; use the original base owner for the exact dev synchronization when execution covers it. Do not synchronize main, waive dev freshness or silently create from main. |
| B3. The human omitted a base; live default is main and its initial OIDs agree. | Resolve main as the selected base without asking an unnecessary base question. Use it consistently for child creation, PR targets and completion. |
| B4. A dev-targeted PR has merged by squash; its actual result is reachable from live dev and not main. Original-owner Check, Review, readiness, Completion, explicit completed Issue closure, archive and required overrides all pass. | Accept full completion after verifying actual result/candidate association. Do not require a later main merge or old feature HEAD ancestry. That node may release its dependent edge. |
| B5. B4 applies except the Issue is still open because a dev merge did not auto-close it. | Retain the incomplete node and request its original Closure owner within actual action delegation. Do not add a main-delivery requirement, assume automatic closure, or release the dependent edge. |
| B6. A heartbeat resumes a dev run after the project's default changes to main. The original human request and existing Task/PR facts consistently select dev; a summary says default base. | Recover dev from original messages and facts, recheck live dev and affected gates, and continue the same owners. Do not retarget to main or rerun initial clean/equal-OID checks on active child worktrees. |
| B7. The human selects dev as integration target and separately requests an existing source ref. The original repository owners confirm that source fits current dependencies and target; the native tool supports it. | Create from that exact supported source and keep dev as PR/completion target. Do not force the source back to dev, retarget to the source branch, or invent a replacement ref. |
| G1. The human delegates full completion and all concrete necessary actions. A child reports a current Ready PR as its final result; later phases are available and pass prerequisites. | Continue through the original merge and closeout owners, observe their actual results and require full proof. Do not return dag_stage_completed merely because that child turn ended. |
| G2. The same completion run discovers that one later operation requires direct human action. Other admitted work is permitted and actionable. | Hold only that operation, display the exact required action, and keep permitted work moving under the failure policy. Preserve remaining completion obligations; do not reinterpret the run as PR-only or use a stage-completed exit. |
| G3. The human expressly pauses after planning; the stage result and safe settlement pass. Later the same human resumes completion with the needed concrete actions. | Initially report only the stage result and remaining obligations using the existing stage exit. On resume recover the same Issue owners, selected base and live proof, then continue toward full completion; do not create replacement identities or count the old stage result as completion. |

## Cross-Repository And Environment Cases

| Supplied facts | Required observable behavior |
| --- | --- |
| Foreign coordinator/provider; API #7 on dev, web #7 on stable depends on it, independent web #8 | Separate repo-qualified nodes/children and exact projects/sources; web #7 waits for API full proof; each merge/completion checked in its own repository/base. |
| Initiative formally binds product final acceptance and two engineering Issues; includes an unrelated reference; requirements already ready | Select only formal members, use actual engineering prerequisites, and make final acceptance follow engineering without a fictitious two-way dependency. |
| A target checkout/project is absent, current supported provisioning entry exists with permission | Covered live operation creates it and rereads project/primary remote/base; dry-run creates nothing. |
| Environment creation permission denied, another project has no supported registration entry, another awaits user App trust; an independent repository is ready | Explain each exact gap and concrete user steps, progress independent work under continue_independent, never edit/click trust; safely settle when necessary and resume same graph/owners after user completion and factual readback. |
| Different repositories share #7 during heartbeat/pending recovery | Preserve repository-qualified child/host/Task/PR associations; no duplicate creation or bare-number lookup. |

The source-only runner `run_native_orchestration.py` exposes `cross-repo`,
`initiative`, `environment-create` and `environment-user` scenes in addition to
the original single-repository scenes. Each uses actual coordinator/child Codex
processes with factual synthetic tools. Raw traces and final messages are
external outputs for independent semantic review, not a keyword-derived verdict.

| Pending cross-repository merge | Two independent repository PRs have real original-owner readiness; API has one pending original merge with unknown result. Web’s fresh gates permit its own merge before API’s result resolves. Keep API’s transaction and owner, never repeat its merge, then complete both and safely stop the heartbeat. Global slots and same-repository serialization remain in force. |

Use `--scene merge-pending` for this difference. Real child turns establish
readiness and the original pending merge before the real coordinator resumes.
A named factual merge operation resolves after its bounded service interval;
the carrier does not inspect message wording or coordinator decisions to choose
its outcome. Observe operation timestamps and actual tool actions, not an exit
keyword alone.

## Quiet Notification Cases

Use the same isolated walkthrough boundary. Supply the native wake's actual
silent-result contract with each case; do not launch notifications to test it.

| Case and supplied conversation/live facts | Required observable decision |
| --- | --- |
| Q1. A fully completes and releases successor C. Independent B changes phase. A slot is free, C's prerequisites pass, and the wake supports the heartbeat DONT_NOTIFY result. No human action is needed. | Observe every unfinished child, admit and immediately observe C, and give actionable idle B its valid continuation. Carry the existing progress exit in the supported silent envelope with the actual automation identity and no surrounding prose. Do not notify for the node completion, admission or phase change. |
| Q2. A failed check has a supported owner repair. B's unchanged wait has ended successfully and permits its next action. | Arrange A's bounded repair, act on B's current passing prerequisite and observe the results. Keep routine output silent; neither the repairable failure nor changed wait alone requires a human notification. |
| Q3. A has an investigated unresolved environment gap requiring App trust from the human. B is independent and remains permitted under continue_independent. | Notify once with A's exact user action and resume condition, preserve A and its descendants, and continue observing and advancing B. Deduplicate the unchanged request on later wakes. Do not use silence to hide the human step or a whole-DAG block to abandon B. |
| Q4. All selected nodes reach their accepted terminal goal and children are safe, but heartbeat stop has not yet been verified. Later the original stop result verifies success. | First return progressing with the actual remaining settlement and recover the operation. Only after verified stop notify once with the existing dag_completed or explicitly selected dag_stage_completed result. Individual nodes reaching a stage never trigger that terminal notification. |
| Q5. The human asks for status during the run; later wakes need no human action. The current native host has not established support for the sample envelope. | Answer the status question directly. For later routine wakes inspect the actual silent transport, preserve every observation and action, and do not claim suppression or invent controls. The status question does not enable recurring notifications. |
