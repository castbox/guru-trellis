---
name: guru-qualify-normal-scenario
description: Qualify one profile-specific candidate set against current normal-scenario authority before a Guru Team caller may promote it into scope, tests, findings, implementation, or publication blocking.
---

# Qualify Normal Scenarios

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Read [references/contract.md](references/contract.md) completely before judging a candidate set.

Use the exact profile supplied by the caller, reread the live locators, complete the semantic AI gate, and invoke `scripts/invoke.sh --invocation -` with one call-local JSON envelope on stdin. Return exactly one declared typed exit.

Keep every decision and typed result inside the current invocation. Do not write a tracked file, ignored runtime artifact, result locator, checkpoint, report, persistent decision state, transcript, assignment, handoff, approval, or signoff.

Fail closed on missing live evidence, stale identity, an unknown or mismatched caller/profile/consumer, an empty candidate set, or any candidate without exactly one current decision.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.

The Author candidate profile and its original-owner returns are defined in
`references/contract.md#author-candidate-set`.
