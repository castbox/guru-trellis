# Release Guru Trellis Version Contract

## Ownership And Boundary

`release-guru-trellis-version` is a repository-private semantic orchestration
Skill for official `castbox/guru-trellis` releases. Its shared definition lives
under `.agents/skills/` and its Codex, Claude, and Cursor copies are
project-local discovery projections. It is not a public `guru-*` Skill and MUST
NOT enter the Guru Team registry, extension manifest, package tree,
marketplace, preset, overlay, ownership inventory, or a business-repository
installation.

This Skill defines no public interface, schema, runtime, script, checkpoint, or
typed exit. It composes the current owners and consumes only their declared,
fresh results. It never copies, replaces, shortens, or weakens an owner's
semantic gate, freshness check, confirmation boundary, mutation, or
fail-closed route.

## Invocation Input And Fresh Authority

Resolve exactly these six inputs for every invocation:

- repository;
- current release Issue;
- target repository tag;
- target extension revision;
- official Trellis CLI version;
- predecessor tag.

Before either stage, fresh-read the live Issue body, comments, and state;
`origin/main`; local branch and worktree state; tags and GitHub Releases;
version surfaces; and the current contracts of every invoked owner. Reject a
missing or ambiguous input, multiple version mapping, stale fact, cross-SHA
candidate, unprovable lineage, or live identity mismatch. Recovery repeats the
live reads and may use only an owner-private checkpoint that its owner still
accepts as fresh.

Keep the version surfaces distinct: `trellis/guru-team-extension.json.version`
is the canonical extension revision; the installed
`.trellis/guru-team/extension.json` owns `extension.version` and `source`
provenance; `.trellis/.version` records the Trellis CLI version. Compare the
last value with `official_cli_version`, not with the extension revision. An
unchanged CLI requires no version-file edit. Source synchronization, a remote
Release, validators and throwaway installation do not establish that a real
local checkout has received the new tools.

At entry, inspect the calling checkout and the retained primary checkout used
for ordinary repository work. Resolve and show which exact local targets this
release request covers. Do not select every registered peer or release-candidate
checkout. Keep this target selection in the current dialogue; it is derived
invocation context, not another release input or a durable workspace mapping.

## Two-Stage Lifecycle

### Stage 1: Preparation Task And PR

Route preparation through standard intake and the existing global workflow.
Original requirements and Planning owners define the whole preparation Task,
the current Delivery slice, its independent completion conditions and remaining
work. Use each actual Delivery's public key and planning_root; a source commit,
one merged slice or a local installation does not establish whole-Task completion.

For every actual preparation Delivery, execute this current owner chain:

1. The original Author completes the slice's stable `prd.md`, `design.md`,
   `implement.md`, Delivery Policy and Docs SSOT Plan. Wording, independent
   Architecture candidate/final assessments, Approval and Activation retain
   their original order and conditions.
2. Phase 2 implements the complete selected slice and its necessary engineering
   checks. Original RDT and Architecture owners integrate every necessary
   complete target and perform readback before the local task commit.
   `integrated_pending_review` records integration only, never quality pass.
3. `guru-create-task-commit` exclusively owns the exact local task commit
   preview, confirmation and mutation after complete slice implementation,
   engineering validation and necessary knowledge integration. Its actual
   `pre_review_committed` enters only the original implementation router.
4. The original constructor and public `begin_check` fix the complete committed
   `B..H` Candidate. A new independent `guru-review-branch` reviewer, uninvolved
   in implementation, performs Architecture before/after, all applicable Check
   responsibilities and full Branch Review in the same complete review.
   Actual passing judgments are recorded as `check` then `full_review`;
   either missing result prevents a complete `passed`.
5. Only current complete Review with zero open P0-P3 findings enters the
   Architecture publication eligibility check and `guru-review-task-delivery`.
   Delivery Review judges the slice, remaining preparation and release work,
   exact diff, real validation and reviewed-content identity, and authors the
   truthful Chinese Refs-only PR title/body. Only its checked `ready` enters
   `guru-publish-task-delivery`.
