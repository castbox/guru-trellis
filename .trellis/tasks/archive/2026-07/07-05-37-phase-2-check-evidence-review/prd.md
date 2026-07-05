# #37 修复 Phase 2 check evidence 与提交后 Review Gate 的 stale 误判

## 目标

修复 Guru Team Branch Review Gate 对 `phase2-check.json` 的 post-commit 校验语义：允许“提交前完整 `trellis-check` 记录 dirty paths，随后 Phase 3.4 将这些 dirty paths 提交”的正常流程通过 Review Gate，同时继续阻断未被 Phase 2 check 覆盖的新提交或非 metadata 工作区改动。

## 背景与证据

- GitHub issue：`https://github.com/castbox/guru-trellis/issues/37`。
- 当前脚本入口：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 中 `validate_phase2_check(..., allow_committed_head=True)`。
- 当前问题：当 `phase2-check.json.head` 是当前 `HEAD` 的祖先时，脚本只接受后续提交全部为 Trellis metadata；正常 task work commit 包含 workflow/docs/tests/config/script 等非 metadata 文件时会被误判为 stale。
- 现有测试：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 已有 metadata-only tail 允许、non-metadata committed tail 阻断、non-metadata dirty 阻断等用例，需要按新语义改写并补充覆盖。
- 官方 Trellis 文档边界：workflow 行为通过 Markdown workflow/preset 表达，脚本只做可机器验证的 executor/validator/recorder 动作。

## 需求

1. `review-branch.sh` 在 Phase 3.5 校验 Phase 2 evidence 时，若 `phase2-check.json.head` 是当前 `HEAD` 的祖先，应接受后续提交中的非 metadata 路径，只要这些路径全部包含在 `phase2-check.json.dirty_paths` 中。
2. 如果 `phase2-check.json.head..HEAD` 或等价提交范围中出现未被 `dirty_paths` 覆盖的非 metadata 路径，Review Gate 必须继续阻断。
3. 如果当前 working tree 存在非 Trellis metadata dirty paths，Review Gate 必须继续阻断。
4. checked artifact digest、coverage、validation_commands、findings、P0/P1/P2 阻断等现有 Phase 2 check 强度必须保持。
5. Workflow / `trellis-continue` 文案必须同步说明：
   - Phase 2 check 是提交前 gate。
   - Phase 3 Branch Review Gate 会做 post-commit audit，确认 task work commit 未超出 Phase 2 `dirty_paths`。
   - 不要求 AI 在 task work commit 后重新 record Phase 2 check，除非提交后又出现新的非 metadata 改动或 evidence 已失效。
6. Canonical source 与 dogfood 运行副本必须同步：
   - canonical Python helper、workflow、overlay / platform entry 文案优先修改；
   - dogfood `.trellis/`、`.agents/skills/`、`.codex/` 运行副本同步；
   - 若修改 overlay，运行 preset apply 和 dogfood overlay drift check。
7. Docs SSOT：本任务属于已有 P0 证据链能力的行为修正，应更新 durable docs 中对应 Phase 2 / Review Gate 语义，避免长期文档仍描述旧的 metadata-only tail 限制。

## 非目标

- 不改变 Branch Review Gate 独立 review 要求、`review.md` digest 要求或 PR publish readiness 规则。
- 不放宽 Phase 2 coverage、validation、checked artifact digest 或 unresolved P0/P1/P2 finding 校验。
- 不把 AI 判断逻辑搬进脚本；脚本只比较提交路径、工作区 dirty state 和 artifact 客观字段。
- 不修改 Trellis 上游源码、全局 npm 包或 `node_modules`。
- 不处理 `trellis-finish-work` publish 语义，除非验证发现必须随本 bug 修复调整。

## 验收标准

- [ ] 正常流程中，提交前记录 `phase2-check.json`，提交这些 `dirty_paths` 后，`review-branch.sh --json --pass ...` 不再因为非 metadata task work commit 误报 stale。
- [ ] 提交后包含未被 Phase 2 `dirty_paths` 覆盖的新代码、docs、config、test 或 script 文件时，Review Gate 仍然阻断。
- [ ] 当前 working tree 存在非 metadata dirty paths 时，Review Gate 仍然阻断。
- [ ] metadata-only tail 仍按现有规则允许。
- [ ] checked artifact digest、coverage、validation_commands、P0/P1/P2 finding 校验仍保持。
- [ ] workflow / `trellis-continue` / README 或 durable docs 明确 post-commit audit 语义，避免 commit 后重录 Phase 2 成为常规流程。
- [ ] 单元测试覆盖 pre-commit dirty paths 被提交后允许、committed path 超出 dirty_paths 阻断、metadata-only tail 允许、non-metadata working tree dirty 阻断。
- [ ] `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 通过，或最终报告明确未覆盖原因和风险。

## Docs SSOT 与知识门禁

- Durable docs 存在：`docs/requirements/requirement-main.md` 第 3 章是 Planning / check / Branch Review Gate 证据链的长期说明，本任务需要同步补充 post-commit audit 语义。
- 中台知识门禁：不适用。本任务修改 Trellis workflow companion script 与文档，不涉及 go-guru、proto-guru、Unity3D Guru SDK 或 Flutter Guru SDK。

## 当前开放问题

无。Issue #37 已明确修复范围，仓库现有脚本、测试、spec 和 durable docs 已能回答实现边界。
