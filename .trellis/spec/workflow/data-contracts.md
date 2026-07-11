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
such as `v0.6.5-guru.3`, not namespaced tags such as
`guru-team/v0.6.5`. The tag must correspond to
`trellis/guru-team-extension.json.version`, and the manifest must expose
`target_trellis_cli` so users can see which official `@mindfoldhq/trellis`
release this Guru Team extension targets. Stable workflow marketplace examples
should use `gh:castbox/guru-trellis/trellis#v0.6.5-guru.3`; unpinned
`gh:castbox/guru-trellis/trellis` means latest/canary and must be reported as a
mutable source in install or upgrade evidence.

Release order matters: merge the manifest/docs PR first, create the annotated
`v<official-trellis-version>-guru.<revision>` tag on the merge commit, verify tag-pinned `trellis init` and
`trellis workflow` marketplace commands, then retire any old competing tag
names only after the new tag is verified.

## Task Start Context and Local Runtime

`.trellis/tasks/<task-slug>/task-start-context.json` is the task-local, tracked, portable intake context. Its schema is `trellis/workflows/guru-team/schemas/task-start-context.schema.json`, uses `additionalProperties: false`, and allows only source issue/repo metadata, task and branch identifiers, repo-relative `task_artifact_dir`, base refs/SHAs, portable workspace ids, actor metadata, issue-ledger seed, and compact duplicate/naming/confirmation summaries. It must never contain absolute paths, `.trellis/.runtime/**`, full preflight payloads, dirty/fetch process logs, existing worktree lists, developer identity paths, or command paths.

Local-only reusable mappings live under the gitignored producer namespace:

- `.trellis/.runtime/guru-team/workspaces/<workspace-slug>.json`
- `.trellis/.runtime/guru-team/tasks/<task-slug>.json`

Runtime cache may contain absolute worktree paths and executor timestamps, but it is disposable, untracked, has no index/developer dimension, and must be reconstructable from the current checkout, task-start-context, `git worktree list`, or explicit parameters. Ordinary task commands read tracked shared config but do not rewrite it.

Planner-only prepare remains stdout-only and writes neither task context nor runtime cache. `--create-worktree` writes/reuses the worktree and local runtime workspace mapping. `--create-task` creates the task, writes `task-start-context.json` and `issue-scope-ledger.json` in that task directory, then writes task/runtime mappings. Naming quality, base freshness, and developer identity remain deterministic executor preconditions and stdout evidence, not fields copied wholesale into the portable task context.

Do not use `task-start-context.source_issue` as PR close scope. The task-level `issue-scope-ledger.json` owns `close_issues`, `related_issues`, and `followup_issues`.

## Finish Summary

`trellis/workflows/guru-team/schemas/finish-summary.schema.json` is the shared
schema SSOT for normal finish and #100 backfill. Normal finish uses generator
`guru-team.finish-work`; backfill uses `guru-team.finish-summary-backfill` and
must carry conditional `backfill` metadata. The Python validator is strict about
field sets, types, lengths, counts, enums, SHA/issue/PR formats, clean relative
paths, normalized duplicates, adjacent repeated clauses, source-artifact links,
and all derived search/retrieval facts.

Duplicate identity is domain-specific. Every path-bearing array, including
`git.changed_paths`, `index.search_terms.paths`,
`index.affected_surfaces[].paths`, and `backfill.source_artifacts`, uses the
exact path string as identity; punctuation-removing text normalization must not
collapse two different valid Git paths. Generators sort and deduplicate Git
paths by exact string, and validators still reject exact duplicates. Non-path
semantic and search-token string arrays continue to reject duplicates after
text normalization.

The AI input is task-local `finish-summary-index.json` with schema version 1 and
only semantic index fields. It accepts at most 19 `contract_changes`; the final
schema accepts 20 so the recorder always has capacity for the fixed
protected-path filtering fact. Final facts come from `task.json`,
`task-start-context.json`, Issue Scope Ledger, Git, archived artifact existence,
UTC time, and publish output. Final artifacts live at
`.trellis/tasks/archive/<YYYY-MM>/<task>/finish-summary.json`; values may not
contain absolute, parent, workspace, runtime, backslash, CR, or LF paths, and
may not contain leading or trailing whitespace. Backfill `source_artifacts`
remain structurally valid without a task directory, but when an archived
`task_dir` is available every clean source path must name an existing file.

