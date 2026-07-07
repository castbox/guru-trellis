# #52 实施计划

## Phase 1 收口

- [x] 读取 source issue #52、官方 Trellis 文档、本仓库 workflow/spec/docs。
- [x] 创建 worktree、branch、Trellis task 与 handoff。
- [x] 写 `prd.md`、`design.md`、`implement.md`。
- [ ] 向用户展示三份规划文档链接，并等待明确 post-planning review confirmation。
- [ ] 用户确认后，调用 `record-planning-approval.sh` 并运行 `check-planning-approval.sh`。
- [ ] `task.py start` 进入 implementation。

## 实现步骤

1. Script 变更
   - 修改 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
   - 将 planning approval artifact schema 升级为 `1.1`。
   - 默认记录 `review_prompt_presented_at`、`approved_at`、`reviewed_artifacts[]`，并保留 `approved_artifacts` alias。
   - 强制 `user_confirmation.source = explicit-post-planning-review`。
   - Validator 要求 `prd.md`、`design.md`、`implement.md` 三份文档完整且 digest 匹配。
   - 更新 CLI help / 参数，必要时保持 backward-compatible 输入但 fail closed 检查旧 source。

2. 测试变更
   - 更新 `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
   - 覆盖有效 approval、Phase 0 confirmation 误用、缺文档、文档修改后失效。
   - 覆盖 Phase 2 或 Branch Review 对 stale planning approval 的阻塞路径。

3. Workflow / overlay 变更
   - 更新 `trellis/workflows/guru-team/workflow.md`。
   - 更新 `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`。
   - 更新 Codex / Claude / Cursor continue prompt/skill/command。
   - 更新 canonical implement agent overlays，要求 dispatch 前置 valid planning approval evidence；subagent 发现缺失时停止。
   - 运行 preset apply 同步 `.trellis/workflow.md`、`.agents/skills/**`、`.codex/**`、`.claude/**`、`.cursor/**` 等 dogfood installed copies。

4. Durable docs / spec
   - 更新 `docs/requirements/requirement-main.md`。
   - 更新 `docs/requirements/guru-team-trellis-flow.md`。
   - 更新 `.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/companion-scripts.md` 和 `.trellis/spec/preset/overlay-guidelines.md` 中 planning approval / overlay 要求。

5. Context manifests
   - 更新 `implement.jsonl` / `check.jsonl`，包含 workflow/spec/script/docs/overlay/test 文件。

6. 验证
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - `python3 -m unittest trellis.workflows.guru-team...` 若包名不适合 dotted import，则直接运行测试文件。
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
   - `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`，如耗时或依赖环境失败，记录未覆盖项。

## Sub-agent 执行安排

- 规划批准后，默认 `sub-agent` mode 下派发 `trellis-implement` / channel `implement` 作为 `实现代理`，由其完成实现。
- 主会话只协调、记录 `agent-assignment.json`、运行 recorder/validator、提交与后续 review gate。
- 实现代理 handoff 必须说明已验证 `check-planning-approval` 通过，列出 changed files、验证结果、剩余风险。
- 随后派发 `trellis-check` / channel `check` 作为 `阶段二检查代理`，完成 Phase 2 check。

## 验证与 Review Gate

- Phase 2 check 后记录 `phase2-check.json`。
- Commit task work 后派发独立 review sub-agent 审查 `origin/main...HEAD` 完整 diff。
- Review result 写入 task-local `review.md`。
- 主会话运行 `review-branch.sh --review-source independent-agent --review-report ... --agent-assignment ...`。
- Gate 通过后停止，等待 `trellis-finish-work` closeout。

## 不适用项

- Middle-platform Knowledge Gate 不适用。
- 不涉及数据库 migration、容器/K8s、运行时配置或外部服务。
