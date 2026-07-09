# Companion Scripts

## Script Boundaries

Bash files under `trellis/workflows/guru-team/scripts/bash/` are thin wrappers.
They should use `set -euo pipefail`, resolve their own `SCRIPT_DIR`, and delegate
behavior to the Python companion:

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/../python/guru_team_trellis.py" <subcommand> "$@"
```

Keep argument parsing and workflow logic in
`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` unless there
is a shell-specific reason to handle it in Bash. Existing examples:

- `trellis/workflows/guru-team/scripts/bash/prepare-task.sh`
- `trellis/workflows/guru-team/scripts/bash/resolve-human-artifacts.sh`
- `trellis/workflows/guru-team/scripts/bash/review-branch.sh`
- `trellis/presets/guru-team/scripts/bash/apply.sh`

## Python Runtime Constraints

The companion script is installed into target repositories. Keep it portable:

- Use the Python standard library only.
- Shell out to `git` and `gh` through helper functions such as `run()` and
  `run_stdout()`.
- Use `pathlib.Path` for filesystem paths.
- Use `json.dumps(..., ensure_ascii=False, indent=2)` for user-visible JSON
  payloads and artifacts.
- Keep typed helpers and constants near the top of the file when they define
  reusable contracts.

Reference files:

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`

## Error Handling

Use `WorkflowError` for expected workflow failures in
`guru_team_trellis.py`. Include `exit_code=2` for user-actionable blocked states
such as duplicate issue confirmation, missing review-gate evidence, dirty
non-metadata paths, or incomplete Issue Scope Ledger.

The `main()` function prints a JSON error payload to stderr when `--json` is
used. Do not scatter `sys.exit()` calls through helper functions in the workflow
companion.

The preset installer currently uses `SystemExit` for missing `.trellis/` or
missing source directory because it is a small installer script. If adding more
complex failure modes there, preserve JSON output for normal success and avoid
printing secrets or local-only data.

## GitHub and Git Operations

Always gate GitHub operations with `gh auth status` through `require_gh_auth()`.
Do not assume the GitHub CLI is configured just because `gh` exists.

Default `prepare` must be side-effect-free for GitHub and filesystem writes
until the corresponding explicit confirmed/executor flag is present. It may call
`gh issue view/list` for explicit issues and duplicate search, but planner
output must stay on stdout and must not write `.trellis/guru-team/handoff.json`.
It must not call `gh issue create`, `git worktree add`, or `task.py create`
unless the corresponding explicit confirmed/executor flag is present and the
workflow has already required AI/human handoff review. Confirming or creating a
source issue alone still must not write handoff; handoff is written only by
`--create-worktree` or `--create-task` in the chosen workspace.

Before publish, reject uncommitted non-metadata changes. Metadata-only paths are
defined by `METADATA_ONLY_PREFIXES` and `METADATA_ONLY_FILES`; update these
constants deliberately if Trellis metadata ownership changes.

`finish-work.sh` and `publish-pr` are internal helpers, not the normal user
path. `finish-work.sh` must reject ordinary direct calls before archive, journal,
metadata commit, push, or PR side effects; only the explicit
`trellis-finish-work` entrypoint may pass the `--from-trellis-finish-work`
intent marker. `publish-pr` must reject ordinary direct calls before `git push`
or `gh pr create`; only `finish-work` may set the internal publish marker after
archive and journal succeed. A separate explicit recovery/debug flag may exist
for rerunning publish after finish-work already completed, but it still must
pass review gate, dirty state, issue ledger, base branch, and GitHub auth
checks.

Use the intake/task `base_branch` for diff ranges and PR base. Do not fall back
to the GitHub default branch when the task has an explicit base.

For PR body publishing, companion scripts may validate objective Markdown
structure, required sections, forbidden low-information phrases, non-empty
validation / impact / safety content, Docs SSOT section/key presence, and Issue
Scope Ledger close/ref semantics. They must not decide whether the release
explanation or Docs SSOT rationale is true or sufficient; that judgment belongs
to the AI readiness review before
`trellis-finish-work`. Non-draft publish must require `--body-file` or
`--body-artifact` inputs that were already reviewed by AI/human; `generated`
bodies are limited to draft/preview paths. `--body-artifact` must carry
`ready: true` and a non-empty `body` or `body_file`. Resolve relative
`body_file` values from the artifact directory, not the repository root.
When `finish-work` archives the active task before publish, rewrite active task
artifact paths to the archived task path and read the final PR body from that
archived artifact. If the archived `review-gate.json` still contains
pre-archive task-local paths for `review.md`, `agent-assignment.json`, or
`issue-scope-ledger.json`, the helper may deterministically rewrite those paths
to the archived task directory and recompute only the affected digest metadata
before publish. This is archive metadata migration, not review judgment.

Planning and Phase 2 helpers follow the same recorder / validator boundary:

- `record-planning-approval.sh` records prior AI/human planning review and the
  user's explicit post-planning confirmation after the main session displayed
  task-local links to `prd.md`, `design.md`, and `implement.md`; it must not
  decide whether planning is sufficient. New artifacts use
  `schema_version=1.1`, `review_prompt_presented_at`, `approved_at`,
  `reviewed_artifacts[]`, the `approved_artifacts` alias, and
  `user_confirmation.source=explicit-post-planning-review`.
