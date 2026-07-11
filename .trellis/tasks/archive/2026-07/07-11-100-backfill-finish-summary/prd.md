# Issue #100：为既有 archived tasks 回填 finish-summary 历史索引

## 1. 来源与目标

- Source issue：<https://github.com/castbox/guru-trellis/issues/100>。
- 前置 issue：#97 已关闭并合并到 `main`，当前任务基线为 `920e7f9f797efb6356286f638efc1995ffe4075d`。
- 目标：为 `.trellis/tasks/archive/**/<task>/` 中缺失 `finish-summary.json` 的历史任务提供一次性、确定性、可预览的 backfill，使 #98 能发现既有归档历史。
- #97 的 `finish-summary.schema.json` 与 Python validator 是字段类型、必填、长度、数组上限、路径净化、禁止内容和 backfill 例外的唯一 SSOT；本任务只增加固定抽取规则、CLI、安装资产、文档和历史产物。

## 2. 已确认事实

- 当前仓库有 45 个 archived task，其中 44 个缺失 `finish-summary.json`。
- canonical Python 已定义 `guru-team.finish-summary-backfill`、`backfill` metadata 校验和共用 `finish_summary_errors()`，但没有 backfill CLI 或 bash wrapper。
- preset installer 通过 `MANAGED_ASSET_PATHS` 显式安装 companion scripts；新增 wrapper 必须加入该列表并同步 dogfood copy。
- 当前 #97 schema 将 `index.affected_surfaces` 限制为 1 到 20 条。
- 历史 `review-gate.json.changed_files[]` 实际最多 96 条，因此 #100 的“每个 changed path 生成一条 surface”与 #97 schema 上限在真实数据上冲突。
- 用户已确认按 `kind` 聚合 surface，GitHub-visible 澄清记录为 <https://github.com/castbox/guru-trellis/issues/100#issuecomment-4941094903>。
- 第 1 轮 Branch Review 在 HEAD `4398046075ac0432a11e1d4687c39488723d2df0` 发现 3 个 P2：显式 `--task` 未验证 task root、固定 fallback/phrase 合同偏差、人类 preview 字段不完整。
- 用户已确认 phrases 与 #97 completion-marker 的最小兼容规则，GitHub-visible 澄清记录为 <https://github.com/castbox/guru-trellis/issues/100#issuecomment-4941670415>。
- 实现复核确认精确 problem fallback 会在 `retrieval_text` 的 task title / problem 边界触发 #97 相邻重复校验；用户已确认严格 backfill-only 例外，GitHub-visible 澄清记录为 <https://github.com/castbox/guru-trellis/issues/100#issuecomment-4941812435>。
- Phase 2 确认 pr-body-only 第一列表项会同时成为 outcome 与 `changed_behavior[0]`，从而在 `retrieval_text` 形成第二处确定性边界重复；用户已确认保留两个字段并增加严格 backfill-only 例外，GitHub-visible 澄清记录为 <https://github.com/castbox/guru-trellis/issues/100#issuecomment-4942002004>。

## 3. 功能需求

### R1. CLI 与扫描边界

- 新增 `.trellis/guru-team/scripts/bash/backfill-finish-summary.sh`，wrapper 只调用 canonical `guru_team_trellis.py backfill-finish-summary`。
- `--dry-run` 与 `--write` 必须二选一；`--force` 只能与 `--write` 同用；非法组合退出 2。
- `--task` 只接受 repo-relative、无 `..` segment、位于 `.trellis/tasks/archive/**/<task>/` 的真实 task root；目标必须含白名单 artifact marker，且 archive root 到目标之间不得存在另一个 task root marker。active task、分组目录、task 子目录、绝对路径、symlink escape 和 repo 外路径退出 2。
- 未提供 `--task` 时扫描全部 archived task；不读取 active task、`.trellis/workspace/**`、`.trellis/.runtime/**`，不访问 GitHub，不调用 `trellis mem`。
- 缺少 `--json` 时输出人类可读表格；每个 `to_write` 项必须显示 `source_artifacts`、`missing_fields` 和 `confidence`。`--json` 输出固定 JSON object，退出码语义一致。

### R2. 固定数据来源与抽取

- 只读取 issue #100 白名单中的 10 类 task-local artifact；JSON 损坏必须记录错误并继续批次，不能把损坏内容作为来源。
- `task`、`git`、`github`、`artifacts`、`index.*` 严格按 issue #100 的优先级生成，不做复杂语义推断，不编造 issue、PR、commit、path 或行为变化。
- 生成器固定为 `guru-team.finish-summary-backfill`，状态固定为 `completed`，并包含 schema-valid `backfill` metadata。
- `retrieval_text` 必须复用 #97 的 `finish_summary_retrieval_text()`；最终 payload 必须通过现有 `finish_summary_errors(..., task_dir=...)`。
- `source_artifacts` 只记录实际存在且成功读取的白名单 artifact；`missing_fields`、`confidence` 按 issue #100 固定规则生成。
- `affected_surfaces` 按 issue 定义的 path-prefix `kind` 聚合；每个 surface 的 `paths[]` 完整、去重、排序，不截断 `git.changed_paths` 或 `index.search_terms.paths`，不修改 #97 schema。
- `problem` 和 `outcome` fallback 必须逐字使用 issue #100 定义的 `<task.title>；旧行为：历史 artifact 未记录。` 与 `<task.title>；非目标：历史 artifact 未记录。`。
- phrases 必须先按 issue #100 固定来源顺序生成、去重，并在少于 3 条时只使用 `task.slug`、`task.title`、`历史归档 task` 补足；仅当结果仍不含 #97 `FINISH_SUMMARY_COMPLETION_MARKERS` 任一标记时追加唯一固定 fallback `历史归档 task 已完成`，不得替换或改写既有 phrase。
- validator 必须仅在 `generator=guru-team.finish-summary-backfill` 且 `index.problem` 精确匹配 `<task.title>；旧行为：历史 artifact 未记录。` 时，对 `retrieval_text` 在 task title / problem 边界出现的这一处确定性相邻重复不报错；其它相邻重复、其它字段和正常 `guru-team.finish-work` 必须继续按 #97 原规则拒绝。
- 当 outcome 的高优先级来源均缺失、pr-body 变更摘要只有列表、outcome 确由第一列表项生成且精确匹配 `changed_behavior[0]` 时，validator 必须只对 `retrieval_text` 的 outcome / behavior 边界这一处确定性重复不报错；实现必须保留完整 `changed_behavior`，并继续拒绝非 pr-body-only 来源、非首项匹配、派生文本不一致、仍含其它相邻重复和 normal finish-work。

