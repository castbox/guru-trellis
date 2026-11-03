# D1 Codex Guru Skill 共享目录迁移需求

## 1. 整体来源与术语

本批源于 https://github.com/castbox/guru-trellis/issues/724 完整正文。
整体 accepted_scope 为 .trellis/tasks/11-03-724-codex-shared-skills/prd.md，revision sha256:1bbb7f2d8bed192a28365e6aab0e9068895d6dd80e77e98d6f8929f822cb3f97；scope_ref 选择 AC1、AC2、AC3、AC4、AC5。本批 planning_root 为 .trellis/tasks/11-03-724-codex-shared-skills/deliveries/a831ddba-681c-480a-9eb9-1e350f48a43d。

整体 PRD 第1节拥有来源表和术语；本批实际读取了 Direct Source、公共分发/安装合同和 #452 设计。Issue 行为与兼容约束为要求。官方 Codex 文档提供外部机制依据；旧实现是待迁移现状。设计处置由本批 design 第3节唯一维护。

## 2. 整体与本批目标、非目标

当前 main 在共享目录和旧 Codex 目录重复投影公共 Skill，专属编排包只进入旧 Codex 目录。本批完整承担 R1–R9：使 Codex 统一消费共享公共投影，并完成兼容迁移、平台选择及宿主调用验证。

本批不删除整个 .codex/，不修改公共 Skill 行为和出口，不清理用户级、第三方或上游资产，不改变 Claude/Cursor 发现目录，也不承担完整发布矩阵。整体 Completion 保留全部验收责任。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首次 D1，没有前序 Delivery。开发起点为 main 的 42ffd32d70be3859a4493e084464738473c45dd6，当前实现和测试仍按旧目录运行。尚无实现、native 调用或交付通过事实。

输入是已接受的整体 PRD、完整 canonical preset、目标安装的 exact selection 及旧受管来源。依赖可调用的 Codex 原生入口；本机 CLI 版本为 0.162.1，具体宿主分组由规划说明。若必需 native 证据无法取得，保留 AC3 未验证并继续独立工作；不得以文件扫描替代。

本批结束须提供完整实现、迁移与选择变化验证、一个代表性 clean 安装及分组 native 证据。Task Completion 审查整体义务；合并事实不自动关闭 Issue。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前提与触发 | 处理与可观察结果 |
| --- | --- | --- |
| S1 新装/reapply | installer，选择包含 codex 的平台集合 | 安装所有适用公共 Skill 及专属包到共享目录；不新建受管旧 Codex 投影 |
| S2 已有安装升级 | 原 upgrade owner，目标已有受管旧投影 | 先完成目标公共投影，再移除未修改的旧受管文件 |
| S3 冲突及重试 | 用户在旧目录或目标目录修改文件，或存在来源不明文件 | 保留内容并走原冲突处理；目标冲突解决前保留待迁移旧副本；正常重试完成同一迁移 |
| S4 平台选择变化 | 目标集合增加或移除 codex | 按适用性安装/退出专属包；共享包、其它平台副本和用户文件按原受管规则保留 |
| S5 宿主调用 | 规划所选真实 Codex 客户端，目标 Skill 无旧副本 | 从共享公共投影发现并经原公开入口调用公共包和专属编排包，观察合法出口 |

## 5. 完整行为、条件与约束

