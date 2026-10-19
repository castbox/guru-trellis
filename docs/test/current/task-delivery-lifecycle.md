# Task / Delivery 生命周期测试策略

知识单元：`RDT-TST-LIFECYCLE`。状态：`current`。适用版本：`current-main-0.7.0-guru.113`；晋升前完整定义为 immutable Git `b470580d4f79f61c66d72db97861fe1564b5e746:docs/test/current/task-delivery-lifecycle.md`（RDT `.112`），更早迁移来源和稳定身份保留。需求：[RDT-REQ-LIFECYCLE](../../requirements/current/task-delivery-lifecycle.md)；设计：[RDT-DES-LIFECYCLE](../../design/current/task-delivery-lifecycle.md)。本单元拥有场景/预期和结果定位；历史结果不等于当前候选通过。

## 策略与完整性

以真实公共owner链验证合法正常路径、普通缺失/过期/输出丢失及完整候选。AI审查职责、因果关系和门禁充分性；schema、测试或脚本只证明其客观层次。不制造恶意artifact/伪造hash/对抗绕过、未要求的锁/压力/崩溃负例。实际Agent、runtime/package、source/dogfood/installed、provider/live、Release证据分别说明。

`TST-002/003/004/007`、`CASE-001/002`、`SCN-001..004` 的 orchestration/AI-script/compatibility身份保留；其旧Task级开发入口和Finalizer顺序已由R531/ADR-030替代，不把旧断言作为当前预期。当前完整场景如下。

| 稳定scenario/test identity | 正常起点/动作 | 必须观察 |
| --- | --- | --- |
| T531-02 / R531-01/02 | 同Task建立D1、独立D2，分别写规划 | key/root/文档和历史分开；Task scope持续；唯一Author、独立Wording/Architecture/Approval，Activation是真公共Planning writer。 |
| T154-02/03/04 | 全量、partial、后继和返工；详细来源及规范性承诺 | 真实完整来源被读取；Task与slice正文分明；设计处置唯一且保条件；Policy/Docs Plan不重复；下游实际消费正文。 |
| T531-03 / R531-03 | 同slice scope/方案变化、部分/全部撤回，各真实stage | 原Clarify及最早stage合法rework，身份/PR/history保留；stop/release不冒充delivered；独立工作不因局部provider缺口阻断。 |
| T531-04 / T530-01..05 | dirty精确提交；clean既有候选freshCheck后首次Review；普通stdout loss | 真实内容进入commit，clean零空/重复commit；Review输入绑定实际H；完整独立Architecture/Branch Review；旧gate不冒充current。 |
| T600-01/02/03/04/05/06 | authority变更的完整tracked/untracked候选与proposed targets；无变化控制 | 独立before/after→原owners晋升→写入适用性→最终Check→commit→committed Review；无变更无ADR/空阶段；mismatch/partial/conflict走原owner。 |
| T535-01..04 | 完整Review无候选，或非空全rejected | 真空集[]与分类区分；完整维度/Docs/Architecture/freshness及route仍审，不凭空集自动passed/ready。 |
| T531-05 / T557-01..04 | 原Publish/Merge成功后投影/输出丢失；正式发布后人工双亲merge | 实际成功读回且零重复副作用；历史事实不等新gate；actual head/CI/delta交Completion；不执行第二merge。 |
| BEH567-01..05 / 该源T567链 | 各阶段固定B/H；无关target前进；实际冲突/依赖同步 | 固定候选正常前进、默认零Reconcile；仅真实触发固定一次target，恢复同Delivery，不追赶、不重放无关门禁。 |
| T531-07 / R531-07 | 完整匹配安装及显式旧数据迁移 | canonical/installed/native/reapply一致，旧公共/私有迁移分owner；source修改不证明旧业务/production已采用。 |

## 执行入口与结果消费

完整精确测试命令由受改package的现行tests和其owner选取；公共profiles/DTO以[canonical packages](../../../trellis/skills/guru-team/packages/)为准，不在此固定易漂移计数。历史结果在各原contribution的唯一test中：[#531](../../requirements-design-test-contributions/531-task-delivery-lifecycle/test.md)、[#154](../../requirements-design-test-contributions/154-planning-body-contract/test.md)、[#530](../../requirements-design-test-contributions/530-clean-committed-reentry/test.md)、[#600](../../requirements-design-test-contributions/600-promotion-before-check/test.md)、[#557](../../requirements-design-test-contributions/557-manual-merged-delivery-recovery/test.md)。它们保留原candidate、首次失败和未验证边界，不能由本轮链接宣称重跑。

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
