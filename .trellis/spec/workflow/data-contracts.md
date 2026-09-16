# Data Contracts

## Configuration

`trellis/workflows/guru-team/config-template.yml` is the reusable default
configuration. `.trellis/guru-team/config.yml` is a target repository's local
copy and must be preserved by the preset installer.

When adding a config field:

1. Add the default only to the package-local runtime or shared utility that
   directly consumes the field; do not create a cross-Skill aggregate config owner.
2. Document the field in `trellis/workflows/guru-team/config-template.yml`.
3. Define each field's current omission behavior explicitly: either a current
   default or a required-field error, without a version-specific reader.
4. Decide whether the preset installer needs current preservation behavior.
5. Update README or workflow text if users must know the field.

Selected-base resolution uses one fixed precedence: explicit `--base`, non-empty
scalar `base_branch`, the first existing exact local or remote-tracking ref in
deduplicated `base_branch_candidates` order, then remote default when no
configured candidate exists. The candidate default is `dev`, `develop`, `main`,
`master`. A one-value candidate list still records `source=config-candidate`;
it is not scalar config. Empty scalar means not configured, multiple existing
candidates follow declared order rather than creating ambiguity, and no config
shape authorizes a current-branch fallback. Resolver validation is lazy by
precedence: selected explicit input is not rejected by malformed lower-priority
scalar/candidate config, and selected scalar input is not rejected by malformed
candidate config. When neither source is selected, candidate shape and branch
validation fail closed before candidate or remote-default facts are produced.

## Base Sync Result

Schema `guru-base-sync-result-1.0` is a closed Draft 2020-12 object for a
successful `guru-sync-base` execution. It records stable skill/status identity,
resolution source/base/remote/candidates and pre-sync resolution digest,
decision checkout branch/HEAD/clean before and after, local and remote
refs/HEADs, fetch and fast-forward facts, the complete synchronized
`post_sync_resolution` with `post_sync_resolution_sha256`, `fresh=true`, and
`facts_sha256`. The facts digest is SHA-256 over canonical JSON with
`facts_sha256` omitted.

Success requires full 40-hex commit ids and exact equality across decision
checkout HEAD after, local base HEAD after, and remote-tracking base HEAD.
Resolution and result facts are canonical JSON transported on stdout only.
No task artifact, public package, installed runtime, repo root, or repo-external
temporary file stores them. The pre-sync digest binds only
resolve-to-execute. `check-base-sync --result-json` validates schema, facts
digest, both resolution identities, and stale live Git facts, then returns the
post-sync digest to the owning public wrapper. That wrapper projects only the
declared `base_current`; no downstream consumer receives or reconstructs the
private result. Already-equal execution may have equal
pre/post digests; fast-forward execution must not.
Workflow and standalone create no evidence file, lease, release command or
cleanup state.

### Phase 0 Current Transition Family

Active-task routing consumes only a closed identity across `task.json`, the
task branch/worktree, live requirement authority, and Guru runtime mappings. A
missing, conflicting, or stale relation is represented as `invalid_task_state`;
session pointers remain locators and are not task authority.

The workflow-owned `guru-stage0-transition-1.0` family consists of five
independent closed schemas. They are lifecycle stages, not one nullable mega
object:

| Stage | Required current projection | Unique consumer |
| --- | --- | --- |
| `base_current` | transition/mode/repository identity plus source-preserving base provenance | `guru-discover-change-context` |
| `context_current` | current base identity, target locator, context continuation and authoritative-content freshness | `guru-clarify-requirements` |
| `clarity_current` | current context identity, target disposition, scope/authority content identity and clarity checker token | `guru-review-contract-wording` |
| `wording_current` | current clarity identity, fixed wording profile, target content identity and wording checker token | `guru-review-change-request` |
| `readiness_current` | current wording identity, ready scope projection, target/content/linkage identity | `guru-create-task-workspace` |

The base provenance is a closed source-preserving value containing resolution
source, selected base, remote, ordered candidates, decision HEAD, local base
HEAD, remote base HEAD, and `post_sync_resolution_sha256`. These HEAD roles are
distinct contract fields and must not be folded into one generic `base_head`.
It preserves an explicit selection as explicit when a later compatibility
caller omits a CLI base; it does not rerun fallback precedence and relabel the
source as `config-candidate`. Discovery receives this `base_current` separately
from its own caller-authored public input and compares the public identity with
live Git before any semantic authority read. It never receives
`guru-base-sync-result-1.0`, its facts digest, or a reconstruction of either.

Each later stage contains only the prior identity plus fields directly consumed
by its next checker. Complete issue bodies, scan or review history, findings,
owner results, artifact locators, file metadata, process/reviewer data, and
authorization are forbidden. Successful consumption retires the prior in-memory
stage; refresh/re-entry discards stale state and starts from a fresh
`base_current`. Normal pre-task transport is stdin/stdout or caller memory only
and writes nothing below `.trellis/tasks/**`, `.trellis/workspace/**`, or
`.trellis/.runtime/**`.

For `guru-review-contract-wording:change_request:pass`, the checked wording
scope contains exactly one title item and one body item. The producer sets both
the top-level and nested `wording_current` target content fields to the canonical
JSON digest of `{"title_sha256": <title item content SHA-256>,
"body_sha256": <body item content SHA-256>}`. Missing or duplicate title/body
items fail closed before transition projection. Change-request readiness uses
that public transition value directly for its current-content linkage; it does
not read or recompute identity from the wording owner's private scope.

The invocation contract uses separate closed call-local envelopes for
deterministic sync, semantic owner invocation, and confirmed workspace
mutation. Semantic transport has three distinct domains: caller-owned public
input, exactly one current transition stage, and the current Skill's checked
owner result. That result is never a public DTO or a cross-Skill transition.
Unknown fields, missing or wrong stages, owner/input/target mismatch, stale
identity, or multiple operations fail closed.

For the active Discovery pre-task profile, caller-owned input is
`guru-stage0-discover-change-context-input-pre-task-2.0`. It contains only the
profile, source exit, mode, closed change clues, and caller continuation; repo
and base authority remain exclusively in the independent `base_current` stage.
The published 1.0 pre-task input remains an immutable legacy asset and is not
selected by the current Interface.

`prepare-task.base_freshness` is the current query projection and
adds pre-sync resolution source/digest, post-sync resolution/digest, decision
checkout, local/remote refs, and three-way equality facts from the same core.
It also exposes `reviewed_resolution_sha256` as the digest consumed by the
current guard and `post_sync_resolution_sha256` as the digest to pass to the
next guard, while `resolution.source` remains the
`explicit`, `config`, `config-candidate`, or `remote-default` provenance rather than a
prepare-generated explicit override. No task artifact persists the complete
base resolution/result payload, process output, or machine path. Current task
identity comes from official `task.json`, ignored runtime mapping, and live Git
worktree facts.

`prepare-task` is compatibility-only and never produces a current transition.
An explicit call must receive the complete reviewed base provenance above.
It supplies that exact `base_current.base` object as one JSON scalar through
`--reviewed-base-provenance`; the value is not a file locator. Optional
`--base-branch` only asserts selected-base equality and cannot rebuild source.
Missing provenance returns the stable local diagnostic
`missing_reviewed_base_provenance`; changed provenance/state returns a stable
base-provenance or base-state diagnostic. Both stop before GitHub reads, fetch,
duplicate search, or semantic Intake. A digest alone cannot reconstruct the
resolution source or ordered candidates. Whether a missing remote ref is legal
for a particular query state is defined by the formal closed schema/runtime
status matrix; callers must not infer a nullable fallback or synthesize a remote
HEAD.

The YAML parser in `load_config()` is intentionally small. It supports simple
scalars, lists, and one level of nested dictionaries used by the current config.
Do not introduce complex YAML structures without replacing or extending the
parser and validating older configs.

## Change Context Discovery Result

Schema `guru-change-context-owner-result-3.0` is the active closed Draft 2020-12
stdout-only owner-result union whose `typed_exit` is exactly `context_ready`,
`refresh_base`, or `blocked`. It contains Discovery-owned live
`base_observation` and current semantic evidence needed by the same owner loop,
but it is neither a
public handoff nor a tracked task artifact. Normal workflow and standalone
execution transport the result through stdin/stdout and create no task,
workspace, or ignored runtime file.
The published owner-result 2.0 schema/example remain immutable legacy assets;
the active Interface, recorder, checker, examples, and evals select 3.0 only.
They do not accept, synthesize, or digest a Sync private result.
The normalized `change_input` object contains the same ten clue-array kinds as
the canonical query source and requires at least one non-empty array in both the
published schema and runtime precondition gate. Neither `issue_binding` nor a
separately populated `canonical_query` counts as change input.
An issue used as the source change may be live `open` or `closed`; the runtime
normalizes the exact supported GitHub state spelling to lowercase before
binding it. This does not weaken the independently open-only duplicate search
or the open-only issue binding created from a reviewed draft.

Each duplicate candidate is a closed object whose deterministic fact
projection is exactly normalized bound `repo`, positive `number`,
`identity=#<number>`, canonical issue `url`, `state=open`, and `updated_at`.
`facts_sha256` is SHA-256 over the canonical JSON projection and excludes
AI-authored `reason` / `observation`. Pure validation recomputes the digest,
identity, and canonical URL from those returned fields. Recorder/checker do not
issue a second duplicate search or re-read candidates after AI review.

A proposed draft keeps its original body and facts digest. When its normalized
change input contains a created issue ref, `live_change.issue_binding` is
required and binds repo, number, canonical URL, state, update time, body digest,
and live facts digest. Recorder/checker must read that exact issue and prove the
live body digest equals the reviewed draft body digest. A missing, mismatched,
or unreadable binding fails closed; no issue ref requires a null binding and no
GitHub read.

Canonical query arrays are `issue_refs`, `pr_refs`, `branches`, `paths`,
`commands`, `config_keys`, `schema_fields`, `symbols`, `terms`, `queries`, and
derived `tokens`. Text uses NFKC, casefold, trimmed/collapsed whitespace and
byte-sorted deduplication; path exact identity preserves case/punctuation and
rejects absolute, parent-traversal, and protected paths. The
newline-terminated compact sorted-key JSON digest is `query_sha256`.

History algorithm `guru-context-history-score-1.0` enumerates only
`.trellis/tasks/archive/**/finish-summary.json`, applies lexical repository and
archive containment, and classifies ordinary non-file/read/JSON/index-shape
failures as portable invalid rows. It parses only top-level `index` and never
consumes sibling fields. Exact weights are issue 1000, PR 900, branch 800, path
700, command/config/schema/symbol 600, term 400 and query 300. Token points
equal `min(99, unique query tokens present)`. Sort is total score, exact count
and token count descending, then summary path UTF-8 bytes ascending; only
positive-score first 20 rows are projected.

Manifest rows are path-sorted `{path,status,index_sha256}` valid facts or
`{path,status,error_code}` invalid facts. Invalid rows are isolated from valid
scoring and never contain raw exceptions/content or absolute paths.
`archive_manifest_sha256` covers all manifest rows; `preview_sha256` binds
algorithm, query, manifest, limit, candidate projections and invalid rows.

When candidates exist, AI history review selects one to three and gives every
unselected candidate an exclusion reason. A zero-candidate preview requires an
empty selected/excluded partition, empty deep reads, and
`mem_review.status=not_needed`; its load-bearing question and summary are null
and every exhausted-source flag is false. It remains successful and cannot
trigger `trellis mem` or any substitute history source. For a candidate preview,
`mem_review.status=used` is valid only when task artifacts, current
Docs/code/tests, GitHub and Git history are each recorded insufficient for one
named load-bearing question and `summary` is a non-empty conclusion; otherwise
status is the same consistent `not_needed` shape. A passed AI Review Gate
requires at least one reviewed-scope row and at least one evidence-bound
load-bearing conclusion. These are structural completeness checks only; scripts
do not author or judge the semantic content.

The exit/Gate matrix is biconditional: `typed_exit=blocked` if and only if
`ai_review_gate.status=blocked`. Both the published schema and runtime reject a
passed Gate carried by `blocked` and a blocked Gate carried by any other exit.