The final pre-archive snapshot combines a NUL-delimited base-to-working-tree
diff with NUL-delimited untracked file enumeration; task metadata is recorded
as individual files, never as an untracked directory placeholder. The
protected-prefix filter and fixed fact rules apply to this snapshot. If the
required diff snapshot fails, both path arrays are `[]`, the
filtering fact is removed, and exactly one fixed non-disclosing
`finish-summary git path snapshot unavailable` fact is recorded before
`retrieval_text` is re-derived. After the unique draft PR is bound, the final
projection sorts and deduplicates raw base-to-HEAD paths, filters
workspace/runtime protected prefixes, and writes the safe set to both
`git.changed_paths` and search `paths`. A non-empty filtered set adds one fixed
`finish-summary protected path filtering` contract fact without path, basename,
or count details; an empty filtered set adds no such fact. Schema and Python
validation reject protected prefixes in every path field. The final summary is
built once in the active task after draft PR binding and moves unchanged to the
archive locator. Readiness binds repo/base/head, reviewed HEAD, exact title,
`pr-body.md`, body SHA-256, `draft=true`, reviewed source, and
`closeout_plan_digest`. Active-state recovery consumes committed plan/readiness
plus Git/remote and PR facts. Reuse and final projection require one exact PR
number/URL/title/body identity; one matching draft is reused, zero creates one,
and multiple identities fail closed. The real-PR final summary has one
deterministic UTF-8 JSON byte representation and digest. Pre-move continuity
and incomplete post-move recovery rebuild those bytes from the immutable
summary template plus the already-bound remote PR number/URL, so a summary and
its PR identity cannot be changed together. After the exact archive commit
exists, fresh recovery reads only that commit's `finish-summary.json` blob,
strictly parses the canonical PR URL and unique PR ref, rebuilds the expected
bytes/digest, and recovers the original number/URL. It does not read the
archived working-tree summary or invoke the general finish-summary artifact
validator. The recovered PR must still exist as the unique open repo/head/base
candidate and match that exact number/URL; missing, closed, or replacement PRs
fail closed. Readiness, body, ledger, and verifier remain unopened after the
official move, while remote title/body and three-way HEAD checks still come
from the immutable plan and remote facts.

Archive content identity is not inferred from the no-renames path set. Before
the exact archive commit exists, each `tracked_move_paths` item binds the
evidence commit active blob to the archived working-tree file and prospective
archive commit blob. All files are byte-identical except `task.json`, where
only the official `status` and `completedAt` archive fields may change.
`untracked_archive_outputs` are validated by their existing template/digest
contracts. Once the exact archive commit exists, its tree and blobs replace the
archived working tree as the authoritative content source.

Failure-state evidence is read from the real filesystem, Git index/log, bare
remote, and fake GitHub PR store after invoking production `cmd_finish_work()`.
Test-owned dictionaries may summarize those observed facts, but must not drive
or manufacture transition state.

### Archived Task Backfill Contract

The #100 backfill reads only these task-local source names: `task.json`,
`issue-scope-ledger.json`, `prd.md`, `design.md`, `implement.md`, `review.md`,
`review-gate.json`, `phase2-check.json`, `pr-body.md`, and
`pr-readiness.json`. A source is recorded in `backfill.source_artifacts` only
after a successful UTF-8/JSON read. Missing files are not read errors; malformed
or unreadable files are isolated to that task and excluded from extraction.
Task, Git, GitHub, artifact, problem/outcome/behavior, contract-table, and
search-term fields follow the fixed priority rules documented by the public
backfill command. The generator never infers facts from GitHub or conversation
history and never invents an issue, PR, commit, branch, path, or behavior.
Git commits use the first non-empty valid source in order: `task.json.commit`,
`review-gate.json.head`, then `pr-readiness.json.commits[]`; values from lower
priority sources are not unioned into a selected higher-priority source.
Problem fallback is exactly `<task.title>；旧行为：历史 artifact 未记录。` and
outcome fallback is exactly `<task.title>；非目标：历史 artifact 未记录。`.
When higher-priority outcome sources and a pr-body summary paragraph are absent,
the first `pr-body.md` `## 变更摘要` list item becomes outcome while the
complete normalized list remains `changed_behavior`.
Search-term phrases first use, in order, task title, task slug, problem prefix,
outcome prefix, and changed-behavior prefixes. Only when fewer than three
unique phrases remain may task slug, task title, and `历史归档 task` be used to
fill the array. After that fixed sequence, and only when no phrase contains a
#97 `FINISH_SUMMARY_COMPLETION_MARKERS` value, the generator appends the single
fixed phrase `历史归档 task 已完成`; it never replaces or rewrites an existing
phrase. During the fixed sequence, only an exact problem or outcome fallback
candidate may be skipped when its first clause equals the last clause of the
previously retained phrase. This narrow edge de-duplication prevents the same
fallback boundary from being repeated inside retrieval phrases; it does not
rewrite candidates or apply clause-level de-duplication to any other phrase.

