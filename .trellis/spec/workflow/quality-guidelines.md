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

Phase 1.0 must not leave bare `task.py create` or legacy `prepare-task`
mutation flags as an active source-checkout path. It mandatory invokes
`guru-create-task-workspace`; only its checker-validated `created` exit enters
planning.

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

For versioned public Skill I/O, the test matrix must keep the exact 1.2 schema
bytes/identity as a regression fixture while validating independent interface
1.3 and registry 1.1 schemas. One mixed test-only registry must contain 1.2
`legacy`, structured semantic 1.3, and scalar deterministic 1.3 packages in the
same run. Tests cover discriminator/`oneOf`, every per-exit schema/example,
every output field's direct consumer use, Skill/workflow/stop consumers,
self-reentry, `direct|select|rename|normalize` projection, and public/private
schema-id and schema-path disjointness. Skill consumers prove target-owned
`skill_input`, exact active-registry target interface path, and exact target
interface identity. Structured workflow and stop consumers prove both
interface-schema and runtime enforcement of canonical `consumers/workflow/`
and `consumers/stop/` owner roots; negative cases cover a
producer output locator, the other consumer root, and non-normalized path
spellings. Both canonical structured roots pass, while the zero-payload stop
retains its schema-free form. Non-`direct` projections and `direct` projections into
`scalar_cli` prove required-source totality and all-valid-output compatibility,
including a normalizer counterexample that passes the producer schema but fails after
normalization when the proof constraint is removed. The stop case proves
`zero_payload` with only routing
`exit_id` and an empty `select`; negative cases reject extra stop payload and
empty `select` for non-zero consumers. Aggregate branches bind the exact
ordered profile schema references, discriminator fields are required constants,
and scalar examples prove ordered flags, declared value types, binding order,
and public-input/invocation argv equality.

Source validation must execute representative package wrappers and revalidate
their single typed-exit stdout. Negative cases cover missing exit schema or
example, missing or non-constant exit identity, unknown public I/O fields,
nullable mega-output authoring, unconsumed field, a stale same-id Skill
interface locator, a direct consumer schema or scalar domain that is narrower
than its producer schema, duplicate projection targets, missing
consumer input, private-field projection, unknown/semantic projection
operation, runtime-source import, comment/dead-code/local-output wrapper
impersonation, 1.2/1.3 state mismatch, new
non-allowlisted production legacy entry, and reserved/planned package install.
Schema mutation cases must prove the recursive Draft 2020-12-compatible closed
subset rejects an otherwise valid but unsupported `patternProperties`, a nested
unsupported keyword, a malformed supported-keyword value, a boolean schema
node, a nested `$id` resource boundary, an unsafe/unresolved/remote/recursive
ref, an invalid regex, and an unsupported format. Existing
`allOf`/`if`/`then`, `oneOf`, nested `properties`, and canonical package-local
profile refs remain passing coverage; an accepted keyword must never be silently
ignored by instance validation.
Portable-pattern tests must exercise the exact grammar from
`skill-package-contract.md`, including unanchored and anchored literals,
capturing/non-capturing groups, alternation, negative lookahead, character
classes/ranges/negation, every quantifier form, syntax/control/ASCII `\\u`
escapes, and `\\s|\\S`. Grammar negatives must reject Python-only groups and
anchors, `\\d|\\D|\\w|\\W`, Unicode properties or non-ASCII source/escape
values, unsupported assertions/groups, backreferences, invalid classes, and
malformed, descending, overlong, lazy, possessive, misplaced, or repeated
quantifiers. Instance regressions must prove strict `$` rejection of a trailing
newline, dot rejection of all four ECMA line terminators while accepting one
astral code point in Unicode mode, and the exact ECMA whitespace domain,
including acceptance of `U+00A0` and rejection of Python-only `U+001C` and
`U+0085`. Astral regressions must separately cover zero-width matches before,
inside, and after a surrogate pair; negative lookahead, anchors, alternation,
empty alternatives, and nullable quantifiers at those positions; and the rule
that `.`, `\\S`, and negated classes consume a valid pair as one code point and
cannot start at its interior low surrogate. Isolated-surrogate regressions must
cover high and low surrogates standalone and on both sides of a BMP code unit,
plus `.`, `\\S`, negated classes, anchors, quantifiers, nullable paths, and
backtracking. The generated value set must include the seven surrogate edge
values: isolated high and low alone, each before and after a BMP value, and one
valid pair. Its JSON transport must preserve isolated surrogates as escapes.
A deterministic generated set of accepted patterns must be compared across
astral, isolated-surrogate, BMP, line-terminator, and mixed values. The full
legal matching matrix must be compared with an independent Node
`new RegExp(pattern, "u").test(value)` run; a Python-only expected-value table
is insufficient.
Strict-JSON cases must cover `NaN`, `Infinity`, `-Infinity`, and numeric overflow
at static schema/example, package-local ref, workflow marker, invocation stdout,
in-memory schema/instance, and public serialization boundaries. Supported-format
cases must accept RFC 3339 lowercase `t`/`z`, valid calendar/offset values and a
valid leap-second boundary, including the year `0000` domain, while rejecting
invalid dates, clocks, offsets, and leap-second positions; RFC 3986 URI cases
must cover ordinary hierarchical and opaque schemes, case-insensitive IPvFuture
`v`, malformed/missing schemes, whitespace/control characters, percent
encoding, authority, and ports.
Discovery tests cover stable help, legacy/minimal variants, unknown skill,
version mismatch, missing asset, installed drift, and stable
`code`/`field_path`/`remediation` errors.

