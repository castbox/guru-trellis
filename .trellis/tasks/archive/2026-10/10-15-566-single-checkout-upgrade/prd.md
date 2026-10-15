# #566 单 checkout 工具升级与独立旧任务维护

## 来源与目标

Direct Source 为 https://github.com/castbox/guru-trellis/issues/566 的“必须满足的行为”“验收场景”和“验证范围与非目标”，本轮修订并回读的更新时间为 2026-10-15T07:50:05Z。来源关系为 exact_source；本任务不以文档存在、工具复制或旧版本号作为安装成功证明。

工具安装升级只处理一个明确 checkout。用户指定路径时优先使用该路径；未指定时按现有基线配置与 dev、develop、main、master、远端默认分支顺序确定分支，再绑定其唯一已注册 checkout。

本轮范围覆盖两层解耦：工具更新与旧任务转换独立；任务迁移/历史收尾入口与目标旧任务的运行时独立。基线工具已升级而旧任务无法启动或 Reconcile 时，仍须能从完整匹配新版来源进入维护能力。

## 需求

- R1：显式 checkout 是唯一工具更新目标，其他 worktree、分支和业务文件不变。执行器不创建安装目标 worktree、不切换分支。
- R2：省略 checkout 时保留既有显式 base/config 优先级及有序候选语义；分支确定后才查找其 checkout。目标缺失、歧义或本地修改冲突给出具体诊断，不降级到低优先级候选，不扩大写集。
- R3：旧 Task、规划、归档和非目标 checkout 保留原 bytes/modes。工具更新不要求执行 Plan2、不转换旧任务，也不将旧记录或旧 gate 当作新模型当前 authority。
- R4：旧 session/binding 与新运行时不兼容时，明确返回受影响能力和可用的独立迁移/历史收尾入口，不产生未分类 internal_error 或重新安装循环。共享状态不因单 checkout 工具升级被转换或清理；工具升级成功不代表原业务会话恢复。
- R5：通过真实目标的工具安装、原生入口及重复 apply 验证后才报告安装成功。正常写入失败后的恢复与回退仅覆盖工具写集，保留新业务工作；暂存检查不能替代目标检查。恢复/回退后必须保持受支持的兼容工具/数据组合；后续迁移或业务工作使单侧回退不兼容时，阻塞该回退或另行审查组合恢复范围，不静默扩大写集。
- R6：Guru 拥有目标选择、工具升级语义和自身受管资产编排；Trellis CLI/Core 拥有公共模板、Task/Delivery 与 session 解释及升级执行。不得复制公共迁移算法、修改全局包，或通过先写新 declaration/.version 获得原本不适用的预检例外。
- R7：原 Plan2 迁移、same-plan resume/rollback 保持独立语义。公共 Skill I/O 的变更必须有明确迁移合同；范围判断留在 Markdown/AI，脚本只执行和验证确定性事实。
- R8：独立维护从完整、匹配且可验证的新版来源加载，可使用已升级的基线 checkout 或固定完整工具包，并显式指定旧任务 checkout；discovery 文案不是完整执行包。入口不依赖目标旧 dispatcher，不要求旧任务先通过新版 Task parser、Identity、Continuation 或 Reconcile，也不要求先合入新版基线才能取得维护工具。
- R9：AI 读取真实旧任务、原始绑定、交付和待补责任，判断继续开发、补验收、迁移后收尾或仅历史保留。脚本不根据旧 status、PR 已合并或旧 gate 自动推导新生命周期成功。
- R10：迁移以选定 TaskId/generation 为单位，保留身份、来源和 accepted scope；可只读检查同一 Task 的继承副本来确定唯一归属，不能因此转换其他任务或全部 worktree。任务转换写集只包括目标任务、必要规划投影及明确关联的 session/binding。需继续执行且目标工具不兼容时，调用独立安装操作，将工具写集显式纳入组合操作审查；不更新其他 checkout。仅历史收尾不要求为归档升级目标工具。
- R11：历史交付由原发布/合并 owner 核实真实 PR、提交、候选与归属；旧 gate 不自动转为当前 pass，外部待补验收保留。无需执行新模型的旧任务可独立历史收尾，不为归档制造新 Delivery 或 Completion/Closure/Finish 成功。归档实际持久化且可读取后，准确退役选定旧任务关联的 active session/binding，并以正常原生上下文验证其不再被选为当前任务；保留 TaskId、历史、外部责任及其他任务/会话，不自动清理 worktree/branch。
- R12：需要整合基线时，预先审查新基线、工具变化、任务转换的组合候选、冲突和续接位置；展示准确写集及基线整合副作用后执行。维护不依赖预先完成正常 Reconcile，也不能代替 Reconcile 的业务差异判断或生成其通过结果。
- R13：固定本次候选及已生成身份，普通重试和结果恢复沿用同次迁移，不重新生成 DeliveryId 或重复导入历史交付。备份、写入失败后的恢复和回退仅覆盖本次写集，保留后续业务工作，并验证恢复后的工具/数据组合兼容性；不兼容时按 R5 阻塞或另行审查组合恢复范围。
- R14：需继续执行的任务迁移后核对实际 Task、规划、绑定，以及目标 checkout 自身正常原生入口在受支持的兼容工具/数据组合下的 continuation，并调用下一位实际 owner 验证续接；外部新版工具代执行不构成恢复完成。分别报告工具可用、数据转换、会话恢复、历史交付恢复与业务完成；JSON 解析、context 打印或业务测试不能替代维护闭环。

## 验收

