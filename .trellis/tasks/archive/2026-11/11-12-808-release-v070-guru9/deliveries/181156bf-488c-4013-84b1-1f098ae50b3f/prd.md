# D2：v0.7.0-guru.9 真实 dogfood 采用需求

## 1. 整体来源与术语

本批为 Task `808-release-v070-guru9` / generation `0` 的 Delivery `181156bf-488c-4013-84b1-1f098ae50b3f`，profile `pull_request`。整体权威为[根 PRD](../../prd.md)，accepted revision `sha256:835586c0c5ca6a22a50a872ce8249a2548dfac4d6f84a4321f78f4d06addb950`；本批选择 AC-01、AC-03、AC-04、AC-05、AC-06，planning_root 为本目录。根要求未变化。

| 来源与章节 | 角色与本批用途 |
| --- | --- |
| [#808](https://github.com/castbox/guru-trellis/issues/808)：前置与准备范围、正式发布与本地收尾、范围边界 | 要求：实际 dogfood 由原 tools source_locked 完成；准备 Refs-only，后置发布及两个最终本地目标另行履行 |
| [根 PRD](../../prd.md)：3.3、5.4、5.5、7；R-01/03/04/05、AC-01/03/04/05/06 | 已接受要求：D1 delivered 后 D2 才实施，全部安装 after 进入本批完整质量与交付链 |
| [私有发布合同](../../../../../.agents/skills/release-guru-trellis-version/references/contract.md)：Complete Source Before Actual Adoption、Whole Preparation Completion | 规范性设计：原 Completion→Creation→独立 Planning/Activation→原 tools；不从本地来源提交直接安装 |
| [MIGRATION-794](../../../../../trellis/presets/guru-team/MIGRATION-794.md)：第1、4、5节 | 规范性设计：同一提交后 Review 双槽及 matching 原 provider 恢复；保用户/Task/session，不转换旧 pass |
| [tools 合同](../../../../../trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md)：Forward behavior、AI Review Gate、Deterministic execution | 既有安装约束：干净完整源与锁定 Fork、明确 checkout、preview/单次 prepare/原 invoke/验证及原同操作恢复 |
| [D1 PR839](https://github.com/castbox/guru-trellis/pull/839)及公共 D1 delivery_result | 历史事实：真实完整来源交付；不作为本批安装、审核或整体完成的通过结果 |

真实 dogfood 指原 Identity/Ensure 解析并在当次对话明确展示的当前 Task checkout 的完整受管安装。本机路径只留当前对话或原 owner 私有输入。`source_locked` 表示原 tools owner 已验证实际 Guru/Fork 来源配对；版本字面相同不构成配对。

## 2. 整体与本批目标、非目标

D1 已交付完整 `.9` 来源，当前 Task checkout 的 installed extension 仍为 `.8`。本批完成 AC-04 的真实 `.9` 采用，并维护实际解除来源/安装差额后必要的当前说明。CLI/Core 保持 `0.7.0-castbox.6`。

本批目标：从已 delivered 的完整干净来源，经原 tools 更新全部选择的平台、workflow、packages、runtime、schema、受管文档和入口；核实际目标可用性与保留边界；将全部安装和必要文档 after 纳入自身原 TaskCommit、独立完整 Review、readiness、Publication/Merge。

本批不重写 D1 历史、根 accepted scope 或 source lock，不修其他开放 Issue，不改上游源码/全局包，不转换历史 Task，不扩累计多平台矩阵。Stage 2 的 fresh candidate、tag/smoke/Release、两个最终本地目标和最终关闭 #808 不属于本批。没有业务 API、数据库或生产部署变化。

## 3. 本批起点、前序结果、依赖与剩余责任

D1 `b40421e8-6213-4f29-bb11-8d3919e533b0` 已由原 Merge 实际 delivered：PR839、merge `647df4de6c4443720b4bacb674dbe3909333bf4d`、reviewed head `ce25043d33e487def1043b4a9fee6cb180844480`，public result `delivery:647df4de6c4443720b4bacb674dbe3909333bf4d`。D1 的私有链、版本消费者、来源样本与知识 after 已交付；原完整 Review 为 passed，三平台定向 CI 通过。

原 Completion 实际返回 additional_delivery_required，原因是实际采用未实施；原 Creation 才建立本 D2。当前 HEAD 为 D1 reviewed head，Task/current selection 已核，当前 installed `.8` 的来源差额保留原观察。D1 样本、fixture/native projection_parity 或历史 pass 不证明本批目标采用。

正式来源须可解析为 D1 真实交付的干净完整 commit，并核其 canonical lock 对应的 Fork build；取源、临时 checkout 和工具调用由实施阶段原 owners 展示精确边界。若来源/未完成事务不满足原合同，先回原 owner，不另换方案绕过。

本批交付后，原 Completion 仍核所有准备义务。只有准备业务无剩余才可能 completed；随后 Closure no_mutation、acceptance-finish Architecture、Finish 归档/bookkeeping 和精确 Cleanup。#808 继续保留全部独立 Stage 2 责任。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置与动作 | 可观察结果 |
| --- | --- | --- |
| D2-SC-01 来源与目标解析 | 本批实施/原tools；Planning/Activation后读取真实 D1 result、完整干净源及源自己的 lock，核匹配 Fork build和明确目标 | preview 指向本 Task checkout 与真实配对；旧 unfinished operation 先由原 owner 恢复 |
| D2-SC-02 正式采用 | 原tools审查实际managed差额、用户配置/AGENTS/workflow、platform/pointer，单次prepare并invoke source_locked | 原installer生成实际 `.9` manifest及完整受管after，Task/session/user config、peer和common pointers保留 |
| D2-SC-03 目标验证 | 原tools/工程执行者使用目标自己的resolver、installed validator/native entry，核完整源映射、CLI/lock、ownership/platform/drift/modes/sidecars | 当前工具能读取真实公共Task/D2并进入原下一owner；零未解决冲突/sidecar，非仅源runtime成功 |
| D2-SC-04 当前说明收敛 | 原实施及RDT/Architecture owners核真实安装after和前序限制解除条件 | 适用README/指南/断言准确；历史失败保留，不预称正式Release已发布 |
| D2-SC-05 独立交付 | 完整工程及必要知识整合后，原TaskCommit→constructor/begin_check→新独立完整Review→readiness→Publication/Merge | 全部D2安装及必要文档after进入自身候选，Refs-only；不由D1 pass代替本批通过 |
| D2-SC-06 正常失败与恢复 | 原owner遇stale/source mismatch、冲突/sidecar、输出丢失或未完成事务 | 保原source pair/operation/plan，合法resume/rollback；保事实，不重复效果、改manifest或转换历史 |

## 5. 完整行为、条件与约束

**D2-R-01 来源与目标（AC-01/04；SC-01）**：六项发布输入保持根PRD定义。仅真实D1 delivered来源可供本批正式采用；使用完整干净源及其自己的lock，CLI与Core均匹配真实Fork commit/build。调用上下文不是安装目标；明确选择当前Task checkout，不扩至primary或其它peer。primary的最终收敛留Stage2。

**D2-R-02 完整正式安装（AC-04；SC-02/03/06）**：使用原guru-upgrade-tools source_locked的preview、一次prepare、invoke及同操作恢复。按实际安装平台维护Shared/Codex/Claude/Cursor投影、workflow、packages/runtime/schema、受管spec/入口及完整manifest。未知用户编辑、旧owned preimage和未完成操作依原合同处置，不普通apply、不手改生成文件、不把local_candidate改称正式来源。CLI文件仍为`.6`，installed extension为`.9`，provenance如实指向真实干净来源。已提交来源经原owner完整比对、确认其受管内容与lock和最终候选一致时，该来源继续有效；不追自引用最终HEAD。

**D2-R-03 保留与真实可用（AC-04；SC-02/03）**：Task、archive、workspace、session与用户配置字节保持，peer工具及common/peer runtime pointer不变；只更新本目标合法工具写集。运行目标自己的resolver、installed检查和实际native入口，验证当前公共Task/D2的正常读取/接续；旧历史仍留给独立maintenance，不转换成当前对象。完整managed集合、来源字节、执行位、CLI/lock/workflow、所有实际平台、ownership和drift均核对。任何未解决冲突、`.new`/`.bak`或缺失必要native证据均不报tools_upgraded。

**D2-R-04 文档/断言承接（AC-03；SC-04）**：D1的来源已交付、实际采用限制在本批满足后，维护真正受影响的当前说明与断言，保留D1原失败/未知记录。三个README的版本说明以canonical目标和已验证安装语义为依据；安装命令只将真实已发布tag用于稳定安装，marketplace/preset必须同一immutable来源。对`.9`正式发布使用明确条件，避免发布前虚称已发布或发布后仍永久断言未发布。当前需哪些完整单元、具体写法和验证由后续Docs Plan及原owners细化，不制造发布状态账本或追逐最终pass的额外提交。

**D2-R-05 完整质量与交付（AC-05/06；SC-05）**：原工程检查、必要RDT/Architecture整合/readback后才原TaskCommit；固定范围基于真实前序delivered head，完整本批after不漏选。提交后新独立reviewer同次完成Architecture、全部Check与完整Review职责，当前零P0-P3 finding后才readiness/Publication；必要修复仍由原writer提交并补受影响审核。中文PR正文真实区分D1来源、本次实际采用、验证层次及剩余终态/Stage2，Refs #808。所有副作用原owner各自展示精确计划，授权只留当前对话。

没有新业务接口、持久化字段或数据转换；公共Skill API、原workflow阶段和typed exits不变化。仅诚实受支持正常路径与常见stale/mismatch/恢复，不新增对抗、竞态压力、fault injection或通用加固。

## 6. 本批验收、验证方式与未决项

| AC | 要求/场景与验证入口 | 预期观察及边界 |
| --- | --- | --- |
| AC-01 | D2-R-01/SC-01：fresh live #808、D1 public result/PR/源commit，canonical/installed/CLI/lock和Fork build | 版本/来源唯一，真实D1依赖成立；来源配对不由相同版本字面推断 |
| AC-03 | D2-R-04/SC-04：三份README、原Docs Plan、命中完整知识单元及必要断言 | 当前说明符合实际解除条件与发布条件，历史原义保持；必要整合已读回，无空贡献或重复authority |
| AC-04 | D2-R-01/02/03、SC-01/02/03/06：原tools实际source_locked与目标完整读回 | `.9`/`.6`/真实source及完整managed资产、平台/workflow/lock一致；目标resolver/installed/native可用，preservation/mode/sidecar/ownership/parity/drift成立 |
| AC-05 | D2-R-05/SC-05：实际after、原提交和固定完整独立Review | 全部安装与必要说明进入本批自身候选；当前独立结论有效，D1通过不替代本批通过 |
| AC-06 | D2-R-05/SC-05：publication eligibility、Delivery Review→Publication→expected-head Merge | 真实中文Refs-only payload，实际交付head匹配；不关闭#808或宣称整体发布完成 |

没有待用户决定的需求问题。精确源取得、tools冻结计划、完整验证入口和Docs差额由后续Author/Architecture展开；当前requirements_ready不代表规划批准、安装已执行或本批验收通过。必要来源/环境缺失在原owner停，实质范围变化回Clarify，普通规划遗漏回Author。

## 7. Canonical 引用与本轮差额

- [RDT requirement](../../../../../docs/requirements/current/task-delivery-lifecycle.md)：R794-01～07与R649，承接逐Delivery链、实际采用及限制解除；本批实施既有机制，原owner再核真实差额。
- [RDT design](../../../../../docs/design/current/task-delivery-lifecycle.md)：D794及D649，承接原tools、知识/提交/独立审核顺序，不新增生命周期或API。
- [RDT tests](../../../../../docs/test/current/task-delivery-lifecycle.md)：T794-05/06/07，分开source/fixture、真实Agent与目标安装证据；不重复D1未变来源suite或扩矩阵。
- [Architecture入口](../../../../../docs/architecture/README.md)、[ownership ARCH-DOM-010](../../../../../docs/architecture/03-domains/ownership.md)、[distribution ARCH-INT-015](../../../../../docs/architecture/04-integrations/distribution.md)：D1已整合的来源→采用关系和原owners，后续独立assessment从固定authority核是否真实有增量；不预填no_change或造空贡献。
- [public-docs](../../../../../.trellis/spec/docs/public-docs.md)：三个README职责、版本来源及同源安装；本批只维护实际过时当前说明，不改全局规则。
- [quality-guidelines](../../../../../.trellis/spec/workflow/quality-guidelines.md)：Test And Validation Value、Validation Scope Ownership，选择证明本批实际采用的最小可靠集合，采用可核验未变D1事实，保全部AC04验证。

本批只写自身规划，不写共享authority或D1规划；必要知识after仍由原维护owners在实施阶段合法整合/readback并进入独立提交审核。
