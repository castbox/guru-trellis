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
9. **Transactional finish** — `finish-work` binds an immutable closeout plan, verifies remote evidence, creates a draft PR, validates the final archive projection, archives once, then marks that same PR ready after local/remote/PR HEAD alignment.
10. **Capture learnings** — after each task, review whether `.trellis/spec/` needs updates.
11. **Knowledge before framework changes** — when a task may touch Guru Team middle-platform SDKs or frameworks, retrieve and cite current framework knowledge before design or implementation.
12. **Task artifacts do not replace durable docs** — reconcile Trellis task artifacts with the repo's long-lived `docs/` source of truth before finish.
13. **Chinese Conventional Commits** — work commits, Trellis metadata commits, and merge commits must use Conventional Commits prefixes with Chinese descriptions and explicit `Refs` / `Closes` separation.

---

## Public Workflow Skill Contract

`trellis/skills/guru-team/` is the canonical registry/package/interface root.
The workflow marketplace installs this global workflow only; the Guru Team
preset validates and installs active external skill packages. `reserved`
registry ids are not installed and must not appear in a production route.

Every mandatory active step is invoked by one stable skill id and one
machine-readable marker:

```markdown
<!-- guru-skill-invoke: {"skill":"guru-example-action","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-example-action","exit":"completed","consumer":{"kind":"workflow","id":"phase-3"}} -->
```

The examples define syntax only and are fenced, not production markers. A real
mandatory invocation marker must appear as an unfenced standalone HTML comment.
Every declared external exit has exactly one consumer or explicit stop.
Missing skills and unknown, duplicate, multiple, or unmapped exits fail closed.
Frontmatter auto-match may aid discovery but never substitutes for the marker.

The workflow owns only phase order, mandatory invocation, transitions, and
typed-exit consumers/stops. The package owns entry/freshness/re-entry and the
exact stage profile selected by its `judgment_mode`: semantic packages use
`forward behavior -> AI Review Gate -> conditional human confirmation ->
recorder/validator -> typed exit`; deterministic packages use `forward behavior
-> recorder/validator -> typed exit`. Commands, prompts, breadcrumbs, and
platform launchers load the stable skill id and must not copy either loop.
Deterministic scripts validate structure and evidence only; they do not make
semantic review or routing judgments.

The production registry currently activates `guru-sync-base`,
`guru-discover-change-context`, `guru-clarify-requirements`, and
`guru-review-contract-wording`, `guru-review-change-request`, and
`guru-create-task-workspace`, and `guru-create-task-commit`. The unfenced
markers below are the only mandatory global routes. New active routes must update
registry, package/interface, this workflow, tests, preset distribution,
extension public API, and migration documentation together.

---

## Guru Team Gate

Before creating a Trellis task or writing task artifacts, complete the Phase 0
chain in order: `guru-sync-base` -> `guru-discover-change-context` ->
`guru-clarify-requirements` -> `guru-review-contract-wording` ->
`guru-review-change-request` -> `guru-create-task-workspace`. Only the final
`created` exit enters Phase 1. Each package owns its entry evidence, semantic
or deterministic stage profile, confirmation, recorder/checker, freshness,
re-entry and typed exit; this workflow does not reproduce those rules.

```bash
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --expected-resolution-sha256 <post-sync-resolution-sha256> \
  "<user request, issue number, or issue URL>"
```

`prepare-task` is a side-effect-free compatibility query only. Its legacy
mutation flags fail closed before writes and point callers to
`guru-create-task-workspace`; it is never an alternate task creation route.

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

The package contract is the sole owner of target authority, naming, assignee,
two mutually exclusive confirmations, exact issue/workspace/task mutations,
four task-local Intake artifacts, ignored runtime mappings, no-developer
boundary, ordinary recovery and fail-closed refresh. Secrets and sensitive raw
records remain prohibited from public packages and portable artifacts.

### Workspace Boundary

When `workspace_mode: worktree`, tracked task-start-context contributes only portable
workspace/task identifiers. The machine-local write boundary is the `expected_workspace`
derived from the current checkout, `.trellis/.runtime/guru-team/**`, and `git worktree list`.
Before writing or reading
task-local recorder/validator inputs such as `planning-approval.json`,
`phase2-check.json`, `agent-assignment.json`, `reviews/*.md`, `review.md`, or
`review-gate.json`, confirm that the shell/editor repo root is exactly that
derived `expected_workspace`:

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>
```

The validator reports expected workspace, actual repo root, source checkout,
task dir, source-checkout status, task-worktree status, and suspicious
source-checkout copies of the current task artifacts. It is a fact collector and
fail-closed validator only; it does not decide stale state, migrate mistaken
patches, clean source checkout files, or replace AI/human review. If it reports
source checkout current-task artifacts or review metadata, treat that as a
`workspace-boundary violation with progress` fact for the main session to
review, not as automatic stale/failure evidence.

All relative task artifact paths are relative to the task worktree. Manual edit
tools that cannot receive an explicit `workdir` must use an absolute path inside
the task worktree selected by local runtime workspace mapping; do not use a source
checkout relative path for task artifacts or patches. `--review-report`,
`--agent-assignment`, `--review-round-report`, and `--checked-artifact` inputs
must resolve inside the current task directory in that worktree. In worktree
mode, do not run recorder/validator helpers from the source checkout or another
worktree.

---

## Shared Branch Commit Validation Contract

All commits that enter a PR branch or `main` are checked by the installed
`check-commit-messages` shared branch validator. Task work subject/body syntax,
candidate construction, AI review, confirmation, exact staging, executor and
postconditions are owned by the mandatory `guru-create-task-commit` package and
its durable contract; this global workflow must not reproduce that step-local
template or define a second parser.

Trellis metadata commits generated by finish/publish use an empty body and the
subject `chore(trellis): #<primary_issue> 固化任务收尾元数据`. Commit messages
must not use close keywords. Issue closing semantics belong only in the PR body
and only for issues listed in `issue-scope-ledger.json.close_issues`.

The repository keeps merge commits. The merge commit subject must use:

```text
chore(merge): #{pull_request} 合并 #{primary_issue} 中文 PR 摘要
```

The merge commit body must use:

```text
合并：
合入 `{head_branch}` 到 `{base_branch}`，保留 PR 内部提交历史。

范围：
本次 PR 完成 #{primary_issue}：中文 PR 摘要。

审计：
Trellis task archive、review gate 和 finish-summary 提交保留在 PR 分支历史中，用于审计任务过程。

PR: #{pull_request}
Refs #{primary_issue}
```

Do not accept GitHub's default `Merge pull request #xx from ...` subject, and do
not use a Chinese PR title such as `完成：#73 ... (#91)` directly as a commit
subject. `format-merge-commit` outputs a `merge_commit` payload with the subject, body,
and explicit `gh pr merge ... --subject ... --body-file ...` command; maintainers
must use that payload when merging instead of relying on GitHub-generated merge
text.

---

## Trellis System

### Official Developer Identity (Optional)

Guru Team installation, Intake, task workspace creation, and later phases do
not require a developer name or developer identity. Do not run an identity
initializer as a Guru workflow prerequisite. If the user independently chooses
to use the official Trellis identity/workspace journal capability, its official
command remains available:

```bash
python3 ./.trellis/scripts/init_developer.py <your-name>
```

That optional official command may create `.trellis/workspace/<your-name>/`; Guru Team
ignores that directory, never uses it for finish/readiness/context evidence, and
the preset keeps `.trellis/workspace/` gitignored. Task completion history lives
in archived task-local `finish-summary.json` instead. Guru Team `trellis-start`
loads only phase, packages, current task, and Git facts. Canonical Codex/Cursor
SessionStart overlays do not import or call journal helpers and do not open,
enumerate, read, count, or output workspace journal data.

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
through the complete Phase 0 chain from `guru-sync-base` through
`guru-create-task-workspace`. Do not use the bare
`task.py create` command below from the source checkout for Guru Team worktree
tasks. Only the exact workspace Skill executor may invoke it with a reviewed
non-empty `--assignee` after the target, naming, confirmation, and freshness
gates pass.

Every task has its own directory under `.trellis/tasks/{MM-DD-name}/` holding
`task.json`, `prd.md`, `design.md`, `implement.md`, `research/` when
applicable, the task-level `issue-scope-ledger.json`, generic sub-agent
assignment/status evidence, and context manifests (`implement.jsonl`,
`check.jsonl`) for sub-agent-capable platforms. Each mandatory Skill owns its
step-local artifact contract; this global workflow does not restate those
private artifact bodies or lifecycle rules. Guru Team implementation tasks
require `prd.md`, `design.md`, and `implement.md` before `task.py start`,
implementation, and check; missing or stale planning documents fail the
explicit post-planning approval gate.

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

Before the explicit finish entrypoint runs, create or review the task-local PR
body at `{TASK_DIR}/pr-body.md`, then preview readiness before the formal
finish:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file "{TASK_DIR}/finish-summary-index.json" \
  --body-file "{TASK_DIR}/pr-body.md" \
  --dry-run
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file "{TASK_DIR}/finish-summary-index.json" \
  --body-file "{TASK_DIR}/pr-body.md" \
  --expected-plan-digest "<closeout_plan_digest>"
