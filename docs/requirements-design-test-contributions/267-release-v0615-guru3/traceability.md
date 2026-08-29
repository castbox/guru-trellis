# #267 Release authority alignment Traceability

| Requirement | Design owner | Test evidence | Architecture refs |
| --- | --- | --- | --- |
| `R267-AUTH-01` | `D267-AUTH-02` | `T267-AUTH-01` | candidate identity / expected current |
| `R267-AUTH-02` | `D267-AUTH-03`, `D267-AUTH-04` | `T267-AUTH-01` | predecessor/successor / single writer |
| `R267-AUTH-03` | `D267-AUTH-06` | `T267-AUTH-02` | CURRENT release evidence |
| `R267-AUTH-04` | `D267-AUTH-04` | `T267-AUTH-03` | constitution / no ADR / no GAP change |
| `R267-AUTH-05` | `D267-AUTH-01`, `D267-AUTH-05` | `T267-AUTH-04`, `T267-AUTH-05` | review and promotion lifecycle |
| `R267-AUTH-06` | `D267-AUTH-03`, `D267-AUTH-05` | `T267-AUTH-05`, `T267-AUTH-06` | freshness / expected current |
| `R267-AUTH-07` | `D267-AUTH-07` | `T267-AUTH-07` | closure boundary |

Current source authority is live Issue #267 `2026-08-29-r18`; task planning locators are
`.trellis/tasks/08-29-267-release-v0615-guru3/{prd,design,implement}.md`。Architecture promotion 已先将
`docs/architecture/README.md` / `current-main-0.6.5-guru.42` / `active` 建立为 current baseline，
随后 RDT promotion 将本 contribution 投影到继承该 baseline 的 `current-main-0.6.5-guru.42`。
promotion-created diff 尚需 fresh Phase 2、commit 与 Branch Review。
