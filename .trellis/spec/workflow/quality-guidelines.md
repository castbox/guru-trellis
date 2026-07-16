# Workflow Quality Guidelines

Finish-work quality evidence must distinguish the reviewed content HEAD, the
pre-draft evidence HEAD, and the final archive metadata HEAD. A dry-run pass is
valid only when formal execution rebuilds the same canonical plan digest.
Successful closeout has one final summary, one archive metadata commit, no
post-archive artifact rewrite, a clean worktree, matching local/remote/PR HEAD,
and a non-draft PR. Any unverified stage must be reported explicitly.

## Source-Backed Changes

Every workflow behavior change should update the canonical source and the
surfaces that expose it:

- reusable workflow: `trellis/workflows/guru-team/workflow.md`
- dogfooded active workflow when needed: `.trellis/workflow.md`
- preset overlay entries under `trellis/presets/guru-team/overlays/`
- README docs for installation, upgrade, and daily entrypoints
- companion scripts and schemas when behavior is executable

For `no_task` file-changing behavior, the canonical workflow must state the
default Phase 0 intake/preflight path and the only allowed current-checkout
direct-edit override: explicit user approval to skip GitHub issue, Trellis
task, worktree, and branch for that turn. Do not express that decision as an
AI-internal convenience path.

When Guru Team overlay is enabled, issue-backed, task-like, or file-changing
`no_task` prompts must name both entry commands:

- `.trellis/guru-team/scripts/bash/check-env.sh --json`
- `.trellis/guru-team/scripts/bash/prepare-task.sh --json`

Phase 1.0 must not leave bare `task.py create` as the apparent source-checkout
path for `workspace_mode: worktree`; it should point to `prepare-task
--create-worktree --create-task` or an equivalent controlled Guru Team executor
after handoff review and user approval.

Search before editing a phrase, command, marker, or config key:

```bash
rg "review-branch|finding|observation|followup-candidate|最终放行审查代理|finish-work|publish-pr|issue-scope-ledger|middle_platform_knowledge|guru-team-overlay"
rg "wait-timeout|progress-observed|continue-waiting|supersedes_agent_id|default at least 5 minutes|stale_after_unanswered_status_request|agent-progress.jsonl|long-command wrapper|periodic heartbeat"
```

## Required Checks

Use these checks before committing workflow or preset changes:

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate <task-dir>
trellis/workflows/guru-team/scripts/bash/check-commit-messages.sh --json --task <task-dir>
trellis/workflows/guru-team/scripts/bash/check-commit-messages.sh --json --candidate-artifact <task-commit-plan>
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

Add targeted script invocations when changing phase parsing, intake, review,
finish, publish, installer behavior, or source-repo dogfood overlay sync.
For `guru-discover-change-context`, tests must cover mode-precondition parity,
stale-before-semantic-read ordering, exact/token score permutations, invalid
isolation, deterministic sort/limit/projection, zero and 1-3 candidate paths,
mem insufficiency gate, pre-task zero-write, same-snapshot task-local record,
ordinary refresh stale-code/superseded-digest re-entry, task target trackability
through repository `.gitignore`, `.git/info/exclude`, and `core.excludesFile`,
duplicate candidate canonical fact digest plus identity/URL/repo/number binding
from one search result, the bidirectional `blocked` exit/Gate matrix, all typed
exits, source/installed distribution and clean
throwaway update/reapply. Any reader of index siblings, workspace/runtime,
repo-level history cache, or transitional legacy overlay payload fails.
For `guru-clarify-requirements`, tests must cover workflow/standalone
precondition parity; initial issue, proposed draft, active-task scope change,
and standalone entry kinds; repository-answerable evidence before user
questions, including rejection of `answered` without evidence;
one-question and atomic-group rounds; partial/refused answers, empty lifecycle,
close-before-open and reopen rejection;
comment/body/draft/new-task/active-task actions; exact action and proposal
confirmation; generic-confirmation rejection; optional-mechanism removal or
replacement; active-task ledger/planning/stale-gate/re-entry bindings; all five
typed exits and unique consumers; pre-task zero-write; live mutation freshness;
caller-aware clear resume targets; confirmed payload/mutation/live body equality;
and source/installed/discovery/throwaway update-reapply distribution. Static
and runtime tests must also prove the package/runtime contain no GitHub write or
issue-create executor and that recorder/checker do not generate semantic
decisions.
When changing Branch Review report generation or gate validation, add or update
tests that reject obvious English template headings in task-local `review.md`
and `reviews/*.md`, including `Review Rounds`, `Findings Lifecycle`,
`Evidence Handoff`, `Deployment / safety impact`, and `Follow-up Candidates`.
This validator is objective template-heading detection only; it must not judge
whether the Chinese review narrative is semantically sufficient.
When changing planning approval behavior, also run
`.trellis/guru-team/scripts/bash/check-planning-approval.sh --json --task <task-dir>`
against a current `schema_version=1.2` artifact with passed
`ambiguity_review` evidence. Include unit tests for the v2 controlled-term
list, fixed `scan_scope`, `hits[]`, `unchecked_normative_hits[]`,
unclassified-hit blocking, `contract_violation` blocking, allowed
classification reasons, rescanning mismatch failures, missing/non-passed
ambiguity review, stale or old-source approval failure, old `schema_version=1.1`
failure, and a regression where current HEAD / dirty-path drift does not block
while `prd.md`, `design.md`, and `implement.md` content digests still match.
When changing workspace boundary behavior, also run
`.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task
<task-dir>` from the selected task worktree and add regression tests for wrong
cwd, worktree mode without current handoff, source checkout same-task artifacts, wrong `--review-report`,
`--agent-assignment`, `--review-round-report`, `--checked-artifact`,
planner-only prepare no-write behavior, and controlled `create_task` cwd.