Backfill reuses the normal `finish_summary_errors(..., task_dir=...)` validator
and `finish_summary_retrieval_text()` derivation. It adds exactly the schema
defined `backfill` object with `generated=true`, a UTC generation time,
successful source artifacts, sorted canonical `missing_fields`, and one of
`complete`, `partial`, or `minimal`. The normal #97 schema remains unchanged;
legacy top-level `summary` and `keywords` are forbidden by its closed field set.
The final validator permits one backfill-only retrieval boundary duplication
only when `generator` is exactly `guru-team.finish-summary-backfill`, problem is
exactly `<task.title>；旧行为：历史 artifact 未记录。`, retrieval starts with the
exact task title followed by that problem, and the retrieval remainder contains
no unapproved adjacent duplicate clause. A second backfill-only boundary is
allowed only when task-local sources prove the higher-priority outcome sources
and pr-body paragraph are absent, outcome equals the first pr-body summary list
item, the complete list equals `changed_behavior`, retrieval exactly matches the
shared helper, and removing one copy leaves no unapproved adjacent duplicate.
The two approved boundaries may coexist. Normal finish-work, non-exact source
text, source drift, and every other duplicate inside problem, outcome, behavior,
surface, contract, or phrase content remain rejected by the shared #97 rules.

Backfill confidence is `complete` only when the required structural artifacts,
`git.branch`, complete changed paths, source issues, PR URL, and core index
fields are present. It is `minimal` only when retrieval fields depend solely on
the archive basename, task title/name, or Markdown H1. Any other generated
semantic or provenance evidence, including artifact/base/branch/commit facts,
issue or PR facts, review outcome, completed checklist, or contract table, makes
the result at least `partial`.

`git.changed_paths` and `index.search_terms.paths` retain the complete clean,
sorted, exact-deduplicated path set. Affected surfaces group paths by the fixed
path-prefix `kind` mapping. Each kind is split into stable chunks of at most 100
paths, and every path remains present in exactly one chunk. If the complete
representation would exceed the schema maximum of 20 surfaces, generation
fails closed for that task instead of truncating paths or expanding the schema.
An empty changed-path set receives the schema-valid `task-artifact` fallback
surface with no paths.

## Workspace Boundary Snapshot

`check-workspace-boundary --json` resolves the task from `--task` or current task, validates the task-local context, then derives the expected workspace from current repo root, local runtime mapping, and Git worktree facts. It never trusts a committed absolute workspace path. The snapshot records `status`, `workspace_mode`, `expected_workspace`, `actual_repo_root`, optional `source_checkout`, `task_dir`, repo-relative `task_dir_relative`, source/task git status, suspicious same-task artifacts, and deterministic errors. Missing task context, a mismatched runtime workspace, a task outside the current repo `.trellis/tasks`, or source-checkout same-task metadata fails closed.

## Planning Approval Artifact

`planning-approval.json` is the start gate evidence for Phase 1.4. New
artifacts use `schema_version=1.2` and are valid only after the main session
has completed planning artifact ambiguity review, displayed task-local links to
all three planning documents, and the user has explicitly confirmed after
seeing them. Phase 0 handoff approval, generic workflow confirmation, old
`schema_version=1.0` / `schema_version=1.1`, missing `ambiguity_review`,
non-passed ambiguity review, or `user_confirmation.source=workflow` must fail
closed.

It records:

- task directory and current `HEAD`
- reviewer / AI process identity metadata
- `review_prompt_presented_at` and `approved_at`
- Chinese approval summary and user confirmation evidence with
  `user_confirmation.source=explicit-post-planning-review`
