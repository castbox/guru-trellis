# Public Documentation

## Audience and Language

Top-level user-facing docs in this repository are primarily Chinese because
the install/upgrade prompts are intended for Guru Team users. Keep command
names, config keys, file paths, GitHub keywords, and Trellis template ids in
English.

Lower-level script comments and Python docstrings may stay English when they
document implementation mechanics.

When public docs describe behavior inside target business repositories, state
the Guru Team default explicitly: `.trellis/spec/**`, `.trellis/tasks/**`,
`docs/**` durable docs, docs SSOT created or completed by
`00-bootstrap-guidelines`, and workflow artifact human-readable fields should be
Chinese. Literal commands, paths, config keys, GitHub keywords, marketplace ids,
and code symbols may remain English. `guru-trellis` itself is a public extension
repository, so public README/source comments/script help/marketplace metadata
may remain English or bilingual when that is clearer.

## Install and Upgrade Prompts

README install docs must provide both:

- a non-interactive command-line installation path for copy/paste or automated
  verification;
- an AI prompt path for users who want Codex, Cursor, or another AI tool to run
  the install, validation, commit, and publish workflow.

Default install commands must not enter the interactive spec template picker.
Use `trellis init -y ... --workflow guru-team --workflow-source ...`, or an
officially supported explicit `--template <name>` path when a specific template
is intended. If docs mention interactive template selection, describe it as an
opt-in user choice, not as the team default or automated validation path.

Stable install and upgrade docs must list the complete current release mapping:
repo release tag, peeled source commit, extension revision, and target official
Trellis CLI. The current mapping is annotated tag `v0.6.5-guru.3`, peeled commit
`dbcbbb2d2776a3952b643b6bcce0a2693d103273`, extension revision
`0.6.5-guru.25`, and target CLI `0.6.5`. Repo release tags and extension
revisions are independent version axes; docs must bind the exact pair instead of
assuming their Guru suffixes match. Workflow marketplace and preset sources must
use the same immutable release tag. Unpinned or branch sources remain mutable
latest/canary inputs and must not be presented as stable release provenance.

Prompts in `README.md` are meant to be copied into an AI coding session in a
target business repository. They should tell the AI to:

- confirm the current `@mindfoldhq/trellis` latest version live, while clearly
  distinguishing it from the pinned official Trellis target used by the current
  Guru Team stable release
- detect conflicting SDD or agent harness frameworks before installing
- use the `guru-team` marketplace workflow source
- apply the preset installer from this public repository
- detect `00-bootstrap-guidelines` after init and explain that spec bootstrap
  is a one-time repo-level task that needs explicit user confirmation before
  AI modifies `.trellis/spec/`
- explain that bootstrap-created `.trellis/spec/**` and docs SSOT content in
  target business repos should use Chinese human-readable prose by default
- keep only selected platform entry directories
- run minimal validation, including `check-env --json`; if `github_repo` cannot
  be inferred, the docs or prompt must tell the user to configure
  `.trellis/guru-team/config.yml` or a GitHub `origin` remote before treating
  GitHub issue intake / publish as ready
- check for secrets before commit
- do Git publishing preflight before pushing or opening a PR

Do not write prompts that assume direct push to protected branches.

Do not write prompts that silently complete spec bootstrap as an install or
upgrade side effect. Installation docs should tell the AI to report the
bootstrap task, explain the intended `.trellis/spec/` changes, and ask whether
to complete it now or leave it for a separate follow-up.

## SSOT Rules

Public docs must identify `trellis/skills/guru-team/` as the only canonical
workflow skill root and distinguish registry lifecycle (`reserved` versus
`active`), package/interface ownership, workflow marker ownership, generated
platform copies, and deterministic script limits. They must state that the
workflow marketplace installs only `.trellis/workflow.md`, while the preset is
the complete Guru Team extension configurator.

