# Workflow Quality Guidelines

## GitHub Channel Regression Gate

Bounded static guards cover current canonical workflow, public Skill, shared
runtime, preset/platform, installed dogfood and public README surfaces. They
reject forbidden GitHub adapter/fallback wording, unbound high-level commands,
and incomplete REST repository endpoints while excluding historical task
archives and unrelated MCP capabilities.

Deterministic fixtures cover the six failure categories, invalid/empty/missing
fields, Issue/PR/comment/label/state/check/review/mergeability/Draft/Ready/
merge/workflow-run/post-merge paths, number/base/head/expected-SHA binding, and
the unchanged `git fetch|push|ls-remote` boundary. Distribution validation also
covers source/installed checks, preset initial/reapply, overlay drift and
sidecars, clean marketplace init/preview/switch, official update/upgrade, and
Codex/Claude/Cursor equality.

Task Commit hook regressions use executable hooks in real temporary Git
repositories, not mocked subprocess assertions. The matrix proves all four
standard commit hooks observe the reviewed parent, exact transaction
index/worktree and message file; pre-ref rejection, message rewrite, extra
tracked/untracked state, rename/delete, stage/unstage and exact-path mutation do
not advance the live branch; post-commit and post-publication failures report a
created commit identity and retain recovery inputs. Tests compare semantic
`mode/blob/stage/path` index entries so stat-cache-only refresh is non-semantic.
The positive matrix includes a parent-tree gitlink plus unrelated
staged/unstaged/untracked state, and both positive and negative paths assert
that transaction worktree registrations and isolated indexes are cleaned up.

Finish-work quality evidence must distinguish the reviewed-content identity and
its `branch_review_commit` anchor from the current metadata tail and the final
archive metadata commit. A dry-run pass is valid only when formal execution
rebuilds the same canonical plan digest.
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

For `no_task` file-changing behavior, the canonical workflow must invoke
`guru-select-workflow-mode` before normal Intake. Explicit task-free intent
selects the bounded current-checkout route directly. Without explicit intent,
the AI automatically selects high-confidence bounded low-risk work, asks once
only when evidence is insufficient, and selects standard Intake for clearly
complex or high-risk work. Issue presence, file count, paths, and keywords are
not independent classifiers. Same-scope recovery reuses the selection. Scripts
must not classify intent.

When standard Intake is selected, the deterministic base and workspace helpers
remain:

- `.trellis/guru-team/scripts/bash/check-env.sh --json`
- compatibility-only `.trellis/guru-team/scripts/bash/prepare-task.sh --json`

Normal Phase 0 does not call `prepare-task`; an explicit diagnostic supplies
complete reviewed base provenance and blocks locally when it is missing.
Phase 1.0 must not leave bare `task.py create` or `prepare-task` mutation
flags as an active source-checkout path. It mandatory invokes
`guru-create-task-workspace`; only its checker-validated `created` exit enters
planning.

Search before editing a phrase, command, marker, or config key:

```bash
rg "review-branch|finding|observation|followup-candidate|最终放行审查代理|finish-work|issue-scope-ledger|middle_platform_knowledge|guru-team-overlay"
rg "wait-timeout|progress-observed|continue-waiting|supersedes_agent_id|default at least 5 minutes|stale_after_unanswered_status_request|agent-progress.jsonl|long-command wrapper|periodic heartbeat"
```

## Required Checks

Use these checks before committing workflow or preset changes:

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate <task-dir>
trellis/workflows/guru-team/scripts/bash/check-commit-messages.sh --json --task <task-dir>
trellis/workflows/guru-team/scripts/bash/check-commit-messages.sh --json --candidate-artifact <task-commit-plan>
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

Add targeted script invocations when changing phase parsing, intake, review,
finish, publish, installer behavior, or source-repo dogfood overlay sync.

For versioned public Skill I/O, the test matrix validates the current Interface
1.4/1.5 and registry 1.4 schemas. One mixed test-only registry contains
structured semantic 1.4 and scalar deterministic 1.4 packages in the same run.
Tests cover discriminator/`oneOf`, every per-exit schema/example,
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

For current Intake activation, run the Interface 1.4 matrix over the live
six-package/23-exit contract rather than only a representative fixture. Every
structurally distinct input profile/signature must have an
executable public invocation probe, every exit/profile must have a non-empty
current eval case binding, and all output fields must resolve to direct consumer
use pointers. Negative tests must reject missing/extra/duplicate/renamed/unknown
current-contract entries, any partially updated Intake graph, stale consumer
profiles,
unconsumed/private fields, unsupported projections, and wrapper-local logic.
Real public-invocation probes must also reject missing owner locators,
checker-failed owner results, and public-input/owner mode or fixed-profile
mismatches. They prove repo-relative caller input works, route selection comes
from the checker-passed owner result, workspace `created` cannot be serialized
from an example or unchecked executor result, and output examples are not read
as production serializer input. The live registry and current package graph are
the complete source, schema, example, eval, and fixture inventory.

