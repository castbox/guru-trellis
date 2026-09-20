# Design Traceability

当前 .58 来源：`castbox/Trellis@43fffc170927c85d9f7fc106cc5a059e80d4530b` / CI `35190729418` / CLI/core `0.6.17`；Guru manifest `0.6.17-guru.42`；repository release target `v0.6.17-guru.1`。Architecture public inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.58` / `active`。
完整继承 immutable `.57` 业务合同，当前增量为 #452；current registry 为 32 packages / 142 exits / 102 commands，production workflow 保持 22 mandatory invokes / 98 exits。

`.58` 完整继承 `.57`，吸收 reviewed #452 contribution；RDT current 为 `.58/active`，Architecture inheritance 仍为 `.57/active`。promotion-created diff 必须重新通过 fresh Phase 2、Task Commit、完整 Branch Review 后才能进入 Publication；本文不声明实现、测试或下游门禁已通过。

| Design / Contract | Requirements | Test |
| --- | --- | --- |
| `DES-001`, `DES-006` | `REQ-002`, `REQ-006`, `REQ-046`, `NFR-001` | `TST-002`, `TST-005`, `SCN-005` |
| `DES-002`, `CON-001` | `REQ-003`, `REQ-008` | `TST-002`, `CASE-001` |
| `DES-003`, `CON-002..003` | `REQ-004`, `NFR-002..003` | `TST-003`, `CASE-002` |
| `DES-004`, `DES-005` | `REQ-001`, `REQ-005`, `BEH-001..006` | `TST-001`, `TST-004` |
| `DES-007` | `REQ-007`, `BEH-007` | `TST-006`, `SCN-006` |
| `DES-008` | `REQ-009`, `NFR-004` | `TST-001`, `TST-008` |
| `DES-009` | `REQ-011`, `BEH-008` | `TST-010`, `SCN-003` |
| `DES-010` | `REQ-013`, `REQ-046`, `BEH-009`, `NFR-001..003` | `TST-005`, `TST-007`, `SCN-005` |
| `DES-011` | `REQ-012` | `TST-011`, `SCN-004` |
| `DES-012`, `CON-004` | `REQ-014`, `BEH-010` | `TST-012`, `SCN-009` |
| `DES-013` | `REQ-015` | `TST-013`, `SCN-010` |
| `DES-014`, `DES-015`, `DES-017` | `REQ-016`, `REQ-017`, `BEH-011` | `TST-014`, `SCN-011..012` |
| `DES-016` | `REQ-018` | `TST-015`, `SCN-013` |
| `DES-018` | `REQ-020` | `TST-017`, `SCN-015..016` |
| `DES-019` | `REQ-006`, `REQ-018` | `TST-014`, `SCN-011`, `SCN-013` |
| `DES-026`, `DES-027`, `DES-032` | `REQ-027`, `REQ-028` | `TST-018`, `SCN-028`, `SCN-031..032` |
| `DES-028` | `REQ-029` | `TST-019`, `SCN-024` |
| `DES-029` | `REQ-030` | `TST-020`, `SCN-024..027` |
| `DES-030`, `DES-033` | `REQ-031`, `REQ-033`, `REQ-034` | `TST-021`, `TST-023..024`, `SCN-025..032` |
| `DES-031`, `DES-032` | `REQ-032` | `TST-018`, `TST-022`, `SCN-029`, `SCN-033` |
| `DES-034` | `REQ-035` | `TST-025..026`, `SCN-024..033` |
| `DES-035`, `DES-036` | `REQ-036`, `REQ-037` | `TST-027`, `SCN-034..035` |
| `DES-037..039` | `REQ-038..040` | `TST-027..028`, `SCN-034..037` |
| `DES-040`, `DES-041` | `REQ-041`, `REQ-042` | `TST-028..029`, `SCN-038..039` |
| `DES-042` | `REQ-043`, `REQ-046` | `TST-030`, `SCN-040` |
| `DES-043` | `REQ-044` | `TST-029`, `SCN-039` |
| `DES-044` | `REQ-045` | `TST-007`, `TST-029`, `SCN-039` |
| `DES-045` | `REQ-047`, `REQ-049` | `TST-031..032`, `SCN-041..043` |
| `DES-046` | `REQ-047..049`, `BEH-008`, `BEH-010` | `TST-031..032`, `SCN-041..044` |
| `DES-047` | `REQ-049..050` | `TST-033..034`, `SCN-045`, `SCN-047` |
| `DES-048` | `REQ-051` | `TST-035`, `SCN-046` |
| `DES-049` | `REQ-052`, `REQ-054..055` | `TST-036`, `TST-038..039` |
| `DES-050` | `REQ-052`, `REQ-054` | `TST-036`, `TST-038` |
| `DES-051` | `REQ-052..054` | `TST-037..038` |
| `DES-052` | `REQ-053`, `REQ-055` | `TST-039` |
| `DES-053`, `CON-005` | `REQ-056` | `TST-040`, `SCN-053` |
| `DES-054` | `REQ-057`, `REQ-061` | `TST-041`, `CASE-003` |
| `DES-055`, `CON-006` | `REQ-058`, `BEH-012`, `NFR-006` | `TST-041..042`, `SCN-049..050` |
| `DES-056` | `REQ-057`, `REQ-061..062`, `BEH-012` | `TST-041`, `TST-045`, `CASE-003` |
| `DES-057` | `REQ-059..060`, `NFR-006` | `TST-043..044`, `SCN-051` |
| `DES-058` | `REQ-060`, `NFR-006` | `TST-042..043`, `SCN-050..052` |
| `DES-059`, `CON-006` | `REQ-061..062`, `BEH-012` | `TST-044..045`, `CASE-004` |
| `DES-060` | `REQ-063`, `REQ-065` | `TST-046`, `TST-048`, `SCN-054` |
| `DES-061` | `REQ-064`, `REQ-066`, `BEH-013` | `TST-047`, `TST-049`, `SCN-054` |
| `DES-062` | `REQ-065..066` | `TST-046..048`, `SCN-054` |
| `DES-063` | `REQ-066..067`, `BEH-013` | `TST-049..050`, `SCN-054`, `CASE-003` |
| `DES-064`, `CON-006` | `REQ-068`, `BEH-013` | `TST-050`, `CASE-004` |
| `DES-065` | `REQ-069`, `REQ-073`, `BEH-014` | `TST-051..052`, `SCN-055..056` |
| `DES-066` | `REQ-069..070`, `BEH-014` | `TST-052`, `SCN-055..056` |
| `DES-067`, `CON-007` | `REQ-071..073`, `BEH-015` | `TST-051`, `TST-053`, `TST-055`, `SCN-057..058` |
| `DES-068`, `CON-007` | `REQ-072`, `BEH-015` | `TST-054`, `SCN-057..058` |
| `DES-069..072` | `REQ-074..077` | `TST-056..058`, `TST-061`, `SCN-059..060` |
| `DES-073..076` | `REQ-077..080` | `TST-056`, `TST-059..060`, `SCN-061` |
| `DES-077..078` | `REQ-081` | `TST-057..058`, `TST-061`, `SCN-062..063` |
| `DES-079` | `REQ-082` | `TST-062`, `SCN-064..065` |
| `DES-080` | `REQ-083` | `TST-063`, `SCN-066` |
| `DES-081` | `REQ-084` | `TST-064`, `SCN-067` |
| `DES-082` | `REQ-085` | `TST-065`, `SCN-068` |
| `DES-083` | `REQ-086` | `TST-066`, `SCN-069` |
| `DES-084` | `REQ-087..088`, `BEH-016` | `TST-067..068`, `SCN-070..071` |
| `DES-085..086` | `REQ-089`, `REQ-092` | `TST-067`, `TST-069`, `SCN-071..072` |
| `DES-087`, `CON-008` | `REQ-088`, `REQ-090`, `BEH-016` | `TST-068`, `TST-070`, `SCN-073` |
| `DES-088`, `CON-008` | `REQ-090..091`, `BEH-016` | `TST-070..071`, `SCN-074..075` |
| `DES-089` | `REQ-092` | `TST-072..073`, `SCN-076` |

## #378 Trace

| Design | Requirements | Test |
| --- | --- | --- |
| D378-01 | R378-01 | T378-01, T378-04 |
| D378-02 | R378-02 | T378-02 |
| D378-03 | R378-03 | T378-03, T378-04 |
| D378-04 | R378-04 | T378-05 |

## #392 Trace

| Design | Requirements | Test / Scenario |
| --- | --- | --- |
| `D392-01` | `R392-01..03` | `T392-01` |
| `D392-02` | `R392-04` | `T392-02`, `SCN-077` |
| `D392-03` | `R392-02..03` | `T392-01` |
| `D392-04` | `R392-05..06`, `BEH-017` | `T392-03..05`, `SCN-077..078` |
| `D392-05` | `R392-06..08`, `BEH-017` | `T392-05..06`, `SCN-078` |
| `D392-06` | `R392-04`, `R392-09` | `T392-02`, `T392-06`, `SCN-077..078` |

Architecture refs：`ARCH-CUR-025`、`ARCH-INT-015`、`EVD-024`。Contribution locator：
`docs/requirements-design-test-contributions/392-release-v0616-guru1/`；其 `reviewed_promoted` 历史状态
保持 immutable。

## #329 Trace

| Design | Requirements | Test / Scenario |
| --- | --- | --- |
| `D329-01` | `R329-01..02` | `T329-01..02`, `SCN-079..080` |
| `D329-02` | `R329-02..03`, `R329-07`, `R329-09` | `T329-02..03`, `T329-07`, `SCN-079..080` |
| `D329-03` | `R329-03`, `R329-05`, `BEH-018` | `T329-04`, `SCN-079`, `SCN-082..083` |
| `D329-04` | `R329-04` | `T329-05`, `SCN-081` |
| `D329-05` | `R329-06`, `BEH-018` | `T329-06`, `SCN-083` |
| `D329-06` | `R329-03`, `R329-07`, `BEH-018` | `T329-03`, `T329-06`, `SCN-083` |
| `D329-07` | `R329-09..10`, `BEH-018` | `T329-01..07`, `SCN-079..084` |
| `D329-08` | `R329-08`, `R329-10` | `T329-08`, `SCN-084` |

Architecture refs：`ARCH-CUR-026`、`ARCH-INT-016`、`EVD-025`。Contribution locator：
`docs/requirements-design-test-contributions/329-adopt-developer-free-trellis/`；状态为
`reviewed_promoted`，`.48` 是 immutable predecessor，`.49` 是 #329 promotion 建立的 immutable
superseded authority。


## #408 Trace

| Design | Requirements | Test |
| --- | --- | --- |
| `D408-01` | `R408-01` | `T408-01` |
| `D408-02` | `R408-02`, `R408-03` | `T408-02`, `T408-03` |
| `D408-03` | `R408-04`, `R408-05`, `R408-06`, `R408-07` | `T408-04`, `T408-05`, `T408-06`, `T408-07` |
| `D408-04` | `R408-02`, `R408-03`, `R408-04`, `R408-08` | `T408-02`, `T408-03`, `T408-04`, `T408-08` |
| `D408-05` | `R408-03`, `R408-04` | `T408-03`, `T408-04` |

状态：`.51` immutable superseded history，implements/verifies。责任定义：[design-main.md](./design-main.md)；
需求与验收定义分别见 [Requirements](../../../requirements/versions/current-main-0.6.17-guru.56/requirement-main.md)
及 [Test](../../../test/versions/current-main-0.6.17-guru.56/test-strategy.md)。反向索引为
[Requirements trace](../../../requirements/versions/current-main-0.6.17-guru.56/traceability.md) 和
[Test trace](../../../test/versions/current-main-0.6.17-guru.56/traceability.md)。
Architecture historical inheritance：`.51` / `superseded`；current public identity 为
[`README.md`](../../../architecture/README.md) / `current-main-0.6.17-guru.56` / `active`；
`ARCH-CUR-028`、`ARCH-DOM-015`、`ARCH-INT-014/016`、`EVD-027`。历史来源保留于
[#408 contribution](../../../requirements-design-test-contributions/408-nightly-session-binding-manual-fallback/design.md)，
不形成第二 current 正文或新的 owner。

## #410 Trace

| Design | Requirements | Test |
| --- | --- | --- |
| `D410-01` | `R410-01..02`, `R410-04` | `T410-01`, `T410-05` |
| `D410-02` | `R410-02..03` | `T410-01..02` |
| `D410-03` | `R410-04..05`, `BEH-018` | `T410-02..03` |
| `D410-04` | `R410-06`, `BEH-018` | `T410-04..05`, `T410-07..08` |
| `D410-05` | `R410-04`, `R410-07`, `BEH-018` | `T410-05..06`, `T410-08` |
| `D410-06` | `R410-06..07`, `BEH-018` | `T410-04`, `T410-06..08` |

Architecture refs：`ARCH-CUR-029`、`ARCH-INT-014..016`。Contribution locator：
`docs/requirements-design-test-contributions/410-release-v0617-guru1/`；状态为
`reviewed_promoted`，`.51` 是 immutable predecessor，`.52` 是 #410 建立的 immutable superseded authority。

## #418 Trace

| Design | Requirements | Test |
| --- | --- | --- |
| D418-01 | R418-01, R418-02, R418-06 | T418-01, T418-02, T418-03 |
| D418-02 | R418-03, R418-06, R418-07 | T418-04, T418-07 |
| D418-03 | R418-02, R418-04, R418-05, R418-06, R418-07 | T418-05, T418-06, T418-07, T418-08, T418-09, T418-10, T418-11 |
| D418-04 | R418-02, R418-04, R418-05, R418-06 | T418-08, T418-09, T418-14 |
| D418-05 | R418-04, R418-05, R418-06 | T418-06, T418-10, T418-13, T418-14 |
| D418-06 | R418-04, R418-05, R418-06 | T418-12 |

定义：[Requirements](../../../requirements/versions/current-main-0.6.17-guru.56/requirement-main.md)、
[Design](./design-main.md)、
[Test](../../../test/versions/current-main-0.6.17-guru.56/test-strategy.md)。
反向索引：[Requirements trace](../../../requirements/versions/current-main-0.6.17-guru.56/traceability.md)、
[Design trace](./traceability.md)、
[Test trace](../../../test/versions/current-main-0.6.17-guru.56/traceability.md)。
关系为 implements/verifies；来源为 [#418 contribution](../../../requirements-design-test-contributions/418-closeout-identity-recovery/manifest.yaml)，
predecessor .52 -> successor .53；Architecture inheritance 为 .53/active，仅引用
[ADR-010](../../../architecture/adr/010-archived-review-authority.md)、
[ARCH-CUR-030](../../../architecture/01-current/system.md)、
[ARCH-INT-018](../../../architecture/04-integrations/distribution.md)、
[EVD-028](../../../architecture/evidence/current-evidence.md)，不复制正文。

## #419 Trace

| Design | Requirements | Test |
| --- | --- | --- |
| `D419-01..02` | `R419-01`, `R419-03` | `T419-01`, `T419-03`, `T419-06` |
| `D419-03` | `R419-02` | `T419-02` |
| `D419-04..05` | `R419-03..04` | `T419-03..05` |
| `D419-06` | `R419-05` | `T419-06` |
| `D419-07` | `R419-06` | `T419-07` |
| `D419-08..10` | `R419-07` | `T419-08..10` |

Architecture refs：`ARCH-CUR-031`、`ARCH-DOM-016`、`ARCH-INT-019`、`ARCH-GOV-010`、
`ADR-011`、`EVD-029`。来源为 task contribution，状态 `reviewed_promoted`。

## #435 Trace

| Design | Requirements | Test |
| --- | --- | --- |
| `D435-01` | `R435-01` | `T435-01..04` |
| `D435-02` | `R435-02` | `T435-05..10` |
| `D435-03` | `R435-03` | `T435-11..16` |
| `D435-04` | `R435-04`, `R435-06` | `T435-17..22`, `T435-29..33` |
| `D435-05` | `R435-05`, `R435-06` | `T435-23..33` |
| `D435-06` | `R435-02` | `T435-05..10` |
| `D435-07` | `R435-03` | `T435-11..16` |
| `D435-08` | `R435-07` | `T435-34..39` |
| `D435-09` | `R435-08` | `T435-40..45` |

Architecture inheritance remains [`README.md`](../../../architecture/README.md) /
`current-main-0.6.17-guru.56` / `active`; `ADR-012` is inherited and `ADR-013` is accepted by the paired Architecture promotion.
来源为 [#435 contribution](../../../requirements-design-test-contributions/435-active-task-delivery-loop/manifest.yaml)，
状态 `reviewed_promoted`。

## #436 Trace

| Design | Requirements | Test |
| --- | --- | --- |
| `D436-01`, `D436-07` | `R436-01` | `T436-01..10` |
| `D436-02`, `D436-07` | `R436-02` | `T436-11..17` |
| `D436-03`, `D436-08` | `R436-03` | `T436-18..30` |
| `D436-04`, `D436-07` | `R436-04` | `T436-31..35` |
| `D436-05`, `D436-08` | `R436-05` | `T436-36..48` |
| `D436-06`, `D436-07` | `R436-06` | `T436-49..56` |

Architecture inheritance is `.56/active`; `ADR-013`, `ARCH-CUR-033`, `ARCH-DOM-018`, `ARCH-INT-021`
and `EVD-031` are references only. 来源为 [#436 contribution](../../../requirements-design-test-contributions/436-post-delivery-completion-finish/manifest.yaml)，
状态 `reviewed_promoted`；promotion 不证明后续 fresh gates 或远端 mutation。

## #443 Trace

| Design | Requirements | Test |
| --- | --- | --- |
| `D443-01`, `D443-03` | `R443-01..03` | `T443-05..08`, `T443-19..20` |
| `D443-02`, `D443-06` | `R443-07` | `T443-01..04` |
| `D443-03..04` | `R443-03..04`, `R443-06` | `T443-05..11`, `T443-16..18` |
| `D443-05` | `R443-03`, `R443-05..06` | `T443-12..18` |
| `D443-07` | `R443-05`, `R443-08` | `T443-19..20` |

Architecture inheritance is `.57/active`; `ADR-014`, `ARCH-CUR-034`, `ARCH-DOM-019`, `ARCH-INT-022`
and `EVD-032` are references only. 来源为 [#443 contribution](../../../requirements-design-test-contributions/443-task-identity-session-binding/manifest.yaml)，
状态 `reviewed_promoted`；promotion 不证明本 combined diff 的 fresh gates 或远端 mutation。

## #452 Trace

| Design | Requirements | Test |
| --- | --- | --- |
| `D452-01` | `R452-01..03` | `T452-01..02`, `T452-09` |
| `D452-02` | `R452-01`, `R452-04`, `R452-07` | `T452-03`, `T452-06`, `T452-09` |
| `D452-03` | `R452-03..06` | `T452-02..05` |
| `D452-04` | `R452-03..05` | `T452-02..04` |
| `D452-05` | `R452-06..07` | `T452-05..06`, `T452-10` |
| `D452-06` | `R452-08` | `T452-07`, `T452-11` |
| `D452-07` | `R452-02`, `R452-09` | `T452-01`, `T452-08..09` |
| `D452-08` | `R452-09..10` | `T452-08..10` |
| `D452-09` | `R452-03`, `R452-09..10` | `T452-02`, `T452-08..11` |
| `D452-10` | `R452-10` | `T452-01..12` |

Architecture inheritance remains [`README.md`](../../../architecture/README.md) /
`current-main-0.6.17-guru.57` / `active`; the reviewed Architecture contribution remains a locator rather than a
new shared Architecture version. 来源为
[#452 contribution](../../../requirements-design-test-contributions/452-all-platform-support/manifest.yaml)。
本 Design promotion 只建立 current contract，不证明 implementation、`T452-01..12`、#434 activation、
release/tag/GitHub Release 或业务仓库生产验证已完成。
