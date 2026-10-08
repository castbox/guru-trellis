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

Stable install and upgrade docs must keep four version axes explicit. The official
release target is repository tag `v0.7.0-guru.3`, extension revision
`0.7.0-guru.3`, Fork CLI/core `0.7.0-castbox.3`, source
`castbox/Trellis@5c760463680ffc10a3f26957b330c57a4b0c3ff8`, package manager
`pnpm@10.32.1`, and reviewed Fork CI `37735554354`. These axes are independent;
do not increment the extension or publish an intermediate `.2` tag for this
release. Preparing these docs does not publish the target or pass its candidate gate.
The published Guru predecessor tag is `v0.7.0-guru.1`; its extension revision is
`0.7.0-guru.1`; its historical framework lock is
`castbox/Trellis@9c36002a324c16a09a85b6aa5a380b74aabf801f`, CLI/core `0.7.0-castbox.1`, package
manager `pnpm@10.32.1`. The published predecessor `v0.6.17-guru.2` does not prove
successor framework-source adoption. After the target's publication and remote tag
verification, stable workflow marketplace and preset sources for one installation
use the same immutable `v0.7.0-guru.3` tag. Until then, the target remains an
unreleased candidate and `v0.7.0-guru.1` remains its published predecessor.
Before publication, marketplace and preset use the same addressable full
candidate SHA; an unreleased reviewed checkout is identified as such and never
described as tag-pinned release provenance. Unpinned or branch sources remain
mutable latest/canary inputs.

The released `v0.7.0-guru.1` Fork's update rejects old installations before
accessing legacy project data and preserves that data unchanged. Public docs
must retain that release boundary. The #495 successor candidate defines an
independent explicit migration for all `v0.6.x-guru.*` and
`v0.7.0-guru.*` normal installations, grouped by actual manifest, managed
assets, and task/control differences. The successor release targets are Guru
`0.7.0-guru.3` and CLI/core `0.7.0-castbox.3`; the historical #495 `.3` Fork lock is
`castbox/Trellis@cc5f9a30652be29cffee9acc7e14d5dc5daaf04c`, successful main
CI `37647767799`. Historical same-source Guru acceptance is verified at exact
`ecd152add05dbeb6df1873f0917ca3a62914ca7a` / EVD-051; a later HEAD is not a rerun.
The current #503 Fork lock is
`castbox/Trellis@5c760463680ffc10a3f26957b330c57a4b0c3ff8`, successful main
CI `37735554354`; CLI/core and extension version axes remain unchanged.
The historical `.2` framework lock is
`castbox/Trellis@8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1`, CLI/core
`0.7.0-castbox.2`, package manager `pnpm@10.32.1`, and its extension revision is
the historical unreleased `0.7.0-guru.2` candidate. Read the formal lock from
`trellis/presets/guru-team/source/trellis-source.json`. Formal migration acceptance
requires a remote-addressable full Guru HEAD shared by source-loaded migration,
workflow marketplace and preset provider. Local migration, owner re-entry and
post-write rollback evidence does not prove that same-source acceptance. Ordinary runtime remains
current-only. Do not describe rejection, dirty local builds or a planned
successor tag as fixed-source upgrade/release success.

Current knowledge authority is `current-main-0.6.17-guru.76` / `active`; it is not a
product release axis. Read Requirements/Design/Test through the three layer
READMEs: reviewed #503 identity-responsibility contribution thinly inherits
immutable `.75`, including its historical #495 version-family acceptance.
All normal `v0.6.x-guru.*` / `v0.7.0-guru.*` sources are supported; actual
manifest/ownership/task differences group representative acceptance, not a
version whitelist. Registry remains 35 active Skills / 159 exits / 106 commands,
zero planned ids; business workflow remains 33 invokes / 153 exits.
Architecture `.76` projects ARCH-CUR-049 / ARCH-DOM-034 / ARCH-INT-037 /
ADR-018 / closed ARCH-GAP-012 / EVD-052. EVD-052 proves only #503 source and
representative clean-installed candidate checks; it is not the final #500 Release
gate. ADR-017 owners/current-only/deletion exits
remain effective; its fixed-source restriction is superseded. EVD-049 retains
historical `.73` fixed `6a563f5f` source_locked/provider/inflight evidence and
cannot prove the new Guru source. The unique family Test contribution owns local
representative actual upgrade, custom/current-state preservation, partial
recovery, actual-source rollback and new-work protection. EVD-051 binds exact Guru `ecd152add05dbeb6df1873f0917ca3a62914ca7a` clean remote
source/public/provider/deferred acceptance, G1/native G8 actual-source rollback
and native AGENTS pause-work protection. EVD-050/.74 retains local history;
Issue remains OPEN and downstream merge/Completion/Closure/Finish are separate.
Retain first failures and same-owner recovery; do not claim full-suite pass,
genuine business inflight or GitHub publication from test doubles. Promotion-created
diff requires fresh Phase2/TaskCommit/independent full BranchReview before Delivery;
knowledge promotion does not prove later gates, whole-task Completion, release,
real-business installation or the full cumulative matrix. A later docs-only HEAD
does not become an exact-source rerun merely by inheritance.
Historical pins and retired internal API/lifecycle boundaries remain unchanged.
Manual Git/gh results never backfill Guru gates, transactions or archives.
Native, mock, installed and unverified evidence remain distinct in Test authority.

