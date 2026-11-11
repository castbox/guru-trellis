# 按各自适用条件加载和调用 qualifier 整体需求

## 1. 来源与术语

| 来源 | 章节／条款 | 角色与用途 |
| --- | --- | --- |
| [castbox/guru-trellis#793](https://github.com/castbox/guru-trellis/issues/793) | 当前完整正文：行为要求、边界与迁移、最小验收；无评论 | 唯一 Direct Source，定义本 Task 完整要求。 |
| `AGENTS.md` | 第2、3、6、7、9、10节 | 仓库约束：AI／脚本职责、最小验证、受管分发与副作用边界。 |
| `docs/architecture/adr/008-solution-mechanism-qualification.md` | Decision | 既有机制 authority 职责，作为兼容约束。 |
| `docs/architecture/adr/020-root-cause-qualification.md` | Decision | 既有因果准入及仍适用结论采用，作为兼容约束。 |

qualifier 指原 `guru-qualify-normal-scenario`、`guru-qualify-solution-mechanism` 和 `guru-qualify-root-cause`。适用条件是原阶段 AI owner 在加载某个 qualifier 全文前判断是否进入该 owner 的条件。仍适用结论是对同一实际对象、authority、机制、条件和证据的有效判断，不是脚本通过或阶段状态。

## 2. 背景与问题

固定调查基线为 `origin/main@e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e`。现有 workflow 在十类候选边界要求 normal／solution 调用。Check 已有空候选不调用，root 已有不变机制结论采用。因此，现状不能描述为每个阶段无条件调用全部三个 qualifier。

剩余差额是：不适用的非空候选仍可能要求全文加载、输入装配和形式化调用；各 caller 的条件、原 Skill 合同、输入及出口承接需要共同收敛。具体条件由 Delivery 规划核对真实 caller 和候选后提出。

## 3. 目标与非目标

目标是在保留正常范围、机制职责和因果证据充分性判断的前提下，按三个 qualifier 各自适用条件加载和调用。整体完成须覆盖实际改变的 caller／consumer、必要迁移及受管投影，不能以删除 global mandatory 文本替代闭环。

不实施 #734、#736 整体或其余拆分项。不承担按步路由／legacy 裁剪、身份解析组合、Check／Branch Review 合并、发布入口合并、归档时序、预算、消息额度、设备治理或事故重放。不新增固定案例数量、成本比例、通用 Agent 评测框架或完整多平台矩阵。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与前置 | 触发及行为 | 可观察结果 |
| --- | --- | --- | --- |
| S1 未触发 | 原阶段 owner 已读当前 authority 与真实候选 | 先读各 qualifier 的适用条件，判断该 qualifier 未触发 | 不加载其全文，不执行形式化空判定；原阶段继续独立判断本阶段工作。 |
| S2 触发 | 真实候选满足某个 qualifier 的条件 | 显式加载原 stable Skill，完成原语义闭环 | 原通过或非通过出口交唯一 consumer；拒绝、修订、诊断、范围选择及 blocked 均有效。 |
| S3 采用 | 同一机制已有仍适用结论 | 仅 caller 或阶段改变 | 采用结论，不重复相同资格判定；仍独立审查本阶段当前工作和证据。 |
| S4 刷新／恢复 | authority、机制、条件或因果证据实质改变，或必要结论丢失 | 原 owner 刷新受影响判断，或恢复／重新判断 | 不以旧结论推进受影响工作，不制造通过或重复副作用。 |
| S5 分发 | canonical 合同已变更 | 沿原安装 owner 同步 dogfood 和实际受影响声明平台 | Claude Code、Codex 等受影响投影一致，必要 drift 检查通过。 |

## 5. 行为要求

- R1：normal、solution、root 在各自原职责中定义清楚的适用条件与 caller 判断落点。caller 在全文加载前可读条件，条件与原 Skill 合同一致。原阶段 AI owner 根据当前 authority、真实候选和变化决定是否触发。关联 S1／S2。
- R2：规划核对真实调用方和候选，说明可省及必须保留的调用。不新增资格判定 Skill、固定问卷或逐候选证明 artifact。不用 OS／内核／进程／文件描述符这一种线索替代全部正常范围、机制和根因判断；不以重命名真实故障／保护机制跳过资格。真实需求或重大风险取舍回原入口。关联 S1／S2。
- R3：触发时显式加载原 stable Skill 并完成其原 semantic 闭环。原拒绝、机制修订、诊断、范围选择、blocked 的意义及唯一 consumer 保持有效；脚本成功不等于语义通过。关联 S2。
- R4：新建或实质改变的事故／保护机制仍进入 root；不变机制采用仍适用结论。阶段或 caller 变化本身不重复相同判断。authority、机制、条件或因果证据实质改变时刷新受影响判断；结论丢失由原 owner 恢复或重新判断。关联 S3／S4。
- R5：同步受影响 caller、workflow mandatory 条件、Skill 合同、输入／出口消费、示例和诊断。保留未受影响资格算法和三个独立 owner，不只删 global mandatory。关联 S1—S4。
- R6：实际改变的公共 id、schema、命令、typed exit 和消费者提供明确兼容／迁移合同，支持在途任务合法恢复。沿原安装 owner 同步 canonical、dogfood 和受影响声明平台。关联 S4／S5。

## 6. 约束与依赖

本项是 #736 第1项的独立修复，正文自足，不以父项整体或其他拆分项完成为前置。采用 #713 已交付公开调用与必要恢复；具体能力缺口只阻塞依赖它的工作，不借机修复整套基础设施。

Markdown 与原 AI owner 负责语义判断；脚本只做确定性查询、投影和校验。不持久化授权信息，不增加审计账本或无直接 consumer 的 DTO 字段。受支持范围是诚实正常路径、普通失误及 stale／mismatch，不扩到恶意伪造、对抗绕过或未要求的竞态／crash 加固。

本项继续执行当前原 Planning、Check、Branch Review、readiness 和发布职责。PR 只面向 main；当前执行段在 merge 前停止，Completion／Closure／Finish 不提前标为完成。创建、提交及远端操作各自保留精确副作用边界。

## 7. 可观察验收与验证方式

| 验收 | 对应要求／场景 | 入口与预期观察 |
| --- | --- | --- |
| AC1 条件触发 | R1／R2／R5；S1／S2 | 从实际改变 caller 的正常入口验证：未触发不要求全文及形式化调用；触发显式进入原 owner。核条件与合同一致，不能仅凭文本删减声称行为成立。 |
| AC2 非通过承接 | R3／R5；S2 | 对真实改变的出口消费进行定向验证，拒绝／机制修订／诊断／范围选择／blocked 回原唯一 consumer，无脚本自动 semantic pass。采用仍适用既有覆盖，补实际缺口。 |
| AC3 采用与刷新 | R4／R6；S3／S4 | 同一未变对象采用仍适用结论；实质变化刷新受影响判断，丢失结论经原 owner 恢复／重判；不因阶段变化固定重跑。 |
| AC4 迁移与分发 | R5／R6；S4／S5 | 检查真实公共合同差额与在途恢复，沿原安装 owner 同步实际受影响投影，运行必要 dogfood drift 及定向 package/runtime／安装验证。 |

验证只覆盖实际改变的 caller／consumer，不要求全阶段乘积矩阵或实际业务事故。测试、静态合同、受管投影和真实 Agent 行为证据分别报告；未验证项不记通过，也不宣称已降低费用。

## 8. 实际未决项

无需要用户补充的需求选择。三个具体触发条件清单、caller 判定落点、薄投影及兼容差额由原 Delivery Author／Architecture 基于当前合同细化，经原规划审查后实施。本正文定义整体责任，尚不代表 accepted_scope、Delivery Planning approval 或 implementation activation。
