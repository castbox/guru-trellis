# D1：v0.7.0-guru.9 完整来源准备设计

## 1. 设计目标、需求承接与内容基线

本方案承接[本批需求](prd.md)的 D1-R-01～05、D1-SC-01～07，以及已选 AC-01、AC-02、AC-03、AC-05、AC-06。Task 为 808-release-v070-guru9 / generation 0，Delivery 为 b40421e8-6213-4f29-bb11-8d3919e533b0。公共范围取[整体 PRD](../../prd.md)第3.3、5.4、5.5、7节及当前 scope_ref；本批不改变 accepted scope。

本批交付完整可分发的 .9 来源、直接版本消费者、私有编排/真实回归和必要文档。实际 eafc dogfood/source_locked 与 AC-04 留给同 Task 后继 D2。D1 自身来源、接口、依赖、安装/投影可用性及必需验证必须完整成立，不能在 D2 修复后再回称 D1 完整。

开发内容基线 B 保持 5c6a4591db7165ece045e6b0eb789c21d06d7d38，来源是 D1 开始时一致的 HEAD、local main、origin/main；本 Task 没有前序 delivered head。Planning H0 为同一提交的起点观察，PR 目标为 main。B 不随 fetch 改变；未来 H 和完整 B..H 由原 constructor 确定，不手填 Candidate/content_ref。

阶段 authority 为 [Architecture](../../../../../docs/architecture/README.md) guru-trellis-architecture、[constitution](../../../../../docs/architecture/00-foundation/design-constitution.md) guru-trellis-design-constitution-v1，以及 [change-contract](../../../../../docs/architecture/06-governance/change-contract.md)。本次新独立 candidate_assessment 实际返回 baseline_current / architecture_impact / target_native，要求在原完整单元维护 ARCH-DOM-010、ARCH-INT-015 的私有发布与来源→实际采用关系，遵从 ARCH-GOV-008/009。真实隔离贡献见第4.4节；不新增 ADR、公共协议或 writer。该结果不替代 Wording-current final_plan、Approval 或实现验证。

本次明确整合目标为 main 的固定提交 29d0c3795ac45f9fc03fbea46c331307cce10b2b，PR 目标仍为 main，内容 B 不变。该来源的 Fork lock 为 e3793251fad8bd261d0c370d408c7675b9f6a140 / CLI .6；原 B 的 aa898d09 构建不证明该来源可用。完成当前规划后，由原 Reconcile 在 delivery_post_plan 边界构造和检查精确基线候选、创建仅含基线整合的本地 merge，再返回同 D1 Activation。保留原 dirty 及其 staged/unstaged/untracked 状态；实际内容修订及其验证不由基线 gate 代替。

## 2. 当前系统、边界与目标差额

| 对象与起点 | D1 的实际差额 | 保持或后继边界 |
| --- | --- | --- |
| canonical extension 仍为 .8 | manifest version、当前安装目标常量、三份输出/consumer schema 及 active output example 成套改为 .9 | CLI/Core 0.7.0-castbox.6、所选 main 自身 Fork lock、公共 shape、历史版本样本不改 |
| 私有 Stage 1 仍要求晋升前后固定两轮 Check/Review，并引用不存在的 early source route | 每个真实 Delivery 采用 #794 当前完整链；来源先实际 delivered，剩余采用经原 Completion/Creation 接续 | 不增加 early profile，不跳 TaskCommit→constructor/begin_check→Review，不安排失败审核 |
| 私有测试仍用旧 Task/status、Check/Review profile 和 receipt | 改用当前 schema2/API1、实际 TaskCommit/Review producer 与直接 consumer | fixture 判断只证明组件链，不能冒充实际独立 Agent 或 GitHub 成功 |
| README 仍以 .8 为 current，workflow README 另存 Fork SHA/CI 表 | 区分未发布 .9 来源准备与稳定 .8，当前 Fork 只链接 canonical lock/build recipe | 未发布不称 latest/stable；真实 .8 前驱继续用自己的 lock |
| 实际 checkout installed .8 | D1 记录来源与目标安装的真实差额，不手改受管副本 | D2 实际 source_locked 更新完整 managed/package/platform/workflow，并验证 installed/native、preservation、parity/drift |
| 已接受根范围与 D1 scope_ref 已分配来源切片 | 本批三份正文与 context 反映已选责任及 staged Policy | AC-04、AC-07/08 和完整 Stage 2 不删除，不提前建立 D2 |

