# #531 Task 与 Delivery 生命周期解耦候选贡献

状态：draft，尚未独立 committed Review 或 promotion。本文是任务候选说明，
不授予 Architecture、Phase 2、Publication、联合验收或原会话恢复通过。
候选 identity：architecture-contribution-531-task-delivery-lifecycle-v1。

当前 authority：docs/architecture/README.md / current-main-0.6.17-guru.86 / active；
constitution：docs/architecture/00-foundation/design-constitution.md /
guru-trellis-design-constitution-v1 / current；项目 change-contract：
guru-trellis-architecture-change-contract-v1，concern set v1。
本贡献提出 legacy_boundary_convergence，实际 path 与结论由独立 owner 决定。

## Before / candidate 与唯一 owner

Before：Task 首次 Planning / activation 与后续 Delivery cycle 不对称；Guru 旧
阶段元数据与私有门禁承接开发状态，Delivery 以周期/分支/PR 事实连接。Task clean
已提交候选可能被形式提交阻断。旧安装仍必须完整可运行。

Candidate：公共Task2/API1/Plan2产品基线为1e40014023de53ddfd9368b3fb4d0a7a31e92293。
当前实际可安装matching mixed-source CLI tar为
5aeeb81ca72508081b7dd94ddb7a19f69444714f78b3a38858d908196cc77916，
Core tar为45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967。
该CLI包含mixed源schema与原binding投影的已审查本地修订；上游PR38正式交付/CI
按live结果另验，不把它标为正式source-lock。185ed1db predecessor及PR36成功
保持历史身份，不能用于当前mixed安装充分性。Guru运行时不虚构公共接口或修改provider。
Task 保留整体 scope、身份、来源和 Completion；全部 Delivery（含 D1）显式 identity、
Planning 和阶段生命周期。Guru 薄 projection 仅调用真实 installed 公共模块，
不建 aggregate/state authority 或 fallback。Guru 私有发布事务保留原 owner。

Task整体需求仅由原Author scope-only写root PRD，再交Clarify semantic owner审查并
投影公共accept_scope；新Task的null scope在首次Delivery创建前完成这两个步骤，
不生成Task方案Planning。Planning由原Author八Delivery profiles、Wording、
Architecture、Approval 与 Activation 各自承接；Activation 记录公共 Planning。
实施调用 begin_check；Check、Branch Review、Readiness 分别拥有对应公共 gate。
TaskCommit 保留必要 dirty 提交和 clean 原 HEAD 接续；改变 HEAD 后由既有 Reviewing
rework、实施 begin_check、fresh Check 再接完整 Review。bounded continuity 只证明
base delta，不能制造 full_review 或 readiness。Publish/Merge 各自恢复其真实副作用
并投影公共事实。Completion/Closure/Finish/Cleanup/Reactivate 继续分工。

## 必要 ADR 候选

531-delivery-authority-owner-exit-candidate-v1：公共 Delivery 执行状态只由上游拥有；
Guru semantic gates 与私有发布事务各自仍有唯一 owner，退出原 Task 开发 writer。
其取舍是旧安装在公共 D2 迁移就绪前继续固定旧完整安装，D1 仅受控新装集成。
这不是新的共享 current ADR，不预分配编号、不关闭既有 GAP。

## Required concerns

| Concern | Applicability | 候选承接 |
| --- | --- | --- |
| authority-binding | applicable | 当前Architecture purpose/Delivery接口、expected .86 与 change-contract v1；公共上游绑定固定真实installed candidate |
| constitution-binding | applicable | 唯一 current constitution；完整 owner/API/迁移变更接受最小必要复杂度语义审查，不机械评分 |
| boundary-and-decision | applicable | 上游公共模型/转换与 Guru 团队门禁/发布事务分离；ARCH-GOV-006..009、ADR-005/009 |
| owner-and-single-writer | applicable | 逐阶段原 owner 投影；scope 不冒充 stage writer；上游 session 唯一选择来源 |
| compatibility-and-exit | applicable | 新 DTO 明确演进，不静默双读；旧安装固定旧包；D2 公共迁移与 Guru 私有转换验证完成后才能成套切换 |
| gap-and-deviation | applicable | ARCH-GAP-006/008 继承当前closed事实，不重开或将既有关闭冒充本次成果；旧 reader 只保留明确历史/恢复 direct consumer |
| parallel-scope | applicable | 只改 #531 隔离候选，不改原业务树、上游源码/provider；共享 baseline/RDT 未 promotion，#292/#530 不覆盖 |
| evidence-and-freshness | applicable | 实际候选 tracked/untracked、真实上游模块、正式 wrapper、定向验证；唯一实际结果见 RDT Test，不用命令 green 替语义通过 |
| review-and-promotion | applicable | contribution/必要 ADR draft；fresh 独立 Phase 2、committed full-range Review、expected-current serialized promotion及新增diff重审依原合同 |

