# Codex Guru Skill 共享目录迁移整体需求

## 1. 来源与术语

| 来源 | 定位 | 角色与用途 |
| --- | --- | --- |
| Direct Source | https://github.com/castbox/guru-trellis/issues/724 全文，2026-11-03 更新 | 本 Task 的完整需求与验收权威 |
| 公共分发合同 | .trellis/spec/workflow/skill-package-contract.md 的 Distribution And Managed Hashes、Instruction-Only Standalone Packages | 公共投影、私有资产和平台适用性约束 |
| 安装合同 | .trellis/spec/preset/installer.md | 安装 owner、受管来源、冲突和重试约束 |
| 官方发现机制 | https://developers.openai.com/codex/skills/ | Codex 从仓库 .agents/skills 发现 Skill 的外部依据 |
| 平台历史 | .trellis/tasks/archive/2026-09/09-20-452-all-platform-support/design.md 第3、5、7节 | exact target platform selection 的历史约束 |

公共投影指 Agent 可发现的既有公开文件集合。完整执行器与私有 runtime 由 .trellis/guru-team/ 管理。Codex 专属编排包的物理目录变化不改变其 platform_destinations 或原生能力前置。

## 2. 背景与问题

main 基线为 42ffd32d70be3859a4493e084464738473c45dd6。当前共享 Guru Skill 同时出现在 .agents/skills/ 与 .codex/skills/。仅适用于 Codex 的编排包仍只分发到旧 Codex 目录。重复目录增加同步、发现和校验成本。

本 Task 要把 Codex Guru Skill 的项目级发现统一到 .agents/skills/。目录存在、静态扫描或本聊天清单不能证明宿主已经调用 Skill。

## 3. 目标与非目标

整体交付包括新装、reapply、已有安装迁移、专属包及元数据承接、平台选择变化、manifest/drift、当前文档和测试，以及规划所选客户端分组的 native 发现与真实调用证据。

不删除整个 .codex/；不改变其配置、Hooks、agents 和 prompts 职责；不迁移 Claude、Cursor 的平台 Skill 目录；不更改公共 Skill id、行为或出口。不清理用户级、第三方或上游 Trellis 拥有的文件。不接管完整多平台 Throwaway 或 Release Gate 矩阵，不承诺所有历史或未来 Codex 版本兼容。

Task Completion 负责所有行为与必需 native 证据；交付切片合并本身不证明整体完成。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前提与触发 | 处理与可观察结果 |
| --- | --- | --- |
| S1 新装/reapply | installer，选择包含 codex 的平台集合 | 安装所有适用公共 Skill 及专属包到共享目录；不新建受管旧 Codex 投影 |
| S2 已有安装升级 | 原 upgrade owner，目标已有受管旧投影 | 先完成目标公共投影，再移除未修改的旧受管文件 |
| S3 冲突及重试 | 用户在旧目录或目标目录修改文件，或存在来源不明文件 | 保留内容并走原冲突处理；目标冲突解决前保留待迁移旧副本；正常重试完成同一迁移 |
| S4 平台选择变化 | 目标集合增加或移除 codex | 按适用性安装/退出专属包；共享包、其它平台副本和用户文件按原受管规则保留 |
| S5 宿主调用 | 规划所选真实 Codex 客户端，目标 Skill 无旧副本 | 从共享公共投影发现并经原公开入口调用公共包和专属编排包，观察合法出口 |

## 5. 行为要求

