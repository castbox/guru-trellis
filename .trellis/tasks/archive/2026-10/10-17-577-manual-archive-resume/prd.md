# #577 支持旧格式人工归档任务恢复执行

## 目标与权威

唯一 Direct Source 为 [Issue #577](https://github.com/castbox/guru-trellis/issues/577) 的完整正文：问题与目标、两仓职责与依赖、必须满足的行为 1–7、验收条件 1–6、非目标与副作用边界。没有另行选定的规范性设计来源。配对公共能力见 [Trellis #46](https://github.com/castbox/Trellis/issues/46) 和 [PR #52](https://github.com/castbox/Trellis/pull/52)；关联交接用于核验公共合同与候选，不替代本仓实现或联合验收。

支持用户从完整匹配来源启动独立维护，将人工历史归档恢复为同一 Task 的当前执行。人工历史归档仅保留历史，没有正式 Completion、Closure、Finish，也没有待恢复收尾事务。保留原身份、来源、历史范围、规划和交付事实；恢复成功只证明当前任务可以续接。

开发基线为 `main@ef0fcdf0c3746e6d84f97732b9ab776a4bf7703e`。上游可审查源码为 `a06b1f764f003001b35fe125177203211fb2152c`，最终 PR HEAD 为 `28fcf4c611d197903b64b818fe9bd4fea7040b3e`，merge 为 `7bcbeaad31380e7a29c97898cb947c6120a61775`。其配对包仍标为 `0.7.0-castbox.4`，属于未发布候选；必须核验实际 source/build/API，不能按同版本标签推断能力。现有正式 source lock 的采用不由该标签自动决定。

## 整体要求

| 编号 | 必须满足的行为 |
| --- | --- |
| R1 | AI 读取显式选定归档、人工收尾说明、真实 Git/GitHub 交付事实、当前来源、原绑定和未完成责任，判断继续原任务的意图及最早实际 owner。身份或来源不唯一时暂停该写入。只读继承副本只用于确定归属。 |
| R2 | 复用 `guru-maintain-legacy-task` 及现有 Identity、Bind、continuation。入口不依赖目标旧 dispatcher、当前会话绑定、新 parser/Identity/Continuation/Reconcile 预先成功，也不要求手动搬移归档。受支持格式、原归档/活动记录关系和 generation 规则采用上游公共模型。 |
| R3 | 人工历史归档由独立检查、转换和恢复路径承接；当前 schema 且正式 Finish 的归档仍由原 Reactivate 承接，包括其合法人工 Cleanup；未完成 Closure/Finish 或旧 Finalizer 残留返回原事务恢复或既定人工处置。不得放宽正式 Reactivate 前置或补造 Completion/Closure/Finish/Cleanup/seal。 |
| R4 | 写集只含选定 Task、必要规划投影、明确关联 session/binding 与本次操作恢复状态。保留可读原归档和转换来源，保护无关 dirty/untracked、其他任务/会话/checkout。所需工具安装由独立升级 owner 审查其写集和数据兼容，不强制转换其他任务或清理资源。 |
| R5 | 由公共恢复结果返回的原 TaskId/generation 建立当前路由，原归档仅作历史查询和溯源，不能成为第二个当前 authority。原交付 owner 核验历史 PR/commit/归属，缺失事实如实保留。旧 gate 不产生当前 pass。scope 补差交原 Clarify，历史 scope 仍保留；仅真实新切片创建 Delivery，补证据/验收不创建空 Delivery。 |
| R6 | 普通重试、输出丢失、部分写入及回退沿用同次 operation 和已分配身份，不额外推进 generation 或重复导入历史。回退限定原写集并保护后续工作。source stale、身份冲突、工具/数据不兼容给出具体原因、原 owner、缺失输入和恢复入口，不循环重装或覆盖新增工作。 |
| R7 | 用目标 checkout 自身原生入口核验同一 TaskId/generation 与真实 session 或合法 explicit-task 路由，再调用下一实际 Guru owner。分别报告工具可用、数据转换、历史保留、会话恢复、原生续接、业务完成。外部代执行、JSON/DTO 检查或上游通过不能代替联合成功。 |

## 验收责任

| 编号 | 可观察结果与范围 |
| --- | --- |
| AC1 | 一个代表性隔离旧安装样本包含人工旧归档、原规划和交付历史且无 Finish seal。经独立维护恢复后，目标原生 continuation 和下一 Guru owner 承接相同 TaskId及公共结果 generation；当前路由唯一指向活动记录，原归档/转换来源可读。覆盖 R1/R2/R4/R5/R7。 |
| AC2 | 历史已交付与当前补差共存。真实历史保留，scope 变化进入原 Clarify，当前工作从实际阶段续接；没有替代任务、空 Delivery 或继承旧 gate pass。覆盖 R1/R5/R7。 |
| AC3 | 正式 Finish/合法人工 Cleanup 的 Reactivate、旧活动转换、仅历史保留、独立完整 Plan2 保持原语义；未完成 closeout 回原事务。覆盖 R2/R3。 |
| AC4 | 缺证据、不支持格式、身份歧义、stale/mismatch和依赖缺失返回具体 owner/缺失输入/处理路径；只读入口不要求预修绑定或手动搬移，不改未选定资源。覆盖 R1/R2/R4/R6。 |
| AC5 | 定向验证同操作重试、丢输出恢复、普通部分写入和回退；身份、generation、历史导入、原写集及兼容组合保持，其他任务/会话/checkout和后续工作保留。覆盖 R4/R6。 |
| AC6 | 核验实际配对 source/build/API，分别提供 canonical/dogfood/installed、声明平台、reapply/drift、sidecar与目标 native 结果。最多一个代表性旧安装拓扑，不承担累计多平台 Release 矩阵。覆盖 R2/R4/R7。 |

## 非目标与完成边界

不修改实际 CMS 或其他业务任务，不跨仓实现公共模型/转换/恢复/updater，不直接改 Task 状态，不修改全局 CLI 或 `node_modules`。不创建通用任意旧格式恢复框架、人员身份或 workspace mapping，不升级全部 worktree、不发布版本或隐式清理资源。不扩大为攻击/伪造、锁/TOCTOU、并发压力、非常规 crash hardening。

Trellis 拥有公共检查、转换、恢复、session/binding、同操作恢复与回退；Guru 拥有意图与范围判断、历史交付核验、原私有 owner 限定维护、工具编排和联合下一 owner 验收。缺少公共能力时仅继续独立只读核查与合同设计，暂停依赖写入和成功声明。本 Task 必须完成 AC1–AC6、当前工作流质量与交付/Completion/Closure/Finish，不能以配对 Issue CLOSED 或局部单测替代整体完成。具体方案及来源处置由选定 Delivery 的 design 唯一拥有；DeliveryPolicy 与 DocsSSOTPlan 由其 implement 唯一拥有。
