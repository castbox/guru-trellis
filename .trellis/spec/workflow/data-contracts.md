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
post-sync digest to the next consumer. Already-equal execution may have equal
pre/post digests; fast-forward execution must not.
Workflow and standalone create no evidence file, lease, release command or
cleanup state.

### Phase 0 Current Transition Family

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
source as `config-candidate`. Discovery and later refresh/workspace boundaries
compare that reviewed provenance with live Git. A changed selected base,
candidate order, remote, clean state, decision/local/remote HEAD, digest, or
authoritative content is real drift and follows the declared refresh route.

Each later stage contains only the prior identity plus fields directly consumed
by its next checker. Complete issue bodies, scan or review history, findings,
owner results, artifact locators, file metadata, process/reviewer data, and
authorization are forbidden. Successful consumption retires the prior in-memory
stage; refresh/re-entry discards stale state and starts from a fresh
`base_current`. Normal pre-task transport is stdin/stdout or caller memory only
and writes nothing below `.trellis/tasks/**`, `.trellis/workspace/**`, or
`.trellis/.runtime/**`.

The invocation contract uses separate closed call-local envelopes for
deterministic sync, semantic owner invocation, and confirmed workspace
mutation. Semantic transport has three distinct domains: caller-owned public
input, exactly one current transition stage, and the current Skill's checked
owner result. That result is never a public DTO or a cross-Skill transition.
Unknown fields, missing or wrong stages, owner/input/target mismatch, stale
identity, or multiple operations fail closed.

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

Schema `guru-change-context-owner-result-2.0` is the closed Draft 2020-12
stdout-only owner-result union whose `typed_exit` is exactly `context_ready`,
`refresh_base`, or `blocked`. It embeds the validator-passed base result and
current semantic evidence needed by the same owner loop, but it is neither a
public handoff nor a tracked task artifact. Normal workflow and standalone
execution transport the result through stdin/stdout and create no task,
workspace, or ignored runtime file.
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
validate schema, digests, base/live facts and reviewed blob identities, and
return canonical JSON or an objective checked exit on stdout. They never
resolve, write, replace, or supersede a task artifact. A base error
short-circuits before live issue/draft, reviewed-blob, or archive-preview reads;
stale evidence reruns the complete owner from live authority without a prior
result chain.

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
interrupted target, or re-entry route. The closed scope-only Ledger 2.0 contains
exactly `schema_version`, `primary_issue`, `close_issues`, `related_issues`, and
`followup_issues`; it does not store the trail. Current planning documents,
context freshness, task-update preimage, re-entry owner facts, and the trail
remain in the transient owner result and are reread from their owning sources.
Pre-task and standalone results remain stdout-only.

A mechanism-only terminal result still requires the same task-local ledger,
planning documents, re-entry owners, and current context evidence in the
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
contracts, and package-local corpora. Sixteen integrated rows select Interface
1.4; normal-scenario qualification selects Interface 1.6; the standalone
verifier selects Interface 1.5. Exact profile, exit,
consumer, projection, current-case, and authoring-edge equality is required.
Eighteen Skills and 73 exits are the current package cardinality regression, not
a hard-coded future registry allowlist; the business workflow independently
asserts 17 invokes, 71 exits, 24 workflow targets, and 18 stop targets.

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
such as `v0.6.5-guru.9`, not namespaced tags such as
`guru-team/v0.6.5`. The tag must correspond to
the exact `trellis/guru-team-extension.json.version` present in the tagged commit,
and the manifest must expose `target_trellis_cli` so users can see which official
`@mindfoldhq/trellis` release this Guru Team extension targets. The repo release
tag and extension revision are independent version axes: release metadata binds
one immutable tag to one exact tagged manifest version rather than assuming their
Guru suffixes are equal. Stable workflow marketplace examples should use
`gh:castbox/guru-trellis/trellis#v0.6.5-guru.9`; unpinned
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
identity and `issue-scope-ledger.json` as the only Guru-owned durable Intake
artifact. Runtime resolves the worktree from current `task.json`, the checkout,
ignored runtime mapping, and live `git worktree list` facts. Any missing or
mismatched identity fails closed; no alternate task identity artifact is read.

Local-only reusable mappings live under the gitignored producer namespace:

