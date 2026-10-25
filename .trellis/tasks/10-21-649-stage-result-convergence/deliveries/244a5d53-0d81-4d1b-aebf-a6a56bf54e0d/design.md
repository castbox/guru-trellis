# 阶段成果收敛与完成证据一致性：D1 设计

## 1. 设计目标、需求承接与内容基线

本批覆盖 root PRD 的 AC649-01..07 和本批 PRD 的 DB649-01..08。目标是在原规划、实施、知识维护、Check、Delivery Review、Completion 和 task-free owner 内收敛阶段事实，不增加状态管理层。本 Task 尚无前序 Delivery；#648 是外部已交付前置，不是本 Task 的 D0。

固定内容基线 B 为 `319202beab79c7666ecdb855291bf117e43d407e`。2026-10-21 已由原 `DeliveryProjection.content_base` 以显式 development baseline 及 observed target 解析；当前没有已绑定 candidate 或本 Task 前序交付。Planning H0 同为该 commit，只描述规划起点。PR target 为 `castbox/guru-trellis:main`；后续 target 前进不自动改变 B，也不要求追赶无关提交。最终内容范围为 B 到实际候选 H，不能把 H0 当最终 HEAD。

阶段适用 Architecture 来源为 `docs/architecture/README.md`（identity `guru-trellis-architecture`）、`00-foundation/design-constitution.md`（`guru-trellis-design-constitution-v1`）及 `06-governance/change-contract.md`。独立原 owner 对当前候选正式返回 `baseline_current`，purpose=`candidate_assessment`、impact=`no_architecture_impact`。其结论只供本轮方案写作使用，不替代 Wording 后的 `final_plan`、Phase2 或 committed Review。

## 2. 当前系统、边界与目标差额

现有公共 Task schema2 和 DeliveryKey、planning_root、candidate、Planning/Check/full_review/readiness/Delivery result 承载生命周期事实。#637 已提供工程事实复用；#638 已提供隔离 proposed targets、candidate Check、final_integration、实际重绑与最终门禁；#648 已提供来源、前提及 operation 适用性判断。保留这些能力及原 owner，不新增 API、字段、exit、runtime 状态或第二写入者。

当前差额有三类。第一，原 Skill 尚未完整要求临时限制在解除后同步当前说明和断言。第二，Delivery Review／Completion 的阶段声明与缺口分类需要覆盖六维和四类责任。第三，#637 当前结果入口没有足够清晰的观察截止点。实施只修改命中的 step-local Markdown、模板／示例、必要 native 测试支持与当前知识，不修改 Backend、业务 API 或其它 Issue。

当前 native framework 已支持 Check 的 current Delivery semantic_authoring；Delivery Review 多为 post_owner，Completion 的 `tests/run_native_causal_eval.py` 使用旧 Task/gate 结构。后两者不能直接证明本项当前语义。新增测试运输将复用现有 runner、隔离 Agent 与原 wrappers，不把 host 构造的语义结果作为被测答案。

## 3. 来源设计处置（唯一）

以下均为 live #649 与已接受依赖的规范性承诺；没有 change/reject，也没有待批准的来源偏离。

