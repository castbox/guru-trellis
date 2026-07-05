# Guru Team Development Workflow

---

## Core Principles

1. **Plan before code** — figure out what to do before implementation starts.
2. **Issue-backed intake** — durable work starts from a GitHub Issue or from a neutral issue proposed by the workflow and created only after AI/human review.
3. **Git preflight before Trellis task files** — resolve base branch and workspace before `task.py create` writes task artifacts.
4. **Specs injected, not remembered** — follow `.trellis/spec/` and task artifacts instead of chat memory.
5. **Persist decisions** — requirements, research, implementation plans, and reusable lessons go to files.
6. **Incremental development** — one task, one branch, one workspace unless the user explicitly approves a current-checkout direct-edit override for this turn.
7. **Chinese artifacts by default** — Trellis task planning artifacts and human-readable review fields are written in Chinese.
8. **Review before finish** — committed branch work must pass Branch Review Gate before `finish-work`.
9. **Publish after finish** — `finish-work` archives the task, records the journal, then automatically pushes and creates a non-draft PR.
10. **Capture learnings** — after each task, review whether `.trellis/spec/` needs updates.
11. **Knowledge before framework changes** — when a task may touch Guru Team middle-platform SDKs or frameworks, retrieve and cite current framework knowledge before design or implementation.
12. **Task artifacts do not replace durable docs** — reconcile Trellis task artifacts with the repo's long-lived `docs/` source of truth before finish.

---

## Guru Team Gate

Before creating a Trellis task or writing task artifacts, run the Guru Team intake and Git preflight.

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json "<user request, issue number, or issue URL>"
```

The default prepare command is side-effect-free intake/preflight planning for GitHub and filesystem writes: it may read an explicit issue and open duplicate candidates, then outputs source/proposed issue, base branch, branch name, workspace path, and `create_task_command`. Planner output is JSON only and does not write `.trellis/guru-team/handoff.json`, create a GitHub issue, worktree, branch, or Trellis task.

If no source issue was supplied, prepare writes `proposed_issue` and `requires_confirmation`. The AI must show the duplicate-search result, proposed issue title/body, base branch, branch name, and workspace path to the user. Only after confirmation may it rerun prepare with `--create-issue-confirmed --issue-title "<reviewed title>" --issue-body-file <reviewed-body-file>`.

After a confirmed source issue exists and the handoff plan has been reviewed, use `--create-worktree` or `--create-task` only with explicit user approval. Those executor paths create or reuse the chosen workspace and then write `.trellis/guru-team/handoff.json` inside that workspace. They must not be used as a shortcut around planning review.

When there is no active task and the current turn requires file changes, do not
silently edit the current checkout. First run Phase 0 intake/preflight, or ask
for and receive explicit user approval for a current-checkout direct-edit
override. That approval must state that the user wants to skip creating or
reusing a GitHub issue, Trellis task, worktree, and branch for this turn. Before
editing, summarize the expected side effects, changed-file scope, current
checkout, current branch, and dirty state. The override only authorizes the
described file edits; commit, push, PR creation, and issue closure still require
their own explicit approval.

The companion scripts live under `.trellis/guru-team/` and are installed by the Guru Team Trellis preset. If they are missing, tell the user to run:

```bash
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh --repo <project>
```

### Intake Rules

- If the user supplies a GitHub issue number or URL, read that issue body and comments before planning.
- If no issue is supplied, decide whether the request is clear enough for an intake issue.
- Before creating an issue, search open issues for likely duplicates and show the result to the user.
- High-similarity candidates are never auto-bound. Ask the user whether to reuse the candidate or create a new issue.
- Proposed issue bodies use a neutral, reusable intake structure. GitHub issue creation requires `--create-issue-confirmed` and an AI/human reviewed body file; never let the default prepare command create the issue.
- Do not rely on `auto_create_issue` in older configs. It is a deprecated compatibility field and must not override the explicit confirmation requirement.
- Do not print tokens, secrets, private keys, signed URLs, `.env` content, or sensitive raw records in logs, docs, issues, or task artifacts.

### Git Preflight Rules

- `gh` must exist and `gh auth status` must pass before any GitHub read/write operation.
- Prefer `dev` or `develop` as base branch, then `main` or `master`.
- If the current branch is not the selected base, report the current branch, selected base, and candidates before proceeding.
- Default workspace is a Git worktree under `../<repo-name>-worktrees`.
- Report current checkout path, current branch, base branch, worktree path, branch name, dirty state, and existing worktrees.
- Slugs, branch names, worktree names, and task names must include an issue number or another unique id. Do not rely on Trellis date prefixes or auto-increment-like names for parallel work.

### Handoff

Planner output, including output with a confirmed `source_issue`, sets `handoff_written: false` and remains stdout-only. After explicit approval for `--create-worktree` or `--create-task`, the executor writes `.trellis/guru-team/handoff.json` inside the chosen workspace. It must not dirty the source checkout merely because a new AI session or intake preflight ran. A written handoff contains:

- confirmed source issue number, URL, title, and creation flag; `source_issue` is intake provenance, not the final close scope
- handoff path and `handoff_written` state
- slug, task slug, task title, branch, base branch, workspace path
- an Issue Scope Ledger seed that the task copies to `{TASK_DIR}/issue-scope-ledger.json`
- duplicate-search candidates
- preflight evidence
- exact `task.py create` command

---

## Trellis System

### Developer Identity

On first use, initialize your identity:

```bash
python3 ./.trellis/scripts/init_developer.py <your-name>
```

Creates `.trellis/.developer` (gitignored) and `.trellis/workspace/<your-name>/`.

### Spec System

`.trellis/spec/` holds coding guidelines organized by package and layer.

- `.trellis/spec/<package>/<layer>/index.md` — entry point with development and quality checks.
- `.trellis/spec/guides/index.md` — cross-package thinking guides.

```bash
python3 ./.trellis/scripts/get_context.py --mode packages
```

Update spec when a task discovers a reusable pattern, pitfall, convention, or technical decision.

### Task System

Every task has its own directory under `.trellis/tasks/{MM-DD-name}/` holding `task.json`, `prd.md`, optional `design.md`, optional `implement.md`, optional `research/`, the task-level `issue-scope-ledger.json`, the Branch Review Gate review report (`review.md`) and recorder artifact (`review-gate.json` by default), and context manifests (`implement.jsonl`, `check.jsonl`) for sub-agent-capable platforms.

```bash
python3 ./.trellis/scripts/task.py create "<title>" --slug <name>
python3 ./.trellis/scripts/task.py start <name>
python3 ./.trellis/scripts/task.py current --source
python3 ./.trellis/scripts/task.py finish
python3 ./.trellis/scripts/task.py archive <name>
python3 ./.trellis/scripts/task.py list [--mine] [--status <s>]
python3 ./.trellis/scripts/task.py add-context <name> <action> <file> <reason>
python3 ./.trellis/scripts/task.py validate <name>
python3 ./.trellis/scripts/task.py set-branch <name> <branch>
python3 ./.trellis/scripts/task.py set-base-branch <name> <branch>
python3 ./.trellis/scripts/task.py set-scope <name> <scope>
```

Run `python3 ./.trellis/scripts/task.py --help` for the authoritative list.

Guru Team companion scripts:

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --review-source independent-agent \
  --reviewer "trellis-check-agent" \
  --review-report ".trellis/tasks/<task>/review.md" \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
.trellis/guru-team/scripts/bash/check-review-gate.sh --json
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work
```