When changing PR publish behavior, include tests or dry-runs for both a blocked
low-information body and an accepted reviewer-readable body. The accepted body
must contain concrete `变更摘要`, `影响范围`, `验证结果`, `Review Gate`,
`Issue 关闭范围`, `安全说明`, and `Docs SSOT` / `文档同步` sections. The Docs
SSOT check remains objective section/key presence only; the AI readiness review
owns whether the strategy, durable docs update/no-update reason, merged delta,
task-history-only content, and follow-up/limitation are true and sufficient.
The blocked case should cover phrases such as `当前 Trellis task`,
`已提交实现与文档更新`, or `详见 artifact`, plus a missing Docs SSOT section.
When changing commit, finish, publish, or merge behavior, add tests for the
Chinese Conventional Commits contract: reject GitHub default merge subjects,
Chinese PR-title-as-subject squash messages, issue ids before the prefix or in
scope, missing issue ids, and English `Update ...` subjects; accept issue-bearing
work/metadata subjects and `chore(merge)` subjects; verify work body fixed
sections plus `Refs`, empty metadata body, fixed merge body, finish metadata
subject, and publish dry-run/formal `merge_commit` payloads.

Transactional finish tests must inject failure at prepare, reviewed-content
push, verifier, evidence commit, evidence push, draft create/reuse, final
projection, archive move, archive commit, archive push, remote/PR HEAD check,
and draft-to-ready. Every case asserts active/archive locator and task status,
PR none/draft/ready state, local/remote/PR HEAD, dirty and staged path sets, and
the one legal next transition. Include regressions for the 2026-07-03
post-archive identity failure, 2026-07-04 dry-run/archive drift, and issue #100
pending marketplace evidence. Recovery tests must reject partial move subsets,
wrong evidence/archive parents, stale task-relative verifier digests, and final
summary bytes outside the immutable sentinel template.

When changing user-facing workflow command examples, especially closeout or
publish examples, add regression coverage or explicit grep checks for both the
runtime entrypoints and public docs (`README.md`, workflow README, preset README,
and durable requirement docs when present). A command example can be correct in
overlays but still mislead users if a README keeps the older copy.

When changing sub-agent liveness, assignment, status request, stale assessment,
or replacement behavior, add tests or explicit grep checks that new active
surfaces use `record-subagent-liveness-event.sh`,
`check-subagent-liveness.sh`, `progress_scan_interval=120s`,
`max_progress_silence=180s`, structured `predecessor_event_id`,
`replacement_reason`, `termination_reason`, and completed-only recovery gates.
The old `record-agent-assignment.sh --status-event`, `wait-timeout`,
`progress-observed`, `continue-waiting`, `supersedes_agent_id`,
periodic heartbeat, daemon/sidecar/long-command wrapper, and
`agent-progress.jsonl` contracts must not appear as active workflow paths.
Schema 1.2 correction/recovery tests must cover a positive corrected ledger and
reject unknown targets, duplicate correction/link ids or targets, cycles or
backward links, cross-agent links, immutable target digest tampering,
invalidated pass evidence, and a link whose replacement chain never reaches
`completed`.

## Review Focus

Before Branch Review Gate, obtain an independent Agent review of the full branch
diff from the task's intake base branch, then record the result with
`review-branch.sh --review-source independent-agent`. Main-session self-review
cannot pass the gate. Include:

- marketplace index and docs
- workflow and dogfood copy
- Phase 1 `Docs SSOT Plan` contract: docs state, evidence paths, strategy,
  affected durable docs or checked no-update paths, task artifact deltas, and
  merge/repair/follow-up checkpoint when required
- Phase 2 consumption of that plan: implementation handoff records strategy,
  docs sync result, task delta merge / task-history-only content, no-update or
  follow-up limits, and durable-docs versus task-delta inputs; `trellis-check`
  verifies durable docs / task artifacts / code / test consistency by strategy
