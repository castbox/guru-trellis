# #567 设计：固定候选、适用 authority 与实际集成阻塞

状态：Planning candidate。来源、范围与验收由 prd.md 拥有；本文件只定义实际机制、责任与迁移设计，不记录前序门禁结论。Architecture 适用 authority 为 `.91` 与 constitution v1，实际判断由独立 owner 完成。

## D567-01 三个对象与唯一 owner

开发基线是进入 Task 时的明确 Git 起点；Delivery 内容候选是该轮完整未交付差额的固定 base/head；PR target 是仓库目标 branch。将三者分别承接，不再用 PR target 的最新 SHA 或祖先关系定义内容资格。

沿用 Task/Delivery 公共身份、Planning writer、Architecture/RDT、Check、TaskCommit、BranchReview、DeliveryReview/Publish/Merge、Completion/Closure/Finish 与 Reconcile 原 owner。共享 delivery_projection 只做公共模型薄投影、明确输入的 Git 事实计算和一致性校验，不新增语义协调器、审批或共享状态库。workflow 只编排，step-local Skill 独占内部行为。

## D567-02 固定完整范围与 D2 算法

原 Author/implementation owner 为当前明确选中的 Delivery 决定范围，确定性能力只计算其所选事实：

1. 结果恢复优先使用该 Delivery 已记录 candidate/result 的完整 OID，不能因恢复时 target 已前进重新选择范围。
2. 首次选择时读取实际 task HEAD `H` 及原公共记录中本 Task 已完成的前序 Delivery。只把真实 delivery_result 中的 reviewed_head 作为已交付事实，不从 Task 状态、branch 名或仅存在的 PR 推断。
3. 前序已交付 heads 中，选择当前 `H` 祖先链上唯一的最大已交付 head `P`，该轮完整内容范围为 `P..H`。这使 D2 不重复 D1；不能机械使用 Task 初始基线。多个不可比较的候选、缺少必要事实或不支持的历史交给原 owner 判断/阻塞，不能自行合并 base 或猜测。
4. 没有本轮需要承接的前序已交付 head 时，使用该轮已明确的开发基线；首次缺少已固定锚时，从 `H` 与一次观察的目标 commit 求唯一 merge base。该计算只读取既有 Git 事实，不 fetch、merge、rebase、创建临时候选或更新 ref。
5. Planning 将选定的固定内容基线 `B`、选择依据与当时观察的 `H0` 写在本 Delivery 已有 design/planning 根中；`H0` 只描述当时内容，不冻结尚未完成的实现。既有 plan_ref 绑定该设计。正常实施或必要提交产生 `H1` 时，原 implementation owner 以固定 `B`、当前实际 `H1` 和完整 `B..H1` 差额加真实 dirty 增量构造已有 candidate，再执行 `begin_check`。既有 candidate.base_ref/head_ref 承接实际 OID，不能继续使用 Planning 的旧 head。后续 public outputs 传本阶段候选，不重新解析 origin/base。
6. candidate.paths 覆盖该固定完整差额及阶段要求的真实 worktree 增量；changed paths 清单不能代替完整范围审查。必要受影响依赖仍由原 Check/Review 判断。D2 lost-result recovery 使用 D2 自己的候选，不能改用后来的 D3 或最新 base。

“固定候选”限定一个正在运行的阶段或同一次恢复操作。实际实现内容变化时，原 owner 建立新候选并重新判断受影响结果；它不是 remote-base 同步，也不因正常实施自动重做 Planning。dirty Check 绑定当时 HEAD 与实际内容；必要 TaskCommit 产生新 HEAD 后，由当前 public stage owner 经 `rework(target_role=implementation)`、implementation `begin_check` 和原 Check 的实际内容承接复核产生新 Check，覆盖原已检查内容与真实提交差额。TaskCommit 不改写 Check 或伪造新结果；若只有提交封装且内容相同，复核提交事实与既有证据适用性，不重跑无关业务验证。clean committed reentry 不改变 HEAD 或候选，沿原结果直接接续，不能为获取资格造空提交。每次 BranchReview 绑定当前提交和固定 `B`，初次仍独立完整覆盖本 Delivery。

本 Task 的开发起点为 `3b165daef0001bd9816c0bf3bbe928bcb59de390`，当前计划一个完整业务 Delivery。产品机制不硬编码该 SHA；不新增 Task base_head、跨任务 ledger、候选数据库或另一种 Delivery 身份。

