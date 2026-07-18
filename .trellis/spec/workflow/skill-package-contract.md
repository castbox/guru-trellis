# Guru Team Workflow Skill Package Contract

## Ownership

`trellis/skills/guru-team/` is the only canonical source for reusable Guru
Team workflow skill packages. The global workflow owns phase order, mandatory
invocation, cross-skill transitions, and typed-exit consumers. Each active
package owns its complete step-local behavior. Installed copies under
`.trellis/guru-team/skills/` and platform skill roots are generated runtime
assets and never become semantic sources of truth.

The workflow marketplace installs `.trellis/workflow.md`; it does not install
external skill packages. The Guru Team preset is the complete extension
configurator and installs active packages after validating the canonical source.

## Registry Lifecycle

`trellis/skills/guru-team/registry.json` is validated by
`schemas/skill-registry.schema.json` and has three states:

- `reserved` claims a stable `guru-<action>-<object>` id only. It has no package,
  route, interface, or platform destination and must never be installed.
- `planned` claims a future stable consumer id only. It has no package,
  interface, invoke marker, exit marker, or platform destination and must never
  be installed. An active Skill may declare a typed exit to that id; callers
  stop at the missing-Skill gate until a later delivery promotes it to a
  complete active package.
- `active` declares a package path, interface path, supported platform targets,
  validator command, and workflow route identity. Every referenced file and
  route must pass source validation before installation.

Activating, renaming, or retiring an id is a public API change. A breaking
change requires a new id or an explicit migration contract. Production
registries must never contain test fixtures.

The task work commit migration keeps `guru-create-work-commit` reserved as a
compatibility tombstone and activates `guru-create-task-commit`. The reserved
reason identifies the active replacement; the old id must never acquire a
different package or route meaning.

## Package And Interface

An active package contains a short `SKILL.md`, `interface.json`, and the
references/scripts/examples/tests declared by its interface. `SKILL.md` starts
with exactly one closed `---` frontmatter block containing only `name` and
`description`. `name` equals the stable `guru-<action>-<object>` id in the
registry and interface; `description` is non-empty and byte-for-byte equal to
the interface description. Missing, duplicated, unclosed, ambiguous, or drifted
frontmatter fails source validation. The Markdown body contains only triggering,
routing, execution entry, and fail-closed rules. Long behavior and authoring
guidance belong in package-local `references/`.

`interface.json` is validated by `schemas/skill-interface.schema.json` and
declares stable identity, workflow and standalone modes, identical entry
preconditions, evidence identity and freshness, `judgment_mode`, ordered stages, artifacts,
schemas, objective validators, external exits, re-entry behavior, tests, and
platform destinations. The stage profile is exact:

1. `semantic`: forward behavior, AI Review Gate, conditional human
   confirmation, deterministic recorder/validator, exactly one typed exit;
2. `deterministic`: forward behavior, deterministic recorder/validator,
   exactly one typed exit.

Only a Skill whose inputs, state transitions, side effects, and pass/block
conditions are completely machine-verifiable may declare `deterministic`, and
only when its boundary contains no scope, sufficiency, finding, revision,
user-choice, or route-intent judgment. Caller-side AI route classification can
precede invocation but is not a Skill-internal post-execution Gate. Any semantic
judgment or human confirmation forces the `semantic` profile.

Every `tests[]` entry is a package-relative `tests/<file>` path. It must be
unique, lexically safe, resolve to an existing regular file below that active
package's `tests/` root, and pass the same component-by-component `lstat`
boundary as other package assets. Labels, missing paths, paths outside
`tests/`, and symlink-backed evidence are invalid. Package tests are part of the
installed/package/platform inventories rather than an untracked assertion.

Workflow and standalone execution use the same preconditions and may reuse
evidence only when its identity and freshness still match. Missing, stale, or
ambiguous evidence fails closed. A deterministic script may execute, record, or
validate machine facts, but never decides scope, sufficiency, findings,
revision action, human-confirmation need, semantic pass, or route intent.

