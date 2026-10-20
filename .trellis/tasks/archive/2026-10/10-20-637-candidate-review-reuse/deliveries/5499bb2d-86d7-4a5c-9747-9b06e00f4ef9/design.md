# #637 D1 候选审核与验证复用设计

## 1. 设计目标、需求承接与内容基线

本批完整承担整体及本批 PRD 的 R637-01..08、S637-01..08、AC637-01..10。目标是以后继候选的真实原覆盖、实际差额和受影响依赖形成当前完整结论，删除没有新事实的重复工作。首次完整独立审核和各 owner 当前正式结果继续成立。

本 Task 没有前序 Delivery。原公开 `DeliveryProjection.content_base` 已从明确 development baseline 解析 B=`39169628f5f79cb48673eae96a36670e73f4dbbb`。Planning H0 等于 B，最终 H 尚未产生；内容是 B..实际 H 加 dirty 增量。PR target 是 `castbox/guru-trellis:main`，不能以 origin/main 后续推进替换 B。

阶段适用 Architecture 为 `docs/architecture/README.md` 的 `.104`、constitution v1、change-contract v1。实际独立 candidate_assessment 返回 `baseline_current / architecture_impact / target_native`，命中 ADR-019/028/029/030/033；该结果只供本次方案写作，不代表 final_plan、实现或晋升通过。

## 2. 当前系统、边界与目标差额

#567 已支持固定候选、无实际阻塞不整合、原完整覆盖加整合差额；#578 已支持工程命令事实的适用性采用；#636 已提供早期 commit/Draft、固定内容分析与验证。本批直接演进这些能力。

当前 Branch Review 的 finding lifecycle 与 promotion alignment 仍要求 finding 闭合后 distinct fresh reviewer 完整重审，与既有差额规则冲突。Architecture 的独立入口需要区分首次独立评估和后继适用性接续。其它 owners、workflow、continuation 和派发入口需要统一读取，避免把重复工作转移到相邻阶段。

目标是在原 canonical `workflow-contract.md` 增加唯一“候选适用性与覆盖”完整小节，七个原 owner 引用并在原职责内执行。原 GateResult 的 candidate、scope_ref、plan_ref、owner、outcome、predecessor、evidence 已能承接正式结果；不新增公共字段、reviewer ledger、跨阶段缓存或长期证明。计划 AuthorityRef 不是原始工程命令日志。

## 3. 来源设计处置（唯一）

| 来源 locator / 条款 | 原承诺 | 处置、设计落点、理由和影响 |
| --- | --- | --- |
| Issue #637 行为1、证据边界 | 首次完整独立审核；后继真实覆盖加差额；合法来源 | retain：§4/5/6。保持完整当前判断，禁止复制旧 pass；无偏离。 |
| Issue #637 行为2/7；#567 contract Fixed complete range | 固定B/H；同树只换绑定；无关base不整合；冲突读组合语义 | retain：§4/6。fetch或最新ancestry不成为业务门禁；无偏离。 |
| Issue #637 行为3；#578 D578-01/02 | 原工程命令定义/输入/依赖/工具链/环境/参数/期望适用才采用 | retain：§4/8。缺原命令则补跑对应项；无偏离。 |
| Issue #637 行为4、证据边界 | 实际职责独立；同合规reviewer可先Architecture后质量审核 | retain：§4/6。消除身份/阶段变化引起的无因重建，仍禁止作者自批。 |
| Issue #637 行为5；原Branch Review finding lifecycle | finding修正后核闭合和受影响覆盖 | change：§6/7。窄替代无条件distinct fresh全量条款；本项明确要求，必要ADR候选保留替代理由。 |
| Issue #637 行为6 | Publication/Merge审自身事实并消费适用内容结论 | retain：§4/6。不重做未变化业务设计，不跳过payload/Issue/HEAD/checks。 |
| Issue #637 行为8、证据来源 | 唯一合同、必要迁移、无新账本或授权记录 | retain：§5/7。直接演进受控consumer，无第二reader。 |
| #636 D636-01..05 / ADR-033 | Draft不写full_review；正式Review有真实Check predecessor | retain：§6/7、V637-07。早期理解可接续，不能机械映射正式pass；本项负责实际接口组合。 |
| ADR-028/030与change-contract | 阶段适用authority；独立Phase2→原owners晋升→最终Check/committed Review | retain：§7/9。不改晋升时机、single-writer或各阶段真实结果。 |

本表是唯一来源设计处置，PRD/implement只引用。除上述明确窄替代，其余来源条件保留；没有待上游确认的scope偏离。

## 4. 模块、职责与设计取舍

共享定义位于 `trellis/presets/guru-team/spec/workflow/workflow-contract.md`。它区分工程执行事实、当前语义判断和Git/PR事实：工程事实在适用条件成立时采用；当前owner必须亲自判断；Git/PR事实按当前动作核验。package step-local合同只写自己的执行、记录和出口，不复制整套规则。平台与continuation只加载、路由，不新增Skill/profile/阶段。