| 来源／原承诺 | 处置 | 具体落点、理由及影响 |
| --- | --- | --- |
| #649 目标1：真实限制的对象、原因、解除、阶段、后继责任 | retain | 第4节 Author 正向写作和本批 implement Policy／Docs Plan；只在有真实限制时展开，不创建注册表 |
| #649 目标2：解除后维护当前成果，局部状态不泛化，历史保留 | retain | 第4节实现／RDT／Architecture，第6节解除流程；当前定义被替换，旧观察保留自身截止点 |
| #649 目标3及修订1：Check 一致性、交付六维分别取证 | retain | 第4节 Check／Delivery Review，第8节 V649-02/03；不把绿命令或部署推成采用 |
| #649 目标4：Completion 四类缺口各回原 owner | retain | 第5节原 completion/evidence_refresh 输入和现有出口，第6节分类；保持全部 accepted scope，不把缺口统一当外部取证 |
| #649 目标5：截止点、正式引用、晚到事实不递归回写 | retain | 第4节结果正文及第7节覆盖适用性；受审正文不追自己的最终 pass/HEAD，不创建空 Delivery 或额外提交 |
| #649 目标6：#637 只改可证过期项 | retain | 第4节有限修正和 V649-05；保留原失败、未知及未证安装／Release／采用／矩阵 |
| #649 目标7及 #638：原单写、最终整合、实际重绑及完整 committed Review | retain | 第6节候选链和 implement 步骤；说明性真实改动同样纳入覆盖，不豁免质量门禁 |
| #649 原 owner 表：Closure／Finish 仅终态／归档／bookkeeping | retain | 第4节原 SKILL 边界及组合最后的路径审查；不把 late facts 更新职责转移给终态 owner |
| #649 验收：原 native、独立与真实多 Delivery 组合、无答案提示 | retain | 第8节固定样本及组合；必要 test transport 执行原 API/wrapper，host 期待隔离 |
| #649 依赖及 #648：真实约束、关键前提、operation 必要性 | retain | 第6节机制冲突与合法修订、第8节组合和无依据 gate 对照；承接 #648 自身实际结果，不以组合替代 |
| #649 修订2/4/6：未激活不否定合同、源码、部署；缺切换证据只阻断依赖声明 | retain | 第4节六维规则及 V649-03；各能力、对象、环境独立说明 |
| #649 修订3/5：task-free 本地结果与 operation gate | retain | 第4节 task-free contract/evals 及 V649-03；不声明外部部署、激活、采用或 E2E |
| #649 边界：公共接口／runtime 不变，诚实正常场景，定向分发且 clean 至多一个 | retain | 第5/7/8节；无新状态台账、审批链、重复 CI 或非常规加固，完整 Release 仍未验证 |

## 4. 模块、职责与设计取舍

### 原规划与知识维护

`guru-author-task-plan/references/{planning-body,authoring}.md` 及 `templates/delivery-implement.md` 定义正向写作方法。存在真实阶段限制时，在现有 Policy、步骤和 Docs Plan 中写明五项边界及直接后继；无变化时不制造文档。既有详细／简略示例只补真实适用的阶段描述，不为教学样例新增 active state。

实施 owner 按有效合同更新实际行为和适用断言。`guru-maintain-requirements-design-test-ssot/references/{contract,current-knowledge}.md` 与 Architecture `references/contract.md` 在自身原边界要求维护完整当前单元、指南和派生说明。限制解除时替换当前有效指令，保留旧观察的来源与截止点。Architecture 仍独立判断是否有真实影响；本候选 no-impact 不创建 contribution 或空 ADR。

### 原质量与完成 owner

`guru-check-task/references/contract.md` 在原质量维度检查行为、当前说明及断言。先从合同确定正确预期，再对照实现和未改 consumers；测试保护旧限制即使命令通过也应指出普通 correctness 缺陷。

`guru-review-task-delivery/references/contract.md` 审本次成果、标题正文和发布载荷；`guru-review-task-completion/SKILL.md` 审整体 accepted scope、所有实际 Delivery、结果入口及剩余责任。两者在原自然语言 reason／evidence／summary 中逐项表达实际适用六维：合同 authority、源码实现、制品部署／入口可达、初始化／启用、消费者采用、原业务请求 E2E。不适用须给对象与理由，不造六维 schema。每维说明实际依据和环境；合同合入、源码存在、部署成功均不推出其它维度。

Completion 先定位真正未满足的 requirement、能力及 operation，再分类。必要消费者／代码遗漏回原实施；有效要求但方案自加前置回原 Author／Architecture；来源或 scope 真冲突回原 Clarify；有依据且必要的外部结果缺口沿原 evidence_refresh；无关未知保留边界并继续合法完成。不是所有信息缺口都要返回 evidence_pending。未激活只阻断依赖该状态的启用、采用、验收或完成声明。

`guru-execute-task-free-change/references/contract.md` 的完成报告只说明 edited paths、本地目标检查和未验证边界。其 gate 逻辑仍消费 #648 的保护对象、不变量、最小迁移及不适用 operation，不能以某能力未开放否定无关合同、源码或部署。

### 当前结果与终态边界

