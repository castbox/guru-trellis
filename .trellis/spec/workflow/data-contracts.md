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
does not run this target gate. The `task_local_reentry` public input supplies an
exact task locator plus fixed `prior_snapshot_locator=context-discovery.json`;
the wrapper binds the owner checker to that task rather than deriving scope
from the private snapshot. Task mode adds private `task_worktree_state`, whose
digest covers current HEAD and every dirty path/status/content/mode/rename fact
except the fixed snapshot and ignored runtime state. An existing byte-identical
snapshot is idempotent. Different bytes require a regular, trackable,
schema/identity-valid prior whose snapshot digest matches explicit
`--expected-prior-snapshot-sha256`, followed by complete validation of the new
snapshot and exact live worktree state. A successful replacement records the
prior digest in optional `superseded_snapshot_sha256`; missing/wrong/invalid
prior or stale new evidence fails before overwrite and produces no sidecar.
The closed schema and source-specific portable locator fields keep raw source
payloads out of the persisted artifact through field-specific validation.

## Requirements Clarification Result

Schema id `guru-requirements-clarification-2.0` is the active closed Draft 2020-12
result. Top-level fields are exactly `schema_version`, `skill_id`,
`generated_at`, `mode`, `typed_exit`, `invocation_context`, `review_target`,
`target_disposition`, `context_evidence`, `confirmed_facts`, `repository_answerable_questions`,
`clarification_rounds`, `open_questions`, `scope_proposals`, `source_actions`,
`mutation_results`, `active_task_evidence`, `ai_review_gate`,
`affected_contracts`, `content_identity`, `reason`, `consumer`, and `error`.
Schema 1.0 is read-only migration history: it cannot express current target
disposition or retarget identity and never satisfies a current invocation.

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
compact `decision_trail` exactly present in
`issue-scope-ledger.json.scope_decisions[]`. The field name is retained only for
compatibility; it is not a process trail. Its exact fields are `trail_id`, final
proposal id/digest/decision rows, and `github_authority` containing kind, URL,
and remote content checksum. It contains no user identity, confirmation
reference, authorization state/digest, authority timestamp, planning identity,
review state, context snapshot, interrupted target, or re-entry route. The
ledger itself must have the normal primary/close/related/followup structure.
Current planning documents, context freshness, task-update preimage, and
re-entry owner facts remain in the transient owner result and are reread from
their owning sources. Pre-task and standalone results remain stdout-only.

A mechanism-only terminal result still requires the same task-local ledger,
planning documents, re-entry owners, and current context evidence in the
transient owner result; only `decision_trail` is null.
Mixed results project only their five-classification subset into the trail.
Every terminal active-task result receives the same live task/context freshness
validation. A legacy full-shape trail and matching task-update payload are
projected once into the compact shape by the recorder. This compatibility
projection does not request a new user choice, mutate GitHub, or preserve the
legacy authorization/process fields. A partial current-shape payload carrying
removed legacy fields fails closed instead of being silently stripped.

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

- compatibility `interface_schema_id` is
  `guru-team-skill-interface-1.3` after #146 removes every active `legacy` row;
- `supported_interface_schema_ids` is the exact ordered set containing 1.2 and
  1.3, while `current_interface_schema_id` is 1.3 for new or materially revised
  public I/O;
- `registry_schema_id` is `guru-team-skill-registry-1.1`;
- `legacy_skill_ids` exactly equals active registry rows with
  `io_contract_state=legacy`;
- `public_input_schema_ids`, `typed_output_schema_ids`, and
  `private_artifact_schema_ids` are exact inventories from all active
  production 1.3 packages. `legacy_skill_ids` is empty after the atomic
  production activation.

The frozen canonical manifest
`trellis/skills/guru-team/migrations/stage0-minimal-handoff.json` has schema id
`guru-team-stage0-migration-manifest-1.0`. It is the immutable historical
activation inventory for exactly six Skills and 24 exits, including every public input profile or
scalar signature, output/example, consumer input, projection, private artifact,
and eval case binding. It also fixes the legacy allowlist to
`guru-approve-task-plan`, `guru-check-task`, and `guru-create-task-commit`, and
the activation policy to `preset_transaction`.