- `.trellis/.runtime/guru-team/workspaces/<workspace-slug>.json`
- `.trellis/.runtime/guru-team/tasks/<task-slug>.json`

Runtime cache may contain absolute worktree paths and executor timestamps, but it is disposable, untracked, has no index/developer dimension, and must be reconstructable from current `task.json`, the checkout, `git worktree list`, or explicit parameters. Ordinary task commands read tracked shared config but do not rewrite it.

Query-only `prepare-task` writes neither task context nor runtime cache. Active
`guru-create-task-workspace` is the only creator. On successful workspace/task
creation it writes official `task.json`, exactly one Guru-owned tracked
task-local Intake artifact (`issue-scope-ledger.json`), and ignored
source/target runtime mappings. Upstream checker results and workspace
plan/result stay in ignored owner-private runtime and are reread only by their
direct consumer.

Assignee remains a portable task/context audit field, never a path namespace.
The workspace executor invokes official `common.task_store.cmd_create` in an
isolated subprocess with the reviewed assignee and a call-scoped null developer
accessor. The official creator fallback therefore produces
`task.json.creator=task.json.assignee=<reviewed-login>`. Guru runtime does not
read, copy, initialize, restore, or require `.trellis/.developer` or
`.trellis/workspace/**`; existing official identity bytes remain untouched.

The task-level `issue-scope-ledger.json` exclusively owns `close_issues`,
`related_issues`, and `followup_issues`.

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
`task.json`, Issue Scope Ledger, ignored runtime identity, live Git, archived
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
closeout plan binds repo/base/head, exact title/body, `draft=true`, and its
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
fail closed. Readiness, body, ledger, and verifier remain unopened after the
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
`design.md`, `implement.md`, the Docs SSOT decision, and the issue scope ledger.
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

Schema `guru-change-request-review-1.0` defines the portable
`issue-review.json` result owned by `guru-review-change-request`. Before task
creation the recorder and checker return JSON on stdout only. The normalized
target is exactly one existing issue, side-effect-free proposed draft, or
side-effect-free standalone request, with title/body, identity, content, and
source authority hashes. `prerequisites` contains portable projections of the
full current context, clarification, and wording payloads; `evidence_linkage`
binds target identity/content, base/current/history/duplicate facts, clarity
facts, wording facts, and one canonical digest.

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
Gate, conditional human confirmation, reason, scalar exit, and exact consumer.
`ready` requires all prerequisites current, all dimensions passed, no blocking
finding, complete linkage, passed Gate, and no required confirmation. Every
non-ready result requires at least one AI-authored failed dimension, blocking
finding, and affected evidence. Deterministic commands validate these facts but
never infer or rewrite the exit.

The public package carries only a deidentified example. Planned #112 Skill
`guru-create-task-workspace` may later persist only the exact checker-passed
bytes at the direct active task's tracked `{TASK_DIR}/issue-review.json`; #101
does not create a task, workspace journal, cache, index, sidecar, or tracked
artifact.

The production regression suite must first pass real current context,
clarification, and wording payloads through their record/check commands and
then consume those full results in change-request record/check. It covers wrong
exits, consumer and target/content mismatch, base/current/history/duplicate
drift, and proposed-draft/standalone source-authority mismatch; handwritten
portable projections alone are not sufficient evidence.

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
the complete `guru-task-workspace-result-2.0` `created_issue` variant with
passed executor/checker stages, valid result and binding facts digests, and the
fixed `refresh_review` consumer. Its current issue facts match the plan and its
complete Intake rerun exposes the canonical live existing issue with
`kind=issue`, canonical URL identity, open state, matching update time, body and
facts digests, and null `issue_binding`. Missing or partial provenance is
invalid.

Schema `guru-task-workspace-result-2.0` is a closed ignored-runtime union:

- `created_issue` binds the exact plan and live created issue and can only
  return `refresh_review`; branch/worktree/task/artifact/runtime operations are
  absent;
- `created_workspace` binds branch/worktree/task identity, exactly one tracked
  Issue Scope Ledger path/digest/size/mode, ignored runtime mapping
  projection, trackability, and workspace-boundary facts and can only return
  `created`;
