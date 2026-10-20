---
name: guru-create-task-commit
description: Create an exact reviewed Delivery commit for early Draft feedback or the final Check-bound path.
---

# Create Task Commit

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

Read and apply `.trellis/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage`
for shared candidate coverage, engineering facts and recovery. This package
retains its own current judgment, formal result and action boundary.

Read the current Delivery integration contract in [references/contract.md](references/contract.md) first.

Use this skill for creating a task commit, committing Phase 2 changes,
committing a Branch Review finding fix, or creating a revision commit.

Read `references/contract.md` completely. Validate every declared entry
precondition in workflow and standalone mode, then execute the ordered
closed-loop stages exactly once for the current candidate and live authority.

`workflow` means mandatory global workflow routing. `standalone` means direct
platform discovery without that routing; it still requires the complete,
current Guru Team preset and extension runtime. This Skill directory is not
a self-contained or portable package.

For a clean committed candidate, use `scripts/invoke.sh --input <delivery_committed_reentry> --owner-result <actual-review>`. After semantic review it returns the existing candidate without stage, commit, hook or ref mutation.

For a necessary dirty increment the Happy Path is exactly two package calls:

1. Use `scripts/prepare-task-commit.sh` once to record the AI-owned path
   classifications, seven structured message fields, and completed semantic
   result. Present its exact repo, branch, HEAD, paths, subject, and body.
2. After the current conversation confirms that unchanged action, use
   `scripts/invoke.sh --candidate-artifact <prepared-locator>` once. Do not
   pass confirmation text or state. The public invocation performs the
   mutation-boundary validation, exact transaction, typed-exit projection, and
   same-commit stdout-loss recovery.

The user may answer with any clear affirmative response after the Skill
presents one current, unique commit action. That conversational authority is
never written to public input, private runtime, task metadata, archive, or the
public invocation. Missing or mismatched runtime state fails closed with
full-preset install/upgrade remediation before a task/Git side effect. A
current exact commit request is the dialogue-local authority for that displayed
action. Branch name, role, protection, sharing, task ownership, remote
publication, or PR state neither grant nor deny commit authority and are not
read as commit preconditions.

`scripts/invoke.sh` is the sole public invocation wrapper. Its
`--candidate-artifact` mode is the exact dirty transaction; `--input` is the
clean committed re-entry. These argument shapes are mutually exclusive.
Legacy `--invocation` envelopes are retired; recover a committed candidate
through the current Delivery input after its fresh Check and semantic review.

`scripts/check-task-commit-plan.sh` and `scripts/create-task-commit.sh` remain
package-private diagnostic, testing, and bounded recovery entries. They must
not be added between prepare and the confirmed public invocation.

Return exactly one declared exit: `draft_committed`, `committed`, `revision-required`, or
`blocked`. Unknown, multiple, stale, or unmapped results fail closed.

For an explicit independent manual operation after an automatic stop, read
`.trellis/workflow.md#manual-gitgithub-operations` (Manual Git/GitHub Operations).
That global boundary does not relax this Skill's entry or completion contract.

The current candidate lives only under ignored
`.trellis/.runtime/guru-team/task-commit-plans/**`, is never staged, and is
removed after success. Candidate delivery-2.0 has no authorization, branch
classification, publication eligibility, freshness digest, or terminal result
fields. The public invocation may retain one minimal ignored result receipt after success
so the same locator can recover lost stdout without repeating the commit; a
fresh prepare for the same task retires that receipt. A pre-Delivery candidate is rejected or replaced only by a complete
reprepare from current Phase 2 and live Git evidence. Git supplies committed
tree/message/path facts.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.

For actual Plan2 planning relocation, this owner may explicitly review and select the bounded `markdown_relative_links_v1` private source mode described in the contract. Existing absent-mode source mappings stay strict bytes/modes. Planning owners never consume this private association.

## Early Draft commit

`delivery_draft_commit` requires the exact registered Task/Delivery, accepted
current Planning and implementing phase. It binds fixed base B without a
check_result_id. Review the complete dirty snapshot and actual proposed content
against scope. Run Planning-selected minimum self-checks. Check sensitive
content, precise target, stage paths, message and unrelated preservation before
prepare and the current-dialogue commit boundary. Complete Check, heavy tests
and final Branch Review remain pending duties.

Use the same prepare and exact invoke transaction, real hooks and same-commit
receipt recovery. The private candidate/result use the closed delivery-2.0 union:
draft contains no Check or phase2 anchor; final retains both real bindings.
`draft_committed` carries task_ref/key/B/commit_sha only to the workflow draft
router and original Publication. It cannot enter formal Branch Review.

For an already committed nonempty B..HEAD candidate, including a legal resolved
integration commit, `delivery_draft_committed_reentry` performs the same bounded
semantic review and proves committed Task identity and all five Planning files.
It returns the early DTO without stage, commit, hook, begin_check or gate.
Active merge/sequencer state is still rejected. New dirty content uses prepare;
no empty commit restores output. Final profiles keep Check and `committed`
semantics. Matching migration is defined by MIGRATION-636.
