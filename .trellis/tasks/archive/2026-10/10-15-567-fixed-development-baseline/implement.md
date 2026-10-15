# #567 执行计划

状态：Planning candidate，未进入实施。需求见 prd.md；唯一机制和源约束处分见 design.md。首轮独立 Architecture candidate_assessment 已返回 architecture_impact/target_native；final Architecture、Wording、Approval 仍须实际完成。

## Delivery Policy

选择 `full`：一个完整业务 Delivery 覆盖 R567-01..08 / A567-01..12，不把只删 workflow 或只改 Reconcile 当可独立完成的部分。Task Completion 仍核验全部 accepted scope 和真实结果。实现中发现确需分轮时回原 Author/Approval 修订政策，不静默降低完整行为；产品本身的多 Delivery 零 reconcile 是本轮验收场景。

业务 PR 使用 Refs #567，Task 继续 active。Merge→Completion→Closure→acceptance/Finish→Cleanup 各走原 owner；只有整体完成才按 exact_source 关闭 #567。bookkeeping PR 不算业务 Delivery。当前 branch/worktree 按创建时 caller_owned 归属保留，Cleanup 必须明确非阻塞处置，不删除来源会话或业务资源。

## 写入边界与顺序

1. 完成当前 Planning：Author requirements/candidate→独立 Architecture candidate_assessment→Author solution→Wording→独立 final_plan→Approval→当前对话展示及 activation。原完整 installed graph 管理本开发 Task，不将 source candidate DTO 混入它。
2. 实施前加载 trellis-before-dev，实际读 workflow/preset/docs/Architecture 规范及 subtraction-first。每个写入批次先执行 `check-task-checkout-boundary.sh --json --task .trellis/tasks/10-15-567-fixed-development-baseline`。
3. 按 design D567-02/03 先收敛既有 Delivery candidate、阶段适用 authority 与恢复事实输入，再同步所有下游 owner；禁止先加 bypass 或暂留第二套 base freshness。真实新 scope/mechanism 先走原 qualification/Architecture/Author，不自动扩大。
4. 收敛 Reconcile 的实际触发、固定操作和局部接续，保留全部普通/resolved/committed/recovery 原子能力。删除失去 consumer 的 guard commands、schema、checkpoint、注册、文案及测试；保留仍有真实消费者的能力。
5. 同步 canonical workflow/continuation、Skill/interfaces/schema/examples/runtime、shared spec 与声明平台入口，写 MIGRATION-567 的逐 owner 切换/正常恢复合同。
6. 执行下述定向验证与代表性 matching installed 公开链路，完成唯一 Test 和 traceability；RDT 原 owner 先协调 task-owned delta。完成实际 semantic Check→TaskCommit→fresh 独立完整 Branch Review，不用结构检查替代。
7. 首次 committed review 后，由原 Architecture/RDT owners 以当时 expected-current 串行 promotion；promotion 新 diff 重走实际 Check/TaskCommit/独立完整 Review。之后 DeliveryReview/PR readiness→Publish→Merge→Completion/Closure/Finish/Cleanup；各独立 Git/GitHub 副作用展示实际目标再确认。

允许的产品范围：`trellis/workflows/guru-team/`；`trellis/skills/guru-team/` 中 D567-01..08 的实际 owners/consumer/测试；`trellis/presets/guru-team/` 的对应 spec、overlay、README、migration 和实际分发；task-owned docs contribution/必要 ADR 及其后合法 promotion。禁止 upstream源码/global npm/node_modules、其他 Task/分支或来源业务仓修改。

## Docs SSOT Plan

策略 `delta_first`。实施前后由原 RDT writer 维护 `docs/requirements-design-test-contributions/567-fixed-development-baseline/`：requirements.md 单写 R/BEH，design.md 单写 DES/CON，test.md 单写计划、实际结果、首次失败/恢复和未验证边界，traceability.md/manifest.yaml 承接 R/BEH→D/CON→T/CASE→canonical 实现。Task 三文档只作为本次规划，不作为长期产品 authority。Architecture contribution 与必要 ADR 见 design.md。

