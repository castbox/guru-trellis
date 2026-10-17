# D1 设计：人工旧归档恢复

## 来源处置与固定范围

Direct Source 为 [Issue #577](https://github.com/castbox/guru-trellis/issues/577)，整体范围读 [Task PRD](../../prd.md)，切片要求读 [D1 PRD](./prd.md)。Clarify 没有选定额外规范性设计；不存在需要逐项迁移的外部设计承诺。下表是本设计唯一来源处置表。

| 来源与原承诺 | 处置与落点 | 理由、影响及上游处理 |
| --- | --- | --- |
| #577 行为1–3：同身份、独立启动、三种生命周期 | 保留；原 maintain-legacy-task 新增 `archive_resume` profile；正式 Finish 仍 Reactivate，未完成 closeout 回原事务 | 不以旧 status 或 PR 合并代替恢复资格；无新 TaskId 或生命周期模型。 |
| #577 行为4–6：精确写集、历史事实、普通恢复回退 | 保留；公共 prepare/apply/resume/rollback 与原 Guru owner checkpoint | 不复制公共算法；不补造 gate、完成结果或资源 seal。 |
| #577 行为7：目标原生入口和下一实际 owner | 保留；原 observe/finalize 增加归档恢复分支，原 Identity/Bind 消费公共 active identity | 外部维护执行和静态 JSON 不能证明目标自身恢复。 |
| Trellis #46 / PR #52 公共 API | 保留其 `inspectTaskTarget(original_task_ref)`、`prepareArchivedTaskResume` 和 `result.resumed_task`；公共 owner 定义支持格式与 generation | Guru 传入经 AI 审查的投影、resume_intent、artifact/session/binding 处置；不改上游。 |
| ADR-024/027：公共模型 authority、source-loaded 维护、原 owner、current-only | 保留；沿原 transport、维护 package、lifecycle 与 delivery adapter 原位扩展 | 正式 source lock 不变。local_candidate 只用于隔离验证，正式能力缺失写前诊断。 |

开发基线、D1 内容 B、观察 H0 均为 `ef0fcdf0c3746e6d84f97732b9ab776a4bf7703e`（选定 main）；PR target 为 main。实现最终 H 由 Task Commit 和独立完整 Review 取得。B 来自 D1 无既往交付时的显式 development_base；target 前进本身不改 B。

## 入口、职责与状态

`guru-maintain-legacy-task` 是唯一 source-loaded 语义入口。新增独立闭合 input schema `archive_resume`，必填原有 source_ref/target_checkout/key/task_ref，再加 original_task_ref 与 active_ref。task_ref 指向选定月归档，original_task_ref 指向其原活动路径，active_ref 是本次活动目标。原 convert/history_closeout/resume/rollback 输入、输出和消费者不改义。新增 profile 和匹配安装边界由 MIGRATION-577 说明。

AI 先读原归档、人工说明、原 scope/规划、来源、提交/PR、session/binding 和未完成责任。AI 区分：公共认可的 legacy/schema1 人工历史归档；当前 schema 正式 Finish 归档；未完成 Closure/Finish/Finalizer。后两类分别回 Reactivate 或原恢复 owner，不调用本恢复写操作。身份/来源不唯一、依赖缺失或未支持格式在写前停止并给出 owner/输入/重入路径。只读入口不依赖旧 dispatcher、当前绑定或人工搬移。

公共 CLI/Core 是 Task、Delivery、session、binding 和数据恢复的唯一 writer。Guru AI 提供完整公共 projection、五份规划 artifact preserve/write 处置、legacy_facts、resume_intent（reason/archive_review AuthorityRef、next_owner_id/next_action）、精确 session dispositions 和 branch binding。generation 保留规则直接消费公共合同与操作返回，不在 Guru 推导或递增。恢复不创建空 Delivery；历史已交付与当前补差分别保留，scope 变化进入原 Clarify。

原 maintenance_transport 原位增加 `prepareArchivedTaskResume` 转发。API1.0 基础三项 capability 保持要求，接受公共已声明 additive `task_resume`；archive_resume 必须在准备前核实实际 task_resume 方法/能力。实际 pair digest 继续绑定 bytes/modes。source_locked 继续完整 source/build/mode 校验；本任务不改 Fork lock、不放宽 mode、不循环重装。

## 公共数据与私有控制的接续

prepare 只读：inspect exact archive + original_task_ref，核对公共输入所选对象；原私有 owners 分别检查原活动路径归属的控制，并从选定 archive 读取原 Task bytes。给原 owner 的 provenance 明确区分 `task_ref=original_task_ref`（控制归属）与 `source_task_ref=archive task_ref`（物理原始记录）；旧 profile 缺少后者时仍用其原 task_ref。该字段由原 owner 检查，不交给 coordinator 解读其状态格式。

私有顺序保持 Publish → Merge → Finish → 明确选定的 Approve/Check/Review。原 owner 检查/冻结/退役/恢复自己的确切文件；coordinator 不删私有目录、不制造空 owner。AI 在准备前识别未完成收尾责任并回原 owner；terminal Finish 和 seal 保留。历史 PR 核验使用原 Publish/Merge `legacy_history_verification`，未知事实保留缺口。私有 schema/projection 同步演进，不复制六套新语义。

apply 冻结同一公共 plan 和原私有 preimages，随后调用公共 apply。公共返回 applied 后，Guru 使用 `resumed_task.key/task_ref` 作为唯一当前活动结果；检查原 archive 及公共保存的 source bytes 可读。原 archive 只作历史/转换溯源。旧 Task 路径只用于控制归属和来源，不再用于 finalize 的 current identity。checkpoint 仅保存同操作恢复必需的 plan、原 owner refs 和公共返回 identity；不保存授权。

resume/rollback 沿原 recovery_ref，不重新 prepare、不再导入交付或分配 generation。普通部分写入、丢输出和重复 resume 保留原 operation。回退先检查原私有 postimages，再由公共 owner 核对数据兼容/后续工作，最后恢复原私有 controls。后续业务改动阻止覆盖；工具回退仍由原独立 tools owner 判定，不扩大写集。

## 当前 Identity、Bind 与下一实际 owner

原创建/历史 reservation 继续读取归档并防止新建重复 TaskId。当前 active 生命周期解析改为消费目标安装的官方 TaskId resolver，并受当前绑定 checkout 约束；不把历史 reservation 计入 active 执行唯一性。复用原 adapter/Bind 对目标 session_storage 的加载和 checkout scope，不复制公共 provenance、转换算法或解析器。显式 archive/history/Reactivate 保留原合同。测试覆盖“保留同 ID legacy archive + 唯一 active”、真正 active 冲突及旧记录仍不可直接 current 使用。

恢复后调用目标自身 installed identity、C3 checkout、C4 branch binding、Bind 和 continuation，确认同一公共返回 TaskId/generation、当前 active locator 及真实 session 或合法 explicit-task。再运行当前工作真正需要的 Guru owner：scope 补差走 Clarify，仅当存在真实新实现切片时进入 `guru-create-delivery → guru-author-task-plan`，已交付待验收走 Completion evidence_pending。该过程不新建 Task。owner 的语义门禁由执行 AI 完成，不从退出码、status 或固定预填 JSON 推导。observe 和 finalize 对 archive_resume 都要求下一 actual owner；最终 task_resumed 仍只交最小 current identity 给原 continuation。

工具、数据、历史、会话、native 和业务完成分开报告。匹配包仅证明所测能力；任务恢复不代表业务完成。现有正式 lock 不含本能力；隔离 local_candidate 来自 PR #52 的实际 source/build/API，不作为正式采用结论。CLI 两个 Python template 的安装 mode 与 source dist 不同这一事实保持可见，严格 source_locked 校验不放宽。

## 架构、兼容与验证

candidate Architecture 的实际结果选定 `legacy_boundary_convergence`；baseline 为 `current-main-0.6.17-guru.97/active`，constitution 为 `guru-trellis-design-constitution-v1/current`，project change contract/concern set 均 v1。任务独占 [contribution](../../../../../docs/architecture/contributions/577-manual-archive-resume.md) 记录九项 concern、before/after、唯一 writer、兼容退出与未验证边界。现有 ADR-024/027 足够，无新 ADR；共享晋升属于原 Architecture owner，先独立 Phase2，再按 expected-current 写入并进入最终 Check。

真实旧格式 consumer 需要 maintenance-only 支持，普通 lifecycle 不新增旧格式 dual-read。旧 profiles 仍有明确 convert/history_closeout/Plan2 consumer；在这些 consumer 退出后由原 maintenance migration 删除。此次直接扩展原 owners，未建通用恢复框架、第二 updater、并行状态机或长期授权/gate审计。

验证采用 [implement](./implement.md) 的唯一计划和 RDT 唯一 Test：定向 package/runtime 回归、一个代表性旧安装拓扑的完整 AI/native/下一 owner 链、原 profiles/正式 Reactivate 兼容、普通恢复与后续工作保护、canonical/dogfood/installed 与声明平台/reapply/drift/sidecar。真实 CMS、正式 Fork 采用、软件发布和完整 Release matrix 均不在本次证据范围。
