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

## Shared Skill Runtime Dispatcher

`scripts/bash/run-skill-command.sh` is the only public dispatcher for active
Guru Team Skill package validators. The Bash file remains a thin wrapper around
the Python `run-skill-command` subcommand. Package wrappers pass only
`--package-root`, one fixed `--validator` id, and the original arguments after
`--`; they never select a runtime path or call a companion command directly.

Before the target companion command runs, the Python dispatcher must derive the
repository root from its audited installed location and component-wise `lstat`
the dispatcher, package root, package interface, installed extension manifest,
installed package inventory, and selected discovery copy. It must then validate
interface schema 1.2, its exact `semantic` or `deterministic` stage profile,
`runtime_dependency`, extension/runtime API identity,
dispatcher identity, distribution/portability, installed package drift, the
fixed validator id, and its declared `runtime_command`. The command must be a
published extension `companion_scripts` id and map to the managed executable
`.trellis/guru-team/scripts/bash/<runtime-command>.sh`.

Any missing manifest/dispatcher/package, incompatible API, dependency or
command mismatch, unmanaged discovery copy, sidecar, or drift exits 2 before
the companion command. The error must say that the Skill package is not
self-contained/portable, instruct the caller to install or upgrade the complete
Guru Team preset, resolve `.new` / `.bak`, rerun source and installed package
validation, and retry. There is no legacy-command fallback. Runtime compatibility
is an objective precondition only and never becomes an AI Review Gate pass.

### Change-Context Preview, Record, And Check

`preview-change-context-history`, `record-context-discovery`, and
`check-context-discovery` are the deterministic commands for
`guru-discover-change-context`. Their Bash wrappers remain thin and their
package wrappers reach them only through `run-skill-command`.

Preview accepts canonical clue arrays and a fixed limit no greater than 20. It
recursively opens only archived `finish-summary.json` files, projects only
`index`, applies `guru-context-history-score-1.0`, isolates malformed, missing,
shape-invalid, ordinary unreadable, and non-file records with stable portable
error rows, and emits query,
archive-manifest and preview digests. It performs no AI selection,
relevance/sufficiency judgment, duplicate decision, deep-read, mem lookup, or
write.

Record accepts an AI-authored reviewed payload from stdin or an explicit input
file. A `refresh_base` payload records current stable stale codes, superseded
query/snapshot digests, reason, and detection time. Recorder/checker compare
those caller-authored facts with current live freshness and require complete
skill re-entry. They consume only the current payload and expected snapshot
identity, without rebuilding an external history chain. Pre-task mode outputs
canonical snapshot bytes only. Task mode requires
the expected snapshot digest and writes only direct active task-local
`context-discovery.json` after objective live freshness checks; archived,
completed, and other non-active task locators are rejected. It then reopens the
written artifact once, compares exact bytes and snapshot identity, and repeats
the required live freshness checks before success. Check reads the same
canonical payload from stdin/file/task artifact. Before a
task-local write and after it, and for every task-local check, the exact target
must pass `git check-ignore --quiet --no-index -- <repo-relative-target>`.
Repository ignore rules, `.git/info/exclude`, and `core.excludesFile` therefore
fail closed even for an already tracked file. Stable errors are
`context_discovery_target_ignored` and
`context_discovery_target_trackability_unreadable`; pre-task stdout-only mode
does not run this target gate. It
verifies the published closed Draft
2020-12
schema/exit shape, digests, selected/excluded candidate cardinality, portable
source-specific deep-read locators, mem insufficiency gate, AI Review Gate evidence, fixed
human-confirmation status, the embedded complete validator-passed base-sync
result and all projection/provenance fields, selected-remote GitHub repository
identity, draft-to-created-issue live body binding,
selected-remote/base/live/reviewed-blob/query/archive freshness, and
same-snapshot identity. Neither command creates semantic conclusions or
rewrites an existing different artifact.
Record/check first execute only pure schema, digest, entry
clue, and semantic-evidence shape validation. `change_input` has ten closed clue
arrays and at least one must be non-empty; a separate issue binding or canonical
query cannot satisfy this entry precondition. The next stage is the base-only
live gate. Any base stale result validates the caller-authored refresh codes and
superseded identities/digests and returns before repository-bound query/current/
deep-read locators, GitHub issues, reviewed blobs, or archive/history are read.
Only a fresh base permits those remaining locator and live checks. Portable
locator validation is structural and source-specific; it does not scan every
payload string.
Source-issue freshness accepts the normalized live GitHub states `open` and
`closed`; duplicate candidates and a reviewed draft's created-issue binding
remain independently open-only. Every 40-character reviewed Git identity must
resolve from `HEAD:<path>` to an object whose live type is exactly `blob`.
Trees, gitlink commits, tags, missing objects, and mismatched blobs fail closed
for Docs, code/contracts, and tests evidence alike.
Task-artifact locators must remain inside the selected archive task, GitHub
locators must be canonical issue/PR URLs without query or fragment, and Git
locators must be exact live object/ref identities.

Duplicate candidate facts use one deterministic projection: normalized bound
`repo`, positive `number`, `identity=#<number>`, canonical issue `url`,
`state=open`, and `updated_at`. The pure gate recomputes `facts_sha256` from
only those fields and validates identity plus canonical URL from the same one
search result. Record/check do not issue a second duplicate search or re-read
candidates after AI review.

