---
name: trellis-start
description: "Guru Team Trellis fallback orientation entry. Use when automatic startup context is unavailable, hooks did not run, or the user explicitly asks to reload full Trellis context."
---

<!-- guru-team-overlay: v1 -->

# Guru Team Trellis Start Fallback

Use this entry as fallback / explicit orientation. In normal auto-bootstrap platforms, users can describe the task, paste an issue URL, or say "handle issue #123"; the AI should classify that request from injected Trellis context, workflow-state, startup context, hook breadcrumbs, or skill matching.

Run this start entry when the platform has no automatic session/startup injection, hooks are disabled or unapproved, bootstrap appears not to have run, or the user asks for a full context report / reload.

1. Run:

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode phase
```

2. If there is no active task and the user's natural-language request is issue-backed, task-like, or requires file changes, the first priority is Guru Team Phase 0 intake, not bare `task.py create` in the current checkout. Do not silently edit the current checkout. Run:

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json "<user request, issue number, or issue URL>"
```

3. Treat default `prepare-task` as intake/preflight planning only. Show duplicate candidates, proposed title/body when present, naming quality result, base branch, branch name, workspace path, and the confirmed command. If `naming_quality.ok=false` or `requires_semantic_name=true`, read the issue and choose a semantic English short-name, then pass it explicitly with `--short-name`, `--workspace-slug`, `--task-slug`, and `--branch`; do not rely on Chinese transliteration or low-information names such as `issue-52`. If prepare returns `proposed_issue` / `requires_confirmation`, stop until the user approves GitHub issue creation. Only then rerun with `--create-issue-confirmed --issue-title "<reviewed title>" --issue-body-file <reviewed-body-file>`.

4. After reading the request or issue body/comments, perform the `.trellis/workflow.md` intake clarity check. If scope, acceptance criteria, close/ref semantics, or implementation target is ambiguous, enter `trellis-brainstorm` before task start; inspect repository evidence before asking user questions. Clarification results must be reflected in a reviewed proposed issue body, an issue comment, or a deliberate issue body update when appropriate.

5. Ask for consent before creating a GitHub issue, worktree, branch, or Trellis task unless the user explicitly requested that side effect. `--create-worktree` and `--create-task` are executor flags for after handoff review, not default intake commands, and they fail closed when naming quality requires semantic overrides. In `workspace_mode: worktree`, use `prepare-task --create-worktree --create-task` or an equivalent controlled Guru Team executor to create the execution worktree and task; do not run bare `python3 ./.trellis/scripts/task.py create ...` in the source checkout.

6. After an executor path writes `.trellis/guru-team/handoff.json`, treat its `workspace_path` as the machine boundary for all task artifact writes. Before writing or validating `planning-approval.json`, `phase2-check.json`, `agent-assignment.json`, `reviews/*.md`, `review.md`, or `review-gate.json`, run `.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>` from the target worktree. If an edit tool cannot receive an explicit `workdir`, use an absolute path under the task worktree, never a source-checkout relative task path.

7. Task creation consent is not current-checkout direct-edit consent. A
   current-checkout direct-edit override is allowed only after explicit user
   approval. The approval must state that the user wants to skip creating or
   reusing a GitHub issue, Trellis task, worktree, and branch for this turn.
   Before editing, summarize the skipped artifacts, current checkout, current
   branch, dirty state, expected side effects, changed-file scope, and that
   commit/push/PR still require separate approval.

8. In target business repositories, keep human-readable documentation in Chinese by default: `.trellis/spec/**`, `.trellis/tasks/**`, `docs/**`, docs SSOT created or completed by `00-bootstrap-guidelines`, and workflow artifact fields such as summaries, evidence, findings, observations, follow-up candidates, PR titles, and PR bodies. Literal commands, paths, config keys, GitHub keywords, external API names, and code symbols may stay in English.

9. During planning, follow `.trellis/workflow.md` for Middle-platform Knowledge Gate and Repo Docs SSOT discovery. MCP availability is checked from current AI tools/capabilities, not shell scripts.

10. Treat `.trellis/guru-team/handoff.json` as intake provenance only. Final close/ref/followup scope belongs in the task-level `issue-scope-ledger.json`; sub-agent assignment and reuse evidence belongs in task-local `agent-assignment.json`.

Full contract lives in `.trellis/workflow.md`.
