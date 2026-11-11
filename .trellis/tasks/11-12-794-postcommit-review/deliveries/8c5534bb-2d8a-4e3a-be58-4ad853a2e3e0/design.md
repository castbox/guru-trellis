# D1 提交后一次独立完整语义审查：设计

## 1. 设计目标、需求承接与内容基线

本设计完整承担本批 PRD 的 D1-R1–R7、D1-S1–S6、D1-AC1–AC6。没有前序 Delivery。development baseline B 为 `4d565c97b5abf634d76ede2d18eed0a57f13bb76`，来自原 Intake 固定并经原 Sync 确认的 main；Planning H0 与 B 相同。PR target 为 `main`。实现后的 H 由原提交 owner 的真实结果确定，不能用 H0 代替。固定 B 不因后继修复、base 推进或阶段变化而缩短。

当前 Architecture authority 为 `docs/architecture/README.md` 的 `guru-trellis-architecture`；constitution 为 `docs/architecture/00-foundation/design-constitution.md` 的 `guru-trellis-design-constitution-v1`；change contract 为 `docs/architecture/06-governance/change-contract.md` 的 `guru-trellis-architecture-change-contract-v1`。独立原 owner 的实际 candidate_assessment 已返回 architecture_impact、target_native，decision refs 为 ADR-KNOWLEDGE-FINAL-INTEGRATION、ADR-033、ADR-028、ADR-034。这一结果只支持方案写作。

选择原 `guru-review-branch` 独占提交后的合并审核。它一次完成原 Check 与 Branch Review 的全部适用语义责任。上游 Task schema2/API1 的 check 与 full_review 继续存在，由同一真实判断顺序记录；它们不是两个独立审查步骤。Planning、Delivery Review、Publication 和终态 owners 保留。

## 2. 当前系统、边界与目标差额

当前 workflow 先执行 candidate Check，原 Architecture/RDT final integration 后重新绑定候选，再执行最终 Check、TaskCommit、提交接续和 Branch Review。`guru-review-branch/runtime/invoke.py` 要求先有 check_result_id；TaskCommit 最终 profiles 也要求 Check。原早期 draft_commit 能在 implementing 下无 Check 地精确提交，但其 consumer 直接进入 early Publication。以上是当前事实，本设计不把每次运行概括为固定三次 Check。

目标链为：已激活 Planning → 实现及工程自检 → 原知识 owners 整合/readback → 原 TaskCommit 精确本地提交 → implementation 绑定固定 committed Candidate → 新独立 reviewer 的一次完整审核 → 原 Delivery Review/readiness → Publication。上游 checking/reviewing phase 仍由公开操作转换，不新增 phase 或并行质量状态。

本批修改 canonical workflow/routing、命中的原 Skills、runtime/schema/interface/consumer、RDT/Architecture 定义、受管平台入口与迁移说明。它不修改上游 Trellis、全局包、hook 或 node_modules，不合并 Delivery Review/Publication，不改变 Completion/Closure/Finish，不实施 #734 或 #736 的其他拆分项。没有服务、数据库或部署配置变更。

## 3. 来源设计处置（唯一）

下表是本批唯一规范性来源设计处置。Issue #794 全文是需求 authority；没有另外选入设计评论。旧规则的被替代范围必须在实现时从活动定义中收敛，不能只在末尾追加相反说明。