Distribution tests prove the new interface schema and executable discovery
wrapper are present in canonical, installed, and selected-platform roots;
production registry/extension inventories contain nine legacy ids and no
fixture ids/schema ids. Fresh throwaway install and the post-`trellis update`
workflow/preset reapply phase each run source/installed validation, legacy
discovery smoke, mixed fixture invocation tests, and a final recursive zero
`.new`/`.bak` scan.
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
confirmation; five-class active-task task-update rejection when the proposal
is confirmed but `confirmed_actions[]` is empty, the task action is absent, or
the confirmation action digest is null/wrong; normal combined proposal/action
confirmation re-entry; generic-confirmation rejection; optional-mechanism removal or
replacement; active-task ledger/planning/stale-gate/re-entry bindings; all five
typed exits and unique consumers; pre-task zero-write; live mutation freshness;
caller-aware clear resume targets; confirmed payload/mutation/live body equality;
unconfirmed related/followup/new-task/out-of-scope rejection; exact structured
ledger decision-trail and live GitHub authority binding; mutation-only
`refresh_context`; fresh re-entry before exact interrupted progression; active
`new_task` trail preservation with side-effect-free draft-only continuation;
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
against a current `guru-planning-approval-2.0` artifact bound to
checker-validated `guru-review-contract-wording:planning_artifacts:pass`
evidence. Package/runtime tests must cover workflow/standalone nine-precondition
parity; all four provenance classes; duplicate/missing/unknown/stale statement
entries; implementation-choice alternatives, selection and no-scope-expansion
flags; every unusual-scenario disposition; dedicated proposal confirmation
versus ordinary post-planning confirmation; refusal and clarification routes;
the four Gate/exit/consumer combinations; unknown/multiple/unmapped exits;
Docs SSOT, authority, wording, planning, base/HEAD invocation and artifact
digest freshness; active 1.2 bootstrap rejection and v2 re-recording; and the
regression where post-activation implementation HEAD/dirty drift does not block
while planning/authority/wording content remains current. Include a fixture in
which a non-required lock/atomic mechanism is removed or replaced and reviewed
again, without manufacturing a scope expansion. Static tests must prove the
runtime does not generate provenance, choice necessity, unusual-scenario
necessity, confirmation sufficiency, semantic pass, or route judgment.
For `approved_scope_expansion`, production recorder/checker tests must cover a
normal planning-artifact locator source, a canonical unusual-candidate source,
both sources coexisting without digest confusion, workflow/standalone parity,
and a non-approved exit carrying an otherwise complete binding. Negative cases
must reject caller-only/wrong proposal digest, stale or invalid content locator,
missing/wrong candidate, generic/wrong-kind or digest-mismatched confirmation,
unknown/stale authority digest, authority absent from entry refs, and an
authority-to-proposal digest mismatch. The checker must reread content and
authority facts rather than accepting recorder-time shape alone.
Run source and installed package validation, dogfood drift, clean throwaway
install, and `trellis update` plus preset reapply because the package, runtime
commands, schema, and four discovery roots are one distribution contract.
The throwaway fresh-install and after-update/reapply phases must each discover
the installed package and execute a real v2 recorder/checker path.
For `guru-review-change-request`, tests must cover workflow/standalone
precondition parity; all three target variants; current context/clarity/wording
projection and hash linkage; each prerequisite missing, stale, wrong-exit, or
target/content mismatched; all ten ordered dimensions; finding/reference/hash
closure; five exits and exact consumers; active #112 exact transition;
unknown/multiple/unmapped exit rejection; empty or incomplete AI Gate;
scanner/checker success without a semantic Gate; non-ready failed-dimension,
blocking-finding, affected-evidence requirements; facts digest freshness;
stdout-only zero-write behavior; source/installed/schema/runtime/platform
distribution; and clean throwaway update/workflow/preset reapply with zero
cache/sidecar residue. Tests must prove scripts preserve the AI-authored route
and contain no readiness, finding, delivery-unit, history, duplicate, or
workspace-creation generator.
When changing workspace boundary behavior, also run
`.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task
<task-dir>` from the selected task worktree and add regression tests for wrong
cwd, worktree mode without current handoff, source checkout same-task artifacts, wrong `--review-report`,
`--agent-assignment`, `--review-round-report`, `--checked-artifact`,
planner-only prepare no-write behavior, and controlled `create_task` cwd.

