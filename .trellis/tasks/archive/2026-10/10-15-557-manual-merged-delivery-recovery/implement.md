# #557 执行与验证规划

状态：Phase 1 candidate；只完成需求和方案写作，不是执行批准。

## Delivery Policy

policy=full：一个有实际产品内容的业务Delivery交付R557-01..09/D557-01..05全部accepted scope；没有隐藏remaining slice。whole-task Completion判断整体scope及真实证据，只有其completed可进Closure/Finish。来源backend与完整多平台/Release矩阵不属于本Task，不能因生命周期恢复宣称成功。

## Docs SSOT Plan

strategy=delta_first。原guru-maintain-requirements-design-test-ssot拥有唯一contribution：
docs/requirements-design-test-contributions/557-manual-merged-delivery-recovery/{manifest.yaml,requirements.md,design.md,test.md,traceability.md}。
需求/设计增量指向PRD/方案源和canonical step-local合同；test.md单写实际结果、first failure、provider fixture/source/installed/live层及未验证边界，task不复制执行结果链。
final Phase2前必须task_delta_reconciliation。首次不同reviewer独立完整committed Branch Review后，由原RDT/Architecture owners基于live expected authority决定必要promotion；promotion新diff重走Phase2/TaskCommit/独立完整Review后才能Publication。
Architecture contribution与ADR exact locators见design；本轮shared current不在Planning写作。

## 实施顺序

1. Author requirements → independent candidate Architecture → Author solution/context → Wording → fresh independent final_plan Architecture → Approval。展示当前三份规划及具体机制/compatibility后，等待本次计划接受，再由原Activation进入实施。创建确认只授权创建，不授权实现、Git提交或外部发布。
2. 以一个完整matching Task2/API1/Plan2样本建立现有formal Creation/Author/Activation/Check/TaskCommit/full Review/Readiness/Publish链。固定受控CLI/Core候选须先核对本地实际bytes/modes与合同tar identities；同版本号不等于matching。源旧完整dogfood不被拆换。
3. 添加正常无trailers/gate、四CI状态、真实Git two-parent事实的聚焦回归，首先观察当前失败。实现原Merge的delivery_merged_recovery profile、独立schema/semantic contract与唯一public事实投影。仅actual MERGED进入record；OPEN不merge。与原expected-head mutation职责共享客观事实primitive，不复制语义gate。
4. 实现actual candidate commit snapshot与公开hash调用、Publication→actual差额/authority/CI事实承接；原Completion合同显式审查该差额及scope-required证据。补输出丢失、base推进/branch删除、公共record重入和缺关联/mismatch边界。
5. 新query2读取公共已记录历史，与合法trailer历史去重/核验；现有query1的具名历史职责保持。更新MIGRATION-557、canonical workflow/step-local Skill/interface/commands/schema/examples及匹配consumer和README。临时snapshot消费即删，不产生新ledger或授权状态。
6. 完整matching installed样本apply/reapply，检验正式public调用与声明平台projection/bytes/modes/drift/sidecars。源旧dogfood普通apply/drift的实际迁移前置如实记录，不单拷新writer。产品源代码以canonical为唯一长期源头。
7. 本Task接受范围要求真实GitHub/Git公开链时，在source repo castbox/guru-trellis内准备一组独立validation base/head与一份含实际fixture内容的正式PR：先正式创建/规划/Check/Review/Publish，再普通无Guru trailers/gate手动merge，原Merge恢复并接续原Completion。该外部验证资源与动作在执行前由原owner展示精确ref/PR/payload并取得独立确认；不触main业务内容或backend，不把provider fixture当live。若所需外部证据缺失，保留unverified/evidence_pending，不能close #557。
8. 原RDT reconciliation、fresh independent Architecture Phase2 + 完整Check → exact Task Commit → fresh independent Branch Architecture/完整origin/main...HEAD Review。必要promotion后重走原gates。
9. 原Delivery Review/中文Refs-only readiness → Publish → 正式Delivery merge → whole-task Completion → Closure → Finish bookkeeping → 精确资源Cleanup。每次Git/GitHub副作用分别展示live目标并使用其当前对话授权；不把规划接受当push、merge、close或cleanup授权。

## 聚焦验证

| Test ref | 正向与普通边界 / 观察 |
| --- | --- |
| T557-01 formal current chain | 同一正式Delivery经完整public owners发布，普通真实two-parent手动merge无trailers/gate，原Merge delivered→原Completion；仅validator单测不能替代。区分provider fixture与实际GitHub。 |
| T557-02 CI truth | 分别全绿、pending、cancelled、missing、failed；都记录可靠MERGED。必要验证失败/未完成返回真实未完成出口；scope不要求某CI时由Completion解释不自动加验收。没有统一completed fixture。 |
| T557-03 identity | 已有唯一public Publication关联；缺Publication、选择歧义、repo/base普通mismatch不记录假归属。不从名字/标题猜；无emptyDelivery/PR/commit。 |
| T557-04 content/scope | 同head/same-content仍适用结果不机械重跑；actualhead内容变更、额外PR路径与authority变化须差额判断与原owner回程，不追认旧pass。actualDeliveryFact与originalPublication保留各自candidate身份。 |
| T557-05 recovery/history | base推进、deleted head branch、不同当前HEAD、newchat显式key、record成功后的stdout/projection丢失；重入same事实，零merge调用/零重复写。history读回无trailersfact，排除bookkeeping；只读保持Task bytes。 |
| T557-06 compatibility | 原expected-head/Guru message/trailers与schema1/2历史、旧formal输出恢复定向回归；query1原行为/query2公记录、same-output consumer绑定。matching采用边界明确，无旧checkpoint作新pass。 |
| T557-07 distribution | canonical source package/runtime/schema/registry、声明平台descriptor/projection；一个matching clean installed正式链/reapply/bytes/modes/sidecars/drift。source旧carrier失败真实保留；不跑完整平台/Release矩阵。 |
| T557-08 static/docs | shell语法、触及Python编译、JSON/schema、官方context validate、git diff --check及触及非generated代码3000行检查；R/D/T双向trace、来源承诺matrix、Architecture九concern完整。不是业务/上线证据。 |

共享kernel不加入业务profile判断；局部重复只在存在真实相同consumer时提取确定性primitive。测试必须执行实际产品logic/public owner并检测真实行为，不用硬编码文本/fixture自证。source/installed各使用自己的完整matching runtime，依赖缺失保留SKIP/blocked，不拼接私有DTO或直接改store。

## 执行边界

本次预计修改canonical Merge/history及必要schema/consumer/Completion合同、workflow/spec/README和聚焦测试/harness，plus独立docs contribution。step-local拥有语义；脚本只执行事实/结构，不自动选择归属、readiness、finding、Completion或Issue disposition。
精确禁区和来源承诺处置只由PRD/design单写。普通scratch/testfixture是验证资源，不是业务Task authority。source/main安装、业务升级、软件Release、完整多平台矩阵、原backend现场恢复均不由本轮Planning或本地tests推定。
