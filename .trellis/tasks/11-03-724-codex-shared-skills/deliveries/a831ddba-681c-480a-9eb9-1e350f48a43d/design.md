# D1 Codex Guru Skill 共享目录迁移设计

## 1. 设计目标、需求承接与内容基线

本批完整覆盖整体 R1–R9、S1–S5、AC1–AC5。development baseline B 为 42ffd32d70be3859a4493e084464738473c45dd6，来源为明确选择的 main；首次 D1 无前序 delivered head，内容范围从 B 起算。Planning H0 同为 B，最终实现 H 待形成。PR 目标为 castbox/guru-trellis 的 main；B、H 与 PR target 分别使用。

独立 Architecture candidate_assessment 已正式返回 baseline_current / architecture_impact / target_native，freshness_identity 为 sha256:081dfc316d6a6db1ede1d9ff2da85b911278f2b02a8b9c4267afa84d1f9c1751。适用 baseline 为 guru-trellis-architecture，constitution 为 guru-trellis-design-constitution-v1，change-contract 为 guru-trellis-architecture-change-contract-v1。决策定位 ARCH-INT-006、ARCH-DOM-020、ARCH-STACK-SOURCE-001；该候选结果不代替后续 final_plan 或实现质量门禁。

## 2. 当前系统、边界与目标差额

guru_platform_inventory.py 与 platform_projection_contract.py 仍把 Codex Skill 根定义为 .codex/skills。installer 总是添加共享根，再按平台根和每包 supported_platforms 投影；专属编排包仅支持 codex，因此现有测试明确要求其不进入共享根。当前 runtime、公有文件 allowlist、受管 hash、sidecar、staged activation 和 exact target selection 已有 owner。

目标是修改 Codex 描述为共享根，使原 selection 判断自然投影专属包。共享根去重仍由原 selected_skill_roots 承担。旧目录退出只由原受管迁移识别，不留新安装双路径。其它 Codex 配置、上游资产、Claude/Cursor 根和 Skill API 保持原合同。

## 3. 来源设计处置（唯一）

| 来源/承诺 | 处置 | 设计落点、理由与影响 |
| --- | --- | --- |
| #724 范围：Codex 新装/reapply 单一共享根 | retain | 第4–6节直接调整 descriptor，所有消费者同步 |
| #724 范围：目标完整后删除未修改旧受管文件 | retain | 第6–7节在原 owner 中验证目标公共集合，再按 previous provenance 退役 |
| #724 范围：两端用户修改及未知来源保留，冲突不报成功 | retain | 第6节沿原 conflict/sidecar 和事务门禁；不覆盖用户内容 |
| #724 范围：专属包及 agents/openai.yaml，选择变化 | retain | 第4–5节保留 supported_platforms=codex，由目标 exact selection 决定共享根中的专属包 |
| #724 范围：仅公共文件、tests 私有、配置及其它平台保留 | retain | 第4节复用 public allowlist 与原 owner；第8节独立检查 |
| #724 范围：真实宿主分组与合法公开调用 | retain | 第8节 G1/V3；能力不足的合法 preflight 出口与实际业务编排区分 |
| #452 design 第3、5、7节：目标安装 exact selection、不从 source 推断 | retain | 第5–7节读取目标 manifest/provenance，升级沿原 owner |
| 原当前 ARCH-INT-006：shared 加 selected platform projection | change | Codex 的 selected root 与 shared root 相同并去重；其它平台继续原合同。隔离 proposed target 窄替代该条 |
| 原 ARCH-DOM-020：inventory、descriptor、target selection 各有 owner | retain | 第4节保留职责，仅补 Codex 根和 predecessor retirement；原 Architecture owner 晋升 |

没有改变来源需求或新增长期兼容路径；无须上游范围修改。

## 4. 模块、职责与设计取舍