These are internal workflow helpers. `review-branch.sh` records and validates a
review that already happened; it is not the reviewer. `publish-pr.sh` is
intentionally omitted from the normal helper sequence because ordinary direct
publish calls are blocked; ordinary direct `finish-work.sh` calls are also
blocked unless the explicit `trellis-finish-work` entrypoint supplies its
intent marker. PR publish is triggered by that finish entrypoint after archive
and journal succeed. They are not new user-facing primary commands.

### Sub-agent Boundary

Trellis ships `trellis-implement`, `trellis-check`, and `trellis-research` sub-agents on agent-capable platforms. Guru Team keeps that official model:

- Phase 2 `trellis-check` is the implementation quality check step. It reviews the current task against specs, runs lint/typecheck/tests when appropriate, and may self-fix before commit.
- Phase 3 Branch Review Gate is a post-commit release gate. First, an AI/human review must inspect the complete branch diff from the intake base branch to `HEAD`, including docs, code, tests, Trellis artifacts, config, scripts, schemas, CI/CD workflows, Docker/Compose files, Kubernetes YAML, Kustomize overlays, database migrations, Makefiles, preset installer, Issue Scope Ledger, and publish readiness.
- Passing Phase 3 Branch Review Gate requires independent Agent review evidence. The main session may coordinate the review, inspect the report, and run the recorder, but the main session's own self-review must not pass the gate.
- On platforms with sub-agents, dispatch `trellis-check` or a dedicated review sub-agent to perform the evidence-gathering review for Phase 3. On inline platforms, stop before a passing gate unless an independent Agent review report is available through an external/team process.
- Codex defaults to `codex.dispatch_mode: sub-agent` in Guru Team projects. The main session's dispatch prompt must start with `Active task: <task path>`, and Codex sub-agents fall back to `task.py current --source` when that line is unavailable. Explicit `codex.dispatch_mode: inline` is a downgrade/debug mode.
- The sub-agent does not own the gate. The gate is valid only after the independent AI/human review has run, written task-local `{TASK_DIR}/review.md`, and `review-branch.sh --review-source independent-agent --review-report {TASK_DIR}/review.md` writes `{TASK_DIR}/review-gate.json` with summary, evidence, findings, reviewer identity, review source, review-report digest, base/head, and current `HEAD`.
- `review-branch.sh` is a recorder / validator, not a reviewer. It must receive the prior review result through `--summary`, `--evidence`, `--finding` / `--findings-file`, `--review-source independent-agent`, and `--review-report`; `--reviewer` is identity metadata only and cannot satisfy passed gate evidence by itself. Reviewer identities such as `codex-main-session`, `claude-main-session`, `cursor-main-session`, `*-main-session`, or `self-review` are rejected for a passing gate.
- Do not skip Phase 2 `trellis-check` just because Branch Review Gate exists; do not treat Phase 2 check success as permission to run `finish-work` without the Phase 3 artifact.