| 原owner / canonical package | 本轮行为差额 |
| --- | --- |
| guru-maintain-architecture-baseline | 首次仍按原独立读序。后继由实际未参与实现的合规reviewer读取原覆盖和全部差额/consumers，判断旧架构结论适用性。新架构事实需要新评估；同合规reviewer可先Architecture后Branch Review，各阶段仍有真实结果。 |
| guru-check-task | 完整scope/九维度仍审；依据原覆盖和真实差额确定受实际差额及依赖变化影响的检查，原工程事实逐项判适用，原record/check/invoke产生当前Check。 |
| guru-create-task-commit | 核精确内容/staging、目标、敏感项、当前Check。同树新提交仅刷新必要绑定；内容变化回受影响owner，提交本身不触发无关重审。早期profile仍只输出早期候选。 |
| guru-review-branch | 保持首次完整独立Review；后继以真实原覆盖、全部差额及依赖形成当前完整结论。finding核闭合及影响，取消无条件新reviewer；原full_review绑定当前candidate/Check predecessor。 |
| guru-review-task-delivery | 消费真实当前Branch Review；审Policy/范围、中文payload、Issue引用、分层验证、安全和部署。无实质变化不重做内容设计。 |
| guru-publish-task-delivery | 读当前payload/候选/live PR，沿原事务push/Draft/Ready/readback；内容适用性和远端事实分别判断。 |
| guru-merge-task-delivery | 核实际HEAD/body/state、required checks、mergeability和Publication relation；消费适用内容结果，真实变化回原owner。 |

修改各canonical Skill/references中的冲突条款与共享引用；`trellis/workflows/guru-team/workflow.md`、preset overlays中continuation、prompt/command及直接派发只修正路由文案，不复制step-local规则。Reconcile仍拥有真实触发及固定目标，不能成为新的内容审核owner。

选择直接修改、删除重复定义与同步consumer。原公开记录和事务足够，不为复用另建覆盖DTO/通用服务。脚本不按后缀、tree相等或reviewer id判断语义适用性。

## 5. 接口与数据

公共Skill/profile/exit、DeliveryKey、GateResult shape、Task schema和远端事务保持。流程为“原profile＋当前公共身份→owner读取共享合同并判断→原recorder/validator→原typed exit/唯一consumer”。没有数据迁移，也不为形式新增schema。

合法来源是：当前调用保留的真实原公开结果/调用对象、public Task/Delivery结果、精确Git对象的原范围和全部差额及当前正文、仍可核验的原始命令结果。原passed full_review的candidate/scope/plan/outcome可定位正式完整覆盖；rework若清理当前slot，可使用仍保留的真实原公开输出，否则走原producer recovery，不能恢复不存在的记录。

首次 `implementation_required` 没有passed full_review。它的commit/finding refs只定位对象和缺陷，不证明已通过覆盖。原完整审核工作必须仍能由实际公开结果、原调用对象、Git和当前正文核验；reviewer已建立的理解只减少重复读取。缺哪段补哪段，组合影响无法界定就完整审核。不得为此保留永久transcript或制造passed结果。

规划AuthorityRef不证明命令执行。缺少原始命令实际结果或适用依据时补跑命中项。当前结论只用原summary/evidence或原owner必要短期checkpoint；不读其它owner私有状态、不重建退休checkpoint、不加hash链或授权字段。

## 6. 状态、顺序、正常与失败流程

1. 固定当前Task/Delivery、B/H、阶段适用authority、职责和检查集合。无关target前进不打断当前对象。
2. 首次候选完整独立审查。后继先取合法原覆盖，再读Hr..Hi全部差额、冲突双方语义、组合结果和受影响未改consumers。
3. 当前owner明确保留/失效/补充范围。导航/版本/引用按真实行为含义判断；同树只说明内容相同，不说明环境和required checks相同。
4. 原工程事实先核定义/版本、输入/依赖、工具链、环境、参数、期望。适用且可验证则注明采用和原来源；变化/未知/缺结果或新检查则执行命中项。
5. 当前owner对完整当前范围形成新结论，经原正式入口绑定精确candidate/predecessor。finding回原stage合法rework；修正后核闭合、修正差额及受影响覆盖。原reviewer仍实际独立且可接续时继续；换人先核证据充分性，不因身份自动全链重跑。
6. 原finding owner可在完成闭合后，以同一合规独立职责完成当前最终覆盖判断；“已修复”不能直接投影passed。原wire值fresh_final_review的窄后继见§7。覆盖不足补审，影响无法界定完整审核。
7. Delivery Review/Publication/Merge各审自身当前payload/Issue/候选/live事实并消费适用内容结果。真实变化回受影响owner；远端等待或输出丢失走原事务恢复，不造新Delivery或空提交。

真实scope、设计前提或依赖变化回最早受影响owner；普通stale/mismatch停在原诊断并同owner新round读取。脚本不能选择“可复用”。mapped recovery自动接续，不增加审批环节。

