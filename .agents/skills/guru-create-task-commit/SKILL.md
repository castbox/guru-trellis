---
name: guru-create-task-commit
description: Create a reviewed Trellis task work commit after Phase 2, including finding-fix and revision commits, with exact staging and fresh evidence.
---

# Create Task Commit

Use this skill for creating a task commit, committing Phase 2 changes,
committing a Branch Review finding fix, or creating a revision commit.

Read `references/contract.md` completely. Validate every declared entry
precondition in workflow and standalone mode, then execute the ordered
closed-loop stages exactly once for the current candidate and live authority.

`workflow` means mandatory global workflow routing. `standalone` means direct
platform discovery without that routing; it still requires the complete,
current Guru Team preset and extension runtime. This Skill directory is not
a self-contained or portable package.

The recommended Happy Path is exactly two package calls:

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
`--candidate-artifact` mode is the normal path. Existing callers that already
orchestrate an executor result may continue to use compatibility-only
`--invocation`; the two argument shapes are mutually exclusive, and the
compatibility branch is never run before the normal transaction.

`scripts/check-task-commit-plan.sh` and `scripts/create-task-commit.sh` remain
package-private diagnostic, testing, and bounded recovery entries. They must
not be added between prepare and the confirmed public invocation.

Return exactly one declared exit: `committed`, `revision-required`, or
`blocked`. Unknown, multiple, stale, or unmapped results fail closed.

The current candidate lives only under ignored
`.trellis/.runtime/guru-team/task-commit-plans/**`, is never staged, and is
removed after success. Candidate 5.0 has no authorization, branch
classification, publication eligibility, freshness digest, or terminal result
fields. The public invocation may retain one minimal ignored result receipt after success
so the same locator can recover lost stdout without repeating the commit; a
fresh prepare for the same task retires that receipt. An unfinished 4.0 candidate is rejected or replaced only by a complete
reprepare from current Phase 2 and live Git evidence. Git supplies committed
tree/message/path facts.
