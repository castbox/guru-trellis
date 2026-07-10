# Guru Team Trellis Preset

The preset installs companion assets and Guru Team entry overlays for the
`guru-team` Trellis workflow into an existing Trellis project.

It does not run `trellis init` and does not modify Trellis upstream files.
It is idempotent: identical files are skipped, missing files are installed,
Guru-managed companion assets are upgraded in place with `.bak` backups,
existing `.trellis/guru-team/config.yml` is preserved, known upstream
Trellis-generated entry files are replaced with Guru Team overlays, and unknown
local modifications are preserved by writing `.new` copies.

The current config template includes `middle_platform_knowledge.mode:
optional_warn`. Existing target repo configs are not overwritten just to add
this key; if it is absent, the workflow interprets it as `optional_warn`.
`required` is opt-in only, and `off` is opt-out only.

The preset also materializes the project-level `.trellis/config.yaml`
`codex.dispatch_mode` default. Missing, commented-out, or invalid values are
updated to `sub-agent` so Codex can dispatch `trellis-implement` /
`trellis-check` and satisfy Branch Review Gate by default. In that default mode
implementation, Phase 2 check, and post-commit Branch Review are three separate
sub-agent evidence boundaries: `trellis-implement` / channel `implement`
produces implementation handoff, `trellis-check` / channel `check` produces
evidence for `phase2-check.json`, and an independent review sub-agent reviews
the full committed branch diff before the main session records Branch Review
Gate. An explicit `codex.dispatch_mode: inline` value is preserved as a
user-selected downgrade or debug mode; missing sub-agent evidence must fail
closed unless explicit inline/self-exemption artifact evidence exists.

The preset also installs Guru Team sub-agent definitions. Technical dispatch ids
stay stable (`trellis-implement`, `trellis-check`, `trellis-research`, channel
runtime `implement` / `check`), while UI-facing labels are Chinese where the
platform supports them. Codex uses Chinese `description`, but keeps
`nickname_candidates` ASCII because current Codex rejects non-ASCII nicknames and
ignores malformed agent files. Markdown-based agent files use Chinese
descriptions and headings. Implement/check definitions require an unfinished
handoff instead of a false completion claim when the main session interrupts or
replaces a worker, including current diff, remaining work, validation state, and
gate blockers for same-agent resume or replacement handoff.

Platform overlays are selectable. By default, the installer applies shared
`.agents/skills` entries plus Codex and Cursor overlays. Repeat
`--platform <name>` to select a specific set; supported values are `codex`,
`cursor`, and `claude`. Use `--all-platforms` to preserve the historical
full-overlay behavior. `--platform` and `--all-platforms` are mutually
exclusive, and invalid platform names fail closed.

The preset records the installed Guru Team extension version and source
provenance in `.trellis/guru-team/extension.json`. The canonical extension
version lives in `trellis/guru-team-extension.json`; it is separate from the
official Trellis CLI version and from the marketplace index schema version in
`trellis/index.json`.

The preset also normalizes known Trellis-generated English documentation
language rules in target business repositories. It deterministically replaces
the fixed `All documentation ... English` template lines in `.trellis/spec/**`,
`.trellis/workspace/index.md`, `.trellis/workspace/*/index.md`, and
`.trellis/tasks/00-bootstrap-guidelines/**/*.md` with the Guru Team Chinese
documentation rule. It does not scan ordinary task history or translate
business `docs/**`; those documents are governed by the workflow's AI-facing
Chinese documentation contract.

Stable workflow marketplace installs should pin the repo release tag that
combines the target official Trellis CLI version and Guru Team revision, for
example `gh:castbox/guru-trellis/trellis#v0.6.5-guru.3`. That release targets
official `@mindfoldhq/trellis` `0.6.5`. Unpinned `gh:castbox/guru-trellis/trellis`
is a latest/canary source and should be reported as mutable provenance.

## Commit Message Helpers

The preset installs objective helpers for the Guru Team Chinese Conventional
Commits contract:

```bash
.trellis/guru-team/scripts/bash/check-commit-messages.sh --json --task <task-path>
.trellis/guru-team/scripts/bash/format-merge-commit.sh --json \
  --task <task-path> \
  --pull-request <pr-number> \
  --summary "中文 PR 摘要"
```

