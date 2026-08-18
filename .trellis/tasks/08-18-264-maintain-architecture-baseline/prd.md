# #264 建立 Architecture Baseline 原子闭环 Skill

## 目标

在当前 Trellis 0.6.5 / Guru v0.6.5-guru.9 source/dogfood surface 上交付并激活公共 semantic Skill `guru-maintain-architecture-baseline`。Skill 必须能被 Bootstrap、Intake、Planning、Implementation discovery、Phase 2、Branch Review、Publication 与 Finish 复用，同时保持 AI 语义判断与脚本确定性事实收集严格分层。

## 范围

- 新增 Interface 1.4-compatible package、registry row、profile-specific schemas、typed exits、consumer projections、runtime/recorder/checker、evals 与 Codex/Claude/Cursor 等平台副本。
- 定义 `bootstrap_foundation`、`task_impact_sync`、`promotion`、`repair` 四个互斥 semantic profiles；每个 profile 使用最小独立 input/output DTO。
- 建立 `docs/architecture/` 逻辑 authority 与状态语义，允许 clean new repo 和既有文档 repo 建立/复用唯一 baseline；初始推断不得伪装成 CURRENT、accepted、TARGET 完成或 PLAN 完成。
- 将最小 baseline locator/version/status/scope/freshness 投影接入现有 workflow/skill contracts，不复制内部判断。
- 更新 canonical source、preset installer 清单与 dogfood 安装副本；完成 current-version clean install/update/reapply/workflow-switch/platform parity/drift/.new/.bak/executable-mode 验证。

## 非目标

不实现 #265 Bootstrap 编排、Requirements/Design/Test SSOT、v0.6.15 compatibility、stable release、上游 Trellis 修改、锁/TOCTOU/攻击模型、无关历史技术债或额外 Issue。

## 验收

以 live Issue #264 的完整 Acceptance 与 Sequencing acceptance 为准。特别要求：active 激活需独立 semantic review、版本、scope、迁移与验证证据；ADR 只有 accepted 且投影到 active baseline 才具有 current authority；不同 task 只能写 task-owned contribution；所有 typed failures 有唯一 consumer 和可验证 re-entry；保留 #262 Draft PR recovery 与 reviewed-content freshness/provenance coverage。

## Docs SSOT Plan

架构 authority 正文仅在目标业务仓库的 `docs/architecture/`；Guru Trellis 只提供可复用 contract、模板、索引读取规则与最小 locator schema。公共 Skill 行为 SSOT 在 `trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/`，全局路由仅在 `trellis/workflows/guru-team/workflow.md` 标记 mandatory invocation/consumer。preset README、registry/interface、平台副本和 dogfood copy 只承接安装与导航，不复制架构正文。
