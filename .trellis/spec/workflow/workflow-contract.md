# Workflow Contract

## Canonical Sources

`trellis/workflows/guru-team/workflow.md` is the reusable marketplace workflow
contract. Keep `.trellis/workflow.md` synchronized when this repo dogfoods a
workflow change, because local scripts such as `.trellis/scripts/get_context.py`
parse the active workflow to inject phase state.

Reference files:

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/index.json`
- `trellis/workflows/guru-team/README.md`
- `README.md`

## Phase Ownership

The workflow has four durable phases:

- Phase 0: issue intake, Git base branch selection, and worktree preflight.
- Phase 1: Trellis task creation, planning artifacts, `Docs SSOT Plan`, explicit post-planning user review, and start gate evidence.
- Phase 2: implementation and quality check.
- Phase 3: spec decision, commit, Branch Review Gate, finish-work, and automatic publish.

`trellis-finish-work` is a single resumable transaction entry. Its mandatory
order is: shared prepare/digest preview, expected-digest handshake, reviewed
content push, deterministic marketplace evidence and readiness commit/push,
unique draft PR binding, final archive projection, official task archive move,
one exact metadata commit/push, local/remote/PR HEAD equality, then
draft-to-ready. Archive is the last repository mutation, not the midpoint of
publish. Normal flow never asks the caller to choose `--skip-archive`,
`--recovery-after-finish-work`, or a separate publish command.
Before archive, the unique PR remains bound by normalized base repository,
exact head repository, head/base refs, number/URL/title and the untrimmed
task-local `pr-body.md` UTF-8 text across draft reuse and final summary. After
archive, ready/recovery uses remote repo/head/base/title/body digest facts from
the plan without reopening task artifacts; the normal invocation also carries
the already-bound number/URL through confirmation. Partial retries derive the exact missing stage
from persisted plan/readiness/evidence, Git/remote state, PR identity, and final
summary presence instead of replaying completed side effects. Archive
recovery also binds every tracked evidence blob to its archived blob; only the
official deterministic `task.json` completion fields may differ.
Raw `remote.<name>.url` / `pushurl` and `url.*.insteadOf` / `pushInsteadOf`
base/pattern values are read with NUL boundaries and origin evidence before
effective resolution. Empty/ambiguous records, boundary whitespace, controls,
unreadable origins, or a relevant config-file NUL fail closed; missing push URL
uses the raw fetch URL set. Effective output is not trimmed, must preserve raw
source cardinality, and after Git rewrite must use credential-free GitHub
HTTPS, `ssh://git@github.com`, or
`git@github.com:` transport. HTTP, `git://`, `file://`, local/bare paths,
scheme-less forms, userinfo/token variants, explicit ports, query/fragment, and
extra paths fail closed; the repo identifier normalizer is never a remote
parser fallback. Each strict URL and GitHub's `headRepository.nameWithOwner`
must normalize to `plan.git.repo`, the reported
owner must agree, and `isCrossRepository` must be false. Same-name fork
candidates and missing/unknown repository fields fail before 0/1/>1 selection
and cannot bind or replace the final summary.
The closeout failure matrix invokes production `cmd_finish_work()` against a
real temporary Git repository and bare remote. Only external GitHub/verifier
responses are faked; production transition functions are not mocked. Every
injected failure is cleared and re-entered through production `cmd_finish_work()`
while exact paths, SHA values, PR state, and transition attempts are asserted.
The preset throwaway verifier separately runs the installed `finish-work.sh`
through one complete dry-run/formal/archive/ready transaction after install and
again after `trellis update` plus preset reapply. It uses installed workflow,
wrapper, companion, schemas, config, and official `task.py`; it does not copy
canonical runtime assets into the fixture.

Do not move Phase 0 side effects into `task.py create`: `prepare-task.sh` must
resolve the source issue, base branch, branch name, executor-selected local worktree, and intake plan
before `.trellis/tasks/` artifacts are written.

`prepare-task.sh --json` is the default planner path. It may read GitHub issues,
search duplicates, and compute source/proposed issue data. Planner output,
including output with a confirmed `source_issue`, must be stdout-only and must
not write `.trellis/tasks/<task-slug>/task-start-context.json`, create a GitHub issue, worktree,
branch, or Trellis task. GitHub issue creation requires an explicit confirmed
executor flag such as `--create-issue-confirmed` plus reviewed title/body input.
`--create-worktree` and `--create-task` are executor flags for after AI intake
plan review and user approval. `--create-worktree` may write only the gitignored
local runtime workspace mapping; `--create-task` additionally writes tracked
task-local `task-start-context.json` after task creation. Ordinary intake does
not dirty the source checkout.