- `no_side_effect` binds a before/after zero-write snapshot and returns
  `refresh_review` or `blocked` according to the AI-authored route. User refusal
  stops before recorder/executor invocation and produces no plan, result, or
  DTO.

The result is never a fifth tracked Intake artifact. Ordinary re-entry may
reuse only exact branch/worktree/task/artifact identity. A mismatch in issue,
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
the completed AI review. Live `task.json`, Issue Scope Ledger, the Phase 2 DTO,
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

## Issue Scope Ledger

`issue-scope-ledger.json` uses current-only schema 2.0 and is scope authority,
not a verification or process journal. Its exact top-level fields are
`schema_version`, `primary_issue`, `close_issues`, `related_issues`, and
`followup_issues`; unknown fields fail closed.

Issue close semantics must be explicit:

- `primary_issue` is intake context and usually the default close candidate.
- `close_issues` are issues the current task fully resolves and may close. The
  array may be empty for a valid refs-only PR; empty means the PR must contain
  no close keyword and merge has no Issue auto-close obligation.
- `related_issues` are references only.
- `followup_issues` are future work and must never be closed by the current PR.

Finalizer `expected_close_issues` and Merge input preserve this exact
zero-or-more set. Schema cardinality must not invent a non-empty requirement:
runtime compares the complete parsed PR close-keyword set with the expected
set, and Merge treats the empty post-merge closure loop as vacuously complete.
For non-empty sets, missing or additional close keywords and any Issue that did
not close after merge remain blocking mismatches.

The ledger never carries verification state, acceptance evidence, proposal
digests, GitHub comment checksums, review metadata, or marketplace state.
Publication and Finalizer reread current Phase 2, Branch Review, Publication,
verification, and live authority facts independently. Publish is blocked when
the current semantic gates do not cover the declared close scope. Existing
enforcement:

- `validate_ledger_for_publish()`
- `build_pr_body()`

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
  "primary_issue": 92,
  "checked_commits": [],
  "errors": []
}
```

When blocked, the command exits non-zero and returns `status=blocked` with
`errors[]` entries that include the commit hash, subject, classified kind
(`work`, `metadata`, `merge`, or `invalid`), and objective validation messages.

`format-merge-commit --json` exposes a `merge_commit` object:

```json
{
  "ready": true,
  "subject": "chore(merge): #91 合并 #92 中文 Conventional Commits 提交规范",
  "body": "合并：\n...",
  "body_file_hint": "<merge-body-file>",
  "expected_head": "<expected-head-sha>",
  "command": ["gh", "pr", "merge", "91", "--repo", "owner/repository", "--match-head-commit", "<expected-head-sha>", "--merge", "--subject", "...", "--body-file", "<merge-body-file>"],
  "errors": []
}
```

The formatter binds the current 40-character pull request head candidate through
`--match-head-commit`; an absent or invalid expected head blocks the payload.
When the pull request number is omitted, the formatter sets `ready=false` and
uses `<pull_request>` as a placeholder; with a real number it returns
`ready=true`.
The single archive transaction commit generated by finalization uses
`chore(trellis): #<primary_issue> 固化任务收尾元数据` and an empty body. There
is no separate readiness/evidence metadata commit.
Commit message payloads must never use close keywords such as `Closes`,
`Fixes`, `Resolves`, `Close`, `Fix`, or `Resolve`; those keywords remain PR
body-only close semantics controlled by Issue Scope Ledger.

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

## Review Gate Artifact

`review-branch.sh` writes compact schema 6.0 `review-gate.json` at the exact
task-owned ignored-runtime checkpoint after the independent semantic judgment
exists. The gate
contains only schema/skill identity, task/mode/review intent, typed exit,
`review_commit`, `reviewed_content_algorithm`, `reviewed_content_sha256`,
`base_ref`, normalized semantic
candidates/findings, minimum independent reviewer/evidence facts, and
`facts_sha256`.

The gate deliberately omits a second conclusion rollup, changed-file/diff
copies, command argv, deployment projection, issue ledger copy, assignment
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
of `publication_head`; equality is valid only after the exact pre-push HEAD and
publication HEAD are bound by the same recovery transaction. The current Ledger close scope must equal the PR close
scope before metadata mutation. Current Publication title/body is the only
convergence authority. Any identity, scope, payload, original state, ancestry,
archive, or transaction drift fails closed. Schema 2.0 remains immutable at its
explicit versioned path and cannot adopt an existing PR.

