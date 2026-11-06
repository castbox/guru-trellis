# `guru-discover-change-context` Contract

All live GitHub reads use the shared authenticated, repo-bound `gh` adapter
defined by `.trellis/spec/workflow/workflow-contract.md`; adapter errors are
facts and never replace this Skill's semantic review.

## Installed Execution Locations

Keep cwd at the reviewed repository root and set the existing package location:

```bash
GURU_SKILL_PACKAGE=.trellis/guru-team/skills/packages/guru-discover-change-context
```

Package-relative `scripts/`, `schemas/`, and `examples/` paths in this contract
are below `GURU_SKILL_PACKAGE`. Cross-package `consumers/` paths are below
`.trellis/guru-team/skills/`. Agent discovery directories contain a thin
`invoke.sh`, not every recorder or example. A missing discovery copy does not
require a new helper, direct module import, or system-Python dependency install.

The public input example is
`.trellis/guru-team/skills/packages/guru-discover-change-context/examples/public-pre-task-input-3.0.json`.
The complete result example is
`.trellis/guru-team/skills/packages/guru-discover-change-context/examples/change-context-owner-result-3.0.json`;
It is a complete result example. Only the recorder-owned fields explicitly
listed below may be omitted; the remaining required source facts and semantic
fields still come from the caller's current read and review.

## Ownership And Modes

The global workflow owns mandatory invocation and exit consumers. This package
declares `judgment_mode=semantic` and owns:

```text
forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit
```

Workflow and standalone modes use byte-identical precondition ids and freshness
meaning. Both require a validator-passed fresh base before any live issue,
repository, or history semantic read. `change_input` is a closed set of ten
clue arrays and at least one array must be non-empty.

## Current Executing Owner

The current executing AI is this Skill's semantic owner in both workflow and
standalone modes. `owner_not_yet_executed` means continue the current review;
it is not a typed exit and does not require an external owner, agent ID,
subagent evidence, or pre-existing owner result. The restriction on runtime
semantic judgment does not restrict the current AI from authoring that judgment.

Read the complete contract and validate the real Sync public transition before
reviewing current authority, Docs/code/tests, duplicates, and history in the
declared order. You select history evidence and author the reviewed scope,
findings, sufficiency, Gate, and route; preview and runtime results supply facts,
not semantic conclusions. Then run record-context-discovery.sh,
check-context-discovery.sh, and invoke.sh with the existing envelopes.

Keep this owner's authoring and recorded result in call-local memory for its
own record/check/invoke sequence. Pass only actual public invoke stdout through
the declared thin projection to the next consumer; never read or reconstruct
producer-private results. This responsibility does not waive missing authority,
freshness, schema, prerequisite, or unresolved-choice checks: use the existing
declared blocker or re-entry route when a real gap remains. Do not bypass the
workspace gate or ask for a corrective Prompt merely because your review has
not run yet.

## Fixed Git Tree And Draft Candidate

Accept actual `baseline_ready` stdout through the declared thin projection.
The current pre-task input is 4.0; context-request is 2.0. Their optional
`candidate_file` intentionally identifies a draft body file. For a file-backed
draft, supply it so the runtime rereads its bytes and binds
`live_change.body_sha256`. The recorder emits a separate candidate locator/body
identity; downstream Wording and Readiness reread it. Ordinary changes require
fresh affected review. This does not commit, publish, or turn the draft into
baseline authority.

For `base.kind=git_object`, `repository` uses `repo`,
`source_kind=git_object`, `selected_ref`, and `commit`. Recorder derives the
owner-private 4.0 observation without checkout branch or cleanliness fields.
Read each current source file through `scripts/read-change-context-source.sh
--source-transition <base_current JSON> --path <path>`; its receipt contains
`commit`, `path`, `blob`, and exact UTF-8 `content`. The same command reads
selected archive bodies. History preview receives `--source-transition` and
enumerates only the adopted tree's archive index. Record/check validate current
Docs/code/tests identities against that tree. Neither dirty checkout bytes nor
a later ref advance can replace the selected objects.

The original `synced` source keeps its distinct eight-field provenance and
live checkout validation. It is not reconstructed from a Git-object source.
Clarify's needs_context return carries the original fixed base and candidate
file into Discovery's current context-request input. A source refresh explicitly
returns to `operation=read` with the adopted commit; choosing a newer baseline
requires the caller's new source selection.