- 平台 inventory/projection contract 只定义 current 根及 exact selection。Codex 根改为 .agents/skills；canonical extension manifest、ownership 描述和派生 claims 同步。固定 upstream id/cliFlag 不变，移除旧根造成的 claim 去重差额按实际集合派生。
- preset installer 继续拥有 public file 投影、previous managed provenance、stale removal、manifest 和 staged activation。主文件已有2973行，先把受影响的 Skill 投影/移除职责机械抽取为同 owner 小模块，保留调用接口并用现有测试验证，再添加必要迁移。不得通过复制逻辑另建第二 installer。
- 新 current managed roots/expected inventory 不包含旧 Codex 根。迁移代码显式识别旧 .codex/skills/guru-*/，只消费旧 receipt 中的具体受管文件。不会整目录删除、扫描并认领第三方内容或新增 broad ownership。
- upgrade-tools 和 upgrade-installation 沿各自现有维护边界读取旧来源、目标 exact selection、冲突和恢复；已有 checkout dogfood 使用 guru-upgrade-tools。不得以普通 apply 的旧 Task 阻塞为由转换无关历史 Task。
- runtime installed validator、平台/dogfood drift、ownership 和相关测试都消费相同 current descriptor 和公开文件集合。退役路径不作为必需，残留待迁移 Guru 文件/冲突不能被忽略为成功。
- Skill 内容、接口与显式调用策略保持。agents/openai.yaml 继续由既有公开元数据投影分发。完整 runtime 和 package-private tests 不进入发现根。

选择直接同步 consumer 和有界一次迁移，避免双根兼容长期成本。文件提取是为控制既有主模块大小；不引入插件、配置开关、额外状态或新公共 DTO。

## 5. 接口与数据

CLI 参数、Skill id/public I/O、typed exits 和 Task/session schema 不变。current descriptor 的 Codex skill_root 值变化；实际平台选择仍在目标 installed manifest 的 install/skill_packages/overlays 三个 section 一致记录。

生产者为 canonical registry/interface 与平台描述；installer 的公共文件 allowlist 产生共享投影，Agent scanner 消费 SKILL.md/interface/声明引用及元数据。私有 runtime 继续由 .trellis/guru-team/ 执行。source platform selection 不是目标选择输入。

旧 installed manifest 的 files/path/hash 是原迁移 owner 的具体删除依据。结果继续使用既有 files、removals、conflicts、sidecars；当前完整 manifest 与磁盘必须一致。无需新增持久字段或跨 owner 迁移台账。旧路径的识别常量只用于退出，不参与新分发和 public current claims。

## 6. 状态、顺序、正常与失败流程

1. 原 owner 读取完整 source、旧 target manifest/provenance、实际文件及目标选择。
2. 按新 descriptor 和 public allowlist 形成目标完整公共文件集合，包括选中 codex 时的专属包。
3. 通过原 provenance copy 形成目标投影。每个必需公共文件的内容、mode 和适用性均满足当前源，且无未解决冲突/sidecar，才算目标完整。文件存在本身不足。
4. 仅在对应目标公共投影完整后，删除 hash 匹配旧受管记录的退役文件，记录 removals 并只清理由这些文件派生的空目录。
5. 目标冲突时保留目标内容、原 sidecar/diagnostic 及仍需迁移的旧副本；旧文件本身被修改或来源不明时保留并报告处置。不得用新旧双目录掩盖未完成。
6. 原 staged activation 通过 installed inventory/实际文件/冲突/mode 检查后才发布结果；失败沿原 owner resume_required/conflict 路径，不宣称 tools_upgraded 或迁移成功。

移除 codex 的选择变化不再需要专属包目标投影：按原 unselected removal 处理其未修改受管共享文件，同时保留其它平台仍使用的 shared 包和各自副本。用户修改的专属文件进入原冲突路径；不静默丢弃。

## 7. 恢复、兼容、迁移与集成

使用一个已有安装样本验证正式 upgrade owner；不手工伪造 manifest/hash 来建立合法前态。目标冲突解决后沿同一原恢复操作重试。已完成写入由原事务识别，不能重建另一个 owner 或用新 source 接管旧 checkpoint。

普通 reapply 在迁移完成后继续同一 current 集合，不恢复旧根。已知旧文件清理依赖原 provenance，未知来源/用户内容由原冲突处置保留。更改平台选择的测试分别覆盖加入和退出 codex；源仓库 dogfood selection 不决定外部目标。

