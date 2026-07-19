# Overlay Guidelines

## Canonical Relationship

Public workflow skill semantics are canonical under
`trellis/skills/guru-team/`. Generated copies in `.agents/skills/`,
`.codex/skills/`, `.cursor/skills/`, and `.claude/skills/` are runtime discovery
copies or format adapters. They must point back to the package/interface and
must not own or expand the step-local behavior. Workflow marketplace selection
does not install these copies; preset apply does.

Overlay files are small platform entrypoints. They should point the AI back to
`.trellis/workflow.md` and the Guru Team companion scripts instead of
duplicating the full workflow.

The current overlay tree is also a frozen migration surface. Its exact 43 paths
and payload hashes are recorded in
`trellis/presets/guru-team/ownership/upstream-ownership.json`; no new
upstream-owned path may be added. New reusable behavior belongs in Markdown
workflow contracts or canonical `guru-*` packages. Reviewed removal keeps an
`upstream_owned/removed` inventory tombstone instead of deleting audit history.

Activating `guru-approve-task-plan` is additive distribution: install its
canonical package below `.trellis/guru-team/skills/**`, shared runtime/schema
below `.trellis/guru-team/**`, and generated `guru-*` discovery copies for the
selected platforms. It must not add or modify a file below the frozen
`trellis/presets/guru-team/overlays/**` tree. Platform entry prose may route to
the stable Skill id but must not duplicate its planning review loop.

Reference overlay groups:

- `.agents/skills/trellis-start/SKILL.md`
- `.agents/skills/trellis-brainstorm/SKILL.md`
- `.agents/skills/trellis-before-dev/SKILL.md`
- `.agents/skills/trellis-check/SKILL.md`
- `.agents/skills/trellis-continue/SKILL.md`
- `.agents/skills/trellis-finish-work/SKILL.md`
- `.trellis/agents/implement.md`
- `.trellis/agents/check.md`
- `.codex/agents/trellis-implement.toml`
- `.codex/agents/trellis-check.toml`
- `.codex/agents/trellis-research.toml`
- `.codex/hooks/session-start.py`
- `.cursor/agents/trellis-implement.md`
- `.cursor/agents/trellis-check.md`
- `.cursor/agents/trellis-research.md`
- `.cursor/hooks/session-start.py`
- `.cursor/hooks/inject-subagent-context.py`
- `.codex/prompts/trellis-start.md`
- `.codex/skills/trellis-continue/SKILL.md`
- `.claude/commands/trellis/continue.md`
- `.cursor/commands/trellis-finish-work.md`
- `.agents/skills/trellis-meta/references/local-architecture/task-system.md`
- `.agents/skills/trellis-meta/references/local-architecture/context-injection.md`
- `.agents/skills/trellis-meta/references/customize-local/change-context-loading.md`
- `.agents/skills/trellis-meta/references/customize-local/change-workflow.md`
- `.agents/skills/trellis-meta/references/platform-files/agents.md`
- `.cursor/skills/trellis-brainstorm/SKILL.md`
- `.cursor/skills/trellis-before-dev/SKILL.md`
- `.cursor/skills/trellis-check/SKILL.md`
- `.cursor/skills/trellis-meta/references/local-architecture/task-system.md`
- `.cursor/skills/trellis-meta/references/local-architecture/context-injection.md`
- `.cursor/skills/trellis-meta/references/customize-local/change-context-loading.md`
- `.cursor/skills/trellis-meta/references/customize-local/change-workflow.md`
- `.cursor/skills/trellis-meta/references/platform-files/agents.md`

## Required Content

All Guru Team overlays should include the marker:

```markdown
<!-- guru-team-overlay: v1 -->
```

Continue entries must:

- preserve the global workflow's Phase 0 mandatory `guru-sync-base` route:
  tool-free classification first, `synced` to `guru-discover-change-context`,
  `skipped` to the original non-repo route, and `blocked` to a fail-closed stop;
  platform entry text must not copy resolution/executor/validator internals;