| 来源 locator/条款 | 原承诺 | 处置与具体落点 | 理由、影响与上游处置 |
| --- | --- | --- | --- |
| `.trellis/delivery-contract.md` Closed phases and owners | Task schema2/API1 固定 role、phase 与真实结果 | retain；第4–6节，同一 guru-review-branch 声明为 check/full_review owner | upstream 没有要求 owner 必须不同；不改其源码或协议 |
| 同合同 Candidate/gates/result recovery | 完整 Candidate、Planning→check→full_review→readiness predecessor、原结果恢复 | retain；第5–7节顺序真实投影及同候选恢复 | 不能从空白 pass、历史提交或远端事实合成新判断 |
| 原 `guru-check-task` 的 Phase2 九维与规划/scope 回程 | 完整当前范围检查、有效验证、docs/consumer/兼容覆盖和原 rollback | change；第4节完整迁入原 Review，第6–7节保留原因/范围回程 | 退休独立重复 Check；#775 已清 Planning 的原恢复仍准确承接 |
| 原 `guru-review-branch` 固定区间、独立性、findings/continuity | 新独立 reviewer、完整 B..H、后继覆盖、Task/base 归属 | retain 并扩充；第4、6、7节 | 不以 caller 传入路径缩区间；保留 ADR-028/034 |
| 原 TaskCommit 最终 Check 前置、early draft_commit 与 committed_reentry | 精确路径提交、hook、干净重入、同提交恢复；早期结果交 Publication | change；第5节新增版本化 pre-review profiles，保留 executor，改交固定审核 | 删除旧 Check 前置和审核前发布边；不静默复用旧 Draft 语义 |
| ADR-KNOWLEDGE-FINAL-INTEGRATION、Architecture change contract 的 final integration | 独立候选 Architecture/Check 后晋升，再最终 Check 与 committed Review | change；第4、6节，原维护方提交前整合，独立 before/after 移入提交后同次审核 | 新 ADR 窄替代该时机，保留 single-writer、expected-current、readback、before authority 与准确完成语义 |
| ADR-033 及 R636/D636/T636 | 完整 Check 前本地提交和 Draft 反馈；已执行动作可恢复 | change；第7节 MIGRATION-794 退出新早期远端动作，保留原事务事实与结果恢复 | 不撤销既有 PR，不重复已发生副作用；新动作先走当前审核/readiness |
| R531/R530/R600/R637/R638/R713 及对应 D/T 当前单元 | 公开身份、完整内容、知识维护、发布和合法恢复 | retain 未命中职责，change 旧 Check 依赖/消费者；第5–9节 | 各原 RDT owner 写完整有效定义；旧历史与原证据不重写 |
| knowledge-maintenance 的 R710/D710/T710、R711/D711/T711 | AI只写真实语义、原recorder生成客观身份、完整结果合法消费/恢复；完整知识单元和局部导航单写 | retain 有效职责，change 重复Check profiles及时机；第4–7节、implement第6节 | 新Review承接正常语义authoring和原完整结果消费；退出重复阶段不退出准确恢复。原维护方整合完整当前定义，不追加共享登记或重写历史专项观察 |
| AGENTS.md 第2、3、6、9、10节；官方 custom-workflow/marketplace 文档 | Markdown 判断、脚本事实、官方扩展、定向验证与副作用控制 | retain；全部章节与 implement 步骤 | 不新增脚本 planner/reviewer、授权字段、账本或完整 Release 矩阵 |

## 4. 模块、职责与设计取舍

### 4.1 原 Review owner 的完整责任

`trellis/skills/guru-team/packages/guru-review-branch/` 的 SKILL、references、interface、commands、schemas、examples 与 runtime 成套修改。首次执行者必须新开、未参与实现，先完整读取固定 B 的 baseline/constitution/change contract，再读 H 与全部影响消费者；最后读取 Task 叙述、验收和贡献解释归属。不能先看实现者的 pass 叙述。保持原 Architecture 的 authority-first 与独立 project-check 方法，由同一 reviewer 在本次先完成一次实现后 Architecture 判断，再完成全部当前审核。Planning Architecture 不被这次取代。

合并审核明确覆盖九维：requirements、design、implementation、tests、docs_ssot、cross_layer、compatibility、deployment_and_operations、verification_completeness。每维从当前完整范围判断适用性和充分性。还承接原 Branch Review 的完整固定区间、P0–P3 findings、必要读取、原消费者追踪、减法优先、维护性、删除/替换/合并、实际发布影响及后继覆盖。没有独立 Check mandatory invocation，没有以九个 true 或命令绿色代替实际审查。

工程事实先按定义/版本、输入/依赖、环境/工具链/参数/期望判断。适用则采用；新增、失效或未覆盖才补验证。后继同一 reviewer 必须仍独立；读取合法原覆盖、Hr..Hi 全部差额、冲突双方/组合语义及受影响未改 consumers，明确保留、失效和补审。覆盖缺失或影响无法界定时完成对应完整审核。阶段或 HEAD 变化本身不要求重跑同一实验。

### 4.2 提交与公开结果

`guru-create-task-commit` 复用原 exact executor、hook、路径隔离、提交前检查和同提交输出恢复。提交语义 gate 判断的是当前计划、自检、整合状态及具体提交内容是否适合形成待审候选，不能声明实现质量已经独立通过。新 pre-review profiles 无 Check pass 输入；删除其通向 early Publication 的直接边。提交后由原 implementation constructor 产生完整 B/H/paths/content_ref，再用原 begin_check 进入 checking。metadata exclusions 保持，Task/session 文件不当作业务 Candidate。