新包调用不需要兼容 wrapper，原 API 和元数据策略保持。本批没有数据库、生产或外部业务写入回滚。Git/PR、归档和清理沿原正式 owners；保留所有并行工作区及无关修改。

## 8. 验证设计

| 验证 | 场景/验收 | 入口与预期观察 |
| --- | --- | --- |
| V1 投影/选择 | S1/S4；AC1/AC4 | 原 installer 相关单元与集成入口覆盖 non-codex、codex-only、含 codex 多平台；观察公共集合、mode、元数据、去重、无私有资产及选择增减 |
| V2 迁移/冲突 | S2/S3；AC2 | 真实旧 source 安装或原测试边界生成合法 old provenance，再经正式 maintenance/installer；观察目标完整后删除、两端修改/未知文件保留、目标冲突时旧副本保留、原恢复/重试、manifest/removals/conflicts 一致 |
| V3 native G1 | S5；AC3 | 使用真实 codex-cli 0.162.1，以名称显式调用公共 Guru Skill 与 Codex 专属编排 Skill。启动时目标无旧副本；从实际 native trace 核对发现和打开的 .agents/skills 路径、原公开 invoke、合法 typed/conversation exit，不向模型预装 package 全文或预告期望结果 |
| V4 clean/reapply | S1；AC1/AC5 | 一个代表性 Codex clean throwaway，经原完整 source installer；同样本 reapply、source/installed validator、public files/mode、private tests 排除与递归 sidecar 检查 |
| V5 dogfood/相关平台 | AC4/AC5 | 原 guru-upgrade-tools 更新当前 Task checkout 后，执行 target 自身 resolver/installed validation/get_context、check-dogfood-overlay-drift.sh；核 Task/session/peer 保护及 Claude/Cursor 原分发 |
| V6 current knowledge | AC5 | 原 RDT/Architecture 独立候选评估与 candidate Check 后 final_integration，实际 targets 重绑后最终 Check、完整 committed Review；文档与真实结果一致 |

G1 采用官方当前 Codex repo-skill scanner 机制：官方 Skills 文档说明 standalone Skills 用于 desktop、CLI、IDE，仓库发现沿 CWD 到 repo root 的 .agents/skills；本仓 .codex/config.toml 也区分终端 CLI 和 desktop bundled CLI 的同配置机制。本次实际代表版本为 CLI0.162.1。代表性依据是相同 repo-skill 发现合同，不是目录存在。记录实际客户端、版本和入口；不将该观察扩张为所有历史/未来版本、桌面 UI 或其它 Agent 的兼容承诺。若实际发现独立受支持入口采用不同 scanner，补定向 native 证据后才能完成其验收。

专属包验证用原显式调用的 dry-run preflight，不启动业务 child、heartbeat 或 GitHub 写入。其原 native chat/async 工具前置必须原样检查；CLI 缺能力时可以观察真实合法 dry_run_blocked，记录具体缺口，不能将其称为真实业务编排已通过。原指令、元数据与能力前置的完整性另由公开投影检查证明。出现实际依赖旧根的受支持宿主时先记录并解决其兼容承接，不直接移除后宣称全兼容。

普通任务不运行完整多平台 Throwaway/Release Gate。local_candidate 安装证据必须保留 formal_fork_source_lock 未验证边界；不以本次安装或模型调用证明发布。

## 9. Canonical 引用、本轮差额与实际未决项

命中 installer/ownership、skill-package-contract 的 Distribution And Managed Hashes、quality-guidelines 的 Validation Scope Ownership/Test And Validation Value，以及 Architecture ARCH-INT-006/ARCH-DOM-020。本批差额为单一 Codex 根、专属包适用性与有界旧根退出；其它职责和公共 I/O 保持。

Author 将创建 docs/architecture/contributions/724-codex-shared-skills.md 及其 proposed 完整 targets 和必要 ADR；RDT 原 owner 在 Phase2 形成 docs/requirements-design-test-contributions/724-codex-shared-skills/ 的完整隔离定义和 traceability。共享 current 在独立 candidate Check 前不写；原 owners 在 final_integration 读实际 before/target 并完成写回。没有未决需求选择；实际 native、升级和其它验证尚待执行。

