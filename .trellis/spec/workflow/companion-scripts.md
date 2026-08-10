# Companion Scripts

## GitHub CLI Adapter

The shared runtime is the only deterministic GitHub platform adapter. It
normalizes `owner/repository`, rejects high-level commands without `--repo`,
rejects incomplete REST repository endpoints, performs CLI/auth/repository
access preflight, decodes complete JSON, and checks operation-specific required
fields. It exposes only exit code, redacted stderr classification, API fields,
and the six stable error facts defined by `workflow-contract.md`.

It never infers semantic readiness, severity, scope, issue disposition, close
semantics, or workflow route and never falls back to an App, MCP, connector, or
browser. `verification_required` remains reserved for extension-installation
evidence and is not a generic GitHub failure.

## Script Boundaries

### Issue #180 Current Finish And Merge Commands

Current Finalizer commands use ignored
`finalization-transaction.json`, not task-local/archive `closeout-plan.json`.
Preview rebuilds live publication/archive/verification facts; record/check own
only the semantic gate; execute persists the minimal transaction only when it
must return a same-owner recovery exit and retires it at `ready_for_merge`.
Finalizer and `finish-work` never call an Issue-close command.

Publication `ready` has exactly one side-effect owner: `guru-finalize-task`.
Callers may project its reviewed title/body into Finalizer input, but must not
push the reviewed/publication HEAD or create/reuse a PR themselves. Finalizer
performs its remote-branch and exact Open-PR preflight before the first new
remote mutation; an unexpected existing PR, disallowed remote head, or parallel
publication consumer fails closed instead of being normalized as recovery.

The Finalizer-owned publication input is ignored-runtime, short-lived authority
for exact title/body bytes. A provenance `reprepare_required` public DTO remains
minimal; its consumer reloads that private input, verifies task, branch-review
commit and publication-head continuity, and only then rebuilds the plan. Missing
or stale authority, or an attempted fallback to a Closed/replacement PR, blocks.
Successful terminal consumption retires the private input with the transaction.

Current Verifier execution records capability completion incrementally against
the immutable repository/ref/reviewed-head/publication-head/source/profile
tuple. Its recorder/checker recover a successful command whose wrapper output
was lost and rerun only missing capabilities. The durable result is minimal;
full execution facts are ignored runtime and are retired after Finalizer
consumption.

`preview-task-pr-merge`, `record-task-pr-merge`, `check-task-pr-merge`, and
`execute-task-pr-merge` are the deterministic commands for
`guru-merge-task-pr`. All GitHub calls are authenticated, repo-bound `gh`/`gh
api` calls. Preview is read-only. Record/check validate the already performed
AI gate. Execute uses the unique repository merge method and
`--match-head-commit`, then performs only read-only PR/Issue post-merge checks.
No command invokes `gh issue close`, an Issue PATCH mutation, `guru-sync-base`,
PR update/rebase, local base synchronization, or cleanup.

`expected_close_issues` is an exact set that may be empty. An empty set requires
the parsed PR close-keyword set to be empty and performs zero post-merge Issue
closure reads; that zero-length obligation is complete. Non-empty sets retain
exact body equality and per-Issue post-merge closure checks.

`guru-create-task-commit` checker recomputes the objective unpublished,
dedicated-branch eligibility facts. The semantic candidate owns
`routine_auto_commit_eligible`; a checked true value enters the existing exact
staging/ordinary commit executor immediately, with no confirmation parameter or
persisted authorization.

Bash files under `trellis/workflows/guru-team/scripts/bash/` are thin wrappers.
They should use `set -euo pipefail`, resolve their own `SCRIPT_DIR`, and delegate
behavior to the Python companion:

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/../python/guru_team_trellis.py" <subcommand> "$@"
```

Keep argument parsing and workflow logic in
`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` unless there
is a shell-specific reason to handle it in Bash. Existing examples:

- `trellis/workflows/guru-team/scripts/bash/prepare-task.sh`
- `trellis/workflows/guru-team/scripts/bash/resolve-human-artifacts.sh`
- `trellis/workflows/guru-team/scripts/bash/review-branch.sh`
- `trellis/presets/guru-team/scripts/bash/apply.sh`

## Python Runtime Constraints

The companion script is installed into target repositories. Keep it portable:

- Use the Python standard library only.
- Shell out to `git` and `gh` through helper functions such as `run()` and
  `run_stdout()`.
- Use `pathlib.Path` for filesystem paths.
- Use `json.dumps(..., ensure_ascii=False, indent=2)` for user-visible JSON
  payloads and artifacts.
- Keep typed helpers and constants near the top of the file when they define
  reusable contracts.

Reference files:

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`

## Error Handling

Use `WorkflowError` for expected workflow failures in
`guru_team_trellis.py`. Include `exit_code=2` for user-actionable blocked states
such as duplicate issue confirmation, missing review-gate evidence, dirty
non-metadata paths, or incomplete Issue Scope Ledger.

The `main()` function prints a JSON error payload to stderr when `--json` is
used. Do not scatter `sys.exit()` calls through helper functions in the workflow
companion.

The preset installer currently uses `SystemExit` for missing `.trellis/` or
missing source directory because it is a small installer script. If adding more
complex failure modes there, preserve JSON output for normal success and avoid
printing secrets or local-only data.

## Shared Skill Runtime Dispatcher

`scripts/bash/run-skill-command.sh` is the only public dispatcher for active
Guru Team Skill package validators. The Bash file remains a thin wrapper around
the Python `run-skill-command` subcommand. Package wrappers pass only
`--package-root`, one fixed `--validator` id, and the original arguments after
`--`; they never select a runtime path or call a companion command directly.

Before the target companion command runs, the Python dispatcher must derive the
repository root from its audited installed location and component-wise `lstat`
the dispatcher, package root, package interface, installed extension manifest,
installed package inventory, and selected discovery copy. It must then validate
current Interface 1.3, its exact `semantic` or `deterministic` stage profile,
`runtime_dependency`, extension/runtime API identity,
dispatcher identity, distribution/portability, installed package drift, the
fixed validator id, and its declared `runtime_command`. The command must be a
published extension `companion_scripts` id and map to the managed executable
`.trellis/guru-team/scripts/bash/<runtime-command>.sh`.

Any missing manifest/dispatcher/package, incompatible API, dependency or
command mismatch, unmanaged discovery copy, sidecar, or drift exits 2 before
the companion command. The error must say that the Skill package is not
self-contained/portable, instruct the caller to install or upgrade the complete
Guru Team preset, resolve `.new` / `.bak`, rerun source and installed package
validation, and retry. There is no alternate-command fallback. Runtime dependency
validation is an objective precondition only and never becomes an AI Review Gate pass.

## Skill Contract Discovery

`scripts/bash/discover-skill-contract.sh` is the thin installed wrapper for
the deterministic `discover-skill-contract` subcommand. Its public CLI is
exactly:

```bash
discover-skill-contract --root <repo> --mode <source|installed> \
  --skill <guru-id> --json
```

The command resolves the registry row, validates the exact current
registry/Interface 1.3 identity, then returns package-relative locators for the
input, invocation, every per-exit output/example, consumer input, projection,
and private artifact. It does not execute the semantic Skill, read private
artifact contents, or ask callers to import the Python runtime.

Source package validation performs the separate representative invocation
probe declared by each 1.3 fixture interface. It executes the package-local
wrapper with its exact example argv, requires a single JSON object containing
one declared exit, validates that object against the independent exit schema,
and applies the declared consumer projection to the actual stdout object.
`kind=skill` is accepted only with a target-owned `skill_input` whose
`interface_path` exactly equals the active registry row's canonical target
interface and whose referenced interface id equals the consumer id.
Structured `kind=workflow` and `kind=stop` contracts are accepted only when the
original locator is already canonical and resolves below the exact
`consumers/workflow/` or `consumers/stop/` owner root. The runtime rejects
producer-package reuse, cross-kind roots, `.`/`..`, repeated separators,
absolute paths, missing files, and symlink components before loading the schema;
zero-payload stops retain no contract locator.
Non-`direct` projections and `direct` projections into `scalar_cli` additionally
prove required-field totality and a conservative all-valid-output
schema/normalizer relation; example-only agreement is insufficient. Public
output/private artifact schema ids and paths are checked as separate disjoint sets. The
invocation wrapper must match the dispatcher-only template as complete bytes,
so comments, dead code, or local `printf` cannot impersonate routing. A
zero-payload stop accepts only the required exit routing identity and an empty
`select` mapping; aggregate structured input binds exact ordered profile schema
references and required discriminator constants; scalar input binds exact
ordered typed argv in both public-input and invocation examples. Wrapper/handler failures,
non-object or multiple stdout values, unknown exits, and output-schema mismatch
fail with stable portable errors.

For the five approved production semantic edges, the same target ownership
check accepts `skill_input_authoring_seed`. The validator exact-resolves the
target structured profile and its package-local authoring example, requires
disjoint `seed_fields` and `authoring_fields`, requires their union to equal the
profile's complete top-level required set, and requires the independently
validated projected seed and authoring example keys to equal those sets. It
then performs a no-overwrite merge and validates the merged object against the
complete target profile schema before a consumer probe can run. Any overlap,
overwrite, missing/extra/unknown field, default/literal/private lookup, or
runtime-authored semantic value fails closed. Projection execution remains
limited to `direct|select|rename|normalize`.

## Current Intake Public Invocation Runtime

Each current Intake package in the active registry owns one dispatcher-only
public wrapper declared by Interface 1.3 `public_contracts.invocation`. The
wrapper passes its package root, fixed `public_invocation` validator id, and
public argv to `run-skill-command`; it contains no local business logic,
semantic route selection, private artifact parser, fallback runtime, or
typed-output fixture. Only the live registry and current package contracts are
valid invocation authority.