Skill ids, external exit ids, registry/interface/schema ids, stable script
commands, and lifecycle states are public APIs. Breaking changes require a new
id or an explicit migration. Upgrade instructions must require workflow and
preset reapply after `trellis update`, resolution of `.new`/`.bak`, and source,
installed, and drift validation before claiming success.

All three public README files must use the same Skill mode/runtime wording:
`workflow` means mandatory global workflow routing, while `standalone` means
direct platform discovery without that routing. Both modes require a complete,
compatible Guru Team preset and shared extension runtime; a Skill directory is
not a self-contained or portable package. The docs must name
`run-skill-command` as the shared dispatcher, describe fail-closed full-preset
install/upgrade remediation, and list its installed executable path.

All three public README files must describe the final ownership boundary:

- the 43 historical upstream paths remain only as
  `upstream_owned/removed` tombstones with immutable path/baseline identity and
  migration-only payload hashes;
- the preset never installs or managed-upgrades `trellis-start`,
  `trellis-continue`, `trellis-finish-work`, official hooks, agents, runtime
  agents, bundled skills, or Trellis meta references;
- the overlay tree contains only the three Guru-owned `guru-finish-work`
  entries;
- known local edits are migrated by provenance, unknown edits are preserved
  with `.new`, and no unresolved `.new`/`.bak` may be reported as success;
- official update/version-upgrade, workflow re-selection, preset reapply, and
  source/installed/ownership/platform/dogfood validation are one documented
  sequence.

Public docs that describe task work commits must name
`guru-create-task-commit` as the active closed-loop owner, retain
`guru-create-work-commit` only as a reserved tombstone, distinguish AI review
from deterministic candidate/executor checks, and document fresh-sequence
re-entry after finding fixes. Platform entry docs should reference the stable
skill and typed exits instead of repeating its step-local contract.

Public planning docs must name `guru-approve-task-plan` as the only semantic
owner of the ignored-runtime `planning-approval.json` checkpoint, schema id
`guru-planning-approval-3.0`, and runtime commands `record-planning-approval` /
`check-planning-approval`. They must state that any necessary task-activation
or scope-choice authorization stays in the current conversation and is not
persisted. They list the four exits and consumers: `approved` to
`phase-1-task-activation`, `revision_required` to the same Skill,
`clarify_scope` to routing-only workflow target
`guru-task-plan-clarify-scope-router`, and `blocked` to
`task-plan-approval-blocked`. Public docs state that the router consumes only
`exit_id`/`task_ref`/`proposal_refs`, establishes scope context, and mandatory
invokes `guru-clarify-requirements:active_task_scope_change`; the caller AI
authors the complete clarification input from fresh live context. Workflow
prose and platform entry text reference the Skill and route only; the package
contract owns adequacy, provenance, unusual-scenario review, authorization
necessity, and re-entry. Upgrade docs state that active schema 1.2/2.0 approval
requires full AI-first re-entry while archives are not rewritten. Public docs
also state that equivalent metadata/formatting deltas refresh only directly
affected owner identity, while material authority/scope/design/acceptance
changes rerun their semantic owners.

Public Intake docs must name active semantic `guru-create-task-workspace` as
the sole consumer of `guru-review-change-request:ready` and the sole
issue/branch/worktree/task mutation owner. All three README files list its
ignored-runtime schemas `guru-task-workspace-plan-2.0` and
`guru-task-workspace-result-2.0`, runtime commands
`record-task-workspace-plan`, `create-task-workspace`, and
`check-task-workspace-result`, and exits `created`, `refresh_review`, and
`blocked` with unique consumers. Refusal stops before recording and returns no
typed exit.

Docs distinguish the two confirmations: a reviewed draft may create only the
exact issue and immediately returns `refresh_review`; the later open-issue
invocation obtains a fresh workspace/task confirmation. They state the fixed
assignee order, the one tracked task-local Issue Scope Ledger, ignored
`.trellis/.runtime/guru-team/**` mappings, exact object reuse/blocking, and the
A/B two-order local merge fixture. `prepare-task` is query-only and its legacy
mutation flags fail closed with migration guidance.

