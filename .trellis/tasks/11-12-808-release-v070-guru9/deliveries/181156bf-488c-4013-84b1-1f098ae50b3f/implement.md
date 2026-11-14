# D2：真实采用实施与验证计划

## 1. 输入与引用

完整读取[PRD](prd.md)、[design](design.md)及design第3节唯一来源设计处置，整体[根PRD](../../prd.md)第3.3/5.4/5.5/7节，真实D1 public result/PR839及源head。实际D2 key为`181156bf-488c-4013-84b1-1f098ae50b3f`，内容B来自前序delivered head `ce25043d33e487def1043b4a9fee6cb180844480`，目标名main，Task/gen不变。

采用[原tools完整源合同](../../../../../trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md)、[MIGRATION794](../../../../../trellis/presets/guru-team/MIGRATION-794.md)、[public-docs](../../../../../.trellis/spec/docs/public-docs.md)与[quality-guidelines](../../../../../.trellis/spec/workflow/quality-guidelines.md)的Test And Validation Value和Validation Scope Ownership。源、Fork和目标的本机路径只通过当次对话/原owner私有参数解析；不写tracked workspace映射。

## 2. 有依赖顺序的步骤与文件责任

| ID | 前置/owner、具体动作与文件 | 完成观察 |
| --- | --- | --- |
| I1 | 完整Planning/Activation后，原tools owner读真实D1 delivery_result，核完整clean H2来源及其lock对应的既有clean Fork build；核当前明确Task checkout、实际unfinished transactions与shared paths | 原preview输入来源配对与唯一目标正确；旧操作先合法终结/恢复，无安装或转换旁路 |
| I2 | 原tools源入口审查实际inspection和managed差额；选择实际Claude/Codex/Cursor，按design5准备AGENTS custom/source/content、Guru custom workflow、原Guru per-path decisions；单次prepare并保实际frozen plan，展示精确写集后原invoke | public maintenance与原installer生成完整当前after；记录原正式tools输出或同operation恢复，不重prepare、不手改manifest/受管字节 |
| I3 | 原实施/原tools使用真实目标自己的resolver、installed runtime、native continuation及原preservation结果；核完整managed/source/lock/版本/platform/workflow/ownership/drift/mode/sidecar | AC04目标可用与保留成立，unverified为空。保存原失败事实；具体缺口返原owner |
| I4 | 采用成功后，原docs实施者只改README.md快速安装/来源版本章节及workflow/preset README的当前版本/Apply And Verify段 | 以canonical `.9`为源码目标；`.9`安装示例明确以正式非draft/nonprerelease Release存在为执行条件。`.8`改为准备起点的正式前驱事实；保历史能力/来源说明及public anchors。移除只适用于D1未采用状态的当前断言，保版本/来源/安装/发布各自验证边界，不写“已发布”或本次pass登记 |
| I5 | 原RDT/Architecture owners读取真实完整after和命中现行单元；有真实delta则准备完整目标并原final_integration/readback，无delta则原no_change；工程执行V4/V5及受影响检查 | 必要知识after在TaskCommit前完整；无空contribution/ADR/共享root登记。工程结果不建立独立Review结论 |
| I6 | 原TaskCommit精确提交全部本批安装、文档和规划after；原constructor/begin_check绑定完整B..H；新独立Review、eligibility、readiness、原Publication/expected-head Merge | D2自身完整真实交付，中文Refs-only。原Completion再审全部准备业务，后续Closure/Finish/Cleanup及Stage2各自接续 |

每次source/test/Task artifact写入前原boundary checker验证。工具更新只由完整clean来源的原tools写受管目标；docs writer不手工同步这些文件。未批准的机制/范围观察仅返candidate_ref、observed_behavior、locators、minimal_reproduction_hint，原owner判断前不自修、加test或severity/route。

## 3. 验证入口、输入与预期观察

### V1/V2：真实来源与原tools生产路径

先核D1已MERGED的PR839/公共result及源commit、clean状态、canonical manifest和其lock，再核实际Fork build-origin与CLI/Core公共maintenance API。源provider的canonical package root由当次实际来源定位为`trellis/skills/guru-team/packages/guru-upgrade-tools`。以下变量均为当次输入，不写入tracked文档或新helper：

