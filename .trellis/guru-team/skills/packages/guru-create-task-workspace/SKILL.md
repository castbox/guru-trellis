---
name: guru-create-task-workspace
description: Create or exactly reuse a reviewed issue workspace and Trellis task through an AI-owned semantic gate, ephemeral scoped confirmation, deterministic execution, and four typed exits.
---

# Guru Create Task Workspace

Use this Skill only after `guru-review-change-request:ready`, or as a standalone
invocation that can supply and revalidate the same five prerequisite results.
Load [references/contract.md](references/contract.md) before acting.

Perform the semantic forward behavior and AI Review Gate, obtain the
invocation-specific human confirmation without persisting it, then run the
deterministic recorder/executor/checker and return exactly one declared typed
exit. GitHub issue mutation and workspace/task
mutation are mutually exclusive invocations. A created issue always returns
`refresh_review`; it never creates a workspace or task in the same invocation.
Retry recovery reuses one exact post-plan open issue, and mutation execution
reruns the shared base sync once before the first business write.

The package wrappers require the complete installed Guru Team preset and route
through `run-skill-command`. They are not standalone implementations. Missing,
stale, mismatched, ambiguous, or unconsumed evidence fails closed.

For an ordinary existing issue, author only `scope`, `naming`, `assignee`,
`side_effects`, and `ai_review_gate`; use the exact input preparation contract
in [references/contract.md](references/contract.md#recorder-input-preparation).
Do not author hashes or reconstruct predecessor private payloads. After the
semantic gate and current confirmation, send `{schema_version, transition,
authoring}` to the recorder; its stdout is the complete existing plan contract.
Drafts and issues carrying created-issue provenance still require the complete
plan compatibility input. The new input never infers missing provenance.

If the user refuses the displayed action, stop before the recorder/executor and
do not generate a plan, result, DTO, or typed exit. After the semantic gate,
confirmation, and owner recorder/executor/checker complete, pipe one closed
call-local workspace envelope to `scripts/invoke.sh --invocation -`. The
envelope contains the current public input, `readiness_current` transition,
owner plan, and checked owner result. The recorder prepares consumer-local
projections from `readiness_current`; complete predecessor owner payloads remain
private. The result checker must be run separately. Public invocation validates
the result schema and its checker status and serializes its typed exit; it does
not re-run live checking or perform an additional issue, worktree, branch, or task
mutation. No predecessor payload, plan, result, or authorization is persisted
for normal transport. Repo-relative plan/result/prerequisite locators remain
compatibility-only until the next breaking Interface migration and must not be
used by normal workflow, production eval, or installed transcript paths.
