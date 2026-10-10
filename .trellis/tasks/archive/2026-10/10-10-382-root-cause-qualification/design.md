# #382 根因候选资格设计

## 当前设计对象与约束来源

当前实现有 `guru-qualify-normal-scenario`、`guru-qualify-solution-mechanism` 两个 process-local owner，ten-profile caller graph 已覆盖 task-free、Intake、Planning、Phase 2、Reconcile、Branch Review、Delivery。canonical 位于 `trellis/skills/guru-team/packages/`，运行副本位于 `.trellis/guru-team/skills/packages/`。共同 causal completion SSOT 当前不存在。

真实约束读取 live `castbox/guru-trellis#382@2026-10-10-r1` 与 `#383@2026-10-10-r9`、current RDT/Architecture、`.trellis/spec/workflow/skill-package-contract.md`、`quality-guidelines.md`、`subtraction-first-compatibility.md`。本文是待审的设计对象，不是符合性证明。

## 唯一 owner 及备选

新增独立 semantic Skill `guru-qualify-root-cause`，使用现有 Interface 1.6、dispatcher 与 qualification 无写入传输模式。normal owner 只判断真实/current/supported，solution owner 只判断 authority承载，root owner 只判断目标感知的 first failure/因果/反事实/失败再分布。stage owner 保留 severity、规划充分性、当前实现审查及完成声明。

把根因认知并入 normal/solution 会把场景真实性或 authority归属与因果修复混为一体，扩大两个已发布 I/O；只在 caller 加规则会重复认知。独立 package 有独立候选输入、AI gate、validator与多出口闭环，不是单脚本 wrapper。

不改现有两资格包的 published schema含义；在当前 caller Markdown 增加新调用，沿已有 caller/profile映射注册新 owner 和独立 router。新增公共 API使用新 skill/schema ids，版本化 consumer contract；旧资格输出保持。迁移只涉及同步 caller加载新依赖，不保留旧 root authority或兼容双读。

## 目标感知语义流程

每次新/实质变化候选先经现有 normal 与 solution owners；原 caller仅把合格 refs交root owner。root owner不调用前两owner，不接受caller自报资格或复制其规则。workflow/caller控制顺序，阻止递归。

1. 读取当前 accepted scope、live行为、affected object/stage和可用运行证据，确定实际声明目标；标签/关键词不决定目标。
2. 普通 feature且无故障解决或保护机制声明时返回 not_incident_applicable。仍检查当前候选未偷偷引入故障控制机制。
3. 诊断审真实故障、有界取证/假设验证及其动作影响。根因未知分类为 diagnosis_incomplete，但返回原owner继续诊断；带副作用的修复不能借诊断名称逃过修复判断。
4. 缓解审自身效果/风险、合法消费者影响、条件、owner、期限/退出；未知根因不阻塞，明确 mitigation_only。期限和owner从实际authority读取，不编造长期字段。
5. 修复审first failure及竞争解释、机制改变的状态/算法/资源/交互、移除机制后的反事实、同输入或严格等价计划。检查 admission、failure stage、classification、final outcome分别可观察，绿色结果不能替代原路径证据。
6. gate或保护声明审对象、损害、直接owner/current authority及当前层必须阻断；合法非默认输入不能由推荐值推导拒绝范围。
7. 无合格修复、缓解或保护依据且仅隐藏/转移失败，判症状抑制。缺修复因果依据判诊断不足；区分可补证的修复假设与已证明的症状替代，不把二者折成blocked。
8. AI完成整组gate，runtime核对所选分类/出口的固定组合与consumer，返回唯一typed exit；runtime不从文本、代码或词表决定分类。

## Public I/O 与最小 handoff

新 input按现有十个真实caller profiles独立闭合schema，用oneOf仅作索引。字段限 profile/caller、当前target/continuation、candidate refs与当前authority/planning/code/test/运行证据locator；profile只携其entry真正需要的locator。不传severity、分类、pass、既往root结果、完整Git/GitHub快照或producer-private路径。

声明目标从live scope和候选实际行为读取，不要求所有任务填写first failure全表。first_failure、causal_chain、hypotheses、counterfactual、protection_claim、redistribution/evidence_gaps是按目标适用的call-local语义维度；checker只核对当前目标分支结构，不判断证据充分性。复杂认知不进入公共DTO。

每个result候选只有一个七类classification；原owner需要继续类型以避免把诊断/缓解当修复。Public output按出口独立schema；四个精确形状如下：

- classified：`exit_id, profile, continuation_id, candidate_dispositions[{candidate_ref, classification}]`。router消费profile/continuation；原owner消费ref/classification，诊断项只继续诊断，缓解项不能声明修复。
- mechanism_revision_required：`exit_id, profile, continuation_id, revision_candidates[{candidate_ref, reason}]`。原机制owner据ref和短理由定位remove/replace对象并重审，保留其它accepted scope。
- diagnosis_required：`exit_id, profile, continuation_id, diagnosis_candidates[{candidate_ref, evidence_gaps}]`。诊断入口据ref和精确待证缺口补证，暂停该root-fix候选；不传完整调查记录。
- blocked：`exit_id, reason`。当前stop consumer据短理由解释实际缺失，定位仍来自当前调用。

上述public字段只服务实际router/原owner；不传整份witness、拒绝历史、根因调查记录或派生digest。consumer_use与真实projection逐字段验证，无consumer字段删除。classified的classification enum排除symptom_suppression_rejected/blocked；diagnosis_incomplete只有当前goal为诊断才进入此出口。checker核对AI已选goal/classification组合，不从文本决定goal。