After the exact recovery transaction binds its PR and advances to `archive`,
`push_archive`, or `mark_ready`, it is the current stage authority. Preview
validates its complete minimal identity before applying any pre-PR provenance
inference; a matching transaction resumes its recorded transition, while a
mismatch fails closed and cannot fall back to fresh adoption or reprepare.

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

`guru-merge-task-pr` owns one ignored-runtime semantic gate. Its public input
binds canonical repository/PR identity, expected head SHA, reviewed base/head
branches and the exact reviewed close-Issue numbers. The gate records those
minimal authorities together with live facts, selected repository merge method,
passed AI dimensions, selected route and the minimal executor marker. Live PR
body/base/head values are evidence to compare, never the source of reviewed
authority. Authorization remains dialogue-local.

The deterministic executor uses repo-bound `gh pr merge` with
`--match-head-commit <expected-head-sha>` and the uniquely selected policy
method. It then rereads the PR and Issues. `merged` carries only PR URL/number
and merged commit identity. `merge_blocked` carries a closed reason/remediation.
`closure_mismatch` carries merged PR identity plus exact Issue mismatches. The
executor never calls Issue-close APIs, updates/rebases the PR branch,
synchronizes local `main`, or cleans task resources.

## Legacy Closeout Plan Compatibility

The remainder of this section documents immutable schema 2.0/3.0 compatibility
assets only. Current Interfaces, registries, workflow markers, manifests,
runtime preparation and archive logic do not select, create, read, move or
retain `closeout-plan.json`. A legacy payload presented to a current route fails
closed unless an explicitly named legacy recovery test consumes it.

Legacy `closeout-plan.json` schema version `3.0` is the immutable machine input
contract shared by the explicit legacy preview and formal-finish selectors. Legacy plans are
untracked active transaction checkpoints that become tracked only in the single
archive commit. One bounded legacy schema 2.0 transaction migration is allowed
only when the invocation also carries a current Publication 4.0 DTO: task,
`branch_review_commit`, title, and every protected transaction fact must match,
and SHA-256 of the DTO body must equal legacy `publish.body_sha256`. Finalizer
then normalizes in memory to schema 3.0, records the legacy plan digest as the
migration predecessor, and rebuilds the current summary template from the exact
DTO body. It never reads `pr-body.md`, `finish-summary-index.json`, a private
checkpoint, or another fallback. Missing/mismatched DTO evidence fails closed
and requires a fresh Publication run. The plan records portable task and
repo/base/`branch_review_commit` identity plus separate
`git.reviewed_content_head` and `git.publication_head`,
protected input SHA-256 values, reviewed paths and close scope, exact draft PR
inputs, marketplace applicability and artifact locator, future archive
projection, and the fixed transition list.
It never records tokens, absolute worktree paths, a real PR URL, verifier
output, or archive commit SHA. Its projection does record a fixed sentinel PR
URL/ref and the complete schema-valid finish-summary template so all local
summary errors are known during prepare.

`review.changed_paths` is rebuilt deterministically from the task's pinned base
commit through `branch_review_commit`; compact gate schema 3.0 does not carry a
duplicate `changed_files` inventory. The rebuilt list is the single input to
closeout review reporting, marketplace candidate-surface classification,
archive retention, and finish-summary changed paths.
`review.close_issues_reviewed` is projected from the publication-validated
`issue-scope-ledger.json.close_issues`, not from removed compact-gate scope
fields.