`workflow` and `standalone` are stable routing mode ids, not package formats.
`workflow.routing=global_workflow` means the global workflow loads the package
through its mandatory marker. `standalone.routing=direct_discovery` means a
selected platform may discover and invoke the package without global workflow
routing. Both modes still require the complete, compatible Guru Team preset,
extension runtime, shared dispatcher, companion scripts, installed manifest,
and managed package inventory. `standalone` never means that one copied Skill
directory is self-contained or portable outside that installation.

Every active interface declares the closed `runtime_dependency` object with
extension id, runtime API version, installed manifest path, shared dispatcher
id, preset distribution id, and package portability. Each validator declares a
stable `runtime_command` that the extension manifest publishes. Source and
installed validation bind those fields to the extension capability, and reject
missing fields, wrong routing, dependency drift, unknown commands, or different
workflow/standalone preconditions before a package command can run.

## Workflow Markers And Typed Exits

Mandatory routing is machine-readable HTML-comment JSON:

```markdown
<!-- guru-skill-invoke: {"skill":"guru-example-action","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-example-action","exit":"completed","consumer":{"kind":"workflow","id":"phase-3"}} -->
```

Every active skill has exactly one mandatory invocation identity. Every
external exit has exactly one workflow/skill consumer or one explicit
fail-closed stop. Unknown, duplicate, multiple, or unmapped markers fail source
validation. Reserved ids must not appear in markers. Planned ids may appear
only as a Skill consumer; a planned invoke or exit marker is invalid.
Frontmatter auto-match is discovery assistance only and never replaces
mandatory invocation markers.

`guru-create-task-commit` is mandatory after a fresh final Phase 2 pass and
before every task work stage/commit side effect. It exposes only `committed`,
`revision-required`, and `blocked`: Branch Review/finding closure consumes the
first, the skill re-enters on the second, and the workflow stops on the third.
Finding-fix task work returns through implementation and full Phase 2 before a
new plan sequence may invoke the skill again. Workflow and standalone entry
preconditions include ordinary Git operation state. Gitlink snapshot identity
is conditional on index mode `160000` and binds an initialized, clean worktree
HEAD; for non-deleted gitlinks that artifact HEAD is also the exact index OID,
not a hint for `git add` to reread from the worktree. Ordinary legacy plan
entries do not require gitlink-only or copy-relation fields. New snapshot
producers distinguish rename and copy with mutually exclusive `renamed_from`
and `copied_from`. Only a rename source inherits destination deletion/exact-
stage authority; copy provenance never stages its source, and a dirty copy
source requires an independent classification. Existing SHA-256/mode/delete/
rename facts remain the ordinary exact-index authority for historical plans.
The validated in-memory plan is the only candidate-self byte authority. Executor
staging and hooks run on an isolated index/detached transaction HEAD; only a
fully validated commit/index/result is published. The executor retains the
real Git index lock through conditional ref/candidate publication and rollback,
immediately guards and verifies the conditionally advanced loose ref, uses a
candidate guard plus exact published-result identity for candidate
rollback, keeps `index.lock` as a sentinel while an independent temporary file
publishes the live index, and linearizes success at the final candidate
inode/content identity read after ref/index/result publication. A candidate
writer before that read forces owned ref/index rollback while preserving its
bytes; a writer after it is a preserved later operation and immutable commit
blob/result digest evidence remains committed.
A failed stage, hook, operation, postcondition or publication preserves exact
transaction-owned preimages; loss of conditional ref/candidate ownership
preserves third-party state and fails closed without claiming exact restore.

`guru-sync-base` is mandatory immediately after tool-free Phase 0 request
classification and before the first repo/network semantic read. It declares
`judgment_mode=deterministic`; its workflow and standalone modes have identical
entry preconditions: `runtime_dependency`, `decision_checkout`,
`selected_base_resolution`, `clean_checkout`, and `result_facts`.
Standalone requires an explicit refresh/verify request and cannot return
`skipped`. Workflow exits are exactly `synced` to
`guru-discover-change-context`, `skipped` to `original-request-route`, and
`blocked` to `base-sync-blocked`.

