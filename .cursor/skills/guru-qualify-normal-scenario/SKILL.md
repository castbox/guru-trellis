---
name: guru-qualify-normal-scenario
description: Qualify one profile-specific candidate set against current normal-scenario authority before a Guru Team caller may promote it into scope, tests, findings, implementation, or publication blocking.
---

# Qualify Normal Scenarios

Read [references/contract.md](references/contract.md) completely before judging a candidate set.

Use the exact profile supplied by the caller, reread the live locators, complete the semantic AI gate, and invoke `scripts/invoke.sh --invocation -` with one call-local JSON envelope on stdin. Return exactly one declared typed exit.

Keep every decision and typed result inside the current invocation. Do not write a tracked file, ignored runtime artifact, result locator, checkpoint, report, ledger, transcript, assignment, handoff, approval, or signoff.

Fail closed on missing live evidence, stale identity, an unknown or mismatched caller/profile/consumer, an empty candidate set, or any candidate without exactly one current decision.