For `guru-create-task-workspace`, tests must cover workflow/standalone
precondition parity; every missing/stale/wrong-exit/target-mismatched
prerequisite; open issue and reviewed-draft variants; mutually exclusive issue
and workspace/task confirmations; draft-created issue live binding plus exact
reviewed title/body/labels bytes without adapter trimming or newline insertion;
immediate `refresh_review`; zero branch/worktree/task writes in that invocation;
create success followed by immediate reread failure and same-plan retry with
exactly one remote issue; exact recovery candidate cardinality 0/1/>1;
checker-passed created-issue result carryover into a complete Intake rerun;
missing/partial carryover, result/binding digest drift, reviewed draft or
creation confirmation mismatch, and fresh live existing-issue identity or null
`issue_binding` mismatch;
target/disposition change and cancellation zero-write results; explicit, one
issue assignee, zero issue assignees/current-login, multiple/user-choice, and
unresolved assignee cases; isolated official `common.task_store.cmd_create`
adapter with a call-scoped null developer accessor; exact
`task.json.creator=task.json.assignee=reviewed login`; preservation of existing
identity bytes; exact object reuse/conflict blocking; four canonical task-local
artifacts; additive
task-start-context 1.0 compatibility; ignored runtime-only mappings; source and
target with no `.trellis/.developer` or `.trellis/workspace/**`; preservation
of existing official identity/journal bytes; all four typed exits and unique
consumers; source/installed/platform distribution; legacy prepare mutation
flags zero-write migration; and clean throwaway update/reapply.

The route tests must prove a confirmed plan cannot be relabeled cancelled,
while refused confirmation, reroute Gate, and blocked Gate produce their exact
zero-write exits and checker-valid consumers. Public plan/result schema,
examples, and stdout must reject or omit absolute machine-local paths.

Mutation-boundary tests use a real remote whose base advances after the initial
checker-passed evidence while the local remote-tracking ref remains stale. They
prove the executor fetches/safely syncs, returns `refresh_review`, and creates
no issue, branch, worktree, task, artifact, or runtime mapping. The
unchanged-remote case still completes the reviewed mutation path.