`guru-sync-base` binds its declared scalar CLI arguments directly. The other
five packages bind their current closed structured profiles and receive public
input through either an exact declared package example or a repo-relative
caller JSON path. Runtime validates only current caller-owned fields; user
authorization and a workspace/task mutation refusal remain conversation-local.
For semantic packages the public wrapper runs only after the owner loop has
recorded its result, reruns the current objective checker, and derives the route
from checker-passed owner evidence. It never accepts a caller-selected expected
exit, reads another Skill's private checkpoint, or reads a public output example
as production input.

`guru-sync-base` executes the formal resolver, executor, and checker inside the
public invocation. Its public `base_branch` scalar is optional: an explicit
value keeps its existing priority, while omission passes an unspecified value
to the formal underlying resolver, which continues to own configured scalar,
candidate-order, and remote-default fallback. The wrapper does not implement a
second fallback order. The other five
packages' owner loops reread Git/GitHub/Trellis state and derive HEAD, digest,
hash, size, mtime, absolute path, and freshness facts before serialization.
Those runtime-derived facts are never required from the Agent-facing public
input.

The clarification serializer treats `target_disposition=null` as public
`retained` only for a checker-passed `active_task_scope_change` clear result.
Initial and standalone null dispositions continue to fail closed.

The Agent remains the semantic owner of scope, adequacy, findings, confirmation,
and typed route for semantic packages. Runtime may only validate the declared
route and objective facts, execute the package's recorder/validator/executor,
apply `direct|select|rename|normalize`, and serialize exactly one declared exit
DTO. Public failures use only stable `code`, repo-relative `field_path`, and
`remediation`. Normal invocation does not load `evals/**`, and an Agent or
consumer must not read or import `guru_team_trellis.py` to perform discovery,
invocation, projection, or error diagnosis.

## Production Public Invocation Runtime

`guru-approve-task-plan`, `guru-check-task`, and `guru-create-task-commit` use
the same dispatcher-only wrapper template and shared public invocation command
as the Intake packages. Invocation identity is resolved from the active
Interface 1.3 registry and the sole current `production-current-v1` contract
manifest. `invoke-stage0-skill` is the current shared dispatcher command id
even though it serves every active production package.

Planning/check invocation validates the selected closed public profile,
materializes the current owner input in ignored runtime state, calls the
existing owner recorder and checker for `task_ref`, and selects the actual exit
only from checker-passed owner evidence. Commit invocation consumes the minimal
Phase 2 DTO plus fresh AI-authored path classifications, structured commit
message fields, and semantic result. A deterministic builder rereads the
current task, ledger, HEAD, base, dirty snapshot, sequence, remote branch and
repo-bound Open PR facts; constructs the ignored-runtime
`guru-task-commit-candidate-4.0`; canonicalizes the complete message; runs the
shared parser; and, only for checker-passed `committed` with
`routine_auto_commit_eligible=true`, calls the exact executor immediately.
User authorization remains dialogue-local and never enters the
public input, candidate, result, or archive.

The builder may return `revision-required` or `blocked` from the caller-owned
route intent before Git mutation. A `committed` result is projected only after
the executor returns a committed result and current HEAD equals its commit SHA.
Public output is exactly `exit_id`, `task_ref`, `base_ref`, and
`branch_review_commit`; candidate/result bodies remain private.

Public consumer probes for planning self-reentry, check-to-commit, and commit
self-reentry consume only the producer's minimal DTO to build the declared
seed. Fresh AI-owned authoring is loaded from the exact target-package example
for validation/probe purposes, never synthesized by runtime. The seed and
authoring objects are validated separately and merged without overwrite before
the target wrapper is invoked; no producer gate/checkpoint/candidate artifact
is read to fill the target input.

Because the installed runtime is Python-standard-library-only, 1.3 contract
validation implements a recursive closed subset of Draft 2020-12, not
the complete vocabulary. It validates the supported keyword grammar before
validating any interface/example instance, rejects every unknown keyword,
malformed keyword value, and nested `$id` resource boundary, and supports a
root-only `$id`, local refs, plus the aggregate input's
exact boundary-contained package-relative profile index. Boolean schemas, remote/unresolved/recursive refs,
`patternProperties` and other unimplemented vocabulary, unsupported formats,
and invalid regexes fail closed. The same grammar check applies to the current
canonical registry/interface schemas and every Interface 1.3 public/private
contract asset. The live registry and current package contracts are the
complete schema-validation input.
The exact accepted syntax and ECMA Unicode-mode search semantics are owned by
`skill-package-contract.md` under `Portable Pattern Grammar`. The runtime uses
one portable compiler for both the schema grammar gate and instance matching;
it projects instance strings onto UTF-16 code units, preserves interior
zero-width search positions, prevents Unicode-consuming atoms from splitting or
starting inside a valid surrogate pair, and consumes isolated high/low
surrogates independently even when a BMP code unit is adjacent. The single-unit
guard excludes only a valid pair start or its interior low surrogate; it does
not exclude an arbitrary BMP unit after an isolated high surrogate. The compiler
also translates strict end anchoring, dot line terminators, and the exact ECMA
whitespace set to Python-standard-library equivalents. It never passes the
original contract pattern to raw Python `re.compile` or `re.search` as a
fallback.
All 1.3 contract and route-marker JSON ingress, package-local refs, and executed
invocation stdout reject non-standard constants and numbers outside the finite
runtime range; in-memory schema/instance validation repeats the finite guard.
Public JSON egress disables non-finite encoding and preserves structured errors
without tracebacks. The closed `date-time` and `uri` implementations follow the
RFC 3339 and RFC 3986 normal syntax boundaries defined by
`skill-package-contract.md`, including lowercase `t`/`z`, leap-second clock
position, calendar/offset validation, required URI scheme, valid percent
encoding, and rejection of whitespace/control characters.

Discovery failures use one closed object with `code`, repo-relative
`field_path`, and `remediation`. Stable codes distinguish unknown skill,
registry/interface version mismatch, missing or unsafe asset, invalid
schema/example, and installed drift. These are deterministic contract facts;
the command never decides semantic pass, scope, route intent, or migration
priority.

### Planning Approval Record And Check

`record-planning-approval` and `check-planning-approval` are the shared
deterministic runtime commands for `guru-approve-task-plan`. Package wrappers
dispatch to these same commands; no parallel artifact or
second runtime implementation is allowed.

The recorder consumes one already completed AI semantic result and writes the
closed `guru-planning-approval-3.0` projection to the owner-private ignored
runtime checkpoint. It validates the exact authored field set, mode, current
task/planning locators, non-empty required planning files, unique authority
refs, compact Docs SSOT shape, semantic/exit/consumer union, and output schema.
It does not copy Git state or current file bytes into the checkpoint.

The checker reads the owner checkpoint, rejects symlinks and unknown schemas,
revalidates schema closure, exact task/planning locators, required non-empty
files, the semantic/exit/consumer union, and any requested exit. It returns only
objective status, locator, exit, and consumer facts. Neither command decides
scope, sufficiency, findings, revision actions, unusual-scenario meaning,
authorization, semantic pass, or route.

The checker accepts only artifacts that validate against current schema 3.0;
every other shape fails closed through the normal checker result. Archived
artifacts are not rewritten.

### Change-Context Preview, Record, And Check

`preview-change-context-history`, `record-context-discovery`, and
`check-context-discovery` are the deterministic commands for
`guru-discover-change-context`. Their Bash wrappers remain thin and their
package wrappers reach them only through `run-skill-command`.

Preview accepts canonical clue arrays and a fixed limit no greater than 20. It
recursively opens only archived `finish-summary.json` files, projects only
`index`, applies `guru-context-history-score-1.0`, isolates malformed, missing,
shape-invalid, ordinary unreadable, and non-file records with stable portable
error rows, and emits query,
archive-manifest and preview digests. It performs no AI selection,
relevance/sufficiency judgment, duplicate decision, deep-read, mem lookup, or
write.

Record accepts one AI-authored reviewed result from stdin or an explicit input
file, normalizes and validates it, and writes canonical JSON only to stdout.
Check accepts that same stdin/file transport and returns the objective checked
exit. On normal pre-task/standalone calls neither command accepts a task
locator, resolves a task artifact, checks Git trackability, replaces prior
bytes, records supersession state, or writes a repository/runtime file. A
normal active-task workflow call supplies `--active-task` independently to
record, check, and public invoke; this binds the direct task branch and current
task worktree while remaining checkpoint-free and permitting ordinary task
edits. Only a real interruption additionally supplies matching
`--recovery-continuation-id` on all three calls, which binds one minimal current
checkpoint below the exact task owner namespace and never copies live facts or
the complete owner result into it. The public wrapper accepts `--owner-result
-`, checks the same bytes, builds one schema-validated typed exit, and only then
consumes a recovery checkpoint and empty owner directory. Stale or invalid
recovery is deleted and rerun from live authority.
Record/check first execute only pure schema, digest, entry
clue, and semantic-evidence shape validation. `change_input` has ten closed clue
arrays and at least one must be non-empty; a separate issue binding or canonical
query cannot satisfy this entry precondition. The next stage is the base-only
live gate. Any base stale result returns before repository-bound query/current/
deep-read locators, GitHub issues, reviewed blobs, or archive/history are read.
Only a fresh base permits those remaining locator and live checks. Portable
locator validation is structural and source-specific; it does not scan every
payload string.
Source-issue freshness accepts the normalized live GitHub states `open` and
`closed`; duplicate candidates and a reviewed draft's created-issue binding
remain independently open-only. Every 40-character reviewed Git identity must
resolve from `HEAD:<path>` to an object whose live type is exactly `blob`.
Trees, gitlink commits, tags, missing objects, and mismatched blobs fail closed
for Docs, code/contracts, and tests evidence alike.
Task-artifact locators must remain inside the selected archive task, GitHub
locators must be canonical issue/PR URLs without query or fragment, and Git
locators must be exact live object/ref identities.

