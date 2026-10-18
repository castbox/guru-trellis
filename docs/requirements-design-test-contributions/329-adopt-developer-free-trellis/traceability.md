# #329 Developer-free Trellis adoption Traceability

状态：`reviewed_promoted`；promotion input：`current-main-0.6.5-guru.48`；current successor：
`current-main-0.6.5-guru.49`。

| Requirement | Design | Test / Scenario | Architecture candidate refs |
| --- | --- | --- | --- |
| `R329-01` | `D329-01` | `T329-01` | `ARCH-CUR-026`, `EVD-025` |
| `R329-02` | `D329-01`, `D329-02` | `T329-02`, `SCN-079..080` | `ARCH-INT-016` |
| `R329-03` | `D329-02`, `D329-03`, `D329-06` | `T329-03..04`, `SCN-079`, `SCN-082` | `ARCH-CUR-026` |
| `R329-04` | `D329-04` | `T329-05`, `SCN-081` | `ARCH-CUR-026` |
| `R329-05` | `D329-03` | `T329-04`, `SCN-082` | `ARCH-CUR-026` |
| `R329-06` | `D329-05` | `T329-06`, `SCN-083` | `EVD-025` |
| `R329-07` | `D329-02`, `D329-06` | `T329-03`, `T329-08` | `ARCH-INT-016` |
| `R329-08` | `D329-08` | `T329-08` | `ARCH-CUR-026`, `ARCH-INT-016` |
| `R329-09` | `D329-02`, `D329-07` | `T329-02`, `T329-07`, `SCN-079..082`, `SCN-084` | `ARCH-INT-016`, `EVD-025` |
| `R329-10` | `D329-07`, `D329-08` | `T329-01..08`, `SCN-084` | `EVD-025` |

`BEH-018` 由 `D329-03..07` 承接，并由 `T329-04..07` 与 `SCN-079..083` 验证；`SCN-084`
独立承接未发布 sample、clean source provenance 与 additive capability comparison，不扩大 legacy lifecycle 行为。
Architecture delta locator 为
[`docs/architecture/contributions/329-adopt-developer-free-trellis.md`](../../architecture/contributions/329-adopt-developer-free-trellis.md)，
identity 为 `architecture-contribution-329-developer-free-trellis-v1`。

本 contribution 不记录动态 HEAD、Gate/checkpoint、执行时间、用户授权、tag/Release 状态或未执行的
验证结果。`.48` 保持 immutable promotion input；`.49` 是唯一 active shared authority。
