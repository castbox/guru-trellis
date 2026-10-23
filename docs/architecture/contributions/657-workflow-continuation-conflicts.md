# #657 活动续接与范围修订合同收敛：Architecture 候选

状态：task-owned candidate，尚未 final_plan、Check 或 promotion。本文拥有本批真实架构差额，不能证明实现、installed/native采用、Task完成或Release。唯一来源为 #657 的F1–F6/R1–R7/V1–V12；本批Delivery规划见 `.trellis/tasks/10-23-657-workflow-continuation-conflicts/deliveries/26065f96-88c8-40fe-aacd-64bbe5ccf949/design.md`。

## Authority、before与target

Architecture identity为guru-trellis-architecture，constitution为current guru-trellis-design-constitution-v1，change-contract为guru-trellis-architecture-change-contract-v1，required concern set为guru-trellis-architecture-change-concerns-v1。晋升前完整authority由Git `319202beab79c7666ecdb855291bf117e43d407e` 的docs/architecture完整单元定位；promotion时原owner再读取真实live expected-current，不能用Planning观察替代。

Before：公共Task2/Delivery API1已支持原identity/binding/checkout/current phase，workflow的写入和created consumer仍泛化初始创建；scope共享说明还将旧clear、private4/scope_ready1和旧Author profile当current。Target：活动续接由原身份和实际阶段owner准入；Creation的created wire保持，consumer查询实际phase，只有planning中真实初始requirements义务且符合入口才进入initial Author；已有planning按实际未完成义务回适用Author/Wording/Architecture/Approval，当前approved进入Activation，缺失或过期输出回原producer；scope严格经历pre-Author→根PRD→Clarify acceptance→post-Author。初始创建恢复保持精确。原实际candidate assessment返回architecture_impact/target_native，尚不是最终方案通过。

## 职责、取舍与窄替代

Global workflow独占跨Skill路由和continuation，原Skill保留entry/gate/recovery内部合同。公共API唯一拥有Task/Delivery状态，Identity/Establish/rebind/Ensure/Bind唯一拥有当前common-dir关系。Creation选择不改变公共phase；created只交最小既有DTO，不携带phase cache、批准或原机资源资格。consumer fresh public query后按现有continuation的真实未完成义务接原owner，包括planning内部已有文档/门禁的原回程；仅真实initial requirements才initialAuthor，current approved进入Activation。阶段不能代替gate。

Clarify先判断范围，scope-only Author独占根PRD，Clarify acceptance核真实AuthorityRef后accept_scope，post-acceptance才交当前stage合法rework/stop。无Delivery按义务进入显式Creation/Completion，不造空切片。Discovery、Review和verifier只收敛当前文字与原可执行模型；pinned-old不是fallback。完整matching安装沿原upgrade/preset机制分发。

必要窄决定候选见[ADR候选](657-workflow-continuation-routing-adr.md)。其替代范围是ADR-011内旧Task status/activation/checkpoint/Finalizer恢复路由、ADR-023内旧scope DTO/profile/resume，以及ADR-024未明确排除的created→initial Author普遍解释。保留它们的原continuation、唯一writer、公共模型、原producer恢复、历史事实和终态owner。当前change-contract的Current Planning旧scope段同步对齐；没有新Skill、出口、schema、状态机、长期台账或legacy双读。

## Required concerns

| Concern | 适用性与本批承接 |
| --- | --- |
| authority-binding | applicable；原Planning candidate/final两目的与真实baseline/change-contract；最终评估重读正文和当前候选 |
| constitution-binding | applicable；命中概念完整、职责隔离、最小必要复杂度、target_native债务收敛；原官方扩展面满足成熟实践。无宪法例外或机械评分 |
| boundary-and-decision | applicable；created consumer的阶段职责和scope两次承接改变当前路由定义；窄ADR给出明确替代，不泛化重构 |
| owner-and-single-writer | applicable；公共状态、Clarify、Author、阶段owner及RDT/Architecture晋升各自单写；consumer不读取producer private |
| compatibility-and-exit | applicable；created wire/API不变，consumer语义按已支持selection事实纠正；完整matching切换，旧在途由原producer恢复，退役格式不转换pass |
| gap-and-deviation | applicable；既有GAP状态保留，无新GAP或宪法例外。本批残余冲突用R1–R7/V1–V12关闭，不将关闭事实预填 |
| parallel-scope | applicable；Author仅写本Delivery规划和本贡献/ADR；实现改canonical，shared current只由原owners final_integration写，保留并行工作 |
| evidence-and-freshness | applicable；固定B和实际candidate分别绑定；source/package、actual Agent、installed、外部层分开，初始诊断不证明修复通过 |
| review-and-promotion | applicable；final_plan审真实贡献和ADR，完整隔离proposed targets经candidate Check，再由原Architecture/RDT final_integration晋升，actual after重新Check/commit/完整Review |

## 拟晋升完整单元与原owner

原Architecture owner准备并独立审查 `01-current/system.md`、`03-domains/ownership.md`、`04-integrations/distribution.md`、`06-governance/change-contract.md` 的实际命中完整单元及正式ADR。导航仅在真实locator/关系改变时更新，不制造全局版本递增、逐Issue摘要或空GAP记录。ADR候选正式落点由原owner查重选择，不能冒占已有编号。RDT原owner维护requirement/design/test/traceability，结果只在唯一Test记录；本贡献不复制运行日志。

Planning不写共享authority。implementation完成完整proposed正文→原candidate/begin_check→独立Architecture/Check→合法回implementation→原owners final_integration/readback→重新candidate/begin_check→最终Check/commit/独立committed Review。promotion后的真实差额不能由候选pass直接放行。

## 验证与未验证边界

V1/V2/V7要求最多一个matching installed/native独立clone，缺原机created/runtime，正式rebind revision>0后由原owner实际写入。V11要求created实际consumer接当前阶段owner；V3/V12要求scope完整两段消费，三种disposition及有/无Delivery定向对照。其余V4–V10检验准确停止、初始恢复、Discovery/Review/verifier及分发一致。普通错误和输出丢失使用正式操作，不伪造artifact构造安全场景。

当前本文是方案候选，所有新增行为仍未验证。fixture、文本一致和入口诊断均不证明原生Agent闭环；source采用不证明已有业务安装、全平台或Release。无待用户决定的架构要求，具体工具链缺失须按原owner报告阻塞，不删减验收。
