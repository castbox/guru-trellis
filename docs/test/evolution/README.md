# Guru Trellis Evolution Test SSOT

状态：`test_candidate_planned` / `design_ready_for_delivery_planning` / `fresh_design_review_passed` /
`evolution_refactor_eligible`。This directory is the target Test authority paired with
[`../../design/evolution/`](../../design/evolution/README.md). It defines what future implementation candidates
must prove. `REQ-REV-133..138` adds #311/#312 prerequisite preservation including installed terminal continuity,
standalone verifier failure evidence and unrelated-dirty isolation, separates Requirements readiness from
refactor eligibility, and makes the prior
`REQ-REV-011..132` / `DES-REV-001..014` review binding stale. All 50 rows now have reviewed Design allocation:
Reconcile owns #312 continuity, Publish/Finish/Merge preserve the #311 installed terminal, and Projection owns
standalone verifier failure evidence. Fresh Design review and deterministic closure passed; no fixture is reported
as executed.

Read in this order:

1. [`test-strategy.md`](./test-strategy.md): evidence layers, selection, result and gate rules;
2. [`fixture-plan.md`](./fixture-plan.md): all 50 fixture owners, candidates, layers, recovery and acceptance;
3. [`traceability.md`](./traceability.md): Requirements/Design/capability closure;
4. [`manifest.yaml`](./manifest.yaml): candidate identity and authority locators.

Current as-built Test remains
[`current-main-0.6.5-guru.41` at selected base](https://github.com/castbox/guru-trellis/blob/3efcce72a0d47e38ec725aa8c0f8498992f3416f/docs/test/versions/current-main-0.6.5-guru.41/test-strategy.md).
The prior `.40` snapshot is comparison evidence only.
Coexistence is current/target documentation separation, not runtime dual-read or evidence reuse.

Allowed result states are `planned_not_executed`, `pass`, `fail`, `blocked`, `skip_unverified`. A historical or
different-candidate result can only be research evidence; it cannot change a row out of `planned_not_executed`.
