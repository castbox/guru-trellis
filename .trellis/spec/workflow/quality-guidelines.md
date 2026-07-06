# Workflow Quality Guidelines

## Source-Backed Changes

Every workflow behavior change should update the canonical source and the
surfaces that expose it:

- reusable workflow: `trellis/workflows/guru-team/workflow.md`
- dogfooded active workflow when needed: `.trellis/workflow.md`
- preset overlay entries under `trellis/presets/guru-team/overlays/`
- README docs for installation, upgrade, and daily entrypoints
- companion scripts and schemas when behavior is executable

For `no_task` file-changing behavior, the canonical workflow must state the
default Phase 0 intake/preflight path and the only allowed current-checkout
direct-edit override: explicit user approval to skip GitHub issue, Trellis
task, worktree, and branch for that turn. Do not express that decision as an
AI-internal convenience path.

When Guru Team overlay is enabled, issue-backed, task-like, or file-changing
`no_task` prompts must name both entry commands:

- `.trellis/guru-team/scripts/bash/check-env.sh --json`
- `.trellis/guru-team/scripts/bash/prepare-task.sh --json`

Phase 1.0 must not leave bare `task.py create` as the apparent source-checkout
path for `workspace_mode: worktree`; it should point to `prepare-task
--create-worktree --create-task` or an equivalent controlled Guru Team executor
after handoff review and user approval.

Search before editing a phrase, command, marker, or config key:

```bash
rg "review-branch|finding|observation|followup-candidate|最终放行审查代理|finish-work|publish-pr|issue-scope-ledger|middle_platform_knowledge|guru-team-overlay"
```

## Required Checks

Use these checks before committing workflow or preset changes:

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate <task-dir>
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

Add targeted script invocations when changing phase parsing, intake, review,
finish, publish, installer behavior, or source-repo dogfood overlay sync.

When changing PR publish behavior, include tests or dry-runs for both a blocked
low-information body and an accepted reviewer-readable body. The accepted body
must contain concrete `变更摘要`, `影响范围`, `验证结果`, `Review Gate`,
`Issue 关闭范围`, and `安全说明` sections. The blocked case should cover phrases
such as `当前 Trellis task`, `已提交实现与文档更新`, or `详见 artifact`.

When changing user-facing workflow command examples, especially closeout or
publish examples, add regression coverage or explicit grep checks for both the
runtime entrypoints and public docs (`README.md`, workflow README, preset README,
and durable requirement docs when present). A command example can be correct in
overlays but still mislead users if a README keeps the older copy.

## Review Focus

Before Branch Review Gate, obtain an independent Agent review of the full branch
diff from the task's intake base branch, then record the result with
`review-branch.sh --review-source independent-agent`. Main-session self-review
cannot pass the gate. Include:

- marketplace index and docs
- workflow and dogfood copy
- companion scripts
- schemas and config templates
- preset installer and overlays
- Trellis task artifacts
- generated or installed-copy expectations
- Phase 0 handoff/preflight evidence, or explicit no-task direct-edit override
  evidence when the branch intentionally skipped issue/task/worktree/branch
- task artifact write location: `review.md`, `review-gate.json`, and similar
  files must be written under the task worktree selected by intake
  `workspace_path`; when a manual editing tool has no explicit working
  directory, use a worktree-local absolute path
- deployment asset impact

## Anti-Patterns

- Adding project-private business policy to the reusable `guru-team` workflow.
- Making shell scripts detect AI runtime capabilities such as MCP availability.
  Treat those as AI runtime/tool capabilities and express the decision in
  workflow or prompt text.
- Relying on chat memory for issue close scope, base branch, or reviewed head.
- Treating "small fix" as permission to modify the current checkout under
  `no_task` without Phase 0 evidence or explicit direct-edit override evidence.
- Writing task review artifacts into the source checkout because a manual edit
  used a relative path while the active task lives in a separate worktree.
- Leaving `.new` or `.bak` installer outputs unresolved in committed changes.
- Committing local identity files, `.env`, tokens, signed URLs, or private
  provider output.