Docs also state that the reviewed-draft GitHub adapter forwards the reviewed
title/body bytes without trimming or appending a newline before the live reread
and created-issue binding check.

They also document retry recovery: before create, exact open-issue
title/body/labels plus creation-at-or-after-plan facts yield a 0/1/>1 decision;
one match is recovered, zero creates once, and multiple block. Complete Intake
re-entry for a workflow-created issue carries the full checker-passed
created-issue result and validates it against the fresh context canonical live
existing-issue identity. That context uses `kind=issue` and null
`issue_binding`; a bare binding digest is not accepted.

Public docs state that the plan binds `post_sync_resolution_sha256` and the
executor reruns the shared resolver/sync core once before the first confirmed
mutation. A fetched remote advance safely refreshes the base but routes to
`refresh_review` before issue/workspace/task mutation; unchanged identity
continues normally.

Public docs state that the workspace executor calls official
`common.task_store.cmd_create` through an isolated adapter, passes the reviewed
assignee explicitly, and disables the developer accessor only for that handler
invocation. They must state that `task.json.creator` and `task.json.assignee`
both equal the reviewed login and that an existing official identity file keeps
its exact bytes.

Guru install commands and prompts do not require a developer name,
`TRELLIS_USER`, `-u`, or `--user`. Public docs accurately state that official
Trellis may independently create/use `.trellis/.developer` and
`.trellis/workspace/**`, while Guru preset apply/update/reapply and the task
workspace executor neither depend on nor create/restore those paths and never
delete existing official data.

Public docs that describe Phase 0 must name `guru-sync-base` as the active
selected-base closed-loop owner, list stable exits `synced` / `skipped` /
`blocked`, and state that the package uses the deterministic schema 1.2 profile
without selected-base or post-execution AI review gates. They must state the
four-level order: explicit, scalar config, first existing ordered candidate
(default `dev`, `develop`, `main`, `master`), then remote default; prohibit
current-branch implicit fallback; require decision/local/remote HEAD equality;
and explain that resolution/result facts stay on stdout, the executor emits a
post-sync resolution digest, the validator passes only that digest forward,
and each `prepare-task` guard consumes the previous post-sync digest and returns
the next one before reads or mutation boundaries. They must not describe
evidence files, leases, release, or cleanup APIs. All three
README files must list the active id, result schema,
runtime commands, full-preset requirement, update/reapply steps, and
missing/drift/sidecar remediation without duplicating the complete Skill loop.