```

Before any phase stop or phase completion reply, resolve the human-facing
Markdown artifacts and include a `Markdown 产物 review 表` in the response:

```bash
.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh --json --task <task-path>
```

The standard table lists only the resolver's five Markdown files: `prd.md`,
`design.md`, `implement.md`, `review.md`, and `pr-body.md`. It must not include
machine JSON artifacts such as `planning-approval.json`, `phase2-check.json`,
`agent-assignment.json`, `review-gate.json`, `pr-readiness.json`, `marketplace-verification.json`, or
`issue-scope-ledger.json` by default. Render existing files as links using the
resolver path/link fields; when `exists=false`, show the filename and status
without a Markdown link so the response does not create a dead link.

These are internal workflow helpers. `publish-pr.sh` is intentionally omitted
from the normal helper sequence because it is an unconditional compatibility
blocker; ordinary direct `finish-work.sh` calls are blocked unless the explicit
`trellis-finish-work` entrypoint supplies its intent marker. That entrypoint
pushes reviewed evidence, binds one immutable draft PR, builds the final
summary, then performs the archive transaction and marks the same PR ready.
They are not new user-facing primary commands.

### Sub-agent Boundary

Trellis ships `trellis-implement`, `trellis-check`, and `trellis-research`
sub-agents on agent-capable platforms. Guru Team keeps that official model:

- Platform dispatch identifiers are stable technical API ids. User-facing
  labels may be localized, while display nicknames never participate in gate
  decisions.
- Each mandatory Skill owns the logical roles, prompt, evidence, judgment and
  recovery rules inside its step-local closed loop. The global workflow only
  coordinates dispatch, waiting and the declared cross-Skill transition.
- The main session must not substitute itself or script output for a
  package-required sub-agent result. Inline/self exemption is valid only when
  the owning contract permits it and current evidence records it explicitly.
- Sub-agent dispatch prompts must include locally derived `expected_workspace` evidence when the task was created through Phase 0; it must not be read from committed task context. At startup, sub-agents should report `pwd`, `git rev-parse --show-toplevel`, and whether the actual repo root matches the expected workspace before reading or writing task artifacts. When an agent file, platform, or editor tool cannot set an explicit working directory, any manual patch/edit path must be an absolute path under the task worktree confirmed by `check-workspace-boundary.sh --task`.
- `wait_agent`, `trellis channel wait`, or an equivalent wait command timing out only means this wait window ended without a final completion event. It is not evidence that the sub-agent is stuck, failed, should stop, or that its partial output is acceptable completion evidence.
- Distinguish long total runtime from stale state. A sub-agent may run for more than an hour. The main session must run the short-lived liveness checker at `progress_scan_interval=120s` or sooner according to checker `next_wait_ms`; this scan interval is not a stale threshold. `max_progress_silence=180s` is measured from `progress_anchor_at`, and stale eligibility exists only when checker has already observed no new progress, a pending `status-requested` exists, that request produced no progress response, and `checked_at >= max_progress_silence_deadline_at`.
- `{TASK_DIR}/agent-assignment.json` is the single task-local assignment, liveness, status, and review ledger. Do not create `{TASK_DIR}/agent-progress.jsonl` or any task-local heartbeat file. Do not require sub-agents to write periodic heartbeat messages, and do not add daemon, sidecar, long-command wrapper, watch loop, or background liveness process. The checker is an on-demand, single-sample command that updates objective snapshot fields and exits.
- When a main session dispatches or reuses a sub-agent, record the AI/human decision with the liveness recorder so it creates `agents[]`, an `assigned` status event, and `liveness[agent_id]` baseline in the same artifact:

```bash
.trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh --json \
  --task ".trellis/tasks/<task>" \
  --source-repo "<source-checkout-path>" \
  --logical-role "实现代理" \
  --agent-id "019f..." \
  --platform-nickname "Gibbs" \
  --event assigned \
  --observed-at "2026-07-07T00:00:00Z" \
  --evidence "中文分配原因"
.trellis/guru-team/scripts/bash/check-agent-assignment.sh --json
```

- Before each liveness decision, the main session must first record platform-visible but non-machine-readable progress in `status_events[]` using `record-subagent-liveness-event.sh`: `explicit-message-observed`, `tool-activity-observed`, `command-output-observed`, `platform-progress-observed`, or `status-response-observed`. UI-only observations that are not written to `status_events[]` are not checker evidence.
- Then run `check-subagent-liveness.sh`; the checker performs one snapshot of task worktree and source checkout `HEAD` / dirty status / diff stat / max file mtime plus progress event digest, compares that snapshot with `last_scan_snapshot`, writes the updated liveness state, returns one decision, and exits. Only changes relative to the previous scan count as progress. Existing dirty diff, old status events, control/bookkeeping events, and `agent-assignment.json`'s own mtime/diff do not refresh `progress_anchor_at`.

```bash
.trellis/guru-team/scripts/bash/check-subagent-liveness.sh --json \
  --task ".trellis/tasks/<task>" \
  --agent-id "<technical-agent-id>" \
  --source-repo "<source-checkout-path>" \
  --progress-scan-interval 120 \
  --max-progress-silence 180