Pre-task and standalone checks bind the live checkout to the base-sync decision
branch. Direct active task mode instead requires the live branch to equal
`task.json.branch`, allowing task/worktree creation to place the unchanged
snapshot HEAD on a feature branch. This exception never weakens complete sync
result provenance, current HEAD, selected local/remote base refs, remote
repository identity, direct active task status/locator, or task-local dirty-path
validation. Zero candidates require empty selection/deep reads plus the exact
`not_needed` mem shape; a `used` or internally inconsistent `not_needed` shape
fails schema and runtime validation before any other history source is accepted.

Any base freshness error short-circuits before live issue/draft,
reviewed-blob, or archive-preview reads. Git status failure is a stable
fail-closed fact, never a clean checkout. `refresh_base` is accepted only when
the caller-authored refresh entry's stable error codes exactly match live
refreshable drift; the same errors reject `context_ready`, so scripts validate
but never choose route intent. Candidate-present `mem_review.status=used`
requires a non-empty summary after all four sources are exhausted; a passed AI
Gate requires non-empty reviewed scope and load-bearing conclusions. Closed
schema fields and source-specific locators keep raw source payloads out of
persisted evidence through field-specific validation. `task_branch_stale` is
refreshable; malformed task facts are not.
Expected failures use stable error codes and do not include raw JSON content,
exception strings containing local paths, or secrets.
The schema and runtime additionally enforce the exact semantic state pair
`typed_exit=blocked` <-> `ai_review_gate.status=blocked` in both directions.

## GitHub and Git Operations

### Shared Base Resolution And Sync

`sync-base` is the only deterministic owner of selected-base resolution and
safe refresh. The fixed precedence is explicit `--base`, non-empty scalar
`base_branch`, the first existing exact local or remote-tracking ref in
`base_branch_candidates` order (default `dev`, `develop`, `main`, `master`), then
remote default from `git ls-remote --symref <remote> HEAD` when no candidate
exists. Multiple existing candidates are ordered, not ambiguous. Validate every
candidate with `git check-ref-format --branch`. Remote-default failure blocks.
Never fall back to the current branch. Evaluate and validate sources in
precedence order: once a higher-priority explicit or scalar source is selected, malformed
lower-priority scalar or candidate input must not reject that selection.
Candidate validation still fails closed before config-candidate or
remote-default facts are produced when neither higher-priority source is selected.

`--resolve-only` emits canonical resolution JSON and SHA-256 before fetch. The
digest covers the complete resolution object, including decision checkout
branch, HEAD and clean state. It
does not write a resolution file. `--execute` requires the expected digest,
recomputes resolution at the execution boundary, and blocks before fetch if
digest, checkout identity, or
resolution changed. The executor uses only:

```text
git fetch --no-tags <remote> refs/heads/<base>:refs/remotes/<remote>/<base>
git merge --ff-only <remote>/<base>
```

The merge is legal only when the clean decision checkout is the selected base
and local base is an ancestor of remote. Missing local/remote refs, dirty state,
fetch failure, divergence, wrong checkout, or post-sync mismatch blocks. It
must not use `git branch -f`, reset, checkout, stash, rebase, force fetch, or a
current-branch fallback.

After synchronization, the executor rebuilds the same source/base/remote/
candidate resolution identity with the synchronized decision checkout and emits
it as `post_sync_resolution` plus `post_sync_resolution_sha256`. The original
`resolution.resolution_sha256` remains the pre-sync identity that binds only
resolve to execute. Already-equal execution may produce equal pre/post digests;
a fast-forward must produce a different post-sync digest.

`check-base-sync` does not mutate Git. It consumes `--result-json` and validates
Draft 2020-12 schema identity, `facts_sha256`, the pre-sync resolution digest,
the post-sync resolution object/digest, selected refs, clean state, and
decision/local/remote full-SHA equality against live Git. Its successful typed
output carries `post_sync_resolution_sha256` for the next consumer instead of
re-exporting the pre-sync digest. It does not fetch, merge, decide scope, judge
semantic pass, choose a route, or manage evidence files. Its workflow-only
`--record-skipped` path emits stdout-only machine facts after the AI has
reviewed a non-repo route; standalone rejects that path.

`prepare-task` requires the prior validator/guard
`post_sync_resolution_sha256` and the same resolver inputs. It calls the shared
resolver/sync core before `gh auth status`, issue read, and duplicate search,
then reruns an independent guard immediately before each GitHub, worktree, and
task mutation boundary. The task guard occurs after worktree/identity setup and
immediately before `task.py create`. `--base-branch` can assert equality but
cannot rewrite config/config-candidate/remote-default provenance as explicit.
The legacy planner/executor freshness functions remain adapters only. A stale
planner result is blocking, not permission to continue planning. Each guard
consumes the preceding guard's post-sync digest and returns its own post-sync
digest for the next boundary. Neither prepare output nor task-start context
persists the complete resolution/result stdout payloads.

Always gate GitHub operations with `gh auth status` through `require_gh_auth()`.
Do not assume the GitHub CLI is configured just because `gh` exists.

