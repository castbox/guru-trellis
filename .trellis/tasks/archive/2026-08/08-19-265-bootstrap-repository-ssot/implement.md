# 实施计划：#265

## 交付顺序

1. 在实现 worktree 中复核官方 custom workflow/marketplace 文档、#263/#264 active interface、当前 registry/installer 和 upstream `trellis-spec-bootstrap` 入口。
2. 建立 canonical `guru-bootstrap-repository-ssot` package：SKILL.md、interface、三个 profile schemas、四个 output schemas、consumer projections、errors、runtime/invoke wrapper、contract tests/evals。
3. 在 registry、production-current inventory、discovery/validation fixtures 中激活 package；同步 shared/Codex/Claude/Cursor platform copies。
4. 更新 global workflow mandatory invocation/typed consumers，preset inventory/ownership/README 与可复用 spec projection contract；保持 installer/update 只报告不执行。
5. 通过 apply/reapply 同步 dogfood 安装副本，检查 canonical/dogfood/installed/declared-platform 逐文件一致和 executable mode；清理并记录所有 `.new/.bak` 结果（不触碰无关文件）。
6. 运行 package/contract/runtime/eval、JSON/schema、Python/Bash、workflow graph、README command、preset reapply/drift 与最小现有回归；运行一个 clean current-version throwaway entry proof。
7. 完成 AI semantic check、独立 branch review、commit/publication readiness 前的证据整理；本 Issue 不执行 commit/push/PR/merge/release，直到后续独立门禁和用户确认。

## 受控文件分区

- `trellis/skills/guru-team/`：canonical package、registry、contracts、tests/evals。
- `trellis/workflows/guru-team/`：mandatory invocation、四 exits 与薄 consumer route。
- `trellis/presets/guru-team/`：inventory、installer/ownership、README、platform overlays。
- `.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.cursor/skills/`、`.trellis/guru-team/`：由 canonical/apply.sh 生成的安装和 dogfood 副本。
- `.trellis/spec/`：仅写可复用 projection/index 规则，不写业务 repository 私有正文。

## 风险与门禁

Skill id、schema id、exit、consumer 和 registry row 是公共 API；任何 graph/cardinality、平台副本、managed-path、freshness 或 projection 漂移均 fail closed。#263/#264 private artifact、授权信息、完整扫描历史和业务正文不得进入 public package。完整多平台 Throwaway、upgrade/update 与 exact-candidate release evidence 记录为 deferred/unverified boundary，由 #260/#267 负责。
