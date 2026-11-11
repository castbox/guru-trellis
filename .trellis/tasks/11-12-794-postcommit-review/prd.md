# #794 提交后一次独立完整语义审查：整体需求

## 1. 来源与术语

| 来源 | 角色及用途 |
| --- | --- |
| https://github.com/castbox/guru-trellis/issues/794 ，完整正文、行为要求1–7及最小验收；当前无评论 | 唯一 Direct Source，定义本 Task 的全部行为与边界 |
| `trellis/workflows/guru-team/workflow.md`；`.trellis/spec/workflow/workflow-contract.md` 的 Phase 2/3、Candidate Applicability And Coverage | 当前行为证据，以及保留的全局职责、独立性和覆盖约束 |
| `trellis/skills/guru-team/packages/guru-check-task/SKILL.md`、`guru-review-branch/SKILL.md` | 原 Check 九维职责、固定区间独立审核和后继审查责任的当前证据 |
| `AGENTS.md` 第2、3、6、9、10节及 AI-first 原则 | Markdown 语义 owner、确定性脚本、验证范围和副作用约束 |

Check 是现行提交前完整质量门禁；Branch Review 是现行提交后独立区间审查。目标链只进行一次实现后的独立完整语义判断。工程自检、Planning、文档原 owner、Delivery Review、Publication、Completion、Closure、Finish 保留各自职责。

## 2. 背景与问题

固定起点为 `origin/main@4d565c97b5abf634d76ede2d18eed0a57f13bb76`。现有链包含 candidate Check、Architecture/RDT final integration、final Check、本地提交后的 Check 接续和独立 Branch Review。early Draft 另有完整 Check 前发布入口。现有工程结果采用和增量覆盖复用尚未合并这些门禁；不把现状概括为每次固定三次 Check。

同一未变候选因阶段转换重复完成完整语义审核。直接删步骤会留下知识晋升、TaskCommit、上游 Delivery gate、发布和恢复消费者仍要求旧结果的问题。

## 3. 目标与非目标

目标链为：实现和工程自检 → 必要文档整合 → 明确副作用边界内的本地提交 → 未参与实现的新独立审查者对固定候选完成一次完整语义审核 → 原 Delivery Review/Publication。

本 Task 覆盖合并审核、必要消费者、公共合同版本迁移、正常后继与 base 集成、受支持在途恢复，以及 canonical/dogfood/受影响平台同步。它是 #736 的独立拆分项，不以 #736 整体完成为前置。

不实施 #734；不承接预算、消息额度、设备治理、事故重放、qualifier 条件化、按步上下文、一次身份解析、Delivery Review/Publication 合并或归档并入业务 PR。保留 Completion、Closure、Finish 的真实终态责任。不引入固定审核轮数、通过计数、评测框架、成本指标、审计账本或无直接 consumer 的 DTO。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、条件与动作 | 可观察结果 |
| --- | --- | --- |
| S1 首次候选 | 实现者在 Planning 批准后完成实现、工程验证及原文档 owner 整合，再提交 | 无须独立 candidate/final Check 即可合法整合文档和提交；提交不宣称语义通过 |
| S2 独立审核 | 新独立审查者接收固定提交区间和真实工程结果 | 审核期间不改候选；一次覆盖全部适用职责，通过前无 push/PR |
| S3 修复后继 | 原 owner 修复当前 finding，形成后继提交 | 仍独立的原审查者可继续；保留可核验覆盖，审核差额及影响；无法界定影响或覆盖丢失时补足完整审核 |
| S4 base 集成 | 原 Reconcile/审查 owner 审核 Task 内容与 base 的实际集成 | 可采用 base 已审核的无关内容；caller 不缩减固定区间，冲突解决及集成影响不遗漏 |
| S5 在途升级 | 原 owner 读取旧 Check/Branch Review/early Draft 的实际阶段和操作结果 | 按明确版本边界继续、恢复或处置；不静默把旧 pass 变成新审核结果，不重复已完成外部动作 |
| S6 审查后交付 | 独立审核已通过，原发布 owner 评估真实候选 | 保留 readiness；披露交付、剩余责任和未验证范围，按原边界确认发布和 merge |

## 5. 行为要求

### R1 工程结果与文档整合

实现者先完成实现、必要 RDT/Architecture 候选及晋升、测试、静态检查和 diff 检查，给出真实工程结果。保留 Planning 批准和原文档 owner 的必要职责。调整当前晋升依赖 candidate Check 的前置及消费者，使文档整合可合法完成，不制造循环。自检不冒充独立语义通过。