Duplicate candidate facts use one deterministic projection: normalized bound
`repo`, positive `number`, `identity=#<number>`, canonical issue `url`,
`state=open`, and `updated_at`. The pure gate recomputes `facts_sha256` from
only those fields and validates identity plus canonical URL from the same one
search result. Record/check do not issue a second duplicate search or re-read
candidates after AI review.

Pre-task and standalone checks bind the live checkout to the base-sync decision
branch. Zero candidates require empty selection/deep reads plus the exact
`not_needed` mem shape; a `used` or internally inconsistent `not_needed` shape
fails schema and runtime validation before any other history source is accepted.

Any base freshness error short-circuits before live issue/draft,
reviewed-blob, or archive-preview reads. Git status failure is a stable
fail-closed fact, never a clean checkout. `refresh_base` is accepted only when
the caller-authored refresh entry's stable error codes exactly match live
refreshable drift; the same errors reject `context_ready`, so scripts validate
but never choose route intent. Candidate-present `mem_review.status=used`
requires a non-empty summary after all four sources are exhausted; a passed AI
Gate requires non-empty reviewed scope and load-bearing conclusions. Closed
schema fields and source-specific locators keep raw source payloads out of
persisted evidence through field-specific validation. `task_branch_stale` is
refreshable; malformed task facts are not.
Expected failures use stable error codes and do not include raw JSON content,
exception strings containing local paths, or secrets.
The schema and runtime additionally enforce the exact semantic state pair
`typed_exit=blocked` <-> `ai_review_gate.status=blocked` in both directions.

### Requirements Clarification Record And Check

`record-requirements-clarification` and
`check-requirements-clarification` are the only runtime commands published for
`guru-clarify-requirements`. Canonical Bash wrappers remain thin; package
wrappers reach them only through `run-skill-command` with fixed validator ids.
There is no mutation executor command.

Record accepts one AI-authored closed payload from stdin or an explicit input
file. It normalizes timestamps and canonical lists, derives proposal/action/
payload/content/result SHA-256 identities, validates the semantic state shape,
and emits the canonical `guru-requirements-clarification-2.0` result on stdout.
Only the closed current schema is accepted before normalization.
It never chooses a question, action, scope decision, confirmation requirement,
AI Gate status, or typed exit. Pre-task and standalone modes reject an output
path and perform no repository write. Active-task mode still creates no
dedicated clarification artifact: it validates caller-authored bindings to the
existing live issue authority, `issue-scope-ledger.json`, `prd.md`, `design.md`,
`implement.md`, current context/task-update facts, compact decision
classification, and re-entry owners. It requires an exact closed scope-only
Ledger 2.0 and keeps the `decision_trail` only in the transient owner result.
Active-task `clear`/`new_task` requires a non-empty terminal proposal set, and
each of the five scope classifications requires one finalized disposition in
that trail. The trail contains only `trail_id`, proposal id/digest/decision, and
remote authority kind/URL/content checksum. It stores no user identity,
confirmation ref, authorization
state/digest, authority timestamp, planning identity, review state, context
snapshot, interrupted target, or re-entry route. Mechanism dispositions require
optional origin and stay outside trail/action mutation. A mechanism-only terminal result still supplies
the current ledger/planning/context/re-entry
evidence with `decision_trail=null`, and it runs through the same task-local live
freshness checker as classification and mixed results. Inputs must satisfy the
current schema before normalization; any mismatch fails closed.

Check accepts the recorder result from stdin or an explicit input file. It
recomputes every derived digest, executes the published closed schema and pure
invariants first, and then reads only the declared live GitHub/Git/task facts
needed for freshness. It may report `needs_context`, `refresh_context`, or
`retarget_context` only when the caller-authored typed exit and deterministic
missing/stale/selected-target facts agree;
it never infers route intent. It must not write GitHub, Git, task artifacts,
workspace state, runtime caches, or sidecars.

GitHub `issue_comment` and `issue_body_edit` mutations are AI-owned. Before a
write the AI rereads the target preimage, verifies the exact objective target
and payload, and obtains any required authority only from the current dialogue;
it then uses only authenticated, explicit repo-bound `gh` / `gh api` and
rereads the result. No GitHub App, MCP, connector, browser UI, or implicit
repository context is an allowed fallback. No authorization field is passed to
or checked by scripts.
Recorder/checker only normalize and validate supplied URL/state/
updated-at/body-or-comment digest facts. The mutation result content digest
must equal the exact `source_actions[].payload.body`, its canonical
payload digest, and the reread live body/comment bytes. Successful GitHub mutation requires
`refresh_context`. `new_issue_draft` remains side-effect-free and requires
`new_task`; no script in this Skill creates an issue. Active-task GitHub
authority mutation requires `refresh_context` before task update. A later
active-task `clear`/`new_task` validates live authority kind/URL/content/time,
requires context `generated_at >= authority.updated_at`, and binds the task
update preimage to that context digest. Task-only update requires no second
context digest change.

Pure validation rejects repository-answerable questions left pending or marked
`answered` without checked evidence before a user round, multiple question ids
in one round, a round whose question id was neither already open nor opened by
that round, a partial answer closing any question, close-before-open,
closure-then-reopen, an unfinalized expansion decision, an optional-mechanism
proposal accepted into current scope, an active-task inclusion without exact
ledger/planning/re-entry linkage, an empty/non-final active-task proposal set,
any five-class active-task classification without an exact trail disposition, a
mechanism disposition with trail/action mutation, an incomplete
planning set, a missing/mismatched compact ledger classification or GitHub authority,
mutation without fresh re-entry, open questions on `clear`, blocked/Gate
matrix mismatch, and any exit/consumer mismatch. Expected failures use stable
non-secret error codes and never echo raw payloads, local absolute paths, or
credentials.

### Task Workspace Record, Execute, And Check

`record-task-workspace-plan`, `create-task-workspace`, and
`check-task-workspace-result` are the deterministic commands published for
active semantic `guru-create-task-workspace`. Their Bash wrappers remain thin;
package wrappers reach them only through `run-skill-command` and fixed
validator ids.

The recorder accepts one AI-authored plan, validates the closed plan schema and
current prerequisite projections, derives canonical digests, and emits the
plan on stdout. It does not choose the final target, duplicate disposition,
naming, assignee route, confirmation requirement, AI Gate, or typed exit.

The executor consumes the exact plan digest. Before each mutation it rechecks
base, target, prerequisite bytes, objective action scope, plan digest, and
current Git/worktree/task facts. The AI alone checks current-dialogue authority
before invoking it. A draft invocation creates the exact reviewed issue
using the reviewed title/body bytes without trimming or newline insertion. It
immediately rereads it and emits a created-issue result with
`typed_exit=refresh_review`, and stops without branch/worktree/task/runtime
writes. An open-issue invocation creates or reuses only exact matching
branch/worktree/task identity. In an isolated subprocess it calls official
`common.task_store.cmd_create` with the reviewed assignee and replaces the
module's developer accessor with a null result only for that handler call, so
  official fallback writes `creator=assignee=reviewed login`. It then writes
  exactly one Guru-owned task-local tracked Intake artifact,
  `issue-scope-ledger.json`, and only ignored
`.trellis/.runtime/guru-team/**` mappings.

Before draft creation, the executor lists live open issues and filters exact
title/body/label matches whose `createdAt` is not earlier than the reviewed
plan capture. It creates only for zero matches, recovers and rereads one match,
and blocks on multiple matches. This makes a retry after successful remote
create plus failed immediate reread reuse the first issue. A later open-issue
plan embeds the complete checker-passed created-issue result; its result and
binding digests, reviewed draft/content identity, current issue, and context live
existing-issue identity are revalidated before workspace/task mutation. The
fresh context uses `kind=issue` and null `issue_binding`, not the pre-create
draft projection.

Immediately before the first permitted GitHub or workspace/task mutation, the
executor reconstructs the original resolver inputs from the checker-passed
base prerequisite, calls `resolve_base_selection`, then `execute_base_sync`,
and validates the fresh result. The plan's `post_sync_resolution_sha256` plus
selected ref and HEAD projection must remain exact. If fetch reveals a normal
remote advance, safe fast-forward may occur but the executor returns
`refresh_review` before any issue/workspace/task/artifact/runtime write. Later
same-invocation guards revalidate the already refreshed plan and local facts;
they do not add locks, concurrency protocols, or a second remote sync loop.

The checker validates the result schema, plan linkage, live issue or
branch/worktree/task identity, artifact bytes/schema/digests/trackability,
runtime ignore state, and workspace boundary. It never turns deterministic
success into a semantic pass or selects a recovery route. Existing objects or
artifacts may be reused only when all identity and bytes match; mismatch fails
closed without overwrite.

Refusal stops in dialogue before recorder/executor and emits no plan, result, or
DTO. The only non-mutation typed results are AI-authored `reroute` ->
`refresh_review` and `blocked` -> `blocked`; the executor/checker validate that
matrix and zero-write snapshots without reading authorization state. Public result stdout omits the
absolute workspace path and the checker derives it from current config, the
reviewed slug, and live Git facts.

Neither command reads, creates, copies, initializes, restores, or deletes
`.trellis/.developer` or `.trellis/workspace/**`. Existing official identity
bytes are unchanged; clean source/target inputs remain absent. The public
plan/result contain no absolute paths, runtime paths, full process output,
secrets, or raw private records.

## GitHub and Git Operations

### Shared Base Resolution And Sync

