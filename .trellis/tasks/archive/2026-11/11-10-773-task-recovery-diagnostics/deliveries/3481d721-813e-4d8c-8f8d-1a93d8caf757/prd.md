# #773 D1：分支发现诊断与同身份恢复需求

## 1. 整体来源与术语

整体权威为 Task 根 `prd.md`，accepted_scope revision 为 `sha256:ad19f6c52b59cda2c4e135d329629b7bb2ef6c9cbb0e5422d79cb2e977675627`。本批 scope_ref 选择 AC1、AC2、AC3、AC4，DeliveryId 为 `3481d721-813e-4d8c-8f8d-1a93d8caf757`，planning_root 为本目录。

| 来源 | 章节／角色 | 本批用途 |
| --- | --- | --- |
| [#773](https://github.com/castbox/guru-trellis/issues/773) | 完整正文；Direct Source、要求及约定设计 | R1/R2、原 owner、公开调用、候选载体前提、最小验收和非目标。 |
| Task 根 `prd.md` | 全文；已接受整体需求 | 整体术语、S1–S4、范围边界和 Completion 责任。 |
| #773「问题与已核验证据」 | #223 历史个案 | 复用已验证结果，保留历史门禁缺口；不视为本批执行证据。 |

TaskId/generation、Delivery、Git 载体和工作区／HEAD 的含义见整体 PRD 第1节。本批“恢复”指恢复同一身份载体及其运行关联，不代表业务交付完成。

## 2. 整体与本批目标、非目标

整体目标是让 AI 从准确诊断进入可执行的同身份有界恢复。本批完整覆盖 R1 和 R2：修复 discovery／plan recorder 的缺失 Task 诊断，补齐原 owners 的恢复顺序、公开调用和停止条件。若现有入口确有具体执行缺口，仅补必需的最小确定性动作。

保留整体非目标：不修复 #223 业务代码，不操作生产存量、部署、删除、退款或业务 Issue 关闭；不补历史交付归属、门禁或空 Delivery，不重合并 PR，不建设恢复框架、缓存、账本、授权记录、锁、压力或对抗性保护。#766、#772、#734 不进入本批。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 尚无前序 Delivery。开发固定基线为 `313d80215f65777fc70893a90c6d8dce8005d6dd`（所选 origin/main），PR 和完成验证目标均为 main。

起点事实：Branch 包 `runtime/invoke.py` 的 discovery／plan recorder 共用分支直接调用 `resolve_task_ref`；正式 invoke 已捕获生命周期异常。候选读取在未绑定时查 HEAD Git 树，在已有绑定时可验证工作区 Task。原生 `task.py set-base-branch` 已提供目标基线字段 writer；Git 已提供精确文件恢复能力。

当前 Branch 初次关联仅消费已验证 HEAD 候选，Rebind 要求已有绑定及 clean/base-contained 边界。Author 必须以这两个边界核对恢复指引的公开可执行性，不以内部调用填补步骤。方案和代表性验证尚未完成。

D1 采用全量交付；不预留另一个切片承接本批遗漏。后续 Check、完整独立 Branch Review、readiness、PR 发布及整体 Completion 均须实际完成。PR 发布后按委托停止，合并仍由协调器具体处置。

## 4. 本批调用方、场景与流程

| 场景 | 条件和调用 | 处理及观察 |
| --- | --- | --- |
| D1-S1 缺失诊断 | AI 以规范 TaskRef 调用 `discover-candidates.sh` 或 `record-plan.sh`，当前 checkout 正常缺 Task | 保持拒绝，返回既有诊断结构中的 `task_not_found`、TaskRef 位置和原恢复指引。 |
| D1-S2 同身份恢复 | 原 Git 载体、TaskId/generation/Delivery、完整规划和历史缺口均有可核对来源；用户选择目标基线及写集 | 先恢复同一 Task 载体，再建立正确分支／资源关联，最后绑定接收聊天自身会话并读 continuation。每层只报告自身结果。 |
| D1-S3 前提差异或已有绑定 | 工作区可读而未绑定 HEAD 不含 Task，或 C4/C5 已有效 | 前者明确候选前提并交原 owner 的合法恢复步骤；后者直接复用有效关联。不得反复扫描、隐含要求提交或重建身份。 |

无法唯一核对原身份或 Git 载体、有矛盾、所需公开动作缺失或新增副作用未确认时，原 owner 停止依赖步骤。已授权同目标恢复自动继续，目标变化按原交互规则处理。

## 5. 完整行为、条件与约束

- R1：在 discovery／recorder 共用 Task 解析边界复用 `LifecycleContractError` 到命令诊断的转换；不把缺失前置转换成无候选成功，不建设通用异常框架。公共合同若变化，明确兼容边界。
- R2：由 Identity、Branch、Ensure、Bind 及实际恢复 owner 各自拥有内部指引；明确固定载体、核对身份／完整规划／历史缺口、目标及写集、文件恢复、分支资源关联、当前聊天绑定、current／continuation 的顺序。
- 基线变更、文件恢复、C4/C5 关联和会话绑定保持各自真实结果。恢复保留原 TaskId/generation/Delivery 和历史 Publication／Delivery／full_review／readiness 缺口。
- Identity 工作区读取和未绑定候选 HEAD 读取的差异必须写清。现有枚举及排序算法不变；不得以恢复要求为由隐含要求提交。
- 实际调用只使用公开入口及原 writer；不调用内部 Python 类，不手编 common-dir JSON，不手改受管副本。
- 只有现有公开入口的具体缺口成立时，补最小动作及原 owner 合同；不预设通用恢复工具。约定设计的唯一逐项处置归本批 design 第3节。
- 原安装／升级 owner 同步受影响投影，保留 Task/session。验证限定于本批 package、分发、drift 和实际变化动作；不继承完整安装／Release 矩阵。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应行为 | 验证入口、输入及预期结果 |
| --- | --- | --- |
| AC1 | R1、D1-S1 | 以正常缺失的规范 TaskRef 调用两个共用路径，观察拒绝、`task_not_found`、TaskRef 定位和恢复指引。复用现有成功／只读回归。 |
| AC2 | R2、D1-S2/S3 | 逐项对照指引与实际公开入口，核对条件、顺序、写集、停止条件、工作区／HEAD 差异和历史缺口；不能以链接或绑定成功代替这些结果。 |
| AC3 | R2、D1-S2 | 若执行动作变化，用一条去敏代表性场景验证该步骤、原身份／Delivery 保留和后续同身份绑定；历史门禁继续缺失。仅指引变化则复用 #223 正文证据，不重建真实聊天或逐一重跑全部原生入口。 |
| AC4 | R1/R2 | 原 owner 同步后执行受影响 package、分发和 dogfood drift 定向检查，处理实际 sidecar 并说明未验证边界。 |

当前没有用户范围未决项。Author/Architecture 已将具体缺口收敛为原 Branch 的显式工作区恢复关联 profile；可执行合同和验证计划见 design 第5–8节。任何实施／测试／安装通过结论均待实际执行。

## 7. Canonical 引用与本轮差额

- 需求／行为：#773 全文和 Task 整体 PRD 第4–7节。本批完整承接已接受范围，不新增业务义务。
- 设计：`trellis/skills/guru-team/packages/guru-establish-task-branch-binding/SKILL.md`、Identity／Ensure／Bind 的现行合同及 `runtime/task_lifecycle/branch_resolution.py`。差额为共用诊断、原 owner 恢复指引和显式工作区恢复关联；方案见 design 第4–7节。
- 测试：Branch 包 `tests/test_contract.py` 的成功、只读、恢复覆盖。差额为缺失 Task 诊断，以及执行动作变化时的一条代表性恢复验证。
- Architecture：`.trellis/spec/workflow/architecture-baseline.md` 所定位的原 Baseline owner、`docs/architecture/` 当前权威及 `.trellis/spec/workflow/skill-package-contract.md` 的公共 I/O／私有状态边界。独立 candidate_assessment 为 architecture_impact/target_native；本目录贡献及 ADR 保持 proposed，不写共享基线。最终方案仍须独立 final_plan。
