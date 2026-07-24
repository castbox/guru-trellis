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

Public docs that describe task work commits must name
`guru-create-task-commit` as the active closed-loop owner, retain
`guru-create-work-commit` only as a reserved tombstone, distinguish AI review
from deterministic candidate/executor checks, and document fresh-sequence
re-entry after finding fixes. Platform entry docs should reference the stable
skill and typed exits instead of repeating its step-local contract.

Public planning docs must name `guru-approve-task-plan` as the only semantic
owner of `planning-approval.json`, schema id `guru-planning-approval-2.0`, and
runtime commands `record-planning-approval` / `check-planning-approval`. They
must distinguish the dedicated unusual-proposal confirmation from ordinary
post-planning confirmation and list the four exits and consumers: `approved`
to `phase-1-task-activation`, `revision_required` to the same Skill,
`clarify_scope` to routing-only workflow target
`guru-task-plan-clarify-scope-router`, and `blocked` to
`task-plan-approval-blocked`. Public docs state that the router consumes only
`exit_id`/`task_ref`/`proposal_refs`, establishes scope context, and mandatory
invokes `guru-clarify-requirements:active_task_scope_change`; the caller AI
authors the complete clarification input from fresh live context. Workflow
prose and platform entry text reference the Skill and route only; the package
contract owns adequacy, provenance, proposal review, Gate, confirmation, and
re-entry. Upgrade docs state that
active schema 1.2 approval requires full v2 re-recording while archives are not
rewritten. Public docs also state that task identity and a scope-ledger
requirement authority use the same issue-category projection, and distinguish
pre-activation invocation-snapshot freshness from allowed post-activation
implementation HEAD/dirty drift. They also state that
`approved_scope_expansion` never accepts a standalone caller-declared digest:
ordinary expansion resolves a controlled current planning-artifact locator,
unusual expansion resolves one canonical candidate, and recorder/checker
recompute the proposal digest and require both the source-appropriate dedicated
confirmation and runtime-materialized current authority SHA-256 to bind that
same digest. An unusual provenance view projects the candidate's existing
confirmation rather than asking twice.

Public Intake docs must name active semantic `guru-create-task-workspace` as
the sole consumer of `guru-review-change-request:ready` and the sole
issue/branch/worktree/task mutation owner. All three README files list its
schemas `guru-task-workspace-plan-1.0` and
`guru-task-workspace-result-1.0`, runtime commands
`record-task-workspace-plan`, `create-task-workspace`, and
`check-task-workspace-result`, and exits `created`, `refresh_review`,
`cancelled`, and `blocked` with unique consumers.

Docs distinguish the two confirmations: a reviewed draft may create only the
exact issue and immediately returns `refresh_review`; the later open-issue
invocation obtains a fresh workspace/task confirmation. They state the fixed
assignee order, the four tracked task-local Intake artifacts, ignored
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
one-question loop, exact action/proposal confirmation, AI-owned GitHub mutation
boundary, stdout-only pre-task result, no dedicated clarification artifact,
schema `guru-requirements-clarification-1.0`, record/check runtime commands,
and exits `clear` / `needs_context` / `refresh_context` / `new_task` /
`blocked` with unique staged consumers. They must state that successful GitHub
mutation returns `refresh_context`, issue creation belongs to #112, and `clear`
uses the caller-aware `guru-requirements-clear-router`: initial/draft still
targets the staged #114 wording route, active-task resumes planning or the
exact interrupted phase, and standalone returns to its caller. Docs also state
that `answered` requires checked evidence, every question id participates in
the reducer lifecycle, and confirmed GitHub payload bytes equal mutation/live
content. For active tasks they must state that `clear`/`new_task` requires a
non-empty terminal proposal set and every five-class scope classification,
regardless of origin, requires exact user-decision evidence; every scope classification
has live GitHub authority and one exact structured
`issue-scope-ledger.json.scope_decisions[]` trail binding planning/review/re-entry
evidence; planning evidence must pass the complete shared
`guru-planning-approval-2.0` validator
rather than a hash/placeholder check; GitHub authority mutation returns
`refresh_context`; context time must not predate authority time, the task update
binds that digest without a second refresh, and mechanism dispositions require
no confirmation/trail/mutation before exact progression or a #112 side-effect-free new-task
draft. Docs also document source-specific task/GitHub/Git deep-read
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
`guru-check-task`, its single `phase2-check.json` / `guru-phase2-check-2.0`
artifact, scope-before-severity rule, full-rerun finding loop, four exits, and
official unchanged `trellis-check` evidence-only role. They must not claim that
coverage flags, successful commands, worker output, or deterministic scripts
can produce Guru pass. Install/update docs must describe additive registry
distribution to shared/Codex/Cursor/Claude roots and explicitly preserve the
upstream ownership inventory.

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
use one of the six production Stage 0 packages after
`stage0-minimal-handoff-v1` activation. Upgrade text states that the separate
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

All three public README files describe the production
`stage0-minimal-handoff-v1` boundary: six Stage 0 packages and 24 exits use
Interface 1.3 `minimal_handoff`. They name the migration manifest, the package-local discovery and
public invocation boundary, and the rule that normal Agents do not read/import
the shared Python runtime or receive private recorder/checker artifacts.
They also document explicit boolean scalar `required`, optional
`guru-sync-base.base_branch` resolver delegation, and the active-task-only null
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
separate atomic unit containing planning, check, and commit with ten profiles
and 11 exits. They state that all ten active packages now use Interface 1.3
`minimal_handoff`, the combined current closure is 10-by-39, and the Stage 0
manifest remains frozen at 6-by-24. They publish discovery, invocation, eval,
pre-#146 upgrade, update/reapply, and drift-validation commands.

The docs show the exact `committed` DTO fields `exit_id`, `task_ref`,
`base_ref`, and `committed_head`, and name active `guru-review-branch` as the
consumer while keeping the #146 committed seed shape unchanged. They state that
#131, rather than #146, activates Branch Review, do not expose private
approval/check/commit/review artifact bodies, and do not present eval
`expected_exit` as a production input.

The docs also name target-owned `skill_input_authoring_seed` for exactly the
planning self-reentry, check-to-commit, commit self-reentry, and
commit-to-review edges. They
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

After #131, public READMEs describe ten active Skills and 39 exits, identify
`guru-review-branch` as the Phase 3.5 semantic owner, and show contract
discovery, public wrapper, eval, fresh install, update and reapply commands.
They show only minimal `exit_id` DTOs and explain that review artifacts remain
private.

They also state that `passed` points to planned
`guru-review-task-publication`; no target schema/profile/authoring contract is
claimed, and invocation fails closed until that package is activated. The
production migration identity and three-Skill/11-exit membership remain
unchanged even though its authoring-seed inventory grows to four.
