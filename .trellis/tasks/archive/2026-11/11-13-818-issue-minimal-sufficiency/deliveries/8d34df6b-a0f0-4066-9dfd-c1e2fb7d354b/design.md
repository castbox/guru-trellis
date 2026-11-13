# #818 D1 设计：在原内容规范内收敛方法

## 1. 设计目标、需求承接与内容基线

本设计承接[本批 PRD](./prd.md)的 R1–R4、D1-S1/S2/S3 和 D1-AC1/AC2，覆盖 Task 整体 R1–R4/AC1/AC2。目标是在既有 Issue 正文规范中补足必要性与主次方法，由原 owner 执行；不新增流程节点或裁决机制。

development baseline **B=`fd0ee32618433a92ae934e29afb5b72e7136b4f7`**，来自 Intake 实际采用的固定 `origin/main` Git object。Planning H0 同为该 commit；后续实现 H 由原 Candidate constructor 读取实际 HEAD，不能把 H0 当作实现候选。PR 目标为 `main`，与固定开发 B 分开。D1 没有前序 Delivery。

阶段适用 authority 为 `docs/architecture/README.md` 的 `guru-trellis-architecture/active`、`docs/architecture/00-foundation/design-constitution.md` 的 `guru-trellis-design-constitution-v1/current` 及 `docs/architecture/06-governance/change-contract.md`。独立原 Architecture candidate_assessment 已正式返回 `baseline_current / no_architecture_impact`：此候选沿既有 Clarify 正文与四原门禁完善方法，不改变 owner、public I/O、状态、阶段或运行依赖。该结论不代替 Wording 后的 final_plan，也不证明行为效果或安装采用。

## 2. 当前系统、边界与目标差额

现有 `issue-content.md` 已拥有来源保留、原 Clarify 整理、内容裁剪、完整正文与局部修订、四原 owner 使用及示例边界。四个 SKILL 和三个原合同已经实际引用同一规范。共同 `review-sufficiency.md` 拥有审核覆盖及结束条件；原分发 writer 递归安装完整 package 和 managed spec。

本轮只修改这些现存 Markdown 方法及必要薄引用。将必要性判断放在充分性检查之前，删除不必要要求的派生义务，按完整规则组织正文，保持验收主次。没有脚本语义算法、schema、注册表、公共 DTO 或工作流路由差额。

## 3. 来源设计处置（唯一）

已读 #818 全文、四份固定方法来源和既有 Guru 合同。#818 明确的 Markdown/AI 判断、四原 owner、单一完整定义、无外仓运行依赖、原安装 owner 等约束直接承接；没有用户另行选定的规范性实现方案，故不建立空处置矩阵。

外仓来源只作为方法参考。其动议生命周期、产品 Authority、跨仓发布、业务字段和私有事实均不迁入公共包。共享规则仍由原完整正文拥有，方法出处不变成运行时读取前置。

## 4. 模块、职责与设计取舍

| 原位置/owner | 本轮落点与边界 |
| --- | --- |
| `trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md` | 唯一完整方法正文。在原第2节整理行为中明确先判断必要性及派生义务收敛；原第3节明确核心规则连续表达与验收主次；原第4节说明独立连续阅读后反查来源和入口；原第5节定位四原职责。重写相应完整段落并删除被替代碎片，不用新摘要叠加旧分散定义。来源保留和局部完整性条件继续有效。 |
| 四个 `packages/<owner>/SKILL.md` 及 Clarify/Wording/Readiness 原 `references/contract.md` | 原 Issue Content 段保持完整加载要求，薄引用新方法；执行仍在原写作、措辞、十维 Readiness、创建语义门禁内。不复制方法全文，不增加轮次或确认。 |
| `trellis/presets/guru-team/spec/workflow/review-sufficiency.md` | 在原覆盖形成职责中准确定位 Issue 内容的原共享规范。只承接引用关系，不复制 Issue 规则，也不把 #818 扩成所有审核阶段改造。 |
| 原 preset/tools owner | 从完整 canonical 安装到本 Task checkout，维护 manifest、managed spec、shared/Codex、Claude、Cursor 投影，保留用户内容和 Task/session。安装器算法不变。 |
| 原 RDT maintenance owner | 在 Phase 2 准备本 Task 的完整内容方法差额与必要 R/D/T 关系，提交前整合/readback；Planning 不改共享 current。 |

选择直接修改原正文并同步受影响 consumer。新增 Skill、独立资格流程、语义脚本或另一份共用摘要都会制造重复 authority，且没有新的直接 consumer。仅改入口提示会让原完整正文继续缺少方法。只删字数会遗漏真实保护和适配；均不采用。

当前没有需要新登记的架构职责或依赖关系，因此不创建空 Architecture contribution 或 ADR。若方案实际扩大 owner、状态、public I/O 或依赖，先回原 Architecture 与受影响 Author，不沿此结论继续。

## 5. 接口与数据

现有入口保持：原 Issue/draft 输入 → 加载原 `issue-content.md` 和写作规范 → 各自原语义门禁 → 原 typed exit/consumer。Clarify 的正文/评论动作、Wording 的完整 title/body scan、Readiness 的十维和 Create Issue 的已审内容核对/回读不变。

本轮没有新增字段、存储、schema、CLI 参数或跨 Skill handoff。无数据迁移或新版本 reader；Skill id、文件路径及既有可解析引用保持。四个职责间交付既有最小 DTO，不能把本方法执行过程写入 public output 或授权记录。

