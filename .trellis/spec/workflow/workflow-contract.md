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

Public mandatory workflow steps are invoked by stable skill id. The global
workflow owns only phase order, `guru-skill-invoke` markers, transitions, typed
exit consumers, and fail-closed stops; the active package under
`trellis/skills/guru-team/` owns the step-local closed loop. Commands, prompts,
breadcrumbs, launchers, and workflow prose must not duplicate that loop. See
[skill-package-contract.md](./skill-package-contract.md).

The workflow has four durable phases:

- Phase 0: issue intake, Git base branch selection, and worktree preflight.
- Phase 1: Trellis task creation, planning artifacts, `Docs SSOT Plan`, explicit post-planning user review, and start gate evidence.
- Phase 2: implementation and quality check.
- Phase 3: spec decision, commit, Branch Review Gate, finish-work, and automatic publish.

Phase 0 begins with tool-free request classification. Before `check-env`,
`prepare-task`, issue/duplicate reads, Docs/code/tests/history reads, or any
other repo/network semantic action, repo-changing routes mandatory invoke the
stable `guru-sync-base` id. The workflow owns only that invocation and these
unique consumers: `synced` -> Skill `guru-discover-change-context`, `skipped` ->
workflow route `original-request-route`, and `blocked` -> stop
`base-sync-blocked`. The change-context Skill owns its complete semantic loop;
the global workflow contains only its mandatory invocation and typed-exit
transitions.

`guru-sync-base` declares `judgment_mode=deterministic`; its deterministic
profile owns stdout resolution facts, pre-sync digest-bound execution,
post-sync resolution generation, objective live Git validation, and typed exit.
Its exact stage order is `forward_behavior -> recorder_validator -> typed_exit`;
it does not perform selected-base AI confirmation, conditional human
confirmation, or a post-execution AI Review Gate. Resolver order is explicit
base, non-empty scalar config, first existing configured candidate in declared
order (default `dev -> develop -> main -> master`), then remote default when no
candidate exists. The validator returns only the successful result's
`post_sync_resolution_sha256` to the next consumer. `prepare-task` receives that
digest and reuses the same resolver/sync core before semantic reads and again
before each GitHub/worktree/task mutation. Every guard consumes the preceding
post-sync digest and returns its own post-sync digest for the next guard; a
pre-sync digest is never reused after a fast-forward. No cross-step
result/resolution file or lifecycle is part of this contract.
Unknown, missing, duplicate, multiple, or unmapped markers fail closed. A
current checkout branch is never an implicit base fallback.

`guru-discover-change-context` declares `judgment_mode=semantic`. Workflow and
standalone modes use the same entry preconditions and freshness bindings. The
positive behavior order is fixed: validate fresh base evidence; read the live
issue or form a side-effect-free proposed draft; search open duplicate facts;
AI-review updated-base Docs; AI-review code/API/config/schema/ownership;
AI-review tests/fixtures/throwaway/update evidence; produce current-state
observations and canonical query clues; execute exactly one archived
finish-summary preview; AI-select one to three candidates when candidates
exist and deep-read explicit evidence, or record an empty selection; execute
the AI Review Gate; record/validate the reviewed payload; emit one typed exit.

Duplicate reuse/new-target choice remains owned by
Skill `guru-clarify-requirements`. Conditional human confirmation is recorded as
`not_required` with reason
`decision_owned_by_guru-clarify-requirements`. Stable exits are
`context_ready` -> Skill `guru-clarify-requirements`, `refresh_base` -> Skill
`guru-sync-base`, and `blocked` -> stop `change-context-blocked`. A stale base,
issue, reviewed blob, canonical query, or archive manifest forces complete
re-entry through `guru-sync-base`; the workflow cannot resume from history or
the AI Gate. Recorder/checker validate the caller-authored `refresh_base`
against deterministic live stale codes and return that typed exit; they never
infer or replace AI route intent. `context_ready` rejects the same stale facts.
At both production command entries, closed schema/digest/semantic-shape
validation is pure and fails before live access. The next gate reads only base
facts. Base stale returns after matching refresh codes and superseded digests.
Duplicate candidates use the deterministic fact projection `repo`, `number`,
`identity=#<number>`, canonical issue URL, `state=open`, and `updated_at`;
`facts_sha256` excludes AI reason/observation and is recomputed in the pure
gate from the fields returned by the one open duplicate search. Recorder and
checker do not run a second search or re-read candidates after AI review. The
schema/runtime state matrix also requires
`typed_exit=blocked` if and only if `ai_review_gate.status=blocked`.
For `refresh_base`, both production entries validate the current stable stale
codes and superseded query/snapshot digests recorded by the caller, then return
for complete re-entry. They consume only the current payload and expected
snapshot identity, without reconstructing a refresh ancestry chain. Repository-bound locators,
issue/blob/history evidence are checked only after a fresh base. Both modes
require at least one non-empty `change_input` clue array.