- R1：规划依据当前声明、官方文档和实际入口确定 Codex 客户端、版本及发现机制分组。相同机制须有代表性依据；不同发现行为的受支持入口须有定向证据。发现真实宿主依赖旧路径时，记录宿主、版本和依赖证据，完成兼容承接后再移除其旧投影。
- R2：新装及 reapply 后，Codex 从 .agents/skills/ 发现和调用适用 Guru Skill；installer 不再生成受管 .codex/skills/guru-*/。
- R3：升级沿正式 owner 及目标安装的 exact platform selection 执行，不从 source checkout 的选择推断。只移除来源明确且内容未修改的旧受管文件。原迁移 owner 确认目标公共投影完整后才移除旧文件。
- R4：旧目录与目标共享目录中的用户修改、来源不明文件均保留并沿既有冲突机制处理。不能以旧副本或 canonical 内容直接覆盖目标冲突文件。目标冲突解决前保留仍需迁移的旧受管副本。保留旧文件造成重复发现或存在未解决冲突时，不得报告迁移成功。重试及 reapply 不恢复退役投影。
- R5：选择包含 codex 时，将 guru-orchestrate-issue-dag、guru-orchestrate-issue-sequence 等专属包公共投影与 agents/openai.yaml 安装到共享目录。未选择 codex 时不因共享目录始终存在而新增这些包。物理目录收敛保留平台适用性、显式调用策略和 Codex 原生能力前置，不扩张为其它 Agent 支持承诺。
- R6：选择从包含 codex 缩减为不包含时，按原受管规则退出仅适用 Codex 的公共投影，保留其它所选平台仍需的共享包、其它平台副本及用户修改。包含 codex 的多平台安装在共享目录只保留一份受管投影。
- R7：共享发现目录只包含既有公开文件集合与本次迁移所需公开元数据。执行器、私有 runtime 和运行证据沿原 owner 合同管理。package-private tests/ 留在 canonical 源，不进入安装 runtime 或发现目录。
- R8：同步平台描述、installer、upgrade-tools、受管 manifest、drift、当前有效文档及测试的旧路径假设。退役路径不再被旧 owner/validator 视为必需。不可变版本与历史归档保留原记录。
- R9：保留 .codex/config.toml、.codex/agents/、.codex/hooks.json、.codex/hooks/ 和 .codex/prompts/ 职责，并保持 Claude、Cursor 分发及公共 API。

## 6. 约束与依赖

使用既有 canonical source、完整 preset、安装/升级 owner 和公共投影 allowlist。遵守诚实协作正常场景边界，不新增攻击模型、锁、竞态压力或 crash consistency 机制。用户修改保护属于已明确要求的正常冲突行为。

native 验证使用真实宿主与原公开入口，满足适用前置并观察合法出口。不得用模拟加载、扫描、聊天注入清单替代。验证不要求执行真实业务仓库的编排、发布或生产写入。外部能力缺失时保留对应验收未验证，不能宣告 Task 完成。

本 Task 无数据库或业务数据迁移；迁移对象是目标仓库中由 Guru 管理的项目级公共 Skill 文件及其受管记录。

## 7. 可观察验收与验证方式

| 验收 | 要求/场景 | 入口、输入与预期证据 |
| --- | --- | --- |
| AC1 | R2、R5、R7；S1 | 一个代表性 Codex clean 安装：共享公共文件、内容、可执行位和元数据完整；无受管旧目录、私有 runtime、tests 或私有证据泄漏 |
| AC2 | R3、R4；S2、S3 | 正式升级及定向测试覆盖目标完整后移除旧文件、两端用户修改和来源不明文件保留、目标冲突时保留旧副本、冲突处置后重试及 reapply 不复活；manifest/conflicts/removals 与磁盘一致 |
| AC3 | R1、R5；S5 | 按规划分组记录真实宿主、版本、发现入口、原公开调用与合法出口；目标 Skill 无旧副本，证明使用共享公共投影；公共与专属包均有证据 |
| AC4 | R5、R6、R9；S4 | 定向测试覆盖增加/移除 codex、非 codex 安装、含 codex 多平台去重，以及其它平台副本、配置、Hooks、agents、prompts 和用户文件保留 |
| AC5 | R8；所有场景 | 当前文档与实现一致，平台投影/drift 检查通过；退役路径不再作为必需。报告实际开箱安装和 update/upgrade 覆盖边界 |

完整多平台发布矩阵属于排除范围，其缺失不构成本 Task 阻塞。AC3 所需 native 证据缺失仍阻塞对应验收和整体完成。

## 8. 实际未决项

需求阶段没有未决产品或范围选择。客户端分组和迁移具体机制由 Delivery Author 与独立 Architecture assessment 在规划阶段确定；实现和所有验收均尚待执行。