`trellis/skills/guru-team/migrations/stage0-ai-first-contract-v2.json` has schema
id `guru-team-stage0-ai-first-contract-migration-1.0`. It supersedes the active
contract, not the frozen bytes: the same six Skills now expose 23 exits, and a
workspace/task mutation refusal stops in dialogue before recorder/executor
instead of emitting `cancelled`. It also declares the public scalar change that
allows `guru-sync-base.repo_root` and `route` to be omitted and derived by the
runtime. Source and installed validation require both
records, their distinct identities, and the exact current 6-by-23 closure.
Missing, extra, duplicate, renamed, unknown, out-of-order, or mixed-version
entries fail closed. Migration contents are contracts, not recovery journals;
archived artifacts remain readable under their original schemas and are never
rewritten during validation or install.

The independent canonical manifest
`trellis/skills/guru-team/migrations/production-minimal-handoff.json` has schema
id `guru-team-production-migration-manifest-1.0` and activation id
`production-minimal-handoff-v1`. It binds exactly the three planning/check/
commit packages, ten structured profiles, 11 stable exits, per-exit output
schema/example identities, consumer inputs, projections, private artifact ids,
and canonical eval cases. Its bytes are immutable historical authority, including
the original `approved` and `passed` output schema ids.

`trellis/skills/guru-team/migrations/production-ai-first-contract-v2.json` has
schema id `guru-team-production-ai-first-contract-migration-1.0`. It supersedes
the production v1 activation projection without rewriting v1: current
`approved` removes private `approval_ref`, current `passed` removes private
`check_ref` and accepts the repository hash width, and both output schemas move
to v2. Legacy Task Commit message/path/semantic fields project once into the
five-field v2 owner-entry seed and ignored-runtime candidate; authorization and
caller-selected exit fields are discarded, and the old terminal result journal
is never written. Both frozen activation manifest locators plus both AI-first
migration locators are published in the extension in activation order.
The Stage 0 v1 manifest bytes and ordered
6-by-24 identity remain a regression authority and are not rewritten to absorb
production packages.

The source and installed closure algorithm reads the live registry, both frozen
activation manifests, both AI-first migrations, Interface public contracts, and
package-local corpora. It requires the active ids to equal the two activation
sets plus any future complete active
1.3 rows; requires every active row to be `minimal_handoff`; and requires exact
profile/exit/current-case set equality. Thirteen Skills and 51 exits are the
current cardinality regression, not a hard-coded future registry allowlist.

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

## Task Identity and Local Runtime

New AI-first tasks use official Trellis `task.json` as their tracked task
identity and `issue-scope-ledger.json` as the only Guru-owned durable Intake
artifact. Existing active `task-start-context.json` schema 1.0 files are
read-only migration evidence; runtime may consume them once when reconstructing
an interrupted legacy task, but must not generate, upgrade, or require them for
new tasks.

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

Legacy `task-start-context.source_issue` never owns PR close scope. The
task-level `issue-scope-ledger.json` owns `close_issues`, `related_issues`, and
`followup_issues`.

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
protected-path filtering fact. Final facts come from `task.json`, Issue Scope
Ledger, ignored runtime identity, live Git, archived artifact existence, UTC
time, and publish output. Final artifacts live at
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
archive locator. Publication's ignored-runtime readiness checkpoint owns its
semantic conclusion and emits only task plus `reviewed_content_head`; Finalizer
does not read or commit that checkpoint. The closeout plan independently binds
repo/base/head, exact title, raw `pr-body.md` SHA-256, `draft=true`, and its
internal digest. Active-state recovery consumes the untracked schema 1.2 plan
plus Git/remote, marketplace owner, task layout, and PR facts. Reuse and final projection require one exact PR
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
`reviewed_content_head` active blob to the archived working-tree file and
prospective schema 1.2 archive commit blob. Persisted schema 1.1 instead binds
its historical evidence-commit blob. All files are byte-identical except `task.json`, where
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

