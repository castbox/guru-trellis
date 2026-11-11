# TaskCommit pre-review contract 3.0

## Entry and semantic responsibility

Use `delivery_pre_review_commit` for a necessary dirty increment and
`delivery_pre_review_committed_reentry` for an already committed candidate.
Both require the exact registered Task/Delivery, applicable accepted Planning,
implementing phase and the Delivery's fixed complete base B. Read the selected
Delivery planning bodies and Task accepted scope. Complete implementation,
Planning-selected engineering validation and necessary original-owner knowledge
integration/readback before this step. Integration remains pending independent
review. This owner judges whether the exact content can form a review candidate;
it does not declare independent implementation quality passed.

The public input aggregate is 3.0. It contains no check_result_id. Dirty candidate
4.0 and result receipt 3.0 use commit_kind=pre_review. Legacy final/draft profiles,
Check-dependent commit and early Publication edges are retired. Follow
MIGRATION-794 with the complete provider at the pinned predecessor for old
operation recovery; never relabel an old pass or import old private runtime.

## Output and clean reentry

`pre_review_committed` contains only task_ref, delivery_key and
branch_review_commit. Its sole consumer is guru-pre-review-commit-router. That
router binds the real implementation Candidate and begin_check before the
fixed complete independent Review. No Commit result enters Publication.

Clean reentry consumes regular JSON file locators through `scripts/invoke.sh
--input <input.json> --owner-result <review.json>`. One object may use stdin `-`.
It verifies actual nonempty B..HEAD, stable committed Task identity/source,
all five Delivery planning files and absence of active Git operations or dirty
business content. It never stages, runs hooks or creates a commit. The bounded
Plan2 committed-source bridge remains owner-private: all current files must
match actual original committed blobs/modes, with the explicitly selected
markdown_relative_links_v1 relocation only when the original owner reviewed it.
No empty commit restores output. A genuine new increment uses exact prepare.

## Dirty transaction and recovery

The two calls remain prepare-task-commit.sh and invoke.sh --candidate-artifact.
Before mutation, review exact content, engineering evidence, knowledge after,
path classifications and message, then present the precise action. The current
dialogue supplies any required Git confirmation. Never persist authorization.
The current candidate contains the complete dirty preimage and exact paths.
Old unexecuted candidates require complete reprepare. A current receipt recovers
the same actual parent/HEAD/tree/message and cleanup without another commit.

Classify every dirty path exactly once:

- `task-reviewed`: current task scope covered by the current scope and engineering self-check;
- `unrelated-preserved`: outside scope and preserved byte-for-byte;
- `unreviewed-blocking`: possibly in scope but not covered by the current approved plan;
- `ambiguous-blocking`: the AI cannot classify reliably.

Only `task-reviewed` paths and a rename source inherited from its reviewed
destination may enter `exact_stage_paths`. Copy provenance does not grant stage
authority. Every ordinary file binds exact bytes and mode; every gitlink binds
the reviewed parent index mode/OID. A staged gitlink deletion records mode
160000 with index_blob=null and deleted=true even when the child directory remains.
The parent HEAD type is read only while capturing this absence. Gitlink rows have
worktree_sha256=null and no child HEAD/initialized/dirty fields. Replacements
whose new index mode is a blob use the ordinary worktree content contract. The
executor rereads the parent entry, writes the captured OID with update-index,
and removes staged deletions and rename sources from the isolated index. It
never enters the child or obtains a pointer through child HEAD/git add.

Author `type`, `scope`, `summary`, `background`, `changes`, `boundaries`, and
`validations` from the current diff, task docs, and durable docs. When the
current task has an owner-native source Issue, the AI may also author the
minimal positive `issue_reference`; no-Issue tasks omit it. The builder
produces the exact Chinese Conventional Commit subject and four-section body,
adding `#<issue>` and `Refs #<issue>` only when that optional reference exists,
then runs the shared parser. Issue close keywords belong to the PR body.

## Semantic Gate And Confirmation

Before any Git side effect, the AI reviews scope, stage paths, message meaning,
issue refs, deployment/upgrade/security impact, unrelated preservation and
evidence freshness. Scripts cannot infer this semantic pass. Branch name,
branch role, protection, sharing, other task ownership, remote branch presence,
open PR presence, and publication state are not commit eligibility facts and
must not be queried to grant or deny this action.

