---
name: guru-sync-base
description: Resolve a fixed Git baseline for read-only Intake, or safely synchronize a selected base checkout.
---

# Guru Sync Base

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Use this Skill when the Guru Team workflow mandatory invokes `guru-sync-base`,
or when the user asks to read a fixed Git baseline, refresh, or verify a repository base branch.

The caller must finish tool-free route classification before invoking this
Skill. Load [references/contract.md](references/contract.md), then invoke
`scripts/invoke.sh --invocation -` exactly once with the closed call-local
envelope. The runtime alone executes the deterministic resolve, execute and
check components before returning exactly one declared typed exit.

Use the [contract locations](references/contract.md#contract-locations-and-public-call)
before authoring that envelope. Interface paths beginning with `consumers/`
resolve from `.trellis/guru-team/skills`, while public `schemas/` and `examples/`
resolve from this package. The envelope is not a package-local schema.

For `operation=read`, the caller selects a repository and `base_ref` (a Git ref
or commit), with optional `base_commit` as an expected resolution assertion.
Omitted `base_ref` reuses the original explicit/config/candidate/default base
selection rules. Runtime fixes the available commit and returns `baseline_ready`
to Discovery. It does not require a base checkout, cleanliness, fetch, or
fast-forward. Later ref movement does not retarget that adopted commit.

For `operation=sync` (the compatibility default), base resolution first selects the branch without consulting the current branch
or registered-worktree availability. It then binds that fixed selection to the
unique clean checkout registered for `refs/heads/<selected-base>` in the same
Git common-dir. The invocation checkout may be detached. Fetch, fast-forward,
live validation, and the public repository locator all use the bound authority
checkout; missing, dirty, or mismatched authority identity returns `blocked`
without selecting another base or creating/switching a checkout.

Workflow mode may return `baseline_ready`, `synced`, `skipped`, or `blocked`.
Standalone read returns `baseline_ready` to its declared Discovery consumer;
standalone sync returns `synced` or `blocked`. Neither creates a Task or worktree. Resolution and result
facts remain on stdout; the Skill does not create or manage cross-step evidence
files.

Fail closed when the complete compatible Guru Team preset/runtime is missing,
when facts are stale or ambiguous, or when any runtime/schema/managed-copy
validation fails. This package is not self-contained or portable.

Normal public handoff uses `scripts/invoke.sh --invocation -`; the declared
scalar CLI remains compatibility-only and is not the workflow route. The
wrapper dispatches only through `run-skill-command`; runtime performs the formal
resolve, execute, and check sequence, then emits one `baseline_ready`, `synced`, `skipped`, or `blocked` minimal DTO. Do not invoke the low-level components first, read/import
the shared Python runtime, or pass the private base-sync result as the next
Skill input.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