`check-workspace-boundary --json` resolves the task from `--task` or current
task, validates `task.json` plus ignored task/workspace mappings and live Git
worktree identity, then derives the expected workspace. A legacy
`task-start-context.json` may supply the same identity once during interrupted
migration, but is never generated or required for a new task. The command never
trusts a committed absolute workspace path. The snapshot records `status`,
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
Task activation and Phase 2 consume only the DTO plus current planning/live facts
and never read or delete this private state. The checkpoint does not retain
per-file hashes, sizes, mtimes, repository snapshots, scan history, reviewer
metadata, raw reports, assignments, liveness, authorization, authorization
wording, or authorization digests.
When task activation or a real scope choice needs authorization, that occurs
in the current conversation and is never projected into persisted or public
state.

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

Schema 1.2 and 2.0 files are one-time read-only migration signals and return
`planning_approval_legacy_requires_ai_first_reentry`. New execution never
recreates their provenance bundles, digest chains, confirmation fields, or
tracked artifact shape. Archived bytes remain historical. `task.py start` is
only a status transition and never approval evidence.

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
the original sync facts digest. This post-sync identity is the comparison
anchor for the shared resolver/sync rerun immediately before the first
confirmed mutation.

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

## Phase 2 Check Artifact

New active evidence uses closed schema `guru-phase2-check-3.0` and
`skill_id=guru-check-task`; the basename remains `phase2-check.json` and no
parallel pass artifact is allowed. The ignored owner checkpoint stores only
mode/task/current checked HEAD, reviewed paths, one composite worktree-content
freshness token, executed validation evidence, the final Docs SSOT result,
semantic adequacy/findings, and one typed exit/route/reason/consumer. The token
has one local deterministic consumer: the checker invoked inside the Phase 2
public wrapper before typed-output projection. It detects same-path drift and
returns control to the AI owner for delta
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
validation scope, Docs SSOT, issue scope, and invocation identity. A legal
ancestor-HEAD post-commit consumer relies on the minimal passed DTO and live Git,
not on reopening this checkpoint. Routine assignment/liveness and the
exceptional private recovery checkpoint are not Phase 2 inputs and do not enter
the owner checkpoint.

The closed exits are `passed`, `implementation_required`, `planning_stale`, and
`blocked`. `planning_stale` alone carries route discriminator `reapprove_plan`
or `clarify_requirements`, with one corresponding consumer. Schema/runtime
reject unknown, multiple, ambiguous, or Gate/exit/consumer-inconsistent states.
Active schema 1.0 evidence is migration-stale and must be replaced only through
a complete semantic re-entry; archived bytes are never rewritten. `passed`
projects only `task_ref + checked_head` to Task Commit. After the checked output
passes its schema, the Phase 2 producer wrapper deletes its checkpoint. Task
Commit consumes only that DTO and live Git; Branch Review then consumes the
committed Task Commit DTO and validates parent, message, paths, content continuity
and the complete range directly from live Git. Neither owner reads, deletes, or
reopens Planning or Phase 2 private state. Downstream workflow metadata is
validated by its owning gate and is never projected back into Phase 2.

## Task Commit Candidate

Each `guru-create-task-commit` invocation owns one temporary candidate under
ignored `.trellis/.runtime/guru-team/task-commit-plans/<task-key>/<sequence>.json`,
where `sequence` is a fresh three-digit
increasing id. Current schema `guru-task-commit-candidate-2.0` binds only task
locator/branch/status, base/pre-commit/checked HEAD, the complete
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
and `null` otherwise. Historical schema 1.0 plans retain their original
optional-field rules only on the read-only compatibility path.
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
classifications, or exact stage set. Legacy schema 1.0 plans retain their
historical shape only for the read-only compatibility path described below.

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
candidate does not reread or expose the producer-private Phase 2 checkpoint;
task-reviewed coverage is derived from the DTO and current reviewed path set.