- preserve the subsequent mandatory semantic Skill route:
  `guru-discover-change-context:context_ready` to
  `guru-clarify-requirements`, `refresh_base` to `guru-sync-base`, and
  `blocked` to `change-context-blocked`; platform entry text must load the
  stable id and must not copy current/history/Gate internals;
- preserve the active `guru-clarify-requirements` invocation and typed exits:
  `clear` to workflow target `guru-requirements-clear-router`, `needs_context` to
  `guru-discover-change-context`, `refresh_context` to `guru-sync-base`,
  `new_task` to workflow target `guru-full-task-intake-chain`, and `blocked` to
  `requirements-clarification-blocked`; platform entry text must load the
  stable id and must not copy its question/action/confirmation/Gate internals;
- preserve the thin readiness-to-workspace transition:
  `guru-review-change-request:ready` mandatory invokes active
  `guru-create-task-workspace`; its `created` exit enters Phase 1,
  `refresh_review` returns to `guru-sync-base`, and `cancelled` / `blocked`
  stop fail closed. Platform entries must not copy target, naming, assignee,
  confirmation, recorder, executor, schema, or recovery internals. #112 adds
  only Guru-owned package/runtime/discovery assets and does not authorize any
  physical change below the frozen overlay tree;
- keep active-task Scope Change mandatory invocation and caller-aware resume
  routing in canonical workflow/package sources. Do not patch the frozen
  upstream-owned continue overlay to implement those semantics;
- keep canonical `guru-workflow-target` / `guru-stop-target` declarations in
  the workflow only. Activating this package does not authorize editing or
  adding frozen upstream-owned overlay payloads; preset-generated `guru-*`
  discovery copies come from the package installer, not this overlay tree;

- run `python3 ./.trellis/scripts/get_context.py`
- run `python3 ./.trellis/scripts/get_context.py --mode phase`
- route by task status
- apply the business-project Chinese documentation default from `.trellis/workflow.md` across `.trellis/spec/**`, `.trellis/tasks/**`, `docs/**`, `00-bootstrap-guidelines` docs SSOT, and human-readable workflow artifact fields
- in `planning`, after `prd.md`, `design.md`, and `implement.md` exist, display
  clickable or absolute links to all three task-local planning documents and
  stop until the user explicitly confirms after seeing them; Phase 0 handoff
  approval, old schema/source, or missing/non-pass/stale
  `guru-review-contract-wording:planning_artifacts` evidence cannot substitute
- in `planning`, before displaying the three task-local planning documents,
  mandatory invoke `guru-review-contract-wording` with fixed profile
  `planning_artifacts`; only checker-validated evidence containing the
  canonical contract's exact, explicitly AI-reviewed planning-only dimensions
  may pass. Overlays should point to the workflow/package and must not duplicate
  vocabulary, classifications, dimension catalog, scanner, or semantic loop
- state that complete same-profile re-entry supersedes current
  `content_changed`/`blocked` task-local evidence only with a different, fully
  current result bound to the exact prior `facts_sha256`; stale evidence uses
  the separate stale replacement path, and identical results and current
  `pass` remain protected. Do not make overlays decide semantic route intent or
  duplicate the package's transition validation
- in `planning`, remind the AI to create or update the `Docs SSOT Plan`
  required by `.trellis/workflow.md`; do not paste the full enum/strategy
  contract into every overlay
- before any planning, Phase 2, or Branch Review stop/completion reply, run
  `.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh --json --task
  <task-path>` and output a `Markdown 产物 review 表` with only `prd.md`,
  `design.md`, `implement.md`, `review.md`, and `pr-body.md`; rows with
  `exists=false` must not be rendered as Markdown links, `review.md` is the
  AI/human review report after Branch Review, raw `reviews/*.md` are reached
  through `review.md`, and JSON artifacts stay out of the standard table