## Forward Behavior

Before the current-state, duplicate, and history searches below, read
`.trellis/spec/workflow/semantic-retrieval.md`, derive the minimal applicable
concept family, and judge combined evidence coverage. This owner does not
persist that query family or add it to public output. Any negative existence
conclusion must satisfy the shared contract.

Execute in this exact order:

1. validate fresh base evidence;
2. read the live issue or form a side-effect-free proposed draft;
3. search open duplicate candidates once and retain returned facts/reasons;
4. AI-review updated-base durable Docs SSOT;
5. AI-review code, API, config, schema and ownership;
6. AI-review tests, fixtures, throwaway and update coverage;
7. record current-state observations and canonical query clues;
8. run `history_previewer` exactly once;
9. AI-select one to three candidates when any exist, record every exclusion,
   and deep-read only explicit selected evidence; use an empty selection when
   the preview has no candidates;
10. run the AI Review Gate;
11. record and objectively validate the result, then return one typed exit.

Current-state review must finish before history preview. Duplicate reuse or new
target selection is handed to `guru-clarify-requirements`.

The `docs`, `code_contracts`, and `tests` arrays contain the same `evidenceRow`
shape. They record evidence for the reviewed area; their names do not require
an existing file of that type. When the scoped search finds no business tests,
the required `tests` row can reference an actual reviewed source or requirement
file that establishes the current behavior or requested validation. Use that
file's actual path and content identity. State the observed coverage gap and
whether execution is missing or unknown in `observation`; keep the real search
clues. For example, a reviewed request can establish that focused tests are
required while the current business-file search found none. That is evidence
about the validation scope, not evidence that tests exist, ran, or passed.
Do not invent a test file, create one during pre-task review, leave the required
array empty, or turn a missing test suite into an automatic intake blocker.
The AI still judges whether the actual evidence is sufficient for this step.

After a draft becomes an Issue, or base/source facts change, first validate the
fresh Sync transition and reread the formal identity and complete live body.
Then compare previously read Docs/code/tests with their actual revisions, the
base delta and this target. Where complete evidence remains available and its
conditions still apply, adopt those investigation facts without repeating an
unchanged broad search. Reread changed or unavailable bodies and affected
unchanged consumers. Perform this target's duplicate search, history preview,
evidence-coverage judgment and AI Gate in their original order. An old target's
pass or private producer result is not reusable current authority. Missing
historical installation/chat records stay unknown. Pass only the new checked
public result to Clarify, which owns intent, source roles and disposition.

For an issue, author `live_change.identity` as the canonical issue URL from
the captured GitHub source response's `url`. This is the origin of
the normal Issue chain's `handoff_target_locator` and `transition.target_locator`.
A short `#N` is a search clue or display label, not this chain's target binding.
Consumers copy the actual invoke stdout's target identity, transition and
`duplicate_snapshot` unchanged; examples do not replace producer output.

Each duplicate candidate fact projection is exactly `repo`, `number`,
`identity=#<number>`, canonical issue `url`, `state=open`, and `updated_at`.
`facts_sha256` is recomputed from those returned fields and excludes the
AI-authored reason/observation. Recorder/checker validate that same projection;
they do not issue a second duplicate search or re-read candidates after review.

`context_ready` schema 5.0 projects one minimal immutable
`duplicate_snapshot` for `standard_intake` and `reviewed_plan_intake` to the sole
Clarification consumer. Active-task and standalone returns omit this snapshot
and retain their original caller identity and resume consumer. The snapshot binds the query,
checked time, target locator, authority body digest, canonical open-candidate
facts and their aggregate digest. This replaces the former 3.0 handoff for the
current graph; missing or mismatched projections require context refresh.

## History Preview And Deep Read

History uses `guru-context-history-score-1.0`. The runtime enumerates only
`.trellis/tasks/archive/**/finish-summary.json`, applies lexical repository and
archive boundaries, reads only regular summary files, and projects only
`index`. It never consumes index siblings, `.trellis/workspace/**`,
`.trellis/.runtime/**`, a repo-level index/cache, or
`finish-summary-index.json`.