When there is no active task and the current turn requires file changes,
current-checkout direct edits are an explicit override, not a silent shortcut.
The user approval must state that the AI should skip creating or reusing a
GitHub issue, Trellis task, worktree, and branch for this turn. Before editing,
the AI must summarize skipped artifacts, current checkout, current branch,
dirty state, side effects, and changed-file scope. This approval does not cover
commit, push, PR creation, or issue closure.

## User-Facing Entrypoints

Daily user entrypoints are natural-language task requests, issue URLs or issue
numbers, `trellis-continue`, and `trellis-finish-work`. `trellis-start` is a
fallback orientation entry for disabled hooks, missing startup context, or an
explicit reload request.

Do not introduce `review-branch`, `check-review-gate`, `finish-work.sh`, or
`publish-pr` as new user-facing phases. They are companion script subcommands
used by the workflow entrypoints.

The explicit finish entry requires AI-authored task-local
`finish-summary-index.json`, dry-runs the shared prepare pipeline, and requires
the returned plan digest for formal execution. It binds one draft PR, builds a
strict final `finish-summary.json` before archive, moves it unchanged in one
archive transaction, then marks the PR ready after three-way HEAD alignment.
Guru Team does not call upstream `add_session.py` and does not use
`.trellis/workspace/**` as finish, readiness, or context evidence.
Shared `trellis-start` and canonical Codex/Cursor SessionStart overlays load
phase/packages/task/Git facts without journal helper imports or workspace
enumeration. Formal finish commits `pr-readiness.json.publish_inputs` before
the first PR create; recovery accepts only that archived immutable snapshot and
validates its Git blob/history, body/snapshot digests, gate, and branch identity
before the 0/1/>1 PR state machine. Git path snapshot command failure produces
empty path arrays and one fixed non-disclosing unavailable fact.

Reference files:

- `trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-finish-work/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md`
- `trellis/presets/guru-team/overlays/.cursor/commands/trellis-finish-work.md`

## Artifact Language

Target business repositories that install `guru-team` use Chinese by default
for human-readable documentation and workflow evidence:

- `.trellis/spec/**` project conventions and bootstrap outputs
- `.trellis/tasks/**`, including `prd.md`, `design.md`, `implement.md`,
  per-round Branch Review raw reports `reviews/*.md`, final rollup
  `review.md`, and human-readable JSON fields in `planning-approval.json`,
  `phase2-check.json`, `agent-assignment.json`, and `review-gate.json`
- `docs/**` durable requirements, design, test, deploy, operations, and
  versioned docs
- docs SSOT files created or completed by `00-bootstrap-guidelines`
- human-readable workflow/helper fields such as summaries, evidence, findings,
  observations, follow-up candidates, PR titles, and PR bodies

Keep literal command names, file paths, GitHub keywords, configuration keys,
external API names, code symbols, and other required tokens in English when
needed, but write the surrounding explanation in Chinese.

Branch Review `reviews/*.md` raw reports and the final `review.md` rollup are
human-readable task artifacts. Their Markdown headings, field labels, summaries,
evidence, findings, observations, follow-up candidates, deployment / safety
impact judgments, Docs SSOT judgments, and final conclusions must be Chinese by
default. Recommended `review.md` rollup sections include `审查轮次`,
`问题生命周期`, `最终审查`, `证据`, `观察项`, `后续候选`, and `结论`. Literal
commands, paths, JSON field names, HEAD values, GitHub keywords, code symbols,
external API names, and technical platform identifiers may remain English.

This source repository, `guru-trellis`, is a public extension repository rather
than a target business project. Its public README, source comments, script help,
marketplace metadata, and literal API tokens may remain English or bilingual
when that is clearer for distribution or interoperability. Do not apply that
exception to business-project `.trellis/spec/**`, `.trellis/tasks/**`, `docs/**`,
or bootstrap-generated docs SSOT.

## Commit Message Contract

The reusable `guru-team` workflow requires Chinese Conventional Commits for all
commits entering a PR branch or `main`:

- work commit and Trellis metadata commit subject:
  `{type}({scope}): #{primary_issue} 中文描述`;