The helpers validate subject/body shape and format merge commit payloads only.
They do not decide whether implementation, Phase 2 check, Branch Review Gate, or
PR readiness is sufficient. Work commits use
`{type}({scope}): #{primary_issue} 中文描述` with fixed body sections and
`Refs #<primary_issue>`; commit messages must not use close keywords such as
`Closes`, `Fixes`, `Resolves`, `Close`, `Fix`, or `Resolve`; Trellis metadata commits use an empty body; publish
payloads provide `chore(merge): #{pull_request} 合并 #{primary_issue} 中文 PR 摘要`
plus the fixed merge body and explicit `gh pr merge ... --subject ... --body-file ...`
command.

## Apply

```bash
git clone --depth 1 --branch v0.6.5-guru.3 \
  https://github.com/castbox/guru-trellis.git /path/to/guru-trellis
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project \
  --platform codex \
  --platform cursor
```

Examples:

```bash
# Shared overlays plus Claude only.
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project \
  --platform claude

# Shared overlays plus every known platform overlay.
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project \
  --all-platforms
```

## Throwaway Install Verification

Maintainers can verify the stable non-interactive install path with:

```bash
./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

The script creates a temporary Git repo, runs `trellis init -y` with the
`guru-team` marketplace workflow, applies the preset with
`--platform codex --platform cursor`, checks that `.trellis/workflow.md`
exists, verifies that the active workflow requires the three Guru Team planning
artifacts, verifies that `check-env.sh` and `version.sh` are executable,
asserts `.trellis/guru-team/extension.json` exists, asserts `.claude/` was not
created, asserts the active workflow, Codex / Cursor SessionStart hooks, Cursor
sub-agent context hook, brainstorm/check/before-dev skills, and Trellis meta
planning references no longer contain legacy `PRD-only` / lightweight /
optional-design planning hints,
asserts target `.trellis/spec/**`, workspace indexes, and
`00-bootstrap-guidelines` do not retain known English documentation language
requirements, and runs `check-env --json` plus `version.sh --json`. Trellis CLI accepts
`gh:user/repo/path#ref` workflow marketplace sources; the script defaults to
`TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#v0.6.5-guru.3` for stable
release verification. When the source is unpinned
`gh:castbox/guru-trellis/trellis`, the script fails closed on non-`main` branches
or dirty marketplace workflow files unless
`TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` is set. This prevents public remote
sampling from being reported as current-branch marketplace verification. When
it does run, it also exercises the existing-project `trellis workflow
--create-new` preview and forced switch paths. It intentionally lives in this
source repository and is not copied into target business repos as a managed
companion asset.

## Dogfood Overlay Drift Check

After changing any file under `trellis/presets/guru-team/overlays/`, maintainers
must re-apply the preset to this source repository and verify that installed
dogfood copies still match the canonical overlays:

```bash
./trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo . \
  --all-platforms
./trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

`check-dogfood-overlay-drift.sh` is read-only. It compares canonical overlay
files with same-path installed copies in this repository and exits non-zero for
missing or changed copies. It is a source-repository maintainer check and is not
installed into target business repositories as a managed companion asset.

If `apply.sh` creates `.new` or `.bak` files, inspect and resolve them before
committing. A passing drift check is not a replacement for AI review or the
Branch Review Gate.

## Installed Files

Managed Guru Team assets are installed under `.trellis/guru-team/` regardless of
platform selection:

- `.trellis/guru-team/config.yml`
- `.trellis/guru-team/extension.json`
- `.trellis/guru-team/schemas/task-start-context.schema.json`
- `.trellis/guru-team/scripts/bash/check-env.sh`
- `.trellis/guru-team/scripts/bash/version.sh`
- `.trellis/guru-team/scripts/bash/prepare-task.sh`
- `.trellis/guru-team/scripts/bash/check-workspace-boundary.sh`
- `.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh`
- `.trellis/guru-team/scripts/bash/record-planning-approval.sh`
- `.trellis/guru-team/scripts/bash/check-planning-approval.sh`
- `.trellis/guru-team/scripts/bash/record-phase2-check.sh`
- `.trellis/guru-team/scripts/bash/check-phase2-check.sh`
- `.trellis/guru-team/scripts/bash/record-agent-assignment.sh`
- `.trellis/guru-team/scripts/bash/check-agent-assignment.sh`
- `.trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh`
- `.trellis/guru-team/scripts/bash/check-subagent-liveness.sh`
- `.trellis/guru-team/scripts/bash/check-commit-messages.sh`
- `.trellis/guru-team/scripts/bash/format-merge-commit.sh`
- `.trellis/guru-team/scripts/bash/review-branch.sh`
- `.trellis/guru-team/scripts/bash/check-review-gate.sh`
- `.trellis/guru-team/scripts/bash/publish-pr.sh`
- `.trellis/guru-team/scripts/bash/finish-work.sh`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`

Shared overlays are always installed:

- `.trellis/agents/implement.md`
- `.trellis/agents/check.md`
- `.agents/skills/trellis-start/SKILL.md`
- `.agents/skills/trellis-brainstorm/SKILL.md`
- `.agents/skills/trellis-before-dev/SKILL.md`
- `.agents/skills/trellis-check/SKILL.md`
- `.agents/skills/trellis-continue/SKILL.md`
- `.agents/skills/trellis-finish-work/SKILL.md`

Default Codex overlays are installed when no platform flag is provided, or when
`--platform codex` / `--all-platforms` is used:

- `.codex/agents/trellis-implement.toml`
- `.codex/agents/trellis-check.toml`
- `.codex/agents/trellis-research.toml`
- `.codex/hooks/session-start.py`
- `.codex/prompts/trellis-start.md`
- `.codex/prompts/trellis-continue.md`
- `.codex/prompts/trellis-finish-work.md`
- `.codex/skills/trellis-start/SKILL.md`
- `.codex/skills/trellis-continue/SKILL.md`
- `.codex/skills/trellis-finish-work/SKILL.md`
- `.agents/skills/trellis-meta/references/customize-local/change-workflow.md`
- `.agents/skills/trellis-meta/references/customize-local/change-context-loading.md`
- `.agents/skills/trellis-meta/references/local-architecture/context-injection.md`
- `.agents/skills/trellis-meta/references/local-architecture/task-system.md`
- `.agents/skills/trellis-meta/references/platform-files/agents.md`

Default Cursor overlays are installed when no platform flag is provided, or when
`--platform cursor` / `--all-platforms` is used:

- `.cursor/agents/trellis-implement.md`
- `.cursor/agents/trellis-check.md`
- `.cursor/agents/trellis-research.md`
- `.cursor/hooks/session-start.py`
- `.cursor/hooks/inject-subagent-context.py`
- `.cursor/commands/trellis-continue.md`
- `.cursor/commands/trellis-finish-work.md`
- `.cursor/skills/trellis-brainstorm/SKILL.md`
- `.cursor/skills/trellis-before-dev/SKILL.md`
- `.cursor/skills/trellis-check/SKILL.md`
- `.cursor/skills/trellis-meta/references/customize-local/change-workflow.md`
- `.cursor/skills/trellis-meta/references/customize-local/change-context-loading.md`
- `.cursor/skills/trellis-meta/references/local-architecture/context-injection.md`
- `.cursor/skills/trellis-meta/references/local-architecture/task-system.md`
- `.cursor/skills/trellis-meta/references/platform-files/agents.md`

Claude overlays are installed only when `--platform claude` or `--all-platforms`
is used:

- `.claude/agents/trellis-implement.md`
- `.claude/agents/trellis-check.md`
- `.claude/agents/trellis-research.md`
- `.claude/commands/trellis/continue.md`
- `.claude/commands/trellis/finish-work.md`

The active `.trellis/workflow.md` is installed or switched through the official
Trellis workflow marketplace:

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.3 \
  --template guru-team
```

## Spec Bootstrap

`trellis init` may create `.trellis/tasks/00-bootstrap-guidelines/`. That task is
a one-time repository-level prompt to replace generic `.trellis/spec/` templates
with the target repository's real conventions.

The Guru Team preset must not silently complete that task as an install or
upgrade side effect. An AI installer may report that the task exists and explain
what spec files it would inspect or modify, but it should ask the user whether
to complete bootstrap now or leave it for a separate follow-up. If the user does
not explicitly confirm, preserve the task and do not rewrite `.trellis/spec/`
template content.

When the user does confirm bootstrap in a target business repository, generated
or refreshed `.trellis/spec/**` prose and any docs SSOT files created or
completed under `docs/**` must use Chinese human-readable prose by default.
Literal commands, paths, config keys, GitHub keywords, external API names, and
code symbols may remain English.

The daily user-facing entry points are natural-language task requests, issue
URLs or issue numbers, `trellis-continue`, and `trellis-finish-work`. The
`trellis-start` overlay remains installed as a fallback / explicit orientation
entry for platforms without automatic startup injection, disabled or unapproved
hooks, suspected bootstrap failures, or manual context reloads.

Planning, check, review, and publish helpers are internal companion script
subcommands used by the workflow; they are not daily user-facing entries.
`record-planning-approval.sh` records the explicit post-planning confirmation
after the main session completed planning artifact ambiguity review and
displayed task-local links to `prd.md`, `design.md`, and `implement.md`. The
artifact uses schema 1.2, passed `ambiguity_review` evidence,
fixed-scope scanner evidence for `prd.md`, `design.md`, and `implement.md`,
`user_confirmation.source=explicit-post-planning-review`, and hash / size /
modified-time metadata for all three files; Phase 0 intake approval, old
schema/source evidence, missing/non-passed ambiguity evidence, unclassified
controlled-term hits, or `contract_violation` hits must fail closed.
Freshness is based on the three planning document content digests and the
rescanned hit set, not later HEAD drift, metadata tail, or unrelated dirty
paths. `task.py start` remains only a status transition.
`resolve-human-artifacts.sh` is the deterministic fact layer for phase replies:
before a planning stop, Phase 2 completion, Branch Review Gate result,
finish-work dry-run reply, or final archive/publish reply, the AI runs it and
renders a `Markdown 产物 review 表` with only `prd.md`, `design.md`,
`implement.md`, `review.md`, and `pr-body.md`. Missing files are shown without
Markdown links, and JSON evidence such as `phase2-check.json`,
`review-gate.json`, or `agent-assignment.json` is not part of the standard
table.
`record-phase2-check.sh` records the full-scope `trellis-check`
result before commit, including the pre-commit `dirty_paths`; validation
commands are evidence inside that report, not a substitute for the check.
`phase2-check.json` is a Guru Team artifact that freezes the completed
`trellis-check` AI judgment, coverage, validation results, findings, and dirty
paths; it is not the Trellis-native step itself and script recorder/validator
success cannot replace `trellis-check`.
`record-subagent-liveness-event.sh` / `check-subagent-liveness.sh` /
`check-agent-assignment.sh` manage task-local `agent-assignment.json` liveness:
Chinese `logical_role` is the Trellis process identity, `agent_id` is the
technical platform id, and `platform_nickname` is display-only. `agent-assignment.json`
schema 1.1 is the single assignment/status/liveness/review ledger with
`agents[]`, `status_events[]`, `liveness[agent_id].last_scan_snapshot`, review
rounds, and reuse decisions. The liveness recorder writes assignment, progress,
status request, stale, resume/replacement, terminal, and workspace-boundary
audit events already observed by AI/human. The checker is short-lived and
single-sample: it reads task/source checkout snapshots plus recorded progress
event digests, returns one decision, and exits. It never reads platform UI,
sends status requests, terminates agents, or judges implementation quality.
`progress_scan_interval=120s` is scan cadence; `max_progress_silence=180s`
starts at `progress_anchor_at`. Only `status_request_required` authorizes one
status request, and only `stale_allowed` authorizes `stale-assessed`.
`status-requested` does not refresh anchor or extend deadline. Stale cutover
must record `termination_reason=stale_cutover`, `termination_source_event_id`,
and `replacement_reason=max_progress_silence_exceeded`; manual/platform
unfinished termination uses
`termination_reason=manual_or_platform_terminated_unfinished`. Failed, stale,
unfinished, or replacement partial output cannot pass Phase 2 / Branch Review
until a recovery chain reaches `completed`. `record-agent-assignment.sh` remains
for review rounds and reuse decisions; its old `--status-event` path fails
closed.

After the task work commit, `review-branch.sh` audits that committed
non-metadata task paths after the Phase 2 recorded HEAD are covered by those
dirty paths and that no non-metadata dirty paths remain in the working tree.
Do not re-record Phase 2 after commit just to make HEAD match. `review-branch.sh`
records and validates the prior AI/human review result; it is not the reviewer.
Passing gates require every finding owner to complete a later same-agent
`问题闭环审查代理` review with zero findings for its finding, or an explicitly
recorded replacement closure chain when the finding owner failed/interrupted and
cannot continue, before a fresh `最终放行审查代理` independent review can pass. The
final review must cover the full current HEAD
diff with zero findings of any priority, must not continue implementation or
patch missing Phase 2 check work, and be recorded with task-local
`reviews/*.md` raw reports, a final `review.md` rollup that links every raw
report, a Chinese summary, concrete evidence, `--review-source
independent-agent`, `--review-report <task-local review.md>`, and
`--agent-assignment <task-local agent-assignment.json>`. The gate stores the
final review digest, raw `review_reports[]` digests, assignment digest, Chinese roles summary, and status event count, and validates
closure-before-final, unfinished termination recovery-chain completeness, the
last fresh final round, and that the final reviewer did not own an earlier
finding round. Observations and follow-up candidates may be recorded separately,
but they must not hide current-scope findings. Independent review sub-agents
review docs, code, tests, artifacts, and diff evidence as AI reviewers; they do
not run Guru Team recorder/validator extension scripts such as
`review-branch.sh`, `check-review-gate.sh`, or `record-*`. The main session runs
those scripts only after the review result exists. `--reviewer` is identity metadata
only and cannot replace the review report digest; `*-main-session` /
`self-review` cannot pass the gate.
Branch Review also verifies Docs SSOT execution instead of performing it for the
first time. The final reviewer must read the approved `Docs SSOT Plan`,
implementation handoff, `phase2-check.json`, durable docs, task artifacts, and
the full diff, then report any current-scope Docs SSOT inconsistency as a
finding. The reviewer does not merge durable docs or patch missing Phase 2 docs
work.
`finish-work.sh` and `publish-pr.sh` reject ordinary direct calls so
`trellis-continue` cannot chain closeout, commit review metadata, push, or
create a PR before the explicit `trellis-finish-work` entrypoint. Normal PR
publish is triggered only by `finish-work.sh --from-trellis-finish-work` after
archive, journal, and remaining Trellis metadata-only commit succeed. That
metadata tail may include `review.md`, `reviews/*.md`, `review-gate.json`, and
PR readiness files; `check-review-gate` / `finish-work` validate and migrate
raw report digest paths after archive. Direct
publish is reserved for explicit recovery/debug after finish-work already
completed.
After a passed gate, finish-work accepts only Trellis metadata tail. Durable
docs, `.trellis/spec/`, source, tests, schema, config, scripts, preset, overlay,
CI/CD, deployment, migration, or Makefile drift after the gate must return to
Phase 2/3; dry-run and formal finish do not perform a first Docs SSOT merge.

`finish-work.sh --dry-run --from-trellis-finish-work` is a side-effect-free
readiness preview. It validates the gate, dirty state, and PR body/readiness,
then prints the planned archive, journal, metadata commit, and publish actions
without moving task files, writing journal entries, creating commits, pushing,
or creating a PR.
After dry-run, the AI should render the active-task `Markdown 产物 review 表`;
after formal archive, it must rerun the resolver and render the archive-path
table because active task links are no longer the final review entry points.

Before finish-work publishes, the AI must generate or review a PR body for
GitHub reviewers who do not know the Trellis task. The body should use concrete
Chinese sections for `变更摘要`, `影响范围`, `验证结果`, `Review Gate`,
`Issue 关闭范围`, `安全说明`, and `Docs SSOT` / `文档同步`. The Docs SSOT section
states the plan strategy, durable docs updates or no-update reason, task deltas
merged back, task-history-only content, and any follow-up or current PR
limitation. Low-information summaries such as
`当前 Trellis task`, `已提交实现与文档更新`, or `详见 artifact` are blocked for
non-draft publish. Non-draft publish requires reviewed Markdown with
`--body-file <path>` or a JSON readiness artifact with `--body-artifact <path>`;
generated fallback bodies are preview/draft-only. These readiness/body files
belong to task metadata and are read from the archived task artifact after
finish-work archives the task. The script validates objective structure,
reviewed source presence, Docs SSOT section/key presence, and close/ref
semantics but does not replace AI release judgment.

## Workflow Guardrails

For `no_task` issue-backed, task-like, or file-changing requests in a Guru Team
project, the first hop is Guru Team intake, not bare `task.py create`:

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json "<user request or issue URL>"
```

`prepare-task.sh --json` is an intake/preflight planner by default. It may read
an explicit issue and search duplicates, but it does not create a GitHub issue,
worktree, branch, Trellis task, or `.trellis/tasks/<task-slug>/task-start-context.json`. Freeform
requests without a source issue return `proposed_issue`, `requires_confirmation`,
`naming_quality`, `preflight.base_freshness`, and `no task context/runtime write` in
stdout JSON. Planner output fetches or explicitly confirms the selected remote
base before reporting freshness; `fetch_performed: false` must not be treated as
`fresh: true` evidence. When local base is behind remote, planner output reports
`fresh: false`, `status: stale`, keeps `fast_forwarded: false`, and leaves
`local_head_before` / `local_head_after` unchanged. The AI must show the
proposed title/body and duplicate evidence, then rerun with
`--create-issue-confirmed --issue-title ... --issue-body-file ...` only after
approval. A confirmed source issue still remains stdout-only until the user
approves `--create-worktree` or `--create-task`; those executor paths write the
handoff inside the chosen workspace, not as a new-session side effect in the
source checkout.

The AI should read the issue and provide a semantic English short-name through
`--short-name`, `--workspace-slug`, and `--task-slug` when the title is Chinese,
non-ASCII, or too generic; use `--branch` only when a special explicit branch
name is needed. Recommended worktree/task slug format is
`NNN-business-capability`; when `--branch` is omitted, recommended branch format
is `<branch-type>/NNN-business-capability`, for example
`feat/052-resume-detail-inline-attachment-preview`. `prepare-task` does not
perform Chinese transliteration or pinyin conversion; it deterministically
infers a supported branch type, assembles the name, checks conflicts, and blocks
low-information names before executor side effects.
When `workspace_mode: worktree`, create the execution workspace and task through
`prepare-task --create-worktree --create-task` or an equivalent controlled Guru
Team executor. Task creation consent is not approval to run bare
`python3 ./.trellis/scripts/task.py create ...` in the source checkout.
Executor paths also enforce `naming_quality` and fail closed before creating a
worktree, branch, or Trellis task if the generated or overridden name is low
information, such as `issue-52`, `52-issue-52`, a bare number, or only generic
tokens like `bug`, `fix`, `task`, `work`, `update`, or `change`.

The tracked `task-start-context.json` provides only portable `workspace_slug`,
`task_workspace_id`, and repo-relative `task_artifact_dir`; it never provides an
absolute `workspace_path`. In worktree mode, derive and validate the machine-local
task worktree from the current checkout, `.trellis/.runtime/guru-team/**`,
`git worktree list`, and `check-workspace-boundary.sh --task`. Before writing or validating
`planning-approval.json`, `phase2-check.json`, `agent-assignment.json`,
`reviews/*.md`, `review.md`, or `review-gate.json`, run:

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>
```

The helper reports expected workspace, actual repo root, source checkout
status, task worktree status, and suspicious current-task artifacts or review
metadata in the source checkout. It is a deterministic validator/fact snapshot,
not stale judgment, cleanup, or patch migration. Editing tools without an
explicit `workdir` must use absolute paths under the task worktree confirmed by the
boundary helper. The #76 liveness checker uses this source/task fact
layer: source checkout `HEAD`, dirty status, diff stat, or mtime changes are
`workspace_boundary_violation_progress`, not stale evidence.

When executor paths create or reuse a worktree, they refresh the selected base
branch again with `git fetch`, keep `preflight.base_freshness` in the current
planner/executor result only, fast-forward the local base only when safe, and fail closed when
the local base diverges from the remote. Planner refresh evidence does not
replace the executor's create-time guard; this prevents new task branches from
silently starting from a stale local base.

After the worktree exists, the executor ensures the target workspace has
Trellis developer identity before writing task context or creating a task. It copies
the gitignored source checkout `.trellis/.developer` when available, initializes
an equivalent target identity from an explicit `--assignee` when the source file
is missing, and otherwise fails closed with the recovery command
`python3 ./.trellis/scripts/init_developer.py <name>`. This makes the new
worktree immediately usable by `get_context.py`, `task.py list --mine`, and
`add_session.py`.

Current-checkout direct edits while `no_task` is active are allowed only as an
explicit user override. The user approval must say this turn should skip
creating or reusing a GitHub issue, Trellis task, worktree, and branch. Before
editing, the AI must summarize skipped artifacts, current checkout, current
branch, dirty state, side effects, changed-file scope, and the separate
commit/push/PR approval boundary.

The installed workflow tells AI sessions to run a Middle-platform Knowledge Gate
when a task may touch Guru Team SDKs or frameworks. If `guru-knowledge-center`
MCP is available, the AI queries `project_domain=middle-platform` and persists
citations in task artifacts. If the MCP is unavailable, the default
`optional_warn` mode warns and continues.

The workflow also requires a Phase 1 `Docs SSOT Plan`. Task artifacts should
record task-scoped deltas and links, while durable requirements, designs, test
plans, deploy / operations guides, versioned docs, or equivalent repo docs
remain the long-term source when they exist. The plan is preferably authored in
`design.md`; `prd.md` records docs state and requirements impact, and
`implement.md` records the checklist / checkpoint.

The plan records docs state (`complete_docs`, `partial_docs`, `stale_docs`, or
`no_docs`) and strategy (`ssot_first`, `delta_first`,
`bootstrap_or_repair_docs`, or `no_docs_update_needed`). It also records
evidence paths, affected durable docs or checked no-update paths, task artifact
deltas to merge back, and any required merge checkpoint, minimum repair scope,
follow-up limit, or no-update reason. Finish and Branch Review Gate evidence
must later record the reconciliation outcome, but the strategy choice belongs
in Phase 1 planning.

Installed implement/check agents consume that plan during Phase 2. The
implementation handoff names the strategy, durable docs sync result, task
delta merged back, task-history-only content, no-update or follow-up / PR
limits, and whether implementation inputs came from durable docs or an
approved temporary task delta. The Phase 2 check agent then verifies durable
docs, task artifacts, code/schema/config/deploy/test, and validation/test
coverage against the same strategy. `delta_first` must merge durable docs
before final Phase 2 check; `ssot_first` uses revised durable docs as primary
input; `bootstrap_or_repair_docs` must complete the minimum repair or name a
bounded follow-up and PR limitation; `no_docs_update_needed` must still have a
concrete reason after the final diff is reviewed.


## Push 后远端 Marketplace 门禁

修改 marketplace/preset/overlay/schema/public API 的发布路径要求 primary/close issue ledger 先保存精确的 `remote_marketplace_verification: pending` 结构，pending 或普通文字不能通过最终 publish。branch push 后、`gh pr create` 前会执行远端分支 `init`、preview、switch 和 preset reapply，生成 schema-valid 的 task-local `marketplace-verification.json`；成功后脚本把真实 artifact path/SHA-256、verified content HEAD、remote HEAD、publish content HEAD 与命令结果回写 ledger，仅允许 artifact + ledger 两个路径形成 metadata tail。metadata push 后重新校验 artifact、ledger、双路径 diff、remote metadata HEAD 与 review gate，缺失、pending、失败、篡改、HEAD 不匹配或 stale 均阻止创建 PR；该门禁不创建 tag，AI 仍负责 close scope 与 PR readiness 判断。
