# #27 实施计划

## 前置证据

- 已读取并更新 issue #27。
- 已运行 Guru Team Phase 0 intake/preflight，worktree 已创建。
- 已读取 `.trellis/spec/workflow/`、`.trellis/spec/preset/`、shared guide 与 `trellis-meta`。
- 官方 Trellis 文档结论：workflow 行为应通过 workflow Markdown 和 marketplace/preset 扩展面表达；companion scripts 只执行确定性动作与校验。

## 步骤

1. 修正 task metadata 与 issue ledger。
2. 在 canonical `guru_team_trellis.py` 中增加 finish-work dry-run plan 构造逻辑。
3. 调整 `cmd_finish_work()`：readiness 校验完成后，dry-run 直接返回 plan，不执行 archive/journal/metadata commit/publish。
4. 更新 parser help。
5. 更新单测：
   - dry-run 不调用 archive；
   - dry-run 不调用 add_session；
   - dry-run 不调用 `commit_if_metadata_dirty`；
   - dry-run 不调用 `cmd_publish_pr`；
   - dry-run payload 包含计划字段。
6. 更新 workflow/README 文案，说明 dry-run 是无副作用 readiness preview。
7. 运行 preset apply 同步 dogfood 安装副本。
8. 执行可行的 dry-run 无副作用验证；如完整 throwaway install 验证耗时或受环境限制，最终报告列出未覆盖项。
9. 扩展 issue #27 正文，把 Codex dispatch 默认模式纳入当前交付范围。
10. 修订 config template 与 dogfood config：默认 `codex.dispatch_mode: sub-agent`，保留显式 `inline`。
11. 修改 Codex hook 与 workflow phase parser：缺省/非法配置走 `sub-agent`，显式 `inline` 才走 inline。
12. 检查并必要时补强 Codex agent prelude，确认 sub-agent 通过 `Active task:` / `task.py current --source` 加载上下文。
13. 更新 workflow/README/preset README，说明 Codex 默认 sub-agent 与 inline 降级语义。
14. 增加或调整测试覆盖默认 sub-agent、显式 inline、hook banner 与 workflow phase selection。
15. 重新运行 preset apply、dogfood drift check、单测和完整验证。

## Phase 2 Check 覆盖计划

- requirements：对照 issue #27 扩展后的验收标准。
- design：确认 dry-run 分支只读且正式路径不变；确认 Codex 默认 sub-agent 与 Branch Review Gate 独立 review 要求一致。
- code：检查 companion helper、Codex hook、workflow phase parser、config template、agent prelude、测试、文档同步。
- tests：运行 targeted unit tests、hook/parser tests 和脚本语法/编译检查。
- spec_sync：判断是否需要更新 `.trellis/spec/`；Codex dispatch 默认行为属于 workflow/preset 约定，若现有 spec 未覆盖需补充。
- cross_layer：检查 canonical、preset overlay、dogfood copy、README/workflow/config/hook/parser 文案一致。
- docs_ssot：更新 README/workflow/config comments。
- deployment：本仓库无部署资产；确认无需 Docker/Compose/K8s/DB/Makefile 变更。