Validate `production-current-v2` as the sole current planning/check/commit
manifest: exactly three packages, ten profiles, 11 exits, current output schema
ids, four authoring-seed edges, private artifact ids, examples, and eval case
bindings. No alternate production manifest, input projector, or fixture may be
present. Then validate the current package closure
at sixteen active Skills and 62 external exits, while the integrated business
workflow projection is 15 invokes, 60 exits, and 36 targets. Negative tests cover missing, extra,
duplicate, renamed, case-mismatched, unknown, or non-current entries; missing
profile/output/consumer/projection assets; private or unconsumed output fields;
invalid discriminator unions; absolute paths; and partial Intake/production
activation. Every manifest and declared asset must pass the same current-contract
validation.

Every production profile and exit executes the real package wrapper through
the shared adapter. The runner validates the actual exit schema before
comparing `expected_exit`; expected values never enter owner construction or
route selection. Commit `committed` evals validate the exact projection into
the active `guru-review-branch` package and dispatch Branch Review through that
closed loop. Existing
commit transaction tests remain mandatory because the new candidate builder is
not authorization to replace or weaken the executor.

The package graph contains nine target-owned `skill_input_authoring_seed`
handoffs. These edges have positive partition/projection probes and negative
overlap, overwrite, missing, extra, unknown, private-lookup,
runtime-semantic-reconstruction, and unsupported fifth-operation fixtures. Each positive
probe independently validates seed and authoring example keys, proves disjoint
union equals the complete target required set, performs a no-overwrite merge,
and validates the merged target input before invoking the real consumer wrapper.
No other edge may declare this consumer kind.

Scalar probes cover both explicit and omitted optional arguments. Omission is
accepted only for `required=false`, preserves declared order, and reaches the
same formal owner resolver; missing required, repeated, unknown, or out-of-order
flags fail. Clarification probes cover the active-task-only null-disposition to
`retained` projection plus initial/standalone null negative cases.

Fresh install and current-manifest update verification must each cover the normal
chain plus refresh/re-entry, stop, retarget, content-changed, issue-only
initial/recovery, and workspace/task initial/recovery families. After `trellis
update` and preset reapply, source, installed, workflow-marker, extension,
manifest, package corpus, and selected-platform byte identities must still
match; `.new`/`.bak` sidecars and mixed activation are blocking. Existing active
tasks re-enter through owner public profiles, while archive fixtures prove
archived artifact bytes are read-only.

Normal Agent transcript and eval trace assertions are separate evidence. Both
must show public-wrapper-only invocation, no Agent read/import of private runtime,
and no normal-package load of `evals/**`. Eval coverage uses the existing #147
schema, runner, grader policy, adapter protocol, and evidence contract unchanged.

Production semantic eval probes require an explicit repo-local owner-result
locator whose existing checker passes current facts. They assert that neither
adapter request nor native request contains `expected_exit`, that actual exit
selects the output schema, shared executes the packaged native runtime, Codex
uses a trusted Git root, Claude uses its supported non-interactive protocol,
and missing Cursor authentication returns `unsupported` without entering an
interactive session.

Source validation must execute representative package wrappers and revalidate
their single typed-exit stdout. Negative cases cover missing exit schema or
example, missing or non-constant exit identity, unknown public I/O fields,
nullable mega-output authoring, unconsumed field, a stale same-id Skill
interface locator, a direct consumer schema or scalar domain that is narrower
than its producer schema, duplicate projection targets, missing
consumer input, private-field projection, unknown/semantic projection
operation, runtime-source import, comment/dead-code/local-output wrapper
impersonation, invalid current interface identity, unexpected registry state,
and planned package install.
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
Discovery tests cover stable help, the current Interface 1.4 contract, unknown
skill, version mismatch, missing asset, installed drift, and stable
`code`/`field_path`/`remediation` errors.

