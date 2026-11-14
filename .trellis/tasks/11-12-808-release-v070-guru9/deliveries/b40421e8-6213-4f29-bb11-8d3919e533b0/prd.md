# D1：v0.7.0-guru.9 完整来源准备需求

## 1. 整体来源与术语

本批属于 Task `808-release-v070-guru9` / generation `0`，Delivery 为 `b40421e8-6213-4f29-bb11-8d3919e533b0`，profile 为 `pull_request`。公共 `accepted_scope` 指向[整体 PRD](../../prd.md)，revision 为 `sha256:835586c0c5ca6a22a50a872ce8249a2548dfac4d6f84a4321f78f4d06addb950`。本批 `scope_ref` 选择其 AC-01、AC-02、AC-03、AC-05、AC-06；实际 `planning_root` 为 `deliveries/b40421e8-6213-4f29-bb11-8d3919e533b0`。

| 来源 | 章节或条款 | 角色与本批用途 |
| --- | --- | --- |
| [#808](https://github.com/castbox/guru-trellis/issues/808) | 背景与目标；前置与准备范围 | Direct Source 要求：六项发布输入、#794 前置、准备业务及 reference_only |
| [#808](https://github.com/castbox/guru-trellis/issues/808) | 冻结候选与验收；正式发布与本地收尾；完成条件与范围边界 | 要求：保留 Stage 2 全部责任、失败停止、非目标及独立副作用边界，不纳入本批交付承诺 |
| [整体 PRD](../../prd.md) | 第3.3、5.4、5.5、7节；R-01～R-06 与 C-01～C-08 | 已接受的分配：本批完整来源；实际采用 AC-04 保留同 Task 后继 D2；AC-05/06 逐 Delivery 履行，AC-07/08 与 Stage 2 全部保留 |
| [MIGRATION-794](../../../../../trellis/presets/guru-team/MIGRATION-794.md) | 第1～5节 | 约定设计：原 owners、新正常链、版本化接口、旧入口退出及逐状态恢复，后续由本批 design 第3节唯一处置 |
| [私有发布合同](../../../../../.agents/skills/release-guru-trellis-version/references/contract.md) | Ownership、Two-Stage Lifecycle、Stage 2、Local Installation Convergence、Forbidden Persistence、Independent Mutation Confirmations | 现有消费者约束：迁移 Stage 1 的旧重复门禁；保持私有边界、Stage 2 及各原副作用责任 |
| [当前 workflow](../../../../../.trellis/workflow.md) | Phase 1～3、Workspace and task boundary | 当前执行约束：唯一 Author、Planning 两次 Architecture、原提交与独立审核、readiness 和终态 |
| [公开文档规范](../../../../../.trellis/spec/docs/public-docs.md) | Document Responsibilities；Version and Evidence Sources | 文档约束：三个 README 分工、版本轴、同源安装及证据层次 |
| [验证规范](../../../../../.trellis/spec/workflow/quality-guidelines.md) | Test And Validation Value；Validation Scope Ownership | 验证约束：行为断言、实际入口、证据适用性及最小可靠集合 |
| [仓库指令](../../../../../AGENTS.md)；[原 Clarify](../../../../../.trellis/guru-team/skills/packages/guru-clarify-requirements/references/contract.md)；[原 Delivery Review](../../../../../.trellis/guru-team/skills/packages/guru-review-task-delivery/references/contract.md) | AGENTS 第6/7节；Delivery scope revision；Stage facts in this slice and payload | 分配及验证约束：本 Task 完整履行同步和漂移验证；来源交付、受管投影和实际采用分别取证，D1 自身必需验证不可推迟 |

原 Clarify 的 `source_selection` 和 `revision_refs` 保持原样。表中的执行与知识引用用于承接既有合同，不重新选择整体范围。首次 D1 没有本 Task 的前序 Delivery。

本文沿用整体 PRD 的 Stage 1、Stage 2、Task Completion、candidate 和真实 dogfood 定义。**本批待审提交**是准备内容的本地候选；**发布 candidate**是 Stage 1 终态合并后另行冻结的对象。两者不互相替代。

## 2. 整体与本批目标、非目标

#808 的整体目标是在 #794 正常完成后发布正式 `.9`，再收敛选定本地目标并正确关闭发布 Issue。本批独立目标是交付完整可分发的 `.9` canonical 来源、版本直接消费者、公开文档、私有发布消费者及必要知识正文，经本批完整验证、原审核/readiness 后合入 `main`，为后继实际采用提供真实 delivered 来源。

本批覆盖整体 R-01～R-03、R-04 中来源自身完整性与验证，以及 R-05 中本 slice 的提交、审核、PR 与 Merge 行为，对应已选 AC-01/02/03/05/06。整体 AC-04 的真实 dogfood/source_locked、受管采用与 parity/drift 验收完整保留给同 Task 后继 D2。本批不能依赖先完成 D2 才满足自己的来源、接口、依赖、安装可用性或必需验证。

六项输入保持唯一：repository `castbox/guru-trellis`；release Issue `#808`；tag `v0.7.0-guru.9`；extension `0.7.0-guru.9`；CLI/Core `0.7.0-castbox.6`；predecessor `v0.7.0-guru.8`。Fork 来源从实际 canonical lock 读取，不因 Guru 发版提升 CLI。

本批不执行本 Task checkout 的 `.9` 实际工具采用，不提前创建 D2，不执行整体 AC-07 的 Completion、AC-08 的 Closure/Finish/Cleanup，也不承诺 Stage 2 的冻结 candidate、发布门禁、tag、smoke、Release、发布后两个选定本地目标收敛或最终 Issue 关闭。这些义务完整保留，不能因本批 Refs-only PR 合并而宣布完成。

整体非目标继续有效：不以 #736 整体完成为前置，不实现其他开放 Issue，不修改上游、全局包或 node_modules，不升级业务仓库、不部署生产、不清理无关资源，不扩大为累计完整多平台矩阵。不得新增公共发布 Skill、流程 authority、schema、checkpoint 体系、状态提交或发布 ledger。

## 3. 本批起点、前序结果、依赖与剩余责任

### 3.1 已核实的准备起点

- #794 是外部硬前置，不是本 Task 的前序 Delivery。其 Issue 为 CLOSED/COMPLETED；业务 PR [#809](https://github.com/castbox/guru-trellis/pull/809) 与 bookkeeping PR [#810](https://github.com/castbox/guru-trellis/pull/810) 已进入本批起点 lineage，唯一[终态归档](../../../../tasks/archive/2026-11/11-12-794-postcommit-review)可定位。执行准备业务前仍须 fresh-read 其适用事实，归档存在不能独立证明本批通过。
- canonical `trellis/guru-team-extension.json` 和实际 installed manifest 的 extension 目前均为 `.8`；`.trellis/.version` 为 CLI `.6`。源码已包含 #794 新链，但私有发布合同仍要求晋升前后固定两轮 Check/Review，其测试也保护该旧顺序。
- 私有测试的 `record_branch_review` 仍使用旧 `branch_review` 输入及旧 gate 消费方式；迁移必须针对真实当前 producer/consumer，不只替换两轮审核的文字。
- 当前安装 provenance 不能证明目标 `.9` 已采用。相同 CLI 版本也不能证明当前与真实 `.8` 前驱使用相同 Fork commit；各自 lock/manifest 仍须独立读取。

原来源验证还暴露两处本批必须修复的遗漏：active `public-upgraded-output.json` 仍输出 `.8`，与本批 `.9` 当前消费者不符；local sample 仍显式选择 legacy `native`，其 bootstrap Task 被当前 preset 的正常 schema2 前置阻止。两处均属于 D1 来源自身的完整性，不转给 D2。演进 main 已更新 canonical Fork lock，CLI 仍为 `.6`；后续来源验证须使用该精确来源的匹配构建，旧 build 结果不能直接采用。具体机制和落点由新的 candidate assessment 与 design 承接。

### 3.2 输入、依赖与输出

输入为已接受整体 PRD、本批 scope_ref、当前 #808/#794、原 owners 的完整匹配 provider、canonical lock 与匹配 CLI/Core 验证环境。本批沿用已经绑定的 branch/worktree；当前没有前序 Delivery，不把未提交的 `.9` 或未来 SHA 当作已经交付的来源。

原 Author 在本需求阶段提供实际 candidate facts 给独立 Architecture `candidate_assessment`，不提前写实质方案。后续原 Author 才形成 design 的唯一来源设计处置，以及 implement 的唯一 Delivery Policy、Docs SSOT Plan、步骤和验证。必要共享正文由原 RDT/Architecture owners 在合法边界整合/readback，不能由 PRD 作者直接晋升。

业务输出是被完整提交、独立审核、通过 readiness 并实际合入 main 的完整 `.9` 来源及其真实验证结果。来源提交由原 TaskCommit 在本 slice 完整实施、所选工程验证及必要整合/readback 后产生，成功仍只进入原 constructor/begin_check/Review；不增加 early source profile 或插入 tools。

本批 delivered 后，原 Completion 对剩余实际采用使用 `additional_delivery_required`，其唯一 consumer 进入原 Creation 和新 slice Planning。D2 从真实 D1 交付来源取得完整干净匹配 provider，再以原 tools 的 `source_locked` 更新本 checkout；完整受管 package/platform/workflow、installed/native、preservation、ownership、mode、sidecar、parity 和 drift 结果由 D2 实际建立。未实施采用不能被改称只待外部观察的 evidence_pending。

全部准备业务及所有 Delivery/证据满足后，原 Completion 才可满足 AC-07；Closure 必须 no_mutation；原 acceptance-finish Architecture、Finish 和 Cleanup 承接 AC-08。D1 不证明这些结果，也不重开为 D2 的执行身份。

Stage 1 业务与 bookkeeping 合并后，Stage 2 仍须 fresh main lineage、唯一 candidate gates、实际 `.8` upgrade、secret scanner、tag-pinned smoke、正式 Release、两个选定本地目标及最终 #808 关闭。完整条件见整体 PRD 第5.6节和原私有合同，本批不发布其通过结论。调用 checkout 与保留主仓的具体本机目标由原发布 owner 在当前对话 fresh-resolve，不写持久 workspace 映射。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置与动作 | 处理行为与可观察结果 |
| --- | --- | --- |
| D1-SC-01 输入核对 | 准备 owner 开始业务或发现版本/来源变化 | 读取六项输入、#794 的交付/关闭/归档、main lineage 和 tag/Release 占用。身份一致才继续；占用或实质变化回原范围 owner，不覆盖 tag、不自动换版本 |
| D1-SC-02 私有消费者迁移 | 原 Author/实施 owner 读取旧私有合同及实际测试 | 采用 #794 当前 owners、profile、typed consumer 和恢复边界；修正四份发现合同及真实调用测试。无独立重复 Check、审核前新 push/PR 或公共分发旁路 |
| D1-SC-03 文档与版本收敛 | 原实施与知识 owners 已有完整拟改内容 | 更新目标版本和实际受影响正文，区分准备目标与已发布版本；原知识 owners 提交前整合/readback。知识整合事实仍 pending review，不预填独立通过 |
| D1-SC-04 来源与投影验证 | 实施 owner 已完成 `.9` canonical 版本及直接消费者；原验证 owner 读取实际源码与完整分发集合 | 验证来源版本、formal source 行为、output→consumer、完整安装/平台投影自身可用性及私有排除分发。真实 checkout 的旧安装、公开 schema 差额和 drift 结果如实报告；不把来源或临时目标验证当实际 `.9` dogfood 采用 |
| D1-SC-05 固定候选审核 | 工程及必要整合完成，原 TaskCommit 已形成本地 committed H | 原 implementation 固定完整 B..H；新独立 reviewer 同次完成 Architecture before/after、九维与 full Review。真实修复回原 writer 后继提交，保 B 并刷新受影响覆盖 |
| D1-SC-06 准备交付 | 当前完整 Review 及 publication Architecture eligibility 已通过 | 原 Delivery Review 审本批、剩余责任、验证和中文 Refs-only payload；原 Publication 执行已审 push/PR/Ready，原 Merge 仅合独立确认的 expected head |
| D1-SC-07 普通中断/不一致 | 某原 owner 发现 stale/mismatch、失败或输出丢失 | 保同 Task/gen/key/B/原事务；核实际已发生效果后原 owner 恢复。缺必要来源或语义覆盖则真实补足，不能重复创建、重算旧结果续命或静默转换 pass |

正常顺序为需求 → 独立 candidate assessment → 方案与 Wording/final_plan/Approval → 当前展示/接受及原 Activation → 实现/工程自检 → 必要知识整合/readback → 原本地提交 → 固定 committed candidate 的独立完整 Review → 原 publication Architecture eligibility/Delivery Review/readiness → Publication/Merge。各 mapped exit 自动交其唯一 consumer；真实选择和副作用保留原边界。

## 5. 完整行为、条件与约束

### 5.1 D1-R-01 输入与版本（整体 R-01；D1-SC-01/03）

目标 extension 为 `.9`；repository tag、extension revision 和 CLI 三轴分开。canonical version 拥有目标定义，installed manifest 的 `extension.version/source` 拥有实际采用事实，`.trellis/.version` 只记录 CLI。CLI 不变时不写成 Guru revision。当前和前驱各自从真实 manifest/lock 派生匹配构建，不以字面版本一致免验来源。

marketplace 和 preset 使用同一个 immutable Guru 来源。公开入口说明未发布候选与正式稳定版本的区别；tag/Release 尚未存在时不宣称已发布。发布集合最终仍为真实 `.8` 到 Stage 2 candidate 的全部 diff，不能缩为 #793/#792/#794 列表。

### 5.2 D1-R-02 私有调用链与恢复（整体 R-02；D1-SC-02/05/07）

私有 `.agents/skills/release-guru-trellis-version/` 是编排消费者，不新增 runtime 或 public I/O。Shared、Codex、Claude、Cursor 的实际 `SKILL.md` 与 `references/contract.md` 副本必须一致；私有 Skill 仍排除在公共 registry、manifest、marketplace、preset、overlay 及业务仓安装之外。

迁移后的 Stage 1 直接调用 #794 当前链：原 RDT/Architecture 的必要完整整合/readback 在本地提交前；原 TaskCommit 只形成待审本地 H；原 Review 在固定完整 B..H 中一次承担 Architecture、Check 九维和全部 Branch Review。真实通过后按上游协议顺序记录 check/full_review 两槽，缺任一槽不能当完整成功。readiness 仍由原 Delivery Review 独占，Publication 仅消费当前通过结果。

不能重新建立独立 candidate/final Check、固定晋升前后第二轮完整审核或 early Draft 发布。后继修复、正文或安装变化仍须原 writer 提交并由合规独立 reviewer 判断全部差额、组合影响和受影响未改 consumer。采用仍适用的工程事实与可核验覆盖；缺失或无法界定影响时补足完整审核，不能用“一次”免审真实变化。

私有测试必须实际经过改变后的当前公开入口和直接消费者，验证顺序、两结果/readiness、未审不发布、普通 stale/后继刷新及命中的合法恢复；fixture、绿色命令或字面 parity 不能证明真实 Agent 独立读取。支持的旧 Check、已提交/已审对象、旧 Draft 与双槽中断按 MIGRATION-794 的逐状态原 provider 处置。已发生 commit/PR/HEAD/metadata 准确恢复；pending 新远端动作先当前独立审核/readiness，不修改历史 pass 或创建第二事务。

私有 Stage 1 的消费者修正还须表达根 PRD 已接受的来源→采用顺序：每个真实 Delivery 都完整经过当前原链，D1 delivered 后的剩余采用交原 Completion/Creation，不把当前 TaskCommit 成功出口改接 tools。测试须触达真实当前生产者与直接消费者，区分组件/fixture、实际 Agent、真实远端结果，不从测试自己写入的 gate 推导生产者成功。

### 5.3 D1-R-03 文档与知识责任（整体 R-03；D1-SC-03）

三个 README 按原职责说明版本、安装来源、升级入口和当前 workflow，不复制私有完整合同或公共 schema。兼容说明保持当前/历史支持域、原 owner、准确正常回程及未验证边界。

必要 RDT/Architecture 修改只落到实际受影响完整单元和关系。保留历史来源及观察，不为本次版本追加全局知识版本、共享索引登记或状态提交。当前知识明确采用 #794，但关联 ADR 正文仍有 proposed 身份时，不能把 proposed 当接受依据；由原 Architecture 判断适用 authority、真实维护需要及合法后续，需求作者不直接改写其状态。

本批有规范性来源设计。其逐项 retain/change/reject、具体落点、理由与上游处置仅由后续本批 design 第3节拥有；本文保留原承诺，不另建处置矩阵。Docs SSOT Plan 及完整拟写由后续原 Author/知识 owners 形成；整合/readback 不冒充 reviewed_promoted。

### 5.4 D1-R-04 完整来源与采用边界（整体 R-04；D1-SC-04/05/07）

D1 必须交付可由原安装/维护消费者使用的完整来源。canonical extension、当前 target constant、输出与直接 consumer schema 成套对齐为 `.9`；原 CLI/Core 和 lock 不因 Guru 发版改变。来源自身版本、接口、依赖、安装和平台投影可用性有实际行为验证，不能只断言版本字面一致，也不能把来源缺陷留给 D2 才修复。

当前被 Interface 选用的输出示例必须与 `.9` producer/consumer 合同一致，历史样本保持原义。来源验证的 local sample 必须从受支持的当前 bootstrap 入口进入原安装链，不先生成 legacy Task 再绕过、删除或转换它。该修复不新增验证模式，也不免除历史 Task guard。

D1 规划须明确提交前来源验证和完整分发集合的检验入口，区分源码/组件、临时安装目标和本 Task checkout 的实际采用。若以临时目标证明源安装/投影行为，必须运行原生产安装入口，核完整实际字节、mode、版本和真实 provenance，并说明该证据的来源锁定及环境边界；它不证明本 checkout 已更新。D1 本地提交后仍经原完整 Review，不制造来源专用提交分支。

本 Task checkout 的 `.9` 实际采用和整体 PRD 第7节 AC-04 的完整匹配验收由 D2 经原 tools `source_locked` 承担。其完整干净来源必须有真实 D1 delivered 依据，并由原 owner 核该来源自己的 lock、匹配 CLI/Core 与实际 target。保留 Task/archive/workspace/session/user config、peer 工具与 common runtime 指针；未知编辑、冲突、sidecar、旧事务仍按原 tools owner 处理，不以普通 apply 或手改受管副本代替。

工程验证按实际差额选择 package/runtime、canonical/dogfood/installed、声明平台、ownership、mode、sidecar、reapply/drift 的最小可靠集合。断言须从要求的条件、动作和可观察结果导出，实际触达被迁移 consumer；不为锁定文案复制实现或增加重复案例。已有证据先判适用性，补真正缺口。源码、组件、安装、实际 Agent 和外部效果分层报告。

canonical 修改后的实际 dogfood 同步义务没有删除。当前来源与旧公开 schema/安装的差额及 drift 失败如实保留，由 D2 完成实际采用及整体 PRD 第7节 AC-04 验收；D1 不能宣称整体 matching 已通过。若 D1 自身操作需要先采用新工具，或其必需验证失败，回原分配/规划 owner，不以本边界取得 pass。

Stage 2 的 focused clean、existing update/reapply、真实 `.8` upgrade、完整候选 scanner/smoke 门禁及整体 PRD 第5.6节列出的其余门禁，仍由原发布 owner 在同一 fresh candidate 上执行。本批不能提前宣称它们通过，也不扩完整多平台矩阵。

### 5.5 D1-R-05 准备 PR 与剩余责任（整体 R-05；D1-SC-05/06/07）

本地提交只归原 `guru-create-task-commit`；独立完整审核及 readiness 前不新 push、不建 PR。原 publication Architecture eligibility 必须为当前 no_change 或 reviewed_promoted；integrated_pending_review 不能进入 readiness。原 Delivery Review 针对完整本批、真实验证、兼容、安全/部署影响、剩余准备业务和 Stage 2 边界形成具体中文标题正文，PR 仅 `Refs #808`。

原 Publication/expected-head Merge 的 fresh live identity、完整已审 payload、事务与独立确认继续有效。每次 merge 前向 coordinator 展示精确方案并停止；其他 Git/GitHub、安装和资源副作用各由原 owner 展示并处理，不能借用其他步骤授权。授权只留当前对话，不写文件或 DTO。

本批交付后不能关闭 #808，不能推导 Task Completion、Finish 或发布通过。剩余实际采用由原 Completion 使用 additional_delivery_required，经原 Creation 建立并规划 D2，不提前创建或实现。所有准备业务及实际采用证据满足后，才可能满足 AC-07；原后续 Closure no_mutation、AC-08 终态归档/bookkeeping、caller-owned 资源保留及 Stage 2 的真实结果仍须分别完成。

### 5.6 共同边界

本批只处理诚实正常路径、常见错误、真实 stale/mismatch 和来源明确恢复，不增加攻击/伪造模型、竞态压力、TOCTOU、锁、fault injection 或非常规 crash 协议。secret/credential redaction、权限与破坏性副作用控制继续有效。

没有业务 API、数据库或生产部署变更，因此本批不新增业务 API、数据迁移或部署验收。不创建 release-notes、PR/Release body handoff、动态 implement checklist、发布 ledger、授权记录或 release-status commit。正文存在及当前 planning phase 都不表示方案已批准或实现已激活。

## 6. 本批验收、验证方式与未决项

下表保留整体选定的 AC 身份，全部是待执行预期；没有任何一项因本次 PRD 写作而通过。

| AC／对应要求与场景 | 验证入口、输入 | 必须观察及结果用途 |
| --- | --- | --- |
| AC-01／D1-R-01、D1-SC-01 | fresh-read #808/#794、真实交付/归档 lineage、tags/Releases、版本与各自 lock/manifest | 六项输入一致，#794 前置可证，版本未被占用；实质变化回原范围 owner。本结果只供准备输入，不是发布候选 pass |
| AC-02／D1-R-02、D1-SC-02/05/07 | 私有四份合同/入口、当前 packages/interfaces、实际公开调用与 consumer 回归、适用旧 provider 样本 | 原新链可消费，无重复独立 Check/固定第二轮或审核前发布；真实两槽/readiness及命中恢复成立，私有排除公共分发。静态/fixture/Agent 证明层次分开 |
| AC-03／D1-R-01/03、D1-SC-03 | 原 Docs Plan、三个 README、实际受影响完整 R/D/T/Architecture 单元与原 owner 整合/readback | 目标版本、正常行为、兼容及证据边界一致；必要关系完整，历史/proposed/current 区分，整合不当独立通过，不产生重复索引/权威 |
| AC-05／D1-R-02/04/05、D1-SC-04/05 | 实际来源/直接consumer/安装与平台投影验证、工程自检、必要知识整合、原本地提交、完整固定 committed candidate 与独立 Review | D1 全部来源、消费者、测试及文档 after 进入完整候选；来源自身可用性及必需验证成立。未参与实现的 reviewer 同次完成全部适用 Architecture/九维/fullrange 职责，零开放 P0～P3 finding；后继差额按影响刷新，不从命令或旧 pass 推导通过 |
| AC-06／D1-R-05、D1-SC-06 | 当前 publication Architecture eligibility、原 Delivery Review→Publication→Merge、精确 main/PR/expected head 与完整 payload | 中文 Refs-only PR 如实说明 D1 来源验证、旧安装/漂移观察和后继 D2 实际采用责任；新 push/PR 在当前审核/readiness 后，实际合并符合已审内容。不产生 #808 关闭或整体完成效果 |

AC-04 仍是整个 Task 的完整验收，由后继 D2 实际 source_locked 及目标读回建立；本表不把它改成 D1 已通过或范围外。D2 对自身全部安装 after 同样承担 AC-05/06，并按实际 freshness/文档差额承接 AC-01/03；AC-07/08 和 Stage 2 保留整体条件。

本需求阶段没有待用户决定的范围问题。来源自身必需验证、私有消费者具体迁移落点和完整 Docs Plan 由后续原 Author/Architecture/Approval 细化。原单 Delivery 方案的来源前置循环不再作为本批拟执行顺序；本次仅刷新需求与真实 candidate，新的独立 assessment 和完整方案尚未发生，不借此宣布 GAP-SOURCE-01 已实际解决或 Planning 已批准。

若发现版本占用、来源承诺冲突或真实范围选择，交原 Clarify；若存在 Architecture authority 身份/状态缺口，交原 Architecture 的已声明出口；普通正文遗漏回原 Author。不得私改 accepted scope、跳过独立判断或用未执行验证填 pass。`requirements_ready` 只说明本批要求和实际 candidate 可进入独立 assessment，不是 Planning acceptance。

## 7. Canonical 引用与本轮差额

以下路径是原 authority 的具体入口及用途，不构成共享正文写入清单。后续原 owners 必须完整读取命中单元及必要关系，按实际差额选择写入；本文只写本批 PRD。

| authority 与具体位置 | 本批承接与实际差额／保持边界 |
| --- | --- |
| [RDT-REQ-LIFECYCLE](../../../../../docs/requirements/current/task-delivery-lifecycle.md)：切片建立与唯一 Planning；提交前整合与一次独立完整审核；R794-01～07 | 当前要求已明确 #794 正常链。差额是私有 release 消费者和测试尚未采用，不重新定义公共 Check/Review，也不重写其他能力需求 |
| [RDT-DES-LIFECYCLE](../../../../../docs/design/current/task-delivery-lifecycle.md)：本地待审提交与旧 Draft 恢复；提交前整合、精确 Commit 与合并 Review；D794-01～05 | 保持原 TaskCommit→Candidate→Review 两槽→readiness→Publication 及逐状态原 provider。后续 design 细化私有消费落点，不新增公共 API 或状态机 |
| [RDT-TST-LIFECYCLE](../../../../../docs/test/current/task-delivery-lifecycle.md)：T636、T638、T794-01～07 | 采用实际影响的 producer/consumer、未审发布阻塞、后继及恢复预期；补私有真实调用覆盖。历史 #794 结果不冒充本批/Stage 2 通过，不无条件重跑全部模型或矩阵 |
| [Architecture authority](../../../../../docs/architecture/README.md)：职责发现、维护与关联 authority；[system](../../../../../docs/architecture/01-current/system.md)：ARCH-CUR-017、提交后审核及 ARCH-CUR-075/076；[ADR-POSTCOMMIT-INDEPENDENT-REVIEW](../../../../../docs/architecture/adr/postcommit-independent-review.md) | 私有发布 consumer 的旧 Finalizer/双轮文字与当前原链需在实际命中范围收敛；保原私有边界、固定范围和后继覆盖。ADR 正文的 proposed 身份与 current 引用分别交原 Architecture 核适用性，不由链接推导已接受或批量改历史 |
| [MIGRATION-794](../../../../../trellis/presets/guru-team/MIGRATION-794.md)：新公共合同、退休入口、在途处置与完整采用 | 规范性机制来源。后续 design 第3节逐项唯一处置；本批消费当前接口及 matching 原 provider，不静默改旧语义 |
| [私有合同及测试](../../../../../.agents/skills/release-guru-trellis-version/)：Stage 1、`test_contract_owns_two_stages_two_reviews_and_independent_confirmations`、`record_branch_review` 与其消费者 | 已定位的直接迁移差额：采用当前逐Delivery完整链和已接受来源→采用分配，移除无当前入口的early来源引用；保持 Stage 2 原 locators、限定 historical-Task observation、两个本地目标收敛和副作用/持久化边界，不能仅把旧链文字改为新链 |
| [public-docs](../../../../../.trellis/spec/docs/public-docs.md)、[canonical extension](../../../../../trellis/guru-team-extension.json)、[source lock](../../../../../trellis/presets/guru-team/source/trellis-source.json) | 三个 README 按原职责对齐 `.9` 完整来源准备和真实安装边界；不维护第二 Fork SHA 表、不把未发布版本称稳定。D1验证来源自身分发，D2的精确实际受管更新与preservation仍归原tools owner |

没有服务分层、业务数据或外部业务依赖变化；本批不新增这些 Architecture 决定。必要知识维护、ADR 是否需要修正及 project checks 由原 Architecture 按真实 candidate 判断，不能从“发布准备”标签推导 no impact。