### Context Script

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode packages
python3 ./.trellis/scripts/get_context.py --mode phase --step <X.Y>
```

---

## Phase Index

```text
Phase 0: Intake  -> issue intake, Git base branch, worktree preflight
Phase 1: Plan    -> create task only after intake, then write planning artifacts
Phase 2: Execute -> implement only after task status is in_progress
Phase 3: Finish  -> verify, update spec, commit, Branch Review Gate, finish-work, publish PR
```

### Request Triage

- Do not require the user to explicitly run `trellis-start` before new work. In normal auto-bootstrap platforms, classify the user's natural-language request from the injected Trellis context, workflow-state, startup context, hook breadcrumb, or skill matcher.
- Simple conversation or non-file-changing small task: ask only whether this turn should create a Trellis task. If the user says no, skip Trellis for this session.
- Issue-backed, task-like, or file-changing request: first run Guru Team issue intake and Git base/worktree preflight before task creation. This includes pasted issue URLs, issue numbers, and clear development tasks. The first commands are:
  - `.trellis/guru-team/scripts/bash/check-env.sh --json`
  - `.trellis/guru-team/scripts/bash/prepare-task.sh --json "<user request, issue number, or issue URL>"`
- File-changing request with no active task: do not silently edit the current
  checkout. A current-checkout direct-edit override is allowed only after the
  user explicitly approves skipping GitHub issue, Trellis task, worktree, and
  branch creation/reuse for this turn.
- Ask for consent before creating a GitHub issue, worktree, branch, or Trellis task unless the user explicitly requested that side effect. Task creation consent is not current-checkout direct-edit consent.
- User approval to create a task is not approval to start implementation. Planning still happens first.

### Planning Artifacts

- `prd.md` — requirements, constraints, acceptance criteria, out of scope.
- `design.md` — technical design for complex tasks: boundaries, contracts, data flow, compatibility, tradeoffs, rollout / rollback.
- `implement.md` — execution plan for complex tasks: ordered checklist, validation commands, review gates, rollback points.
- `planning-approval.json` — start gate evidence for reviewed planning artifacts and user confirmation; `task.py start` is only a status write.
- `phase2-check.json` — Phase 2 `trellis-check` report for full task-scope quality coverage before commit and Branch Review Gate.
- `issue-scope-ledger.json` — task-level close/ref/followup scope; do not overload `source_issue`.
- `review-gate.json` — Branch Review Gate result for the reviewed HEAD.
- `implement.jsonl` / `check.jsonl` — spec and research manifests for sub-agent context. They do not replace `implement.md`.

Lightweight tasks may be PRD-only. Complex tasks must have `prd.md`, `design.md`, and `implement.md` before `task.py start`.

`prd.md`, `design.md`, `implement.md`, `planning-approval.json`, `phase2-check.json`, and human-readable fields in `review-gate.json` / `review.md` must be written in Chinese. If an external API, code symbol, command, or GitHub keyword must stay in English, keep the literal token and write the surrounding explanation in Chinese.

### Middle-platform Knowledge Gate

Apply this gate during planning, design, and implementation planning when the task may involve Guru Team middle-platform SDKs or frameworks. Examples include `go-guru`, `proto-guru`, go-guru ORM / repo proto generation conventions, server framework usage, Unity3D Guru SDKs, and Flutter Guru SDKs.

Configuration comes from `.trellis/guru-team/config.yml`:

- `middle_platform_knowledge.mode: off` — do not check, warn, block, or require persisted citations.
- `middle_platform_knowledge.mode: optional_warn` — default. Retrieve knowledge when available; if `guru-knowledge-center` MCP is unavailable, warn the user and continue.
- `middle_platform_knowledge.mode: required` — opt-in only. Block design and implementation progress if required retrieval cannot be performed or if no relevant knowledge/citation can be persisted.

Missing `middle_platform_knowledge.mode` MUST be interpreted as `optional_warn`. Do not ask the user to choose a mode just because the key is absent.

Do not assume a shell companion script can detect MCP availability. MCP availability is an AI-platform runtime capability: inspect the tools/capabilities available in the current session. If `guru-knowledge-center` is available and the task is relevant, query `project_domain=middle-platform` with the current task context. Persist retrieved knowledge or citations into task artifacts, such as:

- `design.md` section `中台知识依据` / `Framework Contracts`;
- `implement.md` section `实现前知识核对` / `Knowledge Checklist`;
- `{TASK_DIR}/research/middle-platform-knowledge.md`.

If the gate is not relevant to the task, record that it is not applicable in the planning artifact or final report when the task would otherwise appear framework-related.

### Repo Docs SSOT Reconciliation

Trellis task artifacts are task-scoped planning and evidence. They must cooperate with the repo's durable documentation source of truth instead of silently becoming a parallel long-term source.

During planning, inspect whether the target repo has a durable docs library, typically under `docs/`. Look for complete or partial categories such as:

- `docs/requirements/`;
- `docs/designs/`;
- `docs/testplans/`;
- deploy or operations guides;
- versioned design docs.

If complete or partial durable docs exist, `prd.md`, `design.md`, and `implement.md` should describe task-scoped deltas, decisions, evidence, and links to relevant durable docs. They should also list which durable docs need updates in this task, or why no durable docs update is needed.

Before commit, Branch Review Gate, finish-work, and publish, run Docs SSOT reconciliation:

- Did this task change a long-term product, architecture, API, data, deployment, operational, or test contract?
- Which `docs/` files were updated?
- Which task-artifact content was merged back into durable docs?
- Which content remains task history only?
- If durable docs were not updated, why is that acceptable, and does it require user confirmation?

Repos with no complete docs system must still record one explicit outcome:

- create new durable docs;
- append/update existing partial docs;
- or confirm that this repo intentionally has no durable docs SSOT yet and the task artifact remains archived evidence only.

<!-- Per-turn breadcrumb: shown when there is no active task (before Phase 1) -->

[workflow-state:no_task]
No active task. First classify the user's natural-language request; do not require the user to explicitly run `trellis-start`.
If the request includes an issue URL, issue number, clear development task, or file change, the first priority is Guru Team Phase 0 intake, not bare `task.py create`:
`.trellis/guru-team/scripts/bash/check-env.sh --json`
`.trellis/guru-team/scripts/bash/prepare-task.sh --json "<user request, issue number, or issue URL>"`
Default `prepare-task` is planner-only. After handoff review and user approval in `workspace_mode: worktree`, create the execution environment with `prepare-task --create-worktree --create-task` or an equivalent controlled Guru Team executor.
Do not silently edit the current checkout. Direct edits require explicit user approval to skip GitHub issue, Trellis task, worktree, and branch for this turn.
Ask for consent before creating a GitHub issue, worktree, branch, or Trellis task unless the user explicitly requested that side effect.
Task creation consent is not current-checkout direct-edit consent. Do not write `.trellis/tasks/` artifacts until consent is clear and preflight has a clear workspace.
[/workflow-state:no_task]

### Phase 0: Intake

- 0.1 Environment check `[required · once]`
- 0.2 GitHub issue intake `[required · once]`
- 0.3 Git base branch and worktree preflight `[required · once]`
- 0.4 Handoff review `[required · once]`

#### 0.1 Environment check `[required · once]`

Run:

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
```