Each deep read uses a source-discriminated locator: `task_artifact` is a
repo-relative regular file inside the selected archived task, `github` is a
canonical GitHub issue/PR URL without query/fragment, and `git` is an exact
`git:object:<oid>` or `git:ref:<full-ref>@<oid>` identity validated against live
Git. The schema and runtime both reject cross-kind locator substitution.

Record and check accept the same owner result from stdin or an explicit file,
validate schema, Discovery-owned base observation, live facts, semantic
digests, and reviewed blob identities, and
return canonical JSON or an objective checked exit on stdout. They never
resolve, write, replace, or supersede a task artifact. A base error
short-circuits before live issue/draft, reviewed-blob, or archive-preview reads;
normal local/remote HEAD advance or stale public HEAD returns `refresh_base`,
while dirty, wrong-branch/ref, missing, ambiguous, repo-mismatched, or
structurally invalid authority returns `blocked`. Neither route reconstructs a
private Sync result. Stale evidence reruns the complete owner from live
authority without a prior result chain.

Every 40-character reviewed Git identity is resolved again from `HEAD:<path>`
and its object type must be exactly `blob`. A tree, gitlink commit, tag,
missing object, or mismatched blob cannot satisfy any Docs, code/contracts, or
tests evidence group; 64-character content evidence retains its exact byte
digest freshness check.
The same stale evidence rejects `context_ready`. Its public DTO contains only
`exit_id`, `handoff_profile`, `handoff_mode`, `handoff_target_locator`, and
`handoff_continuation_id`; Clarification rereads current authority and never
receives an owner-result locator.

Active-task invocation identity is transported ephemerally and independently
from persistence. Normal mapped active-task record/check/invoke binds the
direct task branch, current task worktree, and fresh selected-base refs while
allowing ordinary worktree edits and creates no checkpoint. Only a genuinely
interrupted active-task owner loop with an explicit recovery continuation may
lazily create one current ignored checkpoint below the existing
owner-checkpoint namespace. It
stores only task identity and non-reconstructable same-owner semantic state,
never authorization, complete scan/review history, repository/file metadata or
digest bundles, reviewer/process metadata, or live Git/GitHub/Trellis facts.
Stale recovery deletes it and restarts from live authority. Successful public
serialization and terminal paths remove the producer result/checkpoint and any
empty owner directory.

## Requirements Clarification Result

Schema id `guru-requirements-clarification-2.0` is the active closed Draft 2020-12
result. Top-level fields are exactly `schema_version`, `skill_id`,
`generated_at`, `mode`, `typed_exit`, `invocation_context`, `review_target`,
`target_disposition`, `context_evidence`, `confirmed_facts`, `repository_answerable_questions`,
`clarification_rounds`, `open_questions`, `scope_proposals`, `source_actions`,
`mutation_results`, `active_task_evidence`, `ai_review_gate`,
`affected_contracts`, `content_identity`, `reason`, `consumer`, and `error`.
`invocation_context.kind` is `initial_issue`, `proposed_draft`,
`active_task_scope_change`, or `standalone_review` and includes a closed
caller-aware `resume_target`. `review_target` carries a portable current issue
or side-effect-free draft identity. `context_evidence` records only whether
current-session/live-authority context is current, stale, or unavailable plus
direct evidence refs and an optional missing reason. It never locates or
identifies Discovery private state; `needs_context` is the only exit that can
omit load-bearing current context.

Repository-answerable questions record one of `pending`, `answered`, or
`not_answerable`. Before the first clarification round no entry may remain
`pending`; both `answered` and `not_answerable` carry non-empty checked evidence
refs, while `not_answerable` also carries a non-empty
missing reason. Each clarification round has one `question_id`, optional
`atomic_group_id` plus an indivisibility reason, category `product_intent` or
`scope_risk_decision`, answer summary, status `complete`, `partial`, or
`refused`, affected contracts, and opened/closed question ids. Its question id
must already be open or be opened in that round. A partial answer cannot close
any question. The replay invariant is exactly `open_questions = opened -
closed`; close-before-open and reopen-after-close are invalid.

Each `scope_proposals[]` row is closed and contains `proposal_id`, `scenario`,
`trigger_evidence`, `proposed_contracts`, `cost`, `alternatives`,
`consequence_if_omitted`, `origin_requirement_status`,
`optional_mechanism_origin`, `decision`, and recorder-derived
`proposal_digest`. `origin_requirement_status` is `explicit`,
`necessary_correctness`, `confirmed_expansion`, or `unconfirmed_expansion`.
Decision is `pending`, `accepted_current`, `related`, `followup`, `new_task`,
`out_of_scope`, `mechanism_removed`, or `mechanism_replaced`. An unconfirmed
expansion is finalized only after the AI obtains the real choice in the current
dialogue; the result stores the selected disposition, never authorization
state, text, ref, timestamp, or digest. An optional-mechanism-origin proposal cannot be
classified into the five scope classes: its terminal disposition is
`mechanism_removed` or `mechanism_replaced`, with
`optional_mechanism_origin=true`.

`source_actions[]` supports only `none`, `issue_comment`, `issue_body_edit`,
`proposed_draft_update`, `new_issue_draft`, `select_existing_issue`,
`reopen_issue`, and `active_task_scope_update`. Every row binds exact objective
target, payload, preimage, status, action digest, payload digest, and mutation
evidence. These digests identify deterministic action bytes for recorder/checker
consumers; they never represent authorization or semantic approval. The AI
checks current-dialogue authority immediately before a write, executes the
approved GitHub/task action, and supplies only objective mutation facts. For
comment/body mutation, mutation content SHA-256 must equal the action payload,
canonical payload digest, and reread live GitHub body/comment content.

Active-task `clear`/`new_task` requires a non-empty array containing only the
seven terminal decisions. Every `accepted_current`, `related`, `followup`,
`new_task`, or `out_of_scope` proposal binds live GitHub authority facts and one
compact owner-result `decision_trail`. It is not a process trail. Its exact
fields are `trail_id`, final proposal id/digest/decision rows, and
`github_authority` containing kind, URL, and remote content checksum. It
contains no user identity, confirmation reference, authorization state/digest,
authority timestamp, planning identity, review state, context snapshot,
interrupted target, or re-entry route. Current planning documents, context
freshness, task-update preimage, re-entry owner facts, and the trail
remain in the transient owner result and are reread from their owning sources.
Pre-task and standalone results remain stdout-only.

A mechanism-only terminal result still requires the same planning documents,
re-entry owners, and current context evidence in the
transient owner result; only `decision_trail` is null.
Mixed results place only their five-classification subset in the trail.
Every terminal active-task result receives the same live task/context freshness
validation. Inputs must satisfy the closed current schema before normalization;
any mismatch fails closed.

`content_identity` contains recorder-derived target, content, context, scope,
action, payload, and result SHA-256 fields. They are local deterministic
identities for this recorder/checker pair, not workflow authority or public
handoff. Result identity is computed from the canonical result projection with
its own field omitted. The checker recomputes every digest and validates current
live facts.

Exit invariants are closed:

- `clear` consumes `guru-requirements-clear-router` and requires no open
  questions, a passed AI Gate, current source/context,
  finalized proposal dispositions, no pending action, and no
  successful unrefreshed GitHub mutation. The router validates
  `resume_target`: initial/draft -> wording route, standalone -> caller,
  accepted active scope -> planning review, otherwise active task -> exact
  interrupted progression;
- `needs_context` binds missing repository/current/history evidence and consumes
  `guru-discover-change-context`;
- `refresh_context` binds stale or mutated authority and consumes
  `guru-sync-base`; successful issue comment/body mutation requires this exit.
  Re-entry requires context `generated_at >= authority.updated_at`, then binds
  task update to that same context digest without requiring a second refresh;
- `retarget_context` binds an exactly selected open duplicate issue and consumes
  `guru-sync-base`; the complete initial chain reruns against that new target;
- `new_task` requires a reviewed side-effect-free `new_issue_draft`, plus a
  fresh persisted compact classification for active-task callers, and consumes
  `guru-full-task-intake-chain`; #112 owns every issue/task creation side effect;
- `blocked` is valid if and only if `ai_review_gate.status=blocked` and consumes
  `requirements-clarification-blocked`.

Unknown/multiple/unmapped exits, mismatched consumer objects, closed-question
drift, objective payload/live-content drift, invocation/resume mismatch, or
stale active-task linkage fail closed.

## Extension Version Manifest

`trellis/guru-team-extension.json` defines the reusable Guru Team extension
version and public API metadata. `.trellis/guru-team/extension.json` is the
installed provenance copy created by the preset installer in each target repo.

The installed manifest is one closed current contract:

- a fresh install may begin without a manifest, but every installed-state
  reader requires the newly written current manifest;
- a missing or invalid installed manifest fails closed with a clear next step;
- every current field is required and installed-state readers accept only the
  current schema;
- `source.tree_state` is objective provenance (`clean`, `dirty`, `archive`, or
  `unknown`), not a release-readiness judgment;
- `source.commit` and `source.tree_state` describe the extension source observed
  at apply time. They are not a self-referential claim that the installed
  manifest file is contained in that same commit;
- Git worktree apply records the full current commit in both `source.ref` and
  `source.commit`, with `source.is_mutable_ref=false`; a later
  manifest-bearing target commit does not change this source identity;
- `selected_platforms` records installer input and should not be inferred from
  directory presence alone.

The installed manifest is installer and ownership provenance only. Its presence,
content, drift, or changed path never makes extension verification applicable to
a business task, Publication, Finalizer, finish-work, re-entry, or recovery.
`guru-verify-extension-installation` instead validates the live clean canonical
source checkout and its `origin`/requested-ref/HEAD identity before any clone,
tempdir, installer, artifact write, or mutation. Its private result belongs only
to ignored source-session runtime and has no target-task identity.

The installed manifest also has an independent closed `overlays` provenance
domain with exactly `schema_version`, `status`, `selected_platforms`, `files`,
`removals`, `conflicts`, and `sidecars`. `files[]` is the complete current
selected-entry set and carries exact canonical-source/hash/mode/action records;
`removals[]` records a safe previous managed hash. `conflicts[]` and
`sidecars[]` are empty for an active installation. The flat
`install.managed_assets` list is not current overlay ownership authority and
must not be used as a fallback when `overlays` is missing or invalid. Marker or
content-text matching is never provenance. Overlay conflict state blocks staged
activation, and the installed validator derives selected/unselected disk
expectations independently.

Do not use `.trellis/guru-team/extension.json` as the canonical source of the
team extension version. The canonical source is `trellis/guru-team-extension.json`.

`public_api.migration_capabilities.guru-ledger-free-runtime` is the closed
capability declaration for the ledger-free current runtime. Version `1.0.0`
contains only `capability_id`, `version`, and a `projection_identity` bound to
the current extension id/version and workflow template id. The preset copies
this declaration unchanged into the installed manifest. It does not include
apply-time source provenance, selected platforms, a manifest digest, or any
claim that a future Task lifecycle, Release, or migration owner is active.
Current source and installed validators require the exact shape and fail closed
on a missing, extra, or mismatched identity field.

### Public Skill I/O Current Fields

The canonical and installed extension manifests publish one closed current
contract under `public_api.skill_contracts`:

- `interface_schema_id` is `guru-team-skill-interface-1.4`, with
  `interface_schema_ids` publishing current 1.4, 1.5, and 1.6 selectors;
- `registry_schema_id` is `guru-team-skill-registry-1.4`;
- `public_input_schema_ids`, `typed_output_schema_ids`, and
  `private_artifact_schema_ids` are exact inventories from all active
  production packages.

The current Intake closure is derived only from the live registry, current
Interface 1.4 packages, workflow markers, extension inventories, eval corpora,
and selected-platform copies. It contains six packages and 23 exits. A
workspace/task mutation refusal stops in dialogue before recorder/executor,
and the current `guru-sync-base` scalar contract delegates omitted optional
arguments to the formal resolver. Source validation, discovery, invocation, and
install consume exactly this live closure.

