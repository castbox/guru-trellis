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
`schemas/skill-registry.schema.json` and has two states:

- `reserved` claims a stable `guru-<action>-<object>` id only. It has no package,
  route, interface, or platform destination and must never be installed.
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
validation. Reserved ids must not appear in markers. Frontmatter auto-match is
discovery assistance only and never replaces mandatory invocation markers.

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
reuses the same resolver/sync core; each semantic-read or mutation guard
consumes the previous post-sync digest and returns the next one.

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

Deep-read shape is source-discriminated: selected archived task artifact,
canonical GitHub issue/PR URL, or exact live Git object/ref. All payload strings
are screened for portable paths and signed-query credentials, and active-task
`task_branch_stale` remains a refreshable complete re-entry reason.

External consumer resolution is part of both source and installed validation.
Skill consumers must name an active registry id. Workflow/stop consumers must
have exactly one matching `guru-workflow-target` / `guru-stop-target` marker;
missing, duplicate, kind-mismatched, or dangling targets fail closed. The
`guru-clarify-requirements` id names the existing Phase 0 workflow route until
#113 activates any separate package.

The package publishes artifact schema `guru-context-discovery-1.0`, scoring
algorithm id `guru-context-history-score-1.0`, and dispatcher-only wrappers for
`preview-change-context-history`, `record-context-discovery`, and
`check-context-discovery`. The history command may enumerate only
`.trellis/tasks/archive/**/finish-summary.json` and project only top-level
`index`; it never reads index siblings, workspace/runtime state, or a repo-level
archive index/cache. Scripts validate AI-authored selection and Gate evidence
but do not select candidates, judge sufficiency, decide duplicate reuse, or
synthesize semantic pass.

The record/check commands require repeatable `--prior-snapshot-input` and
`--expected-prior-snapshot-sha256` pairs for `refresh_base`, ordered from the
oldest `context_ready` ancestor through the direct prior and with one pair per
refresh entry. A chain of `N` refresh entries also requires `N-1` ordered
`--prior-refresh-receipt-input` /
`--expected-prior-refresh-receipt-sha256` pairs. The existing one-ancestor-pair
CLI remains compatible for a single refresh without a receipt. The
deterministic pure gate recomputes every ancestor and receipt identity, binds
exact counts, order, history prefixes and every superseded query/snapshot
digest, requires each receipt to be the unique appended-entry projection from
the preceding ancestor and to equal the next ancestor history prefix, and
accepts only the current appended-entry projection from the direct prior.
Missing, duplicate, reordered, skipped, rewritten, or non-parent evidence fails
closed. Receipts are authoritative only when independently retained with their
digests from the prior production result. Ancestors and receipts are external
evidence, not fields inside the self-hashed result; the recorder re-reads both
chains after a task write, and no evidence bytes are persisted as task data.
Task-local record/check also require the exact target to be non-ignored under
`git check-ignore --quiet --no-index --` before and after recording and during
checking. Ignore matches or unreadable trackability fail closed; pre-task mode
remains stdout-only and does not perform this target gate.

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
