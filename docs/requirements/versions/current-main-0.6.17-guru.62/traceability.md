# Requirements Traceability

当前 .62 来源：`castbox/Trellis@eb370008c7689d4e272ae626bd002190ecbb3296` / CI `35621578090` / CLI/core `0.6.17`；Guru manifest `0.6.17-guru.42`；repository release target `v0.6.17-guru.1`。Architecture public inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.62` / `active`。
完整继承 immutable `.61` 业务合同，当前增量为 #454 C4 branch association；current registry 保持 32 packages / 142 exits / 102 commands并增加三个 planned IDs，production workflow 保持 22 mandatory invokes / 98 exits。

`.62` 完整继承 `.61`，吸收 reviewed #454 C4 contribution；RDT 与 Architecture current 均为 `.62/active`。promotion-created diff 必须重新通过 fresh Phase 2、Task Commit、完整 Branch Review 后才能进入 Publication；剩余 lifecycle migration、#434 activation、tag 与 Release 未完成。

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
[Requirements](./requirement-main.md)、[Design](../../../design/versions/current-main-0.6.17-guru.56/design-main.md)、
[Test](../../../test/versions/current-main-0.6.17-guru.56/test-strategy.md)；反向索引为同版本
[Design trace](../../../design/versions/current-main-0.6.17-guru.56/traceability.md) 与
[Test trace](../../../test/versions/current-main-0.6.17-guru.56/traceability.md)。
Architecture 历史继承为 `.51` / `superseded`；current public identity 见
[`README.md`](../../../architecture/README.md) / `current-main-0.6.17-guru.56` / `active`。证据见
[Test 计划](../../../test/versions/current-main-0.6.17-guru.56/test-plan.md) 与
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

定义：[Requirements](./requirement-main.md)、
[Design](../../../design/versions/current-main-0.6.17-guru.56/design-main.md)、
[Test](../../../test/versions/current-main-0.6.17-guru.56/test-strategy.md)。
反向索引：[Requirements trace](./traceability.md)、
[Design trace](../../../design/versions/current-main-0.6.17-guru.56/traceability.md)、
[Test trace](../../../test/versions/current-main-0.6.17-guru.56/traceability.md)。
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

## #435 Trace

| Requirement | Design | Test | Architecture / Boundary |
| --- | --- | --- | --- |
| `R435-01` | `D435-01` | `T435-01..04` | Delivery Review semantic owner |
| `R435-02` | `D435-02`, `D435-06` | `T435-05..10` | Delivery Publish transaction / #405 equal-head recovery |
| `R435-03` | `D435-03`, `D435-07` | `T435-11..16` | merge-only mutation / terminal recovery |
| `R435-04` | `D435-04` | `T435-17..22` | current-slice policy / existing gate owners |
| `R435-05` | `D435-05` | `T435-23..28` | cross-branch Git/GitHub discovery / no ledger |
| `R435-06` | `D435-04..05` | `T435-29..33` | #436 Reactivate binding boundary |
| `R435-07` | `D435-08` | `T435-34..39` | #407 resolved-tree reconciliation |
| `R435-08` | `D435-09` | `T435-40..45` | additive deferred distribution / #434 activation boundary |

状态为 `reviewed_promoted`；`.54` 是 immutable predecessor，`.55` 是 #435 RDT successor。
来源为 [#435 contribution](../../../requirements-design-test-contributions/435-active-task-delivery-loop/manifest.yaml)。

## #436 Trace

| Requirement | Design | Test | Architecture |
| --- | --- | --- | --- |
| `R436-01` | `D436-01`, `D436-07` | `T436-01..10` | `ARCH-CUR-033`, `ARCH-DOM-018` |
| `R436-02` | `D436-02`, `D436-07` | `T436-11..17` | `ARCH-DOM-018`, `ARCH-INT-021` |
| `R436-03` | `D436-03`, `D436-08` | `T436-18..30` | `ARCH-DOM-018`, `ADR-013` |
| `R436-04` | `D436-04`, `D436-07` | `T436-31..35` | `ARCH-DOM-018`, `ARCH-INT-021` |
| `R436-05` | `D436-05`, `D436-08` | `T436-36..48` | `ARCH-DOM-018`, `ADR-013` |
| `R436-06` | `D436-06`, `D436-07` | `T436-49..56` | `ARCH-CUR-033`, `ARCH-INT-021`, `EVD-031` |

状态为 `reviewed_promoted`；`.55` 是 immutable predecessor，`.56` 是 #436 RDT successor。
来源为 [#436 contribution](../../../requirements-design-test-contributions/436-post-delivery-completion-finish/manifest.yaml)。
Promotion 不证明后续 fresh Phase 2、Task Commit、Branch Review、Publication 或远端 mutation。

## #443 Trace

| Requirement | Design | Test | Architecture |
| --- | --- | --- | --- |
| `R443-01` | `D443-01`, `D443-03` | `T443-05..11` | `ARCH-CUR-034`, `ARCH-DOM-019` |
| `R443-02` | `D443-01`, `D443-06` | `T443-01..04`, `T443-19..20` | `ARCH-DOM-019`, `ADR-014` |
| `R443-03` | `D443-03`, `D443-05` | `T443-05..08`, `T443-12..15` | `ARCH-DOM-019`, `EVD-032` |
| `R443-04` | `D443-03..04` | `T443-05..11` | `ARCH-INT-022`, `ADR-014` |
| `R443-05` | `D443-05`, `D443-07` | `T443-12..15` | `ARCH-GAP-009`, `ADR-014` |
| `R443-06` | `D443-04..05` | `T443-16..18` | `ARCH-DOM-019`, `EVD-032` |
| `R443-07` | `D443-02`, `D443-06` | `T443-01..04` | `ARCH-INT-022` |
| `R443-08` | `D443-07` | `T443-19..20` | `ARCH-CUR-034`, `ARCH-INT-022`, `EVD-032` |

状态为 `reviewed_promoted`；`.56` 是 immutable predecessor，`.57` 是 #443 RDT successor。
来源为 [#443 contribution](../../../requirements-design-test-contributions/443-task-identity-session-binding/manifest.yaml)。
Promotion 不证明本 combined diff 的 fresh Phase 2、Task Commit、Branch Review、Publication 或远端 mutation。

## #452 Trace

| Requirement | Design | Test | Architecture |
| --- | --- | --- | --- |
| `R452-01` | `D452-01..02` | `T452-01`, `T452-05` | `architecture-contribution-452-all-platform-projection-v1` |
| `R452-02` | `D452-01`, `D452-07` | `T452-01..02`, `T452-09` | `architecture-contribution-452-all-platform-projection-v1` |
| `R452-03` | `D452-03..04`, `D452-09` | `T452-02`, `T452-09`, `T452-11` | `architecture-contribution-452-all-platform-projection-v1` |
| `R452-04` | `D452-02..04` | `T452-03..04` | `architecture-contribution-452-all-platform-projection-v1` |
| `R452-05` | `D452-03..04` | `T452-04..05` | `architecture-contribution-452-all-platform-projection-v1` |
| `R452-06` | `D452-03`, `D452-05` | `T452-05..06` | `architecture-contribution-452-all-platform-projection-v1` |
| `R452-07` | `D452-02`, `D452-05` | `T452-06`, `T452-10` | `architecture-contribution-452-all-platform-projection-v1` |
| `R452-08` | `D452-06` | `T452-07`, `T452-11` | `architecture-contribution-452-all-platform-projection-v1` |
| `R452-09` | `D452-07..09` | `T452-08..11` | `architecture-contribution-452-all-platform-projection-v1` |
| `R452-10` | `D452-08..10` | `T452-09..12` | `architecture-contribution-452-all-platform-projection-v1` |

状态为 `reviewed_promoted`；`.57` 是 immutable predecessor，`.58` 是 #452 RDT successor。
来源为 [#452 contribution](../../../requirements-design-test-contributions/452-all-platform-support/manifest.yaml)。
Architecture shared current 为 `current-main-0.6.17-guru.58/active`；表中 identity 仅引用
`reviewed_candidate` task-owned Architecture contribution，不宣称 Architecture promotion、实现或测试完成。#434 activation、
tag、GitHub Release、生产验证与 Issue closure 均保持未授权或 `unverified`。

## #454 Trace

| Requirement | Design | Test | Architecture |
| --- | --- | --- | --- |
| `R454-01` | `D454-01`, `D454-02` | `T454-01`, `T454-03` | `ARCH-CUR-036`, `ARCH-DOM-021`, `ADR-015` |
| `R454-02` | `D454-01`, `D454-02` | `T454-01`, `T454-04` | `ARCH-CUR-036`, `ADR-015` |
| `R454-03` | `D454-01`, `D454-03` | `T454-01`, `T454-05` | `ARCH-DOM-021`, `ARCH-INT-024` |
| `R454-04` | `D454-01`, `D454-04`, `D454-05` | `T454-01`, `T454-02`, `T454-06` | `ARCH-CUR-036`, `ARCH-INT-024` |
| `R454-05` | `D454-02..05` | `T454-03..06`, `T454-08` | `ARCH-DOM-021`, `ADR-015` |
| `R454-06` | `D454-06` | `T454-07`, `T454-08` | `EVD-034` |
| `R454-07` | `D454-07` | `T454-09` | `ARCH-INT-024`, `ARCH-GAP-011`, `EVD-034` |

状态为 `reviewed_promoted`；`.58` 是 immutable predecessor，`.59` 是 #454 RDT successor。
来源为 [#454 contribution](../../../requirements-design-test-contributions/454-task-lifecycle-state-model/manifest.yaml)。
本 trace 只承接 C2+D0；C3-C7、D443、D436、E434 与 promotion-created diff 的 fresh gates 保持未完成。

## #454 C3 Trace

| Requirement | Design | Test | Architecture |
| --- | --- | --- | --- |
| `R454-C3-01` | `D454-C3-01` | `T454-C3-01`, `T454-C3-09` | `ARCH-CUR-037`, `ADR-015` |
| `R454-C3-02` | `D454-C3-03` | `T454-C3-02` | `ARCH-DOM-022` |
| `R454-C3-03` | `D454-C3-01`, `D454-C3-03` | `T454-C3-01`, `T454-C3-03` | `ARCH-DOM-022` |
| `R454-C3-04` | `D454-C3-02..05` | `T454-C3-03..05` | `ARCH-DOM-022`, `ARCH-INT-025` |
| `R454-C3-05` | `D454-C3-06` | `T454-C3-06` | `ARCH-CUR-037` |
| `R454-C3-06` | `D454-C3-06` | `T454-C3-07` | `ARCH-CUR-037` |
| `R454-C3-07` | `D454-C3-07` | `T454-C3-08` | `ARCH-INT-025` |
| `R454-C3-08` | `D454-C3-07..08` | `T454-C3-08`, `T454-C3-10` | `ARCH-GAP-011`, `ARCH-INT-025` |
| `R454-C3-09` | `D454-C3-09` | `T454-C3-09..10` | `EVD-035` |

状态为 `reviewed_promoted`；`.59` 是 immutable predecessor，`.60` 是 #454 C3 RDT successor。
来源为 [#454 C3 contribution](../../../requirements-design-test-contributions/454-task-lifecycle-state-model-c3/manifest.yaml)。
Promotion-created diff、C4-C7、D443、D436、E434 与 Release matrix 不得从本 trace 推定完成。

## #454 C3 Provenance Trace

| Requirement | Design | Test | Architecture |
| --- | --- | --- | --- |
| `R454-C3-10` | `D454-C3-10` | `T454-C3-11`, `T454-C3-15` | `ARCH-CUR-038`, `ARCH-DOM-023` |
| `R454-C3-11` | `D454-C3-11` | `T454-C3-12..13`, `T454-C3-15` | `ARCH-CUR-038`, `ARCH-INT-026`, `EVD-036` |
| `R454-C3-12` | `D454-C3-12` | `T454-C3-14..15` | `ARCH-DOM-023`, `ARCH-INT-026` |

状态为 `reviewed_promoted`；`.60` 是 immutable predecessor，`.61` 是 provenance successor。
来源为 [#454 C3 provenance contribution](../../../requirements-design-test-contributions/454-task-lifecycle-state-model-c3-provenance/manifest.yaml)。

## #454 C4 Trace

| Requirement | Design | Test | Architecture |
| --- | --- | --- | --- |
| `R454-C4-01` | `D454-C4-01..02` | `T454-C4-01`, `T454-C4-10` | `ARCH-CUR-039`, `ARCH-DOM-024`, `ADR-015` |
| `R454-C4-02` | `D454-C4-01..02`, `D454-C4-06` | `T454-C4-01`, `T454-C4-04`, `T454-C4-08` | `ARCH-CUR-039`, `ARCH-INT-027` |
| `R454-C4-03` | `D454-C4-03..04` | `T454-C4-02` | `ARCH-DOM-024`, `EVD-037` |
| `R454-C4-04` | `D454-C4-03..05` | `T454-C4-03`, `T454-C4-05`, `T454-C4-08` | `ARCH-DOM-024`, `ARCH-INT-027` |
| `R454-C4-05` | `D454-C4-03` | `T454-C4-02..03` | `ARCH-DOM-024` |
| `R454-C4-06` | `D454-C4-05..06` | `T454-C4-04..05`, `T454-C4-08` | `ARCH-CUR-039`, `ARCH-INT-027` |
| `R454-C4-07` | `D454-C4-06` | `T454-C4-05` | `ARCH-GAP-011` |
| `R454-C4-08` | `D454-C4-03`, `D454-C4-06` | `T454-C4-06` | `ARCH-DOM-024` |
| `R454-C4-09` | `D454-C4-04..09` | `T454-C4-07..08` | `ARCH-CUR-039`, `EVD-037` |
| `R454-C4-10` | `D454-C4-09..10` | `T454-C4-09..10` | `ARCH-INT-027`, `ARCH-GAP-011` |

状态为 `reviewed_promoted`；`.61` 是 immutable predecessor，`.62` 是 #454 C4 RDT successor。
来源为 [#454 C4 contribution](../../../requirements-design-test-contributions/454-task-lifecycle-state-model-c4/manifest.yaml)。
Promotion-created diff、C5-C7、D443、D436、E434 与 Release matrix 不得从本 trace 推定完成。

该 C4 trace 对 Finalizer provenance 的补充映射为既有 `REQ-048` / `DES-046` / `TST-032` / `SCN-044`：strict-
ancestor initial reprepare、exact `pre_push_remote_head` replacement binding 与 pre-mutation remote identity
revalidation，以及 `FIN454-C4-P1-002` 的 transaction-bound Reactivate branch reuse、历史 terminal PR 分类、
`pre_push_remote_head` single-fast-forward、`publication_head` output-loss convergence 与
allowed-head/Open-PR/transaction-identity drift fail-close，以及 `FIN454-C4-P1-004` 的 same-base reviewed descendant、
predecessor-tail/base-lineage/current-review equality、terminal-PR exclusion 与 intermediate-remote rejection。它不创建第二组 C4 requirement/design/test IDs、宽泛
fallback、PR 人工选择 API、force push 或第二 ledger，也不记录 gate pass。