The package declares `sync-base` and `check-base-sync` runtime commands and
schema `guru-base-sync-result-1.0`. Its wrappers remain dispatcher-only. The
caller owns tool-free route classification and standalone intent recognition.
The runtime deterministically selects the first existing configured candidate;
multiple existing candidates follow config order and are not ambiguous.
Resolution/result facts remain on stdout. The executor preserves
`resolution_sha256` as the pre-sync resolve-to-execute identity and emits
`post_sync_resolution` plus `post_sync_resolution_sha256` after synchronization.
`check-base-sync` validates both identities, schema, facts digest, and live Git
equality without mutation, then returns the post-sync digest. `prepare-task`
reuses the same resolver/sync core for its query-only reads and consumes the
current post-sync digest. It has no mutation guard; active workspace mutation
freshness belongs to `guru-create-task-workspace`.

`guru-discover-change-context` is the active semantic consumer of
`guru-sync-base:synced`. Both modes require identical `runtime_dependency`,
`fresh_base`, `repository_identity`, `change_input`, and
`evidence_freshness` preconditions. Its exact semantic stages are the schema
1.2 five-stage profile. The package owns the fixed current-state-before-history
sequence, AI candidate selection/deep-read, AI Review Gate, conditional human
confirmation recorded as not required, same-snapshot recorder/validator, and
the exits `context_ready`, `refresh_base`, and `blocked`.

Its base evidence embeds the complete validator-passed
`guru-base-sync-result-1.0` object rather than a HEAD-only projection. Runtime
validation rechecks the result/schema digests, post-sync resolution, decision
branch, selected remote refs, strict GitHub remote repository identity, and a
fail-closed Git status read before later semantic sources. Pre-task and
standalone validation bind the live checkout to the sync result's decision
branch. Direct active task recording/checking instead binds the live checkout
to `task.json.branch`, because task/worktree creation may move the same HEAD to
a feature branch after the stdout snapshot was reviewed; it still requires the
original HEAD, complete sync provenance, selected local/remote base refs,
repository identity, direct active task locator/status, and task-local-only
dirty paths. A proposed draft
that names a created issue carries a separate live issue binding whose body
digest must equal the original reviewed draft digest. Semantic evidence shape
requires a non-empty mem summary when used and non-empty reviewed scope plus
load-bearing conclusions for a passed AI Gate. A zero-candidate preview fixes
selected/excluded/deep-read evidence to empty and fixes mem review to the
`not_needed` shape, so it cannot reach `trellis mem` or another history source;
candidate previews retain the four-source insufficiency gate. Scripts validate
these shapes but do not supply the judgment.
The live source change may bind an `open` or `closed` issue after normalizing
the supported GitHub state spelling; duplicate candidates and a draft-created
issue binding remain open-only. Current-state evidence that records a Git
object id must resolve `HEAD:<path>` to exactly a blob. A tree, gitlink commit,
tag, missing object, or mismatched blob cannot satisfy the required Docs,
code/contracts, or tests evidence groups.

Duplicate candidate facts are not caller-trusted free-form fields. Their
canonical digest projection is normalized bound `repo`, positive `number`,
`identity=#<number>`, canonical issue URL, `state=open`, and `updated_at`.
Source validation/runtime pure checks recompute that digest, identity, and URL
from the fields returned by the one duplicate search. They do not issue a
second search or re-read candidates after AI review. The package result schema
and runtime also enforce
`typed_exit=blocked` if and only if `ai_review_gate.status=blocked`.

Deep-read shape is source-discriminated: selected archived task artifact,
canonical GitHub issue/PR URL, or exact live Git object/ref. Each locator is
validated by its own closed structural contract, and active-task
`task_branch_stale` remains a normal refreshable complete re-entry reason.

External consumer resolution is part of both source and installed validation.
Skill consumers must name an active or planned registry id. An active consumer
must resolve to its complete installed package; a planned consumer is an
explicit unavailable transition and stops fail closed without fallback.
Workflow/stop consumers must have exactly one matching
`guru-workflow-target` / `guru-stop-target` marker; missing, duplicate,
kind-mismatched, or dangling targets fail closed.

