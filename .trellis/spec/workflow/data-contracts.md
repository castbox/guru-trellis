# Data Contracts

## Configuration

`trellis/workflows/guru-team/config-template.yml` is the reusable default
configuration. `.trellis/guru-team/config.yml` is a target repository's local
copy and must be preserved by the preset installer.

When adding a config field:

1. Add the default to `DEFAULTS` in
   `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`.
2. Document the field in `trellis/workflows/guru-team/config-template.yml`.
3. Make the parser tolerate missing fields so older installed configs continue
   to work.
4. Decide whether the preset installer needs new preservation or migration
   behavior.
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
Resolution and result facts are canonical JSON transported on stdout only;
neither task-start context, public package, installed runtime, repo root nor a
repo-external temporary file stores them. The pre-sync digest binds only
resolve-to-execute. `check-base-sync --result-json` validates schema, facts
digest, both resolution identities, and stale live Git facts, then returns the
post-sync digest to the next consumer. Already-equal execution may have equal
pre/post digests; fast-forward execution must not.
Workflow and standalone create no evidence file, lease, release command or
cleanup state.

`prepare-task.preflight.base_freshness` remains a compatibility projection and
adds pre-sync resolution source/digest, post-sync resolution/digest, decision
checkout, local/remote refs, and three-way equality facts from the same core.
It also exposes `reviewed_resolution_sha256` as the digest consumed by the
current guard and `post_sync_resolution_sha256` as the digest to pass to the
next guard, while `resolution.source` remains the
`explicit`, `config`, `config-candidate`, or `remote-default` provenance rather than a
prepare-generated explicit override. Task-start context persists only
portable base branch and local/remote SHA identity; it excludes resolution
bytes, result payloads, process output, and machine paths.

The YAML parser in `load_config()` is intentionally small. It supports simple
scalars, lists, and one level of nested dictionaries used by the current config.
Do not introduce complex YAML structures without replacing or extending the
parser and validating older configs.

## Change Context Discovery Result

Schema `guru-context-discovery-1.0` is a closed Draft 2020-12 union whose
`typed_exit` is exactly `context_ready`, `refresh_base`, or `blocked`. Common
identity embeds the complete validator-passed `guru-base-sync-result-1.0`
payload and binds its facts digest, post-sync resolution digest, selected Git
remote, decision checkout, refs/HEADs, and normalized GitHub remote repository
identity. Every projection field must equal the embedded result and current
live Git. A Git status read failure is unknown freshness and fails closed; it
is never treated as an empty clean path set. Common identity also binds
normalized change input, live
issue/proposed-draft facts, duplicate facts, current Docs/code/tests evidence,
canonical query, history preview, AI history review, mem decision, AI Review
Gate, human-confirmation status, refresh history, and snapshot identity.
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

Pre-task recording emits the reviewed snapshot on stdout without repository
writes. Post-task recording requires `--task` and
`--expected-snapshot-sha256`, validates the same query/manifest/base/live facts
and reviewed blob identities, and writes only a direct active
`{TASK_DIR}/context-discovery.json`; archived, completed, and other non-active
tasks are rejected. The recorder reopens the just-written artifact, compares
exact canonical bytes and snapshot identity, then reruns required live
freshness before returning success. Both recorder and checker execute the
published closed Draft 2020-12 schema. Base evidence preserves the complete
sync result and selected remote. Pre-task/standalone live validation requires
the decision checkout branch. Direct active task mode permits the current
checkout to be the feature branch created after the pre-task snapshot only when
it equals `task.json.branch`; the HEAD must remain the snapshot base HEAD, the
selected local/remote base refs and repository identity must remain bound, and
all dirty paths must be task-local. Any base error short-circuits before live
issue/draft, reviewed-blob, or archive-preview reads. A caller-authored
`refresh_base` result is valid only when its latest refresh entry lists the
exact stable refreshable live-error set and records the current superseded
query/snapshot digests, reason, and detection time. Recorder/checker compare
those caller-authored facts with current live freshness, return the authored
typed exit without generating route intent, and require complete skill
re-entry. They consume only the current payload and expected snapshot identity,
without reconstructing a refresh ancestry chain.
That set includes `task_branch_stale` for real feature-worktree task branch
drift; malformed task branch, locator, or state facts remain non-refreshable.
Every 40-character reviewed Git identity is resolved again from `HEAD:<path>`
and its object type must be exactly `blob`. A tree, gitlink commit, tag,
missing object, or mismatched blob cannot satisfy any Docs, code/contracts, or
tests evidence group; 64-character content evidence retains its exact byte
digest freshness check.
The same stale evidence rejects `context_ready`. Before task-local recording,
after the write, and during every task-local check, the exact repo-relative
target must be non-ignored under `git check-ignore --quiet --no-index --`. This
covers `.gitignore`, `.git/info/exclude`, and `core.excludesFile`, including a
tracked file. Ignored or unreadable trackability fails closed with
`context_discovery_target_ignored` or
`context_discovery_target_trackability_unreadable`; pre-task stdout-only mode
does not run this target gate. An existing byte-identical snapshot is
idempotent; different bytes, stale identity, non-task tracked dirty paths,
workspace/runtime/cache targets, or digest mismatch fail without overwrite or
sidecar. The closed schema and source-specific portable locator fields keep raw
source payloads out of the persisted artifact through field-specific
validation.

## Requirements Clarification Result

Schema id `guru-requirements-clarification-1.0` is a closed Draft 2020-12
result. Top-level fields are exactly `schema_version`, `skill_id`,
`generated_at`, `mode`, `typed_exit`, `invocation_context`, `review_target`,
`context_evidence`, `confirmed_facts`, `repository_answerable_questions`,
`clarification_rounds`, `open_questions`, `scope_proposals`, `source_actions`,
`human_confirmation`, `mutation_results`, `active_task_evidence`,
`ai_review_gate`, `affected_contracts`, `content_identity`, `reason`,
`consumer`, and `error`.

`invocation_context.kind` is `initial_issue`, `proposed_draft`,
`active_task_scope_change`, or `standalone_review` and includes a closed
caller-aware `resume_target`. `review_target` carries a portable current issue
or side-effect-free draft identity. `context_evidence` binds the current
`guru-context-discovery-1.0` snapshot/digest where available;
`needs_context` is the only exit that can omit load-bearing current context.

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
`optional_mechanism_origin`, `decision`, recorder-derived `proposal_digest`,
and `confirmation_ref`. `origin_requirement_status` is `explicit`,
`necessary_correctness`, `confirmed_expansion`, or `unconfirmed_expansion`.
Decision is `pending`, `accepted_current`, `related`, `followup`, `new_task`,
`out_of_scope`, `mechanism_removed`, or `mechanism_replaced`. An unconfirmed
expansion accepted into current scope requires a dedicated confirmation bound
to its exact proposal digest. An optional-mechanism-origin proposal cannot be
classified into the five scope classes: its terminal disposition is
`mechanism_removed` or `mechanism_replaced`, with
`optional_mechanism_origin=true` and `confirmation_ref=null`. During an active task, an unconfirmed expansion classified as
`related`, `followup`, `new_task`, or `out_of_scope` also requires exact
proposal-digest-bound user decision evidence.

`source_actions[]` supports only `none`, `issue_comment`, `issue_body_edit`,
`proposed_draft_update`, `new_issue_draft`, and
`active_task_scope_update`. Every row binds exact target, payload, preimage,
status, action digest, payload digest, and mutation evidence. The recorder
derives action/payload digests; it does not execute the action. Human
confirmation records `not_required`, `confirmed`, or `refused`, the exact
action digest, proposal digests, confirmed action ids, confirmer/time, and
evidence summary. Generic continuation/planning/review confirmation action
kinds are invalid. Every five-class active-task scope decision that carries an
`active_task_scope_update` must use one
`confirmation_kind=exact_source_action_and_scope`: its classification proposal
digests are exact, the task-update action id is present in
`confirmed_actions[]`, and `human_confirmation.action_digest` equals the
canonical digest of that confirmed action set. Proposal-only confirmation,
planning approval, or the task update's validated status cannot authorize the
task-local source-of-truth write. For comment/body mutation, mutation content SHA-256 must
equal the exact confirmed action payload body, canonical payload digest, and
reread live GitHub body/comment content.