- `ambiguity_review` object with `status=passed`, non-empty `reviewer`,
  non-empty `summary`, `normative_language.controlled_terms`,
  `normative_language.scan_scope`, `normative_language.hits`,
  `normative_language.unchecked_normative_hits`, and all required
  `checked_dimensions` set to true
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

`ambiguity_review.normative_language.controlled_terms` must equal the full
controlled weak-constraint v2 term list: `可以`, `允许`, `建议`, `推荐`,
`可选`, `尽量`, `尽可能`, `最好`, `应该`, `应当`, `原则上`, `一般`,
`通常`, `视情况`, `根据情况`, `根据需要`, `按需`, `必要时`, `如有需要`,
`需要时`, `适当`, `适当时`, `合理`, `合理时`, `类似`, `相关`, `相应`,
`等`, `等等`, `之类`, `一些`, `若干`, `部分`, `至少`, and `默认`.
`scan_scope` must equal `["prd.md", "design.md", "implement.md"]`.
`hits[]` must contain every controlled-term hit found in those three planning
documents with `path`, `line`, `term`, `text`, `classification`, and `reason`.
`unchecked_normative_hits[]` must contain only unclassified hits and
`classification=contract_violation` hits; it must be empty for passed approval.
Allowed non-blocking classifications are `quoted_source_non_contract`,
`term_definition`, `literal_identifier`, `historical_record_non_contract`,
`deterministic_threshold`, `deterministic_default`, `deterministic_option`, and
`deterministic_reference`, each with a non-empty reason. `checked_dimensions`
must contain `no_requirement_weakening`,
`source_issue_semantics_preserved`, `conditional_paths_have_conditions`,
`no_parallel_implementation_paths`,
`gates_have_machine_verifiable_conditions`,
`acceptance_criteria_are_deterministic`, and
`external_quotes_are_labeled_non_contract`, all set to true.

The companion validator must rescan the same three planning documents and fail
closed if the current scan no longer matches recorded `hits[]`, if
`scan_scope` or `controlled_terms` drift, if a hit uses an unknown
classification, if an allowed classification lacks a reason, or if
`unchecked_normative_hits[]` is non-empty. The scanner is deterministic fact
collection and classification structure validation only; AI semantic review
remains in Markdown workflow / planning artifacts.

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
`pr-readiness.json`, `marketplace-verification.json`, `agent-assignment.json`, `review.md`, and
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
- `liveness[agent_id]` entries with `progress_anchor_at`,
  `pending_status_request_at`, `last_checked_at`, `last_decision`, and
  `last_scan_snapshot`
- `status_events[]` entries for assignment, public progress, status request,
  stale assessment, same-agent resume, replacement start, unfinished
  termination, completion, and explicit failure handling

Allowed logical roles are:

- `实现代理`
- `阶段二检查代理`
- `问题发现审查代理`
- `问题闭环审查代理`
- `最终放行审查代理`

The companion recorder/validator may check JSON structure, required fields,
role enum values, HEAD resolvability, current-HEAD freshness when requested,
file digest metadata, liveness snapshot fields, status event enum values,
required evidence fields, and objective recovery-chain completeness for Phase 2
check / Branch Review Gate pass. It must not decide which sub-agent should be
used, whether implementation is sufficient, whether reviewer reuse is
semantically acceptable, or whether a final release review is sufficient.

`agent-assignment.json` schema version `1.1` is additive over the prior review
round ledger. It keeps `agents[]`, `review_rounds[]`, and
`reuse_decisions[]`, adds `liveness[agent_id]`, and replaces active coarse
status events with the #76 liveness contract. Older artifacts that omit
`liveness` or `status_events[]` are normalized for reading, but old
`wait-timeout`, `continue-waiting`, coarse `progress-observed`, and
unstructured stale/replacement records are not active progress, stale, or pass
evidence.

`liveness[agent_id].last_scan_snapshot` records:

- task worktree `HEAD`, content status digest, content diff stat digest, and
  content max mtime, excluding `agent-assignment.json` bookkeeping writes;
- source checkout `HEAD`, status digest, diff stat digest, and max mtime;
- `progress_events_count`, `progress_events_digest`, and
  `progress_events_newest_event_id`, counting only progress events.

Allowed progress events are:

- `explicit-message-observed`
- `tool-activity-observed`
- `command-output-observed`
- `platform-progress-observed`
- `status-response-observed`