Stop if `gh` is missing or unauthenticated. Tell the user to install GitHub CLI and run `gh auth login`.

#### 0.2 GitHub issue intake `[required · once]`

Run:

```bash
.trellis/guru-team/scripts/bash/prepare-task.sh --json "<user request, issue number, or issue URL>"
```

If the command exits with duplicate candidates, show the candidates and ask the user whether to reuse one or force a new issue. Never silently bind to a candidate the user did not provide.

If the command returns `proposed_issue` / `requires_confirmation`, stop before any GitHub or filesystem write. Show the duplicate-search result, proposed issue title/body, base branch, branch name, workspace path, and next confirmed command. If the user confirms issue creation, write the reviewed issue body to a temporary local file and rerun:

```bash
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --create-issue-confirmed \
  --issue-title "<reviewed issue title>" \
  --issue-body-file <reviewed-issue-body.md> \
  "<user request>"
```

#### 0.3 Git base branch and worktree preflight `[required · once]`

Use the preflight output from `prepare-task.sh`. The default command plans the worktree path but does not create it; `--create-worktree` or `--create-task` is required for filesystem workspace creation and is allowed only after a confirmed `source_issue` exists.

Planner output should include `preflight.base_freshness` when remote refs are available. Executor paths `--create-worktree` and `--create-task` must refresh the selected base before creating the worktree/branch: fetch the remote base, record local/remote HEAD evidence, fast-forward the local base only when safe, and fail closed on divergence or unknown freshness. Do not create a task branch from a stale local base.

If the selected base branch is not the current branch, report the current branch, selected base, and candidates. If the right base branch is ambiguous, ask the user to choose before creating the task.

Default to worktree mode. If the need for a new worktree is uncertain, ask the user before writing task files.

#### 0.4 Handoff review `[required · once]`

Before task creation, summarize:

- source issue URL
- proposed issue title/body when `source_issue` is still null
- duplicate-search result
- base branch
- base freshness evidence from `preflight.base_freshness`
- branch name
- workspace path
- current checkout and current branch
- create-task command or confirmed Guru Team executor command

Only after this is clear, create the Trellis task in the chosen workspace. When
`workspace_mode: worktree`, the normal executor is:

```bash
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --create-worktree \
  --create-task \
  "<source issue URL or approved request>"
```

Do not run bare `python3 ./.trellis/scripts/task.py create ...` in the source
checkout for issue-backed or file-changing Guru Team worktree tasks.

If the user explicitly requests a current-checkout direct-edit override instead
of creating or reusing a GitHub issue, Trellis task, worktree, and branch,
summarize the skipped artifacts, current checkout, current branch, dirty state,
side effects, changed-file scope, and commit/push boundary before editing.
Record the approval evidence in the task artifact, review report, or final
handoff when practical. The override is scoped to the described file edits and
does not approve commit, push, PR creation, or issue closure.

### Phase 1: Plan

- 1.0 Create task `[required · once]` (only after Phase 0)
- 1.1 Requirement exploration `[required · repeatable]`
- 1.2 Research `[optional · repeatable]`
- 1.3 Configure context `[required · once]` for sub-agent-dispatch platforms
- 1.4 Activate task `[required · once]` (artifact review, then `task.py start`)
- 1.5 Completion criteria

[workflow-state:planning]
Load `trellis-brainstorm`; stay in planning.
Confirm Guru Team intake handoff exists in the chosen workspace for durable tasks: `.trellis/guru-team/handoff.json`.
Run docs SSOT discovery and the middle-platform knowledge gate when relevant.
Lightweight: `prd.md` can be enough. Complex: finish `prd.md`, `design.md`, and `implement.md`; ask for review before `task.py start`.
Before `task.py start`, record and check `planning-approval.json`; missing or stale approval blocks implementation.
Sub-agent mode: curate `implement.jsonl` and `check.jsonl` as spec/research manifests before start.
[/workflow-state:planning]

[workflow-state:planning-inline]
Load `trellis-brainstorm`; stay in planning.
Confirm Guru Team intake handoff exists in the chosen workspace for durable tasks: `.trellis/guru-team/handoff.json`.
Run docs SSOT discovery and the middle-platform knowledge gate when relevant.
Lightweight: `prd.md` can be enough. Complex: finish `prd.md`, `design.md`, and `implement.md`; ask for review before `task.py start`.
Before `task.py start`, record and check `planning-approval.json`; missing or stale approval blocks implementation.
Inline mode: skip jsonl curation; Phase 2 reads artifacts/specs via `trellis-before-dev`.
[/workflow-state:planning-inline]

#### 1.0 Create task `[required · once]`

If Phase 0 only produced planner output, rerun `prepare-task.sh` after user approval.
Task creation consent is not current-checkout direct-edit consent, and it is not
permission to bypass the selected worktree, branch, or handoff.

When `workspace_mode: worktree`, prefer the single controlled executor path:

```bash
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --create-worktree \
  --create-task \
  "<source issue URL or approved request>"
```

This creates or reuses the chosen workspace, creates the branch and Trellis task
there, and writes `.trellis/guru-team/handoff.json` inside that workspace.

- Use `--create-worktree` to create or reuse the chosen workspace and write `.trellis/guru-team/handoff.json`; then run the `create_task_command` from that workspace handoff in `workspace_path`.
- Use `--create-task` only when the user approved task creation as part of the executor step; it creates or reuses the chosen workspace, creates the Trellis task, and writes the workspace handoff.

```bash
python3 ./.trellis/scripts/task.py create "<task title>" --slug <issue-or-unique-slug>
```

The bare `task.py create` command above is only a follow-up for controlled
cases where `prepare-task --create-worktree` has already written the handoff and
the shell/editor is operating inside the returned `workspace_path`. Do not run
it from the source checkout for issue-backed or file-changing Guru Team tasks.

