# Guru Team Development Workflow

---

## Core Principles

1. **Plan before code** — figure out what to do before implementation starts.
2. **Issue-backed intake** — durable work starts from a GitHub Issue or from a neutral issue proposed by the workflow and created only after AI/human review.
3. **Git preflight before Trellis task files** — resolve base branch and workspace before `task.py create` writes task artifacts.
4. **Specs injected, not remembered** — follow `.trellis/spec/` and task artifacts instead of chat memory.
5. **Persist irreducible decisions** — write only facts that a later consumer cannot reliably recover from live authority, current plans, diff, tests, or terminal results.
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

The production registry currently activates thirteen workflow Skills, from
`guru-sync-base` through `guru-finalize-task`. The unfenced
markers below are the only mandatory global routes. New active routes must update
registry, package/interface, this workflow, tests, preset distribution,
extension public API, and migration documentation together.

### Global Interaction Contract

For any Skill-owned proposal or side effect, first display its current target,
scope, authority, relevant HEAD, action, and expected result. When that display
contains exactly one current, complete, unambiguous action, the prompt is only
`确认继续`; any clear affirmative reply authorizes the displayed action. Internal
evidence still records the action's semantic purpose and binds its exact digest,
but the user never repeats a SHA, digest, proposal text, or prescribed sentence.

