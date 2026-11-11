# D1 提交后一次独立完整语义审查：需求

## 1. 整体来源与术语

本批为 Task `794-postcommit-review` generation 0 的首次 Delivery，UUID `8c5534bb-2d8a-4e3a-be58-4ad853a2e3e0`。公共 accepted_scope 指向 Task 根 `prd.md` 的实际 revision，scope_ref 选择 R1–R7；planning_root 为 `deliveries/8c5534bb-2d8a-4e3a-be58-4ad853a2e3e0`。

| 来源及章节 | 角色和本批用途 |
| --- | --- |
| https://github.com/castbox/guru-trellis/issues/794 ，完整正文 | Direct Source 要求；本批全部行为、迁移和验收边界 |
| `../../prd.md` 第1–8节 | 已接受的整体定义、R1–R7、S1–S6、AC1–AC6；本批完整覆盖 |
| `.trellis/delivery-contract.md` 的 Closed phases and owners、Candidate/gates/result recovery、Native profiles | 上游 API1 当前规范性技术约束：独立的 check/full_review 槽、真实结果与 predecessor；不能通过写任意 phase 绕过 |
| `docs/requirements/current/task-delivery-lifecycle.md`；`docs/design/current/task-delivery-lifecycle.md` | 当前生命周期、早期 Draft、晋升和恢复的有效合同；本批明确替代重复审核/提前发布部分，保留其他责任 |
| `guru-check-task`、`guru-review-branch`、`guru-create-task-commit` 的 canonical 合同与公开入口 | 原职责和真实消费者证据；本批 design 第3节拥有唯一来源设计处置 |

“一次”按同一未变候选的完整独立语义判断计。记录上游必需结果或脚本校验不构成另一次语义审查，也不能制造未发生的判断。原文档 owner 的编辑、整合与准确性职责仍存在。

## 2. 整体与本批目标、非目标

整体目标是实现、自检、文档整合和本地提交后进入一次独立完整审核。本批独立交付目标是提供完整可运行的替代链，同时迁移全部实际消费者和在途恢复，避免新入口存在而旧前置仍强制重复 Check。

覆盖整体 R1–R7。保持整体第3节全部非目标；不合并 Delivery Review/Publication，不评估或实现 #734 等其他拆分项，不改上游 Trellis 源码、全局包或 node_modules，不新增公共 Task phase 或并行状态 authority。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 尚无前序 Delivery。起点 B 与 Planning H0 均为 `4d565c97b5abf634d76ede2d18eed0a57f13bb76`，PR target 为 `main`。#793 与 #792 已在该树交付并归档，本批采用其现行 qualifier applicability 和按步加载能力，不重复实现。#713 当前公开候选构造、操作及恢复能力已在该树；只使用其支持域。

当前 upstream API1 要求真实 Planning、check、full_review 和 readiness。当前 Guru 则先 candidate Check、晋升、final Check、提交接续及 Branch Review；early Draft 可以早于完整 Check 发布。本批必须在这个真实约束上实现单一语义审核，不能以空白上游 gate 取得前进资格。

本批不预留未交付的 R1–R7 功能责任。实现/验证、业务交付和 Task Completion/Closure/Finish 尚未发生，均是剩余义务；D1 merge 本身不证明整体完成。

## 4. 本批调用方、场景与流程

| 场景 | 条件、动作和可观察结果 |
| --- | --- |
| D1-S1 首次实现 | Planning 已激活；实现者完成代码、原文档 owner 整合与工程结果，经原精确提交 owner 形成固定 H；没有独立提交前 Check |
| D1-S2 固定独立审核 | 新 reviewer 未参与实现，先读 constitution/baseline/change contract，再读固定 B..H 和 consumers；审核期间不写候选；一次覆盖原全部职责，通过后才交原 readiness |
| D1-S3 修复与重审 | reviewer 返回当前缺陷或 Planning/source 问题到原 owner；修复生成后继提交；可核验覆盖和工程结果按适用性采用，差额和影响补审，影响不明或覆盖丢失补足完整审核 |
| D1-S4 base 集成 | 原 Reconcile 判断真实触发、固定 target 与 Task/base 归属；保留 B 和完整候选，审核冲突解决及集成影响；无关已审核 base 内容可被原 owner 采用 |
| D1-S5 正常恢复 | 提交、gate 投影或旧 Draft 外部动作输出丢失；原 owner 读同 key/H/实际结果并仅接续尚未完成动作，不复制 pass 或重建身份 |
| D1-S6 发布 | 未通过合并审核的候选无 push/PR；通过后保留原 Delivery Review、Publication 和精确 merge 门禁，并报告真实结果/缺口 |