`git.repo` is the normalized `owner/repository` identity. All effective fetch
and push URLs of `git.remote` have a raw/effective two-layer contract. Raw
`remote.<name>.url`, optional `pushurl`, and every `url.*.insteadOf` /
`pushInsteadOf` base/pattern are read with NUL value boundaries plus origin.
They reject empty/ambiguous records, leading/trailing whitespace, all control
characters, unreadable origins, and NUL bytes in relevant config files;
missing `pushurl` reuses the raw `url` set. Effective output is never trimmed,
must preserve raw-source cardinality, and after Git rewrite must use
credential-free `https://github.com/...`,
`ssh://git@github.com/...`, or `git@github.com:...` transport and normalize to
this value. HTTP, `git://`, `file://`, relative/absolute filesystem paths,
scheme-less host/path forms, userinfo/password/token variants, explicit ports,
query strings, fragments, and extra path segments are invalid. The repo
identifier normalizer is not a remote URL parser and must never be used as a
fallback for effective remote values. Every queried PR must include
`headRepository.nameWithOwner`,
`headRepositoryOwner.login`, and `isCrossRepository`; the first two must agree
with each other and with `git.repo`, while `isCrossRepository` must be false.
Missing/unknown fields or a same-name fork candidate fail closed before PR
cardinality, final-summary binding, archive, recovery, or ready transition.

`publish.title` and `publish.body` are the exact Publication-reviewed payload
used by active recovery, `gh pr create`, unique draft reuse, final projection,
and archived recovery. Leading/trailing whitespace, trailing newlines, and
Markdown-sensitive spaces are identity data; validators never trim or add a
newline before comparing the remote PR body. The canonical plan digest binds
the complete payload, so there is no separate body-file locator or body hash.

The archive retains only durable files present from this seven-file set:
`task.json`, `prd.md`, `design.md`, `implement.md`,
`issue-scope-ledger.json`, `closeout-plan.json`, and `finish-summary.json`.
Marketplace verification is the only optional eighth archive file. Planning,
Phase 2, Branch Review, Publication, and Finalizer checkpoints remain ignored
runtime state and never enter the archive.

`projection.move_paths` is the complete task-relative filesystem set moved by
the official archive command. On every prepare and same-plan recovery,
`projection.tracked_move_paths` is rebuilt as the intersection of `move_paths`
and the live Git index; each item requires an active deletion and archive
addition in the one archive transaction. `projection.untracked_archive_outputs`
is the exact complement, and `finish-summary.json` remains its required current
member. Current preparation never adds `closeout-plan.json` to either class.

When the live index still tracks a historical `closeout-plan.json` but the
working-tree file is already deleted, the current private projection places
only that path in `projection.retired_tracked_paths`. This closed set is
disjoint from move, retained, required, untracked-output, and reviewed-binding
sets. Its sole consumer is the archive transaction: the parent must contain one
exact regular blob, the working tree and archive must omit it, and the archive
commit must contain its active-side deletion. Re-materialization, replacement,
missing parent continuity, archive retention, or any additional retired path
fails closed. Historical schema files remain immutable compatibility assets;
the retired file is never restored or copied into a current archive.
An already post-bind transaction may replace its predecessor plan digest with
the current retirement-projection digest only when the predecessor digest equals
the deterministic reverse projection with `closeout-plan.json` restored to
`move_paths` and `tracked_move_paths`, every non-digest transaction field is
exactly equal, and `retired_tracked_paths` is exactly this singleton. Any other
shape-valid digest mismatch fails closed.
Preview performs the side-effect-free projection; executor persists it before
the next mutation. Any payload, scope, PR, HEAD, stage, or additional path drift
still fails closed.

`projection.reviewed_tracked_bindings` is the sorted, unique, closed set of
tracked move paths whose current regular-file bytes or mode differ from the
`branch_review_commit` blob. Each row contains exactly task-relative `path`, Git
`mode` (`100644` or `100755`), and content `sha256`. Duplicate, out-of-set,
missing, stale, or unnecessary rows fail closed. A tracked legacy
`closeout-plan.json` is the self-referential exception: its canonical schema and
`plan_digest` bind its bytes instead of a recursive content row on an explicit
legacy route. Current retirement instead excludes it from reviewed bindings and
proves its deletion through the parent blob plus exact archive transaction
path/tree continuity.
`projection.migration_predecessor_plan_digest` is either `null` or the exact
digest of the one legacy schema 2.0 plan normalized into the current immutable
plan under the Publication 4.0 match rules above. It is set only by that
controlled no-retired-file migration, preserved only across same-month
rebuilds, and cleared by cross-month reprepare. A marketplace
verification owner `plan_ref` may match this predecessor only while
`marketplace-verification.json` is itself present in the exact reviewed tracked
binding set; shape-valid but unrelated historical digests remain stale.
An interrupted archive or active-move state written by the immediately
preceding schema 2.0 runtime may have reviewed bindings but no predecessor
field. Recovery validates that immutable legacy shape only as migration input
alongside the current Publication DTO; it never reopens retired files or rewrites
an archive commit. New and normalized active plans always emit the complete
current projection.
The projection also stores `summary_template`,
`summary_template_sha256`, the sentinel PR identity, and the exact runtime
fields that may change. The sentinel uses the
maximum-width positive 64-bit number so replacing it with a real PR number
cannot introduce a new string-length validation failure.