当前 D1 所用 TaskCommit、constructor、Review 和公共 Delivery API 已包含 #794。本次来源版本目标变化作用于后继安装目标及其输出消费者，不要求先安装 .9 才能提交/审核 D1。若实施事实改变这一前提，回原分配/Planning；本方案不提供豁免。

## 3. 来源设计处置（唯一）

PRD 和 implement 只引用本节，不另建来源矩阵。下表为当前设计处置，不是执行结果。

| 来源/原承诺 | 处置 | 落点、理由与影响 |
| --- | --- | --- |
| 根 PRD 第3.3/7节：D1 完整来源，实际 delivered 后 D2 实际采用 | retain | 第4.3、6、8节。保同 Task/D1 身份，D2 由原 Creation 后建；本批完整验证来源自身，不以延期自身缺陷取得 pass |
| 根 PRD 第5.4：完整干净匹配 source_locked、真实目标及 preservation | retain | 第4.3/7节；实际采用归 D2。D1 本地样本不证明正式来源锁定或真实 eafc 安装 |
| MIGRATION-794 §1：提交前工程/必要知识整合，提交后一次独立完整 Review，真实 check/full_review 两槽 | retain | 第4.2、5、6节；每个 Delivery 均履行原职责，真实后继差额仍刷新受影响审核 |
| §1：TaskCommit 只形成待审本地提交；readiness 归 Delivery Review；未审不发布 | retain | 第5/6节；成功 consumer 不变，不插入 tools 或 early Publication |
| §2：公共 profiles、版本化输出与直接 consumer | retain | 当前原 Interface 单写；本次仅更新既有当前安装目标值，不改 shape，不把旧结果改成新版本 |
| §3/4：旧独立 Check、early Draft 新入口退出；合法旧操作按原完整 provider 恢复 | retain | 第4.2/7节；已执行事实恢复，pending 新动作先当前审核/readiness，不恢复退休正常路线 |
| §5：canonical/installed/platform 成套采用，保 Task/session/user/mode/sidecar | retain | D1 第8节验证来源分发，D2 完整验证实际采用；同 Task 最终仍满足全项，不把 source 或 sample 成功当整体 matching |
| 私有 release Stage 1：固定两轮晋升前后 Check/Review | change | 第4.2。按 #808 迁移私有消费者及四份发现合同，采用当前逐 Delivery 完整链，不改变公共 owners |
| 私有 release 的 existing reviewed early-commit/source-acquisition route | change | 删除失效引用，明确根 PRD 已接受的 D1 delivered→Completion additional_delivery_required→Creation→D2 tools 顺序；不只删文案而遗漏真实采用 |
| 私有 Stage 2：fresh exact candidate、原 locators、限定 historical-Task observation、tag/smoke/Release、本地收敛、最终关闭 | retain | 第6.3及根 PRD 第5.6节完整保留；D1 不执行或预填通过 |
| AGENTS §6/7、quality 的定向验证与同步义务 | retain | 第4.3/8节。D1 必需来源与完整投影验证不删；真实 checkout 采用/drift 完整留在 D2，失败不改记 pass |
| public-docs：三个 README 分工、独立版本轴、同 immutable 来源 | retain | 第4.1/8节。正式安装/Stage 2 仍需同一精确远端来源；D1 local sample 明确不证明它 |

没有拒绝来源承诺。当前采用既有 owner 分配即可表达来源依赖；若出现公共 owner/API/phase 或机制变化，回原 Clarify/Architecture，不在私有合同中自授新路线。

