# `guru-discover-change-context` Contract

## Ownership And Modes

The global workflow owns mandatory invocation and exit consumers. This package
declares `judgment_mode=semantic` and owns:

```text
forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit
```

Workflow and standalone modes use byte-identical precondition ids and freshness
meaning. Both require a validator-passed fresh base before any live issue,
repository, or history semantic read.
`change_input` is a closed set of ten clue arrays and at least one array must be
non-empty; an issue binding or populated canonical query cannot substitute for
caller-supplied change input.

## Forward Behavior

Execute in this exact order:

1. validate fresh base evidence;
2. read the live issue or form a side-effect-free proposed draft;
3. search open duplicate candidates and record facts/reasons only;
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
target selection is not decided here and is handed to
`guru-clarify-requirements`.

## History Preview And Deep Read

History uses `guru-context-history-score-1.0`. The runtime enumerates only
`.trellis/tasks/archive/**/finish-summary.json`, component-wise rejects unsafe
paths, records symlinked or unreadable subtrees as isolated portable invalid
rows instead of silently skipping them, and projects only `index`. It never consumes index siblings,
`.trellis/workspace/**`, `.trellis/.runtime/**`, a repo-level index/cache, or
`finish-summary-index.json`.

Canonical query, scoring weights, token cap, path-sorted valid/invalid manifest,
sort order, positive-score limit 20, projection, `query_sha256`,
`archive_manifest_sha256`, and `preview_sha256` are deterministic. Invalid rows
carry only portable path and stable error code. Zero candidates is success with
empty selected/excluded/deep-read evidence and the exact `not_needed` mem shape;
it cannot trigger `trellis mem` or another history source.

AI deep-read uses one to three selected candidates and records a source-specific
portable locator, purpose, and conclusion. `task_artifact` locators are regular
repo-relative files inside the selected archived task; `github` locators are
canonical issue/PR URLs without query or fragment; `git` locators are exact
`git:object:<oid>` or `git:ref:<full-ref>@<oid>` identities whose object/ref is
verified live. `trellis mem` is permitted only after task
artifacts, current Docs/code/tests, GitHub, and Git history are each recorded
insufficient for one named load-bearing question. Otherwise record
`mem_review.status=not_needed`, a sufficiency reason, null question/summary, and
four false exhausted-source flags.

## AI Review Gate And Confirmation

The AI Gate records reviewed/excluded scope, relevance, sufficiency, conflicts,
reusable/non-reusable mechanisms, evidence-bound load-bearing conclusions,
findings with severity/status, and `passed` or `blocked`. Runtime scripts only
validate this evidence; they never generate it or choose the semantic exit.
A passed Gate must contain at least one reviewed-scope row and one
evidence-bound load-bearing conclusion. `mem_review.status=used` must include a
non-empty summary after all four insufficiency facts. These are objective shape
requirements, not script-authored semantic judgment.

Conditional human confirmation is always `not_required` with reason
`decision_owned_by_guru-clarify-requirements`. If a safe result cannot be
formed without product choice, return `blocked`.

## Snapshot, Freshness, And Exits

Pre-task recording is stdout-only and produces no repository/runtime/cache
write. After task creation, `snapshot_recorder --task` requires
`--expected-snapshot-sha256` and may write only byte-identical canonical output
to a direct active `{TASK_DIR}/context-discovery.json`; archived, completed, and
other non-active task locators fail closed. After atomic write the recorder
reopens the artifact, compares exact bytes and snapshot identity, and reruns
required live freshness before success. Existing different content is not
overwritten and no `.new`/`.bak` is created.