The package publishes artifact schema `guru-context-discovery-1.0`, scoring
algorithm id `guru-context-history-score-1.0`, and dispatcher-only wrappers for
`preview-change-context-history`, `record-context-discovery`, and
`check-context-discovery`. The history command may enumerate only
`.trellis/tasks/archive/**/finish-summary.json` and project only top-level
`index`; it never reads index siblings, workspace/runtime state, or a repo-level
archive index/cache. Scripts validate AI-authored selection and Gate evidence
but do not select candidates, judge sufficiency, decide duplicate reuse, or
synthesize semantic pass.

For `refresh_base`, the result records the current stable stale codes,
superseded query digest, superseded snapshot digest, reason, and detection
time. Recorder/checker compare those caller-authored facts with current live
freshness and require complete skill re-entry. The commands consume only the
current payload and expected snapshot identity; they do not reconstruct an
external ancestry chain.
Task-local record/check also require the exact target to be non-ignored under
`git check-ignore --quiet --no-index --` before and after recording and during
checking. Ignore matches or unreadable trackability fail closed; pre-task mode
remains stdout-only and does not perform this target gate.

`guru-clarify-requirements` is an active semantic package with identical
workflow/standalone preconditions: compatible runtime, current review target,
current context evidence, source authority, and invocation-context freshness.
Its exact schema 1.2 stages are `forward_behavior -> ai_review_gate ->
conditional_human_confirmation -> recorder_validator -> typed_exit`. The Skill
loads `trellis-brainstorm` as its one-question method, but owns question
selection, convergence, scope classification, action selection, confirmation
necessity, semantic pass/block, and typed route.

The result uses closed top-level fields and artifact schema
`guru-requirements-clarification-1.0`. Repository-answerable questions must be
`answered` or `not_answerable` with at least one checked evidence reference
before the first user
question. Each clarification round contains one `question_id`; an
`atomic_group` is permitted only for an indivisible product choice and records
its reason. Every round's `question_id` must be opened in that round or already
open; `answer_status=partial` cannot close any question and therefore cannot
disappear through an empty lifecycle. The reducer keeps exactly
`open_questions = opened - closed`, rejects closing-before-open and reopening
after closure. The recorder
derives all proposal, action, payload, content, and result digests; the checker
recomputes them and validates current live/task facts without generating
questions, choosing actions, classifying scope, executing GitHub writes, or
turning deterministic success into a semantic pass.

Source actions are `none`, `issue_comment`, `issue_body_edit`,
`proposed_draft_update`, `new_issue_draft`, and
`active_task_scope_update`. GitHub mutation remains AI-owned: after exact
action-digest-bound confirmation, the AI uses an existing connector or a
reviewed `gh` command, rereads live facts, and supplies mutation evidence to
the recorder. Checker binds the human-confirmed action payload, canonical
payload digest, mutation result content digest, and reread live body/comment;
any byte mismatch fails closed. Generic continuation, task creation, planning approval, or
review confirmation cannot satisfy action or scope-proposal confirmation.
`unconfirmed_expansion + accepted_current` requires a dedicated
proposal-digest-bound confirmation. A proposal with
`optional_mechanism_origin=true` cannot be `accepted_current`; the mechanism is
removed/replaced or its independent product value is proposed separately.
For an active task, `unconfirmed_expansion` classified as `related`,
`followup`, `new_task`, or `out_of_scope` also requires dedicated
proposal-digest-bound user decision evidence; an AI-only classification is not
a final auditable decision.

The five exits and unique consumers are `clear` -> workflow target
`guru-requirements-clear-router`, `needs_context` -> Skill
`guru-discover-change-context`, `refresh_context` -> Skill `guru-sync-base`,
`new_task` -> workflow target `guru-full-task-intake-chain`, and `blocked` ->
stop `requirements-clarification-blocked`. Active-task `clear`/`new_task`
requires a non-empty terminal proposal set. `clear` requires no open questions,
a passed current AI Gate, current authority/context, every five-class scope
classification exactly confirmed, confirmation-free mechanism dispositions,
and no unrefreshed mutation. A successful GitHub mutation
returns `refresh_context`; a reviewed side-effect-free new issue draft returns
`new_task`; `blocked` is valid if and only if the AI Gate is blocked.