## 兼容退出与证据边界

公共接口可安装不等于Guru私有旧安装迁移完成。当前1e400140产品基线与5aeeb mixed CLI/45bb Core提供公共
Plan2、schema2首次入口、continuation extractor与C4 worktree copies/binding原事实合同；
5181/077/ce363均保留原身份及失败，不将旧collision继续列作当前候选缺口。
Guru原owner分别完成旧clean来源桥接、发布/合入/整体收尾私有转换、Upgrade恢复及
支持组合验证，当前实际结果仅由RDT Test记录。当前legacy dogfood Task在自身匹配
证据和必要副作用边界就绪前保持；受控验证不能冒充原业务会话恢复。
上游#31按最新正文独立验收，旧SDK/legacy最终退休归后续breaking release，
不以Guru joint或上游Issue CLOSED作为接口消费前置。

历史 Merge/Publication 成功先由原事务 owner 核验；历史事实不能生成当前
Planning/Check/Review/readiness pass。丢失输出接续原操作，不能重复 commit、push、
建 PR、merge。多个 Delivery、退出及 Reactivate generation 不混用门禁。
无真实副作用的样本测试不等于 GitHub 全链。

旧 writer 的删除及安装出口由 managed task-delivery-migration spec定义；旧 reader
退出以最后直接 consumer 完成为条件，公共旧数据转换仍由上游 D2 拥有。
本 Issue 的最小定向验证不扩张为完整 Release 矩阵。

Project check 使用 guru-trellis-architecture-convergence:repository:1，entrypoint
为 docs/architecture/06-governance/change-contract.md 的 AI 语义协议；最终 before/after
与阻塞判断由独立 reviewer 执行。本文不记录 reviewer pass 或授权。

最终包更换来源需fresh Plan2模板及全部workspace/session盘点；archive公共两facts由原owner投prospective目标后只读恢复。完整旧安装tracked产品增量沿独立Git边界处置，五规划source bridge不吸收安装dirty；实际新HEAD必须freshCheck并完整Review，零安装增量不提交。旧077来源/结果保留历史身份，matching joint与原业务恢复仍由实际证据证明。

## 当前 #292/#530 与公共副本合同承接

RDT authority为current-main-0.6.17-guru.89，Architecture为.86；#292的Author唯一规划writer、
Planning3两目的独立Architecture评估和#530原TaskCommit clean committed_reentry均继续保留。
无新增clean入口、owner或旧私有Phase2 authority；首次full Review仍须fresh Check及原pair guard。
公共C4原branch_bindings bytes/modes和完整registered project roots/common/local sessions由
Upgrade原owner透传；公共Plan2拥有copy组合法性，Guru不重建判定。defer peer保持Task及
五规划/raw/mode/binding，不新增peer Delivery或Guru私有migration/checkpoint。
workspace.root已为project root，project_relative只供上游逆算Git top；Guru直接投影root。
同plan丢输出恢复保留原checkpoint；source/binding/topology演进fresh prepare，不刷新旧rollback anchors。
当前local snapshot fingerprint仅标识受控副本内容，不冒充已提交树或正式source lock。
受控定向预检与最终冻结installed/joint、独立Phase2分别记录；源码suite及stub不冒充完整安装。

旧规划来源等价由TaskCommit显式markdown_relative_links_v1承担，默认原字节模式
不变；Plan2只执行真实目标内容，Planning不读私有bridge。真实e27两个空context
是合法空选择，Author校验存在和实际entries、AI判断充分性。Architecture贡献的
Task-local指任务专属owner而非Task物理目录；保留实际项目docs/contributions文件
及内容身份，不为迁移复制镜像。当前148注册root全量切换会写并行安装，故主保留
原完整legacy；受控dogfood验证与原安装实际迁移明确分开。
