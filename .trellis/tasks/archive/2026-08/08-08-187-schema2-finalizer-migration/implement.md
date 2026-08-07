# 实施计划

## Phase 0：基线与契约

- [ ] 运行 workspace boundary 检查并确认当前 task/worktree 身份。
- [ ] 先更新 canonical Finalizer contract 和 closeout-plan schema，定义 reviewed tracked binding 与 schema 2.0 migration normalization。
- [ ] 为 schema validator 增加 path 唯一性、tracked 集合归属、mode、SHA-256 和闭合集合校验。

## Phase 1：Plan builder

- [ ] 抽取 live Git index 分类 helper，统一计算 `tracked_move_paths` 与 `untracked_archive_outputs`。
- [ ] existing schema 2.0 projection 保留 move set，但不再复用历史 tracked/untracked 分类。
- [ ] 基于 transaction-parent blob 与当前工作树生成最小 reviewed tracked binding 集合。
- [ ] 增加受支持 migration delta 判定，仅接纳同一 active task、同一 review identity、同一 move set 的已知分类/绑定升级。

## Phase 2：直接 consumer

- [ ] 修改 pre-move continuity，使 parent bytes 或精确 binding 任一匹配时通过，其他变化阻塞。
- [ ] 修改 verification fallback expected dirty set，纳入当前匹配的 tracked binding。
- [ ] 确保 archive transaction 继续从同一 projection 读取分类和 move paths。
- [ ] 对被裁剪 metadata intermediate 保留 move、validate、prune 的显式顺序。

## Phase 3：恢复与 wrapper

- [ ] 修正 public wrapper 的 checker 参数重建，使其与 direct checker 使用同一 plan-derived 上下文。
- [ ] 保留 checker-passed `blocked` / `evidence_ready` route，不错误包装成 `owner_result_not_checked`。
- [ ] 验证 existing Draft recovery 复用唯一 Draft，且不触发 Branch Review 或重复 PR。

## Phase 4：回归测试

- [ ] tracked legacy `closeout-plan.json` + untracked `finish-summary.json` 分类测试。
- [ ] dirty reviewed `prd.md` / `design.md` / `implement.md` 内容绑定通过测试。
- [ ] dirty 可裁剪 metadata intermediate 绑定、移动后裁剪测试。
- [ ] 未绑定 path、digest drift、mode drift 负例测试。
- [ ] verification network fallback 接受 plan-owned tracked metadata、拒绝额外 dirty path 测试。
- [ ] direct checker 与 public wrapper blocked/evidence-ready 一致性测试。
- [ ] existing Draft same-plan/migration resume 不创建重复 PR、不重跑 Branch Review 测试。

## Phase 5：同步与验证

- [ ] 运行目标 Python 单元测试和 Finalizer contract tests。
- [ ] 运行完整 `test_guru_team_trellis.py`、Skill package tests、schema/compile/shell syntax 与 `git diff --check`。
- [ ] 运行 preset `apply.sh --repo .`，处理所有 `.new` / `.bak`，再运行 dogfood overlay drift checker。
- [ ] 验证 canonical、installed shared、Codex、Claude、Cursor package bytes 一致。
- [ ] 在 clean throwaway repo 验证 marketplace workflow、preset install/reapply、Finalizer wrapper discovery/invocation 和基础 Phase 入口。
- [ ] 若外部网络或环境导致任一门禁无法执行，在 Phase 2 check 和最终报告中明确标记为未验证，不以静态测试替代。

## Phase 6：Trellis 质量闭环

- [ ] 按 `codex.dispatch_mode: sub-agent` 由 `trellis-implement` 执行实现，不生成 `implementation-handoff.md`。
- [ ] 由独立 `trellis-check` 执行实现检查并修复 findings。
- [ ] 主会话执行 `guru-check-task`，覆盖需求、设计、实现、测试、Docs SSOT 与分发一致性。
- [ ] 未获得单独授权前不 commit、push、创建 PR 或修改 Issue。

## 预期变更文件

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/workflows/guru-team/schemas/closeout-plan.schema.json`
- `trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md`
- `trellis/skills/guru-team/packages/guru-finalize-task/schemas/closeout-plan.schema.json`
- 由 preset 同步生成的 installed/platform 对应副本
- 必要的 `.trellis/spec/workflow/` SSOT 小范围更新

## 完成定义

全部 Issue #187 验收场景有自动化证据，Finalizer 公共合同保持兼容，canonical 与安装副本无漂移，且完整 Phase 2 语义检查通过。外部 consumer 现场不作为本任务写入目标。
