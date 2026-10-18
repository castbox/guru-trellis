# #332 Release current-fact alignment Traceability

| Requirement | Design owner | Test evidence | Architecture refs |
| --- | --- | --- | --- |
| `R332-AUTH-01` | `D332-AUTH-01`, `D332-AUTH-02` | `T332-AUTH-01` | `.43 -> .44`, single active authority |
| `R332-AUTH-02` | `D332-AUTH-02` | `T332-AUTH-01` | current release mapping |
| `R332-AUTH-03` | `D332-AUTH-03`, `D332-AUTH-04` | `T332-AUTH-02` | history preservation, navigation |
| `R332-AUTH-04` | `D332-AUTH-06`, `D332-AUTH-07` | `T332-AUTH-03`, `T332-AUTH-06` | #240/#348 reviewed contribution promotion, ADR-008 |
| `R332-AUTH-05` | `D332-AUTH-01`, `D332-AUTH-03`, `D332-AUTH-05` | `T332-AUTH-04` | single-writer, promotion freshness |
| `R332-AUTH-06` | `D332-AUTH-04` | `T332-AUTH-05` | exact-candidate boundary and close scope |
| `R332-AUTH-07` | `D332-AUTH-06`, `D332-AUTH-07` | `T332-AUTH-03`, `T332-AUTH-06` | review provenance and historical evidence preservation |

当前 source authority 是 live Issue #332；task planning locators 为
`.trellis/tasks/09-05-332-release-v0615-guru5-r2/{prd,design,implement}.md`。Architecture
delta 由 `docs/architecture/contributions/332-release-v0615-guru5.md` 承接。Architecture owner 已先
激活 `docs/architecture/README.md` / `.44` / `active`，RDT owner 随后将本 contribution 投影为继承
该 baseline 的 `.44` current authority。两份 contribution 不记录动态实施、Review、Publication、
Finalizer 或 release lifecycle 状态；promotion-created diff 的下一 route 是 fresh Phase 2。
