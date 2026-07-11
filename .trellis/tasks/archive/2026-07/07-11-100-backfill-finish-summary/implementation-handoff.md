# Issue #100 实现交接

## 完成状态

- 状态：Implementation Complete，新一轮 Phase 2 `trellis-check` 已通过。Branch Review F-001/F-002/F-003 与 Phase 2 新发现的 4 个 P2 均已按批准合同修复。
- 实现代理：`/root/trellis_implement_100`。
- Phase 2 检查代理：`/root/trellis_check_100_round2`。
- 未执行：Phase 2 recorder、commit、push、Branch Review Gate 和发布 recorder。

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
- 最终 builder 通过逐 task 显式 `--task --write --force` 重建 44 个 backfill summary，全部为 `partial`；主要缺失字段为不可验证的 `github.pr_url`。
- 40 个 summary 恢复原 active `task.artifact_dir`；4 个旧 gate 仅保留 archive path，按 schema 例外留空并记录 missing field。
- Python validator 与 Draft 2020-12 JSON Schema：45/45 通过。
- 写后 dry-run：0 candidates，45 skipped，0 errors。
- 44/44 去时间字段确定性重建通过，44/44 surface paths 与 `git.changed_paths` 完全一致，敏感路径扫描 45/45 通过。
- #97 正常 finish-work summary 的 SHA-256 在重建前后均为 `f18370b72df53c720f33e170b2113a6a7958311913f787a4c64279e7d025fd80`。

## 已运行验证

- Canonical unittest：334 passed（含 Branch Review 与 Phase 2 回归）。
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

## Phase 2 自修复闭环

- P2-1：按 GitHub comment `4942002004` 支持 pr-body-only 第一列表项 outcome，同时保留完整 `changed_behavior`；validator 只允许可从 task-local source 重建的 outcome / `changed_behavior[0]` 单边界重复。现存 44 份 backfill 中 13 份命中该分支。
- P2-2：`git.commits` 改为按 `task.json.commit` -> `review-gate.json.head` -> `pr-readiness.json.commits[]` 取第一个非空有效来源，不再 union 低优先级值；非法 SHA/类型 fail closed。
- P2-3：`complete` confidence 现在强制要求非空 `git.branch`；结构证据齐全但 branch 缺失的 fixture 回归为 `partial`。
- P2-4：`minimal` 只允许 basename、task title/name 或 Markdown H1 基础来源；artifact/base/branch/commit、issue/PR、problem/outcome/behavior、review summary、checklist 或 contract table 任一语义/溯源证据都使 confidence 至少为 `partial`。
- 负向回归覆盖 paragraph/更高 outcome 优先级、source drift、行为列表不完整、retrieval 篡改、其它重复和 normal finish-work；通用 retrieval/text helper 与 #97 schema 未修改。

## Branch Review 第 1 轮修复交接

### F-001 已完成：统一 archived task-root 判定

- Explicit `--task` 与 discovery 共用 direct marker：白名单 artifact 或现有 `finish-summary.json`。
- Explicit 目标必须有 marker，且 archive root 到目标的严格祖先不得已有 marker；因此月份/日期分组、无 marker 子目录、任意带 nested marker 的 task 子目录均在扫描/写入前退出 2。
- Discovery 使用 top-down walk，命中 task root 后停止下降，不依赖 `research` / `reviews` basename 特判；symlink 目录不递归，escape 继续 fail closed。
- 回归覆盖真实 task root、archive 分组、plain child、arbitrary nested marker、research/reviews 等价子目录、symlink escape，以及 dry-run/write/write-force 均不产生错误位置的 summary。

### F-003 已完成：JSON/table preview parity

- 非 JSON 表格的每个 `to_write` 行稳定显示 `source_artifacts`、`missing_fields`、`confidence`。
- 回归同时构造 complete、partial、minimal 三类 preview，并逐项将 JSON 值序列化后匹配文本表格行。

### F-002 已完成：精确 fallback 与严格 backfill-only retrieval 例外

- GitHub comment `4941812435` 已批准严格 backfill-only 例外；durable data contract、canonical/dogfood Python 与测试已同步该合同。
- Builder 已恢复逐字 problem fallback `<task.title>；旧行为：历史 artifact 未记录。` 和 outcome fallback `<task.title>；非目标：历史 artifact 未记录。`；最终数据分别触发 6 个和 6 个 task。
- Final validator 只有在 generator、problem、retrieval 首两行和 deterministic derivation 全部精确匹配，且删除首行后的 retrieval 不含其它相邻重复时，才过滤这一条 title/problem 边界错误。
- Exact problem/outcome phrase 候选只有在其首 clause 与上一条保留 phrase 的末 clause 相同时才跳过整条候选；不改写候选、不扩为通用 clause 去重，之后仍执行少于 3 条补足和唯一 completion fallback。
- 回归覆盖 4 个真实冲突 title、normal finish-work、非精确 fallback、其它相邻重复、精确 outcome、minimal 边界和 8 个真实 completion fallback fixture；正常 helper、schema 与 finish-work 行为未修改。
- 最终 44 份 backfill 已整体重建；problem/outcome/completion fallback 统计为 6/6/8，pr-body-only outcome 分支为 13，0 个构建或 validator error，#97 正常 summary 字节未变。

### 本轮验证结果

- Canonical unittest：334 passed；preset unittest：36 passed。
- `py_compile`、全部 canonical/preset Bash `bash -n`、task validate、`git diff --check`：通过。
- Canonical/dogfood workflow、Python、wrapper 一致；overlay drift 为零；无 `.new` / `.bak`。
- 现存数据保持 Python validator 45/45、Draft 2020-12 JSON Schema 45/45、当前 builder 确定性重建 44/44、surface path 守恒 44/44、敏感路径扫描 45/45、写后 dry-run 45 skipped / 0 errors。
- Fresh throwaway 使用可达 `gh:castbox/guru-trellis/trellis#main` 样本完成 init、当前 canonical preset apply、wrapper dry-run、workflow preview/switch、`trellis update --force`、workflow 重选、preset reapply 和 sidecar gate；当前分支仍须 push 后执行真实 remote marketplace gate。