Use `task.py set-branch`, `set-base-branch`, and `set-scope` to record handoff details only when the prepare script has not already done that.

Copy or materialize the Issue Scope Ledger seed from `.trellis/guru-team/handoff.json` into:

```text
{TASK_DIR}/issue-scope-ledger.json
```

If the companion script has not created it yet, create it with `primary_issue`, `close_issues`, `related_issues`, and `followup_issues`. The default `primary_issue` is the intake issue; it is only a close candidate until acceptance evidence and review coverage are present.

Run only `create` here. Save `start` for step 1.4.

#### 1.1 Requirement exploration `[required · repeatable]`

Load `trellis-brainstorm` and update `prd.md` immediately after each important user answer or repository finding.

Issue body and comments are intake evidence, not a replacement for `prd.md`. If issue comments conflict, prefer the latest explicit final closeout comment and record the chosen source in `prd.md`.

Discover the repo's durable docs SSOT before planning converges. Inspect `docs/` or equivalent long-lived documentation directories and record one of these in `prd.md`, `design.md`, or `implement.md`:

- complete docs exist and the task's affected durable docs are listed;
- partial docs exist and the task's update/follow-up responsibility is listed;
- no durable docs SSOT exists and task artifacts are temporary task evidence only unless this task creates docs.

Run the Middle-platform Knowledge Gate when the task may involve Guru Team middle-platform SDKs or frameworks. Persist citations or the unavailable-MCP warning before design and implementation artifacts are considered ready.

When scope changes, update `issue-scope-ledger.json` immediately:

- `primary_issue`: the intake/handoff issue that anchors the task.
- `close_issues`: issues this task explicitly promises to complete and close.
- `related_issues`: context, reusable mechanism, partial overlap, or references only.
- `followup_issues`: new scope, new bug, or expansion that should become a new Trellis task.

Do not put active task state, PR runtime state, or project-private business rules into a spec template or marketplace entry.

Only add a newly discovered issue to `close_issues` when all conditions hold:

- it belongs to the same delivery unit as the current task;
- it does not materially expand design boundary, test scope, or risk level;
- `prd.md`, `design.md`, and `implement.md` are updated when present;
- the user explicitly confirms this issue should be solved in the current task;
- Branch Review Gate later records coverage for that issue.

#### 1.2 Research `[optional · repeatable]`

Research can use local code, docs, issue comments, Trellis specs, MCP servers, and web search when needed. Persist durable findings under `{TASK_DIR}/research/`.

When `guru-knowledge-center` MCP is available and the task is middle-platform relevant, research MUST include a `project_domain=middle-platform` retrieval using the current task context. Prefer persisting a concise citation file such as `{TASK_DIR}/research/middle-platform-knowledge.md` and referencing it from `design.md` or `implement.md`.

When the configured mode is `optional_warn` and MCP is unavailable, warn visibly and record the warning in task artifacts or the final report. When the mode is `required`, stop until retrieval succeeds, the user changes the configuration, or the team provides an equivalent approved knowledge source.

#### 1.3 Configure context `[required · once]`

For sub-agent-dispatch platforms, curate `implement.jsonl` and `check.jsonl` with real spec/research entries. Seed `_example` rows do not count.

Inline Codex/Kilo/Antigravity/Devin workflows skip this step and load context through `trellis-before-dev`.

#### 1.4 Activate task `[required · once]`

After artifact review and explicit user approval, write the task-local start gate evidence:

```bash
.trellis/guru-team/scripts/bash/record-planning-approval.sh --json \
  --reviewer "codex-main-session" \
  --summary "中文规划审查结论" \
  --user-confirmation "用户确认进入实现的证据摘要"
.trellis/guru-team/scripts/bash/check-planning-approval.sh --json
```

Only after the check passes:

```bash
python3 ./.trellis/scripts/task.py start <task-dir>
```

Do not start implementation until the user approves the planning artifacts and `planning-approval.json` matches the current planning artifact hashes. `task.py start` is only a status transition; it is not planning review evidence.

#### 1.5 Completion criteria

| Condition | Required |
| --- | :---: |
| Guru Team handoff exists for durable tasks | yes |
| `prd.md` exists | yes |
| User confirms task should enter implementation | yes |
| `planning-approval.json` exists and `check-planning-approval` passes | yes |
| `task.py start` has been run | yes |
| `design.md` exists for complex tasks | yes |
| `implement.md` exists for complex tasks | yes |
| curated JSONL manifests exist for sub-agent dispatch | yes |
| Middle-platform Knowledge Gate handled when relevant | yes |
| Docs SSOT discovery recorded | yes |

### Phase 2: Execute

- 2.1 Implement `[required · repeatable]`
- 2.2 Quality check `[required · repeatable]`
- 2.3 Rollback `[on demand]`

[workflow-state:in_progress]
Flow: `trellis-implement` -> `trellis-check` -> `trellis-update-spec` -> commit (Phase 3.4) -> Branch Review Gate (Phase 3.5) -> stop. The next entry is `/trellis:finish-work` only when the user/session explicitly invokes it.
Do not push the branch, create a PR, call `publish-pr`, or invoke `finish-work` from `trellis-continue`; PR publish is owned by the explicit `trellis-finish-work` entrypoint after archive and journal succeed.
Before commit, record and check `phase2-check.json`; validation commands alone are not a complete `trellis-check`.
Main-session default on dispatch platforms: dispatch implement/check sub-agents. Dispatch prompt starts with `Active task: <task path from task.py current>`.
Sub-agent self-exemption: if already running as `trellis-implement` or `trellis-check`, do the work directly and do not spawn another Trellis implement/check agent.
Before edits, confirm knowledge gate and docs SSOT responsibilities from artifacts.
Read context: jsonl entries -> `prd.md` -> `design.md if present` -> `implement.md if present`.
[/workflow-state:in_progress]