When the current conversation already contains one exact commit request, that
request is the authority for the matching displayed action. Otherwise, when one
current, unique commit action requires user authorization,
display its repo, branch, HEAD, paths and message and prompt `确认继续`. Any clear
affirmative response authorizes the displayed action in the conversation only;
the user never repeats its SHA, digest or prescribed sentence. Reconfirm only
when plan, target, HEAD, scope or authority changes.

Return `revision-required` when the candidate can be corrected without new
scope/evidence. Return `blocked` when task ownership, evidence or a path remains
ambiguous.

## Validation And Execution

### Public Happy Path

The package root for the two commands below is
`.trellis/guru-team/skills/packages/guru-create-task-commit/`. Thus the installed
preparation entry is
`.trellis/guru-team/skills/packages/guru-create-task-commit/scripts/prepare-task-commit.sh`.
Platform discovery copies include `scripts/invoke.sh` but do not include this
preparation script.

The unique recommended normal path is one
`scripts/prepare-task-commit.sh` call followed, after the unchanged action is
confirmed in the current conversation, by one
`scripts/invoke.sh --candidate-artifact <prepared-locator>` call. Its stable
command id is `invoke-guru-create-task-commit`. The normal branch accepts only
the prepared package-owned candidate locator; it never accepts confirmation,
authorization, a selected exit, message authoring, or replacement Git facts.

The public invocation reuses the existing exact executor directly. It does not call the
compatibility checker first because the executor already performs the same
authoritative candidate validation at the mutation boundary. It then projects
the executor's actual result through the current Delivery output schemas. Thus
the normal Agent path is two package invocations rather than prepare, check,
create, and legacy projection, while preserving one pre-confirmation prepare
and one post-confirmation authoritative validation.

After the commit object, parent, tree and message are verified and the live
pre-publication conditions still hold, the exact executor writes one minimal
ignored `task_commit_happy_path_result` receipt before `git update-ref`. The
receipt binds the exact candidate locator, task/base/ref identity, parent,
commit tree and raw message digest. It is not a committed result by itself: the
public invocation projects `pre_review_committed` only when the live symbolic ref points to the bound
commit and all receipt identities verify. If ref mutation did not occur, the
candidate remains authoritative for a normal retry and the executor may
replace the prewritten receipt. If interruption occurs after ref mutation, the
public invocation uses the candidate plus receipt to finish the exact-path live-index
postconditions and cleanup without rerunning hooks, creating another commit or
updating the ref again. A changed ref, parent, tree or message fails closed.
The next complete prepare for the same task retires the previous receipt before
creating its new candidate. Compatibility executor calls do not request or
write this public-invocation receipt.

The old `scripts/invoke.sh --invocation <envelope>` raw-result projection and
old Task candidate public invocation are retired with `schema_mismatch`.
Pinned-old private executor diagnostics do not establish a current Delivery gate.
`check-task-commit-plan.sh` and `create-task-commit.sh` remain stable
package-private testing, diagnostic, and bounded recovery entries.

`scripts/prepare-task-commit.sh` canonicalizes and validates current `delivery-4.0` candidates
before any required confirmation. `scripts/check-task-commit-plan.sh` repeats
objective validation immediately before execution. `scripts/create-task-commit.sh` repeats
that validation, rejects active merge/cherry-pick/revert/rebase/sequencer/`git
am` state, and rejects staged paths outside the exact plan.

The executor creates a temporary detached worktree at the reviewed parent,
materializes exact blobs/modes in an isolated index, checks that index out into
the transaction worktree, and invokes real repository hooks through
`git commit --cleanup=verbatim -F <0600-message-file>`. The hook lookup honors
the repository's current `core.hooksPath`; a transaction-local proxy only
forwards arguments and records each hook exit code so `post-commit` failure can
be reported even though Git itself does not fail the command for that exit.
Hooks therefore observe the reviewed parent HEAD, exact index and worktree, and
the reviewed message file rather than the unrelated live workspace.