Public Phase 0 docs must also name active semantic
`guru-discover-change-context` as the only `guru-sync-base:synced` consumer.
They state the fixed current-state-before-history order, workflow/standalone
freshness parity, archived `finish-summary.json:index.*`-only reader,
`guru-context-history-score-1.0`, stable query/manifest/preview digests, invalid
isolation, 1-3 candidate deep-read, zero-candidate success with empty
selection/deep reads and consistent `mem_review=not_needed`, candidate-present
four-source mem insufficiency gate, stdout-only pre-task result, and exact
same-snapshot task-local persistence. Public docs distinguish pre-task/
standalone decision-branch binding from direct active task-mode
`task.json.branch` feature-worktree binding at the unchanged snapshot HEAD; all
sync provenance, selected base refs, repository identity, active task and
task-local dirty-scope checks remain mandatory. They list exits `context_ready` / `refresh_base` /
`blocked`, schema `guru-context-discovery-1.0`, all three runtime commands, and
the no-workspace/no-runtime/no-repo-cache boundary. Docs must not imply that
the Skill chooses duplicate reuse/new target or that a script performs its AI
Review Gate.
They also state that duplicate candidate facts are digest-bound to canonical
repo/number/identity/URL/open-state/update-time facts recomputed from the one
duplicate search result without a second search/re-read, and that `blocked` is
valid exactly when the AI Review Gate is blocked. Public examples must not
imply candidate fields or Gate/exit pairs are caller-trusted.
They also identify active semantic `guru-clarify-requirements` as the only
`context_ready` consumer. Public docs describe its initial/active-task/
standalone entry coverage, repository-answerable-before-user-question rule,
one-question loop, current-dialogue action/scope choices, AI-owned GitHub mutation
boundary, stdout-only pre-task result, no dedicated clarification artifact,
active schema `guru-requirements-clarification-2.0`, read-only v1 migration,
record/check runtime commands, and exits `clear` / `needs_context` /
`refresh_context` / `retarget_context` / `new_task` / `blocked` with unique
staged consumers. They must state that successful GitHub
mutation returns `refresh_context`, issue creation belongs to #112, and `clear`
uses the caller-aware `guru-requirements-clear-router`: initial/draft still
targets the staged #114 wording route, active-task resumes planning or the
exact interrupted phase, and standalone returns to its caller. Docs also state
that `answered` requires checked evidence, every question id participates in
the reducer lifecycle, and confirmed GitHub payload bytes equal mutation/live
content. For active tasks they must state that `clear`/`new_task` requires a
non-empty terminal proposal set and every five-class scope classification has a
finalized disposition, live GitHub authority, and one exact compact
`issue-scope-ledger.json.scope_decisions[]` classification containing only
`trail_id`, proposal id/digest/decision, and remote authority kind/URL/content
checksum. Planning/context/review/interrupted/re-entry facts are live or
owner-private checks and must not be copied into the ledger. Public docs must explicitly forbid persisting user authorization
state, text, refs, timestamps, digests, or process in the clarification result,
ledger, runtime, checkpoint, archive, schema, example, or DTO. GitHub authority mutation returns
`refresh_context`; context time must not predate authority time, the task update
binds that digest without a second refresh, and mechanism dispositions require
no trail/mutation before exact progression or a #112 side-effect-free new-task
draft. Legacy full-shape trails are projected once to compact form without a
new user choice or GitHub mutation; partial legacy fields on current shapes fail
closed. Docs also document source-specific task/GitHub/Git deep-read
locators, structured no-raw-payload persistence, and field-specific
validation. Workflow and stop route markers must
be described as validator-resolved target declarations, not new Skill packages.
Refresh documentation must state that record/check compare caller-authored
current stale codes, superseded query/snapshot digests, reason, and detection
time with live freshness, then require complete re-entry from only the current
payload and expected snapshot identity. It must also state that
task-local recorder/checker prove the exact target is not ignored by repository,
`.git/info/exclude`, or global Git exclude rules using `--no-index`, while
pre-task stdout mode does not run that target gate.

When workflow behavior changes, update the docs that users actually read:

Public docs describing Phase 2 must name active semantic Skill
`guru-check-task`, its single `phase2-check.json` artifact, active
`guru-phase2-check-3.0` schema for new records, read-only compatibility for
existing `guru-phase2-check-2.0` artifacts, scope-before-severity rule,
full-rerun finding loop, four exits, and official unchanged `trellis-check`
evidence-only role. They must not claim that coverage flags, successful
commands, worker output, or deterministic scripts can produce Guru pass.
Install/update docs must describe additive registry distribution to
shared/Codex/Cursor/Claude roots and explicitly preserve the upstream ownership
inventory.

- `README.md` for install/upgrade and daily operation
- `trellis/workflows/guru-team/README.md` for marketplace workflow behavior
- `trellis/presets/guru-team/README.md` for installer behavior and installed files

Do not let README instructions contradict the canonical workflow in
`trellis/workflows/guru-team/workflow.md`.

## Safety

Public docs must not include tokens, private repository URLs that reveal
secrets, signed URLs, `.env` contents, database URLs, or raw provider responses.

## Validation

For docs-only changes:

```bash
git diff --check
rg "publish-pr|review-branch|finish-work|trellis-start|trellis-continue" README.md trellis/workflows/guru-team/README.md trellis/presets/guru-team/README.md
```

When docs mention installed files, compare with the actual overlay and managed
asset lists:

```bash
find trellis/presets/guru-team/overlays -type f | sort
rg "MANAGED_ASSET_PATHS|Installed Files" trellis/presets/guru-team trellis/workflows/guru-team
```

## Skill Eval Public Documentation

All three public README files document `discover-skill-evals` and
`run-skill-evals`, schema id `guru-team-skill-evals-1.0`, the four adapter ids,
the four run statuses, repo-external evidence, and the distinction between
deterministic grading, external semantic grading, and human feedback. Examples
use a caller-selected Interface 1.3 package and explicit external run root; they
use one of the six production Stage 0 packages after the frozen
`stage0-minimal-handoff-v1` activation and current
`stage0-ai-first-contract-v2` migration. Upgrade text states that the separate
#146 production unit migrates the three non-Stage-0 packages to Interface 1.3,
and requires source/installed/platform discovery plus zero-sidecar validation
after update/reapply.

The README usage contract also names the four installed executable wrappers,
their `PATH`-resolved native commands, discovery capability reporting, the
shared command requirement, and the repo-external native argv/context/output/
trace transcript. It must not present hidden `GURU_TEAM_*` executable variables
as the adapter implementation.
It also names the closed native trace-helper receipt boundary: trace assertions
are emitted only after a minimal native request, public-only projection, exact
Skill/wrapper digests, exact public-wrapper invocation, and returned output are
bound. Public docs state that the runner reads canonical corpus outside native
execution and native context receives no canonical package/corpus/private
runtime locator. A parseable native DTO without that receipt, or a projection
that exposes eval/private runtime assets, is an `execution_error`; context
construction or wrapper source scanning is not execution evidence.

README eval guidance states that shared uses the preset-managed native executor,
semantic cases reference repo-local checker-passed owner results, actual exit
selects the output schema before expected-exit comparison, Codex uses a trusted
Git root, Claude uses safe non-interactive input, and unauthenticated Cursor is
`unsupported`.

## Stage 0 Minimal Handoff Documentation

All three public README files distinguish the frozen historical
`stage0-minimal-handoff-v1` boundary from the current AI-first contract. The
frozen manifest remains byte-identical at six Stage 0 packages and 24 exits;
`stage0-ai-first-contract-v2` records the current six-package/23-exit contract,
including the dialogue-local pre-recorder stop that replaces `cancelled` and the
`guru-sync-base.repo_root` / `route` required-to-optional scalar migration.
Both use Interface 1.3 `minimal_handoff`. The READMEs name both migration
locators, the package-local discovery and public invocation boundary, and the
rule that normal Agents do not read/import the shared Python runtime or receive
private recorder/checker artifacts.
They also document explicit boolean scalar `required`, optional
`guru-sync-base.repo_root`, `base_branch`, and `route` resolver delegation, and the active-task-only null
clarification disposition projection.

Examples use actual production Skill ids and explicit source/installed mode.
Validation text includes manifest/registry/workflow/extension set equality,
six canonical corpora through the existing #147 runner, selected-platform byte
identity, fresh install, pre-activation upgrade, `trellis update`, preset
reapply, existing-task re-entry, archive read-only behavior, and recursive zero
`.new`/`.bak` checks. README commands must run from a clean repository without
machine-local hidden state.

## Production Minimal Handoff Documentation

All three public README files describe `production-minimal-handoff-v1` as a
separate immutable historical unit containing planning, check, and commit with
ten profiles and 11 exits. They also publish
`production-ai-first-contract-v2` as the current three-Skill migration. It
removes private `approval_ref` / `check_ref` fields from `approved` / `passed`
and moves those two output schemas to v2 without changing v1 bytes. It also
describes the one-time Task Commit projection from legacy message/path/semantic fields into
the five-field v2 owner-entry seed and ignored-runtime candidate, with retired
authorization, caller-selected exit, and terminal result state discarded. They
state that all thirteen active packages use Interface 1.3
`minimal_handoff`, the current package closure is 13-by-51, the integrated global
workflow closure is 13 invokes, 51 exits, and 28 targets, and the Stage 0
manifest remains frozen at 6-by-24. They publish discovery, invocation, eval,
pre-#146 upgrade, update/reapply, and drift-validation commands.