`sync-base` is the only deterministic owner of selected-base resolution and
safe refresh. The fixed precedence is explicit `--base`, non-empty scalar
`base_branch`, the first existing exact local or remote-tracking ref in
`base_branch_candidates` order (default `dev`, `develop`, `main`, `master`), then
remote default from `git ls-remote --symref <remote> HEAD` when no candidate
exists. Multiple existing candidates are ordered, not ambiguous. Validate every
candidate with `git check-ref-format --branch`. Remote-default failure blocks.
Never fall back to the current branch. Evaluate and validate sources in
precedence order: once a higher-priority explicit or scalar source is selected, malformed
lower-priority scalar or candidate input must not reject that selection.
Candidate validation still fails closed before config-candidate or
remote-default facts are produced when neither higher-priority source is selected.

`--resolve-only` emits canonical resolution JSON and SHA-256 before fetch. The
digest covers the complete resolution object, including decision checkout
branch, HEAD and clean state. It
does not write a resolution file. `--execute` requires the expected digest,
recomputes resolution at the execution boundary, and blocks before fetch if
digest, checkout identity, or
resolution changed. The executor uses only:

```text
git fetch --no-tags <remote> refs/heads/<base>:refs/remotes/<remote>/<base>
git merge --ff-only <remote>/<base>
```

The merge is legal only when the clean decision checkout is the selected base
and local base is an ancestor of remote. Missing local/remote refs, dirty state,
fetch failure, divergence, wrong checkout, or post-sync mismatch blocks. It
must not use `git branch -f`, reset, checkout, stash, rebase, force fetch, or a
current-branch fallback.

After synchronization, the executor rebuilds the same source/base/remote/
candidate resolution identity with the synchronized decision checkout and emits
it as `post_sync_resolution` plus `post_sync_resolution_sha256`. The original
`resolution.resolution_sha256` remains the pre-sync identity that binds only
resolve to execute. Already-equal execution may produce equal pre/post digests;
a fast-forward must produce a different post-sync digest.

`check-base-sync` does not mutate Git. It consumes `--result-json` and validates
Draft 2020-12 schema identity, `facts_sha256`, the pre-sync resolution digest,
the post-sync resolution object/digest, selected refs, clean state, and
decision/local/remote full-SHA equality against live Git. Its successful typed
output carries `post_sync_resolution_sha256` for the next consumer instead of
re-exporting the pre-sync digest. It does not fetch, merge, decide scope, judge
semantic pass, choose a route, or manage evidence files. Its workflow-only
`--record-skipped` path emits stdout-only machine facts after the AI has
reviewed a non-repo route; standalone rejects that path.

`prepare-task` requires the prior validator/guard
`post_sync_resolution_sha256` and the same resolver inputs. It calls the shared
resolver/sync core before `gh auth status`, issue read, and duplicate search.
It has no mutation path. `--base-branch` can assert equality but cannot rewrite
config/config-candidate/remote-default provenance as explicit. The planner
freshness functions remain adapters to the shared core. A stale
planner result is blocking, not permission to continue planning. Each guard
consumes the preceding validator's post-sync digest and returns its current
post-sync digest. Neither prepare output nor any task artifact or runtime
checkpoint persists the complete resolution/result stdout payloads.

Always gate GitHub operations with `gh auth status` through `require_gh_auth()`.
Do not assume the GitHub CLI is configured just because `gh` exists.

`prepare-task` is query-only. It may call `gh issue view/list` for explicit
issues and duplicate search, but output stays on stdout and it never calls
`gh issue create`, `git worktree add`, or `task.py create`. The exact workspace
executor may reuse base, naming, GitHub, worktree, and task helpers, but no
second mutation entrypoint exists.

Before publish, reject uncommitted non-metadata changes. Metadata-only paths are
defined by `METADATA_ONLY_PREFIXES` and `METADATA_ONLY_FILES`; update these
constants deliberately if Trellis metadata ownership changes.

Task work commits use three deterministic entrypoints.
`prepare-task-commit` writes and validates the next ignored-runtime candidate,
canonicalizes its structured Chinese Conventional Commit message, and runs the
shared `validate_commit_message()` parser before the commit action is shown.
`check-commit-messages --candidate-artifact <ignored-runtime-path>` repeats
schema, task, HEAD, complete dirty snapshot, path classification, exact stage
set, message, parser, and Git-operation-state validation. `create-task-commit`
accepts only the current schema 3.0 candidate; every other shape fails closed.
The range form of `check-commit-messages` is standalone diagnostics only;
Branch Review, Publication, and Finalizer do not consume it or use commit
subject/body/`Refs` as a freshness gate.

The executor materializes exact reviewed blobs/modes in an isolated index and
detached transaction HEAD, runs the repository's real commit hooks, and verifies
parent, raw message bytes, committed paths, complete tree, gitlink identities,
candidate bytes, live worktree, operation state, branch ref, and live index
preimage before publication. Rename sources inherit deletion authority; copy
sources do not. A non-deleted gitlink is written with `git update-index
--cacheinfo` from the reviewed `gitlink_head`, never reread through broad
`git add`.

After isolated validation, standard Git compare-and-swap
`git update-ref <ref> <new> <old>` publishes the commit and `git reset --mixed
--quiet HEAD` refreshes the live index. The runtime does not create its own
lock, atomic-replace, rollback, linearization, or concurrency protocol. Any
failure before `update-ref` leaves the live ref/index untouched; a failure after
the conditional ref advance reports the created commit for bounded same-plan
recovery instead of attempting a custom rollback. On success the candidate is
removed and immutable Git history remains the source for parent, message, paths,
and tree facts.

Neither command classifies scope, authors message semantics, chooses a route,
pushes, rewrites published history, stashes, amends, rebases, force-updates, or
uses broad `git add`.

### Legacy Closeout Plan Engine Compatibility

The following closeout-plan engine contract is retained only for explicit
legacy selectors and regression fixtures. Current Finalizer preparation,
re-entry, recovery and archive routes use the Issue #180 transaction commands
defined at the top of this document and never select `closeout-plan.json`.

Legacy `finish-work.sh` is an internal helper, not the normal user path. It must reject
ordinary direct calls before closeout-plan, push, draft PR, archive, or publish
side effects; only `guru-finalize-task`'s checked private transition executor
may invoke it. Direct calls report `required_entrypoint=guru-finish-work`.
The canonical user route is `guru-finish-work`. Every interruption returns
through the same finalizer semantic loop and mapped recovery consumer.

Finish-summary separates AI judgment from deterministic facts without a second
AI-authored handoff file. Publication supplies one exact reviewed PR payload;
Finalizer parses its required change-summary section, injects
task/Git/ledger/artifact/time/PR facts, classifies affected surfaces from exact
changed paths, derives search terms and `retrieval_text`, and validates current
finish-summary schema 2. Historical schema 1 remains discovery-readable but is
never written by the current path. Dry-run and formal
finish call the same `prepare_closeout()` pipeline. Dry-run returns the
immutable `closeout-plan.json` bytes and canonical `closeout_plan_digest`
without writing. Formal finish requires `--expected-plan-digest`, rebuilds and
compares the plan before its first side effect, then persists the exact plan as
an untracked active transaction checkpoint. Publication readiness and the
Finalizer gate remain ignored runtime; neither is copied into the plan or task
archive. Formal finish never writes an empty-PR summary,
never invokes upstream `add_session.py`, and never reads/writes
`.trellis/workspace/**`.

Prepare parses `.trellis/config.yaml` with the installed official
`parse_simple_yaml` implementation and binds the empty `hooks.after_archive`
state into protected inputs. Missing or empty configuration is supported;
non-empty, ambiguous, unreadable, NUL-containing, or symlinked configuration
fails before push, PR creation, or archive. The companion never executes or
interprets an `after_archive` command and does not include hook mutations in the
transaction allowlist.

Prepare must also build and schema-validate the complete future archived
finish-summary before dry-run/formal diverge. The immutable plan stores that
template with the fixed maximum-width sentinel PR
`#9223372036854775807`, its exact UTF-8 `write_json` byte digest, the Branch Review Gate
`generated_at` snapshot time, and the only runtime-substitution fields:
`github.pr_url` and `index.search_terms.pr_refs`. Formal final projection copies
the template and substitutes one canonical PR identity; it does not call the
general summary builder after content push, verifier, or draft
creation. Dry-run and formal therefore expose the same local build/path/schema
errors before the first side effect.

