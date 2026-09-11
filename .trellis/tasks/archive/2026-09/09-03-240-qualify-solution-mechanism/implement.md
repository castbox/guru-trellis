# 实施计划：解决机制资格 Skill

## 1. 交付顺序

1. 盘点现有 registry/interface/manifest/workflow consumer 结构以及 `guru-qualify-normal-scenario` 的可复用 deterministic substrate，确认新 Skill 的稳定 id、schema id、exit id 和 profile caller 映射。
2. 在 canonical package 新增 `guru-qualify-solution-mechanism` 的 `SKILL.md`、`references/contract.md`、`interface.json`、四平台无语义差异的 schemas/examples/evals/tests/runtime/script wrappers。
3. 更新 canonical `registry.json`、`guru-team-extension.json`、workflow marker/target/router 和所需 consumer schemas；保留既有 owner 的语义边界，不复制调用方内部步骤。
4. 按 preset contract 同步 `.trellis/guru-team/`、`.agents/`、`.codex/`、`.claude/`、`.cursor/` dogfood projection，更新必要 README/spec，清理并检查 sidecar/drift。
5. 运行 package、registry/manifest、workflow graph、preset/install/reapply/drift 和真实 wrapper eval；对失败项先由 AI 判断是否属于本 Issue scope，再修复并 fresh 重跑。

## 2. Docs SSOT Plan

- Requirements authority：本 task 的 `prd.md` 仅固定 #240 的机制边界、非目标和验收。
- Design authority：本 task 的 `design.md` 固定 owner、I/O、接入点、架构取舍和验证分层。
- Workflow authority：`trellis/workflows/guru-team/workflow.md`；dogfood mirror 为 `.trellis/workflow.md`。
- Skill authority：`trellis/skills/guru-team/packages/guru-qualify-solution-mechanism/`；其 contract/interface/schema/eval 是 package-local SSOT。
- Registry/distribution authority：`trellis/skills/guru-team/registry.json`、`trellis/guru-team-extension.json`、preset scripts/README 与生成安装副本。
- Durable project spec：仅在实现揭示新的可复用 workflow/package/preset 约定时，按 `.trellis/spec/` 现有分层更新；不写 tracked qualification report、ledger 或 approval artifact。

## 3. 主要文件分区

- 新增：canonical mechanism package 全部声明资产及 package tests。
- 修改：canonical workflow、dogfood workflow、registry、extension manifest、consumer schemas、preset README/manifest/validation tests、声明平台投影和必要 durable spec。
- 不修改：业务仓库、#237/#239 语义 owner、上游 Trellis 源码、`node_modules`、历史 task archive。

## 4. 验证清单

- `python3 -m json.tool` 校验所有 JSON/manifest；`bash -n` 校验 shell；canonical Python `py_compile`。
- 新 package contract/runtime tests 与真实 installed wrapper stdin/stdout probe。
- registry/manifest 完整闭合：active package、schema、examples、commands、consumer/projection、platform destinations 一致。
- workflow marker/target 唯一且 kind/consumer 不悬空；六个 mandatory caller 的 mechanism invocation 文案一致。
- canonical、dogfood、shared/Codex/Claude/Cursor 字节/权限一致；preset apply/reapply、upstream ownership、dogfood overlay drift 和 zero sidecar 通过。
- paired eval 至少覆盖 Issue #240 R4 的八类机制/压力场景；评估必须使用真实安装后的 public wrapper 和目标模型，禁止 keyword classifier/mock semantic result。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-03-240-qualify-solution-mechanism`、`git diff --check` 以及针对变更 package 的定向测试通过。

## 5. Architecture implementation handoff

- 在 Phase 2 前维护 `docs/architecture/contributions/240-qualify-solution-mechanism.md`，绑定
  current `.43`、设计宪法、project change-contract、required concerns、target-native path、
  owner/single-writer、before/after、project check、证据边界、ADR candidate 与 expected current。
- Phase 2 使用 fresh `guru-maintain-architecture-baseline:task_impact_sync(stage=phase2)`；独立
  Branch Review 必须重新从 `dbfbeea6f87e8973ca42f0feee3856a5b0a244bb...HEAD` 的完整 committed
  diff 判断，不复用旧 Branch Review 或旧 Architecture 结果。
- 当前贡献只允许 task-owned 写入；shared Architecture current、ADR index 与 promotion 仍由
  Architecture owner 串行维护。

## 6. 下游边界

本计划不授权 commit、push、PR、merge、release、Issue closure、跨仓库迁移或生产操作；这些动作分别由后续门禁和独立授权决定。