Execution requires a passed AI review, no blocking classifications, fresh
task/HEAD/snapshot/message/parser facts, and exact index equality. The
executor first revalidates planned gitlinks before any stage side effect, binds
their artifact OIDs into the exact index, and then binds the complete pre-hook
index tree and each exact path's blob/mode,
then verifies the real commit SHA, parent, message/path evidence, tree, blobs,
modes and unrelated preservation from Git before advancing the live ref/index.
Before publication, the executor creates and validates the isolated commit. It
then uses standard `git update-ref <ref> <new> <old>` followed by `git reset
--mixed --quiet HEAD`; it owns no custom lock, atomic replacement, rollback, or
concurrency protocol. On success it returns only `pre_commit_head` and
`commit_sha`, deletes the private candidate, and never writes Git-derived
result/tree evidence into tracked metadata. Failure before ref publication
leaves the live ref/index untouched; failure after a successful conditional ref
advance reports the created commit for bounded same-plan recovery. A later finding-fix commit requires a new
sequence and fresh Phase 2 evidence; a prior plan cannot be replayed.

### Executor Boundary

`create-task-commit --candidate-artifact <ignored-runtime-candidate>` validates
one schema `guru-task-commit-candidate-2.0` private candidate. It materializes only
authorized blobs/modes in an isolated index, runs repository commit hooks, and
verifies parent, raw message, committed path set, complete tree and unrelated
preservation before conditionally advancing the live branch/index.

The private candidate is never staged. A normal validation or hook failure
preserves the candidate and unrelated state for bounded recovery. Success
returns `pre_commit_head` and `commit_sha`, then removes the candidate. Commit
tree, message, path and parent facts remain derivable from Git and are not
copied into tracked task metadata.

Existing task-local schema 1.0 `task-commit-plans/*.json` and their
schema/example are legacy read-only evidence, never current package output.
A completed plan may prove an already-created commit for one active task; a
planned legacy file is never executed or rewritten and must be rebuilt under
ignored runtime through the current public input.

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

### Legacy Assignment Migration

Existing active tasks may retain `agent-assignment.json`, raw review reports
and `review.md` bytes. Legacy Phase 2 and Branch Review validators may read
them only to validate an already-recorded result. New or re-entered Phase 2
checks write schema 3.0 and Branch Reviews write schema 2.2; neither updates,
normalizes, copies, or requires those artifacts. Archives remain byte-for-byte
unchanged.

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
The single archive transaction commit generated by finalization uses
`chore(trellis): #<primary_issue> 固化任务收尾元数据` and an empty body. There
is no separate readiness/evidence metadata commit.
Commit message payloads must never use close keywords such as `Closes`,
`Fixes`, `Resolves`, `Close`, `Fix`, or `Resolve`; those keywords remain PR
body-only close semantics controlled by Issue Scope Ledger.

## Review Gate Artifact

`review-branch.sh` writes compact schema 2.2 `review-gate.json` in ignored
owner-private runtime after the independent semantic judgment exists. The gate
contains only schema/skill identity, task/mode/review intent, typed exit,
reviewed `head`, `base_ref`, normalized semantic candidates/findings, minimum
independent reviewer/evidence facts, and `facts_sha256`.

The gate deliberately omits a second conclusion rollup, changed-file/diff
copies, command argv, deployment projection, issue ledger copy, assignment
continuity and report digests. The consumer derives Git/range/task facts from
live state and validates the compact semantic result. A resolved finding keeps
its original `introduced_head` and records the fix commit as
`resolved_at_head`; these values are expected to differ on a normal finding-fix
closure. `passed` after any resolved finding requires
`review_intent=fresh_final_review` over the complete current range.

The gate is valid only for `reviewed_content_head`, except that finalization may
accept an exact descendant tail limited to the current task's declared
publication/finalization metadata files. `review_source` must be
`independent-agent`; main-session/self-review identities are rejected. Schema
2.0 gates remain read-only compatibility evidence and are not rewritten.
Enforcement lives in `validate_review_gate()` and
`review_branch_content_continuity_errors()`; unknown task, nested lookalike,
runtime, code, test, planning, or durable-spec descendants fail closed.

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

`closeout-plan.json` is current schema version `1.2` and is the immutable
machine input contract shared by preview and formal finish. It is an untracked
active transaction checkpoint that becomes tracked only in the single archive
commit. It records portable task and
repo/base/head identity, protected input SHA-256 values, Branch Review Gate
coverage, exact draft PR inputs, marketplace pending machine evidence, future
archive projection, exact metadata allowlist, and the fixed transition list.
It never records tokens, absolute worktree paths, a real PR URL, verifier
output, or archive commit SHA. Its projection does record a fixed sentinel PR
URL/ref and the complete schema-valid finish-summary template so all local
summary errors are known during prepare.