The real A/B fixture must use one clean base, production
record/executor/checker, independent worktrees/tasks, task-local closeout and
archive, complete commits, then both A -> B and B -> A local merge orders. The
second merge in each order must have no Guru metadata conflict, tracked Guru
metadata path intersection must be empty, and neither diff may contain a fixed
handoff, `.trellis/workspace/**`, `.trellis/.developer`, shared tracked runtime,
index, or cache. It uses no remote PR or concurrent process and does not expand
into locks, TOCTOU, stress, cross-OS, hostile-input, or extra fault injection.

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

Phase 2 package regressions must cover source and installed package validation,
workflow/standalone precondition parity, missing/legacy/stale planning and
repository evidence, unchanged worker evidence isolation, scope-before-severity,
exact completed implementation/check role binding and complete worker-agent
coverage,
the four scope dispositions, all ten adequacy dimensions, blocking/non-blocking
unverified items, four exit/consumer invariants, planning discriminator closure,
finding-fix full rerun, failed/unfinished/stale/replacement/completed recovery,
dirty/reviewed-path/post-commit freshness, legacy migration, and the single
artifact owner. Distribution validation must compare canonical/shared/Codex/
Claude/Cursor package bytes, preserve the frozen 43-entry upstream inventory,
run dogfood apply/drift and sidecar checks, and exercise clean marketplace init,
preview/switch, preset apply, installed invocation, `trellis update --force`,
and workflow/preset reapply.

Phase 2 regression coverage must also prove that empty provenance/handoff/docs/
reviewed-path/command evidence, empty adequacy references, missing current or
scope-change trigger references, unknown/incomplete evidence-source closure,
and every incorrect recorder-derived semantic digest fail closed. A real Git
post-commit fixture must include `agent-assignment.json` in implementation
handoff and distinguish legal review assignment/status/completed/round metadata
tail from implementation/check/recovery drift.

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

## Skill Eval Quality Matrix

+ Skill eval tests use the mixed representative Interface 1.2/1.3 fixture and
  execute real public wrappers.
+ Negative coverage includes unknown/null fields, duplicate or non-string ids,
  profile/exit drift, unsafe/missing/symlink fixtures, unknown assertions,
  canonical legacy `expectations`, missing external semantic grading, feedback
  overriding deterministic failure, one-sided/floating comparison, internal
  run root, platform corpus drift, and malformed public output.
+ Adapter integration injects fake shared/Codex/Claude/Cursor executables to
  exercise the real descriptor-selected adapter wrappers, prove four distinct
  native argv shapes, exact Skill/prompt/staged-file context, public output and
  trace collection, and byte-identical corpus without local CLI assumptions;
  native absence separately returns `unsupported`. A fake adapter may not
  replace the four real wrappers in this integration test.
+ Four-platform comparison covers a repo current package and a repo-external
  byte-identical exact package with native commands available and no dispatcher
  override. Both sides pass through one runner-resolved private runtime target,
  while every native-visible request/context/projection/receipt/boundary remains
  free of that locator.
+ Exact comparison also covers valid sides with different declared wrapper
  paths and pre-execution closed failures for missing outputs, fixtures,
  Interface fields, or public assets. One invalid side must not execute the
  other side or escape through `KeyError`/`OSError`.
+ Adapter integration validates the repo-external native read/invocation
  receipt and rejects a native CLI that returns a schema-valid typed DTO without
  reading the Skill and invoking the public wrapper through the trace helper.
  Wrapper-source scanning or unconditional synthetic trace events cannot
  satisfy the three public-invocation trace invariants.
+ All four native envelopes receive only the public staged projection. Raw
  reads of projection-relative `evals/evals.json` and private runtime source
  must produce real filesystem denial evidence and `execution_error`; native
  request/context must contain no canonical package/corpus/private-runtime
  locator while the runner grades canonical corpus outside execution.
+ Fresh install and post-`trellis update` preset reapply rerun source/installed
  discovery and run smoke, selected-platform byte/mode checks, dogfood drift,
  and recursive zero `.new`/`.bak` scans.
+ A normal public invocation trace proves no eval corpus/descriptor/evidence or
  private runtime source enters ordinary Skill context.