- state that Phase 1 mandatory invokes `guru-approve-task-plan`, whose single
  `planning-approval.json` uses schema `guru-planning-approval-2.0`, current
  wording/authority/planning/Docs SSOT bindings, four-class provenance,
  unusual-proposal dispositions, distinct confirmations, AI Gate, facts digest,
  and four typed exits; platform text must not copy that step-local loop
- state that schema 1.0 wording evidence missing the planning-only field is
  stale and requires complete AI re-review, redisplay of all three planning
  documents, and fresh post-planning confirmation; never patch old evidence
- in `in_progress`, rerun `check-planning-approval.sh --json` before dispatching
  `trellis-implement` / channel `implement` or recording `phase2-check.json`
- in `in_progress`, tell the AI to consume the approved `Docs SSOT Plan` during
  Phase 2: implementation handoff records strategy execution and docs sync
  outcome, while `trellis-check` verifies durable docs / task artifacts /
  code/API/schema/config/deploy/test consistency by strategy
- after a fresh final Phase 2 pass, load and mandatory invoke the stable
  `guru-create-task-commit` id, then consume only its declared typed exit;
  continue/command/prompt/launcher entries must not copy candidate fields, AI
  review criteria, confirmation policy, executor steps, message template or
  postconditions
- route `committed` to Branch Review/finding closure,
  `revision-required` back to the same skill, and `blocked` to fail-closed stop;
  non-metadata finding fixes return through implementation and full Phase 2
  before another invocation
- state that default `sub-agent` mode requires the main session to dispatch
  `trellis-implement` / channel `implement`, then `trellis-check` / channel
  `check`, and later a Branch Review review sub-agent; the main session cannot
  replace those boundaries with its own implementation, check, self-review, or
  script validation output
- write task-local Chinese `reviews/*.md` raw reports and a Chinese
  `review.md` rollup, run Branch Review Gate with `--review-source
  independent-agent` and `--review-report <task-local review.md>`, then stop
  before finish-work
- state that Branch Review is the final verification of Phase 2 Docs SSOT
  reconciliation: it reads the approved `Docs SSOT Plan`, implementation
  handoff, `phase2-check.json`, durable docs, task artifacts, and the full diff;
  it must not first merge durable docs or patch missing Phase 2 docs work
- state that current-scope Docs SSOT inconsistency is a blocking finding and
  may not be downgraded to `observation` or `followup_candidate`
- state that any finding priority blocks Branch Review Gate, while
  `observation` and `followup_candidate` are separate non-blocking records
- state that a review agent with findings may only perform closure review and
  must do that same-agent closure review before the passing gate can use a fresh
  `最终放行审查代理`
- state that independent review sub-agents review docs/code/diff evidence as AI
  reviewers and must not run Guru Team recorder/validator extension scripts
  such as `review-branch.sh`, `check-review-gate.sh`, or `record-*`; the main
  session runs those scripts only after review
- state that passing Branch Review Gate requires task-local
  `--agent-assignment`
- state that `wait_agent`, `trellis channel wait`, or equivalent timeout is only
  a wait-window result, not failure or partial-completion evidence
- state the #76 liveness loop: after dispatch the main session records
  `assigned` through `record-subagent-liveness-event.sh`, runs
  `check-subagent-liveness.sh` at `progress_scan_interval=120s` or
  `next_wait_ms`, writes non-machine-readable progress to `status_events[]`
  before checker evidence, sends status request only after
  `status_request_required`, records `status-requested` then immediately
  rechecks, does not repeat a pending ping, records `stale-assessed` only after
  `stale_allowed`, and performs stale cutover with
  `terminated-unfinished termination_reason=stale_cutover` plus
  `replacement-started replacement_reason=max_progress_silence_exceeded`
- state that `max_progress_silence=180s` is measured from
  `progress_anchor_at`; `status-requested` does not refresh that anchor or
  extend `max_progress_silence_deadline_at`
- state that failed, stale, unfinished, or replacement partial output must not
  become Phase 2 / Branch Review pass evidence until same-agent resume or
  replacement recovery reaches `completed`; replacement `failed` requires
  further recovery
