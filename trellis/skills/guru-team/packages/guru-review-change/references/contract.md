# Independent Change Review Contract

## Ownership And Entry

`guru-review-change` owns a complete independent read-only review: target and
scope interpretation, evidence collection, semantic analysis, finding judgment,
coverage, verification sufficiency and the final user report. It uses
`judgment_mode=semantic`:

```text
forward behavior -> AI Review Gate -> conditional human interaction
-> objective validator -> one typed exit
```

The global workflow selects this owner for independent review and consumes its
terminal exit. It does not implement the review method. Formal
`guru-check-task`, `guru-review-branch` and Completion owners retain their own
entry conditions, stage-specific qualification, result recording and consumers.
They read `review-method.md` within those responsibilities; they do not obtain a
formal result by invoking this independent Skill.

### Discover By Object And Purpose

The AI matches the current conversation's review object and purpose. Natural
expressions include 审核、审查、评审、复审、review、code review、代码审核 and
equivalent requests. These are discovery cues, not a keyword classifier or an
instruction to take over every review request. Do not implement this decision
as a Python or regular-expression classifier.

Use this entry for independent review of implementation completion, requirement
→ design → code → test-plan/test-case consistency, test coverage, duplicate
implementations or test coverage, tests that merely confirm their own setup,
and other applicable anti-patterns. Examples include “审核 xx 需求的完成情况”,
“需求审核” when implementation is the established object, “检查这个需求是否做完”,
“评审当前分支是否完整实现某个需求”, “确认需求、设计、代码、测试是否一致”,
“检查测试是否覆盖这次需求”, “审查是否存在重复实现/重复测试覆盖”, and
“检查这次改动是否闭环”. The selected object may be the current branch, a PR,
uncommitted changes, or an explicit set of documents, code and tests. Preserve
that selection; do not default to a whole branch or Task when it is narrower.

“审核需求是否已实现” reviews implementation against requirement authority.
“审核需求本身是否完整合理” reviews the requirement itself and does not enter
this Skill. Apply the same distinction when an Issue or initiative supplies
authority for an implementation review: using that authority does not make
review of the Issue or initiative itself this Skill's responsibility.
For a mixed request, preserve the implementation-review scope here and leave
each upstream-content portion to its original owner; do not absorb the entire
request or discard its implementation review.

| Actual object and purpose | Entry boundary |
| --- | --- |
| Issue content, requirement clarification, Issue readiness or Issue wording | Leave to the existing `guru-clarify-requirements`, `guru-review-change-request` or `guru-review-contract-wording` owner according to its scope and prerequisites. |
| Completeness or reasonableness of requirements themselves, including full product or technical requirement documents | Leave to the existing requirement process and applicable `requirement-review` or `technical-requirement-review` specialist. |
| An initiative, 动议 or proposal itself | Leave to the original project's upstream initiative or requirements process. If no dedicated owner exists, report that gap to the caller for its existing entry; do not invent a Skill or owner. |

Resolve this boundary before constructing public input or running capture.
For an excluded object, explain the mismatch and stop this independent-review
entry. Do not run its scripts, emit its `reviewed` or `blocked` result, or
manufacture an upstream owner's typed exit. A discussion of Skill design,
trigger wording or routing is not itself a request to review an actual object.

For a bare “review”, “审核一下” or “再看一遍”, inherit the object already made
clear by the current conversation. If it is still unclear, ask one minimal
question about the review object before executing scripts. Do not choose a
Task from inventory, expand scope or assume implementation review solely from
the verb. Once the object is clear, apply its existing owner and prerequisites.

Entry requires a readable selected repository, an identifiable review purpose
and an adequate review scope. It requires no Task or Delivery. Read available
Task planning only when it is relevant current authority for the requested
object, after the method's first independent Architecture read and judgment.
Do not infer an accepted Task, choose one from inventory, restore a
binding or require a Planning template to make review possible.

If the request explicitly asks for a formal stage result, retain that original
owner's entry before selecting this Skill. If a caller has selected this Skill
but actually needs a formal result, explain that mismatch and return `blocked`;
do not reinterpret an independent `reviewed` exit as that result.

## Public Input And Private Context

The exact closed schemas and examples selected by `interface.json` own the
wire contract. Public input contains intentional caller selections only:

| Profile | Required selections | Optional selection |
| --- | --- | --- |
| `working_tree` | `mode=standalone`, `repository` | `paths` |
| `committed_range` | `mode=standalone`, `repository`, `base`, `head` | `paths` |

`repository` selects the Git repository to review and may be an absolute root
or intentionally relative to the Guru provider root. Normalize an external
target to its absolute Git root before invocation; the launcher runs from its
provider root. `base` and `head` select the intended committed range. `paths`
are literal repository-relative paths or directories; omission selects the
complete profile range. Resolve an ambiguous repository, version or range from
current facts first. Ask only when a real choice remains. Do not widen a
specified function or file review into an entire Task or branch.