Allowed control / terminal / audit events are:

- `assigned`
- `status-requested`
- `status-request-failed`
- `stale-assessed`
- `resume-same-agent`
- `replacement-started`
- `terminated-unfinished`
- `completed`
- `failed`
- `workspace-boundary-violation`

Every status event records `event_id`, `event`, `agent_id`, `logical_role`,
`platform_nickname`, `observed_at` as UTC ISO-8601, `recorded_at`, `head`,
`source`, and non-placeholder `evidence`. `replacement-started` additionally
requires `predecessor_agent_id`, `predecessor_event_id`,
`replacement_reason`, and `handoff_summary`. `resume-same-agent` requires
`predecessor_event_id` and `handoff_summary`. `terminated-unfinished` requires
`termination_reason` and `handoff_summary`; `termination_reason=stale_cutover`
requires `termination_source_event_id` pointing to the same agent's
`stale-assessed`, while
`termination_reason=manual_or_platform_terminated_unfinished` requires an
empty `termination_source_event_id`.

The liveness checker is a short-lived, on-demand, single-sample command:

```bash
.trellis/guru-team/scripts/bash/check-subagent-liveness.sh --json \
  --task ".trellis/tasks/<task>" \
  --agent-id "<technical-agent-id>" \
  --source-repo "<source-checkout-path>" \
  --progress-scan-interval 120 \
  --max-progress-silence 180
```

It returns exactly one decision:
`workspace_boundary_violation_progress`, `progress_observed`,
`status_request_required`, `continue_waiting_no_repeat_ping`,
`stale_allowed`, or `blocked_missing_evidence`. `progress_scan_interval=120s`
controls scan cadence. `max_progress_silence=180s` is measured from
`progress_anchor_at`; `status-requested` does not refresh that anchor and does
not extend `max_progress_silence_deadline_at`. If the deadline has already
passed but there is no pending status request, checker must still return
`status_request_required`; only after a successful `status-requested` and an
immediate recheck can `stale_allowed` be returned when no progress appeared.

Source checkout snapshot changes are
`workspace_boundary_violation_progress`, not stale evidence. Task worktree
snapshot changes and recorded progress events are `progress_observed`. Only new
changes relative to `last_scan_snapshot` refresh `progress_anchor_at`. Existing
dirty diffs, old progress events, control/bookkeeping events, and
`agent-assignment.json` writes do not refresh liveness.

`record-subagent-liveness-event.sh` is the active status/liveness writer.
`record-agent-assignment.sh` remains for review rounds and reuse decisions, and
its old `--status-event` path must fail closed. `status-requested` and
`status-request-failed` may be recorded only after checker decision
`status_request_required`. `stale-assessed` may be recorded only after checker
decision `stale_allowed`, and recorder must verify current task/source
snapshot plus progress event digest still match `last_scan_snapshot`; otherwise
it fails closed and requires a recheck.

After `stale-assessed`, the workflow must not resume or continue waiting for
that predecessor. The same liveness handling turn must record
`terminated-unfinished termination_reason=stale_cutover
termination_source_event_id=<stale-assessed.event_id>`, then replacement
`assigned`, then `replacement-started` with
`replacement_reason=max_progress_silence_exceeded`. Manual/platform unfinished
termination is structurally separate through
`termination_reason=manual_or_platform_terminated_unfinished`.

`wait_agent`, `trellis channel wait`, or equivalent wait command timeout means
only that the current wait window ended without final completion. It is not a
failure signal and must not be used as pass evidence. `completed` means the
agent execution chain ended, not that Phase 2 or Branch Review passed. `failed`,
unfinished, stale, or replacement partial output must not support a passing
Phase 2 check or Branch Review Gate until a same-agent resume or replacement
chain later reaches `completed`. A replacement `failed` requires further
resume/replacement and cannot close the chain.