Default `prepare` must be side-effect-free for GitHub and filesystem writes
until the corresponding explicit confirmed/executor flag is present. It may call
`gh issue view/list` for explicit issues and duplicate search, but planner
output must stay on stdout and must not write `.trellis/tasks/<task-slug>/task-start-context.json`.
It must not call `gh issue create`, `git worktree add`, or `task.py create`
unless the corresponding explicit confirmed/executor flag is present and the
workflow has already required AI/human intake plan review. Confirming or creating a
source issue alone still must not write handoff; handoff is written only by
`--create-worktree` or `--create-task` in the chosen workspace.

Before publish, reject uncommitted non-metadata changes. Metadata-only paths are
defined by `METADATA_ONLY_PREFIXES` and `METADATA_ONLY_FILES`; update these
constants deliberately if Trellis metadata ownership changes.

Task work commits use two deterministic entrypoints. `check-commit-messages
--candidate-artifact <task-local-path>` validates schema/evidence/freshness,
then calls the existing `validate_commit_message()` parser even when the branch
range contains no commits. `create-task-commit --candidate-artifact
<task-local-path>` consumes only a passed AI-reviewed and authorized plan,
stages literal exact paths, binds the full expected index tree and each exact
path's blob/mode before hooks run, uses `git commit --cleanup=verbatim -F`, and
checks parent, raw message bytes, committed paths, real commit tree/blob/mode,
unrelated preservation and hook mutation. Candidate validation, executor entry
before staging, and the
check immediately before `git commit` reject active merge, cherry-pick, revert,
rebase, sequencer, or `git am` state without consuming markers or changing
HEAD/index/worktree. Snapshot capture recognizes index mode `160000`, requires
an initialized and clean submodule rooted at the exact path, and records its
worktree HEAD; uninitialized, dirty, unborn, or ambiguous gitlinks fail closed.
The executor revalidates every planned gitlink immediately before staging. It
does not pass a non-deleted gitlink to `git add`: it writes the artifact's
reviewed `gitlink_head` to the exact mode `160000` index entry with
`git update-index --cacheinfo`, then verifies both the index OID and current
worktree HEAD. A B-to-C change before exact staging therefore blocks before
index mutation; a later change cannot place C in the index because the index
content comes from the artifact rather than the mutable worktree. Deliberate
gitlink deletion remains on the ordinary literal delete path.
The same authority applies to ordinary files, executable modes, symlinks and
deletes. Snapshot capture maps a rename destination to `renamed_from` and a
copy destination to `copied_from`; the fields are mutually exclusive. The
executor treats only `renamed_from` as authority to remove and exact-stage the
source. `copied_from` is provenance only: it never authorizes source removal or
automatic staging. A dirty copy source appears as its own snapshot entry and
must pass its own classification/Phase 2 coverage; unrelated staged source
content blocks before the isolated transaction. The executor re-reads each
authorized ordinary path once, requires its bytes/mode to match the artifact's
SHA-256/mode/delete identity, writes the matching blob to the object database,
and constructs the index with exact cache entries. It never delegates reviewed
content choice to live `git add`. Candidate self bytes come from the already
validated in-memory plan using deterministic JSON serialization; raw bytes
appended after validation are never staged.

Staging and hook execution use an isolated index plus a detached transaction
HEAD that shares the repository object/config/hook store. `git commit
--cleanup=verbatim -F` therefore runs the real hook chain without changing the
live branch or index. Parent/message/path/tree/blob/mode, full worktree
snapshot, candidate bytes, operation state, branch ref and complete live index
preimage are revalidated before publication. The executor holds the real Git
`index.lock` as a sentinel across the conditional ref advance, candidate
publication, final live-index publication and every rollback. The sentinel is
never renamed into the live index: final index bytes use an independent
same-directory temporary file and are published while the sentinel still
blocks real Git writers. A separate candidate guard prevents a compliant
candidate writer from racing publication. Immediately after conditional ref
advance, the executor acquires the corresponding loose-ref lock and verifies
the advanced value; a concurrent `update-ref` either wins before that guard and
is preserved, or fails while the guard is held. Rollback may restore candidate
bytes only while that guard and the exact executor-published result identity
still match. Only a fully validated commit is published to the real branch,
live index and committed candidate result. A
partial cache write, rejecting or mutating hook, operation-state change,
postcondition mismatch, or candidate/index publication failure restores or
keeps transaction-owned entry state and returns blocked. Ref rollback is
compare-and-swap; ownership loss preserves a concurrent ref/candidate state and
reports incomplete rollback rather than overwriting it. After candidate result
and live index publication, while the ref guard and index sentinel still hold,
the executor validates the guarded ref/index transaction state and performs one
final candidate inode/content identity read. That read is the success
linearization point. A bypassing atomic/editor candidate writer that publishes
C before the read is detected; the executor conditionally rolls back ref/index,
preserves C and returns blocked. A writer after the read is a later operation;
the executor returns immutable commit blob/result digest evidence, never
overwrites C, and performs no later fallible success check. Candidate guards
remain mandatory for every project companion candidate writer, while this
ordering handles writers that bypass the guard without claiming impossible
cross-file atomicity.
Path-bearing identity queries use
literal pathspecs and require zero or one exact NUL-delimited record. Same-path
content or mode mutation is a blocked postcondition with preserved Git state.
Blocked evidence distinguishes planned paths that merely remain staged after an
unchanged hook rejects the commit from real mutation: the former records
`hook_mutation=false`, while unexpected dirty paths, planned-path unstaged
drift, tree/blob/mode drift, unrelated drift, or unexpected staged paths are
recorded explicitly and make hook mutation true only after hook execution.
The blocked recorder and validator use the failure-stage state matrix from
`data-contracts.md`: `pre-commit` has unchanged HEAD and either no tree or a
matching index tree; `commit` always has tree evidence sourced from the index
when HEAD is unchanged and from the commit when HEAD changed; `postcondition`
always has changed HEAD, created message/path identity and commit-sourced tree
evidence. A missing tree, wrong source, impossible HEAD/identity combination,
pre-commit mismatch, or mutation flag inconsistent with recorded drift fails
before result bytes are written. Package schema tests and runtime tests must
carry the same positive and negative cross-product rather than adding one-off
conditions for individual payloads.
Neither command classifies scope, authors message semantics, chooses a route,
pushes, or rewrites history; broad `git add`, automatic reset, stash, amend,
rebase and force operations are prohibited.

