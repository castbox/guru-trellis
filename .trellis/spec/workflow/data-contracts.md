# Data Contracts

## Configuration

`trellis/workflows/guru-team/config-template.yml` is the reusable default
configuration. `.trellis/guru-team/config.yml` is a target repository's local
copy and must be preserved by the preset installer.

When adding a config field:

1. Add the default to `DEFAULTS` in
   `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`.
2. Document the field in `trellis/workflows/guru-team/config-template.yml`.
3. Make the parser tolerate missing fields so older installed configs continue
   to work.
4. Decide whether the preset installer needs new preservation or migration
   behavior.
5. Update README or workflow text if users must know the field.

The YAML parser in `load_config()` is intentionally small. It supports simple
scalars, lists, and one level of nested dictionaries used by the current config.
Do not introduce complex YAML structures without replacing or extending the
parser and validating older configs.

## Extension Version Manifest

`trellis/guru-team-extension.json` defines the reusable Guru Team extension
version and public API metadata. `.trellis/guru-team/extension.json` is the
installed provenance copy created by the preset installer in each target repo.

The installed manifest should remain additive/backward-compatible for readers:

- missing manifest means an older install; `check-env` should warn and continue;
- invalid manifest should report `status: invalid` and continue with a clear
  next step;
- new fields should be optional for old installed manifests;
- `source.tree_state` is objective provenance (`clean`, `dirty`, `archive`, or
  `unknown`), not a release-readiness judgment;
- `source.commit` and `source.tree_state` describe the extension source observed
  at apply time. They are not a self-referential claim that the installed
  manifest file is contained in that same commit;
- `selected_platforms` records installer input and should not be inferred from
  directory presence alone.

Do not use `.trellis/guru-team/extension.json` as the canonical source of the
team extension version. The canonical source is `trellis/guru-team-extension.json`.

Repository release tags for the Guru Team extension use repo-level tags that
combine the target official Trellis CLI version and the Guru Team revision,
such as `v0.6.5-guru.2`, not namespaced tags such as
`guru-team/v0.6.5`. The tag must correspond to
`trellis/guru-team-extension.json.version`, and the manifest must expose
`target_trellis_cli` so users can see which official `@mindfoldhq/trellis`
release this Guru Team extension targets. Stable workflow marketplace examples
should use `gh:castbox/guru-trellis/trellis#v0.6.5-guru.2`; unpinned
`gh:castbox/guru-trellis/trellis` means latest/canary and must be reported as a
mutable source in install or upgrade evidence.

Release order matters: merge the manifest/docs PR first, create the annotated
`v<official-trellis-version>-guru.<revision>` tag on the merge commit, verify tag-pinned `trellis init` and
`trellis workflow` marketplace commands, then retire any old competing tag
names only after the new tag is verified.

## Handoff

`.trellis/guru-team/handoff.json` records intake provenance and preflight:

- source issue
- slug, task slug, task title
- `naming_quality` with `ok`, `reason`, `requires_semantic_name`, `current_slug`, and `suggested_override_flags`
- branch, base branch, workspace path
- duplicate-search result
- Issue Scope Ledger seed
- exact task creation command
- preflight evidence
- base freshness evidence under `preflight.base_freshness`

The schema lives at
`trellis/workflows/guru-team/schemas/intake-handoff.schema.json`. Keep it
permissive with `additionalProperties: true` so older and newer helpers can
interoperate.

Do not use `handoff.source_issue` as PR close scope. The task-level
`issue-scope-ledger.json` owns `close_issues`, `related_issues`, and
`followup_issues`.

In `workspace_mode: worktree`, `handoff.workspace_path` is the machine boundary
for task artifact writes. `handoff.preflight.current_checkout` records the
source checkout used for intake and lets boundary validators compare both sides.

Planner-only prepare paths must refresh or explicitly confirm the selected
remote base before reporting `preflight.base_freshness`. The planner may run
`git fetch <remote> <base>` and update the remote-tracking ref, but it must not
fast-forward or otherwise move the local base branch, write handoff artifacts,
create a worktree, or create a task. Its freshness payload must make the
evidence source auditable:

- `fetch_attempted: true` when a remote refresh was attempted;
- `fetch_performed: true` only after the selected remote base was successfully
  refreshed or equivalently confirmed;
- `fast_forwarded: false` for planner-only output;
- `fresh: false`, `status: stale`, and unchanged
  `local_head_before` / `local_head_after` when local base is behind remote;
- `status: diverged` when local and remote are not in an ancestor relationship;
- `status: fetch_failed` or `remote_ref_missing` when remote freshness cannot
  be confirmed.

`fetch_performed: false` must never be presented as `fresh: true` handoff
evidence. If the planner cannot confirm remote freshness, the AI handoff review
must treat the freshness evidence as blocked or stale-risk instead of
approving a task branch from local cache.

