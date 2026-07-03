<!-- TRELLIS:START -->
# Trellis Instructions

These instructions are for AI assistants working in this project.

This project is managed by Trellis. The working knowledge you need lives under `.trellis/`:

- `.trellis/workflow.md` — development phases, when to create tasks, skill routing
- `.trellis/spec/` — package- and layer-scoped coding guidelines (read before writing code in a given layer)
- `.trellis/workspace/` — per-developer journals and session traces
- `.trellis/tasks/` — active and archived tasks (PRDs, research, jsonl context)

If a Trellis command is available on your platform (e.g. `/trellis:finish-work`, `/trellis:continue`), prefer it over manual steps. Not every platform exposes every command.

If you're using Codex or another agent-capable tool, additional project-scoped helpers may live in:
- `.agents/skills/` — reusable Trellis skills
- `.codex/agents/` — optional custom subagents

Managed by Trellis. Edits outside this block are preserved; edits inside may be overwritten by a future `trellis update`.

<!-- TRELLIS:END -->

# Project Instructions

This repository extends Trellis through workflow templates, preset overlays,
project skills, and small companion scripts. Treat those layers as having
different responsibilities.

## Core Boundary

Markdown workflow, prompts, skills, hooks, and preset overlays define the
process. They tell the AI agent when to plan, ask questions, review, check,
publish, or stop.

Python and shell code execute deterministic operations. Use scripts for
specific side effects and fixed validation only, such as creating a worktree,
reading GitHub metadata, writing structured artifacts, checking schema shape,
committing, pushing, archiving a task, or creating a PR from an already-reviewed
body.

Do not move AI judgment into Python or shell. If a step requires understanding
intent, weighing risk, judging sufficiency, identifying missing requirements,
reviewing a diff, deciding issue close scope, or assessing PR readiness, that
step belongs in an AI-facing prompt/workflow/skill. A script may record or
validate the result, but it must not replace the judgment.

## Script Role

Scripts in this repository should be one of:

- **Executor**: performs a concrete requested operation with explicit inputs.
- **Validator**: checks objective, machine-testable conditions.
- **Recorder**: persists reviewed decisions into structured artifacts.

Scripts should not be:

- **Planner**: deciding what the task means or whether scope is sufficient.
- **Reviewer**: deciding a branch has no defects.
- **Product owner**: deciding issue close/ref/followup semantics.
- **Publisher of record**: inventing final PR claims without AI review.

When a script is useful for a gate, the AI process must run first. The script
then records the reviewed findings, validates freshness, and blocks later
steps if evidence is missing or stale.

## Workflow Design

Prefer markdown-first control surfaces:

- `.trellis/workflow.md` for phase order, routing, and required gate behavior.
- `.agents/skills/` for reusable AI procedures.
- platform overlays under `trellis/presets/guru-team/overlays/` for Codex,
  Claude, Cursor, and other tool entry points.
- `.trellis/spec/` for durable project rules and implementation constraints.

Keep generated or installed copies aligned with canonical marketplace and
preset sources. If changing a workflow behavior, check the canonical workflow,
the active `.trellis/workflow.md`, preset overlays, and installed local
overlays together.

## Required Judgment Points

The following steps must be AI-reviewed before any script records or executes
their result:

- deciding whether a user request needs a GitHub issue or Trellis task;
- choosing to create, reuse, or force a new issue after duplicate search;
- approving `prd.md`, `design.md`, and `implement.md` before `task.py start`;
- deciding whether implementation satisfies requirements and design;
- running `trellis-check` as a full task-scope review, not just command output;
- deciding whether `.trellis/spec/` needs updates;
- reviewing the complete branch diff before Branch Review Gate;
- deciding issue `close_issues`, `related_issues`, and `followup_issues`;
- reviewing PR readiness, PR body, validation claims, and security notes.

For these steps, scripts may provide raw facts and enforce artifact presence,
but the actual conclusion must come from the AI review process and be captured
as evidence.

## Side Effects

Do not create GitHub issues, worktrees, branches, Trellis tasks, commits, pushes,
or PRs unless the user explicitly asked for that side effect or has confirmed a
clear handoff plan.

For side-effecting workflows, report the proposed target first: issue, base
branch, branch name, worktree path, task directory, changed files, and command
to be run. Then proceed only within the confirmed scope.

## Evidence And Gates

Prefer explicit, auditable artifacts for gates. A good gate artifact records:

- task and issue scope;
- source artifacts reviewed;
- diff range or file hashes;
- findings and severity;
- validation commands and results;
- reviewer or AI process identity;
- current HEAD or working-tree state;
- blocking decision and rationale.

Passing gates must not be blank assertions. Evidence should describe what was
reviewed and why the result is safe enough to continue.

## Repository Safety

Keep secrets out of logs, issues, task artifacts, PR bodies, and generated
evidence. Never print tokens, private keys, signed URLs, `.env` content,
database URLs, or raw sensitive records.

Respect dirty worktrees. Do not stage, commit, overwrite, or revert unrelated
changes. When asked to commit a narrow change, stage only the files that belong
to that request.

Use this repository's public workflow and preset assets as reusable team
mechanisms. Do not put business-repository private rules or active task state
into generic marketplace templates.