`finish-work.sh` is an internal helper, not the normal user path. It must reject ordinary direct calls before closeout-plan,
push, draft PR, archive, or publish side effects; only the explicit
`trellis-finish-work` entrypoint may pass the `--from-trellis-finish-work`
intent marker. `publish-pr` is retained only as an unconditional compatibility
blocker: it performs no repo/task resolution or side effect and points callers
to `trellis-finish-work`. Every interruption is resumed through that same
state-aware entry.

Finish-summary separates AI judgment from deterministic facts. The explicit
finish entry writes task-local `finish-summary-index.json` with reviewed
problem/outcome/behavior/surface/contract/search-term judgment and passes it via
`--finish-summary-index-file`. The companion rejects factual issue/PR/branch/path
fields in that input, injects task/Git/ledger/artifact/time facts, derives
`retrieval_text`, and validates the strict shared schema. Dry-run and formal
finish call the same `prepare_closeout()` pipeline. Dry-run returns the
immutable `closeout-plan.json` bytes and canonical `closeout_plan_digest`
without writing. Formal finish requires `--expected-plan-digest`, rebuilds and
compares the plan before its first side effect, then persists the exact plan
with immutable readiness. Formal finish never writes an empty-PR summary,
never invokes upstream `add_session.py`, and never reads/writes
`.trellis/workspace/**`.

Prepare parses `.trellis/config.yaml` with the installed official
`parse_simple_yaml` implementation and binds the empty `hooks.after_archive`
state into protected inputs. Missing or empty configuration is supported;
non-empty, ambiguous, unreadable, NUL-containing, or symlinked configuration
fails before push, PR creation, or archive. The companion never executes or
interprets an `after_archive` command and does not include hook mutations in the
transaction allowlist.

Prepare must also build and schema-validate the complete future archived
finish-summary before dry-run/formal diverge. The immutable plan stores that
template with the fixed maximum-width sentinel PR
`#9223372036854775807`, its exact UTF-8 `write_json` byte digest, the Branch Review Gate
`generated_at` snapshot time, and the only runtime-substitution fields:
`github.pr_url` and `index.search_terms.pr_refs`. Formal final projection copies
the template and substitutes one canonical PR identity; it does not call the
general summary builder after content push, verifier, evidence commit, or draft
creation. Dry-run and formal therefore expose the same local build/path/schema
errors before the first side effect.

Formal finish pushes the reviewed content HEAD first, records deterministic
pending marketplace evidence, runs the required verifier against that remote
HEAD, replaces only the machine evidence with passed facts, and commits/pushes
the exact plan/readiness/verifier/ledger allowlist. It then creates or reuses
one draft PR for the exact base-repo/head-repo/head-branch/base-branch/title/body
identity. Every effective fetch and push URL for `plan.git.remote` returned by
Git is preceded by a raw-config gate. The validator reads every
`remote.<name>.url` and `remote.<name>.pushurl` with NUL-delimited values and
origins, rejects empty values, boundary whitespace, Unicode/ASCII controls,
ambiguous framing, unreadable origins, and any NUL byte in a relevant config
file. Missing `pushurl` uses the raw `url` set, matching Git semantics. Every
raw `url.*.insteadOf` / `url.*.pushInsteadOf` base and pattern receives the
same boundary/control/origin validation before rewrite. Effective output is
then consumed without trim/normalization, must have one newline-delimited value
per raw source value, and after Git rewrite resolution must use one credential-free
GitHub transport form: `https://github.com/<owner>/<repo>[.git]`,
`ssh://git@github.com/<owner>/<repo>[.git]`, or
`git@github.com:<owner>/<repo>[.git]`. HTTP, `git://`, `file://`, local or bare
paths, scheme-less host/path forms, userinfo/password/token variants, explicit
ports, query strings, fragments, and extra path segments fail closed. Each
strictly parsed URL and `headRepository.nameWithOwner` must normalize to the
immutable `plan.git.repo`; `headRepositoryOwner.login` must agree and
`isCrossRepository` must be `false`. Because `gh pr list --head` cannot scope
by owner, the query requests all three head-repository fields, rejects missing
or inconsistent fields, and rejects a same-name cross-repository candidate
before applying the 0/1/>1 exact-candidate rule. Before archive, the body
identity is the task-local `pr-body.md` raw UTF-8 text: no trim, newline
insertion, or second normalization is permitted between plan hashing,
readiness, create, reuse, and final projection. After the official move, remote
PR queries are checked only against the plan's exact title and raw-body digest;
they do not reopen task-local body or readiness artifacts. The normal flow also
carries the already-bound PR number/URL across archive and ready confirmation.
A fresh exact-archive reentry recovers that number/URL from the immutable
commit's deterministic `finish-summary.json` blob, without opening the
working-tree summary or invoking the general summary validator, then requires
the unique target-repository repo/head/base candidate to match it. A fork
candidate, multiple target-repo matches, changed title/body, or a number/URL
change within one bound invocation fails closed.
The canonical PR URL is used to build the only final finish-summary in the
active task, including exactly one `PR #<number>` ref. A temporary future
archive projection validates schema, path safety, artifact locators, ledger,
gate, readiness, and the exact archive allowlist before the official
`task.py archive --no-commit` move.
Final projection and both incomplete/exact recovery use the same strict PR URL
parser. It compares GitHub owner/repository identity case-insensitively against
normalized `plan.git.repo`, but preserves the exact valid remote URL casing as
the canonical summary output. It still rejects a different repository,
non-HTTPS transport, invalid owner/repository component, non-positive or
leading-zero number, trailing/extra path, query, and fragment.