Active-task `clear`/`new_task` requires a non-empty array containing only the
seven terminal decisions. Every `accepted_current`, `related`, `followup`, `new_task`, or
`out_of_scope` proposal requires proposal-digest-bound exact user-decision
evidence regardless of origin status, plus live GitHub authority facts and
one structured `decision_trail` exactly present in
`issue-scope-ledger.json.scope_decisions[]`. The trail carries proposal
id/digest/decision/confirmation refs, user-decision evidence, GitHub
comment/body URL, content digest, and `updated_at`, the
`context_before_task_update_sha256`, exact
content SHA-256 for `prd.md`, `design.md`, and `implement.md`, planning approval,
review status, stale Phase-2/Branch-Review identities, interrupted resume target,
and exact re-entry owners `guru-approve-task-plan`, `guru-check-task`, and
`guru-review-branch`. The ledger itself must have the normal
primary/close/related/followup structure. Planning evidence must pass the shared
`guru-planning-approval-2.0` validator and exact-bind both reviewed/approved aliases plus current
path/hash/size for all three documents; `{}`, two-line planning placeholders,
minimal approval JSON, and hash-only files are invalid. These are validation bindings to existing artifacts, not a
dedicated clarification file. Pre-task and standalone results remain stdout-only.

A mechanism-only terminal result still requires the same task-local ledger,
planning documents, complete planning approval, review/stale identities,
re-entry owners, and current context evidence; only `decision_trail` is null.
Mixed results project only their five-classification subset into the trail.
Every terminal active-task result receives the same live task/context freshness
validation. When `review-gate.json` exists, `review_evidence.status` must be
`stale` and bind that exact artifact path/content digest. `not_started` is valid
only when the file is absent, the artifact is null, and the stale downstream
Branch Review digest is null; `current` is invalid during re-entry.

`content_identity` contains recorder-derived target, content, context, scope,
action, payload, and result SHA-256 fields. Result identity is computed from
the canonical result projection with its own field omitted. The checker
recomputes every digest and validates current live facts.

Exit invariants are closed:

- `clear` consumes `guru-requirements-clear-router` and requires no open
  questions, a passed AI Gate, current source/context,
  all accepted proposals exactly confirmed, no pending action, and no
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
- `new_task` requires a reviewed side-effect-free `new_issue_draft`, plus a
  fresh persisted classification trail for active-task callers, and consumes
  `guru-full-task-intake-chain`; #112 owns every issue/task creation side effect;
- `blocked` is valid if and only if `ai_review_gate.status=blocked` and consumes
  `requirements-clarification-blocked`.

Unknown/multiple/unmapped exits, mismatched consumer objects, closed-question
drift, confirmation/digest drift, confirmed-payload/live-content drift,
invocation/resume mismatch, or stale active-task linkage fail closed.

## Extension Version Manifest

`trellis/guru-team-extension.json` defines the reusable Guru Team extension
version and public API metadata. `.trellis/guru-team/extension.json` is the
installed provenance copy created by the preset installer in each target repo.

The installed manifest should remain additive/backward-compatible for readers:

- missing manifest means an older install; `check-env` should warn and continue;
- invalid manifest should report `status: invalid` and continue with a clear
  next step;
- new fields should be optional for old installed manifests;
- `source.tree_state` is objective provenance (`clean`, `dirty`, `archive`, or
  `unknown`), not a release-readiness judgment;
- `source.commit` and `source.tree_state` describe the extension source observed
  at apply time. They are not a self-referential claim that the installed
  manifest file is contained in that same commit;
- `selected_platforms` records installer input and should not be inferred from
  directory presence alone.

Do not use `.trellis/guru-team/extension.json` as the canonical source of the
team extension version. The canonical source is `trellis/guru-team-extension.json`.

### Public Skill I/O Migration Fields

The canonical and installed extension manifests publish one additive migration
contract under `public_api.skill_contracts`:

- compatibility `interface_schema_id` remains
  `guru-team-skill-interface-1.2` through #145 and switches only after #146 has
  removed every active `legacy` row;
- `supported_interface_schema_ids` is the exact ordered set containing 1.2 and
  1.3, while `current_interface_schema_id` is 1.3 for new or materially revised
  public I/O;
- `registry_schema_id` is `guru-team-skill-registry-1.1`;
- `legacy_skill_ids` exactly equals active registry rows with
  `io_contract_state=legacy`;
- `public_input_schema_ids`, `typed_output_schema_ids`, and
  `private_artifact_schema_ids` are exact inventories from active production
  1.3 packages only. After `stage0-minimal-handoff-v1` activation they contain
  the exact inventories of the six Stage 0 packages; the three #146 packages
  remain excluded because they are still 1.2 legacy.

The canonical manifest
`trellis/skills/guru-team/migrations/stage0-minimal-handoff.json` has schema id
`guru-team-stage0-migration-manifest-1.0`. It is the closed activation inventory
for exactly six Skills and 24 exits, including every public input profile or
scalar signature, output/example, consumer input, projection, private artifact,
and eval case binding. It also fixes the legacy allowlist to
`guru-approve-task-plan`, `guru-check-task`, and `guru-create-task-commit`, and
the activation policy to `preset_transaction`.

Source and installed validation compare the manifest bidirectionally with the
registry, package Interfaces, workflow markers, extension inventories, and
package eval corpora. Missing, extra, duplicate, renamed, unknown, out-of-order,
or mixed-version entries fail closed. Manifest contents are an activation
contract, not a recovery journal; archived 1.2 artifacts remain readable under
their original schemas and are never rewritten during validation or install.

Test fixture schema ids belong only to the fixture extension manifest and must
not appear in production extension, installed production inventory, platform
copies, or workflow mandatory routes. Registry schema 1.1 requires every
active row to select exactly one legal pair: 1.2 with `legacy`, or 1.3 with
`minimal_handoff`. Reserved/planned rows remain lifecycle-only.

`public_api.companion_scripts` includes stable id
`discover-skill-contract`. Its success DTO is a closed union selected by
`io_contract_state`: `legacy` exposes only version/migration identity;
`minimal_handoff` exposes package-relative public input, invocation, per-exit
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
such as `v0.6.5-guru.2`, not namespaced tags such as
`guru-team/v0.6.5`. The tag must correspond to
`trellis/guru-team-extension.json.version` in the tagged commit, and the manifest must expose
`target_trellis_cli` so users can see which official `@mindfoldhq/trellis`
release this Guru Team extension targets. Stable workflow marketplace examples
should use `gh:castbox/guru-trellis/trellis#v0.6.5-guru.2`; unpinned
`gh:castbox/guru-trellis/trellis` means latest/canary and must be reported as a
mutable source in install or upgrade evidence.
An unreleased branch may carry the next canonical extension version while
public stable examples continue to point at the latest existing verified tag.

Release order matters: merge the manifest/docs PR first, create the annotated
`v<official-trellis-version>-guru.<revision>` tag on the merge commit, verify tag-pinned `trellis init` and
`trellis workflow` marketplace commands, then retire any old competing tag
names only after the new tag is verified.

## Task Start Context and Local Runtime

`.trellis/tasks/<task-slug>/task-start-context.json` is the task-local, tracked, portable intake context. Its schema is `trellis/workflows/guru-team/schemas/task-start-context.schema.json`, uses `additionalProperties: false`, and allows only source issue/repo metadata, task and branch identifiers, repo-relative `task_artifact_dir`, base refs/SHAs, portable workspace ids, actor metadata, issue-ledger seed, and compact duplicate/naming/confirmation summaries. It must never contain absolute paths, `.trellis/.runtime/**`, full preflight payloads, dirty/fetch process logs, existing worktree lists, developer identity paths, or command paths.

Local-only reusable mappings live under the gitignored producer namespace:

- `.trellis/.runtime/guru-team/workspaces/<workspace-slug>.json`
- `.trellis/.runtime/guru-team/tasks/<task-slug>.json`

Runtime cache may contain absolute worktree paths and executor timestamps, but it is disposable, untracked, has no index/developer dimension, and must be reconstructable from the current checkout, task-start-context, `git worktree list`, or explicit parameters. Ordinary task commands read tracked shared config but do not rewrite it.

Query-only `prepare-task` writes neither task context nor runtime cache. Active
`guru-create-task-workspace` is the only creator. On successful workspace/task
creation it writes exactly four tracked task-local Intake artifacts:
`task-start-context.json`, `issue-scope-ledger.json`,
`context-discovery.json`, and `issue-review.json`, then writes ignored
source/target runtime mappings. The last two artifacts preserve the exact
checker-passed canonical bytes.

Task-start-context keeps schema id/version `1.0`. Its closed `intake_summary`
adds optional `final_source_issue_binding` and `prerequisite_evidence`
properties for backward compatibility; new workspace results require both,
while archived old tasks need no backfill. The final binding records the live
open issue identity/title/body/update facts plus target-disposition and optional
created-draft binding digests. Prerequisite evidence records the schema, exit,
facts/content/linkage digests for the five upstream Skills.