- Phase 3 verification of that plan: final review checks the approved plan,
  implementation handoff, `phase2-check.json`, durable docs, task artifacts,
  code/test/schema/config/script/preset/overlay changes, and confirms Docs SSOT
  reconciliation already happened; it must record any current-scope
  inconsistency as a finding and must not perform the first docs merge
- companion scripts
- schemas and config templates
- preset installer and overlays
- task work commit contract: mandatory `guru-create-task-commit` invocation,
  fresh task/issue/Phase 2/HEAD/snapshot binding, exhaustive single-category
  path review, exact staging, shared-parser candidate validation, raw message
  bytes, postconditions, unrelated preservation, hook mutation and fresh
  sequence on finding-fix re-entry; real regressions must prove active Git
  operation/sequencer state is preserved and blocked, and gitlink A/B/C changes,
  uninitialized/dirty/ambiguous boundaries are fail closed; the gitlink race
  regression must switch B to C after executor entry validation but before exact
  staging, prove the candidate/HEAD/operation state is preserved, and prove C
  is absent from both the index and commit; ordinary tracked, symlink, delete,
  delete/add rename, multiple-path, candidate-self and entry-index A/worktree B
  races must prove the same artifact authority. A real repository configured
  with `status.renames=copies` must prove that a clean copy source is not staged,
  and that an independently dirty/staged source classified as
  `unrelated-preserved` blocks or remains byte-for-byte/index-identical without
  entering the commit; the test must still fail if copy and rename relation
  handling is collapsed. Partial cache writes, rejecting
  or mutating hooks, operation drift, candidate publication failure, candidate
  writer contention, success-window concurrent `git add`, index publication
  failure and concurrent ref update must preserve transaction-owned preimages
  or third-party state without overwrite. Publication regressions must prove
  the real `index.lock` remains a sentinel while an independent final-index
  temporary is published, so real `git add` is still blocked. A normal-return
  candidate C writer injected at final-index publication must be detected by
  the later final candidate identity read, roll back owned ref/index and
  preserve C. A writer injected immediately after that successful read must be
  preserved as a later operation while the executor remains committed. The
  positive path proves guarded ref, commit tree, live index and candidate
  result agree at that final identity-read linearization point, returned commit
  blob/result digest evidence is exact, cleanup leaks no guard/temp, and no
  later fallible success branch exists
- commit message contract: work commit subject/body, Trellis metadata commit
  subject with empty body, `Refs` in commit messages, PR body-only close keywords,
  and publish/merge payload command that avoids GitHub's default merge subject
- Trellis task artifacts
- generated or installed-copy expectations
- Phase 0 handoff/preflight evidence, or explicit no-task direct-edit override
  evidence when the branch intentionally skipped issue/task/worktree/branch
- task artifact write location: `review.md`, `review-gate.json`, and similar
  files must be written under the task worktree derived from the current
  checkout, `.trellis/.runtime/guru-team/**`, `git worktree list`, and portable
  task-start-context identifiers; the committed context must not provide or be
  treated as an absolute `workspace_path`. When a manual editing tool has no explicit working
  directory, use a worktree-local absolute path
- Branch Review raw reports `reviews/*.md` and final rollup `review.md` must be
  Chinese human-readable task artifacts: Chinese headings, Chinese labels,
  Chinese findings/observations/follow-up candidates, Chinese deployment /
  safety and Docs SSOT judgments, and Chinese conclusion, with literal tokens
  kept as-is only where required.
- PR body readiness must include reviewer-readable Docs SSOT / 文档同步 result
  text: plan strategy, durable docs updated or no-update reason, merged task
  deltas, task-history-only content, and follow-up/current PR limitation.
- deployment asset impact

For `Docs SSOT Plan` changes, check that the contract is expressed in
Markdown workflow / docs / specs / overlays and remains repo-neutral. Do not
move semantic docs sufficiency, stale-docs, or strategy selection judgment into
Python or shell.

## Anti-Patterns

- Adding project-private business policy to the reusable `guru-team` workflow.
- Making shell scripts detect AI runtime capabilities such as MCP availability.
  Treat those as AI runtime/tool capabilities and express the decision in
  workflow or prompt text.
- Relying on chat memory for issue close scope, base branch, or reviewed head.
- Treating "small fix" as permission to modify the current checkout under
  `no_task` without Phase 0 evidence or explicit direct-edit override evidence.
- Writing task review artifacts into the source checkout because a manual edit
  used a relative path while the active task lives in a separate worktree.
- Leaving `.new` or `.bak` installer outputs unresolved in committed changes.
- Committing local identity files, `.env`, tokens, signed URLs, or private
  provider output.
