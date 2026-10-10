# #468 task-owned Architecture contribution

Identity：architecture-contribution-468-direct-source-replanning-compatibility-v1；状态：reviewed_promoted；本贡献实现范围已通过独立 committed Architecture 与完整 Branch Review，按 expected `current-main-0.6.17-guru.80` 晋升至 `current-main-0.6.17-guru.81`；晋升产生的新 diff 仍待 fresh gates，不表示 Delivery 或任务完成。

## Authority / boundary

Task locator：.trellis/tasks/10-10-468-direct-source-replanning-compatibility；requirement authority：castbox/guru-trellis#468 live 正文；repository Requirements/Design：docs/requirements/README.md、docs/design/README.md。
Guru contract：guru-maintain-architecture-baseline:2.0。
Current baseline / expected current：docs/architecture/README.md / current-main-0.6.17-guru.80 / active。
Constitution：docs/architecture/00-foundation/design-constitution.md / guru-trellis-design-constitution-v1 / content / current。
Project contract：docs/architecture/06-governance/change-contract.md / guru-trellis-architecture-change-contract-v1；concern set：guru-trellis-architecture-change-concerns-v1。
Boundary/decision refs：ARCH-FND-002/004/005、ARCH-GOV-006..009、ADR-005、ADR-009、ADR-011、ADR-012、ADR-015、ADR-016；descriptor 继承的 ARCH-GAP-006/008 不改变 lifecycle。
Domain refs：current Guru workflow / Task Lifecycle。Integration refs：current Planning approved -> workflow presentation/pair guard -> Lifecycle -> Phase2 Check。
Candidate change path：target_native；实际选择由独立 Architecture owner判断，本贡献不记录 owner pass。

## Required concern applicability

| Concern | Applicability | 当前候选依据 |
| --- | --- | --- |
| authority-binding | applicable | 绑定上述 Guru/current baseline/change contract、live #468；task delta 不替代 repository authority |
| constitution-binding | applicable | 新 action/output 与短期状态由 current consumer/正常丢失窗口驱动，读取 current原则；不复制原则正文或评分 |
| boundary-and-decision | applicable | current approved 唯一 consumer 原地按 lifecycle承接；Direct Source/accepted scope、Delivery与Completion/Closure边界不变 |
| owner-and-single-writer | applicable | Planning仍审规划，workflow审对话与route，Lifecycle审/执行当前承接、独占execution result writer，Check完成后通过原owner retirement；shared current仍原promotion owner |
| compatibility-and-exit | applicable | 单一 schema/public入口直接演进，activate/recover_activation原输入与语义保持，新增 resume/recover_execution和execution_resumed；受控consumer同步，不建dual-read/adapter |
| gap-and-deviation | applicable | 修复当前in_progress新规划无正式执行路由及其输出丢失窗口；未实现不称closed，不处理无因果关联历史债务 |
| parallel-scope | applicable | 本task隔离canonical/runtime/tests/贡献；review前禁止shared current/constitution/GAP变更，禁止并行task、业务安装及生产写入 |
| evidence-and-freshness | applicable | DR468-01..04、真实Planning/Lifecycle wrappers、TaskId/gen/C4/C5/base与metadata观察；Planning评估设计候选，Phase2独立评估完整实际before/after，Branch Review完整committed范围 |
| review-and-promotion | applicable | contribution独立审查；committed review后expected-current-bound serialized promotion；promotion新增diff回fresh Phase2/commit/完整Branch Review |

## Owner、数据生命周期与 compatibility exit

Current owner graph：Clarification / Planning / Check / Delivery / Completion / Closure / Finish / Reactivate 均沿 current #454/#434/#435/#436；#464 owns dependency-scoped invalidation。
Target owner graph 相同；guru-activate-task增加明确的活动执行承接，并保持 semantic profile。新 checkpoint 仅记录其已执行结果，不是授权、批准或source authority。
Single writer：本task checkout 的实施owner写task-isolatedcandidate；Lifecycle executor/recorder独占其private执行结果写入，retirement由Lifecycle原helper执行；Architecture/RDT shared current只由各自promotion owner在review后写。

