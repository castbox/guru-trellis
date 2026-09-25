# #454 C5 Session And Resource Control Traceability

状态：`reviewed_promoted`。Expected current RDT 为 `.62/active`；successor RDT 与 Architecture 为
`current-main-0.6.17-guru.63 / active`。

| Requirement | Design | Test | Inherited authority |
| --- | --- | --- | --- |
| `R454-C5-01` | `D454-C5-01`, `D454-C5-09` | `T454-C5-01`, `T454-C5-09` | `I-454-07`; `TaskLifecycleDTO`; Fixed Fork schema-2 record |
| `R454-C5-02` | `D454-C5-01`, `D454-C5-02` | `T454-C5-01` | official session store single-writer; no rollback |
| `R454-C5-03` | `D454-C5-01` | `T454-C5-02` | stable TaskId; generation invalidation; fresh TaskRef resolution |
| `R454-C5-04` | `D454-C5-03` | `T454-C5-03` | `I-454-08`; repository-local ownership authority |
| `R454-C5-05` | `D454-C5-05` | `T454-C5-04` | `R-454-06`; unknown ownership is caller-owned |
| `R454-C5-06` | `D454-C5-03`, `D454-C5-04` | `T454-C5-03`, `T454-C5-04` | C4 `OwnershipPort`; whole-ledger active recovery; exact-incarnation remote recovery; minimum-sufficient authority consistency |
| `R454-C5-07` | `D454-C5-06` | `T454-C5-05` | rebind resource-incarnation retention |
| `R454-C5-08` | `D454-C5-07`, `D454-C5-08` | `T454-C5-06` | `R-454-09`; Finish/Cleanup separation |
| `R454-C5-09` | `D454-C5-03`, `D454-C5-06` | `T454-C5-06` | `R-454-08`; portable remote identity |
| `R454-C5-10` | `D454-C5-01`, `D454-C5-05` | `T454-C5-07` | `I-454-06`; manual selection uses the same validator |
| `R454-C5-11` | `D454-C5-09`, `D454-C5-10` | `T454-C5-08`, `T454-C5-09` | E434 activation ownership |

Architecture source reference：`architecture-contribution-454-task-lifecycle-state-model-c5-v1`。C6-C7、D443、
D436、E434、#434 activation 与完整 Release matrix 继续保持独立后续边界。Promotion-created diff
须重新进入 fresh Phase 2、Task Commit 与完整 Branch Review。