This interaction rule does not merge distinct semantic approvals: a scope
expansion, post-planning approval, commit, push, PR, merge, Issue mutation, or
cleanup keeps its own authority and evidence. It only standardizes how one
already displayed action is accepted. Ask an actual question when choices or
ambiguity remain. Reconfirm only when target, HEAD, scope, authority, available
options, or side-effect plan changes. Mapped exits, stale/re-entry/reprepare,
recorder/checker transitions, and same-plan recovery are automatically consumed
inside the AI workflow and never become generic continuation prompts.

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
`phase2-check.json` or `review-gate.json`, confirm that the shell/editor repo root is exactly that
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
checkout relative path for task artifacts or patches. `--checked-artifact`
inputs must resolve inside the current task directory in that worktree. Legacy
`--review-report`, `--agent-assignment`, and `--review-round-report` inputs have
the same boundary when migrating an existing task. In worktree
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
context manifests (`implement.jsonl`,
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

Before finalization, create or review the task-local PR body at
`{TASK_DIR}/pr-body.md` and the current `finish-summary-index.json`, then invoke
the active `guru-review-task-publication` owner. Only its `ready` exit enters
`guru-finalize-task`. The finalizer privately runs closeout preview, plan-bound
confirmation, gate recording/checking, and deterministic transitions; global
workflow and platform entries must not invoke `finish-work.sh` or reproduce its
command flags.

Before any phase stop or phase completion reply, resolve the human-facing
Markdown artifacts and include a `Markdown 产物 review 表` in the response:

```bash
.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh --json --task <task-path>
```

The standard table lists only the resolver's four Markdown files: `prd.md`,
`design.md`, `implement.md`, and `pr-body.md`. It must not include
machine JSON artifacts such as `planning-approval.json`, `phase2-check.json`,
`agent-assignment.json`, `review-gate.json`, `pr-readiness.json`, `marketplace-verification.json`, or
`issue-scope-ledger.json` by default. Render existing files as links using the
resolver path/link fields; when `exists=false`, show the filename and status
without a Markdown link so the response does not create a dead link.

These are internal workflow helpers. `publish-pr.sh` is intentionally omitted
from the normal helper sequence because it is an unconditional compatibility
blocker; ordinary direct `finish-work.sh` calls are blocked. The explicit
`trellis-finish-work` entrypoint is a thin live-workflow router; the active
finalizer privately pushes reviewed evidence, binds one immutable draft PR,
builds the final summary, performs the archive transaction, and marks the same
PR ready only after its semantic gate and plan-bound confirmation. They are not
new user-facing primary commands.

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
- Routine dispatch does not start a liveness protocol. Use the platform-visible
  terminal result together with the live diff, tests and owner gate. Do not
  poll on a fixed cadence, transcribe progress messages, or create a separate
  handoff/liveness journal merely because an agent is running or a wait window
  ended.
- New tasks do not create `{TASK_DIR}/agent-assignment.json`, raw review rounds,
  progress journals, heartbeat files, daemons, watch loops, or background
  liveness processes. Existing files remain legacy-only migration inputs.
- Persist recovery only when an agent has actually ended unfinished and a
  replacement is genuinely required. Record the unfinished event and its
  replacement through `record-agent-recovery.sh`, then validate the gitignored
  task-keyed checkpoint with `check-agent-recovery.sh`. The scripts validate
  only the explicit recovery chain; they do not infer failure from elapsed time
  or a wait timeout, and the checkpoint is not a Phase 2 or review prerequisite.
- A replacement must carry only the context that cannot be recovered from live
  task files, current diff and terminal output: predecessor identity/terminal
  event, remaining work, validation still pending, and blockers. Do not repeat
  planning, schemas, digests, or already-readable task artifacts as prose.
- Existing active-task schema 2.0 assignment/liveness artifacts remain
  read-only validator inputs. No assignment/liveness recorder or checker
  command is exposed; new installations expose only the minimal private
  recovery checkpoint.
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
- Simple conversation or a non-file-changing small request: answer directly without creating a GitHub Issue or Trellis task and without asking whether one should be created. Ask only when missing intent prevents reliable classification.
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
Classify the request. For repo changes, run Intake and auto-chain mapped internal exits in the same turn. Ask only for missing intent or one bounded issue/workspace/task mutation approval. Do not write task artifacts before approval.
[/workflow-state:no_task]

### Phase 0: Intake

- 0.0 Base sync route `[required · once]`
- 0.1 Change-context discovery `[required · once]`
- 0.2 Requirements clarification `[required · once]`
- 0.3 Contract wording review `[required · repeatable]`
- 0.4 Change-request readiness review `[required · repeatable]`
- 0.5 Task workspace creation `[required · repeatable]`

Run the mapped Phase 0 chain continuously in the same turn. `synced`,
`context_ready`, clear/pass/ready routes, refreshes, and re-entry are internal
control flow, not user checkpoints. Ask only for missing product intent or one
bounded mutation approval that covers the selected Issue action plus the exact
branch, worktree and task creation. Do not ask for generic continuation between
packages and do not persist pre-task stdout as a chain of task-local handoffs.

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
Complete proportionate planning and invoke `guru-approve-task-plan`. The Skill owns schema, review, evidence, and re-entry. Auto-consume mapped exits; ask only when scope or a material plan choice needs user approval.
[/workflow-state:planning]

[workflow-state:planning-inline]
Complete proportionate planning and invoke `guru-approve-task-plan`. Inline execution reads approved plans and specs directly. Auto-consume mapped exits; ask only for unresolved scope or a material plan choice.
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
Implement and check the approved scope. Treat agent terminal output as ephemeral evidence and persist only the final Phase 2 gate. Batch findings before recheck/commit; auto-consume mapped commit and review exits. Publication remains explicit.
[/workflow-state:in_progress]

[workflow-state:in_progress-inline]
Implement inline from approved plans/specs, run the full semantic check, and persist only the final Phase 2 gate. Batch findings before recheck/commit and auto-consume mapped review exits. Publication remains explicit.
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

The implementation agent returns one concise terminal result. Treat it as
ephemeral input to `guru-check-task`; do not create
`implementation-handoff.md` or transcribe live diff/test facts into another
Markdown artifact. A wait timeout is only an observation. Persist recovery
evidence only when an unfinished agent is actually replaced; ordinary
assignment, progress pings and completed output do not need a liveness journal.

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
channel-runtime `check` worker. Its
report is raw evidence only; it never owns Guru pass, scope, severity, route, or
`phase2-check.json`. Persist a private recovery checkpoint only if that worker
actually ends unfinished and is replaced. Then load and invoke the active
public Skill by stable id:

<!-- guru-skill-invoke: {"skill":"guru-check-task","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"passed","consumer":{"kind":"skill","id":"guru-create-task-commit"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-resume-implementation"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"planning_stale","consumer":{"kind":"workflow","id":"guru-task-check-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"blocked","consumer":{"kind":"stop","id":"task-check-blocked"}} -->

<!-- guru-workflow-target: {"id":"guru-resume-implementation"} -->
<!-- guru-workflow-target: {"id":"guru-task-check-planning-router"} -->
<!-- guru-stop-target: {"id":"task-check-blocked"} -->

The package owns all ten entry checks, repository-command selection,
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
`design.md`, `implement.md`, and `pr-body.md`; missing files stay
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
- 3.6 Task publication semantic review `[required · repeatable]`
- 3.7 Finalize and publish `[required · once]`

[workflow-state:completed]
Use `guru-finalize-task`. One approved closeout plan covers push, required verification, Draft PR, archive, and Ready. Auto-route verification and same-plan recovery; stop only for changed side effects, new authority, or a real external blocker.
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

`passed` targets active `guru-review-task-publication` through its target-owned
authoring seed.
`implementation_required` resumes implementation and must then pass a complete
`guru-check-task`, fresh task commit, and this Skill again.
`scope_confirmation_required` routes to requirements clarification; the caller
AI freshly authors the existing clarification profile from current live
evidence and the exact proposal refs. `blocked`, unknown, multiple, stale, or
unmapped results stop fail closed.

Before any Phase 3.5 stop or pass reply, follow the global human-artifact
resolution requirement.

#### 3.6 Task publication semantic review `[required · repeatable]`

After the current Branch Review `passed` exit and before the mandatory
invocation below, the workflow caller is the explicit owner of initial
publication-content authoring. Read the current task-local requirements,
planning approval, Phase 2 result, Issue Scope Ledger, Docs SSOT reconciliation,
Branch Review evidence, and complete reviewed diff, then author current
candidates at `{TASK_DIR}/pr-body.md` and
`{TASK_DIR}/finish-summary-index.json`.

This is producer-side entry preparation, not a second publication review or a
new workflow exit. The caller authors the candidate content but must not decide
PR-body sufficiency, Issue closure, the ten publication dimensions, finding
routes, or readiness. Scripts must not synthesize those semantic conclusions.
The active `guru-review-task-publication` Skill remains the sole semantic owner;
its existing recorder/checker later reuses the deterministic PR-body,
finish-summary-index, artifact, HEAD, and freshness validators after the AI
Review Gate. Do not call that recorder/checker to manufacture entry evidence.
If either candidate is absent or objectively malformed, stop fail closed,
complete this authoring preparation, and do not invoke the Skill.

After both current candidates exist, load and invoke the active public Skill by
stable id:

<!-- guru-skill-invoke: {"skill":"guru-review-task-publication","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-publication","exit":"ready","consumer":{"kind":"skill","id":"guru-finalize-task"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-publication","exit":"return_to_task_work","consumer":{"kind":"workflow","id":"guru-task-publication-work-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-publication","exit":"blocked","consumer":{"kind":"stop","id":"task-publication-review-blocked"}} -->

<!-- guru-workflow-target: {"id":"guru-task-publication-work-router"} -->
<!-- guru-stop-target: {"id":"task-publication-review-blocked"} -->

The caller merges the Branch Review seed with only the target package's fresh
authoring fields. This workflow owns the invocation and the three routes above;
the active Skill owns publication judgment, task-local evidence, metadata-only
revision, recorder/checker, freshness, and re-entry.

`ready` enters active `guru-finalize-task`. `return_to_task_work` resumes implementation and must
then repeat complete Phase 2 check, task commit, Branch Review, and publication
review. `blocked`, unknown, missing, multiple, stale, consumer-mismatched, or
unmapped results stop fail closed.

The active extension verifier is independently discoverable for standalone use
and is conditionally reached from the active finalizer:

<!-- guru-skill-invoke: {"skill":"guru-verify-extension-installation","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-verify-extension-installation","exit":"verified","consumer":{"kind":"skill","id":"guru-finalize-task"}} -->
<!-- guru-skill-exit: {"skill":"guru-verify-extension-installation","exit":"not_required","consumer":{"kind":"skill","id":"guru-finalize-task"}} -->
<!-- guru-skill-exit: {"skill":"guru-verify-extension-installation","exit":"return_to_task_work","consumer":{"kind":"workflow","id":"guru-extension-verification-work-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-verify-extension-installation","exit":"blocked","consumer":{"kind":"stop","id":"extension-installation-verification-blocked"}} -->

<!-- guru-workflow-target: {"id":"guru-extension-verification-work-router"} -->
<!-- guru-stop-target: {"id":"extension-installation-verification-blocked"} -->

The `verification_required` DTO is a machine handoff from finalizer to verifier,
not a user-visible stop. The verifier alone owns applicability, capability
selection, adequacy, findings, retry and actual exit; the runtime only executes,
records and checks objective facts.

#### 3.7 Finalize and publish `[required · once]`

After `guru-review-task-publication:ready`, load and mandatory invoke the active
finalizer. The user confirms one bounded closeout plan before its first Git or
GitHub side effect. That approval covers the declared content push,
plan-required installation verification, one Draft PR, the task archive
transaction, and the Ready transition. A changed side-effect set or changed
authority requires a new plan; internal checkpoints do not.

<!-- guru-skill-invoke: {"skill":"guru-finalize-task","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"verification_required","consumer":{"kind":"skill","id":"guru-verify-extension-installation"}} -->
<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"publication_review_stale","consumer":{"kind":"skill","id":"guru-review-task-publication"}} -->
<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"resume_finalization","consumer":{"kind":"skill","id":"guru-finalize-task"}} -->
<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"reprepare_required","consumer":{"kind":"skill","id":"guru-finalize-task"}} -->
<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"published","consumer":{"kind":"workflow","id":"guru-finalization-finish-response"}} -->
<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"blocked","consumer":{"kind":"stop","id":"task-finalization-blocked"}} -->

<!-- guru-workflow-target: {"id":"guru-finalization-finish-response"} -->
<!-- guru-stop-target: {"id":"task-finalization-blocked"} -->

The finalizer owns plan review, plan-bound confirmation, recovery intent and the six
exits. Its deterministic engine owns the immutable transaction facts. The
workflow automatically consumes `verification_required`,
`publication_review_stale`, `resume_finalization`, and `reprepare_required` in
the same closeout loop. Never display those exit ids as choices or ask for a
generic `确认继续`. Stop only for the declared `blocked` result, missing external
authority, or a materially changed side-effect plan.

For a single current side effect, the user-facing prompt is `确认继续`; any clear
affirmative reply authorizes that displayed action. Internal evidence still
binds the exact HEAD, digest, target, and scope, but the user never repeats
those tokens. A changed or ambiguous plan must be shown and confirmed again.

`guru-verify-extension-installation` is conditional: invoke it only when the
finalizer emits `verification_required`. Its `verified` and `not_required`
results return directly to the same finalizer plan. `return_to_task_work`
resumes implementation and the complete downstream check/review sequence;
`blocked` stops.

The task-local `pr-body.md` and `finish-summary-index.json` are authored before
publication review and are not regenerated after `ready`. Publication review
owns reviewer-facing sufficiency and issue close/ref semantics. The finalizer
validates objective structure and executes push, Draft PR, archive metadata,
three-way HEAD equality and Ready; scripts never invent release judgments.

Existing active tasks may still contain legacy intake snapshots, raw review
rounds, and tracked commit plans. New task commit candidates and real agent
replacement checkpoints live only in gitignored runtime. Closeout plan 1.1 does
not turn compatibility inputs into permanent handoff paperwork: after the
official move it retains only `task.json`, `prd.md`, `design.md`, `implement.md`,
`issue-scope-ledger.json`, `planning-approval.json`, `phase2-check.json`,
`review-gate.json`, `closeout-plan.json`, `task-finalization-gate.json`, and
`finish-summary.json`, plus `marketplace-verification.json` only when that gate
applies. The exact evidence commit and GitHub authority remain the recovery
source for pruned intermediates. A persisted schema 1.0 plan keeps its original
full-move behavior.

On `published`, resolve human artifacts from the archived task and return the
canonical PR URL plus the archive locator. Do not expose private plan, gate,
verification, digest, or checkpoint artifacts in the standard response.

### Rules

1. Phase 0 runs before durable Trellis task creation.
2. The Phase 0 mutation approval, planning/implementation authorization, and
   final publication authorization are distinct; routine work must not add
   confirmation stops between mapped internal exits.
3. Current-checkout direct edits with no active task require explicit user
   approval to skip GitHub issue, Trellis task, worktree, and branch for this
   turn; that approval does not approve commit, push, PR creation, or issue
   closure.
4. Planning artifacts must be persisted before implementation.
5. In business projects, `.trellis/spec/**`, `.trellis/tasks/**`, `docs/**` durable docs, `00-bootstrap-guidelines` generated docs SSOT, and workflow artifact human-readable fields are Chinese by default, with English reserved for literal tokens such as commands, paths, config keys, GitHub keywords, and code symbols.
6. Daily user entry points are natural-language task requests, issue URLs or issue numbers, `trellis-continue`, and `trellis-finish-work`; `trellis-start` remains a fallback / explicit orientation entry for no-auto-injection platforms, disabled hooks, suspected bootstrap failures, or manual context reloads.
7. `review-branch` and `finish-work.sh` are companion script subcommands, not user-facing phases; `publish-pr` is a compatibility-only blocked command. Ordinary direct `finish-work.sh` and every `publish-pr` call are blocked before archive/push/PR.
8. Branch Review Gate belongs after commit and before finalization; do not put it in a non-blocking hook.
9. Push, Draft PR, verification, archive and Ready belong to one finalizer plan; do not ask users to run a separate publish flow.
10. Hooks are reminders and context injection only; the workflow contract owns the Guru Team process.
11. Companion scripts are local project assets under `.trellis/guru-team/`; do not modify Trellis upstream, `node_modules`, or generated copies in business repositories as the long-term source.
12. Long-term Guru Team rules live in this marketplace workflow, preset installer, companion scripts, overlays, and team docs.
13. If a platform command/skill entry must be overridden, use the Guru Team preset overlay and document its relationship with `trellis update`.
14. Spec templates may contain reusable conventions, review checklists, and artifact language rules; they must not contain active task state, Issue Scope Ledger instances, PR runtime state, or project-private business rules.
15. Missing `middle_platform_knowledge.mode` means `optional_warn`; `required` is opt-in only and `off` is opt-out only.
16. `guru-knowledge-center` availability is checked by the AI runtime from available tools/capabilities, not by shell scripts.
17. Trellis task artifacts may act as temporary task evidence, but durable repo docs remain the long-term SSOT when they exist.
18. Active-task recovery artifacts are not automatically long-term archive artifacts; closeout keeps only the plan-declared compact set with a direct history or recovery consumer.
19. Never print tokens, secrets, private keys, signed URLs, `.env` content, or database URLs.

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