- state that main-session self-review cannot pass Branch Review Gate; if
  independent Agent review is unavailable, continue must stop with the gate
  pending
- state that `trellis-continue` must not stage/commit review metadata, push,
  create a PR, call `publish-pr`, or invoke `finish-work`
- avoid adding a separate user-facing publish step

Finish entries must:

- call `.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work`
- require the AI to create/review task-local `finish-summary-index.json` and pass
  it through `--finish-summary-index-file` for dry-run and formal finish
- explain that the `--from-trellis-finish-work` marker belongs only in explicit
  finish entries and must not be copied into continue entries
- explain that finish-work binds an immutable plan, creates a draft PR, records
  final task-local `finish-summary.json` before archive, never calls
  `add_session.py` or reads/writes `.trellis/workspace/**`, and marks the PR
  ready only after archive HEAD alignment
- explain that after finish-work dry-run the AI must run
  `resolve-human-artifacts.sh` against the active task and output the active
  `Markdown 产物 review 表`, and after formal archive it must run the resolver
  again against the archive path/name and output the archive-path table
- explain that finish-work may commit Trellis metadata-only changes after the
  reviewed HEAD, but rejects non-metadata changes
- explain that one exact draft PR is bound before final projection; recovery
  validates committed plan/readiness and active/archive/Git/remote/PR facts,
  reuses one draft, creates one for zero, and fails closed for multiple
- explain that finish-work/archive never performs the first Docs SSOT merge;
  durable docs, `.trellis/spec/`, source, tests, schema, config, scripts,
  preset, overlay, CI/CD, deployment, migration, and Makefile drift after the
  gate must return to Phase 2/3
- require the reviewed PR body to include a `Docs SSOT` / `文档同步` result with
  strategy, durable docs update or no-update reason, merged task delta,
  task-history-only content, and follow-up/current PR limitation
- explain that the gate must already contain task-local `review.md`
  `review_report` digest evidence and raw `review_reports[]` digest evidence,
  and that those Markdown reports are already Chinese human-readable task
  artifacts except for literal command/path/JSON/HEAD/API/code tokens
- state that only `close_issues` may use close keywords

Start entries must:

- identify themselves as fallback/explicit orientation
- load only phase, packages, current-task, and Git facts; never run bare
  `get_context.py` or open/enumerate `.trellis/workspace/**`
- support natural-language issue-backed intake when no active task exists
- ask for consent before creating GitHub issues, worktrees, branches, or Trellis
  tasks unless explicitly requested
- treat `handoff.json` as intake provenance only

SessionStart, sub-agent context injection, brainstorm, and trellis-meta reference overlays must:

- stay context-injection/documentation surfaces only; do not move AI planning
  sufficiency judgment into Python hooks
- avoid legacy `PRD-only`, lightweight-PRD-only, or optional design/implement
  planning wording for Guru Team start gates; if they mention native Trellis
  optional planning behavior, they must explicitly say it is not the Guru Team
  start gate and that Guru Team requires `prd.md`, `design.md`, and
  `implement.md` before implementation
- point agents back to workflow-state / `.trellis/workflow.md` for the full
  process instead of duplicating the workflow in hooks
- keep Codex/Cursor SessionStart free of journal helper imports/calls and prove
  with a fresh-install access-guard sentinel that workspace journal path,
  basename, content, and line count are neither read nor output

Sub-agent overlay entries must:

The 43 inventory-pinned upstream overlay payloads remain byte-frozen
`transitional_legacy` assets owned by issue #132. Their legacy `schema 1.2`
and `explicit-post-planning-review` implement-agent wording is retained only as
transitional history; it must not guide current Guru package/runtime behavior
or be copied into canonical `guru-*` packages, workflow contracts, durable
docs, or new non-frozen platform sources.

- keep technical dispatch `name` values stable;
- use Chinese UI-facing descriptions and headings;
- for Codex custom agents, keep `nickname_candidates` ASCII so Codex loads the
  agent file, and put the Chinese display role in `description`;