Pre-task and standalone results remain stdout-only. There is no dedicated
tracked clarification artifact. Every five-class active-task classification binds a
structured `decision_trail` that must exactly match one current
`issue-scope-ledger.json.scope_decisions[]` entry. The trail records exact
proposal decisions, user-decision evidence, live GitHub comment/body authority
including `updated_at`, `context_before_task_update_sha256`, all three planning documents, planning
approval, review state, interrupted resume target, stale downstream identities,
and re-entry owners `guru-approve-task-plan`, `guru-check-task`, and
`guru-review-branch`. The active-task checker reuses the shared complete schema
1.2 planning validator and exact-binds reviewed/approved document evidence; a
prior file hash, placeholder planning body, or minimal approval JSON does not
qualify. GitHub authority mutation returns `refresh_context`; only a context
snapshot generated at or after authority `updated_at`, followed by a task update
bound to that snapshot, may later return active-task `clear` or `new_task`.
That `active_task_scope_update` is authorized by the same
`exact_source_action_and_scope` confirmation as the classification proposals:
its action id is listed in `confirmed_actions[]`, and the confirmation action
digest exact-binds the canonical confirmed action set. Proposal-only
confirmation, planning approval, or validated task evidence cannot substitute.
Task-only update requires no second refresh. `mechanism_removed/replaced`
remains outside confirmation/trail/action mutation. `new_task` still contains only the
side-effect-free reviewed draft and #112 owns creation. A copied package without
the complete compatible preset remains non-portable and fails closed through
the dispatcher.

`invocation_context.resume_target` is caller-aware and closed. Initial
issue/draft accepts only `guru-review-contract-wording`; standalone accepts only
`guru-standalone-caller`; active-task accepts the planning-review target or one
of the declared interrupted Phase 1/2/3/Branch Review targets. Accepted-current
scope requires the planning-review target.

`guru-review-contract-wording` is the active semantic owner for controlled
contract wording review. Workflow and standalone modes use identical runtime,
scope, mutation-authority, semantic-evidence, and freshness preconditions. Its
exact schema 1.2 stages are `forward_behavior -> ai_review_gate ->
conditional_human_confirmation -> recorder_validator -> typed_exit`.

The package owns vocabulary `contract-wording-v2`, classification contract
`contract-wording-classifications-v1`, the rewrite/classification/review loop,
profile scope contracts, confirmation policy, artifact schema
`guru-contract-wording-review-1.0`, and exits `pass`, `content_changed`, and
`blocked`. The three profiles are closed: `change_request` always includes
title/body plus AI-selected authoritative comments whose stable identity,
non-empty author, update time, selection reason, and content hash are all
present; `planning_artifacts`
always binds the active task's `prd.md`, `design.md`, and `implement.md` and
requires the canonical contract's exact
`semantic_review.ai_review_gate.planning_checked_dimensions` object before a
successful exit; it writes task-local `contract-wording-review.json`.
`change_request` and `explicit_paths` prohibit that planning-only object, and
`explicit_paths` accepts only
the standalone caller's explicit repo-relative Markdown regular files and is
stdout-only. Workflow callers cannot substitute `explicit_paths` for either
fixed workflow profile.