Assignee remains a portable task/context audit field, never a path namespace.
The workspace executor invokes official `common.task_store.cmd_create` in an
isolated subprocess with the reviewed assignee and a call-scoped null developer
accessor. The official creator fallback therefore produces
`task.json.creator=task.json.assignee=<reviewed-login>`. Guru runtime does not
read, copy, initialize, restore, or require `.trellis/.developer` or
`.trellis/workspace/**`; existing official identity bytes remain untouched.

Do not use `task-start-context.source_issue` as PR close scope. The task-level `issue-scope-ledger.json` owns `close_issues`, `related_issues`, and `followup_issues`.

## Finish Summary

`trellis/workflows/guru-team/schemas/finish-summary.schema.json` is the shared
schema SSOT for normal finish and #100 backfill. Normal finish uses generator
`guru-team.finish-work`; backfill uses `guru-team.finish-summary-backfill` and
must carry conditional `backfill` metadata. The Python validator is strict about
field sets, types, lengths, counts, enums, SHA/issue/PR formats, clean relative
paths, normalized duplicates, adjacent repeated clauses, source-artifact links,
and all derived search/retrieval facts.

Duplicate identity is domain-specific. Every path-bearing array, including
`git.changed_paths`, `index.search_terms.paths`,
`index.affected_surfaces[].paths`, and `backfill.source_artifacts`, uses the
exact path string as identity; punctuation-removing text normalization must not
collapse two different valid Git paths. Generators sort and deduplicate Git
paths by exact string, and validators still reject exact duplicates. Non-path
semantic and search-token string arrays continue to reject duplicates after
text normalization.

The AI input is task-local `finish-summary-index.json` with schema version 1 and
only semantic index fields. It accepts at most 19 `contract_changes`; the final
schema accepts 20 so the recorder always has capacity for the fixed
protected-path filtering fact. Final facts come from `task.json`,
`task-start-context.json`, Issue Scope Ledger, Git, archived artifact existence,
UTC time, and publish output. Final artifacts live at
`.trellis/tasks/archive/<YYYY-MM>/<task>/finish-summary.json`; values may not
contain absolute, parent, workspace, runtime, backslash, CR, or LF paths, and
may not contain leading or trailing whitespace. Backfill `source_artifacts`
remain structurally valid without a task directory, but when an archived
`task_dir` is available every clean source path must name an existing file.

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
archive locator. Readiness binds repo/base/head, reviewed HEAD, exact title,
`pr-body.md`, body SHA-256, `draft=true`, reviewed source, and
`closeout_plan_digest`. Active-state recovery consumes committed plan/readiness
plus Git/remote and PR facts. Reuse and final projection require one exact PR
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
evidence commit active blob to the archived working-tree file and prospective
archive commit blob. All files are byte-identical except `task.json`, where
only the official `status` and `completedAt` archive fields may change.
`untracked_archive_outputs` are validated by their existing template/digest
contracts. Once the exact archive commit exists, its tree and blobs replace the
archived working tree as the authoritative content source.

Failure-state evidence is read from the real filesystem, Git index/log, bare
remote, and fake GitHub PR store after invoking production `cmd_finish_work()`.
Test-owned dictionaries may summarize those observed facts, but must not drive
or manufacture transition state.

### Archived Task Backfill Contract

The #100 backfill reads only these task-local source names: `task.json`,
`issue-scope-ledger.json`, `prd.md`, `design.md`, `implement.md`, `review.md`,
`review-gate.json`, `phase2-check.json`, `pr-body.md`, and
`pr-readiness.json`. A source is recorded in `backfill.source_artifacts` only
after a successful UTF-8/JSON read. Missing files are not read errors; malformed
or unreadable files are isolated to that task and excluded from extraction.
Task, Git, GitHub, artifact, problem/outcome/behavior, contract-table, and
search-term fields follow the fixed priority rules documented by the public
backfill command. The generator never infers facts from GitHub or conversation
history and never invents an issue, PR, commit, branch, path, or behavior.
Git commits use the first non-empty valid source in order: `task.json.commit`,
`review-gate.json.head`, then `pr-readiness.json.commits[]`; values from lower
priority sources are not unioned into a selected higher-priority source.
Problem fallback is exactly `<task.title>；旧行为：历史 artifact 未记录。` and
outcome fallback is exactly `<task.title>；非目标：历史 artifact 未记录。`.
When higher-priority outcome sources and a pr-body summary paragraph are absent,
the first `pr-body.md` `## 变更摘要` list item becomes outcome while the
complete normalized list remains `changed_behavior`.
Search-term phrases first use, in order, task title, task slug, problem prefix,
outcome prefix, and changed-behavior prefixes. Only when fewer than three
unique phrases remain may task slug, task title, and `历史归档 task` be used to
fill the array. After that fixed sequence, and only when no phrase contains a
#97 `FINISH_SUMMARY_COMPLETION_MARKERS` value, the generator appends the single
fixed phrase `历史归档 task 已完成`; it never replaces or rewrites an existing
phrase. During the fixed sequence, only an exact problem or outcome fallback
candidate may be skipped when its first clause equals the last clause of the
previously retained phrase. This narrow edge de-duplication prevents the same
fallback boundary from being repeated inside retrieval phrases; it does not
rewrite candidates or apply clause-level de-duplication to any other phrase.

Backfill reuses the normal `finish_summary_errors(..., task_dir=...)` validator
and `finish_summary_retrieval_text()` derivation. It adds exactly the schema
defined `backfill` object with `generated=true`, a UTC generation time,
successful source artifacts, sorted canonical `missing_fields`, and one of
`complete`, `partial`, or `minimal`. The normal #97 schema remains unchanged;
legacy top-level `summary` and `keywords` are forbidden by its closed field set.
The final validator permits one backfill-only retrieval boundary duplication
only when `generator` is exactly `guru-team.finish-summary-backfill`, problem is
exactly `<task.title>；旧行为：历史 artifact 未记录。`, retrieval starts with the
exact task title followed by that problem, and the retrieval remainder contains
no unapproved adjacent duplicate clause. A second backfill-only boundary is
allowed only when task-local sources prove the higher-priority outcome sources
and pr-body paragraph are absent, outcome equals the first pr-body summary list
item, the complete list equals `changed_behavior`, retrieval exactly matches the
shared helper, and removing one copy leaves no unapproved adjacent duplicate.
The two approved boundaries may coexist. Normal finish-work, non-exact source
text, source drift, and every other duplicate inside problem, outcome, behavior,
surface, contract, or phrase content remain rejected by the shared #97 rules.

Backfill confidence is `complete` only when the required structural artifacts,
`git.branch`, complete changed paths, source issues, PR URL, and core index
fields are present. It is `minimal` only when retrieval fields depend solely on
the archive basename, task title/name, or Markdown H1. Any other generated
semantic or provenance evidence, including artifact/base/branch/commit facts,
issue or PR facts, review outcome, completed checklist, or contract table, makes
the result at least `partial`.

`git.changed_paths` and `index.search_terms.paths` retain the complete clean,
sorted, exact-deduplicated path set. Affected surfaces group paths by the fixed
path-prefix `kind` mapping. Each kind is split into stable chunks of at most 100
paths, and every path remains present in exactly one chunk. If the complete
representation would exceed the schema maximum of 20 surfaces, generation
fails closed for that task instead of truncating paths or expanding the schema.
An empty changed-path set receives the schema-valid `task-artifact` fallback
surface with no paths.

## Workspace Boundary Snapshot

`check-workspace-boundary --json` resolves the task from `--task` or current task, validates the task-local context, then derives the expected workspace from current repo root, local runtime mapping, and Git worktree facts. It never trusts a committed absolute workspace path. The snapshot records `status`, `workspace_mode`, `expected_workspace`, `actual_repo_root`, optional `source_checkout`, `task_dir`, repo-relative `task_dir_relative`, source/task git status, suspicious same-task artifacts, and deterministic errors. Missing task context, a mismatched runtime workspace, a task outside the current repo `.trellis/tasks`, or source-checkout same-task metadata fails closed.

## Planning Approval Artifact

`planning-approval.json` is the single task-local Phase 1 planning gate
artifact. New artifacts use `schema_version=2.0`, `skill_id` equal to
`guru-approve-task-plan`, and closed Draft 2020-12 schema id
`guru-planning-approval-2.0`. This is a breaking replacement of the active 1.2
contract because provenance, unusual proposals, AI Gate, four typed exits,
consumers, and facts digest are mandatory. Active 1.2 artifacts fail with
stable complete-re-entry migration guidance; archived artifacts remain
historical and are never rewritten.

The payload records task and repository snapshots, requirement authorities,
`reviewed_artifacts[]` and byte-identical `approved_artifacts[]` entries for
`prd.md`, `design.md`, and `implement.md`, the located `Docs SSOT Plan`, current
`guru-review-contract-wording:planning_artifacts:pass` evidence,
`ambiguity_review` compatibility projection, provenance review, unusual
scenario review, final AI Review Gate, user confirmation, typed exit, unique
consumer, reason, and `facts_sha256`. Recorder/checker may rebuild these
deterministic facts and projections but never author semantic review fields.