The finish-work prepare path has its own reviewed-body resolver. It preserves
the lexical path and rejects paths outside the lexical repo root. The only
re-anchor is Darwin's verified fixed `/var` -> `/private/var` system prefix:
the code requires `/var` itself to be that symlink and requires both the repo
suffix and file-relative suffix to match structurally. It never searches
arbitrary ancestors with `samefile`, so an external user symlink that points
back to the repo remains outside and is rejected. It then uses `lstat` to
reject any existing symlink component from repo root through
`.trellis/tasks/<task>/pr-body.md`. This includes directory aliases,
multi-level ancestors, task-directory parents, dangling/loop links, and the
final file. It then requires `--body-file` to equal that direct task path,
reads both source and task-local bytes, requires exact byte equality, and
decodes strict UTF-8. It rejects `--body-artifact`, external files even when
their stripped text is equal, final-newline differences, and Markdown
hard-break space differences. The `publish-pr` compatibility command never
resolves a body file or artifact.

Marketplace machine evidence uses the task-relative locator
`marketplace-verification.json`, never the active task path. Final projection
resolves that locator while the task is active, requires the artifact bytes to
exist, and requires the ledger digest to match. Archive and archived recovery
never parse or rewrite the ledger or verifier artifact.

The archive transaction creates one metadata commit containing only the
prevalidated active-to-archive task move, pushes it, and requires local branch,
remote branch, and draft PR head to match. Only then may the executor run
`gh pr ready`. A retry derives its exact failed transition from persisted
plan/readiness, pending or passed marketplace evidence, final-summary presence,
active/archive locators, Git index/tree state, remote HEAD, and PR identity
before archive; after the move it uses only the committed plan, exact
path/blob/commit lineage, remote HEAD, and remote PR identity. It
must not repeat a completed push, verifier, evidence commit, draft bind, or
final projection and must not skip the failed transition. After archive
push it may only recheck identity and retry draft-to-ready; it must not rebuild
artifacts, rerun the verifier, commit, or push.

Immediately before official `task.py archive`, the executor rechecks the
official current `YYYY-MM`, the empty `after_archive` state, a clean index, the
exact planned untracked output set, every tracked path as a regular file, Git
mode equality (`100644`/`100755`), and working bytes against the evidence blob.
Any failure leaves the task active and the PR draft; official archive has not
run.

Before dry-run and formal diverge, prepare lexically `lstat`s each existing
archive root, month, and final destination component. It rejects every symlink,
including dangling links and links to repo-internal targets, without following
or reading the target; the final locator must also be absent. The identical
preflight runs again immediately before official move to reject
prepare-to-move drift. Prepare also validates the effective
`task.json.children` value as `list[str]` and mirrors
official active-task exact/suffix lookup. A matching active child with
`task.json` blocks because official archive would rewrite that child; an
already archived child is historical metadata and does not block the parent.
Initial failures happen before Git, GitHub, or recorder mutation.