The sole current manifest is
`trellis/skills/guru-team/contracts/production-current-4.0.json`, with schema id
`guru-team-production-contract-manifest-4.0` and contract id
`production-current-v4`. It binds exactly the three planning/check/commit
packages plus `guru-qualify-normal-scenario`, 20 structured profiles, 15 stable
exits, current per-exit schema and example identities, consumer inputs,
projections, private artifact ids, four authoring-seed edges, the 160 x 5 host
production control, and canonical eval cases. Inputs and owner artifacts must
validate against the current package schemas; versioned v2/v3 files are
immutable legacy assets and no alternate executor, projection, or manifest
participates in current invocation.

The source and installed closure algorithm reads the live registry, current
package contracts, the production current manifest, Interface public
contracts, and package-local corpora. Nineteen integrated rows select Interface
1.4; normal-scenario qualification selects Interface 1.6; the standalone
verifier selects Interface 1.5. Exact profile, exit,
consumer, projection, current-case, and authoring-edge equality is required.
Twenty-three Skills and 100 exits are the current package cardinality regression, not
a hard-coded future registry allowlist; the business workflow independently
asserts 22 invokes, 98 exits, 35 workflow targets, and 24 stop targets.

The production manifest also binds the exact four
`skill_input_authoring_seed` edges. Each binding names the target Interface and
profile, projected `seed_fields`, target-owned `authoring_fields`, and the
package-local authoring example id. Interface and manifest validation require
the two sets to be disjoint, their union to equal the target profile's complete
top-level required set, the projected seed and authoring example to contain
exactly their declared keys, and the no-overwrite merged object to validate
against the complete target profile schema. This is a consumer contract kind,
not a projection operation; the operation inventory remains exactly
`direct|select|rename|normalize`.

The immutable `production-current.json` v1 asset remains legacy-only and is not
selected by current registry, extension, installation, or invocation. Test
fixture schema ids belong only to the fixture extension manifest and must
not appear in production extension, installed production inventory, platform
copies, or workflow mandatory routes. Registry schema 1.3 remains legacy-only;
current registry 1.4 selects Interface 1.4 for existing integrated rows,
Interface 1.6 for normal-scenario qualification, and Interface 1.5 for the
standalone verifier. Planned rows remain lifecycle-only.

`public_api.companion_scripts` includes stable id
`discover-skill-contract`. Its success DTO exposes the current package-relative
public input, invocation, per-exit
outputs/examples, consumer contracts, projections, and private-artifact
locators. Expected failures use `code`, repo-relative `field_path`, and
`remediation`; no absolute paths or raw contract bytes are persisted.

Its structured non-Skill consumer contracts are a closed ownership union:
`consumer.kind=workflow` requires a canonical schema locator below
`consumers/workflow/`, while structured `consumer.kind=stop` requires one below
`consumers/stop/`. A `zero_payload` stop carries no schema contract. Producer
package/output locators, cross-kind consumer roots, non-normalized spellings,
unsafe traversal, and missing or symlink-backed files are invalid.

Schema dialect identity remains Draft 2020-12, while the portable companion
implements a documented standard-library-only compatible closed subset rather
than the complete vocabulary. The recursive grammar accepts a root-only `$id`
and the validation keywords enumerated by `skill-package-contract.md`, including closed object,
array, conditional, union, scalar, and resolvable local ref forms. Only the
aggregate structured-input index may use exact package-relative refs to its
independently validated profile schemas. Unknown or unimplemented keywords,
boolean schemas, nested `$id` resource boundaries, invalid keyword types,
unsupported formats, malformed regexes,
and remote/unresolved/recursive refs fail
closed before an example or interface can be accepted.
The same boundary accepts only standard JSON with finite runtime numbers across
registry/interface/schema/example/marker/ref/invocation/discovery ingress and
public DTO egress. Its supported format set remains `date-time` and `uri`, with
RFC 3339 calendar/offset/lowercase/leap-second handling and RFC 3986 ASCII
scheme/component/percent-encoding validation as specified by
`skill-package-contract.md`; malformed values produce the existing structured
error rather than a traceback.

Repository release tags for the Guru Team extension use repo-level tags that
combine the target official Trellis CLI version and the Guru Team revision,
such as `v0.6.5-guru.10`, not namespaced tags such as
`guru-team/v0.6.5`. The tag must correspond to
the exact `trellis/guru-team-extension.json.version` present in the tagged commit,
and the manifest must expose `target_trellis_cli` so users can see which official
`@mindfoldhq/trellis` release this Guru Team extension targets. The repo release
tag and extension revision are independent version axes: release metadata binds
one immutable tag to one exact tagged manifest version rather than assuming their
Guru suffixes are equal. Stable workflow marketplace examples should use
`gh:castbox/guru-trellis/trellis#v0.6.5-guru.10`; unpinned
`gh:castbox/guru-trellis/trellis` means latest/canary and must be reported as a
mutable source in install or upgrade evidence.
An unreleased branch may carry the next canonical extension version while
public stable examples continue to point at the latest existing verified tag.

Release order matters: merge the manifest/docs PR first, create the annotated
`v<official-trellis-version>-guru.<revision>` tag on the merge commit, verify tag-pinned `trellis init` and
`trellis workflow` marketplace commands, then retire any old competing tag
names only after the new tag is verified.

## Task Identity and Local Runtime

Current AI-first tasks use official Trellis `task.json` as their tracked task
identity and create no Guru-owned durable Intake aggregate. Runtime resolves
the worktree from current `task.json`, the checkout,
ignored runtime mapping, and live `git worktree list` facts. Any missing or
mismatched identity fails closed; no alternate task identity artifact is read.

Local-only reusable mappings live under the gitignored producer namespace:

- `.trellis/.runtime/guru-team/workspaces/<workspace-slug>.json`
- `.trellis/.runtime/guru-team/tasks/<task-slug>.json`

Runtime cache may contain absolute worktree paths and executor timestamps, but it is disposable, untracked, has no index/developer dimension, and must be reconstructable from current `task.json`, the checkout, `git worktree list`, or explicit parameters. Ordinary task commands read tracked shared config but do not rewrite it.

Finalizer's archive executor must converge the same task's existing source and
target `task_artifact_dir` projections to the exact committed archive locator.
Validate both task/workspace mappings and registered owner identity before
either write; preserve workspace/branch/source identities and unrelated
fields. Same-transaction archived recovery accepts only the exact old active
or already-current archived locator. Missing or conflicting mappings stay
fail-closed; boundary validators remain read-only and cannot perform a repair.
The source mapping points into the task workspace, so archive convergence does
not create a second tracked archive in the source checkout.

Query-only `prepare-task` writes neither task context nor runtime cache. Active
`guru-create-task-workspace` is the only creator. On successful workspace/task
creation it writes official `task.json` and ignored source/target runtime
mappings. Upstream checker results and workspace
plan/result stay in ignored owner-private runtime and are reread only by their
direct consumer.

Assignee remains a portable task/context audit field, never a path namespace.
The workspace executor invokes official `common.task_store.cmd_create` in an
isolated subprocess with explicit reviewed creator and assignee values.
Official task creation therefore produces
`task.json.creator=task.json.assignee=<reviewed-login>` and rejects missing
ownership before writes. Guru runtime does not
read, copy, initialize, restore, or require `.trellis/.developer` or
`.trellis/workspace/**`; existing official identity bytes remain untouched.
The `workspace_slug` and workspace mappings above identify the isolated task
checkout/worktree only; they have no journal/index/developer dimension.

## Finish Summary

`trellis/workflows/guru-team/schemas/finish-summary.schema.json` is the current
finish-work summary SSOT. The only accepted generator is
`guru-team.finish-work`; unknown generators and non-current fields fail closed.
The Python validator is strict about field sets, types, lengths, counts, enums,
SHA/issue/PR formats, clean relative paths, normalized duplicates, adjacent
repeated clauses, and all derived search/retrieval facts.

Duplicate identity is domain-specific. Every path-bearing array, including
`git.changed_paths`, `index.search_terms.paths`, and
`index.affected_surfaces[].paths`, uses the exact path string as identity;
punctuation-removing text normalization must not collapse two different valid
Git paths. The generator sorts and deduplicates Git paths by exact string, and
validators still reject exact duplicates. Non-path semantic and search-token
string arrays continue to reject duplicates after text normalization.

Current finish-summary schema version 2 has no task-local semantic input file.
Finalizer builds it once from the exact Publication-reviewed PR payload,
`task.json`, ignored runtime identity, live Git, archived
artifact existence, UTC time, and the unique publish output. `index.problem`
comes from task/Issue identity; `index.outcome` and `index.changed_behavior`
come from the validated PR body change-summary section; affected surfaces come
from the closed changed-path classifier; contract changes are empty except for
fixed machine-triggered facts. Search terms and `retrieval_text` remain derived
facts. Historical schema version 1 summaries remain readable by Discovery, but
the current writer never emits schema 1. Final artifacts live at
`.trellis/tasks/archive/<YYYY-MM>/<task>/finish-summary.json`; values may not
contain absolute, parent, workspace, runtime, backslash, CR, or LF paths, and
may not contain leading or trailing whitespace.

The final pre-archive snapshot combines a NUL-delimited base-to-working-tree
diff with NUL-delimited untracked file enumeration; task metadata is recorded
as individual files, never as an untracked directory placeholder. The
protected-prefix filter and fixed fact rules apply to this snapshot. If the
required diff snapshot fails, both path arrays are `[]`, the
filtering fact is removed, and exactly one fixed non-disclosing
`finish-summary git path snapshot unavailable` fact is recorded before
`retrieval_text` is re-derived. After the unique draft PR is bound, the final
projection sorts and deduplicates raw base-to-HEAD paths, filters
workspace/runtime protected prefixes, and writes the safe set to both
`git.changed_paths` and search `paths`. A non-empty filtered set adds one fixed
`finish-summary protected path filtering` contract fact without path, basename,
or count details; an empty filtered set adds no such fact. Schema and Python
validation reject protected prefixes in every path field. The final summary is
built once in the active task after draft PR binding and moves unchanged to the
archive locator. Publication's ignored-runtime readiness checkpoint owns its
semantic conclusion and emits exact title/body with task plus
`branch_review_commit`; Finalizer does not read or commit that checkpoint. The
finalization plan binds repo/base/head, exact title/body, `draft=true`, and its
internal digest. Active-state recovery consumes the active schema 3.0 plan plus
Git/remote, marketplace owner, task layout, and PR facts. Reuse and final projection require one exact PR
number/URL/title/body identity; one matching draft is reused, zero creates one,
and multiple identities fail closed. The real-PR final summary has one
deterministic UTF-8 JSON byte representation and digest. Pre-move continuity
and incomplete post-move recovery rebuild those bytes from the immutable
summary template plus the already-bound remote PR number/URL, so a summary and
its PR identity cannot be changed together. After the exact archive commit
exists, fresh recovery reads only that commit's `finish-summary.json` blob,
strictly parses the canonical PR URL and unique PR ref, rebuilds the expected
bytes/digest, and recovers the original number/URL. It does not read the
archived working-tree summary or invoke the general finish-summary artifact
validator. The recovered PR must still exist as the unique open repo/head/base
candidate and match that exact number/URL; missing, closed, or replacement PRs
fail closed. Readiness, body, and verifier remain unopened after the
official move, while remote title/body and three-way HEAD checks still come
from the immutable plan and remote facts.

Final projection, incomplete recovery, and exact recovery share one strict PR
URL parser. The URL must be exactly
`https://github.com/<owner>/<repository>/pull/<positive-number>` with no
alternate transport, leading-zero number, trailing or extra path, query, or
fragment. GitHub owner/repository identity is compared case-insensitively with
the normalized `plan.git.repo`, while the canonical output preserves the exact
valid owner/repository casing returned by the bound remote PR, such as
`microsoft/PowerToys`. A different repository remains invalid regardless of
casing.

