# #332 Release current-fact alignment Traceability

| Requirement | Design owner | Test evidence | Architecture refs |
| --- | --- | --- | --- |
| `R332-AUTH-01` | `D332-AUTH-01`, `D332-AUTH-02` | `T332-AUTH-01` | `.43 -> .44`, single active authority |
| `R332-AUTH-02` | `D332-AUTH-02` | `T332-AUTH-01` | current release mapping |
| `R332-AUTH-03` | `D332-AUTH-03`, `D332-AUTH-04` | `T332-AUTH-02` | history preservation, navigation |
| `R332-AUTH-04` | `D332-AUTH-05` | `T332-AUTH-03` | target_native, no ADR/GAP/API change |
| `R332-AUTH-05` | `D332-AUTH-01`, `D332-AUTH-03`, `D332-AUTH-05` | `T332-AUTH-04` | single-writer, promotion freshness |
| `R332-AUTH-06` | `D332-AUTH-04` | `T332-AUTH-05` | exact-candidate boundary and close scope |

当前 source authority 是 live Issue #332；task planning locators 为
`.trellis/tasks/09-05-332-release-v0615-guru5-r2/{prd,design,implement}.md`。Architecture
delta 由 `docs/architecture/contributions/332-release-v0615-guru5.md` 承接。两份 contribution
均不拥有 shared-current promotion，也不记录动态实施、Review、Publication、Finalizer 或
release lifecycle 状态。