- `check-planning-approval.sh` validates all three planning artifact entries,
  hash / size metadata, confirmation source, and required audit fields before
  `task.py start`, before implementation dispatch, and before
  `phase2-check.json` can be recorded. Recorded HEAD, modified-time, and
  `dirty_paths` remain audit context, but validator freshness is tied to
  `prd.md`, `design.md`, and `implement.md` content digests. A later
  implementation commit, metadata tail, or unrelated working-tree dirty path
  must not block planning approval while those three reviewed planning documents
  still match. Old `source=workflow`, Phase 0 handoff confirmation, missing
  docs, or changed planning document content fail closed.
- `record-phase2-check.sh` records prior full-scope `trellis-check` evidence;
  it must not replace check judgment with command exit codes.
- `check-phase2-check.sh` validates coverage, validation evidence, findings,
  hashes, and stale state before commit.
- `record-subagent-liveness-event.sh` records prior AI/human sub-agent
  assignment, public progress observation, status request outcome, stale
  assessment, resume/replacement, unfinished termination, completion, or failure
  decisions in task-local `agent-assignment.json`; it must not decide which
  sub-agent to use, whether implementation is sufficient, whether to send a
  status request, or whether to start a replacement. It must fail closed unless
  `status-requested` / `status-request-failed` follows checker decision
  `status_request_required`, and unless `stale-assessed` follows checker
  decision `stale_allowed` with unchanged snapshot/progress evidence.
- `check-subagent-liveness.sh` is an on-demand, single-sample, immediate-exit
  checker. It reads task/source git snapshots and recorded progress event
  digests, writes liveness bookkeeping, returns one decision JSON, and never
  watches, sleeps, reads platform UI, sends status requests, terminates agents,
  or judges implementation quality.
- `record-agent-assignment.sh` remains for non-liveness review round and reuse
  decision evidence. Its old `--status-event` path must fail closed and point
  callers to `record-subagent-liveness-event.sh`; it must not maintain a second
  active status event enum.
- `check-agent-assignment.sh` validates JSON structure, Chinese logical-role
  enum values, required fields, HEAD resolvability, optional current-HEAD
  freshness, liveness snapshot fields, status event enum/evidence fields,
  recovery-chain completeness, and digest metadata; it must not judge semantic
  reuse quality or review sufficiency.

Workspace boundary helpers are deterministic validators and fact snapshots:

- `check-workspace-boundary.sh --json --task <task-path>` reports
  `workspace_mode`, `expected_workspace`, `actual_repo_root`,
  `source_checkout`, `task_dir`, `task_dir_relative`, source checkout status,
  task worktree status, suspicious source artifacts, `status`, and `errors`.
- In `workspace_mode: worktree`, recorder/validator commands that write or
  validate task artifacts must confirm the actual repo root equals handoff
  `workspace_path` before touching `planning-approval.json`,
  `phase2-check.json`, `agent-assignment.json`, `review.md`, `reviews/*.md`,
  `review-gate.json`, or equivalent task-local artifacts.
- In `workspace_mode: worktree`, a missing current-checkout `handoff.json` is
  also a boundary failure for these recorder/validator commands, because the
  script cannot confirm the selected `workspace_path` and must not fall back to
  a same-named task directory in the source checkout.
- Task artifact arguments such as `--review-report`, `--agent-assignment`,
  `--review-round-report`, and `--checked-artifact` must resolve inside the
  current task directory under the selected task worktree. Absolute paths are
  allowed only when they stay under that task directory.
- Source checkout current-task artifacts, review metadata, or current-task dirty
  paths are fail-closed boundary facts. The script must not decide whether a
  sub-agent is stale, migrate a misplaced patch, or clean source checkout files;
  AI/human workflow owns those decisions.
- `--allow-source-clean` may be used only for a clean source checkout probe that
  reports facts without treating a clean source checkout mismatch as a blocker;
  it must not permit source checkout task artifacts or review metadata.

`resolve-human-artifacts.sh --json --task <task-path-or-name>` is a
deterministic resolver for user-facing Markdown task artifacts. It may resolve
the active task directory or archived task directory and report path/existence
facts for only `prd.md`, `design.md`, `implement.md`, `review.md`, and
`pr-body.md`. It must not read planning/check/review gate JSON artifacts, must
not decide phase sufficiency, and must not create links for missing files.