## 5. 完整行为、条件与约束

- D1-R1 承接 R1/S1：真实工程结果包括 Planning 选择的测试、静态检查及 diff 检查；必要 Architecture/RDT 候选和晋升在本地提交前完成。去除 candidate Check 的循环前置，保留原文档 owner、readback 和普通冲突处理。自检不等于独立通过。
- D1-R2 承接 R2/R3/S2：选择一个原 Skill 独占合并审核，完整承接 Check 九维、Branch Review、必要消费者、减法/维护/兼容及实现后一次独立 Architecture。保留 Planning Architecture；真实后续变化刷新受影响判断。
- D1-R3 承接 R4/S4：固定 B..H 覆盖 Task 全部改动、知识整合、base 集成及冲突处理。caller 不能缩区间或把 undelivered 提交当已交付前驱。
- D1-R4 承接 R5/S3：先确定完整适用检查，再评估原工程结果；采用有效结果，仅补具体缺口。合规独立 reviewer 可接续后继；不能只审修复点、只看新增行或无条件重跑所有完整检查。
- D1-R5 承接 R6/S5/S6：新链停止 early Draft 的审核前发布；旧路径按明确版本边界恢复/处置，不静默转义。已完成 push/PR/metadata/state 事实保留，尚未发生动作不因旧事务存在获得新发布资格。readiness 仍是原发布前责任。
- D1-R6 承接 R7/全部场景：版本化每个实际改变的 input/output/schema/profile/命令/出口及 projection；完整迁移 upstream gate、TaskCommit、知识、架构、回退、continuity、发布和 Completion 的必要消费者。只保留有直接 consumer 的结果；无授权、账本、双状态机或无 consumer 字段。
- D1-R7 承接 R7：canonical 先改，已有 Task/session checkout 经原工具维护 owner 成套采用；声明平台包含 Codex/Claude Code，Cursor 等实际命中投影同样验证。用户内容和并行资源保留，sidecar 沿原 owner 处理。

## 6. 本批验收、验证方式与未决项

| 验收 | 入口、输入与预期观察 |
| --- | --- |
| D1-AC1 → AC1/AC5 | 新公开提交→固定审核→readiness 链；没有提交前独立 Check；原职责和必要读取顺序全部由实际 reviewer 完成 |
| D1-AC2 → AC2 | 对未通过、已通过及 HEAD 正常改变的候选调用原发布入口；只有当前通过候选可产生远端动作，仍先 readiness |
| D1-AC3 → AC3 | 修复后继、base integration/冲突和丢失覆盖正常输入；采用可核验结果并补真正失效/变化，固定范围保持 |
| D1-AC4 → AC4 | 旧 Check/已提交/已审、Draft 已执行或 pending 输入，和原输出丢失恢复；同 key、真实结果、不重复副作用、不补造 pass |
| D1-AC5 → AC5 | 公开 schemas/examples/exit projections 与真实 upstream API 测试；单次语义结果足以合法写必要上游结果，拒绝缺职责的空白结论 |
| D1-AC6 → AC6 | 定向 package/runtime、canonical/installed/platform、reapply/sidecar/mode/drift；若当前 clean 安装路径缺少可靠证据且本批验收依赖该证据，补一个代表性 clean；分清脚本、Agent、安装和外部证据 |

需求已清楚。上游必要 gate 的合法承接、具体原 Skill 承载、old transaction cutover 是当前候选评估问题；先进入独立 Architecture candidate_assessment，再由 Author 写完整 design/implement。尚未批准或执行实现。

## 7. Canonical 引用与本轮差额

- Requirement/behavior：`docs/requirements/current/task-delivery-lifecycle.md` 的“早期提交、Draft 反馈”“最终检查、提交和独立审核”“候选适用性与完整覆盖”及 R713；本批替代重复门禁和审核前发布，保留身份、范围、工程采用及原恢复。
- Design：`docs/design/current/task-delivery-lifecycle.md` 的 D531/D600/D638、D636、D637/D713；迁移实际 owner、投影、前置和消费者，精确 public I/O 仍由各 package 独占。
- Test：`docs/test/current/task-delivery-lifecycle.md` 的 T531/T600/T636/T637/T638/T713；采用支持域内测试，补本批新顺序与迁移的真实观察，不要求无关完整生命周期重放。
- Architecture：`docs/architecture/README.md`、constitution、`06-governance/change-contract.md`，实际影响由独立原 Architecture owner 判断；Planning 不写 shared current。知识整合 consumer 与晋升责任须在本批方案具体调整。