原 `guru-maintain-requirements-design-test-ssot:task_impact_sync` 在最终 Phase2 前协调完整 delta；不把文档补齐首次留到 Branch Review。普通 CURRENT 前进不自动改变已选适用版本；promotion 写入冲突由其原 owner 处理真实差额，不制造 Task base 同步。

## 验证计划与证据层

所有条目当前均为未执行，不记为通过。使用当前完整 matching CLI/Core/Guru 资产，先核验来源与版本；测试依赖缺失是环境阻塞，不改断言、跳过失败或用全局包替代。

| 层级 | 内容/入口 | 检出的问题与边界 |
| --- | --- | --- |
| Package/runtime | 按实际受影响 packages 独立运行其 contract/runtime tests；重点原 Reconcile、Check、TaskCommit、Review、DeliveryReview/Publish/Merge、Completion/Finish 与 Architecture/RDT | 固定 OID、真实 Task/Delivery、正确消费者、在途ref、旧guard退出；保留既有普通/resolved/hooks/recovery 正常回归。不能只比字符串常量。 |
| 实际候选演进 | Planning观察H0→正常实施/必要提交H1→Check/TaskCommit/首次完整Review；以及旧full_review→真实整合Hi→原rework/begin_check/Check/full_review/readiness/publication | 固定B不冻结实现HEAD；新结果精确绑定当前candidate/predecessor。保留的旧结果只作历史证据，candidate变化后不得作为applicable gate；实际owner补受影响审查后写新结果，无额外提交/机械完整重跑，覆盖每个owner结果丢失后的正常恢复。 |
| 公开跨 owner 链 | 实际 wrappers 和原 Task/Delivery API；A/B 同基线，B 多阶段合入；记录调用与 Git parents/HEAD/结果，断言自动 Reconcile、同步提交和 base 回退为0 | A567-01/02/03/04/10。覆盖 D1→D2、D2 lost-result recovery、整体 Completion。仅 host 预写 owner pass 不证明 AI owner 运行。 |
| 实际阻塞/局部恢复 | 原公开 owner 处理 Proto/生成物/文档冲突、具体 required check失败、整合期间base再次前进、服务端已确认更新要求及无此要求的behind对照 | A567-05..09/11。核对同 PR/Delivery、固定目标、原子能力、必要差额验证与无不必要全链重跑。模拟服务事实不冒充真实GitHub服务端效果。 |
| 历史 consumer | 原已存在查询结果的明确截点与真实 Delivery facts；无关前进、新增本Task交付、scope/evidence变化分别进入原 Completion | A567-04/10；只测 consumer，不实现 #569 fetch/遍历/数据准备。 |
| source/installed | source package validator；一个代表性完整 matching installed 公开链路；含完整source+installed的受控 source-repository dogfood | 不把开发checkout旧graph误称已迁移；实际AI执行与确定性fixture/静态检查分别陈述。 |
| reapply/drift | 从受控dogfood自身运行 canonical apply.sh，再运行 check-dogfood-overlay-drift.sh；校验声明平台/shared、managed inventory、sidecar | A567-12；.new/.bak逐项处理。普通Issue不扩完整多平台Throwaway/Release矩阵。 |

source validation 命令采用仓库 `check-skill-packages.sh --root <source> --mode source --json`；installed 使用其自身 `--mode installed`。具体 unittest 通过原 managed Python、matching upstream assets 与各 package tests 运行，防止同名模块跨包串扰。语义完整性由实际 owner 检查，命令绿色不等同 Check/Review/PR readiness。

必须真实演练两类反事实：仅共享ref/base/CURRENT前进不发生同步工作；真实候选、scope、依赖或方案变化仍发生对应原owner检查。对已交付内容不得只测“最后走通”；比较每轮完整范围、恢复对象和实际省掉的调用。

未要求：来源业务生产验证/安装、tag/Release、全部历史Task迁移、完整多平台矩阵。实际 GitHub服务端、native入口和代表性installed的未覆盖项必须由唯一 Test/最终报告明确列出；若缺口属于 A567 当前验收，不得称全部完成。