6. Publish owns its reviewed push, PR binding and Ready transaction. Only its
   checked `ready_for_merge` enters `guru-merge-task-delivery`, which owns the
   independently confirmed expected-head merge. Only its checked `delivered`
   enters `guru-review-task-completion`. Output loss returns to the original
   TaskCommit, Review, Publish or Merge owner for the same operation, key,
   fixed base and actual commit/PR facts; it does not repeat completed effects.

The per-Delivery honest path is:

```text
stable_plan -> implementation_and_engineering_checks -> necessary_rdt_architecture_integration_and_readback -> guru-create-task-commit -> constructor/begin_check -> guru-review-branch -> publication_architecture_eligibility -> guru-review-task-delivery -> guru-publish-task-delivery -> guru-merge-task-delivery -> guru-review-task-completion
```

There is no separate candidate/final Check, fixed pre/post-promotion second
review, early Draft publication or source-only TaskCommit profile. Real
successor content changes still return to the original writer, then TaskCommit
and affected independent review. The original reviewer judges retained
coverage, the complete delta and combined effects; “one review” never exempts
changed content or a necessary unchanged consumer. Keep the original fixed
base and actual history, and adopt engineering facts only when applicable.

#### Complete Source Before Actual Adoption

The preparation installation uses the original `guru-upgrade-tools` contract
with `dependency_mode=source_locked`. When actual adoption requires a new clean
committed preparation source, original scope and Planning owners allocate
ordered independently deliverable slices within the same Task:

- D1 delivers the complete distributable canonical source, version producers
  and direct consumers, private release contracts and real regressions, and
  necessary public documentation and knowledge. D1 must validate its own
  source, interfaces, dependencies, installation and complete selected-platform
  projections before its full commit/review/readiness/Delivery. A temporary
  installation may prove those source behaviors at its declared layer, but
  never actual checkout adoption or formal `source_locked`.
- Only after D1 is actually `delivered`, original Completion returns
  `additional_delivery_required` for the unimplemented adoption. Its original
  planning router invokes Creation to establish D2. D2 receives its own Planning
  and Activation.
  D2 reads the real D1 Delivery result and complete clean matching source,
  then the original tools owner previews, prepares, invokes and verifies actual
  `source_locked` adoption. D2 includes all installed-content after in its own
  complete engineering, TaskCommit, Review, readiness and Delivery chain.

Do not create D2 early or route TaskCommit success to tools. D1's own completeness
cannot depend on D2 already being complete. D1 source defects or required
validation failures cannot be deferred to obtain a pass. If D1 itself needs
prior target adoption, return to original scope/Planning before proceeding.
A dirty source, an undelivered commit, planned failed Review or rewritten
historical pass cannot supply the formal adoption source.

The tools owner must validate the actual target extension, complete managed
package/platform/workflow projections, source provenance, CLI and source lock,
target resolver and native entry, ownership, executable modes, sidecars,
preservation, parity and drift. Preserve Task/archive/workspace/session/user
configuration, peer tools and common runtime pointers. Current old installation,
schema-projection differences and drift failures retain their actual meaning
until the adoption slice establishes its results. Do not treat ordinary
self-reapply blocked by historical Tasks as permission to leave adoption
unfinished, convert those Tasks, use ordinary apply or hand-edit managed files.

#### Whole Preparation Completion And Reference-Only Closure

Completion reviews the *whole preparation task* against accepted scope and all
Delivery/evidence facts. Unimplemented adoption follows
`additional_delivery_required`, not `evidence_pending`; other real gaps retain
their original owner routes. Do not Finish while preparation business work
remains. Only `completed` enters `guru-complete-task-closure`. The release Issue
is `reference_only`, so Closure must return `no_mutation`, never close it.