| External exit | 固定条件与最小 payload | 唯一 consumer |
| --- | --- | --- |
| classified | 每项为eligible root/protection、mitigation、ordinary feature或可继续的诊断；profile/continuation、candidate disposition。diagnosis_incomplete诊断项明确 continue_diagnosis，不给修复资格。 | `guru-root-cause-classified-router` 按profile返回原owner；原owner继续自己的阶段审查。 |
| mechanism_revision_required | 存在symptom_suppression_rejected且无真实blocked；只传需remove/replace的refs和短理由，整组重审。 | `guru-root-cause-mechanism-router` 返回该阶段原机制owner；不转scope confirmation。 |
| diagnosis_required | 存在声明root fix而diagnosis_incomplete、无blocked或待remove/replace项；只传暂停修复的refs和需补证内容。 | `guru-root-cause-diagnosis-router` 返回原阶段owner的有界诊断入口；保留合法调查/已合格缓解；补证后回root owner。 |
| blocked | 缺真实authority、入口或外部证据使当前目标无法可靠判断；未知根因本身不是诊断/缓解blocked条件。 | `root-cause-qualification-blocked`，说明具体缺失。 |

集合aggregation优先 blocked → mechanism revision → diagnosis required → classified；这只校验AI选定result之间的结构一致性，不替AI选择目标/classification。诊断任务本身的diagnosis_incomplete落classified，避免反复回一个要求先证明根因的入口。

三个router按相同固定profile返回下表；diagnosis_required把修复候选转为该原owner的有界诊断内容，原owner读缺口、暂停未经证明修复并继续现有阶段流程，不新建diagnosis Skill。实质scope改变才使用已有clarification；同scope补证自动接续。

| Profile | classified / mechanism / diagnosis 当前owner与resume |
| --- | --- |
| task_free_pre_write / task_free_evolution | guru-execute-task-free-change 当前entry；诊断不得自动取得生产写权限。 |
| requirements_scope_set | guru-clarify-requirements 当前requirements entry。 |
| change_request_candidate_set | guru-review-change-request 当前候选entry。 |
| planning_scenario_set | guru-approve-task-plan 当前Planning entry，诊断准入不要求已证明root cause。 |
| implementation_discovery | guru-phase2-implementation-coordinator 拥有判断，通过现有 guru-resume-implementation target接续。 |
| base_impact_candidate_set | guru-reconcile-task-base 当前base pair entry。 |
| phase2_candidate_set | guru-check-task 当前Check entry；诊断不足不是新增generic blocked。 |
| branch_review_candidate_set | guru-review-branch 当前完整range entry；必要诊断修改回其既有 implementation_required route。 |
| publication_candidate_set | guru-review-task-delivery 当前Delivery entry；当前owner按证据和修改性质使用既有 planning_revision_required / implementation_required，真实scope选择使用 scope_confirmation_required，无法可靠判断使用 blocked；新router不选择完成声明。 |

原owner消费自身input contract，router只select/rename/normalize；不能重读private semantic result推导hand off。新增router是workflow target，不造另一wrapper Skill。

## 跨阶段适用性与 #383 接口

同一机制的已审结论保留在当前会话，或由本就存在且确有下一阶段consumer的owner gate保留最小目标/结论；不保存qualification stdout、locator、digest或专用缓存。当前stage AI重读accepted scope、机制、条件与证据，判断仍适用，且完成自己的stage审查。仅stage/caller变化不重跑同一资格。机制行为、适用条件、authority或关键因果证据实质变化时重新形成候选。结论丢失/事实stale时自动重读并重新资格，不能重构虚假pass。

Delivery/Completion只接收当前候选disposition与liveauthority，#382不添加完成证据模板、完成分类器或新阶段gate。#383独占共同causal completion语义；该文件出现前，本package最小接口只说明“qualification不是completion”，并沿既有阶段审查；缺文件不让全部#383成为前置。文件出现后由#383更新共同引用和阶段承接，本task不复制共同正文。

## Canonical与实现边界

新包及其contract/schema/interface/consumer maps/evals落 `trellis/skills/guru-team/packages/guru-qualify-root-cause/`。共享runtime只增加对应deterministic命令/校验并复用已有schema/profile/locator事实工具，不创建semantic classifier。新增包执行脚本选择当前dispatcher；normal path全程stdin/stdout，无输出path选项，无tracked或ignored写入。

候选接点涉及canonical workflow、前述十profile caller skills、registry/interface与current manifests、spec的skill/data/usage/quality合同、三份public README、preset分发与selected platform投影。只改current部分；immutable历史不改写。修改overlay后用canonical apply同步dogfood，再检查drift与全部sidecar。官方 marketplace/preset机制承接update，不patch upstream。

## Architecture/Docs路径与验证

Architecture由独立fresh worker以current constitution/baseline/change-contract、本文及实际consumer图判断impact/path/concerns；主caller不预填结论。任务隔离RDT contribution拥有REQ/DES/TST/CASE trace，Architecture contribution和ADR由该owner决定；shared current只通过独立审查和expected-current-bound promotion更新。

语义验证运行真实native Agent读取事实，候选上下文不给expected classification/关键词答案；期望值在native上下文外用于独立grading。deterministic tests仅证明实际wrapper/schema/aggregation/freshness/projection，不声称根因认知通过。普通合法流程覆盖unknown diagnosis、mitigation、root fix证据不足、实质变化复审、ordinary feature、stale与零residue；不增加人为篡改或攻击fixture。

一个代表性clean installed候选验证新Skill可发现/调用，current manifest update、Trellis update/preset reapply、selected-native byte identity、dogfood drift与零sidecar。业务#354/#355/#357只读素材按目标回放；原生业务repo接续须具备实际环境及权限，缺失明确unverified。完整Release矩阵不在此task。