Distribution tests prove the new interface schema and executable discovery
wrapper are present in canonical, installed, and selected-platform roots;
production registry/extension inventories contain the exact thirteen current
ids and no fixture ids/schema ids. Fresh throwaway install and the post-`trellis update`
workflow/preset reapply phase each run source/installed validation, production
discovery smoke, current-only fixture invocation tests, and a final recursive zero
`.new`/`.bak` scan.
For `guru-discover-change-context`, tests must cover mode-precondition parity,
stale-before-semantic-read ordering, exact/token score permutations, invalid
isolation, deterministic sort/limit/projection, zero and 1-3 candidate paths,
mem insufficiency gate, stdin/stdout record/check/invoke, pre-task and
standalone zero-write, exact minimal DTO projection, real Git ref freshness,
base-stale short-circuit before semantic reads, unknown current owner-state
rejection, clean active-task normal routing with zero checkpoint, dirty
active-task same-owner recovery, successful consume-and-clean,
stale checkpoint deletion, unsafe cleanup rejection, and terminal zero residue,
duplicate candidate canonical fact digest plus identity/URL/repo/number binding
from one search result, the bidirectional `blocked` exit/Gate matrix, all typed
exits, source/installed distribution and clean
throwaway update/reapply. Any reader of index siblings, workspace/runtime,
repo-level history cache, or any file outside the current three-overlay set fails.
For `guru-clarify-requirements`, tests must cover workflow/standalone
precondition parity; initial issue, proposed draft, active-task scope change,
and standalone entry kinds; repository-answerable evidence before user
questions, including rejection of `answered` without evidence;
one-question and atomic-group rounds; partial/refused answers, empty lifecycle,
close-before-open and reopen rejection;
comment/body/draft/new-task/select-existing/reopen/active-task actions; current-
dialogue scope and side-effect choices; static/runtime rejection of any
authorization state, text, ref, timestamp, digest, or process in result, ledger,
checkpoint, runtime, archive, schema, example, or public DTO; rejection of an
ambiguous continuation when multiple actions or proposals remain (while any
clear affirmative response accepts one fully displayed unchanged action);
optional-mechanism removal or
replacement; active-task scope-only Ledger plus owner-result decision trail and live planning/context/action/re-entry bindings; all five
scope dispositions; all six typed exits including `retarget_context` and unique
consumers; exact current schema 2.0 rejection/acceptance paths; pre-task
zero-write; live mutation freshness; caller-aware clear resume targets;
payload/mutation/live body equality; unfinalized related/followup/new-task/
out-of-scope rejection; exact scope-only Ledger validation, owner-result trail,
and live GitHub authority binding; unknown current-shape field rejection; mutation-only
`refresh_context`; fresh re-entry before exact interrupted progression; active
`new_task` scope classification with side-effect-free draft-only continuation;
and source/installed/discovery/throwaway update-reapply distribution. Static
and runtime tests must also prove the package/runtime contain no GitHub write or
issue-create executor and that recorder/checker do not generate semantic
decisions.
When changing Branch Review recording or gate validation, add or update tests
that prove the semantic owner records only one compact owner-private checkpoint
under ignored runtime. Publication consumes the minimal typed exit and live
facts, not that checkpoint. The Branch Review public wrapper must delete its own
checkpoint only after the selected typed output passes schema validation; tests
must prove Publication succeeds without it. Routine independent-agent assignment, liveness,
per-round raw reports, final rollups, reviewer metadata, and Git-derived facts
must not be persisted. Tracked `review-gate.json`, `agent-assignment.json`,
`reviews/*.md`, and `review.md` are invalid current owner inputs; no recorder,
wrapper, platform entry, or test fixture may generate or consume them.
When changing planning approval behavior, also run
`.trellis/guru-team/scripts/bash/check-planning-approval.sh --json --task <task-dir>`
against a current ignored-runtime `guru-planning-approval-3.0` checkpoint.
Package/runtime tests must cover workflow/standalone eight-precondition parity,
all three entry profiles, all four semantic/exit/consumer combinations,
unknown/multiple/unmapped exits, missing or empty planning files, task/planning
locator mismatch, duplicate or empty authority refs, Docs SSOT closure, and
current schema 3.0 rejection of every other input shape. Static tests must prove that public input,
private evidence, public output, and archive state contain no authorization,
authorization digest, repository snapshot, file metadata, raw review,
assignment, liveness, or handoff fields. Semantic delta tests must distinguish
equivalent formatting/link/derived-text changes from requirement, authority,
scope, design, acceptance, behavior, or verification changes without replaying
unaffected owners. Recorder/checker tests must prove they preserve an existing
AI result and never generate findings, sufficiency, unusual-scenario meaning,
authorization, semantic pass, or route judgment. Planning and Phase 2 tests must
also prove that same-path content drift invalidates the current owner checkpoint
through exactly one owner-private composite token, while that token never enters
public DTOs or becomes authorization, semantic approval, or whole-chain
authority. The Planning wrapper deletes its checkpoint only after checker and
output-schema success. The Phase 2 wrapper retains only a valid `passed`
checkpoint for Task Commit and deletes every other valid exit checkpoint; Task
Commit tests must prove candidate construction and execution reread it, failures
retain it, and successful publication or recovery deletes it.
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
cwd, worktree mode without a matching `task.json`, ignored runtime mapping, and
live Git worktree identity, source checkout same-task artifacts, wrong private
gate/check checkpoint locators, planner-only prepare no-write behavior, and
controlled `create_task` cwd.

