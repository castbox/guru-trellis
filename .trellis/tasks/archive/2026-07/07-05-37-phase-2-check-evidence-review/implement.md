# #37 实现计划

## 前置结论

- Source issue：`https://github.com/castbox/guru-trellis/issues/37`。
- Base branch：`main`，handoff 记录 executor 已刷新至 `93be70b768ac331b673870529e560b4d0257692c`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/37-phase-2-check-evidence-review`。
- 中台知识门禁：不适用。
- Docs SSOT：需要更新 `docs/requirements/requirement-main.md`。

## 实施步骤

1. [x] 修改 canonical Python helper：
   - 在 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 中新增/调整 committed path 覆盖校验 helper。
   - 更新 `validate_phase2_check(..., allow_committed_head=True)` 的 ancestor 分支，允许 `dirty_paths` 覆盖的 non-metadata committed tail。
2. [x] 修改 canonical 单元测试：
   - 将现有 `test_validate_phase2_rejects_post_commit_non_metadata_committed_tail` 调整为“超出 `dirty_paths` 才阻断”。
   - 新增“pre-commit dirty paths 被提交后允许”的用例。
   - 保留 metadata-only tail 允许与 non-metadata working tree dirty 阻断用例。
3. [x] 同步 installed dogfood helper：
   - 将 canonical Python helper 同步到 `.trellis/guru-team/scripts/python/guru_team_trellis.py`。
4. [x] 同步 workflow / entrypoint 文案：
   - 修改 `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md` Phase 3.5 描述。
   - 修改 overlay 中 `trellis-continue` / Codex prompt / Cursor command 文案。
   - 运行 preset apply 同步 `.agents/skills/`、`.codex/prompts/`、`.codex/skills/` 等 dogfood installed copies。
5. [x] 更新 durable docs：
   - 更新 `docs/requirements/requirement-main.md` 的 Planning / check / Branch Review Gate 说明。
6. [x] 更新 `issue-scope-ledger.json`：
   - 在验收后补充 #37 acceptance evidence。

## 验证计划

最低验证命令：

```bash
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-05-37-phase-2-check-evidence-review
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

若 overlay 修改导致 dogfood 漂移：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

## Review Gate 前自检

- Phase 2 `trellis-check` 必须覆盖 requirements、design、code、tests、spec_sync、cross_layer、docs_ssot、deployment。
- `phase2-check.json` 记录提交前 dirty paths。
- 提交后通过 Branch Review Gate 时，不应重录 Phase 2 evidence 来伪装 commit 后检查。
- Branch Review Gate 必须由独立 Agent review 完整 `origin/main...HEAD` diff 后写 `review.md`，主会话只负责记录 gate。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：70 tests OK。
- `python3 -m json.tool trellis/index.json`、`trellis/workflows/guru-team/schemas/intake-handoff.schema.json`、task ledger、planning approval：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py .trellis/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-05-37-phase-2-check-evidence-review`：通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`：输出已包含新的 post-commit audit 文案。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `git diff --check`：通过。
- 临时真实 git repo dry-run：covered dirty path 提交后 `review-branch --dry-run --pass` 通过；随后新增未覆盖 `README.md` 提交会被 Phase 2 stale 校验阻断。

## Docs SSOT Reconciliation

- 本任务改变长期 workflow evidence contract，已同步 durable docs `docs/requirements/requirement-main.md`。
- 任务 artifact 中的临时规划、验证细节保留为 task history；长期可复用规则已同步到 workflow README 与 `.trellis/spec/workflow/*`。
- 不涉及服务部署形态、CI/CD workflow、Docker、Compose、K8s/Kustomize、DB migration 或 Makefile 运行入口变更。

## 风险与回滚点

- 风险：提交路径比较使用错误 diff range 会误判 coverage。用单测固定 `<recorded_head>..HEAD` 的行为。
- 风险：只改 canonical 未同步 dogfood installed copy。用 overlay apply 与 drift check 防止漂移。
- 回滚点：Python helper 与文案改动可独立回滚；若 helper 回滚，相关测试与文档必须一起回滚。
