# #812 D1：贯通 explicit-task 资格事实与原 caller

## 1. 整体来源与术语

整体 authority 是本 Task 根 prd.md 的 accepted_scope；当前 scope_ref 选定 R812-01～07 与 AC812-01～04。DeliveryKey 为 b16230bb-e24c-4d8e-8709-764cc35c3538 / Task 812-explicit-task-qualification / generation 0，planning_root 是本目录。

Direct Source 为 [#812](https://github.com/castbox/guru-trellis/issues/812) 的全部要求、验收与兼容边界，已完整读取且无评论。根 PRD 第1节定义 explicit-task、DeliveryKey、context 模式；本批沿用这些定义。现行 qualifier-applicability 三层完整单元约束条件调用与证据层级。来源未引入独立规范性方案，具体方案由本批 design 第3节处置。

## 2. 整体与本批目标、非目标

本批交付三个 qualifier 公开输入、共享身份事实和 caller 的一条完整 explicit-task 路径。无官方 context key 时，当前合法对象通过原身份校验并返回原 caller；有 context 时保持匹配及冲突拒绝。修复与必要兼容、分发、真实公开验收合为一个可独立合并的修复单位。

本批覆盖全部 R812-01～07。根 PRD 第3节非目标完整适用：无第二选择/绑定 authority、资格 ledger 或授权记录，不改三个语义 owner，不触碰 #808 或其他排队任务，不增加攻击、并发压力、crash 或完整发布矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

这是 D1，尚无前序 Delivery。开发起点与 Planning H0 均为 f16bb562e4ea844939786cebd5c6c20e686914b2；PR 目标是 main。该起点已含 #813 PR #816 与归档 PR #817。它们只证明前置交付，不证明本批资格路径成功。

本 Task 真实 Identity/Ensure 已成功，原 Bind 返回 explicit_task_mode；未制造环境键。当前 Delivery 在 planning，规划、Check、full_review、readiness 均未通过。实现和公开验收仍待完成；合并后还需整体 Completion、Closure、Finish 和资源 disposition。D1 不把合并事实当作整体完成。

## 4. 本批调用方、场景与流程

- DS812-01：原阶段 caller（Author、Approval、implementation、Reconcile、Check/Branch Review、Delivery Review）在自身真实适用条件触发资格时，传当前显式 Task/Delivery 身份与既有 Planning/候选事实。三个 qualifier 校验同一对象，返回原 classified 或原非通过出口，caller 继续自身义务。
- DS812-02：官方 context 存在时使用其当前选择，匹配完整身份才成功；缺失、错误或冲突保持原 owner 恢复，不将其误判为无 context。
- DS812-03：正常 generation、branch binding、registered checkout、Planning 或候选变化后旧输入拒绝。原 caller 重读同一对象，恢复后刷新受影响判断，不创建替代 Task/Delivery。
- DS812-04：matching provider 的公共合同与调用方成套更新，经原 tools owner 同步安装；原身份、scope、phase、计划、session 和历史保持。未采用安装仍按明确兼容合同处理。

## 5. 完整行为、条件与约束

DREQ812-01（R812-01/02/04）：无 context 的资格入口必须由原 Identity/Ensure/Bind 确认后，验证完整显式 key、当前 generation、C4/C5 与 registered checkout、真实 Delivery 关系、Planning 和候选。context 存在时不能以显式参数绕过官方选择。

DREQ812-02（R812-03）：normal/solution/root 的共享事实入口与所有受影响调用方使用同一合同。保留三个独立 AI 语义闭环、条件加载、非空集合和各原出口/唯一 consumer。不新增选择 writer 或绑定存储；同 caller 的当前调用上下文继续由其自己持有，不持久化资格结果。

DREQ812-03（R812-05）：公开 closed schema 所需字段变化用新版 path/id，旧发布字节保留；aggregate、Interface、命令元数据、示例、eval/test/caller 同步。明确在途和旧输入重入、采用与回退合同，不能从 ambient state 猜缺失身份。

DREQ812-04（R812-06）：验收必须通过真实原身份 owner 和三个适用 qualifier 的公开 wrapper，观察成功、非通过回原 caller 与普通 mismatch。正式 context 测试使用真实官方 context 来源，不人工制造环境键；若环境不支持该观察，如实保留缺口。

DREQ812-05（R812-05/07）：canonical 与受管 dogfood/声明平台由原安装 owner 更新，保留用户修改和 sidecar 处理。提交前完整工程检查及 Docs 整合；提交后独立完整 Review/Check，readiness 后发布，merge 后整体 Completion/Closure/Finish。每次 merge 前暂停，由协调方处置。

## 6. 本批验收、验证方式与未决项

| 本批验收 | 要求/场景 | 入口、输入与预期观察 |
| --- | --- | --- |
| DAC812-01 | DREQ812-01/02/04；DS812-01 | 原 Identity/Ensure/Bind 和三个适用 qualifier 的公开 wrapper：真实无 context 对象成功，原 classified/非通过输出被原 caller 消费，未转移失败阶段或制造身份 |
| DAC812-02 | DREQ812-01/04；DS812-02/03 | 正式 context 匹配成功，实际选择冲突与普通 generation/checkout/Planning/候选 mismatch 拒绝；恢复走原 owner |
| DAC812-03 | DREQ812-03/05；DS812-04 | 新旧 schema 与 current projection 行为、源/安装/平台及必要 reapply/drift/sidecar 定向验证；保留历史字节、Task/gen/key/root/session |
| DAC812-04 | DREQ812-05 | 本地固定完整候选 Check/full Review、readiness 与真实交付；整体终态在 main 可达，未执行边界清楚 |

选择与成本按 Test And Validation Value：长期回归覆盖当前正式入口和独立断言，临时诊断仅回答尚未解决的身份或因果问题。没有新增产品选择；公开输入迁移与验证装配由方案阶段细化，不预填通过。

## 7. Canonical 引用与本轮差额

- Requirements：docs/requirements/current/qualifier-applicability.md 的完整要求；本批补其 current identity 承接，保条件调用。
- Design：docs/design/current/qualifier-applicability.md 的完整职责与路径；共享 qualification_facts 当前 Planning 查询漏显式 key 是本次差额，不重构三个资格算法。
- Test：docs/test/current/qualifier-applicability.md 的 TST-793-01/03/05；补真实 explicit-task、context/mismatch 和 caller 观察，历史截止保持。
- Architecture：docs/architecture/README.md 的发现与维护合同；独立 Architecture 先读 constitution/change contract 和必要当前单元，再审本候选。原 owner 决定真实贡献/ADR及后续整合，Planning 不晋升共享基线。
