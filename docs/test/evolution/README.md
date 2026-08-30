# Guru Trellis Evolution Test SSOT

状态：`test_candidate_planned` / `fresh_design_review_passed` / `evolution_refactor_eligible`。This directory is the target Test authority paired with
[`../../design/evolution/`](../../design/evolution/README.md). It defines what future implementation candidates
must prove. `REQ-REV-133..142` adds #311/#312 prerequisite preservation including installed terminal continuity,
standalone verifier failure evidence and unrelated-dirty isolation, separates Requirements readiness from
refactor eligibility, and makes the prior
`REQ-REV-011..132` / `DES-REV-001..014` review binding stale. PR #317 exact installed platform-set preservation is
projected into the existing installed publication row. All 50 rows have a Design planning allocation:
Reconcile owns #312 continuity, Publish/Finish/Merge preserve the #311 installed terminal, and Projection owns
standalone verifier failure evidence. The pre-`REQ-REV-142` Design review remains stale historical evidence; current
fresh Design review and deterministic closure have passed, and no fixture is reported as executed.

Read in this order:

1. [`test-strategy.md`](./test-strategy.md): evidence layers, selection, result and gate rules;
2. [`fixture-plan.md`](./fixture-plan.md): all 50 fixture owners, candidates, layers, recovery and acceptance;
3. [`traceability.md`](./traceability.md): Requirements/Design/capability closure;
4. [`manifest.yaml`](./manifest.yaml): candidate identity and authority locators.

Current as-built Test remains
[`current-main-0.6.5-guru.42` at selected base](https://github.com/castbox/guru-trellis/blob/5650df47fe17fe89b7cb616be6c9551608164832/docs/test/versions/current-main-0.6.5-guru.42/test-strategy.md).
Its `TST-036..039` / `SCN-048` additions are fact-only release-authority checks and do not add an Evolution fixture;
the prior `.41` / `.40` snapshots are comparison evidence only; `a41b8a34...9f560ec1` only corrects #267 lifecycle
evidence, dogfood provenance and archive/merge facts；`9f560ec1...736ef333` is a material platform-selection
runtime advance whose focused matrix is projected into the existing fixture rather than a new row；
`736ef333...5650df47` is another fact-only caller-inventory/provenance correction.
Coexistence is current/target documentation separation, not runtime dual-read or evidence reuse.

Allowed result states are `planned_not_executed`, `pass`, `fail`, `blocked`, `skip_unverified`. A historical or
different-candidate result can only be research evidence; it cannot change a row out of `planned_not_executed`.