结果正文说明观察候选、所执行检查和截止点；较晚正式结果由原公共结果及 Git／PR 事实承接。当前入口准确指向唯一结果，不复制第二套完成台账。`guru-complete-task-closure/SKILL.md` 和 `guru-finish-task/SKILL.md` 只澄清原写入边界，不取得共享 Docs 修改权。

对 `docs/requirements-design-test-contributions/637-candidate-review-reuse/test.md`，逐项重读原记录及 archive，使用 PR #644 的 head `0aae5dda625278948d646a6d2027eb7785de93b6`、merge `3a38020b456112fd329e9a6616e4222e589dea12` 及其 main ancestry，限定原“实施中／未完成”的观察，并准确引用后续 Check/full_review/Delivery/Completion。只修当前入口描述，不改原命令、旧失败或当时未知。原未证安装、formal_fork_source_lock、#636 当时组合、#638 当时未来接口、业务／生产与完整矩阵按原观察保留；后续依据不足的项目不升级为通过。

### 必要测试支持

在 `trellis/skills/guru-team/adapters/eval/` 增加私有 `stage_result_authoring.py`，按现有 `stage/context/commands/validate_trace` 协议提供真实事实与原 wrapper 运输；对 native_adapter、owner_staging、eval_constants、eval_runner 仅作实际所需接线。现有接口无法表达时先在测试层解决，不修改生产 public API 或生成被测语义。

Check、Delivery Review、Completion 和 task-free 原 evals 保存各自样本；Completion 新建原 package 的 evals，不改变 legacy runner 的历史含义。fixture 通过原 public APIs 创建合法 Task/Delivery 前置；被测判断和本轮连续结果必须由 Agent 实际产生。host 的职责限于构建事实、执行 Agent 请求、收集 stdout／Git／文件差额；不得代选 exit、代写 owner result 或把 expected 表注入 Agent。

选择原 owner 正文加必要测试支持，避免新状态模块、DTO 和通用 reviewer。这样直接修复语义职责，并保持所有现有消费者兼容。

## 5. 接口与数据

公共接口和持久化字段均无变化，因此没有业务数据迁移或公共 I/O 升级。下表只说明原入口如何承接新职责；精确字段和 projection 仍由各 package schema/interface 拥有。

| 原入口与输入 | 本项读取／判断 | 原输出与 consumer |
| --- | --- | --- |
| Author `delivery_solution_planning`，当前 key 与 candidate_assessment | 当前 PRD、阶段限制、具体方案／步骤／Policy／Docs Plan | `plan_ready` → 原 Wording；不是 Planning acceptance |
| Check `delivery_candidate_check`／`delivery_check`，真实 content_ref 与原 maintenance 结果 | 完整候选、阶段适用 authority、说明、测试及 consumers | 原 candidate_checked 或最终 passed/修订出口；不互相替代 |
| Delivery Review 原 current Delivery 输入 | 实际范围、工程事实、当前发布载荷与适用六维 | 按该原 package interface 声明返回唯一出口并交其唯一 consumer；ready 交 Publication，保持现有字段 |
| Completion `delivery_completion`／`delivery_evidence_refresh` | accepted scope、全部实际 Delivery、必要证据及四类缺口 | 原 remaining_work、additional_delivery_required、implementation_revision_required、requirements_revision_required、evidence_pending、completed 或 blocked；按实际现有 consumer 路由 |
| task-free 原当前 profile | 本地 edited paths、checks、operation 影响及未证边界 | 原本地结果／evolution/scope route，不增加部署状态 |

普通缺文件、过期 input/key/content_ref 或必要事实未知，按原 owner stale/re-entry/blocked 合同处理。测试 raw trace、期望与评分只在 repo 外短生命周期测试目录；长期结果限原 RDT Test 中无法重新推导且有直接 consumer 的实际观察和结论。任何位置均不记录用户授权。

## 6. 状态、顺序、正常与失败流程