[workflow-state:in_progress-inline]
Flow: `trellis-before-dev` -> edit -> `trellis-check` -> validation -> `trellis-update-spec` -> commit (Phase 3.4) -> Branch Review Gate (Phase 3.5) -> stop. The next entry is `/trellis:finish-work` only when the user/session explicitly invokes it.
Do not push the branch, create a PR, call `publish-pr`, or invoke `finish-work` from `trellis-continue`; PR publish is owned by the explicit `trellis-finish-work` entrypoint after archive and journal succeed.
Before commit, record and check `phase2-check.json`; validation commands alone are not a complete `trellis-check`.
Do not dispatch implement/check sub-agents in inline mode.
Before edits, confirm knowledge gate and docs SSOT responsibilities from artifacts.
Read context: `prd.md` -> `design.md if present` -> `implement.md if present`, plus relevant spec/research loaded by skills.
[/workflow-state:in_progress-inline]

#### 2.1 Implement `[required · repeatable]`

Dispatch or inline-implement according to the platform mode. Keep changes focused on the reviewed task artifacts and the source issue scope.

Before writing code or generated assets, confirm the Middle-platform Knowledge Gate result for any middle-platform-relevant work:

- `off`: no action required.
- `optional_warn`: use persisted citations when present; if unavailable, continue only after the user-visible warning is recorded.
- `required`: do not implement until retrieval evidence or an approved equivalent source is persisted.

Also follow the planning artifact's durable docs responsibilities. If implementation reveals that a long-term product, architecture, API, data, deployment, operational, or test contract changes, update the durable docs or return to Phase 1 to record why the task scope changed.

#### 2.2 Quality check `[required · repeatable]`

Run `trellis-check` or dispatch the check agent. The final check before commit must cover the full task scope, not only the latest implementation chunk.

After the AI/human check has completed, record the task-local check report:

```bash
.trellis/guru-team/scripts/bash/record-phase2-check.sh --json --pass \
  --checker "codex-main-session" \
  --summary "中文 trellis-check 结论" \
  --coverage requirements \
  --coverage design \
  --coverage code \
  --coverage tests \
  --coverage spec_sync \
  --coverage cross_layer \
  --coverage docs_ssot \
  --coverage deployment \
  --validation "验证命令|结果摘要"
.trellis/guru-team/scripts/bash/check-phase2-check.sh --json
```

Use `--finding 'P2|中文问题说明|path/to/file'` or `--findings-file findings.json` when check finds issues. P0/P1/P2 findings must be resolved before `--pass`. `record-phase2-check` is a recorder / validator; validation commands are evidence inside the report, not a substitute for complete `trellis-check` coverage.

#### 2.3 Rollback `[on demand]`

If implementation reveals a requirement defect, return to Phase 1 and update artifacts before continuing.

### Phase 3: Finish

- 3.2 Debug retrospective `[on demand]`
- 3.3 Spec update and Docs SSOT reconciliation `[required · once]`
- 3.4 Commit changes `[required · once]`
- 3.5 Branch Review Gate `[required · repeatable]`
- 3.6 Finish-work archive and journal `[required · once]`
- 3.7 Publish PR `[automatic after finish-work]`

[workflow-state:completed]
Code committed. Before `/trellis:finish-work`, confirm `review-gate.json` passed for the current HEAD. If missing or stale, run Branch Review Gate in Phase 3.5.
[/workflow-state:completed]

#### 3.2 Debug retrospective `[on demand]`

If the same bug or misunderstanding was fixed repeatedly, load `trellis-break-loop` and capture the prevention rule.

#### 3.3 Spec update and Docs SSOT reconciliation `[required · once]`

Load `trellis-update-spec` and decide whether `.trellis/spec/` needs a reusable update. If nothing should change, record that judgment in the final report.

Run Docs SSOT reconciliation before committing task work:

- record whether this task changed a long-term product, architecture, API, data, deployment, operational, or test contract;
- list durable docs updated by this task;
- list task-artifact content merged back into durable docs;
- list task-artifact content that remains task history only;
- if no durable docs were updated, record why this is acceptable and whether user confirmation is needed.

This reconciliation may live in `implement.md`, `review-gate.json` evidence, the final report, or a task research note, but Branch Review Gate must later record coverage for the outcome.

#### 3.4 Commit changes `[required · once]`

Before staging or committing, run:

```bash
.trellis/guru-team/scripts/bash/check-phase2-check.sh --json
```

If the report is missing, stale, lacks full coverage, lacks validation evidence, or contains unresolved P0/P1/P2 findings, return to Phase 2.2 and run the full check again.

Inspect dirty state, separate this task's changes from unrelated changes, draft a commit plan, and wait for user confirmation before committing.

The commit must include task work and relevant artifact updates through `prd.md`, `design.md`, `implement.md`, `issue-scope-ledger.json`, code, tests, config, scripts, schema, or preset installer changes. Do not include unrelated parallel work.

#### 3.5 Branch Review Gate `[required · repeatable]`

Run after the task work commit and before `finish-work`.

`review-branch.sh` validates that planning approval evidence exists and that a Phase 2 check report exists for the work that was committed. It uses post-commit audit semantics: planning approval may point at the approved pre-implementation HEAD as long as the approved artifact hashes still match, and Phase 2 check may point at an ancestor when only Trellis metadata changed after the check. Do not use Branch Review Gate to bypass `trellis-check`; Phase 2 check and Phase 3 review gate are separate artifacts.

##### 3.5.1 AI Review Prompt

Dispatch or obtain an independent reviewer/check Agent review. The main session
may prepare context and later record the result, but its own self-review cannot
pass Branch Review Gate. The review scope is the complete current branch diff
against the base branch selected during intake, normally:

```text
origin/<base>...HEAD
```

Use the handoff/task `base_branch`; do not guess from GitHub default branch.

The AI/human review must cover:

