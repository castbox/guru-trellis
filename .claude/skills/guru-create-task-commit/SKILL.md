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

Use `scripts/prepare-task-commit.sh` to record the AI-owned path classifications,
seven structured message fields, and final semantic result into the private
candidate. It deterministically canonicalizes the complete message and runs the
shared parser before any confirmation. Use `scripts/check-task-commit-plan.sh`
for objective candidate validation and `scripts/create-task-commit.sh` for the
exact deterministic side effect. These
thin wrappers dispatch through the shared `run-skill-command` runtime and never
replace AI scope/message review or required human confirmation. The user may
answer with any clear affirmative response after the Skill presents one
current, unique commit action. That conversational authority is never written
to public input, private runtime, task metadata, or archive. Missing or
mismatched runtime state fails closed with full-preset install/upgrade
remediation before a task/Git side effect.

Return exactly one declared exit: `committed`, `revision-required`, or
`blocked`. Unknown, multiple, stale, or unmapped results fail closed.

The v2 candidate lives only under ignored
`.trellis/.runtime/guru-team/task-commit-plans/**`, is never staged, and is
removed after success. Its schema has no authorization, freshness digest, or
terminal result fields. Git supplies committed tree/message/path facts.