For Branch Review Gate, any review agent that recorded findings may be reused
only as `问题闭环审查代理` for fix confirmation. This includes a previous
`最终放行审查代理` round that found a new issue. A finding owner may be closed
by a later same-agent closure round with `findings_count: 0` and
`reuse_decision: reuse-for-closure`; or by a different fresh
`问题闭环审查代理` whose technical `agent_id` has not appeared in any earlier
`review_rounds[]` and whose `reuse_decisions[]` entry records
`decision=new-agent` with exact `from_round`, `to_round`, closure `agent_id`,
reviewed `head`, and non-empty `reason`. If the finding owner objectively
failed, was interrupted, or became stale and cannot continue, the workflow may
record a replacement closure chain: predecessor liveness evidence in `status_events[]`,
`replacement-started` with `predecessor_agent_id`, `predecessor_event_id`,
`replacement_reason`, and `handoff_summary`, `reuse_decisions[]`
`decision=replace` with `from_round` / `to_round`, then a replacement
`问题闭环审查代理` round with `findings_count: 0` and
`reuse_decision: replace`. Every finding owner must have one of those three
closure forms before a passing gate can be recorded. A closure round that still
reports findings becomes a new finding owner and must itself have a later
explicit closure; a closure that reports zero findings confirms its targeted
finding is closed and does not need to be repeated for every later HEAD. The final
passing review round must be the last `最终放行审查代理`, use a fresh technical
`agent_id` that has not appeared in any earlier `review_rounds[]`, set `findings_count` to 0, set
`reuse_decision` to `new-agent`, record the reviewed code `HEAD` in
`reviewed_head`, and have a unique, strictly increasing `round` value so no
later record can make the final round ambiguous.

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

## Commit Message Payloads

`check-commit-messages --json` validates objective commit subject/body shape
for the checked range. It must not decide whether implementation, Phase 2 check,
Branch Review, or PR readiness is sufficient. The payload is additive and uses:

```json
{
  "status": "ok",
  "base_ref": "origin/main",
  "head": "<sha>",
  "range": "origin/main..HEAD",
  "primary_issue": 92,
  "checked_commits": [],
  "errors": []
}
```

When blocked, the command exits non-zero and returns `status=blocked` with
`errors[]` entries that include the commit hash, subject, classified kind
(`work`, `metadata`, `merge`, or `invalid`), and objective validation messages.

`format-merge-commit --json` and `publish-pr` expose a `merge_commit` object:

```json
{
  "ready": true,
  "subject": "chore(merge): #91 合并 #92 中文 Conventional Commits 提交规范",
  "body": "合并：\n...",
  "body_file_hint": "<merge-body-file>",
  "command": ["gh", "pr", "merge", "91", "--merge", "--subject", "...", "--body-file", "<merge-body-file>"],
  "errors": []
}
```

Dry-run publish may set `ready=false` and use `<pull_request>` as a placeholder.
Formal publish must parse the created PR number and return `ready=true`.
Trellis metadata commit messages generated by finish/publish use
`chore(trellis): #<primary_issue> 固化任务收尾元数据` and an empty body.
Commit message payloads must never use close keywords such as `Closes`,
`Fixes`, `Resolves`, `Close`, `Fix`, or `Resolve`; those keywords remain PR
body-only close semantics controlled by Issue Scope Ledger.

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

Before `task.py archive`, `prepare_closeout()` fixes both the active and future
archive locators. The active task remains the task-local boundary until the
single archive metadata transaction moves it to the prevalidated archive
locator. Validators may accept gate digest entries that still use the active
locator when the projected archived files have matching bytes; no artifact is
rewritten after the archive move.

The future locator must not already exist when prepare builds the plan. The
archive root, month, and final destination are lexical components: every
existing component is inspected with `lstat`, any symlink including dangling or
repo-internal targets is rejected without following it, and the same check is
repeated immediately before official move.
`task.json.children` uses the official missing-as-empty convention but must
otherwise be `list[str]`; active children found by official exact/suffix lookup
block only when their `task.json` would join the archive mutation, while archived
children remain valid historical references.

## Closeout Plan

`closeout-plan.json` is schema version `1.0` and is the immutable machine input
contract shared by dry-run and formal finish. It records portable task and
repo/base/head identity, protected input SHA-256 values, Branch Review Gate
coverage, exact draft PR inputs, marketplace pending machine evidence, future
archive projection, exact metadata allowlist, and the fixed transition list.
It never records tokens, absolute worktree paths, a real PR URL, verifier
output, or archive commit SHA. Its projection does record a fixed sentinel PR
URL/ref and the complete schema-valid finish-summary template so all local
summary errors are known during prepare.

