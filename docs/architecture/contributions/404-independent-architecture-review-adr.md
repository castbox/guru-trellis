# #404 draft ADR：独立评估执行与下游 eligibility
状态：draft/task-owned，未 accepted，未 promotion；不分配 shared ADR 编号。唯一候选identity：404-independent-architecture-review-adr-v1。
来源：Issue #404 r4、task design.md；继承 ADR-005 的 task-local contribution / expected-current / independent committed review / promotion 责任，不修改它的accepted历史。

## Context 与候选决策
当前 Architecture Skill 的semanticowner与formalwrapper存在，但当前AI先读taskscope再自行author，Planning/Phase2native路径也预载完成framing。候选将新Architecture评估执行交给未参与候选作者/实现、第一轮未暴露叙事的freshsubagent；semanticSkillowner不变。
Planning、实际architecture-expandingdiscovery、Phase2worktree和committedBranchReview各自形成新独立判断。genericworker只用官方fresh调度与操作性context，先读currentauthority、实际候选与真实consumer/约束，再核对解释；不能用checkergreen或角色名字替代独立执行。
publication/acceptance_finish保留既有2.0profile/stage/formalwrapper，由原Architectureowner做currenteligibility，消费仍适用的独立结论，不因caller改变重做同质assessment；需要新判断则回原stagefreshreview。main不author新Architecturepass或relabelupstreamDTO。

## Alternatives 与影响
不选第二Skill/审批链/ledger，因为既有owner能承接完整能力；不选script判责任/必要性，因为必须semantic；不选继续自评或仅平台prompt改，因为不能支持真实独立评估或全投影一致。
public2.0schema/profile/exit/consumer identity、sharedpromotionwriter、其它整体gate和sourceClosure不变。方法与eval直接演进，不支持长期混合旧执行路径，不增加compatadapter。
代价：真实fresh调度/first-roundreads/自主wrapper及consumer continuation需native行为验证；能力不足返回existingblocked，不降级主会话。必要局部重构可做，无关债务不升级current修复。

## Verification / acceptance status
只有真实native方法证据、适用projectchecks、independentcommittedfullreview与expected-currentpromotion完成，才能形成accepted/current决策。当前均为候选，测试计划不是执行证据。promotion新diff须freshPhase2/commit/fullBranchReview；Release矩阵和业务部署不在本task。