`working_tree` covers the index and working-tree projections, including
selected untracked and deleted files, against the current HEAD when one
exists. A newly initialized repository without a first commit is supported:
review its actual staged, unstaged and untracked content, with the snapshot
preserving the true absence of commit anchors. Do not create a commit or invent
an OID to make review possible. Staged and unstaged versions can differ;
inspect both when they affect the requested review. A committed range requires
the selected commits and reviews the direct `base` to `head` tree difference,
without selecting a merge base automatically. If the user intends a merge-base
branch comparison,
resolve that base explicitly first. Existing dirty content is outside that
range unless the user also selected a working-tree review.

For multiple repositories or separate ranges, use one invocation per selected
repository and target. The same semantic reviewer may inspect necessary
cross-repository consumers and explain the combined coverage, while preserving
each invocation's exact scope and evidence layer.

Run `scripts/capture.sh --input -` with one public input on stdin. Its
intermediate receipt `result` is a private call-local snapshot. Keep it in
memory for the final validator. It identifies the selected Git facts and
content; it does not prove semantic coverage. Do not write it to a temporary
result file, repository artifact, ignored checkpoint or handoff.

The snapshot binds selected content. The semantic owner also reads relevant
unchanged dependencies and rechecks affected dependency facts before reporting.
An unchanged selected diff cannot prove that an independently changed consumer
or required external contract remains applicable.

## Forward Behavior

Read `review-method.md` completely, including its provider resolution. Apply
its mandatory original-owner source reads, independent Architecture order and
business-implementation coverage judgment. Read their actual sections from the
same provider; the method's reference list is not a substitute. Apply that
provider's `semantic-retrieval.md` before semantic retrieval and
`quality-guidelines.md#specialist-review-standards` for specialist methods.
Framework contracts come from that complete Guru source or installation;
project authority comes from the selected review repository. That repository
need not contain a Trellis installation, preset, Task or framework spec copies.
Use actual current sources and affected consumers, not a prior pass, worker
summary, heading set or link list in place of reading them.

### Required Independent Perspectives

The independent owner must actually use three different independent subagents
for these perspectives. One Agent describing itself as several roles does not
satisfy this entry.

| Perspective | Required review responsibility within the selected scope |
| --- | --- |
| Architecture | Apply the original Architecture semantic sources, authority-first read order, current checks and adopted-mechanism judgment to the complete selected candidate and affected consumers. |
| Business implementation and code | Trace actual source/accepted obligations and necessary scenarios through implementation, consumers, remaining work and the original business-coverage evidence layers. |
| Test effectiveness and boundary evidence | Judge actual test entry, observations and defect detection, together with applicable cross-layer, compatibility and distribution/installation evidence and its limits. |

Every carrier, including the final semantic owner, must not have authored or
implemented the candidate. When the caller is the author, it obtains an
independent final owner; the author cannot aggregate reports into an independent
conclusion. The final owner retains full review responsibility rather than
delegating its Gate to a worker, majority vote or command result.

For the first Architecture assessment, use the method's fresh generic carrier
with empty history and `fork_turns=none` on Codex. It reads original project
authority before candidate bodies and forms its independent Architecture
judgment before Task narratives or the business/test reports reach it. Do not
preload those reports through dispatch or conversation history. If the caller
already dispatched the final owner as that compliant Architecture subagent,
the owner first performs this perspective itself, then dispatches the other two
perspectives to different subagents and may aggregate their results. Do not
dispatch a second Architecture carrier merely to repeat that assessment.

Schedule these perspectives in waves or sequentially when concurrency slots
are limited. Slot availability is a scheduling constraint, not proof that
collaboration is unavailable. Finish the initial isolated Architecture judgment
before sharing later Task narratives or other perspectives' reports with that
carrier. No additional approval flow is required for this Skill's review work.

Each worker reads the complete shared method and its mandatory same-provider
original semantic sources, then the actual authority, candidate and necessary
consumer bodies for its perspective. Reports or source lists cannot replace
those reads. All workers operate read-only within the selected scope. They
neither repair code nor create a gate, report, assignment, checkpoint, reviewer
ledger or other repository/runtime record. Their findings, evidence locators,
coverage and gaps remain ephemeral inputs to this invocation.

The final owner reads underlying evidence locators, resolves contradictory
observations, supplements coverage gaps and personally performs the final AI
Review Gate. Worker count, agreement, file count and green commands do not
prove completeness or semantic correctness. If a required carrier cannot
execute, does not finish, or lacks the necessary independence, report the
actual limitation and return `blocked` with any supported partial observations.
Do not silently downgrade to one Agent or claim complete coverage.

Later candidates retain eligible reviewers and verifiable coverage under the
original sources' continuation and engineering-fact applicability rules.
Changed Architecture facts return to the eligible Architecture carrier for the
corresponding assessment; missing or unbounded coverage needs the original
complete assessment. A different worker, stage or HEAD alone does not require
repeating unchanged assessment or validate an old pass. Necessary current
conclusions from all perspectives still require actual coverage.

