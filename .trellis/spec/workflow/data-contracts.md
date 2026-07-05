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

Repository release tags for the Guru Team extension use repo-level SemVer tags
such as `v0.6.5`, not namespaced tags such as `guru-team/v0.6.5`. The tag's
`X.Y.Z` must match `trellis/guru-team-extension.json.version`. Stable workflow
marketplace examples should use
`gh:castbox/guru-trellis/trellis#vX.Y.Z`; unpinned
`gh:castbox/guru-trellis/trellis` means latest/canary and must be reported as a
mutable source in install or upgrade evidence.

Release order matters: merge the manifest/docs PR first, create the annotated
`vX.Y.Z` tag on the merge commit, verify tag-pinned `trellis init` and
`trellis workflow` marketplace commands, then retire any old competing tag
names only after the new tag is verified.

## Handoff

`.trellis/guru-team/handoff.json` records intake provenance and preflight:

- source issue
- slug, task slug, task title
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

Executor prepare paths (`--create-worktree` / `--create-task`) must refresh the
selected base branch before creating the task worktree. Record remote, local
head before/after, remote head, fetch state, fast-forward state, and the ref used
for worktree creation in `preflight.base_freshness`. Fail closed on divergence
or unknown freshness instead of creating a branch from a stale base.

Executor prepare paths must also ensure the selected workspace has
`.trellis/.developer` before handoff/task creation continues. Prefer copying the
source checkout identity into the target worktree. If the source identity is
missing but an explicit developer/assignee name is available, initialize an
equivalent target identity. If neither source identity nor explicit developer is
available, fail closed with a recovery command instead of allowing journal or
`task.py list --mine` to fail later. Record the objective result in
`preflight.developer_identity`.

## Planning Approval Artifact

`planning-approval.json` is the start gate evidence for Phase 1.4. It records:

- task directory and current `HEAD`
- reviewer / AI process identity metadata
- Chinese approval summary and user confirmation evidence
- approved planning artifact digests for `prd.md`, `design.md`, and
  `implement.md` when present
- dirty paths at approval time

The artifact is valid only while the recorded artifact hashes and `HEAD` match.
`task.py start` is a status transition only and must not be treated as planning
review evidence.

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

## Agent Assignment Artifact

`agent-assignment.json` is optional for older tasks and expected for new
sub-agent-dispatch Guru Team tasks. It records the AI/human assignment decisions
that already happened in the workflow:

- `schema_version`, current task path, and current `HEAD`
- `agents[]` entries for implementation/check/review assignment events
- `logical_role` as the Chinese Trellis process identity
- `agent_id` as the technical platform identity used for continuing/reusing an
  agent
- `platform_nickname` as display-only UI metadata that never participates in
  gate decisions; prefer configured Chinese UI nicknames when the platform
  exposes them, otherwise record the raw automatic/random nickname
- `review_rounds[]` entries with review round number, reviewed HEAD,
  findings count, reuse policy, and reuse decision
- `reuse_decisions[]` entries for explicit reuse/replacement decisions across
  rounds

Allowed logical roles are:

- `实现代理`
- `阶段二检查代理`
- `问题发现审查代理`
- `问题闭环审查代理`
- `最终放行审查代理`

The companion recorder/validator may check JSON structure, required fields,
role enum values, HEAD resolvability, current-HEAD freshness when requested,
and file digest metadata. It must not decide which sub-agent should be used,
whether reviewer reuse is semantically acceptable, or whether a final release
review is sufficient.

Because `最终放行审查代理` is assigned after the task work commit,
`agent-assignment.json` is the only Phase 2 checked artifact that may receive a
post-commit metadata update before Branch Review Gate. `review-branch.sh` must
then receive `--agent-assignment` so the gate records the current digest,
roles, assignment count, review round count, and reuse decision count. This
does not permit post-commit changes to non-metadata paths or to other checked
artifacts.

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
  passed gates
- required review report digest: `review_report.path`, `sha256`,
  `size_bytes`, and `modified_at`
- findings
- Issue Scope Ledger coverage
- validation evidence
- optional `agent_assignment` digest summary when `review-branch.sh` receives a
  task-local `agent-assignment.json`

The gate is valid only for the reviewed `HEAD`, except that `finish-work` may
allow metadata-only commits after the gate. A passed gate is invalid if it lacks
review report metadata, `review_source: independent-agent`, or a task-local
file named `review.md`. `--reviewer` alone is only identity metadata and cannot
prove the review report evidence; main-session/self-review identities are
rejected for passed gates. Enforcement lives in `validate_review_gate()` and
`metadata_only_since()`.

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