- merge commit subject:
  `chore(merge): #{pull_request} 合并 #{primary_issue} 中文 PR 摘要`;
- `type` is one of `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`,
  `build`, `ci`, `chore`, or `revert`;
- `scope` matches `[a-z0-9._/-]+`;
- issue id appears after the Conventional Commits prefix and before the Chinese
  description, never before the prefix or inside scope;
- work commit body uses fixed sections `背景：`, `变更：`, `边界：`, `验证：`
  followed by `Refs #<primary_issue>`;
- Trellis metadata commits use an empty body and a Chinese metadata action such
  as `chore(trellis): #73 固化任务收尾元数据`;
- merge commit body uses fixed sections `合并：`, `范围：`, `审计：`, followed by
  `PR: #<pull_request>` and `Refs #<primary_issue>`.

Commit messages never use close keywords such as `Closes`, `Fixes`,
`Resolves`, `Close`, `Fix`, or `Resolve`. Closing semantics belong only in the
PR body and only for issues listed under
`issue-scope-ledger.json.close_issues`; commit messages use `Refs` for issue
links. `publish-pr` must output the merge commit subject/body/command payload so
maintainers do not rely on GitHub's default `Merge pull request #xx from ...`
subject or a Chinese PR title such as `完成：#xx ... (#yy)`.

Phase 2 check must verify planned work/metadata/merge commit message coverage.
Phase 3.4 runs `check-commit-messages.sh` before commit planning proceeds.
Branch Review Gate reviews committed messages and publish readiness payloads.
Finish-work metadata commits and publish merge payloads must be generated from
the same objective formatter/validator contract.

## Branch Review Gate

Branch Review Gate is a post-commit release gate. An independent Agent review
step must review the complete branch diff from the intake base branch to `HEAD`,
not just the latest edit, and must have zero findings before the gate can pass.
Any finding priority (`P0`, `P1`, `P2`, or `P3`) blocks. `review-branch.sh`
then records and validates that prior review result; the script is not the
reviewer. Non-blocking `observations[]` and out-of-scope
`followup_candidates[]` may be recorded separately, but must not hide
current-scope defects.

Independent review agents must inspect docs, code, tests, artifacts, and diff
evidence from an AI reviewer perspective. They must not run Guru Team
recorder/validator extension scripts such as `review-branch.sh`,
`check-review-gate.sh`, `record-agent-assignment.sh`, or `record-*` as part of
their review. The main session runs recorder/validator scripts only after the
review result exists, to persist objective gate evidence.

Phase 1.4 and Phase 2.2 have their own evidence gates before the Branch Review
Gate:

- `planning-approval.json` records that the main session completed planning
  artifact ambiguity review before display, displayed task-local links to
  `prd.md`, `design.md`, and `implement.md`, then received explicit
  post-planning user confirmation before `task.py start`. It must use
  `schema_version=1.2`, include passed structured `ambiguity_review` evidence,
  including fixed-scope controlled-term scanner results, use
  `user_confirmation.source=explicit-post-planning-review`, and record matching
  hash / size metadata for all three planning documents, plus
  modified-time, HEAD, and dirty paths as audit context. Validator freshness is
  based on the reviewed planning document digests, not current `HEAD` or
  working-tree dirty paths: implementation commits, metadata tail, or unrelated
  dirty paths do not invalidate approval while `prd.md`, `design.md`, and
  `implement.md` content still matches the last explicit user review. If any of
  those three planning documents changes, show the three links again and wait
  for fresh explicit post-planning confirmation. Phase 0 intake approval,
  generic workflow confirmation, old `source=workflow`, old schema, missing
  `ambiguity_review`, non-passed ambiguity evidence, unclassified scanner hits,
  `contract_violation` hits, or stale scanner evidence fails closed. `task.py
  start` is not proof of planning review.
- `phase2-check.json` records complete `trellis-check` coverage before commit.
  Passing validation commands alone is not proof that requirements, design,
  implementation, tests, specs, docs, cross-layer flow, and deployment impact
  were checked. It also records the pre-commit `dirty_paths` that the later
  post-commit audit may accept as the task work commit.
- `agent-assignment.json` records Chinese logical roles, technical `agent_id`,
  display-only platform nickname, HEAD evidence, review rounds, and
  reuse/replacement decisions for sub-agent-dispatch tasks. It is assignment
  evidence, not a script-owned decision about who should review or implement.