Canonical query, scoring weights, token cap, path-sorted valid/invalid manifest,
sort order, positive-score limit 20, projection, `query_sha256`,
`archive_manifest_sha256`, and `preview_sha256` are deterministic. Malformed
JSON, missing index, invalid index shape, and ordinary unreadable/non-file
summaries are isolated as portable invalid rows. Zero candidates is success
with empty selected/excluded/deep-read evidence and the exact `not_needed` mem
shape; it cannot trigger `trellis mem` or another history source.

AI deep-read uses one to three selected candidates and records a source-specific
portable locator, purpose, and conclusion. `task_artifact` locators are
repo-relative files inside the selected archived task; `github` locators are
canonical issue/PR URLs without query or fragment; `git` locators are exact
`git:object:<oid>` or `git:ref:<full-ref>@<oid>` identities verified live.
`trellis mem` is permitted only after task artifacts, current Docs/code/tests,
GitHub, and Git history are each recorded insufficient for one named
load-bearing question. Otherwise record `mem_review.status=not_needed`.

## AI Review Gate And Conditional Confirmation

The AI Gate records reviewed/excluded scope, relevance, sufficiency, conflicts,
reusable/non-reusable mechanisms, evidence-bound load-bearing conclusions,
findings with severity/status, and `passed` or `blocked`. Runtime scripts only
validate this evidence; they never generate it or choose the semantic exit. A
passed Gate requires non-empty reviewed scope and load-bearing conclusions.

`typed_exit=blocked` if and only if `ai_review_gate.status=blocked`; schema and
runtime enforce both directions. This step has no user-owned decision or
mutation, so the conditional confirmation stage continues without prompting
and writes no authorization field to owner state.

## Owner Result, Freshness, And Exits

Workflow and standalone recording are stdout-only. The recorder and checker
accept one closed invocation envelope from stdin or an explicit envelope file,
validate it, and never create a task, workspace, or ignored runtime file. Each
command reads the envelope exactly once. The public wrapper accepts the same
envelope and emits one typed DTO only after the recorded owner result passes
the objective checker. The input transport is not a semantic approval.

An active-task workflow owner passes the direct task identity independently as
`--active-task`, for source-selection recovery and context review by the
current Task/Delivery owner without a Task development-status prerequisite.
Record, check, and public invoke then bind the live checkout to
the task's TaskId/lifecycle generation, its Git common-dir branch binding,
registered checkout, and fresh selected-base refs while
allowing ordinary in-progress worktree edits; this normal mapped route remains
repository-write-free. Only a real interruption adds
`--recovery-continuation-id`, which writes one
`change-context-recovery.json` below that task's ignored owner-checkpoint
namespace. It retains only task identity, requested exit, Gate status,
reviewed scope, load-bearing conclusions, and reason. The checker binds those
bytes to a complete fresh owner rerun. Stale/invalid recovery is deleted, and
the public wrapper deletes a current checkpoint only after its typed DTO passes
the output schema. The public `return_identity` of an active-task context
request binds the same live TaskId and lifecycle generation independently of
the optional `--active-task` owner-recovery argument. Other profiles cannot
select active-task or recovery invocation identity.

The recorder and checker execute the published closed Draft 2020-12 schema and
validate query/manifest/preview/payload/result digests. Matching live stale
facts return the caller-authored `refresh_base` exit for complete re-entry from
live authority. The commands do not reconstruct or persist a prior-result
chain.

The caller supplies the Sync public `base_current` transition separately from
Discovery public input. Before reading issue, Docs, code, test, or history
content, the executing Discovery AI checks the transition's actual source variant.
For `base.kind=git_object`, use the adopted commit and the public source reader
in Fixed Git Tree And Draft Candidate above; checkout branch and cleanliness
are not its authority. For the original synchronized variant, check the
current public Git facts in the authority checkout named by
`transition.repo_locator`; an active Task's working checkout can be different. Set
`discovery_authority_checkout`, `discovery_base_branch`, and `discovery_remote`
from that actual transition's `repo_locator`, `base.selected_base`, and
`base.remote`. The existing read-only Git commands are sufficient:

```sh
git -C "$discovery_authority_checkout" rev-parse --show-toplevel
git -C "$discovery_authority_checkout" remote get-url "$discovery_remote"
git -C "$discovery_authority_checkout" symbolic-ref --short HEAD
git -C "$discovery_authority_checkout" rev-parse --verify HEAD
git -C "$discovery_authority_checkout" rev-parse --verify "refs/heads/$discovery_base_branch"
git -C "$discovery_authority_checkout" rev-parse --verify "refs/remotes/$discovery_remote/$discovery_base_branch"
git -C "$discovery_authority_checkout" status --porcelain=v1
git -C "$discovery_authority_checkout" worktree list --porcelain
```

Check the exact repository root and GitHub repository identity, selected branch,
three HEAD/ref values, clean base authority, and its unique registered worktree
against the Sync transition. The three values must equal `base.decision_head`,
`base.local_base_head`, and `base.remote_base_head`. Use the existing Sync
repository-identity contract for supported remote URL forms. A normal HEAD
advance returns to original Sync for fresh `base_current`; wrong, dirty,
missing, mismatched, or ambiguous authority retains the original blocked route.
These commands do not fetch, check out, reset, stash, or write a ref. Ordinary
active-Task edits retain the separate `--active-task` contract above.

After the semantic reads and AI Gate, the original recorder and checker run
their read-only observer again for the selected source variant. Record derives
`base_observation` from those current facts. The observer is part of record/check,
not a separate public command or an earlier semantic result that the caller
must obtain. Do not call record with a placeholder Gate to perform the first
check. Neither public input nor owner authoring reconstructs Sync private
fields or `base_observation`.

Before `context_ready`, validation also binds the live issue or draft, reviewed
Git blobs/content, canonical query, archive manifest and owner result. A base error
short-circuits before those later reads. A source issue may be live `open` or
`closed`. A separately bound draft/Issue remains open-only and its live body
digest must equal the original reviewed draft body digest when claiming that
same-content binding. `guru-create-issue:created` does not use this draft
binding: after Sync it enters fresh Intake as a live `issue`, with
`issue_binding=null` and a digest of the complete live body including the
creation-attempt marker. The original draft is not carried across Sync as
source authority. An ordinary Issue edit is reviewed against that fresh live
Issue, not a stale draft binding. Every 40-character
reviewed Git identity resolves from the selected Git tree to exactly a `blob` (the synchronized
profile uses `HEAD:<path>`);
64-character content evidence is checked by exact byte digest.

- `context_ready` -> Skill `guru-clarify-requirements`;
- `refresh_base` -> `guru-sync-base`;
- `blocked` -> `change-context-blocked`.

Unknown, multiple, or unmapped exits fail closed. The package requires the
complete compatible Guru Team preset and `run-skill-command`; it is not
self-contained or portable.

## Interface 1.8 Public Handoff

The public profiles are `pre_task` (schema 4.0) and `context_request` (schema
2.0). After the owner loop,
`scripts/invoke.sh --invocation -` validates the closed call-local public input,
`base_current` transition, current live base observation, and checker-passed
owner result, then derives the matching per-exit DTO without another duplicate
search. Recorder and checker receive that same envelope via `--invocation -`;
they do not accept a private Sync artifact.
`context_ready` schema 5.0 contains route/profile/mode/target/continuation
identity and the original `return_identity`. Standard and reviewed Intake also
receive the minimal checker-bound `duplicate_snapshot`; Clarification consumes
it without repeating duplicate search or candidate reads. Active and standalone
returns preserve their original task or caller identity and resume consumer.
No return receives an owner-result locator. A
genuinely interrupted owner additionally supplies one recovery continuation and
may lazily use one minimal ignored checkpoint, which the same owner deletes on
stale restart or successful consumption.

## Issue #384 Invocation Migration

This is a direct command-input replacement. The recorder/checker flags
`--input`, `--public-input`, and `--transition`, and recorder `--mode`, are
removed. Existing scripts must migrate together with this package; old argv
returns `invalid_arguments`, not an implicit compatibility path. At that
migration, public input 2.0 and owner result 3.0 were retained. Public input and
handoffs now follow the current Interface 1.8 contract above; owner result 3.0
and the command envelope remain current. Previously incomplete invoke envelopes must also add the declared
`schema_version` and `owner_context` fields.