`review-branch.sh --pass` must fail before writing Branch Review Gate when
`phase2-check.json` is missing, stale, incomplete, or contains unresolved
P0/P1/P2 findings. It must also fail when the Phase 3 review result contains
any finding, including P3. A passed gate must include zero findings,
`--review-source independent-agent` and a reviewer identity that is not a
main-session/self-review identity, and `--review-report` must point to the
task-local file named `review.md`. The script validates those objective
metadata fields; it still does not judge review quality. It may also validate
objective review-report template traces: task-local `review.md` and every raw
`reviews/*.md` report recorded through `review_reports[]` must not contain known
English template headings such as `Review Rounds`, `Findings Lifecycle`,
`Evidence Handoff`, `Deployment / safety impact`, or `Follow-up Candidates`.
This is fixed-string/template-heading validation only and must not become a
Chinese semantic sufficiency reviewer.
Failed findings artifacts are also Branch Review Gate records. They must include
`--review-source independent-agent` and a task-local `--review-report review.md`
so the artifact records a prior independent review instead of only reviewer
identity metadata. They do not require the final-pass `agent-assignment`
closure checks unless the user is trying to pass the gate.
For post-commit Phase 2 audit, the script may accept a `phase2-check.json`
recorded at an ancestor HEAD only when every later non-metadata committed path
is covered by the artifact's `dirty_paths`, or when the later tail is Trellis
metadata only. The validator may ignore stale Phase 2 digest metadata for
task-local Branch Review Gate / publish readiness metadata during this
post-commit audit because final review and release readiness are produced after
the work commit. The allowed mutable task-local digest entries are
`issue-scope-ledger.json`, `pr-body.md`, `pr-readiness.json`,
`agent-assignment.json`, `review.md`, and `review-gate.json`; Branch Review
Gate or publish validators must revalidate the current files before passing.
Any uncovered non-metadata committed path or current non-metadata dirty path
must block the gate instead of encouraging a post-commit Phase 2 re-record.

`review-branch.sh --pass` must receive `--agent-assignment <task-local
agent-assignment.json>`. It validates that artifact and records its digest,
roles, assignment count, review round count, and reuse decision count under
`review-gate.json.verification_evidence.agent_assignment`. Missing assignment
evidence blocks a passed gate because the recorder cannot verify closure-before-
final or fresh final reviewer metadata.

When `agent-assignment.json.status_events[]` contains `failed`,
`stale-assessed`, or `terminated-unfinished`, `review-branch.sh --pass` must
fail closed unless the ledger has later objective evidence that the same
technical agent resumed or a replacement started, and that active recovery chain
later reached `completed`. A replacement `failed` requires further recovery and
cannot close the chain. This is only ledger-completeness validation. The script
must not decide whether a `wait_agent` timeout means stale, whether a running
agent should be stopped, or whether a failed/stale/unfinished partial output is
acceptable.

When a review round has findings, including a previous final-review round that
found a new issue, the same technical `agent_id` normally must later be
recorded only as `问题闭环审查代理` to confirm its finding is closed. If that
finding owner objectively failed, was interrupted, or became stale and cannot
continue, a replacement closure reviewer may close only that finding when
`reuse_decisions[]` records `decision=replace` with `from_round` / `to_round`
and `status_events[]` records the predecessor evidence plus
`replacement-started` with `predecessor_agent_id`, `predecessor_event_id`,
`replacement_reason`, `handoff_summary`, and replacement `completed` evidence.
A passing gate
must validate that every finding owner has a later same-agent closure round with
`findings_count: 0` and `reuse_decision: reuse-for-closure` or a complete
replacement closure chain with a replacement `问题闭环审查代理` round carrying
`findings_count: 0` and `reuse_decision: replace`, and then validate a fresh
`最终放行审查代理` review round: `review_rounds[].round` values are unique and
strictly increasing in recorded order, it is the unambiguous last round,
`reviewed_head` equals the reviewed code HEAD, `findings_count` is 0,
`reuse_decision` is `new-agent`, and the final reviewer did not own any earlier
finding round or act as replacement closure reviewer. This is an objective
metadata check only; the AI/human review still owns the judgment that the
review covered the full diff.

Independent review agents do not run Guru Team recorder/validator extension
scripts as part of their review. They may inspect docs, code, tests, diffs, and
ordinary validation evidence, but `review-branch.sh`, `check-review-gate.sh`,
`record-agent-assignment.sh`, and `record-*` calls belong to the main session
after the review result exists. Those calls record and validate objective
artifact evidence; they are not review work.

`review-branch.sh` may record non-blocking `observations[]` and
`followup_candidates[]` in `review-gate.json`. They are not findings and do not
block by themselves, but the AI/human reviewer must not downgrade an actual
current-scope defect into either category to make the gate pass.

For Docs SSOT, reviewer judgment stays outside the script: `review-branch.sh`
may record evidence/finding strings supplied by the reviewer, but it must not
decide whether `ssot_first`, `delta_first`, `bootstrap_or_repair_docs`, or
`no_docs_update_needed` was semantically sufficient. The companion boundary is
objective evidence shape and stale/non-metadata drift validation only.

## Security Rules

Never print or persist tokens, private keys, signed URLs, `.env` contents,
database URLs, or sensitive raw records in logs, JSON artifacts, issues, PR
bodies, or README examples.

When writing temporary PR or issue body files, use `tempfile.NamedTemporaryFile`
and unlink the file in a `finally` block. Existing examples:

- `create_issue()`
- `cmd_publish_pr()`

## Validation

For any script change, run:

```bash
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
```

When changing `review-branch`, `finish-work`, or `publish-pr`, also run dry-run
or representative script paths in a disposable worktree whenever practical.
