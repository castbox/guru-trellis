# Explicit source-loaded installation migration

`judgment_mode=semantic`. This owner has no workflow-mode entry. Initial,
resume and rollback use independent public inputs.
All normal `v0.6.x-guru.*` and `v0.7.0-guru.*` installations are supported
when the selected target is a successor. The installed extension, core, schema
and exact receipt/source bytes determine the migration path, not a revision
whitelist. Public `source_profile` is `guru0.6-family` or `guru0.7.0-family`;
callers of the former fixed `.41` selector must replace it with `guru0.6-family`.
Command/profile/exit ids remain unchanged, and published tags remain immutable.
Old conversion belongs to the formal Fork
migration and this source-loaded package; ordinary update, preset apply and
lifecycle target readers stay current-only. Shared identity inventory may
recognize known legacy headers solely for identity reservation and diagnosis.

The source must contain the target migration package and its complete managed
Python runtime. Bootstrap that source using its canonical bootstrap entry when
necessary. The package wrapper enters its source launcher/resolver; target
`--root` never changes which interpreter or package is loaded. Installed or
platform copies describe the contract, but initial migration requires the
complete target canonical source checkout. Do not patch generated target files,
global npm installations or node_modules to bypass the old-version guard.

## Forward behavior and AI review

1. Read current public profiles and command help. For `initial_upgrade`, obtain
   the exact target source ref and old profile. Run `preview.sh --root TARGET
   --input INPUT` to read old versions, observed provenance, exact managed hashes,
   task field/branch/PR clues, dirty state and registered worktrees. Also inspect
   user config/spec/platform customization, archives and current session facts
   without treating historical personnel or old gates as current authority.
   Read the complete old `.template-hashes.json`, compare it with target
   templates, and explicitly decide remove/preserve for retired receipt-owned
   paths. Current template actions alone are not the old ownership inventory.
   Schema 1.0 receipts can lack package/overlay domains; schema 2.0 receipts
   can lack expanded hashes. Use recorded file hashes first. Resolve missing
   hashes from the observed old source commit and matching formal release
   sources, checking actual extension/core contracts. Early dirty/mutable
   receipts can name an installer predecessor; they are observed facts, not
   invalid installations. The same castbox/guru-trellis repository may use
   HTTPS, SCP-style SSH or ssh:// Git origin forms, with or without .git.
   Never use target source hashes as old hashes. Match
   the actual old bytes against exact old sources; absent/ambiguous provenance
   requires explicit preserve/replace of the actual preimage. Acquire missing
   release objects before the zero-write preview; no network fallback occurs
   inside the executor. A normal core-only update can leave an older core
   requirement in the receipt; preview reports recorded and live cores separately
   and passes the supported live core to Fork migrate. Old asset sources still
   match the receipt's recorded extension/core contract.
   Early upstream-owned overlay claims belong to the Fork
   and cannot be retired by Guru.
2. AI owns every source/field/relationship projection. Preserve legal TaskId,
   initialize missing generation to zero, retire creator/assignee and empty
   subtasks. Supply complete current records to the Fork. Preserve valid
   business fields and relations; use explicit no_issue for non-GitHub sources,
   retaining TAPD/business facts in original description/meta. Missing current
   optional business values use the approved empty/null/P2 defaults; unknown
   creation date is the schema's empty string, never the migration date.
   Unknown fields and nonempty relations require explicit lossless disposition.
   Inventory may contain both valid current and known legacy active records.
   Current tasks go in `core_plan.current_tasks` as `{task_ref,expected_sha256}`
   and preserve raw bytes/modes, id, generation, source, status, relations and
   meta. Do not reconvert them or rebuild valid binding/session/control.
   Select each legacy record for conversion or explicitly defer it using the
   Fork's private `core_plan.deferred_tasks` rows, each containing `task_ref`
   and the exact old raw-byte `expected_sha256`. Converted/deferred refs are
   mutually exclusive. Deferred records retain their original TaskRef and
   bytes; they reserve identity but supply no lifecycle, source, binding,
   session or gate authority. Omitted or unreviewed legacy and malformed current
   records block completion. Final inventory and resume require the exact
   residual legacy refs and hashes to match this reviewed deferred set.
   Diagnose actual PR, merge and old Finish/Finalizer separately from schema
   conversion. Do not turn old publication evidence into a new pass.
3. Build the private plan: `core_plan` is the Fork's exact task/file projection;
   `selected_platforms` is the reviewed installed selection; `guru_decisions`
   contains explicit replace/preserve decisions for local managed edits;
   `workflow` binds the same source ref, action and old bytes; `controls`
   lists actual Git-private state paths that current owners may change.
   `dependency_mode=source_locked` requires the formal fixed Fork dependency.
   `local_candidate` is an isolated development rehearsal only and produces
   an explicit unverified formal-source-lock boundary. It is not release proof.
4. Run preview again with `--plan PLAN --fork FORK_CLI`. AI reviews every write,
   deletion, preservation and per-task re-entry, target identity, actual session
   coordination and preservation/rollback coverage. Show exact source/target,
   commands and paths. Obtain current-dialogue confirmation for the actual
   target write or a real choice. Never serialize authorization or review
   transcripts. Initial pre-write blocking leaves the target untouched.