All three commands use the existing shared closed schema
`consumers/workflow/stage0/invocations/semantic-owner.schema.json`:

```json
{
  "schema_version": "1.0",
  "public_input": {},
  "transition": {},
  "owner_context": {},
  "owner_result": {}
}
```

The empty public/transition/owner objects above illustrate only the envelope
shape, not a runnable valid call. Populate them with the current Discovery
`pre_task` 3.0 or `context_request` 1.0 public input, the independent Sync
`base_current` transition, and the
AI authoring fields described below. Record completes owner result 3.0;
check and invoke consume that complete result. Discovery has no additional owner-context fields,
so supply `{}` for `owner_context`. `public_input.mode` is the sole mode input.
The shared envelope schema closes the outer shape; the existing Discovery
validators still own the nested semantic evidence and freshness contracts.

Use these dispatcher entrypoints, supplying one complete JSON object on stdin
to each command:

```bash
"$GURU_SKILL_PACKAGE/scripts/record-context-discovery.sh" --root . --invocation -
"$GURU_SKILL_PACKAGE/scripts/check-context-discovery.sh" --root . --invocation -
"$GURU_SKILL_PACKAGE/scripts/invoke.sh" --root . --invocation -
```

Before recording, the AI authors the semantic scope, observed source and
duplicate facts, current Docs/code/test rows, history selection, mem disposition,
and Review Gate. Record derives `mode` and `change_input` from `public_input`,
then derives `base_observation`, `canonical_query`, `history_preview`, and
`result_identity`. Omit those derived fields from normal record authoring;
when a non-default preview limit was used, supply only
`history_preview={"limit":N}` so record uses that same limit. Do not import
`canonical_query`, `preview`, or identity helpers from package/eval runtime.

`live_change.body_sha256` and `live_change.facts_sha256` are source evidence,
not recorder-owned fields. Supply the SHA-256 of the exact UTF-8 body and the
digest of the captured source facts; do not copy the example's placeholder
values or omit these fields. For an issue, the existing fact projection is
`repo`, `number`, `url`, lowercase `state`, `updated_at`, and `body_sha256`,
encoded as sorted compact UTF-8 JSON with a trailing newline before hashing.
Use ordinary JSON/SHA-256 APIs on the facts already read, not a private runtime
helper or another live request. An issue has `issue_binding=null`; a draft
retains the complete source shape required by the referenced schema.

For a new local text-only draft with no external Issue binding, the caller can
capture its complete UTF-8 body as the source evidence. In that supported
capture, `body_sha256` and `facts_sha256` both hash those exact body bytes;
`identity=draft:<body_sha256>` is one valid new local identity, `state=draft`,
`updated_at` is the actual capture time, and `issue_binding=null`. Preserve any
identity already returned by a producer. This example does not impose a unique
draft-facts projection or replace other supported capture representations.
An existing bound draft retains its actual Issue binding and corresponding
source facts.

The following standard-library example reads an existing local draft body and
writes only its source-evidence fragment to stdout. Replace `docs/request.md`
with the actual source file. The fragment is not a complete owner result or a
passed Gate; finish the original semantic review and author the remaining
fields yourself. Keep the same captured body in this call-local review.

```sh
python3 - docs/request.md <<'PY'
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

body = Path(sys.argv[1]).read_bytes()
body.decode('utf-8')
body_sha256 = hashlib.sha256(body).hexdigest()
print(json.dumps({
    'kind': 'draft', 'identity': 'draft:' + body_sha256, 'state': 'draft',
    'updated_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
    'body_sha256': body_sha256, 'facts_sha256': body_sha256,
    'issue_binding': None,
}, ensure_ascii=False, indent=2))
PY
```

Capture complete preview stdout in caller memory and inspect its `result` candidate
projection before choosing history. A shortened tool display is not a new
preview or proof of absence; it does not require rebuilding private preview
bytes. Record rebuilds the deterministic preview itself from the current clues.
Check and invoke consume the complete recorder result unchanged, not the
pre-record authoring subset.

The caller retains the envelope in memory, captures record receipt `result` and replaces
only its `owner_result`, then sends that envelope independently to check and
invoke. Check receipt `result` is a validation result, not a replacement owner result.
Do not concatenate JSON documents or pipe record receipt `result` directly into check.
No public/transition/owner input files, shell descriptor tricks, input caches,
or repository checkpoints are needed. `--invocation <file>` remains an
explicit file transport for that same envelope and loader, not the former
three-file interface; literal inline JSON argv is not supported.