Formal finish first verifies that the current branch HEAD preserves the reviewed
content identity, pushes that HEAD, invokes the current verification owner
against the remote commit, and validates the resulting
task-local `marketplace-verification.json` while keeping the scope-only Ledger
bytes unchanged. Closeout schema 3.0 keeps that artifact uncommitted until the
one archive commit; it binds the exact Publication-reviewed title/body and does
not create a separate plan/readiness/evidence metadata commit. It then creates or reuses
one draft PR for the exact base-repo/head-repo/head-branch/base-branch/title/body
identity. Every effective fetch and push URL for `plan.git.remote` returned by
Git is preceded by a raw-config gate. The validator reads every
`remote.<name>.url` and `remote.<name>.pushurl` with NUL-delimited values and
origins, rejects empty values, boundary whitespace, Unicode/ASCII controls,
ambiguous framing, unreadable origins, and any NUL byte in a relevant config
file. Missing `pushurl` uses the raw `url` set, matching Git semantics. Every
raw `url.*.insteadOf` / `url.*.pushInsteadOf` base and pattern receives the
same boundary/control/origin validation before rewrite. Effective output is
then consumed without trim/normalization, must have one newline-delimited value
per raw source value, and after Git rewrite resolution must use one credential-free
GitHub transport form: `https://github.com/<owner>/<repo>[.git]`,
`ssh://git@github.com/<owner>/<repo>[.git]`, or
`git@github.com:<owner>/<repo>[.git]`. HTTP, `git://`, `file://`, local or bare
paths, scheme-less host/path forms, userinfo/password/token variants, explicit
ports, query strings, fragments, and extra path segments fail closed. Each
strictly parsed URL and `headRepository.nameWithOwner` must normalize to the
immutable `plan.git.repo`; `headRepositoryOwner.login` must agree and
`isCrossRepository` must be `false`. Because `gh pr list --head` cannot scope
by owner, the query requests all three head-repository fields, rejects missing
or inconsistent fields, and rejects a same-name cross-repository candidate
before applying the 0/1/>1 exact-candidate rule. Before archive, the body
identity is `plan.publish.body`: no trim, newline insertion, or second
normalization is permitted between Publication projection, plan digest, create,
reuse, and final projection. After the official move, remote PR queries are
checked against the plan's exact title/body; they do not reopen Publication
readiness. The normal flow also
carries the already-bound PR number/URL across archive and ready confirmation.
A fresh exact-archive reentry recovers that number/URL from the immutable
commit's deterministic `finish-summary.json` blob, without opening the
working-tree summary or invoking the general summary validator, then requires
the unique target-repository repo/head/base candidate to match it. A fork
candidate, multiple target-repo matches, changed title/body, or a number/URL
change within one bound invocation fails closed.
The canonical PR URL is used to build the only final finish-summary in the
active task, including exactly one `PR #<number>` ref. A temporary future
archive projection validates schema, path safety, artifact locators, ledger,
gate, readiness, and the exact archive allowlist before the official
`task.py archive --no-commit` move.
Final projection and both incomplete/exact recovery use the same strict PR URL
parser. It compares GitHub owner/repository identity case-insensitively against
normalized `plan.git.repo`, but preserves the exact valid remote URL casing as
the canonical summary output. It still rejects a different repository,
non-HTTPS transport, invalid owner/repository component, non-positive or
leading-zero number, trailing/extra path, query, and fragment.

The finish-work prepare path accepts PR title/body only through the current
Finalizer `publication_ready` input. It validates strict UTF-8 JSON strings,
required Markdown sections, objective body quality, Issue Scope Ledger
semantics, and exact equality through the readiness output and immutable plan.
No `--body-file`, `--body-artifact`, alternate locator, task-local fallback, or
generated body source participates.

Marketplace machine evidence uses the task-relative locator
`marketplace-verification.json`, never the active task path. Final projection
resolves that locator while the task is active, requires the artifact bytes to
exist, and requires the ledger digest to match. Archive and archived recovery
never parse or rewrite the ledger or verifier artifact.

The archive transaction creates one metadata commit containing only the
prevalidated active-to-archive task move, pushes it, and requires local branch,
remote branch, and draft PR head to match. Only then may the executor run
`gh pr ready`. A retry derives its exact failed transition from persisted
untracked plan, pending or passed marketplace evidence, final-summary presence,
active/archive locators, Git index/tree state, remote HEAD, and PR identity
before archive; after the move it uses only the committed plan, exact
path/blob/commit lineage, remote HEAD, and remote PR identity. It
must not repeat a completed push, verifier, draft bind, or
final projection and must not skip the failed transition. After archive
push it may only recheck identity and retry draft-to-ready; it must not rebuild
artifacts, rerun the verifier, commit, or push.

Immediately before official `task.py archive`, the executor rechecks the
official current `YYYY-MM`, the empty `after_archive` state, a clean index, the
exact planned untracked output set, every tracked path as a regular file, Git
mode equality (`100644`/`100755`), and working bytes against the transaction-parent blob.
Any failure leaves the task active and the PR draft; official archive has not
run.

Before dry-run and formal diverge, prepare lexically `lstat`s each existing
archive root, month, and final destination component. It rejects every symlink,
including dangling links and links to repo-internal targets, without following
or reading the target; the final locator must also be absent. The identical
preflight runs again immediately before official move to reject
prepare-to-move drift. Prepare also validates the effective
`task.json.children` value as `list[str]` and mirrors
official active-task exact/suffix lookup. A matching active child with
`task.json` blocks because official archive would rewrite that child; an
already archived child is historical metadata and does not block the parent.
Initial failures happen before Git, GitHub, or recorder mutation.

Schema 2.0 archives exactly the durable files that exist from the seven-file
task/content/plan/summary set. `marketplace-verification.json` is the only
optional eighth file when required. Publication readiness and the Finalizer
gate remain ignored runtime and never enter the archive. Any other active-task
file fails the closed projection.

The plan records sorted `move_paths`, `tracked_move_paths`,
and `untracked_archive_outputs`. Before Draft creation it may contain exactly
one validated provenance metadata-tail whose parent is
`branch_review_commit`; the tail becomes `publication_head` without changing
the reviewed-content identity. The archive commit is a direct child of
`publication_head`.
`tracked_move_paths` require
both active deletion and archive addition. Untracked transaction outputs,
including `closeout-plan.json` and `finish-summary.json`, require only archive
additions because they never entered the Git index while the task was active.
A schema 2.0 plan already tracked by a migrated active task remains in the
tracked class and is bound through its predecessor digest.
The reviewed content tree plus exact pre-move index/status prove the tracking
classification. A month change while the task remains active rebuilds only the
still-untracked schema 3.0 plan and digest; it does not create a supersession
commit, reset history, rerun the verifier, replace the PR, or migrate an archive
directory. The only accepted non-current plan is schema 2.0 paired with a
Publication 4.0 DTO whose task/commit/title/protected facts and body hash match;
normalization uses the DTO body and never reads retired body/index files. Every
other non-current plan fails closed.
Until the exact archive commit exists, fresh execution and recovery require
this exact mixed no-renames set, active locator absence, the complete
prevalidated archived working-tree file set, exact dirty/staged paths, and
working-tree-to-Git blob continuity. Every tracked active blob in the source
tree must equal its archived working-tree and archive-commit blob
byte-for-byte, except `task.json`, whose only permitted change is the official
`status=completed` and `completedAt=YYYY-MM-DD` transition. A partial, missing,
extra, misclassified, or content-tampered pre-commit set is never valid.
The final summary is also a deterministic continuity input: fresh execution
and incomplete recovery rebuild its exact UTF-8 JSON bytes/digest from the
immutable template and the already-bound remote PR number/URL.

Once current `HEAD` is the exact planned archive commit, every archived
finish-work reentry reads the immutable plan from the current commit blob. The plan and
that commit's parent, path set, tree, and blobs are authoritative. Missing or
tampered archived working-tree files and their dirty status do not block
pushing that exact commit, remote/PR HEAD checks, or draft-to-ready. Fresh exact
recovery reads the committed `finish-summary.json` blob to recover the original
PR number/URL and verify the deterministic bytes/digest without calling the
general local summary validator; it never reads the archived working-tree
summary. A missing, closed, or replacement PR fails closed. If current `HEAD`
is absent from or mismatched with the planned archive transaction,
recovery falls back to the pre-commit metadata path and keeps all layout,
dirty/staged path, blob, official `task.json`, and lineage checks fail closed.
An archived directory containing only `closeout-plan.json` is resolvable only
by the canonical `guru-finish-work` recovery route; ordinary task resolution
still requires `task.json`. That plan-only
entry reads the plan from the current
commit blob rather than trusting working-tree bytes, then applies a dedicated
fail-closed workspace boundary before GitHub access or committed-archive
recovery. The boundary requires the actual Git toplevel, configured and remote
repository identity, current head branch, available base ref, current HEAD,
plan digest, active/archive locator relationship, task identity, and exact
archive transaction to match the immutable plan. It is not a context-free
bypass and is unavailable to every other command, which continues to require
`task.json` and a boundary derived from the current task, ignored runtime mapping,
and live Git worktree facts. No alternate task identity artifact participates
in ordinary or plan-only recovery.
Before ordinary resolution or canonicalization, the finish entry classifies
the raw locator as only a task basename, the exact former active locator, or
the exact archive locator. Path-like locators require lexical containment and
`lstat` from repo root through every ancestor and the final task directory.
Basename locators apply the same raw check, before ordinary resolution, to
`<repo>/<basename>`, `.trellis/tasks/<basename>`, the archive root, and archive
candidates in ordinary resolver order. Each direct or archive candidate first
retains only raw `symlink_component` evidence, then applies the ordinary
resolver's exact follow-symlink `directory + task.json` predicate. A matching
alias is rejected, while an unmatched alias continues to the next candidate.
These checks reject internal/external,
relative/absolute, ancestor/final, multilevel, dangling, and loop symlinks
before the ordinary resolver can discard raw alias evidence. The ordinary
resolver then runs so explicit `task.json`, active task, and normal archived
`task.json` precedence stays unchanged. Plan-only recovery runs
only when ordinary resolution returns not-found: an exact archive locator may
select that exact candidate, while basename/former-active fallback must find
exactly one matching archive month and fails closed on multiple matches. The
resolved plan-only target must still equal the plan's canonical archive
locator. The only outer re-anchor is the verified Darwin system `/var` ->
`/private/var` mapping; arbitrary `samefile` or user-created aliases are never
trusted.

Closeout failure injection must enter through production `cmd_finish_work()`.
Use a real temporary Git repository, bare remote, official `task.py archive`,
and a controllable fake GitHub store/verifier at external command boundaries.
Do not mock `prepare_closeout`, draft binding, final projection, archive
transaction, recovery, or ready transition. Every failed stage records
real active/archive locator and path state, task status, PR draft/state/number,
exact local/remote/PR HEAD SHA values, complete dirty/staged path sets, then
clear the failure and re-enter production `cmd_finish_work()`. The observed
retry must execute the failed transition without repeating an earlier mutating
transition or skipping ahead.
The negative matrix also covers a fork PR with the same branch, SHA, title, and
body. It must fail while the task is active and before final-summary binding;
archived recovery must reject the fork from remote repository facts without
opening or rebinding the already-archived summary.

