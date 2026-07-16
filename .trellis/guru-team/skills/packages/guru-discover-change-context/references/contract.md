# `guru-discover-change-context` Contract

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

## AI Review Gate And Confirmation

The AI Gate records reviewed/excluded scope, relevance, sufficiency, conflicts,
reusable/non-reusable mechanisms, evidence-bound load-bearing conclusions,
findings with severity/status, and `passed` or `blocked`. Runtime scripts only
validate this evidence; they never generate it or choose the semantic exit. A
passed Gate requires non-empty reviewed scope and load-bearing conclusions.

`typed_exit=blocked` if and only if `ai_review_gate.status=blocked`; schema and
runtime enforce both directions. Conditional human confirmation is always
`not_required` with reason
`decision_owned_by_guru-clarify-requirements`.

## Snapshot, Freshness, And Exits

Pre-task recording is stdout-only. After task creation, `snapshot_recorder
--task` requires `--expected-snapshot-sha256` and may write only the canonical
snapshot to direct active `{TASK_DIR}/context-discovery.json`. Existing
different bytes are not overwritten. After a write, the recorder reads the file
back once, compares exact bytes and snapshot identity, confirms Git
trackability with `git check-ignore --quiet --no-index --`, and reruns normal
live freshness checks.

The recorder and checker execute the published closed Draft 2020-12 schema and
validate query/manifest/preview/payload/snapshot digests. A caller-authored
`refresh_base` entry records stable live stale codes, superseded query digest,
superseded snapshot digest, reason, and detection time; matching live stale
facts return `refresh_base` for complete re-entry. The commands consume only
the current payload and expected snapshot identity; they do not reconstruct an
external history chain.

Base evidence embeds the complete validator-passed
`guru-base-sync-result-1.0`. Validation checks its schema and digests, then
compares selected base/remote refs, GitHub repository identity, current HEAD,
branch and clean/task-local dirty scope with live Git. Pre-task and standalone
bind the decision branch. Direct active task mode binds `task.json.branch` at
the unchanged snapshot HEAD.

Before `context_ready`, validation also binds the live issue or draft, reviewed
Git blobs/content, canonical query, archive manifest and snapshot. A base error
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