`task.scope_ledger_sha256`, and the SHA-256 of any requirement-authority entry
whose task artifact is that same ledger, are not digests of the complete
`issue-scope-ledger.json` bytes. It digests one canonical projection containing
the positive `primary_issue` number and the sorted, deduplicated positive issue
numbers in `close_issues`, `related_issues`, and `followup_issues`. Acceptance
evidence, structured decision trails, embedded planning hashes, and other
metadata are excluded so their normal post-approval updates do not create a
circular identity. Any category membership change remains planning scope drift.

Each authoritative provenance entry binds a stable id, repo-relative planning
artifact path, statement locator, canonical UTF-8 statement SHA-256,
classification, authority references, reason, and class-specific data. The
closed classifications are:

- `explicit_requirement`: current source authority reference;
- `necessary_implementation_choice`: ordered alternatives, a selected id that
  resolves to one alternative, non-empty selection reason, and both
  `product_scope_expanded=false` and `risk_scope_expanded=false`;
- `approved_scope_expansion`: a `proposal_binding`, dedicated `confirmation`,
  and current `authority_binding` whose proposal digests are identical and
  runtime-recomputable;
- `out_of_scope_proposal`: proposal reason and terminal route/disposition, and
  exclusion from approved execution.

`provenance_review.coverage` binds reviewer, summary, reviewed entry ids,
`all_load_bearing_items_covered`, and review digest. AI selects load-bearing
statements and classifications; runtime only resolves locators, recomputes
digests, checks unique ids and class field combinations, and verifies the
caller-authored coverage value.

`approved_scope_expansion.scope_expansion` is a closed three-part binding.
`proposal_binding.source_kind=planning_artifact` resolves one controlled
locator under the current task's `prd.md`, `design.md`, or `implement.md` and
recomputes the canonical UTF-8 statement digest.
`source_kind=unusual_scenario_candidate` resolves one current candidate id and
recomputes the existing canonical unusual-proposal projection digest. The
former requires `dedicated-scope-expansion`; the latter projects the same
`dedicated-unusual-scenario` confirmation already recorded by that candidate,
so there is no duplicate proposal content or second confirmation.
`authority_binding` records the referenced current authority SHA-256 and the
same proposal digest. Recorder and checker reject a caller-only digest, stale
or ambiguous locator, missing/wrong candidate, wrong confirmation kind or
digest, stale/unknown authority digest, an authority absent from the provenance
entry refs, or any disagreement among the three proposal digests. Ordinary and
unusual proposal bindings may coexist but retain independent source identities.

`unusual_scenario_review.candidates[]` uses the closed scenario classes
`security_or_threat`, `attack_or_malicious_actor`,
`toctou_or_concurrency_race`, `fault_injection_or_crash_consistency`,
`cross_os_atomicity`, and `other_nonstandard`. Each candidate records trigger,
scope, cost, at least one alternative, consequence, source refs, and exactly one
disposition: `explicit_requirement`, `mechanism_removed`,
`mechanism_replaced`, `confirmed_scope_expansion`, `clarification_required`,
or `out_of_scope`. `confirmed_scope_expansion` requires
`confirmation_kind=dedicated-unusual-scenario`, the exact proposal digest,
user confirmation summary/time, and updated authority reference. The ordinary
`user_confirmation.kind=post-planning-approval` is separate and can never
satisfy this field. `explicit_requirement` requires at least one source
requirement ref, and every recorded source requirement ref resolves to one
current `requirement_authorities[].id`.
When a confirmed unusual proposal is also a load-bearing provenance item, its
`approved_scope_expansion` entry references that candidate id and must project
the candidate's exact confirmation and authority ref; it does not create a
second approval.

Typed exit, AI Gate, evidence, and consumer form one closed union:

- `approved` requires passed AI Gate with empty findings, revision actions,
  scope proposals, and blocking reasons; complete provenance; no unresolved
  unusual proposal; current wording pass; exact post-planning confirmation
  with non-null prompt and confirmation timestamps; and consumer
  `workflow:phase-1-task-activation`;
- `revision_required` records task-local gaps and non-empty revision actions,
  performs no authority mutation, and consumes itself through
  `skill:guru-approve-task-plan`;
- `clarify_scope` records a non-empty authority/scope mutation proposal that is
  excluded from approved execution and uses
  `skill:guru-clarify-requirements`;
- `blocked` records a missing authority, refusal, external blocker, or unsafe
  revision condition and uses `stop:task-plan-approval-blocked`.

Recorder invocation captures selected base, base ref/HEAD, invocation HEAD,
and dirty paths and rereads them around the write so in-invocation drift fails.
While the task remains in planning, the checker rebuilds and compares all five
repository snapshot facts so approval cannot activate from a stale invocation.
Downstream validation binds task identity, current requirement/wording
authority, and planning/Docs SSOT content digests. Expected implementation HEAD
or dirty-path changes after `approved` task activation do not alone make the
plan stale. Any planning document, source authority, Docs SSOT locator, or
wording evidence change requires complete Skill re-entry and new evidence.
`task.py start` is only a status transition and never approval evidence.

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

Schema `guru-task-workspace-plan-1.0` is a closed stdout-only plan produced by
`record-task-workspace-plan`. It binds skill/mode/invocation identity; the five
checker-passed prerequisite results and their digests; final issue or reviewed
draft authority; readiness scope projection; selected base and three-way HEAD
facts; semantic branch/workspace/task naming; one resolved assignee and source;
exact issue/worktree/task/artifact/runtime operations; structured command argv;
the two mutually exclusive confirmation scopes; AI Review Gate evidence; and
the canonical plan digest. It contains no absolute path, runtime payload,
secret, raw private record, or shell command string.

The `base` projection includes the checker-passed
`post_sync_resolution_sha256` in addition to selected base, refs, HEADs, and
the original sync facts digest. This post-sync identity is the comparison
anchor for the shared resolver/sync rerun immediately before the first
confirmed mutation.

Assignee source is exactly `explicit_input`, `single_issue_assignee`,
`current_github_login`, `user_selected_from_candidates`, or
`user_supplied_after_unresolved`. Candidate order is explicit input, exactly
one issue assignee, zero issue assignees to current GitHub login, then AI/user
choice for multiple or unresolved candidates. An unresolved assignee cannot
authorize workspace/task mutation.

Confirmation scope `github_issue_mutation` is legal only for a reviewed draft;
`workspace_and_task_mutation` is fixed to not-current. Confirmation scope
`workspace_and_task_mutation` is legal only for a live open issue; GitHub issue
mutation is fixed to not-current. A created issue binding covers normalized
repo, positive number, canonical URL, `state=open`, title/body SHA-256,
`updated_at`, reviewed draft id/digest, creation confirmation digest, and its
canonical facts digest.

Target provenance uses two coordinated nullable fields:
`created_issue_binding_sha256` and `created_issue_result`. A normal existing
issue and a reviewed draft before create require both null. An existing issue
produced by an earlier draft invocation requires both non-null: the binding SHA
equals the embedded created issue facts digest, and `created_issue_result` is
the complete `guru-task-workspace-result-1.0` `created_issue` variant with
passed executor/checker stages, valid result and binding facts digests, and the
fixed `refresh_review` consumer. Its current issue facts match the plan and its
complete Intake rerun exposes the canonical live existing issue with
`kind=issue`, canonical URL identity, open state, matching update time, body and
facts digests, and null `issue_binding`. Missing or partial provenance is
invalid.

Schema `guru-task-workspace-result-1.0` is a closed stdout-only union:

- `created_issue` binds the exact plan and live created issue and can only
  return `refresh_review`; branch/worktree/task/artifact/runtime operations are
  absent;
- `created_workspace` binds branch/worktree/task identity, exactly the four
  tracked artifact paths/digests/sizes/modes, ignored runtime mapping
  projection, trackability, and workspace-boundary facts and can only return
  `created`;
- `no_side_effect` binds a before/after zero-write snapshot and returns
  `refresh_review`, `cancelled`, or `blocked` according to the AI-authored
  route.

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

## Phase 2 Check Artifact

New active evidence uses closed schema `guru-phase2-check-2.0` and
`skill_id=guru-check-task`; the basename remains `phase2-check.json` and no
parallel pass artifact is allowed. The artifact binds current task/workspace,
checker-validated `guru-planning-approval-2.0`, requirement provenance, Docs
SSOT Plan, implementation handoff, issue ledger, agent recovery, base/HEAD/diff,
complete dirty paths and reviewed path digests, executed command facts, worker
evidence, scope qualification, adequacy dimensions, findings, unverified items,
AI Gate, one typed exit/consumer, full-round identity, and `facts_sha256`.