Archive content identity is not inferred from the no-renames path set. Before
the exact archive commit exists, each `tracked_move_paths` item binds the
`branch_review_commit` blob to the archived working-tree file and prospective
schema 3.0 archive commit blob. A tracked file that differs from that parent
blob must match its exact `reviewed_tracked_bindings` mode and SHA-256; an
unbound difference fails closed. `task.json` may then apply only the official
`status` and `completedAt` archive fields to those reviewed pre-move bytes.
`untracked_archive_outputs` are validated by their existing template/digest
contracts. Once the exact archive commit exists, its tree and blobs replace the
archived working tree as the authoritative content source.

Failure-state evidence is read from the real filesystem, Git index/log, bare
remote, and fake GitHub PR store after invoking production `cmd_finish_work()`.
Test-owned dictionaries may summarize those observed facts, but must not drive
or manufacture transition state.

## Workspace Boundary Snapshot

`check-workspace-boundary --json` resolves the task from `--task` or current
task, validates `task.json` plus ignored task/workspace mappings and live Git
worktree identity, then derives the expected workspace. The command never
trusts a committed absolute workspace path or alternate task identity artifact.
The snapshot records `status`,
`workspace_mode`, `expected_workspace`, `actual_repo_root`, optional
`source_checkout`, `task_dir`, repo-relative `task_dir_relative`,
source/task Git status, suspicious same-task artifacts, and deterministic
errors. Missing or mismatched task/runtime/worktree identity, a task outside the
current repo `.trellis/tasks`, or source-checkout same-task metadata fails
closed.

## Planning Approval Checkpoint

`guru-approve-task-plan` is the sole semantic owner of Phase 1 planning
approval. New owner evidence uses closed schema
`guru-planning-approval-3.0` and lives only in ignored
`.trellis/.runtime/guru-team/owner-checkpoints/<task-key>/planning-approval.json`.
It is a short-lived owner checkpoint, not a tracked task artifact, public DTO,
handoff, or archive file.

The AI rereads live requirement authority, current wording result, `prd.md`,
`design.md`, `implement.md`, and the Docs SSOT decision.
It reviews eight dimensions: requirement authority, scope boundary, design
adequacy, implementation plan, acceptance verifiability, Docs SSOT,
provenance, and supported unusual scenarios. Formatting, spelling, link,
derived-text, and workflow-metadata changes are classified by their real
semantic effect; only changed dependencies are refreshed.

The compact checkpoint retains only mode, task locator, the three planning
locators, one composite planning-content freshness token, current authority
references, Docs SSOT strategy/durable paths/summary, the final eight-dimension
semantic result, typed exit, reason, and unique consumer. The token has one
local deterministic consumer: the planning checker invoked inside the Planning
public wrapper before typed-output projection. It detects same-path drift and
returns control to the AI owner for delta classification; it is not authorization,
semantic approval, public handoff, or whole-chain authority. After the checked
typed output passes its schema, the same producer wrapper deletes the checkpoint.
The activation workflow consumes only the DTO plus current planning/live facts,
then separately presents the plan and owns the dialogue-local review pause.
Task activation and Phase 2 never read or delete this private state. The checkpoint does not retain
per-file hashes, sizes, mtimes, repository snapshots, scan history, reviewer
metadata, raw reports, assignments, liveness, authorization, authorization
wording, or authorization digests.
The Phase 1 plan reply and any real scope choice occur only in the current
conversation and are never projected into persisted or public state. The Skill
recorder/checker does not inspect that reply. Phase 0 confirmation and replies
about a materially changed plan are not reusable; explicit autonomous execution
may omit only the ordinary unchanged-plan pause and is likewise not persisted.

The closed exits are:

- `approved` -> `workflow:phase-1-task-activation`, with every dimension true
  and no finding, revision action, scope proposal, or blocker;
- `revision_required` -> `skill:guru-approve-task-plan`, with one or more
  task-local revision actions;
- `clarify_scope` -> `workflow:guru-task-plan-clarify-scope-router`, with one
  or more exact scope proposal refs;
- `blocked` -> `stop:task-plan-approval-blocked`, with one or more concrete
  authority or evidence blockers.

`record-planning-approval` writes an already completed AI semantic result.
`check-planning-approval` validates schema closure, task/planning locators,
required non-empty files, the recomputed composite content token,
semantic/exit/consumer union, and requested exit.
Neither command decides scope, sufficiency, finding severity, revision,
authorization, or route. Unknown, multiple, stale, ambiguous, or
consumer-mismatched results fail closed; mapped re-entry remains automatic.

The recorder accepts only current schema 3.0. Any other shape returns
`planning_approval_schema_version_invalid` and requires a complete current
semantic review. `task.py start` is only a status transition and never approval
evidence.

### Change request readiness result

Schema `guru-change-request-review-2.0` defines the portable
`issue-review.json` result owned by `guru-review-change-request`. Before task
creation the recorder and checker return JSON on stdout only. The normalized
target is exactly one existing issue, side-effect-free proposed draft, or
side-effect-free standalone request, with title/body, identity, content, and
source authority hashes. `prerequisites` is derived only from the public
`wording_current` transition, or the original `clarity_current` / `context_current`
transition for a missing-prerequisite reroute. It never accepts complete
producer-private results, caller-authored flat projections, or invented pass
fields. Unconsumed upstream payload hashes are absent from result 2.0.
`evidence_linkage` keeps target identity/content, clarity facts/disposition, and
wording facts distinct. Clarification `content_sha256` hashes its semantic
content, not the target title/body; the wording target-content digest alone
binds the canonical title/body pair. The two disposition digest domains retain
their producer definitions rather than being equated by field name.

For both draft variants, `source_request_sha256` is the canonical digest of the
same current authority projection owned by #113 `review_target`: `kind=draft`,
normalized `repo`, null `issue_number`, `url`, and `updated_at`, `state=draft`,
and the current reviewed-body SHA-256. Runtime rebuilds this projection from
the current change-request input bytes and rejects any merely well-shaped but
wrong or stale digest. Title bytes and draft/request/caller identity remain
separate target fields and continue to participate in target content/identity
digests.

The semantic portion contains the ten ordered readiness dimensions, a closed
finding category set, affected evidence/hashes, scope conclusion, AI Review
Gate, reason, scalar exit, and exact consumer. User interaction is dialogue-only.
`ready` requires all prerequisites current, all dimensions passed, no blocking
finding, complete linkage, passed Gate, and no required confirmation. Every
non-ready result requires at least one AI-authored failed dimension, blocking
finding, and affected evidence. Deterministic commands validate these facts but
never infer or rewrite the exit.

The public package carries only a deidentified example. The active
`guru-create-task-workspace` consumes the public `ready` transition, not the
private review result, and persists no Guru-owned task-local scope aggregate.
Readiness creates no task, workspace journal, cache, index, sidecar, or tracked
artifact. Owner result 1.0 and the old prerequisite-payload CLI are retired by
the explicit #386 direct migration; no legacy reduction path remains active.

The production regression suite must pass actual Discovery, Clarification and
Wording public outputs into the next input and consume the resulting transition
in Readiness record/check/invoke. It covers wrong stages, missing prerequisites,
target mismatch, real title/body drift and draft source-authority mismatch.
Handwritten flat projections cannot prove this chain. Shape errors fail with
`schema_mismatch`; actual target/content drift remains `stale_identity`.

## Task Workspace Plan And Result

Schema `guru-task-workspace-plan-2.0` is a closed ignored-runtime plan produced by
`record-task-workspace-plan`. It binds skill/mode/invocation identity; the five
checker-passed prerequisite results and their digests; final issue or reviewed
draft authority; readiness scope projection; selected base and three-way HEAD
facts; semantic branch/workspace/task naming; one resolved assignee and source;
exact issue/worktree/task/artifact/runtime operations; structured command argv;
the mutually exclusive action scope; AI Review Gate evidence; and
the canonical plan digest. It contains no absolute path, runtime payload,
secret, raw private record, or shell command string.

The `base` projection includes the checker-passed
`post_sync_resolution_sha256` in addition to selected base, refs, HEADs, and
the original sync facts digest. This post-sync identity anchors the
mutation-time comparison against revalidated local facts and the current
remote HEAD returned by read-only `git ls-remote`; it does not authorize a
second fetch, fast-forward, or ref update outside `guru-sync-base`.

Assignee source is exactly `explicit_input`, `single_issue_assignee`,
`current_github_login`, `user_selected_from_candidates`, or
`user_supplied_after_unresolved`. Candidate order is explicit input, exactly
one issue assignee, zero issue assignees to current GitHub login, then AI/user
choice for multiple or unresolved candidates. An unresolved assignee blocks
workspace/task mutation.

The draft invocation may perform only the reviewed GitHub issue mutation; the
open-issue invocation may perform only the reviewed workspace/task mutation.
The exact side effect is confirmed in the current dialogue before the
recorder/executor, but no confirmation scope, state, identity, text, ref, or
digest enters the plan/result/schema/DTO. A created issue binding covers only
the objective normalized repo, positive number, canonical URL, `state=open`,
title/body SHA-256, `updated_at`, reviewed draft id/digest, and its canonical
facts digest.

Target provenance uses two coordinated nullable fields:
`created_issue_binding_sha256` and `created_issue_result`. A normal existing
issue and a reviewed draft before create require both null. An existing issue
produced by an earlier draft invocation requires both non-null: the binding SHA
equals the embedded created issue facts digest, and `created_issue_result` is
the complete `guru-task-workspace-result-3.0` `created_issue` variant with
passed executor/checker stages, valid result and binding facts digests, and the
fixed `refresh_review` consumer. Its current issue facts match the plan and its
complete Intake rerun exposes the canonical live existing issue with
`kind=issue`, canonical URL identity, open state, matching update time, body and
facts digests, and null `issue_binding`. Missing or partial provenance is
invalid.

Schema `guru-task-workspace-result-3.0` is a closed ignored-runtime union:

- `created_issue` binds the exact plan and live created issue and can only
  return `refresh_review`; branch/worktree/task/artifact/runtime operations are
  absent;
- `created_workspace` binds branch/worktree/task identity, ignored runtime
  mapping projection, trackability, and workspace-boundary facts and can only return
  `created`;
- `no_side_effect` binds a before/after zero-write snapshot and returns
  `refresh_review` or `blocked` according to the AI-authored route. User refusal
  stops before recorder/executor invocation and produces no plan, result, or
  DTO.

The result is never a tracked Intake artifact. Ordinary re-entry may reuse only
exact branch/worktree/task identity. A mismatch in issue,
base, naming, locator, task state, or bytes is `blocked`; runtime does not
overwrite, delete, rename, or silently adopt a conflicting object.

Before a draft create, exact recovery candidate facts are title, body, the
order-independent exact label set, `state=open`, and `createdAt` not earlier
than the reviewed plan capture. Zero candidates authorize one create; one is
recovered and live reread; multiple candidates block. A recovered issue emits
the same checker-valid `created_issue` result and `refresh_review` route as a
newly created issue.

## Normal Scenario Qualification Invocation Data

Qualification has no repository artifact contract. Each of the ten public
input schemas is closed around one fixed `profile`, fixed caller identity,
workflow or standalone mode, current target identity, a non-empty unique
`candidate_refs` set, and only the locators needed for the semantic owner to
reread live authority and repository evidence. The aggregate input is a
`oneOf` discriminator and adds no fields.

The qualification Interface 1.6 invocation binding declares only
`profile_selector={source: aggregate_public_input, field: profile}`. The full
public stdin envelope remains unchanged through the installed wrapper, whose
aggregate and selected closed schemas remain authoritative. The owner-private
adapter transcript may record only the observed public `profile`; host grading
compares that receipt with its private control-map profile after model return.
The receipt is excluded from the adapter request, native request, prompt, argv,
model environment, public DTO, and shared artifacts. Missing, unknown,
duplicate, mismatched, or multiple discriminator selection fails closed.