The deterministic runtime publishes `record-contract-wording-review` and
`check-contract-wording-review`. It builds fixed scope facts, scans current
content, derives identities/digests and unchecked hits, validates schema,
classification/reason structure, freshness, rescan binding, Gate/exit
invariants, exact planning-dimension shape/value, and trackability. It never
chooses scope, rewrite, classification,
reason sufficiency, semantic pass/block, confirmation need, or route intent.
It also never infers or defaults a planning semantic result; only the AI Review
Gate may produce the values required by the canonical package contract.
Every content change invalidates the prior scope/scan identity and requires a
complete rebuild and rescan before evidence can pass.
Task-local evidence replacement uses one objective state transition contract.
Stale evidence requires `--replace-stale`. After the fixed consumer has entered
a complete same-profile re-entry, structurally current `content_changed` or
`blocked` evidence may be superseded only when
`--supersede-reentry-facts-sha256` equals the existing `facts_sha256`; the new
evidence must differ from the old artifact and independently pass full current
validation. The flags are mutually exclusive; identical-result, wrong-profile,
or stale supersession fails closed, and a current `pass` remains protected. The
recorder validates these facts but does not decide that the AI/workflow should
re-enter or which new exit is correct.
For a live issue revision, the recorder derives the exact confirmed-payload
digest from source identity, locator, field, preimage hash, and confirmed
content hash, and derives a mutation-result identity from the current reread
content plus source update time. The checker requires human confirmation to
bind the ordered payload digest set and the mutation result to equal the
rebuilt live scope. This is deterministic normal-flow consistency evidence,
not an authenticity, hostile-input, locking, or TOCTOU boundary.

Unique consumers are `pass` -> workflow target
`guru-contract-wording-pass-router`, `content_changed` -> workflow target
`guru-contract-wording-change-router`, and `blocked` -> stop
`contract-wording-blocked`. Those routers use only the checker-validated
profile and exit. Unknown, multiple, stale, or unmapped profile/exit evidence
fails closed. Planning approval is only a consumer/projection of current
`planning_artifacts:pass` evidence and cannot become a second vocabulary,
classification, scanner, or semantic-review owner.
Its compatibility projection copies each already-validated planning dimension
from that evidence. Planning evidence recorded before the planning-only field
existed is stale even with schema id `guru-contract-wording-review-1.0`; active
tasks must perform a complete fresh AI review, display all three planning
documents again, and obtain fresh post-planning confirmation. Missing booleans
must never be patched into old evidence, while archived artifacts remain
historical.

## Change Request Readiness Package

Active semantic Skill `guru-review-change-request` is the sole pre-task
readiness owner after `guru-review-contract-wording:change_request:pass`. It
consumes current context, clarification, and wording results; normalizes one
`existing_issue`, `proposed_draft`, or `standalone_request`; reviews the fixed
ten dimensions; records findings, scope conclusion, AI Review Gate, optional
confirmation, and exactly one exit. Its exits are `ready` -> active
`guru-create-task-workspace`, `clarify_requirements` ->
`guru-clarify-requirements`, `review_wording` ->
`guru-review-contract-wording`, `refresh_context` -> `guru-sync-base`, and
`blocked` -> stop `change-request-review-blocked`.

The record/check commands are stdout-only before task creation. They reuse the
existing objective context, clarification, and wording validators; project
portable hashes and error codes; rebuild target/linkage/facts digests; and
validate closed schema, fixed dimensions/findings references, Gate/exit
invariants, consumer identity, and freshness. They never search history or
duplicates, read Docs/code/tests for semantic judgment, generate findings,
select a delivery unit, infer a Gate, or map objective error codes to an exit.
For a proposed draft or standalone request they derive `source_request_sha256`
from #113's exact draft authority projection: `kind=draft`, normalized repo,
null issue/URL/update authority, `state=draft`, and current reviewed-body
SHA-256. Title hash and draft/request/caller identity stay separately bound.
An arbitrary 64-hex value, including a normal producer's stale prior digest,
fails closed before prerequisite linkage is accepted.
Only the active `guru-create-task-workspace` package may persist the exact
checker-passed bytes as task-local `issue-review.json` while creating the
workspace. `ready` has no legacy prepare fallback.

## Task Workspace Package

Active semantic Skill `guru-create-task-workspace` is the sole owner of GitHub
issue creation and branch/worktree/task creation after change-request
readiness. Workflow and standalone modes use identical `runtime_dependency`,
`base_evidence`, `context_evidence`, `clarity_evidence`, `wording_evidence`,
`readiness_evidence`, `target_authority`, `naming_and_assignee`,
`side_effect_authorization`, and `invocation_freshness` preconditions. Its
exact stages are `forward_behavior -> ai_review_gate ->
conditional_human_confirmation -> recorder_validator -> typed_exit`.