Fresh-base evidence includes the complete validator-passed
`guru-base-sync-result-1.0` identity and provenance, not only matching HEADs.
The selected remote must resolve to the same normalized GitHub repository, and
Git status read failure fails closed. A proposed draft that later names a
created issue remains bound to the original draft digest and must prove the
live issue body digest is identical before recording.

The pre-task invocation is stdout-only. After task creation, the recorder may
write only the byte-identical expected snapshot to
`{TASK_DIR}/context-discovery.json`. Before writing and again after writing, the
recorder, and every task-local checker invocation, must prove that this exact
repo-relative target is not ignored via `git check-ignore --quiet --no-index --
<target>`. This covers repository `.gitignore`, `.git/info/exclude`, and
`core.excludesFile`, including an already tracked target. Ignored or unreadable
trackability fails closed as `context_discovery_target_ignored` or
`context_discovery_target_trackability_unreadable`; stdout-only pre-task mode
does not run this target gate. Neither mode reads or writes
`.trellis/workspace/**`, repo-level history indexes/caches, or shared handoff
state.

Workflow and stop consumers are declared by one unfenced
`guru-workflow-target` or `guru-stop-target` marker at the actual continuation
or fail-closed stop. Source and installed validators require every Skill
consumer to resolve to an active registry entry and every workflow/stop target
to have exactly one matching-kind declaration; missing, multiple,
kind-mismatched, or dangling targets fail closed.

`guru-clarify-requirements` is the active semantic consumer of
`guru-discover-change-context:context_ready`. It owns initial intake clarity,
active-task scope change, and explicit standalone clarification review in one
step-local closed loop. Workflow and standalone modes use identical runtime,
authority, context, target, and freshness preconditions. Its positive behavior
classifies confirmed facts, repository-answerable questions, product-intent
questions, scope-risk decisions, and out-of-scope facts; exhausts
repository-answerable questions before asking the user; runs a one-question
clarification loop; selects a source-of-truth action; completes the AI Review
Gate; obtains exact action/proposal confirmation when required; records and
validates current facts; and returns exactly one typed exit.

The workflow owns only the mandatory invocation and unique consumers. The one
mandatory invocation marker is located in the shared active-task Scope Change
Gate and is also consumed by the initial intake route; neither call site may
copy the Skill's classification loop. `clear` -> workflow target
`guru-requirements-clear-router`, `needs_context` ->
Skill `guru-discover-change-context`, `refresh_context` -> Skill
`guru-sync-base`, `new_task` -> workflow target
`guru-full-task-intake-chain`, and `blocked` -> stop
`requirements-clarification-blocked`. The clear router validates the closed
`invocation_context.resume_target`: initial issue/draft resumes the staged #114
wording route, standalone returns to its direct caller, accepted active-task
scope returns to planning review, and non-current active-task classification
returns to the exact interrupted phase target. It performs no semantic
reclassification. #112 owns the complete task-intake chain. Unknown, multiple,
unmapped, or invocation/resume mismatched exits fail closed.

