---
name: guru-create-task-workspace
description: Create or exactly reuse a reviewed issue workspace and Trellis task through a semantic gate, scoped confirmation, deterministic execution, and four typed exits.
---

# Guru Create Task Workspace

Use this Skill only after `guru-review-change-request:ready`, or as a standalone
invocation that can supply and revalidate the same five prerequisite results.
Load [references/contract.md](references/contract.md) before acting.

Perform the semantic forward behavior, AI Review Gate, invocation-specific
human confirmation, deterministic recorder/executor/checker, then return
exactly one declared typed exit. GitHub issue mutation and workspace/task
mutation are mutually exclusive invocations. A created issue always returns
`refresh_review`; it never creates a workspace or task in the same invocation.

The package wrappers require the complete installed Guru Team preset and route
through `run-skill-command`. They are not standalone implementations. Missing,
stale, mismatched, ambiguous, or unconsumed evidence fails closed.
