# D1：约束与关键前提审查方法及行为验证设计

## 1. 设计目标、需求承接与内容基线

本批覆盖 [PRD](prd.md) D1-R01..07、D1-S01..08 和 D1-AC01..08，全量承担整体 [PRD](../../prd.md) R648-01..07。没有前序 Delivery。目标是在原语义 owner 内落实约束和前提审查，并补足可复核的跨阶段真实行为证据。

开发基线 B 为 `cca65742bc485f8ab4e6399623b70dd5aebc25bd`，来自本批显式选定的 development baseline。原 `DeliveryProjection.content_base` 已返回同一 B。Planning H0 同 B；最终 H 是实际实施候选，不能把 H0 当最终 HEAD。内容范围固定 B..H 加实际 dirty paths；PR 目标为 `castbox/guru-trellis:main`，目标前进不自动改 B 或要求集成。

适用 Architecture 为 `docs/architecture/README.md` 定位的 `guru-trellis-architecture`、`00-foundation/design-constitution.md` 的 `guru-trellis-design-constitution-v1` 与 `06-governance/change-contract.md`。独立原 owner 已对五项候选事实完成 `candidate_assessment`，原 wrapper 返回 `baseline_current / no_architecture_impact`：本候选不改 owner、single-writer、公共 I/O、阶段、出口、持久状态或兼容机制。该结果只允许本轮 solution planning，不代替后续 final_plan、Phase 2 或 committed Review。

## 2. 当前系统、边界与目标差额

现有 Author 已有完整来源读取与唯一设计处置；Architecture 已有独立读取、实际消费者及 before_authority；Check/Branch Review 已有完整候选、测试价值和九维审核。task-free 已有 pre-write/evolution qualification、受影响写入停点与 scope route。#637 的覆盖/工程事实复用和 #638 的 candidate Check→最终整合→实际重绑→final Check 保持。

当前研究冻结了 B 的源码 archive。两项原 Architecture native 样本中，真实 Agent 已调用原 wrapper：业务默认值样本返回 fitness_regression，合法技术 selector 样本返回 baseline_current。具体记录显示前者追踪未改 summary caller 的输出影响，后者读取 provider 兼容规范并区分合法配置。这是已存在能力的局部证据，不能写成新增收益。两次 runner 汇总均为 execution_error：trace 缺少 runner 要求的若干公共 schema 读取；没有取得完整评测通过。更早的隔离环境/provider 配置失败同样保留，不算语义失败。

确定的交付差额包括：Author 的实际约束落点样本；实施发现规划内冲突的停点/三分流/恢复；Check/Review 从有效合同识别共同错误预期及未改消费者；同 reviewer 前提变化与无变化对照；task-free 同域 A/B 的真实行为。现有两项 Architecture 样本不足以证明这些要求。方法正文只修订真实证据和完整条款核对确认的缺口；已经有充分现行定义和行为证据的 owner 保留原文，不能为了凑改动遍改全部 owner。

## 3. 来源设计处置（唯一）