The docs show the exact `committed` DTO fields `exit_id`, `task_ref`,
`base_ref`, and `committed_head`, and name active `guru-review-branch` as the
consumer while keeping the #146 committed seed shape unchanged. They state that
#131, rather than #146, activates Branch Review, do not expose private
approval/check/commit/review artifact bodies, and do not present eval
`expected_exit` as a production input.

The docs also name target-owned `skill_input_authoring_seed` for the complete
set of twelve semantic handoffs: the five production/review/publication edges
and the seven finalization-family edges. They
explain that producer projection supplies only minimal seed fields, the caller
AI authors every remaining required semantic field, validation proves a
disjoint exact required-field partition and a no-overwrite full-schema merge,
and no new projection operation, private-artifact lookup, default, or runtime
semantic reconstruction is introduced.

The public READMEs also describe the compatible active-task context re-entry
contract: exact validated task/snapshot locators, private full dirty-worktree
binding, and exact-prior formal replacement of the fixed snapshot. They state
that the existing target must be regular and trackable, a successful
different-byte replacement records `superseded_snapshot_sha256`, failed
pre-write validation preserves prior bytes, and same-byte retry is idempotent.

Public READMEs describe thirteen active Skills and 51 external exits, identify
`guru-review-branch` as the Phase 3.5 semantic owner and
`guru-review-task-publication` as the Phase 3.6 semantic owner, and show contract
discovery, public wrapper, eval, fresh install, update and reapply commands.
They show only minimal `exit_id` DTOs and explain that review artifacts remain
private.

They also state that Branch Review `passed` points to active
`guru-review-task-publication` through the target-owned authoring seed. The
workflow caller authors initial task-local `pr-body.md` and
`finish-summary-index.json` candidates before invocation without deciding
readiness; publication `ready` points to active `guru-finalize-task` through the
integrated global invocation. The production migration identity and three-Skill/11-exit membership
remain unchanged; the current package graph contains twelve target-owned
authoring handoffs without rewriting that manifest.

## Task Publication Review Documentation

All three public README files describe active Interface 1.3 semantic
`guru-review-task-publication`, its two target-owned input profiles, runtime
commands `record-task-publication-review` /
`check-task-publication-review`, public dispatcher invocation, and three
minimal exits. They state that `ready` targets active, globally integrated
`guru-finalize-task`;
`return_to_task_work` repeats implementation through Branch Review, and
`blocked` stops.

Docs identify ignored-runtime `pr-readiness.json` as the sole semantic gate
under schema `guru-task-publication-readiness-2.0`. It stores only the reviewed
content identity, ten semantic dimensions, findings, conclusions, and route;
objective live bindings are rebuilt transiently and Finalizer-owned publish
inputs do not augment the checkpoint. A legacy deterministic `ready=true`
snapshot cannot pass. They do not expose artifact bodies or duplicate the
package's ten-dimension review and metadata revision procedure.

The `ready` DTO is exactly `exit_id`, `task_ref`, and
`reviewed_content_head`. Publication consumes the current Branch Review passed
DTO and live Git only; it never opens Branch Review private checkpoint state.

README package closure numbers are thirteen active Skills and 51 external exits;
global workflow markers remain 13 invokes, 51 exits, and 28 targets.
The separate
`production-minimal-handoff-v1` remains byte-identical at three Skills/11 exits,
while `production-ai-first-contract-v2` owns the current production projection; the frozen Stage
0 v1 manifest remains six Skills/24 exits while the AI-first v2 contract is six
Skills/23 exits. The #131 `passed` bytes remain unchanged while its target-owned
authoring partition is documented.