## 4. 模块、职责与设计取舍

### 4.1 版本与公开文档

实施 owner 修改以下六个 canonical 目标：

1. trellis/guru-team-extension.json 的 version。
2. trellis/skills/guru-team/packages/guru-upgrade-installation/runtime/owner.py 的 TARGET_GURU。
3. 同 package 的 schemas/public-upgraded-output.schema.json。
4. 同 package 的 consumers/stop/production/upgrade-installation-upgraded.schema.json。
5. trellis/skills/guru-team/consumers/stop/production/upgrade-installation-upgraded.schema.json。
6. trellis/skills/guru-team/packages/guru-upgrade-installation/examples/public-upgraded-output.json 的 active installed_version。

它们均对齐 0.7.0-guru.9；TARGET_CORE、所选来源自己的 source lock、Task schema/API、历史 schema/样本和正式 .8 Release 不改。实际 formal_guru_source、installed_version 生产者和三份直接 consumer 必须执行验证。active example 继续由原 source validator 消费，不过滤失败样本。当前 formal-source 测试的目标 fixture 应随真实 manifest 目标构造，不能全仓替换历史 .8 或仅锁版本字面。

README.md 保留稳定 .8 例与 guru-team-extension-version anchor，说明 .9 为未发布来源准备。workflow/preset README 维护各自完整受影响章节；workflow README 的第二当前 Fork SHA/CI 表改为 canonical source/trellis-source.json 和原 build recipe 的链接。不可把 local sample 文案包装为远端 .9 已可安装或已发布。

### 4.2 私有编排与真实回归

Shared .agents/skills/release-guru-trellis-version/references/contract.md 是私有源；.codex/skills、.claude/skills、.cursor/skills 的同名合同逐字同步。四份 SKILL.md 只有实际入口语义需要变化时才同步，仍只定位完整合同。私有内容不经公共 preset/overlay 分发，不加入 registry/manifest。

Stage 1 对每个实际 Delivery 只定位原当前 owner，不复制其内部 gate/schema。原工程自检与必要 RDT/Architecture 整合/readback→TaskCommit→constructor/begin_check→同次独立完整 Review→当前 publication Architecture eligibility/Delivery Review/readiness→Publication/Merge。后继内容变化按原覆盖方法重审；不是同一候选固定重复两轮。

D1 delivered 后，私有编排消费原 Completion 的实际 additional_delivery_required，原 Creation 才建立 D2。D2 规划和激活后，从真实 D1 完整干净来源加载原 tools，以 source_locked 更新真实目标；D2 自身的提交和完整质量链照常执行。所有准备业务满足后才可能 Completion completed，随后 Closure no_mutation、Finish/Cleanup；Stage 2 另行 fresh freeze。

修改 .agents/skills/release-guru-trellis-version/tests/test_contract.py：
- 将旧 Task/status、initial_commit、旧 branch_review/Check fixture 迁至当前公共 Task schema2/API1 和 Delivery。
- 可复用 canonical guru-check-task/tests/test_delivery_flow.py:DeliveryFlow 的测试前置，以及 guru-create-task-commit/tests/test_committed_reentry.py 的 prepare/invoke 方法；其所在旧 Check package 不使旧 Check 重新成为生产门禁。
- 当前 TaskCommit public prepare/invoke 必须实际产生提交；公开 constructor 和公共 begin_check 实际固定完整 B/H；原 Review record/check/invoke 实际形成两槽，再检验真实当前输出可被下游消费。不能直接写被测 producer 应生成的结果。
- fixture 提供的 Planning 状态必须在测试声明边界前合法成立；fixture semantic 判断必须显式标为 fixture。这些只证明组件协议，不证明独立 AI 的质量结论。新真实独立 Review 仍由实际原 reviewer 执行。
- 复用适用的 scope/Delivery Creation/Completion 原覆盖，补私有编排的真实来源→后继消费关系；测试中远端 executor 用明确替身，未审无调用，不能把替身当真实交付。
- 保留四份私有一致、公共分发排除、真实后继/stale、同操作输出丢失与命中的旧 Draft/双槽恢复。没有真实新差额时不重复造同类案例，不执行业务仓或真实远端发布。