## D567-03 在途与适用 authority

每个 stage 开始时由原 owner 确认完整候选和实际适用的 Requirements/Design/Architecture/constitution/工程规则/工具合同版本。阶段内的 candidate/result、现有规划与 authority 引用承接这些对象；完整 commit OID 或文档版本/内容绑定只服务直接消费者的一致性。

Architecture/RDT 的适用版本来自本阶段真实 requirement/plan 与具体 authority，不是“忽略所有 docs 目录”。immutable version 页面或 Git 历史可提供已选正文。普通 CURRENT、导航、归档、其他非依赖代码或工具安装版本前进不自动替换适用对象，不更新 contribution、不触发重签、轮询或子 phase guard。

用户新需求、明确要求立即适用于本 Task 的规则、失效的规划假设、明确依赖和实际方案/实现语义变化，仍由当前 owner 调用原 Clarify/Author/Architecture/RDT 路由，指出受影响结论和验证。旧快照不能遮盖这些实际变化。

本轮设计依赖 `.91` 的原 owner 边界、constitution v1 与 RDT `.97`。shared-current promotion 的写入仍验证当时 expected-current，防止普通错误覆盖他人贡献；该写前一致性不转成整个开发 Task 的 base 同步资格。

## D567-04 删除默认追赶边

删除 canonical workflow/continuation 在 Planning/Activation、Check、TaskCommit、BranchReview、DeliveryReview/Publish、Completion/Finish 的默认 pair guard→new_pair→Reconcile 及无条件 fresh Phase2 回边。明确 typed exit 直接进入原唯一 consumer。

原 pair guard 命令及其结果、无直接消费者的 pair checkpoint/同步字段/文案从当前 graph、package inventory、schema/examples/tests 和受管投影一起退出。真实 Reconcile 的 candidate/executor/validator、resolved 操作、committed reentry、bounded continuity 和同操作 recovery 继续存在。不得以 skip flag、同义 gate 或新 wrapper 保留默认追赶。

## D567-05 实际整合与局部接续

Reconcile 只由原阶段 owner 已观察并判断的以下实际需要调用：真实冲突、必需检查的具体集成失败、原 merge 流程确认的既有服务端强制更新、明确依赖/需求承接、用户主动同步。仅 behind 或 base SHA 不同不构成触发，不新增 Ruleset/branch-protection 查询。

原 owner 为每次操作选择固定 `new_base_head` OID，现有 selected_base_ref 接受该固定整合目标。它与 Delivery 内容基线 `B` 分开；整合不会把内容审查基线悄然替换成 target。candidate、实际 Git executor、recorder/checker 与 terminal recovery 均比较该操作对象，不能再跟随同名 remote-tracking ref。期间 ref 再前进不重建候选、不废弃已完成部分；后续只有仍存在的实际阻塞才处理新增差额。

保留实施前仅 integration_paths/stage0_tree 的 resolved baseline 与无关 dirty 保留；保留实施后 resolved candidate、合法普通冲突解决、提交 hooks/精确 staging 和 parents/tree/message 的同操作恢复。必要 mutation 仍展示精确目标和 payload，消费当前对话确认；身份、候选和真实事务一致性检查保留，不记录授权。

局部整合不改变 scope/方案时，原 Check owner 判断先前业务证据与解决差额/受影响依赖的适用性；原 BranchReview owner 判断已完整审查的业务范围加真实整合差额。需要当前 candidate/result 身份投影时由这些原 owner 完成实际局部语义审查，再经既有合法 public operations/recorder 承接。不能把旧 pass 改标签、用 tree 等价单独证明、伪造 gate，或只调用 recorder 取得新资格；也不能机械运行完整 Phase2/TaskCommit/full Review。缺少既有完整审查时仍执行首次独立完整 Review。

局部整合的 public 转换按下列单一路径完成：

