---
name: guru-sync-base
description: Resolve, safely synchronize, and deterministically validate the selected Git base before Guru Team reads repository task context or starts intake side effects.
---

# Guru Sync Base

Use this Skill when the Guru Team workflow mandatory invokes `guru-sync-base`,
or when the user explicitly asks to refresh or verify a repository base branch.

The caller must finish tool-free route classification before invoking this
Skill. Load [references/contract.md](references/contract.md), then invoke
`scripts/invoke.sh --invocation -` exactly once with the closed call-local
envelope. The runtime alone executes the deterministic resolve, execute and
check components before returning exactly one declared typed exit.

Base resolution first selects the branch without consulting the current branch
or registered-worktree availability. It then binds that fixed selection to the
unique clean checkout registered for `refs/heads/<selected-base>` in the same
Git common-dir. The invocation checkout may be detached. Fetch, fast-forward,
live validation, and the public repository locator all use the bound authority
checkout; missing, dirty, or mismatched authority identity returns `blocked`
without selecting another base or creating/switching a checkout.

Workflow mode may return `synced`, `skipped`, or `blocked`. Standalone mode
may return only `synced` or `blocked`; it never enters issue intake, task
creation, worktree creation, or change-context discovery. Resolution and result
facts remain on stdout; the Skill does not create or manage cross-step evidence
files.

Fail closed when the complete compatible Guru Team preset/runtime is missing,
when facts are stale or ambiguous, or when any runtime/schema/managed-copy
validation fails. This package is not self-contained or portable.

Normal public handoff uses `scripts/invoke.sh --invocation -`; the declared
scalar CLI remains compatibility-only and is not the workflow route. The
wrapper dispatches only through `run-skill-command`; runtime performs the formal
resolve, execute, and check sequence, then emits one `synced`, `skipped`, or
`blocked` minimal DTO. Do not invoke the low-level components first, read/import
the shared Python runtime, or pass the private base-sync result as the next
Skill input.