The package owns target presentation, semantic naming, assignee routing, exact
side-effect plan, two mutually exclusive confirmation scopes, AI Review Gate,
ordinary recovery disposition, and typed route. Runtime commands are
`record-task-workspace-plan`, `create-task-workspace`, and
`check-task-workspace-result`; artifact schemas are
`guru-task-workspace-plan-1.0` and `guru-task-workspace-result-1.0`. Recorder,
executor, and checker validate deterministic facts only and never select a
duplicate, target, closed-state disposition, semantic name, assignee route,
confirmation need, Gate status, or exit intent.

A reviewed-draft invocation may only create the exact confirmed issue. Before
create, it searches live open issues for the exact reviewed title, body,
labels, and a creation time not earlier than the reviewed plan. Zero matches
permits one create, one match is recovered and reread, and multiple matches
fail closed. It binds the live title/body/update facts to the reviewed draft
and confirmation, returns `refresh_review`, and performs no
branch/worktree/task/runtime mutation. An open-issue invocation uses a separate
`workspace_and_task_mutation` confirmation and may return `created` only after
the branch/worktree/task, four tracked task-local Intake artifacts, ignored
runtime mappings, and workspace boundary all pass objective validation.
The non-mutation matrix is equally explicit: passed Gate plus a digest-bound
`refused` active confirmation yields `cancelled`; `reroute` with no active
confirmation yields `refresh_review`; `blocked` with no active confirmation
yields `blocked`. Runtime preserves these AI-authored facts and may mutate only
for passed plus confirmed.

An open-issue plan that continues a workflow-created draft embeds the complete
prior checker-passed `created_issue` result and its binding digest. The result
facts digest, binding facts digest, reviewed draft id/digest, creation
confirmation digest, current issue authority, and complete Intake rerun's live
existing-issue identity must all agree. The fresh context is `kind=issue` with
canonical URL/open state/update time/body/facts identity and null
`issue_binding`. Ordinary existing issues carry null result and binding fields;
missing, partial, or mixed provenance fails closed.

The plan also binds the checker-passed base result's
`post_sync_resolution_sha256`. Before the first GitHub issue or workspace/task
mutation, the executor runs the shared resolver and sync core once. The fresh
selected base, refs, decision/local/remote HEADs, and post-sync identity must
equal the reviewed plan. A normal remote advance may be fetched and safely
fast-forwarded, but it returns `refresh_review` before issue, branch, worktree,
task, artifact, or runtime mutation because the reviewed base identity changed.

Assignee resolution order is explicit input, exactly one issue assignee, zero
issue assignees to current GitHub login, then an AI/user choice for multiple or
unresolved candidates. In an isolated subprocess, the exact executor calls
official `common.task_store.cmd_create` with the resolved assignee and replaces
that module's developer accessor with a null result only for the handler
invocation. The official fallback therefore writes
`task.json.creator=task.json.assignee=<reviewed-login>` without reading or
rewriting `.trellis/.developer`. The executor never copies, initializes, or
restores `.trellis/.developer` or `.trellis/workspace/**`; existing official
identity/journal bytes are outside this package and remain unchanged.

External exits are exactly `created` to workflow target
`guru-task-workspace-created`, `refresh_review` to active Skill
`guru-sync-base`, `cancelled` to stop `task-workspace-cancelled`, and `blocked`
to stop `task-workspace-blocked`. A target/disposition change is
`refresh_review` with zero writes. Unknown, multiple, unmapped, stale, or
consumer-mismatched exits fail closed.
Public plan/result stdout and examples contain no absolute workspace path; the
checker derives the expected worktree from current repo config, reviewed slug,
and live Git facts. Absolute mappings stay only in ignored runtime files.

## Distribution And Managed Hashes