## Extension Installation Verification Documentation

All three public README files name active Interface 1.3 semantic
`guru-verify-extension-installation`, its `verification_required` and
`standalone_verification` inputs, runtime commands
`execute-extension-verification`, `record-extension-verification`,
`check-extension-verification`, and `invoke-extension-verification`, and four
minimal exits. They state that workflow `verified` and reachable task-bearing
standalone `not_required` target active `guru-finalize-task`, while the
workflow-shaped not-required schema branch remains compatible but unreachable
from a workflow applicability conflict. `return_to_task_work` repeats Phase 2 and downstream
review, and `blocked` stops.

Docs explain that the package owns applicability, capability profile, adequacy,
findings, and route. Changed paths, successful commands, checker pass, and
production eval are facts only. A workflow-required target cannot silently
return `not_required`; an applicability conflict blocks. #117 owns the target
input contract, and active finalizer producer/consumer edges bind it without
expanding either public DTO. The #119 combined route carries the checker-passed
owner evidence only as a private in-memory finalizer projection through retry,
final projection, normal archive, and active-completed recovery.

The READMEs distinguish task-bearing
`marketplace-verification.json` from taskless session-only owner state, name the
one-artifact/no-cache boundary, and keep private profile/reason/commands/digests/
assets/ownership/findings out of public DTOs. They document full-preset runtime
requirements, source/installed discovery, canonical/installed/shared/Codex/
Cursor/Claude byte identity, update/reapply, ownership freeze, sidecar cleanup,
and redaction.

Public validation text treats package-local real-wrapper production eval and
real pushed-remote clean installation as independent acceptance surfaces. It
must not claim the remote-ref gate passed when only local or public stable
marketplace sampling ran. It identifies local/install combined acceptance
separately from the pushed-remote gate and states that upstream overlay cleanup
is complete only when the 43 tombstones, three-entry overlay tree, migration
matrix, update/upgrade/reapply, and zero-sidecar checks all pass.

Install/update text requires canonical/installed/shared/Codex/Cursor/Claude
byte identity, source and installed validation, real-wrapper eval, workflow
consumer uniqueness, preset reapply after `trellis update`, dogfood drift, and
zero unresolved `.new`/`.bak`. It names the three canonical
`guru-finish-work` platform entries, executes the installed combined integration
suite before and after update/reapply, explicitly leaves pushed-remote branch
verification to the finalization gate, and states that upstream
`trellis-finish-work` files are official Trellis assets outside Guru managed
ownership.

## Task Finalization Documentation

All three public README files name active Interface 1.3 semantic
`guru-finalize-task`, its seven distinct public input profiles, six `exit_id`
outputs, owner-private closeout/gate/recovery facts, current-dialogue side-effect
confirmation without digest recital, and reuse of the existing #105 deterministic transaction engine. They state
that scripts execute, validate, and record only after AI review and any required
human confirmation; scripts do not choose plan, scope, readiness, recovery
route, or semantic pass.
They distinguish the preserved workflow-compatible not-required profile from
the reachable task-bearing standalone #117 edge. That edge publishes only
`repo_ref/resolved_head/verification_ref`; the finalizer target authors
`profile/mode/task_ref`, binds current task-local evidence to the private plan,
and does not expose plan identity in the producer handoff.

The READMEs describe the current package graph as thirteen active Skills and 51
external exits with twelve target-owned `skill_input_authoring_seed` handoffs.
They identify the integrated global workflow projection as 13 invokes, 51 exits,
and 28 targets. They name `guru-finish-work` as the canonical Codex, Claude, and
Cursor finish entry; document the two terminal `published` evals and the private
checked-verification projection; and keep every public DTO unchanged. Official
`trellis-finish-work` payloads remain upstream-owned and are not installed or
managed by the Guru preset.