- keep recursion guards and task-context loading preludes intact;
- require implement agents to run `check-planning-approval.sh --json --task
  <task-path>` before reading implementation context or editing, and to report
  `Implementation Blocked` if the artifact is missing, is not the Skill-owned
  `guru-planning-approval-2.0` closed union, does not have
  `typed_exit=approved`, fails the shared
  `check-planning-approval --require-exit approved` validator, lacks current
  wording/authority/Docs SSOT/provenance/AI Gate evidence, does not carry
  `user_confirmation.kind=post-planning-approval` with confirmed timestamps,
  or the reviewed planning document content digests no longer match;
- require implement agents to output a completion handoff with files changed,
  requirement/design carryover, verification state, remaining risks, completion
  status, and focus areas for `trellis-check`;
- require implement agents to read the task `Docs SSOT Plan`, execute
  `ssot_first` / `delta_first` / `bootstrap_or_repair_docs` /
  `no_docs_update_needed`, and include strategy, durable docs sync result, task
  delta merge, task-history-only content, no-update reason or follow-up / PR
  limitation, and durable-docs versus task-delta implementation inputs in the
  handoff;
- require check agents to distinguish Phase 2 check from Branch Review: Phase 2
  may self-fix small in-scope mechanical issues and must output evidence that
  can support `phase2-check.json`; Branch Review is review-only over the full
  committed diff and must report, not patch, missing implementation/check work;
- require check agents in Phase 2 mode to run
  `check-planning-approval.sh --json --task <task-path>` before reviewing the
  implementation diff, and to treat missing/old/non-pass/stale planning wording
  evidence as a start-gate blocker; Branch Review mode verifies recorded gate
  evidence without running Guru Team recorder/validator scripts;
- require check agents in Phase 2 mode to verify durable docs, task artifacts,
  code/schema/config/deploy/test, and validation/test coverage against the
  approved `Docs SSOT Plan`, including final checks for `delta_first`,
  `ssot_first`, `bootstrap_or_repair_docs`, and `no_docs_update_needed`;
- require check agents in Branch Review mode to use Chinese report templates for
  raw `{TASK_DIR}/reviews/*.md` reports and final `{TASK_DIR}/review.md`
  rollup content: Chinese headings, Chinese labels, Chinese review narrative,
  Chinese deployment / safety and Docs SSOT judgment, Chinese observations and
  follow-up candidates, and Chinese conclusion;
- require unfinished handoff reporting when interrupted/replaced before
  completion, including current diff, remaining work, validation state, and gate
  blockers for same-agent resume or replacement;
- require agents to respond to explicit main-session status requests with
  platform-visible current step, last concrete progress, active command/tool,
  changed files or review scope, remaining work, and blockers; agents must not
  emit periodic heartbeat messages and must not write `agent-assignment.json` or
  any liveness artifact themselves;
- avoid turning agent files into workflow judgment rules.

## Cross-Platform Consistency

When changing one overlay, search all copies:

```bash
find trellis/presets/guru-team/overlays -type f | sort
rg "Branch Review Gate|finding|observation|followup-candidate|最终放行审查代理|finish-work|handoff.json|PRD-only|guru-team-overlay" trellis/presets/guru-team/overlays
```

After canonical overlay edits, re-apply the preset to this source repository and
run the dogfood drift check:

```bash
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

The drift check is read-only and only verifies file presence/content equality.
It does not decide whether an overlay change is semantically correct.

Keep platform-specific command names only where needed, such as
`/trellis:finish-work` for Claude and `/trellis-finish-work` for Cursor.

## Anti-Patterns

- Pasting the entire workflow into every overlay.
- Creating platform-only semantics that do not exist in
  `trellis/workflows/guru-team/workflow.md`.
- Omitting the overlay marker, which makes installer conflict detection weaker.
- Mentioning publish as a separate user-facing step.
- Adding an upstream namespace overlay or managed-path claim outside the frozen
  ownership inventory.