Use the intake/task `base_branch` for diff ranges and PR base. Do not fall back
to the GitHub default branch when the task has an explicit base.

For PR body publishing, companion scripts may validate objective Markdown
structure, required sections, forbidden low-information phrases, non-empty
validation / impact / safety content, Docs SSOT section/key presence, and Issue
Scope Ledger close/ref semantics. They must not decide whether the release
explanation or Docs SSOT rationale is true or sufficient; that judgment belongs
to the AI readiness review before
`guru-finish-work`. Formal closeout accepts only the exact `pr_title` and
`pr_body` projected by the current Publication `ready` output and binds them
directly into schema 3.0 closeout-plan repo/base/head/payload/draft facts. No
file locator, generated source, or payload override participates. Publication's
semantic checkpoint remains ignored runtime; Finalizer consumes only its
checked `ready`
DTO and never commits or parses `pr-readiness.json`. Active-state retries consume
the untracked plan and live transaction facts; after the official archive move,
recovery reads only the committed immutable
plan and uses its exact title/body plus Git/remote facts. Command-line
title/body/draft/base overrides fail closed.
Final projection validates all task-relative artifact locators while the task
is active. The official archive move carries those files unchanged to the
planned archive locator; no gate, readiness, body, ledger, report, or summary
path is rewritten after archive. Archived recovery checks the exact planned
locator/file set and Git blob continuity without re-entering body, summary,
ledger, readiness, or marketplace artifact validators.

Planning and Phase 2 helpers follow the same recorder / validator boundary:

- `record-phase2-check` accepts one AI-authored closed input for new
  `guru-phase2-check-4.0` records, materializes `phase2_capture_commit` and the
  current reviewed-content identity, verifies that reviewed
  paths cover current dirty paths, writes one ignored-runtime owner checkpoint,
  and never infers scope, severity, adequacy, Docs SSOT consistency, semantic
  pass, or route intent;
- `check-phase2-check` validates the published closed schema, commit-anchor and
  reviewed-content freshness, current dirty-path coverage,
  finding/scope linkage, and the four exit/consumer combinations;
- reviewed paths are non-empty, while validation commands, unverified items,
  Docs SSOT, adequacy dimensions, scope decisions, findings and summaries remain
  the compact AI-authored semantic result rather than recorder-derived
  conclusions; the one local token is not authorization, semantic approval,
  public handoff, or whole-chain authority;
- the current command ids accept only the structured `--input` contract and
  reject every other CLI shape before invoking the recorder;
- command exit zero, coverage booleans, or official worker output are facts
  only and cannot create a passed AI Gate.
- Phase 2 candidate hygiene consults the official
  schema-v2 `.trellis/.template-hashes.json` provenance only to suppress Git
  diff-check or untracked-text whitespace/blank-EOF findings when the checked
  `HEAD`, index, or worktree projection has an exact same-path byte match. This
  includes tracked upstream-template migration deltas without allowing one
  exact projection to exempt a different staged or committed candidate.
  Unknown or locally edited paths, invalid/missing provenance, and hash mismatch
  receive no exemption; path escape, invalid UTF-8, and invalid JSON remain
  fail-closed deterministic errors.

- `record-contract-wording-review.sh` and
  `check-contract-wording-review.sh` are the generic deterministic recorder and
  checker for `guru-review-contract-wording`. They rebuild the fixed profile
  scope, rescan current bytes, derive local digests/unchecked facts, validate
  the published schema and Gate/exit/freshness invariants, and return one
  stdout-only owner result. They do not persist task-local
  `contract-wording-review.json` or choose rewrite, classification, reason,
  confirmation, semantic pass/block, or route intent. For
  `planning_artifacts`, they require the canonical planning-only dimension
  object and validate its exact shape/value; they never infer or generate those
  AI judgments. Other profiles reject the field.
  Stale results are discarded and the owner performs complete same-profile
  re-entry against current content. The runtime exposes no `--replace-stale`,
  supersession flag, or prior-result digest chain. For `change_request`
  selected comments it rejects missing author or update time. For a live issue
  revision it compares source/locator/field, objective preimage, exact proposed
  bytes, current reread bytes, and source update time with the rebuilt live
  scope. Authorization remains in the current dialogue and is never passed to,
  derived by, or validated by the script.
- `record-change-request-review.sh` and
  `check-change-request-review.sh` are the stdout-only recorder/checker for
  `guru-review-change-request`. The recorder accepts a complete AI-authored
  review and one exact change-request input; the checker accepts the recorded
  result plus the current full prerequisite payload set and same target input.
  Both reuse existing context/clarification/wording objective helpers, rebuild
  portable projections and linkage, validate schema/hash/ref/Gate/consumer/
  ready invariants, and return the AI-authored exit unchanged. They do not
  accept an output/task locator, create `issue-review.json`, generate findings
  or Gate status, choose a delivery unit, search history/duplicates, or map an
  objective error to a route. Missing or stale evidence remains input for the
  AI's next complete Skill round. For draft and standalone targets they reuse
  #113's exact draft `review_target` projection and canonical digest to derive
  the only valid `source_request_sha256`; 64-hex shape alone is insufficient.
  Production tests must invoke the actual context, clarification, wording, and
  change-request record/check commands before asserting `ready` or linkage
  drift, rather than supplying only handwritten projections to a structural
  helper.
- `record-planning-approval.sh` consumes one completed AI-reviewed
  `guru-approve-task-plan` result and writes only the compact ignored-runtime
  schema 3.0 checkpoint. It validates the authored field set, current task and
  planning locators, required non-empty files, authority refs, Docs SSOT shape,
  and semantic/exit/consumer union. It must not decide adequacy, provenance,
  proposal necessity, authorization sufficiency, Gate status, or route.
- `check-planning-approval.sh` validates the closed current schema 3.0, task/planning
  locators, required files, and four exit/consumer invariants before task
  activation, implementation dispatch, or Phase 2 evidence.
- `record-phase2-check.sh` records the prior AI-authored full-scope
  `guru-check-task` result, including unchanged official `trellis-check`
  evidence; it must not replace semantic judgment with worker output or command
  exit codes.
- `check-phase2-check.sh` validates closed schema 4.0, the nine adequacy
  dimensions, objective linkage, finding lifecycle, exit/consumer union,
  hashes, and stale state before commit. Routine assignment, handoff, liveness,
  raw worker payload, and review rounds are absent.
- `record-agent-recovery.sh` writes ignored
  `.trellis/.runtime/guru-team/agent-recovery/<task-key>.json` only after an
  agent explicitly returns unfinished and a replacement must inherit the work.
  It records one minimal `unfinished` event followed by one linked
  `replacement` event; routine dispatch/wait/progress/completion never invokes
  it.
- `check-agent-recovery.sh` validates that exceptional two-event chain and
  returns objective recovery facts. The checkpoint is owner-private runtime and
  never enters a task artifact, public DTO, commit, or archive.

Workspace boundary helpers are deterministic validators and fact snapshots:

- `check-workspace-boundary.sh --json --task <task-path>` reports
  `workspace_mode`, `expected_workspace`, `actual_repo_root`,
  `source_checkout`, `task_dir`, `task_dir_relative`, source checkout status,
  task worktree status, suspicious source artifacts, `status`, and `errors`.
- In `workspace_mode: worktree`, recorder/validator commands that write or
  validate task artifacts must validate current `task.json`, derive the
  machine-local task worktree from the current checkout,
  `.trellis/.runtime/guru-team/**`, and
  `git worktree list`, then confirm the actual repo root equals that derived
  worktree before touching owner-private ignored-runtime checkpoints such as
  `planning-approval.json`, `phase2-check.json`, and `review-gate.json`.
- Current task identity is resolved only from `task.json`, ignored runtime
  mapping, the current checkout, and live Git worktree facts. Missing or
  mismatched identity fails closed, and runtime must not fall back to a
  same-named task directory in the source checkout.
- Task artifact arguments such as `--checked-artifact` must resolve inside the
  current task directory under the selected task worktree. Absolute paths are
  allowed only when they stay under that task directory.
- Source checkout current-task artifacts, review metadata, or current-task dirty
  paths are fail-closed boundary facts. The script must not decide whether a
  sub-agent is stale, migrate a misplaced patch, or clean source checkout files;
  AI/human workflow owns those decisions.
- `--allow-source-clean` may be used only for a clean source checkout probe that
  reports facts without treating a clean source checkout mismatch as a blocker;
  it must not permit source checkout task artifacts or review metadata.

`resolve-human-artifacts.sh --json --task <task-path-or-name>` is a
deterministic resolver for user-facing Markdown task artifacts. It may resolve
the active task directory or archived task directory and report path/existence
facts for only `prd.md`, `design.md`, and `implement.md`. It must
not read planning/check/review gate JSON artifacts, must
not decide phase sufficiency, and must not create links for missing files.

`review-branch.sh` records only schema 3.0 after an independent AI semantic
review exists. It requires the six-field public input, one semantic review
payload, the selected typed exit, reviewer identity/source, and concise evidence.
It writes one compact owner-private `review-gate.json` checkpoint under ignored
runtime; no `review.md`, `reviews/*.md`, assignment ledger, report digest,
rollup, command argv, changed-file copy, or deployment projection is generated.

The recorder fails before writing when the public task/base/`branch_review_commit`
identity is stale, live commit validation fails, the working tree has undeclared
non-metadata drift, or semantic finding/exit invariants contradict. Open P0-P3 findings route to
`implementation_required`; unconfirmed scope routes to
`scope_confirmation_required`; passed requires zero open findings and one
`fresh_final_review` over the complete current range.
The new Branch Review path consumes the committed Task Commit DTO and validates
parent, committed paths, content continuity and the complete live Git range
directly. Commit message format is not downstream freshness authority. It never
opens the Planning or Phase 2 owner checkpoint. Any
undeclared current non-metadata dirty path blocks the gate; allowed downstream
workflow metadata is validated by its owning gate rather than projected back
into Phase 2.