1. 当前 `checking/reviewing/publishing` 的原 public stage owner（分别为 check、full_review/readiness、publication/delivery）读取同 Delivery 的真实旧 candidate、Check、full_review 和 publication 事实，判断实际阻塞后调用原 `rework` 到 implementation。scope/plan 不变时只清除 readiness；旧 Check/full_review 保留为历史事实，不能将其当新候选的 applicable gate。实现前尚无这些结果时不制造记录。
2. 原 Reconcile 处理固定目标并提交必要整合，保留其普通/resolved/同操作恢复。原 implementation owner 以同一 `B` 与实际整合 HEAD `Hi`、完整差额路径调用 `begin_check`。新旧 candidate 不同使保留的 Check/full_review 经 upstream applicability 成为 not_applicable；phase 与精确 HEAD 检查继续防止错误接续。只推进 remote ref 时不运行这一转换。
3. 原 Check owner 读取仍保留的旧 Check、原证据与实际解决差额及依赖，实际判断当前完整候选的覆盖性；通过后用原 `record_gate(check)` 写新 candidate-bound Check。若旧证据不能覆盖当前内容，只补所需检查；真实方案/语义变化回其原 owner。新 Check 可以替换旧 Check，但此时原 full_review 记录尚未被覆盖。
4. 原 BranchReview owner 读取保留的真实旧 full_review、其已审提交 `Hr` 与证据、新 Check 以及 `Hr..Hi` 的实际整合差额，判断“既有完整范围 + 已审解决差额/依赖”是否覆盖当前完整 `B..Hi`。成立时以原 full_review `record_gate` 写本人本轮真实结论、绑定新 Check predecessor，再输出原 `passed`；这不是把 `continuity_passed` DTO 换标签。原 bounded continuity 能力保留为局部判断入口，单独 continuity 结果不能替代上述真实 full_review result。没有可用旧 full_review 或覆盖性不成立时，进入首次/受影响的实际完整审查，不能凭 commit/tree 相同制造 pass。
5. 原 readiness 重新判断实际当前 PR payload，原 Publish 更新同一 PR/publication_result；原接口已要求 repo/PR/producer identity 保持。原 Merge 继续实际 expected-head 合并。已有必要整合提交走 clean reentry，不再次 TaskCommit。各 owner 丢失输出时只恢复自身已经写入且与新 candidate/predecessor 匹配的结果；若尚未完成该 owner 的语义审查就实际执行，不从 phase 推导成功。

该路径直接调整现有 owners 的输入校验、结果适用性与正文，不增加 public phase、gate 类型、跨 owner 私有状态读取或第二份历史账本。旧结果只在被对应新结果替换前提供必要历史事实；完成后由现有 public candidate/result 接续。需改变的 schema/受管 consumer 与 MIGRATION-567 同步，不能用上游 model 外的 gate 写入绕过合法转换。

真实需求/方案/实现语义变化回对应原 owner，明确失效部分；局部集成失败不能泛化为全链重置，也不能被零 reconcile 目标忽略。必要提交已由原 Reconcile/TaskCommit 产生后恢复同一 commit，不造空或同内容提交。

## D567-06 消费者同步与真实发布事务

| Consumer | 当前需退出的耦合 | 保留的事实/行为 |
| --- | --- | --- |
| Planning/Activation/Architecture/RDT | 仅 ref/CURRENT/version 改变就 stale、回规划或同步贡献 | 当前 Task/Delivery/plan、适用 authority、真实 source/方案变化、promotion 写前 expected-current |
| Check/TaskCommit | 从 origin/base 重取候选、base 前进重做 Check/commit | 固定完整候选、actual worktree、Check predecessor、exact staging/hooks、clean committed recovery |
| BranchReview | latest base ancestry、动态 ref 相等、先同步才收录 | 独立完整业务候选与依赖审查；固定 OID、真实 prior full review、受影响 integration review |
| DeliveryReview/Publish | current base SHA equality、仅 behind 拒绝 PR 或复签业务 gate | current reviewed content、PR target 名称、实际 payload/remote HEAD、同 PR 事务恢复和 readiness |
| Merge | base 前进直接重置业务 gate 或期待旧 base parent | 实际 GitHub 合并资格/checks、既有服务端强制要求、expected task head、实际返回 merge 身份和可达性 |
| Completion/Finish | 整体 remote SHA/历史 freshness 差异触发开发门禁或同步 | 全部 accepted scope、真实交付与证据、Closure/Finish 同操作结果、真实 bookkeeping 候选及 PR/merge |