### 4.3 D1 来源验证与 D2 实际采用

D1 用现有 source validator 和原安装入口检验未提交来源，不伪称 source_locked。既有 verify-throwaway-install.sh 的 focused profile 支持 TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1。Python owner verify_trellis_compatibility_matrix.py 的 _install_workflow 原 local_sample 选择 legacy native，不能满足 current preset 的 schema2 前置；改成显式 native-delivery-v1 又会按匹配 Fork 的 native policy 建立 manual bootstrap，后续 Guru workflow 下的官方 update 正常拒绝该 profile。新的候选评估已针对这个实际 consumer 差额重新判断，不能采用前次 native selector 的结论。

本批直接复用原 nonlocal 的公开 custom 初始化参数：`--workflow guru-team --workflow-source <workflow_source>`。local_sample 仍只在既有显式许可及未发布来源条件下成立，使用可达的公开 Guru marketplace 初始化，再由原 sample copy 写入当前本地 canonical workflow，并用同一本地来源 apply preset。matching Fork 将 custom workflow 视为非 bundled 所有权，不登记它的官方 template hash；bootstrap 保持原 schema2、空 deliveries。不得先产生 manual/legacy Task 再删除、停止、转换或扩大 Guru 支持来取得通过。

因此，本批临时新增的 local_workflow_template 参数、known native workflow 投影例外及其专属测试不再有 consumer，须从本批增量中完整删除。_assert_template_hashes、validate_cell 和各调用恢复原合同，不放宽未知漂移，也不手改目标文件或官方 hash。长期回归执行真实 _install_workflow，观察公开 init 参数、本地 canonical workflow 字节及原许可拒绝；完整 focused 验证实际 bootstrap、官方 update、本地 sample 预览/应用、preset reapply、session 和 installed/native 结果。sample 不调用官方 workflow --force，不作为该命令的验证证据；非 local 精确 marketplace 的官方 preview/force 路径、guard、bootstrap 和原验证模式保持。

公开 marketplace 仅提供这个 local sample 的 bootstrap；candidate workflow 和 preset 的实际内容来自当前本地来源，不声称是 immutable .9 远端安装。失败时保留原现场和结果，完整通过前不宣称来源验证成立。该机制不要求把 dirty .9 作为正式 tools 来源，不改 TaskCommit 前置。

一个 Codex focused 项目只证明 Shared/Codex 的实际路径。为覆盖本次受影响的完整 Shared/Codex/Claude/Cursor 公开 schema 及选定受管资产，在同一个临时项目上经原 apply 扩展到 claude+codex+cursor，并再次验证完整 installed/package/platform、实际源对照、mode 和无 sidecar。不是新增三个 throwaway 单元或完整矩阵。

完整源对照使用原 installer managed_source_projections 的全量当前集合：逐个比较临时目标与 canonical_bytes 的真实内容，不能抽样。原 installed validator 另校验 package inventory、平台文件集合/内容/执行位、manifest/provenance；检查所有受管入口执行权限、实际 .9 extension、CLI .6、lock、workflow 字节及实际 source provenance。动态生成的 installed manifest 以其原规则验证，不要求它预先存在于 source HEAD。测试不修补坏输出来取得成功。

D1 的来源样本、fixture 或 source validator 均不证明正式 immutable marketplace、source_locked、eafc .9 安装、实际 preservation 或整体 dogfood drift。对真实 checkout 运行的诊断保留实际旧安装及漂移，失败不记 pass。它们按已接受责任留给 D2；D1 来源自身验证失败仍阻塞 D1。若原 verifier/installer 的正常前置或 D1 自身执行要求先采用 .9，立即回原分配/Planning，不改 flag 绕过。