A successful GitHub issue comment/body mutation returns `refresh_context`, not
`clear`, so the base/context/clarification chain reruns against the new
authority. `new_issue_draft` is side-effect-free and returns `new_task`; this
Skill never creates a GitHub issue. Pre-task and standalone results are
stdout-only and create no repository clarification cache, workspace journal,
or fixed handoff. Active-task `clear`/`new_task` requires a non-empty set of the
seven terminal decisions. Every accepted-current, related, followup, new-task,
or out-of-scope scope classification requires proposal-digest-bound exact user
evidence, regardless of origin status. It binds live GitHub-visible authority and one structured
decision trail exactly present in current
`issue-scope-ledger.json.scope_decisions[]`, including all three planning
document digests, a shared-validator-passed complete schema 1.2 planning
approval, review state, stale downstream identities, authority `updated_at`,
and `context_before_task_update_sha256`,
the interrupted target and re-entry owners `guru-approve-task-plan`,
`guru-check-task`, and `guru-review-branch`. GitHub comment/body authority mutation
returns `refresh_context`; only that GitHub mutation requires the
refresh. The refreshed context `generated_at` must not predate authority
`updated_at`; task update then binds that same digest and does not require a
second context refresh. `mechanism_removed/replaced` requires optional origin,
null confirmation, no trail, and no authority mutation. An active-task
`new_task` preserves that current-task trail and still hands #112 only a
side-effect-free reviewed draft.
The active-task Scope Change Gate mandatory invokes this Skill rather than
asking/classifying/updating the ledger directly in workflow Markdown.

After initial requirement clarification returns `clear`, and again after all
three planning artifacts exist, the workflow mandatory invokes
`guru-review-contract-wording`. The initial route uses fixed profile
`change_request`; the planning route uses fixed profile `planning_artifacts`.
The global workflow owns only invocation and these unique external consumers:
`pass` -> `guru-contract-wording-pass-router`, `content_changed` ->
`guru-contract-wording-change-router`, and `blocked` ->
`contract-wording-blocked`. The pass/change routers restore the continuation
from the checker-validated profile: change-request pass continues task intake,
planning-artifacts pass permits planning artifact presentation, and content
changes re-enter the corresponding full review. Unknown, missing, multiple,
stale, or unmapped profile/exit evidence fails closed.

The workflow, prompts, launchers, and platform entries must not reproduce the
Skill's vocabulary, classification catalog, rewrite/classification/review
loop, scanner behavior, or evidence derivation. They reference only stable
Skill id, fixed profile, schema `guru-contract-wording-review-1.0`, typed exit,
and their consumer obligation. For `planning_artifacts`, that obligation also
requires the canonical contract's exact planning-only dimension evidence with
every value explicitly AI-reviewed as true. A zero-hit deterministic scan or
runtime-generated default is not a substitute for the Skill's semantic Review
Gate.

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
not dirty the source checkout. Every invocation receives the expected
resolution digest; each planner or executor guard must reproduce the same
provenance before it may continue.

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

Do not introduce `review-branch`, `check-review-gate`, or `finish-work.sh` as
new user-facing phases. They are companion script subcommands used by the
workflow entrypoints; `publish-pr` is only a compatibility blocker.

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
links. `format-merge-commit` must output the merge commit subject/body/command payload so
maintainers do not rely on GitHub's default `Merge pull request #xx from ...`
subject or a Chinese PR title such as `完成：#xx ... (#yy)`.

Phase 2 check verifies implementation and message-relevant evidence, but it does
not ask for manual approval of a planned work message. After a fresh final Phase
2 pass, Phase 3.4 mandatory invokes `guru-create-task-commit`. The skill owns
candidate construction, AI review, conditional confirmation and re-entry; its
candidate mode calls the shared `validate_commit_message()` parser, and its
exact executor validates the resulting commit. Candidate validation, executor
entry before staging, and the boundary immediately before `git commit` each
fail closed while merge, cherry-pick, revert, rebase, sequencer, or `git am`
state is active; scripts only observe that state and do not consume or clear it.
Mode `160000` dirty entries bind an initialized, clean submodule worktree HEAD,
so changing the gitlink revision after AI review makes the candidate stale.
Immediately before exact staging, the executor compares that worktree HEAD
again. It then writes the reviewed `gitlink_head` directly as the mode `160000`
index OID instead of asking `git add` to read the mutable submodule worktree.
The staged index identity must equal the artifact identity before commit; an
unreviewed revision can never become the expected index tree.
Ordinary files, modes, symlinks and deletes use their existing artifact
SHA-256/mode/delete identity the same way. Snapshot producers write
`renamed_from` only for rename destinations and `copied_from` only for copy
destinations. Only a rename source inherits the reviewed destination's exact
stage and deletion authority. A copy source never enters exact stage because
of the relation; when it is itself dirty, it is a separate snapshot path that
must be classified and reviewed independently. Candidate self uses
deterministic bytes from the validated in-memory plan. Hooks and exact staging
run against an isolated index plus detached transaction HEAD. The real branch,
live index and committed candidate result are published only after the commit
object and current worktree/candidate/operation/index preconditions all match;
the real `index.lock` remains owned through candidate publication and rollback,
the conditionally advanced loose ref and candidate writes are guard-bound, and
an independent final-index temporary file is published to the live index while
the `index.lock` sentinel still exists. With ref/index guards still held and
the ref, index and candidate result already in transaction state, one final
candidate inode/content identity read is the success linearization point. A
candidate replacement before that read blocks, rolls back the owned ref/index
and preserves the replacement; a replacement after the read is a later
operation and does not retroactively block or overwrite the committed result.
Ref/candidate rollback is conditional and never overwrites third-party state;
after the successful final read only best-effort guard/temp cleanup and return
may occur.
Branch Review Gate reviews
committed messages and publish readiness payloads. Finish-work metadata commits
and publish merge payloads remain on the same objective formatter/validator
contract.

