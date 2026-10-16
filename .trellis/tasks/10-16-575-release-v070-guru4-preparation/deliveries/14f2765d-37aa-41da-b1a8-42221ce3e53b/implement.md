# #575 S5 同源 exact-provider 执行计划

需求读PRD；全部规范来源处置仅由design D2拥有。

## P1. 唯一Delivery Policy

策略staged；S1来源、S2准备、S3来源修复、S4工具/捕获修复均保持实际历史。本切片是既有整体准备范围的最后计划业务阶段：入口为S4已交付且存在包含helper修复的真实clean committed来源；当前范围为完整Codex focused、本次根定向证据终审、唯一最终RDT收敛与必要晋升及前后fresh完整门禁。

出口是A575-S5-01..04全部满足、当前独立交付条件和post-promotion完整Review满足后以Refs-only发布/合并。正常情况下不预留另一个业务切片；新发现的必要工作由原qualification与WholeCompletion判断，不能强行complete或预造下一UUID。Task的Closure/Finish/archive/bookkeeping仍是交付后的原生命周期责任。

Stage2 final-main/provider/predecessor-release-diff/tag/smoke/Release/关闭#575不属于准备Task业务剩余；完整累计多平台/native-host、真实业务/原始在途/生产不声称验证。当前准备完成只由WholeCompletion按全部根要求判断。原local-sample机制的真实失败不会因direct provider执行成功而变成已修复声明。

## P2. 唯一Docs SSOT Plan

采用delta_first，writer=`guru-maintain-requirements-design-test-ssot`，唯一根=`docs/requirements-design-test-contributions/575-release-preparation/`。requirements.md、design.md、test.md、traceability.md、manifest.yaml承接完整准备及当前增量，Test单写执行结果。沿当前RDT .101/active与Architecture .94/active读取实际authority，写前复核适用性及shared expected-current；不预造版本身份。

在本切片最终Phase2前原owner完成draft reconcile。第一次完整committedReview后原owner串行执行最终shared RDT promotion，Architecture按真实影响处理；promotion差额fresh Check/TaskCommit/完整Review。S1独立source-adoption贡献及历史原结果保持，不新建第二份Test、release notes、PR/Release body handoff或动态checklist。

## P3. 稳定执行顺序

1. 当前Author requirements与候选资格后，独立candidate Architecture；Author写完整solution/context，原Wording全三文档审查，fresh独立final_plan Architecture，原Approval。当前从已实施首失败修订验证机制，同key合法rework后重走受影响门禁；phase-1-delivery-activation展示实际计划并在当前对话接受后，原Activation写public Planning；此前不执行focused或Docs promotion。
2. 从真实已提交07884 source取得干净隔离checkout，不用自建fixture commit；按design D3将workflow-source固定同一远端完整07884 SHA、关闭local-sample，单次PATH选择原CPython3.12.8 seed，其它原shell/profile/正式Fork/stages/预算保持。执行前复核该SHA仍可寻址及本地HEAD同源；在全新work directory执行完整focused，保留每阶段、原两轮失败与新结果。不得缩小profile、改预算或只取最后一次成功。
3. 原工程执行owners对design D4所列完整定向集进行依赖审查；不变事实采用且注明来源/理由，受影响或缺失检查补验。真实predecessor分离维护/native/next owner/resume/rollback的scope-required缺口不能用外部DTO替代。
4. 原RDT owner完成P2唯一完整贡献与draft reconcile；fresh Phase2 Architecture/完整Check→原TaskCommit精确预览/确认/提交→不同独立reviewer完整committed B..HEAD Review。开放finding经原route处理；不是来源修复S4 Review的复用。
5. 首次完整Review通过后，原RDT/Architecture owners按真实impact与expected-current串行晋升；共享diff回到fresh Phase2→TaskCommit独立确认→不同reviewer完整Review。无impact的Architecture不制造贡献；shared RDT不能跳过。
6. publication Architecture→Delivery Review十维→Publish预览/独立确认→Merge预览/独立确认→WholeCompletion。之后只有其completed进入reference_only Closure/no_mutation及Finish独立归档/bookkeeping边界；Stage2与清理继续各自独立。

## P4. 最小可靠验证

| 验证 | 实际入口/对象 | 可观察条件 |
| --- | --- | --- |
| V1 | design D3原focused shell，真实clean修复source+正式Fork，Codex一cell | init/preset、两轮update/reapply、source lock/template/Docs/sidecar、native load、session binding及最终status/exit满足；明确仅为准备07884同源exactprovider，非最终main candidate gate；原local路径仍FAIL。 |
| V2 | design D4根A575-01..05、A/B平台与stable `.3`真实维护 | 每项当前依赖判定、采用来源与理由明确；变化/缺失/不确定补受影响验证，目标自身与下一consumer、同操作恢复及不兼容回退证据不遗漏。 |
| V3 | P2唯一RDT五文件与真实shared diff | requirement/design/Test双向trace及根验收完整；原owner reconcile/promotion及前后fresh门禁真实，shared版本不是预造。 |
| V4 | 每轮实际changed/new范围、current Task/规划与Docs | secret scanner覆盖当前bytes无未审查告警；语法/JSON、graph/投影、diff/权限/sidecar与递归bytecode卫生按受影响对象执行，失败/SKIP不当通过。 |

#578事实采用只作用于可核实的工程执行，不替代当轮AI完整语义判断、artifact currentness或正式typed exit。73suite历史两FAIL与Bhelper对照层次保留；不变代码不重复跑无关矩阵，新增Docs与公共gate变化后执行V4中secret、JSON和差额检查。普通准备任务不继承累计多平台release gate职责。

## P5. 边界与停止

本切片不新增产品实现；发现正常路径新缺陷先保留首次失败、原qualification与诊断，技术依赖返工走原当前Delivery planning/implementation owner，不先修后补审批。scope/authority改变回原Clarify；Architecture边界改变刷新原评估。

保留同Task/gen0、原source relation、全部Delivery/规划/raw历史、合法未选archives、配置/定制及caller/main/peer指针。只写本切片规划、已选RDT共享目标和原owner最小runtime；隔离验证只在其全新临时对象执行。没有资源清理、真实业务迁移、跨仓实现或软件发布授权。用户授权只在对话，不进入tracked/ignored/runtime/DTO。