- Sub-agent technical identifiers remain stable and usually English
  (`trellis-implement`, `trellis-check`, `trellis-research`, channel runtime
  `implement` / `check`). User-facing labels should be Chinese where the
  platform has a display surface. Markdown-based agent files use Chinese
  descriptions/headings. Codex custom agents currently require ASCII
  `nickname_candidates`, so use Chinese `description` plus assignment
  `logical_role` for Chinese UI semantics there. Never change dispatch
  identifiers just for display.
- Default `sub-agent` mode has three mandatory execution boundaries:
  implementation is performed by `trellis-implement` / channel `implement`,
  Phase 2 check is performed by `trellis-check` / channel `check`, and
  Branch Review is performed by an independent review sub-agent after the task
  work commit. The main session coordinates dispatch, waiting, recovery,
  evidence recording, commit, and recorder/validator calls. It must not present
  its own implementation, its own Phase 2 check, its own self-review, or script
  validation output as any of those sub-agent results. Inline/self-exemption is
  valid only with explicit artifact evidence; otherwise missing sub-agent
  evidence fails closed. Before dispatching implementation or recording
  `phase2-check.json`, the main session must rerun
  `check-planning-approval.sh --json`; implement agents must also stop if that
  validator fails for the active task.
- `phase2-check.json` is Guru Team evidence for a completed `trellis-check`
  AI check. It records coverage, validations, findings, and dirty paths, but it
  is not the Trellis-native check step itself and recorder/validator success is
  not a substitute for the AI check judgment.
- Branch Review sub-agents are review-only. They inspect the full committed
  diff, normally `origin/<base>...HEAD`, and report findings/observations/
  follow-up candidates. They do not continue implementation, patch missing
  Phase 2 work, or run Guru Team recorder/validator scripts.
- Branch Review sub-agents verify Docs SSOT reconciliation that Phase 2 already
  completed. They read the approved `Docs SSOT Plan`, implementation handoff,
  `phase2-check.json` Docs SSOT coverage, durable docs, task artifacts, code,
  tests, scripts, schemas, presets, and overlays; they do not perform the first
  durable docs merge or patch missing Phase 2 docs work. Any current-scope Docs
  SSOT inconsistency is a blocking finding, not an observation or follow-up.
- Branch Review raw reports and the final rollup must use Chinese Markdown
  headings and Chinese field labels. Raw reports should record checked diff
  range, reviewed HEAD, evidence, findings, observations, follow-up candidates,
  deployment / safety impact, Docs SSOT judgment, sub-agent status/reuse
  evidence, and conclusion in Chinese narrative. The final `review.md` rollup
  should use sections such as `审查轮次`, `问题生命周期`, `最终审查`, `证据`,
  `观察项`, `后续候选`, and `结论`, while linking every raw report.

`review-branch.sh` must verify Phase 2 check evidence before writing
`review-gate.json` so Branch Review Gate cannot bypass Phase 2. When
`phase2-check.json.head` is an ancestor of the current `HEAD`, the audit may
accept non-metadata committed paths only when every such path is covered by
`phase2-check.json.dirty_paths` and the current working tree has no
non-metadata dirty paths. Branch Review Gate / publish readiness metadata may
change after Phase 2 because final review and release readiness are produced
after the work commit. The post-commit audit may ignore stale Phase 2 digest
entries for task-local `issue-scope-ledger.json`, `pr-body.md`,
`pr-readiness.json`, `agent-assignment.json`, `review.md`, and
`review-gate.json`; Branch Review Gate or publish validators must revalidate
the current files before pass or publish. Source, config, script, schema, docs,
preset, overlay, and non-gate task artifact drift still blocks the gate. Do not
re-record Phase 2 after the task work commit just to make HEAD match.

## Docs SSOT Plan

Phase 1 planning must create or update one locatable `Docs SSOT Plan`.
Prefer `design.md` as the authoritative section. `prd.md` records docs state
and requirement impact; `implement.md` records the checklist, merge checkpoint,
repair boundary, or no-update checkpoint. Do not require the full plan to be
duplicated across all three planning documents.

The plan records one docs state:

- `complete_docs`
- `partial_docs`
- `stale_docs`
- `no_docs`

The plan records one synchronization strategy:

- `ssot_first`
- `delta_first`
- `bootstrap_or_repair_docs`
- `no_docs_update_needed`