For `guru-create-task-workspace`, tests must cover workflow/standalone
precondition parity; every missing/stale/wrong-exit/target-mismatched
prerequisite; open issue and reviewed-draft variants; mutually exclusive issue
and workspace/task dialogue-only confirmations; proof that refusal stops before
recorder/executor and that plan/result/runtime/public DTO contain no
authorization fields; draft-created issue live binding plus exact
reviewed title/body/labels bytes without adapter trimming or newline insertion;
immediate `refresh_review`; zero branch/worktree/task writes in that invocation;
create success followed by immediate reread failure and same-plan retry with
exactly one remote issue; exact recovery candidate cardinality 0/1/>1;
checker-passed created-issue result carryover into a complete Intake rerun;
missing/partial carryover, result/binding digest drift, reviewed draft or
created-issue identity mismatch, and fresh live existing-issue identity or null
`issue_binding` mismatch;
target/disposition change `refresh_review` and blocked zero-write results; explicit, one
issue assignee, zero issue assignees/current-login, multiple/user-choice, and
unresolved assignee cases; isolated official `common.task_store.cmd_create`
adapter with a call-scoped null developer accessor; exact
`task.json.creator=task.json.assignee=reviewed login`; preservation of existing
identity bytes; exact object reuse/conflict blocking; exactly one Guru-owned
tracked task-local artifact (`issue-scope-ledger.json`); task identity derived
only from current `task.json`, ignored runtime mappings, and live Git worktree
facts; source and target with no `.trellis/.developer` or
`.trellis/workspace/**`; preservation
of existing official identity/journal bytes; exactly three typed exits and unique
consumers; source/installed/platform distribution; removed prepare mutation
flags remaining zero-write; and clean throwaway update/reapply.

Route tests require `created`, `refresh_review`, or `blocked`; refusal has no
recorder/result/DTO route. Public plan/result schema, examples, and stdout must
reject authorization fields and absolute machine-local paths.

Mutation-boundary tests use a real remote whose base advances after the initial
checker-passed evidence while the local remote-tracking ref remains stale. They
prove the executor detects the advance with read-only `git ls-remote`, never
calls the base-sync executor, leaves the decision HEAD plus local and
remote-tracking refs unchanged, returns `refresh_review`, and creates no issue,
branch, worktree, task, artifact, or runtime mapping. The unchanged-remote case
still completes the reviewed mutation path.

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
push, verifier, draft create/reuse, final projection, archive move, archive
commit, archive push, remote/PR HEAD check, and draft-to-ready. Every case also
asserts that no separate pre-draft metadata commit/push occurs, plus active/archive locator and task status,
PR none/draft/ready state, local/remote/PR HEAD, dirty and staged path sets, and
the one legal next transition. Include regressions for the 2026-07-03
post-archive identity failure, 2026-07-04 dry-run/archive drift, and issue #100
pending marketplace evidence. Recovery tests must reject partial move subsets,
wrong transaction/archive parents, stale task-relative verifier digests, and final
summary bytes outside the immutable sentinel template.

When changing user-facing workflow command examples, especially closeout or
publish examples, add regression coverage or explicit grep checks for both the
runtime entrypoints and public docs (`README.md`, workflow README, preset README,
and durable requirement docs when present). A command example can be correct in
overlays but still mislead users if a README keeps the older copy.

When changing agent replacement behavior, add tests or explicit grep checks
that routine dispatch, completion, mapped exits, stale re-entry, and wait
timeouts create no assignment, liveness, status, progress, or handoff artifact.
Only a real unfinished agent followed by a replacement may use
`record-agent-recovery.sh` and `check-agent-recovery.sh`; the minimal ignored
checkpoint under `.trellis/.runtime/guru-team/agent-recovery/` records the task,
role, predecessor/replacement agents, HEADs, reasons, and handoff summary needed
by that recovery consumer. Tests must reject replacement without a matching
unfinished event and prove the checkpoint is never tracked or required after
the recovery closes. Assignment/liveness ledgers have no current reader,
recorder, checker, fixture, or re-entry route.

### Phase 0 Public Transition Gate

The six-package/23-exit Phase 0 graph requires one stateful clean-install
transcript in addition to package-local contract tests. The harness runs the
installed production wrappers and feeds each producer's actual stdout through
the declared projection into the next call-local envelope. It must not handwrite
an intermediate transition, import/read `guru_team_trellis.py`, create a hidden
owner/prerequisite locator, or compare `expected_exit` until the runtime has
validated and emitted the actual typed output.

The transcript covers the existing Open Issue happy path through real
workspace/task creation; reviewed draft creation and full refresh/re-entry;
duplicate retain and retarget; wording `content_changed`; readiness reroute and
ready; every structurally distinct stop/refresh/re-entry family; and explicit
base provenance followed by a compatibility prepare call with omitted base.
Negative cases change selected HEAD or authoritative content and prove stale
evidence is rejected. Before workspace creation, repository scans assert zero
owner-result, prerequisite, transition, task, workspace, and ignored-runtime
files.