```bash
bash "$GURU_D2_SOURCE/trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/preview.sh"   --root "$PWD" --input "$GURU_TOOLS_INPUT" --upstream-source "$GURU_UPSTREAM_SOURCE"
bash "$GURU_D2_SOURCE/trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/prepare.sh"   --root "$PWD" --input "$GURU_TOOLS_INPUT" --plan "$GURU_PRIVATE_PREPARE"
bash "$GURU_D2_SOURCE/trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/invoke.sh"   --root "$PWD" --input "$GURU_TOOLS_INPUT" --plan "$GURU_FROZEN_TOOLS_PLAN"
```

`GURU_TOOLS_INPUT`为design5既有install输入，source_ref真实H2、source_locked与明确当前checkout。upstream descriptor来自实际源/匹配SDK的身份、byte identities和lock；private-prepare为原schema的实际inspection decisions。`GURU_FROZEN_TOOLS_PLAN`只承接prepare实际receipt.result.plan，不手工重造其operation ID或目标。先完成AI审查及当前精确副作用展示；脚本不能从变量或receipt推导充分性/授权。

预期原public/tools都成功，actual installed extension `.9`、CLI `.6`、clean H2 provenance和lock一致，选定完整平台集合/受管writes准确；未完成只沿实际recovery_ref同source/plan恢复。preservation按原owner读回完整范围，不能从Git diff为空推出保留。

### V3/V4：真实目标验证与完整集合

原tools本身在成功前运行真实目标installed与native continuation；消费其实际结果并读必要stdout。工程执行以下目标本身入口及完整字节检查：

```bash
bash .trellis/guru-team/runtime/resolve-python.sh   "$PWD" "$PWD/.trellis/guru-team/runtime"   -m runtime.validate --root "$PWD" --mode installed --json
bash .trellis/guru-team/runtime/resolve-python.sh   "$PWD" "$PWD/.trellis/guru-team/runtime"   "$PWD/.trellis/scripts/get_context.py" --mode continuation
bash trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
```

实际native须读到当前Task/D2及正确Phase2 continuation；旧历史的maintenance诊断不代表当前D2可用。完整映射复用原installer `managed_source_projections`/`canonical_bytes`只读比对，不复制hash/mapping算法，不新增长期helper。核完整expected managed set、当前manifest/source/selected_platforms、CLI、workflow和source lock，以及源和目标原规则下的执行mode。installed validator负责完整public package/platform inventory、mode及退休public Codex根清退。原tools own preservation/public postvalidation覆盖Task/archive/workspace/session/user config、peer/common pointers；任何缺失或未知都保持未验证。

官方tools内容采用后的projection核对使用已有`verify_dogfood_upstream_projection.py --repo-root . --fork-source <实际匹配Fork> --json`；该层仍是projection，与目标实际native结果分别报告。不运行普通apply以绕过历史guard，不新增throwaway。扫描本次受管目标及工作区`.new/.bak`/Python residue，保原existing baseline并禁止新未处理残留；新冲突原owner处置。

### V5/V6：文档、完整质量与交付

检查三个README changed links/anchors、命令block的Bash语法及真实条件/版本语义，运行`git diff --check`；保`guru-team-extension-version`、`发布身份边界`和原安装导航。只修改当前说明，不回写历史test失败或Stage2观察。无代码源新增，不为版本字面或文案添加测试。

D1私有10项、verifier6+1、版本3项、源/临时完整投影和CI结果按inputs/dependencies/toolchain/环境/定义/期望的实际适用性采用；本批不改变这些源机制。当前source validator可由已核未变源结果支撑，实际受影响安装/target检查全部执行。若具体schema/native/consumer因after变化失效，在原owner补该受影响验证；不是惯例全suite重跑。

全部安装/文档after进入本批精确TaskCommit及固定完整committed Review，真实新reviewer的Architecture/九维/fullReview和当前readiness之后才Publication。命令、fixture和parity不证明AI语义审核或GitHub结果。满足所选AC和具体证据缺口后停止追加实验；Stage2的fresh唯一candidate gates另行执行。

## 4. 停止条件与适用回退点