Prompts in `README.md` are meant to be copied into an AI coding session in a
target business repository. They should tell the AI to:

- read the canonical `trellis/presets/guru-team/source/trellis-source.json`,
  verify its exact `castbox/Trellis` commit and successful local build, and use
  that checkout's normal Node CLI; do not select the original npm distribution,
  global CLI or mutable latest as a fallback. Keep framework commit, CLI version,
  Guru extension revision and historical stable release identity distinct
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
workflow skill root and distinguish registry lifecycle (`planned` versus
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

- ownership schema 4.0 contains exactly 22 platform descriptors, 43 derived
  managed claims, and 22 descriptor-bound additive overlay files;
- ownership rule, claim, and overlay-file cardinalities describe the current
  ownership schema only. They do not define the upstream platform inventory,
  the target repository selected platform set, or the guru-trellis dogfood set;
- the preset never installs or managed-upgrades `trellis-start`,
  `trellis-continue`, `trellis-finish-work`, official hooks, agents, runtime
  agents, bundled skills, or Trellis meta references;
- the overlay tree contains exactly one Guru-owned `guru-finish-work` entry for
  every pinned platform descriptor; each target installs only its exact
  manifest-selected entries;
- current managed upgrades use only the previous managed hash; unknown current
  edits are preserved with `.new`, and no unresolved `.new`/`.bak` may be
  reported as success;
- a fresh target may omit the installed manifest, but any existing manifest
  must satisfy the complete current schema 2.0; non-current inputs fail
  current-contract validation;
- official update/version-upgrade, workflow re-selection, preset reapply, and
  source/installed/ownership/platform/dogfood validation are one documented
  sequence.

All three README files must state that current task identity is TaskId and
lifecycle generation from current task metadata. Path-free session focus or an
explicit TaskId selects the task; TaskBranchBinding owns the branch, and live
registered Git worktree facts resolve the checkout. Ignored runtime mapping and
checkout paths are not task identity or checkout-path authority. They must
document `finish-summary.json` as output of the normal current
`guru-team.finish-work` path only, with no alternate summary command. Public
package documentation keeps live ids such as `invoke-guru-check-task` and
`guru-stage0-*`, and lists only schemas, examples, fixtures, and eval contracts
declared by the live registry and current packages.

Public docs that describe task work commits must name
`guru-create-task-commit` as the active closed-loop owner, distinguish AI review
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
necessity, and re-entry. Public docs state that only current schema 3.0 is
accepted and every other shape fails closed without upgrade or projection. Public docs
also state that equivalent metadata/formatting deltas refresh only directly
affected owner identity, while material authority/scope/design/acceptance
changes rerun their semantic owners.

Public Intake docs name the independent active semantic owners
`guru-create-issue` and `guru-create-task` after
`guru-review-change-request:ready`. The reviewed draft's exact Issue mutation
returns to fresh Sync and Intake; only a separately reviewed existing-Issue or
standalone request can create a task. Before task creation, docs show the exact
TaskId, TaskRef, selected base, branch, checkout and resource ownership, and
obtain current-dialogue confirmation for those side effects. Issue creation and
task creation each retain their own current result recovery and typed exits;
the retired `guru-create-task-workspace` package is not a current route.

Public docs state that `guru-create-task` uses the source-locked Fixed Fork's
official `task.py create --no-start`, then materializes TaskId/source and the
current branch/resource binding. Its public input and official `task.json`
contain no task `creator` or `assignee`, and no login is inferred from GitHub,
Git author, session, or local identity files. A missing session context key
uses explicit-task mode; current schema-2 session binding does not reintroduce
personnel identity. Recovery rereads the exact task and binding without
creating another task or checkout.

Guru install commands and prompts do not initialize or read a developer
identity and do not use `TRELLIS_DEVELOPER`, `TRELLIS_USER`, `-u`, `--user`,
`--creator`, `--assignee`, or `--mine` for task identity or task creation. The
source-locked Fork leaves historical `.trellis/.developer`,
`.trellis/workspace/**`, and `.trellis/agent-traces/**` bytes untouched; normal
Guru runtime does not read, index, copy, migrate, restore, or delete those
roots. Old personnel-bearing task archives retain TaskId for non-reuse and
only the strictly bounded read-only rejection diagnosis; they are not current
lifecycle or Reactivate candidates. Guru resolves a task checkout from its
current TaskBranchBinding and live registered Git worktrees; ignored runtime
state and the retired journal workspace namespace are not checkout-path authority.

Public docs that describe Phase 0 must name `guru-sync-base` as the active
selected-base closed-loop owner, list stable exits `synced` / `skipped` /
`blocked`, and state that the package uses the deterministic schema 1.2 profile
without selected-base or post-execution AI review gates. They must state the
four-level order: explicit, scalar config, first existing ordered candidate
(default `dev`, `develop`, `main`, `master`), then remote default; prohibit
current-branch implicit fallback; require decision/local/remote HEAD equality;
and explain that resolution/result facts stay on stdout, the executor emits a
post-sync resolution digest, and the validator returns that digest only to the
owning public wrapper. The wrapper exports only `base_current`; downstream
Skills never receive the private result, `facts_sha256`, or private result
identity. Each explicit compatibility
`prepare-task` guard consumes its own reviewed provenance before reads or
mutation boundaries. They must not describe
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
selection/deep reads and consistent `mem_review=not_needed`, and the
candidate-present four-source mem insufficiency gate. The current owner result
uses schema `guru-change-context-owner-result-3.0`; active pre-task input is
`guru-stage0-discover-change-context-input-pre-task-2.0`. The 1.0 input and 2.0
owner-result remain immutable legacy bytes outside the active Interface.
Public input and actual Sync `base_current` are independent call-local domains;
Discovery live-reads the authority into owner-private `base_observation` and
never reconstructs a Sync private result, `facts_sha256`, or result identity.
Normal HEAD advance returns
`refresh_base`; invalid authority returns `blocked`. Record/check/public invoke
accept stdin and return stdout, while `context_ready` contains only the route,
mode, target locator, and continuation identity required by Clarify. Normal
pre-task and standalone paths write no task, workspace, or runtime artifact.
Normal mapped active-task invocation carries direct task identity ephemerally,
binds the task branch/current worktree, permits ordinary task edits, and creates
no checkpoint. Stale evidence restarts the complete owner from live authority, and only a
real interrupted active-task recovery may lazily create one ignored current
owner checkpoint that the same owner consumes and removes. They list exits
`context_ready` / `refresh_base` / `blocked` and all three runtime commands.
Docs must not imply that
the Skill chooses duplicate reuse/new target or that a script performs its AI
Review Gate.
Public validation examples use the real Sync wrapper, declared projection,
Discovery wrapper, and Clarify projection through managed Python. A handwritten
private payload, low-level Sync executor, private runtime import, or bare PATH
Python import result is not public-edge evidence.
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
closed current schema `guru-requirements-clarification-2.0`,
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
finalized disposition, live GitHub authority, and one compact owner-result
`decision_trail` containing only `trail_id`, proposal id/digest/decision, and
remote authority kind/URL/content checksum. No task-local Issue classification
aggregate is created; planning/context/review/interrupted/re-entry facts remain
owner-private or are reread from live authority.
Public docs must explicitly forbid persisting user authorization
state, text, refs, timestamps, digests, or process in the clarification result,
runtime, checkpoint, archive, schema, example, or DTO. GitHub authority mutation returns
`refresh_context`; context time must not predate authority time, the task update
binds that digest without a second refresh, and mechanism dispositions require
no trail/mutation before exact progression or a #112 side-effect-free new-task
draft. Inputs must satisfy the current closed schema before normalization; any
mismatch fails closed. Docs also document source-specific
task/GitHub/Git deep-read
locators, structured no-raw-payload persistence, and field-specific
validation. Workflow and stop route markers must
be described as validator-resolved target declarations, not new Skill packages.
Refresh documentation must state that record/check compare caller-authored
current stale codes with live freshness, discard stale owner material, and
require a complete owner rerun from live authority. It must also state that
normal record/check/invoke transport is stdin/stdout and repository-write-free;
active-task identity remains separate from checkpoint persistence, and only a
genuinely interrupted active-task owner with a recovery continuation may lazily create one ignored
same-owner checkpoint, which successful output projection consumes and removes.

When workflow behavior changes, update the docs that users actually read:

Public docs describing Phase 2 must name active semantic Skill
`guru-check-task`, its single `phase2-check.json` artifact, active
`guru-phase2-check-5.0` current-only schema, legacy 4.0 compatibility inventory,
private `guru-phase2-worktree-content-1.0` identity over live tracked and
untracked worktree paths, `phase2_capture_commit`, public
`phase2_commit_anchor`, scope-before-severity rule, full-rerun finding loop,
four exits, and official unchanged `trellis-check` evidence-only role. Phase 2
docs must not claim it consumes the four-stage durable
`guru-reviewed-content-1.0` contract. They must
state that non-current artifact shapes fail current schema validation and must
not claim that coverage flags, successful commands, worker output, or
deterministic scripts can produce Guru pass.
Install/update docs must describe additive registry distribution to the shared
root plus every selected registry-bound native platform root. They must keep
the complete pinned upstream inventory distinct from the target repository's
exact installed selection and from the Claude/Codex/Cursor no-flag default and
guru-trellis dogfood selection.

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
rg "review-branch|finish-work|trellis-start|trellis-continue" README.md trellis/workflows/guru-team/README.md trellis/presets/guru-team/README.md
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
use a caller-selected Interface 1.4 package and explicit external run root; they
use one of the six current production Stage 0 packages. Upgrade text requires
source/installed/platform discovery plus zero-sidecar validation after
update/reapply and does not advertise an alternate contract path.

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
`post_owner` cases reference repo-local checker-passed owner results, while
`semantic_authoring` cases require the Agent to author the call-local result.
Actual exit selects the output schema before expected-exit comparison. Codex
`post_owner` uses the installed runtime's trusted Git root; Codex
`semantic_authoring` uses a repo-external isolated model root with
`--skip-git-repo-check`. Claude uses safe non-interactive input, and
unauthenticated Cursor is `unsupported`.

## Current Intake Contract Documentation

All three public README files name active semantic
`guru-execute-task-free-change`, its `selected_route` and `interaction_resume`
profiles, commands `record-task-free-change` / `check-task-free-change` /
`invoke-guru-execute-task-free-change`, and seven typed exits. They state that
selector `task_free` remains the one-field DTO and reaches the execution Skill
through a target-owned authoring seed; checkout facts never enter the selector.
They also state that `completed` requires AI-authored pre-write suitability,
actual edited paths, a passed targeted check with no failed check, and passed
post-write scope/risk review. Runtime validation cannot create or semantically
approve that evidence. Location and explicit-choice exits self-reenter;
automatic expansion returns to the selector; lifecycle/publication effects stay
unauthorized.

All three public README files describe the live six-package/23-exit Intake
contract, including the dialogue-local pre-recorder stop and optional
`guru-sync-base.repo_root` / `route` scalar arguments. They state that only the
live registry and current package contracts are installed or accepted for
discovery and invocation. The READMEs
also document the package-local discovery/public invocation boundary and the
rule that normal Agents do not read/import the shared Python runtime or receive
private recorder/checker artifacts.
They also document explicit boolean scalar `required`, optional
`guru-sync-base.repo_root`, `base_branch`, and `route` resolver delegation, and the active-task-only null
clarification disposition projection.

Examples use actual production Skill ids and explicit source/installed mode.
Validation text includes manifest/registry/workflow/extension set equality,
six canonical corpora through the existing #147 runner, selected-platform byte
identity, fresh install, current-manifest update, `trellis update`, preset
reapply, existing-task re-entry, archive read-only behavior, and recursive zero
`.new`/`.bak` checks. A non-current installed manifest fails current-contract
validation. README commands must run from a clean repository without
machine-local hidden state.

## Production Current Contract Documentation

All three public README files describe
`trellis/skills/guru-team/contracts/production-current.json` with contract id
`production-current-v4` as the sole current planning/check/commit/qualification
manifest. It contains exactly the current four Skills, 20 profiles, 15 exits,
output schemas, authoring-seed edges, private-artifact ids, examples, production
control, and eval bindings. The READMEs publish only this current manifest and
its declared assets; v2/v3 are immutable legacy assets. Inputs
outside current package schemas fail closed and the owning Skill is rerun from
its current public profile.

The docs show the current Phase 2 `passed` DTO fields `exit_id`, `task_ref`, and
`phase2_commit_anchor`; the current Task Commit `committed` DTO fields
`exit_id`, `task_ref`, `base_ref`, and `branch_review_commit`; and the current Branch
Review seed field `branch_review_commit`. They do not expose private
approval/check/commit/review artifact bodies or present eval `expected_exit` as
a production input.

The docs also name target-owned `skill_input_authoring_seed` for the complete
Interface-declared semantic handoff set, including the production/review/publication,
finalization-family, task-free execution, and archived read-only review edges. They
explain that producer projection supplies only minimal seed fields, the caller
AI authors every remaining required semantic field, validation proves a
disjoint exact required-field partition and a no-overwrite full-schema merge,
and no new projection operation, private-artifact lookup, default, or runtime
semantic reconstruction is introduced.

The public READMEs also describe current active-task recovery as lazy,
owner-private, ignored runtime state created only for a real interrupted owner
consumer. Normal mapped active-task invocation binds its task worktree through
ephemeral identity and creates no checkpoint; stale recovery deletes the
current checkpoint and restarts from live authority; successful public
serialization and terminal paths consume the owner material and remove empty
owner directories. No Discovery artifact locator or supersession history is a
public or durable contract.

Public READMEs describe twenty-six active Skills and 114 external exits, identify
`guru-review-branch` as the Phase 3.5 semantic owner and
`guru-review-task-publication` as the Phase 3.6 semantic owner, and show contract
discovery, public wrapper, eval, fresh install, update and reapply commands.
They show only minimal `exit_id` DTOs and explain that review artifacts remain
private. The three Delivery packages remain workflow-deferred until #434.

They also state that Branch Review `passed` points to active
`guru-review-task-publication` through the target-owned authoring seed. The
Publication AI directly authors and reviews the exact Chinese PR title/body;
its ready 4.0 output projects that payload to active `guru-finalize-task`
through the integrated global invocation without a task-local body or summary
index handoff. `production-current-v4` binds the current
four-Skill/15-exit membership; the complete package handoff set is derived from
the current Interface-declared `skill_input_authoring_seed` edges.

## Task Publication Review Documentation

All three public README files describe active Interface 1.4 semantic
`guru-review-task-publication`, its three target-owned input profiles (two
ordinary profiles plus `archived_publication_review`), runtime
commands `record-task-publication-review` /
`check-task-publication-review`, public dispatcher invocation, and four
minimal exits. They state that `ready` targets active, globally integrated
`guru-finalize-task`;
`return_to_task_work` repeats implementation through Branch Review, and
`blocked` stops. `archived_ready` targets Finalizer's `archived_review_refresh`;
the archived profile returns only `archived_ready|blocked` and never enters
ordinary metadata revision or task-work mutation.

Docs identify ignored-runtime `pr-readiness.json` as the owner-local semantic
gate, with the ordinary `guru-task-publication-readiness-5.0` schema and the
separate `archived-pr-readiness.schema.json` variant. It stores only the reviewed
content identity, exact PR payload, ten semantic dimensions, findings,
conclusions, and route; objective live bindings are rebuilt transiently.
Inputs outside the current schemas fail closed. They do not expose the private
checkpoint or duplicate the package's
ten-dimension review and metadata revision procedure.

The `ready` DTO is exactly `exit_id`, `task_ref`, `branch_review_commit`,
`pr_title`, and `pr_body`. Publication consumes the current Branch Review passed
DTO and live Git only; it never opens Branch Review private checkpoint state.
Docs also state that Finalizer binds the exact payload in its in-memory or
owner-private transaction, derives current finish-summary schema 2 once, keeps
schema 1 history readable, and rejects legacy Publication/Finalizer 3.0 shapes
without fallback.

README package closure numbers are twenty-six active Skills and 114 external exits;
business workflow markers remain 22 invokes, 98 exits, 35 workflow targets, and
24 stop targets. The three Delivery packages remain workflow-deferred until #434;
#436 owns Completion, Closure, Finish, Cleanup, and Reactivate, and the complete
Release matrix remains unverified.
`production-current-v4` owns the current planning/check/commit/qualification
contract; the live Intake contract remains six Skills/23 exits.

## Extension Installation Verification Documentation

All three public README files describe active Interface 1.5 semantic
`guru-verify-extension-installation` as a standalone-only source-repository
package. They name its single `source_repository_verification` input, stable
execute/record/check/invoke commands, and `verified|blocked` exits. They state
that it has no workflow marker, task-bearing profile, `not_required` round,
`return_to_task_work`, Finalizer projection, or task-local artifact.

Docs explain that explicit verification begins from a clean
`castbox/guru-trellis` source checkout. Canonical assets, origin, repo/ref,
resolved commit, HEAD, and clean state are checked before clone, tempdir,
installer, artifact write, or mutation. Non-source and task-bearing calls fail
closed with zero external actions. Successful execution uses a clean throwaway
target and covers marketplace, preset, workflow, platform equality, ownership,
update/reapply, sidecars, README commands, and redaction. Source-session owner
state is ignored runtime and is deleted after direct consumption.

The READMEs also state that a failed compatibility matrix retains a bounded
credential-safe stage/cell/command/exit tail before temporary cleanup. Missing
or malformed matrix terminal output is explicit
`unparseable_failure_output`; command stdout/stderr hashes and sizes remain
supplementary evidence. These facts are standalone-verifier-private and never
enter Finalizer or business closeout DTOs.

Install/update text requires canonical/installed/shared/selected-native-platform byte
identity, source and installed validation, real-wrapper eval, preset reapply
after `trellis update`, dogfood drift, and zero unresolved `.new`/`.bak`. It
distinguishes standalone source verification from business closeout and never
claims that an installed target manifest transfers source verification
responsibility to a business repository.

## Task Finalization Documentation

All three public README files name active Interface 1.4 semantic
`guru-finalize-task`, its five current public input profiles (four ordinary
profiles plus `archived_review_refresh`), six outputs, ordinary gate/transaction
and owner-private recovery, dialogue-local
side-effect confirmation, and deterministic executor. Scripts execute, validate,
and record facts after semantic review; they do not choose plan, scope,
readiness, recovery route, or semantic pass. The archived profile validates
current review and archive continuity without entering a mutation transaction;
it returns only the existing `ready_for_merge|blocked` exits.

The READMEs describe the current package graph as twenty-six active Skills and 114
external exits with the Interface-declared target-owned authoring handoffs. The integrated business
workflow is 22 invokes, 98 exits, 35 workflow targets, and 24 stop targets. The three `guru-finish-work`
entries route Publication -> Finalizer -> Merge only. Publication
`return_to_task_work` remains available for real content drift.

Current Finalizer content push proceeds directly to Draft PR, archive, Ready,
and Merge. It never invokes verifier, emits `verification_required`, accepts a
verification re-entry profile, reads verifier state/ref, or moves a verifier
artifact. Current archive contains exactly five durable core files. Retired
task-bearing verification and task-local plan DTOs, schemas, examples, readers,
and recovery paths are absent from current Interface, manifest, eval, runtime,
and documentation inventories.

The READMEs also explain installed pre-PR provenance reprepare without exposing
private implementation DTOs. The business reviewed checkout owns the target
manifest tail and publication lineage; a separate clean detached extension
source checkout supplies canonical preset bytes. Self-hosted source binds
reviewed HEAD, while installed source binds the current manifest's immutable
canonical repo/ref/commit through exact-OID fetch. The apply executable comes
from source and receives the business checkout through `--repo`; neither the
installed manifest nor this source checkout invokes or substitutes for the
standalone verifier.

The READMEs also name active semantic `guru-merge-task-pr`, its ordinary workflow
and standalone inputs plus read-only `archived_review_request`, five exits,
repo-bound `gh` fact/merge operations,
expected-head precondition, separate merge confirmation, and post-merge
close-keyword verification. `merged` alone reaches the finish response;
`merge_blocked` and `closure_mismatch` stop distinctly;
`phase2_reentry_required` targets the existing archived-task restoration owner.
`review_refresh_required` targets Branch Review's read-only `archived_review`
without selecting a merge. The archived read-only route does not call
Issue-close APIs, update the PR branch, synchronize local `main`, or clean resources.