Source validation, preset staging, and installed validation treat the six
packages, five transition schemas, call-local envelope schemas, consumer
projections, package runtimes, minimal shared kernel, registry/extension inventory, and activation
manifest as one versioned unit. Mixed old/new bytes, missing assets, or a
partially activated graph fail closed and preserve the prior complete
installation. Clean init, existing-workflow preview/switch, official `trellis
update`, preset reapply, dogfood synchronization, selected platform parity,
managed hash/mode validation, and recursive zero `.new`/`.bak` sidecars are all
required evidence; isolated wrapper success cannot substitute for these gates.

## Review Focus

Phase 2 package regressions must cover source and installed package validation,
workflow/standalone precondition parity, missing/stale planning and
repository evidence, scope-before-severity, the four scope dispositions, all
nine adequacy dimensions, blocking/non-blocking unverified items, four
exit/consumer invariants, planning discriminator closure, finding-fix full
rerun, exceptional unfinished/replacement recovery, dirty/reviewed-path and
post-commit freshness, the current schema 4.0 checkpoint, and the single compact
artifact owner. Routine implementation/check identity remains live semantic
context and must not become persisted assignment or liveness evidence.
Distribution validation must compare canonical/shared/Codex/Claude/Cursor
package bytes and validate the current-only ownership schema 3.0 with exactly
11 Guru-owned rules, nine managed claims, and three Guru-owned overlay entries.
Non-current ownership or installed manifests, unknown claims, and unexpected
overlay paths must fail current-contract validation. Validation must run dogfood
apply/drift and sidecar checks and exercise clean
marketplace init, preview/switch, preset apply, installed invocation,
`trellis update --force` or the selected version upgrade, and workflow/preset
reapply.

Phase 2 regression coverage must also prove that empty provenance/docs/
reviewed-path/command evidence, empty adequacy references, missing current or
scope-change trigger references, unknown/incomplete evidence-source closure,
and every incorrect recorder-derived semantic digest fail closed. A real Git
metadata-descendant fixture must prove the current owner-private ignored-runtime
Phase 2 checkpoint remains valid before Task Commit without adding assignment,
status, liveness, review-round, or implementation-handoff metadata. Successful
Task Commit and successful same-plan recovery fixtures must prove that the
checkpoint is then removed.
Candidate-hygiene coverage must separately prove that exact same-path official
Trellis template bytes under valid schema-v2 provenance may retain upstream
whitespace/EOF formatting in tracked migration deltas and untracked install
candidates, while a byte-exact worktree must not exempt a mismatched index or
committed `HEAD`; hash mismatch, unknown path, or invalid/missing provenance
must not suppress applicable findings, and path escape, invalid UTF-8, or
invalid JSON must still block.

Publication regression coverage must additionally reject missing stale reason,
missing or mismatched `branch_review_commit`, checked-owner commit mismatch, and
continuity drift on any exit other than `return_to_task_work`, public inputs
that carry Branch Review private identities, any `ready`
gate with a failed one of the eight transient entry preconditions or failed
shared Finalizer preflight, open objects hidden by the private schema, duplicate
finding refs that remain schema-valid, and empty finding
scope/evidence/affected/closure fields. Source and installed real-wrapper cases
must prove stale replacement and durable-drift return behavior without allowing
the runtime to choose the semantic route or Publication to read Branch Review
private checkpoints.

Before Branch Review Gate, obtain an independent Agent review of the full branch
diff from the task's intake base branch, then record the result with
`review-branch.sh --review-source independent-agent`. Main-session self-review
cannot pass the gate. Include:

- marketplace index and docs
- workflow and dogfood copy
- Phase 1 `Docs SSOT Plan` contract: docs state, evidence paths, strategy,
  affected durable docs or checked no-update paths, task artifact deltas, and
  merge/repair/follow-up checkpoint when required
- Phase 2 consumption of that plan: the implementation terminal result and live
  repository facts are ephemeral inputs to the `guru-check-task` semantic Gate;
  its ignored-runtime schema 4.0 checkpoint stores only the final Docs SSOT
  conclusion, adequacy dimensions, findings, verification evidence, and route,
  without an implementation handoff or raw worker transcript
- Phase 3 verification of that plan: final review checks the current planning
  documents, checker-passed minimal DTO, durable docs, task artifacts,
  code/test/schema/config/script/preset/overlay changes, and confirms Docs SSOT
  reconciliation already happened; it must record any current-scope
  inconsistency as a finding and must not perform the first docs merge