workflow runtime declaration 将 `owners.check`、`owners.full_review` 同时指向 `guru-review-branch`。原 Review 记录器保存一次实际判断所需的最小不可重推结论到原短生命周期 private review gate，运行时只核固定 Candidate、required fields、predecessor 和公共 owner。语义失败不记录通过结果。语义通过后先 record check（predecessor=planning），再 record full_review（predecessor=该 check）。只有两个真实投影都完成才输出 passed。删除独立 phase2 checkpoint、重复结论和无 consumer 的历史 bundle；不新增公共 coverage DTO 或授权信息。

### 4.3 原知识 owners

`guru-maintain-requirements-design-test-ssot` 与 `guru-maintain-architecture-baseline` 保留唯一写入、隔离完整拟写、真实 target 重读、expected-current、普通部分写入恢复和实际 readback。新提交前 integration profile 依据已批准 Planning、完整实现及真实工程结果开展必要整合；不要求尚未发生的独立候选 Check/Architecture pass。整合结果只能表示文档已写入、待提交后独立审查，不能标成 reviewed_promoted。

Architecture 新版非 Planning 合同必须区分整合事实和真正审核状态：提交前用 `integrated_pending_review` 表示适用 target 已整合；独立 committed before/after 成功后才返回 `reviewed_promoted`。这是原 promotion_state 的明确版本扩展，仅被原提交前 integration、Review 和 readiness 消费，不建立第二状态存储。public 输出仅保留下步所需 key/authority 或 candidate identity；实际 targets、写入 intent 与恢复属于原 owner-private 状态。无影响仍走 no_change，不造贡献。

必要 docs 在同一个本地实现提交中完成。若独立审查发现当前定义缺陷，由原维护方修正并形成后继提交，重新审受影响范围；不能在冻结 H 审查期间直接改正文。RDT 不负责 Architecture 正文，Architecture 不负责 RDT 三层 authority。

### 4.4 取舍

直接演进原 Review、TaskCommit 和维护 owners，退休重复流程。另建质量 Skill 会增加 owner、接口与迁移责任，当前没有独立 consumer，故不采用。改上游 phase/schema 会扩大依赖且无需求依据；也不采用。双公共结果是现有 API 必需事实，不能删槽，也不能以自动复制 pass 应付。早期 Draft 不保留第二个发布选项；仅保留第7节受支持在途处置。

## 5. 接口与数据

所有版本切换由 `trellis/presets/guru-team/MIGRATION-794.md`、原 interface 选中版本、workflow/routing 与安装资产一起交付。旧 schemas 保留为 pinned validation assets，不由当前 runtime 自动回退。以下名称是本批拟实施公共合同，尚未发布。

| 生产者/输入变化 | 新版本与字段边界 | 唯一直接 consumer |
| --- | --- | --- |
| TaskCommit 新 `delivery_pre_review_commit`、`delivery_pre_review_committed_reentry`；相同 profiles 内按原精确内容/输出恢复 | Delivery input aggregate 3.0；沿用原身份、message、exact selected paths/clean HEAD 所需字段，去除 check_result_id；新 `pre_review_committed` output1.0 只交 task_ref/delivery_key/commit | 原 workflow 待审提交 router；调用 constructor/begin_check 后投影 Review input；不交 Publication |
| Review `delivery_branch_review` | input2.0，aggregate Delivery4.0；保留 mode/task_ref/delivery_key/base_ref/branch_review_commit/review_intent，删除先验 check_result_id | 原 Review 自身完成两组语义判断，非独立 Check |
| Review continuity 与 promotion alignment | 各 input2.0，同 aggregate；去除旧 Check producer 前置，使用原固定 Candidate、真实旧覆盖与 Reconcile 结果 | 原 Review；alignment 只在原窄事实条件成立时适用，不能绕过新语义职责 |
| Review passed | output2.0；形状保持 exit_id/task_ref/delivery_key/branch_review_commit/full_review_result_id | 原 Delivery Review input/projection 升级到该语义版本；不跨读 private gate |
| Review implementation_required / scope_confirmation_required / scope_revision / stopped | 命中语义改变的 output/consumer 升级2.0；沿用最小实际 finding_refs、scope/revision_refs，不带 reviewer 历史或授权 | 原 implementation/Clarify/Author/Completion 唯一路由；范围由原 owner 判定 |
| Architecture 提交前 integration 与 committed review | 非 Planning6.0 / Delivery4.0；移除 candidate Check/phase2 独立评估前置，新增 integrated_pending_review；保留 before_authority、完整 candidate 与 committed_range | 原 TaskCommit 准入；新 Review；原 readiness 只接受 no_change 或 reviewed_promoted |
| RDT integration | input/output3.0；以完整实现/工程与 target intent 接入，移除 candidate_ready 的旧 Check 前置 | 原 integration router → TaskCommit；必要 readback 不丢失 |
| Reconcile resolved/full-review projection | 命中的 input/output/consumer 升级；`phase2_commit_anchor` 改为其真实语义 `committed_candidate_anchor`，仅原同候选恢复使用 | 原 Review input2.0，固定 B 与完整冲突/集成范围；不生成 check pass |
| early Draft、旧 Check gate 和回退 | 当前接口退出；MIGRATION-794 明示旧 provider 版本/commit 与原命令定位 | 原 Commit/Publication/Review migration owner；第7节逐状态处理 |