The preset installs an audited canonical registry/schema/package copy under
`.trellis/guru-team/skills/`, then distributes each active package to
`.agents/skills/<id>/` and only the selected platform roots:
`.codex/skills/<id>/`, `.cursor/skills/<id>/`, and
`.claude/skills/<id>/`. Unselected roots are not created.

Every distributed file uses exact previous managed hashes, never overlay
content heuristics:

| Target state | Result |
| --- | --- |
| missing | install canonical bytes and record the hash |
| equals canonical | unchanged; refresh deterministic provenance |
| differs, but equals the previous managed hash | write `.bak`, then install the new canonical bytes |
| unknown local edit | preserve target, write canonical bytes to `.new`, fail closed |
| missing or invalid provenance with different bytes | preserve target, write `.new` or fail before mutation |

The installed manifest binds registry digest/schema version, reserved and
active ids, selected platforms, package/interface/tree digests, each installed
repo-relative path, file digest, executable bit, managed removals, conflicts,
and sidecar outcome. `files[]` is the complete current managed-file inventory;
`removals[]` records previous-managed paths removed during platform shrink;
`conflicts[]` records preserved paths plus explicit remediation; and
`sidecars[]` exactly equals the `.new`/`.bak` files on disk. A manifest with an
unresolved conflict or sidecar has `status=conflict`, never `ok`. It never stores
an absolute local path.

A conflict manifest is reusable as previous managed provenance only for the
deterministic known-upgrade recovery state: `conflicts[]` is empty, every
declared sidecar is a unique repo-relative `.bak` adjacent to a current
`files[]` path, and every still-present sidecar is a regular file behind a
non-symlink path. Reapply preserves the remaining `.bak` inventory and stays
blocked; after all declared backups are removed, the next reapply may return
`status=ok`. A `.new`, semantic conflict, malformed path, unbound backup, or
non-regular sidecar never enters this recovery path and invalidates previous
provenance.

Every source, installed, platform, target, and sidecar path is lexically bound
to the repository. Before any read, write, removal, chmod, or digest, the
installer/validator walks every component with `lstat`. A regular, dangling,
internal, external, or multilevel symlink at the target or any ancestor fails
closed; no asset may be read from or written through it.

Package command files are thin wrappers. They locate only the managed
`run-skill-command` dispatcher, pass their package root and fixed validator id,
and forward the original arguments. They must not locate an old companion
command directly, parse task/gate evidence, validate commit messages, stage Git
content, or implement transaction/rollback behavior. Missing or incompatible
runtime state fails before the target companion command and reports that the
package is not self-contained/portable, that the complete Guru Team preset must
be installed or upgraded, and that unresolved `.new` / `.bak` sidecars and
source/installed validation must be handled before retry.

## Deterministic Validation

The stable command is:

```bash
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
```

`source` binds the canonical registry/interface Draft 2020-12 schemas by exact
dialect, schema id, and contract digest, then applies every declared constraint
to production and fixture instances. It also validates ids, paths, required
package files, parseable package-local artifact schemas, safe existing
artifact/schema/validator/test files, strict `SKILL.md` discovery frontmatter,
workflow markers, and unique exit mappings.
Every untrusted JSON value is type-checked before set, hash, path, or string
operations; malformed values return structured `failed` errors without a Python
traceback. `installed` validates manifest provenance, selected roots, installed
file/package inventory, hashes and modes, reserved absence, unexpected or
unknown platform copies, drift, and declared-versus-actual `.new`/`.bak` files.
Both modes report objective facts and fail with
non-zero status on structural errors; neither substitutes for an AI review.

## Upgrade, Test, And Safety Contract

After `trellis update`, reapply the selected marketplace workflow, reapply the
Guru Team preset, resolve every `.new`/`.bak`, and rerun source, installed, and
dogfood drift validation. Tests must cover registry/interface failures,
missing/reserved/unknown/multiple/unmapped routes, schema and provenance
failure, every managed-hash transition, platform selection, fixture discovery,
and clean throwaway update/reapply.

Public packages, fixtures, manifests, and examples must not contain active task
state, workspace journals, platform prompts, project-private data, secrets,
signed URLs, `.env` values, or machine-specific absolute paths.