The plan records sorted `move_paths`, `tracked_move_paths`,
`untracked_archive_outputs`, and exact pre-draft `evidence_paths`.
Initial evidence commit parent equals `reviewed_work_head`. A task that remains
active across a month boundary may supersede only an exact committed evidence
plan: a new dry-run uses the official current month, formal requires its new
digest, and an additive evidence commit changes only `closeout-plan.json` and
`pr-readiness.json`. `git.evidence_parent_head` binds that predecessor, whose
plan/evidence chain is recursively validated; no reset, force-push, directory
migration, verifier rerun, or PR replacement occurs. The archive commit parent
must equal the latest validated evidence commit. `tracked_move_paths` require
both active deletion and archive addition. Outputs created only after the
evidence commit, currently `finish-summary.json`, are immutable
`untracked_archive_outputs` and require only the archive addition; an active
deletion for them is invalid because that path never entered the Git index.
Evidence validation uses the evidence commit tree to prove that every and only
`tracked_move_paths` exists under the active locator before archive.
Until the exact archive commit exists, fresh execution and recovery require
this exact mixed no-renames set, active locator absence, the complete
prevalidated archived working-tree file set, exact dirty/staged paths, and
working-tree-to-Git blob continuity. Every tracked active blob in the evidence
commit must equal its archived working-tree and archive-commit blob
byte-for-byte, except `task.json`, whose only permitted change is the official
`status=completed` and `completedAt=YYYY-MM-DD` transition. A partial, missing,
extra, misclassified, or content-tampered pre-commit set is never valid.
The final summary is also a deterministic continuity input: fresh execution
and incomplete recovery rebuild its exact UTF-8 JSON bytes/digest from the
immutable template and the already-bound remote PR number/URL.

Once current `HEAD` is the exact planned archive commit, every archived
finish-work reentry, including a normal task that still has
`task-start-context.json`, reads the immutable plan from the current commit
blob. The plan and
that commit's parent, path set, tree, and blobs are authoritative. Missing or
tampered archived working-tree files and their dirty status do not block
pushing that exact commit, remote/PR HEAD checks, or draft-to-ready. Fresh exact
recovery reads the committed `finish-summary.json` blob to recover the original
PR number/URL and verify the deterministic bytes/digest without calling the
general local summary validator; it never reads the archived working-tree
summary. A missing, closed, or replacement PR fails closed. If current `HEAD`
is absent from or mismatched with the planned archive transaction,
recovery falls back to the pre-commit metadata path and keeps all layout,
dirty/staged path, blob, official `task.json`, and lineage checks fail closed.
An archived directory containing only `closeout-plan.json` is resolvable only
by the `trellis-finish-work` recovery entry; ordinary task resolution still
requires `task.json`. That plan-only entry reads the plan from the current
commit blob rather than trusting working-tree bytes, then applies a dedicated
fail-closed workspace boundary before GitHub access or committed-archive
recovery. The boundary requires the actual Git toplevel, configured and remote
repository identity, current head branch, available base ref, current HEAD,
plan digest, active/archive locator relationship, task identity, and exact
archive transaction to match the immutable plan. It is not a context-free
bypass and is unavailable to every other command, which continues to require
`task.json` and `task-start-context.json` in worktree mode.
Before ordinary resolution or canonicalization, the finish entry classifies
the raw locator as only a task basename, the exact former active locator, or
the exact archive locator. Path-like locators require lexical containment and
`lstat` from repo root through every ancestor and the final task directory.
Basename locators apply the same raw check, before ordinary resolution, to
`<repo>/<basename>`, `.trellis/tasks/<basename>`, the archive root, and archive
candidates in ordinary resolver order. Each direct or archive candidate first
retains only raw `symlink_component` evidence, then applies the ordinary
resolver's exact follow-symlink `directory + task.json` predicate. A matching
alias is rejected, while an unmatched alias continues to the next candidate.
These checks reject internal/external,
relative/absolute, ancestor/final, multilevel, dangling, and loop symlinks
before the ordinary resolver can discard raw alias evidence. The ordinary
resolver then runs so explicit `task.json`, active task, and normal archived
`task.json` precedence stays unchanged. Plan-only recovery runs
only when ordinary resolution returns not-found: an exact archive locator may
select that exact candidate, while basename/former-active fallback must find
exactly one matching archive month and fails closed on multiple matches. The
resolved plan-only target must still equal the plan's canonical archive
locator. The only outer re-anchor is the verified Darwin system `/var` ->
`/private/var` mapping; arbitrary `samefile` or user-created aliases are never
trusted.

Closeout failure injection must enter through production `cmd_finish_work()`.
Use a real temporary Git repository, bare remote, official `task.py archive`,
and a controllable fake GitHub store/verifier at external command boundaries.
Do not mock `prepare_closeout`, evidence commit, draft binding, final projection,
archive transaction, recovery, or ready transition. Every failed stage records
real active/archive locator and path state, task status, PR draft/state/number,
exact local/remote/PR HEAD SHA values, complete dirty/staged path sets, then
clear the failure and re-enter production `cmd_finish_work()`. The observed
retry must execute the failed transition without repeating an earlier mutating
transition or skipping ahead.
The negative matrix also covers a fork PR with the same branch, SHA, title, and
body. It must fail while the task is active and before final-summary binding;
archived recovery must reject the fork from remote repository facts without
opening or rebinding the already-archived summary.

Use the intake/task `base_branch` for diff ranges and PR base. Do not fall back
to the GitHub default branch when the task has an explicit base.