Executor prepare paths (`--create-worktree` / `--create-task`) must refresh the
selected base branch before creating the task worktree. Record remote, local
head before/after, remote head, fetch state, fast-forward state, and the ref used
for worktree creation in `preflight.base_freshness`. Fail closed on divergence
or unknown freshness instead of creating a branch from a stale base.

Executor prepare paths must also enforce `naming_quality` before any worktree,
branch, GitHub issue, or Trellis task side effect. Chinese or non-ASCII source
titles must not be transliterated or mechanically converted to pinyin by the
script; the agent reads the issue and passes semantic English naming through
`--short-name`, `--workspace-slug`, `--task-slug`, and `--branch`. Low-information
names such as `issue-52`, `52-issue-52`, a bare number, or only generic tokens
like `bug`, `fix`, `task`, `work`, `update`, and `change` must block create
paths with a user-actionable error. Planner-only output may report
`naming_quality.ok=false` so the handoff review can choose the semantic
override before executor flags are used.

Executor prepare paths must also ensure the selected workspace has
`.trellis/.developer` before handoff/task creation continues. Prefer copying the
source checkout identity into the target worktree. If the source identity is
missing but an explicit developer/assignee name is available, initialize an
equivalent target identity. If neither source identity nor explicit developer is
available, fail closed with a recovery command instead of allowing journal or
`task.py list --mine` to fail later. Record the objective result in
`preflight.developer_identity`.

## Workspace Boundary Snapshot

`check-workspace-boundary --json` and recorder/validator boundary failures use
an additive payload with these fields:

- `status`: `ok` or `blocked`;
- `workspace_mode`: normally `worktree` for Guru Team issue-backed tasks;
- `expected_workspace`: resolved `handoff.workspace_path` when present;
- `actual_repo_root`: repo root for the current command;
- `source_checkout`: resolved `handoff.preflight.current_checkout` when present;
- `task_dir`: resolved current task directory;
- `task_dir_relative`: task path relative to the worktree, usually
  `.trellis/tasks/<task>`;
- `source_checkout_status`: normalized `git status --porcelain` paths from the
  source checkout;
- `task_worktree_status`: normalized `git status --porcelain` paths from the
  expected workspace when known, otherwise the actual repo root;
- `suspicious_source_artifacts[]`: objects with `kind`, `path`,
  `absolute_path`, and optional `matches_current_task` / `error` for source
  checkout handoff, same-task artifacts, review metadata, review directories, or
  dirty paths;
- `errors[]`: machine-verifiable boundary failures.

The payload is audit evidence only. It must remain additive and must not embed
AI judgments about stale state, cleanup, patch migration, issue closure, or
review sufficiency.

## Planning Approval Artifact

`planning-approval.json` is the start gate evidence for Phase 1.4. New
artifacts use `schema_version=1.1` and are valid only after the main session
has displayed task-local links to all three planning documents and the user has
explicitly confirmed after seeing them. Phase 0 handoff approval, generic
workflow confirmation, old `schema_version=1.0`, or
`user_confirmation.source=workflow` must fail closed.

It records:

- task directory and current `HEAD`
- reviewer / AI process identity metadata
- `review_prompt_presented_at` and `approved_at`
- Chinese approval summary and user confirmation evidence with
  `user_confirmation.source=explicit-post-planning-review`
- `reviewed_artifacts[]` entries for `prd.md`, `design.md`, and
  `implement.md`, each with path, sha256, size, and modified-time metadata
- `approved_artifacts[]` as a compatibility alias for the same three entries
- dirty paths at approval time

The artifact is valid while the recorded `prd.md`, `design.md`, and
`implement.md` hashes / sizes still match the current files. `HEAD`,
`modified_at`, and `dirty_paths` are recorded as audit context for when the
user approved the plan; they are not freshness keys. `check-planning-approval.sh`
must verify all three planning docs are present, required digest metadata
exists, sha256 / size still match, and the confirmation source is
`explicit-post-planning-review`. Later implementation commits, metadata tail
changes, or unrelated working-tree dirty paths must not invalidate planning
approval by themselves. If any of the three planning document contents changes,
the validator must fail closed so the workflow can show the three links again
and wait for fresh explicit post-planning user confirmation. `task.py start` is
a status transition only and must not be treated as planning review evidence.

## Phase 2 Check Artifact

`phase2-check.json` is the commit-preflight evidence for Phase 2.2. It records:

- task directory, base branch, current `HEAD`, diff range, and dirty paths
- checker / AI process identity metadata
- task artifacts and spec files read during check
- validation commands and result summaries
- coverage keys for requirements, design, code, tests, spec sync, cross-layer
  consistency, Docs SSOT, and deployment impact