## 6. 状态、顺序、正常与失败流程

运行顺序仍属于原 owner：完整读取来源和共享正文 → 在原职责内判断必要性、组织或审核完整规则 → 原语义 Gate → 真实选择/副作用才交互 → 原 recorder/validator → 原出口。

正文已有清楚且充分的规则时保留，不为形式重写。普通扩张由原写作 owner 删除要求及派生义务；普通必要遗漏回原受影响 owner，修后按原刷新和重审路径继续。真实未决需求仍回 Clarify，不把无依据或已排除内容包装成确认问题。

规范或来源不可读、实际源已变或必要事实缺失时，按原 missing/stale/恢复合同停止依赖判断；不能用旧摘要补出 pass。无状态机或新的失败分类。

## 7. 恢复、兼容、迁移与集成

正文直接演进，不建立旧新双读或适配层。完整 matching provider 的既有安装 owner 更新 managed copy；旧安装只有实际更新后才采用新规则。明确的 public I/O 兼容合同继续有效，没有需要兼容例外确认的新增路径。

正式 Task 已存在，同步使用 `guru-upgrade-tools` 的完整 canonical source 合同及明确本 checkout，不运行普通 apply 绕过历史 Task 前置，不手抄生成副本。逐路径判断 preserve/replace，沿原 owner 处理 `.new`/`.bak` 和同操作恢复；冲突不靠改 hash 消除。当前未提交源码只能按其合法 `local_candidate` 边界验证，不能声称正式 source_locked、Release 或业务仓采用。

新分支、正式 checkout 和 Task 已由原 Creation 建立。后续没有数据迁移或外部系统恢复协议。验证不要求写真实 GitHub 对象；创建/正文编辑/评论、提交、push、PR 和 merge 仍各受原副作用边界约束。

## 8. 验证设计

| 验证 | 入口、输入与独立观察 | 层级与限制 |
| --- | --- | --- |
| V1 写作与修订 | 从现有 brief/revision 教学例和本次真实来源关系形成侧效应为空的请求。明确区分原始要求、未采用建议和当前草稿；包含普通过度要求及派生验收，并保留同源必要保护/真实入口。通过原 Clarify 写作入口观察完整正文。 | 在旧安装和更新后的同一正常入口使用等价输入，保留首轮真实输出。检查删减、主目标与保留语义；不将预期 Finding 注入被测 Agent，不把示例旧结果当当前结果。无需真实创建 Issue。 |
| V2 原审核 | 将正常未完成草稿交原 Wording/Readiness 审核；Create Issue 执行创建前原语义核对，停在外部写入前。审核者独立读正文和来源，指出多余项与必要遗漏，修后观察原适用重审结果。 | 验证原职责的真实 Agent 判断，分开报告各入口覆盖。未实际创建/修订 GitHub 时不得宣称外部回读已验证；原创建 executor 本次无差额，不为补证据制造外部对象。 |
| V3 分发与引用 | 复用 `test_issue_content_distribution.py`，若共同审核规范确有差额，再运行 `test_review_sufficiency_distribution.py`。调用真实 writer，核完整 installed 与声明平台的正文、四入口引用、reapply、用户内容和 sidecar。 | 定向 fixture 证明分发，不证明所有平台 Agent 行为，不等同完整安装矩阵。只在现有资产范围确有缺口时改测试，不能增加关键词自证。 |
| V4 本 checkout 采用 | 原 tools owner 更新、readback、同源 reapply；再运行 source/installed package、upstream ownership、dogfood drift 和本目标 native continuation。 | 分开报告源码、实际安装和原生行为；保留 local_candidate 的 source-lock 限制。不得使用全局旧 CLI 代替匹配 Fork。 |

验证由接受目标的条件、动作和结果派生。先观察旧正常入口，再修改 canonical、验证新输出和受管采用；不普遍要求旧版必须失败或人为回退构造红灯。源和输出足够回答本项问题后停止，不加固定样本数、设备数或完整矩阵。设施失败先判断是否到达业务路径；未到达不能当作行为缺陷或通过。

## 9. Canonical 引用、本轮差额与实际未决项

RDT 读取三层稳定根和原 #153 完整贡献（当前 `.109` 未迁移边界），以及 `docs/{requirements,design,test}/current/review-sufficiency.md`。本轮差额是 Issue 方法职责与验证，完整规则仍在原 canonical package，不在 RDT 复制。原 RDT owner 于 Phase 2 准备本 Task 隔离贡献，并在 `docs/{requirements,design,test}/current/issue-content.md` 承接该能力的完整当前责任、原 R153 别名/来源与新增行为/验证关系；声明本能力对旧 `.109` 定义的精确替代范围，保留旧 Git/贡献历史。只维护实际能力，不迁移整个语料或修改全局索引。原维护判断若发现已有 current 同能力，整合原完整单元，不能并列第二定义。

Architecture 引用本文件第1节三 authority 和实际 candidate_assessment。原 Architecture final_plan 独立复核 Wording-current 正文。现无阻塞产品或方案选择；匹配 Fork CLI/Core 根及 fixture 脚本位置在原 tools owner 预检时核实，不能以全局 `trellis 0.6.17` 代替项目锁定 `0.7.0-castbox.6`。未满足依赖时停止采用及依赖验证，不伪报通过。
