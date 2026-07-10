# #96 实施计划

## 执行顺序

1. 建立 contract 与 fixture。
   - 新增 `task-start-context.schema.json`，定义字段白名单、repo-relative path 和 forbidden local state。
   - 删除 `intake-handoff.schema.json`，更新 config template 与 extension manifest 公共 API。
   - 在单测中先建立 task context、runtime cache、并行 task 和 forbidden-path fixtures。
   - 为 preset installer 增加 obsolete managed artifact 清单和安全删除/冲突保留 fixture。

2. 重构 canonical prepare/runtime writer。
   - 移除 handoff path/load/write helper 和 payload 字段。
   - 实现 task-start-context writer/loader/validator。
   - 实现 `.trellis/.runtime/guru-team/workspaces|tasks/*.json` 原子 writer/loader/rebuilder。
   - 保持 planner-only stdout-only；create-worktree 只写 workspace runtime；create-task 再写 task context 与 task runtime。

3. 重构 workspace boundary 与下游读取。
   - 使用当前 checkout、task context、runtime cache、`git worktree list` 实时推导 workspace。
   - 每次重算 branch、dirty、base freshness、fetch/fast-forward 和 worktree existence。
   - 迁移 finish/check/review/publish、issue ledger seed 和 human artifact resolver 对 `load_handoff()` 的依赖。

4. 增加写入边界与安全测试。
   - 断言 task-start-context 不含绝对路径、runtime path、完整 preflight、existing worktrees、dirty/fetch 或 developer identity path。
   - 断言 runtime cache 被 ignore 且删除后可通过 current checkout/task context/worktree list 重建。
   - 创建同一 developer 的两个并行 task fixture，断言 tracked Trellis metadata diff 不共享固定路径。
   - 断言普通 task 命令不修改 `.trellis/workspace/**`、`.trellis/.developer`、共享 config/workflow/preset/schema/overlay。

5. 更新 workflow/spec/docs canonical source。
   - 修改 canonical workflow、README、requirements docs 和 `.trellis/spec/workflow/**`。
   - 修改 preset overlays 中所有受支持平台入口，统一使用“任务启动上下文”和“本机运行态”。
   - 删除 handoff artifact/public API 文案；仅保留 agent replacement 流程描述所需的自然语言“交接摘要”，并明确其不是 repository artifact。

6. 同步 dogfood installed copies。
   - 执行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
   - 逐项处理 `.new` / `.bak`。
   - 执行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
   - 验证 dogfood 和升级目标均不存在旧 `.trellis/guru-team/handoff.json` 与 `schemas/intake-handoff.schema.json` 残留。

7. Phase 2 check。
   - 运行 JSON/schema、shell、Python compile、canonical unit tests、task validation、context reads、drift 和 `git diff --check`。
   - 使用 `trellis-check` 子代理覆盖完整 task scope、数据流、路径安全、docs SSOT 和 canonical/dogfood 一致性。
   - 记录 `phase2-check.json`，未通过不得提交。

8. 开箱即用验证。
   - 执行 `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` 或扩展该脚本覆盖 Issue #96。
   - 在干净临时 repo 验证 marketplace workflow preview/install、preset install、可执行权限和平台入口。
   - 创建普通 task，断言无 `.trellis/guru-team/handoff.json`、无 `.trellis/workspace/**` 写入、task context 可移植、runtime cache ignored。

9. Upgrade/update 验证。
   - 在 throwaway repo 执行 `trellis update`；若当前 CLI 使用不同的官方 update 命令，先从 `trellis --help` 和官方文档确认后执行。
   - 检查 `.trellis/.template-hashes.json`、`.new`、`.bak` 和 preset 重应用结果。
   - 重新运行普通 task fixture，确认 task context/runtime boundary 语义未回退。
   - 覆盖旧 managed file 未修改时确定性删除、被用户修改时 fail-safe 保留并报告冲突两条路径。

10. Commit、Branch Review Gate 与发布。
   - 工作提交只 stage Issue #96 明确范围和当前 task artifacts。
   - Branch Review 覆盖 `origin/main...HEAD` 完整 diff，保留 raw reports 和 final rollup。
   - PR readiness 明确安全、部署、配置、schema、脚本、CI/CD、容器、K8s、DB migration、Makefile 影响。
   - PR body 使用 `Closes #96`；`#53`、`#97`、`#98`、`#99`、`#100` 只作为 related/followup，不关闭。

## 验证命令

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-10-096-task-runtime-boundary
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.4
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
git diff --check
```

实现中根据新增 schema/validator 增加以下专项验证：

```bash
# task-start-context schema 与 forbidden-key/path 扫描
# runtime cache gitignore 与 cache-miss 重建
# 两个并行 task 的 tracked metadata path diff
# planner-only 零写入与 create-worktree/create-task 分层写入
# trellis update 后重新应用 preset 和行为回归
```

## Phase 2 检查重点

- 数据 ownership 是否严格拆成 task-local portable、local-only runtime、tracked shared config 三层。
- 是否彻底移除 handoff artifact/public API，而不是仅改文件名。
- 所有 `load_handoff()` 调用点是否完成语义迁移。
- workspace boundary 是否完全摆脱 committed absolute workspace path。
- 普通 task 路径是否只写 allowlist；workflow/config 变更是否全部被本 issue scope 覆盖。
- canonical、schema、config、manifest、README、requirements docs、overlays 和 dogfood copies 是否一致。
- throwaway install 与 upgrade/update 是否基于干净状态，而非 dogfood 历史 patch。

## 回滚点

- schema/fixture 与 Issue 固定字段不一致时，停在步骤 1 重新审查设计。
- prepare writer 无法保持 planner-only 零写入时，不进入下游迁移。
- 任一 finish/check/review/publish 路径仍依赖旧 handoff 时，不执行 dogfood apply。
- `.new` / `.bak` 未处理或 drift check 失败时，不提交。
- throwaway 或 update 验证失败时，不声称开箱即用；先修复或在 PR body 明确阻塞与风险。

## 计划提交范围

- `.trellis/tasks/07-10-096-task-runtime-boundary/**`
- `trellis/workflows/guru-team/**`
- `trellis/presets/guru-team/**`
- `trellis/guru-team-extension.json`
- `.trellis/guru-team/**`
- `.trellis/workflow.md`
- `.agents/skills/**`
- `.codex/prompts/**`、`.codex/skills/**`
- `.cursor/commands/**`
- `.claude/commands/trellis/**`
- `.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`.trellis/spec/docs/**`
- `docs/requirements/**`
- installer 管理的 ignore 文件（仅当干净安装验证证明需要）

不 stage 用户或其他 task 的并行改动；不修改 Trellis upstream、全局 npm 包或 `node_modules`。
