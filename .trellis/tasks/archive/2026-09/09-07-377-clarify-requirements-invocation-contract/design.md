# 技术设计

## 1. 最小行为差距

当前 public envelope 的声明边界与 runtime 的数据来源不一致。目标是让
runtime 只从声明且可被调用方合法提交的输入中得到 checked owner result 和
typed exit，同时不把完整 clarification 私有证据提升为 public DTO。

## 2. 方案

采用直接合同收敛，不保留旧路径：

1. 以 `semantic-owner.schema.json` 和当前 Interface 1.4 public handoff 为
   唯一 envelope authority。
2. 调整 `guru-clarify-requirements` runtime，使其从 checked owner result 的
   合同字段确定出口和最小输出；如果确需输出对象，则将其作为 owner result
   的已声明字段，而不是 envelope 顶层隐藏输入。优先复用现有
   `validate_owner`、typed-exit schema 选择和 freshness 校验。
3. 更新 Skill/interface/references 中对 owner result、typed exit 与 public
   output 的描述，避免“runtime 派生出口”和“调用方提供 typed_output”并存。
4. 将现有正向测试改为先用 Draft 2020-12 validator 验证 envelope，再执行真实
   wrapper；补充缺失字段、声明外字段、错误出口和 stale target 回归。
5. 通过 preset apply 重新生成 `.trellis`、`.agents`、`.codex`、`.claude`、
   `.cursor` 安装投影和 manifest，验证 canonical/installed/platform 字节一致。

## 3. 受影响文件边界

- `trellis/skills/guru-team/packages/guru-clarify-requirements/`：
  interface、Skill/reference、runtime、schema、examples、eval、tests。
- `trellis/skills/guru-team/consumers/workflow/stage0/invocations/`：公开
  invocation schema。
- `trellis/presets/guru-team/`：仅在生成/安装投影需要时更新，不手改生成副本。
- `.trellis/guru-team/`、`.agents/`、`.codex/`、`.claude/`、`.cursor/`：由现有
  preset/apply 流程同步。

不修改 global workflow、upstream `trellis-*` agent/Skill、其他 package 或
Issue #108 的已有 worktree。

## 4. Docs SSOT Plan

- `docs_state`: `no_durable_docs_change`。这是当前 public schema/runtime
  一致性修复，不改变产品需求、Architecture Baseline 或 RDT authority。
- `strategy`: `contract_local`。保留现有 owner 与 typed exits，只收敛 package
  public invocation 边界。
- `task_artifact`: 本 task 文档仅记录 Issue 目标、技术边界和验证计划，不成为
  current workflow authority。
- `projection`: canonical package 是唯一源；安装副本通过 preset apply 生成，
  不直接编辑作为语义来源。

## 5. 风险与控制

- 风险：修改 runtime 后只修复单一 `clear` 路径。控制：对全部 typed exits
  做 schema-driven 选择，并执行 current/stale/error matrix。
- 风险：测试继续绕过 envelope schema。控制：回归测试必须先验证 envelope，
  再调用真实 wrapper。
- 风险：安装副本漂移。控制：运行 apply、managed equality、drift 和 sidecar
  检查，并记录未覆盖的完整 Release 矩阵边界。

