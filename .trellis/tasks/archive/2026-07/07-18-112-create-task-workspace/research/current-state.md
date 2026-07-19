# #112 current-state research

## Live authority

- Issue #112 remained open at `2026-07-18T08:09:46Z` and names #139 as a
  prerequisite already merged into fresh main.
- The task scope ledger closes #112, #99, and #54; #98 and #53 remain related;
  #132 remains follow-up.
- The abandoned #112 attempt is not an evidence source for this task.

## Official Trellis evidence

- Official custom workflow documentation states that workflow behavior belongs
  in `.trellis/workflow.md`; parser hooks should not embed a second workflow.
- Official marketplace documentation separates workflow installation from spec
  template installation.
- Local `trellis --version` returned `0.6.5`.
- `trellis init --help` exposes `-u/--user` as developer identity input.
- A disposable clean init without `-u` still resolved the Git-config user and
  created `.trellis/.developer` plus `.trellis/workspace/**`. This is official
  Trellis behavior. The Guru preset must preserve official support while proving
  that Guru apply/update/task creation neither depends on nor creates those paths.

## Current repository evidence

- `trellis/skills/guru-team/registry.json` records
  `guru-create-task-workspace` as `planned`; no canonical package exists.
- `trellis/workflows/guru-team/workflow.md` already routes
  `guru-review-change-request:ready` to the planned id and stops fail closed.
- The workflow still contains legacy 0.5-0.8 environment/prepare/handoff prose
  after that stop.
- `cmd_prepare()` owns issue/worktree/task mutations and still calls
  `infer_assignee()` plus `ensure_workspace_developer_identity()`.
- `task-start-context.json` is portable schema 1.0, but its current
  `intake_summary` lacks final-source and prerequisite linkage fields.
- Preset skill installation is registry-driven and already distributes each
  active package to installed/shared/Codex/Cursor/Claude roots with managed-hash
  conflict handling.
- Durable requirements/specs/public docs still describe prepare-task and
  developer identity as active Guru contracts; docs state is `stale_docs`.

## Design consequences

- Activate one semantic package and one exact mutation command.
- Keep pre-task plan/result on stdout; persist only four portable task-local
  Intake artifacts plus ignored producer runtime mappings.
- Deprecate direct prepare mutation to prevent standalone review bypass.
- Add exact draft-created issue binding and force complete Intake refresh before
  workspace creation.
- Add an additive task-start-context linkage projection for new tasks while
  retaining old task compatibility.
- Validate Guru no-developer behavior from an initialized repo where official
  identity/workspace paths are absent; never delete existing user identity data.
- Prove task-local conflict isolation with both A-to-B and B-to-A Git merge order.