merge parent/base 取真实操作结果，不要求与较早语义 gate 观察的 target SHA 恒等。仅 target 前进且服务器仍允许原 expected-head 合并时接续；真实 task HEAD、PR payload、Task/Delivery identity 或事务结果错配仍阻塞。Finish 不能要求 task 分支先包含最新 target；bookkeeping PR 仍有自己的精确文件、commit、PR、merge 与恢复核验，不改业务交付事实。

## D567-07 Completion 截点与 #569 边界

原 Completion 判断当前 Task/generation、全部 accepted scope、每项真实 Delivery 和实际所需证据。消费既有公开历史查询的明确截点及真实记录；截点后仅其他 Task/bookkeeping 前进不使该结果过期。明确发现同 Task 新增 Delivery、scope 或相关证据变化时，只取得缺少事实并重判受影响结论，不能以旧截点声称整体齐全，也不重跑已交付开发门禁。

本项只调整 query consumer 与其 freshness/恢复条件；不新增 fetch/history traversal、数据准备、截点生产者或 #569 查询算法。普通必要事实读取保持原 owner，查询准备的真实缺口诚实报告，不将 #569 设为实施/关闭前置。

## D567-08 直接迁移与投影

新增 `trellis/presets/guru-team/MIGRATION-567.md`：列出退役 guard/字段、既有 base_ref 作为固定内容对象的调用方式、候选/authority 适用性及受控 consumer 同步切换。现有公开 Skill/exit 身份保持；任何实际改变的公开 I/O 由其 owner 的 schema/interface/example/command/consumer 同步声明，迁移表不得遗漏。

新安装只运行新合同；旧安装通过完整 matching upstream/Guru 切换，工具/旧数据维护使用 #566 原 owner。正常在途任务在采用后先读取已有 public candidate/result、原 gate 的固定 base_head 与真实 source/plan；符号 ref 被 pin 到已审查对象，结果丢失回原 producer。缺少足够证据时该 owner fresh 审查/恢复自己的阶段，不强制整合、不造 Task/Delivery 或成功 DTO。只替换必要私有短期 checkpoint，不保留旧 guard 双跑或长期双读。

开发 checkout 依 canonical Candidate migration boundary 保留旧 graph。产品 canonical/dogfood/声明平台一致性在包含完整 source 与 matching installed graph 的受控 source-repository dogfood 中验证，并从其自身运行 apply/reapply/drift；不把仅业务 fixture 叫 dogfood，不声称开发 Task 已整体迁移。逐项处理 .new/.bak，保留无关修改。

## 来源约束处分与 Architecture

Issue 未指定规范性外部设计、DTO 或算法；其明确机制/职责边界仍是约束，不是 advisory。

| 来源 | 原承诺与处分 | 真实落点/影响 |
| --- | --- | --- |
| 行为1/4 | retain：开发基线/完整范围/target 分离、D2 不重复 D1 | D567-01/02；原 Delivery candidate 与实际 delivery_result |
| 行为2/3/5/7/8/9/19 | retain：零默认追赶、固定在途对象、退出旧耦合 | D567-03/04/06；全体 producer/consumer 直接迁移 |
| 行为10..15 | retain：实际触发、既有服务端例外、固定操作、局部审查与原子恢复 | D567-05/06；原 owner/executor/恢复，不新增规则查询 |
| 行为6及验收4/10边界 | retain：截点不冒充当前完整事实，#569 独占准备 | D567-02/07；只改 consumer，不增加查询生产者 |
| 行为16..18/20 | retain：适用 authority、真实变更原 owner、Markdown 判断 | D567-01/03/06；无新协调器或状态库 |
| 行为19及验收9/12 | retain：公开迁移、正常在途恢复与完整投影 | D567-08；MIGRATION-567 与受控 matching dogfood |
| 范围/非目标 | retain：不改业务仓、无Release矩阵、无攻击/锁压力扩张 | PRD/implement 验证边界与全部写入范围 |

task-owned Architecture contribution：`.trellis/tasks/10-15-567-fixed-development-baseline/architecture-contribution.md`。必要新决策 `ADR-567-CANDIDATE` 位于同目录 `architecture-adr.md`；原 ADR-005/012/013/024 保持历史含义。九 concern、before/after 与 promotion 要求由该 contribution 单写。共享 Architecture/RDT 仅在首次完整独立 committed Review 后由原 owners 晋升，晋升新 diff 再经 Check/TaskCommit/完整独立 Review，不以知识晋升代替 Delivery/Completion。
