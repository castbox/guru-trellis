# #147 行为评测基础设施证据摘要

## Live authority

- Issue #147：<https://github.com/castbox/guru-trellis/issues/147>。
- Direct prerequisite #144：当前 main 已提供 Interface 1.3、exact public invocation、per-exit output schema 和 consumer/private-state contract。
- Follow-up #145/#146：production Skill migration 与 coverage closure，不进入当前 task。

## Trellis 官方边界

- <https://docs.trytrellis.app/index.md>
- <https://docs.trytrellis.app/advanced/custom-workflow.md>
- <https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md>

结论：workflow 与 semantic judgment 保持在 Markdown/AI 边界；marketplace/preset 是持久分发入口；不得修改 upstream/global npm/node_modules 实现项目扩展。

## 当前仓库证据

- `.trellis/spec/workflow/skill-package-contract.md`：Interface 1.3 public/private ownership SSOT。
- `trellis/skills/guru-team/tests/fixtures/representative-active/`：test-only semantic structured-input 与 deterministic scalar-CLI packages。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`：现有 source/installed validation、`discover-skill-contract` 与 public invocation dispatcher。
- `trellis/guru-team-extension.json`：extension public API 与 companion scripts inventory。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：fresh install、update/reapply 与 sidecar 验证入口。

## Factory 起点

读取 `castbox/guru-codex-plugin-skill-factory`：

- `resources/skill/skill-evals.schema.json` 只有 `skill_name`/`evals`，case 使用 integer `id`、`prompt`、`expected_output`，可选 `files`/`expectations`，且允许未知字段。
- `.agents/skills/skill-contract-validate/evals/evals.json` 证明 package-local corpus 形式可复用，但 `expectations` 仅是人类可读字符串。

结论：只复用 package-local `evals/evals.json` 概念。Guru schema 必须独立版本化并 closed，增加 stable string id、expected typed exit、Interface refs、typed assertions、adapter/runner/grader/evidence 边界；factory 的 `expectations` 只做单向 legacy migration test。

## 无剩余产品问题

Issue 已确定 corpus、runner、grader、adapter、comparison、evidence、normal-runtime zero-impact、acceptance 与 out-of-scope。规划不需要向用户重新确认仓库可回答的事实或已由 issue 固定的产品选择。