`summary_template_sha256` hashes the exact UTF-8 `write_json` encoding: two-space
indentation, `ensure_ascii=false`, and one trailing newline. Active final
projection requires that exact byte encoding, then normalizes the two PR
runtime fields back to the sentinel and compares the template digest before
the official move. Archived recovery proves continuity through the exact
path/commit/blob transaction and never reparses the summary.

`plan_digest` is the SHA-256 of canonical JSON with `plan_digest` omitted.
Dry-run returns the complete plan and digest. The Finalizer passes that digest
internally to formal execution; the user confirms the already displayed exact
side effects and never repeats a digest, SHA, or branch. A mismatch or protected
input drift fails before push or file writes. Formal schema 3.0 writes the exact
plan as its active transaction class; Publication readiness
and the Finalizer gate stay ignored runtime and are not plan inputs, move paths,
or archive files. Before draft binding, partial retries derive the next missing
transition from the active plan, `branch_review_commit`, marketplace owner
evidence when applicable, live Git/GitHub facts, and the active/archive layout.
The scope-only ledger is never augmented or used as verification state.

`git.reviewed_content_head` equals `branch_review_commit` and remains the
semantic review/content anchor. `git.publication_head` is either that same
commit or its single validated provenance metadata-tail child. The tail may
change only `.trellis/guru-team/extension.json` fields `installed_at`,
`source.ref`, `source.commit`, `source.tree_state`, and
`source.is_mutable_ref`; it must bind a detached clean canonical preset apply
to the reviewed HEAD. The archive transaction parent, pushed remote branch,
PR expected head, and verifier target checkout use `publication_head`.

`task.archive_locator` uses the same live `YYYY-MM` that the unmodified official
archive command will use. Formal checks it before the first side effect and
again immediately before official move. If the month changes while a schema 3.0
task is still active, dry-run rebuilds only the active plan with the
new archive-derived values and a new digest, then the same Finalizer loop reviews
and confirms it. No evidence/readiness commit, history rewrite, verifier rerun,
or alternate archive relocation occurs.

`inputs.official_after_archive_hooks.sha256` binds the canonical empty command
state parsed by the official Trellis config parser. Missing or empty
`hooks.after_archive` maps to `{"commands":[]}`. Non-empty, ambiguous,
unreadable, invalid-byte, or symlinked config has no valid digest because
prepare rejects it without executing any hook command.

When marketplace verification applies, the plan binds the task-relative
`marketplace-verification.json` locator. Finalizer consumes only a current
checker-passed verification owner result and validates the independent artifact,
repository, remote ref, `branch_review_commit`, and local/remote reviewed-content
identity. It never writes verification state into the scope ledger. Missing,
duplicate, altered, path-bound, or stale verification evidence fails closed.

Before PR creation or archive, stale/dirty installed provenance may select the
single mapped `reprepare_required` route. Its gate retains a private marker
until the deterministic executor prepares one metadata tail in an isolated
detached checkout and retires the old owner-private plan, Finalizer gate, and
verification request. A pre-#191 schema 3.0 plan without
`reviewed_content_head/publication_head` is eligible only when its exact
`verification_required` gate/request remain owner-private and current, every
task/repository/remote/base/head identity matches the prospective current plan,
the task is active and unarchived, no PR or parallel consumer exists, the old
reviewed head is an ancestor of the current reviewed head, and the remote branch
is a fast-forwardable ancestor. Publication checks those facts without mutation;
only the checked Finalizer transition retires state, creates or reuses the tail,
and persists a minimal ignored Finalizer transaction containing the exact
publication payload and recovery stage. Archive-month reprepare
changes no HEAD and retains its complete current DTO. The public DTO carries
exactly task, reason, `branch_review_commit`, and `publication_head`; the next
preview validates current HEAD and the optional single-tail parent/allowlist
contract against the rebuilt plan. PR already
created, archive started, reviewed content/scope drift, non-fast-forward remote,
or manifest changes outside the allowlist remain fail-closed boundaries.