```

- Checker decisions are binding for the next main-session action:
  - `workspace_boundary_violation_progress`: source checkout changed since the previous scan. Record `workspace-boundary-violation`, treat it as progress, correct the workspace boundary, and do not stale the agent.
  - `progress_observed`: task worktree machine evidence or recorded progress event changed. Continue waiting for the same agent.
  - `status_request_required`: no new progress and no pending status request. Only this decision authorizes a status request. After the request is successfully sent, record `status-requested` and immediately run the checker again; the record does not refresh `progress_anchor_at` or extend `max_progress_silence_deadline_at`. If the request could not be sent, record `status-request-failed`; do not set pending status, stale, terminate, or replace.
  - `continue_waiting_no_repeat_ping`: no new progress, a pending status request exists, and the deadline has not passed. Continue waiting for `next_wait_ms`; do not send a repeated status request.
  - `stale_allowed`: no new progress, a pending status request exists, no status response/progress arrived, and the deadline has passed. Only this decision authorizes `stale-assessed`.
  - `blocked_missing_evidence`: artifact, schema, source repo, path, snapshot, or time evidence is missing or invalid. Fix evidence; do not stale, terminate, replace, record Phase 2 pass, or pass Branch Review Gate.
- If the deadline has already passed but no pending `status-requested` exists, checker must still return `status_request_required`. The subsequent `status-requested` only completes the stale precondition audit; it must not move `max_progress_silence_deadline_at`. When checker returns `stale_allowed`, the main session must first record any newly observed public progress and rerun checker if such progress exists.
- After `stale-assessed` is successfully recorded, do not wait for or resume that predecessor. In the same liveness handling turn, record `terminated-unfinished termination_reason=stale_cutover termination_source_event_id=<stale-assessed.event_id>`, dispatch and record the replacement `assigned`, then record `replacement-started predecessor_agent_id=<stale predecessor> predecessor_event_id=<stale-assessed.event_id> replacement_reason=max_progress_silence_exceeded` with a handoff summary covering predecessor output, current diff, task artifacts, remaining work, and gate blockers.
- Manual/platform unfinished termination must use `termination_reason=manual_or_platform_terminated_unfinished` with an empty `termination_source_event_id`. Failed or manually terminated unfinished agents may be resumed with `resume-same-agent` or replaced with `replacement-started`; stale cutover may only be replaced. Every recovery chain must later reach `completed`; a replacement `failed` requires further resume/replacement before pass gates can use the output.
- `completed` means only that the sub-agent execution chain ended. It cannot
  replace the owning Skill's semantic gate or authorize skipping a later
  mandatory Skill invocation. Failed, unfinished, stale, or partial recovery
  output remains intermediate evidence.
- Codex defaults to `codex.dispatch_mode: sub-agent` in Guru Team projects.
  Dispatch prompts start with `Active task: <task path>`; Codex sub-agents fall
  back to `task.py current --source` when that line is unavailable. Explicit
  `codex.dispatch_mode: inline` is a downgrade/debug mode.

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
- Issue-backed, task-like, or file-changing request: first mandatory invoke `guru-sync-base`; after its `synced` exit, mandatory invoke `guru-discover-change-context`, `guru-clarify-requirements`, `guru-review-contract-wording`, `guru-review-change-request`, and `guru-create-task-workspace` in order. This includes pasted issue URLs, issue numbers, and clear development tasks. `check-env` and `prepare-task` are compatibility queries, not workflow hops or mutation authorization.
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
- `Docs SSOT Plan` — required Phase 1 planning contract, preferably a section in `design.md`; `prd.md` records docs status and requirement impact, and `implement.md` records the checklist/checkpoint. Do not duplicate the full plan across all three files.
- `planning-approval.json` — the single schema 2.0 result owned by `guru-approve-task-plan`; the global workflow consumes only its declared typed exit and treats `task.py start` as a status write.
- `contract-wording-review.json` — current `guru-review-contract-wording:planning_artifacts` evidence consumed by planning approval; its profile-specific `semantic_review.ai_review_gate.planning_checked_dimensions` obligation, vocabulary, classification, semantic review, and typed exits remain owned by the canonical Skill package.
- `phase2-check.json` — Phase 2 `trellis-check` report for full task-scope quality coverage before commit and Branch Review Gate.
- `issue-scope-ledger.json` — task-level close/ref/followup scope; do not overload `source_issue`.
- Skill-owned private gate evidence — each active package defines and validates
  its own task-local artifact model; the global workflow does not restate
  per-round, lifecycle, digest, or rollup fields.
- `pr-body.md` — reviewed Markdown PR body for GitHub reviewers.
- `implement.jsonl` / `check.jsonl` — spec and research manifests for sub-agent context. They do not replace `implement.md`.

Guru Team implementation tasks must have `prd.md`, `design.md`, `implement.md`, and one locatable `Docs SSOT Plan` before `task.py start`; a Phase 0 intake approval never substitutes for this post-planning review.

Contract wording review is owned by the mandatory semantic Skill
`guru-review-contract-wording`. Consumers reference only its fixed profile,
schema `guru-contract-wording-review-1.0`, and typed exit. Vocabulary,
classification semantics, rewrite/review loop, confirmation policy, and
scanner evidence are defined only by the canonical package contract. A
`planning_artifacts:pass` consumer additionally requires that contract's exact
planning-dimension object with every AI-reviewed value recorded as true; no
consumer or deterministic runtime may synthesize those judgments.

### Business Project Documentation Language

For repositories that install and use the Guru Team workflow as a business project workflow, human-readable documentation is Chinese by default:

- `.trellis/spec/**` project conventions and bootstrap outputs;
- `.trellis/tasks/**` human-readable task artifacts and human-readable fields in
  task-local JSON evidence;
- `docs/**` durable requirements, design, test, deploy, operations, and versioned docs;
- docs SSOT files created or completed by `00-bootstrap-guidelines`;
- workflow/helper artifact fields that are meant for humans to read, including summaries, evidence, findings, observations, follow-up candidates, PR titles, and PR bodies.

Keep literal command names, file paths, GitHub keywords, configuration keys, external API names, code symbols, and other required tokens in English when needed, but write the surrounding explanation in Chinese.

Exact headings, fields and evidence structure remain owned by the Skill that
creates each artifact; this global language rule does not duplicate those
step-local templates.

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

During planning, create or update one `Docs SSOT Plan`. The recommended authority is `design.md`; `prd.md` should record the docs state and requirement impact, and `implement.md` should record the execution checklist and checkpoint. The plan must stay repo-neutral and may point to any durable docs structure the repo actually uses, not only `docs/`.

The plan must record one docs state:

- `complete_docs` — durable docs exist and are usable for the task's affected product, architecture, API, data, deploy, operations, or test contracts.
- `partial_docs` — some durable docs exist, but relevant categories or current-scope contracts are missing.
- `stale_docs` — durable docs exist but conflict with current code, behavior, issues, or intended changes.
- `no_docs` — no durable docs SSOT or equivalent long-lived documentation exists for the current task scope.

It must record one task strategy:

- `ssot_first` — update durable docs / specs / workflow contracts first, then keep task artifacts as deltas and evidence. Prefer this for broad, clear requirements, design, workflow, API, data, deploy, operations, or test contract changes.
- `delta_first` — keep early exploration or a narrow local change in task artifacts first, but name the merge checkpoint when durable docs will be updated or explicitly re-evaluated.
- `bootstrap_or_repair_docs` — create minimal durable docs, repair stale docs, or define a bounded follow-up when docs are absent, partial, or stale.
- `no_docs_update_needed` — no durable docs update is needed; the plan must state the concrete reason and the docs checked.

At minimum the `Docs SSOT Plan` records:

- docs state and evidence paths;
- strategy and reason;
- affected durable docs files, or the checked paths when none are affected;
- task artifact deltas that must be merged back into durable docs;
- for `delta_first`, the merge checkpoint;
- for `bootstrap_or_repair_docs`, the minimum repair scope or follow-up limit;
- for `no_docs_update_needed`, the concrete reason.

When inspecting durable docs, look for complete, partial, or stale categories such as:

- `docs/requirements/`;
- `docs/designs/`;
- `docs/testplans/`;
- deploy or operations guides;
- versioned design docs.

Task artifacts should describe task-scoped deltas, decisions, evidence, and links to relevant durable docs. They must not become the long-term substitute for durable docs when the plan chose `ssot_first`, `delta_first`, or `bootstrap_or_repair_docs`.

Any durable docs created or updated through this workflow, including docs SSOT files created or completed by `00-bootstrap-guidelines`, must follow the business-project Chinese documentation default above.

Before commit, Branch Review Gate, finish-work, and publish, run Docs SSOT reconciliation:

- Did this task change a long-term product, architecture, API, data, deployment, operational, or test contract?
- Which `docs/` files were updated?
- Which task-artifact content was merged back into durable docs?
- Which content remains task history only?
- If durable docs were not updated, why is that acceptable, and does it require user confirmation?

Repos with `no_docs`, `partial_docs`, or `stale_docs` must still record one explicit outcome:

- create new durable docs;
- append/update or repair existing partial/stale docs;
- or bound the follow-up and explain why the current task artifact remains archived evidence only.

<!-- Per-turn breadcrumb: shown when there is no active task (before Phase 1) -->

[workflow-state:no_task]
No active task. First classify the user's natural-language request; do not require the user to explicitly run `trellis-start`.
If the request includes an issue URL, issue number, clear development task, or file change, the first priority is the mandatory Phase 0 `guru-sync-base` invocation, not `check-env`, `prepare-task`, semantic repository reads, or bare `task.py create`.
Only the `synced` exit enters mandatory `guru-discover-change-context`. Only its `context_ready` exit enters mandatory `guru-clarify-requirements`; initial clarification `clear` enters mandatory `guru-review-contract-wording:change_request`, whose current `pass` enters mandatory `guru-review-change-request`. Only readiness `ready` enters mandatory `guru-create-task-workspace`, and only its checker-passed `created` exit enters Phase 1. `refresh_review` re-enters `guru-sync-base`; `cancelled` and `blocked` stop. Other exits re-enter their declared prerequisite owner, stage a separate new-task route where explicitly owned, or stop.
The `skipped` exit returns to `original-request-route`; `blocked`, unknown, multiple, or unmapped exits stop fail closed.
`prepare-task` is query-only compatibility. All issue/workspace/task mutation is owned by `guru-create-task-workspace`.
Do not silently edit the current checkout. Direct edits require explicit user approval to skip GitHub issue, Trellis task, worktree, and branch for this turn.
Ask for consent before creating a GitHub issue, worktree, branch, or Trellis task unless the user explicitly requested that side effect.
Task creation consent is not current-checkout direct-edit consent. Do not write `.trellis/tasks/` artifacts until consent is clear and preflight has a clear workspace.
[/workflow-state:no_task]

### Phase 0: Intake

- 0.0 Base sync route `[required · once]`
- 0.1 Change-context discovery `[required · once]`
- 0.2 Requirements clarification `[required · once]`
- 0.3 Contract wording review `[required · repeatable]`
- 0.4 Change-request readiness review `[required · repeatable]`
- 0.5 Task workspace creation `[required · repeatable]`

#### 0.0 Base sync route `[required · once]`

After tool-free request classification and before any repository/network
semantic read, load and mandatory invoke the active public Skill by stable id:

<!-- guru-skill-invoke: {"skill":"guru-sync-base","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-sync-base","exit":"synced","consumer":{"kind":"skill","id":"guru-discover-change-context"}} -->
<!-- guru-skill-exit: {"skill":"guru-sync-base","exit":"skipped","consumer":{"kind":"workflow","id":"original-request-route"}} -->
<!-- guru-skill-exit: {"skill":"guru-sync-base","exit":"blocked","consumer":{"kind":"stop","id":"base-sync-blocked"}} -->

<!-- guru-workflow-target: {"id":"original-request-route"} -->
<!-- guru-stop-target: {"id":"base-sync-blocked"} -->

The caller-side AI classification decides only whether this invocation is a
repo-changing refresh or an allowed non-repository skip. The package declares
`judgment_mode=deterministic` and owns stdout-only selected-base resolution,
digest-bound fetch/fast-forward, objective live Git validation, and one typed
exit. It does not perform selected-base AI confirmation, a post-execution AI
Review Gate, or conditional human confirmation.

For a repo-changing route, run the package wrappers in this order:

```bash
.trellis/guru-team/skills/packages/guru-sync-base/scripts/sync-base.sh \
  --json --mode workflow --resolve-only [--base <explicit-base>]
.trellis/guru-team/skills/packages/guru-sync-base/scripts/sync-base.sh \
  --json --mode workflow --execute [--base <same-explicit-base>] \
  --expected-resolution-sha256 <pre-sync-resolution-sha256>
.trellis/guru-team/skills/packages/guru-sync-base/scripts/check-base-sync.sh \
  --json --mode workflow --result-json '<executor-result-json>' \
  --expected-resolution-sha256 <pre-sync-resolution-sha256>
```

The resolver order is exact: explicit `--base`; non-empty scalar
`base_branch`; first existing `base_branch_candidates` entry in configured
order (default `dev -> develop -> main -> master`); remote default only when no
candidate exists; otherwise `blocked`. Multiple existing candidates are not
ambiguous. Resolution and result facts remain on stdout; no cross-step evidence
file, lease, release, quarantine, replacement-cleanup, or terminal-residue
contract exists.

The execute command retains `resolution_sha256` as the pre-sync identity and
adds `post_sync_resolution` plus `post_sync_resolution_sha256` after the fetch /
fast-forward. The validator checks both identities and returns the post-sync
digest as the only digest passed to `prepare-task`. Already-equal execution may
produce equal digests; fast-forward execution must produce different digests.

This workflow consumes exactly one declared exit: `synced` enters
`guru-discover-change-context`; `skipped`
returns to the original non-repository request route; `blocked` stops. Unknown,
multiple, or unmapped exits and missing package/runtime evidence stop fail
closed. Do not run `check-env`, `prepare-task`, issue reads, duplicate search,
or repository history/docs/code/test discovery before this route returns
`synced`.

#### 0.1 Change-context discovery `[required · once]`

Load and mandatory invoke the active semantic package by stable id. The global
workflow owns only this invocation and its unique consumers:

<!-- guru-skill-invoke: {"skill":"guru-discover-change-context","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-discover-change-context","exit":"context_ready","consumer":{"kind":"skill","id":"guru-clarify-requirements"}} -->
<!-- guru-skill-exit: {"skill":"guru-discover-change-context","exit":"refresh_base","consumer":{"kind":"skill","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-discover-change-context","exit":"blocked","consumer":{"kind":"stop","id":"change-context-blocked"}} -->

Run the package contract with the validated `guru-sync-base` stdout facts,
user request, and live issue or proposed-draft clues. The package owns its
fixed current-state-before-history behavior, AI Review Gate, recorder/
validator, artifact freshness, and re-entry. Do not copy that loop into this
workflow or a platform entry.

Pre-task recording remains stdout-only. After task creation, persist only the
same expected snapshot at `{TASK_DIR}/context-discovery.json`. `context_ready`
enters `guru-clarify-requirements`; `refresh_base` re-enters
`guru-sync-base` and repeats this complete Skill; `blocked` stops at
`change-context-blocked`. Unknown, multiple, or unmapped exits fail closed.

<!-- guru-stop-target: {"id":"change-context-blocked"} -->

#### 0.2 Requirements clarification `[required · once]`

Load and mandatory invoke the active semantic package by stable id. The global
workflow owns only this invocation and its unique consumers:

<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"clear","consumer":{"kind":"workflow","id":"guru-requirements-clear-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"needs_context","consumer":{"kind":"skill","id":"guru-discover-change-context"}} -->
<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"refresh_context","consumer":{"kind":"skill","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"retarget_context","consumer":{"kind":"skill","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"new_task","consumer":{"kind":"workflow","id":"guru-full-task-intake-chain"}} -->
<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"blocked","consumer":{"kind":"stop","id":"requirements-clarification-blocked"}} -->

Run the package contract with the current context snapshot and exact issue or
draft authority. The package owns evidence classification, one-question
clarification, scope proposals, source-action selection, AI Review Gate,
conditional exact confirmation, recorder/checker, freshness and re-entry. Do
not copy that loop into this workflow or a platform entry.

The public artifact contract is `guru-requirements-clarification-2.0`.
Schema 1.0 artifacts and callers cannot express the checker-bound target
disposition, authority impact, or retarget identity, so recorder/checker return
`requirements_clarification_legacy_schema_requires_refresh`. Do not infer a
semantic migration or resume a downstream pass: re-enter `guru-sync-base` and
rerun the complete sync, discovery, clarification, wording, and readiness chain
against the current target.

Pre-task and standalone recording remains stdout-only. The package has no
GitHub mutation executor and no dedicated clarification artifact. A successful
comment/body/reopen mutation returns `refresh_context`; an exactly selected
different open issue returns `retarget_context`. Both re-enter `guru-sync-base`,
but retargeting must rerun the complete initial sync, discovery, clarification,
wording, and readiness chain for the selected issue without reusing old-target
passes. Active-task
`clear`/`new_task` requires a non-empty set containing only seven terminal
decisions. Every accepted-current/related/followup/new-task/out-of-scope scope
classification must have proposal-digest-bound exact user-decision evidence,
live GitHub authority, and one structured trail exactly persisted in current
`issue-scope-ledger.json.scope_decisions[]`. Its planning evidence must pass the
shared `guru-planning-approval-2.0` validator and exact reviewed/approved document
bindings; hash-only or placeholder evidence is invalid. `mechanism_removed` and
`mechanism_replaced` are terminal dispositions with optional origin, null
confirmation, no trail, and no authority mutation. GitHub mutation refreshes
context first; complete re-entry requires context `generated_at` not earlier
than authority `updated_at`, then a task update bound to that same context
digest. It does not require a second context digest change. Only then may
active-task `clear` or `new_task` return; the latter still carries only a reviewed
side-effect-free new issue draft. `clear` enters the single
caller-aware router, which validates `invocation_context.resume_target` before
resuming the initial, active-task, or standalone caller. #112 owns the full
task-intake continuation. Unknown, multiple, or unmapped exits fail closed.

<!-- guru-workflow-target: {"id":"guru-requirements-clear-router"} -->
<!-- guru-workflow-target: {"id":"guru-full-task-intake-chain"} -->
<!-- guru-stop-target: {"id":"requirements-clarification-blocked"} -->

#### 0.3 Contract wording review `[required · repeatable]`

Load and mandatory invoke the active semantic package by stable id. The global
workflow owns only this invocation, the profile-aware routers, and the stop:

<!-- guru-skill-invoke: {"skill":"guru-review-contract-wording","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-review-contract-wording","exit":"pass","consumer":{"kind":"workflow","id":"guru-contract-wording-pass-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-contract-wording","exit":"content_changed","consumer":{"kind":"workflow","id":"guru-contract-wording-change-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-contract-wording","exit":"blocked","consumer":{"kind":"stop","id":"contract-wording-blocked"}} -->

The `pass` router maps `change_request` to `guru-review-change-request`,
`planning_artifacts` to planning document presentation/approval, and
`explicit_paths` to the standalone caller. The `content_changed` router maps
`change_request` to base/context refresh, `planning_artifacts` to complete
planning review re-entry, and `explicit_paths` to standalone wording re-entry.
The router consumes only the checker-validated profile and exit; unknown,
multiple, stale, or unmapped results fail closed. The Skill package owns fixed
scope, semantic revision/classification, AI Review Gate, confirmation,
recorder/checker, evidence freshness, and re-entry.
After a `content_changed` consumer or resumed `blocked` stop enters complete
same-profile re-entry, task-local current non-pass evidence is superseded only
with a different, fully current result bound to its exact prior `facts_sha256`.
Stale evidence follows the separate stale replacement path; an identical
result and current `pass` remain protected. The recorder validates these
objective transition facts without deciding semantic route intent.
For `planning_artifacts`, `pass` also requires the canonical package's exact
profile-specific planning-dimension evidence. Evidence recorded before that
field existed is stale even when its schema id is still `1.0`.

<!-- guru-workflow-target: {"id":"guru-contract-wording-pass-router"} -->
<!-- guru-workflow-target: {"id":"guru-contract-wording-change-router"} -->
<!-- guru-stop-target: {"id":"contract-wording-blocked"} -->

#### 0.4 Change-request readiness review `[required · repeatable]`

After a checker-validated `guru-review-contract-wording:change_request:pass`,
load and mandatory invoke the active semantic package by stable id. The global
workflow owns only this invocation, five unique consumers, and the stop:

<!-- guru-skill-invoke: {"skill":"guru-review-change-request","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"ready","consumer":{"kind":"skill","id":"guru-create-task-workspace"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"clarify_requirements","consumer":{"kind":"skill","id":"guru-clarify-requirements"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"review_wording","consumer":{"kind":"skill","id":"guru-review-contract-wording"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"refresh_context","consumer":{"kind":"skill","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"blocked","consumer":{"kind":"stop","id":"change-request-review-blocked"}} -->

The package owns the ten-dimension readiness review, findings, delivery-unit
and scope conclusion, AI Review Gate, conditional human confirmation,
stdout-only recorder/checker, evidence linkage, freshness, and typed exit. The
workflow does not copy or infer those judgments. Unknown, duplicate, multiple,
stale, consumer-mismatched, or unmapped exits fail closed.

`ready` invokes active `guru-create-task-workspace` only after complete
compatible package/runtime validation. Do not use `prepare-task`, bare
`task.py create`, or `guru-full-task-intake-chain` as a mutation fallback. The
three reroute exits completely re-enter their declared prerequisite owner;
`blocked` stops.

<!-- guru-stop-target: {"id":"change-request-review-blocked"} -->

#### 0.5 Task workspace creation `[required · repeatable]`

Load and mandatory invoke the active semantic package by stable id. The global
workflow owns only this invocation, four unique consumers, and the two stops:

<!-- guru-skill-invoke: {"skill":"guru-create-task-workspace","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"created","consumer":{"kind":"workflow","id":"guru-task-workspace-created"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"refresh_review","consumer":{"kind":"skill","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"cancelled","consumer":{"kind":"stop","id":"task-workspace-cancelled"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"blocked","consumer":{"kind":"stop","id":"task-workspace-blocked"}} -->

The package consumes the complete checker-passed Intake evidence and owns its
semantic forward behavior, AI Review Gate, invocation-specific confirmation,
recorder/executor/checker, ordinary recovery and exact artifacts. A reviewed
draft invocation creates and checks only the issue, then returns
`refresh_review`; an existing open issue invocation may return `created` after
the exact workspace/task result passes. Task workspace confirmation is not
planning approval.

<!-- guru-workflow-target: {"id":"guru-task-workspace-created"} -->
<!-- guru-stop-target: {"id":"task-workspace-cancelled"} -->
<!-- guru-stop-target: {"id":"task-workspace-blocked"} -->

### Phase 1: Plan

- 1.0 Confirm created task workspace `[required · once]` (only after Phase 0)
- 1.1 Requirement exploration `[required · repeatable]`
- 1.2 Research `[optional · repeatable]`
- 1.3 Configure context `[required · once]` for sub-agent-dispatch platforms
- 1.4 Task plan approval `[required · repeatable]` (mandatory Skill, exactly one typed exit)
- 1.5 Activate task `[required · once]` (`approved` only, then `task.py start`)
- 1.6 Completion criteria

[workflow-state:planning]
Load `trellis-brainstorm`; stay in planning.
Confirm the Guru Team task-start context exists in the chosen workspace for durable tasks: `.trellis/tasks/<task-slug>/task-start-context.json`.
Run docs SSOT discovery and the middle-platform knowledge gate when relevant.
Create or update the `Docs SSOT Plan`; prefer `design.md` as the authority, with docs status/requirement impact in `prd.md` and checklist/checkpoint in `implement.md`.
Finish `prd.md`, `design.md`, and `implement.md`, then mandatory invoke `guru-approve-task-plan`. That Skill exclusively owns its nine-precondition semantic loop and returns exactly one of `approved`, `revision_required`, `clarify_scope`, or `blocked`; this breadcrumb must not duplicate its review, confirmation, recorder, validator, or re-entry internals.
Only `approved` enters `phase-1-task-activation`; every other exit follows its declared Skill or stop consumer, and missing/unknown/multiple/unmapped results fail closed.
Sub-agent mode: curate `implement.jsonl` and `check.jsonl` as spec/research manifests before start.
[/workflow-state:planning]

[workflow-state:planning-inline]
Load `trellis-brainstorm`; stay in planning.
Confirm the Guru Team task-start context exists in the chosen workspace for durable tasks: `.trellis/tasks/<task-slug>/task-start-context.json`.
Run docs SSOT discovery and the middle-platform knowledge gate when relevant.
Create or update the `Docs SSOT Plan`; prefer `design.md` as the authority, with docs status/requirement impact in `prd.md` and checklist/checkpoint in `implement.md`.
Finish `prd.md`, `design.md`, and `implement.md`, then mandatory invoke `guru-approve-task-plan`. That Skill exclusively owns its nine-precondition semantic loop and returns exactly one of `approved`, `revision_required`, `clarify_scope`, or `blocked`; this breadcrumb must not duplicate its review, confirmation, recorder, validator, or re-entry internals.
Only `approved` enters `phase-1-task-activation`; every other exit follows its declared Skill or stop consumer, and missing/unknown/multiple/unmapped results fail closed.
Inline mode: skip jsonl curation; Phase 2 reads artifacts/specs via `trellis-before-dev`.
[/workflow-state:planning-inline]

#### 1.0 Confirm created task workspace `[required · once]`

Enter this step only through `guru-task-workspace-created`. The upstream Skill
has already created or exactly reused the reviewed branch, worktree and
planning-status Trellis task, and has checked the four task-local Intake
artifacts. Resolve the local worktree from ignored runtime/Git facts and run
`check-workspace-boundary.sh --json --task <task-path>` before task-local writes.
Do not rerun `prepare-task`, bare `task.py create`, or any second creator.

Task workspace confirmation authorizes only Intake creation. The mandatory
`guru-approve-task-plan` result remains the separate Phase 1 activation gate.

#### 1.1 Requirement exploration `[required · repeatable]`

Load `trellis-brainstorm` and update `prd.md` immediately after each important user answer or repository finding.

Issue body and comments are intake evidence, not a replacement for `prd.md`. If issue comments conflict, prefer the latest explicit final closeout comment and record the chosen source in `prd.md`.

When intake evidence is incomplete, use `trellis-brainstorm` before implementation planning. Ask only for product intent, scope, risk tolerance, or close/ref decisions that cannot be answered from repository evidence. After each material clarification, update `prd.md` immediately and decide whether the GitHub source of truth needs one of these updates:

- append a comment to the current source issue with the clarified scope, user confirmation, or final closeout interpretation;
- ask the user to update the original issue body when the body has become misleading for future sessions;
- create or propose a new issue when the clarification is a separate delivery unit or materially expands the current task.

Do not let task artifacts become the only record of changed requirements when a GitHub issue anchors the work. The issue or a related issue must carry enough public evidence for a later session to understand why the task scope changed.

Create or update the `Docs SSOT Plan` before planning converges. The plan should be easy to locate, with `design.md` as the recommended authority. `prd.md` records docs state and requirements impact; `implement.md` records the execution checklist, any `delta_first` merge checkpoint, and any `bootstrap_or_repair_docs` repair/follow-up boundary.

The plan must record:

- docs state: `complete_docs`, `partial_docs`, `stale_docs`, or `no_docs`;
- evidence paths inspected for that state;
- strategy: `ssot_first`, `delta_first`, `bootstrap_or_repair_docs`, or `no_docs_update_needed`;
- strategy reason;
- affected durable docs, or checked durable docs when no update is needed;
- task artifact deltas that must be merged to durable docs;
- `delta_first` merge checkpoint when that strategy is chosen;
- `bootstrap_or_repair_docs` minimum repair scope or follow-up limit when that strategy is chosen;
- `no_docs_update_needed` reason when that strategy is chosen.

Run the Middle-platform Knowledge Gate when the task may involve Guru Team middle-platform SDKs or frameworks. Persist citations or the unavailable-MCP warning before design and implementation artifacts are considered ready.

Scope Change Gate: when an active task receives a new requirement, referenced
issue, discovered bug, or possible scope expansion, pause the interrupted
progression and mandatory invoke the same active semantic Skill used by initial
intake:

<!-- guru-skill-invoke: {"skill":"guru-clarify-requirements","required":true} -->

Pass `invocation_context.kind=active_task_scope_change`, the current task
locator, and one exact `resume_target` naming the interrupted progression. The
Skill exclusively owns repository-first evidence classification, the
current/related/followup/new-task/out-of-scope decision, question loop, exact
confirmation, GitHub-visible authority, ledger/planning update requirements,
stale downstream evidence, and typed exit. This workflow must not repeat or
pre-decide those step-local semantics.

For active-task `clear`/`new_task`, the Skill requires a non-empty terminal
proposal set. For every five-class scope classification, the Skill requires
exact user evidence and a structured
decision trail exactly present in current
`issue-scope-ledger.json.scope_decisions[]`, regardless of proposal origin. The
trail binds live GitHub comment/body authority, planning documents and the
current schema 2.0 `guru-approve-task-plan` result, review state, stale downstream
identities, authority `updated_at`, `context_before_task_update_sha256`,
interrupted target, and re-entry owners. `mechanism_removed/replaced` stays
outside confirmation/trail/action mutation. GitHub authority mutation returns
`refresh_context`; only authority-before-context-before-task-update re-entry may
resume, and a task-only update does not require a second context refresh. Active-task
`new_task` preserves this trail and gives #112 only the side-effect-free draft.

The `clear` consumer is always `guru-requirements-clear-router`. The router is
only a workflow target declaration: it validates the caller-aware target
already recorded by the Skill and then routes as follows, without reclassifying
scope:

- initial issue or proposed draft -> `guru-review-contract-wording`;
- standalone review -> `guru-standalone-caller`;
- active-task accepted-current scope -> `guru-active-task-planning-review`;
- active-task non-current classification -> the exact interrupted target among
  `guru-resume-requirement-exploration`, `guru-resume-implementation`,
  `guru-resume-phase2-check`, `guru-resume-spec-evaluation`,
  `guru-resume-task-commit`, or `guru-resume-branch-review`.

Any invocation kind/resume target mismatch, unknown target, missing package,
multiple exit, or unmapped exit stops fail closed. Do not put active task state,
PR runtime state, or project-private business rules into a spec template or
marketplace entry.

#### 1.2 Research `[optional · repeatable]`

Research can use local code, docs, issue comments, Trellis specs, MCP servers, and web search when needed. Persist durable findings under `{TASK_DIR}/research/`.

When `guru-knowledge-center` MCP is available and the task is middle-platform relevant, research MUST include a `project_domain=middle-platform` retrieval using the current task context. Prefer persisting a concise citation file such as `{TASK_DIR}/research/middle-platform-knowledge.md` and referencing it from `design.md` or `implement.md`.

When the configured mode is `optional_warn` and MCP is unavailable, warn visibly and record the warning in task artifacts or the final report. When the mode is `required`, stop until retrieval succeeds, the user changes the configuration, or the team provides an equivalent approved knowledge source.

#### 1.3 Configure context `[required · once]`

For sub-agent-dispatch platforms, curate `implement.jsonl` and `check.jsonl` with real spec/research entries. Seed `_example` rows do not count.

Inline Codex/Kilo/Antigravity/Devin workflows skip this step and load context through `trellis-before-dev`.

#### 1.4 Task plan approval `[required · repeatable]`

After the planning artifacts are ready for semantic review, load and invoke the
active `guru-approve-task-plan` package. The package is the only
owner of planning adequacy, provenance, unusual-scenario review, AI Gate,
confirmation policy, evidence recording, and re-entry. This workflow owns only
the mandatory invocation and typed transitions below.

<!-- guru-skill-invoke: {"skill":"guru-approve-task-plan","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"approved","consumer":{"kind":"workflow","id":"phase-1-task-activation"}} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"revision_required","consumer":{"kind":"skill","id":"guru-approve-task-plan"}} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"clarify_scope","consumer":{"kind":"workflow","id":"guru-task-plan-clarify-scope-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"blocked","consumer":{"kind":"stop","id":"task-plan-approval-blocked"}} -->

Consume exactly one declared exit. Unknown, multiple, unmapped, missing-package,
or consumer-mismatched results fail closed.

<!-- guru-stop-target: {"id":"task-plan-approval-blocked"} -->
<!-- guru-workflow-target: {"id":"guru-task-plan-clarify-scope-router"} -->

This routing-only target consumes only the checked `exit_id`, `task_ref`, and
`proposal_refs` from `guru-approve-task-plan:clarify_scope`. Validate that
exact exit and consumer, and resolve `task_ref` to the one current task. Fail
closed on missing, stale, mismatched, multiple, unknown, or unmapped input.

Fresh-read the live issue authority, current task and scope ledger, current
planning artifacts and approval state, and every referenced proposal before
continuing. These reads establish caller context only; they do not expand the
producer DTO or authorize workflow/runtime reconstruction of semantic input.

The caller AI must then author all eight existing
`guru-clarify-requirements:active_task_scope_change` input fields from that
fresh context: `profile`, `source_exit`, `mode`, `target_locator`,
`context_locator`, `task_locator`, `resume_target`, and `continuation_id`.
Enter the Scope Change Gate above and mandatory invoke the existing active
`guru-clarify-requirements` package with that complete input. Do not add a
clarification authoring-seed edge: this router still authors all eight fields.
The separate `guru-create-task-commit:committed -> guru-review-branch` edge is
the fourth `skill_input_authoring_seed`, so the declared authoring-edge
cardinality remains exactly four. Do not infer, default, merge,
or recover these eight clarification fields from private runtime state or the
three-field proposal DTO.

#### 1.5 Activate task `[required · once]`

<!-- guru-workflow-target: {"id":"phase-1-task-activation"} -->

Only `guru-approve-task-plan:approved` enters this global transition. Recheck
the current artifact with `check-planning-approval --require-exit approved`,
then run the official task status transition:

```bash
.trellis/guru-team/scripts/bash/check-planning-approval.sh --json \
  --task <task-path> \
  --require-exit approved
python3 ./.trellis/scripts/task.py start <task-dir>
```

`task.py start` is only a status transition; it is not planning review
evidence. All other exits are consumed by their declared Skill or stop target.

#### 1.6 Completion criteria

| Condition | Required |
| --- | :---: |
| Guru Team task-start context exists for durable tasks | yes |
| `prd.md` exists | yes |
| `design.md` exists | yes |
| `implement.md` exists | yes |
| `guru-approve-task-plan` returned exactly one declared exit | yes |
| `planning-approval.json` uses `guru-planning-approval-2.0` and `check-planning-approval --require-exit approved` passes before activation | yes |
| `task.py start` has been run | yes |
| curated JSONL manifests exist for sub-agent dispatch | yes |
| Middle-platform Knowledge Gate handled when relevant | yes |
| `Docs SSOT Plan` records docs state, evidence paths, strategy, affected durable docs or no-update reason, and any required merge/repair/follow-up checkpoint | yes |

### Phase 2: Execute

- 2.1 Implement `[required · repeatable]`
- 2.2 Quality check `[required · repeatable]`
- 2.3 Rollback `[on demand]`

[workflow-state:in_progress]
Flow: `trellis-implement` -> `trellis-check` -> `trellis-update-spec` -> commit (Phase 3.4) -> Branch Review Gate (Phase 3.5) -> stop. The next entry is `/trellis:finish-work` only when the user/session explicitly invokes it.
Do not push the branch, create a PR, call `publish-pr`, or invoke `finish-work` from `trellis-continue`; closeout is owned by the explicit `trellis-finish-work` entrypoint, which binds the draft and final summary before archive and marks that same PR ready only after archive HEAD alignment.
Before dispatching `trellis-implement` / channel `implement` or recording
`phase2-check.json`, require a current `guru-approve-task-plan:approved` schema
2.0 result through the installed objective checker. Missing, legacy,
non-approved, or stale evidence blocks Phase 2. Post-activation implementation
`HEAD` or dirty-path drift alone does not block while the reviewed planning and
authority content remain current.
Before task work commit, record and check `phase2-check.json`; it records completed `trellis-check` AI evidence, and validation commands or recorder success alone are not a complete check. Message candidate review is owned later by mandatory `guru-create-task-commit`; Phase 2 still checks compatibility with the shared commit-message, metadata, and merge payload contracts.
Main-session default on dispatch platforms: dispatch `trellis-implement` / channel `implement`, wait for an implementation handoff, then dispatch `trellis-check` / channel `check`. Dispatch prompt starts with `Active task: <task path from task.py current>`. The main session may coordinate and record evidence, but it must not directly implement or directly check in default `sub-agent` mode.
After dispatching an implement/check sub-agent, record `assigned` for `实现代理` or `阶段二检查代理` with `record-subagent-liveness-event.sh` so `agent-assignment.json` contains `agents[]`, `status_events[]`, and `liveness[agent_id]` baseline. Then run `check-subagent-liveness.sh` at `progress_scan_interval=120s` or the checker-provided `next_wait_ms`. A wait timeout is only a wait-window result; record visible progress first, let checker return the single decision, and follow `status_request_required` / `continue_waiting_no_repeat_ping` / `stale_allowed` / progress decisions exactly. Old `record-agent-assignment.sh --status-event` status paths are deprecated and fail closed.
Sub-agent self-exemption: if already running as `trellis-implement` or `trellis-check`, do the work directly, do not spawn another Trellis implement/check agent, and return the role-specific handoff/report as artifact evidence. Main-session inline/self-exemption needs explicit artifact evidence; otherwise missing sub-agent evidence fails closed.
Before edits, confirm knowledge gate and the `Docs SSOT Plan` from artifacts. Phase 2 implementation/check must consume that plan, not re-decide it late at Branch Review or finish-work. The implementation handoff must name the plan strategy, docs sync result, task delta merged to durable docs, task-history-only content, no-update or follow-up limits, and which inputs came from durable docs versus confirmed task deltas. The Phase 2 check report must verify durable docs, task artifacts, code/API/schema/config/deploy/test, and validation evidence against the plan strategy.
Read context: jsonl entries -> `prd.md` -> `design.md` -> `implement.md`.
Every Phase 2 or Phase 3 stop/completion reply must first run `resolve-human-artifacts.sh --json --task <task-path>` and include a `Markdown 产物 review 表` with only `prd.md`, `design.md`, `implement.md`, `review.md`, and `pr-body.md`.
[/workflow-state:in_progress]

[workflow-state:in_progress-inline]
Flow: `trellis-before-dev` -> edit -> `trellis-check` -> validation -> `trellis-update-spec` -> commit (Phase 3.4) -> Branch Review Gate (Phase 3.5) -> stop. The next entry is `/trellis:finish-work` only when the user/session explicitly invokes it.
Do not push the branch, create a PR, call `publish-pr`, or invoke `finish-work` from `trellis-continue`; closeout is owned by the explicit `trellis-finish-work` entrypoint, which binds the draft and final summary before archive and marks that same PR ready only after archive HEAD alignment.
Before editing or recording `phase2-check.json`, require a current `guru-approve-task-plan:approved` schema 2.0 result through the installed objective checker. Missing, legacy, non-approved, or stale evidence blocks inline Phase 2. Post-activation `HEAD` or dirty-path drift alone does not block while the reviewed planning and authority content remain current.
Before task work commit, record and check `phase2-check.json`; validation commands alone are not a complete `trellis-check`. Message candidate review is owned later by mandatory `guru-create-task-commit`; Phase 2 still checks compatibility with the shared commit-message, metadata, and merge payload contracts.
Do not dispatch implement/check sub-agents in inline mode.
Before edits, confirm knowledge gate and the `Docs SSOT Plan` from artifacts. Inline Phase 2 still consumes the plan: implementation records strategy execution and docs sync handoff, and the later check verifies durable docs, task artifacts, code/API/schema/config/deploy/test, and validation evidence against that strategy.
Read context: `prd.md` -> `design.md` -> `implement.md`, plus relevant spec/research loaded by skills.
Every Phase 2 or Phase 3 stop/completion reply must first run `resolve-human-artifacts.sh --json --task <task-path>` and include a `Markdown 产物 review 表` with only `prd.md`, `design.md`, `implement.md`, `review.md`, and `pr-body.md`.
[/workflow-state:in_progress-inline]

#### 2.1 Implement `[required · repeatable]`

Dispatch or inline-implement according to the platform mode only after
`check-workspace-boundary.sh --json --task <task-path>` and
`check-planning-approval.sh --json --require-exit approved` passes for the
current schema 2.0 `guru-approve-task-plan` result. In default
`sub-agent` mode, the main session must dispatch `trellis-implement` or
channel-runtime `implement`; it may not directly edit files and later present
that work as `实现代理` evidence. Keep changes focused on the reviewed task
artifacts and the source issue scope.

On sub-agent-capable platforms, the main session records implementation assignment after dispatch:

```bash
.trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh --json \
  --task ".trellis/tasks/<task>" \
  --source-repo "<source-checkout-path>" \
  --logical-role "实现代理" \
  --agent-id "<technical-agent-id-or-empty>" \
  --platform-nickname "<display-name-or-empty>" \
  --event assigned \
  --observed-at "2026-07-07T00:00:00Z" \
  --evidence "中文说明为什么本轮实现由该 agent 承担"
```

The assignment artifact is evidence of an AI/human decision already made by the workflow. The companion script must not choose the agent or infer whether reuse is appropriate.

The implementation handoff must include files changed, key requirement/design carryover points, verification already run or explicitly deferred to Phase 2, remaining risks or a no-known-risk statement, completion status, and concrete focus areas for the later `trellis-check`. It must also include the `Docs SSOT Plan` strategy, durable docs updated or deliberately not updated, task artifact deltas merged back into durable docs, content retained only as task history, any `no_docs_update_needed` reason, any `bootstrap_or_repair_docs` minimum repair / follow-up / current PR limitation, and which code/test work used durable docs as primary input versus a confirmed task delta as temporary input. Do not report implementation completion until the requested scope is actually complete, docs strategy execution is accounted for, and verification status is known.

When a dispatched implementation agent reaches a wait timeout, do not infer failure. Record any public non-machine-readable progress with `record-subagent-liveness-event.sh`, then run `check-subagent-liveness.sh`. If checker reports progress, keep waiting. If checker reports `status_request_required`, send one status request, record `status-requested`, immediately rerun checker, and use the new `next_wait_ms`. If checker reports `continue_waiting_no_repeat_ping`, keep waiting without another ping. If checker reports `stale_allowed`, record `stale-assessed` only after confirming no newer public progress appeared, then perform the required stale cutover to replacement in the same liveness handling turn. If a terminal failure or manual/platform unfinished termination occurs, record `failed` or `terminated-unfinished termination_reason=manual_or_platform_terminated_unfinished`, then recover through same-agent resume or replacement until a later `completed` closes the chain. Failed, unfinished, stale, or replacement partial output must not be used as Phase 2 or Branch Review pass evidence.

Before writing code or generated assets, confirm the Middle-platform Knowledge Gate result for any middle-platform-relevant work:

- `off`: no action required.
- `optional_warn`: use persisted citations when present; if unavailable, continue only after the user-visible warning is recorded.
- `required`: do not implement until retrieval evidence or an approved equivalent source is persisted.

Also follow the planning artifact's `Docs SSOT Plan` responsibilities before writing implementation changes. Execute the strategy explicitly:

- `ssot_first`: use the revised durable docs / specs / workflow contracts as the primary implementation input, and keep task artifacts as deltas and evidence.
- `delta_first`: keep the task delta temporary only until the named merge checkpoint; merge the durable docs before the final Phase 2 check.
- `bootstrap_or_repair_docs`: create or repair the minimum durable docs promised by the plan, or record the bounded follow-up and current PR limitation before check.
- `no_docs_update_needed`: preserve the checked durable docs paths and concrete reason so Phase 2 check can re-evaluate whether the reason still holds.

If implementation reveals that a long-term product, architecture, API, data, deployment, operational, test, or workflow contract changes beyond the approved plan, update `prd.md`, `design.md`, `implement.md`, and the `Docs SSOT Plan`; when the planning documents' reviewed content changes, return to Phase 1 for fresh planning approval before continuing and rerun Phase 2 check afterward. Do not defer first discovery of this scope drift to Branch Review Gate or finish-work.

#### 2.2 Quality check `[required · repeatable]`

In default `sub-agent` mode, dispatch the official unchanged `trellis-check` or
channel-runtime `check` worker and record the assignment/recovery chain. Its
report is raw evidence only; it never owns Guru pass, scope, severity, route, or
`phase2-check.json`. Then load and invoke the active public Skill by stable id:

<!-- guru-skill-invoke: {"skill":"guru-check-task","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"passed","consumer":{"kind":"skill","id":"guru-create-task-commit"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-resume-implementation"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"planning_stale","consumer":{"kind":"workflow","id":"guru-task-check-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"blocked","consumer":{"kind":"stop","id":"task-check-blocked"}} -->

<!-- guru-workflow-target: {"id":"guru-resume-implementation"} -->
<!-- guru-workflow-target: {"id":"guru-task-check-planning-router"} -->
<!-- guru-stop-target: {"id":"task-check-blocked"} -->

The package owns all eleven entry checks, repository-command selection,
scope-before-severity, adequacy, Docs SSOT review, finding/full-rerun loop, AI
Review Gate, the single closed v2 artifact, recorder/checker entry, and exact
route result. The planning router consumes only checker-validated discriminator
`reapprove_plan` -> `guru-approve-task-plan` or `clarify_requirements` ->
`guru-clarify-requirements`; it performs no new scope judgment. Unknown,
multiple, unmapped, ambiguous, or consumer-mismatched results fail closed.

Before the Phase 2 stop/completion reply, run:

```bash
.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh --json --task <task-path>
```

Include a `Markdown 产物 review 表` so the user can open the current human
task artifacts from the latest reply. The table lists only `prd.md`,
`design.md`, `implement.md`, `review.md`, and `pr-body.md`; missing files stay
plain text with their resolver status and no Markdown link. Do not add
`phase2-check.json`, `agent-assignment.json`, or other JSON evidence to the
standard table.

#### 2.3 Rollback `[on demand]`

If implementation reveals a requirement defect, return to Phase 1 and update artifacts before continuing.

### Phase 3: Finish

- 3.2 Debug retrospective `[on demand]`
- 3.3 Spec update and Docs SSOT reconciliation `[required · once]`
- 3.4 Commit changes `[required · once]`
- 3.5 Branch Review Gate `[required · repeatable]`
- 3.6 Finish-work archive and finish-summary `[required · once]`
- 3.7 Publish PR `[automatic after finish-work]`

[workflow-state:completed]
Fallback/legacy closeout breadcrumb for an active task already marked `completed`; the normal path is `trellis-continue` stops after Branch Review Gate and the user/session explicitly invokes `/trellis:finish-work`.
If the current `guru-review-branch:passed` handoff is unavailable or stale,
return to Phase 3.5; do not reconstruct its private evidence in this fallback
breadcrumb.
If the gate passed, create or review task-local PR readiness at `{TASK_DIR}/pr-body.md`. Finish-work must pass that exact direct task path via `--body-file "{TASK_DIR}/pr-body.md"`; every existing path component from repo root through the task directory and final file must be non-symlink. It rejects `--body-artifact`, external/user-alias paths, and trim/newline-equivalent substitutes; only the verified Darwin `/var` to `/private/var` system root prefix may be structurally re-anchored.
Run a dry-run first:
`.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work --finish-summary-index-file "{TASK_DIR}/finish-summary-index.json" --body-file "{TASK_DIR}/pr-body.md" --dry-run`
After dry-run, run `resolve-human-artifacts.sh --json --task <task-path>` and include an active-task `Markdown 产物 review 表`; review the complete plan and rerun formal finish with `--expected-plan-digest <closeout_plan_digest>`.
After the formal finish archives the task, run `resolve-human-artifacts.sh --json --task <task-name-or-archive-path>` again and include the archive-path `Markdown 产物 review 表` in the final reply.
The finish-work owner validates its declared metadata tail. Any non-metadata
dirty path or non-metadata committed drift must go back to
`trellis-continue` / Phase 2-3.
Finish-work and archive do not perform the first Docs SSOT merge. If durable docs, `.trellis/spec/`, source, tests, schema, config, scripts, preset, overlay, CI/CD, deployment, migration, or Makefile assets changed after the gate, return to Phase 2/3 instead of treating the change as metadata tail.
Do not call `publish-pr` directly; normal publish and every recovery transition run only through the explicit state-aware `trellis-finish-work` closeout.
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

This reconciliation may live in `implement.md`, the owning phase evidence, the
final report, or a task research note, but the later mandatory review Skill
must cover the outcome.

#### 3.4 Create task work commit `[required · repeatable]`

After the final Phase 2 report passes and before any task work stage/commit side
effect, load and invoke the active public skill by stable id:

<!-- guru-skill-invoke: {"skill":"guru-create-task-commit","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"committed","consumer":{"kind":"skill","id":"guru-review-branch"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"revision-required","consumer":{"kind":"skill","id":"guru-create-task-commit"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"blocked","consumer":{"kind":"stop","id":"task-commit-blocked"}} -->

<!-- guru-stop-target: {"id":"task-commit-blocked"} -->

The package owns entry checks, candidate construction, AI Review Gate,
conditional human confirmation, deterministic validator/executor,
postconditions and typed-exit evidence. This global workflow owns only the
mandatory invocation, the three unique consumers above, and the repeat route.
Do not reproduce the step-local contract here or perform a parallel direct
task work commit path.

The stable `workflow` mode means this mandatory global route. Stable
`standalone` mode means selected-platform direct discovery without the global
route; it does not make the package self-contained or portable. Both modes
require the complete compatible Guru Team preset and extension runtime, use the
same entry preconditions and closed-loop behavior, and dispatch objective
commands through the shared `run-skill-command` runtime.

`committed` proceeds to Phase 3.5. `revision-required` re-enters the same skill
without guessing another route. `blocked`, unknown, multiple or unmapped exits
stop fail closed. Frontmatter auto-match is standalone discovery only and does
not satisfy this mandatory invocation.

#### 3.5 Branch Review Gate `[required · repeatable]`

After a committed task-work exit, load and invoke the active public Skill by
stable id:

<!-- guru-skill-invoke: {"skill":"guru-review-branch","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"passed","consumer":{"kind":"skill","id":"guru-review-task-publication"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-branch-review-implementation-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"scope_confirmation_required","consumer":{"kind":"workflow","id":"guru-branch-review-scope-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"blocked","consumer":{"kind":"stop","id":"branch-review-blocked"}} -->

<!-- guru-workflow-target: {"id":"guru-branch-review-implementation-router"} -->
<!-- guru-workflow-target: {"id":"guru-branch-review-scope-router"} -->
<!-- guru-stop-target: {"id":"branch-review-blocked"} -->

The caller projects the `guru-create-task-commit:committed` seed and freshly
authors only the target package's declared authoring fields. The active Skill
owns its complete step-local closed loop; this workflow only invokes it and
routes one declared exit.

`passed` targets planned `guru-review-task-publication`; while that package is
unavailable, stop fail closed and do not infer publication behavior.
`implementation_required` resumes implementation and must then pass a complete
`guru-check-task`, fresh task commit, and this Skill again.
`scope_confirmation_required` routes to requirements clarification; the caller
AI freshly authors the existing clarification profile from current live
evidence and the exact proposal refs. `blocked`, unknown, multiple, stale, or
unmapped results stop fail closed.

Before any Phase 3.5 stop or pass reply, follow the global human-artifact
resolution requirement.

#### 3.6 Finish-work archive and finish-summary `[required · once]`

Start only after `guru-review-branch:passed` for the current HEAD. The
finish-work owner validates that handoff and its declared metadata-tail
preconditions; this global workflow does not invoke the Branch Review checker
directly.

Then create and AI-review `{TASK_DIR}/finish-summary-index.json`. It contains only
`problem`, `outcome`, `changed_behavior`, `affected_surfaces`,
`contract_changes`, and non-factual `commands` / `config_keys` /
`schema_fields` / `symbols` / `phrases` search terms. The AI must not place
issue, PR, branch, path, commit, timestamp, or derived retrieval facts in this
input; the recorder injects those objective facts. AI input may contain at most
19 `contract_changes`; the final summary remains bounded at 20 so the recorder
can append the fixed protected-path filtering fact when required. Create or
review the task-local PR body at `{TASK_DIR}/pr-body.md` and
run the internal Guru Team finish helper first as a side-effect-free readiness
preview, then as the formal finish:

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file "{TASK_DIR}/finish-summary-index.json" \
  --body-file "{TASK_DIR}/pr-body.md" \
  --dry-run
# Review `closeout_plan_digest` from the JSON payload, then pass it unchanged:
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file "{TASK_DIR}/finish-summary-index.json" \
  --body-file "{TASK_DIR}/pr-body.md" \
  --expected-plan-digest "<closeout_plan_digest>"
```

The `--from-trellis-finish-work` marker is required proof that the explicit finish entrypoint was invoked; `trellis-continue` must not add or synthesize it. Dry-run and formal finish call the same `prepare_closeout()` validators and produce the same immutable `closeout-plan.json` bytes. Prepare builds and schema-validates the complete future archived summary with a deterministic maximum-width sentinel PR, exact task-relative move/evidence path sets, and task-relative marketplace artifact locator before dry-run/formal diverge. From the trusted repo-local archive root through month and final destination, it lexically `lstat`s each existing component, rejects every symlink including dangling and repo-internal targets without following it, and requires the final locator to be absent. The identical preflight repeats immediately before official move to reject prepare-to-move drift. Missing `task.json.children` means an empty list; otherwise the value must be `list[str]`, and official active-task exact/suffix lookup blocks only a child whose active `task.json` would be rewritten, not an archived historical child. Prepare parses `.trellis/config.yaml` with the installed official parser and accepts only missing/empty `hooks.after_archive`; unsupported, ambiguous, unreadable, NUL-containing, or symlinked hook config fails without executing a command. Formal execution compares `--expected-plan-digest` before its first write, push, or GitHub mutation. The helper pushes the reviewed content HEAD, records deterministic pending/passed marketplace evidence, commits and pushes plan/readiness/evidence, creates or reuses one exact draft PR, and substitutes only its canonical PR URL/ref into the prevalidated summary template. Final projection and incomplete/exact recovery share one strict parser: GitHub owner/repository identity is case-insensitive, canonical output preserves the exact valid remote casing, and transport/host/path/positive-number/query/fragment rules remain fail closed. The helper then calls the unmodified official `task.py archive --no-commit`.

The archive transaction creates one exact metadata commit, pushes it, requires local/remote/draft-PR HEAD equality, and only then marks the PR ready. Evidence commit parent/path identity and archive commit parent/mixed no-renames path set are immutable plan constraints: tracked task files require active deletion plus archive addition, while final outputs created after the evidence commit require archive addition only. Before that exact archive commit exists, recovery requires active absence, the complete prevalidated archived working-tree file set, exact dirty/staged paths, tracked blob continuity, the official `task.json` delta, and final-summary deterministic bytes rebuilt against the already-bound remote PR; partial, missing, extra, misclassified, tampered, or rebound state fails closed. Once current `HEAD` is the exact planned archive commit, the immutable plan and Git parent/path/tree/blob lineage are authoritative: missing or tampered archived working-tree files do not block pushing the exact commit, checking remote/PR HEAD, or retrying draft-to-ready. Exact recovery reads the immutable archive commit's `finish-summary.json` blob, not the working-tree summary, to recover the original PR number/URL and verify deterministic bytes/digest without invoking the general summary artifact validator. The original PR must remain the unique open repo/head/base candidate; missing, closed, or replacement PRs fail closed. An absent or mismatched archive commit falls back to the strict pre-commit metadata recovery path. A plan-only archived directory is resolvable only by the `trellis-finish-work` recovery entry; ordinary task commands still require `task.json`. The plan-only entry reads the plan from the current commit blob and applies a dedicated fail-closed boundary before GitHub or fast-path actions: Git toplevel, configured/effective repo, current head branch, available base ref, current HEAD transaction, expected digest, task identity, and active/archive locator must all match. Before ordinary resolution it preserves the raw locator, accepts only a task basename, exact former active locator, or exact archive locator, and uses lexical archive containment plus component-wise `lstat` through the final directory to reject internal/external, relative/absolute, ancestor/final, multilevel, dangling, and loop symlinks. The resolved target must still equal the plan's canonical archive locator; only the verified Darwin `/var` -> `/private/var` system mapping may re-anchor, never arbitrary `samefile` or user aliases. It never treats missing context as an unconditional boundary bypass; other commands retain `task.json` and worktree-mode `task-start-context.json` requirements. Neither recovery path parses archived verifier, ledger, readiness, or body artifacts, and no repo artifact is built, generally revalidated, or rewritten after archive. The same `trellis-finish-work` entry resumes verifier, draft binding, archive commit/push, remote identity, or draft-to-ready interruptions from persisted facts; callers never select `--skip-archive`, `--recovery-after-finish-work`, or a separate publish command. Guru Team never calls `.trellis/scripts/add_session.py` and never reads or writes `.trellis/workspace/**`.
Before ordinary task resolution, finish-work preflights raw path-like locators and basename candidates. Basename preflight follows ordinary candidate order across `<repo>/<basename>`, the active candidate, the archive root, and archive candidates. Every direct or archive candidate first retains only raw `symlink_component` evidence, then applies the ordinary resolver's exact follow-symlink `directory + task.json` predicate; a matching alias fails closed, while an unmatched alias continues to the next candidate. Ordinary resolution then preserves explicit `task.json`, active task, and normal archived `task.json` precedence. Only ordinary not-found enables plan-only fallback: an exact archive locator tries that candidate, while basename/former-active fallback requires one unique archive-month match and fails closed on ambiguity.
Immediately before official move, the live archive month must still equal the plan, the index must be empty, untracked paths must equal the planned final outputs, every move path must be a regular file, tracked Git/working modes must match as `100644`/`100755`, and every working byte must equal its evidence blob. A committed stale-month plan keeps the task active: rerun this same entry in dry-run mode, review the new digest, then run formal with that digest. The executor may append only a plan/readiness supersession evidence commit bound by `git.evidence_parent_head`; it reuses the draft/verifier facts and never rewrites history or migrates an archive directory. Every tracked evidence blob must match its archive working-tree and commit blob byte-for-byte, except the official deterministic `task.json.status/completedAt` transition. Draft reuse and final projection bind one repo/head/base/number/URL/title/body identity to the active final summary. Every archived exact-commit reentry reads the plan and final-summary runtime PR facts from current commit blobs even when task context remains. Post-archive ready and recovery validate the remote repo/head/base/title/body digest from the plan and require the remote candidate's number/URL to equal the committed summary facts. The failure matrix enters production `cmd_finish_work()` with real temporary Git/bare remote and fakes only external GitHub/verifier responses, including cross-month reprepare and a repo-mutating `after_archive` hook that must be rejected without execution.

Repositories upgrading from archives created before this finish-summary
contract may run the one-time public migration helper before history discovery:

```bash
.trellis/guru-team/scripts/bash/backfill-finish-summary.sh --json --dry-run
.trellis/guru-team/scripts/bash/backfill-finish-summary.sh --json --write
```

The backfill scans archived tasks only, uses the fixed task-local artifact
whitelist, validates the unchanged #97 schema, and isolates per-task failures.
It groups complete changed paths by surface kind, splitting each kind at 100
paths and failing closed if the result would exceed 20 surfaces. It never reads
workspace/runtime state, calls GitHub or `trellis mem`, changes active tasks, or
creates a global index. `--force` may overwrite an existing summary only with
`--write`; `--task` must be a clean repo-relative archived task directory.

After the dry-run returns, run the human artifact resolver against the active
task and include the active-task `Markdown 产物 review 表` in the preview reply:

```bash
.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh --json --task <task-path>
```

After the formal finish archives the task, run the resolver again against the
archived task name or archived task path and include the archive-path
`Markdown 产物 review 表` in the final reply. This second resolve is required
because old active task links are not expected to remain valid after
`task.py archive`; do not create symlinks, pointer dirs, or old-path stubs.

`finish-work` may create Trellis metadata commits for archive and finish-summary. These metadata commits do not invalidate the earlier code review gate; the helper only accepts Trellis metadata after the reviewed HEAD and blocks any code, config, script, schema, CI/CD, deployment, or preset change that appears after the gate.
It also blocks durable docs, `.trellis/spec/`, tests, overlay, migration, and
Makefile drift after the gate. Dry-run and formal finish both fail closed for
that drift. Finish-work/archive must not be used to first execute Docs SSOT
reconciliation; missing docs sync sends the task back to `trellis-continue` so
Phase 2 check and Branch Review can run again.

#### 3.7 Publish PR `[automatic after finish-work]`

Publish is a set of internal `trellis-finish-work` closeout transitions, not a user-facing phase or separate command. `publish-pr.sh` is retained only as a compatibility blocker that fails closed and points to the same state-aware `trellis-finish-work` invocation.

After `gh pr create` returns a URL, publish sorts and deduplicates the raw final base-to-HEAD paths, filters `.trellis/workspace/**` and `.trellis/.runtime/**`, and writes the safe set to both `git.changed_paths` and search `paths`. If filtering occurred, the recorder appends exactly one fixed `finish-summary protected path filtering` contract fact without path, basename, or count details; if no filtering occurred, that fact is absent. If the initial diff, initial untracked enumeration, or final/recovery diff fails, both path arrays are empty, the filtering fact is absent, and exactly one fixed `finish-summary git path snapshot unavailable` fact is recorded without path, basename, count, stderr, or ref details. Retrieval text is re-derived and path validation remains fail closed.

Before draft PR create, finish-work writes and commits task-local `pr-readiness.json.publish_inputs`. It binds normalized repo, base/head branch, Branch Review Gate HEAD, exact title, `pr-body.md`, body SHA-256, `draft=true`, reviewed source, and `closeout_plan_digest`. Remote identity uses a raw/effective two-layer gate: every raw `remote.<name>.url` / optional `pushurl` and `url.*.insteadOf` / `pushInsteadOf` base/pattern is read with NUL value boundaries plus origin, and empty/ambiguous records, boundary whitespace, controls, unreadable origins, or relevant config-file NUL fail closed; absent `pushurl` reuses the raw fetch set. Effective output is never trimmed, must preserve raw-source cardinality, and after Git rewrite must be credential-free `https://github.com/...`, `ssh://git@github.com/...`, or `git@github.com:...`; HTTP, `git://`, `file://`, local/bare paths, scheme-less forms, userinfo/token variants, ports, query/fragment, and extra paths fail closed, with no repo-identifier fallback. Each strict URL plus the queried PR's `headRepository.nameWithOwner` must normalize to that repo; `headRepositoryOwner.login` must agree and `isCrossRepository` must be false. `gh pr list --head` cannot scope by owner, so missing/unknown repository fields or any same-name fork candidate fail closed before 0/1/>1 selection. Before archive, the task-local file's raw UTF-8 text is the canonical body: leading/trailing whitespace, final newlines, and Markdown-sensitive spaces are never trimmed or normalized before create, reuse, or final projection. After archive, remote PR body bytes are hashed against the immutable plan without reopening task-local artifacts. Retries use the plan plus the facts permitted at the current transition and never re-enter local artifact validators after the official move.

The final active-task summary contains the canonical PR URL and exactly one derived `PR #<number>` ref before archive. The archive move carries it unchanged to the final locator. Any code, config, schema, workflow, preset, docs, test, CI/CD, deployment, migration, or Makefile path in the archive transaction fails closed. Multiple target-repo PRs or any cross-repository same-name candidate fail closed. Archived recovery never opens or rebinds the summary; it identifies the unique remote candidate from repo/head/base plus the plan's title/body digest.

The final publish/finish response must use the archive-after-finish resolver
result from Phase 3.6 for its `Markdown 产物 review 表`; do not reuse active
task links captured before archive.

Before invoking finish-work, the AI must generate or review the PR body for a
GitHub reviewer who has no Trellis session context. The body is not a task
artifact summary. It must explain what behavior changed, which modules or
workflow surfaces are affected, how the change was validated, what Review Gate
covered, which issues are closed vs only referenced, and the real safety /
deployment impact. Finish-work requires the exact current task-local
`pr-body.md` through `--body-file <pr-body.md>`; `--body-artifact` and generated
fallback bodies are not closeout readiness evidence. The reviewed
body/readiness files are task metadata under the current task directory before
finish-work. They are fully validated before archive and are not reopened by
post-archive recovery or ready steps.

Publish behavior:

- push the current branch;
- create or reuse one exact draft GitHub PR, then mark it ready only after the archive transaction and three-way HEAD check;
- target the intake/task `base_branch`, not the GitHub default branch;
- write the PR title, headings, and body in Chinese;
- include Chinese sections for `变更摘要`, `影响范围`, `验证结果`, `Review Gate`, `Issue 关闭范围`, and `安全说明`;
- include a reviewer-readable `Docs SSOT` or `文档同步` section that states the plan strategy, durable docs updated or the no-update reason, task artifact deltas merged to durable docs, content retained only as task history, and any follow-up or current PR limitation;
- require the AI-reviewed task-local `pr-body.md` through `--body-file`; reject `--body-artifact` and generated fallback bodies from the closeout path;
- block non-draft publish if `变更摘要`, `影响范围`, `验证结果`, or `安全说明` are missing, empty, or low-information;
- never use phrases such as `当前 Trellis task`, `已提交实现与文档更新`, or `详见 artifact` as the main PR summary;
- use `Closes #xx` only for `close_issues` in `issue-scope-ledger.json`;
- use only `Refs #xx` or `Related #xx` semantics for `related_issues`;
- never close `followup_issues`.
- use `format-merge-commit` to produce the final `merge_commit` payload after the PR number is known. Maintainers must use that payload for the final merge and must not rely on GitHub's default merge commit subject.

The PR body quality judgment belongs to the AI readiness review. `trellis-finish-work`
only validates objective structure, forbidden low-information phrases,
the exact reviewed task-local body file, Docs SSOT section/key presence, close/ref
issue semantics, commit-message payload shape, archive-path resolution, and then executes the closeout transitions. It must not invent
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
7. `review-branch` and `finish-work.sh` are companion script subcommands, not user-facing phases; `publish-pr` is a compatibility-only blocked command. Ordinary direct `finish-work.sh` and every `publish-pr` call are blocked before archive/push/PR.
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

`task-start-context.source_issue` only records intake provenance. It is not the final set of issues that the PR closes.

Task-level `issue-scope-ledger.json` owns close/ref/followup semantics:

- `primary_issue`: the intake issue, default close candidate.
- `close_issues`: issues this task explicitly commits to fully resolving; PR body may use `Closes/Fixes/Resolves` only for these.
- `related_issues`: context, reuse, partial overlap, or non-closing references; PR body may use `Refs` or `Related`, never close keywords.
- `followup_issues`: expanded scope, newly found bug, or later work; never close from the current PR.

Default best practice for new issues, new bugs, or expanded requirements is to create a new Trellis task. Add a new issue to current `close_issues` only when it is the same delivery unit, does not materially expand boundary/risk/test scope, the planning artifacts are updated, the user explicitly confirms inclusion, GitHub-visible evidence records the decision, and Branch Review Gate records coverage.

If a user changes requirements during an active task, the AI must preserve the decision trail before continuing implementation: summarize the new request, recommend `close_issues` / `related_issues` / `followup_issues`, get confirmation when classification is not explicit, update planning artifacts when the current task scope changes, and add issue comment/body/new issue evidence as appropriate. Do not close a referenced issue merely because it was discussed during the task.

### Remote Marketplace Verification Gate

For tasks that change the workflow marketplace, preset, overlays, installer, schema, or public extension contract, publish is fail-closed after the branch push and before `gh pr create`. The deterministic `verify-marketplace` companion command records task-local `marketplace-verification.json` with repository, remote, branch/ref, verified content HEAD, remote HEAD, command exit codes, stdout/stderr digests and sizes, and installed workflow/preview/schema digests. It executes remote branch `trellis init`, workflow preview, workflow switch, canonical preset reapply, and runtime-ignore checks in a clean temporary repository. It does not decide PR readiness.

`issue-scope-ledger.json` must carry one exact structured `remote_marketplace_verification` machine object in the primary issue and every close issue. The recorder creates pending from the closeout plan after the reviewed content push; human reason text is outside the machine identity. Pending and passed use the portable task-relative `marketplace-verification.json` locator, but the verifier and artifact/digest validators resolve it only while the task is active. The verifier replaces only that object with passed facts. The exact pre-draft metadata commit contains plan, readiness, verifier artifact, ledger, and every reviewed task metadata path recorded by the plan, then is pushed and remote-HEAD checked before draft PR binding. Archived recovery proves the prevalidated artifact's continuity only through the exact Git move/blob transaction and never reparses it. Missing, duplicate, pending, failed, stale, tampered, path-bound, or digest-mismatched evidence blocks before archive. The AI remains responsible for close scope and evidence sufficiency; scripts only execute, record, and validate deterministic facts. No release tag is created.
