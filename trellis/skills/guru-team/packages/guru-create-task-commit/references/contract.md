## Public Delivery integration 1.0

This current Skill consumes the target installation's reviewed Delivery API
1.0 and Task schema 2.0 through a thin projection. `task_ref` is a locator;
`delivery_key` is the opaque public identity. Read the current `interface.json`
profile schema and its exact exit consumer before invoking. Do not derive an
identity from branch, worktree, legacy cycle, PR, or Task status. D1 and later
Deliveries use the same entry and lifecycle. The public phase never proves a
semantic pass. Historical facts never prove a currently applicable gate.

Read the Delivery's public `planning_root` for its three planning documents and
context JSONL; Task-root PRD remains overall scope. Rework keeps the Delivery
identity and returns through the real current stage owner's public operation to
the earliest affected role. Invalidate only the affected results. Unchanged,
still-applicable execution facts need not be rerun. A successful recorder is
objective evidence only; the AI must actually perform this Skill's full review.
Missing public API or an unmigrated old record stops with precise migration
remediation. Do not install a private alternative, select a source fallback,
convert a legacy checkpoint into pass, or switch an old installation before
upstream migration/default-cutover qualification.

### Committed content and mutation are distinct

All current commit profiles bind `delivery_key` and `check_result_id`.
`delivery_committed_reentry` reviews the actual registered checkout, exact HEAD,
non-metadata clean candidate and nonempty full fixed base-to-HEAD diff. Latest
target ancestry is not a qualification condition.
The public Task record must name a nonempty selected `base_branch`; missing base
returns `stale_identity/base_branch` to its original base/binding owner. This
clean path never inherits the dirty preparation path's default `main`.
Current public Check identity, applicability and candidate verification remain
required after base reconciliation. Its consumer obtains fresh applicable
Delivery Architecture and the first full independent Branch Review;
Check and bounded continuity cannot replace that first Review. If clean stdout
is lost, the same owner rereads the unchanged public Check/candidate and returns
the same committed DTO. It keeps the public Check fact and creates no additional
clean receipt or legacy Task checkpoint.
The stable Task identity/source/generation and all five current Delivery
planning files must match committed bytes. Actual Plan2 path relocations may
use this owner's minimal committed source bridge below. A passed clean candidate
returns `committed` without stage, commit, hook or tracked gate writes.

Dirty `delivery_initial_commit`, `delivery_revision_reentry`, and
`delivery_finding_fix_commit` retain exact path classifications, structured
Chinese message, AI review, current conversational commit confirmation,
executor and same-commit receipt recovery. Preserve unrelated paths and index
state. The owner-private Delivery candidate/receipt is versioned independently;
legacy Task candidates cannot become new Delivery pass. `committed` hands
`task_ref`, `delivery_key`, `check_result_id`, `base_ref`, and
`branch_review_commit` to the committed-candidate router. If the commit changed
HEAD, that router invokes the real current stage owner for rework and a fresh
Check before first full independent Review; a clean retained HEAD can proceed
directly. A committed fact cannot replace that Review.

### Bounded Plan2 committed source migration

The original TaskCommit semantic owner reads the actual reviewed Plan2 artifact
write set and original Git blobs, and judges the same Task/generation/scope and
five-file association. Only then call owner-private
`scripts/migrate-delivery-source.sh --input <delivery_source_migration> --owner-result <actual-review>`.
Its independent input schema binds the actual Plan2 locator/workspace, key,
source commit and five source paths, with optional `planning_projection=markdown_relative_links_v1`. Absence preserves strict original bytes/modes and existing associations are not automatically upgraded. It validates exact relocated bytes/modes,
source ancestry and the upstream parsed Task/Delivery relation. The ignored
source association retains only key, original commit, five source paths and the explicitly selected projection mode;
no gate, content copy, review history, digest bundle or authorization is stored.
Upgrade consumes its intermediate `source_binding` locator only for backup and
same-plan recovery/rollback; it does not judge or fabricate the source mapping.

Clean reentry uses direct HEAD paths when present. Only genuinely absent HEAD
paths can consume that association; every current file must equal the original
blob/mode (or the explicitly reviewed destination-only projection) and the current Check/candidate, stable identity and full diff remain
required. Actual content changes use the dirty path. A successful necessary
dirty commit retires the association. Missing input returns to this original
owner, never invents a new commit or a private public-state authority.

