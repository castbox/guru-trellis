# #66 Docs SSOT Branch Review/finish-work enforcement 需求

## 背景

GitHub issue: https://github.com/castbox/guru-trellis/issues/66

这是 Docs SSOT hardening 系列 3 / 3，依赖 #64 和 #65。当前 `main` 已经具备通用 Phase 3 发布基线：Branch Review Gate 要求 independent Agent review，任意 finding 阻断，review 后只允许 Trellis metadata tail，finish-work 拒绝 non-metadata dirty paths，non-draft PR publish 需要 AI-reviewed PR body。

本任务不重复实现这些通用 gate，而是让 Phase 3 / Branch Review / finish-work / PR body 明确验证 #64 的 `Docs SSOT Plan` 和 #65 的 Phase 2 执行结果：最终审查只验证 reconciliation 已经按策略完成，不能首次执行 docs merge，也不能替 Phase 2 补缺失工作。

## 目标

- Branch Review Gate 明确覆盖 `Docs SSOT Plan` 策略链、Phase 2 implementation handoff 与 `phase2-check.json` 的 Docs SSOT 执行结果。
- final reviewer 只做独立验证；发现当前 scope 的 durable docs / task artifacts / code / test 不一致时必须记录 blocking finding。
- Gate 后到 finish-work 只允许 Trellis metadata tail；durable docs、`.trellis/spec/`、source、test、schema、config、script、preset、overlay 等 non-metadata drift 必须回 Phase 2/3。
- finish-work / archive 明确禁止首次执行 Docs SSOT merge，只能 archive task、record journal、commit metadata-only tail、publish PR。
- PR body 必须给 GitHub reviewer 说明本次 Docs SSOT 处理结果，包括策略、durable docs 更新或 no-update 理由、merged delta、task-history-only 内容、follow-up 或限制。
- 如增强 PR readiness validator，只做客观结构检查，例如 Docs SSOT section / key presence；不让脚本判断语义充分性。

## 范围

当前任务关闭候选仅为 #66。#1 只作为 `Refs` 背景，不关闭。#64/#65 视为已合入 `main` 的前置基线，本任务验证并强化 Phase 3 对它们的承接。

需要检查并可能更新的 surface：

- Canonical workflow: `trellis/workflows/guru-team/workflow.md`
- Dogfood workflow: `.trellis/workflow.md`
- Preset overlays: `trellis/presets/guru-team/overlays/**`
- Dogfood installed copies: `.agents/skills/**`、`.codex/prompts/**`、`.codex/skills/**`、`.cursor/**`、`.claude/**`、`.trellis/agents/**`
- Durable docs/spec: `docs/requirements/**`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、workflow/preset README
- Companion script/tests only if objective PR body presence validation is needed: `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` and tests

## 非目标

- 不在 archive 阶段执行 AI 判断、docs merge 或 scope 决策。
- 不把 companion script 变成 reviewer、planner、product owner 或 publisher of record。
- 不重复实现 independent review、finding 阻断、metadata-tail fail-closed、reviewed PR body source、close/ref 语义等已有通用门禁。
- 不修改 Trellis 上游源码、全局 npm 包或 `node_modules`。
- 不关闭 #1。

## 文档状态与需求影响

仓库已有 durable docs / spec / workflow SSOT：`trellis/workflows/guru-team/workflow.md`、`docs/requirements/**`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**` 以及 platform overlay canonical copies。本任务是长期 workflow / publish 合同变更，必须同步 durable docs，任务 artifact 只保留规划和证据。

`Docs SSOT Plan` 的权威定义在 `design.md`。本文件只记录需求影响：Phase 3 文档合同需要从“通用 review/finish/publish gate”强化为“显式验证 Docs SSOT 策略链已经在 Phase 2 完成”。

## 验收标准

- Branch Review Gate 文案明确：current-scope Docs SSOT inconsistency 是 blocking finding，不能降级为 observation 或 follow-up。
- final reviewer 明确只验证 #64 `Docs SSOT Plan` 和 #65 Phase 2 执行结果，不首次执行 docs merge，不替 Phase 2 补工作。
- Gate 后 durable docs / `.trellis/spec/` / source / test / schema / config / script / preset / overlay 等 non-metadata 改动必须重新 Phase 2 check 和 Branch Review Gate；metadata-tail 规则仍保持。
- finish-work / archive 明确禁止首次修改 durable docs 或 `.trellis/spec/`，dry-run / formal finish 均 fail closed。
- PR body 合同要求包含 Docs SSOT 处理结果，并说明策略、durable docs 更新或 no-update 理由、merged delta、task-history-only 内容、follow-up/限制。
- 如增强 PR body validator，测试覆盖缺失 Docs SSOT section 被阻断、包含 section 的 reviewer-readable body 被接受；脚本只做客观存在性校验。
- Canonical workflow、dogfood copy、preset overlays、installed copies、docs/spec 保持一致。
- 运行必要验证，包括 task validate、脚本编译/单测、workflow context read、overlay apply、dogfood drift check、`git diff --check`。如无法完成 throwaway install / upgrade-update 验证，最终说明明确未覆盖项和风险。

## 中台知识门禁

本任务修改 Trellis workflow/preset/overlay/docs 和 companion helper，不涉及 go-guru、proto-guru、Unity3D Guru SDK、Flutter Guru SDK 或其他 Guru middle-platform SDK。Middle-platform Knowledge Gate 不适用。