1. 规划读取当前 source、整体 scope、所选 Delivery 和适用 authority。Author 写真实临时限制；Wording、独立 Architecture final_plan、Approval 后，由原 Activation 接受当前 Planning 并开始实现。
2. 实现发现限制解除时更新其实现及断言，并由原 maintenance owners 准备完整隔离 proposed targets。遇 #648 约束冲突，停止受影响写入，按实际来源／机制／实现问题回原 owner；合法修订刷新受影响规划及判断后恢复同 key，不改 scope 来迁就错误机制。
3. implementation 以固定 B、实际 H、完整 tracked/untracked 差额构造 candidate/begin_check。独立 Architecture phase2 与原 candidate Check 审晋升前 authority、完整 implementation／proposed targets 和受影响未改 consumers。candidate 结果不写 final public Check。
4. candidate_checked 唯一 consumer 调原 RDT／Architecture final_integration。原 owners 读取真实 target 和组合差额，实际写入、读回；无影响按原 no_change，不造空贡献。
5. implementation 以同 B、实际 after 和全部差额重新 candidate/begin_check。最终 Architecture、Check、精确 commit、独立 committed Architecture／完整 B..H Branch Review、Delivery Review、Publication 和 Merge 各自真实发生。文件修订触发实际受影响覆盖判断，不以“补结果”免审；适用工程事实按 #637 复用。
6. Completion 对整体 scope 分类缺口，或以真实结果合法完成。Closure／Finish／Cleanup 仅消费其原终态事实，执行各自原副作用边界。

正常失败包含正文遗漏、错误断言、实现遗漏、外部证据未到和普通 stale/mismatch。修复停在最早受影响 owner；不得用 recorder/checker 成功替代 semantic pass。没有限制变化的交付保持原流程，不新增空文件或门禁。

## 7. 恢复、兼容、迁移与集成

所有 mapped re-entry、事实刷新与输出丢失沿原 producer 恢复；不从 phase、文件存在或旧摘要合成 pass。机制变化刷新 candidate_assessment，等义措辞只刷新受影响 gates。保持同 TaskId/generation/DeliveryKey 和 B，不重建资源。

canonical package 和 spec 是长期源；完整 apply 同步 dogfood/installed。没有公共字段变更，不需要双 reader 或迁移状态。旧 legacy tests 仍只证明其固定版本；本项 current 评测明确使用当前公共 Task/Delivery。源码修改不代表业务安装已采用。

RDT 使用隔离 delta，原 final_integration 才改 shared current。当前结果晚到时引用原结果；确有文件修订由原 writer 在合法候选边界完成并重审实际覆盖。已经执行的测试、合并或晋升不为追记完成而重放。

本项没有业务部署、DB 迁移或生产写入，不设计生产回滚协议。保留全部无关工作区与旧记录。普通分发冲突按原 `.new/.bak` 机制逐项处理，不静默覆盖用户内容。

## 8. 验证设计

固定比较起点为 B 的 #648 完整匹配方法和本项实际修改方法。两侧使用同语义事实、原预期、模型配置、权限与起点；新测试运输及 corpus 可作为双方相同的测试支持，旧侧生产方法／合同保持 B。先执行 before，再执行 new；同组各一次独立调用，失败修复后只重跑受影响组，保留首次结果。此安排不成为通用固定次数门槛。host 期待值与其它侧轨迹不进入 Agent；样本事实或环境实质变化时双方按同口径重跑。