- findings and resolution status

P0/P1/P2 findings block commit until resolved. Validation commands are evidence
inside the report, not a substitute for full `trellis-check` coverage.
`review-branch.sh` must verify Phase 2 check evidence exists before recording
Branch Review Gate. After the task work commit, a Phase 2 artifact recorded at
an ancestor HEAD remains valid only when all later non-metadata committed paths
are covered by the recorded `dirty_paths`, or the later tail is Trellis
metadata only. Any uncovered non-metadata committed path, or any current
non-metadata dirty path, makes the artifact stale.
Branch Review Gate and publish readiness metadata may legitimately change after
Phase 2 because independent final review and release readiness happen after the
task work commit. In post-commit audit mode, the validator may ignore stale
Phase 2 digest entries for task-local `issue-scope-ledger.json`, `pr-body.md`,
`pr-readiness.json`, `agent-assignment.json`, `review.md`, and
`review-gate.json`; those files are instead revalidated by Branch Review Gate
or publish-specific validators before pass or publish. This exception does not
allow source, config, script, docs, schema, preset, overlay, or other
non-metadata drift.

## Agent Assignment Artifact

`agent-assignment.json` is required for Branch Review Gate pass and expected for
new sub-agent-dispatch Guru Team tasks. It records the AI/human assignment decisions
that already happened in the workflow:

- `schema_version`, current task path, and current `HEAD`
- `agents[]` entries for implementation/check/review assignment events
- `logical_role` as the Chinese Trellis process identity
- `agent_id` as the technical platform identity used for continuing/reusing an
  agent
- `platform_nickname` as display-only UI metadata that never participates in
  gate decisions; prefer configured Chinese UI nicknames when the platform
  exposes them, otherwise record the raw automatic/random nickname
- `review_rounds[]` entries with unique, strictly increasing review round
  number, reviewed HEAD,
  findings count, reuse policy, and reuse decision
- `reuse_decisions[]` entries for explicit reuse/replacement decisions across
  rounds
- `status_events[]` entries for wait-window timeout, progress observation,
  stale assessment, continue-waiting, same-agent resume, replacement start,
  unfinished termination, completion, and explicit failure handling

Allowed logical roles are:

- `实现代理`
- `阶段二检查代理`
- `问题发现审查代理`
- `问题闭环审查代理`
- `最终放行审查代理`

The companion recorder/validator may check JSON structure, required fields,
role enum values, HEAD resolvability, current-HEAD freshness when requested,
file digest metadata, status event enum values, required evidence fields, and
objective recovery-chain completeness for Branch Review Gate pass. It must not
decide which sub-agent should be used, whether an agent is stale, whether an
agent should be terminated, whether reviewer reuse is semantically acceptable,
or whether a final release review is sufficient.

`status_events[]` is additive and older artifacts that omit it are normalized
to an empty array by the loader. Each status event records:

- `event`: one of `wait-timeout`, `progress-observed`, `stale-assessed`,
  `continue-waiting`, `resume-same-agent`, `replacement-started`,
  `terminated-unfinished`, `completed`, or `failed`;
- `logical_role`: one of the allowed Chinese roles listed above;
- `agent_id`: technical platform identity, empty only when the platform cannot
  expose it and the human-readable reason explains that fact;
- `platform_nickname`: display-only UI nickname;
- `head`: current Git commit when the status was recorded;
- `observed_at`: ISO-8601 observation time;
- `last_observed_progress_at`: ISO-8601 time of the last observable progress
  when available, required for stale/unfinished termination events;
- `workspace_evidence`: Chinese summary of output, worktree, diff, validation,
  or channel-event evidence;
- `running_command_evidence`: Chinese summary of running, stuck, completed, or
  non-applicable command state;
- `decision`: one of `continue-waiting`, `resume-same-agent`,
  `start-replacement`, `terminate-unfinished`, `mark-completed`, or
  `mark-failed`;
- `reason`: Chinese AI/human rationale for the status handling decision;
- `supersedes_agent_id`: predecessor technical id for `replacement-started`;
- `handoff_summary`: predecessor output, current diff, remaining work, and gate
  blockers for `replacement-started` and `terminated-unfinished`.

`wait_agent`, `trellis channel wait`, or equivalent wait command timeout means
only that the current wait window ended without final completion. It is not a
failure signal and must not be used as pass evidence. A stale assessment is
based on no observable progress for a recent window, default at least 5
minutes, not on total runtime. If `status_events[]` contains
`terminated-unfinished`, a passing Branch Review Gate must fail closed unless
later events show same-agent resume or replacement start and a later
`completed` or `failed` event for that recovery chain. This is an objective
ledger-completeness check; the AI/human review still owns whether the work is
actually complete and whether failed agent output blocks the task.

