# #579 执行计划

## Delivery Policy

full：单次完整交付 R1-R5；没有 partial/staged 交付。整个Task必须具备：canonical修复、独立oracle与正式链回归、受影响installed及分发证据、完整独立审查、Delivery合入main、Completion/Closure/Finish；业务 #564 的采用不作为前置。

## 步骤

1. 完成 Author candidate → independent Architecture candidate assessment → solution writing → Wording → Architecture final_plan → Approval → Activation。
2. 实现子代理只修改 canonical common.py 及必要 test 文件；先读spec，保持scope，发现扩张回原owner。
3. 执行直接 package 回归，证明修复前/后及身份不变。使用匹配受管Python，环境缺失不能记通过。
4. Docs SSOT策略 delta_first：按原 RDT owner 把需求/设计/测试长久可消费部分放到本任务独立 contribution；若现有 authority 已充分且无新合同，可判 no-op，并说明证据。在最终Phase2前完成对账，不在BranchReview首次补齐。
5. 通过支持的installer流程验证受影响投影；当前旧安装与canonical差异不自动升级本任务或业务仓。必要使用隔离匹配source/installed；仅与#579直接相关的投影进入候选，避免无关资产变动。
6. 独立Phase2（先独立Architecture）→精确TaskCommit→不同fresh代理完整 committed BranchReview（含独立Architecture）。
7. Delivery Review/Publish/Merge → Task Completion → Closure → Finish bookkeeping → exact-resource Cleanup，分别使用各owner，不以手工Git动作冒充结果。

## 最小验证与证据

- V1：原失败/双写栈/原样本反事实已由#579引用；新fixture原入口完成且输出正确，保留平台边界。
- V2：逐对象digest oracle与现有gitlink表示，正常文件/空/二进制/重复OID/执行位/符号链接保持。
- V3：真实 recorder/checker/public invoke 到continuity_passed及checkpoint退休。
- V4：package回归、必要source/installed公开链与reapply/drift；不跑完整Release矩阵。
- V5：task validate、diff格式/路径/链接及canonical与实际安装投影核对；保留无关dirty。
- 未验证：业务升级、部署、原业务任务正式交付、所有OS故障复现、Release多平台矩阵。

当前状态：源码与定向验证已完成，待正式Check、TaskCommit、完整BranchReview与Delivery；未声称整体任务闭环。源约束唯一处置见design.md。

## 实施与验证事实（2026-10-16）

- 生产变更限定原common.py请求传输；TemporaryFile完整写入/回卷，原解析和摘要不变。测试扩展原独立逐blob oracle，新增4096复制资产及大/空/二进制/executable/symlink/gitlink真实树，走正式record/check/invoke并验证checkpoint退休及HEAD/index/refs保留。
- 相同fixture旧传输在review-branch.sh recorder内60秒超时，单测62.394秒FAILED；仅诊断自身进程组被终止，临时源已恢复修复。修复版本package 45 tests共44通过/1既有外部API条件skip；独立reviewer亲跑相同匹配managed package亦为45/OK(skip1)。
- 使用正式Fork source lock2a6f10ba的完整scripts模板补齐隔离target前置后，原skip的schema2 archived单项1/3.571秒OK。没有用主仓旧模板或伪造API降级来取得通过。
- 完整匹配preset临时安装及installed validator通过。installed中无canonical源码树，大树正式record/check/invoke单项1/7.618秒OK；installed common与canonical字节一致。三平台Claude/Codex/Cursor reapply status ok、overlay drift status ok、递归零.new/.bak。
- 本仓旧dogfood为前序installed快照，与canonical已有全包差异；installer无单包更新合同，未热替换活跃工具/manifest、未把无关全量迁移并入#579。上列证明匹配完整安装的本修复，不证明本仓或业务旧安装已升级；最终本仓工具投影继续由#575 M/S2原owner负责。
- 原RDT owner实际task_impact_sync返回ssot_current：既有.100合同已覆盖身份及连续性职责，本次无公共行为/接口/owner新合同，delta_first对账为no-op，不制造新RDT版本或重复贡献。独立Architecture按当前93/constitution-v1判断局部技术决策无架构影响，未创建ADR/贡献。
- git diff --check与official task validate通过；context超长警告不作为通过断言，实际已读相关完整spec。默认系统python缺jsonschema的初次尝试为环境失败，未计为有效测试。
- 未验证边界：完整CLI构建与Release矩阵、所有OS同缺陷复现、真实业务安装/部署与原#564会话完成。上述均非本Issue工具修复验收前置。

必要原始验证输出在本次临时验证目录中供当前reviewer读取；本文件只保留Completion/归档消费者所需的结果及边界，不持久化调用历史或授权过程。
