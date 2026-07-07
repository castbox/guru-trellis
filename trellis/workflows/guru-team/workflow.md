# Guru Team Development Workflow

---

## Core Principles

1. **Plan before code** — figure out what to do before implementation starts.
2. **Issue-backed intake** — durable work starts from a GitHub Issue or from a neutral issue proposed by the workflow and created only after AI/human review.
3. **Git preflight before Trellis task files** — resolve base branch and workspace before `task.py create` writes task artifacts.
4. **Specs injected, not remembered** — follow `.trellis/spec/` and task artifacts instead of chat memory.
5. **Persist decisions** — requirements, research, implementation plans, and reusable lessons go to files.
6. **Incremental development** — one task, one branch, one workspace unless the user explicitly approves a current-checkout direct-edit override for this turn.
7. **Business project Chinese docs by default** — In target business repositories, `.trellis/spec/**`, `.trellis/tasks/**`, `docs/**` durable docs, `00-bootstrap-guidelines` generated docs SSOT, and human-readable workflow artifact fields are written in Chinese by default.
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

The default prepare command is side-effect-free intake/preflight planning for GitHub and filesystem writes: it may read an explicit issue and open duplicate candidates, then outputs source/proposed issue, base branch, branch name, workspace path, `create_task_command`, and `naming_quality`. Planner output is JSON only and does not write `.trellis/guru-team/handoff.json`, create a GitHub issue, worktree, branch, or Trellis task.

If no source issue was supplied, prepare writes `proposed_issue` and `requires_confirmation`. The AI must show the duplicate-search result, proposed issue title/body, base branch, branch name, and workspace path to the user. Only after confirmation may it rerun prepare with `--create-issue-confirmed --issue-title "<reviewed title>" --issue-body-file <reviewed-body-file>`.

After a confirmed source issue exists and the handoff plan has been reviewed, use `--create-worktree` or `--create-task` only with explicit user approval. Those executor paths create or reuse the chosen workspace and then write `.trellis/guru-team/handoff.json` inside that workspace. They must not be used as a shortcut around planning review. They also enforce `naming_quality`: if the generated or overridden slug, branch, workspace slug, or task slug is low-information, the executor fails before creating a worktree or Trellis task and asks the agent to pass semantic overrides.

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
- After reading the request, issue body, and comments, perform an intake clarity check before handoff review. If the problem statement, acceptance criteria, close scope, risk boundary, or implementation target is still ambiguous, load `trellis-brainstorm`, inspect repository evidence before asking user questions, and clarify the scope before creating or starting the Trellis task.
- For an existing source issue, decide whether clarified requirements should be captured as a new issue comment or by asking the user to update the original issue body. Use comments for additive clarifications, scope decisions, and user confirmations; use body edits only when the original body would mislead future intake and the edit has been reviewed.
- For a no-issue natural-language request, proposed issue title/body must incorporate the clarified scope before `--create-issue-confirmed`; do not create a generic placeholder issue and expect `prd.md` to repair the source issue later.
- Before creating an issue, search open issues for likely duplicates and show the result to the user.
- High-similarity candidates are never auto-bound. Ask the user whether to reuse the candidate or create a new issue.
- Proposed issue bodies use a neutral, reusable intake structure. GitHub issue creation requires `--create-issue-confirmed` and an AI/human reviewed body file; never let the default prepare command create the issue.
- If the task scope evolves during planning or execution, pause and ask the user whether the new requirement or referenced issue belongs in the current task, should be recorded as related context, or should become a follow-up issue / new Trellis task. Record the decision in both GitHub-visible issue evidence and task-local artifacts.
- Do not rely on `auto_create_issue` in older configs. It is a deprecated compatibility field and must not override the explicit confirmation requirement.
- Do not print tokens, secrets, private keys, signed URLs, `.env` content, or sensitive raw records in logs, docs, issues, or task artifacts.

### Git Preflight Rules

- `gh` must exist and `gh auth status` must pass before any GitHub read/write operation.
- Prefer `dev` or `develop` as base branch, then `main` or `master`.
- If the current branch is not the selected base, report the current branch, selected base, and candidates before proceeding.
- Default workspace is a Git worktree under `../<repo-name>-worktrees`.
- Report current checkout path, current branch, base branch, worktree path, branch name, dirty state, and existing worktrees.
- Slugs, branch names, worktree names, and task names must include an issue number or another unique id plus semantic English business tokens. Do not rely on Trellis date prefixes or auto-increment-like names for parallel work.
- If an issue title is Chinese, non-ASCII, or too generic to produce business tokens, the agent must read the issue and explicitly pass a semantic English short-name. `prepare-task` must not translate Chinese, convert titles to pinyin, or pretend it inferred business meaning from non-ASCII text.
- Recommended worktree/task slug format is `NNN-business-capability`; recommended branch format is `codex/NNN-business-capability`. Example: `052-resume-detail-inline-attachment-preview`.
- Use `--short-name`, `--workspace-slug`, `--task-slug`, and `--branch` as the deterministic interface from the agent's semantic judgment into the companion script. Explicit overrides still go through the same low-information naming gate.

### Handoff

Planner output, including output with a confirmed `source_issue`, sets `handoff_written: false` and remains stdout-only. After explicit approval for `--create-worktree` or `--create-task`, the executor writes `.trellis/guru-team/handoff.json` inside the chosen workspace. It must not dirty the source checkout merely because a new AI session or intake preflight ran. A written handoff contains:

- confirmed source issue number, URL, title, and creation flag; `source_issue` is intake provenance, not the final close scope
- handoff path and `handoff_written` state
- slug, task slug, task title, branch, base branch, workspace path
- `naming_quality` with `ok`, `reason`, `requires_semantic_name`, `current_slug`, and `suggested_override_flags`
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

Reference only: this command list documents the Trellis task CLI. In Guru Team
workflows, durable, issue-backed, task-like, or file-changing work enters
through Phase 0 `check-env` + `prepare-task` first. Do not use the bare
`task.py create` command below from the source checkout for Guru Team worktree
tasks. The bare create command is only a Phase 1.0 controlled follow-up after
`prepare-task` has returned or written the selected `workspace_path` and the
shell/editor is already operating inside that workspace.

Every task has its own directory under `.trellis/tasks/{MM-DD-name}/` holding `task.json`, `prd.md`, optional `design.md`, optional `implement.md`, optional `research/`, the task-level `issue-scope-ledger.json`, sub-agent/review assignment and status evidence (`agent-assignment.json`), the Branch Review Gate review report (`review.md`) and recorder artifact (`review-gate.json` by default), and context manifests (`implement.jsonl`, `check.jsonl`) for sub-agent-capable platforms.

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
  --agent-assignment ".trellis/tasks/<task>/agent-assignment.json" \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
.trellis/guru-team/scripts/bash/check-review-gate.sh --json
```

Before the explicit finish entrypoint runs, create or review the task-local PR
body at `{TASK_DIR}/pr-body.md`, then preview readiness before the formal
finish:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --body-file "{TASK_DIR}/pr-body.md" \
  --dry-run
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --body-file "{TASK_DIR}/pr-body.md"
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

- Guru Team workflow identity uses Chinese logical roles recorded in task artifacts, not platform UI names. Allowed roles are `实现代理`, `阶段二检查代理`, `问题发现审查代理`, `问题闭环审查代理`, and `最终放行审查代理`.
- `logical_role` is the Trellis process identity used in task artifacts, review reports, review gates, and final handoff. `agent_id` is the technical platform identity used for continuing or reusing an agent. `platform_nickname` is display-only and must not participate in gate decisions.
- Platform agent dispatch identifiers such as `trellis-implement`, `trellis-check`, `trellis-research`, channel-runtime `implement`, and channel-runtime `check` are technical API ids and must stay stable. User-facing agent labels should be Chinese where the platform supports it. Markdown-based agent files use Chinese headings and descriptions. Codex custom agents use Chinese `description`, but `nickname_candidates` must stay ASCII in current Codex releases or Codex ignores the agent file. If a platform still emits an automatic/random nickname, record that raw value in `platform_nickname` only and continue to use `logical_role` for workflow judgment.
- In default `sub-agent` mode, Guru Team has three mandatory execution boundaries:
  - implementation must be performed by `trellis-implement` or channel-runtime `implement` and produce an implementation handoff;
  - Phase 2 check must be performed by `trellis-check` or channel-runtime `check` and produce evidence that can be recorded in `phase2-check.json`;
  - Branch Review must be performed by an independent review sub-agent after the task work commit and produce task-local `review.md` before the main session records Branch Review Gate.
- The main session coordinates planning, dispatch, waiting, resume/replacement decisions, evidence recording, commit, recorder/validator calls, and finish preparation. It must not replace the three mandatory sub-agent boundaries with its own implementation, its own Phase 2 check, its own Branch Review, or script validation output.
- Inline mode or self-exemption is valid only when explicit artifact evidence explains why the default `sub-agent` boundary does not apply. A sub-agent that is already running as `trellis-implement` / `trellis-check` must do its own role directly and return the required handoff/report; a main session in default `sub-agent` mode cannot claim that exemption for itself. Missing implement, check, or review sub-agent evidence fails closed.
- `wait_agent`, `trellis channel wait`, or an equivalent wait command timing out only means this wait window ended without a final completion event. It is not evidence that the sub-agent is stuck, failed, should stop, or that its partial output is acceptable completion evidence.
- Distinguish long total runtime from stale state. A sub-agent may run for more than an hour. If it is still producing output, changing the worktree in-scope, running validations, emitting channel events, or otherwise showing meaningful progress, continue waiting and record that observation when needed. Stale assessment must be based on no observable progress for a recent window, default at least 5 minutes, not on total runtime.
- When a main session dispatches or reuses a sub-agent, record the AI/human decision in `{TASK_DIR}/agent-assignment.json`. The recorder can be:

```bash
.trellis/guru-team/scripts/bash/record-agent-assignment.sh --json \
  --logical-role "实现代理" \
  --agent-id "019f..." \
  --platform-nickname "Gibbs" \
  --reason "中文分配原因"
.trellis/guru-team/scripts/bash/check-agent-assignment.sh --json
```

- When review rounds reuse or replace a reviewer, record the review round and reuse decision. The script validates objective fields only; it does not decide whether reuse is semantically correct.
- When a wait timeout, stale assessment, interruption, unfinished termination, same-agent resume, replacement start, completion, or explicit failure happens, record `status_events[]` in the same task-local `agent-assignment.json`. The companion script records objective fields only; the AI/human workflow decides whether the agent is stale, should continue, should be interrupted, or should be replaced:

```bash
.trellis/guru-team/scripts/bash/record-agent-assignment.sh --json \
  --logical-role "实现代理" \
  --agent-id "<technical-agent-id-or-empty>" \
  --platform-nickname "<display-name-or-empty>" \
  --status-event wait-timeout \
  --decision continue-waiting \
  --reason "等待窗口 timeout，但最近仍有输出和工作区变化，继续等待。" \
  --last-observed-progress-at "2026-07-07T00:00:00Z" \
  --workspace-evidence "git diff 仍在变化。" \
  --running-command-evidence "验证命令仍在运行。"