`git.repo` is the normalized `owner/repository` identity. All effective fetch
and push URLs of `git.remote` have a raw/effective two-layer contract. Raw
`remote.<name>.url`, optional `pushurl`, and every `url.*.insteadOf` /
`pushInsteadOf` base/pattern are read with NUL value boundaries plus origin.
They reject empty/ambiguous records, leading/trailing whitespace, all control
characters, unreadable origins, and NUL bytes in relevant config files;
missing `pushurl` reuses the raw `url` set. Effective output is never trimmed,
must preserve raw-source cardinality, and after Git rewrite must use
credential-free `https://github.com/...`,
`ssh://git@github.com/...`, or `git@github.com:...` transport and normalize to
this value. HTTP, `git://`, `file://`, relative/absolute filesystem paths,
scheme-less host/path forms, userinfo/password/token variants, explicit ports,
query strings, fragments, and extra path segments are invalid. The repo
identifier normalizer is not a remote URL parser and must never be used as a
fallback for effective remote values. Every queried PR must include
`headRepository.nameWithOwner`,
`headRepositoryOwner.login`, and `isCrossRepository`; the first two must agree
with each other and with `git.repo`, while `isCrossRepository` must be false.
Missing/unknown fields or a same-name fork candidate fail closed before PR
cardinality, final-summary binding, archive, recovery, or ready transition.

`publish.body_sha256` hashes the task-local `pr-body.md` bytes. Those bytes must
decode as non-empty UTF-8, and the decoded text is the one canonical body value
used by active readiness recovery, `gh pr create`, unique draft reuse, and final
projection. Leading/trailing whitespace, trailing newlines, and
Markdown-sensitive spaces are identity data; validators never trim or add a
newline before comparing the remote PR body. After archive, the remote body's
UTF-8 bytes are hashed directly and compared with `publish.body_sha256`; the
task-local body is not reopened.

`projection.move_paths` is the complete task-relative filesystem set moved by
the official archive command. `projection.tracked_move_paths` is the subset in
the Git index after the evidence commit; each requires an active deletion and
archive addition. `projection.untracked_archive_outputs` is the subset created
after that commit; currently it is exactly `finish-summary.json`, and Git must
report only its archive addition. `projection.evidence_paths` is the complete
active task path set owned by the pre-draft metadata commit. These tracking
classes are immutable plan facts derived before archive, not inferred from
post-move status. The evidence commit tree must contain exactly the active
locator projection of `tracked_move_paths`; this Git-tree check proves the
classification before final projection writes any untracked output. The
projection also stores `summary_template`,
`summary_template_sha256`, the sentinel PR identity, and the exact runtime
fields that may change. The sentinel uses the
maximum-width positive 64-bit number so replacing it with a real PR number
cannot introduce a new string-length validation failure.

`summary_template_sha256` hashes the exact UTF-8 `write_json` encoding: two-space
indentation, `ensure_ascii=false`, and one trailing newline. Active final
projection requires that exact byte encoding, then normalizes the two PR
runtime fields back to the sentinel and compares the template digest before
the official move. Archived recovery proves continuity through the exact
path/commit/blob transaction and never reparses the summary.

`plan_digest` is the SHA-256 of canonical JSON with `plan_digest` omitted.
Dry-run returns the complete plan and digest. First formal execution accepts
only the same digest through `--expected-plan-digest`; a mismatch or protected
input drift fails before push or file writes. `pr-readiness.json` binds the same
digest under `publish_inputs.closeout_plan_digest`. After the first metadata
commit, retries load the committed plan and validate reachable successor facts;
passed ledger evidence is never used to reconstruct the initial plan.
Before draft binding, partial retries distinguish reviewed content pushed,
verifier pending/failed, verifier passed but evidence uncommitted, and evidence
committed but unpushed from the exact plan/readiness/evidence/Git/remote facts.
They retry only the missing transition.

`task.archive_locator` uses the same live `YYYY-MM` that the unmodified official
archive command will use. Formal checks it before the first side effect and
again immediately before official move. If a committed plan becomes stale while
the task is still active, dry-run may produce a replacement plan only when the
old plan is the exact current evidence commit and neither old nor new archive
locator exists. The replacement carries `git.evidence_parent_head`, changes
only archive-derived projection values plus `projection.evidence_paths`, and a
formal run with the new digest appends an exact plan/readiness evidence commit.
The predecessor plan and evidence lineage remain in Git and are recursively
validated. This is plan supersession, not archive-directory migration or
history rewrite.