D2 的来源、构建、目标 preview/prepare/invoke/恢复均由原 tools owner 重新核定：真实 D1 delivered、完整干净 source HEAD、自身 Fork lock、匹配 CLI/Core/build/API、精确 checkout、全部 managed 写集及 Task/session/user/peer/pointer preservation。该实际安装不在 D1 执行，未知编辑、事务、sidecar 按原 owner 处理。

### 4.4 知识与架构

R794/D794/T794 和既有 scope allocation/Delivery stage-facts 已提供责任定义。本次实际差额在私有消费者、版本目标和公开说明；本次不为发布制造通用定义、全局版本、索引登记或“通过”段落。原 RDT owner 在实施时核实际差额；只有发现真实正文差额时，才由原 final_integration 完整写入/readback。

本次独立 candidate assessment 选择 target_native。真实贡献为 docs/architecture/contributions/808-release-v070-guru9.md；两个完整 proposed targets 位于同名目录 proposed/docs/architecture/03-domains/ownership.md 和 04-integrations/distribution.md。前者更新 ARCH-DOM-010 的原 owner 及 D1/Completion/Creation/D2 责任；后者将 ARCH-INT-015 的现行定义收敛到逐 Delivery 当前链，保留 #392 的历史来源和窄替代范围。第3节的完整 Stage2、真实采用与当前未验证边界全部承接。

Planning 只写隔离提案。实施与工程事实齐全后，原 Architecture delivery_promotion(stage=final_integration) 核 expected-current、写入两个完整共享目标并 readback，结果仅 integrated_pending_review。TaskCommit 后同一新独立 committed reviewer 审真实 before/after，只有其通过才建立 reviewed_promoted。原 baseline identity、根入口、ADR index 与 proposed ADR 状态不改；现行依据来自当前 GOV/change-contract/ownership，不把 proposed ADR 当接受凭证。真实机制扩张回原 assessment。

## 5. 接口与数据

本批无新 API、字段、数据库或业务服务。接口以当前各 package Interface 为 SSOT：

| 生产者/输入 | 实际出口/consumer | 责任 |
| --- | --- | --- |
| Author delivery_solution_planning + 本次 candidate_assessment | plan_ready→Wording→final_plan→Approval | 当前五份正文/context 必须完整，不从 candidate pass 推导完整计划批准 |
| TaskCommit 两个当前 pre_review profiles | pre_review_committed→原 router | 完整实施、工程验证及必要整合在前，无来源专用出口 |
| constructor + public begin_check | 固定完整 Candidate，implementing→checking→原 Review | B/H/paths 从真实 Git/public 模型取得，不手写 digest |
| Review delivery_branch_review | 当前 check/full_review 两槽及 passed→Delivery Review | 实际完整同次独立判断，真实后继按影响重审 |
| Delivery Review→Publication→Merge | ready→ready_for_merge→delivered | 当前中文 Refs #808 payload 和 expected head，不提前关闭 Issue |
| Completion 的剩余实施判断 | additional_delivery_required→原 Creation→新 slice Planning | 仅真实 delivered 后接续，不把未交付提交当前序 |
| D2 tools install/source_locked | tools_upgraded 或原恢复/阻塞 | 正式 source/目标采用事实，不成为 Task/Delivery 质量通过 |

本批 .9 schema 值投影保留现有 shape 和历史版本解释。完整工程数据、Gate 和 public handoff 仍按原最小 consumer 合同，不新增审查账本、授权字段或共享状态。

## 6. 状态、顺序、正常与失败流程

### 6.1 当前 D1

1. 当前 requirements_ready→新的独立 candidate_assessment→本方案及 implement/context。
2. 后续 Wording→fresh final_plan→Approval→完整计划展示/接受→原 Activation。
3. 实施版本目标、私有编排/回归和公开 docs；完成第8节来源自身验证及必要知识整合/readback。
4. 原 TaskCommit 形成完整本地 H；唯一 router 固定 B..H，原 reviewer 同次完成 Architecture before/after、九维和 full Review。
5. 真实修复回原 writer 后继提交/补审；当前 eligibility/readiness 后才 Publication/Merge。实际 Git/GitHub 副作用保持各原边界。

