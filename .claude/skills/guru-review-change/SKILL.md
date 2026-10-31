---
name: guru-review-change
description: 使用多个不同 subagent 从架构、业务实现、测试及跨层证据等角度独立只读审核代码、变更文档和测试，无需 Task 或 Delivery。适用于审核、审查、评审、复审、review、code review、代码审核，以及审核需求完成情况、需求审核（实现完成度）、检查需求是否已实现/做完、审核这些修改、改动是否闭环、需求→设计→代码→测试一致性、测试计划与用例覆盖、重复实现/重复测试覆盖、测试自证、反模式，或审核当前分支、PR、未提交修改、明确文件/范围。先按对象和目的作 AI 语义匹配；关键词本身不触发。Issue 内容、需求本身是否完整合理、动议/initiative/proposal 本身均不属于本 Skill。仅说“review/审核一下/再看一遍”时继承当前对话明确对象，仍不清楚才作最小澄清。讨论 Skill 或触发词不发起真实审核。正式 Check、Branch Review、Completion 保留原 owner 与前置。
---

# Guru Review Change

Resolve the complete Guru source or installation that provides this Skill.
Before substantive output, read its workflow-spec
`clear-technical-writing.md` in full and apply it within this entry's scope.
The provider root is `trellis/presets/guru-team/spec/workflow` in source, or
`.trellis/spec/workflow` after installation. Until that read succeeds, use
only short progress messages or a concrete missing-dependency diagnostic. If
reading fails, pause substantive output, then read it and resume the same request
when available. That recovery requires no additional approval.

This Skill is the semantic owner of independent read-only change review. Read
[the complete contract](references/contract.md), the selected input contract in
`interface.json`, and [the shared review method](references/review-method.md)
before acting. The package declares `judgment_mode=semantic`.

No Task, Delivery, accepted Planning result, public candidate or prior formal
Check is required. An existing Task may supply relevant scope and authority;
its presence does not select formal execution. A user or workflow requesting a
formal stage result uses that stage's original owner and full prerequisites.
This Skill produces no formal Check, Branch Review, readiness or Completion.

Execute the contract's [required independent perspectives](references/contract.md#required-independent-perspectives)
with different subagents. One Agent claiming several roles is insufficient.
The final semantic owner must be independent of implementation and personally
integrates the evidence before its Gate. This dispatch requirement belongs only
to this independent Skill; formal Check and Branch Review keep their own policy.

Resolve package-local `references/`, `scripts/`, schemas and examples from
`trellis/skills/guru-team/packages/guru-review-change` in that source, or
`.trellis/guru-team/skills/packages/guru-review-change` in that installation.
Keep the package and shared framework specs from the same provider. The
selected review repository may be elsewhere and need not have Trellis or the
Guru preset. A discovery projection is an entry, not a separately maintained
method.

## Select The Review Entry

Before constructing input or running capture, use the requested object and
purpose to decide whether this independent implementation or change review
applies. Read [Ownership And Entry](references/contract.md#ownership-and-entry)
for discovery expressions and object boundaries. Review verbs help discovery;
they do not override the actual object or select a formal stage.

Reviewing whether a requirement has been implemented belongs here. Reviewing
Issue content, the completeness or reasonableness of requirements themselves,
or an initiative/proposal itself does not. Stop this entry before capture and
leave those requests to their existing upstream owners. Do not manufacture a
review result or another owner's typed exit.

For “review”, “审核一下” or “再看一遍”, inherit an object already clear in the
current conversation. If the object remains unclear, ask one minimal object
clarification before running scripts. Do not select a Task or enlarge scope.
Discussion about this Skill or its trigger wording is not a request to review
an actual object.

## Execute The Review

1. After the entry decision, resolve the requested repository, review purpose
   and scope from the current conversation and live facts. Choose `working_tree`
   or `committed_range`; preserve any explicitly selected paths. Clarify only
   a real ambiguity that remains. Do not create a Task to obtain review inputs.
2. Run `scripts/capture.sh --input -` with the selected public input on stdin.
   Keep its receipt `result` as this invocation's private snapshot in memory.
   Capture supplies objective context only. Do not start candidate or Task
   narrative reading ahead of the method's independent Architecture read order.
3. Execute the contract's three independent perspectives with distinct
   subagents, reading the entire shared method and its original-owner sources.
   Complete the isolated Architecture assessment before Task narratives or
   other perspectives' reports reach that carrier. Then obtain the business
   implementation/code and test/cross-layer perspectives. Use waves when
   concurrency is limited. Include the selected candidate and necessary unchanged
   consumers without expanding scope or inventing a formal result.
4. Personally reconcile the perspectives against their original evidence,
   resolve contradictions and supplement coverage gaps. Complete the AI Review
   Gate in the contract. Judge candidate validity,
   necessity, severity, coverage and evidence gaps. Keep the draft report in
   memory. Use only verification whose known effects fit the current read-only
   request; do not fix code, generate assets or mutate external state.
5. Recheck the current input, selected content and relevant dependencies. Invoke
   `scripts/invoke.sh --invocation -` with the call-local envelope defined in
   the contract. The validator verifies objective input and content continuity;
   it cannot judge whether the report is sufficient or the code is correct.
6. After a validated terminal exit, display the current report directly to the
   user in Chinese and return exactly that exit. Follow its declared terminal
   consumer. Never announce a stale draft report as the completed review.

## Typed Exits And Recovery

- `reviewed`: the semantic owner completed the requested review and the final
  content validation succeeded. Report findings, or explicitly report that no
  actionable issue was found, together with coverage and unverified limits.
  `reviewed` may contain findings; it does not mean defect-free or formal pass.
- `blocked`: a concrete scope, authority, independence, access or execution gap
  prevents the requested review. Explain the gap and any supported partial
  observations without claiming complete coverage.

A normal change to the selected input or content invalidates the affected
draft judgment. Reread current facts, recapture, and review the changed content
and affected dependencies before invoking again. Missing or invalid input and
runtime errors retain their original diagnostic; do not manufacture a snapshot
or rename a validator error to a semantic success.

This Skill never creates or binds a Task, calls `begin_check` or `record_gate`,
advances lifecycle, records a formal gate, stages or changes reviewed files, or
publishes to GitHub. It stores no report, checkpoint, authorization or reviewer
history in the repository or ignored runtime.
