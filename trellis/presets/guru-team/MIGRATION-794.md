# 提交后一次独立完整审核：采用与退出

本合同迁移 #794 的审核、提交、知识整合和必要消费者。固定前驱完整 provider 为 Git `4d565c97b5abf634d76ede2d18eed0a57f13bb76`。它的 workflow、packages、runtime、schemas 和平台投影共同解释前驱操作；不能将一份旧 checkpoint 交给新版 parser 猜测。

新正常链为：Planning/Activation → 实现与工程自检 → 原知识 owners 必要整合/readback → 原 TaskCommit 本地提交 → 固定 B..H 的一次独立完整 Review → 原 Delivery Review/readiness → Publication。原 Completion、Closure、Finish 保持。

## 1. 唯一原 owner 与公开边界

- 原 `guru-review-branch` 同时承接 Check 九维和完整 Branch Review，首次审查者新开且未参与实现。它沿原 Architecture 方法先判断固定 before/after，再完成完整当前审核；不编辑冻结候选。
- workflow 的公开 `owners.check`、`owners.full_review` 都指向该原 Review。上游 Task schema2/API1 的两个结果槽与 predecessor 保留。真实同次判断通过后先写 check，再写 full_review；完整成功才输出 passed。第一槽、历史 pass、文件或摘要不能代替第二组真实职责。
- 原 `guru-create-task-commit` 提供待审本地提交及干净重入。它的 semantic gate 和精确 executor 不声明独立质量通过。结果经原 implementation constructor/begin_check 进入固定提交审核，不交早期 Publication。
- 原 RDT/Architecture owners 在提交前整合完整目标并读回。Architecture 的 `integrated_pending_review` 表示整合事实；只有实际提交后独立评估才能形成 `reviewed_promoted`。下游 readiness 只接受真实 no_change 或 reviewed_promoted。
- 原 Delivery Review 判断并记录 readiness，返回 ready。Publication 只消费其当前 ready/readiness 并执行已审发布内容。未独立通过前不新 push、不建 PR。

## 2. 本次选中的新公共合同

精确字段、schema path、命令参数和出口以各 package 当前 `interface.json` 为唯一接口定义。以下表说明版本和语义差额；不得将旧资产原地改成新版含义。

| 原 owner | 当前选中合同与直接 consumer |
| --- | --- |
| TaskCommit | Delivery aggregate3.0 的 `delivery_pre_review_commit`、`delivery_pre_review_committed_reentry`；`pre_review_committed` 仅交 TaskRef、DeliveryKey 与 `branch_review_commit` 到 `guru-pre-review-commit-router`。固定 B 和完整 Candidate 从原 constructor 取得，不增加可重推 Git bundle |
| Review | Delivery aggregate4.0；普通 committed、continuity、alignment 当前 input2.0 不要求先验 `check_result_id`。passed2.0 交原 Delivery Review；当前 finding/scope/planning 出口各用独立 schema 和唯一 consumer。Check 的正常语义 authoring、完整结果合法消费及恢复职责迁入此 owner |
| Architecture | 非 Planning6.0 / Delivery4.0 的 precommit integration 与 committed assessment；Planning 两目的仍用原 purpose-bound 合同。保留原 before authority、完整候选及原 concern/project-check，不增加第二 authority |
| RDT | impact/promotion3.0 从真实工程准备和完整拟写进入原整合。candidate_ready 是完整贡献准备结果，ssot_current 是整合事实，不生成独立 pass |
| Reconcile | 命中的 resolved input/result/authoring2.0 使用实际 `committed_candidate_anchor`，不再以旧 Check pass 为前置。原 owner 判断 Task/base 归属、完整范围、冲突及组合影响 |
| Delivery Review | input/aggregate2.0 消费新版当前 full_review，仍是 readiness 唯一 writer |
| Publication | Delivery aggregate4.0 退出新 `delivery_draft_publish`。remote Draft recovery 当前 input2.0 只恢复真实完整 PR/HEAD/payload 事实；pending 新远端动作回当前审核/readiness。原 return-to-Draft 修复回程保留 |

Review 当前 owner-private gate 为 `guru-review-branch-private-delivery-gate-2.0`（schema_version 8.0），alignment gate为2.0，archive保留1.0。TaskCommit private candidate4.0/result3.0仅供原同操作consumer。旧公开 schema、示例和历史结果保留原版本意义，作为 pinned validation/history assets；它们不是当前 runtime fallback。没有双正常路径、自动 pass 转换、长期兼容开关或共享授权状态。

## 3. 从活动图退出的前驱入口

原 `guru-check-task` 不再是 mandatory 开发门禁。以下前驱开发 profiles 的工作分别由新工程准备、原知识整合和原 committed Review 承接：

- `delivery_candidate_check`、`delivery_initial_check`；
- `delivery_finding_fix_rerun`、`delivery_planning_reentry`；
- `delivery_resolved_reconciliation`、`delivery_scope_revision`、`delivery_scope_withdrawal`；
- 原 candidate_checked、final passed、提交改变 HEAD 后再 Check 的回程。

原 `check-phase2-check`、`project-resolved-reconciliation` 开发命令及当前执行脚本退出。`record-phase2-check` 仅为显式 rollback recovery 做 required `--dry-run` / `--skill-input` 校验，不写新的 phase2-check checkpoint。原 Check 的显式 `delivery_planning_stale_recovery` 仅恢复已经执行的旧 rollback；原 legacy_control_inspection/retirement 保持其独立支持域。它们不重新启动开发 Check。scope 修订、撤回和当前 planning_stale 由实际当前 Review/阶段 owner 承接。 当前Check eval catalog仅保仍支持的legacy retirement reader场景，旧normal eval不再被current runner选择；历史文件不转换成新质量通过。Review native authoring按input2/gate2读取和传输，不种历史Check，其真实接收者自行完成九维和两项role judgment。

