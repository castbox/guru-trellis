---
name: guru-sync-base
description: Resolve, safely synchronize, and deterministically validate the selected Git base before Guru Team reads repository task context or starts intake side effects.
---

# Guru Sync Base

Use this Skill when the Guru Team workflow mandatory invokes `guru-sync-base`,
or when the user explicitly asks to refresh or verify a repository base branch.

The caller must finish tool-free route classification before invoking this
Skill. Load [references/contract.md](references/contract.md) and execute its
deterministic closed loop: resolve stdout facts, execute only with the expected
pre-sync resolution digest, generate and validate the post-sync resolution
digest against live Git, then return exactly one declared typed exit.

Workflow mode may return `synced`, `skipped`, or `blocked`. Standalone mode
may return only `synced` or `blocked`; it never enters issue intake, task
creation, worktree creation, or change-context discovery. Resolution and result
facts remain on stdout; the Skill does not create or manage cross-step evidence
files.

Fail closed when the complete compatible Guru Team preset/runtime is missing,
when facts are stale or ambiguous, or when any runtime/schema/managed-copy
validation fails. This package is not self-contained or portable.

Public handoff uses `scripts/invoke.sh` with the declared scalar CLI signature.
The wrapper dispatches only through `run-skill-command`; runtime performs the
formal resolve, execute, and check sequence, then emits one `synced`, `skipped`,
or `blocked` minimal DTO. The public `base_branch` scalar is the caller-owned
result of the selected-base resolution step. Do not read/import the shared
Python runtime or pass the private base-sync result as the next Skill input.