- R1：规划依据当前声明、官方文档和实际入口确定 Codex 客户端、版本及发现机制分组。相同机制须有代表性依据；不同发现行为的受支持入口须有定向证据。发现真实宿主依赖旧路径时，记录宿主、版本和依赖证据，完成兼容承接后再移除其旧投影。
- R2：新装及 reapply 后，Codex 从 .agents/skills/ 发现和调用适用 Guru Skill；installer 不再生成受管 .codex/skills/guru-*/。
- R3：升级沿正式 owner 及目标安装的 exact platform selection 执行，不从 source checkout 的选择推断。只移除来源明确且内容未修改的旧受管文件。原迁移 owner 确认目标公共投影完整后才移除旧文件。
- R4：旧目录与目标共享目录中的用户修改、来源不明文件均保留并沿既有冲突机制处理。不能以旧副本或 canonical 内容直接覆盖目标冲突文件。目标冲突解决前保留仍需迁移的旧受管副本。保留旧文件造成重复发现或存在未解决冲突时，不得报告迁移成功。重试及 reapply 不恢复退役投影。
- R5：选择包含 codex 时，将 guru-orchestrate-issue-dag、guru-orchestrate-issue-sequence 等专属包公共投影与 agents/openai.yaml 安装到共享目录。未选择 codex 时不因共享目录始终存在而新增这些包。物理目录收敛保留平台适用性、显式调用策略和 Codex 原生能力前置，不扩张为其它 Agent 支持承诺。
- R6：选择从包含 codex 缩减为不包含时，按原受管规则退出仅适用 Codex 的公共投影，保留其它所选平台仍需的共享包、其它平台副本及用户修改。包含 codex 的多平台安装在共享目录只保留一份受管投影。
- R7：共享发现目录只包含既有公开文件集合与本次迁移所需公开元数据。执行器、私有 runtime 和运行证据沿原 owner 合同管理。package-private tests/ 留在 canonical 源，不进入安装 runtime 或发现目录。
- R8：同步平台描述、installer、upgrade-tools、受管 manifest、drift、当前有效文档及测试的旧路径假设。退役路径不再被旧 owner/validator 视为必需。不可变版本与历史归档保留原记录。
- R9：保留 .codex/config.toml、.codex/agents/、.codex/hooks.json、.codex/hooks/ 和 .codex/prompts/ 职责，并保持 Claude、Cursor 分发及公共 API。

复用整体 PRD 第6节的正常协作、公开文件 allowlist、原 owner 和无生产写入边界。迁移目标是项目级受管文件及记录，不涉及数据库。目标公共投影完整是移除旧受管文件的前置；两端用户修改与来源不明内容均不能静默覆盖或删除。保留旧文件造成重复发现时，不宣称迁移成功。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 入口、输入与预期证据 |
| --- | --- | --- |
| AC1 | R2、R5、R7；S1 | 一个代表性 Codex clean 安装：共享公共文件、内容、可执行位和元数据完整；无受管旧目录、私有 runtime、tests 或私有证据泄漏 |
| AC2 | R3、R4；S2、S3 | 正式升级及定向测试覆盖目标完整后移除旧文件、两端用户修改和来源不明文件保留、目标冲突时保留旧副本、冲突处置后重试及 reapply 不复活；manifest/conflicts/removals 与磁盘一致 |
| AC3 | R1、R5；S5 | 按规划分组记录真实宿主、版本、发现入口、原公开调用与合法出口；目标 Skill 无旧副本，证明使用共享公共投影；公共与专属包均有证据 |
| AC4 | R5、R6、R9；S4 | 定向测试覆盖增加/移除 codex、非 codex 安装、含 codex 多平台去重，以及其它平台副本、配置、Hooks、agents、prompts 和用户文件保留 |
| AC5 | R8；所有场景 | 当前文档与实现一致，平台投影/drift 检查通过；退役路径不再作为必需。报告实际开箱安装和 update/upgrade 覆盖边界 |

完整多平台发布矩阵属于排除范围，其缺失不构成本 Task 阻塞。AC3 所需 native 证据缺失仍阻塞对应验收和整体完成。

当前需求没有未决产品选择。Author/Architecture 在方案阶段细化受支持宿主分组、旧目录退役和冲突重试机制。所有验收仍待执行，尤其 AC3 尚未取得真实调用结果。

## 7. Canonical 引用与本轮差额

| 引用 | 本批用途及差额 |
| --- | --- |
| .trellis/spec/workflow/skill-package-contract.md 的 Distribution And Managed Hashes | 保留公共文件、runtime/test 边界；Codex 公共发现根由旧目录收敛到共享目录 |
| .trellis/spec/preset/installer.md 的平台安装合同 | 沿原安装和受管冲突 owner，补齐迁移先后次序 |
| trellis/presets/guru-team/scripts/python/guru_platform_inventory.py 与 platform_projection_contract.py | 平台描述改变发现根，平台适用性保持 |
| trellis/presets/guru-team/scripts/python/test_dogfood_platform_selection.py | 旧路径断言迁移，补齐专属包和选择变化用例 |
| .trellis/spec/workflow/quality-guidelines.md 的 Validation Scope Ownership、Test And Validation Value | 定向证据和真实 native 调用，完整发布矩阵排除 |
| .trellis/spec/architecture/baseline-usage.md | 定位当前 Architecture/constitution/change-contract，由独立原 owner 评估候选影响 |

当前有效 requirements/design/test 和 Architecture 的详细关联将由原维护 owner 按实际变更承接；不可变版本及历史记录保持原身份。

