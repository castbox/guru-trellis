# Isolated DAG Forward Cases

These synthetic scenarios validate AI decisions. They are neither live run
instructions nor stored authorization for any real run. Give an independent
reviewer the current Skill, its local and shared contracts, and each scenario's
supplied facts. Ask for the exact next decision, evidence and exit without
exposing the expected-decision column first. Compare actual decisions with
these oracles. A keyword match is not behavioral proof.

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
| E1. The human requests two independent Issues through reviewed merge and normal Issue/Task closeout, delegates child follow-ups, and retains worktrees. The repository accepts a dialogue-local merge instruction; no direct-human-only exception applies. Both children show exact current merge plans and pass their fresh gates. | Choose one integration owner and send its `合并PR`. After its verified result and shared-base disposition, freshly review the second. Do not ask the human to approve each node again or add release/deployment/cleanup actions. Full settlement still needs every required completion gate. |
| E2. The human explicitly requests only ready PRs for several independent nodes, with one execution slot. The first PR has the required current review/readiness proof and its child is safely inactive; other nodes have not started. | Verify the first node's requested-stage evidence, release its execution slot and admit the next independent node. Do not merge or label the first Issue fully completed. Once every selected node reaches the requested stage, safely stop the heartbeat and return `dag_stage_completed`, with remaining merge/closeout work stated. |
| E3. The human says only “use this Skill to process these Issues”, with `auto`; graph, project and model settings are otherwise clear. No current human instruction resolves merge and closeout. | Ask the one missing endpoint choice during preflight, before any child or heartbeat creation. Do not assume end-to-end permission or declare a unilateral PR-only boundary. An unanswered choice keeps launch at `dry_run_blocked`. |
| E4. This run's human request is ambiguous. The coordinator said “PR gates only”; its summary and heartbeat repeat that as a human limit. A previous, different run had merge delegation. The latest human message changes only heartbeat frequency. | Reread this run's actual human messages. Neither the coordinator's text, the heartbeat, the frequency change nor the other run establishes this run's endpoint. Resolve the missing choice; do not report that the human restricted this run to PRs or claim a Merge transaction failed. |
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