`--expected-result-sha256` remains available to record/check. `--active-task`
and `--recovery-continuation-id` retain their existing contracts on all three
commands; this migration does not enable recovery for normal pre-task calls.
Malformed JSON returns `invalid_json`; missing or malformed envelope fields
return `schema_mismatch`. Existing nested validation, dirty/wrong authority,
stale-base classification, and interrupted-owner recovery behavior are retained.

### Current-owner mismatch diagnostics

After JSON reading succeeds, check preserves its existing receipt
`result.status`, `typed_exit` and `reason`. An objective binding/base failure
also supplies `result.diagnostic={code,field_path,remediation}` to this executing
Discovery AI. Invoke preserves its public DTO and emits that same three-field
diagnostic to stderr where it previously narrowed the failure to blocked or
base refresh. Record retains its direct error object/status. Errors already
returned directly by parameter, schema or target checks keep their original
stdout shape and exit status; they are not universally converted to blocked.
This is diagnostic information for this owner, not a Skill handoff, new Gate,
recovery store or authority token. `status=passed` means the checker completed;
the actual `typed_exit` still determines whether context can continue.

| Field/evidence class | Current owner's recovery |
| --- | --- |
| `owner_result.mode`, `change_input` or `base_observation` difference | Reread current public input and the actual Sync transition; rebuild this owner's complete result through record/check/invoke. Nested equality failures identify the first differing key or array position. |
| `owner_result.history_preview` difference | Reread current preview, review selection and affected evidence, then rebuild through the same original sequence. |
| `owner_result.result_identity` binding difference | Reread current source evidence and complete recorder output, then rebuild. A digest only identifies the binding/evidence class; it does not locate a source byte or establish a UTF-8 root cause. |
| `base_current`/`transition` authority evidence | Preserve the existing blocked/refresh classification. Resolve wrong, dirty, missing or mismatched authority with its original owner; obtain fresh `base_current` through `guru-sync-base/scripts/invoke.sh`, then re-enter Discovery. |
| `repository.selected_base` or `repository.decision_branch` during record | Match current live base authority in this owner's authoring, then record/check/invoke. |
| `return_identity.target_locator` | Return through the original Clarify `needs_context` and Discovery `context_request` for the current target. Preserve the original direct `stale_identity`, field and exit status. |

Do not patch recorded digests, another producer's transition or a previous pass.
Capture complete external-command bytes before UTF-8 decoding, or use a
streaming decoder that preserves partial characters across chunk boundaries.
Do not independently decode chunks and concatenate their replacement text.
The diagnostics contain only code, field/evidence location and recovery
instructions, never expected/actual values, body text, raw byte fragments or
OS exception details. These deterministic comparisons do not add provider
reads or automatically compare the current live Issue body. This AI still
reads that complete body and judges applicability before invoking the original
chain. Ordinary same-scope assembly repair follows its mapped recovery without
another continuation question; real scope choices and side effects retain
their original boundaries.

## Caller-aware context requests (#250)

Discovery owns evidence inventory and coverage, never intent, requirement
authority, source classification or user choices. The current initial order
remains Sync → Discovery → Clarify. `pre_task` explicitly names
`clarify_profile=standard_intake|reviewed_plan_intake`; reviewed Intake also
supplies selected source locators. `context_request` consumes actual Clarify
`needs_context` plus fresh caller-owned retrieval clues. Its four closed
`return_identity` branches preserve the original profile, target, continuation,
active TaskId/generation/interrupted consumer or standalone consumer. They
contain no Clarify owner result or private checkpoint.

`context_ready` returns those exact values and current evidence to Clarify.
Rebuild a legal current profile input from every actual return, including
repeated and stale/repaired loops. Initial/reviewed inputs reuse the new checked
duplicate snapshot; active and standalone inputs preserve their original
identity/consumer. A changed target is stale, never a silent retarget. The two
qualification confirmation profiles repair missing authority through their
original qualifier rather than this context loop.

See the Clarify package's MIGRATION-250.md for the synchronized schema migration.