- companion scripts
- schemas and config templates
- preset installer and overlays
- task work commit contract: mandatory `guru-create-task-commit` invocation,
  fresh task/issue/Phase 2/HEAD/snapshot binding, exhaustive single-category
  path review, pre-confirmation canonicalization/shared-parser validation,
  exact isolated-index staging, real hooks, raw message bytes, parent/path/tree
  postconditions, unrelated preservation, and a fresh private sequence on
  finding-fix re-entry. Real regressions prove active Git operation/sequencer
  state blocks without mutation; ordinary files, executable mode, symlink,
  delete, rename, copy, gitlink, multiple-path, candidate-self, and live-index
  mismatch cases fail before standard ref publication. A clean copy source is
  not staged, an independently dirty/staged source is classified separately,
  and a changed gitlink cannot replace the reviewed OID. The positive path
  proves `git update-ref <ref> <new> <old>` publishes the validated commit,
  `git reset --mixed --quiet HEAD` refreshes the live index, Git provides final
  tree/message/path facts, and the ignored candidate plus consumed Phase 2
  checkpoint are removed. Tests must not
  add custom locks, atomic replacement, rollback, concurrency stress, or
  linearization assertions outside the #161 normal-path scope
- commit message contract: `guru-create-task-commit` reviews and validates the
  work commit it creates; Branch Review, Publication, and Finalizer prove
  ancestry/diff/reviewed-content identity without treating subject/body/`Refs`
  as cross-Skill freshness authority or creating message-only metadata commits;
  close keywords remain PR-body-only and publish/merge avoids GitHub's default
  merge subject
- Trellis task artifacts
- generated or installed-copy expectations
- Phase 0 scope and authority evidence, or the current semantic task-free
  selection when the branch intentionally skipped issue/task creation; user
  authorization and its process remain conversation-only and are never
  persisted as evidence
- owner-private checkpoint location: `review-gate.json` and similar current
  gate checkpoints must be written under ignored
  `.trellis/.runtime/guru-team/owner-checkpoints/**`, with identity derived from
  the current `task.json`, ignored runtime mapping, and live `git worktree list`
  facts. Non-current tracked gate files and alternate task-identity inputs are
  invalid and are never read. When a manual editing tool has no
  explicit working directory, use a worktree-local absolute path
- Branch Review retains only its compact owner-private ignored-runtime
  checkpoint and returns the minimal typed exit consumed by Publication. Raw
  reports, per-round review files, assignment/liveness logs, and final Markdown
  rollups are routine conversation context and must not be created as task
  artifacts.
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
- Relying on chat memory for issue close scope, base branch, or `branch_review_commit`.
- Treating one phrase, Issue presence, file count, or path as an independent
  task-free classifier instead of applying the complete semantic decision in
  `guru-select-workflow-mode`.
- Writing task review artifacts into the source checkout because a manual edit
  used a relative path while the active task lives in a separate worktree.
- Leaving `.new` or `.bak` installer outputs unresolved in committed changes.
- Committing local identity files, `.env`, tokens, signed URLs, or private
  provider output.

## Skill Eval Quality Matrix

+ Skill eval tests use the current-only representative Interface 1.4 fixture and
  execute real public wrappers.
+ Negative coverage includes unknown/null fields, duplicate or non-string ids,
  profile/exit drift, unsafe/missing/symlink fixtures, unknown assertions,
  unknown `expectations` fields, missing external semantic grading, feedback
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
+ Branch Review tests cover workflow and standalone input, all four actual
  exits, finding-fix and fresh-final intent, qualification-before-severity, and
  planned-publication missing-Skill failure.
+ Negative coverage includes incomplete qualification, mutually inconsistent
  disposition, severity on a proposal/out-of-scope item, missing or
  digest-mismatched report, round gap, stale HEAD, unfinished replacement, open
  closure finding, reused final reviewer, unconsumed business field, and an
  over-specified planned target contract.
+ Source, installed, shared/Codex/Claude/Cursor and throwaway validation prove a
  sixteen-Skill/62-exit current package closure while the production activation
  unit remains three Skills/11 exits and business markers remain integrated at
  15 invokes, 60 exits, and 36 targets. Update and preset reapply must reproduce
  that closure with zero unresolved `.new` or `.bak`.

## Task Publication Review Quality

Phase 3 publication review uses active semantic
`guru-review-task-publication`. The AI reviews diff/outcome consistency, Issue
scope closure, PR body quality, validation claims, Branch Review summary, Docs
SSOT reconciliation, safety/deployment impact, finish-summary semantics,
metadata-tail integrity, and artifact-binding freshness. Every dimension has
current evidence and every finding has a stable ref, scope basis, route,
status, and closure evidence.

Global-route tests must prove the normal authoring order independently of eval
fixtures: Branch Review `passed` enters the active Publication owner directly;
that owner authors, reviews, records, checks, and projects the exact PR payload
without creating `pr-body.md` or `finish-summary-index.json`. Tests must prove
Finalizer receives byte-identical title/body through the ready 4.0 projection
and cannot regenerate or reinterpret them. The ready projection has Finalizer
as its only side-effect consumer: workflow and package tests reject caller-owned
push or PR creation before Finalizer, and Finalizer preflight detects an
unexpected existing Open PR or disallowed remote head before any new mutation.