## Preserved semantic and transaction duties

The duties below apply to the current Delivery input and output contracts.
Historical data is read only by its named history or migration owner.

# `guru-create-task-commit` Contract

## Entry And Candidate

Workflow and standalone mode read the current Task identity, Delivery plans,
actual passed public Check, exact current candidate and complete Git state.
The input binds `delivery_key` and `check_result_id`; the original commit
transaction validates them again at its mutation boundary. It does not read
Check or Planning private checkpoints. Dirty paths are facts, not authority.

Build the next three-digit candidate under the ignored owner-private path
`.trellis/.runtime/guru-team/task-commit-plans/<task-key>/<sequence>.json`.
The candidate is a temporary semantic plan and executor input. It contains
only task/Git preimage, the complete dirty snapshot, AI path classifications,
derived exact paths, canonical message, and final AI semantic result. It has no
authorization, cross-Skill digest, freshness journal, or terminal result. It is never a
task artifact, never enters `path_classifications` or `exact_stage_paths`, and
is never staged or committed.

The current Delivery candidate uses `delivery-1.0`. Older Task candidates are not converted and
no removed facts are synthesized. The owner deletes or rejects it and performs
a complete reprepare from current Phase 2 evidence, live task/HEAD/snapshot,
scope classifications, and message review.

Classify every dirty path exactly once:

- `task-reviewed`: current task scope covered by fresh Phase 2 evidence;
- `unrelated-preserved`: outside scope and preserved byte-for-byte;
- `unreviewed-blocking`: possibly in scope but not covered by Phase 2;
- `ambiguous-blocking`: the AI cannot classify reliably.

Only `task-reviewed` paths and a rename source inherited from its reviewed
destination may enter `exact_stage_paths`. Copy provenance does not grant stage
authority. Every ordinary file binds exact bytes and mode; every gitlink binds
the reviewed submodule HEAD and clean state. The executor rechecks these facts
before any index/ref mutation.

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
public invocation projects `committed` only when the live symbolic ref points to the bound
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

`scripts/prepare-task-commit.sh` canonicalizes and validates current `delivery-1.0` candidates
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
branch remains at the reviewed parent and the private candidate plus Phase 2
checkpoint remain available for bounded recovery.

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

Return exactly one declared exit: `committed`, `revision-required`, or
`blocked`. The committed DTO is projected to Branch Review, which verifies the
current commit directly from live Git. A finding fix returns through
implementation and a full Phase 2 rerun before a fresh private candidate.

### Explicit Markdown link projection compatibility

The original TaskCommit AI owner reviews actual committed blobs, each original reference target, and the exact Plan2 artifact writes before selecting `markdown_relative_links_v1`. The deterministic function `runtime/migration.py:project_planning_links` is shared by that write preparation and source equivalence validation. It supports UTF-8 inline Markdown links/images with plain or angle-bracket destinations and optional quoted titles; only relative destinations without spaces, escapes or parentheses are rebased to the same existing file from the new public planning root. Query/fragment and all other bytes are preserved. External schemes, absolute paths, fragment-only links, fenced/inline code and JSONL are unchanged. Reference definitions or unsupported inline syntax return to this original migration/Author owner; missing targets require restoration or semantic revision. No Markdown normalization, public origin field, Planning private bridge reader or second state authority is introduced.

Clean validation recomputes projected bytes from original Git blobs and current public planning_root, including modes and ancestry. Direct HEAD paths always remain strict, regardless of association mode. A genuine content change uses the dirty path. Existing absent-mode associations cannot be relabeled; prepare a fresh execution copy/Plan2 and review its real mapping. The optional field is an explicit additive private 1.0 schema extension; old readers reject this mode until the matching package is installed, while existing absent-mode inputs retain their prior semantics.

## Fixed content baseline

Both dirty commit and clean re-entry consume the current Check candidate’s
exact base OID. The Task base_branch remains the PR target name; origin/base
is not reread to select content or require ancestry. A clean candidate needs
its complete nonempty fixed base..HEAD diff and all original identity, plan,
content, staging/hook and recovery facts. Necessary commits evolve actual HEAD
through the original candidate/Check owners; clean retained content makes no
extra commit. Remote-ref advancement alone never changes this transaction.