Required fields are docs state and evidence paths, strategy and reason,
affected durable docs or checked durable docs, task artifact deltas to merge
back, the `delta_first` merge checkpoint when applicable, the
`bootstrap_or_repair_docs` minimum repair scope or follow-up limit when
applicable, and the concrete `no_docs_update_needed` reason when applicable.

Broad and clear requirement, design, workflow, API, data, deploy, operations,
or test contract changes should prefer `ssot_first`. Small local fixes or early
exploration may use `delta_first`, but the plan must name the merge checkpoint.
`no_docs`, `partial_docs`, and `stale_docs` must choose
`bootstrap_or_repair_docs` or otherwise explain a bounded follow-up; task
artifacts must not silently become a long-term substitute for durable docs.

This is an AI planning judgment expressed in Markdown workflow / planning
artifacts. Companion scripts may record paths, hashes, or approval evidence,
but must not decide whether durable docs are semantically complete, stale, or
adequately repaired.

Phase 2 consumes the approved plan. Implementation must execute the recorded
strategy and include in its handoff: strategy, durable docs sync result, task
artifact deltas merged back into durable docs, task-history-only content,
`no_docs_update_needed` reason when applicable, `bootstrap_or_repair_docs`
minimum repair / follow-up / current PR limitation when applicable, and which
implementation inputs came from durable docs versus confirmed temporary task
deltas. Phase 2 check must verify durable docs, `prd.md` / `design.md` /
`implement.md`, code/API/schema/config/deploy/test, and validation/test
coverage against the same plan. `delta_first` cannot pass final Phase 2 check
until durable docs merge is complete; `ssot_first` must use revised durable
docs / specs / workflow contracts as primary implementation input;
`bootstrap_or_repair_docs` must complete minimum repair or explicitly bound
follow-up / PR limitations; `no_docs_update_needed` must be rechecked against
the final diff.

If implementation or check discovers a long-term product, architecture, API,
data, deployment, operations, test, or workflow contract change that the plan
does not cover, update planning artifacts and the `Docs SSOT Plan`; when
`prd.md`, `design.md`, or `implement.md` content changes, obtain fresh
explicit post-planning approval before continuing and rerun Phase 2 check. Do
not defer the first semantic docs consistency judgment to Branch Review Gate or
finish-work.

## Branch Review Gate Coverage

The gate must cover docs, code, tests, Trellis artifacts, config, scripts,
schemas, CI/CD, container files, Kubernetes/Kustomize/Helm assets, database
migration assets, Makefiles, preset installer changes, generated marketplace
files, Issue Scope Ledger, and publish readiness. If the task or branch used a
no-task current-checkout direct-edit override, the review must verify explicit
user approval evidence; otherwise it must verify Phase 0 handoff/preflight
evidence for file-changing work.

For Docs SSOT, the gate must verify the full strategy chain without becoming
the merge step: the approved plan exists, the implementation handoff records
strategy execution and durable-docs versus task-delta inputs, and
`phase2-check.json` covers docs consistency. For `ssot_first`, durable docs /
specs / workflow contracts are the primary implementation input; for
`delta_first`, task deltas are merged back before final Phase 2 check; for
`bootstrap_or_repair_docs`, the minimum repair is complete or current PR
limitations and follow-up are bounded; for `no_docs_update_needed`, the reason
still holds for the final diff. Missing or inconsistent current-scope docs
sync blocks the gate.

Before writing `review.md`, `review-gate.json`, or any task artifact during the
gate, the AI must verify the shell/editor working directory is the task
worktree selected by local runtime and Git worktree facts. Manual edits must use a
worktree-local absolute path when the editing tool cannot receive an explicit
working directory. Relative task artifact paths are never relative to the source
checkout or another worktree.
The normal deterministic probe is
`.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task
<task-path>`. It provides expected/actual workspace evidence, source checkout
status, task worktree status, suspicious source artifact facts, and fail-closed
errors. The probe does not determine stale status, clean up source checkout
state, migrate misplaced changes, or replace AI/human review.

Passing the gate requires:

- `review-branch.sh --json --pass`
- `--review-source independent-agent`
- a Chinese `--summary`
- at least one concrete `--evidence` line
- task-local `review.md`
- `--review-report <task-local review.md>`
- `--reviewer` only as optional identity metadata for the independent reviewer;
  `*-main-session` and `self-review` identities are rejected for passed gates
- `--review-report` must point to the task-local file named `review.md`, not
  another task artifact, and the recorded digest must still match the current
  file