5. Invoke the public entry with the same `--root`, `--input`, `--plan` and
   `--fork`. Its executor backs up only actual core/Guru/workflow/sidecar/control
   paths, calls formal Fork migrate, then removes exact old Guru-managed files
   under reviewed ownership and removes the old manifest explicitly. It does
   not fabricate a current manifest. Marketplace create-new verifies canonical
   target bytes before force apply; current preset then performs a real fresh
   install and current installed validation. User config and unknown edits are
   preserved; unresolved edits/sidecars produce same-owner resume facts.
   Explicit preserved companion paths pass as a thin executor projection to
   the same preset. Their bytes/modes remain local and leave managed_assets
   ownership; a later ordinary reapply uses that existing provenance to retain
   them and report a canonical conflict proposal rather than overwrite them.
   Package/overlay contracts that require canonical bytes remain conflicts
   until reconciled; preservation cannot fabricate current validation.
   Retire only empty directories left by the reviewed old managed paths;
   retain unknown or preserved content. Validate the actual target through its
   installed runtime before returning `upgraded`; staged validation alone
   cannot establish live installation validity. A failed live check returns
   `resume_required` without weakening the current validator.
   Legal existing config values remain intact; official necessary additive
   config is allowed. Compare historical/business/spec/planning bytes and modes
   explicitly rather than treating an untouched path as migration proof.

## Resume and rollback

`resume_required` carries only `profile=resume` and `recovery_ref` to this
Skill's resume input. Read this owner's private checkpoint to diagnose the
unfinished phase. AI reviews ordinary changed state and any material decision;
automatic mapped resume needs no new permission when already within the exact
confirmed action. Repeat the public entry with the resume input. Core accepts
old or already-converted bytes; a converted task is not converted twice.
Do not retry initial_upgrade after partial writes or regard `.version` alone
as completion. Preserve unknown new bytes and return to fresh inventory/review.
Legitimate new task metadata or control work during a preset pause can survive
resume, because that remaining phase does not rewrite those paths. Such work
can invalidate rollback eligibility even when installation completes. New
valid current tasks are allowed; explicitly deferred old task bytes must remain
exact and their diagnosis cannot be silently omitted.

Rollback is a separately reviewed write using only the recovery reference.
AI first checks whether newer tasks, deliveries, commits or business/control
work exist. The executor compares the refreshed managed baseline and local
business token, plus two fixed rollback-only tokens: converted and explicitly
deferred task content at core completion, and non-preset control content before
the first write. Explicitly preserved core/workflow, companion and retired Guru paths remain user-owned in
the existing fixed business-before comparison; a normal edit during a pause
can survive resume but cannot be overwritten by rollback. Required current package/overlay
reconciliation follows the preset's existing source projection as managed work;
consuming its canonical `.new` alone permits rollback to the old customized preimage.
A failed resume cannot absorb newer deferred notes into rollback
eligibility by refreshing its baseline. Managed
Python pointer paths and aliases are excluded from the latter token. Resume
and baseline refresh never replace these anchors. Older recovery checkpoints
without required anchors are blocked, never silently re-baselined. Newer work
blocks overwrite. Eligible rollback restores backed
up bytes/modes, deletes only the migration's newly created files, restores the
managed-runtime pointer and selected control paths, verifies exact preimages,
and retires the consumed backup. It never resets Git, rewinds commits, deletes
remote PRs or rewrites archives/journals. Run the old runtime smoke and focused
preservation comparisons after actual rollback before returning rolled_back.
Backups after an upgraded result remain private only for this rollback consumer;
they do not grant permission or supply current lifecycle authority.

## Task continuation and typed exits

Installation and task continuation are separate facts. After actual installation,
invoke the existing current branch-establishment → checkout-ensure →
session-binding owners for each selected committed task. Read source authority
and live refs rather than trusting old branch/base/worktree strings. Current
dirty task work is legitimate; do not apply new-checkout clean acquisition to
same-checkout dirty resume. Planning enters fresh current Planning; unpublished
in_progress preserves commits/uncommitted business work and enters fresh
Planning Approval before current development/check. An untracked-only old task
without HEAD identity requires its own current acquisition/binding disposition.
An unrelated known legacy task does not block a valid current target. A direct
legacy target, occupied TaskId/TaskRef or casefold identity collision remains
blocked. Invalid current generation/source, unknown fields, bad JSON and missing
id remain errors rather than being accepted as known legacy. Deferred tasks
receive precise per-task diagnosis and stay outside current lifecycle candidates.
Do not create replacement TaskIds.

Planning continuation requires the real project Architecture baseline, actual
normal-scenario and solution-mechanism qualifications, and AI semantic
Architecture, wording and Planning gates. Recorder/checker/invoke success only
proves objective structure and does not replace these judgments. Preserve the
original planning bytes while establishing the fresh current results.

AI reviews complete actual installation, current owner results, tests and
unverified boundaries before returning one exit. Executor output proves facts,
not this semantic judgment. `upgraded` reports installed version, the rollback
reference and formal dependency boundary to stop `upgrade-installation-upgraded`;
report task-level results in the current conversation. `resume_required` selects
this owner's resume input by the thin profile/reference projection.
`rolled_back` reports the actual before-installation Guru version (never a
fixed `.41`), captured with core/source identity before the first write, to stop
`upgrade-installation-rolled-back`; `blocked` reports a concrete reason to stop
`upgrade-installation-blocked`. Each public field has that direct consumer;
backup rows, old records, complete inventories and business hashes are private.
