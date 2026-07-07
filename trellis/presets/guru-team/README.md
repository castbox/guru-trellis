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
`trellis-check` and satisfy Branch Review Gate by default. An explicit
`codex.dispatch_mode: inline` value is preserved as a user-selected downgrade
or debug mode.

The preset also installs Guru Team sub-agent definitions. Technical dispatch ids
stay stable (`trellis-implement`, `trellis-check`, `trellis-research`, channel
runtime `implement` / `check`), while UI-facing labels are Chinese where the
platform supports them. Codex uses Chinese `description`, but keeps
`nickname_candidates` ASCII because current Codex rejects non-ASCII nicknames and
ignores malformed agent files. Markdown-based agent files use Chinese
descriptions and headings.

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
example `gh:castbox/guru-trellis/trellis#v0.6.5-guru.1`. That release targets
official `@mindfoldhq/trellis` `0.6.5`. Unpinned `gh:castbox/guru-trellis/trellis`
is a latest/canary source and should be reported as mutable provenance.

## Apply

```bash
git clone --depth 1 --branch v0.6.5-guru.1 \
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
exists, verifies that `check-env.sh` and `version.sh` are executable, asserts
`.trellis/guru-team/extension.json` exists, asserts `.claude/` was not created,
asserts target `.trellis/spec/**`, workspace indexes, and
`00-bootstrap-guidelines` do not retain known English documentation language
requirements, and runs `check-env --json` plus `version.sh --json`. Trellis CLI accepts
`gh:user/repo/path#ref` workflow marketplace sources; the script defaults to
`TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#v0.6.5-guru.1` for stable
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
- `.trellis/guru-team/schemas/intake-handoff.schema.json`
- `.trellis/guru-team/scripts/bash/check-env.sh`
- `.trellis/guru-team/scripts/bash/version.sh`
- `.trellis/guru-team/scripts/bash/prepare-task.sh`
- `.trellis/guru-team/scripts/bash/record-planning-approval.sh`
- `.trellis/guru-team/scripts/bash/check-planning-approval.sh`
- `.trellis/guru-team/scripts/bash/record-phase2-check.sh`
- `.trellis/guru-team/scripts/bash/check-phase2-check.sh`
- `.trellis/guru-team/scripts/bash/record-agent-assignment.sh`
- `.trellis/guru-team/scripts/bash/check-agent-assignment.sh`
- `.trellis/guru-team/scripts/bash/review-branch.sh`
- `.trellis/guru-team/scripts/bash/check-review-gate.sh`
- `.trellis/guru-team/scripts/bash/publish-pr.sh`
- `.trellis/guru-team/scripts/bash/finish-work.sh`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`

Shared overlays are always installed:

- `.trellis/agents/implement.md`
- `.trellis/agents/check.md`
- `.agents/skills/trellis-start/SKILL.md`
- `.agents/skills/trellis-continue/SKILL.md`
- `.agents/skills/trellis-finish-work/SKILL.md`

Default Codex overlays are installed when no platform flag is provided, or when
`--platform codex` / `--all-platforms` is used:

- `.codex/agents/trellis-implement.toml`
- `.codex/agents/trellis-check.toml`
- `.codex/agents/trellis-research.toml`
- `.codex/prompts/trellis-start.md`
- `.codex/prompts/trellis-continue.md`
- `.codex/prompts/trellis-finish-work.md`
- `.codex/skills/trellis-start/SKILL.md`
- `.codex/skills/trellis-continue/SKILL.md`
- `.codex/skills/trellis-finish-work/SKILL.md`

Default Cursor overlays are installed when no platform flag is provided, or when
`--platform cursor` / `--all-platforms` is used:

- `.cursor/agents/trellis-implement.md`
- `.cursor/agents/trellis-check.md`
- `.cursor/agents/trellis-research.md`
- `.cursor/commands/trellis-continue.md`
- `.cursor/commands/trellis-finish-work.md`

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
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.1 \
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
`record-planning-approval.sh` records reviewed planning artifact hashes and the
user confirmation before `task.py start`; `task.py start` remains only a status
transition. `record-phase2-check.sh` records the full-scope `trellis-check`
result before commit, including the pre-commit `dirty_paths`; validation
commands are evidence inside that report, not a substitute for the check.
`record-agent-assignment.sh` / `check-agent-assignment.sh` manage task-local
`agent-assignment.json`: Chinese `logical_role` is the Trellis process identity,
`agent_id` is the technical platform id, and `platform_nickname` is display-only.
When the platform exposes a configured Chinese UI nickname, record that value;
when it exposes only an automatic/random nickname, record the raw value. Either
way, gate decisions use `logical_role`, `agent_id`, HEAD, and digest evidence,
not display names. The scripts record assignment, review round, reuse, and
replacement decisions already made by AI/human; they do not decide which
sub-agent should be used.
After the task work commit, `review-branch.sh` audits that committed
non-metadata task paths after the Phase 2 recorded HEAD are covered by those
dirty paths and that no non-metadata dirty paths remain in the working tree.
Do not re-record Phase 2 after commit just to make HEAD match. `review-branch.sh`
records and validates the prior AI/human review result; it is not the reviewer.
Passing gates require every finding owner to complete a later same-agent
`问题闭环审查代理` review with zero findings for its finding before a fresh `最终放行审查代理`
independent review can pass. The final review must cover the full current HEAD
diff with zero findings of any priority and be recorded with task-local
`review.md`, a Chinese summary, concrete evidence, `--review-source
independent-agent`, `--review-report <task-local review.md>`, and
`--agent-assignment <task-local agent-assignment.json>`. The gate stores the
assignment digest and Chinese roles summary and validates closure-before-final,
the last fresh final round, and that the final reviewer did not own an earlier
finding round. Observations and follow-up candidates may be recorded separately,
but they must not hide current-scope findings. Independent review sub-agents
review docs, code, tests, artifacts, and diff evidence as AI reviewers; they do
not run Guru Team recorder/validator extension scripts such as
`review-branch.sh`, `check-review-gate.sh`, or `record-*`. The main session runs
those scripts only after the review result exists. `--reviewer` is identity metadata
only and cannot replace the review report digest; `*-main-session` /
`self-review` cannot pass the gate.
`finish-work.sh` and `publish-pr.sh` reject ordinary direct calls so
`trellis-continue` cannot chain closeout, commit review metadata, push, or
create a PR before the explicit `trellis-finish-work` entrypoint. Normal PR
publish is triggered only by `finish-work.sh --from-trellis-finish-work` after
archive, journal, and remaining Trellis metadata-only commit succeed; direct
publish is reserved for explicit recovery/debug after finish-work already
completed.

`finish-work.sh --dry-run --from-trellis-finish-work` is a side-effect-free
readiness preview. It validates the gate, dirty state, and PR body/readiness,
then prints the planned archive, journal, metadata commit, and publish actions
without moving task files, writing journal entries, creating commits, pushing,
or creating a PR.

Before finish-work publishes, the AI must generate or review a PR body for
GitHub reviewers who do not know the Trellis task. The body should use concrete
Chinese sections for `变更摘要`, `影响范围`, `验证结果`, `Review Gate`,
`Issue 关闭范围`, and `安全说明`. Low-information summaries such as
`当前 Trellis task`, `已提交实现与文档更新`, or `详见 artifact` are blocked for
non-draft publish. Non-draft publish requires reviewed Markdown with
`--body-file <path>` or a JSON readiness artifact with `--body-artifact <path>`;
generated fallback bodies are preview/draft-only. These readiness/body files
belong to task metadata and are read from the archived task artifact after
finish-work archives the task. The script validates objective structure,
reviewed source presence, and close/ref semantics but does not replace AI
release judgment.

## Workflow Guardrails

For `no_task` issue-backed, task-like, or file-changing requests in a Guru Team
project, the first hop is Guru Team intake, not bare `task.py create`:

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json "<user request or issue URL>"
```

`prepare-task.sh --json` is an intake/preflight planner by default. It may read
an explicit issue and search duplicates, but it does not create a GitHub issue,
worktree, branch, Trellis task, or `.trellis/guru-team/handoff.json`. Freeform
requests without a source issue return `proposed_issue`, `requires_confirmation`,
`naming_quality`, `preflight.base_freshness`, and `handoff_written: false` in
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
`--short-name`, `--workspace-slug`, `--task-slug`, and `--branch` when the title
is Chinese, non-ASCII, or too generic. Recommended worktree/task slug format is
`NNN-business-capability`; recommended branch format is
`codex/NNN-business-capability`, for example
`052-resume-detail-inline-attachment-preview`. `prepare-task` does not perform
Chinese transliteration or pinyin conversion; it deterministically assembles the
name, checks conflicts, and blocks low-information names before executor side
effects.
When `workspace_mode: worktree`, create the execution workspace and task through
`prepare-task --create-worktree --create-task` or an equivalent controlled Guru
Team executor. Task creation consent is not approval to run bare
`python3 ./.trellis/scripts/task.py create ...` in the source checkout.
Executor paths also enforce `naming_quality` and fail closed before creating a
worktree, branch, or Trellis task if the generated or overridden name is low
information, such as `issue-52`, `52-issue-52`, a bare number, or only generic
tokens like `bug`, `fix`, `task`, `work`, `update`, or `change`.

When executor paths create or reuse a worktree, they refresh the selected base
branch again with `git fetch`, record `preflight.base_freshness` in
`handoff.json`, fast-forward the local base only when safe, and fail closed when
the local base diverges from the remote. Planner refresh evidence does not
replace the executor's create-time guard; this prevents new task branches from
silently starting from a stale local base.

After the worktree exists, the executor ensures the target workspace has
Trellis developer identity before writing handoff or creating a task. It copies
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

The workflow also requires Repo Docs SSOT reconciliation. Task artifacts should
record task-scoped deltas and links, while durable `docs/` requirements,
designs, test plans, deploy / operations guides, or versioned docs remain the
long-term source when they exist. Finish and Branch Review Gate evidence must
record the reconciliation outcome.