Legacy compatibility exception：无。Controlled schema/runtime/platform consumers同次原地升级，不新增旧reader、fallback或长期双实现。首次activate/recover_activation仍有当前真实consumer，保持并测试；新活动重规划不会调用这两个旧action替代新承接。
Exit / cleanup：不支持的旧 aggregate/schema声明更新为2.0；同一新schema中旧activate/recover_activation输入形状保持合法，不构建version-dispatch。无消费者旧投影/辅助实现若由该变更退出，在本task删除；仍有真实consumer的路径保留。新execution-result由原owner在current Phase2 checked passed 已产生其原checkpoint之后retire；失败和未消费结果留给same-owner recovery，不留永久history。

## Before / implementation candidate / deviation

Before：approved consumer无in_progress执行承接；首次activation只写planning -> in_progress，其recover只负责真实首次输出丢失。
Implementation candidate：相同approved consumer在AI当前展示/接受/pair guard后按合法lifecycle选择activate或resume_execution；resume不写task metadata，recover_execution只读取原owner完成结果并验证current binding/plan/continuity。唯一continuation对pending semantic DTO丢失重审、接受丢失重新展示、完成resume结果丢失只读恢复。细节由design DR468-02/03定义，不在贡献另建workflow。
deviations.closed：尚无长期关闭声明；实施候选须通过 current Phase2、committed review 与 promotion。retained：既有descriptor的ARCH-GAP-006/008与无因果关联历史债务；new：当前没有已证明新增偏移，Phase2/Branch Review仍需判断。
Design responsibility overview：.trellis/tasks/10-10-468-direct-source-replanning-compatibility/design.md 的DR468-01..04。Detailed：canonical guru-activate-task contract/interface与shared deterministic validation，workflow与continuation原consumer，Check的same-owner retirement。

## Project check 与证据

Descriptor identity：guru-trellis-architecture-convergence:repository:1；check：guru-trellis-architecture-convergence / 1。
Entrypoint：docs/architecture/06-governance/change-contract.md；result contract：guru-project-architecture-check-result-2.0。
Applicable scope：stage invocation、authority binding、path exclusivity、required concern completeness、before/after regression、single-writer、parallel stale、contribution/ADR review与promotion freshness。
Rule refs：ARCH-GOV-006..009；decision refs：ADR-005、ADR-009；gap refs：ARCH-GAP-006、ARCH-GAP-008。
Freshness source：currentPlanning design bytes、本贡献与authority的当前invocation；后续Phase2候选与BranchReview exact committedrange。独立owner亲自执行此AI语义协议，并在其原semantic result记录descriptor-bound结果；本贡献不填reviewed/pass。
Test refs：.trellis/tasks/10-10-468-direct-source-replanning-compatibility/implement.md 验证计划；docs/requirements-design-test-contributions/468-direct-source-replanning-compatibility/test.md 是本任务唯一实际证据记录位置；package/runtime、distribution、semantic review 与外部未验证边界分别记录。
Runtime refs：trellis/workflows/guru-team/workflow.md、trellis/skills/guru-team/packages/guru-activate-task、trellis/skills/guru-team/runtime/task_lifecycle/composition.py、current Planning/Check public wrappers。
External refs：#468记录Backend现场仅支持问题诊断；Backend安装、重试、生产effect均unverified。完整Upgrade/Release多平台matrix归专门owner。

## ADR、review与promotion

ADR candidate：required=false、locator为空。当前候选不改变Task Identity/source/lifecycle状态、owner/single-writer或existing architecture决策；公共action/schema增量由existing ADR-015/011承接。是否存在真实决策变化仍由独立Architecture owner复核；发现变化则先补必要ADR，不推定豁免。
Review：reviewed / independent=true；exact committed_range：origin/main@8dfa2a35bd2ccae236f7b8bc679f107f3ec1ffde...00102ccc5cb6a2102c6146421224962782ecd49f，144 paths。独立 reviewer 先完成 Architecture 再读取必要任务叙事并完成 Branch Review；两者分别实际调用正式边界，无 current-scope P0–P3 findings。
Promotion：reviewed_promoted / promoted_identity=current-main-0.6.17-guru.81 / expected_current_identity=current-main-0.6.17-guru.80。原 owner 串行晋升；live current 推进时回 sync_required，不覆盖新 authority。此次新 diff 必须重过 fresh Phase2、TaskCommit、独立完整 Branch Review；上述旧范围 pass 不替代晋升后 gates。

历史候选段落保留 before/after 和原阶段 pending 含义；当前 review/promotion 状态只以上述结尾和 identity 为准。实际 suite 与失败/未验证边界仍由唯一 Test 拥有；无新 ADR、constitution/决策/GAP lifecycle 或软件版本变化。
