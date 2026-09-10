# #392 Release v0.6.16-guru.1 Traceability

状态：`reviewed_promoted`；immutable superseded predecessor：
`current-main-0.6.5-guru.47`；promoted/current active successor：
`current-main-0.6.5-guru.48`。

| Requirement | Design | Test / Scenario | Architecture candidate refs |
| --- | --- | --- | --- |
| `R392-01` | `D392-01` | `T392-01` | `ARCH-CUR-025`, `EVD-024` |
| `R392-02` | `D392-01`, `D392-03` | `T392-01` | `ARCH-CUR-025`, `ARCH-INT-015`, `EVD-024` |
| `R392-03` | `D392-03` | `T392-01` | `ARCH-CUR-025`, `EVD-024` |
| `R392-04` | `D392-02`, `D392-06` | `T392-02`, `SCN-077` | `ARCH-CUR-025`, `ARCH-INT-015`, `EVD-024` |
| `R392-05` | `D392-04` | `T392-03`, `T392-04`, `SCN-077` | `ARCH-INT-015` |
| `R392-06` | `D392-04`, `D392-05` | `T392-05`, `SCN-078` | `ARCH-CUR-025`, `EVD-024` |
| `R392-07` | `D392-05` | `T392-05`, `SCN-078` | `ARCH-INT-015`, `EVD-024` |
| `R392-08` | `D392-04`, `D392-05` | `T392-06`, `SCN-078` | `ARCH-INT-015` |
| `R392-09` | `D392-06` | `T392-02`, `T392-06`, `SCN-077..078` | `ARCH-CUR-025`, `ARCH-INT-015` |

`BEH-017` 由 `D392-04..06` 承接，并由 `T392-04..06`、`SCN-077..078` 验证。
Requirements、Design 与 Test candidate 定义分别位于
[requirements.md](./requirements.md)、[design.md](./design.md) 与 [test.md](./test.md)。

Architecture delta locator 为
[#392 Architecture contribution](../../architecture/contributions/392-release-v0616-guru1.md)，
identity 为 `architecture-contribution-392-release-v0616-guru1-v2`。`ARCH-CUR-025`、
`ARCH-INT-015`、`EVD-024` 是已 promotion 的 `.48` current refs；public Architecture
inheritance 以 [baseline](../../architecture/README.md) /
`current-main-0.6.5-guru.48` / `active` 为 authority，`.47` 为 immutable predecessor。

本 contribution 绑定 Issue [#392](https://github.com/castbox/guru-trellis/issues/392)、
task `392-release-v0616-guru1`、expected predecessor `.47` 与 promoted successor `.48`。
promotion identity 不证明后续 Gate outcome；本 contribution 不记录动态 HEAD、
Gate/checkpoint、runtime state、时间、tag/Release 状态或用户授权。