- docs and Trellis artifacts;
- durable docs SSOT reconciliation result and any `docs/` files that should have changed;
- code and tests;
- config;
- scripts;
- schemas;
- CI/CD workflows and release automation such as `.github/workflows/*`;
- Dockerfiles, Docker Compose files, and container entrypoint/startup scripts;
- Kubernetes manifests, Helm values when present, and Kustomize bases/overlays;
- database schema/migration/seed/backfill scripts;
- Makefiles in any directory when changed;
- preset installer and overlays;
- source-repo dogfood overlay drift check when the diff changes `trellis/presets/guru-team/overlays/` or installed dogfood copies;
- any generated or marketplace files changed by this task.

Findings use `P0`, `P1`, `P2`, `P3`:

- `P0/P1/P2`: block `finish-work`.
- `P3`: record but does not block.

Persist the independent review result in the conversation and in the task-local
artifact `{TASK_DIR}/review.md`. The review report must include concrete
summary/evidence, checked diff range, validation notes, deployment impact
judgment, Docs SSOT reconciliation, and findings, even when findings are empty.

Before writing `review.md`, `review-gate.json`, or any task artifact, confirm the
current working directory is the task's selected `workspace_path`, not the source
checkout or another worktree. Use the worktree-local absolute path for manual
file edits when the editing tool does not take an explicit working directory.
Relative task artifact paths such as `{TASK_DIR}/review.md` are relative to the
task worktree only.

##### 3.5.2 Gate Artifact Recorder

Only after the independent Agent review has completed with no P0/P1/P2 findings
and `{TASK_DIR}/review.md` exists, write the passing gate artifact. The pass path
must include `--review-source independent-agent` and `--review-report
{TASK_DIR}/review.md`; `--reviewer` may additionally record the independent
reviewer identity, but it cannot replace the review report:

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --review-source independent-agent \
  --reviewer "trellis-check-agent" \
  --review-report ".trellis/tasks/<task>/review.md" \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
```

or, when findings exist:

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json \
  --reviewer "trellis-check-agent" \
  --review-report ".trellis/tasks/<task>/review.md" \
  --summary "中文审查结论" \
  --finding 'P2|中文问题说明|path/to/file'
```

The artifact records base/head, diff command, conclusion, reviewer identity metadata, review source, review-report digest, summary, concrete evidence lines, findings, changed files, Issue Scope Ledger coverage, and validation evidence. It is written to `{TASK_DIR}/review-gate.json` by default.

Passing the gate is not a blank assertion. `--pass` requires `--review-source independent-agent`, a non-main-session `--reviewer`, a Chinese `--summary`, at least one concrete `--evidence` line from the actual review, and `--review-report` pointing at the task-local `review.md`. `review-gate.json` must record `review_source`, `review_report.path`, `sha256`, `size_bytes`, and `modified_at`. Use additional `--evidence` lines for important validation commands or review coverage notes. If the current platform/session cannot provide independent Agent review evidence, do not write a passing gate; stop with Branch Review Gate pending.

`--review-report` must be exactly the task-local `review.md`; do not pass `prd.md`, `design.md`, `phase2-check.json`, or any other task artifact as the review report.

When the diff includes `docs/` files, CI/CD, container, Kubernetes, Kustomize, database migration, or Makefile changes, the gate evidence or findings must explicitly name those changed assets and the validation or risk judgment used for them.

When the diff does not change deployment assets but the requirement or code changes the app's deployment shape, such as adding/removing an API service, CLI command, background worker, scheduled job, queue consumer, migration entrypoint, or runtime configuration, the gate evidence must still record whether Dockerfile, Docker Compose, GitHub Actions, Kubernetes/Kustomize, database migration, and Makefiles need updates. If no deployment asset update is needed, record the reason.

When the diff does not change durable docs but the task changes a long-term product, architecture, API, data, deployment, operational, or test contract, the gate evidence must record why no durable docs update is acceptable or produce a blocking finding. For repos with no durable docs SSOT, record the explicit no-docs outcome.

If a user manually commits on the command line, the next `trellis-continue` or `trellis-finish-work` must check whether `review-gate.json` matches the current HEAD. A missing, failed, stale, or reviewer-only gate blocks finish-work.

Do not implement this gate as a non-blocking task lifecycle hook. The workflow phase owns the review judgment; the companion script only records and validates the gate artifact.

#### 3.6 Finish-work archive and journal `[required · once]`

Start only after Branch Review Gate has passed for the current HEAD. If only
Trellis metadata such as `review.md` / `review-gate.json` remains uncommitted
after the reviewed code HEAD, finish-work may allow that metadata tail:

```bash
.trellis/guru-team/scripts/bash/check-review-gate.sh --json --allow-metadata-after-gate
```

