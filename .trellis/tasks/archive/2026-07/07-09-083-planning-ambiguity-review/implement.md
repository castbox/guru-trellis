# #83 实施计划：planning ambiguity review gate

## 前置检查

- [x] 已读取 issue #83 正文。
- [x] 已核对官方 Trellis custom workflow / spec template marketplace 文档。
- [x] 已读取 `trellis-meta`、`trellis-brainstorm`、`trellis-before-dev` 入口说明。
- [x] 已读取 workflow / preset / docs 规格。
- [ ] 用户完成 post-planning approval 后，才能记录 `planning-approval.json` 并进入实现。

## 实施步骤

1. 更新 planning approval data contract。
   - 修改 `PLANNING_APPROVAL_SCHEMA_VERSION` 为 `1.2`。
   - 增加 ambiguity review 常量、payload builder、validator。
   - 增加 `record-planning-approval` CLI flags。
   - 更新 unit tests。

2. 更新 canonical workflow。
   - `trellis/workflows/guru-team/workflow.md` 增加 planning artifact normative language rule。
   - Phase 1.4 增加 ambiguity review 步骤。
   - Phase 1.5 示例命令增加 ambiguity evidence flags。
   - Phase 2 start 前检查说明加入 ambiguity evidence。

3. 同步 dogfood active workflow。
   - 将同一 workflow 改动复制到 `.trellis/workflow.md`。

4. 更新 platform overlay。
   - 修改 preset overlay 中 continue / brainstorm / before-dev / implement / check 入口。
   - 修改 dogfood `.agents` / `.codex` 运行副本。
   - 运行 preset apply 同步 dogfood。

5. 更新 durable docs / specs。
   - 更新 `docs/requirements/guru-team-trellis-flow.md` 与 `docs/requirements/requirement-main.md`。
   - 更新 `.trellis/spec/workflow/workflow-contract.md`、`data-contracts.md`、`quality-guidelines.md`。
   - 更新 `.trellis/spec/preset/overlay-guidelines.md`。

6. 更新 task context manifests。
   - `implement.jsonl` 写入实际 spec / docs context。
   - `check.jsonl` 写入实际 spec / docs / validation context。

7. 运行同步和验证。
   - `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
   - `python3 -m json.tool trellis/index.json`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - targeted unit tests for planning approval
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-083-planning-ambiguity-review`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.4`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.5`
   - `git diff --check`

## Ambiguity Review Checklist

实现前与实现后均按以下维度检查本 task 的 planning artifacts 与 workflow 改动：

- [ ] 无需求弱化。
- [ ] issue #83 原始语义完整保留。
- [ ] 可选执行路径均有明确触发条件。
- [ ] 同一目标不存在并行实现路径。
- [ ] gate 条款均有机器可验证条件。
- [ ] acceptance criteria pass/fail 语义确定。
- [ ] 外部引用均标明来源，且不承担执行合同语义。

## Docs SSOT Checkpoint

- Strategy: `ssot_first`
- Phase 2 check 前必须确认 durable docs / specs 已包含 ambiguity review gate、受控词表、planning approval 1.2 contract、script boundary。
- Branch Review Gate 必须复核本 checkpoint 已完成，不得把 docs sync 延后到 review 或 finish。

## 风险与回滚点

- 风险：新增 `planning-approval.json` 必填字段会阻塞旧 overlay 示例命令。缓解：同步 overlay、README、workflow 示例和 tests。
- 风险：过度脚本化语义判断违反仓库边界。缓解：脚本只校验结构化 evidence，语义 sufficiency 留在 AI review。
- 回滚点：在 commit 前可直接回滚 workflow/docs/script/test 改动；在 commit 后通过 revert PR 恢复 1.1 contract。
