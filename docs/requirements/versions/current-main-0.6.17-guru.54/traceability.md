# Requirements Traceability

当前 .54 来源：`castbox/Trellis@43fffc170927c85d9f7fc106cc5a059e80d4530b` / CI `35190729418` / CLI/core `0.6.17`；Guru manifest `0.6.17-guru.42`；repository release target `v0.6.17-guru.1`。Architecture public inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.54` / `active`。
完整继承 immutable `.53` 业务合同，当前增量为 #419；旧 pin、release mapping、计数及 promotion/evidence 叙述只绑定其明确历史版本。当前 graph 见 Design inventory，旧验证不证明本次 candidate。

`.54` 完整继承 `.53`，吸收 reviewed #419 contribution；Architecture 与 RDT 共享 `.54/active` current identity。promotion-created diff 必须重新通过 fresh Phase 2、Task Commit、完整 Branch Review 后才能进入 Publication；本文不声明下游门禁已通过。

| Requirement / Behavior | Design | Test | Architecture |
| --- | --- | --- | --- |
| `REQ-001`, `BEH-001..006` | `DES-004`, `DES-005` | `TST-004`, `SCN-001..004` | `ARCH-CUR-001`, `ARCH-DOM-001` |
| `REQ-002`, `REQ-003` | `DES-001`, `DES-002` | `TST-002`, `CASE-001` | `ARCH-FND-001` |
| `REQ-004` | `DES-003`, `CON-002` | `TST-003`, `CASE-002` | `ARCH-FND-002` |
| `REQ-005` | `DES-004`, `DES-005` | `TST-004`, `SCN-003` | `ARCH-DOM-002` |
| `REQ-006` | `DES-006` | `TST-005`, `SCN-005` | `ARCH-INT-001` |
| `REQ-007`, `BEH-007` | `DES-007` | `TST-006`, `SCN-006` | `ARCH-CUR-003` |
| `REQ-008` | `CON-001` | `TST-007`, `CASE-001` | `ARCH-GOV-001` |
| `NFR-001` | `DES-006`, `DES-010` | `TST-005`, `SCN-005` | `ARCH-INT-001` |
| `NFR-002..003` | `CON-002..003`, `DES-010` | `TST-003`, `TST-007` | `ARCH-GOV-001` |
| `REQ-009`, `NFR-004` | `DES-008` | `TST-001`, `TST-008` | `ARCH-GAP-001` |
| `REQ-010`, `NFR-005` | `DES-003` | `TST-003` | `ARCH-FND-003` |
| `REQ-011`, `BEH-008` | `DES-005`, `DES-009` | `TST-010`, `SCN-003` | `ARCH-DOM-002` |
| `REQ-012` | `DES-004`, `DES-011` | `TST-011`, `SCN-004` | `ARCH-DOM-002` |
| `REQ-013`, `BEH-009` | `DES-006`, `DES-010` | `TST-005`, `TST-007`, `SCN-005` | `ARCH-INT-001` |
| `REQ-014`, `BEH-010` | `DES-012`, `CON-004` | `TST-012`, `SCN-009` | `ARCH-CUR-007`, `ARCH-DOM-002` |
| `REQ-015` | `DES-013` | `TST-013`, `SCN-010` | `ARCH-INT-001` |
| `REQ-016`, `REQ-017`, `BEH-011` | `DES-014`, `DES-015`, `DES-017` | `TST-014`, `SCN-011..012` | `ARCH-CUR-008`, `ARCH-INT-006` |
| `REQ-018` | `DES-016` | `TST-015`, `SCN-013` | `ARCH-CUR-009` |
| `REQ-019` | `DES-014`, `DES-017` | `TST-016`, `SCN-014` | `ARCH-CUR-003`, `ARCH-INT-004` |
| `REQ-020` | `DES-018` | `TST-017`, `SCN-015..016` | `ARCH-DOM-007`, `ARCH-CUR-010` |
| `REQ-027`, `REQ-028` | `DES-026`, `DES-027`, `DES-032` | `TST-018`, `SCN-028`, `SCN-031..032` | `ARCH-GOV-006`, `ARCH-DOM-008` |
| `REQ-029` | `DES-028` | `TST-019`, `SCN-024` | `ARCH-FND-006` |
| `REQ-030` | `DES-029` | `TST-020`, `SCN-024..027` | `ARCH-FND-006`, `ARCH-GOV-006` |
| `REQ-031` | `DES-026`, `DES-029..030`, `DES-033` | `TST-021`, `SCN-025..028` | `ARCH-GOV-007`, `ARCH-DOM-008` |
| `REQ-032` | `DES-030..032` | `TST-018`, `TST-022`, `SCN-029`, `SCN-033` | `ARCH-INT-007`, `ARCH-GAP-006` |
| `REQ-033` | `DES-027`, `DES-033` | `TST-023`, `SCN-031..032` | `ARCH-GOV-008`, `ADR-005` |
| `REQ-034` | `DES-033` | `TST-024`, `SCN-030` | `ARCH-GOV-008` |
| `REQ-035` | `DES-034` | `TST-025..026`, `SCN-024..033` | `ARCH-INT-007`, `ARCH-GAP-006` |
| `REQ-036`, `REQ-037` | `DES-035`, `DES-036` | `TST-027`, `SCN-034..035` | `ARCH-CUR-013`, `ADR-006` |
| `REQ-038`, `REQ-039`, `REQ-040` | `DES-037..039` | `TST-027..028`, `SCN-034..037` | `ARCH-CUR-013`, `ADR-006` |
| `REQ-041`, `REQ-042` | `DES-040`, `DES-041` | `TST-028`, `TST-029`, `SCN-038..039` | `ARCH-CUR-013` |
| `REQ-043` | `DES-042` | `TST-030`, `SCN-040` | `EVD-014`, 独立的重构前稳定版 Release boundary |
| `REQ-044` | `DES-043` | `TST-029`, `SCN-039` | `ARCH-CUR-013` |
| `REQ-045` | `DES-044` | `TST-007`, `TST-029`, `SCN-039` | `ARCH-CUR-013` |
| `REQ-046` | `DES-006`, `DES-010`, `DES-042` | `TST-005`, `TST-007`, `TST-030`, `SCN-005`, `SCN-040` | `EVD-014`, 独立的重构前稳定版 Release boundary |
| `REQ-047` | `DES-045`, `DES-046` | `TST-031`, `SCN-041..043` | `ARCH-CUR-014`, `ARCH-INT-008`, `ADR-007` |
| `REQ-048`, `BEH-008`, `BEH-010` | `DES-046` | `TST-032`, `SCN-044` | `ARCH-CUR-014`, `ARCH-GAP-007` |
| `REQ-049` | `DES-045..047` | `TST-032..033`, `SCN-043..045` | `ARCH-DOM-009`, `ADR-007` |
| `REQ-050` | `DES-047` | `TST-033..034`, `SCN-045`, `SCN-047` | `ARCH-INT-001`, `EVD-015` |
| `REQ-051` | `DES-048` | `TST-035`, `SCN-046` | `ARCH-CUR-015`, `ARCH-DOM-009`, `EVD-015` |
| `REQ-052` | `DES-049..051` | `TST-036..037` | `ARCH-CUR-004`, `ARCH-CUR-008`, `EVD-016` |
| `REQ-053` | `DES-051..052` | `TST-037`, `TST-039` | `ARCH-GAP-007`, `EVD-016` |
| `REQ-054` | `DES-049..051` | `TST-038` | `ARCH-FND-006`, `ARCH-GOV-006..008`, `EVD-016` |
| `REQ-055` | `DES-049`, `DES-052` | `TST-036`, `TST-039` | `ARCH-CUR-011..012`, `EVD-016` |
| `REQ-056` | `DES-053`, `CON-005` | `TST-040`, `SCN-053` | `ARCH-CUR-002`, `ARCH-CUR-017`, `ARCH-DOM-010`, `ARCH-INT-001`, `EVD-017` |
| `REQ-057` | `DES-054`, `DES-056` | `TST-041`, `CASE-003` | `ARCH-CUR-017`, `ARCH-GOV-006..008`, `ARCH-INT-009`, `ARCH-GAP-007`, `EVD-017` |
| `REQ-058`, `BEH-012` | `DES-055`, `CON-006` | `TST-041..042`, `SCN-049..050` | `ARCH-CUR-006`, `ARCH-CUR-017`, `ARCH-DOM-002`, `ARCH-DOM-010`, `ARCH-INT-009` |
| `REQ-059` | `DES-057` | `TST-044` | `ARCH-DOM-002`, `ARCH-INT-009`, `EVD-017` |
| `REQ-060`, `NFR-006` | `DES-057..058` | `TST-042..044`, `SCN-049..052` | `ARCH-DOM-010`, `ARCH-GOV-001`, `ARCH-GOV-008`, `ARCH-INT-009` |
| `REQ-061` | `DES-054`, `DES-056`, `DES-059` | `TST-041`, `TST-045`, `CASE-003` | `ARCH-INT-009`, `ARCH-GAP-006..007` |
| `REQ-062`, `BEH-012` | `DES-056`, `DES-059`, `CON-006` | `TST-044..045`, `CASE-004` | `ARCH-CUR-017`, `ARCH-DOM-002`, `ARCH-DOM-010`, `ARCH-INT-001`, `ARCH-INT-009`, `ARCH-GAP-007`, `EVD-017` |
| `REQ-063` | `DES-060` | `TST-046`, `SCN-054` | `ARCH-CUR-002`, `ARCH-CUR-018`, `EVD-018` |
| `REQ-064` | `DES-061` | `TST-047`, `SCN-054` | `ARCH-CUR-014..018`, `ARCH-INT-008..009`, `EVD-018` |
| `REQ-065` | `DES-060`, `DES-062` | `TST-046`, `TST-048` | `ARCH-CUR-018`, `ARCH-INT-001`, `EVD-018` |
| `REQ-066`, `BEH-013` | `DES-061`, `DES-063` | `TST-047`, `TST-049`, `SCN-054` | `ARCH-CUR-018`, `ARCH-GOV-006..008`, `ARCH-GAP-007`, `EVD-018` |
| `REQ-067`, `BEH-013` | `DES-063` | `TST-049..050`, `SCN-054`, `CASE-003` | `ARCH-CUR-018`, `ARCH-INT-001`, `ARCH-INT-008..009`, `ARCH-GAP-007`, `EVD-018` |
| `REQ-068`, `BEH-013` | `DES-064`, `CON-006` | `TST-050`, `CASE-004` | `ARCH-CUR-018`, `ARCH-DOM-002`, `ARCH-DOM-010`, `EVD-018` |
| `REQ-069`, `BEH-014` | `DES-065`, `DES-066` | `TST-051..052`, `SCN-055..056` | `ARCH-CUR-019`, `ARCH-DOM-011`, `ARCH-INT-010`, `ADR-008`, `EVD-019` |
| `REQ-070` | `DES-066` | `TST-052`, `SCN-055..056` | `ARCH-CUR-019`, `ADR-008` |
| `REQ-071`, `BEH-015` | `DES-067`, `CON-007` | `TST-053`, `SCN-057..058` | `ARCH-CUR-020`, `ARCH-DOM-012`, `ARCH-INT-011`, `EVD-020` |
| `REQ-072`, `BEH-015` | `DES-067`, `DES-068`, `CON-007` | `TST-053..054`, `SCN-057..058` | `ARCH-CUR-020`, `ARCH-DOM-012`, `ARCH-INT-011` |
| `REQ-073` | `DES-065`, `DES-067` | `TST-051`, `TST-055` | `ARCH-CUR-001`, `ARCH-CUR-018..020`, `EVD-018..020` |
| `REQ-074` | `DES-069..070` | `TST-056`, `SCN-059..060` | `ARCH-CUR-021`, `ARCH-INT-012`, `EVD-021` |
| `REQ-075..076` | `DES-070..072` | `TST-057..058`, `TST-061`, `SCN-059..060` | `ARCH-CUR-021`, `ARCH-DOM-013`, `EVD-021` |
| `REQ-077` | `DES-069`, `DES-072`, `DES-075` | `TST-056`, `TST-060` | `ARCH-CUR-021`, `ARCH-INT-012`, `EVD-021` |
| `REQ-078..079` | `DES-073..074`, `DES-076` | `TST-059`, `SCN-061` | `ARCH-INT-012`, `EVD-021` |
| `REQ-080` | `DES-075` | `TST-060` | `ARCH-INT-012`, `ARCH-DOM-013`, `EVD-021` |
| `REQ-081` | `DES-071`, `DES-077..078` | `TST-057..058`, `TST-061`, `SCN-062..063` | `ARCH-CUR-021`, `ARCH-DOM-013`, `EVD-021` |
| `REQ-082` | `DES-079` | `TST-062`, `SCN-064..065` | `ARCH-CUR-022`, `ARCH-GOV-006..008`, `EVD-021` |
| `REQ-083` | `DES-080` | `TST-063`, `SCN-066` | `ARCH-CUR-022`, `ARCH-INT-009`, `EVD-021` |
| `REQ-084` | `DES-081` | `TST-064`, `SCN-067` | Guru finish exclusivity and incomplete-closeout fail closed |
| `REQ-085` | `DES-082` | `TST-065`, `SCN-068` | Branch Review visibility and pass timing |
| `REQ-086` | `DES-083` | `TST-066`, `SCN-069` | displayed-action confirmation continuity |
| `REQ-087` | `DES-084` | `TST-067`, `SCN-070..071` | `ARCH-CUR-023`, `ARCH-DOM-014`, `EVD-022` |
| `REQ-088`, `BEH-016` | `DES-084`, `DES-087` | `TST-067..068`, `SCN-070..073` | `ARCH-CUR-023`, `ARCH-INT-013`, `EVD-022` |
| `REQ-089` | `DES-085..086` | `TST-067`, `TST-069`, `SCN-071..072` | `ARCH-CUR-023`, `ARCH-DOM-014`, `EVD-022` |
| `REQ-090`, `BEH-016` | `DES-087..088` | `TST-068`, `TST-070..071`, `SCN-073..074` | `ARCH-CUR-023`, `ARCH-INT-013`, `EVD-022` |
| `REQ-091` | `DES-088` | `TST-071`, `SCN-075` | `ARCH-INT-013`, `EVD-022` |
| `REQ-092` | `DES-086`, `DES-089` | `TST-069`, `TST-072..073`, `SCN-076` | `ARCH-CUR-023`, `ARCH-DOM-014`, `EVD-022` |

引用仅传 identity、locator、version/status，不复制正文。

## #378 Trace

| Requirement | Design | Test | Architecture |
| --- | --- | --- | --- |
| R378-01 | D378-01 | T378-01, T378-04 | ARCH-CUR-024, ARCH-INT-014, EVD-023 |
| R378-02 | D378-02 | T378-02 | ARCH-CUR-024, ARCH-INT-014, EVD-023 |
| R378-03 | D378-03 | T378-03, T378-04 | ARCH-CUR-024, ARCH-INT-014, EVD-023 |
| R378-04 | D378-04 | T378-05 | ARCH-CUR-024, ARCH-INT-014, EVD-023 |

定义定位：同版本 Requirements requirement-main.md、Design design-main.md、Test test-strategy.md；R378-01 的 pin 与对应 source evidence 是历史，current pin 见 R408-01，其余继承机制关系为 implements/verifies。原 contribution 保留 promotion 来源引用，不再重复 current 正文。

## #392 Trace

| Requirement | Design | Test / Scenario | Architecture |
| --- | --- | --- | --- |
| `R392-01` | `D392-01` | `T392-01` | `ARCH-CUR-025`, `EVD-024` |
| `R392-02` | `D392-01`, `D392-03` | `T392-01` | `ARCH-CUR-025`, `ARCH-INT-015`, `EVD-024` |
| `R392-03` | `D392-03` | `T392-01` | `ARCH-CUR-025`, `EVD-024` |
| `R392-04` | `D392-02`, `D392-06` | `T392-02`, `SCN-077` | `ARCH-CUR-025`, `ARCH-INT-015`, `EVD-024` |
| `R392-05` | `D392-04` | `T392-03`, `T392-04`, `SCN-077` | `ARCH-INT-015`, `EVD-024` |
| `R392-06` | `D392-04`, `D392-05` | `T392-05`, `SCN-078` | `ARCH-CUR-025`, `EVD-024` |
| `R392-07` | `D392-05` | `T392-05`, `SCN-078` | `ARCH-INT-015`, `EVD-024` |
| `R392-08` | `D392-04`, `D392-05` | `T392-06`, `SCN-078` | `ARCH-INT-015` |
| `R392-09` | `D392-06` | `T392-02`, `T392-06`, `SCN-077..078` | `ARCH-CUR-025`, `ARCH-INT-015` |

`BEH-017` 由 `D392-04..06` 承接，并由 `T392-04..06`、`SCN-077..078` 验证。
定义定位：本版本 Requirements `requirement-main.md`、Design `design-main.md`、Test
`test-strategy.md` / `test-plan.md`。reviewed promotion 来源保留在
`docs/requirements-design-test-contributions/392-release-v0616-guru1/`；其稳定状态为
`reviewed_promoted`，`.47` 是 immutable predecessor，`.48` 是该 promotion 的 immutable superseded successor。
该 promotion identity 不证明后续 Phase 2、Branch Review 或发布 gate outcome。

## #329 Trace

| Requirement / Behavior | Design | Test / Scenario | Architecture |
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

`BEH-018` 由 `D329-03..07` 承接，并由 `T329-04..07`、`SCN-079..083` 验证。
reviewed promotion 来源保留在
`docs/requirements-design-test-contributions/329-adopt-developer-free-trellis/`；`.48` 是 immutable
predecessor，`.49` 是 #329 promotion 建立的 immutable superseded authority。promotion 不证明后续
Phase 2、Publication 或远端动作。


## #408 Trace

| Requirement | Design | Test | Architecture / Evidence |
| --- | --- | --- | --- |
| `R408-01` | `D408-01` | `T408-01` | `ARCH-CUR-028`, `ARCH-INT-014`, `EVD-027` |
| `R408-02` | `D408-02`, `D408-04` | `T408-02`, `T408-08` | `ARCH-INT-014`, `ARCH-INT-016`, `EVD-027` |
| `R408-03` | `D408-02`, `D408-04`, `D408-05` | `T408-03` | `ARCH-CUR-028`, `ARCH-INT-016`, `EVD-027` |
| `R408-04` | `D408-03`, `D408-04`, `D408-05` | `T408-04` | `ARCH-CUR-028`, `ARCH-DOM-015`, `EVD-027` |
| `R408-05` | `D408-03` | `T408-05` | `ARCH-CUR-028`, `EVD-027` |
| `R408-06` | `D408-03` | `T408-06` | `ARCH-CUR-028`, `ARCH-DOM-015`, `EVD-027` |
| `R408-07` | `D408-03` | `T408-07` | `ARCH-CUR-028`, `ARCH-DOM-015`, `EVD-027` |
| `R408-08` | `D408-04` | `T408-08` | `EVD-027` |

状态：`.51` immutable superseded history，关系为 implements/verifies。定义分别位于
[Requirements](./requirement-main.md)、[Design](../../../design/versions/current-main-0.6.17-guru.54/design-main.md)、
[Test](../../../test/versions/current-main-0.6.17-guru.54/test-strategy.md)；反向索引为同版本
[Design trace](../../../design/versions/current-main-0.6.17-guru.54/traceability.md) 与
[Test trace](../../../test/versions/current-main-0.6.17-guru.54/traceability.md)。
Architecture 历史继承为 `.51` / `superseded`；current public identity 见
[`.53` active](../../../architecture/README.md)。证据见
[Test 计划](../../../test/versions/current-main-0.6.17-guru.54/test-plan.md) 与
[EVD-027](../../../architecture/evidence/current-evidence.md)。
R408-01 supersedes R329-01 的旧 pin only；R378-01 的旧 pin 为 history，R329-02..10 与其余
R378 合同继承。`.50` 保持 immutable；本关系不声明 post-promotion gate 或 release 完成。

## #410 Trace

| Requirement | Design | Test | Architecture |
| --- | --- | --- | --- |
| `R410-01` | `D410-01` | `T410-01`, `T410-05` | `ARCH-CUR-029` |
| `R410-02` | `D410-01`, `D410-02` | `T410-01` | `ARCH-CUR-029` |
| `R410-03` | `D410-02` | `T410-02` | `ARCH-CUR-029`, `ARCH-INT-014` |
| `R410-04` | `D410-01`, `D410-03`, `D410-05` | `T410-02`, `T410-05` | `ARCH-CUR-029`, `ARCH-INT-016` |
| `R410-05` | `D410-03` | `T410-03` | `ARCH-INT-015` |
| `R410-06` | `D410-04`, `D410-06` | `T410-04`, `T410-05`, `T410-07`, `T410-08` | `ARCH-CUR-029`, `ARCH-INT-015` |
| `R410-07` | `D410-05`, `D410-06` | `T410-06`, `T410-08` | `ARCH-CUR-029`, `ARCH-INT-015` |

`BEH-018` 由 `D410-03..06` 承接，并由 `T410-03..08` 验证。状态为
`reviewed_promoted`；`.51` 是 immutable predecessor，`.52` 是 #410 建立的 immutable superseded authority。
本 trace 只记录 stable contract，不声明 post-promotion gate、tag、GitHub Release 或 Issue closure 完成。

## #418 Trace

| Requirement | Design | Test |
| --- | --- | --- |
| R418-01 | D418-01 | T418-01, T418-02, T418-03 |
| R418-02 | D418-01, D418-03, D418-04 | T418-02, T418-08, T418-09 |
| R418-03 | D418-02 | T418-04 |
| R418-04 | D418-03, D418-04, D418-05, D418-06 | T418-05, T418-08, T418-10, T418-12, T418-14 |
| R418-05 | D418-03, D418-04, D418-05, D418-06 | T418-06, T418-09, T418-11, T418-12, T418-13 |
| R418-06 | D418-01, D418-02, D418-03, D418-04, D418-05, D418-06 | T418-01, T418-02, T418-03, T418-04, T418-05, T418-06, T418-07, T418-08, T418-09, T418-10, T418-11, T418-12, T418-13, T418-14 |
| R418-07 | D418-02, D418-03 | T418-07, T418-11 |

定义：[Requirements](../../../requirements/versions/current-main-0.6.17-guru.54/requirement-main.md)、
[Design](../../../design/versions/current-main-0.6.17-guru.54/design-main.md)、
[Test](../../../test/versions/current-main-0.6.17-guru.54/test-strategy.md)。
反向索引：[Requirements trace](../../../requirements/versions/current-main-0.6.17-guru.54/traceability.md)、
[Design trace](../../../design/versions/current-main-0.6.17-guru.54/traceability.md)、
[Test trace](../../../test/versions/current-main-0.6.17-guru.54/traceability.md)。
关系为 implements/verifies；来源为 [#418 contribution](../../../requirements-design-test-contributions/418-closeout-identity-recovery/manifest.yaml)，
predecessor .52 -> successor .53；Architecture inheritance 为 .53/active，仅引用
[ADR-010](../../../architecture/adr/010-archived-review-authority.md)、
[ARCH-CUR-030](../../../architecture/01-current/system.md)、
[ARCH-INT-018](../../../architecture/04-integrations/distribution.md)、
[EVD-028](../../../architecture/evidence/current-evidence.md)，不复制正文。

## #419 Trace

| Requirement | Design | Test | Architecture / Evidence |
| --- | --- | --- | --- |
| `R419-01` | `D419-01..02` | `T419-01` | `ARCH-CUR-031`, `ARCH-INT-019`, `ADR-011` |
| `R419-02` | `D419-03` | `T419-02` | `ARCH-DOM-016`, `ARCH-GOV-010` |
| `R419-03..04` | `D419-02`, `D419-04..05` | `T419-03..05` | `ARCH-CUR-031`, `ARCH-DOM-016`, `ADR-011` |
| `R419-05` | `D419-06` | `T419-06` | `ARCH-INT-019`, `ARCH-GOV-010` |
| `R419-06` | `D419-07` | `T419-07` | `ARCH-DOM-005`, `ARCH-INT-019` |
| `R419-07` | `D419-08..10` | `T419-08..10` | `EVD-029` |

状态为 `reviewed_promoted`；`.53` 是 immutable predecessor，`.54` 是 #419 successor。
来源为 [#419 contribution](../../../requirements-design-test-contributions/419-active-task-continuation/manifest.yaml)。