- A1：显式目标优先；未指定路径时分别验证 dev/develop/main/master/remote-default 解析；当前分支与 checkout 可用性不改变候选顺序。
- A2：多个 worktree、目标含合法旧 active/archived Task 和 session 的代表性旧安装，只更新选定 checkout 的工具；旧记录、共享业务控制状态和非目标 checkout bytes/modes 不变。
- A3：新安装运行时必须实际服务当前新任务能力；读取旧 Task/session 时给出明确待迁移诊断，旧记录不产生当前生命周期或 gate。
- A4：同一真实目标安装、重应用、原生入口、普通本地编辑冲突与有限恢复/回退分别提供结果。安装成功、任务迁移、业务恢复分别陈述。
- A5：执行定向 package/runtime、canonical/dogfood/installed、声明投影、reapply/drift 和 sidecar 验证；最多一个代表性旧安装，不扩张完整 Release 矩阵。
- A6：基线 checkout 已升级，旧任务 checkout 尚未合入新版工具，正常续接/Reconcile 被格式拒绝，但 Git 候选无冲突。从完整新版来源进入只读维护准备不依赖预先修改旧任务或合入基线；后续按审查的限定写集转换/整合，必要工具升级独立执行并纳入组合审查，最终由目标 checkout 自身正常原生入口验证真实续接。
- A7：无需继续执行的旧任务（历史样本 CMS #1）独立历史收尾，保留已交付事实和未完成外部责任，不制造新模型通过结果或强制全仓转换、升级目标工具。归档可读后准确退役选定旧绑定，正常原生上下文不再选择旧任务，其他任务/会话及 worktree/branch 保留。
- A8：已合并但待补验收任务（历史样本 CMS #4），迁移后身份、规划和历史 Delivery 正确，当前 gate 不自动通过；下一位实际 owner 进入待验收路径，不凭空选择新 Delivery。
- A9：固定候选重试、结果丢失恢复、普通写入失败恢复与回退保持同一迁移身份，保留后续业务工作；非目标任务和 checkout 不受写入影响。覆盖“安装工具 → 迁移任务 → 请求工具回退”的正常顺序：单侧工具回退不兼容时阻塞或另行审查组合恢复范围，执行后的组合必须兼容。

## 范围与依赖

本任务实现单 checkout 工具升级、独立任务迁移和历史收尾能力，修改 Guru canonical Skill、确定性编排、必要 schema/投影、文档与定向测试。实现能力与实际业务数据处理分开：真实业务仓库安装/迁移/收尾、原安装会话、全局 CLI、全 worktree 更新、跨仓实现、提交/push/PR/merge/发布与清理均不在本轮写集。

现有 CLI 的首次 legacy→Delivery 切换会由 `preflightDeliveryWorkflow` 要求迁移；`preservedHistory` 只适用于已经存在 installed Delivery declaration 的安装。正式 tools-only 模板更新、独立单任务维护入口、匹配的 CLI/Core 和旧记录原生诊断需逐项核实 owner/prerequisite；Guru 不能仅跳过安装诊断，也不能用临时手工脚本声称通用维护已交付。共享 runtime pointer 的实际影响范围也必须审查。

CMS #4 的限定写集手动迁移和 CMS #1 的人工归档是当前需求证据，不是本任务对原业务数据的写入许可，也不证明通用正式入口或真实验收完成。原先仅针对工具升级候选的 Architecture 判断不能代替本轮扩大后候选的 fresh assessment。PRD 已同步当前 Issue 的目标原生运行时、历史收尾终态与组合回退兼容性要求。任务保持 planning；Author 已基于当前独立 candidate assessment 写作 design/implement。Wording、final Architecture 与 Planning Approval 仍须消费当前文档；尚未进入实现。

本轮尚无额外 normative source design；Issue #566 的 owner 与兼容性条款属于当前约束。未来 design.md 独占来源设计处置，不在本 PRD 写入设计批准结论。


## 上游候选与当前规划输入

本轮重新回读 Issue #566，updatedAt 仍为 `2026-10-15T07:50:05Z`；配对 Trellis #40 为 `2026-10-15T08:04:48Z`。需求范围没有扩大。#40 已在隔离工作树完成本地实现及原生/打包验证，尚未提交、发布或进入 Guru source lock。

实际可消费候选是匹配的 CLI/Core `0.7.0-castbox.3` 本地包，不是同版本号的任意 npm 包。公开入口为 `trellis maintain` 和 CLI root `maintenance` namespace；能力版本 `maintenance_api=1.0`，独立 operation kinds 为 `tools_install`、`task_conversion`、`legacy_closeout`。Core 提供显式 `/task/maintenance` 子路径。包 SHA-256：CLI `eb6cdff3fac92079a174469c04366e0cc004fb670fc0fa26dd6a252dc0caef8f`；Core `156ea541c68cf941ef1b11d3304031658276944e74db11b19423bccfdee28425`。源基线 `dde5f90903e9299236e3574d4dfab6441daec09d` 本身不包含未提交实现，不能以该 SHA 声称候选可重建。

上游候选覆盖显式 checkout、只读准备、固定 operation/recovery、旧任务正向识别与投影、精确旧 carrier 退役、真实目标原生入口、Task 目录链接及不兼容工具回退阻断。其通过结果只证明公共层 fixture/package；Guru 受管资产、原私有 owner、runtime pointer 影响、团队续接及本 Issue 联合验收仍须本任务证明。Guru 当前正式 source lock 不因此改变；既有 `source_locked` 和仅供隔离开发验证的 `local_candidate` 边界继续适用。正式来源尚无包含该能力的固定提交时，真实 source-locked 安装必须给出缺少前置的诊断，不能把本地候选变成正式来源证明。

本轮从 Author initial_review 续接，已评估机制候选并写作 design/implement；当前 Task 仍为 planning。本地上游能力与文档存在都不代表 Guru 规划批准或进入实现。