For finding closure, schema 3.0 retains the original `introduced_head`, binds
the fixing commit as `fix_head`, binds the later transient judgment as
`closure_head`, and uses `review_commit` for the distinct fresh-final range.
The semantic normalizer and lifecycle validator both accept this normal
finding -> fix -> closure path. Non-3.0 gates and tracked assignment/report
files are invalid current inputs and fail closed without projection or re-entry.

Independent review agents do not run Guru Team recorder/validator extension
scripts as part of their review. They may inspect docs, code, tests, diffs, and
ordinary validation evidence, but `review-branch.sh`, `check-review-gate.sh`,
and `record-*` calls belong to the main session
after the review result exists. Those calls record and validate objective
artifact evidence; they are not review work.

`review-branch.sh` may record non-blocking `observations[]` and
`followup_candidates[]` in `review-gate.json`. They are not findings and do not
block by themselves, but the AI/human reviewer must not downgrade an actual
current-scope defect into either category to make the gate pass.

For Docs SSOT, reviewer judgment stays outside the script: `review-branch.sh`
may record evidence/finding strings supplied by the reviewer, but it must not
decide whether `ssot_first`, `delta_first`, `bootstrap_or_repair_docs`, or
`no_docs_update_needed` was semantically sufficient. The companion boundary is
objective evidence shape and stale/non-metadata drift validation only.

## Security Rules

Never print or persist tokens, private keys, signed URLs, `.env` contents,
database URLs, or sensitive raw records in logs, JSON artifacts, issues, PR
bodies, or README examples.

When writing temporary issue body files, use `tempfile.NamedTemporaryFile`
and unlink the file in a `finally` block. Existing example:

- `create_issue()`

## Validation

For any script change, run:

```bash
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
```

When changing `review-branch` or `finish-work`, also run dry-run
or representative script paths in a disposable worktree whenever practical.

### Extension Installation Verification Runtime

The stable runtime commands for `guru-verify-extension-installation` are
`execute-extension-verification`, `record-extension-verification`,
`check-extension-verification`, and `invoke-extension-verification`. Canonical
package wrappers and current closeout invoke those commands only through
`run-skill-command`.

`marketplace_verification_required()` returns changed-surface facts only and
does not decide applicability for the active Skill. Closeout uses those same
candidate-surface facts after rebuilding the reviewed path set from the pinned
task base through `branch_review_commit`.

The executor accepts an already AI-selected closed capability list and creates
three disjoint roots: `target-checkout`, `extension-source-checkout`, and
`install/project`. It resolves and verifies target ref/HEAD/reviewed content
first, reads installed source provenance only from the target checkout, then
requires clean task-bearing source provenance, resolves source direct/peeled facts,
and requires the selected source commit to
equal the manifest commit before source checkout. A full 40-hex source ref
initializes the isolated source checkout, configures the canonical locator as
`origin`, fetches exactly that OID through `origin`, and requires
`FETCH_HEAD^{commit}` to match the requested and manifest commits. Branch and
tag refs retain the `ls-remote` direct/peeled path. Taskless standalone fallback is
allowed only for an absent manifest and explicit source-repository intent.
Malformed provenance and unsafe non-canonical or credential-bearing source
locators fail before clone or artifact reflection.
Dirty task-bearing provenance fails before source ref resolution and cannot be
accepted as passed private evidence by the recorder or checker.

Installer, canonical workflow/runtime/schema/package bytes, ownership and
source sidecars are read only from `extension-source-checkout`; target
reviewed-content facts are read only from the target checkout/current task.
Recorded command ownership is the closed `target_checkout` or
`extension_source_checkout` label, and every asset expectation/digest,
ownership fact, and sidecar fact explicitly carries
`extension_source_checkout`.
The executor then runs the selected clean install,
preview/switch, preset, update/reapply, ownership, sidecar, discovery, platform,
README, and redaction probes. It records sanitized argv, exit code, output
digest/size, capability status, asset digests, current ownership inventory, and
sidecar facts. It neither chooses the capability set nor turns command success
into `verified`.

The recorder consumes the public input, deterministic execution facts, and an
already completed AI review containing applicability, profile coverage,
adequacy, findings, route, redaction, and optional supersession. It rebuilds
current identity and writes the sole task-local
`marketplace-verification.json`, or returns the same owner result without a
repository write for taskless standalone. The checker validates the closed
schema, task/session persistence, target repo/ref/HEAD/content, installed
manifest/source repo/ref/direct/peeled/checkout HEAD, and plan bindings,
machine/semantic/final digests, redaction, unique consumer, and current
supersession. It does not revisit semantic conclusions.

For workflow and task-bearing standalone invocations, execute, record, and
check each rebuild the exact direct active-task identity before continuing.
They require the current active-task pointer, reject archived/completed tasks,
match public `task_ref`/`repo_ref` to current `task.json` and repository facts,
match the live branch, and run the shared workspace-boundary validator using
the current task, ignored runtime mapping, and live Git worktree inventory.
Wrong-task, missing-identity, and wrong-worktree invocations fail before command
execution, artifact mutation, or DTO projection. Session-only standalone mode
bypasses only the task-specific checks and remains repository-write-free.

The public invocation reruns the checker, reads the actual exit only from the
checked owner result, selects that exit's schema, and emits one minimal DTO.
`expected_exit` is eval-only. Workflow `not_required` is rejected; when a
plan-required target conflicts with AI `applicability=not_required`, private
evidence records the conflict and returns `blocked` without fabricating an
execution profile. A taskless installation failure also returns a standalone
`blocked` report rather than a false task-work route.

The ownership fact reader consumes only current schema 3.0: exactly 11 Guru
rules, nine managed claims, and three additive overlays. Non-current schema,
additional fields, unknown claims, or unexpected overlays fail verification.
Raw command output, credential URLs, tokens, and temporary repository locators
are never retained; only safe locators and digest/size facts cross the runtime
boundary.
HTTP(S) URL scanning treats authority userinfo as sensitive across
username-only, username/password, percent-encoded, empty, and multiple-`@`
forms. Whitespace and `/` terminate the authority candidate. Recorder errors,
public wrapper output, and eval traces expose only generic failure text or
digests and never the rejected credential URL.

## Skill Eval Discovery And Runner

`discover-skill-evals.sh` and `run-skill-evals.sh` are thin wrappers for the
deterministic `discover-skill-evals` and `run-skill-evals` subcommands.
Discovery validates source/installed registry and Interface 1.3 state before it
loads the fixed package-local corpus, then validates corpus identity, profile
and exit references, fixtures, assertions, adapter inventory, and exact public
invocation. A package without a declared current corpus returns a stable
unsupported error rather than a fabricated empty corpus.

The runner requires an absolute `--run-root` outside the repository/package,
executes each selected case through the public wrapper, captures one DTO,
records the actual exit, validates its per-exit output schema, applies only the
closed deterministic assertion grammar, and mechanically binds external
semantic grading and separate human feedback to each comparison side. It never imports or reads
`guru_team_trellis.py` to construct Skill input or interpret output, never
generates semantic pass, and never turns static corpus shape into behavior
success. Exact comparison package paths must be supplied as a pair; floating
version/ref resolution belongs to the caller. The runner resolves one exact
public runtime target from its selected source/installed extension context
before iterating either comparison side and writes it only to the private
adapter request. Current and repo-external comparison packages use the same
target; adapters never derive runtime location from a compared package path.

The shared/Codex/Claude/Cursor adapter descriptors use one request/response
protocol. Native argv assembly is adapter-local; corpus/schema/grader/status
policy stays in the shared runtime. Missing CLI/capability is `unsupported`,
launch or malformed-output failure is `execution_error`, and behavior or
grading mismatch is `evaluation_failed`. Expected non-success typed exits are
ordinary passing behavior when their declared contract succeeds.

Each closed descriptor names one executable wrapper and one native command.
`run-skill-evals` resolves the wrapper below the selected source/installed
`adapters/eval/` root, requires a regular executable file, and invokes it with
the closed request. It never selects an adapter through an undocumented
environment variable. The shared adapter resolves its preset-managed
`guru-team-shared-eval` executable beside the adapter; Codex, Claude, and Cursor
resolve their native commands from `PATH`. Shared uses the documented
request/context/workdir argv, while the other three assemble their native
non-interactive argv. Every wrapper materializes a repo-external public-only
projection with exact `SKILL.md`, Interface, public wrapper, and invocation
schemas/examples plus a separate case workdir. Canonical package/corpus and
private runtime locators stay outside native execution. The wrapper records
case prompt and staged files,
then records native argv, stdout/stderr, context, output, and trace in the
transcript locator. Discovery reports deterministic `native_available` facts;
absence remains `unsupported` without creating run output inside the repo.
The context gives the native CLI a repo-external trace helper and exact
read/invoke commands instead of inlining `SKILL.md`. The helper receipt is
validated against `guru-team-skill-eval-native-trace-1.0`, the minimal native
request digest, projection root, exact Skill/wrapper bytes, public wrapper
path/argv/return code, and returned DTO bytes.
Missing, incomplete, unbound, or output-mismatched receipts are
`execution_error`. A projection containing `evals/` or private runtime also
fails closed. Trace invariants are never inferred from wrapper source text or
the mere presence of a parseable native DTO.

