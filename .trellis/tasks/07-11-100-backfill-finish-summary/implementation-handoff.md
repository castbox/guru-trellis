# Issue #100 实现交接

## 完成状态

- 状态：Implementation Complete。
- 实现代理：`/root/trellis_implement_100`。
- 未执行：commit、push、Phase 2 check、Branch Review Gate 和发布 recorder。

## 变更范围

- canonical `guru_team_trellis.py` 已实现 backfill CLI、白名单抽取、archive 路径边界、JSON/表格输出、0/1/2 退出码、atomic write 和逐 task 错误隔离。
- canonical/dogfood 已新增 `backfill-finish-summary.sh`。
- `affected_surfaces` 按 kind 聚合，每 surface 最多 100 paths；完整表达超过 20 surfaces 时 fail closed，不截断路径。
- preset installer、installer tests、extension public companion list 和 throwaway verifier 已同步。
- #97 schema 和正常 finish/publish 路径未修改；extension 保持 `0.6.5-guru.3`，未创建 tag。

## Docs SSOT

- 策略：`ssot_first`。
- Durable docs 已更新：`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/preset/installer.md`、canonical/dogfood workflow、workflow README、preset README。
- 实现以更新后的 durable docs 为主要输入；task delta 仅提供 #100 的确认聚合规则和迁移验收范围。
- Task-history-only 内容：本仓库迁移数量、执行证据和 44 份历史 `finish-summary.json`。
- 未遗留 durable docs delta 或当前 PR 限制。

## 历史迁移结果

- 写前：45 scanned，44 candidates，1 existing，0 errors。
- 写入：44 个 backfill summary，全部为 `partial`；主要缺失字段为不可验证的 `github.pr_url`。
- 40 个 summary 恢复原 active `task.artifact_dir`；4 个旧 gate 仅保留 archive path，按 schema 例外留空并记录 missing field。
- Python validator 与 Draft 2020-12 JSON Schema：45/45 通过。
- 写后 dry-run：0 candidates，45 skipped，0 errors。
- 44 个 backfill summary 的 surface paths 与 `git.changed_paths` 完全一致。

## 已运行验证

- Canonical unittest：317 passed。
- Preset unittest：36 passed。
- `py_compile`、全部 Bash `bash -n`、JSON 解析、task validate、`git diff --check`：通过。
- Overlay drift、sidecar 清零、可执行权限、版本/schema 未漂移：通过。
- Workspace boundary 与 planning approval：通过；source checkout clean。
- Throwaway fresh install、workflow preview/switch、`trellis update --force`、workflow 重选、preset reapply、空 archive dry-run：通过。

## Phase 2 Check 重点

- 复核字段优先级与损坏 artifact 的继续策略。
- 复核绝对路径、parent segment、active task、repo 外路径和 symlink escape 拒绝。
- 复核 surface 100-path/20-surface 上限和完整路径不截断合同。
- 复核 44 份历史产物、45/45 schema 验证与二次 dry-run 幂等结果。
- 复核 Docs SSOT、canonical/dogfood/preset/manifest/throwaway verifier 一致性。
- 分支尚未 push；remote marketplace gate 必须在发布阶段验证真实 branch ref。
