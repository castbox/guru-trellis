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
validation / impact / safety content, and Issue Scope Ledger close/ref
semantics. They must not decide whether the release explanation is true or
sufficient; that judgment belongs to the AI readiness review before
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

- `record-planning-approval.sh` records prior AI/human planning review and user
  confirmation; it must not decide whether planning is sufficient.
- `check-planning-approval.sh` validates artifact presence, hashes, and HEAD
  freshness before `task.py start`.
- `record-phase2-check.sh` records prior full-scope `trellis-check` evidence;
  it must not replace check judgment with command exit codes.
- `check-phase2-check.sh` validates coverage, validation evidence, findings,
  hashes, and stale state before commit.
- `record-agent-assignment.sh` records prior AI/human sub-agent assignment,
  review round, reuse, or replacement decisions in task-local
  `agent-assignment.json`; it must not decide which sub-agent to use.
- `check-agent-assignment.sh` validates JSON structure, Chinese logical-role
  enum values, required fields, HEAD resolvability, optional current-HEAD
  freshness, and digest metadata; it must not judge semantic reuse quality.

`review-branch.sh --pass` must fail before writing Branch Review Gate when
`phase2-check.json` is missing, stale, incomplete, or contains unresolved
P0/P1/P2 findings. It must also fail when the Phase 3 review result contains
any finding, including P3. A passed gate must include zero findings,
`--review-source independent-agent` and a reviewer identity that is not a
main-session/self-review identity, and `--review-report` must point to the
task-local file named `review.md`. The script validates those objective
metadata fields; it still does not judge review quality.
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

When a review round has findings, including a previous final-review round that
found a new issue, the same technical `agent_id` must later be recorded only as
`问题闭环审查代理` to confirm its finding is closed. A passing gate
must validate that every finding owner has such a later closure round with
`findings_count: 0` and `reuse_decision: reuse-for-closure`, and then validate a
fresh `最终放行审查代理` review round: `review_rounds[].round` values are unique
and strictly increasing in recorded order, it is the unambiguous last round,
`reviewed_head` equals the reviewed code HEAD, `findings_count` is 0,
`reuse_decision` is `new-agent`, and the final reviewer did not own any earlier
finding round. This is an objective metadata check only; the AI/human review
still owns the judgment that the review covered the full diff.

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