After the acceptance-finish Architecture check, `guru-finish-task` owns archive
and a separately reviewed, confirmed bookkeeping commit, PR and expected-head
merge. Only its checked `success` enters `guru-cleanup-task-resources`, whose
exact resource deletion needs its own review and confirmation. Finish
bookkeeping is not another business Delivery, release-status commit or a
substitute for independent business Review. Preserve caller-owned resources.

Every preparation PR uses `Refs #<issue>` with no closing keyword. The release
Issue still owns the post-merge exact candidate, tag, smoke, GitHub Release,
selected local convergence and separate Issue-closure boundary. Stage 1
reference-only Closure never substitutes for that Stage 2 decision.

Keep #794's supported in-flight recovery with its matching complete original
provider. Recover already executed commit, PR, metadata and binding facts
without repeating them; pending new remote effects require current independent
Review and readiness. A partially recorded Review resumes the same key/B/H and
original judgment through its owner; the first slot cannot invent the second.
Owner-private metadata and integration facts do not prove reviewed content,
convert old pass results or create a release-status commit or self-reference
loop.

### Stage 2: Post-Merge Exact Candidate

After Stage 1 Delivery and Finish bookkeeping merges, discard the preparation
branch HEAD, Branch Review, Delivery Review result, and all earlier release
evidence. Fresh-fetch `origin/main`, prove its live merge/base lineage (including
the terminal archive), and freeze one exact candidate
commit and tree. Every release check and later mutation must bind that same
candidate identity; the preparation reviewed HEAD is never substituted for it.

Before any tag mutation, perform the release Issue's scoped minimum gate. Run
it from the clean candidate checkout with `HEAD` equal to `candidate_commit`,
and bind every command and result to `predecessor_tag` and `candidate_commit`:

| Gate | Stable repository locator and executable entrypoint |
| --- | --- |
| candidate lineage and predecessor-to-candidate full diff | `git rev-parse HEAD`, `git rev-parse "${predecessor_tag}^{commit}"`, `git merge-base --is-ancestor "${predecessor_tag}^{commit}" "${candidate_commit}^{commit}"`, `git diff --find-renames --find-copies "${predecessor_tag}^{commit}" "${candidate_commit}^{commit}" --`, and `git diff --name-status "${predecessor_tag}^{commit}" "${candidate_commit}^{commit}" --` |
| version-axis mapping and public release text | Fresh-read `README.md`, `trellis/guru-team-extension.json`, `.trellis/spec/docs/public-docs.md`, `trellis/workflows/guru-team/README.md`, and `trellis/presets/guru-team/README.md` from the candidate tree; run `git show "${candidate_commit}:trellis/guru-team-extension.json" \| python3 -m json.tool` and `git show "${candidate_commit}:README.md"` and compare the target repository tag, extension revision, and official Trellis CLI version with the six invocation inputs. |
| candidate dogfood installation identity | Read `git show "${candidate_commit}:.trellis/guru-team/extension.json"` and `git show "${candidate_commit}:.trellis/.version"`. Require installed `extension.version` to equal the canonical target extension revision and the CLI record to equal `official_cli_version`; validate the actual managed projections and source lock. Resolve the installed `source` to its real reviewed source and compare its canonical managed assets and lock with the candidate. A proven equivalent committed predecessor source is valid: do not require installed provenance to name the candidate's own final HEAD. A missing, stale or unprovable installation returns to preparation and the affected original gates before a new freeze; passing validators alone does not satisfy this comparison. |
| source and installed validators | `./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json` and `./.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json` |
| Shared/Codex/Claude/Cursor parity | Run the source validator once for each current public projection root: `for root in .agents/skills .claude/skills .cursor/skills; do ./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --platform-root "$root" --json; done`. Codex uses the shared `.agents/skills` root; require no retired managed `.codex/skills/guru-*/` projection, under the current ownership and `MIGRATION-724.md` contracts. Separately inventory this private release Skill's actual discovery copies and byte-compare their `SKILL.md` and `references/contract.md` with `.agents/skills/release-guru-trellis-version/`; the current private copies are in `.codex/skills`, `.claude/skills`, and `.cursor/skills`. Private copies do not restore a public managed root or enter public distribution. |
| ownership, preset, and dogfood drift | `./trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json`, `./trellis/presets/guru-team/scripts/bash/apply.sh --repo . --platform claude --platform codex --platform cursor`, and `./trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .`; inspect and reject any unexpected mutation from reapply. The narrowly reviewed historical-Task preflight route below can cover only the distributable preset part of this cell. |
| install/update/reapply checks | Resolve `trellis_fork_source` to the already-built clean Fork checkout whose HEAD equals the candidate tree's pinned Trellis source-lock commit, then run the verifier's focused profile against the exact candidate: `TRELLIS_FORK_SOURCE="${trellis_fork_source}" TRELLIS_WORKFLOW_SOURCE="gh:castbox/guru-trellis/trellis#${candidate_commit}" ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh --mode focused --platform codex`. The resolved checkout is invocation-local evidence, not a seventh release input. This one clean Shared plus Codex install with existing-project update/reapply is the ordinary Issue's targeted proof; four-platform source-contract parity remains the separate gate above, using the three current public roots with Codex sharing `.agents/skills`, and this focused invocation is not the cumulative multi-platform Release Gate matrix. |
| predecessor upgrade and retired assets | For an Issue requiring predecessor cleanup, read `trellis/guru-team-extension.json` and `trellis/presets/guru-team/source/trellis-source.json` from the actual `predecessor_tag` tree. Require its manifest `target_trellis_cli` to equal its lock `cli_version`; a mismatch stops this cell. Derive invocation-local `predecessor_cli_version` from that agreed value and `predecessor_fork_commit` from the same lock, then resolve the already-built clean predecessor Fork checkout. These derived values are not additional release inputs; `official_cli_version` still identifies the current candidate CLI. Run `TRELLIS_FORK_SOURCE="${trellis_fork_source}" TRELLIS_PREDECESSOR_SOURCE="${predecessor_fork_source}" TRELLIS_PREDECESSOR_COMMIT="${predecessor_fork_commit}" TRELLIS_WORKFLOW_SOURCE="gh:castbox/guru-trellis/trellis#${candidate_commit}" ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh --mode existing --platform codex --before-tag "${predecessor_tag}" --before-cli "${predecessor_cli_version}"`. Compare the predecessor managed Skill/package/command inventory to the candidate registry and inspect the upgraded target: every retired managed asset must be absent, with no unresolved local-edit conflict or `.new`/`.bak` sidecar. This is one targeted existing-install cell, not the cumulative multi-platform matrix. |
| secret scan | Derive the exact changed-file set with `git diff --name-only --diff-filter=ACMRT "${predecessor_tag}^{commit}" "${candidate_commit}^{commit}" --` and run the current environment's real secret-scanning capability over those candidate file bytes. A missing scanner, incomplete file set, alert, or unavailable result is `SKIP` or `FAIL`, not a pass. |
| residue check; residue and diff hygiene | `git status --short`, `git diff --check`, and `find . \( -type d -name '__pycache__' -o -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*.new' -o -name '*.bak' \) \) -print`; any unexpected output is blocking. |

#### Historical-Task Preflight Observation

Always execute and retain the ordinary candidate self-reapply result above.
If it stops, the independent Release reviewer may consider a separate clean
standalone installation only when all of these conditions hold:

- The sole stop is `upstream_delivery_migration_required` from ordinary
  `delivery_installation.py` preflight. Review its actual Task references and
  caller path; the diagnostic code alone is insufficient. Establish that they
  are preserved historical records, with no invalid current Task input or
  missing actual tools upgrade hidden by that early stop.
- The source candidate remains unchanged. Its installed extension version,
  CLI version, complete actual managed assets, source lock and real reviewed
  provenance independently satisfy the candidate dogfood installation gate.