### R3. 写入与错误隔离

- dry-run 不写文件，预览 `to_write`、`skipped`、`errors`、source artifacts、missing fields 和 confidence。
- write 只写缺失的 `finish-summary.json`；已有文件在未提供 `--force` 时跳过，只有 `--write --force` 才覆盖。
- 单个 task 的损坏 JSON、缺失 artifact 或最终 schema 失败不得中断其它 task；无法生成 schema-valid payload 的 task 必须留在 `errors[]` 且不得写文件。
- 所有目标路径必须位于对应 archived task 目录；不创建 committed 全局 index。
- 修复 fallback/phrase 规则后必须用最终 builder 重建全部 44 个 backfill summary；#97 正常 summary 不得覆盖。

### R4. Canonical、preset、dogfood 与文档

- canonical Python、bash wrapper、tests、preset installer asset list、extension public companion list、workflow/README/spec 文档必须表达同一命令合同。
- 运行 `apply.sh --repo . --all-platforms` 后，canonical 与 `.trellis/guru-team/**` dogfood copy 必须一致，且 overlay drift 为零。
- 本仓库一次性执行 dry-run，再执行 write，为 44 个缺失历史任务生成 summary；写入后再次 dry-run 必须全部显示为 skipped 或已有文件。
- throwaway repo 必须验证 preset 安装后 wrapper 可执行并能 dry-run；upgrade/update 兼容性验证必须证明 reapply 后能力仍存在。

## 4. 非目标

- 不修改 #97 schema 或正常 finish-work/publish 路径。
- 不实现 #98 的历史发现命令。
- 不恢复 workspace journal，不创建全局 index。
- 不修改 Trellis upstream、全局 npm、`node_modules` 或官方 Trellis workflow。
- 不创建 release tag。

## 5. 已确认设计决策

- `affected_surfaces` 按 `kind` 聚合，并在 surface `paths[]` 保留全部路径。单个 kind 超过 schema 的 100-path 上限时按稳定排序分批；若完整表达仍会超过 20 个 surface，则该 task fail closed、写入 `errors[]` 且不生成文件。
- 不扩大 #97 schema，不截断历史 path，不把路径信息藏入自然语言字段。
- phrases 的固定 completion fallback 只解决 #97 validator 与 #100 固定来源在 8 个历史任务上的交集，不扩大其它字段、来源或正常 finish-work 合同。
- 显式 `--task` 与无参数 discovery 共用 task-root marker/ancestor 判定；task 子目录和 archive 分组目录不能成为写入目标。
- `0.6.5-guru.3` 尚未发布 release tag，本任务更新其尚未发布的 public companion list，不创建新版本号或 tag。

## 6. Docs SSOT 状态

- 状态：`complete_docs`。现有 `workflow.md`、README、`.trellis/spec/workflow/{companion-scripts,data-contracts}.md` 与 preset installer spec 已完整描述 #97 正常路径，但尚未描述 #100 backfill 增量。
- 策略：`ssot_first`。实现时先把确认后的 CLI、抽取、超限和一次性迁移合同写入 durable workflow/spec/README，再同步 dogfood copy。
- Durable docs：`trellis/workflows/guru-team/workflow.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/data-contracts.md`，以及安装资产规则变化对应的 `.trellis/spec/preset/installer.md`。

## 7. 验收标准

- [ ] CLI 参数、扫描边界、JSON/表格输出和退出码符合 R1。
- [ ] 生成 payload 符合 #97 schema/validator，且没有旧式顶层 `summary` / `keywords`。
- [ ] 测试覆盖空 archive、skip、force、complete/partial/minimal、损坏 JSON、路径净化、index 生成和旧字段拒绝。
- [ ] 测试覆盖显式 `--task` 对 task root、task 子目录、archive 分组目录和 symlink escape 的统一判定。
- [ ] 测试覆盖 issue 固定 problem/outcome fallback、8 个 completion fallback 分支和 JSON/table preview 字段一致性。
- [ ] 测试覆盖 4 个真实 problem fallback 冲突 fixture、严格 backfill-only 边界例外，以及 normal finish-work / 非精确 fallback / 其它相邻重复继续拒绝。
- [ ] 测试覆盖 pr-body-only 第一列表项同时生成 outcome 与 `changed_behavior[0]`，并覆盖 paragraph 优先、其它 outcome 来源、非首项匹配、派生篡改、其它相邻重复和 normal finish-work 继续拒绝。
- [ ] 44 个既有缺失 task 完成一次性回填，所有新文件通过 validator。
- [ ] canonical tests、preset tests、compile、shell syntax、JSON、task validation、overlay drift、canonical/dogfood equality 和 `git diff --check` 全部通过。
- [ ] throwaway 安装与 upgrade/update 兼容性验证通过；若环境阻塞，PR body 明确记录未验证项和风险。