### 6.2 GAP-SOURCE-01 与新的接续

原单 Delivery 方案要求安装先于来源提交，而 source_locked 要求已提交 .9，且 TaskCommit 没有 early consumer。这些原失败观察保持原义；原 Author blocked 不改写为历史 pass。

当前原 Clarify 已接受同 Task 来源→采用分配，planning owner 已将同 D1 scope_ref 修订为 AC-01/02/03/05/06。本次新候选经独立 assessment。新的拟执行顺序使 D1 自身完整性不再要求先完成 D2，但来源验证、完整 Planning 和所有后续业务结果仍须实际建立。删除旧引用或修改 Policy 标签不能证明实际来源已取得。

若 D1 来源自身验证不成立，回原工程/Planning；若必须先采用 .9 才能完成 D1，回原分配/Architecture。不能将该失败移给 D2、借旧 provider 开新早期操作或计划性取得 Review finding。

### 6.3 后继与发布

D1 实际 delivered→原 Completion additional_delivery_required→原 Creation 建 D2→完整 D2 Planning/Activation→原 tools source_locked 实际采用→D2 完整提交/审核/交付。D2 读取真实前序结果和其 content base，不现在预选 UUID、source SHA 或执行选择。

全部准备业务后原 Completion 判 AC-07；Closure no_mutation，acceptance-finish Architecture/Finish 的唯一归档与 bookkeeping、Cleanup 承接 AC-08。随后 Stage 2 按根 PRD 第5.6节完整执行 fresh main lineage、唯一 candidate、真实 .8 upgrade、focused/existing、secret scanner、self-reapply及限定 historical-Task observation、tag/smoke/Release、两个选定本地目标和独立关闭。D1/D2 的通过均不能直接作 Stage 2 pass。

## 7. 恢复、兼容、迁移与集成

| 正常状态 | 原处置 |
| --- | --- |
| 旧合法 Check/已提交/Review/readiness | MIGRATION-794 的固定完整 provider 或合法同 slice rework；不转换旧 pass |
| TaskCommit 完成但输出丢失 | 同原 parent/HEAD/paths/operation 恢复，不重复 commit |
| Review check 已录、full_review 未完 | 同 key/B/H/Candidate 原 owner 补缺步；缺语义覆盖实际补审 |
| 新正文/源码/测试/整合或 base 变化 | 原 owner 判断完整差额与组合影响，刷新真实受影响 Planning/Review；保原 B 与适用证据。单纯 base advance 不重规划；本次来源入口缺陷与匹配 Fork 改变是实际修订依据 |
| 旧 Draft 已执行/pending | 原 Publication 恢复同 PR/HEAD 的已发生事实；pending 新动作先当前审核/readiness |
| 临时来源样本失败/sidecar | 保留真实失败，在原测试/安装入口诊断；不修补产物、修改断言或转成正式采用成功 |
| D2 source/事务/目标异常 | 原 tools 按其原 source pair、冻结计划与恢复边界处理；D1 不提前 prepare 或接管 |
| Publication/Merge 已成功但输出丢失 | 原 owner 核同 PR/HEAD 后恢复，不重复 push/建 PR/merge |
| scope/authority 或公共机制变化 | 原 Clarify/Architecture/Planning，不能直接改 anchors 或沿旧结果继续 |

没有业务数据迁移或生产部署变化，不造 DB/生产回滚协议。source lock、官方 template hashes、mode、用户修改和 sidecar 保持原解释；真实 eafc installed manifest/projections 留原 D2 tools writer。本地样本只是原验证临时目标，不新增长期 provider、runtime、schema 或恢复状态。

## 8. 验证设计

