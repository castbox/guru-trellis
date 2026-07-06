# 设计说明

## 范围

本任务只收紧 Guru Team Branch Review Gate 的 recorder 语义与入口文案，不改变 Trellis 官方 CLI、全局 npm 包或 `node_modules`。

涉及文件预计包括：

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/presets/guru-team/overlays/**/trellis-continue*`
- dogfood installed copies：`.agents/skills/trellis-continue/SKILL.md`、`.codex/prompts/trellis-continue.md`、`.codex/skills/trellis-continue/SKILL.md`、`.claude/commands/trellis/continue.md`、`.cursor/commands/trellis-continue.md`

## 关键合同

### Branch Review Gate 记录合同

- `review-branch.sh` 是 recorder / validator，不是 reviewer。
- pass path 和 findings path 都必须来自独立审查：
  - `--review-source independent-agent`
  - task-local `--review-report .trellis/tasks/<task>/review.md`
  - `--reviewer` 只能作为 reviewer identity metadata，不能替代 review source/report。
- `--pass` 是产生 `conclusion.passed=true` 的必要条件。
- 只要存在任何 finding，包含 `P0/P1/P2/P3`，`conclusion.passed` 必须为 `false`，且 `--pass` 必须 fail closed。
- `observations[]` 与 `followup_candidates[]` 不是 findings，不阻断 pass，但不能用于隐藏 current-scope defect。

### Workflow / overlay 关系

- canonical source 是 `trellis/workflows/guru-team/workflow.md`。
- `.trellis/workflow.md` 是本仓库 dogfood active copy，需要同步。
- overlay canonical source 在 `trellis/presets/guru-team/overlays/`；修改后通过 preset apply 同步到 dogfood installed copies。
- 平台入口只表达 routing 与关键门禁语义，不复制完整 workflow。

## 实现策略

1. 在 `cmd_review_branch()` 中把 `independent_review_source_errors()` 从 pass-only 校验提升为所有 Branch Review Gate 记录路径校验。
2. 在 `build_review_gate_payload()` 增加显式 `pass_gate` 输入，使用 `bool(pass_gate and not blockers)` 计算 `conclusion.passed`，避免未来调用路径在未传 `--pass` 时因为 `findings=[]` 误写 `passed=true`。
3. 保持 findings path 要求 task-local `review.md` digest 的现有校验，并补充缺失 review source 的测试。
4. 更新 workflow findings 示例，加入 `--review-source independent-agent`。
5. 更新 continue overlay 文案，明确 findings path 也必须携带独立来源和 task-local review report。
6. 运行 preset apply 同步 dogfood 副本，再用 drift check 验证无漂移。

## 兼容性与风险

- 对已有旧 artifact：`check-review-gate` / `validate_review_gate()` 本来只接受 passed gate；旧 failed artifact 不用于 finish-work。新增校验主要影响新写入的 findings artifact，符合 issue 目标。
- 对 review agents：不会要求 findings path 必须有 final pass reviewer；findings path 是失败记录，只要求 independent source 和 task-local review report。
- 对 Phase 2：本任务不改变 `phase2-check.json` 的 P0/P1/P2 阻断语义；用户修正只作用于 Branch Review Gate findings/pass 语义。

## Docs SSOT

本任务改变长期 workflow 行为和 companion script 合同，因此 durable SSOT 是 workflow contract、preset overlays、README 片段和 `.trellis/spec/workflow/*`。当前 specs 已记录 “P0/P1/P2/P3 全阻断” 和 independent review source；实现后需要核对 README 是否已有相同语义。若 README 已准确，则无需额外 docs 改动。

## 官方文档依据

- `https://docs.trytrellis.app/advanced/custom-workflow`
- `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace`

这些文档只作为扩展边界依据：优先使用 workflow Markdown / marketplace / local preset overlay，不通过修改 Trellis upstream 或 global npm 包实现团队流程分叉。