- The standalone source and installed targets bind the same exact candidate.
  Compare the complete canonical source set with the candidate Git bytes and
  modes. Perform actual clean installation, reapply for Claude, Codex and
  Cursor, and installed validation through the existing owners. Require the
  complete expected managed set, manifest candidate/source identity, source
  lock and workflow to match that candidate, with no unresolved sidecar or
  residue. A sampled subset or a focused single-platform result is insufficient
  for this route.

Only after reviewing those results may the independent Release reviewer accept
the standalone proof for distributable preset installation and reapply. It does
not replace actual candidate dogfood evidence or selected local target updates.
The source self-reapply remains stopped; its guard is unchanged and historical
data is unconverted. Report that observation separately from the standalone
coverage. Any other apply error, unknown input, missing evidence, stale version
or asset mismatch follows the ordinary fail-closed stop. This route creates no
new executor, state, DTO, lifecycle phase or cumulative Release Gate matrix.

After these deterministic results are current, independently review the full
diff, version mapping, command outputs, secret-scan result, residue result, and
unverified boundaries. This Skill MUST NOT replace these targeted locators with
an ad hoc command set and MUST NOT expand the task into the cumulative
multi-platform Release Gate matrix owned by a dedicated Release Gate Issue.

Immediately before the GitHub Release mutation, generate the Release title and
body from the live Issue, exact candidate diff, current validation evidence,
and candidate identity, then perform semantic review. Do not create a
task-local body handoff.

Only after the candidate gate passes, independently confirm annotated tag
creation/push for that candidate. Verify the remote tag points to the exact
candidate before running the separately confirmed tag-pinned smoke. Only a
passing smoke for that tag and candidate permits the separately confirmed
GitHub Release; verify its tag and published state. Then handle the selected
local targets under Local Installation Convergence below before reviewing the
live release Issue for its separate closure confirmation and mutation. A failed
or skipped check blocks the later action, subject only to the precisely bounded
historical-Task observation above. The Stage 1 reference-only Closure never
substitutes for this Stage 2 decision.

## Local Installation Convergence And Final Report

After verified publication, handle every local target selected at entry before
final Issue closure and the completion response. Close the release Issue only
after those targets converge, or after the original scope owner resolves a real
scope question and explicitly establishes that a target is outside this release
request's accepted scope. Do not automatically exclude a blocked target. Reread
the live Issue and all release and local results at that final closure boundary.
This is local release closeout, outside the preparation Task's accepted scope.
It does not change the frozen candidate or an immutable published tag. Reread
each target's live Git state, canonical and
installed versions, installed provenance, actual managed bytes and CLI record.
An already matching, usable installation needs verification, not a redundant
write. Any required Git synchronization remains its original separate operation.

For a tools update, load `guru-upgrade-tools` from the complete clean published
source and use `source_locked` with the exact checkout. Follow that owner's
read-only preview, one prepare for the reviewed operation, original invoke and
same-operation recovery. Use its locked local Fork checkout and matching build;
do not clone another checkout or modify upstream packages. When building is
needed, use current pnpm without pinning the execution version or changing the
source's package-manager declaration. The original owner supplies actual target
validation and native-entry evidence and preserves Task, archive, workspace,
session and user configuration bytes, peer tools and common runtime pointers.
Do not copy its implementation or replace it with a hand-edited manifest.

Historical Task guards do not authorize a full installation migration or Task
conversion. If the request genuinely needs data conversion, return to the
original `guru-upgrade-installation` owner with that separately reviewed scope.
Do not bypass guards, rewrite archives, change `.trellis/.version` to a Guru
revision, or use successful throwaway evidence in place of these real targets.
An installed source may be an actual reviewed predecessor with the same
canonical managed assets and source lock; do not chase a self-referential HEAD,
create a release-status commit, or mutate a published tag to refresh provenance.

