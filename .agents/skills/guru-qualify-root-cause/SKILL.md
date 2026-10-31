---
name: guru-qualify-root-cause
description: 在 Guru 当前步骤中评估新增或实质变更的诊断、缓解、根因修复与保护机制，判断候选是否有充分因果依据、是否仅掩盖症状，并返回原步骤。用于真实 caller/profile 下的机制准入；独立 review 复用其语义方法，直接故障排查由当前项目执行职责承接。
---

# Qualify Root Cause

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

This Skill owns candidate admission for the current Guru step. It assesses a
proposed investigation, mitigation, repair or protection mechanism; the current
execution owner performs the investigation or change and judges its completion.

## Select The Entry

Read `references/contract.md` completely, including its entry boundaries, and
select the actual use before constructing input or invoking a script:

- **Candidate qualification:** use a declared caller/profile from the current
  `interface.json`, a real target and candidate set, and the actual normal-scenario
  and solution-mechanism outcomes consumed by that caller. Standalone mode has
  the same prerequisites and runtime dependency as workflow mode.
- **Independent change review:** `guru-review-change` reads the causal method
  and common semantics within its own review. Method reuse invokes no root
  qualification and creates no Task, candidate identity, profile or typed exit.
- **Direct investigation:** a request such as “排查根因” or “定位这个 bug” stays
  with the current project's actual investigation/execution entry. That owner
  collects evidence and may later submit an eligible mechanism here. Unknown
  cause alone does not prevent bounded diagnosis.
- **Discussion of this Skill:** explain the Skill without running qualification.

When an actual caller/profile or upstream outcome is missing, state the concrete
prerequisite gap and return control to the actual caller or current project
entry before constructing invocation input. Do not create resources or invent
identities, upstream results or a qualification exit to make the request fit.
A valid qualification whose current authority or evidence is unavailable still
uses its declared `blocked` result. Runtime input errors retain their actual
diagnostic; they are not semantic results.

## Execute Candidate Qualification

Read the same provider's `causal-completion-semantics.md` before goal judgment:
`.trellis/spec/workflow/` after installation, or
`trellis/presets/guru-team/spec/workflow/` in the complete source. It owns common
causal evidence and completion semantics; this package owns candidate admission.

Read current scope, authority, mechanism and evidence yourself. Apply the
contract's goal-specific method to the complete eligible set, then author the
call-local semantic result and perform its AI Review Gate. Invoke
`scripts/invoke.sh --invocation -` on stdin. The runtime validates facts and
structure only, and writes no qualification state. Return one declared exit.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.

The Author candidate profile and its original-owner returns are defined in
`references/contract.md#author-candidate-set`.
