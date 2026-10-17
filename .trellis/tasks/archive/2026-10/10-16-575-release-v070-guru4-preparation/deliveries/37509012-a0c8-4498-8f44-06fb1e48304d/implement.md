# #575 S4 执行计划

PRD独占需求，design D2独占source-design disposition matrix，实际结果只归既有唯一Test。

## P1. 唯一 Delivery Policy

策略staged。S1正式来源、S2准备与S3 ownership来源修复保持原历史。当前S4入口为真实已交付修复源；独立切片交付A完整`.4`工具投影和目标运行、B/四平台证据、正常focused输出捕获修复与直接回归。当前出口为R575-S4-01..04全部满足、draft RDT本切片reconcile及完整Check/commit/独立Review/Refs-only交付。

剩余阶段由WholeCompletion审查并经原Creation建立：从含helper修复的真实clean committed source执行完整focused clean/local-workflow、完成真实stable predecessor分离维护/native/下一consumer/恢复/兼容回退的最终证据判定，以及完整RDT收敛、完整准备candidate首次Review后原owner晋升与fresh门禁。当前不预造后继key，不以当前切片完成缩减根A575-01..08，也不把准备验证欠缺归为软件发布。

当前修复使后继可直接使用正常verifier，独立价值不依赖完整focused已经通过。source先提交的依赖不得用于虚构完整Check或以fixture commit冒充正式源；整体Completion仍由原owner判断。Stage2最终main/provider/tag/smoke/Release及关闭#575保持软件发布责任。

## P2. 唯一 Docs SSOT Plan

采用delta_first，writer=`guru-maintain-requirements-design-test-ssot`，唯一贡献根=`docs/requirements-design-test-contributions/575-release-preparation/`。requirements/design/Test/traceability/manifest五文件承接当前切片与历史边界；Test单写实际来源、失败、诊断、回归及剩余未验收层次。最终Check前由原owner reconcile本切片delta。

本切片不晋升shared RDT；完整准备范围的最后切片由原owner在首次完整committedReview后以现场expected-current晋升，再fresh Check/commit/完整Review。当前适用RDT为`.101/active`；Architecture为`.94/active`，是否需贡献/晋升由其原owner判断。不得把当前文档草稿或历史Review当最终晋升凭据。

## P3. 稳定顺序

1. 原Clarify与Author保持根scope，implementation原owner将同Delivery合法rework至planning。Author修订切片requirements/candidate→fresh独立candidate Architecture→Author solution/context→全量Wording→fresh独立final_plan Architecture→Approval；展示当前三文档并接受后由原Activation写新Planning。新Planning未激活不改helper或tests。
2. 原tools owner负责A原source_locked操作及其结果；本次helper不投影，不改变该已冻结operation source/ref/preimages。A目标自身resolver/installed/native/下一owner与保留对象独立复核。B平台与四projection/release Skill parity按D4判真实依赖，不自动复装或重复无关矩阵。
3. 实现worker只改D5的source helper、必要直接capture消费者与定向测试；每批写前检查精确checkout边界。保留CLI输出、exit/timeout和首失败，不以参数/样本/过滤改名求绿。执行V3直接回归和真实CLI初始化，不宣称完整focused通过。
4. 原RDT owner按P2收敛并reconcile；fresh独立Phase2 Architecture/完整当前切片Check→原TaskCommit展示精确写集并独立确认→首次完整committed独立Review。开放P0–P3为零才进入publication Architecture/DeliveryReview。
5. Publish、Merge各自精确确认后交原WholeCompletion；剩余准备责任走原additional_delivery_required→Creation→Planning，不能直接Finish。后继完整clean/真实predecessor和最终晋升按D6继续。Closure/Finish/bookkeeping/cleanup与软件发布仍为独立边界。

## P4. 最小可靠验证与层次

| 验证 | 对象/入口 | 可观察条件 |
| --- | --- | --- |
| V1 | A原tools install/source_locked及目标resolver/installed/native/current/下一owner | tools_upgraded及实际`.4`受管graph，原Task/session/历史/配置与peer/common保留；真实来源不改称新HEAD安装。 |
| V2 | 四平台source validators/ownership/私有release Skill；B三平台apply→reapply→drift | 每root bytes/权限/退休项匹配，审查全部sidecars，reapply未审查差额为0；递归bytecode/.new/.bak无未声明residue。 |
| V3 | source helper定向真实子进程与相同正式Fork初始化 | 双流strict UTF8，stdout capture不混入stderr，日志与非零错误保存两流与真实exit；timeout分类及残留输出保留。真实CLI相同init越过原解码阶段；完整focused仍保留后继义务。 |
| V4 | 唯一RDT及完整changed/new范围验证 | 本切片双向trace、secret scanner完整覆盖无未审查告警、脚本/JSON/Python定向检查、源/安装图与卫生；当前差额diffcheck无错误。继承EOF历史诊断保留Review判断，不改历史。 |

按#578工程事实合同先判断完整检查集与scope/bytes/工具链/参数/预期/原始输出依赖，再采用可核实且未受影响的执行事实并注明来源/原因。缺失、新变化或不确定检查实际补跑；旧semantic pass/其它owner private checkpoint/测试数量不替代当轮判断。ordinary切片不扩张累计多平台/native-host矩阵。

## P5. 停止与保留

新scope/authority/API/owner/机制要求返回原qualification/Clarify/Architecture；新故障先保留第一失败并核因，不放宽guard、timeout或换样本掩盖。缺依赖/环境/结果保持FAIL/SKIP或明确gap，不算通过。source改变不扩旧恢复写集。

保留当前Task/generation、历史Delivery/规划/raw source、未选择archives、用户定制与caller/main/peer。无授权信息、动态发布账本、task-local PR/Release body、隐式同步或资源清理。最终Stage2证明由最终main exact candidate重做。
