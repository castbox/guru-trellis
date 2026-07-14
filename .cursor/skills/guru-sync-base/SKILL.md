---
name: guru-sync-base
description: Resolve, review, safely synchronize, and validate the selected Git base before Guru Team reads repository task context or starts intake side effects.
---

# Guru Sync Base

Use this Skill when the Guru Team workflow mandatory invokes `guru-sync-base`,
or when the user explicitly asks to refresh or verify a repository base branch.

Load [references/contract.md](references/contract.md) and execute the complete
closed loop. Resolve first, review invocation intent and the selected base,
execute only with the reviewed resolution digest, perform the AI Review Gate,
run the declared objective validator, clean result evidence, then either clean
resolution evidence or transfer its controlled workflow lease before returning
exactly one declared typed exit.

Workflow mode may return `synced`, `skipped`, or `blocked`. Standalone mode may
return only `synced` or `blocked`; it never enters issue intake, task creation,
worktree creation, or change-context discovery. Workflow `synced` transfers the
exact external resolution raw-byte/digest lease to its unique consumer; every
other terminal return cleans all owned evidence.

Fail closed when the complete compatible Guru Team preset/runtime is missing,
when evidence is stale or ambiguous, or when any runtime/schema/managed-copy
validation fails. This package is not self-contained or portable.
