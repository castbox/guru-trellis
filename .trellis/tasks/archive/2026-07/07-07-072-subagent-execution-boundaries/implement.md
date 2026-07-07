# #72 实施计划

## 1. 读取与定位

- 读取 issue #72、task artifacts、workflow specs、preset overlay specs、durable docs。
- 搜索 `trellis-implement`、`trellis-check`、`phase2-check`、`Branch Review Gate`、`agent-assignment`、`实现代理`、`阶段二检查代理`、`最终放行审查代理`。

## 2. Canonical workflow

- 更新 `trellis/workflows/guru-team/workflow.md`：
  - Sub-agent Boundary 增加三个强制边界。
  - Phase 2 `in_progress` 和 2.1/2.2 明确默认 sub-agent mode 下不能由主 agent 替代。
  - Phase 3.5 明确 Branch Review 必须由 review subagent 执行，review subagent 不继续实现、不补 Phase 2 工作。
  - 明确 `phase2-check.json` 的 evidence artifact 语义。

## 3. Overlay 与 agent contract

- 更新 `trellis/presets/guru-team/overlays/`：
  - shared / Codex / Claude / Cursor continue entries。
  - Codex / Claude / Cursor `trellis-implement`、`trellis-check` agent overlays。
  - channel runtime `.trellis/agents/implement.md`、`.trellis/agents/check.md`。
- 保持技术 dispatch id 和 Codex ASCII `nickname_candidates` 不变。

## 4. Durable docs / README

- 更新 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` 和 `docs/requirements/**` 中长期流程说明，确保文档明确：
  - subagent 执行工作；
  - main agent 协调；
  - scripts recorder/validator；
  - `phase2-check.json` 不是脚本替代 check；
  - Branch Review subagent 不替 implement/check 补工作。

## 5. Dogfood 同步

- 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 同步 installed copies。
- 检查并处理 `.new` / `.bak`。
- 运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。

## 6. Subagent 执行与检查

- 规划批准后，主线程 dispatch `trellis-implement` 作为 `实现代理` 完成实现。
- 实现完成后，主线程 dispatch `trellis-check` 作为 `阶段二检查代理` 完成 Phase 2 check 和必要自修复。
- 主线程只记录 assignment/status evidence 与 `phase2-check.json`，不把自己的命令结果当成 check。

## 7. 验证与提交

- 运行设计中的验证命令。
- 记录并校验 `phase2-check.json`。
- 确认 dirty state 后提交 task work。
- commit 后 dispatch 独立 review subagent，写 `review.md`，再由主线程运行 Branch Review Gate recorder。

## 8. 回滚

- 若 overlay apply 产生不可接受 `.new` / `.bak`，先回到 canonical diff，重新确认 overlay 源头。
- 若 workflow parsing 失败，回滚最近 workflow 文案变更并缩小 patch。
