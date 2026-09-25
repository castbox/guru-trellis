# #454 D443 Bind Session Traceability

Status: contribution candidate based on `.64/active`; no shared authority has been promoted. Architecture candidate:
`architecture-contribution-454-task-lifecycle-d443-v1`; #456 migration rows `443-*` define the exact predecessor
retirement surface, and `ARCH-GAP-011` remains partial/open until E434.

| Requirement | Design | Test | Boundary |
| --- | --- | --- | --- |
| `R454-D443-01` | `D454-D443-01` | `T454-D443-01` | C2 TaskLifecycleDTO, C4 binding, C5 official session adapter |
| `R454-D443-02` | `D454-D443-01/02` | `T454-D443-02` | #456 `443-MAPPING-DEPENDENCY`, `443-MANUAL-RECOVERY`; branch/ownership owners unchanged |
| `R454-D443-03` | `D454-D443-03` | `T454-D443-03` | #456 success/blocked DTO and explicit-mode migration; E434 router owner |
| `R454-D443-04` | `D454-D443-04` | `T454-D443-04` | #456 selector/projection deferral, #434 graph and #410 Release matrix |

The old #443 task remains historical evidence. D436, E434, production cutover and Release proof are not credited
by this candidate.