This multiple-subagent requirement belongs only to `guru-review-change`.
Formal Check and Branch Review consume the shared semantic method under their
own worker policy, independence, qualification, Architecture results and exits;
they do not inherit this Skill's perspective count or dispatch protocol.

Inspect the commands and their effects before executing verification. Run only
checks already authorized by the request and compatible with read-only review.
An isolated check may use its normal scratch outputs when it leaves the
reviewed repository and external state unchanged. A command that rewrites
source, installs dependencies, generates repository assets, changes refs or
performs external mutation needs its own applicable authorization and owner.
Keep unavailable verification as an explicit evidence gap. Do not alter tests,
fixtures or code to obtain a green result.

## AI Review Gate

After the current analysis, the semantic owner judges all of the following:

- The required distinct subagent perspectives actually executed with the
  necessary independence and coverage. The final owner checked their original
  evidence, resolved contradictions and supplemented gaps; labels or consensus
  did not replace that work.
- The actual selected content and relevant dependencies have been covered.
  Coverage respects the user's scope and every applicable common dimension.
- Each reported defect has current authority, a real supported entry and
  consumer, an honest normal trigger, evidence and a concrete impact. Necessary
  local correction is distinguished from unrelated historical improvement.
- Finding severity follows impact. An excluded scenario, speculative future
  requirement, duplicate text or unexecuted test is not promoted mechanically.
- The original semantic sources were read and applied. Independent Architecture
  judgment addresses applicable project authority, the baseline rules' own
  applicability, current semantic project checks and the complete selected
  candidate's adopted mechanisms and affected consumers. Missing authority or
  evidence limits only its dependent conclusions; baseline agreement or
  passing functional tests cannot replace that judgment.
- Actual source and accepted obligations have been traced to the necessary
  scenarios, behavior paths, implementation, tests and unfinished work within
  the requested scope. Code/test agreement alone is not business completeness.
  Whole-Task scope, a Delivery slice, implementation still missing and evidence
  still unavailable remain distinct under the original semantic sources.
- Validation execution, adopted engineering facts, static analysis, integration
  evidence and external or production effects are described at their real
  layers. A command pass or snapshot match does not settle semantic correctness.
- The report is supported by the current candidate and dependencies. An
  author self-check, partial review or specialist pass is not presented as an
  independent complete review or formal stage result.
- `reviewed` or `blocked` accurately expresses the current assessment. Scripts
  have not selected the outcome or supplied a finding, sufficiency or route
  judgment.

Keep this judgment and report in the current invocation. No durable artifact
is needed for this terminal user response. Do not persist user authorization,
reviewer metadata, raw search history, findings history or a second evidence
store.

## Objective Invocation And Terminal Response

After the AI Review Gate, invoke `scripts/invoke.sh --invocation -` with the
envelope selected by `interface.json` and its package examples on stdin. Pass
the actual current capture receipt `result` object as the reviewed owner's
snapshot; never author or reconstruct its fields yourself. The blocked owner
result instead carries its concrete blocking reason under its separate closed
schema. That reason is current semantic content, not authorization or recovery
state. The schemas and examples own field shapes; this method does not create
a second wire definition.

The runtime validates input shape and, for `reviewed`, the captured selected
content against current Git facts. It validates and projects the owner-selected
terminal exit. It does not read a report to classify meaning or choose an
outcome. A stale or invalid invocation retains its actual diagnostic. Reread,
recapture and reassess affected coverage; do not repeatedly submit an old
snapshot.

After successful validation, the same semantic owner displays its in-memory
report directly to the user in Chinese, then returns the one validated exit.
The exit DTO contains only `exit_id`. Its sole terminal consumer is
`independent-review-response` for `reviewed`, or `independent-review-blocked`
for `blocked`. There is no next Skill that reads a report artifact or private
snapshot.

The report contains findings first, ordered by actual severity. Each actionable
finding names the current location, trigger, authority, impact and focused
revision. If there is no actionable issue, say so explicitly. Then state the
reviewed repository and scope, relevant coverage, validation execution or
adoption, and unverified boundaries. Explain Architecture fit and any necessary
reconsideration of baseline rules, actual business-implementation coverage
(complete, incomplete or insufficiently evidenced, with concrete reasons),
remaining work and the other applicable dimensions. Name missing project
authority or required checks specifically. Distinguish the original sources'
contract, implementation, deployment/entry, enablement, adoption and end-to-end
evidence layers where applicable. Dimension names or empty pass assertions are
not those conclusions. A blocked report names the necessary gap and any
supported partial observations; it does not claim complete coverage.

`reviewed` means this requested review is complete, with or without findings.
It does not assert defect-free code, formal Check, Branch Review, readiness,
Task Completion, successful installation or production effect.

Neither exit creates or binds a Task, advances lifecycle, calls `begin_check`
or `record_gate`, records formal evidence, repairs files or publishes to an
external system. A later fix or formal stage invocation is a separate request
under its original owner and authority.