- `--agent-assignment` must point to the task-local `agent-assignment.json` so
  the gate records its digest and Chinese logical-role summary
- `review_rounds[].round` values must be unique and strictly increasing in
  recorded order, so the final pass round is unambiguous
- every review round with `findings_count > 0` must have a later same-agent
  `问题闭环审查代理` round with `findings_count: 0` and
  `reuse_decision: reuse-for-closure`, or a replacement closure chain when the
  finding owner objectively failed, was interrupted, or became stale and cannot
  continue; replacement closure requires predecessor liveness evidence in
  `status_events[]`, `replacement-started` with `predecessor_agent_id`,
  `predecessor_event_id`, `replacement_reason`, and `handoff_summary`,
  `reuse_decisions[]` `decision=replace` with `from_round` / `to_round`, and a
  replacement `问题闭环审查代理` round with `findings_count: 0` and
  `reuse_decision: replace` before any fresh final round can pass. This closure
  proves the finding is closed and does not need to be repeated for every later
  HEAD
- the final `最终放行审查代理` review round must be fresh and last: reviewed code
  HEAD, `findings_count: 0`, `reuse_decision: new-agent`, and a technical
  `agent_id` that did not own any earlier finding round
- deployment impact evidence, even when the conclusion is that no deployment
  asset needs a change
- no findings of any priority

## Publish Boundary

`trellis-finish-work` is the closeout entry. It calls `finish-work.sh` with the
required `--from-trellis-finish-work` intent marker. The helper validates the
passed review gate and its `review_report` digest, allows only Trellis
metadata after the reviewed HEAD, rejects uncommitted non-metadata changes,
builds and validates the immutable plan, pushes reviewed content and evidence,
binds one draft PR, validates the final projection, archives the active task in
one metadata transaction, and then marks the PR ready.

The shared prepare stage must construct the full future finish-summary with a
deterministic sentinel PR and validate its schema, artifact set, archive paths,
ledger, readiness inputs, and exact move set before any write, push, verifier,
or GitHub call. Once the draft PR exists, the executor may substitute only the
canonical PR URL and unique `PR #<number>` ref into that prevalidated template.
Marketplace evidence locators are task-relative and remain valid after archive.

Finish-work and archive must not execute the first Docs SSOT merge. If durable
docs, `.trellis/spec/`, source, tests, schema, config, scripts, preset, overlay,
CI/CD, deployment, migration, Makefile, or other non-metadata assets drift after
the gate, dry-run and formal finish fail closed and the task returns to Phase
2/3 for check and review.

`trellis-continue` must stop at Branch Review Gate and must not push, create a
PR, invoke `publish-pr`, or invoke `finish-work`. The finish and publish helpers
are fail-closed: ordinary direct `finish-work.sh` calls are rejected before
archive/finish-summary/push side effects, and ordinary direct `publish-pr` calls are
rejected before `git push` / `gh pr create`. Every closeout interruption is
resumed through the same state-aware `trellis-finish-work` entry.

Before the exact archive commit exists, same-entry archive recovery is bound to
the plan's complete `move_paths`, `tracked_move_paths`,
`untracked_archive_outputs`, exact `evidence_paths`, evidence commit parent,
active-locator absence, archived working-tree completeness, exact dirty/staged
paths, and tracked blob continuity. Git paths are exact: tracked moves appear
on both sides, while outputs first generated after the evidence commit appear
only at archive. A partial, missing, extra, misclassified, or tampered
pre-commit state is invalid. If current `HEAD` is absent from or mismatched with
the planned archive transaction, this metadata recovery path remains fail
closed.