For PR body publishing, companion scripts may validate objective Markdown
structure, required sections, forbidden low-information phrases, non-empty
validation / impact / safety content, Docs SSOT section/key presence, and Issue
Scope Ledger close/ref semantics. They must not decide whether the release
explanation or Docs SSOT rationale is true or sufficient; that judgment belongs
to the AI readiness review before
`trellis-finish-work`. Formal closeout accepts only `--body-file` pointing
directly to the current task-local `pr-body.md`; it rejects `--body-artifact`,
generated body fallbacks, and readiness-relative `body_file` resolution. Formal
finish binds that reviewed `pr-body.md` into
`pr-readiness.json.publish_inputs`, including the exact
repo/base/head/title/raw-body digest/draft/reviewed source and canonical snapshot
digest. Active-state retries consume the committed readiness artifact;
after the official archive move, recovery reads only the committed immutable
plan and uses its title/body digest plus Git/remote facts. Command-line
title/body/draft/base overrides fail closed.
Final projection validates all task-relative artifact locators while the task
is active. The official archive move carries those files unchanged to the
planned archive locator; no gate, readiness, body, ledger, report, or summary
path is rewritten after archive. Archived recovery checks the exact planned
locator/file set and Git blob continuity without re-entering body, summary,
ledger, readiness, or marketplace artifact validators.

Planning and Phase 2 helpers follow the same recorder / validator boundary:

- `record-planning-approval.sh` records prior AI/human planning review and the
  user's explicit post-planning confirmation after the main session completed
  planning artifact ambiguity review and displayed task-local links to
  `prd.md`, `design.md`, and `implement.md`; it must not decide whether
  planning is sufficient or whether natural-language ambiguity was actually
  resolved. New artifacts use `schema_version=1.2`,
  `review_prompt_presented_at`, `approved_at`, `reviewed_artifacts[]`, the
  `approved_artifacts` alias,
  `user_confirmation.source=explicit-post-planning-review`, and structured
  `ambiguity_review` evidence. The recorder builds controlled-term,
  scan-scope, hit, unchecked-hit, and checked-dimension fields from fixed
  constants and deterministic scans after receiving AI-provided
  `--ambiguity-reviewer`, `--ambiguity-summary`, passed status, and one
  classification record for each retained controlled-term hit. It must fail
  closed before writing when any hit is unclassified or classified as
  `contract_violation`.
- `check-planning-approval.sh` validates all three planning artifact entries,
  hash / size metadata, confirmation source, structured `ambiguity_review`
  fields, and required audit fields before `task.py start`, before
  implementation dispatch, and before `phase2-check.json` can be recorded. It
  must fail closed on old schema, missing or non-passed `ambiguity_review`,
  missing reviewer/summary, incomplete controlled terms, wrong fixed
  `scan_scope`, missing or stale `hits`, non-empty
  `unchecked_normative_hits`, missing checked dimensions, old source, Phase 0
  handoff confirmation, missing docs, or changed planning document content.
  It must rescan `prd.md`, `design.md`, and `implement.md` and compare the
  current scan to the recorded scanner evidence instead of trusting the stored
  array blindly.
  Recorded HEAD, modified-time, and `dirty_paths` remain audit context, but
  validator freshness is tied to `prd.md`, `design.md`, and `implement.md`
  content digests. A later implementation commit, metadata tail, or unrelated
  working-tree dirty path must not block planning approval while those three
  reviewed planning documents still match.
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
  decision evidence. It also owns the two append-only schema 1.2 repair records:
  `--invalidate-event-id` appends one digest-bound provenance invalidation, and
  `--link-failed-event-id` plus `--link-termination-event-id` appends one
  digest-bound same-agent failed-to-termination recovery edge. The AI/main
  session supplies reason/evidence after making the correction judgment; the
  recorder only verifies target identity and writes it. Its old `--status-event`
  path must fail closed and point callers to
  `record-subagent-liveness-event.sh`; it must not maintain a second active
  status event enum.
- `check-agent-assignment.sh` validates JSON structure, Chinese logical-role
  enum values, required fields, HEAD resolvability, optional current-HEAD
  freshness, liveness snapshot fields, status event enum/evidence fields,
  correction/link unique ids and target digests, forward same-agent recovery
  graph, recovery-chain completion, and digest metadata. Its effective
  projection excludes invalidated progress/status-request rows; raw history is
  never deleted. It must not judge semantic reuse quality or review sufficiency.

Workspace boundary helpers are deterministic validators and fact snapshots:

- `check-workspace-boundary.sh --json --task <task-path>` reports
  `workspace_mode`, `expected_workspace`, `actual_repo_root`,
  `source_checkout`, `task_dir`, `task_dir_relative`, source checkout status,
  task worktree status, suspicious source artifacts, `status`, and `errors`.
- In `workspace_mode: worktree`, recorder/validator commands that write or
  validate task artifacts must validate portable `workspace_slug`,
  `task_workspace_id`, and `task_artifact_dir`, derive the machine-local task
  worktree from the current checkout, `.trellis/.runtime/guru-team/**`, and
  `git worktree list`, then confirm the actual repo root equals that derived
  worktree before touching `planning-approval.json`,
  `phase2-check.json`, `agent-assignment.json`, `review.md`, `reviews/*.md`,
  `review-gate.json`, or equivalent task-local artifacts.
- In `workspace_mode: worktree`, a missing task-local `task-start-context.json` is
  also a boundary failure for these recorder/validator commands, because the
  script cannot validate portable identifiers before local runtime/Git worktree
  resolution and must not fall back to
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
`issue-scope-ledger.json`, `pr-body.md`, `pr-readiness.json`, `marketplace-verification.json`,
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