Each candidate receives exactly one of
`qualified_current`, `qualified_explicit_nonstandard`,
`qualified_approved_expansion`, `scope_confirmation_required`,
`rejected_no_authority`, `rejected_unsupported_entry`,
`rejected_not_reproduced`, `rejected_out_of_scope`, `mechanism_removed`,
`mechanism_replaced`, or `blocked`. The current invocation aggregates these
into exactly one of `classified`, `scope_confirmation_required`,
`mechanism_revision_required`, or `blocked`, with the fixed consumers declared
by the workflow/interface graph. Unknown, missing, duplicate, multi-exit,
profile/caller mismatch, stale identity, or consumer mismatch fails closed.

No schema defines a qualification result/report/checkpoint locator. The checked
result is process-local stdout and expires when the invocation ends. Phase 2
and Publication current schema 5.0 gates and the Branch Review current schema
6.0 gate independently record only terminal qualified/rejected classifications
for their own direct consumers.
Every row contains unique `candidate_ref`, one terminal decision, a six-field
witness (`requirement_refs`, `supported_entry_refs`,
`existing_caller_refs`, `honest_action_sequence`, `defect_observation`,
`excluded_assumptions`), and the fixed `consumer_use`. Their semantic
findings/dispositions bind a candidate in the same gate. Legacy Phase 2 and
Publication schema 4.0 checkpoints, plus Branch Review schema 5.0 or older
checkpoints, are stale and require a complete fresh owner round; no
compatibility reader converts them to a current schema.

## Phase 2 Check Artifact

New active evidence uses closed schema `guru-phase2-check-5.0` and
`skill_id=guru-check-task`; the basename remains `phase2-check.json` and no
parallel pass artifact is allowed. The ignored owner checkpoint stores only
mode/task, `phase2_capture_commit`, `reviewed_content_sha256`, reviewed paths,
executed validation evidence, the final Docs SSOT result, semantic
adequacy/findings, final candidate classifications with direct-consumer
witness, and one typed exit/route/reason/consumer. The private
`guru-phase2-worktree-content-1.0` identity covers live tracked and untracked
worktree paths and has one local deterministic consumer: the checker invoked
inside the Phase 2 public wrapper before typed-output projection. It is
distinct from the four-consumer durable `guru-reviewed-content-1.0` contract.
Its supported atomic entries include regular files, executable files,
symlinks, missing paths, and Gitlinks. An unchanged uninitialized Gitlink binds
the unique stage-0 superproject index mode `160000` and OID after the current
commit records the same pointer. An initialized Gitlink additionally requires
an exact submodule root, clean status, and submodule `HEAD` equal to that OID.
Dirty, HEAD-drifted, index/commit-pointer-drifted, deleted, replaced,
root-mismatched, unmerged, or ambiguous Gitlinks fail closed. This is an
additive `1.0` compatibility rule: the former runtime produced no valid digest
for a Gitlink, while every previously supported non-Gitlink entry keeps its
existing payload and digest. It does not relax Task Commit's separate rule that
a Gitlink selected for staging must be initialized and clean.
It detects reviewed-content drift and returns control to the AI owner for delta
classification; it is not authorization, semantic approval, public handoff, or
whole-chain authority. Live implementation output, Planning owner state, issue
scope, repository snapshots, raw worker evidence, assignment/liveness,
per-file or artifact digest bundles, and handoff narration are transient entry
facts and are not copied into it.

Reviewed paths and validation evidence are non-empty. The semantic owner uses
current planning, implementation, Docs SSOT, issue scope, diff, tests, and
worker observations directly to judge the nine adequacy dimensions and
findings; the recorder/checker validates only the compact closed result and live
freshness, never semantic sufficiency.

Every candidate issue is classified before severity as `current_scope`,
`scope_change_required`, `followup_proposal`, or `out_of_scope`; only
`current_scope` may carry P0-P3 and a finding id. Every `current_scope`
candidate must carry a non-empty finding id and resolve to exactly one matching
finding with the same candidate id and severity; every finding points back to
one current-scope candidate and is referenced by at least one adequacy
dimension. Every unverified item is likewise referenced by an adequacy
dimension; unknown, duplicate, missing, or dangling ids fail closed. Every
finding is blocking; a passing Gate requires no
open current-scope finding,
no blocking unverified item, all nine adequacy dimensions passed, and a full
rerun over the complete current
scope. A fixed finding cannot promote a prior partial round to pass.

The checker rereads the current task, planning, live implementation/diff,
validation scope, Docs SSOT, issue scope, `phase2_capture_commit` ancestry, and
the current reviewed-content identity. A metadata-only HEAD/status change keeps
the identity fresh; a reviewed-content change fails closed. The `passed` DTO's
unique consumer, Task Commit, rereads this checkpoint together with the current
reviewed-content identity and commit parent before candidate construction and
execution. Routine assignment/liveness and the exceptional private recovery
checkpoint are not Phase 2 inputs and do not enter the owner checkpoint.

The closed exits are `passed`, `implementation_required`, `planning_stale`, and
`blocked`. `planning_stale` alone carries route discriminator `reapprove_plan`
or `clarify_requirements`, with one corresponding consumer. Schema/runtime
reject unknown, multiple, ambiguous, or Gate/exit/consumer-inconsistent states.
Any non-current shape fails schema validation and the owner must run a complete
current semantic round. `passed` projects only
`task_ref + phase2_commit_anchor` to Task Commit. After output-schema validation,
the Phase 2 producer retains the `passed` checkpoint for that one consumer and
deletes it for `implementation_required`, `planning_stale`, and `blocked`.
Task Commit deletes the retained checkpoint only after a commit is successfully
published or the same published commit is successfully recovered; a failed
candidate or executor attempt retains it for bounded retry. Branch Review then
consumes the committed Task Commit DTO and validates parent, paths, content
continuity and the complete range directly from live Git. Commit message format
is not downstream freshness authority. Downstream
workflow metadata is validated by its owning gate and is never projected back
into Phase 2.

## Task Commit Candidate

Each `guru-create-task-commit` invocation owns one temporary candidate under
ignored `.trellis/.runtime/guru-team/task-commit-plans/<task-key>/<sequence>.json`,
where `sequence` is a fresh three-digit
increasing id. Current schema `guru-task-commit-candidate-5.0` binds only task
locator/branch/status, base/pre-commit/Phase 2 commit anchor, the complete
staged/unstaged/untracked/delete/rename/copy snapshot, unique path
classifications, exact stage paths, canonical UTF-8 message fields/bytes, and
the completed AI review. Live `task.json`, the Phase 2 DTO,
Git operation state, snapshot freshness, and shared commit-message parser facts
are reread by the builder/validator; they are not copied into a cross-Skill
digest chain. The candidate contains no user authorization, confirmation
wording, terminal result journal, reviewer identity, or timestamp.

Snapshot entries whose index mode is `160000` additionally require
`gitlink_head`, `gitlink_initialized=true`, and `gitlink_dirty=false`.
`gitlink_head` is the unique commit checked out by the submodule rooted at the
exact worktree path. Uninitialized, dirty, unborn, or root-mismatched submodules
cannot produce a safe candidate. These fields are conditional. Current snapshot
producers always emit `copied_from`, using a repo path only for copy destinations
and `null` otherwise.
Candidate validation and executor revalidation compare the current
gitlink identity, so a reviewed B revision changed to C before exact staging is
stale before any index mutation. For non-deleted mode `160000` paths,
`gitlink_head` is also the exact index-content authority: the executor writes
that OID through `git update-index --cacheinfo` rather than reading the mutable
submodule worktree through `git add`, then verifies the staged mode/OID and the
current worktree identity. Consequently a B-to-C change detected before
publication cannot place C in the index or commit. A deliberate gitlink delete keeps the conditional deletion
identity and ordinary literal delete behavior.

For every non-gitlink snapshot entry, `worktree_sha256`, `mode`, and `deleted`
form the path's ordinary content authority. `renamed_from` and `copied_from`
are mutually exclusive relation fields: only `renamed_from` grants the reviewed
destination authority to remove and exact-stage its source. `copied_from`
records provenance only and never grants source deletion or staging authority.
If a copy source has its own staged, unstaged or untracked state, it appears as
an independent snapshot entry and requires its own classification and Phase 2
coverage; unrelated staged source content blocks, while a clean source is not
added to the plan. A non-delete path must still expose the exact reviewed bytes
and mode when the executor materializes its Git blob; a delete or rename source
is an exact index absence. The private candidate never enters its own snapshot,
classifications, or exact stage set.

Repository operation state is immediate runtime evidence rather than a plan
field. Candidate validation and executor checks before staging and immediately
before `git commit` reject active merge, cherry-pick, revert, rebase, sequencer,
or `git am` state. The detector never clears or rewrites operation markers.

Every dirty path belongs to exactly one of `task-reviewed`,
`unrelated-preserved`, `unreviewed-blocking`, or `ambiguous-blocking`. The plan
candidate is ignored owner-private runtime and is excluded from the snapshot.
Public artifacts store
only repo-relative paths, digests and structured facts, never file bodies,
credentials, signed URLs, customer data or machine-local absolute paths.
The current Phase 2 passed DTO is consumed before candidate construction. The
candidate builder and executor reread the producer-private Phase 2 checkpoint,
verify its current reviewed-content identity and `phase2_capture_commit`, and
bind the DTO's `phase2_commit_anchor` without exposing the checkpoint or its
digest in the candidate or public output.

Execution requires a passed AI review, no blocking classifications, fresh
task/HEAD/snapshot/message/parser facts, and exact semantic index equality. The
executor first revalidates planned gitlinks before any stage side effect, binds
their artifact OIDs into the exact index, and then binds the complete pre-hook
index tree and each exact path's blob/mode. Real hooks run against a temporary
detached worktree plus that isolated index. Their objective exit records,
message-file bytes, post-hook index/worktree state and the created commit object
must all match the reviewed candidate before the live ref can advance.

The failure result separates transaction creation from live publication. If a
hook or post-hook gate fails after Git created the temporary commit, it reports
`created_commit_sha` and a transaction stage while the live branch remains at
`pre_commit_head`; candidate and Phase 2 checkpoint remain recovery inputs. A
failure after conditional live-ref advance reports
`transaction_stage=live_ref_published`. The successful public DTO remains only
`pre_commit_head` and `commit_sha`.
Before publication, the executor creates and validates the isolated commit. It
then uses standard `git update-ref <ref> <new> <old>` followed by `git reset
--mixed --quiet HEAD`; it owns no custom lock, atomic replacement, rollback, or
concurrency protocol. On success it returns only `pre_commit_head` and
`commit_sha`, deletes the private candidate and consumed Phase 2 checkpoint, and
never writes Git-derived result/tree evidence into tracked metadata. Failure
before ref publication leaves the live ref/index untouched and retains both
checkpoints; failure after a successful conditional ref advance reports the
created commit for bounded same-plan recovery, which retires both checkpoints
after verifying the published commit. A later finding-fix commit requires a new
sequence and fresh Phase 2 evidence; a prior plan cannot be replayed.

### Executor Boundary

`create-task-commit --candidate-artifact <ignored-runtime-candidate>` validates
one schema `guru-task-commit-candidate-5.0` private candidate. It materializes
only AI-reviewed blobs/modes in an isolated index, runs repository commit hooks, and
verifies parent, raw message, committed path set, complete tree and unrelated
preservation before conditionally advancing the live branch/index.

The private candidate is never staged. A normal validation or hook failure
preserves the candidate and unrelated state for bounded recovery. Success
returns `pre_commit_head` and `commit_sha`, then removes the candidate. Commit
tree, message, path and parent facts remain derivable from Git and are not
copied into tracked task metadata.

## Private Agent Recovery Checkpoint

Routine assignment, progress, status requests, completion, review rounds and
liveness are ephemeral workflow facts. New tasks do not create
`agent-assignment.json`, `reviews/*.md`, `review.md`, progress journals,
heartbeat files or scan snapshots.

Only a real unfinished-to-replacement transition may persist recovery state.
The checkpoint lives under ignored
`.trellis/.runtime/guru-team/agent-recovery/<task-key>.json` and contains one
task identity plus a minimal ordered event chain:

- `unfinished`: logical role, predecessor agent, concrete reason, remaining
  work/validation/blocker summary, observed branch HEAD and timestamp;
- `replacement`: replacement agent, the exact unfinished event id, acceptance
  reason, accepted remaining-work summary, observed branch HEAD and timestamp.

A replacement must close the currently open unfinished event for the same
logical role. The recorder/checker validate identity, sequence, ancestry,
timestamps and the event linkage; they never infer failure from elapsed time
or a platform wait timeout. The checkpoint is owner-private recovery input and
is not a Phase 2 dimension, Branch Review prerequisite, public DTO, tracked
handoff or archive artifact.

## External Work Item Publication Effect

Publication rereads current requirement authority and live GitHub state and is
the sole semantic owner of the PR's external-work-item effect. A fully delivered
Issue-backed task normally receives a closing keyword when the PR targets the
default branch. Concrete post-merge validation, observation, release, or
incomplete-delivery requirements keep the Issue reference-only. A task with no
external work item receives no Issue reference or closure effect.

For a non-default target branch, Publication emits reference-only semantics;
the later default-branch Publication must decide closure again from current
authority. Finalizer binds the reviewed payload, and Merge validates the exact
payload plus GitHub's resulting state. Neither step re-decides closure or calls
an Issue-close API.

## Commit Message Payloads

`check-commit-messages --json` is an explicit standalone quality diagnostic for
objective commit subject/body shape. `guru-create-task-commit` still validates
the exact message it is about to create, but Branch Review, Publication, and
Finalizer do not rerun range-level message parsing or use subject/body/`Refs` as
freshness authority. Message-only deviation therefore cannot require a metadata
commit while reviewed content identity is unchanged. The diagnostic must not
decide whether implementation, Phase 2 check, Branch Review, or PR readiness is
sufficient. Its payload is additive and uses:

```json
{
  "status": "ok",
  "base_ref": "origin/main",
  "head": "<sha>",
  "range": "origin/main..HEAD",
  "checked_commits": [],
  "errors": []
}
```

When blocked, the command exits non-zero and returns `status=blocked` with
`errors[]` entries that include the commit hash, subject, classified kind
(`work`, `metadata`, `merge`, or `invalid`), and objective validation messages.

The single archive transaction commit generated by finalization uses
the Task Commit owner's reviewed Chinese metadata subject and an empty body. There
is no separate readiness/evidence metadata commit.
Commit message payloads must never use close keywords such as `Closes`,
`Fixes`, `Resolves`, `Close`, `Fix`, or `Resolve`; those keywords remain PR
body-only semantics controlled by Publication.

## Reviewed Content Identity

`guru-reviewed-content-1.0` is the durable content-continuity contract shared
by Branch Review, Publication, Finalizer, and source Verification. Its digest is
SHA-256 over this canonical UTF-8 JSON payload, encoded with sorted object keys,
no ASCII escaping, and compact separators:

```json
{
  "algorithm": "guru-reviewed-content-1.0",
  "entries": [
    {"path": "<UTF-8 repository-relative path>", "mode": "<Git mode>", "oid": "<Git object id>"}
  ]
}
```

The metadata-excluded entry set is derived from the selected Git commit and,
when explicitly requested for current `HEAD`, its worktree overlay. Each entry
contains exactly `path`, `mode`, and `oid`; Git object kind, `base_commit`,
review range, stage-private fields, and any other metadata are not identity
input. Entries are ordered by the raw bytes of `path.encode("utf-8")` before
the payload is hashed. Paths must decode as strict UTF-8. Supported atomic Git
entries retain the existing regular/executable blob, symlink, and gitlink
semantics; ambiguous or unavailable entries fail closed.

The closed metadata exclusion set is:

- `.trellis/tasks` and every descendant, including archived tasks;
- `.trellis/workspace` and every descendant;
- `.trellis/.runtime` and every descendant;
- the exact provenance-tail manifest `.trellis/guru-team/extension.json`;
- `.DS_Store` at any path depth, matched by basename.

The canonical shared helper owns this exclusion classifier and all tree,
worktree-overlay, gitlink, ordering, payload, and digest behavior. Branch
Review, Publication, Finalizer, and Verification call that helper; a stage must
not keep a package-local algorithm or metadata classifier.

This digest proves reviewed business-content continuity only. Base ref and base
commit identity, review range, review/current commit, target ref/HEAD, and
ancestry are independent freshness authorities owned by their existing gates.
Changing an included path, mode, or oid changes the digest and fails continuity;
changing only an excluded path leaves it unchanged and does not waive any
independent freshness check.

Branch Review owner-private checkpoints are current-only for this contract.
Any schema 5.0 or older checkpoint written by the former package-local identity
implementation is stale: current loaders do not dual-read, migrate, rewrite,
or synthesize it.
Recovery is one fresh Branch Review over current authority and content.

### Finalizer provenance source/target binding

The pre-PR provenance metadata tail has two independent Git identities. The
`target_reviewed_checkout` belongs to the task repository at
`reviewed_content_head`; it is the only installer target, manifest mutation
owner, metadata-tail commit parent, and publication-lineage owner. The
`extension_source_checkout` supplies only canonical Guru Team preset bytes and
must remain detached and clean. Neither checkout may be inferred from path
presence, a hidden local checkout, `PATH`, or a global installation.

Finalizer constructs one invocation-local closed binding from the installed
manifest and current target repository identity:

- `self_hosted`: source and target canonical repository identities are equal;
  the source commit is the target `reviewed_content_head` and is checked out
  from the target Git object database;
- `installed`: identities differ; source repo/ref/commit are the manifest's
  clean immutable identity, and a separate repository is initialized with a
  canonical `origin`, exact full-OID fetch, detached checkout, exact HEAD, and
  clean-state validation.

There is no fallback or dual-read between modes. Missing or malformed source
repo/ref/commit, a non-full OID, dirty or mutable provenance, origin/HEAD
mismatch, or a dirty source checkout stops before target apply or any remote
mutation. The binding is package-private and ephemeral; it is not a public DTO,
checkpoint, transaction field, or verifier result.

The Finalizer provenance producer reads canonical bytes from
`extension_source_checkout` but does not invoke the full preset installer and
does not mutate the source checkout. It may write only the installed manifest
in `target_reviewed_checkout`. The existing field allowlist remains closed.
Self-hosted postimage source ref/commit bind `reviewed_content_head`; installed
postimage repo/ref/commit retain the selected immutable extension identity. A
tail, when required, has one parent equal to target `reviewed_content_head`,
changes only `.trellis/guru-team/extension.json`, and is the unique valid
publication child. An installed manifest that already satisfies its immutable
source binding requires no tail and remains published at the reviewed head.

## Review Gate Artifact

`review-branch.sh` writes compact schema 7.0 `review-gate.json` at the exact
task-owned ignored-runtime checkpoint after the independent semantic judgment
exists. The gate
contains only schema/skill identity, task/mode/review intent, typed exit,
`review_commit`, `reviewed_content_algorithm`, `reviewed_content_sha256`,
`base_ref`, normalized semantic
candidates/findings, minimum independent reviewer/evidence facts, and
`facts_sha256`.

The gate deliberately omits a second conclusion rollup, changed-file/diff
copies, command argv, deployment projection, assignment
continuity and report digests. The consumer derives Git/range/task facts from
live state and validates the compact semantic result. A resolved finding keeps
its original `introduced_head`, records the fixing commit as `fix_head`, binds
the later transient closure as `closure_head`, and uses `review_commit` for the
distinct fresh-final range. Ancestry across those anchors proves normal
finding-fix closure. `passed` after any resolved finding requires
`review_intent=fresh_final_review` over the complete current range.

The gate is valid only while `guru-reviewed-content-1.0` recomputes to the
stored `reviewed_content_sha256`; excluded task/publication/finalization metadata
may change without changing that identity. `review_commit` remains the Git
anchor for review range and finding ancestry. `review_source` must be
`independent-agent`; main-session/self-review identities are rejected. Any
non-current gate shape fails closed. Enforcement lives in
the package-local recorder, checker, and public wrapper.

The recorder returns only a minimal receipt. The checker resolves the exact
checkpoint from task identity, and the public wrapper accepts only current
public input before rerunning that checker. Successful `passed`,
`continuity_passed`, and zero-payload stop `blocked` projection retires the
checkpoint; active re-entry routes retain the same checkpoint for deterministic
same-owner re-entry. No public DTO
or caller-authored invocation contains the private gate.

Before `task.py archive`, `prepare_closeout()` fixes both the active and future
archive locators. The active task remains the task-local boundary until the
single archive metadata transaction moves it to the prevalidated archive
locator. Validators may accept gate digest entries that still use the active
locator when the projected archived files have matching bytes; no artifact is
rewritten after the archive move.

The future locator must not already exist when prepare builds the plan. The
archive root, month, and final destination are lexical components: every
existing component is inspected with `lstat`, any symlink including dangling or
repo-internal targets is rejected without following it, and the same check is
repeated immediately before official move.
`task.json.children` uses the official missing-as-empty convention but must
otherwise be `list[str]`; active children found by official exact/suffix lookup
block only when their `task.json` would join the archive mutation, while archived
children remain valid historical references.

## Current Finalizer Transaction

Current Finalizer transaction schema `guru-finalization-transaction-3.0` is an
owner-private, task-scoped ignored-runtime contract named
`finalization-transaction.json`. It is persisted before the first remote
mutation so the same owner can distinguish its own pushed state from an
out-of-order caller mutation, including after an interrupted process.

The closed transaction contains only:

- schema/skill identity, `ordinary_publication|existing_pr_recovery` mode, and
  task/repository/base/branch identity;
- `branch_review_commit`, `publication_head`, exact PR title/body, and the next
  deterministic transition;
- exact `pre_push_remote_head` while `next_transition=push_content`, using an
  empty string for an absent ref and a full commit OID for a historical baseline;
- optional canonical PR number/URL after ordinary Draft creation;
- recovery-only canonical adopted PR number/URL, original Draft/Ready state,
  and exact pre-push remote HEAD, retained through every transition.

It never stores live Git/GitHub/Trellis snapshots, reviewed path inventories,
archive projections, finish-summary templates, semantic review history,
authorization, command argv/output, retry history, timestamps, or digest
bundles. Preview and executor reread live authority and compare it with these
minimal immutable inputs immediately before mutation.

Recovery requires one unique non-fork Open PR on the exact repository/head/base.
The PR and remote HEAD must agree. Fresh adoption requires a strict Git ancestor
of `publication_head`; equality is valid after the exact pre-push HEAD and
publication HEAD are bound by the same recovery transaction, or while one exact
current `ordinary_publication/push_content` transaction remains unbound and the
remote, PR and Publication HEADs already equal. In the latter case preview keeps
the live title/body bytes, field-equality facts and convergence decision;
execute rereads them, converts the same schema 3.0 transaction to
`existing_pr_recovery/bind_pr`, and persists the original comparison and
decision in its additive private `adopted_pr` binding before any PR, archive or
Ready mutation. Existing strict-ancestor transactions without those additive
fields remain valid, while an equal-HEAD `bind_pr` resume requires internally
consistent fields and accepts only the original bound metadata or, when the
decision required convergence, an exact current Publication payload left by a
successful edit before the interrupted transaction advance. The converged retry
performs no second edit; every other metadata state fails closed. No second
transaction, publication push or PR create is permitted. Fresh equal-HEAD adoption without
this owner transaction remains invalid. The current Publication payload effect
must equal the live PR body effect before metadata mutation. Current Publication
title/body is the only convergence authority. Any identity, effect, payload, original state, ancestry,
archive, or transaction drift fails closed. Schema 2.0 remains immutable at its
explicit versioned path and cannot adopt an existing PR.

Schema 3.0 also supports one current-plan rebind without adding fields or
stages. The predecessor must be unbound
`ordinary_publication/push_content`; task, repository, base/head branch,
Publication payload and PR body effect remain exact; predecessor Publication HEAD
equals live remote/PR HEAD; and current reviewed/publication HEAD is its single
direct-child manifest-only provenance tail under the existing validator. The
replacement is written once as current-plan
`existing_pr_recovery/push_content`, retaining the predecessor remote HEAD in
`pre_push_remote_head` and `adopted_pr`, before the exact new Publication HEAD
is pushed once. Non-provenance plan drift and the existing equal-HEAD
`push_required=false` conversion retain their prior contracts.