### R2 固定提交与独立性

在原明确副作用边界形成本地提交后，由新开的、未参与实现的独立审查者审核固定区间。审查期间不修改该候选。需修复时由原 owner 修改并提交后继候选。

### R3 完整职责合并

将 Check 与 Branch Review 的全部适用语义责任收敛到该次审核，不保留独立重复 Check 门禁。审核需求/设计承接、实现与测试有效性、必要消费者、减法优先、可维护性、删除/替换/合并及兼容约束。实现后的独立架构影响判断在本次完成一次，保持原必要读取顺序。Planning 架构判断及后续实质变化的刷新继续有效。

### R4 完整区间与 base 集成

审核本 Task 改动及与 base 的集成结果。只有原 Reconcile/审查 owner 判断归属后，才可采用 base 已审核的无关内容。caller 不得自行缩区间；冲突解决和集成影响必须进入覆盖。

### R5 工程采用与后继覆盖

先判断原工程结果适用性；适用则采用，只补新增、失效输入及具体缺口。后继候选可由仍独立的原审查者继续。保留可核验原覆盖，补审实际差额及影响范围；影响无法界定或覆盖丢失时补足完整审查。不承诺只看新增行。

### R6 发布及 early Draft 迁移

独立审查通过前不 push、不创建 PR。显式迁移或退出现有 early Draft 路径，保留原支持在途操作的恢复/处置，不静默切换旧语义。审查后由原发布边界判断 readiness，披露实际交付、剩余责任和未验证范围。本项不合并 Delivery Review 与 Publication。

### R7 公共合同和全体消费者

Planning 确定实际承载合并审查的原 Skill。完整迁移 Check/Branch Review 出口、upstream Delivery gate、TaskCommit 前置、知识晋升、架构消费、发布/回退及必要恢复。实际变化的公共 id、schema、命令、typed exit 及消费者提供版本和迁移合同；不以删 Markdown 或生成空白 pass 代替迁移。

## 6. 约束与依赖

复用已交付 #713 的公开调用及必要恢复能力；只有具体缺失依赖阻塞依赖它的工作。#793/#792 是实际前序交付，不在本项重复交付。Markdown 与原 AI owner 判断语义；脚本仅查询、执行、投影和校验确定性事实。不持久化用户授权，不扩张到恶意伪造、攻击、竞态压力或非常规 crash 加固。

沿原安装 owner 同步 canonical、dogfood 和实际受影响的声明平台，包含 Codex 与 Claude Code。保留用户内容、Task/session 和 `.new/.bak`。执行受影响定向验证；本项不承担完整多平台 upgrade/Release 矩阵。没有业务服务、数据库或部署配置需求，不新增这些资产。

## 7. 可观察验收与验证方式

| 验收 | 对应要求/场景 | 验证入口与预期 |
| --- | --- | --- |
| AC1 | R1–R3、S1/S2 | 经真实公开入口完成工程自检、文档整合和本地提交后进入固定候选独立审核；同一未变候选无独立重复 Check，完整语义责任未丢失 |
| AC2 | R2/R6、S2/S6 | 未通过候选的正常发布调用不产生 push/PR；通过后仍执行原 readiness 和发布边界 |
| AC3 | R4/R5、S3/S4 | 定向执行修复后继、工程结果采用、base 集成与覆盖丢失分支；采用适用证据，刷新实际变化，保留冲突及影响覆盖 |
| AC4 | R6/R7、S5 | 通过旧 gate、已提交、early Draft 已执行/未完成操作的受支持输入验证迁移/恢复；不造新 pass、不重复远端动作 |
| AC5 | R3/R7、全部场景 | 原审核 owner 核对完整职责、必要读取顺序和真实生产者→消费者；公共 schema/出口/命令版本边界与实际调用一致 |
| AC6 | R7、全部场景 | 定向 package/runtime、source/installed、受影响平台、reapply/sidecar 和 dogfood drift 验证通过；必要时仅一个代表性 clean throwaway，明确未验证边界 |

命令结果只证明其执行范围，不替代实际独立语义审核。整体完成仍须业务 Delivery、Task Completion、Closure 和 Finish 的原责任。

## 8. 实际未决项

没有阻塞整体需求写作的产品问题。具体原 Skill 承载、上游 gate 的合法迁移、知识晋升前置和在途兼容机制由后续 Delivery Author/Architecture 研究并写入方案；它们尚未获得 Planning 批准。