For Branch Review Gate, any review agent that recorded findings may be reused
only as `问题闭环审查代理` for fix confirmation. This includes a previous
`最终放行审查代理` round that found a new issue. Every finding owner must have a
later same-agent closure round with `findings_count: 0` and
`reuse_decision: reuse-for-closure` before a passing gate can be recorded. That
closure confirms the agent's own finding is closed and does not need to be
repeated for every later HEAD. The final passing review round must be the last
`最终放行审查代理`, use a fresh technical `agent_id` that did not own an earlier
finding round, set `findings_count` to 0, set `reuse_decision` to `new-agent`,
record the reviewed code `HEAD` in `reviewed_head`, and have a unique,
strictly increasing `round` value so no later record can make the final round
ambiguous.

Because `最终放行审查代理` is assigned after the task work commit,
`agent-assignment.json` may receive a post-commit metadata update before Branch
Review Gate. `review-branch.sh` must then receive `--agent-assignment` so the
gate records the current digest, roles, assignment count, review round count,
reuse decision count, and status event count. This does not permit post-commit
changes to non-metadata paths or to non-gate task artifacts.

Project agent definitions have a separate display contract. Technical dispatch
ids (`trellis-implement`, `trellis-check`, `trellis-research`, `implement`,
`check`) are public API. UI-facing text belongs in Codex
Markdown descriptions, headings, and assignment `logical_role`. Codex
`nickname_candidates` must stay ASCII in current Codex releases. Do not use
`agent-assignment.json.platform_nickname` as the source of dispatch behavior.

## Issue Scope Ledger

Issue close semantics must be explicit:

- `primary_issue` is intake context and usually the default close candidate.
- `close_issues` are issues the current task fully resolves and may close.
- `related_issues` are references only.
- `followup_issues` are future work and must never be closed by the current PR.

Publish is blocked when a close issue lacks acceptance evidence or the Branch
Review Gate did not record coverage for that issue. Existing enforcement:

- `validate_ledger_for_publish()`
- `build_pr_body()`

## Review Gate Artifact

`review-branch.sh` writes `review-gate.json` in the task directory by default.
The artifact records:

- base branch/ref and current `HEAD`
- diff range
- changed files and classified deployment impact
- review scope
- conclusion summary
- reviewer identity metadata
- independent review source metadata (`review_source: independent-agent`) for
  both passed gates and failed findings artifacts
- required review report digest: `review_report.path`, `sha256`,
  `size_bytes`, and `modified_at`
- findings
- observations
- follow-up candidates
- Issue Scope Ledger coverage
- validation evidence
- required `agent_assignment` digest summary from task-local
  `agent-assignment.json`
- objective language-template validation evidence: `review.md` and raw
  `reviews/*.md` reports are Chinese human-readable task artifacts, so
  validators may reject fixed English template headings while leaving semantic
  sufficiency to the AI/human review

The gate is valid only for the reviewed `HEAD`, except that `finish-work` may
allow metadata-only commits after the gate. A passed gate is invalid if it lacks
review report metadata, `review_source: independent-agent`, or a task-local
file named `review.md`. `--reviewer` alone is only identity metadata and cannot
prove the review report evidence; main-session/self-review identities are
rejected for passed gates. Enforcement lives in `validate_review_gate()` and
`metadata_only_since()`.

A failed findings artifact is also invalid recorder evidence when it lacks
`review_source: independent-agent` or a task-local `review.md` digest. Its
`conclusion.passed` must be `false`; `passed=true` is reserved for explicit
`--pass` with zero findings.

After `task.py archive`, the archived task is the new task-local boundary.
Validators may accept a gate whose digest entries still point at the
pre-archive active task path when the corresponding archived files exist and
their content digests match. Finish/publish recovery may then rewrite only the
task path, ledger path, `review_report`, and `agent_assignment` digest metadata
to the archived task path before committing Trellis metadata. This does not
change the reviewed code `HEAD` or the AI review conclusion.

Branch Review Gate treats every finding priority (`P0`, `P1`, `P2`, `P3`) as
blocking. `observations[]` are non-blocking notes, and
`followup_candidates[]` are out-of-scope future work candidates. They must not
be used to hide current-scope defects.

## JSON and Text Encoding

All JSON artifacts should be UTF-8, formatted with two-space indentation, and
written with `ensure_ascii=False` because Chinese summaries and evidence are
first-class data.

Validate JSON assets with:

```bash
python3 -m json.tool trellis/index.json
python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json
```

## Common Mistakes

- Adding a config key to `config-template.yml` without adding a default in
  `DEFAULTS`.
- Adding a new handoff field that is required by code but absent from the JSON
  schema or older installed handoffs.
- Letting PR generation close `related_issues` or `followup_issues`.
- Recording review-gate evidence that does not mention deployment impact.
