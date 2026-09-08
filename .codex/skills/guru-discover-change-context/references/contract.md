# `guru-discover-change-context` Contract

All live GitHub reads use the shared authenticated, repo-bound `gh` adapter
defined by `.trellis/spec/workflow/workflow-contract.md`; adapter errors are
facts and never replace this Skill's semantic review.

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

Each duplicate candidate fact projection is exactly `repo`, `number`,
`identity=#<number>`, canonical issue `url`, `state=open`, and `updated_at`.
`facts_sha256` is recomputed from those returned fields and excludes the
AI-authored reason/observation. Recorder/checker validate that same projection;
they do not issue a second duplicate search or re-read candidates after review.

`context_ready` schema 3.0 additionally projects one minimal immutable
`duplicate_snapshot` to the sole Clarification consumer. It binds the query,
checked time, target locator, authority body digest, canonical open-candidate
facts and their aggregate digest. This replaces the former 2.0 handoff for the
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
`--active-task`. Record, check, and public invoke then bind the live checkout to
`task.json.branch`, the current task worktree, and fresh selected-base refs while
allowing ordinary in-progress worktree edits; this normal mapped route remains
repository-write-free. Only a real interruption adds
`--recovery-continuation-id`, which writes one
`change-context-recovery.json` below that task's ignored owner-checkpoint
namespace. It retains only task identity, requested exit, Gate status,
reviewed scope, load-bearing conclusions, and reason. The checker binds those
bytes to a complete fresh owner rerun. Stale/invalid recovery is deleted, and
the public wrapper deletes a current checkpoint only after its typed DTO passes
the output schema. Pre-task and standalone calls cannot select active-task or
recovery invocation identity.

The recorder and checker execute the published closed Draft 2020-12 schema and
validate query/manifest/preview/payload/result digests. Matching live stale
facts return the caller-authored `refresh_base` exit for complete re-entry from
live authority. The commands do not reconstruct or persist a prior-result
chain.

The caller supplies the Sync public `base_current` transition separately from
Discovery public input. Before any issue, Docs, code, test, or history read, a
read-only Discovery observer validates that transition and reads the authority
checkout, GitHub repository identity, selected branch, local ref, remote-tracking
ref, HEAD, cleanliness, and worktree ownership. It never fetches, checks out,
resets, stashes, or writes a ref. A current transition becomes the owner-private
`base_observation`; a normal HEAD advance returns `refresh_base`, while dirty,
wrong, missing, mismatched, or ambiguous authority returns `blocked`. Neither
the public input nor owner result reconstructs Sync private result or digest
fields.

Before `context_ready`, validation also binds the live issue or draft, reviewed
Git blobs/content, canonical query, archive manifest and owner result. A base error
short-circuits before those later reads. A source issue may be live `open` or
`closed`. A draft-created issue binding remains open-only and its live body
digest must equal the original reviewed draft body digest. Every 40-character
reviewed Git identity resolves from `HEAD:<path>` to exactly a `blob`;
64-character content evidence is checked by exact byte digest.

- `context_ready` -> Skill `guru-clarify-requirements`;
- `refresh_base` -> `guru-sync-base`;
- `blocked` -> `change-context-blocked`.

Unknown, multiple, or unmapped exits fail closed. The package requires the
complete compatible Guru Team preset and `run-skill-command`; it is not
self-contained or portable.

## Interface 1.4 Public Handoff

`pre_task` is the only public profile. After the owner loop,
`scripts/invoke.sh --invocation -` validates the closed call-local public input,
`base_current` transition, current live base observation, and checker-passed
owner result, then derives the matching per-exit DTO without another duplicate
search. Recorder and checker receive that same envelope via `--invocation -`;
they do not accept a private Sync artifact.
`context_ready` contains route/profile/mode/target/continuation identity plus the
minimal checker-bound `duplicate_snapshot`. Clarification validates and consumes
that snapshot on the normal current path without repeating duplicate search or
candidate reads. It still receives no owner-result locator. Active-task identity remains an
ephemeral `--active-task` invocation argument rather than a public DTO field. A
genuinely interrupted owner additionally supplies one recovery continuation and
may lazily use one minimal ignored checkpoint, which the same owner deletes on
stale restart or successful consumption.

## Issue #384 Invocation Migration

This is a direct command-input replacement. The recorder/checker flags
`--input`, `--public-input`, and `--transition`, and recorder `--mode`, are
removed. Existing scripts must migrate together with this package; old argv
returns `invalid_arguments`, not an implicit compatibility path. Public input
2.0, owner result 3.0, typed exits, handoff projections, and recovery remain
unchanged. Previously incomplete invoke envelopes must also add the declared
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
shape, not a runnable valid call. Populate them with the current Discovery 2.0
public input, the independent Sync `base_current` transition, and complete
AI-reviewed owner result 3.0. Discovery has no additional owner-context fields,
so supply `{}` for `owner_context`. `public_input.mode` is the sole mode input.
The shared envelope schema closes the outer shape; the existing Discovery
validators still own the nested semantic evidence and freshness contracts.

Use these dispatcher entrypoints, supplying one complete JSON object on stdin
to each command:

```bash
scripts/record-context-discovery.sh --root . --invocation -
scripts/check-context-discovery.sh --root . --invocation -
scripts/invoke.sh --root . --invocation -
```

The caller retains the envelope in memory, captures record stdout and replaces
only its `owner_result`, then sends that envelope independently to check and
invoke. Check stdout is a validation result, not a replacement owner result.
Do not concatenate JSON documents or pipe record stdout directly into check.
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