After current `HEAD` is the exact archive commit, recovery validates the
immutable plan and Git parent/path/tree/blob lineage instead of archived
working-tree layout or dirty state. Missing or tampered local archived files do
not block pushing that exact commit when remote is behind, verifying
local/remote/PR HEAD, or retrying `gh pr ready`; no task artifact may be built
or rewritten. A plan-only archived directory is resolvable only through
`trellis-finish-work`; ordinary task commands still require `task.json`.
Plan-only recovery reads the immutable plan from the current commit blob and
uses a dedicated boundary, not an unconditional workspace-boundary skip. Before
GitHub access or committed recovery it must match the Git toplevel,
configured/effective repo, current head branch, available base ref, current
HEAD transaction, expected plan digest, task identity, and exact active/archive
locator relationship. All other discovery and command paths retain the normal
`task.json` and worktree-mode `task-start-context.json` requirements.
The finish entry validates its raw locator before ordinary resolution: only a
basename, exact former active locator, or exact archive locator is accepted,
and path-like input receives lexical repo/archive containment plus
component-wise `lstat` through the final directory before any fallback, which
rejects internal/external, relative/absolute, ancestor/final, multilevel,
dangling, and loop aliases. The ordinary resolver then keeps explicit
`task.json`, active task, and normal archived `task.json` precedence. Only its
not-found result enables plan-only recovery. An exact archive locator selects
that candidate; basename/former-active fallback requires one unique archive
match and fails closed on ambiguity. The resulting non-symlink plan-only target
must still resolve to the plan's canonical archive locator. Do not use
arbitrary `samefile` re-anchoring; only the verified Darwin system `/var` ->
`/private/var` mapping is an allowed outer-path normalization.

The generated PR must start as draft, target the intake/task `base_branch`, and
become non-draft only after archive HEAD alignment. Close keywords are allowed
only for issues in `issue-scope-ledger.json.close_issues`.

Before publish, the AI must generate or review a PR body that is readable to a
GitHub reviewer without Trellis session context. The body must include concrete
Chinese sections for `变更摘要`, `影响范围`, `验证结果`, `Review Gate`,
`Issue 关闭范围`, `安全说明`, and `Docs SSOT` / `文档同步`. The Docs SSOT section
must state the strategy, durable docs updated or no-update reason, task delta
merged back, task-history-only content, and follow-up or current PR limitation.
Non-draft publish must receive an AI-reviewed
`--body-file` or `--body-artifact`; script-generated `generated` bodies are
preview/draft-only and never count as publish readiness evidence. Reviewed
body/readiness files are task metadata: they are written and fully validated in
the active task before `finish-work` performs the official archive move.
Post-archive ready/recovery hashes the remote PR body against the immutable plan
and does not reopen these artifacts. If an active readiness artifact
references a relative `body_file`, resolve it relative to the artifact's own
directory. `publish-pr` validates objective structure, forbidden
low-information phrases, reviewed source presence, Docs SSOT section/key
presence, archive-path resolution, and close/ref issue semantics, but it must
not decide whether the business explanation is true or sufficient.

Do not treat `.trellis/tasks/<task-slug>/task-start-context.json` as final close scope. It is
intake provenance only.

## Common Mistakes

- Updating only `.trellis/workflow.md` and forgetting the reusable workflow in
  `trellis/workflows/guru-team/workflow.md`.
- Adding a new phase that users must remember instead of making it part of
  `trellis-continue` or `finish-work`.
- Treating Phase 2 `trellis-check` as a replacement for the Phase 3 Branch
  Review Gate.
- Using `source_issue` to decide PR close keywords instead of the task-level
  Issue Scope Ledger.
- Silently editing the current checkout in `no_task` because the change looks
  small, instead of running Phase 0 or obtaining explicit direct-edit override
  approval.
- Recording project-private business rules in the reusable marketplace workflow.

### Remote Marketplace Verification Gate

For tasks that change the workflow marketplace, preset, overlays, installer, schema, or public extension contract, publish is fail-closed after the branch push and before `gh pr create`. The deterministic `verify-marketplace` companion command records task-local `marketplace-verification.json` with repository, remote, branch/ref, verified content HEAD, remote HEAD, command exit codes, stdout/stderr digests and sizes, and installed workflow/preview/schema digests. It executes remote branch `trellis init`, workflow preview, workflow switch, canonical preset reapply, and runtime-ignore checks in a clean temporary repository. It does not decide PR readiness.

`issue-scope-ledger.json` must carry one exact structured `remote_marketplace_verification` evidence object in the primary issue and every close issue. Before the verifier it is `status=pending`, `required=true`, points to task-relative `marketplace-verification.json`, and explicitly does not satisfy final publish. Formal closeout pushes the reviewed content HEAD, runs the verifier, replaces only those structured entries with real `status=passed` facts, then commits and pushes the exact immutable plan/readiness/verifier/ledger evidence allowlist. Only after remote equality may it bind the unique draft PR, build the final summary once, and perform the archive transaction. Missing, pending, failed, stale, tampered, or mismatched evidence blocks. The AI remains responsible for close scope and evidence sufficiency; scripts execute and validate deterministic facts. No release tag is created by this gate.