TaskCommit 的前驱 initial/revision/finding/recovery/committed profiles 与两个 draft_commit profiles 不作为当前新调用入口；新输入沿当前版本进入待审提交。已经发生的本地提交仍归原 TaskCommit 同操作恢复，不另造提交。

Review 的 `delivery_draft_content_review` 及其 early feedback 出口退出新正常链。未带 DeliveryKey 的旧 `branch_review` / `base_continuity` 普通调用在当前 provider 只返回迁移诊断，不运行旧 schema7 或旧 passed 输出；原历史 archive/legacy 明确支持域保留。原 `guru-draft-commit-router`、候选 Check 的 final-integration router 和重复 Check 回程退休；新的 `guru-pre-review-commit-router` 只在原本地提交成功后固定候选。Publication 的 draft_published 若由合法恢复返回，只报告既有事实并接续当前义务，不触发新早期发布或独立反馈旁路。

## 4. 在途对象的实际处置

原安装/升级 owner 先读确切 Task/Delivery、generation、phase、scope、固定 B、现有结果和原事务。原阶段 owner 判断实际义务，不能由脚本从版本号决定 semantic route。

| 实际状态 | 原 owner 的处置 |
| --- | --- |
| Planning 或 implementing，尚无远端动作 | 成套切换 matching provider；保留身份、scope、B、规划和实际资源。按新链完成工程、整合、提交及首次独立审核，不转换旧 pass |
| 已有旧 check、缺当前 full_review | 原阶段 owner 合法 rework 清真正失效结果，在同 Delivery/B 上形成 committed candidate。工程事实与原覆盖先判适用性，再用于新真实审核 |
| 旧 full_review/readiness 仍适用 | 保留其原版本和真实范围。原 owner 可用固定旧完整 provider 完成已经承诺的同操作结果恢复，或合法 rework 后进入新链。任何新远端动作仍须当前独立审核及 readiness；不得把旧结果改名为新版 pass |
| 本地 commit 已完成、输出丢失 | 原 TaskCommit 核原 operation、实际 parent/HEAD/精确路径，恢复同一 commit。干净已提交候选不再 stage/commit，结果接当前固定审核 |
| 新 check 已录、full_review 或最终输出未完 | 原 Review 对同 key/B/H/Candidate 与真实语义结果恢复缺步。已录结果不重复创建。必要语义覆盖不可得时实际重审，不能由第一槽自动补出第二组判断 |
| Draft 事务已有 ensure_draft/push/bind/metadata 事实 | 原 Publication 只读实际同 PR/HEAD/payload/state，恢复准确已完成结果。保留原 PR 和副作用，不重建 Task/Delivery，不再 push 或创建 PR |
| Draft 尚有 pending 远端动作 | 原 Publication 报告 completed/pending，停止 pending 新动作，回当前独立审核及原 Delivery Review readiness。随后同 PR/原事务 owner 接续；禁止先 push 后补审 |
| Planning rollback 已执行、handoff 丢失 | 原 rollback producer 用实际已清结果、cause/revision refs 与原 scope disposition 恢复准确 handoff；旧 Check 使用其显式 recovery，当前 Review 使用自身 recovery。不重复 rework、恢复旧 Planning 或分配新身份 |
| 普通 source/HEAD/expected-current 不匹配 | 回该事实的原 owner 判断差额；必要时修复并形成后继候选。不能重算 digest、替换 owner_id 或使用 phase 推导通过 |

原完整 provider 只服务明确旧操作和原支持域，不作为当前正常 runtime 的第二 reader。其合法旧操作已经恢复/处置并切到当前对象后，后续不再从它继续开发门禁。历史 Git 和原日志保留原义，不回填后来的成功。

## 5. 完整采用与验证

canonical workflow/routing、原 packages、共同 runtime、schemas/interfaces/consumer、spec 和实际平台投影必须一起采用。 本合同canonical来源为 `trellis/presets/guru-team/MIGRATION-794.md`，原managed-source owner将同一正文投影到 `.trellis/guru-team/MIGRATION-794.md`；consumer按完整provider定位，不依赖源码布局的相对链接。已有 Task/session checkout 用原 `guru-upgrade-tools`；普通 apply 的前置阻塞不授权手工覆盖或历史迁移。保留用户内容、其它 Task/session、workspace journal、mode 与原 sidecar 处置。

本 Task 的源码自举同样保留实际适用旧链。实现新规则不等于当前安装已经切换，安装切换也不补造旧 gate。先由原 owners 完成旧阶段实际必要工作，再按本表在合法边界采用 matching source；完整当前结果仍由实际语义 owner 判断。

必要定向证据包括真实 TaskCommit→Candidate→Review 双结果→Delivery Review/readiness→Publication gate 的 producer/consumer、正常后继/base 集成、旧事务恢复，以及 canonical/installed/platform/reapply/sidecar/drift。实际 AI 读取、判断与覆盖采用须由真实 Agent 执行单独说明。脚本、fixture 和安装投影不能证明这些行为或外部采用。

这是普通 workflow Issue；完整多平台升级/Release 矩阵不在本次范围。若当前 clean 安装路径的具体验收缺少可靠证据，最多补一个代表性 clean throwaway。没有固定审查轮数、成本降幅、通用 Agent 评测框架、授权记录或证明账本。