Before live-ref publication, the executor verifies hook exits, the unchanged
message file, transaction index and worktree, parent, raw commit-object message,
committed path set, every blob/mode and complete tree. Any hook rejection,
message rewrite, extra tracked or untracked path, rename, deletion, stage,
unstage, exact-path mutation or mode drift fails closed. A transaction commit
created before such a failure is reported as `created_commit_sha`; the live
branch remains at the reviewed parent and the private candidate remain available for bounded recovery.

The same pre-publication gate compares the live worktree's semantic dirty
snapshot as well as its branch and semantic index preimage, so a normally
misconfigured hook cannot publish after touching the user's live tracked,
untracked, staged, unstaged, or gitlink state. The isolated index lives inside
the transaction temporary directory. Every success and failure path removes
the detached worktree registration; cleanup failure is a bounded recovery and
retains any already-created commit identity.

Only after those checks pass does the executor conditionally advance the live
branch with `git update-ref <ref> <new> <old>`. It then refreshes only the exact
live index paths and compares semantic `mode/blob/stage/path` entries, never raw
index-file bytes. A failure after live ref advance reports the same created
commit with `transaction_stage=live_ref_published`. It never pushes,
rewrites published history, stashes, amends, or guesses a correction, and owns
no custom lock, rollback, atomic-replace, or concurrency protocol. A failure
before ref publication preserves the live ref/index and keeps the private
candidate; a failure after ref advance reports the created commit for bounded
same-plan recovery.

On success, immutable Git history is the source for parent, message, paths and
tree facts. The executor returns only `pre_commit_head` and `commit_sha`, then
deletes the private candidate and call-local semantic authoring. A failed attempt
retains both for bounded retry; successful same-plan recovery verifies the
published commit before deleting both. The executor does not append `committed`,
`result`, `tree_evidence` or other Git-derived facts to tracked task metadata.

## Exit

Return exactly one declared exit: `pre_review_committed`, `revision-required`
or `blocked`. The successful minimal DTO enters the fixed-candidate router,
which constructs and binds the actual candidate before independent Review.
Finding fixes return through implementation, necessary integration and current
engineering checks before a fresh exact pre-review commit. They do not pass an
independent pre-commit Check.
Apply the shared candidate contract to determine the fix delta, affected
checks and still-applicable facts; a commit does not require unrelated review
or command repetition. Same-tree commits refresh only necessary binding,
without claiming unchanged environment, toolchain or required checks.

### Explicit Markdown link projection compatibility

The original TaskCommit AI owner reviews actual committed blobs, each original reference target, and the exact Plan2 artifact writes before selecting `markdown_relative_links_v1`. The deterministic function `runtime/migration.py:project_planning_links` is shared by that write preparation and source equivalence validation. It supports UTF-8 inline Markdown links/images with plain or angle-bracket destinations and optional quoted titles; only relative destinations without spaces, escapes or parentheses are rebased to the same existing file from the new public planning root. Query/fragment and all other bytes are preserved. External schemes, absolute paths, fragment-only links, fenced/inline code and JSONL are unchanged. Reference definitions or unsupported inline syntax return to this original migration/Author owner; missing targets require restoration or semantic revision. No Markdown normalization, public origin field, Planning private bridge reader or second state authority is introduced.

Clean validation recomputes projected bytes from original Git blobs and current public planning_root, including modes and ancestry. Direct HEAD paths always remain strict, regardless of association mode. A genuine content change uses the dirty path. Existing absent-mode associations cannot be relabeled; prepare a fresh execution copy/Plan2 and review its real mapping. The optional field is an explicit additive private 1.0 schema extension; old readers reject this mode until the matching package is installed, while existing absent-mode inputs retain their prior semantics.

## Fixed content baseline

Dirty commit and clean reentry retain the caller-selected fixed development
base B and the existing Delivery candidate base when present. Task base_branch
remains the PR target name. A remote base advance never selects a new content
base or adds ancestry requirements. Both paths preserve the complete nonempty
fixed B..HEAD range and actual identity, Planning, exact paths, hooks and
recovery facts. Necessary commits evolve HEAD through the original
implementation/TaskCommit owners; clean retained content creates no extra
commit. The committed-candidate router constructs the actual Candidate before
single independent Review. No independent Check supplies commit eligibility.
