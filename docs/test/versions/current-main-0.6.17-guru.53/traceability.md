# Test Traceability

当前 .53 来源：`castbox/Trellis@db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0` / CI `34838784963` / CLI/core `0.6.17`；Guru manifest `0.6.17-guru.42`；repository release target `v0.6.17-guru.1`。Architecture public inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.53` / `active`。
完整继承 immutable `.52` 业务合同，当前增量为 #418；旧 pin、release mapping、计数及 promotion/evidence 叙述只绑定其明确历史版本。当前 graph 见 Design inventory，旧验证不证明本次 candidate。

`.53` 完整继承 `.52` 与 reviewed #418 contribution；Architecture 与 RDT 共享 `.53/active` current identity。promotion-created diff 必须重新通过 fresh Phase 2、Task Commit、完整 Branch Review 后才能进入 Publication；本文不声明下游门禁已通过。

| Strategy / Scenario | Requirements | Design | Evidence |
| --- | --- | --- | --- |
| `TST-001` | `NFR-004` | `DES-008` | #266 docs/spec checks |
| `TST-002`, `CASE-001` | `REQ-003`, `REQ-008` | `DES-002`, `CON-001` | package tests / registry-interface graph |
| `TST-003`, `CASE-002` | `REQ-004`, `REQ-010` | `DES-003`, `CON-002` | semantic eval + independent review |
| `TST-004`, `SCN-001..004` | `REQ-001`, `REQ-005`, `BEH-001..006` | `DES-004`, `DES-005` | integration/task history |
| `TST-005`, `SCN-005` | `REQ-006`, `NFR-001` | `DES-001`, `DES-006` | throwaway/reapply/platform parity |
| `TST-006`, `SCN-006` | `REQ-007`, `BEH-007` | `DES-007` | RDT/Architecture/Bootstrap validation |
| `TST-007` | `REQ-008`, `NFR-003` | `CON-001..003` | schema/exit/consumer closure |
| `TST-008` | `REQ-009`, `NFR-004` | `DES-008` | GitHub/release/exact candidate owner evidence |
| `TST-009`, `SCN-007` | `REQ-005`, `REQ-011`, `REQ-012`, `REQ-013` | `DES-005`, `DES-009`, `DES-010`, `DES-011` | business parallel matrix owner evidence |
| `TST-010` | `REQ-011`, `BEH-008` | `DES-005`, `DES-009` | task index/archive/finish-summary query evidence |
| `TST-011`, `SCN-008` | `REQ-012` | `DES-011` | provider/base/partial recovery evidence |
| `TST-012`, `SCN-009` | `REQ-014`, `BEH-010` | `DES-012`, `CON-004` | Finalizer focused package + Throwaway closeout evidence |
| `TST-013`, `SCN-010` | `REQ-015` | `DES-013` | source/installed registry-derived inventory validation |
| `TST-014`, `SCN-011..012` | `REQ-016`, `REQ-017`, `BEH-011` | `DES-014`, `DES-015`, `DES-017` | six-cell matrix summary + cell results |
| `TST-015`, `SCN-013` | `REQ-018` | `DES-016`, `DES-019` | three-group capability comparison + independent consistency/installation comparison |
| `TST-016`, `SCN-014` | `REQ-019` | `DES-007`, `DES-014` | installed RDT/Architecture/Bootstrap evals + docs projection checks |
| `TST-017`, `SCN-015..016` | `REQ-020` | `DES-018` | local A/B lifecycle + real GitHub A merge/closure/cleanup evidence |
| `TST-018`, `SCN-028`, `SCN-031..032` | `REQ-027`, `REQ-028` | `DES-026`, `DES-027`, `DES-032` | workflow stage routes + exact Phase 2/Branch Review/promotion re-entry |
| `TST-019`, `SCN-024` | `REQ-029` | `DES-028` | current design constitution locator/identity + public projection separation |
| `TST-020`, `SCN-024..027` | `REQ-030` | `DES-029` | schema/eval path exclusivity and no-impact contract |
| `TST-021`, `SCN-025..028` | `REQ-031` | `DES-026`, `DES-029`, `DES-030`, `DES-033` | task-local Architecture contribution + project change contract |
| `TST-022`, `SCN-029`, `SCN-033` | `REQ-032` | `DES-030..032` | project-check descriptor/result binding + route fixtures |
| `TST-023`, `SCN-031..032` | `REQ-033` | `DES-027`, `DES-033` | reviewed contribution、ADR-005与 serialized promotion |
| `TST-024`, `SCN-030` | `REQ-034` | `DES-033` | parallel stale and shared-current single-writer fixtures |
| `TST-025..026`, `SCN-024..033` | `REQ-035` | `DES-034` | source/installed projections、evals、reapply/drift与 representative clean install |
| `TST-027`, `SCN-034..037` | `REQ-036..040` | `DES-035..039` | canonical/installed sync-base 15/15 and exact authority fixtures |
| `TST-028..029`, `SCN-038..039` | `REQ-038`, `REQ-041..042` | `DES-037`, `DES-039..041` | post-sync transition and workspace freshness continuity tests |
| `TST-030`, `SCN-040` | `REQ-043` | `DES-042` | validators、projection equality、reapply/drift/sidecar-zero and representative detached wrapper |
| `TST-029`, `SCN-039` | `REQ-044..045` | `DES-043..044` | Sync-to-Discovery public transition、live observation与 source-aware freshness |
| `TST-005`, `TST-007`, `TST-030`, `SCN-005`, `SCN-040` | `REQ-046` | `DES-006`, `DES-010`, `DES-042` | #295 canonical/installed/platform/preset contract closure |
| `TST-031`, `SCN-041..043` | `REQ-047`, `REQ-049` | `DES-045..046` | Finalizer canonical/installed 59/59 + binding/tail negative fixtures |
| `TST-032`, `SCN-044` | `REQ-048`, `REQ-049`, `BEH-008`, `BEH-010` | `DES-046` | prepared-state/existing-PR/absent-remote focused regression |
| `TST-033`, `SCN-045` | `REQ-049..050` | `DES-047` | verifier-zero dependency + source/installed/platform/reapply/drift checks |
| `TST-034`, `SCN-047` | `REQ-050` | `DES-047` | current real fixture `unverified`; local fake-GitHub integration only |
| `TST-035`, `SCN-046` | `REQ-051` | `DES-048` | verifier 17/17、routing 44/44、closed failure schema/postcheck evidence |
| `TST-036`, `SCN-048` | `REQ-052`, `REQ-055` | `DES-049..050`, `DES-052` | historical #267 unique active `.42` / superseded `.41` / expected-current checks；`.43` successor history 与 current `.44` identity 分离 |
| `TST-037` | `REQ-052..053` | `DES-051` | historical `.3/.39/CLI 0.6.15` mapping and release-boundary review |
| `TST-038` | `REQ-054` | `DES-049..051` | historical #267 `.41...42` semantic diff and no-ADR/no-runtime-change review |
| `TST-039`, `SCN-048` | `REQ-053`, `REQ-055` | `DES-049`, `DES-052` | historical #267 contribution review + serialized owners + post-promotion fresh lifecycle |
| `TST-040`, `SCN-053` | `REQ-056` | `DES-053`, `CON-005` | four project-local projections + public/installed inventory exclusion |
| `TST-041`, `CASE-003` | `REQ-057..058`, `REQ-061`, `BEH-012` | `DES-054..056`, `CON-006` | invocation, owner-composition and fail-closed contract guards |
| `TST-042`, `SCN-049..050` | `REQ-058`, `REQ-060`, `BEH-012`, `NFR-006` | `DES-055`, `DES-058`, `CON-006` | honest-path temporary Git fixture + planless reconciliation regression |
| `TST-043`, `SCN-051..052` | `REQ-060`, `NFR-006` | `DES-057..058` | reviewed-content checkpoint/drift table tests |
| `TST-044`, `CASE-004` | `REQ-059`, `REQ-062`, `NFR-006` | `DES-057`, `DES-059`, `CON-006` | live payload, forbidden artifact and independent confirmation checks |
| `TST-045`, `CASE-003` | `REQ-057`, `REQ-061..062`, `BEH-012` | `DES-054`, `DES-056`, `DES-059` | post-merge minimum gate scope and stop-before-mutation guard |
| `TST-046`, `SCN-054` | `REQ-063`, `REQ-065` | `DES-060`, `DES-062` | `.44` unique current、latest stable `.4/.39`、target `.5/.40/CLI 0.6.15` mapping review |
| `TST-047`, `SCN-054` | `REQ-064`, `REQ-066` | `DES-061` | fresh #311/#333/#339/#358/#361 merged prerequisite consumption |
| `TST-048`, `SCN-054` | `REQ-065..066` | `DES-060`, `DES-062` | expected `.43` serialized RDT promotion、Architecture `.44` inheritance and navigation closure |
| `TST-049`, `SCN-054`, `CASE-003` | `REQ-066..067`, `BEH-013` | `DES-061`, `DES-063` | same-candidate predecessor diff、version/distribution/platform/install gates and fail-closed routes |
| `TST-050`, `SCN-054`, `CASE-004` | `REQ-067..068`, `BEH-013` | `DES-063..064`, `CON-006` | installed business chain、secret/residue、tag/smoke/Release/closure/cleanup independent transactions |
| `TST-051` | `REQ-073` | `DES-065`, `DES-067` | current registry/interface/workflow/preset graph closure |
| `TST-052`, `SCN-055..056` | `REQ-069..070`, `BEH-014` | `DES-065..066` | #240 package/evals + PR #346 review + ADR-008 |
| `TST-053`, `SCN-057..058` | `REQ-071`, `BEH-015` | `DES-067`, `CON-007` | Merge/Restore routing tests + PR #351 review |
| `TST-054`, `SCN-057..058` | `REQ-072`, `BEH-015` | `DES-068`, `CON-007` | restore package success/idempotent/zero-write negative tests |
| `TST-055` | `REQ-069..073` | `DES-065..068` | EVD-019/EVD-020 + `.44` serialized promotion and fresh re-entry boundary |
| `TST-056`, `SCN-059..060` | `REQ-074`, `REQ-077` | `DES-069..072` | four affected package suites and interface/command inventory |
| `TST-057..058`, `TST-061`, `SCN-059..060`, `SCN-062..063` | `REQ-075..076`, `REQ-081` | `DES-070..072`, `DES-077..078` | closeout integration, operation budget, installed fixture and restore regressions |
| `TST-059`, `SCN-061` | `REQ-078..079` | `DES-073..074`, `DES-076` | source/installed/matrix/throwaway/runtime/eval and all-platform actual-load |
| `TST-060` | `REQ-077`, `REQ-080` | `DES-072`, `DES-075` | preset 85/85, ownership/reapply/drift and recursive sidecar zero |
| `TST-062`, `SCN-064..065` | `REQ-082` | `DES-079` | reviewed contribution, expected `.44`, serialized `.45` and required fresh re-entry |
| `TST-063`, `SCN-066` | `REQ-083` | `DES-080` | post-merge fresh candidate and from-zero #332 Release Gate boundary |
| `TST-064`, `SCN-067` | `REQ-084` | `DES-081` | source/installed finish-family exclusivity and invalid-state regression |
| `TST-065`, `SCN-068` | `REQ-085` | `DES-082` | Branch Review contract/runtime visibility and dual-pass identity regression |
| `TST-066`, `SCN-069` | `REQ-086` | `DES-083` | three-platform canonical/installed continuous actual-load regression |
| `TST-067`, `SCN-070..071` | `REQ-087..089`, `BEH-016` | `DES-084..085` | Reconcile source/installed route and executor regressions |
| `TST-068`, `SCN-073` | `REQ-088`, `REQ-090`, `BEH-016` | `DES-084`, `DES-087`, `CON-008` | Review Branch source/installed pair, tree and output contract |
| `TST-069`, `SCN-072` | `REQ-089`, `REQ-092` | `DES-085..086` | real Git repository commit/recovery and zero-write negatives |
| `TST-070`, `SCN-074` | `REQ-090`, `BEH-016` | `DES-087..088` | real Publication recorder/checker/wrapper continuity integration |
| `TST-071`, `SCN-075` | `REQ-091` | `DES-088`, `CON-008` | Finalizer output example and Interface projection integration |
| `TST-072` | `REQ-092` | `DES-086`, `DES-089` | source validator, graph recomputation, schema/platform parity |
| `TST-073`, `SCN-076` | `REQ-092` | `DES-089` | expected `.45`, reviewed contribution, `.46` promotion and fresh re-entry |

## #378 Trace

| Test | Requirements | Design | Evidence |
| --- | --- | --- | --- |
| T378-01 | R378-01 | D378-01 | test-plan.md #378 reviewed focused evidence |
| T378-02 | R378-02 | D378-02 | test-plan.md #378 reviewed focused evidence |
| T378-03 | R378-03 | D378-03 | test-plan.md #378 reviewed focused evidence |
| T378-04 | R378-01, R378-03 | D378-01, D378-03 | test-plan.md #378 reviewed focused evidence |
| T378-05 | R378-04 | D378-04 | test-plan.md #378 reviewed focused evidence |

## #392 Trace

| Test / Scenario | Requirements | Design | Architecture / Evidence |
| --- | --- | --- | --- |
| `T392-01` | `R392-01..03` | `D392-01`, `D392-03` | `ARCH-CUR-025`, `EVD-024` |
| `T392-02` | `R392-04`, `R392-09` | `D392-02`, `D392-06` | `ARCH-CUR-025`, `ARCH-INT-015`, `EVD-024` |
| `T392-03` | `R392-01..03`, `R392-05` | `D392-01`, `D392-03..04` | `ARCH-INT-015`, `EVD-024` |
| `T392-04`, `SCN-077` | `R392-04..05`, `BEH-017` | `D392-02`, `D392-04`, `D392-06` | `ARCH-CUR-025`, `ARCH-INT-015`, `EVD-024` |
| `T392-05`, `SCN-078` | `R392-06..07`, `BEH-017` | `D392-04..05` | `ARCH-CUR-025`, `ARCH-INT-015` |
| `T392-06`, `SCN-078` | `R392-08..09`, `BEH-017` | `D392-05..06` | `ARCH-INT-015` |

本 trace 只记录 stable contract。post-promotion fresh review、Publication、merge、exact-candidate gate、
tag、Release、business smoke 与 Issue closure 的动态结果不得写回本 authority。

## #329 Trace

| Test / Scenario | Requirements | Design | Architecture / Evidence |
| --- | --- | --- | --- |
| `T329-01` | `R329-01`, `R329-10` | `D329-01`, `D329-07` | `ARCH-CUR-026`, `EVD-025` |
| `T329-02`, `SCN-079..080` | `R329-02`, `R329-09` | `D329-01..02`, `D329-07` | `ARCH-INT-016`, `EVD-025` |
| `T329-03` | `R329-03`, `R329-07` | `D329-02`, `D329-06` | `ARCH-CUR-026`, `ARCH-INT-016` |
| `T329-04`, `SCN-082` | `R329-03`, `R329-05`, `BEH-018` | `D329-03` | `ARCH-CUR-026` |
| `T329-05`, `SCN-081` | `R329-04` | `D329-04` | `ARCH-CUR-026` |
| `T329-06`, `SCN-083` | `R329-06`, `BEH-018` | `D329-05..06` | `EVD-025` |
| `T329-07`, `SCN-079..084` | `R329-09`, `BEH-018` | `D329-02..07` | `ARCH-INT-016`, `EVD-025` |
| `T329-08`, `SCN-084` | `R329-07..10` | `D329-06..08` | `ARCH-CUR-026`, `ARCH-INT-016`, `EVD-025` |

本 trace 记录 `reviewed_promoted` stable contract；fresh Phase 2、Branch Review、Publication 与远端动作
结果不写回 authority。

## #247 Trace

| Test / Scenario | Requirements | Design | Architecture / Evidence |
| --- | --- | --- | --- |
| `T247-01` | `R247-01..02` | `D247-01`, `D247-06` | `ARCH-CUR-027`, `ARCH-GAP-008`, `EVD-026` |
| `T247-02` | `R247-03` | `D247-01` | `ARCH-CUR-027`, `ARCH-DOM-015` |
| `T247-03`, `SCN-087` | `R247-04..05`, `BEH-020` | `D247-02..03` | `ARCH-GOV-006..009`, `ARCH-INT-017` |
| `T247-04`, `SCN-085..087`, `SCN-090` | `R247-05..06`, `BEH-020` | `D247-03..05` | `ARCH-CUR-027`, `ARCH-DOM-015`, `ARCH-INT-017`, `ARCH-GOV-009`, `ADR-009` |
| `T247-05`, `SCN-089` | `R247-07` | `D247-04..05` | `ARCH-DOM-015`, `EVD-026` |
| `T247-06`, `SCN-088` | `R247-08..09`, `BEH-019` | `D247-08` | `ARCH-CUR-027`, `ARCH-GAP-008`, `ADR-009` |
| `T247-07` | `R247-01..02`, `R247-09` | `D247-06`, `D247-08` | `ARCH-CUR-027`, `ARCH-GAP-008`, `EVD-026` |
| `T247-08`, `SCN-090` | `R247-10`, `BEH-020` | `D247-06..08` | `ARCH-CUR-027`, `ARCH-INT-017`, `EVD-026` |

本 trace记录 `reviewed_promoted` stable contract；`.49` 是 immutable predecessor，`.50` 是 #247 建立的 immutable
superseded authority。promotion-created diff、Publication与远端Release/Issue结果仍由后续owner fresh验证。

## #408 Trace

| Test | Requirements | Design | Evidence |
| --- | --- | --- | --- |
| `T408-01` | `R408-01` | `D408-01` | `EVD-027`; source/build/CI |
| `T408-02` | `R408-02` | `D408-02`, `D408-04` | `EVD-027`; generated/reapply |
| `T408-03` | `R408-03` | `D408-02`, `D408-04`, `D408-05` | `EVD-027`; installed/native session |
| `T408-04` | `R408-04` | `D408-03`, `D408-04`, `D408-05` | `EVD-027`; authoring/old lifecycle |
| `T408-05` | `R408-05` | `D408-03` | `EVD-027`; native error reporting |
| `T408-06` | `R408-06` | `D408-03` | `EVD-027`; stateful/native local fixture |
| `T408-07` | `R408-07` | `D408-03` | `EVD-027`; residue preservation |
| `T408-08` | `R408-02`, `R408-08` | `D408-04` | `EVD-027`; focused installed/boundaries |

状态：`.51` immutable superseded history，verifies/implemented-by；策略定义和证明边界分别见
[test-strategy.md](./test-strategy.md)、[test-plan.md](./test-plan.md)。反向索引为
[Requirements trace](../../../requirements/versions/current-main-0.6.17-guru.53/traceability.md) 与
[Design trace](../../../design/versions/current-main-0.6.17-guru.53/traceability.md)。Architecture historical
inheritance 为 `.51` / `superseded`；current public identity 为
[`README.md`](../../../architecture/README.md) / `current-main-0.6.17-guru.53` / `active`，对应
[EVD-027](../../../architecture/evidence/current-evidence.md)。表中引用不等于本轮重跑、post-promotion
gate、真实 GitHub mutation、完整 Release matrix 或发布完成。

## #410 Trace

| Test | Requirements | Design | Architecture / Boundary |
| --- | --- | --- | --- |
| `T410-01` | `R410-01..02` | `D410-01..02` | `ARCH-CUR-029`; four-axis current mapping |
| `T410-02` | `R410-03..04` | `D410-02..03` | `ARCH-INT-014`, `ARCH-INT-016`; package/source/API compatibility |
| `T410-03` | `R410-05`, `BEH-018` | `D410-03` | `ARCH-INT-015`; promotion and fresh review |
| `T410-04` | `R410-06`, `BEH-018` | `D410-04`, `D410-06` | `ARCH-CUR-029`, `ARCH-INT-015`; candidate lineage |
| `T410-05` | `R410-01`, `R410-04`, `R410-06` | `D410-01`, `D410-04..05` | source/installed and platform parity |
| `T410-06` | `R410-07`, `BEH-018` | `D410-05..06` | ownership, reapply, drift, secret and residue hygiene |
| `T410-07` | `R410-06`, `BEH-018` | `D410-04`, `D410-06` | focused install/update/preview/switch/reapply |
| `T410-08` | `R410-06..07`, `BEH-018` | `D410-04..06` | exact-candidate tag/smoke/Release/closure boundaries |

本 trace 记录 `reviewed_promoted` stable contract；`.51` 是 immutable predecessor，`.52`
是 #410 建立的 immutable superseded authority。知识 promotion、历史 evidence 或 preparation checks 均不替代后续
exact-candidate live gate。

## #418 Trace

| Test | Requirements | Design |
| --- | --- | --- |
| T418-01 | R418-01, R418-06 | D418-01 |
| T418-02 | R418-01, R418-02, R418-06 | D418-01 |
| T418-03 | R418-01, R418-06 | D418-01 |
| T418-04 | R418-03, R418-06 | D418-02 |
| T418-05 | R418-04, R418-06 | D418-03 |
| T418-06 | R418-05, R418-06 | D418-03, D418-05 |
| T418-07 | R418-06, R418-07 | D418-02, D418-03 |
| T418-08 | R418-02, R418-04, R418-06 | D418-03, D418-04 |
| T418-09 | R418-02, R418-05, R418-06 | D418-03, D418-04 |
| T418-10 | R418-04, R418-06 | D418-03, D418-05 |
| T418-11 | R418-05, R418-06, R418-07 | D418-03 |
| T418-12 | R418-04, R418-05, R418-06 | D418-06 |
| T418-13 | R418-05, R418-06 | D418-05 |
| T418-14 | R418-04, R418-06 | D418-04, D418-05 |

定义：[Requirements](../../../requirements/versions/current-main-0.6.17-guru.53/requirement-main.md)、
[Design](../../../design/versions/current-main-0.6.17-guru.53/design-main.md)、
[Test](../../../test/versions/current-main-0.6.17-guru.53/test-strategy.md)。
反向索引：[Requirements trace](../../../requirements/versions/current-main-0.6.17-guru.53/traceability.md)、
[Design trace](../../../design/versions/current-main-0.6.17-guru.53/traceability.md)、
[Test trace](../../../test/versions/current-main-0.6.17-guru.53/traceability.md)。
关系为 implements/verifies；来源为 [#418 contribution](../../../requirements-design-test-contributions/418-closeout-identity-recovery/manifest.yaml)，
predecessor .52 -> successor .53；Architecture inheritance 为 .53/active，仅引用
[ADR-010](../../../architecture/adr/010-archived-review-authority.md)、
[ARCH-CUR-030](../../../architecture/01-current/system.md)、
[ARCH-INT-018](../../../architecture/04-integrations/distribution.md)、
[EVD-028](../../../architecture/evidence/current-evidence.md)，不复制正文。
