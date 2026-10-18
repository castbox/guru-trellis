# #454 C4 Branch Association Traceability

状态：`reviewed_promoted`。Expected current RDT/Architecture 为
`current-main-0.6.17-guru.61 / active`；promoted successor 为
`current-main-0.6.17-guru.62 / active`。

| Requirement | Design | Test | Inherited authority |
| --- | --- | --- | --- |
| `R454-C4-01` | `D454-C4-01`, `D454-C4-02` | `T454-C4-01`, `T454-C4-10` | `I-454-04`; `ADR-015`; repository-local application control identity |
| `R454-C4-02` | `D454-C4-01`, `D454-C4-02`, `D454-C4-06` | `T454-C4-01`, `T454-C4-04`, `T454-C4-08` | approved epoch/revision contract at `b695adc9` |
| `R454-C4-03` | `D454-C4-03`, `D454-C4-04` | `T454-C4-02` | `R-454-06` recovery matrix; new epoch only after complete control-state loss |
| `R454-C4-04` | `D454-C4-03`, `D454-C4-04`, `D454-C4-05` | `T454-C4-03`, `T454-C4-05`, `T454-C4-08` | live Git facts; expected-HEAD freshness; retained control-ref exclusion |
| `R454-C4-05` | `D454-C4-03` | `T454-C4-02`, `T454-C4-03` | C5 ownership owner isolation |
| `R454-C4-06` | `D454-C4-05`, `D454-C4-06` | `T454-C4-04`, `T454-C4-05`, `T454-C4-08` | `AC-454-18`; candidate label is not freshness |
| `R454-C4-07` | `D454-C4-06` | `T454-C4-05` | named reconcile boundary |
| `R454-C4-08` | `D454-C4-03`, `D454-C4-06` | `T454-C4-06` | resource incarnation exclusivity; epoch-aligned current set |
| `R454-C4-09` | `D454-C4-04`, `D454-C4-05`, `D454-C4-07`, `D454-C4-08`, `D454-C4-09` | `T454-C4-07`, `T454-C4-08` | exact epoch/HEAD-bound rollback and recovery |
| `R454-C4-10` | `D454-C4-09`, `D454-C4-10` | `T454-C4-09`, `T454-C4-10` | E434 activation ownership |

Architecture source reference：`architecture-contribution-454-task-lifecycle-state-model-c4-v1`。C5-C7、D443、
D436、E434、#434 activation 与完整 Release matrix 继续保持独立后续边界。Architecture/RDT owners 已按
expected `.61` 串行提升到 `.62`；后续 promotion-created diff 的 fresh Phase 2、Task Commit 与完整 Branch Review
仍须独立完成。

Finalizer provenance closure is intentionally mapped to existing shared authority rather than a second C4 identity:
`REQ-048` / `DES-046` / `TST-032` / `SCN-044` cover strict-ancestor initial reprepare, exact
`pre_push_remote_head` replacement binding and pre-mutation remote revalidation. The execution regression is located at
`trellis/skills/guru-team/packages/guru-finalize-task/tests/test_provenance.py`; it is evidence for this mapping only.

`FIN454-C4-P1-002` remains on the same mapping: `REQ-048` owns the transaction-bound Reactivate branch reuse condition,
`DES-046` owns identity-matched transaction authority plus Open-PR/terminal-PR/allowed-head classification, and
`TST-032/SCN-044` own pre-push single-fast-forward, publication-head output-loss convergence and drift rejection. No
broad fallback, manual PR-selection API, force push or second ledger is introduced. The focused recovery `47/47` and
complete Finalizer package `111/111` pass for the current implementation candidate; this trace does not record a fresh
Phase 2, Branch Review, Publication or Finalizer gate pass.

`FIN454-C4-P1-004` also remains on that mapping. `REQ-048` owns same-base fresh-reviewed reprepare under one matching
unbound transaction; `DES-046` owns predecessor-tail/base-lineage/current-review equality and Open-PR classification;
`TST-032/SCN-044` own both transaction endpoint positives plus intermediate-remote/Open-PR/identity negatives and
replacement-transaction binding. This adds no C4 authority identity or stricter session/path/branch binding.