Then run the internal Guru Team finish helper:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work
```

The `--from-trellis-finish-work` marker is required proof that the explicit finish entrypoint was invoked; `trellis-continue` must not add or synthesize it. Ordinary direct `finish-work.sh` calls fail before gate, archive, journal, push, or PR side effects. The helper then runs the normal finish-work actions: it verifies the passed gate has `review_report` digest evidence, rejects uncommitted non-metadata changes, archives the active task with `task.py archive`, records the session journal with `add_session.py`, commits any remaining Trellis metadata-only changes, then invokes publish.

When `--dry-run` is also passed with the explicit finish intent marker, the helper is a side-effect-free readiness preview: it validates the same gate, dirty-state, and PR body/readiness inputs, then prints the planned archive, journal, metadata commit, and publish actions without moving task files, writing journal entries, creating commits, pushing, or creating a PR.

`finish-work` may create Trellis metadata commits for archive and journal. These metadata commits do not invalidate the earlier code review gate; the helper only accepts Trellis metadata after the reviewed HEAD and blocks any code, config, script, schema, CI/CD, deployment, or preset change that appears after the gate.

#### 3.7 Publish PR `[automatic after finish-work]`

After archive and journal succeed, automatically publish the PR. This is not a new user-facing phase or command. The normal path is through the explicit `trellis-finish-work` entrypoint, which calls `finish-work.sh --from-trellis-finish-work`; `publish-pr.sh` is an internal helper and rejects ordinary direct calls. Direct `publish-pr.sh` is allowed only when `finish-work` calls it with its internal marker, or when an operator uses the explicit recovery/debug flag after `finish-work` already completed archive and journal but publish must be retried.

Before invoking finish-work, the AI must generate or review the PR body for a
GitHub reviewer who has no Trellis session context. The body is not a task
artifact summary. It must explain what behavior changed, which modules or
workflow surfaces are affected, how the change was validated, what Review Gate
covered, which issues are closed vs only referenced, and the real safety /
deployment impact. For non-draft publish, pass the reviewed body through
`--body-file <reviewed-pr-body.md>` or a readiness artifact passed as
`--body-artifact <pr-readiness.json>`; `generated` bodies are preview-only and
are not publish readiness evidence. The reviewed body/readiness files are task
metadata, should normally live under the current task directory before
finish-work, and are read from the archived task artifact after archive.

Publish behavior:

- push the current branch;
- create an open, non-draft GitHub PR;
- target the intake/task `base_branch`, not the GitHub default branch;
- write the PR title, headings, and body in Chinese;
- include Chinese sections for `变更摘要`, `影响范围`, `验证结果`, `Review Gate`, `Issue 关闭范围`, and `安全说明`;
- require an AI-reviewed `--body-file` / `--body-artifact` for non-draft publish; generated fallback bodies are allowed only for draft/preview paths and must still pass reviewer-readability checks;
- block non-draft publish if `变更摘要`, `影响范围`, `验证结果`, or `安全说明` are missing, empty, or low-information;
- never use phrases such as `当前 Trellis task`, `已提交实现与文档更新`, or `详见 artifact` as the main PR summary;
- use `Closes #xx` only for `close_issues` in `issue-scope-ledger.json`;
- use only `Refs #xx` or `Related #xx` semantics for `related_issues`;
- never close `followup_issues`.

The PR body quality judgment belongs to the AI readiness review. `publish-pr`
only validates objective structure, forbidden low-information phrases,
reviewed body-file/artifact presence, close/ref issue semantics, archive-path
resolution, and then executes the GitHub operation. It must not invent
reviewer-facing justification or replace the AI's release judgment with a
script-generated claim.

`trellis-continue` must never run this publish behavior or call `finish-work`. It stops after Branch Review Gate and waits for the user/session to explicitly invoke `trellis-finish-work`.

If any `close_issues` entry lacks acceptance/verification evidence, or the review gate does not record coverage for it, publish is blocked or the issue must be downgraded to `related_issues`.

### Rules

1. Phase 0 runs before durable Trellis task creation.
2. Task creation approval is not implementation approval.
3. Current-checkout direct edits with no active task require explicit user
   approval to skip GitHub issue, Trellis task, worktree, and branch for this
   turn; that approval does not approve commit, push, PR creation, or issue
   closure.
4. Planning artifacts must be persisted before implementation.
5. `prd.md`, `design.md`, `implement.md`, and review-gate human-readable fields are Chinese by default.
6. Daily user entry points are natural-language task requests, issue URLs or issue numbers, `trellis-continue`, and `trellis-finish-work`; `trellis-start` remains a fallback / explicit orientation entry for no-auto-injection platforms, disabled hooks, suspected bootstrap failures, or manual context reloads.
7. `review-branch`, `finish-work.sh`, and `publish-pr` are companion script subcommands, not user-facing phases; ordinary direct `finish-work.sh` and `publish-pr` calls are blocked before archive/push/PR.
8. Branch Review Gate belongs after commit and before finish-work; do not put it in a non-blocking hook.
9. Publish PR belongs after successful finish-work; do not ask users to run a separate publish flow.
10. Hooks are reminders and context injection only; the workflow contract owns the Guru Team process.
11. Companion scripts are local project assets under `.trellis/guru-team/`; do not modify Trellis upstream, `node_modules`, or generated copies in business repositories as the long-term source.
12. Long-term Guru Team rules live in this marketplace workflow, preset installer, companion scripts, overlays, and team docs.
13. If a platform command/skill entry must be overridden, use the Guru Team preset overlay and document its relationship with `trellis update`.
14. Spec templates may contain reusable conventions, review checklists, and artifact language rules; they must not contain active task state, Issue Scope Ledger instances, PR runtime state, or project-private business rules.
15. Missing `middle_platform_knowledge.mode` means `optional_warn`; `required` is opt-in only and `off` is opt-out only.
16. `guru-knowledge-center` availability is checked by the AI runtime from available tools/capabilities, not by shell scripts.
17. Trellis task artifacts may act as temporary task evidence, but durable repo docs remain the long-term SSOT when they exist.
18. Never print tokens, secrets, private keys, signed URLs, `.env` content, or database URLs.

### Issue Scope Ledger Rules

`handoff.source_issue` only records intake provenance. It is not the final set of issues that the PR closes.

Task-level `issue-scope-ledger.json` owns close/ref/followup semantics:

- `primary_issue`: the intake/handoff issue, default close candidate.
- `close_issues`: issues this task explicitly commits to fully resolving; PR body may use `Closes/Fixes/Resolves` only for these.
- `related_issues`: context, reuse, partial overlap, or non-closing references; PR body may use `Refs` or `Related`, never close keywords.
- `followup_issues`: expanded scope, newly found bug, or later work; never close from the current PR.

Default best practice for new issues, new bugs, or expanded requirements is to create a new Trellis task. Add a new issue to current `close_issues` only when it is the same delivery unit, does not materially expand boundary/risk/test scope, the planning artifacts are updated, the user explicitly confirms inclusion, and Branch Review Gate records coverage.