An unused current schema 3.0 plan with the complete seven-field Git identity may
use the same mapped base-evolution route without a legacy gate/request. Its
recorded provenance tail must remain structurally valid, its publication head
must be an ancestor of the new reviewed head, and the remote branch must remain
at or before the predecessor reviewed-content head. A remote at the predecessor
publication tail or any later descendant proves an outbound publication side
effect and fails closed. The task and plan remain active, unarchived, and
untracked, with no PR, verification artifact/request, or preexisting Finalizer
gate. The initial current `publication_ready` DTO supplies
the exact reviewed `publish.title/body` for the base-evolution candidate and may
differ from the predecessor plan. The four-field `reprepare_required` DTO does
not grow payload fields. Only after the executor retires the predecessor and
persists the minimal transaction does `reprepare_preview` rebuild the replacement
plan from that exact immutable publication payload. Recorder writes the ordinary
`task-finalization-gate.json`; checker/executor may privately admit only that
byte-identical checked gate while rerunning the preflight.

The pre-#191 base-evolution route temporarily has two same-owner, same-schema
ignored gate instances with disjoint direct uses: the normal
`task-finalization-gate.json` remains the exact legacy verification evidence,
while `task-finalization-transition-gate.json` contains the current semantic
executor marker. Recorder never overwrites the former. Checker/executor require
both, reject the transition gate on every ordinary route, and successful
supersession retires both together with the exact old plan/request. Neither gate
is public, tracked, archived, or a replacement handoff DTO.

Before the exact archive commit exists, archive recovery accepts only the
complete mixed no-renames working-tree path set: both sides for every tracked
move and archive-only for every untracked output. Schema 2.0 validates exact
dirty/staged paths, `branch_review_commit` ancestry and content identity, active
absence, archive completeness, tracked blob continuity, and the official
`task.json` delta before it may create the single archive commit. Missing or
mismatched transaction state keeps this metadata recovery path fail closed.
After the exact archive commit exists, workspace-boundary recovery requires
`closeout-plan.json` to belong to `move_paths` and to exactly one of the same
tracked/untracked projection classes. A tracked migrated plan is therefore a
valid committed recovery anchor for an interrupted Draft-to-Ready transition.

Before official move, the same continuity contract applies to the active task:
the index has no staged changes, dirty paths equal the plan-owned output set,
every move path is a regular file, and tracked Git modes are `100644` or
`100755`. Each tracked file must either equal its transaction-parent bytes and
mode or exactly match its reviewed binding; the tracked plan must equal its
canonical immutable bytes. Verification fallback uses the same set: existing
untracked outputs plus existing binding-matched tracked metadata and the
canonical tracked plan. Extra dirty paths or binding drift fail closed.
Metadata intermediates selected by archive pruning are validated and moved
under this contract before they are explicitly pruned. This gate also rechecks
the live archive month and empty official hook state.

When current `HEAD` is the exact planned archive commit, both normal archived
tasks with context and plan-only damaged tasks load the plan from that commit
blob and validate only the immutable plan and Git parent/path/tree/blob lineage.
Archived working-tree deletion, content tampering, and the resulting dirty
paths are ignored; recovery may only push that exact commit when needed, check
remote PR identity and three-way HEAD alignment, and retry draft-to-ready. An
archived directory containing only `closeout-plan.json` is resolvable for this
path only by the canonical `guru-finish-work` recovery entry. The Guru preset
installs only the current `guru-finish-work` entry; all other commands still
require `task.json`. The recovery path neither parses, rebuilds,
validates, nor rewrites an archived body, summary, ledger, readiness, or
marketplace artifact.