Metadata-only corrections require a reread/rescan and complete fresh review
inside the Skill. Any durable implementation drift returns to task work and
must repeat implementation, Phase 2, task commit, Branch Review, and
publication review. A current-scope defect cannot be downgraded to an
observation or follow-up.

Exit-quality tests exercise the complete semantic union in both schema and
runtime: `ready` rejects any non-passed conclusion, `return_to_task_work`
requires open task-work evidence bound to a finding dimension, and `blocked`
requires blocked dimension/conclusion plus matching open external-blocker
evidence. Normal AI-authored contradictory combinations must fail before the
recorder writes and must remain invalid to the checker and public wrapper.

Package/runtime/eval tests cover both profiles and modes, three exits, stale
re-entry, metadata correction to fresh pass, metadata correction that reveals
durable drift, non-current readiness rejection, and the shared side-effect-free
Finalizer preflight before `ready`. Finalization tests prove the ready DTO
(`exit_id/task_ref/branch_review_commit/pr_title/pr_body`) plus live facts is sufficient;
the Finalizer stale DTO preserves that same commit anchor through the
unique Publication projection, and a combined regression proves content drift
returns `finding_refs` with `resume_target=phase-2`;
the Publication wrapper retires its checkpoint after valid output, old 3.0
Publication/Finalizer shapes fail closed, and Finalizer
never augments, parses, or deletes that checkpoint. Finalizer terminal tests
prove it retires its transaction, gate, and request only after the
`ready_for_merge` DTO validates. The closeout transaction must leave Issue Scope
Ledger bytes unchanged and must not invoke, read, archive, or retain extension
verification state.
Recovery tests build a real commit topology where an existing PR/remote HEAD is
a strict ancestor of the current publication HEAD. They prove exact
fast-forward push, metadata convergence, Ready preservation, Draft-to-Ready,
archive/three-way HEAD completion and idempotent resume without duplicate push,
edit, PR creation, archive, or Ready mutation. Negative coverage includes
multiple/fork/closed identity, repo/head/base mismatch, unknown or non-ancestor
HEAD, force-push drift, scope/payload/Publication drift, archive conflict and
unknown transaction state. Ordinary first publication continues to reject any
Open PR without an explicitly previewed recovery binding.
Finish-family integration additionally proves current finish-summary schema 2
is derived once from the reviewed payload and live facts, historical schema 1
remains discoverable, and the current runtime/inventories contain no retired
body/index reader, writer, CLI flag, fixture, or managed asset. Message-only
commit deviations do not force a downstream revision when reviewed content is
unchanged; real descendant content drift still returns to task work.
Shared, Codex, Claude, and Cursor consume byte-identical
canonical corpus bytes; every semantic case executes the real public wrapper,
and actual exit selects the schema before grader comparison.

Source/installed/platform/throwaway checks assert sixteen active Skills and 62
package exits, exactly one `production-current-v2` three-Skill/11-exit current
manifest, and business workflow markers of 15 invokes, 60 exits, and 36 targets.

## Extension Installation Verification Quality

`guru-verify-extension-installation` quality coverage exercises the single
`source_repository_verification` profile and independent `verified|blocked`
outputs. Contract tests prove Interface 1.5 standalone-only discovery, no global
workflow marker, no Finalizer consumer/projection, ignored source-session state,
and exclusion of task identity and private fields from public DTOs.

Runtime coverage proves canonical source assets, source repository/origin,
requested ref, resolved commit, HEAD, and clean tree are validated before clone,
tempdir creation, installer execution, artifact write, or mutation. Non-source,
task-bearing, dirty, ref-mismatch, and HEAD-mismatch cases assert zero executor
calls and zero verifier artifacts. Source success uses an isolated clean
throwaway target and covers marketplace, preset, workflow, platform equality,
ownership, update/reapply, sidecars, README commands, and redaction.

The package-local production corpus contains two real-wrapper cases spanning
`verified` and `blocked`. Shared/Codex/Claude/Cursor consume byte-identical
canonical corpus and package bytes. Actual exit chooses the output schema before
`expected_exit` comparison; native requests do not receive expected exit or
private verification state. Remote-ref acceptance and production eval remain
independent evidence surfaces.

## Task Finalization Quality

`guru-finalize-task` quality coverage exercises four current public input
profiles, six outputs, the four finalization-family authoring handoffs, semantic
Gate/confirmation ordering, and the owner-private recovery loop. Together with
the five prior handoffs, the active package graph contains nine target-owned
`skill_input_authoring_seed` handoffs.

Current gate 5.0 and transaction 3.0 regressions prove Publication input, exact
pre-push authority, Draft/Ready identity, archive recovery, and terminal cleanup.
Current interfaces, manifests, runtime preparation and archives do not select,
create, read, move, or retain `closeout-plan.json` or a verifier result; legacy
schemas/examples remain immutable and are tested only by explicit rejection or
compatibility selectors. Archive projection contains exactly six durable core
files.