Requirement provenance artifacts, implementation handoff artifacts, Docs SSOT
durable paths, repository reviewed paths, and command facts are non-empty.
Every adequacy dimension references at least one known current-round source and
the complete dimension set covers planning, provenance, handoff, Docs SSOT,
repository, execution, and agent evidence. `current_scope` and
`scope_change_required` candidates carry non-empty trigger references. The
checker verifies only this objective existence/closure; the AI Gate decides
whether the evidence is semantically sufficient.

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
no blocking unverified item, all ten adequacy dimensions passed, a current
completed agent recovery chain, and a full rerun over the complete current
scope. A fixed finding cannot promote a prior partial round to pass.

The `agent_assignment` projection requires the current task-local
`agent-assignment.json`. Its implementation and Phase 2 check agent id sets
must be non-empty and exactly equal the effective `completed` events for their
respective roles after corrections and recovery validation. The worker evidence
agent id set must exactly equal the completed Phase 2 check agent set; partial,
unassigned, failed, unfinished, stale, or replacement-only evidence cannot enter
the round. The projection records the task-local locator and a digest of only
Phase-2-stable assignment state: implementation/check agent records, their
status events and liveness, corrections targeting those events, recovery links
for those events, exact completed id sets, and recovery closure. It does not
bind the whole assignment file digest. Post-commit Branch Review agent records,
status events, review rounds, and reuse decisions may therefore append without
staling Phase 2; any change to the Phase 2 stable projection still fails closed.
The Branch Review Gate independently validates and digests the complete current
`agent-assignment.json` before it can pass.

The checker independently derives and exactly compares `execution_sha256`,
`scope_sha256`, `adequacy_sha256`, Gate planning/snapshot/scope/adequacy
bindings, `findings_count`, and `full_round_sha256`. When implementation
handoff artifacts include task-local `agent-assignment.json`, a legal
ancestor-HEAD post-commit audit preserves that recorded raw path digest and
uses the stable agent projection for freshness. This permits only Branch Review
metadata tail and still rejects implementation/check/recovery drift.

The closed exits are `passed`, `implementation_required`, `planning_stale`, and
`blocked`. `planning_stale` alone carries route discriminator `reapprove_plan`
or `clarify_requirements`, with one corresponding consumer. Schema/runtime
reject unknown, multiple, ambiguous, or Gate/exit/consumer-inconsistent states.
Active schema 1.0 evidence is migration-stale and must be replaced only through
a complete semantic re-entry; archived bytes are never rewritten. Post-commit
consumers retain the recorded-dirty-path coverage rule and never re-record pass
merely to match a new commit HEAD.

`review-branch.sh` must verify Phase 2 check evidence exists before recording
Branch Review Gate. After the task work commit, a Phase 2 artifact recorded at
an ancestor HEAD remains valid only when all later non-metadata committed paths
are covered by the recorded `dirty_paths`, or the later tail is Trellis
metadata only. Any uncovered non-metadata committed path, or any current
non-metadata dirty path, makes the artifact stale.
Branch Review Gate and publish readiness metadata may legitimately change after
Phase 2 because independent final review and release readiness happen after the
task work commit. In post-commit audit mode, the validator may ignore stale
Phase 2 digest entries for task-local `issue-scope-ledger.json`, `pr-body.md`,
`pr-readiness.json`, `marketplace-verification.json`, `review.md`, and
`review-gate.json`; those files are instead revalidated by Branch Review Gate
or publish-specific validators before pass or publish. Assignment freshness
uses the stable projection above rather than a whole-file digest exception.
This exception does not
allow source, config, script, docs, schema, preset, overlay, or other
non-metadata drift.

## Task Commit Plan Artifact

Each `guru-create-task-commit` invocation owns one task-local
`task-commit-plans/<sequence>.json`, where `sequence` is a fresh three-digit
increasing id. Schema `guru-task-commit-plan-1.0` binds task/branch/status,
primary issue and ledger digest, base ref, pre-commit HEAD, planning/Phase 2/
ledger/task evidence digests, the complete staged/unstaged/untracked/delete/
rename/copy snapshot, unique path classifications, exact stage paths, exact UTF-8
message bytes/digest, AI review, authorization, freshness and result.

Snapshot entries whose index mode is `160000` additionally require
`gitlink_head`, `gitlink_initialized=true`, and `gitlink_dirty=false`.
`gitlink_head` is the unique commit checked out by the submodule rooted at the
exact worktree path. Uninitialized, dirty, unborn, or root-mismatched submodules
cannot produce a safe candidate. These fields are conditional: existing plan
entries for ordinary files, symlinks, deletes, and renames remain valid without
them. The additive optional `copied_from` field likewise keeps historical
schema 1.0 ordinary plans structurally valid; current snapshot producers always
emit it, using a repo path only for copy destinations and `null` otherwise.
Candidate validation and executor revalidation compare the current
gitlink identity, so a reviewed B revision changed to C before exact staging is
stale before any index mutation. For non-deleted mode `160000` paths,
`gitlink_head` is also the exact index-content authority: the executor writes
that OID through `git update-index --cacheinfo` rather than reading the mutable
submodule worktree through `git add`, then verifies the staged mode/OID and the
current worktree identity. Consequently a later B-to-C race cannot place C in
the index or commit. A deliberate gitlink delete keeps the conditional deletion
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
is an exact index absence. The candidate self path is authorized by the already validated in-memory plan and
its deterministic JSON bytes, not by re-reading mutable raw file bytes. These
rules are additive to the existing schema 1.0 fields, so legacy ordinary plans
remain structurally valid while receiving the stronger executor behavior.

Repository operation state is immediate runtime evidence rather than a plan
field. Candidate validation and executor checks before staging and immediately
before `git commit` reject active merge, cherry-pick, revert, rebase, sequencer,
or `git am` state. The detector never clears or rewrites operation markers.

Every dirty path belongs to exactly one of `task-reviewed`,
`unrelated-preserved`, `unreviewed-blocking`, or `ambiguous-blocking`. The plan
self path uses explicit `skill-artifact` coverage and is excluded from the
snapshot content digest to avoid self-hash recursion. Public artifacts store
only repo-relative paths, digests and structured facts, never file bodies,
credentials, signed URLs, customer data or machine-local absolute paths.
The fresh `phase2-check.json` recorder output may use task-reviewed coverage
through the candidate's evidence digest because the Phase 2 artifact cannot
recursively bind its own final bytes in `repository_snapshot.reviewed_paths`;
this exception does
not cover any other task, source, docs, schema, preset or overlay path.

Execution requires `result.status=planned`, no blocking classifications, fresh
evidence/HEAD/snapshot/message digest, and exact index equality. Post-commit
result uses a closed `planned` / `revision-required` / `blocked` / `committed`
state machine with exact status/exit pairing and no undeclared fields. The
executor first revalidates planned gitlinks before any stage side effect, binds
their artifact OIDs into the exact index, and then binds the complete pre-hook
index tree and each exact path's blob/mode,
then records the real commit SHA, parent, message/path evidence, expected/actual
tree and per-path blob/mode evidence, preservation/hook checks and exactly one
external exit. `committed` requires matching tree evidence and
`hook_mutation=false`; every `blocked` branch requires a failure stage,
current-or-created commit identity, non-empty errors and explicit preservation/
hook facts, including unexpected staged/dirty paths and planned-path unstaged
drift. A hook that rejects without changing the bound index, worktree, or
unrelated state records `hook_mutation=false`; planned paths merely remaining
staged are not mutation evidence. The runtime validates a constructed terminal
result against the public schema and rejects cross-field contradictions before
writing it. A later finding-fix commit requires a new
sequence and fresh Phase 2 evidence; a prior plan cannot be replayed.

### Scenario: artifact-authorized exact-index transaction

#### 1. Scope / Trigger

This contract applies whenever `create-task-commit --candidate-artifact
<task-commit-plans/NNN.json>` consumes one reviewed plan containing ordinary
paths, gitlinks, candidate self, or any mixture of those identities.

#### 2. Signatures

- Input command: `create-task-commit --candidate-artifact <repo-relative-plan>`.
- Artifact input: schema `guru-task-commit-plan-1.0`.
- Success output: `status=committed`, `exit=committed`, exact commit/tree facts.
- Failure output: exit code 2 with blocked transaction evidence; the plan file
  remains at its exact entry bytes because failure is not published.

#### 3. Contracts

- Ordinary non-delete: artifact SHA-256 + mode authorizes one persisted blob.
- Ordinary delete/rename source: artifact authorizes exact index absence.
- Copy destination: artifact authorizes the destination blob only;
  `copied_from` never authorizes or stages the source.