For current tasks, `review.changed_paths` is rebuilt deterministically from the
live merge base of the task's current `base_branch` through immutable Branch
Review `reviewed_content_head`; compact gate schema 2.2 does not carry a duplicate
`changed_files` inventory. Only older tasks without a pinned base may reuse a
legacy gate's `changed_files`. The rebuilt list is the single input to closeout
review reporting, marketplace candidate-surface classification, ledger
evidence projection, archive retention, and finish-summary changed paths.
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

`publish.body_sha256` hashes the task-local `pr-body.md` bytes. Those bytes must
decode as non-empty UTF-8, and the decoded text is the one canonical body value
used by active readiness recovery, `gh pr create`, unique draft reuse, and final
projection. Leading/trailing whitespace, trailing newlines, and
Markdown-sensitive spaces are identity data; validators never trim or add a
newline before comparing the remote PR body. After archive, the remote body's
UTF-8 bytes are hashed directly and compared with `publish.body_sha256`; the
task-local body is not reopened.

Schema 1.2 has a 10-file core compatibility allowlist: `task.json`, the three
planning Markdown files, `issue-scope-ledger.json`, legacy task-local Planning/
Phase 2/Branch Review artifacts when present, `closeout-plan.json`, and
`finish-summary.json`. New AI-first tasks normally retain only the seven durable
task/content/plan/summary files because their semantic review checkpoints live
in ignored runtime. Marketplace verification is the only optional eleventh
archive file. Legacy schema 1.1 retains its historical 11-file core plus that
optional verifier, for a maximum of 12.

`projection.move_paths` is the complete task-relative filesystem set moved by
the official archive command. `projection.tracked_move_paths` is the subset
already tracked at `reviewed_content_head`; each requires an active deletion and
archive addition in the one archive transaction. `projection.untracked_archive_outputs`
is the complementary subset created or still untracked while the task is active;
schema 1.2 requires it to include both `closeout-plan.json` and
`finish-summary.json`, which appear only as archive additions. Current
`projection.evidence_paths` is always `[]`: schema 1.2 has no pre-draft metadata
commit. These tracking classes are immutable plan facts derived before archive,
not inferred from post-move status. The reviewed content tree plus the exact
pre-move index/status and archive transaction tree prove the classification.
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
input drift fails before push or file writes. Formal schema 1.2 writes the exact
plan only as an untracked active transaction checkpoint; Publication readiness
and the Finalizer gate stay ignored runtime and are not plan inputs, move paths,
or archive files. Before draft binding, partial retries derive the next missing
transition from the untracked plan, reviewed content HEAD, marketplace owner
evidence when applicable, live Git/GitHub facts, and the active/archive layout.
Passed ledger evidence is never used to reconstruct the initial plan.

`task.archive_locator` uses the same live `YYYY-MM` that the unmodified official
archive command will use. Formal checks it before the first side effect and
again immediately before official move. If the month changes while a schema 1.2
task is still active, dry-run rebuilds only the still-untracked plan with the
new archive-derived values and a new digest, then the same Finalizer loop reviews
and confirms it. No evidence/readiness commit, history rewrite, verifier rerun,
or archive-directory migration occurs. Persisted schema 1.0/1.1 plans retain
their historical committed-plan supersession and recursive lineage validation
only in the explicit compatibility path.

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
move and archive-only for every untracked output. For schema 1.2 it validates
exact dirty/staged paths, the direct `reviewed_content_head` parent, active
absence, archive completeness, tracked blob continuity, and the official
`task.json` delta before it may create the single archive commit. Missing or
mismatched transaction state keeps this metadata recovery path fail closed.

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
path only by the canonical `guru-finish-work` recovery entry; the frozen
`trellis-finish-work` entries may route there as compatibility assets through
Issue #132, while other commands still require `task.json`. Neither path
parses, rebuilds, validates, or rewrites an archived body, summary, ledger,
readiness, or marketplace artifact.

