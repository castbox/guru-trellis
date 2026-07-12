# #120 建立 Guru Team 闭环 Skill 合同与 Canonical 分发基础设施

## 目标

把根 `AGENTS.md` 已确立的 Skill-first 原则落实为一套可复用、可安装、可升级、可机器校验的 Guru Team 公共 workflow skill 基础设施，使后续具体 skill 直接复用同一 package、interface、typed exit、平台分发和冲突处理合同。

## 背景与已确认事实

- GitHub issue [#120](https://github.com/castbox/guru-trellis/issues/120) 是本任务唯一 primary issue 和 close 候选。
- `AGENTS.md` 已定义 global workflow SSOT、step-local skill SSOT、mandatory invocation、closed-loop 顺序、typed exits、脚本边界和 `guru-<action>-<object>` 命名规则。
- 官方 Trellis workflow marketplace 只安装 `.trellis/workflow.md`；external skills 必须经 Guru Team preset 分发。
- 当前 preset 从 canonical workflow 目录复制 companion assets，并从 `trellis/presets/guru-team/overlays/` 分发平台入口；未知本地 overlay 改动会保留原文件并生成 `.new`。
- 当前 installed extension manifest 记录 `managed_assets`，但没有逐文件 previous managed hash、公共 skill registry、package interface 或 typed exit route 证据。
- #109 的任务历史把 `guru-create-work-commit` 定义为 #120 完成后的具体 skill 候选；本任务只保留该 id，不实现其行为。
- 历史讨论与当前仓库证据共同支持 canonical root `trellis/skills/guru-team/`；本任务不引入 external skill marketplace。

## 需求

### R1：公共 closed-loop skill 合同

必须定义所有 Guru Team 公共 workflow skills 共同遵守的 package/interface 合同，覆盖：

- stable `name`、`description`、workflow trigger 和 `guru-<action>-<object>` id；
- workflow mode 与 standalone mode 使用一致的 entry preconditions；
- input evidence、artifact identity、freshness 和 re-entry；
- 正向行为、AI Review Gate、命中条件时的 human confirmation、recorder/validator、typed exit 的固定顺序；
- external exit id、exit evidence、唯一 consumer 或 fail-closed stop；
- artifact/schema/hash、测试、安装、升级和跨平台一致性。

`SKILL.md` 必须只承载 trigger、routing、执行入口和 fail-closed 核心规则；长合同必须放入 package-local `references/`。Workflow、command、prompt、breadcrumb 和平台 launcher 不得复制 step-local skill 正文。

### R2：唯一 canonical package 与 registry

必须在 `trellis/skills/guru-team/` 建立唯一 canonical root，并提供机器可读 registry、interface schema 和 registry schema。

Registry 必须区分：

- `reserved`：只占用公共 id；不得安装，不得被 production workflow mandatory route 引用；
- `active`：必须具有完整 package、interface、schema/validator 声明、测试证据和 workflow route evidence。

Production registry 在本任务中只能登记 `guru-create-work-commit` 为 `reserved`。代表性 `active` package 只能存在于 test fixture，不得成为 production 安装资产。

### R3：deterministic platform distribution

Preset installer 必须从 canonical package 向以下 runtime roots 分发 active packages：

- `.trellis/guru-team/skills/`：完整 installed registry/package/provenance 副本；
- `.agents/skills/<skill-id>/`：shared runtime copy；
- `.codex/skills/<skill-id>/`、`.cursor/skills/<skill-id>/`、`.claude/skills/<skill-id>/`：仅在对应 platform 被选择时安装。

平台副本只能是 canonical 内容的生成副本或格式 adapter，不得成为正文 SSOT。未选择的平台 root 不得由 installer 创建。

### R4：managed hash 与冲突合同

Installed extension manifest 必须记录公共 skill 分发所需的 registry/package/interface/目标文件 hash 和来源版本，使下一次 preset reapply 能区分以下状态：

| 状态 | 必须结果 |
| --- | --- |
| target 不存在 | 安装 canonical bytes 并记录 hash |
| target bytes 与 canonical bytes 一致 | 标记 unchanged 并刷新确定性 provenance |
| target bytes 与 previous managed hash 一致 | 生成 `.bak`，再写入新 canonical bytes |
| target 是未知本地改动 | 保留 target，写入 `.new`，返回冲突证据 |
| provenance 缺失或无效且 target 与 canonical 不同 | 保留 target，写入 `.new` 或 fail closed；不得静默覆盖 |

公共 skill package 不得复用 `looks_like_trellis_generated_entry()` 的内容启发式覆盖逻辑。

### R5：deterministic structure validator

必须新增 stable command `check-skill-packages`，提供 `source` 与 `installed` 两种 mode：

- `source` 校验 canonical registry、package、interface、schema、stable id、production workflow marker 和 exit consumer/stop；
- `installed` 校验 installed manifest、selected platform roots、文件 hash、package drift 和未处理 sidecar。

Validator 只能检查机器事实。它不得判断意图、scope、语义充分性、AI Gate 是否通过、revision action 或 route 是否符合已审阅的流程意图。

以下状态必须返回非零：missing mandatory skill、unknown/multiple/unmapped exit、active package 缺必需合同、schema/validator 缺失、reserved 被安装或被 mandatory route 引用、installed hash 漂移、invalid provenance。

### R6：workflow 机器 route evidence

Canonical workflow 和 test fixture workflow 必须使用稳定、可解析的 `guru-skill-invoke` 与 `guru-skill-exit` marker 表达 mandatory invocation 和 typed exit consumer/stop。Auto-trigger 只能辅助发现，不能替代 marker 所声明的 mandatory invocation。

Production registry 没有 active skill 时，production workflow 不得伪造 mandatory route。测试必须用 fixture active package 验证 complete route 和全部 fail-closed 分支。

### R7：durable docs 与公共 API

必须更新 durable requirements、workflow/preset spec、根 README、workflow README 和 preset README，统一说明：

- canonical/package/interface/registry 的责任边界；
- workflow marketplace 不安装 external skills；
- preset 才是完整 Guru Team extension configurator；
- id、external exit id、schema/interface id、script command 和 registry lifecycle 是公共 API；
- 破坏性变更必须新建 id 或提供明确迁移合同；
- `trellis update` 后必须重放 workflow 与 preset，并处理 `.new` / `.bak`。

### R8：安装、升级与跨平台验证

必须覆盖以下验证层：

- registry/interface/validator unit fixtures；
- missing、reserved、active、unknown、multiple、unmapped、schema 缺失、invalid provenance 失败矩阵；
- missing install、unchanged、known managed upgrade、unknown local edit、`.new` / `.bak`；
- shared、Codex、Cursor、Claude 的选择性 platform discovery；
- clean throwaway 中的 workflow init、preview、switch、preset apply、`trellis update --force`、workflow reapply、preset reapply、drift 检查和最终零 sidecar；
- canonical overlay reapply 与 dogfood drift 检查。

## 验收标准

- [ ] AC1：durable docs 对 workflow、skill、platform adapter、script、schema、installer 的 owner 只有一种解释，并逐项承接 R1-R8。
- [ ] AC2：canonical root 只有 `trellis/skills/guru-team/`；production registry 只有 `guru-create-work-commit` reserved entry，production install 不产生该 skill 的平台副本。
- [ ] AC3：fixture active package 能被 shared、Codex、Cursor、Claude 声明平台发现，且 fixture 不进入 production registry 或 production install。
- [ ] AC4：active package 缺 required file、interface、schema/validator、workflow invoke marker、exit mapping 任一项时，`check-skill-packages --mode source` 返回非零。
- [ ] AC5：reserved 被安装或被 production mandatory route 引用时返回非零；unknown/multiple/unmapped exit 均返回非零。
- [ ] AC6：preset reapply 对 missing、unchanged、known upgrade、unknown edit、invalid provenance 分别产生 R4 规定的结果，unknown/invalid 状态不覆盖原文件。
- [ ] AC7：installed manifest 绑定 selected platforms、installed registry/package paths 和逐文件 hash；`installed` mode 能发现 drift、错误平台副本和未处理 sidecar。
- [ ] AC8：workflow marketplace 和 preset 的文档/命令真实可执行；clean throwaway 完成 update/reapply 后不存在 `.new` / `.bak`。
- [ ] AC9：canonical workflow、dogfood workflow、canonical preset、dogfood installed assets 和声明平台入口通过一致性检查。
- [ ] AC10：公共 extension version、managed paths、artifact/script API 清单与新增基础设施一致。
- [ ] AC11：代码、测试和 task artifact 不包含 secret、本机绝对路径、active workspace journal 或业务私有状态。
- [ ] AC12：PR close scope 只能关闭 #120；不得关闭或实现 `guru-create-work-commit`、#98、#115 或其它具体 workflow skill issue。

## 范围外

- 不实现 `guru-create-work-commit` 或其它具体业务 skill 的正向行为、AI Gate、artifact 和 typed exits。
- 不把任何现有 monolithic workflow step 拆成 active skill。
- 不建立 external skill marketplace。
- 不修改 Trellis upstream、全局 npm package 或 `node_modules`。
- 不把 active task、workspace journal、平台 prompt、业务私有状态、secret 或本机绝对路径写入公共 package。
- 不借 #120 修改 #98、#115 或其后续业务 workflow chain。

## 阻塞问题

无。当前 issue、官方文档、仓库证据和 #109 历史决策足以进入设计与实现规划。