```

- Before soft interrupt, hard stop, or terminating an unfinished sub-agent, record the latest output/change time, worktree/channel/diff evidence, running command evidence, decision, reason, and handoff summary. If an unfinished agent is interrupted or terminated, recover the same technical `agent_id` or start a replacement agent with the predecessor output/channel log summary, current diff, task artifacts, remaining checklist, and blocking gate. Continue until a later `completed` or explicit `failed` status event closes that recovery chain.
- Unfinished, interrupted, terminated, or unclosed replacement output is intermediate evidence only. It must not be treated as implementation completion, Phase 2 check pass evidence, or Branch Review Gate pass evidence. `review-branch.sh --pass` validates objective ledger completeness and fails closed when `status_events[]` contains an unclosed `terminated-unfinished` chain.
- Phase 2 `trellis-check` is the implementation quality check step. It reviews the current task against specs, runs lint/typecheck/tests when appropriate, and may self-fix before commit. `phase2-check.json` is the Guru Team artifact that records the completed `trellis-check` AI judgment, coverage, validations, findings, and dirty-path evidence; it is not the Trellis-native step itself and recorder/validator scripts cannot substitute for that AI check.
- Phase 3 Branch Review Gate is a post-commit release gate. First, an AI/human review must inspect the complete branch diff from the intake base branch to `HEAD`, including docs, code, tests, Trellis artifacts, config, scripts, schemas, CI/CD workflows, Docker/Compose files, Kubernetes YAML, Kustomize overlays, database migrations, Makefiles, preset installer, Issue Scope Ledger, and publish readiness.
- Passing Phase 3 Branch Review Gate requires independent Agent review evidence. The main session may coordinate the review, inspect the report, and run the recorder, but the main session's own self-review must not pass the gate.
- Phase 3 also performs a post-commit Phase 2 audit: `phase2-check.json` is recorded before commit with the then-current `dirty_paths`, and `review-branch.sh` later verifies that committed non-metadata task work after the recorded HEAD is covered by those paths. Do not re-record Phase 2 after the task work commit just to make HEAD match; return to Phase 2 only when new non-metadata changes appear or evidence is invalid.
- In default `sub-agent` mode, dispatch `trellis-check` in an independent review role or a dedicated review sub-agent to perform the evidence-gathering review for Phase 3. The review sub-agent reviews docs, code, tests, artifacts, and diff evidence as an AI reviewer; it must not continue implementation, patch Phase 2 gaps, or run Guru Team recorder/validator extension scripts such as `review-branch.sh`, `check-review-gate.sh`, `record-agent-assignment.sh`, or `record-*` as part of its review. On inline platforms, stop before a passing gate unless an independent Agent review report is available through an external/team process.
- Codex defaults to `codex.dispatch_mode: sub-agent` in Guru Team projects. The main session's dispatch prompt must start with `Active task: <task path>`, and Codex sub-agents fall back to `task.py current --source` when that line is unavailable. Explicit `codex.dispatch_mode: inline` is a downgrade/debug mode.
- The sub-agent does not own the gate. The gate is valid only after the independent AI/human review has run, written task-local `{TASK_DIR}/review.md`, and `review-branch.sh --review-source independent-agent --review-report {TASK_DIR}/review.md --agent-assignment {TASK_DIR}/agent-assignment.json` writes `{TASK_DIR}/review-gate.json` with summary, evidence, findings, reviewer identity, review source, review-report digest, agent-assignment digest, base/head, and current `HEAD`.
- `review-branch.sh` is a recorder / validator, not a reviewer. It must receive the prior review result through `--summary`, `--evidence`, `--finding` / `--findings-file`, optional `--observation` / `--followup-candidate`, `--review-source independent-agent`, and `--review-report`; `--reviewer` is identity metadata only and cannot satisfy passed gate evidence by itself. Reviewer identities such as `codex-main-session`, `claude-main-session`, `cursor-main-session`, `*-main-session`, or `self-review` are rejected for a passing gate.
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
- `design.md` — technical design before implementation: boundaries, contracts, data flow, compatibility, tradeoffs, rollout / rollback.
- `implement.md` — execution plan before implementation: ordered checklist, validation commands, review gates, rollback points.
- `planning-approval.json` — start gate evidence that the main session displayed links to `prd.md`, `design.md`, and `implement.md`, then received explicit post-planning user confirmation; `task.py start` is only a status write.
- `phase2-check.json` — Phase 2 `trellis-check` report for full task-scope quality coverage before commit and Branch Review Gate.
- `issue-scope-ledger.json` — task-level close/ref/followup scope; do not overload `source_issue`.
- `agent-assignment.json` — task-local sub-agent assignment ledger with Chinese logical roles, technical `agent_id`, display-only `platform_nickname`, HEAD evidence, review rounds, and reuse/replacement decisions.
- `review-gate.json` — Branch Review Gate result for the reviewed HEAD.
- `implement.jsonl` / `check.jsonl` — spec and research manifests for sub-agent context. They do not replace `implement.md`.

Guru Team implementation tasks must have `prd.md`, `design.md`, and `implement.md` before `task.py start`; a Phase 0 handoff approval never substitutes for this post-planning review.

### Business Project Documentation Language

For repositories that install and use the Guru Team workflow as a business project workflow, human-readable documentation is Chinese by default:

- `.trellis/spec/**` project conventions and bootstrap outputs;
- `.trellis/tasks/**` task artifacts, including `prd.md`, `design.md`, `implement.md`, `review.md`, and human-readable fields in JSON artifacts such as `planning-approval.json`, `phase2-check.json`, `agent-assignment.json`, and `review-gate.json`;
- `docs/**` durable requirements, design, test, deploy, operations, and versioned docs;
- docs SSOT files created or completed by `00-bootstrap-guidelines`;
- workflow/helper artifact fields that are meant for humans to read, including summaries, evidence, findings, observations, follow-up candidates, PR titles, and PR bodies.

Keep literal command names, file paths, GitHub keywords, configuration keys, external API names, code symbols, and other required tokens in English when needed, but write the surrounding explanation in Chinese.

The `guru-trellis` source repository itself is a public extension repository, not a target business project. Its public README/source comments/script help/marketplace metadata may remain English or bilingual when that is clearer for distribution, interoperability, or literal API compatibility. Do not use that exception to keep business-project `.trellis/spec/**`, `.trellis/tasks/**`, `docs/**`, or bootstrap-generated docs SSOT in English.

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

Any durable docs created or updated through this workflow, including docs SSOT files created or completed by `00-bootstrap-guidelines`, must follow the business-project Chinese documentation default above.

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

Planner output must include `preflight.base_freshness` based on a fresh `git fetch origin <base>` or an explicit remote-confirmation failure status. Treat `fetch_performed: false` with `fresh: true` as invalid evidence. If local base is behind the refreshed remote, planner output must report `fresh: false`, `status: stale`, and keep `fast_forwarded: false`; if local and remote diverged, it must report `status: diverged` or fail closed. Executor paths `--create-worktree` and `--create-task` must refresh the selected base again before creating the worktree/branch: fetch the remote base, record local/remote HEAD evidence, fast-forward the local base only when safe, and fail closed on divergence or unknown freshness. Do not create a task branch from a stale local base.

If the selected base branch is not the current branch, report the current branch, selected base, and candidates. If the right base branch is ambiguous, ask the user to choose before creating the task.

Default to worktree mode. If the need for a new worktree is uncertain, ask the user before writing task files.

#### 0.4 Handoff review `[required · once]`

Before task creation, summarize:

- source issue URL
- proposed issue title/body when `source_issue` is still null
- duplicate-search result
- naming quality result, including whether `--short-name`, `--workspace-slug`, `--task-slug`, or `--branch` semantic overrides are required
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
- 1.4 Explicit planning review `[required · once]` (show links, wait for user confirmation)
- 1.5 Activate task `[required · once]` (`planning-approval.json`, then `task.py start`)
- 1.6 Completion criteria

[workflow-state:planning]
Load `trellis-brainstorm`; stay in planning.
Confirm Guru Team intake handoff exists in the chosen workspace for durable tasks: `.trellis/guru-team/handoff.json`.
Run docs SSOT discovery and the middle-platform knowledge gate when relevant.
Finish `prd.md`, `design.md`, and `implement.md`; then visibly show links to all three task-local planning documents and stop for explicit post-planning user confirmation before `task.py start`.
Before `task.py start`, record and check `planning-approval.json` with `user_confirmation.source=explicit-post-planning-review`; Phase 0 handoff confirmation or generic workflow confirmation must fail closed. Missing or stale approval blocks implementation and Phase 2 check recording.
Sub-agent mode: curate `implement.jsonl` and `check.jsonl` as spec/research manifests before start.
[/workflow-state:planning]

[workflow-state:planning-inline]
Load `trellis-brainstorm`; stay in planning.
Confirm Guru Team intake handoff exists in the chosen workspace for durable tasks: `.trellis/guru-team/handoff.json`.
Run docs SSOT discovery and the middle-platform knowledge gate when relevant.
Finish `prd.md`, `design.md`, and `implement.md`; then visibly show links to all three task-local planning documents and stop for explicit post-planning user confirmation before `task.py start`.
Before `task.py start`, record and check `planning-approval.json` with `user_confirmation.source=explicit-post-planning-review`; Phase 0 handoff confirmation or generic workflow confirmation must fail closed. Missing or stale approval blocks implementation and Phase 2 check recording.
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

Run only `create` here. Save `start` for step 1.5.

#### 1.1 Requirement exploration `[required · repeatable]`

Load `trellis-brainstorm` and update `prd.md` immediately after each important user answer or repository finding.

Issue body and comments are intake evidence, not a replacement for `prd.md`. If issue comments conflict, prefer the latest explicit final closeout comment and record the chosen source in `prd.md`.

When intake evidence is incomplete, use `trellis-brainstorm` before implementation planning. Ask only for product intent, scope, risk tolerance, or close/ref decisions that cannot be answered from repository evidence. After each material clarification, update `prd.md` immediately and decide whether the GitHub source of truth needs one of these updates:

- append a comment to the current source issue with the clarified scope, user confirmation, or final closeout interpretation;
- ask the user to update the original issue body when the body has become misleading for future sessions;
- create or propose a new issue when the clarification is a separate delivery unit or materially expands the current task.

Do not let task artifacts become the only record of changed requirements when a GitHub issue anchors the work. The issue or a related issue must carry enough public evidence for a later session to understand why the task scope changed.

Discover the repo's durable docs SSOT before planning converges. Inspect `docs/` or equivalent long-lived documentation directories and record one of these in `prd.md`, `design.md`, or `implement.md`:

- complete docs exist and the task's affected durable docs are listed;
- partial docs exist and the task's update/follow-up responsibility is listed;
- no durable docs SSOT exists and task artifacts are temporary task evidence only unless this task creates docs.

Run the Middle-platform Knowledge Gate when the task may involve Guru Team middle-platform SDKs or frameworks. Persist citations or the unavailable-MCP warning before design and implementation artifacts are considered ready.

Scope Change Gate: when scope changes, first stop and ask the user how to classify the new requirement or referenced issue unless the user already made that classification explicit. Then update `issue-scope-ledger.json` immediately:

- `primary_issue`: the intake/handoff issue that anchors the task.
- `close_issues`: issues this task explicitly promises to complete and close.
- `related_issues`: context, reusable mechanism, partial overlap, or references only.
- `followup_issues`: new scope, new bug, or expansion that should become a new Trellis task.

The same decision must also leave GitHub-visible evidence: add a comment to the current issue, add a comment to the referenced issue, or create/propose a follow-up issue. Companion scripts may execute deterministic writes after reviewed text is supplied, but they must not decide whether the new scope belongs in the current task.

Do not put active task state, PR runtime state, or project-private business rules into a spec template or marketplace entry.

Only add a newly discovered issue to `close_issues` when all conditions hold:

- it belongs to the same delivery unit as the current task;
- it does not materially expand design boundary, test scope, or risk level;
- `prd.md`, `design.md`, and `implement.md` are updated;
- the user explicitly confirms this issue should be solved in the current task;
- Branch Review Gate later records coverage for that issue.

#### 1.2 Research `[optional · repeatable]`

Research can use local code, docs, issue comments, Trellis specs, MCP servers, and web search when needed. Persist durable findings under `{TASK_DIR}/research/`.

When `guru-knowledge-center` MCP is available and the task is middle-platform relevant, research MUST include a `project_domain=middle-platform` retrieval using the current task context. Prefer persisting a concise citation file such as `{TASK_DIR}/research/middle-platform-knowledge.md` and referencing it from `design.md` or `implement.md`.

When the configured mode is `optional_warn` and MCP is unavailable, warn visibly and record the warning in task artifacts or the final report. When the mode is `required`, stop until retrieval succeeds, the user changes the configuration, or the team provides an equivalent approved knowledge source.

#### 1.3 Configure context `[required · once]`

For sub-agent-dispatch platforms, curate `implement.jsonl` and `check.jsonl` with real spec/research entries. Seed `_example` rows do not count.

Inline Codex/Kilo/Antigravity/Devin workflows skip this step and load context through `trellis-before-dev`.

#### 1.4 Explicit planning review `[required · once]`

After `prd.md`, `design.md`, and `implement.md` are complete, the main session
must visibly present all three task-local planning documents to the user and
then stop for an explicit post-planning confirmation. The message must include
clickable or absolute links to:

- `{TASK_DIR}/prd.md`
- `{TASK_DIR}/design.md`
- `{TASK_DIR}/implement.md`

The same message must state that, until the user confirms after seeing those
links, the workflow will not enter implementation, will not dispatch
`trellis-implement` / channel `implement`, and will not record
`phase2-check.json`.

The user's Phase 0 handoff approval to create a GitHub issue, worktree, branch,
or Trellis task is not planning approval. Do not reuse a Phase 0 confirmation,
generic "continue" consent, or historical `planning-approval.json` with
`user_confirmation.source=workflow`. If `planning-approval.json` is missing,
stale, has old schema/source, or no longer matches the current
`prd.md`/`design.md`/`implement.md` digests, show the three links again and wait
for a fresh explicit post-planning confirmation.

#### 1.5 Activate task `[required · once]`

After the explicit post-planning confirmation, write the task-local start gate evidence:

```bash
.trellis/guru-team/scripts/bash/record-planning-approval.sh --json \
  --reviewer "codex-main-session" \
  --summary "中文规划审查结论" \
  --user-confirmation "用户在看到 prd.md、design.md、implement.md 三个链接后确认进入实现" \
  --confirmation-source explicit-post-planning-review
.trellis/guru-team/scripts/bash/check-planning-approval.sh --json
```

Only after the check passes:

```bash
python3 ./.trellis/scripts/task.py start <task-dir>
```

Do not start implementation until the user approves the displayed planning
artifacts and `planning-approval.json` matches the current planning artifact
hash, size, and modified-time metadata. `task.py start` is only a status
transition; it is not planning review evidence.

#### 1.6 Completion criteria

| Condition | Required |
| --- | :---: |
| Guru Team handoff exists for durable tasks | yes |
| `prd.md` exists | yes |
| `design.md` exists | yes |
| `implement.md` exists | yes |
| Main session displayed links to `prd.md`, `design.md`, and `implement.md` after generating them | yes |
| User confirms task should enter implementation after seeing the three planning links | yes |
| `planning-approval.json` exists and `check-planning-approval` passes | yes |
| `task.py start` has been run | yes |
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
Before dispatching `trellis-implement` / channel `implement` or recording `phase2-check.json`, run `.trellis/guru-team/scripts/bash/check-planning-approval.sh --json`; missing, stale, old-schema, or non-`explicit-post-planning-review` approval blocks Phase 2.
Before commit, record and check `phase2-check.json`; it records completed `trellis-check` AI evidence, and validation commands or recorder success alone are not a complete check.
Main-session default on dispatch platforms: dispatch `trellis-implement` / channel `implement`, wait for an implementation handoff, then dispatch `trellis-check` / channel `check`. Dispatch prompt starts with `Active task: <task path from task.py current>`. The main session may coordinate and record evidence, but it must not directly implement or directly check in default `sub-agent` mode.
After dispatching an implement/check sub-agent, record `实现代理` or `阶段二检查代理` in `agent-assignment.json`; prefer the Chinese UI nickname configured by the agent file when available. If the platform does not expose `agent_id` or nickname, keep the field as an empty string and explain that fact in the Chinese reason. A wait timeout is only a wait-window result; do not terminate or summarize a still-progressing sub-agent because total runtime is long. Record `status_events[]` for wait timeout, progress observed, stale assessment, continue-waiting, resume/replacement, unfinished termination, completion, or explicit failure.
Sub-agent self-exemption: if already running as `trellis-implement` or `trellis-check`, do the work directly, do not spawn another Trellis implement/check agent, and return the role-specific handoff/report as artifact evidence. Main-session inline/self-exemption needs explicit artifact evidence; otherwise missing sub-agent evidence fails closed.
Before edits, confirm knowledge gate and docs SSOT responsibilities from artifacts.
Read context: jsonl entries -> `prd.md` -> `design.md` -> `implement.md`.
[/workflow-state:in_progress]

[workflow-state:in_progress-inline]
Flow: `trellis-before-dev` -> edit -> `trellis-check` -> validation -> `trellis-update-spec` -> commit (Phase 3.4) -> Branch Review Gate (Phase 3.5) -> stop. The next entry is `/trellis:finish-work` only when the user/session explicitly invokes it.
Do not push the branch, create a PR, call `publish-pr`, or invoke `finish-work` from `trellis-continue`; PR publish is owned by the explicit `trellis-finish-work` entrypoint after archive and journal succeed.
Before editing or recording `phase2-check.json`, run `.trellis/guru-team/scripts/bash/check-planning-approval.sh --json`; missing, stale, old-schema, or non-`explicit-post-planning-review` approval blocks inline Phase 2.
Before commit, record and check `phase2-check.json`; validation commands alone are not a complete `trellis-check`.
Do not dispatch implement/check sub-agents in inline mode.
Before edits, confirm knowledge gate and docs SSOT responsibilities from artifacts.
Read context: `prd.md` -> `design.md` -> `implement.md`, plus relevant spec/research loaded by skills.
[/workflow-state:in_progress-inline]

#### 2.1 Implement `[required · repeatable]`

Dispatch or inline-implement according to the platform mode only after
`check-planning-approval.sh --json` passes for the current task. In default
`sub-agent` mode, the main session must dispatch `trellis-implement` or
channel-runtime `implement`; it may not directly edit files and later present
that work as `实现代理` evidence. Keep changes focused on the reviewed task
artifacts and the source issue scope.

On sub-agent-capable platforms, the main session records implementation assignment after dispatch:

```bash
.trellis/guru-team/scripts/bash/record-agent-assignment.sh --json \
  --logical-role "实现代理" \
  --agent-id "<technical-agent-id-or-empty>" \
  --platform-nickname "<display-name-or-empty>" \
  --reason "中文说明为什么本轮实现由该 agent 承担"
```

The assignment artifact is evidence of an AI/human decision already made by the workflow. The companion script must not choose the agent or infer whether reuse is appropriate.

The implementation handoff must include files changed, key requirement/design carryover points, verification already run or explicitly deferred to Phase 2, remaining risks or a no-known-risk statement, completion status, and concrete focus areas for the later `trellis-check`. Do not report implementation completion until the requested scope is actually complete and verification status is known.

When a dispatched implementation agent hits a wait timeout, first inspect recent output, worktree changes, validation progress, and channel events. If progress exists, keep waiting and optionally record `--status-event wait-timeout --decision continue-waiting` or `--status-event progress-observed`. Only after at least the stale window with no observable progress should the AI/human workflow assess stale state and record `--status-event stale-assessed`; interruption or unfinished termination must be followed by `resume-same-agent` or `replacement-started`, then a later `completed` or `failed` event for the same recovery chain.

Before writing code or generated assets, confirm the Middle-platform Knowledge Gate result for any middle-platform-relevant work:

- `off`: no action required.
- `optional_warn`: use persisted citations when present; if unavailable, continue only after the user-visible warning is recorded.
- `required`: do not implement until retrieval evidence or an approved equivalent source is persisted.

Also follow the planning artifact's durable docs responsibilities. If implementation reveals that a long-term product, architecture, API, data, deployment, operational, or test contract changes, update the durable docs or return to Phase 1 to record why the task scope changed.

#### 2.2 Quality check `[required · repeatable]`

Run `trellis-check` or dispatch the check agent. In default `sub-agent` mode, the main session must dispatch `trellis-check` or channel-runtime `check`; it may not directly run a few validations or inspect the diff and then present that as `阶段二检查代理` evidence. The final check before commit must cover the full task scope, not only the latest implementation chunk.

When dispatching a Phase 2 check agent, record `阶段二检查代理` in `agent-assignment.json` before or immediately after the check handoff. This is separate from `phase2-check.json`: assignment records who took the logical role; `phase2-check.json` records the check judgment and evidence.

Before recording a passing Phase 2 check, confirm the check did not rely on a terminated-unfinished implementation/check sub-agent's partial output. If `agent-assignment.json.status_events[]` contains unfinished termination, the same agent or a replacement must have continued the work and reached `completed` or explicit `failed`; otherwise return to implementation/check handoff instead of passing Phase 2.

After the `trellis-check` AI check has completed, record the task-local check report:

```bash
.trellis/guru-team/scripts/bash/record-phase2-check.sh --json --pass \
  --checker "trellis-check-agent" \
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

Use `--finding 'P2|中文问题说明|path/to/file'` or `--findings-file findings.json` when check finds issues. P0/P1/P2 findings must be resolved before `--pass`. `record-phase2-check` is a recorder / validator; validation commands and script success are evidence inside the report, not a substitute for complete `trellis-check` coverage.

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
Fallback/legacy closeout breadcrumb for an active task already marked `completed`; the normal path is `trellis-continue` stops after Branch Review Gate and the user/session explicitly invokes `/trellis:finish-work`.
If `review-gate.json` is missing, failed, stale for the current HEAD, or reviewer-only, return to Phase 3.5 for independent review and the `review-branch` recorder.
If the gate passed, create or review task-local PR readiness: `{TASK_DIR}/pr-body.md` via `--body-file "{TASK_DIR}/pr-body.md"` or a task-local `--body-artifact`.
Run a dry-run first:
`.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work --body-file "{TASK_DIR}/pr-body.md" --dry-run`
Review the dry-run output, then run the same command without `--dry-run`.
Finish-work accepts only Trellis metadata tail such as `review.md`, `review-gate.json`, `pr-body.md`, and `pr-readiness.json`; any non-metadata dirty path or non-metadata committed drift must go back to `trellis-continue` / Phase 2-3.
Do not call `publish-pr` directly; normal publish is only through the explicit `trellis-finish-work` closeout after archive and journal.
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

`review-branch.sh` validates that planning approval evidence exists and that a Phase 2 check report exists for the work that was committed. It uses post-commit audit semantics: planning approval may point at the approved pre-implementation HEAD as long as the approved artifact hashes still match, and Phase 2 check may point at an ancestor when later non-metadata committed paths are covered by the recorded `phase2-check.json.dirty_paths` or when the later tail is Trellis metadata only. Branch Review Gate and publish readiness metadata may change after Phase 2 because final review and release readiness happen after the work commit; stale Phase 2 digest entries for task-local `issue-scope-ledger.json`, `pr-body.md`, `pr-readiness.json`, `agent-assignment.json`, `review.md`, and `review-gate.json` may be ignored only in this post-commit audit and are revalidated by the gate or publish validators before pass or publish. This exception must not apply to source, config, script, docs, schema, preset, overlay, or other non-metadata paths. If the commit contains non-metadata paths that were not recorded in Phase 2 dirty paths, or the current working tree has non-metadata dirty paths, return to Phase 2 instead of re-recording evidence after the fact. Do not use Branch Review Gate to bypass `trellis-check`; Phase 2 check and Phase 3 review gate are separate artifacts.

##### 3.5.1 AI Review Prompt

Dispatch or obtain an independent reviewer/check Agent review. In default
`sub-agent` mode this must be a real review sub-agent, using `trellis-check` in
a review role or a dedicated review sub-agent. The main session may prepare
context and later record the result, but its own self-review cannot pass Branch
Review Gate. The review sub-agent must not continue implementation or fill
missing Phase 2 check work; if it finds that implement/check evidence is
missing or stale, it reports a blocking finding and the workflow returns to the
earlier phase. The review scope is the complete current branch diff against the
base branch selected during intake, normally:

```text
origin/<base>...HEAD
```

Use the handoff/task `base_branch`; do not guess from GitHub default branch.

Before or immediately after dispatching the independent review, record the reviewer logical role in `agent-assignment.json`:

- first issue-finding review uses `问题发现审查代理`;
- follow-up review that verifies fixes may use `问题闭环审查代理`;
- the pass/final release review uses `最终放行审查代理`.

Use `review_rounds[]` to record `round`, `reviewed_head`, `findings_count`, `reuse_policy`, and `reuse_decision`; `round` values must be unique and strictly increasing in recorded order so the final round is unambiguous. If any review round finds a finding, including a previous `最终放行审查代理` round that discovered a new issue, that same technical `agent_id` must later be reused as `问题闭环审查代理` and record `findings_count: 0` with `reuse_decision: reuse-for-closure` to confirm its own finding is closed. Only after every finding owner has a later successful closure round may the workflow dispatch a fresh new `最终放行审查代理`. A finding owner must not become the `最终放行审查代理`. The final pass round must be the last review round, use a fresh new `最终放行审查代理`, set `reuse_decision: new-agent`, review the current HEAD's complete diff, and record `findings_count: 0`. If the same technical agent is reused for closure, record why reuse is limited to closure. If an agent is replaced or an unfinished review agent is interrupted, record the `status_events[]` reason, predecessor output/diff handoff, and later completion/failure chain. `platform_nickname` should be the Chinese UI nickname when the platform provides one; otherwise record the raw automatic nickname. It remains display-only either way.

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

Review results must distinguish:

- `finding`: current diff has a known issue. Any finding priority `P0`, `P1`, `P2`, or `P3` blocks Branch Review Gate and `finish-work`.
- `observation`: non-blocking review note that does not claim the current PR is defective.
- `followup_candidate`: out-of-scope future work candidate that should become a follow-up issue or Issue Scope Ledger entry when appropriate, but is not a current PR finding.

Persist the independent review result in the conversation and in the task-local
artifact `{TASK_DIR}/review.md`. Independent review agents must review the
branch diff and repository artifacts directly from an AI reviewer perspective;
they do not execute Guru Team recorder/validator extension scripts such as
`review-branch.sh`, `check-review-gate.sh`, `record-agent-assignment.sh`, or
`record-*`. The main session runs those scripts only after the review result
exists, to record and validate objective gate evidence. The review report must
include concrete
summary/evidence, checked diff range, validation notes, deployment impact
judgment, Docs SSOT reconciliation, findings/observations/follow-up candidates
even when each list is empty, and the Chinese logical review role plus whether
`agent-assignment.json` records reuse/replacement decisions and any wait timeout, stale, interruption, unfinished termination, resume/replacement, completion, or failure status events that affected sub-agent evidence.

Before writing `review.md`, `review-gate.json`, or any task artifact, confirm the
current working directory is the task's selected `workspace_path`, not the source
checkout or another worktree. Use the worktree-local absolute path for manual
file edits when the editing tool does not take an explicit working directory.
Relative task artifact paths such as `{TASK_DIR}/review.md` are relative to the
task worktree only.

##### 3.5.2 Gate Artifact Recorder

Only after every finding owner has completed a successful same-agent
`问题闭环审查代理` closure round for its finding, then a fresh `最终放行审查代理` has completed an
independent review of the current HEAD's full diff with zero findings and
`{TASK_DIR}/review.md` exists, and `agent-assignment.json.status_events[]` has no unclosed `terminated-unfinished` chain, write the passing gate artifact. The pass path must include
`--review-source independent-agent` and `--review-report {TASK_DIR}/review.md`;
`--reviewer` may additionally record the independent reviewer identity, but it
cannot replace the review report. Always pass task-local `agent-assignment.json`
so the recorder validates that every finding owner has a later closure round, every unfinished terminated agent has same-agent resume or replacement plus later `completed`/`failed` status evidence, and
the final review round is fresh, last, has `findings_count: 0`, reviewed the
current HEAD, and is not an agent that found findings in an earlier round:

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --review-source independent-agent \
  --reviewer "trellis-check-agent" \
  --review-report ".trellis/tasks/<task>/review.md" \
  --agent-assignment ".trellis/tasks/<task>/agent-assignment.json" \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
```

or, when findings exist:

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json \
  --review-source independent-agent \
  --reviewer "trellis-check-agent" \
  --review-report ".trellis/tasks/<task>/review.md" \
  --agent-assignment ".trellis/tasks/<task>/agent-assignment.json" \
  --summary "中文审查结论" \
  --finding 'P3|中文问题说明|path/to/file'
```

Use `--observation '中文观察|path/to/file'` for non-blocking observations and
`--followup-candidate '中文后续候选|path/to/file'` for out-of-scope follow-up
candidates. Do not downgrade an actual current-scope defect into an observation
or follow-up candidate to pass the gate.

The artifact records base/head, diff command, conclusion, reviewer identity metadata, review source, review-report digest, agent-assignment digest/roles summary, summary, concrete evidence lines, findings, observations, follow-up candidates, changed files, Issue Scope Ledger coverage, and validation evidence. It is written to `{TASK_DIR}/review-gate.json` by default.

Passing the gate is not a blank assertion. `--pass` requires zero findings, `--review-source independent-agent`, a non-main-session `--reviewer`, a Chinese `--summary`, at least one concrete `--evidence` line from the actual review, `--review-report` pointing at the task-local `review.md`, and `--agent-assignment` pointing at the task-local `agent-assignment.json`. `review-gate.json` must record `review_source`, `review_report.path`, `sha256`, `size_bytes`, `modified_at`, `agent_assignment.path`, `sha256`, `size_bytes`, `modified_at`, `roles`, review round counts, and status event counts, so the recorder can validate closure-before-final, fresh final reviewer metadata, and unfinished sub-agent recovery-chain completeness. Use additional `--evidence` lines for important validation commands or review coverage notes. If the current platform/session cannot provide independent Agent review evidence, do not write a passing gate; stop with Branch Review Gate pending.

Findings artifacts are failed Branch Review Gate records, but they still record
a prior independent review. The findings path must also include
`--review-source independent-agent` and `--review-report` pointing at the
task-local `review.md`; omitting either means the artifact is reviewer-only and
must be rejected.

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

Then create or review the task-local PR body at `{TASK_DIR}/pr-body.md` and
run the internal Guru Team finish helper first as a side-effect-free readiness
preview, then as the formal finish:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --body-file "{TASK_DIR}/pr-body.md" \
  --dry-run
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --body-file "{TASK_DIR}/pr-body.md"
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
5. In business projects, `.trellis/spec/**`, `.trellis/tasks/**`, `docs/**` durable docs, `00-bootstrap-guidelines` generated docs SSOT, and workflow artifact human-readable fields are Chinese by default, with English reserved for literal tokens such as commands, paths, config keys, GitHub keywords, and code symbols.
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

Default best practice for new issues, new bugs, or expanded requirements is to create a new Trellis task. Add a new issue to current `close_issues` only when it is the same delivery unit, does not materially expand boundary/risk/test scope, the planning artifacts are updated, the user explicitly confirms inclusion, GitHub-visible evidence records the decision, and Branch Review Gate records coverage.

If a user changes requirements during an active task, the AI must preserve the decision trail before continuing implementation: summarize the new request, recommend `close_issues` / `related_issues` / `followup_issues`, get confirmation when classification is not explicit, update planning artifacts when the current task scope changes, and add issue comment/body/new issue evidence as appropriate. Do not close a referenced issue merely because it was discussed during the task.