其余 unchanged 输入/出口保留原精确 schema。实施先列当前 interface 的每个实际 consumer 并验证 projection；若字段或版本名已被 live source 占用，回 Author 修订具体命名，不静默复用。没有新的顶层 Task 字段、public phase、账本或通用 wrapper。

上游公开 operation 为 `record_gate`，仍使用 Candidate、scope_ref、plan_ref、evidence 与 obligations 原 shape；CLI 运输命令 `record-result` 保持原名。原 Review 必须分别填写真实 Check 充分性和 full_review 覆盖结论；两个槽的 outcome 不由 recorder 推导。旧结果不能只替换 owner_id 后当新 pass。原 Delivery Review 记录 readiness，Publication 消费其 ready/readiness；Merge、Completion、Finish 保留真实结果读取及适用性判断，同步命中的 Check producer/知识状态引用。

## 6. 状态、顺序、正常与失败流程

1. Planning 批准并由原 Activation 激活后处于 implementing。实现者完成代码、必要完整知识拟写和选定工程验证，原维护方整合/readback。未整合、冲突或输入已失效时留原维护 owner，不能提交成已独立通过。
2. TaskCommit 对确切待审文件完成 semantic gate，在原副作用边界形成本地 H。干净已提交候选走新 committed_reentry，只核实际 Git，不 stage 或重复 commit。
3. 原 constructor 复用本 Delivery 的 B，加入全部 B..H 与实际 dirty increment（正常新链此时没有业务 dirty），产生真实 Candidate。begin_check 将 implementing→checking。若构造失败，修复事实后从原 owner 重试，不能手填 content_ref。
4. 新独立 reviewer 冻结 B/H，完成 authority-first Architecture 与第4.1节全部审查。工程验证未覆盖的具体缺口由 reviewer 执行或退原实现者补齐；需要改文件时结束本候选审核，回原 owner 修复及提交。
5. 通过时顺序写 check（checking→reviewing）与 full_review（保持 reviewing），再返回 passed。普通 schema、HEAD、predecessor 或写入错误不得输出 passed，保留原 owner 的同候选恢复。没有独立 Check transition consumer。
6. 实现缺陷使用原 implementation_required→implementation rework，清失效 check/full_review/readiness，保留合法 Planning、固定 B 和原覆盖；修复、整合、自检、提交后重新绑定 H。实际 Planning 变化走承接原 planning_stale/reapprove_plan 语义的合并 Review 回程，再进入最早受影响 Author/Wording/Architecture/Approval。若发现来源或scope真实变化，先由原Clarify处理。不以新 Finding 自动扩 scope。
7. 完整 full_review 通过后，原 `guru-review-task-delivery` 检查本批政策、真实交付、知识状态及发布充分性，完成并记录 readiness，返回 ready。原 `guru-publish-task-delivery` 只消费该当前 ready/readiness，再执行已审发布内容。未有当前 full_review、缺 readiness 或仅 integrated_pending_review 均不得进入远端动作。merge 与 Task 终态仍沿原 owner。

原 Reconcile 在真实 base 变化时判断适用 target、Task/base 归属、冲突与集成影响，固定 B 和完整新候选不变。无关已审 base 内容可采用；有冲突或消费者影响时补审真实组合。caller 不传自选窄区间冒充 full review，也不把 Reconcile 结果当 check/full_review pass。

## 7. 恢复、兼容、迁移与集成