| 验证 | 输入与真实入口 | 预期观察、对应验收及证据限制 |
| --- | --- | --- |
| V649-01 | 命中 package 单测、runtime adapter／runner 定向测试、原公共 schema/interface 校验 | test transport 调实际逻辑，旧消费者兼容、无新增生产字段；AC01/06。字面检查不证明语义 |
| V649-02 | 原 Check native：C01 后继实现但当前限制失效；C02 测试断言仍保护旧限制且命令绿；C03 同范围 A 已实现/B 未实现；C04 无变化合法候选 | Agent 自主读合同／代码／说明／断言及 consumer，检出前三者实际差额、保留 C04 合法完成；AC02。实际 wrapper、理由与读取分别审，exit 相等不独立算通过 |
| V649-03 | 原 Delivery Review native：D01 合同/源码/部署已成立但 phase 未开放；D02 缺能力切换证据且存在无关已交付能力；原 task-free：F01 本地改动完成、F02 gate 只约束特定迁移 | 六维分别表达或说明不适用；保留前三项，仅阻断依赖声明；task-free 限本地并消费 #648 operation；AC03 |
| V649-04 | 原 Completion native：P01 必要后台 consumer 未实现；P02 机制自加无依据启用前置；P03 有依据必要外部证据未到；P04 无关环境未知但范围已满足；P05 正式终态晚于正文且 cutoff/引用完整；P06 混合能力仍有 accepted scope 未交付 | 分别回真实实施、原机制／Architecture、原 evidence_refresh 或合法完成；局部不扩大。缺文档真实修订不能免受影响 gate；AC02/03/05。所有起点由原 API 建立，当前 owner result 由 Agent 自写 |
| V649-05 | #637 全文、archive 公共结果、live PR #644 和 main ancestry；P05 对照及真实文件修改覆盖 | 修正可证旧当前声明，保留原失败／未知／其它未证；后续事实可通过引用核实，不追自身 pass/HEAD，Closure/Finish 不代写；AC05 |
| V649-06 | 匹配 #648 后，一个真实 stateful Task：D1 partial 合同限制→D2 实现；原各 owner 与公共 API | D1/D2 都有实际 Planning、candidate/final、commit/merge 和 Delivery 事实；D2 含约束冲突、合法修订及原 owner 重入，说明/断言收敛；最终 Delivery Review／Completion 读取实际前序 stdout，不预填被测 gate。AC04/07 |
| V649-07 | 原 apply/reapply、drift、package source/installed、声明平台投影、executable modes、sidecars、一个代表 clean 安装 | 方法与测试支持可从匹配安装运行，用户内容保留、零未处理 sidecar；AC06。不等完整多平台升级／Release 或业务采用 |
| V649-08 | 本 Task 实际最终候选链、PR/main、Completion/Closure/Finish/Cleanup | AC07 各结果和 ancestry 真实；不以样本远端替代本项 GitHub 交付，不预填完成 |

V649-06 在一个代表 clean matching 安装上建立受控测试 provider，但必须执行原 executor、真实本地 Git commit/merge、原公共 Task/Delivery 操作和原 wrappers。provider 只承担外部 I/O 的测试层，不直接写 DeliveryFact 或返回预填 semantic pass。合同／实现／RDT proposed／promotion／真实重绑在同一连续样本发生；旧侧与新侧各有自己的同语义起点，不拼接独立样本冒充连续链。该组合只证明测试 provider 环境内的真实流程，不证明真实远端 GitHub 或生产。本 Task 的正式 PR／merge／终态由 V649-08 另行证明。

完整 #648 自身验证由其原 Test 和正式交付事实承接，逐组区分有效检错、合法对照、有效 false、execution_error/no-grade 和真实剩余边界。组合不能替代 #648 自身或本项独立样本；若发现依赖证明有必要缺口，停在实际依赖 owner，不静默启动其它 Issue。

## 9. Canonical 引用、本轮差额与实际未决项

`docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 承接 Author／Check／Delivery 状态、Policy、候选和终态事实关系；同三层 `completion-closure.md` 承接六维、四类缺口及原 Completion/Closure/Finish 责任；同三层 `knowledge-maintenance.md` 承接当前说明收敛、观察截止点和单写／晋升。只改命中条款，不重新编号旧 ID。Test 策略指向本项唯一实际结果，不复制结果摘要。

RDT 原 owner 在 `docs/requirements-design-test-contributions/649-stage-result-convergence/` 编写真实 contribution、完整 proposed targets 和 trace；第6节的原 final_integration 晋升。必要的 spec projection 落在 `trellis/presets/guru-team/spec/workflow/{quality-guidelines,workflow-contract}.md` 的既有质量／知识边界，只定位 step-local 方法，不复制流程。canonical spec apply 后同步 `.trellis/spec/`。

Architecture authority 及五原则按第1节；当前 no-impact 不创建 Architecture contribution/ADR。Wording 后独立 final_plan、实施／最终／committed 阶段仍由原 owner 新判，实际影响变化时回最早受影响阶段。

没有待用户裁决的需求、scope 或技术方案问题。实现、真实评测、安装和终态均尚未执行；本设计不预告任何通过。完整升级／Release 矩阵、业务安装采用、外部生产和原业务请求真实 E2E 均不由本仓测试推定。
