---
name: guru-create-task-commit
description: Create a reviewed Trellis task work commit after Phase 2, including finding-fix and revision commits, with exact staging and fresh evidence.
---

# Create Task Commit

Use this skill for creating a task commit, committing Phase 2 changes,
committing a Branch Review finding fix, or creating a revision commit.

Read `references/contract.md` completely. Validate every declared entry
precondition in workflow and standalone mode, then execute the ordered
closed-loop stages exactly once for the current plan sequence.

`workflow` means mandatory global workflow routing. `standalone` means direct
platform discovery without that routing; it still requires the complete,
compatible Guru Team preset and extension runtime. This Skill directory is not
a self-contained or portable package.

Use `scripts/check-task-commit-plan.sh` for objective candidate validation and
`scripts/create-task-commit.sh` for the exact deterministic side effect. These
thin wrappers dispatch through the shared `run-skill-command` runtime and never
replace AI scope/message review or required human confirmation. Missing or
incompatible runtime state fails closed with full-preset install/upgrade
remediation before a task/Git side effect.

Return exactly one declared exit: `committed`, `revision-required`, or
`blocked`. Unknown, multiple, stale, or unmapped results fail closed.
