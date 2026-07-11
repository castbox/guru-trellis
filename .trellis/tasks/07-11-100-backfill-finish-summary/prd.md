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

## 3. 功能需求

### R1. CLI 与扫描边界

- 新增 `.trellis/guru-team/scripts/bash/backfill-finish-summary.sh`，wrapper 只调用 canonical `guru_team_trellis.py backfill-finish-summary`。
- `--dry-run` 与 `--write` 必须二选一；`--force` 只能与 `--write` 同用；非法组合退出 2。
- `--task` 只接受 repo-relative、无 `..` segment、位于 `.trellis/tasks/archive/**/<task>/` 的目录；active task、绝对路径和 repo 外路径退出 2。
- 未提供 `--task` 时扫描全部 archived task；不读取 active task、`.trellis/workspace/**`、`.trellis/.runtime/**`，不访问 GitHub，不调用 `trellis mem`。
- 缺少 `--json` 时输出人类可读表格；`--json` 输出固定 JSON object，退出码语义一致。

### R2. 固定数据来源与抽取

- 只读取 issue #100 白名单中的 10 类 task-local artifact；JSON 损坏必须记录错误并继续批次，不能把损坏内容作为来源。
- `task`、`git`、`github`、`artifacts`、`index.*` 严格按 issue #100 的优先级生成，不做复杂语义推断，不编造 issue、PR、commit、path 或行为变化。
- 生成器固定为 `guru-team.finish-summary-backfill`，状态固定为 `completed`，并包含 schema-valid `backfill` metadata。
- `retrieval_text` 必须复用 #97 的 `finish_summary_retrieval_text()`；最终 payload 必须通过现有 `finish_summary_errors(..., task_dir=...)`。
- `source_artifacts` 只记录实际存在且成功读取的白名单 artifact；`missing_fields`、`confidence` 按 issue #100 固定规则生成。
- `affected_surfaces` 按 issue 定义的 path-prefix `kind` 聚合；每个 surface 的 `paths[]` 完整、去重、排序，不截断 `git.changed_paths` 或 `index.search_terms.paths`，不修改 #97 schema。

### R3. 写入与错误隔离

- dry-run 不写文件，预览 `to_write`、`skipped`、`errors`、source artifacts、missing fields 和 confidence。
- write 只写缺失的 `finish-summary.json`；已有文件在未提供 `--force` 时跳过，只有 `--write --force` 才覆盖。
- 单个 task 的损坏 JSON、缺失 artifact 或最终 schema 失败不得中断其它 task；无法生成 schema-valid payload 的 task 必须留在 `errors[]` 且不得写文件。
- 所有目标路径必须位于对应 archived task 目录；不创建 committed 全局 index。

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
- `0.6.5-guru.3` 尚未发布 release tag，本任务更新其尚未发布的 public companion list，不创建新版本号或 tag。

## 6. Docs SSOT 状态

- 状态：`complete_docs`。现有 `workflow.md`、README、`.trellis/spec/workflow/{companion-scripts,data-contracts}.md` 与 preset installer spec 已完整描述 #97 正常路径，但尚未描述 #100 backfill 增量。
- 策略：`ssot_first`。实现时先把确认后的 CLI、抽取、超限和一次性迁移合同写入 durable workflow/spec/README，再同步 dogfood copy。
- Durable docs：`trellis/workflows/guru-team/workflow.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/data-contracts.md`，以及安装资产规则变化对应的 `.trellis/spec/preset/installer.md`。

## 7. 验收标准

- [ ] CLI 参数、扫描边界、JSON/表格输出和退出码符合 R1。
- [ ] 生成 payload 符合 #97 schema/validator，且没有旧式顶层 `summary` / `keywords`。
- [ ] 测试覆盖空 archive、skip、force、complete/partial/minimal、损坏 JSON、路径净化、index 生成和旧字段拒绝。
- [ ] 44 个既有缺失 task 完成一次性回填，所有新文件通过 validator。
- [ ] canonical tests、preset tests、compile、shell syntax、JSON、task validation、overlay drift、canonical/dogfood equality 和 `git diff --check` 全部通过。
- [ ] throwaway 安装与 upgrade/update 兼容性验证通过；若环境阻塞，PR body 明确记录未验证项和风险。