完整旧 provider 固定为当前前驱 Git `4d565c97b5abf634d76ede2d18eed0a57f13bb76`。迁移前读取其完整合同/命令；新 runtime 不导入旧模块作为 fallback。原 tools/upgrade owner 先确认当前 Task/Delivery phase、实际 gate 与未完成事务，再选择同操作恢复或 matching 成套切换。范围、固定 B、C4/C5、scope、Task/session、实际 PR 与外部事实全部保留。

| 实际在途边界 | 原 owner 的动作与退出 |
| --- | --- |
| 仅 Planning/implementing，尚无远端动作 | 原安装 owner 成套切换；按新链完成工程/整合/提交/首次独立审核；不转换旧 pass |
| 旧 check 已存在、旧 full_review 缺失或过期 | 原阶段 owner 合法 rework 清失效结果，以同 Delivery/B 进入新 committed review；原工程与覆盖只经 AI 适用性判断采用 |
| 旧 full_review/readiness 仍适用 | 不把它改名为新版 pass；固定旧完整 provider 完成其已承诺后续，或原 owner 判断后合法 rework 到新链；需要新的远端动作时须当前独立审核/readiness，不能从旧版本号推定完成 |
| 本地 commit 已发生但 stdout 丢失 | 原 TaskCommit 按 parent/HEAD/exact paths 与原事务事实恢复同 commit；已提交干净树不 stage、不再 commit，结果交新固定审核 |
| 新 check 已记录、full_review 未完成或输出丢失 | 原 Review 核同 key/B/H/Candidate 与真实 check 及仍可用语义结果，只补缺步或恢复相同已记录结果；丢失必要语义覆盖则重新实际审查。不能无 Review 结论补 full_review |
| 旧 Draft 事务已有 ensure_draft/push/bind/metadata 事实 | 旧原 Publication owner 只恢复已执行动作的准确结果，保留现有 Draft/PR/remote HEAD；不重复外部动作、不把 Draft 当最终 publication/pass |
| 旧 Draft 事务尚有未执行远端动作 | MIGRATION-794 使该动作停止在原迁移 owner；清楚报告已完成与 pending，接回当前独立审核与 readiness 后由同 PR/原事务 owner 接续，禁止先 push 再补审 |
| #775 等 Planning rollback 已执行、handoff 丢失 | 保留原清空结果、cause/revision_refs 与先前 scope disposition，由原 producer 恢复准确 handoff；不重复 rework、恢复旧 Planning pass 或另建 Delivery |

`guru-check-task` 当前开发 profiles/出口和 candidate_checked router 从活动图退出。独立历史/legacy 控制维护职责按其原明确入口保留；原旧 Task provider 用完整 --root 定位恢复，不从当前 normal graph 借道。旧 draft_content_review、其 Publication consumer 及 promotion alignment 对独立 Check 的循环全部退出或按新版窄事实迁移。MIGRATION-794 必须列实际退休 profiles、schema IDs、commands、private checkpoints 和唯一新 consumer，不能仅写“更新后继续”。

本批自举采用也由原 upgrade owner 处理：已有本 Task/其他 Task 的旧状态先按迁移矩阵处置，不能 reapply 后假定所有旧 gate 已适用。canonical 变更先完成，dogfood 与平台投影通过匹配的 tools owner 同步；保留 journal、其他 Task、用户内容和 sidecar。不得手工覆盖生成副本或因 apply 遇旧 Task 阻塞而扩成历史迁移。

## 8. 验证设计

下表的断言来自条件→动作→结果；不是通过数、字符串快照或 fixtures 自证。长期回归优先复用现有真实 runtime tests，改变 producer 时从其真实入口产出，不在消费者 fixture 中补造新 gate。纯 reader 单测可预置边界外的有效记录，但不得声称覆盖 producer。