The same schema and transaction route support one composed descendant: legal
base evolution followed by one direct-child provenance metadata tail. The
current tail is accepted only by `provenance_tail_commit_errors()` against its
Git-derived direct parent; the existing base-evolution ancestry and exact
binary-delta comparison then treats that validated parent as the current
endpoint. Pure base evolution still compares through the current Publication
HEAD, and direct-tail recovery keeps its existing path. Only the composed
base-evolution-plus-tail topology may carry current Publication title/body
different from the predecessor payload and delegate it to existing metadata
convergence; pure base evolution plus Publication drift remains invalid. No
manifest-path diff filter, parallel drift authority, arbitrary tail sequence,
field, stage, or public projection is added.

Schema 3.0 also accepts one direct fresh-reviewed descendant after those legacy
classifications fail on provenance shape. The current Branch Review comparison
commit is the current Publication HEAD, descends from both predecessor
Publication and the evolved selected base, and does not already contain that
selected base in the predecessor lineage. Fresh Branch Review and Publication
identity provide the reviewed Task Commit authority without a changed-path
heuristic. The unique Open PR and remote must agree on a commit descended from
predecessor Publication and strictly ancestral to current Publication; only
this classification permits that exact pre-push HEAD to differ from predecessor
Publication. The same `existing_pr_recovery/push_content` transaction records
the classifier's pre-push remote HEAD before mutation. No DTO, mode, stage or
schema field changes.

After the exact recovery transaction binds its PR and advances to `archive`,
`push_archive`, or `mark_ready`, it is the current stage authority. Preview
validates its complete minimal identity before applying any pre-PR provenance
inference; the persisted original metadata remains decision evidence, while
current Publication and live reread own convergence. A matching transaction
resumes its recorded transition, while a mismatch fails closed and cannot fall
back to fresh adoption or reprepare.

Archive commit/push may complete before a Draft-to-Ready call returns. In that
normal interruption window the archived task and owner transaction retain
`archive` or `push_archive`; same-plan recovery validates the archived task,
bound PR's recorded initial Draft/Ready state, and local/remote/PR HEAD
equality, performs only Ready, then
persists `mark_ready` and retires owner state. It never repeats archive or PR
creation.

`ready_for_merge` deletes the transaction, Finalizer gate/request and every
superseded Finalizer-owned file. A
`blocked` route retains a transaction only when the declared same-owner recovery
input schema requires it; otherwise it deletes owner state. The official archive
never moves or retains a transaction. Durable `finish-summary.json` remains only
the minimal archived change-context index/summary and PR identity.

The post-cleanup public projection accepts only the exact retired gate locator
previously emitted for that task. Because the private gate and transaction are
already absent, it reconstructs the executor marker from the committed archive
terminal authority and requires current local/remote/Ready PR HEAD to remain the
exact reviewed archive metadata commit. It revalidates that commit's active-task
deletion, five-file archive tree, reviewed-content continuity, canonical PR,
three-way HEAD/branch identity, Publication payload effect and the declared output
schema. Wrong or unsafe locators, a transaction without its gate, incomplete
archive identity, or any live drift fail closed; the projection does not revive
Publication authority or repeat a mutation.

## Current Source Verification Result

The verifier current input profile is only `source_repository_verification` in
standalone mode. Its immutable identity binds `castbox/guru-trellis`, remote,
requested ref, resolved current HEAD and selected capability profile. Current
public exits are only `verified|blocked`; neither projects to Finalizer.

The private result schema `guru-extension-installation-verification-result-5.0`
contains source identity, semantic result, explicit unverified boundaries and a
session reference. It is ignored source-session runtime, deleted after direct
standalone consumption, and never written below `.trellis/tasks/**`. Legacy
task-bearing verification schemas, including the immutable result 4.0 bytes,
remain compatibility assets only and are absent from current inventories. The
current semantic input requires `applicability.status=required`; explicit source
intent cannot route through `not_required`.

## Current Task Commit Authority

Candidate 5.0 removes branch classification and publication-state eligibility.
A current exact commit request authorizes only the matching action in the
conversation. Without that request, the Skill asks once after displaying the
exact repo, ref, HEAD, paths, and message. Branch name, role, protection,
sharing, other-task ownership, remote branch presence, and PR state neither
grant nor deny authority and are not read as commit preconditions. Task/HEAD,
Phase 2, snapshot, exact staging, message, Git operation state, and unrelated
preservation still fail closed. Authorization is never persisted.

An unfinished 4.0 owner-private candidate is not converted or supplemented. It
is rejected or removed and the owner fully reprepares candidate 5.0 from current
Phase 2 and live Git evidence.

## Current Merge Gate And Results

`guru-merge-task-pr` owns one ignored-runtime semantic gate. Active public input
2.0 binds canonical repository/PR identity, expected head SHA, reviewed
base/head branches, the exact Publication-reviewed external-work-item effect,
and one reviewed merge message. Finalizer keeps its
1.0 `ready_for_merge` output unchanged; the Merge semantic owner authors the
message fields in the target-owned consumer input before the gate. Input/gate
1.0 schemas and examples remain immutable compatibility inventory and are not
selected by the current Interface or runtime.

The gate records those minimal authorities together with live facts, the
pre-merge base head, reviewed-message digest, selected repository merge method,
passed AI dimensions, selected route and the minimal executor marker. Subject
must exactly equal `chore(merge): #<pr> 合并 #<primary-issue> <中文摘要>`; the
subject, summary, and body must contain no Issue close-keyword reference at any
position, and the body uses the fixed `合并/范围/审计/PR/Refs` contract. Live PR
body/base/head values are evidence to compare, never the
source of reviewed authority. Authorization remains dialogue-local.

The deterministic executor writes the exact reviewed body to ignored
`task-pr-merge/<identity>/merge-body.md`, uses repo-bound `gh pr merge` with
`--match-head-commit <expected-head-sha> --merge --subject <subject>
--body-file <path>`, and removes the body file after success, failure or
terminal recovery. It then rereads the PR, merge commit, expected base ref and
Issues. Post-merge verification requires merge SHA equality, parents exactly
`[pre-merge-base-head, expected-head]`, exact subject/body bytes, correct PR and
primary-Issue refs, remote base at the merge SHA, and the existing Issue closure
timing contract. `merged` carries only PR URL/number
and merged commit identity. `merge_blocked` carries a closed reason/remediation.
`closure_mismatch` carries merged PR identity plus exact Issue mismatches. The
executor never calls Issue-close APIs, updates/rebases the PR branch,
synchronizes local `main`, or cleans task resources.

## Current Finalization Transaction

Publication produces the exact reviewed PR title and body for one current task.
Finalizer combines that DTO with live task, Git, remote, and archive facts to
build an invocation-local finalization plan. The plan is validated and hashed
in memory; it is not written into the active task or archived task.

Before the first remote mutation, Finalizer persists only the minimal ignored
`finalization-transaction.json` needed by the next transition. It binds the
current task and repository identity, base/head branches, reviewed and
publication heads, exact Publication payload, transition state, accepted
pre-push remote head, and optional bound PR identity. It contains no user
authorization, semantic-review history, live scan transcript, archive
projection, or Issue-scope aggregate.

The current archive contains exactly the durable files that exist from
`task.json`, `prd.md`, `design.md`, `implement.md`, and
`finish-summary.json`. Planning, Phase 2, Branch Review, Publication, and
Finalizer checkpoints remain ignored runtime state and never enter the archive.
Every tracked move requires active deletion plus archive addition with exact
blob continuity. `finish-summary.json` is the only generated archive output and
is validated before the archive move.

Current recovery is transaction-bound. An active task resumes from the exact
ignored transaction and live PR/remote state. After the archive commit, recovery
uses that transaction plus committed `task.json` and `finish-summary.json`
authority. If neither current transaction nor terminal committed authority is
available, Finalizer fails closed. Removed task-local plans, old DTOs, and old
tasks have no migration or compatibility route.

Publication alone decides the external-work-item effect from current authority.
A complete default-branch delivery normally emits a closing keyword; an
explicit post-merge validation, observation, publication, or incomplete-delivery
requirement remains reference-only; no external work item emits no Issue
reference. A PR targeting a non-default branch is reference-only, and a later
Publication for the default-branch integration decides the effect again.
GitHub executes any closing keyword when the relevant PR reaches the default
branch. Finalizer preserves the reviewed body exactly, and Merge only verifies
the resulting live effect; neither closes an Issue through an API.

## JSON and Text Encoding

All JSON artifacts should be UTF-8, formatted with two-space indentation, and
written with `ensure_ascii=False` because Chinese summaries and evidence are
first-class data.

Validate JSON assets with:

```bash
python3 -m json.tool trellis/index.json
```

## Common Mistakes

- Adding a config key to `config-template.yml` without adding a default in
  `DEFAULTS`.
- Adding an alternate task identity reader instead of using current
  `task.json`, ignored runtime mapping, and live Git worktree facts.
- Letting Finalizer or Merge re-decide Publication's external-work-item effect.
- Recording review-gate evidence that does not mention deployment impact.

## Skill Evaluation Data Contracts

The optional `run-skill-evals --codex-model` execution setting is Codex-only and
applies only when the corpus does not pin a model. The existing `model_id` field
may therefore occur on a Codex post-owner adapter request. Corpus schema rules
and pinned semantic-authoring/qualification models do not change. The request
and actual native argv record the selected model; it is not semantic evidence.

`public_api.skill_evals` publishes schema id `guru-team-skill-evals-1.0`, native
trace schema id `guru-team-skill-eval-native-trace-1.0`, the four adapter ids,
the closed run-status set, and the repo-relative canonical
schema/adapter roots. `public_api.companion_scripts` publishes
`discover-skill-evals` and `run-skill-evals`. These inventories are additive
extension API; they do not add eval schema ids to production Skill public input,
typed output, or private artifact inventories.

Each closed descriptor contains exact adapter/platform identity, one
package-relative executable basename, one non-empty native command, and the
fixed capability list. Shared resolves its preset-managed native command below
the adapter root; Codex, Claude, and Cursor resolve theirs from `PATH`.
Discovery may report current
`native_available` as a live machine fact. The request remains byte-identical
across adapters; platform-specific argv/context and native output envelopes are
private adapter execution details retained through the transcript locator. The
native trace locator identifies a repo-external closed receipt whose events are
bound to the minimal native request digest, public projection root, exact
Skill/wrapper digests, request-bound reads, and one exact projected wrapper
invocation. The native request contains only projection/workdir/prompt/files/
invocation locators; canonical package, corpus, adapter request, and private
runtime locators stay runner-private. The closed adapter request carries the
runner-resolved public runtime target; every side in one comparison receives
the same value, and no native request, context, argv, projection, receipt, or
boundary client contains that locator. The receipt is not public Skill I/O or
a semantic verdict.

The corpus schema, semantic grading input, human feedback input, adapter
request/response, native trace, and run evidence are separate closed contracts. The corpus
contains references and expectations but no output-schema/private-artifact
locator. Its optional `native_execution_mode` is closed to
`post_owner|semantic_authoring`, with omission equal to `post_owner`.
`native_execution_adapter` and `model_id` are mandatory for
`semantic_authoring` and schema-invalid in every `post_owner` case. Semantic
grading contains exact comparison-side/case/assertion identity
plus an external verdict; human feedback uses comparison-side/case identity and
cannot carry a grader verdict. Run evidence
contains only corpus/interface/package/platform/adapter/comparison identity,
actual exit, assertion results, status, transcript locator, timing, and
feedback. It forbids gate/checkpoint/audit/release/provenance fields.