Plan-only recovery does not use an empty task context as authorization. It
loads `closeout-plan.json` from the current commit blob and, before GitHub or
fast-path side effects, validates canonical digest plus Git toplevel,
configured/effective repository, current head branch, base ref availability,
current HEAD transaction, active/archive locator and basename relationship,
summary task/branch/base/source-issue identity, and the exact task directory.
Working-tree plan bytes cannot replace the committed plan. Ordinary task
discovery and workspace-boundary commands do not enable this mode and still
require normal `task.json`, ignored runtime mapping, and live Git worktree
identity. No alternate task identity source is accepted.
The raw finish-work locator is preserved before ordinary resolution. Only a
basename, exact former active locator, or exact archive locator may select the
plan-only search. Path-like input is checked component-by-component with
`lstat` from repo root through the final task directory. Basename input checks
the raw `<repo>/<basename>` and `.trellis/tasks/<basename>` candidates, then
checks archive candidates in ordinary resolver order before resolution. Every
direct or archive candidate first retains only `symlink_component` evidence,
then uses the ordinary resolver's exact follow-symlink `directory + task.json`
predicate. A matching alias is rejected; an unmatched alias continues to the
next candidate. This rejects internal/external, relative/absolute,
ancestor/final, multilevel, dangling, or loop aliases before raw evidence can
be discarded. The ordinary resolver then runs and preserves explicit
`task.json`, active task, and normal archived `task.json` precedence. Only an
ordinary not-found result enables plan-only fallback. An exact archive locator
selects only that candidate; basename or
former-active fallback requires a unique matching archive month and fails
closed when multiple months match. The verified plan-only target must resolve
to the same canonical archive locator recorded by `task` and `projection`.
Only the structurally verified Darwin `/var` -> `/private/var` system mapping
may re-anchor an outer path; arbitrary `samefile` discovery and user aliases
are not valid identity.

Branch Review Gate treats every finding priority (`P0`, `P1`, `P2`, `P3`) as
blocking. `observations[]` are non-blocking notes, and
`followup_candidates[]` are out-of-scope future work candidates. They must not
be used to hide current-scope defects.

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
- Letting PR generation close `related_issues` or `followup_issues`.
- Recording review-gate evidence that does not mention deployment impact.

## Skill Evaluation Data Contracts

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
locator. Semantic grading contains exact comparison-side/case/assertion identity
plus an external verdict; human feedback uses comparison-side/case identity and
cannot carry a grader verdict. Run evidence
contains only corpus/interface/package/platform/adapter/comparison identity,
actual exit, assertion results, status, transcript locator, timing, and
feedback. It forbids gate/checkpoint/audit/release/provenance fields.

Neither adapter request nor native request carries `expected_exit`. Semantic
case files may carry exact wrapper arguments referencing a repo-local,
checker-passed owner result, but never a caller-selected route. Actual wrapper
output selects the per-exit schema before the runner performs the independent
expected-versus-actual assertion.

## Branch Review Data Boundary

Branch Review aggregate public input schema 3.0 dispatches two independent
profiles. The `branch_review` schema 2.0 profile contains workflow/standalone
mode, task/base/`branch_review_commit` identity, and one of
`initial_review|fresh_final_review`. The `base_continuity` schema 1.0 profile
binds the unchanged task review to one bounded old-base/new-base candidate and
the `base_continuity` intent. Its public outputs are the five minimal DTOs
defined by the Skill package contract. `review_ref`, finding refs, proposal
refs, and continuity identity are opaque consumer identities, not embedded
artifact bodies.

After a fix commit, finding closure is an internal transient AI judgment by the
finding owner or a real unfinished-agent replacement. It has no public exit or
artifact and automatically dispatches a distinct fresh reviewer. Current gate
schema 6.0 accepts the intent allowed by the selected current profile.
Aggregate input schema 2.0 and gate schema 5.0 or older remain legacy stale
inventory, not current runtime authority; any non-6.0 gate fails closed.

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
`branch_review_commit`, `pr_title`, and `pr_body`; Publication consumes
Branch Review continuity from its current `passed` DTO plus live Git and never
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

Legacy active-task state is adapted once from current package contracts. An
existing same-task-content Branch Review may retain its task review validity,
while any legacy Publication stale reason is classified by its current owner:
base-only mismatch routes to base reconciliation and content/metadata stale
remains Publication-owned. Migration does not rewrite active task artifacts,
read another package's private state, or restore the retired shared dispatcher.