The global workflow owns only the invocation point, finding-fix repeat
condition, and the unique consumers for `committed`, `revision-required`, and
`blocked`. Candidate fields, exact staging, confirmation policy, executor steps,
and postconditions belong only to the canonical skill package.

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

- `planning-approval.json` records that the main session obtained a current
  checker-validated `guru-review-contract-wording:planning_artifacts:pass`
  artifact before display, displayed task-local links to `prd.md`, `design.md`,
  and `implement.md`, then received explicit post-planning user confirmation
  before `task.py start`. It must use `schema_version=1.2`, bind the current
  `guru-contract-wording-review-1.0` artifact/schema/scope/scan identity, include
  its deterministic compatibility projection under `ambiguity_review`, copied
  value-for-value from the checker-validated planning-only dimensions without
  defaults, use
  `user_confirmation.source=explicit-post-planning-review`, and record matching
  hash / size metadata for all three planning documents, plus
  modified-time, HEAD, and dirty paths as audit context. Validator freshness is
  based on the reviewed planning document digests, not current `HEAD` or
  working-tree dirty paths: implementation commits, metadata tail, or unrelated
  dirty paths do not invalidate approval while `prd.md`, `design.md`, and
  `implement.md` content still matches the last explicit user review. If any of
  those three planning documents changes, or schema 1.0 wording evidence lacks
  the planning-only dimension field, rerun the complete AI review, show the
  three links again, and wait for fresh explicit post-planning confirmation;
  never patch missing booleans into old evidence. Phase 0 intake approval,
  generic workflow confirmation, old `source=workflow`, old schema, missing or
  non-pass wording evidence, projection drift, non-empty unchecked hits, or
  stale wording evidence fails closed. `task.py start` is not proof of planning
  review. Active approvals created before the wording-evidence binding require
  a fresh wording review, document presentation, and explicit confirmation;
  archived artifacts are not rewritten.
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
- schema 1.2 append-only provenance corrections must digest-bind an existing
  same-agent correctable event; invalidated events remain in raw history but
  are excluded from liveness/gate projection. Recovery links may only connect
  an earlier same-agent `failed` event to a later manual/platform
  `terminated-unfinished`; the validator must then traverse the existing
  replacement chain to a real `completed`
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

Initial prepare walks the existing archive root, month, and final destination
components with lexical `lstat`, rejects every symlink including dangling
links without reading its target, and requires the planned final locator to be
absent. The same preflight runs again immediately before the official move, so
prepare-to-move ancestor drift cannot redirect or nest the task. Task
`children` defaults to `[]` but otherwise must be `list[str]`; using the
official active-task exact/suffix lookup, only children whose active
`task.json` would be rewritten block closeout. Historical archived children do
not block their parent.

Finish-work and archive must not execute the first Docs SSOT merge. If durable
docs, `.trellis/spec/`, source, tests, schema, config, scripts, preset, overlay,
CI/CD, deployment, migration, Makefile, or other non-metadata assets drift after
the gate, dry-run and formal finish fail closed and the task returns to Phase
2/3 for check and review.

`trellis-continue` must stop at Branch Review Gate and must not push, create a
PR, invoke `publish-pr`, or invoke `finish-work`. The finish helper and publish
compatibility command are fail-closed: ordinary direct `finish-work.sh` calls
are rejected before archive/finish-summary/push side effects, and every
`publish-pr` call is rejected before repo/task resolution, `git push`, or
`gh pr create`. Every closeout interruption is
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
closed. The final summary's deterministic real-PR bytes/digest are part of both
pre-move and incomplete-recovery continuity and must be rebuilt against the
already-bound remote PR; the summary cannot self-authorize a different PR.

