# #467 preparation design

## Version mapping

Treat repository tag, extension revision, official CLI/core, and fixed Fork
source as independent axes. Change the current target to
`v0.6.17-guru.2`/`0.6.17-guru.43`/`0.6.17`/`8336e78b8fafe2a4bc4ea3d01815a61cf4f08983`.
Describe `.2` as a target until GitHub confirms tag and published Release.
The predecessor `.1` remains a historical release. The exact release candidate
is determined only from fresh post-Finish `origin/main`.

## Intake correction

The `guru-create-task` precondition must search every registered checkout and
local branch for the proposed TaskId and TaskRef, while leaving unrelated old
states untouched. Worktree scanning may read each artifact but must not require
unrelated legacy active/archive copies to be globally unique. Historical
branch artifacts with invalid JSON are irrelevant unless they occupy the
proposed TaskRef. Resource-ledger validation applies to the proposed TaskId;
legacy ledger schema for a different task is not a creation precondition.
Keep the existing target conflict and stale-base failures.

The canonical implementation is under `trellis/skills/guru-team/runtime/`;
the installed `.trellis/guru-team/` copy is a preset projection. Add focused
unit coverage for these three normal-path regressions and target conflicts,
then reapply the preset and verify byte parity.

## Lifecycle and release gates

Phase 2 reviews the preparation candidate and its tests. Task Commit owns
exact staging and commits. The first full Branch Review precedes serialized
Architecture/RDT promotion; promotion mutates shared delivery content, so
Phase 2, Task Commit and full Branch Review run again. Delivery Review authors
the Chinese `Refs #467` PR. Publish, Merge, Completion, Closure, Finish and
Cleanup retain their existing owner contracts and independent side effects.

After Finish, release validation is a new clean candidate checkout. Use the
exact commands in `release-guru-trellis-version/references/contract.md` and
the live Issue, including focused Fork-backed install/update/reapply and real
changed-file secret scan. Bind every result to one predecessor/candidate pair.
Add one predecessor `v0.6.17-guru.1` existing-install cell for the user's
retired-asset requirement. Compare the predecessor managed Skill inventory
with the candidate registry and inspect the target after update/reapply for
retired Skill/package/command paths. A preserved local edit or unresolved
sidecar blocks that upgrade claim.
Tag, smoke, Release and Issue closure each reread live identity.

## Compatibility

No new public Skill id, exit, schema, or wrapper. Historical docs and tags
are read-only. The Intake correction is additive for unrelated legacy state;
new task identity collision behavior remains fail closed. Full multi-platform
matrix and business production claims remain explicitly unverified.