Production semantic case staging supplies explicit public-wrapper arguments
whose owner-result locators resolve inside the current repository. The private
runtime boundary maps the repo-external public projection wrapper to the
corresponding installed, validator-audited package before dispatch, reruns the
owner checker, and returns the actual exit. Adapter and native requests omit
`expected_exit`; only the runner reads it after wrapper completion. Codex runs
from the installed runtime's trusted Git root, Claude uses safe non-interactive
input, and missing Cursor authentication returns deterministic `unsupported`.

## Branch Review Recorder And Checker

`review-branch` records only an already completed AI semantic review. It may
rebuild task/worktree/base/HEAD/range, planning, Phase 2, issue-ledger,
commit-evidence, Docs SSOT, working-tree, hash, schema and freshness facts, then
write compact schema 3.0 `review-gate.json` under owner-private ignored runtime.
It must not decide
scope, scenario class, qualification, severity, reviewer sufficiency, route, or
pass.

`check-review-gate` revalidates the same objective facts, finding lifecycle,
`introduced_head`/`fix_head`/`closure_head`, final-review freshness and the selected
typed exit. Only schema 3.0 is accepted; other gate shapes fail closed without
projection. The public package wrapper accepts a closed public input
and repo-local owner-result locator, reruns the checker, reads the actual exit,
and emits exactly one declared DTO. `expected_exit` is never a wrapper input,
owner-result field, or route selector.

## Task Publication Recorder, Checker, And Invocation

Stable commands are `record-task-publication-review` and
`check-task-publication-review`. The recorder accepts only a caller-authored,
already completed semantic review payload, rebuilds the eight objective entry
preconditions transiently, and writes the single ignored-runtime schema 4.0
`pr-readiness.json`. That checkpoint contains only task/content identity, the
closed exact `pr_payload(title,body)`, all
ten semantic dimensions, findings, conclusions, and the selected route. The
checker rereads the same live facts and the shared Finalizer preflight; neither
command stores deterministic bindings, publication refs, supersession chains,
reviewer process, or confirmation evidence.

The Publication AI authors and reviews the exact title/body before invoking the
recorder. Deterministic payload validators are reused inside the active owner's
recorder/checker after semantic review; calling a recorder to fabricate missing
content, infer semantic sufficiency, or synthesize a pass remains forbidden.

Stale re-entry carries only `task_ref`, the Finalizer-projected
`branch_review_commit`, and the current `stale_reason`; the recorder replaces
its own current checkpoint after a delta-scoped semantic rereview. The wrapper
requires the checked owner result to retain that same commit anchor. Normal
continuity drift is valid only with an AI-selected `return_to_task_work` after
the branch review commit is proven to be an ancestor of current HEAD and its descendant
diff is successfully inspected. Invalid or non-ancestor identities and
inspection failure remain fail closed on every exit. No
supersession identity or re-entry narrative enters public input, private
checkpoint, or output.

Neither command decides review dimension status, issue disposition, PR body or
Docs sufficiency, safety/deployment conclusions, finding route, metadata edit,
human-confirmation need, or `ready`. Empty findings, scanner success, changed
file classification, a `--pass` flag, or tests passing cannot synthesize a
semantic conclusion.

Both commands validate the already AI-authored closed union without selecting
it: `ready` binds passed conclusions/dimensions and closed findings;
`return_to_task_work` binds open `task_work` findings to `finding` dimensions
without blocked evidence; `blocked` binds open `external_blocker` findings to
`blocked` dimensions and at least one blocked conclusion. Every open finding
references a non-passed dimension, and open metadata-revision findings cannot
leave the internal rereview loop.

The package `scripts/invoke.sh` remains the exact dispatcher-only wrapper. The
shared public invocation validates one of the two target-owned inputs, reruns
the owner checker against a repo-local result, selects the output schema from
the checker's actual `exit_id`, and emits one minimal DTO. `expected_exit` is
available only to the eval grader after wrapper completion.

`ready` emits exactly `exit_id`, `task_ref`, `branch_review_commit`, `pr_title`,
and `pr_body` after the
same side-effect-free closeout preflight used by Finalizer. Finalizer consumes
that DTO and live facts directly; projection preserves exact body bytes and
Finalizer never reads or augments Publication's
checkpoint. Inputs outside the current Publication schemas fail closed before
owner invocation.

## Task Finalization Recorder, Checker, Executor, And Invocation

Stable commands are `preview-finalization`, `record-finalization-gate`,
`check-finalization-gate`, `execute-finalization-transition`, and the package
`scripts/invoke.sh`. The recorder and executor may validate a pending transition
route; public invocation always reruns strict route validation and never calls
the transition executor implicitly.

Current Finalizer uses `guru-finalization-transaction-1.0` only when a
same-owner deterministic transition must survive re-entry. Preview and execute
rebuild live Git/GitHub/Trellis facts, locate the transaction by exact
`task_ref`, and bind immutable publication input plus the local `plan_digest`
consumer token. Verification-required writes the transaction before returning;
terminal `ready_for_merge` retires Finalizer and Verifier owner state. Current
archive preparation allows six core files and the minimal verification result
as the only optional seventh file. Archive-move failure restores the task
locator's tracked bytes from immutable `publication_head`; archived recovery
reads committed task/summary facts and ignores damaged working-tree copies.

### Legacy Plan Engine Selectors

The remainder of this section preserves the explicit pre-#180 plan engine and
#191 recovery selectors. It is not current Interface, registry, manifest,
preparation, recovery, or archive authority.

The legacy extension-verification checker validates the dedicated
`marketplace-verification.json` owner artifact against the immutable plan,
task, repository, remote ref, `branch_review_commit`, reviewed-content identity,
and exact transaction paths. Closeout schema 3.0 creates no pre-draft commit and
rejects every additional dirty path or identity/commit drift.

The verifier treats `branch_review_commit` as `reviewed_content_head` and
`publication_head` as the exact target/ref checkout identity. Current producers
always emit both fields. Legacy closed schemas remain byte-stable historical
contracts, but a legacy payload without `publication_head` fails current-schema
validation and must be regenerated by the owning current producer; the verifier
never defaults or derives the missing identity. A validated single manifest-only
provenance tail preserves reviewed-content identity while moving the
remote/PR/archive parent to `publication_head`.

When the current closeout plan requires extension verification, finalization
consumes only a checker-passed current `guru-verify-extension-installation`
owner result and its task-local artifact. The artifact is passed unchanged
through preview, retry, final archive projection, active projection validation,
normal archive execution, and archive recovery. It never rewrites the owner
result, creates a second artifact, enters a public DTO, or augments the Ledger.
A missing, stale, consumer-mismatched, or otherwise invalid owner result stops
before archive mutation. Plans that do not require verification carry no
verification artifact.

Closeout plan preparation owns one deterministic reviewed-change projection.
It derives `review.changed_paths` from the live merge base of the task's current
`base_branch` through immutable `branch_review_commit`, derives
`review.close_issues_reviewed` from the publication-validated Issue Scope
Ledger, and feeds the same reviewed paths to marketplace candidate-surface
classification, archive retention, and the finish-summary template. Compact Branch Review remains semantic and
small; the finalizer does not require it to duplicate path or issue-scope
inventories.

`verification_required.repo_ref` must equal the immutable plan repository.
Its current DTO also carries both reviewed and publication HEADs. The
pre-PR `reprepare_required` executor uses the canonical preset apply entry in a
detached clean worktree, validates the five-field manifest allowlist, commits
one tail, fast-forwards the task branch, and removes only the superseded private
plan/gate/request state. Its private gate retains an executor marker; only after
the tail is committed does the executor return the public task/reason plus
`branch_review_commit/publication_head` DTO. A pre-#191 base-evolution candidate
must first prove its exact legacy gate/request, matching task/repository/remote/
base/head identities, active/no-PR/no-archive/single-consumer state, untracked
artifacts, old-to-current ancestry, and a fast-forwardable remote ancestor.
Preview and discovery only prove those facts. The checked transition repeats the
proof, retires the predecessor, and persists only the freshly rebuilt ignored
Finalizer transaction; the next preview rebuilds the plan from its exact
publication payload and validates both heads.
For an unused current schema 3.0 predecessor, the runtime instead validates the
complete seven-field Git shape, the historical tail structure and ancestry, a
remote branch at or before the predecessor reviewed-content head, untracked
owner state, and the absence of PR/archive/verification/request/gate consumers.
A remote at the predecessor publication tail or any later descendant proves an
outbound publication side effect and fails closed. Initial preview rejects every
preexisting gate. Recorder then writes the ordinary Finalizer gate; checker and
executor pass only that exact checked in-memory gate back into the repeated
preflight. The executor retires the old plan/gate, creates or reuses the current
tail, uses the real `prepare_closeout()` path to rebuild the candidate, and
records only its minimal `finalization-transaction.json` recovery projection.
The initial `publication_ready` invocation supplies the current reviewed exact
title/body to the base-evolution candidate even when they differ from the
predecessor plan. Only after the executor records that transaction does a
minimal `reprepare_preview` reuse its immutable exact publication payload;
public `reprepare_required`
remains task/reason/two-head identity only.
For the pre-#191 base-evolution route, recorder does not overwrite the legacy
gate whose bytes the checker and executor must still validate. It writes the
current marker to the same-owner ignored
`task-finalization-transition-gate.json`; default gate resolution selects it
only while the exact legacy gate and base-evolution state remain current.
Successful checked supersession removes both gate files, while an orphan or a
transition gate outside that state fails closed.
`resume_finalization` accepts only declared same-plan post-content recovery
states; `prepared`, reprepare/stale state, and terminal `ready` are invalid. The
ignored owner-private gate stores the private executor marker for publication
and provenance reprepare, while archive-month reprepare retains its complete
current DTO because HEAD does not change. After the archive transaction and
ready PR are objectively complete, public invocation
materializes the DTO in memory with the exact archive locator and canonical PR
identity; it never rewrites the gate with that public DTO.