Before official move, the active side is checked earlier: the live official
archive month still equals the plan, the index is empty, untracked paths equal
the planned final outputs, every move path is a regular file, tracked modes are
`100644` or `100755` and match the working mode, and working bytes equal the
evidence blobs. Prepare uses the installed official config parser to accept only
missing/empty `hooks.after_archive`; non-empty, ambiguous, unreadable, invalid,
or symlinked config fails before side effects and no hook command is executed.
The archive root/month/final lexical ancestor preflight is repeated before these
move checks and before `task.py archive`; it never follows a symlink target.

If the live month changes while the task remains active, same-entry dry-run may
replace only an exact old evidence plan with a new-month digest. Formal appends
a plan/readiness-only evidence commit whose `git.evidence_parent_head` binds the
previous evidence commit, reuses the existing draft/verifier facts, and
rechecks the month before move. It does not rewrite history or migrate a moved
archive directory.

After current `HEAD` is the exact archive commit, every archived reentry reads
the immutable plan from that commit blob, including normal archived tasks that
still retain context. It validates Git parent/path/tree/blob lineage instead of archived
working-tree layout or dirty state. Missing or tampered local archived files do
not block pushing that exact commit when remote is behind, verifying
local/remote/PR HEAD, or retrying `gh pr ready`; no task artifact may be built
or rewritten. Exact recovery reads the immutable archive commit's
`finish-summary.json` blob, not the archived working tree, to recover the
original PR number/URL and verify its deterministic bytes/digest against the
plan template. This narrow runtime-facts check does not invoke the general
finish-summary artifact validator. The original PR must remain the unique open
repo/head/base candidate; missing, closed, or same-branch replacement PRs fail
closed. A plan-only archived directory is resolvable only through
`trellis-finish-work`; ordinary task commands still require `task.json`.
Final projection, incomplete recovery, and exact recovery use one strict PR URL
parser. GitHub owner/repository comparison is case-insensitive, consistent with
remote repository identity, while canonical output preserves the exact valid
remote casing (for example `microsoft/PowerToys`). Transport, host, path shape,
positive number, and absence of query/fragment remain strict; a different
repository never matches.
Plan-only recovery uses the same committed authority plus a dedicated boundary,
not an unconditional workspace-boundary skip. Before
GitHub access or committed recovery it must match the Git toplevel,
configured/effective repo, current head branch, available base ref, current
HEAD transaction, expected plan digest, task identity, and exact active/archive
locator relationship. All other discovery and command paths retain the normal
`task.json` and worktree-mode `task-start-context.json` requirements.
The finish entry validates its raw locator before ordinary resolution: only a
basename, exact former active locator, or exact archive locator is accepted,
and path-like input receives lexical repo/archive containment plus
component-wise `lstat` through the final directory before any fallback.
Basename input performs the same raw preflight for `<repo>/<basename>`, the
active task candidate, the archive root, and archive candidates in ordinary
resolver order. Each direct or archive candidate first retains only raw
`symlink_component` evidence, then applies the ordinary resolver's exact
follow-symlink `directory + task.json` predicate. A matching alias fails closed,
while an unmatched alias continues to the next candidate. This rejects
internal/external, relative/absolute, ancestor/final, multilevel, dangling,
and loop aliases before raw evidence is discarded. The ordinary resolver then
keeps explicit `task.json`, active task, and normal archived `task.json`
precedence. Only its not-found result enables plan-only recovery. An exact
archive locator selects that candidate; basename/former-active fallback
requires one unique archive
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
`trellis-finish-work` accepts exactly one reviewed body source: `--body-file`
must point directly to the current task-local `pr-body.md`. `--body-artifact`,
external same-content files, generated body fallbacks, and readiness-relative
`body_file` resolution are rejected and do not participate in closeout.
`pr-body.md` is task metadata and is fully validated in the active task before
`finish-work` performs the official archive move. Post-archive ready/recovery
hashes the remote PR body against the immutable plan and does not reopen the
task-local body. `trellis-finish-work` validates objective structure, forbidden
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
