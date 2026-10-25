# Task / Delivery 生命周期测试策略

本次 #649 最终整合的完整前驱：Git `4fea68613de4181d7cb55532b8758515472ba31b:docs/test/current/task-delivery-lifecycle.md`。贡献、#657 继承及原来源见 [#649 追踪](../../requirements-design-test-contributions/649-stage-result-convergence/traceability.md)。

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
| T531-04 / T530-01..05 | dirty精确提交；clean既有候选freshCheck后首次Review；普通stdout loss | 真实内容进入commit，clean零空/重复commit；Review输入绑定实际H；完整独立Architecture/Branch Review；旧gate不冒充current。 |
| T600-01/02/03/04/05/06 | authority变更的完整tracked/untracked候选与proposed targets；无变化控制 | 独立before/after与候选Check→合法回implementation→原owners最终整合→重新candidate/begin_check→最终Check→commit→committed Review；no-change无空文件/ADR/commit；mismatch/partial/conflict走原owner。 |
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

## #636 早期反馈的新增完整场景

| Test identity | 正常起点与实际入口 | 必须观察与证据边界 |
| --- | --- | --- |
| T636-01 / R636-01/03 | 已激活候选尚无完整 Check/重型结果，经公共 TaskCommit 早期 prepare/invoke，再经原 Publication | 真实非空提交和 Draft 先于完整审核/重型检查；精确 paths/消息/敏感检查/目标正确；正文列待完成，缺最终 gates不能 Ready/Merge。fixture不代替真实GitHub Draft。 |
| T636-02 / R636-03/04 | 同 Draft 发布修订或真实冲突解决候选；同一 Ready PR需先发布未审候选 | 同 PR/key保留；退 Draft 在push之前，最终审核未完成时保持 Draft；完整新证据后再 Ready；旧readiness不能放行新HEAD。 |
| T636-03 / R636-04/06 | 正常 commit、create、push、edit、Draft/Ready已成功但正式输出丢失，从原 producer同调用恢复 | 实际 commit/PR/HEAD/payload/state读回，同操作只补剩余步骤，无第二commit/PR或重复已成功动作；失败/SKIP不变为green。不手改hash/伪造artifact构造安全负例。 |
| T636-04 / R636-02/05 | Draft后固定B/H，独立Agent内容分析与HEAD命中命令并行；期间target前进、冲突/无merge ref/CI未触发 | 审核固定B/H完整内容，HEAD验证仍推进，T/M组合结果分开保留原因/恢复条件。早期结果不写full_review；正式独立Review仍真实Check predecessor。fixture只证明调用/候选逻辑，不证明业务CI。 |
| T636-05 / R636-04/06 | 当前候选准备最终readiness/Ready/Merge；full/partial、默认/非默认目标对照 | 全部 Delivery Refs-only，Closure独占整体关闭；Draft/Ready/一次merge不证明Task完成；实际候选拥有全部适用gates。 |
| T636-06 / R636-07 | matching packages/workflow/runtime、声明平台投影及本仓dogfood的apply/reapply | public input/exit/唯一consumer匹配；installed实际行为、drift、可执行mode和sidecar逐项正确；source parity不代替现有业务采用。非完整Release矩阵。 |
| T636-07 / R636-06/07 | implementing/checking/reviewing/publishing在途任务、旧commit receipt与旧Publication pending/Ready事务 | 由原owner一次性恢复/迁移同key/PR、已执行动作和真实gate义务；无伪造pass、runtime双读或新建Task/Delivery。 |

本轮实际命令、首次失败、恢复及未验证边界唯一记录在 [#636 Test](../../requirements-design-test-contributions/636-early-draft-pr/test.md)。本文只拥有完整策略/场景，不复制执行日志。

## 候选适用性与覆盖完整场景

| Test identity | 正常起点与实际入口 | 必须观察与证据边界 |
| --- | --- | --- |
| T637-01 / R637-01/04 | 原公共 Task/Delivery 和七 owner 首次完整链 | 首次真实独立覆盖、当前 Check/full_review/candidate/predecessor；Planning、自检和 Draft 反馈不替代。 |
| T637-02 / R637-01/02/05 | matching installed 实际 Agent；首次完整后真实文档冲突、定位修订及未改 consumer | 原覆盖加双方/组合/完整差额与受影响依赖形成当前完整结果；finding 修正后核闭合及覆盖，无无因换新全量。 |
| T637-03 / R637-03 | 正常共享 Runtime/事务实现缺陷，原命令缺失或环境改变 | 扩审未改 consumers 并检出具体缺陷；缺项补跑，其余可核验事实按当前适用性采用。 |
| T637-04 / R637-02/07 | 实际同树新提交、无关 target 前进、公开输出恢复与已退休 checkpoint | 固定 B/同 Delivery；只刷新必要绑定、不假定环境；旧 gate 不冒充当前，缺覆盖补审，无私有跨读或重建。 |
| T637-05 / R637-04/05/08 | 旧/新完整安装的同初始实际 Agent 样本 | 先比较充分性/检错，再分别实测语义、命令、正式记录、远端等待和重复动作；fixture/scanner 不证明 Agent 行为，不预设收益比例。 |
| T637-06 / R637-06/07 | #636 已交付 installed 早期入口与真实同 PR/HEAD 修订、最终门禁 | 同 key/PR 接续，早期不写 full_review，真实 Check predecessor 与 payload/live 资格；#638当前组合按T638实际证明，不从历史通过推断。 |
| T637-07 / R637-08 | canonical/声明平台、单 clean matching、reapply/drift/mode/sidecar 与在途恢复 | 完整 matching 投影和实际 installed owner 运行，旧完整安装固定或原 owner 显式成套迁移；不推定全平台实际 Agent、业务/生产或完整 Release 矩阵。 |

本轮实际命令、首次失败、Agent/fixture/installed/remote 层次、分阶段耗时及未验证边界唯一由 [#637 Test](../../requirements-design-test-contributions/637-candidate-review-reuse/test.md)维护。本文定义完整策略，不将规划、旧结果或知识晋升当作通过证据。

## T638：候选到真实最终内容

T638-01..07的完整场景由 [knowledge test](knowledge-maintenance.md#t638稳定身份与最终整合场景) 定义。本单元重点验证实际公共phase为implementing→checking→implementing→checking→reviewing；候选不写finalgate，真实写入后旧candidate不能放行，原implementation重新绑定全部after差额。未晋升不能Ready，no-change不造空贡献/commit，实际Git无整合阻塞可直接晋升。旧pass不转换，三类在途/普通输出丢失恢复同key/B，无第二current。

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