Representative business fixtures cover docs, code, config, `.trellis/**`,
platform copies, and an installed extension manifest. Their complete
Publication -> Finalizer -> Merge trace asserts zero verifier wrapper calls,
zero verifier commands, and zero verifier artifacts even when verifier network
or API access is unavailable. Publication `return_to_task_work` remains covered
for real descendant content drift.

Finalizer and Merge cardinality regressions retain empty, one-Issue, and
multi-Issue cases, expected-head merge, close-keyword validation, and post-merge
closure verification. The installed #174 replay executes Branch Review,
Publication, Finalizer, and Merge public wrappers in one shared owner repository;
actual stdout and declared projections bind every edge. It explicitly excludes a
verifier hop and scans terminal task/runtime state for verifier residue.

Canonical, installed shared, Codex, Claude, and Cursor package/corpus bytes and
script modes match after fresh install, update, and preset reapply. Package
closure is sixteen active Skills and 62 exits; business global markers remain 15
invokes, 60 exits, and 36 targets. Upstream Finish assets remain unchanged.

## Base Evolution Gate Quality

Source and installed contract tests cover all six
`guru-reconcile-task-base` exits, unique consumers, thin projections, closed
`resume_target` values, package-private state, and the bounded Branch Review
continuity profile. Semantic evals exercise unchanged, unrelated,
related-compatible, equivalent integration, validation failure, textual and
semantic conflict, authority change, upstream supersession, PR-ready base
advance, and non-ancestor history. A base SHA or path hit alone must never
synthesize stale, finding, pass, reset, or block.

One shared stateful integration fixture passes actual producer stdout through
the pair guard, semantic owner, router, and target consumer at every eligible
boundary. It proves an unchanged pair causes zero semantic invocation,
GitHub/Docs/history scan, artifact write, and interaction; multiple base
advances form one accumulated delta; a current pair result is consumed at most
once; and a task-content HEAD change prevents reuse. Performance assertions
derive counts from the event log and live workflow markers rather than case
labels or duplicated literal tables.

Bounded continuity tests prove the existing task semantic review is not replayed
when task content is unchanged, while a required task change still performs
fresh implementation, Phase 2, commit, and Branch Review. Finalizer tests keep
`base_reconciliation_required` distinct from Publication content/metadata
stale. Current-runtime replays for the historical #132 and #161 scenarios must
reconstruct valid live facts without treating old HEADs, digests, or fabricated
state as authority.

Distribution acceptance covers canonical and installed specs, package/runtime
inventory, Shared/Codex/Claude/Cursor discovery bytes and executable modes,
clean marketplace init, preview/switch, preset apply/reapply, official Trellis
update and supported version upgrade, managed-hash replacement, unknown-edit
`.new`, known-upgrade `.bak`, legacy cleanup, recursive zero sidecars, and
README commands. Graph cardinalities are derived from the current registry,
interfaces, and workflow markers; documentation and tests must not preserve
stale hard-coded counts after package activation.

## Managed Python Runtime Gate

Runtime changes require package/runtime unit tests for stable identity, same-id
reuse, lock drift, damaged managed runtime repair, candidate failure preserving
the active pointer, resolver failure JSON, pinned dependency versions, and real
Draft 2020-12 behavior. Identity coverage includes OS, architecture, Python ABI
and platform tag. Locator tests cover macOS, Linux/XDG and Windows user-cache
roots plus an isolated override. A real Git main-checkout -> linked-worktree
lifecycle must prove a new linked checkout inherits the Git-common-dir default
and shared runtime without copying a venv. A two-checkout, two-identity case
must also prove each checkout retains its exact runtime selection after
sequential apply. Preset tests must prove the runtime contract files are
in the managed inventory with canonical bytes and executable modes.

Runtime test harnesses must bootstrap against an isolated temporary repository,
not the source checkout under test. Subprocesses that intentionally exercise the
source checkout wrappers must not inherit a test-only cache-root override. The
suite must prove the source checkout's active pointer bytes are unchanged before
and after execution so test cleanup cannot leave a stale interpreter path.

At least one focused clean install must use a PATH Python that can create a venv
but cannot import `jsonschema`, apply the real preset, and execute a real public
schema-bound wrapper through the installed managed interpreter. The focused
gate also includes targeted reapply, canonical/installed equality, dogfood drift,
and a recursive zero-unknown-sidecar check. Missing pointer,
missing/stale cache entry and failed dependency probe must remain distinct stable
errors.

This focused gate does not replace the complete extension release verification:
the full capability suite, marketplace matrix, official Trellis update, complete
platform throwaway matrix, and business-repository upgrade smoke remain separate
cumulative release evidence.