所有项目是未来实施后的预期，不预填通过。既有事实按输入/代码/工具/环境和实际边界判适用性；补真实缺口、证据足够支持当前阶段后，停止追加实验。

| ID→AC | 实际层次、输入与入口 | 必须观察及证明边界 |
| --- | --- | --- |
| V-01→01/03 | live #808/#794、真实 PR/归档 lineage、版本五面、README 命令/链接/anchor | .9 未发布目标与 .8 稳定事实分明，当前/前驱 Fork 各用自己的 lock，必要文档完整一致 |
| V-02→02/05 | 私有当前 public TaskCommit→constructor/begin_check→Review 两槽→readiness/Publication gate 的真实组件回归 | producer 真执行，完整 B/H/结果 predecessor 可消费；未审无远端 executor 调用，不以自己种出的 gate 自证 |
| V-03→02/05 | 命中的真实后继/stale、输出丢失、双槽缺步和合法旧 Draft/provider 恢复 | 同 identity/B/PR、无重复效果，缺口回原 owner；不增加攻击、压力、故障注入或无关历史转换 |
| V-04→02/05 | canonical source validator 消费 active .9 output example、实际 formal-source/installed_version→三 consumer；私有四份与排除分发回归 | 当前 .9 来源和直接版本消费者可运行，公共分发完整；source/schema 正常 mismatch 不能被字面一致掩盖 |
| V-05→01/03/05 | 一个临时 Codex focused local sample 的真实 init/preset/update/reapply/native-load；再在同项目原 apply 全部 claude/codex/cursor | 完整源映射逐文件 bytes、mode、workflow/CLI/lock/版本/provenance、installed/package/platform 和无冲突/sidecar；单平台 focused 不独立证明全部平台 |
| V-06→05/06 | 实际工程结果、知识 readback、TaskCommit、完整 committed Review、eligibility/readiness、Publication/Merge | 全部 D1 after 在完整实际候选中，零开放 P0～P3 后才当前中文 Refs-only 发布；不从 fixture 推导独立 Agent 或真实远端成功 |

实际 checkout installed/native/preservation、完整 source_locked 和 dogfood parity/drift 属 D2 AC-04，必须如实保留未完成状态。D1 对自身必需项的 FAIL/SKIP 不可移给 D2。D1 只做一个代表性临时项目的定向来源证明，不扩累计多平台矩阵；Stage 2 的 exact immutable candidate 门禁另行实际执行。

## 9. Canonical 引用、本轮差额与实际未决项

- 根 PRD 第3.3、5.4、5.5、7节及 D1 PRD：分配、来源自身完整性、实际采用和整体 Completion 的约束。
- docs/{requirements,design,test}/current/task-delivery-lifecycle.md 的 R794/D794/T794，以及既有 scope allocation/Delivery stage-facts：原质量链与剩余责任。原维护 owners 按实际差额判断；本次不直接写共享正文。
- 本文第1节 Architecture authorities 与本次新的 candidate_assessment：architecture_impact / target_native，真实贡献及两个完整 proposed targets 见第4.4节，无新 ADR。后续 final_plan 必须基于 Wording-current 方案和真实贡献另行判断。
- .trellis/spec/docs/public-docs.md：三个 README 的受影响完整章节、稳定/候选和 immutable 同源安装边界。
- 当前 TaskCommit/Review/Completion/Creation/tools 的原 SKILL、Interface 与 routing：逐步真实 consumer 和恢复，不复制第二公共合同。
- 原安装验证器的 focused/local-sample、managed_source_projections 与 installed validator：第4.3/8节的实际来源证明，限制不变。

当前没有未决需求选择或必须演进公共 TaskCommit/router 的方案前置。完整工程、来源样本、实际交付、D2采用及 Stage 2 均尚未执行；它们不是预填通过，也不成为本规划已完成的证据。若来源自身先采用依赖、原验证入口或正常前置不成立，停止在最早原 owner，不现场拼接新正常路径。