- Gitlink non-delete: `gitlink_head` + mode `160000` authorizes one cache entry.
- Candidate self: deterministic serialization of the validated in-memory plan
  authorizes the planned blob; raw post-validation bytes have no authority.
- Transaction: staging and hooks run against an isolated index/detached HEAD;
  real branch/index/candidate publication occurs only after every validation.
- Publication ownership: the executor keeps the real Git `index.lock` from
  executor entry through candidate publication and every rollback. It also
  holds a candidate guard, then immediately acquires and verifies the Git
  loose-ref lock after conditional branch advance. The `index.lock` is a
  sentinel, not the final index file; an independent same-directory temporary
  file carries final index bytes and is renamed to the live index while the
  sentinel remains present. Ref and candidate guards remain held through that
  publication.
- Success linearization: after candidate result and live index publication, the
  executor verifies the guarded ref/index transaction state, then performs one
  final candidate inode/content identity read while both guards still hold.
  That read is the linearization point. At that point the ref names the validated
  commit, the commit tree and live index share the exact artifact-authorized
  tree, and candidate bytes match the committed result whose digest is returned
  as executor evidence.
- Conditional rollback: a candidate C published before the final identity read
  makes the read fail. While the index sentinel still blocks Git writers, the
  executor restores its owned live-index preimage, releases its owned ref guard
  only for compare-and-swap ref rollback, preserves C, and returns blocked.
  Candidate rollback is permitted only while the candidate guard and exact
  executor-published result identity still match. Loss of any ownership
  preserves the third-party state and reports incomplete rollback instead of
  overwriting it or claiming exact restoration.
- Post-linearization writer: a candidate C published after the successful final
  identity read is a later independent operation. It is preserved and cannot
  retroactively change `committed` to `blocked`; immutable commit blob and
  returned result digest evidence remain authoritative. Mutable candidate bytes
  are required to be exact at linearization, not at every later instant.
- Success cleanup: after the successful final candidate read, only best-effort
  closure/removal of ref, candidate and index guards and transaction temporary
  files may occur. Cleanup failure cannot change the committed/blocked result.

#### 4. Validation & Error Matrix

| Condition | Required result |
| --- | --- |
| B changes to C before blob materialization | block; real HEAD/index/candidate unchanged |
| B changes to C after materialization or a hook restages C | isolated commit/tree mismatch blocks; C never reaches real HEAD/index |
| partial cache write or rejecting hook | block; exact live index preimage remains |
| operation marker appears before publication | block; marker and real Git state remain |
| isolated parent/message/path/tree mismatch | block before real ref update |
| candidate publication fails while index lock is held | conditionally roll back the ref; live index remains its entry preimage and no concurrent `git add` can be overwritten |
| live index publication fails after candidate publication | while the index sentinel and ref/candidate guards remain held, conditionally roll back owned ref/index and restore candidate only from the exact executor-published identity; preserve third-party state on ownership loss |
| candidate writer publishes C before final identity read | final read fails; roll back owned ref/index, preserve C, return blocked |
| candidate writer publishes C after final identity read | preserve C as a later operation; return committed using immutable commit blob/result digest evidence |
| existing candidate guard | block before publication; every compliant companion writer must honor the guard |
| concurrent branch writer | initial conditional ref advance or immediate ref-guard acquisition blocks; rollback preserves any third-party ref instead of forcing the task ref |
| every identity and publish precondition matches | publish one exact commit and committed result; no later fallible blocked check |

#### 5. Good/Base/Bad Cases

- Good: reviewed B becomes the exact blob/mode in the commit and live index;
  `result.status=committed` names that commit.
- Base: entry index A plus reviewed worktree B commits B while preserving every
  non-task index entry and unrelated worktree path.
- Bad: live `git add` re-reads C, or real HEAD advances before a fallible
  postcondition. Both patterns violate the transaction contract.

#### 6. Tests Required

- Real tracked, symlink, delete, delete/add rename, multi-path, candidate-self,
  entry-index A/worktree B, Unicode/pathspec, gitlink and deliberate gitlink
  delete cases assert the exact commit blob/mode/delete identities.
- Controlled B-to-C windows assert either no-side-effect blocked or an
  artifact-authorized B commit, never C.
- Partial staging, rejecting/mutating hook, operation drift, candidate
  publication failure, index publication failure, concurrent candidate writer,
  concurrent `git add`, and concurrent ref writer assert either exact entry
  preimages or preserved third-party state according to conditional ownership;
  rollback must never overwrite the third party or falsely report exact restore.
- A pre-linearization writer injected at final live-index publication must
  return normally, replace the candidate with C, then be detected by the final
  identity read; ref/index roll back, C is preserved, the index sentinel blocks
  real `git add`, and no guard/temp leaks.
- A post-linearization writer injected immediately after the successful final
  candidate read is preserved as a later operation while the executor returns
  committed; the immutable candidate plan blob in the commit and returned
  committed-result digest remain exact. Positive publication proves guarded
  ref/commit tree/live index/candidate-result equality at that read, with no
  fallible success check afterward.

#### 7. Wrong vs Correct

Wrong: call `git add` on reviewed paths, derive `expected_tree` from that live
index, and run postconditions only after real HEAD moved.

Correct: materialize artifact-authorized blobs, build and validate an isolated
index/commit, then publish the already validated commit/index/result as one
recoverable transaction.

Blocked evidence follows one failure-stage matrix, shared by the public schema,
runtime validator and package tests:

| `failure_stage` | Required HEAD/identity state | Required tree state |
| --- | --- | --- |
| `pre-commit` | unchanged HEAD; `commit_sha=pre_commit_head`; null parent/message and empty committed paths; `hook_mutation=false` | `null` before the expected tree exists, otherwise matching `actual_source=index`; mismatch is forbidden |
| `commit` with unchanged HEAD | null parent/message and empty committed paths | non-null `actual_source=index`; matching tree with no other drift represents a non-mutating rejecting hook |
| `commit` with changed HEAD | created message and non-empty path evidence; parent remains nullable only to record invalid parent cardinality | non-null `actual_source=commit` |
| `postcondition` | changed HEAD plus created message and non-empty path evidence; parent remains nullable only to record invalid parent cardinality | non-null `actual_source=commit`; matching tree remains legal for a non-tree error |

For `commit` and `postcondition`, tree/blob/mode mismatch, unexpected
staged/dirty paths, planned-path unstaged drift, unrelated drift, or a changed
HEAD with a divergent committed path set derives `hook_mutation=true`. The
boolean is evidence output, not caller-selected state. JSON Schema constrains
the public shape; runtime validation additionally checks identity equality,
tree/path match flags, exact path coverage and cross-object set equality. Both
layers fail closed on every combination they can evaluate.

## Agent Assignment Artifact

`agent-assignment.json` is required for Branch Review Gate pass and expected for
new sub-agent-dispatch Guru Team tasks. It records the AI/human assignment decisions
that already happened in the workflow:

- `schema_version`, current task path, and current `HEAD`
- `agents[]` entries for implementation/check/review assignment events
- `logical_role` as the Chinese Trellis process identity
- `agent_id` as the technical platform identity used for continuing/reusing an
  agent
- `platform_nickname` as display-only UI metadata that never participates in
  gate decisions; prefer configured Chinese UI nicknames when the platform
  exposes them, otherwise record the raw automatic/random nickname
- `review_rounds[]` entries with unique, strictly increasing review round
  number, reviewed HEAD,
  findings count, reuse policy, and reuse decision
- `reuse_decisions[]` entries for explicit reuse/replacement decisions across
  rounds
- `liveness[agent_id]` entries with `progress_anchor_at`,
  `pending_status_request_at`, `last_checked_at`, `last_decision`, and
  `last_scan_snapshot`
- `status_events[]` entries for assignment, public progress, status request,
  stale assessment, same-agent resume, replacement start, unfinished
  termination, completion, and explicit failure handling

Allowed logical roles are:

- `实现代理`
- `阶段二检查代理`
- `问题发现审查代理`
- `问题闭环审查代理`
- `最终放行审查代理`

The companion recorder/validator may check JSON structure, required fields,
role enum values, HEAD resolvability, current-HEAD freshness when requested,
file digest metadata, liveness snapshot fields, status event enum values,
required evidence fields, and objective recovery-chain completeness for Phase 2
check / Branch Review Gate pass. It must not decide which sub-agent should be
used, whether implementation is sufficient, whether reviewer reuse is
semantically acceptable, or whether a final release review is sufficient.

`agent-assignment.json` schema version `1.2` is additive over the prior review
round ledger. It keeps `agents[]`, `review_rounds[]`, `reuse_decisions[]`,
`liveness[agent_id]`, and `status_events[]`, and adds append-only
`event_corrections[]` plus `recovery_links[]`. Older artifacts that omit
`liveness` or `status_events[]` are normalized for reading, but old
`wait-timeout`, `continue-waiting`, coarse `progress-observed`, and
unstructured stale/replacement records are not active progress, stale, or pass
evidence.

