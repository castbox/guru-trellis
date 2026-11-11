---
name: guru-qualify-solution-mechanism
description: Qualify whether a proposed implementation mechanism can carry the required business authority without delegating it to OS, kernel, process, or descriptor primitives.
---

# Qualify Solution Mechanisms

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Caller first reads [applicability](references/applicability.md) before loading this Skill. When it requires invocation, read `references/contract.md` completely and judge the actual applicable nonempty candidate set.

Read current requirement, planning, Architecture, dependency/caller graph, diff, tests and repository contract yourself. Keywords, scanner output and passing tests cannot replace the contract's semantic review.

Complete the AI Gate and invoke `scripts/invoke.sh --invocation -` with one call-local envelope on stdin. Consume the original exit and unique consumer; recorder/checker success never supplies semantic qualification.

Runtime checks only shape, identity, freshness, enums and consumer binding. It decides no mechanism suitability and writes no qualification state.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipt projection. Author inputs/returns: `references/contract.md#author-candidate-set`; before computing its file-set token, load the shared [format and recipe](../guru-qualify-normal-scenario/references/contract.md#file-set-identity).