## 7. 恢复、兼容、迁移与集成

直接演进Markdown及matching安装，无长期兼容reader。`MIGRATION-637.md`明确旧无条件新reviewer/完整重跑条款的替代位置、首次独立覆盖和当前完整判断。保留 `fresh_final_review` wire值与finding continuity机器条件，但明确它表示当前最终结论，不再要求更换身份；旧安装不得悄然消费新语义。公共结构不变，不加enum别名或parser分支。

现有安装继续完整旧合同，或经原升级owner成套切换workflow/preset/packages/consumers，再由同Task/Delivery原阶段owner判断当前候选和仍适用事实。旧pass不转换成新pass；原private只由原owner消费/退休。source编辑或dogfood apply不隐式热迁移开发Task活动安装。canonical/matching dogfood和单clean安装在独立临时验证位置执行完整apply/reapply/drift，逐个处理sidecar。若本Task后续拟采用新语义，先显式matching迁移；此前正式门禁仍按原安装，不能以本候选规则为自己豁免。

#636在B中已交付，组合使用实际安装early TaskCommit/Publication和Draft分析入口；早期不写full_review，正式仍消费真实Check。#638未来接口未交付，由后项负责组合，明确未验证而不等待关闭。不改Backend CI/队列、生产、完整Release矩阵或tag。

## 8. 验证设计

| ID / AC | 层、入口与输入 | 必须观察与限制 |
| --- | --- | --- |
| V637-01 / 01、05、10 | 扩展原guru-check-task/tests/test_delivery_flow.py真实Git/public wrappers链 | 首次Check/Review/Readiness绑定正确，checkpoint消费退休后合法公开来源可接续。fixture语义输入只证明接口，不证明AI。 |
| V637-02 / 02、03、07 | matching installed实际独立Agent：小型文档能力及未改consumer，首次完整→真实文档冲突/定位→finding修正 | 审双方/组合/依赖，说明保留/失效/补充，形成当前正式结果；不因finding无条件换人。 |
| V637-03 / 04、06 | 实际Agent：正常共享Runtime/事务实现错误；另有原命令缺失或环境变化 | 扩到未改consumer并检出具体缺陷；补缺项保留其它适用事实。改产品fixture代码，不手改state/hash构造问题。 |
| V637-04 / 02、05、06 | 原owner tests：同树新提交、无关target前进、输出丢失原recovery、原覆盖不足 | 零无因整合/空提交/新key；缺覆盖补审，无法界定则完整；无其它owner私有读取。 |
| V637-05 / 08 | B旧完整安装与matching新安装：同初始对象、同冲突/修订的#693同构实际Agent样本 | 先比充分性/检错，再分语义工作、命令、正式记录、远端等待计elapsed；记录重复动作。无远端的样本标为本地，不声称远端提速或固定比例。 |
| V637-06 / 01..08 | 七owner定向tests、既有alignment/early Draft tests及命中eval，结合实际Agent输出 | 绑定错误/遗漏依赖应失败。scanner/text只证明分发，不能代替行为判断。 |
| V637-07 / 09 | #636实际installed early commit→Draft/修订→独立分析＋HEAD检查→最终正式链；真实GitHub用本Task授权PR动作 | 同Task/key/PR保留，Draft不冒充full_review，真实Check predecessor和最终资格成立；fixture/Agent/远端分别报告，#638未验证。 |
| V637-08 / 10 | 单代表性clean matching throwaway；canonical/平台投影、apply/reapply/drift/mode/sidecar和在途恢复 | installed owners真实运行、声明平台投影一致、重复apply无漂移；不宣称全平台实际Agent或完整Upgrade/Release矩阵。 |

实际结果由实施阶段唯一Test维护；规划不预填通过。实际Agent样本须完成真实owner语义与正式调用，不从fixture复制pass；远端动作保留各自边界。

## 9. Canonical 引用、本轮差额与实际未决项

`docs/{requirements,design,test}/current/task-delivery-lifecycle.md`（RDT `.113`）是本批命中的三个完整知识单元。本轮收敛固定候选/最终审核/早期Draft适用性，不改整体完成和关闭。Architecture `.104` 的current/domain/integration/governance及ADR-019/028/029/030/033约束本批；实施前读命中完整单元及必要关系。

真实Architecture贡献为 `docs/architecture/contributions/637-candidate-review-reuse.md`，必要ADR候选为本目录 `architecture-adr.md`，承接九concern及窄替代，尚非共享已晋升authority。原Architecture owner在独立Phase2审完整实现/拟晋升内容后，按live expected-current单写晋升；RDT按implement §6处理。最终Check/committed Review覆盖全部实际写入。

当前没有用户产品选择缺口。实际验证、耗时和远端组合待实施；失败不能降格为通过。如果出现现有公开结果无法表达、且下一consumer必需的真实最小覆盖缺口，先回Author/Architecture明确迁移，不能临时加ledger或字段。