`event_corrections[]` has one narrow meaning: invalidate a prior observational
or status-request event whose recorded provenance is not valid. Each entry has
a unique `correction_id`, fixed `kind=invalidate-provenance`,
`target_event_id`, target `agent_id`, canonical `target_event_sha256`, current
resolvable `head`, UTC `recorded_at`, `source=main-session`, non-placeholder
`reason`, and concrete `evidence`. The target must already exist, belong to the
same agent, and be a progress or status-request event; terminal, assignment,
stale, resume, termination, replacement, completion, failure, and workspace
boundary events cannot be invalidated. A target may be invalidated once.
Effective liveness progress/status projection and all pass gates exclude the
invalidated target while retaining its raw append-only row for audit. Unknown
targets, duplicate ids/targets, cross-agent entries, or digest mismatch fail
closed.

`recovery_links[]` has one narrow meaning: append the missing same-agent edge
from an earlier `failed` event to a later
`terminated-unfinished termination_reason=manual_or_platform_terminated_unfinished`
event. Each entry has a unique `recovery_id`, fixed
`kind=failed-to-termination`, `failed_event_id`, `termination_event_id`, same
`agent_id`, canonical SHA-256 for both immutable target event objects, current
resolvable `head`, UTC `recorded_at`, `source=main-session`, reason, and
evidence. Both events must already exist, remain non-invalidated, have matching
digests, use the same agent, and occur in forward order. A failed event may
have at most one recovery link. Unknown/duplicate/cyclic/backward, cross-agent,
wrong-kind, or tampered links fail closed. Recovery traversal follows the linked
termination into the existing `replacement-started` predecessor edge and
requires the active replacement chain to reach `completed`; a link alone never
supplies completion evidence.

`liveness[agent_id].last_scan_snapshot` records:

- task worktree `HEAD`, content status digest, content diff stat digest, and
  content max mtime, excluding `agent-assignment.json` bookkeeping writes;
- source checkout `HEAD`, status digest, diff stat digest, and max mtime;
- `progress_events_count`, `progress_events_digest`, and
  `progress_events_newest_event_id`, counting only progress events.

Allowed progress events are:

- `explicit-message-observed`
- `tool-activity-observed`
- `command-output-observed`
- `platform-progress-observed`
- `status-response-observed`

Allowed control / terminal / audit events are:

- `assigned`
- `status-requested`
- `status-request-failed`
- `stale-assessed`
- `resume-same-agent`
- `replacement-started`
- `terminated-unfinished`
- `completed`
- `failed`
- `workspace-boundary-violation`

Every status event records `event_id`, `event`, `agent_id`, `logical_role`,
`platform_nickname`, `observed_at` as UTC ISO-8601, `recorded_at`, `head`,
`source`, and non-placeholder `evidence`. `replacement-started` additionally
requires `predecessor_agent_id`, `predecessor_event_id`,
`replacement_reason`, and `handoff_summary`. `resume-same-agent` requires
`predecessor_event_id` and `handoff_summary`. `terminated-unfinished` requires
`termination_reason` and `handoff_summary`; `termination_reason=stale_cutover`
requires `termination_source_event_id` pointing to the same agent's
`stale-assessed`, while
`termination_reason=manual_or_platform_terminated_unfinished` requires an
empty `termination_source_event_id`.

The liveness checker is a short-lived, on-demand, single-sample command:

```bash
.trellis/guru-team/scripts/bash/check-subagent-liveness.sh --json \
  --task ".trellis/tasks/<task>" \
  --agent-id "<technical-agent-id>" \
  --source-repo "<source-checkout-path>" \
  --progress-scan-interval 120 \
  --max-progress-silence 180
```

It returns exactly one decision:
`workspace_boundary_violation_progress`, `progress_observed`,
`status_request_required`, `continue_waiting_no_repeat_ping`,
`stale_allowed`, or `blocked_missing_evidence`. `progress_scan_interval=120s`
controls scan cadence. `max_progress_silence=180s` is measured from
`progress_anchor_at`; `status-requested` does not refresh that anchor and does
not extend `max_progress_silence_deadline_at`. If the deadline has already
passed but there is no pending status request, checker must still return
`status_request_required`; only after a successful `status-requested` and an
immediate recheck can `stale_allowed` be returned when no progress appeared.

Source checkout snapshot changes are
`workspace_boundary_violation_progress`, not stale evidence. Task worktree
snapshot changes and recorded progress events are `progress_observed`. Only new
changes relative to `last_scan_snapshot` refresh `progress_anchor_at`. Existing
dirty diffs, old progress events, control/bookkeeping events, and
`agent-assignment.json` writes do not refresh liveness.

`record-subagent-liveness-event.sh` is the active status/liveness writer.
`record-agent-assignment.sh` remains for review rounds and reuse decisions, and
its old `--status-event` path must fail closed. `status-requested` and
`status-request-failed` may be recorded only after checker decision
`status_request_required`. `stale-assessed` may be recorded only after checker
decision `stale_allowed`, and recorder must verify current task/source
snapshot plus progress event digest still match `last_scan_snapshot`; otherwise
it fails closed and requires a recheck.

After `stale-assessed`, the workflow must not resume or continue waiting for
that predecessor. The same liveness handling turn must record
`terminated-unfinished termination_reason=stale_cutover
termination_source_event_id=<stale-assessed.event_id>`, then replacement
`assigned`, then `replacement-started` with
`replacement_reason=max_progress_silence_exceeded`. Manual/platform unfinished
termination is structurally separate through
`termination_reason=manual_or_platform_terminated_unfinished`.

`wait_agent`, `trellis channel wait`, or equivalent wait command timeout means
only that the current wait window ended without final completion. It is not a
failure signal and must not be used as pass evidence. `completed` means the
agent execution chain ended, not that Phase 2 or Branch Review passed. `failed`,
unfinished, stale, or replacement partial output must not support a passing
Phase 2 check or Branch Review Gate until a same-agent resume or replacement
chain later reaches `completed`. A replacement `failed` requires further
resume/replacement and cannot close the chain.

For Branch Review Gate, any review agent that recorded findings may be reused
only as `问题闭环审查代理` for fix confirmation. This includes a previous
`最终放行审查代理` round that found a new issue. A finding owner may be closed
by a later same-agent closure round with `findings_count: 0` and
`reuse_decision: reuse-for-closure`; or by a different fresh
`问题闭环审查代理` whose technical `agent_id` has not appeared in any earlier
`review_rounds[]` and whose `reuse_decisions[]` entry records
`decision=new-agent` with exact `from_round`, `to_round`, closure `agent_id`,
reviewed `head`, and non-empty `reason`. If the finding owner objectively
failed, was interrupted, or became stale and cannot continue, the workflow may
record a replacement closure chain: predecessor liveness evidence in `status_events[]`,
`replacement-started` with `predecessor_agent_id`, `predecessor_event_id`,
`replacement_reason`, and `handoff_summary`, `reuse_decisions[]`
`decision=replace` with `from_round` / `to_round`, then a replacement
`问题闭环审查代理` round with `findings_count: 0` and
`reuse_decision: replace`. Every finding owner must have one of those three
closure forms before a passing gate can be recorded. A closure round that still
reports findings becomes a new finding owner and must itself have a later
explicit closure; a closure that reports zero findings confirms its targeted
finding is closed and does not need to be repeated for every later HEAD. The final
passing review round must be the last `最终放行审查代理`, use a fresh technical
`agent_id` that has not appeared in any earlier `review_rounds[]`, set `findings_count` to 0, set
`reuse_decision` to `new-agent`, record the reviewed code `HEAD` in
`reviewed_head`, and have a unique, strictly increasing `round` value so no
later record can make the final round ambiguous.

Because `最终放行审查代理` is assigned after the task work commit,
`agent-assignment.json` may receive a post-commit metadata update before Branch
Review Gate. `review-branch.sh` must then receive `--agent-assignment` so the
gate records the current digest, roles, assignment count, review round count,
reuse decision count, and status event count. This does not permit post-commit
changes to non-metadata paths or to non-gate task artifacts.

Project agent definitions have a separate display contract. Technical dispatch
ids (`trellis-implement`, `trellis-check`, `trellis-research`, `implement`,
`check`) are public API. UI-facing text belongs in Codex
Markdown descriptions, headings, and assignment `logical_role`. Codex
`nickname_candidates` must stay ASCII in current Codex releases. Do not use
`agent-assignment.json.platform_nickname` as the source of dispatch behavior.

## Issue Scope Ledger

Issue close semantics must be explicit:

- `primary_issue` is intake context and usually the default close candidate.
- `close_issues` are issues the current task fully resolves and may close.
- `related_issues` are references only.
- `followup_issues` are future work and must never be closed by the current PR.

Publish is blocked when a close issue lacks acceptance evidence or the Branch
Review Gate did not record coverage for that issue. Existing enforcement:

- `validate_ledger_for_publish()`
- `build_pr_body()`

## Commit Message Payloads

`check-commit-messages --json` validates objective commit subject/body shape
for the checked range. It must not decide whether implementation, Phase 2 check,
Branch Review, or PR readiness is sufficient. The payload is additive and uses:

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
  "command": ["gh", "pr", "merge", "91", "--merge", "--subject", "...", "--body-file", "<merge-body-file>"],
  "errors": []
}
```

When the pull request number is omitted, the formatter sets `ready=false` and
uses `<pull_request>` as a placeholder; with a real number it returns
`ready=true`.
Trellis metadata commit messages generated by finish/publish use
`chore(trellis): #<primary_issue> 固化任务收尾元数据` and an empty body.
Commit message payloads must never use close keywords such as `Closes`,
`Fixes`, `Resolves`, `Close`, `Fix`, or `Resolve`; those keywords remain PR
body-only close semantics controlled by Issue Scope Ledger.

## Review Gate Artifact

`review-branch.sh` writes `review-gate.json` in the task directory by default.
The artifact records:

- base branch/ref and current `HEAD`
- diff range
- changed files and classified deployment impact
- review scope
- conclusion summary
- reviewer identity metadata
- independent review source metadata (`review_source: independent-agent`) for
  both passed gates and failed findings artifacts
- required review report digest: `review_report.path`, `sha256`,
  `size_bytes`, and `modified_at`
- findings
- observations
- follow-up candidates
- Issue Scope Ledger coverage
- validation evidence
- required `agent_assignment` digest summary from task-local
  `agent-assignment.json`
- objective language-template validation evidence: `review.md` and raw
  `reviews/*.md` reports are Chinese human-readable task artifacts, so
  validators may reject fixed English template headings while leaving semantic
  sufficiency to the AI/human review

The gate is valid only for the reviewed `HEAD`, except that `finish-work` may
allow metadata-only commits after the gate. A passed gate is invalid if it lacks
review report metadata, `review_source: independent-agent`, or a task-local
file named `review.md`. `--reviewer` alone is only identity metadata and cannot
prove the review report evidence; main-session/self-review identities are
rejected for passed gates. Enforcement lives in `validate_review_gate()` and
`metadata_only_since()`.

A failed findings artifact is also invalid recorder evidence when it lacks
`review_source: independent-agent` or a task-local `review.md` digest. Its
`conclusion.passed` must be `false`; `passed=true` is reserved for explicit
`--pass` with zero findings.

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

## Closeout Plan

`closeout-plan.json` is schema version `1.0` and is the immutable machine input
contract shared by dry-run and formal finish. It records portable task and
repo/base/head identity, protected input SHA-256 values, Branch Review Gate
coverage, exact draft PR inputs, marketplace pending machine evidence, future
archive projection, exact metadata allowlist, and the fixed transition list.
It never records tokens, absolute worktree paths, a real PR URL, verifier
output, or archive commit SHA. Its projection does record a fixed sentinel PR
URL/ref and the complete schema-valid finish-summary template so all local
summary errors are known during prepare.

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

`publish.body_sha256` hashes the task-local `pr-body.md` bytes. Those bytes must
decode as non-empty UTF-8, and the decoded text is the one canonical body value
used by active readiness recovery, `gh pr create`, unique draft reuse, and final
projection. Leading/trailing whitespace, trailing newlines, and
Markdown-sensitive spaces are identity data; validators never trim or add a
newline before comparing the remote PR body. After archive, the remote body's
UTF-8 bytes are hashed directly and compared with `publish.body_sha256`; the
task-local body is not reopened.

`projection.move_paths` is the complete task-relative filesystem set moved by
the official archive command. `projection.tracked_move_paths` is the subset in
the Git index after the evidence commit; each requires an active deletion and
archive addition. `projection.untracked_archive_outputs` is the subset created
after that commit; currently it is exactly `finish-summary.json`, and Git must
report only its archive addition. `projection.evidence_paths` is the complete
active task path set owned by the pre-draft metadata commit. These tracking
classes are immutable plan facts derived before archive, not inferred from
post-move status. The evidence commit tree must contain exactly the active
locator projection of `tracked_move_paths`; this Git-tree check proves the
classification before final projection writes any untracked output. The
projection also stores `summary_template`,
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
Dry-run returns the complete plan and digest. First formal execution accepts
only the same digest through `--expected-plan-digest`; a mismatch or protected
input drift fails before push or file writes. `pr-readiness.json` binds the same
digest under `publish_inputs.closeout_plan_digest`. After the first metadata
commit, retries load the committed plan and validate reachable successor facts;
passed ledger evidence is never used to reconstruct the initial plan.
Before draft binding, partial retries distinguish reviewed content pushed,
verifier pending/failed, verifier passed but evidence uncommitted, and evidence
committed but unpushed from the exact plan/readiness/evidence/Git/remote facts.
They retry only the missing transition.

`task.archive_locator` uses the same live `YYYY-MM` that the unmodified official
archive command will use. Formal checks it before the first side effect and
again immediately before official move. If a committed plan becomes stale while
the task is still active, dry-run may produce a replacement plan only when the
old plan is the exact current evidence commit and neither old nor new archive
locator exists. The replacement carries `git.evidence_parent_head`, changes
only archive-derived projection values plus `projection.evidence_paths`, and a
formal run with the new digest appends an exact plan/readiness evidence commit.
The predecessor plan and evidence lineage remain in Git and are recursively
validated. This is plan supersession, not archive-directory migration or
history rewrite.

`inputs.official_after_archive_hooks.sha256` binds the canonical empty command
state parsed by the official Trellis config parser. Missing or empty
`hooks.after_archive` maps to `{"commands":[]}`. Non-empty, ambiguous,
unreadable, invalid-byte, or symlinked config has no valid digest because
prepare rejects it without executing any hook command.

Marketplace machine evidence has one deterministic pending identity and one
deterministic passed identity. Pending and passed use the same fixed machine
fields; pending uses empty artifact/remote digests and `commands_passed=false`.
Human scope reasons remain outside this object and do not affect its identity.
`artifact_path` is exactly task-relative `marketplace-verification.json`, so
the same locator resolves after the active directory moves to archive.
Missing, duplicate, altered, path-bound, or digest-mismatched machine fields
fail closed.

Before the exact archive commit exists, archive recovery accepts only the
complete mixed no-renames working-tree path set: both sides for every tracked
move and archive-only for every untracked output. It validates exact
dirty/staged paths, evidence-commit parent/path identity, active absence,
archive completeness, tracked blob continuity, and the official `task.json`
delta before it may create the commit. Missing or mismatched commit state keeps
this metadata recovery path fail closed.

Before official move, the same continuity contract applies to the active task:
the index is empty, untracked paths equal the planned final outputs, every move
path is a regular file, tracked Git modes are `100644` or `100755` and match the
working mode, and every working byte equals its evidence blob. This gate also
rechecks the live archive month and empty official hook state.

When current `HEAD` is the exact planned archive commit, both normal archived
tasks with context and plan-only damaged tasks load the plan from that commit
blob and validate only the immutable plan and Git parent/path/tree/blob lineage.
Archived working-tree deletion, content tampering, and the resulting dirty
paths are ignored; recovery may only push that exact commit when needed, check
remote PR identity and three-way HEAD alignment, and retry draft-to-ready. An
archived directory containing only `closeout-plan.json` is resolvable for this
path only by `trellis-finish-work`; other commands still require `task.json`.
Neither path parses, rebuilds, validates, or rewrites an archived body, summary,
ledger, readiness, or marketplace artifact.

Plan-only recovery does not use an empty task context as authorization. It
loads `closeout-plan.json` from the current commit blob and, before GitHub or
fast-path side effects, validates canonical digest plus Git toplevel,
configured/effective repository, current head branch, base ref availability,
current HEAD transaction, active/archive locator and basename relationship,
summary task/branch/base/source-issue identity, and the exact task directory.
Working-tree plan bytes cannot replace the committed plan. Ordinary task
discovery and workspace-boundary commands do not enable this mode and still
require the normal `task.json` / `task-start-context.json` contracts.
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
python3 -m json.tool trellis/workflows/guru-team/schemas/task-start-context.schema.json
```

## Common Mistakes

- Adding a config key to `config-template.yml` without adding a default in
  `DEFAULTS`.
- Adding a new task-start-context field required by code but absent from the strict JSON schema.
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