Plan-only recovery does not use an empty task context as authorization. It
loads `closeout-plan.json` from the current commit blob and, before GitHub or
fast-path side effects, validates canonical digest plus Git toplevel,
configured/effective repository, current head branch, base ref availability,
current HEAD transaction, active/archive locator and basename relationship,
summary task/branch/base/source-issue identity, and the exact task directory.
Working-tree plan bytes cannot replace the committed plan. Ordinary task
discovery and workspace-boundary commands do not enable this mode and still
require normal `task.json`, ignored runtime mapping, and live Git worktree
identity. A legacy `task-start-context.json` is only a one-time compatibility
source for that identity.
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
- Changing the legacy task-start-context compatibility reader without updating its strict JSON schema.
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

The Branch Review public input contains only the `branch_review` profile,
workflow/standalone mode, task/base/committed-head identity, and one of
`initial_review|fresh_final_review`. Its public outputs are
the four minimal DTOs defined by the Skill package contract. `review_ref`,
finding refs, and proposal refs are opaque consumer identities, not embedded
artifact bodies.

After a fix commit, finding closure is an internal transient AI judgment by the
finding owner or a real unfinished-agent replacement. It has no public exit or
artifact and automatically dispatches a distinct fresh reviewer. Public input
schema 1.1 and new gate schema 2.2 reject `finding_fix_review`; legacy schema
2.0 gates may retain that value as read-only evidence. Migration carries only
the closure result into a new `fresh_final_review` invocation.

Only `review-gate.json` is written for a new review. A reviewed candidate has
exactly one of `qualified_finding`, `scope_proposal`,
`observation`, `followup_candidate`, or `rejected_candidate`.
`qualified_finding` alone carries P0-P3 severity and must bind requirement
references, scope basis, scenario class, qualification reason,
`introduced_head`, `resolved_at_head`, and closure evidence. `scope_proposal` uses
`unconfirmed_nonstandard_proposal`, contains no severity, and never selects an
implementation route.

The five closed scenario classes are `normal_required_behavior`,
`explicit_nonstandard_requirement`, `approved_nonstandard_expansion`,
`unconfirmed_nonstandard_proposal`, and `out_of_scope`. Qualification always
precedes severity. The last two cannot become current P0-P3 findings.

## Publication Readiness Gate

Ignored-runtime `pr-readiness.json` is the only publication readiness gate.
Active schema `guru-task-publication-readiness-2.0` stores only
`schema_version`, `skill_id`, `task_ref`, immutable `reviewed_content_head`, all
ten AI-reviewed dimensions, findings/closure, scope/Docs/safety conclusions,
and the selected route. Finding summary, scope basis, evidence refs, affected
artifacts, and closure evidence are non-empty. The eight objective entry
preconditions and shared Finalizer preflight are rebuilt transiently by the
recorder/checker; their digests, Branch Review checkpoint, publication identity,
reviewer process, confirmation evidence, and Finalizer publish inputs never
enter this private checkpoint.

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
`task_ref`, `stale_reason`, and target-authored profile/mode/review intent. The
public wrapper reruns the current owner checker; no re-entry narrative or
supersession identity enters the public input, private checkpoint, or exit.
Publication `ready` already runs the same side-effect-free Finalizer preflight
that the first preview uses. Finalizer consumes only the minimal ready DTO and
never augments or interprets the Publication checkpoint.
After the checked output passes its schema, the Publication producer wrapper
deletes that checkpoint before Finalizer entry; a failed check or projection
retains it only for same-owner repair.
The compatibility reader may recognize the old `ready=true` snapshot shape,
but the publication checker rejects it as a semantic pass.

`pr-body.md` and `finish-summary-index.json` remain independent task-local
content inputs, not public handoff state. In the global workflow the caller
authors their initial current candidates after Branch Review `passed` and
before publication invocation; the mandatory `publication_content` entry
binding then validates both exact contents. `ready` binds those bytes, so
Phase 3.7 cannot first create, regenerate, or revise them. The `ready` output is
exactly `exit_id`, `task_ref`, and `reviewed_content_head`; Publication consumes
Branch Review continuity from its current `passed` DTO plus live Git and never
opens the Branch Review private checkpoint. Full review bodies, paths, findings,
histories, and derived bindings stay owner-private or transient.