If local maintenance blocks or returns recovery, preserve the remote published
facts and the exact target's unfinished result. Resume only through its original
owner; do not repeat tag or Release creation or prematurely close the Issue.
Do not report overall completion while a selected target remains unverified or
outdated. The final response
separately states the remote tag/Release result, each local target's installed
extension version, real source provenance, CLI version and actual validation,
and any unfinished target or unverified boundary. Keep these observations in
the dialogue and the original owner's permitted recovery state, not a new
release ledger or tracked status file.

## Reviewed-Content Freshness

Use the existing `guru-reviewed-content-1.0` owner contract. Changes to actual
delivery bytes, durable README or Docs authority, configuration, schema,
scripts, or tests make every affected Phase 2, Branch Review, Delivery Review,
Publish, Merge, Completion, Finish, or exact-candidate gate stale and require
its owner to rerun.

Changes confined to `.trellis/tasks/**`, `.trellis/workspace/**`,
`.trellis/.runtime/**`, `.trellis/guru-team/extension.json`, or `.DS_Store`
remain lifecycle/provenance metadata only when the current owner contract
allows them. They do not refresh, repair, or prove a gate. Finish's exact
terminal bookkeeping is owner-controlled; arbitrary metadata commits are never
used to record or recover release progress.

## Forbidden Persistence

MUST NOT create task-local `release-notes*.md`, a PR or Release body handoff,
or a dynamic checkbox checklist in `implement.md`. `implement.md` remains a
stable implementation plan.

MUST NOT write tracked lifecycle state containing HEAD, timestamps, phase
progress, Gate pass/fail, finding closure, candidate status, tag status, smoke
status, GitHub Release status, or user authorization. Authorization exists only
in the current dialogue and is never reused, serialized, hashed, or persisted.

## Independent Mutation Confirmations

Each mutation is a separate boundary. Immediately before that one action,
fresh-read its authority, display the exact repository/object/ref/SHA, command,
files or remote objects affected, and expected result, then obtain confirmation
that authorizes only that displayed action:

| Mutation | Exclusive owner or boundary |
| --- | --- |
| task commit | `guru-create-task-commit` |
| preparation PR push/bind/Ready | `guru-publish-task-delivery` |
| preparation PR merge | `guru-merge-task-delivery` |
| Finish archive projection | `guru-finish-task` |
| Finish bookkeeping publication | `guru-finish-task` |
| Finish bookkeeping PR merge | `guru-finish-task` |
| annotated tag creation/push | post-merge tag boundary |
| tag-pinned smoke | post-tag smoke boundary |
| GitHub Release creation | post-smoke Release boundary |
| release Issue closure | Issue closure boundary |
| each selected local tools installation | `guru-upgrade-tools` |
| branch/worktree/task cleanup | cleanup boundary |

Confirmation for one row cannot authorize, pre-authorize, or be reused for any
other row. Publish's reviewed preview identifies its exact repository, branch,
HEAD, PR payload and remote actions before one current-dialogue confirmation;
it does not authorize the later preparation PR merge. Finish has three distinct
owner-confirmed mutations (archive projection, bookkeeping publication, and
bookkeeping merge), not a single inherited Publish confirmation. A failed or
changed plan requires its owner's fresh review and confirmation; Completion and
reference-only Closure cannot borrow a mutation confirmation or close the
release Issue. Tag, smoke, Release, Issue closure, and cleanup remain separately
reviewable even when the same user performs them consecutively.

## Fail-Closed Stops

Stop in the current owner before later publication or release side effects on
stale evidence, cross-SHA evidence, `FAIL`, `SKIP`, identity mismatch,
unsupported input, or an unknown, multiple, ambiguous, consumer-mismatched, or
unmapped exit. The Historical-Task Preflight Observation above is the sole
bounded alternative for that source preflight stop; it never turns the original
result into a pass or exempts another failure. Do not guess a route and do not
create a metadata commit to mark the stop or resume point.

This contract never itself runs a real commit, push, PR, merge, tag, smoke,
GitHub Release, Issue closure, local installation, or cleanup mutation. Those
actions remain with their named owner or explicit post-merge boundary and
require the independent current-dialogue confirmation above.