| ID / 对应验收 | 层、入口和输入 | 独立预期观察与证据限制 |
| --- | --- | --- |
| V1 / AC1、AC5 | package/runtime；原 TaskCommit 新公开 profiles、constructor/begin_check、Review invoke、上游 public record API；正常无 Check 的已激活实现、必要整合、确切 commit | 无先验 Check 也能提交并进入固定 H；真实一次 Review 顺序产生两槽且 full_review predecessor 正确；不依靠手工注入 check 才到达入口。脚本只证明状态/投影，不能证明 AI 审查已做 |
| V2 / AC2、AC5 | 原 Delivery Review/Publication runtime；正常未审、只完成第一槽、当前全审、HEAD 改变与 integrated_pending_review | 未审、只第一槽、HEAD改变后旧结果或pending-review输入不执行push/PR。当前全审且其余前置满足的候选仍由Delivery Review记录readiness，再由Publication消费并执行。mock只隔离远端执行，观察调用是否发生，不能声称真实GitHub已验证 |
| V3 / AC3 | 现有 Review candidate reuse、Reconcile joint resolved flow；正常修复后继、合法 base 前进/冲突及覆盖丢失 | 固定 B/full range 保持；真实原覆盖被采用、受影响消费者与组合语义补审，无法界定时补足完整范围。AI 覆盖判断另由 V6 验证 |
| V4 / AC4 | 原 Commit/Review/Publication migration tests；真实 executor/recorder 产出的提交、check写完/full_review未完、旧Draft已执行或pending、Planning rollback后输出丢失 | 同 Task/key/commit/PR 恢复，不重复 commit/push/PR/rollback；pending 远端动作必须先新审核/readiness；旧 pass 不机械转换；不靠恶意篡改状态构造用例 |
| V5 / AC1、AC5 | 原 Architecture/RDT promotion tests；新版提交前 integration 与 committed before/after，正常 expected-current 差额、读回和修复 | 无 candidate Check 循环；整合仅 pending review，独立审后才 reviewed_promoted；before 精确 Git authority 和真实 after 全纳入 H；普通冲突回原 owner |
| V6 / AC1、AC3、AC5 | 真实 AI 行为定向执行；以新公开入口和小型 throwaway 的真实提交对象，首次新 reviewer、同 reviewer 后继及一次真实 consumer 缺口 | 实际遵守 authority-first、九维、独立性、完整范围、有效工程采用和差额/影响审查；缺陷能形成具体 finding；不编辑冻结候选。调用日志/原stdout与当前说明为证据，不新增通用评测框架或固定轮数 |
| V7 / AC5、AC6 | 现有 package interface/graph/eval、source+installed discovery、Codex/Claude及实际命中Cursor投影、tools reapply/sidecar和dogfood drift | 新出口唯一 consumer、旧 mandatory Check/早期发布边退出；matching安装保留Task/session/用户正文；验证实际路由，不只比声明文本。受影响安装定向足够时不加完整矩阵 |

先做受影响行为/runtime，再做合同图与投影、真实 AI 和安装消费。语义路径可先实现再补回归，也可对清晰低成本状态断言先写测试；不强制红绿/回退重复。设施失败先判断是否到达目标行为；反复未达时修复设施、换同问题的直接观察或保留明确缺口。只有具体未决问题才追加实验。必要验收和受影响回归证据充分后停止。没有生产效果、所有外部项目采用或完整多平台 Release 结论。

## 9. Canonical 引用、本轮差额与实际未决项

RDT canonical 为 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`，以及 `current/knowledge-maintenance.md` 中真实命中的晋升定义。原 RDT writer 要完整整合 R531/530/600/636/637/638/713 的当前语义及 R794/D794/T794，保留未被替代条件，不保留相反活动规则。实施前由原 owner 确定完整目标集合并读取正文。

Architecture 的真实 task-owned contribution 为同 planning_root 的 `architecture-contribution.md`，必要 ADR 候选为 `adr-postcommit-independent-review.md`。后者拟晋升为 `docs/architecture/adr/postcommit-independent-review.md`。贡献承接真实 DOMAIN/GOVERNANCE 单元、change contract、根入口自身维护时机合同和实际引用；Planning 不直接写共享 current。ADR 只窄替代本次门禁/时机决定，保留 ADR-028/034 及其余责任。

canonical workflow 为 `trellis/workflows/guru-team/workflow.md` 与 `references/routing.md`；公共 packages 在 `trellis/skills/guru-team/packages/`，共同确定性投影在 `trellis/skills/guru-team/runtime/delivery_projection/`；spec 在 `trellis/presets/guru-team/spec/workflow/`。同步 README、interface inventory、commands、schemas、examples、evals 和实际命中平台 overlays。狗食 `.trellis/`、`.agents/`、`.codex/`、`.claude/` 等只由原安装 owner 生成。

没有阻塞方案写作的产品选择。尚待实施与验证的义务为 V1–V7、真实公共版本/退休清单、完整拟晋升目标及 matching 采用；这些不是已完成事实。若上游公共 owner 或 API 实际不支持本设计，停止依赖工作并回 Author/Architecture，不用空 pass 绕过。本轮只交规划，不激活或实现。