Neither adapter request nor native request carries `expected_exit`.
`post_owner` case files may carry exact wrapper arguments referencing a
repo-local checker-passed owner result, but never a caller-selected route.
`semantic_authoring` instead exposes only the public input and permitted
repository evidence to the contract-designated Agent, which authors the
owner-result envelope and calls the formal wrapper without a host-prepared
semantic result. Full runs execute every `post_owner` case for every adapter and
only the `semantic_authoring` cases declared for that adapter; focused adapter
mismatch remains an explicit `unsupported` result. Aggregate evidence is valid
only when actual case ids exactly equal the independently derived declared
applicable set, with missing, duplicate, unknown, and unexpected ids rejected.
Actual wrapper output selects the per-exit schema before the runner performs the
independent expected-versus-actual assertion.

`native_authoring_flow`, when present, is exactly `standard_intake` and requires
`native_execution_mode=semantic_authoring`. Its direct consumers are the eval
runner, native adapter, facts-only staging, and flow trace validator. It is not
a production Skill input, output, owner state, or authorization field. Existing
single-Skill authoring and post-owner cases retain their own trace contracts.

The standard Intake flow records each declared command's actual input/output
identity and the terminal public producer in eval-private trace evidence. The
terminal producer's current interface, not the corpus-owning package, defines
the schema for its unchanged output. The Agent-visible projection contains
the participating public contracts, declared consumer projections, and source
facts; it excludes expected exits, semantic verdicts, private runtime, and
host-prepared owner or prerequisite results. Actual public outputs bind the
next public inputs without a producer-private payload handoff. Flow case ids
remain subject to the same declared-versus-actual aggregate completeness rule.

For `standard_intake`, model-visible assets are an explicit minimal set, not a
directory-copy policy. Schemas and command boundaries are distinct from sample
answers: no Interface input/output/error example reference adds a visible
artifact. The helper and trace use that same declared read set and reject
examples, eval controls and private runtime.

Intake transcript assertions consume the existing semantic-grading 1.0 rows
by comparison side, case and assertion identity. Completed focused or full/mixed
runs containing declared `standard_intake` cases retain their entire original
applicable case/side set. Grading must match exactly the Intake assertions only;
non-flow grading rows are rejected. Only Intake semantic results/status and the
derived aggregate may change; all non-flow fields and raw execution evidence
remain unchanged. Runs with no Intake cases keep their existing lifecycle.
The completed run root can be graded by the original runner after independent review of its actual
transcript. No new public DTO, grading field, hidden summary token or long-lived
ledger is introduced. The runner checks existing request/corpus/execution
identity and preserves raw execution evidence while updating only semantic
results and aggregate status. This associates grading with the selected
completed execution; it does not claim a new grade-to-transcript byte digest.

## Branch Review Data Boundary

Branch Review aggregate public input schema 5.0 dispatches three independent
profiles, including read-only `archived_review` schema 1.0. The original
`branch_review` schema 2.0 profile contains workflow/standalone
mode, task/base/`branch_review_commit` identity, and one of
`initial_review|fresh_final_review`. The current-only `base_continuity` schema
2.0 profile separately binds the prior complete `branch_review_commit` and the
current committed reconciled `task_head` to one bounded old-base/new-base
candidate and the `base_continuity` intent. The complete Interface's public
outputs are the six minimal DTOs, including `archived_review_passed`,
defined by the Skill package contract. `review_ref`, finding refs, proposal
refs, and continuity identity are opaque consumer identities, not embedded
artifact bodies.

After a fix commit, finding closure is an internal transient AI judgment by the
finding owner or a real unfinished-agent replacement. It has no public exit or
artifact and automatically dispatches a distinct fresh reviewer. Current gate
schema 7.0 accepts the intent allowed by the selected current profile and, for
continuity, records the prior complete review commit separately from the current
`review_commit`. Aggregate input schema 3.0 and gate schema 6.0 or older remain
legacy stale inventory, not current runtime authority; any non-7.0 gate fails
closed.

Only `review-gate.json` is written for a new review. It contains a non-empty
terminal-only `candidate_classifications` set. Each row binds `candidate_ref`,
one of the three qualified or four rejected terminal decisions, the six-part
normal-scenario witness, and `consumer_use=branch_review_route_checker`.
Duplicate refs, a scope-confirmation/mechanism/blocked decision, or any
qualification result/checkpoint locator fail closed. A reviewed candidate has
exactly one of `qualified_finding`, `scope_proposal`,
`observation`, `followup_candidate`, or `rejected_candidate`.
`qualified_finding` alone carries P0-P3 severity and must bind the current
`candidate_ref`,
`introduced_head`, `fix_head`, `closure_head`, and closure evidence. `scope_proposal` uses
no severity and never selects an implementation route. Every semantic
disposition row binds one candidate from the same gate.

## Publication Readiness Gate

Ignored-runtime `pr-readiness.json` is the only publication readiness gate.
Current-only schema `guru-task-publication-readiness-5.0` stores only
`schema_version`, `skill_id`, `task_ref`, `branch_review_commit`,
`reviewed_content_sha256`, exact `pr_payload(title,body)`, a non-empty
terminal-only `candidate_classifications` set, all ten AI-reviewed dimensions, findings/closure,
scope/Docs/safety conclusions, and the selected route. Finding summary, scope
basis, evidence refs, affected artifacts, and closure evidence are non-empty.
The eight objective entry
preconditions and shared Finalizer preflight are rebuilt transiently by the
recorder/checker; their digests, Branch Review checkpoint, publication identity,
reviewer process, and confirmation evidence never enter this private
checkpoint. The payload is present because the wrapper is its one direct
consumer, not as a durable audit artifact.

`ready`, `return_to_task_work`, and `blocked` share this one artifact and a
closed exit/consumer union. Stale re-entry rereads current facts and replaces
only the Publication owner's checkpoint after delta-scoped semantic review; it
does not carry a supersession identity or re-entry narrative.
Every `ready` entry binding, dimension, and scope/Docs/safety conclusion is
`passed`, and every finding is closed. `return_to_task_work` requires an open
`task_work` finding bound to a `finding` dimension and has no blocked dimension
or conclusion. `blocked` requires an open `external_blocker` finding bound to
a `blocked` dimension and at least one blocked conclusion. All open findings
reference non-passed dimensions, and an open metadata-revision finding cannot
escape the internal rereview loop through an external exit. A
checker-reproducible failed precondition may support only an already AI-selected
non-ready route; recorder/checker rebuild it transiently and do not persist the
binding or choose the semantic route. A stale invocation carries only
`task_ref`, `branch_review_commit`, `stale_reason`, and target-authored
profile/mode/review intent. The commit binds the Finalizer projection to the
checked Publication owner while `reviewed_content_sha256` remains private.
Normal content continuity drift is accepted only for an AI-selected
`return_to_task_work` after the commit is proven to be an ancestor of current
HEAD and the shared identity proves reviewed content changed. Invalid or
non-ancestor identities and inspection failure remain fail closed on every
exit; `ready` remains continuity-strict. The public
wrapper reruns the current owner checker; no re-entry narrative or supersession
identity enters the public input, private checkpoint, or exit.
This stale profile never consumes a base-only mismatch. Such a mismatch belongs
to Finalizer's `base_reconciliation_required` output and must pass through the
confirmed local reconciliation commit plus bounded continuity before the
current commit can be supplied to Publication.
Publication `ready` already runs the same side-effect-free Finalizer preflight
that the first preview uses. Finalizer consumes only the checked ready DTO and
never augments or interprets the Publication checkpoint.
After the checked output passes its schema, the Publication producer wrapper
deletes that checkpoint before Finalizer entry; a failed check or projection
retains it only for same-owner repair. Any non-current input or checkpoint shape
fails schema validation.

The Publication AI authors and reviews the exact PR payload in memory, and the
recorder stores it only in the owner-private readiness checkpoint. The wrapper
projects it without byte-changing normalization and deletes the checkpoint only
after output validation. The `ready` output is exactly `exit_id`, `task_ref`,
`branch_review_commit`, `pr_title`, and `pr_body`; Publication consumes either
the complete review's current `passed` DTO or the bounded continuity router's
current continuity-reviewed `branch_review_commit` plus live Git and never
opens the Branch Review private checkpoint. Full review bodies, paths, findings,
histories, and derived bindings stay owner-private or transient.

The ready output schema is
`guru-production-review-task-publication-output-ready-4.0`. Its sole active
consumer is `guru-finalize-task-input-publication-ready-4.0` within aggregate
input schema `guru-finalize-task-input-aggregate-6.0`; the `select` projection
carries `task_ref/branch_review_commit/pr_title/pr_body`, and target-owned
authoring adds `profile/mode`. Legacy 3.0 shapes fail closed and require a fresh
Publication run; no compatibility reader or task-local fallback exists.

## Base Evolution Identity And Private State

Active-task validity has three independent clocks:

- authority binds the live Issue, requirement, Docs acceptance, and confirmed
  scope;
- task content binds planning, code, tests, and docs on the task branch;
- integration binds build, test, and review readiness for one exact
  `(task_head, base_head)` candidate.

A new integration pair does not invalidate the other two clocks. A task-content
HEAD change creates a new pair and prevents reuse of older integration
readiness. Multiple base advances between stable boundaries collapse into one
`old_base...new_base` delta. Non-ancestor base history, a missing anchor, or
ambiguous task/base identity fails closed rather than synthesizing continuity.

The pair guard may read one ignored owner checkpoint containing only the exact
task/base pair, selected exit, `resume_target`, and minimum validation identity
needed by the next consumer. It is neither a public handoff nor durable audit
evidence. The consumer deletes it after successful projection; incomplete
same-owner recovery or replacement is the only reason to retain it. Git and
GitHub facts, semantic scans, candidate directories, full findings, validation
logs, authorization, and cross-chain hash bundles never enter public output or
tracked task artifacts.

For a post-review candidate whose shared reviewed-content identity changes while
task content and authority remain unchanged, the current-only reconcile result
binds the prior complete review commit, expected task HEAD, new base HEAD, and
candidate tree. After current-dialogue confirmation, the deterministic executor
creates one local reconciliation commit. The bounded continuity input then
requires `task_head == HEAD`, prior review and new base ancestry, and exact tree
equality. The prior review remains owner-private gate evidence; its output sets
`branch_review_commit` to the current reconciled HEAD for Publication and omits
the prior commit because no downstream consumer requires it. No authorization,
complete review body, or private checkpoint crosses either public boundary.

Legacy active-task state is adapted once from current package contracts. An
existing same-task-content Branch Review may retain its task review validity,
while any legacy Publication stale reason is classified by its current owner:
base-only mismatch routes to base reconciliation and content/metadata stale
remains Publication-owned. Migration does not rewrite active task artifacts,
read another package's private state, or restore the retired shared dispatcher.

## Closeout Invocation State

Closeout invocation state is package-local, ignored, and bounded to one direct
consumer behind the existing public command. Publication's current full
snapshot is process-local and reused only by its record/check/projection
sequence. Finalizer's preview identity is a dialogue-local confirmation binding,
not authorization evidence; any retained transaction records only the minimum
same-owner recovery state already required by the Finalizer contract. Merge
binds its pre-merge snapshot to repo, PR, expected head, reviewed message,
policy/check facts, PR-body closing effect, and pre-merge base head, then discards it after
terminal projection. No invocation state or compatibility branch creates a
second public wrapper, command authority, or cross-Skill handoff.

Commit may retain a minimal success receipt after the live ref has advanced so
loss of invocation stdout can recover the exact published commit without a
second commit or ref mutation. The receipt binds candidate locator, task, base,
branch, pre-commit head, commit/tree, and commit-message identity; it carries no
review narrative, authorization, timestamp, live repository snapshot, or
cross-Skill authority. Normal consumption removes it together with the
candidate and consumed Phase 2 checkpoint.

Operation-count evidence uses normalized categories for complete authority
reads, record/check/project operations, mutations, recovery inspection,
watcher polls, and post-terminal operations. It is test evidence rather than a
public Skill DTO or durable audit artifact. Wall-clock samples are observational
and must separate Agent orchestration, deterministic command, GitHub API, and
external CI wait.