| 实际条件 | 原停点/consumer |
| --- | --- |
| live来源/accepted_scope/六输入实质变化、版本占用 | 原Clarify/Planning刷新受影响范围，不私改根PRD或B |
| 来源不clean/不是D1 delivered、Fork/build/API缺失或身份不配 | 原tools/source owner补真实前置；不local_candidate伪装、不改锁/marker或全局包 |
| unfinished operation覆盖本写集 | 该操作原owner及原source pair/plan恢复后，才新operation；不删checkpoint或refresh rollback anchor |
| unknown owned edits/AGENTS capability或custom目标错误/shared whole-.trellis alias | 原tools在写前审具体差额与合法决策；无法保留则具体blocked，不转完整迁移 |
| tools partial/stale/mismatch/sidecar/native/preservation不满足 | 原tools同operation恢复，必要rollback独立审查；不重复prepare/效果或手修生成物取得pass |
| 代码/说明/断言或Knowledge真实缺口 | 原writer/maintenance修复并整合；机制变化返原Architecture/Planning，普通工程修复后补受影响验证 |
| commit/Review/PR/merge输出丢失 | 原owner核真实同operation结果恢复；不造空提交、pass或第二PR |

没有数据迁移、生产部署或业务回滚。本地tool rollback仅用原维护合同，不reset/revert用户并行工作。权限及敏感数据规则保持。证据不足不记pass；设施反复失败回原入口诊断或保具体缺口，不无限追加实验/扩矩阵。

## 5. Delivery Policy（唯一）

选择 **staged**。本批为整体准备的 **D2实际采用** 阶段；scope_ref仅AC-01/03/04/05/06。D1真实delivered及原Completion/Creation已经成立；当前进入条件是本批完整Planning/Activation及原tools实际来源前置。

本批完整承担实际`.9`安装、保留和target可用性、必要当前说明以及自身工程/知识/提交/独立Review/readiness/Publication/Merge。退出条件为这些要求全部满足且D2真实delivered；不把D1来源通过当本批通过，不把实际未实施工作称evidence_pending。原owner完整比对确认安装来源的managed资产/lock与最终候选一致时，保真实已提交provenance，不追最终自引用HEAD。

本批没有延期的准备实施能力。若仍有真实准备业务缺口，原Completion按实际事实回原owner或新增必要Delivery；全部准备业务无剩余才可能completed。随后Closure no_mutation、acceptance-finish Architecture、Finish唯一归档/bookkeeping及精确Cleanup各自完成。D2合并不关闭#808；fresh main发布candidate、独立gates、tag/smoke/Release、eafc/primary最终收敛和最终Issue关闭由Stage2原owner承担，不成为本批循环前置。

D1“未实际采用”的限制只针对当时真实checkout，其解除条件是本批原tools正式成功与完整目标证据；当前说明在条件满足后由I4更新，历史原观察保留。没有全Task或整个版本冻结。

## 6. Docs SSOT Plan（唯一）

选择 **delta_first**。原writer先读取真实after，只写命中的完整当前单元；必要知识在TaskCommit前原owner整合/readback，提交后独立完整Review审actual after。

| 目标及原writer | 实际差额与直接consumer | 处理与验证 |
| --- | --- | --- |
| installer生成的`.trellis/guru-team/**`、spec及实际受管平台/入口/manifest/配置/AGENTS块；原tools/installer | 本checkout真实`.8`→`.9`采用与matching原公共tools，consumer为目标原resolver/native/Skill与用户 | 只由原生产owner生成/清退并验证，保Task/session/user/peer/pointers，无手工副本同步 |
| README.md与workflow/preset README受影响完整版本/安装章节；原docs实施writer | D1来源已交付且本批真实采用后，原“当前未发布准备/尚未采用”陈述须改为源码目标、Release存在条件、历史前驱与验证职责；consumer为安装用户和Release reviewer | 维护目标`.9`条件安装示例与版本语义，保anchors及历史`.8`来源事实；不写本次pass/最终HEAD/Release状态，核links、shell语法和diff |
| lifecycle现行R649/R794、D649/D794、T794；原RDT maintenance | 已定义原tools正式采用与限制解除，本批不新增通用机制；直接consumer为实施、Review及Completion | 原owner核实际after及完整关系，真实no_change不造空贡献；若真实文义缺口则原完整target整合/readback，不追自身最终结果 |
| ARCH-DOM-010/ARCH-INT-015；原Architecture maintenance与新独立committed reviewer | candidate assessment无新架构impact，D1现行单元已承接D2；consumer为质量/下游eligibility | 实施after仍核真实scope/risk/owner变化；无delta走原no_change，无contribution/ADR；真实变化回原owner，不由Planning预填实现结论 |

保D1的原规划、历史失败/unknown和test观察，不改根accepted_scope、RDT/Architecture root/index、spec规则或source lock。本计划不创建task-local release notes、PR/Release body handoff、动态checklist、发布ledger、状态提交或授权记录。
