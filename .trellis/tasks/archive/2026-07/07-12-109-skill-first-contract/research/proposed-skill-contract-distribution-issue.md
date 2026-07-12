## 背景

Guru Team 先在根 `AGENTS.md` 建立 Skill-first 强制原则：global workflow SSOT、step-local skill SSOT、mandatory invocation、AI judgment 与 deterministic script 边界、typed exits 和模块化拆分条件。

原则确定后，还需要一个独立架构任务把这些原则落实为所有 Guru Team 公共 workflow skills 共用的闭环 package 合同、single canonical source、平台分发机制和结构门禁。该能力不能分散到第一个业务 skill，也不能等所有 skill 各自实现后再迁移，否则 package path、platform copies、managed hash、`.new/.bak` 和 update/reapply 会产生多套临时约定。

官方依据：

- https://docs.trytrellis.app/advanced/custom-skills.md
- https://docs.trytrellis.app/advanced/custom-workflow.md
- https://docs.trytrellis.app/advanced/architecture.md
- https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md

Official workflow marketplace 只安装 `.trellis/workflow.md`，不会自动安装 external skills。Guru Team 必须继续使用 preset 作为完整 extension configurator。

## 目标

### 1. 闭环 Skill 外部合同

为每个 Guru Team 公共 workflow skill 定义统一 package contract：

- Stable `name` / `description` 和显式 workflow trigger。
- Workflow mode 与 standalone mode。
- Entry preconditions、input evidence、freshness/binding。
- 正向行为、AI Review Gate、human confirmation、recorder/validator 的固定顺序。
- Stable external exits、每个 exit 的 evidence 和唯一 consumer/stop。
- Artifact、schema、hash、stale/re-entry 合同。
- Tests、throwaway install、update/reapply 和 cross-platform drift 验收。

长合同放在 skill-local `references/`；`SKILL.md` 只保留 trigger、routing、执行入口和必要 fail-closed 规则。Workflow、command、prompt、breadcrumb 和平台 launcher 不得复制 skill 内部正文。

### 2. Canonical package

确定唯一 Guru Team canonical skill package 目录和机器可读 registry/interface contract。新公共 skill id 使用：

```text
guru-<action>-<object>
```

Skill id、external exit id、schema/interface id 和 script command 是团队公共 API。破坏性调整必须新建 id 或提供迁移。

Registry 必须区分 reserved 与 active：

- reserved id 不安装、不被 workflow mandatory route 引用；
- active id 必须具有完整 package、interface、schema/validator、tests 和 workflow route evidence；
- missing、unknown、multiple 或 unmapped 状态全部 fail closed。

### 3. Deterministic platform distribution

Preset installer 从 single canonical source 确定性分发到声明支持的平台目录：

- `.agents/skills/`
- `.codex/skills/`
- `.cursor/skills/`
- `.claude/skills/`
- 仓库后续明确声明支持的其它 platform skill roots

平台文件只能是格式 adapter 或生成副本，不能成为正文 SSOT。

Installer 必须记录 installed managed hashes，并遵守：

```text
target missing -> install
target == canonical -> unchanged
target == previous managed hash -> .bak + managed upgrade
target unknown/local edit -> preserve target + write .new
missing/invalid provenance -> fail closed or .new; never silent overwrite
```

`trellis update` 后必须能重新应用 preset；不得依赖对上游生成文件的一次性 patch。

### 4. Deterministic structure validation

新增机器结构检查，只验证客观事实：

- required files、JSON/schema、stable ids 和 package paths；
- active/reserved lifecycle；
- mandatory workflow reference；
- external exits 与唯一 consumer/stop；
- installer manifest、selected platform copies、managed hashes 和 drift；
- missing mandatory skill、unknown/multiple/unmapped exit、schema/validator 缺失时返回非零。

Validator 不得判断语义充分性、AI Review 是否通过、scope、revision action 或 route 是否合理。

## Scope

要做：

- 更新 durable requirements/spec，承载通用闭环 skill 与 Canonical/package/distribution 合同。
- 确定 canonical directory、registry/interface schema 和 public API lifecycle。
- 扩展 preset installer 与 installed extension manifest 的 managed hash 语义。
- 增加 deterministic structure validator、unit fixtures 和 fail-closed tests。
- 更新 workflow/preset README 的作者指南、完整安装和 upgrade/update 规则。
- 从 clean throwaway repo 验证 workflow + preset、platform discovery、`trellis update`、workflow reapply、preset reapply、drift 和 `.new/.bak`。
- 同步 dogfood 生成副本并验证无 overlay drift。

不做：

- 不实现任何具体业务 skill 的正向行为、AI Gate、artifact 或 typed exits。
- 不集成任何业务 workflow chain。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 不建立 external skill marketplace；继续使用 Guru Team preset。
- 不把 active task、workspace journal、平台 prompt、业务私有状态、secret 或本机绝对路径写入公共 skill package。

## 验收标准

- Durable Docs/spec 对闭环 skill、workflow、platform adapter、script、schema 和 installer 的责任边界只有一种解释。
- Canonical skill source 只有一个；平台副本由 deterministic installer 生成或同步。
- Reserved skill 不安装、不被 mandatory route 引用；active skill 缺任一必需合同即 fail closed。
- Missing mandatory skill、unknown/multiple/unmapped exit、schema/validator 缺失均 fail closed。
- Auto-trigger failure 不能绕过 mandatory workflow step。
- Structure validator 只检查客观事实，不承担 AI review。
- Managed hash、known upgrade、unknown local edit、`.new/.bak` 和 invalid provenance 均有测试。
- Test-only representative package fixture 能在声明平台被发现；fixture 不作为已交付业务 skill 安装到 production registry。
- README 明确 workflow marketplace 不安装 external skills，完整 Guru Team 安装必须同时应用 preset。
- Clean throwaway 覆盖 workflow install/preview/switch、preset apply、skill discovery、`trellis update`、workflow reapply、preset reapply、drift 和最终零未处理 sidecar。
- 后续具体 skill issue 不再自行选择 canonical path、platform copy、managed hash 或 conflict 语义。

## Close Scope

本 PR 只关闭本 issue，不借此关闭任何具体 skill、workflow 或其它功能 issue。
