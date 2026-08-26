# Guru Trellis Evolution Test SSOT

状态：`test_candidate_planned` / `requirements_input_current` / `design_ready_for_delivery_planning`。This directory is the target Test authority paired with
[`../../design/evolution/`](../../design/evolution/README.md). It defines what future implementation candidates
must prove; it is bound to the `REQ-REV-011..132` Requirements-ready identity and the fresh-reviewed
`DES-REV-001..014` Design candidate. No fixture is reported as executed by this planning task.

Read in this order:

1. [`test-strategy.md`](./test-strategy.md): evidence layers, selection, result and gate rules;
2. [`fixture-plan.md`](./fixture-plan.md): all 47 fixture owners, candidates, layers, recovery and acceptance;
3. [`traceability.md`](./traceability.md): Requirements/Design/capability closure;
4. [`manifest.yaml`](./manifest.yaml): candidate identity and authority locators.

Current as-built Test remains
[`../versions/current-main-0.6.5-guru.40/`](../versions/current-main-0.6.5-guru.40/test-strategy.md).
Coexistence is current/target documentation separation, not runtime dual-read or evidence reuse.

Allowed result states are `planned_not_executed`, `pass`, `fail`, `blocked`, `skip_unverified`. A historical or
different-candidate result can only be research evidence; it cannot change a row out of `planned_not_executed`.
