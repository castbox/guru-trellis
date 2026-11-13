# Task / Delivery 生命周期测试策略

导航别名：`BEH-001..006`；`R531-01..05/08`；`R636/BEH636`；`R637/BEH637`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/test/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

本次 #679 拟整合的完整前驱：Git `e6c3b8276d62ac174ab42cba5bca4d5784be2ca3:docs/test/current/task-delivery-lifecycle.md`。来源及窄补充见 [#679 追踪](../../requirements-design-test-contributions/679-session-continuation/traceability.md)。

本次 #649 最终整合的完整前驱：Git `4fea68613de4181d7cb55532b8758515472ba31b:docs/test/current/task-delivery-lifecycle.md`。贡献、#657 继承及原来源见 [#649 追踪](../../requirements-design-test-contributions/649-stage-result-convergence/traceability.md)。

并行 #663 晋升的完整前驱：Git `e9583202b67750d7b3ec2b7eab4b037c0c52a226:docs/test/current/task-delivery-lifecycle.md`；来源及窄修改见 [#663追踪](../../requirements-design-test-contributions/663-contract-continuity/traceability.md)。

更早晋升的完整前驱：Git `319202beab79c7666ecdb855291bf117e43d407e:docs/test/current/task-delivery-lifecycle.md`。贡献与窄替代边界见 [#657 追踪](../../requirements-design-test-contributions/657-workflow-continuation-conflicts/traceability.md)。
知识单元：`RDT-TST-LIFECYCLE`。状态：`current`。authority identity：`guru-trellis-rdt`；精确内容由完整Git revision与locator定位；较早历史完整定义为 immutable Git `39169628f5f79cb48673eae96a36670e73f4dbbb:docs/test/current/task-delivery-lifecycle.md`（RDT `.113`），更早迁移来源和稳定身份保留。需求：[RDT-REQ-LIFECYCLE](../../requirements/current/task-delivery-lifecycle.md)；设计：[RDT-DES-LIFECYCLE](../../design/current/task-delivery-lifecycle.md)。本单元拥有场景/预期和结果定位；历史结果不等于当前候选通过。

## 策略与完整性

以真实公共owner链验证合法正常路径、普通缺失/过期/输出丢失及完整候选。AI审查职责、因果关系和门禁充分性；schema、测试或脚本只证明其客观层次。不制造恶意artifact/伪造hash/对抗绕过、未要求的锁/压力/崩溃负例。实际Agent、runtime/package、source/dogfood/installed、provider/live、Release证据分别说明。

`TST-002/003/004/007`、`CASE-001/002`、`SCN-001..004` 的 orchestration/AI-script/compatibility身份保留；其旧Task级开发入口和Finalizer顺序已由R531/ADR-030替代，不把旧断言作为当前预期。当前完整场景如下。

| 稳定scenario/test identity | 正常起点/动作 | 必须观察 |
| --- | --- | --- |
| T531-02 / R531-01/02 | 同Task建立D1、独立D2，分别写规划 | key/root/文档和历史分开；Task scope持续；唯一Author、独立Wording/Architecture/Approval，Activation是真公共Planning writer。 |
| T154-02/03/04 | 全量、partial、后继和返工；详细来源及规范性承诺 | 真实完整来源被读取；Task与slice正文分明；设计处置唯一且保条件；Policy/Docs Plan不重复；下游实际消费正文。 |
| T531-03 / R531-03 | 同slice scope/方案变化、部分/全部撤回，各真实stage | 原Clarify及最早stage合法rework，身份/PR/history保留；stop/release不冒充delivered；独立工作不因局部provider缺口阻断。 |
| T531-04 / T530-01..05 | dirty精确提交；clean既有候选完成真实工程/整合后首次Review；普通stdout loss | 真实内容进入commit，clean零空/重复commit；Review输入绑定实际H；完整独立Architecture/Branch Review；旧gate不冒充current。 |
| T600-01/02/03/04/05/06 | authority变更的完整tracked/untracked候选与proposed targets；无变化控制 | 原owners提交前整合/readback→TaskCommit→完整committed candidate/begin_check→同次独立before/after/九维/fullReview；no-change无空文件/ADR/commit；mismatch/partial/conflict走原owner。 |
| T535-01..04 | 完整Review无候选，或非空全rejected | 真空集[]与分类区分；完整维度/Docs/Architecture/freshness及route仍审，不凭空集自动passed/ready。 |
| T531-05 / T557-01..04 | 原Publish/Merge成功后投影/输出丢失；正式发布后人工双亲merge | 实际成功读回且零重复副作用；历史事实不等新gate；actual head/CI/delta交Completion；不执行第二merge。 |
| BEH567-01..05 / 该源T567链 | 各阶段固定B/H；无关target前进；实际冲突/依赖同步 | 固定候选正常前进、默认零Reconcile；仅真实触发固定一次target，恢复同Delivery，不追赶、不重放无关门禁。 |
| T531-07 / R531-07 | 完整匹配安装及显式旧数据迁移 | canonical/installed/native/reapply一致，旧公共/私有迁移分owner；source修改不证明旧业务/production已采用。 |

## T657：当前续接、选择与范围修订

| 稳定场景 | 正常入口和观察 | 证据边界 |
| --- | --- | --- |
| T657-01 / R657-01 | V1/V2：无原 created/runtime 的独立 common-dir clone，经正式 identity/binding/rebind revision>0/Ensure/Bind 与原 owner合法写入 | 一个 matching installed/native 实际 Agent 样本，不以解析DTO或fixture代替 |
| T657-02 / R657-01 | V4/V5：同阶段无scope变化，真实stale/mismatch/缺ref/歧义 | 保留适用结果；错误写前停止且原工作及无关Task保持 |
| T657-03 / R657-01 | V6：初始创建与同操作输出丢失 | 原精确身份/绑定/资源校验保持，恢复同结果而非重复创建 |
| T657-04 / R657-02 | V11：planning及implementing/checking/reviewing/publishing选择和恢复 | 公共phase保持，真实consumer进入原owner；至少一个实际Agent完整消费 |
| T657-05 / R657-03 | V3/V12：revised/no_change/withdrawal_required，有/无current Delivery | pre-Author→根PRD→acceptance→post-Author→原stage；真实rework/stop，无旧clear/DTO/空切片；至少一个原生闭环 |
| T657-06 / R657-04 | V8/V9/V10：Discovery当前身份、Review真实candidate/readiness refresh、verifier旧输入诊断与合法standalone入口 | 原validator严格性保留，不索取旧branch/status或退役current Finalizer |
| T657-07 / R657-04 | V7：canonical/package/dogfood/installed/platform、reapply/drift/mode/sidecar | 分层报告真实采用，最多一个clean安装；不证明完整Release矩阵或业务现场 |

本批唯一实际结果位于 [#657 Test](../../requirements-design-test-contributions/657-workflow-continuation-conflicts/test.md)。历史结果保留原对象，不能推定当前候选通过。

## 执行入口与结果消费

完整精确测试命令由受改package的现行tests和其owner选取；公共profiles/DTO以[canonical packages](../../../trellis/skills/guru-team/packages)为准，不在此固定易漂移计数。历史结果在各原contribution的唯一test中：[#531](../../requirements-design-test-contributions/531-task-delivery-lifecycle/test.md)、[#154](../../requirements-design-test-contributions/154-planning-body-contract/test.md)、[#530](../../requirements-design-test-contributions/530-clean-committed-reentry/test.md)、[#600](../../requirements-design-test-contributions/600-promotion-before-check/test.md)、[#557](../../requirements-design-test-contributions/557-manual-merged-delivery-recovery/test.md)。它们保留原candidate、首次失败和未验证边界，不能由本轮链接宣称重跑。

本轮迁移/查询证据是 T331-01/V331-A、T331-05/V331-E及相关新旧对照；实际全部结果唯一写 [#331 test](../../requirements-design-test-contributions/331-current-effective-knowledge/test.md)。测试owner逐次判断完整性，保留首次失败与修复；当前本文只定义预期。Whole Task实际完成另由Completion，Release完整矩阵和外部业务采用不由此推定。

## T636：原本地提交与旧 Draft 迁移场景

T636-01..07稳定身份和#636原专项结果保留，当前受#794窄替代的输入/预期如下；旧已发生事实仍按其原provider解释。

| Test identity | 正常入口与输入 | 当前必须观察及边界 |
| --- | --- | --- |
| T636-01 / R636-01/03 | 激活implementing，工程/知识整合完成但无先验Check，原TaskCommit pre-review invoke | 真实精确非空本地提交、中文消息/敏感/hook/paths正确；只交固定候选Review，无push/PR或独立pass。 |
| T636-02 / R636-03/04 | 旧同PR Draft/Ready中有实际已执行和pending动作，当前新HEAD未审 | 原迁移owner保同PR/key/历史，不因pending先push；新远端动作待当前独立Review/readiness。 |
| T636-03 / R636-04/06 | 原commit/push/create/edit/状态已成功但输出丢失 | 同操作精确readback、零重复commit/PR/mutation；已执行事实不变成新pass，SKIP/失败保持。 |
| T636-04 / R636-02/05 | 固定B/H和真实target/组合缺口 | HEAD内容审核/命中命令与组合T/M分开；目标前进不缩范围，冲突/无merge-ref/CI未触发保缺口，不推定业务CI。 |
| T636-05 / R636-04/06 | 当前独立Review后原readiness/Publication/Merge；full/partial/目标对照 | 全部Delivery Refs-only；旧Draft/Ready/merge不证明Task完成；只有当前适用full_review/readiness可新发布。 |
| T636-06 / R636-07 | matching packages/workflow/runtime、平台/dogfood/reapply | 真实I/O/唯一consumer匹配，mode/sidecar/drift正确；source不证明业务采用。 |
| T636-07 / R636-06/07 | 旧Check/已提交/已审、Draft实际已执行或pending、正常输出丢失 | 固定provider与MIGRATION-794明确原owner/阶段处置；不转换pass、不重复外部动作，pending回当前审核/readiness。 |

历史实际结果唯一在 [#636 Test](../../requirements-design-test-contributions/636-early-draft-pr/test.md)，当前差额结果在 [#794 Test](../../requirements-design-test-contributions/794-postcommit-review/test.md)；两者不互相回填。

## 候选适用性与覆盖完整场景

| Test identity | 正常起点与实际入口 | 必须观察与证据边界 |
| --- | --- | --- |
| T637-01 / R637-01/04 | 原公共 Task/Delivery 和七 owner 首次完整链 | 首次真实独立完整覆盖、同次实际check/full_review/candidate/predecessor；Planning、自检和 Draft 反馈不替代。 |
| T637-02 / R637-01/02/05 | matching installed 实际 Agent；首次完整后真实文档冲突、定位修订及未改 consumer | 原覆盖加双方/组合/完整差额与受影响依赖形成当前完整结果；finding 修正后核闭合及覆盖，无无因换新全量。 |
| T637-03 / R637-03 | 正常共享 Runtime/事务实现缺陷，原命令缺失或环境改变 | 扩审未改 consumers 并检出具体缺陷；缺项补跑，其余可核验事实按当前适用性采用。 |
| T637-04 / R637-02/07 | 实际同树新提交、无关 target 前进、公开输出恢复与已退休 checkpoint | 固定 B/同 Delivery；只刷新必要绑定、不假定环境；旧 gate 不冒充当前，缺覆盖补审，无私有跨读或重建。 |
| T637-05 / R637-04/05/08 | 旧/新完整安装的同初始实际 Agent 样本 | 先比较充分性/检错，再分别实测语义、命令、正式记录、远端等待和重复动作；fixture/scanner 不证明 Agent 行为，不预设收益比例。 |
| T637-06 / R637-06/07 | 旧#636实际事务与当前同PR/HEAD审查后发布入口 | 同key/PR准确恢复已执行事实，pending远端动作先当前独立Review/readiness，真实双槽predecessor与payload/live资格；#638当前组合按T638实际证明，不从历史通过推断。 |
| T637-07 / R637-08 | canonical/声明平台、单 clean matching、reapply/drift/mode/sidecar 与在途恢复 | 完整 matching 投影和实际 installed owner 运行，旧完整安装固定或原 owner 显式成套迁移；不推定全平台实际 Agent、业务/生产或完整 Release 矩阵。 |

本轮实际命令、首次失败、Agent/fixture/installed/remote 层次、分阶段耗时及未验证边界唯一由 [#637 Test](../../requirements-design-test-contributions/637-candidate-review-reuse/test.md)维护。本文定义完整策略，不将规划、旧结果或知识晋升当作通过证据。

## T638：候选到真实最终内容

T638-01..07的完整场景由 [knowledge test](knowledge-maintenance.md#t638稳定身份与最终整合场景) 定义。本单元重点验证整合/TaskCommit在implementing完成，committed candidate/begin_check进入checking，同次实际判断顺序记录check/full_review进入reviewing。完整after差额进入固定候选；integrated_pending_review不能Ready，只有真实reviewed_promoted/no_change可进入原eligibility。no-change不造空贡献/commit。旧pass不转换，三类在途/普通输出丢失恢复同key/B，无第二current。

实际命令、失败、Agent/fixture/installed/GitHub及未验证边界唯一由 [#638 Test](../../requirements-design-test-contributions/638-shared-current-promotion/test.md)维护。历史T600/T636/T637保留其实际对象和结果，不冒充当前组合通过。

## T635：活动接续、既成副作用与资源隔离

| 稳定身份 | 正常入口和输入 | 必须观察 |
| --- | --- | --- |
| T635-02 / R635-01/03 | 已提交但未入默认分支的 source ref/commit；无 A session/binding/checkpoint 的独立 common-dir B | 原 Identity/Establish/Ensure/Bind 继续同 Task/generation 和实际 Delivery；只补受影响判断/命中检查，不重开 Intake/Planning，不继承 pass。 |
| T635-03 / R635-03 | 精确既有 Draft/metadata 未完与 Ready 已成 PR，B local branch 不同；原私有交易缺失；公共 MERGED 对照 | 原 Publish 显式 source/PR 恢复并只补剩余动作；已完成 create/push/edit/Ready 零重复，当前 readiness 仍审；MERGED 原 recovery 零 merge，只交 Completion。 |
| T635-04 / R635-04 | 两 common-dir 同名 local branch、旧资源 pending、新代不同合法资源、推进后的 remote full ref、两独立 Task | ownership 不串认；旧 expected head/generation 保留新提交/新代；不同 Task runtime 缺失与 Cleanup pending 不改写或阻止另一方。 |
| T635-05 / R635-01/03/04 | 实际不可获取 ref/commit、未发布必要代码、归属不唯一、当前语义或 provider 条件变化 | 返回准确缺口与原 owner，保留无关环境；可恢复共享事实不以原机隐藏目录为前置，不把缺语义资格变成绿色。 |
| T635-07 / R635-05 | matching source、完整 packages/workflow、原工具维护、最多一个代表安装、reapply/drift/sidecar | source、installed/native、Agent、GitHub 和完整 Release 分层；旧安装按显式迁移；不批量迁移无关档或手改版本绕过前置。 |

实际执行与证据边界由 [#635 Test](../../requirements-design-test-contributions/635-portable-lifecycle/test.md) 单写。测试预期不等于通过；跨 clone 完整再次 Finish 和固定正式旧格式由终态测试单元定义。

## T649：阶段限制、当前候选与连续交付

| Test / requirement → design | 正常输入及原 owner | 必须观察 |
| --- | --- | --- |
| T649-01 / R649-01 → D649-01 | Author 的真实阶段限制及无变化控制 | 对象、原因、解除、阶段、后继责任可核；Policy 与 Docs Plan 各司其职，无空清单 |
| T649-02 / R649-02/03 → D649-02 | C01 旧当前说明、C02 绿测试保护旧限制、C03 局部 consumer 未完成、C04 合法无变化 | 从有效合同判断实际行为、说明、断言及未改消费者；前三者实际问题被指出，合法对照不制造阻塞 |
| T649-06 / R649-01/02/03 → D649-01/02 | 同一 Task D1 partial 合同限制→D2 实现，含 R648 冲突、合法修订及原 owner 重入 | 各真实 Planning／candidate／最终链／本地 commit/merge／Delivery；实际前序 stdout 连续消费，限制／说明／断言收敛，不拼接独立 fixture |

实际 source／installed、Agent、受控 provider 与正式 GitHub 交付分层。完整结果唯一见 [#649 Test](../../requirements-design-test-contributions/649-stage-result-convergence/test.md)。预置历史入口门禁不证明本轮连续判断，当前测试策略不预告通过。

## T663：正常合同承接与原 owner行为

| Test / requirement → design | 正常输入与入口 | 必须观察及边界 |
| --- | --- | --- |
| T663-01 / R663-01 → D663-01 | 正式Bootstrap repair_required→声明projection→同owner repair；new/existing/standalone及普通missing/profile/continuation mismatch | mode/context/identity保持，consumer无字段失配并实际继续维护；受控wrapper与真实owner分开 |
| T663-02 / R663-02 → D663-02 | 从Interface指定example填真实schema2 archive/key/HEAD/PR snapshot，经原recorder/checker/invoke | 合法只读出口，archive与snapshot不变，无当前Check/active gate或业务推进；原disposition stop保持 |
| T663-03 / R663-03 → D663-03 | fixed B无authority，原Planning/Bootstrap建立后整合/readback→TaskCommit→同次committedArchitecture/full Review；B已有文件对照 | 真实before缺失与完整B..H保持，当前新增文件实际审核；受控链不代替native owner |
| T663-04 / R663-04 → D663-04 | 正式final promotion baseline_incomplete/bootstrap→phase2维护→同原promotion，whole-task/Delivery及repair对照 | identity/root/continuation保持，维护不等integration/reviewed_promoted或独立Review通过；原后继实际可执行 |
| T663-05 / R663-05 → D663-05 | current registry全部profile examples及声明output variants，profile/aggregate/schema/projection/consumer | 实际组合可消费、唯一consumer及stop；不以marker/parity或固定数量代替；动态分支另审 |
| T663-06 / R663-01/05 → D663-01/05 | 一个代表性clean完整安装、真实Bootstrap repair消费、reapply/drift/mode/平台/sidecar | 真实owner修复结果与事实一致，分发实际覆盖分层报告；不证明完整Release矩阵或业务旧安装 |

本项实际结果由 [#663 Test](../../requirements-design-test-contributions/663-contract-continuity/test.md) 单写。以上定义预期；未执行项不能以先前扫描或schema通过冒充。实际最终质量链仍按T638覆盖晋升后真实内容。

## T679：跨会话接续与请求身份

| 稳定身份 → requirement/design | 正常输入与入口 | 必须观察及证据边界 |
| --- | --- | --- |
| T679-01 → R679-01/D679-01 | 正常 writer 隔离 Task/D1；真实主接收者与 fresh Architecture 接收者初始未绑定/未选 | 普通执行自行读安装合同，经原 owners 补缺并到原 Author/Architecture 正式出口；独立 final_plan 按 T694-01 只读对象入口评审。提示只给事实、目标、边界；人工预绑、环境借用或 mock 不证明原生行为。 |
| T679-02 → R679-01/02、D679-01/02 | 原正常 Bind/Selection 和公共 phase/scope/reopen 操作形成五种 current、不同选择、真实失配；原 API/读取 error 边界 | 首失败、原 owner 和后续重读正确；已有方案回未完义务，无 context 不写 session，保 Task/gen/key/root、规划、Git 与并行会话。unit/mock error 仅证明该层。 |
| T679-03 → R679-03/D679-03 | 原 Intake fixtures 执行公开 recipe；两 mode × 两 profile、合法不同 caller_locator、普通错 request_id/mode；一条真实 mode 的 native error replay | package 只证明 transport。原生 Agent 从未改 producer/source 完整重建 consumer、重审十维，经真实 record/check/invoke 到 ready；不能由 helper 代填映射/receipt。fixture 必须包含当前 runtime public-wrapper 检查的真实依赖。 |
| T679-04 → R679-04/D679-04 | 原 Approval artifacts 测试提取并执行文档命令：selected/missing、Task-only、正常 public closeout 后 archive | 真实 key 返回实际路径；缺文件准确；Task-only 无 slice/selection 副作用，archive 保实际 ref/key。无 key 错误对照不当成正向展示通过。 |
| T679-05 → 全部行为/职责 | 五 Planning 原 tests、#548 context/no-context、#443 隔离及 #396 proposed_draft | 命中边逐项保留，真实初始/已有进度与合法/失配分开；旧 Interface 测试不可因独立 legacy profile 存在而误拒当前 Planning 合同。 |
| T679-06 → 分发边界 | 一个代表 clean matching workflow/preset、完整 reapply、dogfood/声明平台、mode/sidecar、当前 Task 保持 | source/package、installed/native 与真实 Agent分别报告；历史archive不为安装手改。含旧数据的原 tools-only路径及其 preservation 单独记录。不证明完整Release/Upgrade、多平台Agent或业务安装采用。 |

实际首失败、机制、命令与观察截止由 [#679 Test](../../requirements-design-test-contributions/679-session-continuation/test.md) 唯一维护。缺原生或环境证据时保留未验证，不能以绿色fixture、文本parity或补绑定关闭对应验收。

## T694：显式评审对象与执行选择

| 稳定身份 → requirement/design | 正常入口 | 必须观察及边界 |
| --- | --- | --- |
| T694-01 → R694-01/02、D694-01 | 实际 installed upstream public API 形成有 context 无绑定、同 Task 无选择、匹配选择及无 context；原正式 Architecture wrapper | final_plan 通过完整对象校验并返回 typed stdout；Task、session、planning、baseline 和资源字节不变。语义 fixture 只证明集成层，不代替 AI 判断。 |
| T694-02 → R694-01、D694-01 | 正常不同选择、scope/phase/root/generation/C4 失配、普通读取错误 | 保实际首失败和原 owner，不覆盖或改报成功；其他目的/Planning consumers 原 guard 保持。unit API error 不证明原生恢复。 |
| T694-03 → R694-02、D694-02 | 实际 invoke stdout 与 Interface 当前 aggregate/分支/projection/current consumer、相邻 Approval 当前输入 | key/root/purpose/design freshness 保持；只允许原成功到 Approval，非成功保原路由；Approval 自身选择规则不变。 |
| T694-04 → R694-02、D694-02 | canonical/installed/声明平台、matching reapply/drift/mode/sidecar，提交前完整整合及提交后独立质量链 | 路由/无写与普通恢复 runtime 边界一致；原独立读序保持。source、fixture、installed、Agent 与未验证边界分开，不新增专项或完整矩阵。 |

本项实际观察由 [#694 Test](../../requirements-design-test-contributions/694-final-plan-object/test.md) 唯一维护。历史 T679 的原结果不证明新入口已验证。


## T713：公开执行合同与定向交付验收

| Test → requirement/design | 正常输入与原入口 | 必须观察及限制 |
| --- | --- | --- |
| T713-01 → R713-01/D713-01 | 原 creation 合法 Issue/no_issue 及已观察 relation 误填；当前多 profile/真实旧 consumer | 原正向执行及字段错误的定向证据，具体 field/contract/恢复，导航与 authoring 边界一致；仅 schema 拒绝不证明模型首次能力 |
| T713-02 → R713-02/D713-02 | 原 construct 完整 Candidate→公开 begin-check/rework；同 D1 恢复、实际 delivered 及真实编辑的已有证据 | Git/C4/current 前置、完整 B..H/dirty、固定 B 和合法 stale；git_free 保持上游原 consumer 边界；不追加完整 native 恢复链 |
| T713-03 → R713-03/D713-03 | 原命令 exit/stdout/stderr、record/check/invoke、普通错误或实际内部故障；C4 binding 引用→Closure、当前Review无scope或current_scope范围内返工→Author，旧Check回退按原provider恢复、真实范围变化→Clarify、已回退原结果恢复/纠正、legacy finalize 既有 REVIEW | receipt.result/checker/typed exit 分清；原 consumer 消费最小引用与具体动作，普通形状错误在对应 transition/重执行前诊断，旧合法成功域及恢复保持；不加无范围 fault injection |
| T713-04 / N1 → R713-04/D713-04 | C1 / AC5：新增 preTask→Finish 首次正确完整 native 链验收取消 | 保留原首装配失败与纠正后实际生命周期结果；取消/未验证不得记为全链 passed，不追加新 run 或必需补证支线 |
| T713-05 / N2 → R713-03/04、D713-03/04 | 已有普通字段、authoring/result 或 receipt 误用与公开纠正 | 按实际层级采用原结果，首失败与纠正分开；不计 N1 首次正确，不为本项重新准备独立案例 |
| T713-06 / N3 → R713-02/03/04、D713-02/03/04 | 缩减 AC6：已有真实编辑/stale、合法推进、结果丢失/恢复的定向或局部命令证据 | 原 key/B/适用证据保持；C2 取消新增独立 public-only native 恢复链及旧 fixture 接续，保留 N3 不充分与原 finding/证据不足 |
| T713-07 → R713-01/05、D713-01/04/05 | 缩减 AC7：固定 B 及当前差额的 43 active packages / 127 commands / 180 structured profiles；F1–F13 与 mode/profile/consumer | 完整导航、输入/输出与 consumer 核对；已有结构、命令、安装、synthetic、局部 native 各按其层采用。C3 取消 F10 及其余非等价 family/profile/caller/goal 追加 native 代表，未验证行为明确保留，不扩 #712 |
| T713-08 → R713-04/05、D713-04 | 缩减 AC8：R5 owner_schema/public_reads、native 提示、observe_candidate 的生产职责对照与原入口模块回归 | 生产知识/事实由原公开 owner 提供，eval 不保第二调用实现，合法 fixture/观测保持。C4 取消完整方法加载、Planning→同 fixture Activation/resume 与 Drift 新模型补证，保留方法不足、execution_error 与 fitness_regression |
| T713-09 → R713-05/D713-05 | 当前 canonical/dogfood/平台/代表 matching 安装、reapply/drift/sidecar/mode 与原 consumer 恢复的已有实绩 | 核仍匹配的实际结果，仅刷新真实变更依赖。C5 取消为追加 native 重复环境准备、损坏 clean 恢复与再次安装；source、installed、native/provider 分层，完整 Release 矩阵、部署及业务采用不由此推定 |

T713-03 的 #775历史恢复差额按固定旧provider复用原生产Check fixture：从正常 current_scope + reapprove_plan 语义输入调用实际 recorder/checker/invoke，将实际 planning_stale stdout 按正式薄投影交真实 Author 输入 schema，并断言具体修复动作保持。由原公开流程实际回退、清除 Planning 后，从目标外完整provider wrapper用既有--root调用声明恢复/纠正入口，观察同 key、candidate 与业务内容保持，无第二次 rework、Planning/Check pass 或旧结果字节改写。旧无绑定转换只覆盖新增入口或转换实际改变部分，并消费真实既有原因果来源；真实 scope/plan/内容变化与来源缺失保留原 owner 停点。

两项共享已有前置与证据，受影响无 scope、真实范围变化、成功 Check 以及 canonical/dogfood/consumer/drift 采用命中回归。该验证证明框架公开入口及消费者合同，不要求完整 Author 写作、业务历史重演、完整 Intake/native Agent 全链、多平台或 Release 矩阵。具体执行结果由当前 Task 原质量 owners 实际给出，此处不预填通过。

本节定义 #713 当前保留验收，不预填本轮通过。观察截止于已有原命令/run 的实际记录及本 Task 验证结果，后续正式结果由原 owner 输出承接。原首输入、命令/退出状态/双输出、读取、消费与出口保持在原记录；最终 typed exit 或 no-source-read 断言单独不证明模型行为。源码工程诊断和 #710 旧 native 不计本轮正常入口通过；新修正不改写旧失败。

N1 首装配失败、N3 public-only 不充分、F10/H2 非通过、R5 方法不足/resume execution_error/Drift fitness_regression，以及污染、未知退出码和部分成功均保留原边界。R3 仅 runtime 准备通过，未启动 native；旧 clean 后续损坏不证明 installer 缺陷，也不证明当前可用。取消或缺失的 native 不记为 passed，不再作为本项必须补跑的验收。已知正确性缺陷仍须修复，当前范围仍须完成原知识final_integration/readback、TaskCommit、完整committed candidate的一次独立Review、Delivery Review/readiness、发布/交付和 Completion/Closure/Finish，合并前保留 fresh merge gate。受控 GitHub 替身只证明本地层次，不证明真实 GitHub 发布、部署或业务生产效果。


## T779：委托方法与受管投影

| 稳定身份 → requirement/design | 输入与原入口 | 必须观察与证明边界 |
| --- | --- | --- |
| T779-01 → R779-01/D779-01 | 当前 Phase 2 完整方法、加载引用及原 discovery/Check/Review consumers，经提交后一次原九维与独立完整Review | 六项来源行为的条件、例外及交接顺序完整；自主工作不越委托，介入先核本次运行及具体缺口；最小对话结果、事实层次、原句柄接管、实际冲突目标交接及结果采用保持；没有逐轮审批或持久运行状态。语义审核证明合同质量，不证明现场成本效果。 |
| T779-02 → R779-01/D779-01 | 原安装/tools owner 同步实际受影响的 canonical/dogfood/声明平台；实际 drift、mode、sidecar 和适用 native/preservation 验证 | 实际受管内容采用且无未解决漂移/sidecar，当前 Task/session/peer 保留；source、installed 与 Agent 行为分别报告。无需为本项新增设备、评测框架、整场事故重放、消息计数或完整多平台/Release 矩阵。 |

实际观察截止与命中验证由 [#779 Test](../../requirements-design-test-contributions/779-delegation-results-intervention/test.md) 维护。本文定义预期，不预填本项通过或节省比例；原final_integration/readback、TaskCommit、完整committed after绑定和一次独立Review保持。未运行的外部业务采用与实际效果保持未验证。


## T792：出口查询与按步骤加载

| 场景→要求/职责 | 入口与条件 | 独立观察及边界 |
| --- | --- | --- |
| T792-01→R792-01/02/05、D792-01/02 | 原public wrapper，真实Skill/workflow条件target/stop/instruction-only出口及无exit查询 | 唯一consumer与原Interface/正文一致，输入投影能由真实consumer消费；无exit保持原语义，不返回私有/全图，不把查询当下游pass。 |
| T792-02→R792-01/02/05、D792-01/02 | 普通unknown、多exit、更新漏映射/重复标记、缺引用/漂移，单一权威及Interface合法演进 | 错误非零明确停止；合法演进自然更新。fixture只模拟普通遗漏，不造攻击或人为篡改防御范围。 |
| T792-03→R792-03、D792-03 | 原native get_context phase/step/continuation | 当前步骤必要全局约束/原owner/producer恢复可得，正常index不要求无关全表或历史；不以行数或关键词数量证明充分性。 |
| T792-04→R792-04、D792-03 | 正常legacy识别转交及原维护owner完整references | 原支持家族、转换、控制退役及历史恢复准确来源可达；静态可达不证明实际历史转换。 |
| T792-05→R792-05、D792-01/04 | source/installed snapshot、matching .new preview、原tools更新及installed/drift/sidecar定向回归 | 明确资产根，同一图，不用旧installed引用替新candidate，当前Task/session和peer保持；不是完整矩阵。 |
| T792-06→R792-02/03/04/05、D792-02/03/04 | 更新matching安装后AI实际使用原context/出口query并加载consumer；普通接续和维护读取各一条 | 当前必要内容可得并由原owner接续或stop；维护只读不执行未经选择的转换。source/installed/Agent分别记录，不声称所有平台、性能或成本收益。 |

T792-01/02/03是长期回归，T792-04/06是本项语义/实际行为观察。已有适用工程事实可采用，具体缺口才追加实验；必要验收不足保持未验证。实际命令、首次失败、修正、终态及范围唯一见[#792 Test](../../requirements-design-test-contributions/792-step-context/test.md)；本单元不预填候选/最终Check、committed Review、发布或Completion结果。

## T794：提交后一次独立完整审核

| 场景 → requirement/design | 真实入口与正常输入 | 必须观察及证据边界 |
| --- | --- | --- |
| T794-01 / V1 → R794-01/02/03、D794-01/02 | 原公开提交→constructor/begin_check→独立Review→readiness链；无先验Check | 文档实际整合/精确本地提交进入固定B/H；同次九维/Architecture/fullrange真实判断，顺序两槽结果；通过前无push/PR。真实Git/API组件不证明Agent已独立读序。 |
| T794-02 / V2 → R794-05、D794-04 | 未通过/已通过/HEAD正常变化候选，原Publication边界及可观察executor替身 | 未通过无新远端动作；当前通过仍readiness和精确payload；替身只证明本地资格/调用，不证明GitHub。 |
| T794-03 / V3 → R794-04、D794-03 | 真实finding修复后继、原reviewer仍独立、base组合/冲突、覆盖不可得或影响不明 | 保B/完整范围，采用可核验原覆盖/工程事实，补真实差额/受影响未改consumer，必要时完整补审，不只看新增行。 |
| T794-04 / V4 → R794-03/06、D794-02/04 | 旧check/已提交/已审、旧Draft已执行/pending，单次双槽记录中断/输出丢失 | matching原provider、同key/B/H/候选和真实结果，只补缺步或准确恢复；必要语义丢失真实补审，无旧pass转换、重复副作用或未审pending发布。 |
| T794-05 / V5 → R794-01/03、D794-01/02 | 原Architecture/RDT正常targets、expected-current、partial/output-loss、真实committed before/after | 整合只pending，实际readback/原单写与同intent恢复保留；committed独立判断后才reviewed_promoted；pending不能下游readiness。 |
| T794-06 / V6 → R794-02/04、D794-01/03 | matching公开入口的实际新独立reviewer、修复后继及补足路径 | reviewer真实authority-first，冻结候选不改；同次Architecture/九维/fullReview及实际差额判断；首次失败/缺口保持，不用fixture或预写pass替代。 |
| T794-07 / V7 → R794-06/07、D794-04/05 | 真实profile/schema/producer→consumer、原tools matching采用和受影响平台/reapply/drift/mode/sidecar | 当前图无重复Check/审核前发布边；原恢复/终态保留；source/installed/Agent/外部分层，保用户和Task/session，不扩完整Release矩阵。 |

本轮实际命令、首次失败、修订、正式结果和未验证范围唯一在 [#794 Test](../../requirements-design-test-contributions/794-postcommit-review/test.md)。本单元仅定义行为与验证策略，不预填本候选pass/最终H/Delivery/Completion/安装或生产效果。


## T815：真实 manifest 冲突与原 tools 接续

| 场景 → requirement/design | 正常输入与入口 | 必须观察及边界 |
| --- | --- | --- |
| T815-01 → R815-01/02、D815-01/02 | 两个真实 canonical 分支，各自原 installer 输出，再实际 Git merge | manifest 冲突自然形成；固定完整旧 blob 原字节/provenance/hash 保持，未手造状态或修补输出。 |
| T815-02 → R815-01/02/05、D815-01/02 | 执行 Agent 实际完整读修订合同，经原 tools preview/prepare/invoke 接续 | AI 逐路径判断后原 installer 生成两侧组合；目标自身 resolver/installed/native/drift、sidecar/mode 与最终候选均正确。driver 或正文相等不能证明 AI 行为。 |
| T815-03 → R815-03、D815-03 | 原 resolved executor、同请求 stdout-loss recovery | 正确父序/最终 tree、零 unmerged、同 key/PR、自然 dirty 当前 task.json 与无关 Task/session/peer 保持；只观察本地 Git/provider fixture 层。 |
| T815-04 → R815-04、D815-04 | 原 Publication 完成事务到后继 action、未完成/未知动作的同操作恢复 | 原 retire_completed 退役完成私有事务及 gate，公共 facts 不丢；未知动作不重复。受控 provider 不证明 live GitHub。 |
| T815-05 → R815-05、D815-02/03 | 受影响 source/packages、原 tools 同步本 checkout、matching installed/平台/reapply/drift | 保 Task/session/peer，零未处理 sidecar，原 modes 保持；local_candidate 的 formal_fork_source_lock 边界保留，正式采用、完整矩阵、外部交付分别说明。 |

本项实际命令、首失败、结果和观察截止唯一在 [#815 Test](../../requirements-design-test-contributions/815-manifest-conflict-recovery/test.md) 维护；前文历史观察保持。本策略不预填安装、Check、committed Review、正式采用或 Task 完成。