以下逐项承接 live [#648](https://github.com/castbox/guru-trellis/issues/648) 的规范性设计承诺。全部 retain，没有改变上游承诺；具体机制在第4至8节展开。PRD 与 implement 仅引用本节。

| 来源章节/承诺 | 处置与具体落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| 目标1：完整条件、否定、例外、对象、来源进入实际设计与唯一处置 | retain；第4节 Author 在原 planning-body/authoring/template 内说明实际行为落点；V648-01 检查实际产物 | 不建逐约束 ledger，不复制 baseline；无上游变更 |
| 目标2/3：四类来源、关键前提原证据、合法例外、before_authority、独立但不漏约束 | retain；第4节 Architecture 原 contract 与 native authority projection，V648-02 | 批准/晋升和候选新基线不自证；缺来源走原 incomplete/blocked；不改独立 reviewer 载体 |
| 目标4与分流表：规划内也停、原 owner 三分流、依赖范围与恢复 | retain；第6节实施/协调顺序与 V648-03 三种原因 | 不新增 profile/exit/冲突记录；scope 不变的方案修订留 Author/Architecture |
| 目标5：有效合同先于实现测试、真实状态与未改消费者、职责缺陷无需生产事故 | retain；第4节 Check/Review 原 contract；V648-04 | 不机械枚举全状态；不把绿测试当合同正确 |
| 目标6与10/21补充：依赖必要性、task-free gate六项语义、A/B | retain；第4/6节 task-free 原 pre-write/evolution；V648-06 | 通用 gate/invariant/operation，停止受影响写入；不引入业务名称或跨能力普遍前置 |
| 目标7：新证据否定前提即刷新、合法无变化复用、影响不明完整评估 | retain；第7节覆盖适用性；V648-05 | 保留 #637；无无因全链重跑，无新覆盖缓存 |
| 验收：先固定当前匹配版本、真实盲测、等价输入、原 wrapper、跨阶段行为 | retain；第8节样本和证据方法；第2节如实记已有结果及失败 | 期待在 host 外侧，单点出口/静态检查不替代语义；本项不延期 #649 |
| 边界与依赖：公共API不变、原#638晋升、定向分发与SSOT同步 | retain；第5/7/9节与 V648-07/08 | 无新schema/stage/DTO/runtime；最多一个clean，不发版本、不改业务现场 |

## 4. 模块、职责与设计取舍

**Author。** 在 `trellis/skills/guru-team/packages/guru-author-task-plan/references/{planning-body,authoring}.md` 和 `templates/delivery-design.md` 内，核实原方法是否把完整适用约束转成设计具体行为与落点。仅在不足处补写：对影响可行性、职责、拒绝条件和依赖的假设，标明原证据与未验证边界；retain 与原则引用不等于遵守。沿原 design 第3节处置来源，不制造第二台账。真实 Author 样本必须产生正文并由原 Author wrapper 返回；宿主不能预写正确落点供其复制。

**Architecture。** 原 `guru-maintain-architecture-baseline/references/contract.md` 保留独立入口及读取顺序。必要细化限定于四类来源、关键前提原证据、合法例外和候选不能自证 before_authority。现有 `adapters/eval/architecture_authoring.py` 负责投影实际 authority、候选、原始证据与未改消费者；不把 host 答案、期待出口或另一侧运行记录注入。读取/trace不足只报告执行缺口，不改为语义通过。

**实施与协调。** workflow 只写受支持的停点触发及既有 owner 重入；原实施/Check Skill 或 dispatch 方法拥有具体行为。发现规划内冲突也停受影响操作。不得修改 upstream-owned 官方 Trellis agent 文件来植入流程。第6节三分流由当前 AI 根据真实条款和候选判断，脚本不作路由判断。跨阶段 native fixture 先给已接受方案，再提供实际发现的原证据，观察是否在下一次受影响写入前停下；后续修订和恢复必须真实发生。

**Check/Branch Review。** 原 `guru-check-task/references/contract.md` 与 `guru-review-branch/references/contract.md` 只补未明确的合同先于断言、共同错误预期和真实未改消费者。Check 的原 `adapters/eval/phase2_authoring.py` 继续真实独立 Architecture predecessor→qualifiers→原 recorder/checker/wrapper。Branch Review 样本使用实际 committed B..H，并真实调用原 Review wrapper；早期反馈或 Architecture 出口不能冒充完整 Review。

**Task-free。** `guru-execute-task-free-change/references/contract.md` 及原 evals/files 增加 gate/invariant 的正常成对样本。执行 owner 说明保护对象与不变量、最小触发迁移、不适用 operation、缺证据阻断范围和 evidence owner/consumer。该判断留在原 semantic gate，不交脚本按 operation 名称分类。A 只读历史内容或改展示属性、不改变生效目标；B 变更生效目标，保护的是目标进入运行前的资格不变量。两者同域、同一缺失资格证据。共同错误实现把 A 也拒绝时，原审核必须指出无依据前置。

**确定性测试支持。** 只在 `trellis/skills/guru-team/adapters/eval/` 的原 staging/native 路径扩充事实、调用与记录；对应 test_architecture_authoring/test_phase2_authoring 证明投影、真实入口与结果绑定。若被触碰的非生成代码文件超过3000行，先做机械拆分/小幅解耦评估，在原职责中拆出本项事实 fixture，不能新增通用执行框架。测试脚本不判断语义充分性；每次语义结果由 AI 审核原记录。

直接细化现行 owner 比新建公共 Skill、审查阶段或 ledger 更合适：现有入口已拥有所需判断和唯一 consumer。保持现行独立 reviewer 机制，#651 不在本项；保持结果/Completion 状态机制，#649 不在本项。没有新的架构决策，因此不预建 Architecture contribution 或 ADR；若实际机制扩大，回原 candidate qualification/assessment。

## 5. 接口与数据

公共 API、DTO、schema、profile、typed exit 和 runtime 状态全部保持。原 Author requirements_ready→Architecture candidate_assessment→solution planning→Wording→Architecture final_plan→Approval/Activation 顺序不变。Phase 2 仍由现行候选和 knowledge consumers 承接。

原 Check/Review/task-free inputs 与输出由各自 Interface 定义；新增样本只提供真实来源、源码/设计/测试、候选与当前阶段事实。原 wrapper 校验结构、身份及freshness；AI完成适用性、finding和route。缺证据和机制不适用分开，不能把候选引入的错误依赖当外部阻塞。

没有生产持久化数据、DB migration或新配置。repo外raw native记录只供当前验证和结果摘要，不进入公共 handoff。临时 isolated CODEX_HOME 与provider凭据沿原权限边界，最终删除临时凭据，不输出值，不进入仓库或报告。

## 6. 状态、顺序、正常与失败流程

先修复测试调用的可执行条件并对冻结 B 运行完整所选样本，再决定方法差额。随后改原Markdown/示例，在相同或严格等价事实、模型、权限和起点上复核。期待表始终在被测上下文外；改变输入口径时两边重跑。新的测试 staging 先在冻结方法上执行，不能先改方法再补称 before。

实施冲突按原职责分三支：

1. 需求/约束有效，方案或关键前提错误：暂停依赖该方案的写入，回 Author/Architecture 修订；保留accepted_scope，完成受影响规划与审核再继续。
2. 需求承诺、规范来源或例外authority冲突，或确需改范围：原Clarify处理来源/范围选择。涉及架构时原Architecture提供具体冲突；它不成为所有来源修订的新增前置。
3. 规划有效，仅实现或断言偏离：原implementation/Check修复，按有效合同恢复断言。

协调者必须核实冲突已解决、受影响规划/审核与实际候选重新匹配后才恢复。脚本通过和旧批准不能恢复。无冲突工作仅在不存在真实依赖时继续，不能借并行推进受影响目标。

task-free A在缺相同门禁证据时成功，说明未改变保护不变量。B改变不变量，缺证据时原owner阻止依赖写入/操作并指出真实缺口。若A被共同错误规则限制，暂停受影响target write，经原task_free_evolution或scope route修机制，不静默扩大到业务政策。

## 7. 恢复、兼容、迁移与集成

失败结果保留首次记录。环境/调用错误修复后新开本轮原入口，不覆盖失败；真正wrapper非零停止当前invocation，不能拼造pass。输出丢失按原producer恢复，阶段和历史事实不被重建为语义结论。

#637复用以真实定义、输入、依赖、环境、工具链、参数和预期的适用性为依据。新增原证据否定关键前提时，即使代码/测试相同也补审受影响判断；其余事实保持。组合影响无法界定时完整评估。不得跨读或重建已退休private checkpoint，也不为该规则新增缓存。

无public接口迁移、旧路径替代或双reader；新定义通过canonical source、完整preset和原managed projections同步。修改overlay时执行`trellis/presets/guru-team/scripts/bash/apply.sh --repo .`并检查drift，逐项处理sidecar。workflow修改同步dogfood同名副本，不改上游Trellis源码、全局包或node_modules。更新/reapply保持用户修改和官方template-hashes语义，不能靠直接覆盖安装副本维持效果。

RDT走隔离proposed delta；candidate Check完整审实现和拟写内容，通过后合法回implementation。原RDT/Architecture owners执行final_integration并读回，implementation以同B和实际after重建candidate/begin_check，再最终Check、commit和独立完整committed Review。no-impact/no-change仍沿原合法回程，不制造空贡献或空提交。

## 8. 验证设计

固定以下样本组，每组各两次独立before/new运行；同reviewer前提变化组在一次运行中真实接续同owner。原有两次不完整runner结果是探索记录，不计完整次数。before方法来自固定B；新fixture投影到同一冻结方法，事实与新侧严格等价。模型采用各原corpus声明，当前Architecture/Check semantic_authoring为`gpt-5.6-sol`；reasoning high和原权限保持，不能以CLI覆盖声明冒充模型一致。

| 验证 | 要求、入口与输入 | 必须观察与证据边界 |
| --- | --- | --- |
| V648-01 | R01/AC01..03；原Author native跨阶段入口；含完整否定/例外的来源与真实候选 | 实际正文具体落点、唯一来源处置，原wrapper；不得由host预写正确答案 |
| V648-02 | R02/AC01..03；原Architecture semantic_authoring；错误默认/未改consumer、原证据否定已接受前提、合法来源例外对照 | 自主指出原条款与因果，例外理由成立；完整trace/正式wrapper成功，单出口不足 |
| V648-03 | R03/AC03；原跨阶段native；已批准方案内的三类冲突分别给真实新事实 | 停止下一次受影响写入；条款/候选/影响、原owner分流、真实修订与匹配恢复；独立工作按依赖继续 |
| V648-04 | R04/AC03；原Check semantic_authoring和实际B..H Branch Review；设计/源码/测试共同错误地拒绝A，未改caller依赖A | 先确定有效预期再审实现/断言，指出共同错误与consumer影响；正式Check/Review，不以Architecture单点替代 |
| V648-05 | R06/AC05..06；原reviewer接续；代码测试不变、原证据否定前提；另给完全无变化对照 | 命中判断刷新、合法工程事实复用；影响不明完整评估；无无因全链重跑 |
| V648-06 | R05/AC04；task-free原evals；同域A/B均缺同资格证据及共同错误限制A候选 | A真实成功及不适用理由，B真实失败及不变量/阻断范围/owner/consumer；错误限制A被审查指出 |
| V648-07 | AC07；命中packages/runtime/native staging定向tests、source/installed、声明平台、完整apply/reapply/drift/mode/sidecar | 记录真实命令及结果，零未处置.new/.bak；最多一个代表clean，完整Release矩阵未验证 |
| V648-08 | AC06/08；原RDT/Architecture、候选Check/整合/重绑/finalCheck/committedReview | 完整实际after及必要未改consumer、追踪一致；真实源码分发与Agent行为分别报告，不声称业务安装采用 |

原公开入口为`.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill <原skill-id> --adapter codex --case <原case-id> --run-root <repo外路径> --json`。确定性fixture tests不代替实际Agent行为。before/new每次审核具体约束、因果、测试预期和原owner路由；两边都检错记已有能力。若before已满足方法，只交付新增覆盖/示例；若有漏检，在同输入验证修订收益。执行失败不等于检错失败，不能从绿色汇总反推语义通过。

## 9. Canonical引用、本轮差额与实际未决项

命中RDT为`docs/{requirements,design,test}/current/knowledge-maintenance.md`的来源/适用性、真实对照和最终整合部分。原RDT writer准备`docs/requirements-design-test-contributions/648-constraint-premise-review/`完整delta，测试正文保留V648行为/入口/观察，实际结果只有一个具名位置。共享current在原final_integration晋升，不在Planning提前写入。

Architecture约束仍由第1节authority及`docs/architecture/06-governance/change-contract.md`拥有；当前no-impact不修改基线/constitution/ADR或建立空贡献。canonical Skill/原测试方法为第4节路径；spec `workflow-contract.md#candidate-applicability-and-coverage`与`quality-guidelines.md#validation-scope-ownership`继续拥有各自共享规则，必要投影只定位原owner。

没有待用户决定的产品范围问题。实施前尚需完成V648的有效before调用、真实分组覆盖和方法差额确认；这属于计划中的第一步，缺语义证据时停止受影响方法修改/验收声明。若修复评测入口需改公共API、权限边界、fresh reviewer载体或新runtime，则超出候选，返回原qualification/Architecture/Clarify，不在本项顺带实施。
