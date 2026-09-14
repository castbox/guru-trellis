# #410 Release v0.6.17-guru.1 Traceability

| Requirement | Design | Test | Architecture refs |
| --- | --- | --- | --- |
| `R410-01` | `D410-01` | `T410-01` | authority-binding |
| `R410-02` | `D410-01`, `D410-02` | `T410-01` | boundary-and-decision |
| `R410-03` | `D410-02` | `T410-02` | compatibility-and-exit |
| `R410-04` | `D410-01`, `D410-03` | `T410-02`, `T410-03` | owner-and-single-writer |
| `R410-05` | `D410-03` | `T410-03` | review-and-promotion |
| `R410-06` | `D410-04`, `D410-06` | `T410-04`, `T410-06` | evidence-and-freshness |
| `R410-07` | `D410-05`, `D410-06` | `T410-05`, `T410-06` | authority-binding |

`BEH-018` is covered by `D410-03..06` and `T410-03..06`. This contribution is
still a candidate and does not prove promotion, merge, tag, Release, or Issue
closure.
