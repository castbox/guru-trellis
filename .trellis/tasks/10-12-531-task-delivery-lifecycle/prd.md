# #531：Task 整体责任与 Delivery 生命周期解耦

当前来源重绑定：2026-10-13 已实读上游 Plan2 副本补修 PR #36 的提交、公共接口、独立质量审查与同源安装包。新候选为 `1e40014023de53ddfd9368b3fb4d0a7a31e92293`，原本地snapshot manifest `17ea37fbfcfe81a7e2c43f223cacdeee6ebd4c90cd28fff74c143a75bebd1a50`，CLI tar `185ed1db6865b72138bb10b6d799225721bf50fddfb370f84d8ec330558f472d`，Core tar保持 `45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967`。新增公共 `branch_bindings` 由上游唯一 Plan2 executor 解释；具体来源层级、公共约束与Guru承接见 design §16。整体 accepted scope、Task/generation 与 .86/.89 authority不变。下文5181/collision及其Planning是旧候选历史与原失败，不能重标为新候选验证。新来源已进入原Author的独立候选评估与方案写作；当前计划仍须Wording/final_plan/Approval及展示后的执行接受。PR #36已合入且CI成功，不以merge状态替代Guru门禁。

## 1. 当前需求与边界

Direct Source：[castbox/guru-trellis#531](https://github.com/castbox/guru-trellis/issues/531)，disposition 为 exact_source。配对 [castbox/Trellis#31](https://github.com/castbox/Trellis/issues/31) 拥有通用模型与接口；链接关系不改变本 Task 的来源或 Closure authority。本文依据 2026-10-13 fresh 读取的两 Issue 最新正文（均无评论）与实际安装候选收敛。本 Task 已整合 main@bebf1993d2698d6e7e8fbd4f5388f6c4119958b0，树内 current Architecture .86 / RDT .89；当前 Task HEAD 为独立本地 base merge f03e8a04c487e64722e90697543ec7398de2b338。此前 9bee7a4e55262319fe413af6e406ed03c1c87d0a 承接 main@8b55f624/.85/.88，保留为历史前序。两个 base merge 均不含 #531 未提交工作，不构成 Guru gate pass；pending 内容、原 staged 文件与 runtime 已恢复，未应用新 Delivery runtime。

Task 保留稳定身份、Direct Source、整体 accepted scope、总体验收、Delivery 关系及绑定当前需求版本的整体完成结论。Task 不再拥有 Planning/实施/检查/发布开发阶段。每次 Delivery 包括 D1 都拥有自己的完整 Planning 与生命周期；单次交付只是一个 Delivery 的正常情况。

上游拥有公共身份、关系、阶段、合法转换、查询、session/context 及内置 workflow 采用。Guru 保留团队语义门禁、中文 Refs-only 发布政策、私有发布事务、历史归属判断和整体 Completion/Closure/Finish/Cleanup/Reactivate；以明确、最小、确定性 projection 集成。公共阶段不能代替 gate evidence，Guru 不另建公共 Delivery 状态 authority。

## 2. 当前成果与实施前提

本轮为同 Task 活动机制重规划与最终来源重绑定：整体 accepted scope 与下列验收保持，当前接口绑定
前序来源见 design §16 的真实产品提交 `1e400140…`、CLI `185ed1db…` / Core `45bbfee5…` 与实际公共 Plan 2.0/branch_bindings；本次实际来源为design §17 mixed候选及§17.2显式局部投影。§11/§15的5181绑定和collision为历史。077 绑定与已执行门禁保留为原候选历史；最终模板/安装前置变化重入原 Author，不把同版本或相同Core当整包等价。
原 ce363 D1 准入和执行记录是历史快照，不是新候选的当前批准。受影响 Planning
门禁重新执行；不重置 Task/generation，不重复首次激活。#292 交付已改变原规划的接口前提，正式 Reconcile 已返回 planning_stale；旧 .84 approved 及此前 installed 结果仅为各自候选的历史事实。当前 Clarify 已 fresh 返回 scope_ready，整体 scope 不变，唯一 Author 重新收敛受影响需求与候选；本轮 #530 来源差额的candidate_assessment、solution、Wording及final_plan曾完成；随后真实旧拓扑触发新的final_plan contract_incomplete，随后上游已交付副本补修，当前由原Author按design §16绑定实际API并完成Guru承接设计。旧轮结果不授予当前Approval，受影响候选重新评估。

| 来源 | 已核验事实 | 本任务承接 |
| --- | --- | --- |
| 上游 #31 | 已 CLOSED/COMPLETED；PR #34产品提交 bd18d5c9、PR #35最终main 780819aa均MERGED。最终已审查源码fingerprint 5181ab66…，CLI tar 6763278a…、Core tar 45bbfee5…；API1/schema2/package0.7.0-castbox.3。已实读同一最终候选连续两轮独立审查与上游安装证据；旧SDK/Plan1/显式legacy隔离保留，破坏性退休归后续breaking release。077及ce363只为历史候选 | 现有基础API保留；副本补修产品1e400140/PR36及185e新CLI实际已交付。安装、模板、binding/session前置按design§16 fresh prepare并匹配验证。不以单仓结束、报告或版本号代替Guru joint、原业务恢复或Release证据；不重写旧失败 |
| Guru #292 | 已 CLOSED，最新 main@8b55f624 已交付唯一 Author 八 profiles、来源设计处置、两个 purpose-bound Planning 3.0、revision_actions/change_refs/scope_ready 回程；当前安装仍是 Task-root 合同 | 保留已交付正向能力，迁移对象归属及薄消费者到公共 DeliveryKey/planning_root；不能直接复制 Task-root reader 后声称完成，也不能恢复旧 Planning 2.0 |
| Guru #530 | 已 CLOSED、无评论；产品 d7cde2f062a25b43fe1f554b3187506457225820 经 PR #540 合入（6cdcfbac8fcf26004c61c6d2081b47a8631551aa），PR #541 归档合入后 remote main 为 bebf1993d2698d6e7e8fbd4f5388f6c4119958b0。已读取正式 committed_reentry contract/schema/runtime | 复用原 TaskCommit clean 接续与 fresh Check、post_commit pair guard、fresh Branch Architecture、首次完整 Review；Delivery 对象迁移的逐项处置见 design §14。缺 selected base 返回诊断，不默认 main；不覆盖其工作树，不建立第二 clean authority |
| Guru #468 | 已交付活动重规划、首次激活与恢复执行输出丢失能力 | 保留合法接续与局部失效，退役 Task 首次/后继激活分叉 |

这些事实区分远端已交付能力、本 Task 当前安装与各历史候选，不构成新公共模型接口。#532/#535 已交付的真实零候选 Check/Branch Review 行为也须保留：[] 不取消完整 evidence、freshness、finding 和独立审查义务。上游 Issue OPEN 不阻止设计；上游 CLOSED 不是候选可用条件。

## 3. Accepted scope

1. 迁移 canonical workflow、step-local Skill、registry/interface/schema/runtime/consumer 以及 Task/Delivery planning 产物归属。去掉依赖 Task status 的开发路由，D1/D2 走相同 owner 链。
2. 保留 Author、Wording、Architecture、Approval、正式 Check、TaskCommit、独立完整 Branch Review、Delivery Review/Publish/Merge 的语义职责。原生入口发现时沿当前 Guru owner/profile 路由，不能先做 competing native gate。
3. 区分 Task 整体 authority、Delivery 切片与计划、candidate/基线/证据。方案变化在同一 Delivery 返工；整体需求变化先更新正确 authority，再判断受影响 Delivery。后继工作不回写已交付事实。
4. 未交付 Delivery 全范围撤回/替代时，由 scope owner 判断退出，再使用上游合法停止/unbind 接口。保留身份、已有 commit/PR；PR关闭和资源清理另走原 owner。部分范围变化仍在同一 Delivery 返工。
5. dirty 必要增量精准提交；已提交 clean 候选经 fresh Check 正式进入首次完整独立 Review，不制造空提交、重复提交、人工 dirty 或 tracked gate 文件。
6. 恢复实际 Publish/Merge 成功及公共投影失败/输出丢失；回原事务 owner 恢复同一结果，不重复远端动作。记录历史事实不要求伪造当下 gate pass；继续执行仍检查当前适用门禁。
7. 显式迁移旧 active/archived Task、多 PR/cycle、checkpoint/DTO、session/branch/worktree 与新 generation；保留文件、交付和资源，诊断缺失事实，不自动补造批准。
8. 保留整体 Completion 各回程、仅补证据/验证而无需 Delivery 的路径、独立 Closure/Finish/Cleanup 及 Reactivate。task-free 与独立手动 Git/GitHub 请求不强制 formal Task/Delivery。
9. 完成 canonical/dogfood/installed、声明平台入口、apply/reapply/drift/sidecar、native continuation 定向验证及绑定两仓固定候选的联合证据。

## 4. 结果与验收

| ID | 正常触发 | 必须观察的结果 |
| --- | --- | --- |
| AC01 | 新 Task，D1 完成后需要 D2 | 两次 Delivery 首次 Planning 前有不同上游身份；同一完整生命周期；Task无开发阶段 writer；D2不覆盖D1唯一恢复计划 |
| AC02 | D1实施中方案返工、finding-fix、Delivery Review修订 | 同一Delivery回最早受影响owner；保留候选事实；无首次Task激活；未受影响证据不整链失效 |
| AC03 | 整体需求修订、部分/全部撤回未交付范围 | 整体authority先收敛；部分同Delivery返工，全撤回合法停止/unbind；退出不伪装交付，Completion按新scope判断 |
| AC04 | 已提交clean候选，post_commit基线整合后fresh Check | 保留实际commit，首次完整独立Review可达；无空/重复commit，无跳审 |
| AC05 | Publish/Merge真实远端成功，DTO丢失或公共projection未完成 | 原owner读回同一PR/commit结果再投影；无重复push/PR/merge；公共phase滞后与门禁实质变化分别判断 |
| AC06 | 多历史PR、旧cycle、Reactivate新generation | history owner由first-parent trailers及GitHub重建事实，映射原Delivery归属；旧gate不成为新pass；已有成果按当前scope重新判适用 |
| AC07 | 已知Deliveries均交付，但存在未分配scope/待验证事实 | Completion不误报整体完成；remaining_work/evidence_pending/下一Delivery/需求修订/实现修订有唯一consumer |
| AC08 | Completion补证据、Reactivate仅验证或closeout | 无currentDelivery仍可合法继续，不强制空Delivery；完成/关闭/归档/清理相互独立；清理失败不撤销完成 |
| AC09 | 旧安装升级/reapply、入口压缩恢复 | 版本组合切换前诊断；旧数据经原owner迁移；真实installed native continuation读取唯一Task/Delivery；无reader/writer混用或永久双写 |
| AC10 | 局部provider依赖缺失 | 仅阻塞真实依赖场景；已确认必要且独立的consumer工作继续；缺口不以mock/空值声称完成 |
| AC11 | 普通method check、native入口发现、手动/task-free请求 | 普通检查不推进正式阶段；native沿Guruowner；手动事实不冒充formal pass；无Task请求不被强制建Task |

#149/#444/#155 的验收使用受控旧安装副本中保留实际旧形态的代表性事实。#149证明同Task活动重规划；#444证明clean既有候选正式Review接续；#155证明依赖不扩大为全部停摆。#149当前owner规划记载D3a已由PR461交付、D2b为planning_candidate；#155当前owner记载D1已由PR454交付且remaining_work，P406-1/P406-2仅阻奖励恢复与真实ELIGIBLE，不阻独立查询工作。以上为历史与当前scope事实，均不授予新门禁，不接管provider业务。

最终5181候选的全注册工作树Plan2在正常同TaskId继承副本下已复现collision；当时接口缺口与原失败见design §15；当前已可消费的新公共接口、原Upgrade承接与实际验收见design §16。不得省略副本、删除Task或改身份以通过验收。#149五规划与真实HEAD一致；#155当前三规划不同于HEAD，属dirty/fresh Planning，不以clean五blob样本替代。API存在与本支持组合可迁移分别判断，受影响旧安装暂不切换。

## 5. 非目标与报告边界

不修改原业务工作树、不补provider业务、不部署、不全量清理、不创建Release完整矩阵；不引入攻击/伪造/锁/竞态压力/非常规crash模型；不patch上游源码、全局包或node_modules实现Guru分叉。

四种结果分别报告：设计文档完成及审查状态、Guru实现完成、固定两仓候选联合验证、原业务owner实际恢复。受控副本成功只证明该类断点，不证明原会话已恢复；package可调用不证明native continuation；历史交付不证明当前门禁通过。本版绑定 design §16 的已审查可安装产品候选/tar/API与公共Plan2；当前承接 #292/#530，通过唯一 Author 和两个 purpose-bound Planning 3.0 刷新受影响门禁。旧 .84/.85 通过不授予本轮 .86 实施准入。旧安装切换仍以 Guru 私有迁移、公共副本支持和匹配验证为前置；当前 #531 与原业务 Task 尚未切为公共 Delivery 模型。