The recorder and checker execute the published closed Draft 2020-12 schema,
including `additionalProperties`, constants, formats, and conditional exits.
Their production entry order is pure schema/digest/security/semantic-shape
validation, then the base-only live gate. A `refresh_base` result requires one
repeatable `--prior-snapshot-input` / `--expected-prior-snapshot-sha256` pair
for every refresh-history entry, ordered from the oldest `context_ready`
ancestor through the direct prior. A history of length `N` also requires `N-1`
independently retained `--prior-refresh-receipt-input` /
`--expected-prior-refresh-receipt-sha256` pairs in hop order; the one-ancestor-
pair CLI remains valid for a single refresh without a receipt. The pure gate
recomputes every external identity, requires exact counts and distinct ordered
evidence, binds each history prefix and superseded query/snapshot digest to the
preceding real snapshot, requires every receipt to be the unique one-step
projection from the preceding ancestor and its history to equal the next
ancestor prefix, and accepts only the current one-step projection from the
direct prior. Missing, duplicate, reordered, skipped, rewritten, or non-parent
evidence fails closed. A receipt must be independently retained with its digest
from the preceding production result; current-candidate-derived evidence has no
authority. All evidence bytes remain external, are re-read after task recording
to detect drift, and are not persisted. Task-local recording before/after write
and every task-local check require the exact target to pass `git check-ignore
--quiet --no-index --`; ignored or unreadable trackability fails closed while
pre-task stdout mode skips this target gate. A stale base then
validates only the caller-authored refresh codes before returning;
it cannot inspect repository-bound query/current/deep-read locators, GitHub
issues, reviewed blobs, or archive/history state. Only a fresh base permits those
remaining locator and live checks. Pure invalid input fails before either live
stage.
Base evidence embeds the complete validator-passed
`guru-base-sync-result-1.0`; validation rechecks its facts/post-sync digests,
selected base/remote refs, strict GitHub remote repository identity, and current
HEAD. Pre-task and standalone checks also require the live decision branch.
Direct active task mode instead requires the live branch to equal
`task.json.branch`, allowing task/worktree creation to move the unchanged
snapshot HEAD to its feature branch while retaining full provenance, base refs,
repository identity, task status/locator, and task-local dirty-path checks. Git
status failure is not an empty clean result.
Before `context_ready`, validation also binds clean/task-local dirty scope,
live issue or draft digest, reviewed Git
blobs, canonical query, archive manifest, payload and snapshot digests. Any base
error short-circuits before live issue/draft, reviewed-blob, or history reads.
The source issue may be live `open` or `closed`; supported GitHub state casing
is normalized to lowercase. Duplicate candidates and a draft-created issue
binding remain independently open-only. Every 40-character reviewed Git
identity is re-resolved from `HEAD:<path>` and its live object type must be
exactly `blob`; a tree, gitlink commit, tag, missing object, or mismatched blob
cannot satisfy Docs, code/contracts, or tests evidence. A 64-character content
identity retains its exact byte-digest freshness check.
For a draft with a created issue ref, a separate issue binding records live
identity/body facts and the live body digest must equal the original reviewed
draft body digest. Stale evidence records stable refresh error codes; direct
active task branch drift emits refreshable `task_branch_stale`, while malformed
or otherwise non-refreshable task facts still block. Refresh entries bind the
ordered external ancestor identities; recorder/checker validate the caller-authored
`refresh_base` and return it for complete re-entry without choosing the route.
The same stale facts reject `context_ready`. Existing target inspection uses
`lexists`/`lstat`; every symlink including dangling links and every non-regular
target fails closed, while only byte-identical regular content is idempotent.
Portable-content validation walks every payload string, including observations,
duplicate facts/URLs, deep reads, findings, and errors. It rejects POSIX,
Windows-drive, UNC, home, and temporary machine-local absolute paths, AWS/GCS/
Azure SAS and generic signed-query credentials, private-key material,
GitHub/Bearer tokens, and database URLs without returning the raw matched value.
Normal HTTPS URLs and repo-relative paths remain valid. A precise
`/<namespace>:<command>` span is also portable when bare, inline-code, bold, or
sentence/Chinese-punctuation wrapped; this exception never admits `/workspace`,
`/custom`, multi-segment POSIX paths, Windows/UNC/home/temp paths, or signed URLs.

- `context_ready` -> workflow route `guru-clarify-requirements`;
- `refresh_base` -> `guru-sync-base`;
- `blocked` -> `change-context-blocked`.

Unknown, multiple, or unmapped exits fail closed. The package requires the
complete compatible Guru Team preset and `run-skill-command`; it is not
self-contained or portable.