When an append-only ledger already contains an incorrect observational
provenance row, natural-language correction text is disclosure only. A main
session must append a schema 1.2 `event_corrections[]` record bound to the exact
target event digest before the machine gate can exclude it. When a historical
`failed` row resumed, failed again, was terminated, and then handed to a
replacement, but the failed-to-termination edge was not recorded, the main
session may append one schema 1.2 `recovery_links[]` edge. The validator must
still traverse the existing resume/replacement predecessors through a real
later `completed`; correction/link rows cannot invent, rewrite, or delete any
status event.

When a review round has findings, including a previous final-review round that
found a new issue, it must later be closed by one of three explicit forms: the
same technical `agent_id` recorded as `问题闭环审查代理` with
`findings_count: 0` and `reuse_decision: reuse-for-closure`; a different fresh
`问题闭环审查代理` whose technical `agent_id` has not appeared in any earlier
`review_rounds[]` and whose `reuse_decisions[]` entry records
`decision=new-agent` with exact `from_round`, `to_round`, closure `agent_id`,
reviewed `head`, and non-empty `reason`; or, when the finding owner objectively
failed, was interrupted, or became stale and cannot continue, a replacement
closure reviewer that may close only that finding when
`reuse_decisions[]` records `decision=replace` with `from_round` / `to_round`
and `status_events[]` records the predecessor evidence plus
`replacement-started` with `predecessor_agent_id`, `predecessor_event_id`,
`replacement_reason`, `handoff_summary`, and replacement `completed` evidence.
A passing gate must validate that every finding owner has one of those three
closure forms. A closure round that still reports findings becomes a new
finding owner and must itself have a later explicit closure before the gate can
pass. The gate then validates a fresh
`最终放行审查代理` review round: `review_rounds[].round` values are unique and
strictly increasing in recorded order, it is the unambiguous last round,
`reviewed_head` equals the reviewed code HEAD, `findings_count` is 0,
`reuse_decision` is `new-agent`, and the final reviewer technical `agent_id` has
not appeared in any earlier `review_rounds[]`. This is an objective
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

When writing temporary issue body files, use `tempfile.NamedTemporaryFile`
and unlink the file in a `finally` block. Existing example:

- `create_issue()`

## Validation

For any script change, run:

```bash
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
```

When changing `review-branch`, `finish-work`, or `publish-pr`, also run dry-run
or representative script paths in a disposable worktree whenever practical.

## Archived Finish-Summary Backfill

`backfill-finish-summary.sh` is a public, one-time migration helper for
archived tasks created before normal finish-work wrote `finish-summary.json`.
The Bash file is a thin wrapper around the canonical Python
`backfill-finish-summary` subcommand. It never reads active tasks,
`.trellis/workspace/**`, or `.trellis/.runtime/**`, and it never calls GitHub or
`trellis mem`.

The command requires exactly one of `--dry-run` and `--write`. `--force` is
valid only with `--write`; `--task` accepts only a clean repo-relative archived
task root. A task root contains a direct whitelist artifact or existing
`finish-summary.json` marker, and none of its strict ancestors below the archive
root contains such a marker. Discovery uses the same marker rule and stops
descending after the first task root. This rejects archive grouping directories
and every task subdirectory without relying on directory basenames. Invalid
arguments, non-root targets, or symlink escapes exit 2 before scanning. A
completed batch exits 0, while any task-local read/build,
validation, or write error is isolated, reported, and makes the final exit code
1 after the remaining tasks are processed. `--json` returns the stable object
fields `mode`, `archive_glob`, `scanned_tasks`, `to_write`, `skipped`, and
`errors`; the default renderer prints the same facts as a stable table. Every
`to_write` table row includes `source_artifacts`, `missing_fields`, and
`confidence` so a human preview preserves the JSON decision evidence.

Dry-run and write share discovery, extraction, build, and schema validation.
Write mode creates only missing summaries unless `--force` is present, uses a
same-directory temporary file plus `os.replace()`, then rereads and validates
the result. No invocation creates a committed global archive index. Per-task
errors contain only repo-relative task/artifact paths and reasons, never source
content or secrets.

### Remote Marketplace Verification Gate

For tasks that change the workflow marketplace, preset, overlays, installer, schema, or public extension contract, publish is fail-closed after the branch push and before `gh pr create`. The deterministic `verify-marketplace` companion command records task-local `marketplace-verification.json` with repository, remote, branch/ref, verified content HEAD, remote HEAD, command exit codes, stdout/stderr digests and sizes, and installed workflow/preview/schema digests. It executes remote branch `trellis init`, workflow preview, workflow switch, canonical preset reapply, and runtime-ignore checks in a clean temporary repository. It does not decide PR readiness.

`issue-scope-ledger.json` must carry one exact structured `remote_marketplace_verification` evidence object in the primary issue and every close issue. Before the verifier it is `status=pending`, `required=true`, points to task-relative `marketplace-verification.json`, and explicitly does not satisfy final publish. Formal closeout pushes the reviewed content HEAD, runs the verifier, replaces only those structured entries with real `status=passed` facts, then commits the immutable plan/readiness/verifier/ledger evidence allowlist and pushes it before binding a draft PR. The final summary is created once in the active task with that draft identity and is included only in the archive transaction; no post-PR or post-archive metadata tail is allowed. Missing, pending, failed, stale, tampered, or mismatched evidence blocks. No release tag is created by this gate.