`inputs.official_after_archive_hooks.sha256` binds the canonical empty command
state parsed by the official Trellis config parser. Missing or empty
`hooks.after_archive` maps to `{"commands":[]}`. Non-empty, ambiguous,
unreadable, invalid-byte, or symlinked config has no valid digest because
prepare rejects it without executing any hook command.

Marketplace machine evidence has one deterministic pending identity and one
deterministic passed identity. Pending and passed use the same fixed machine
fields; pending uses empty artifact/remote digests and `commands_passed=false`.
Human scope reasons remain outside this object and do not affect its identity.
`artifact_path` is exactly task-relative `marketplace-verification.json`, so
the same locator resolves after the active directory moves to archive.
Missing, duplicate, altered, path-bound, or digest-mismatched machine fields
fail closed.

Before the exact archive commit exists, archive recovery accepts only the
complete mixed no-renames working-tree path set: both sides for every tracked
move and archive-only for every untracked output. It validates exact
dirty/staged paths, evidence-commit parent/path identity, active absence,
archive completeness, tracked blob continuity, and the official `task.json`
delta before it may create the commit. Missing or mismatched commit state keeps
this metadata recovery path fail closed.

Before official move, the same continuity contract applies to the active task:
the index is empty, untracked paths equal the planned final outputs, every move
path is a regular file, tracked Git modes are `100644` or `100755` and match the
working mode, and every working byte equals its evidence blob. This gate also
rechecks the live archive month and empty official hook state.

When current `HEAD` is the exact planned archive commit, both normal archived
tasks with context and plan-only damaged tasks load the plan from that commit
blob and validate only the immutable plan and Git parent/path/tree/blob lineage.
Archived working-tree deletion, content tampering, and the resulting dirty
paths are ignored; recovery may only push that exact commit when needed, check
remote PR identity and three-way HEAD alignment, and retry draft-to-ready. An
archived directory containing only `closeout-plan.json` is resolvable for this
path only by `trellis-finish-work`; other commands still require `task.json`.
Neither path parses, rebuilds, validates, or rewrites an archived body, summary,
ledger, readiness, or marketplace artifact.

Plan-only recovery does not use an empty task context as authorization. It
loads `closeout-plan.json` from the current commit blob and, before GitHub or
fast-path side effects, validates canonical digest plus Git toplevel,
configured/effective repository, current head branch, base ref availability,
current HEAD transaction, active/archive locator and basename relationship,
summary task/branch/base/source-issue identity, and the exact task directory.
Working-tree plan bytes cannot replace the committed plan. Ordinary task
discovery and workspace-boundary commands do not enable this mode and still
require the normal `task.json` / `task-start-context.json` contracts.
The raw finish-work locator is preserved before ordinary resolution. Only a
basename, exact former active locator, or exact archive locator may select the
plan-only search. Path-like input is checked component-by-component with
`lstat` from repo root through the final task directory. Basename input checks
the raw `<repo>/<basename>` and `.trellis/tasks/<basename>` candidates, then
checks archive candidates in ordinary resolver order before resolution. Every
direct or archive candidate first retains only `symlink_component` evidence,
then uses the ordinary resolver's exact follow-symlink `directory + task.json`
predicate. A matching alias is rejected; an unmatched alias continues to the
next candidate. This rejects internal/external, relative/absolute,
ancestor/final, multilevel, dangling, or loop aliases before raw evidence can
be discarded. The ordinary resolver then runs and preserves explicit
`task.json`, active task, and normal archived `task.json` precedence. Only an
ordinary not-found result enables plan-only fallback. An exact archive locator
selects only that candidate; basename or
former-active fallback requires a unique matching archive month and fails
closed when multiple months match. The verified plan-only target must resolve
to the same canonical archive locator recorded by `task` and `projection`.
Only the structurally verified Darwin `/var` -> `/private/var` system mapping
may re-anchor an outer path; arbitrary `samefile` discovery and user aliases
are not valid identity.

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
python3 -m json.tool trellis/workflows/guru-team/schemas/task-start-context.schema.json
```

## Common Mistakes

- Adding a config key to `config-template.yml` without adding a default in
  `DEFAULTS`.
- Adding a new task-start-context field required by code but absent from the strict JSON schema.
- Letting PR generation close `related_issues` or `followup_issues`.
- Recording review-gate evidence that does not mention deployment impact.
