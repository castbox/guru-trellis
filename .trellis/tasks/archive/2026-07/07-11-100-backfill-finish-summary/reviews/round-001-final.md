# 第 1 轮最终放行审查原始报告

## 审查身份

- 角色：最终放行审查代理
- 代理标识：`/root/branch_review_100_final`
- 审查来源：独立 fresh agent
- 基线：`origin/main`（`920e7f9f797efb6356286f638efc1995ffe4075d`）
- 差异范围：`origin/main...HEAD`
- 审查 HEAD：`4398046075ac0432a11e1d4687c39488723d2df0`
- 审查结论：失败，不予最终放行
- 问题数量：3（P0=0，P1=0，P2=3，P3=0）

## 审查范围与证据

本轮独立读取并复核了以下证据：

- GitHub issue #100 全文及 comment `4941094903`；后者确认 `affected_surfaces` 按 `kind` 聚合、完整保留路径，并替代 issue 正文中“一路径一 surface”的冲突表述。
- `prd.md`、`design.md`、`implement.md`、`implementation-handoff.md`、`planning-approval.json`、`phase2-check.json`、`check.jsonl`、`issue-scope-ledger.json`、`agent-assignment.json`。
- `origin/main...4398046075ac0432a11e1d4687c39488723d2df0` 的完整 73 文件 committed diff、唯一 work commit 及完整 commit message。
- Canonical Python、bash wrapper、320 个 canonical tests、preset installer 与 36 个 preset tests、canonical/dogfood workflow、extension manifest、两份 README、durable specs、throwaway verifier。
- 44 份新增 backfill `finish-summary.json` 及 #97 正常 finish-work 生成的既有 summary。
- Trellis 官方 workflow 与 spec marketplace 文档，确认 workflow 应由 Markdown 定义、脚本只执行确定性动作、marketplace/update 必须通过公开扩展面恢复。

## 阻断问题

### F-001 [P2] `--task` 可把 archive 内任意子目录当成 task 根并写入错误位置

- 证据：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:1274` 到 `:1290` 只校验目标位于 archive root 下且是目录，没有确认它是 archived task 根，也没有拒绝 `research/`、`reviews/` 或月份分组目录。
- 复现：

  ```bash
  .trellis/guru-team/scripts/bash/backfill-finish-summary.sh --json --dry-run \
    --task .trellis/tasks/archive/2026-07/07-03-2-align-guru-team-workflow-trellis/research
  ```

  返回 `scanned_tasks=1`、`errors=[]`，并把目标声明为 `.../research/finish-summary.json`。对应 `--write` 会在非 task 根创建 artifact，`--write --force` 还可能覆盖该错误位置的同名文件。
- 合同偏差：issue #100、`prd.md` R1/R3 和 design 4.1 都把写入边界限定为 archived task 目录；无参数 discovery 已排除 `research`/`reviews`，显式 `--task` 却能绕过同一边界。
- 影响：public migration helper 可污染历史 task 的研究/审查子目录或 archive 分组目录，违反“所有目标路径位于对应 archived task 目录”的副作用边界。
- 修订要求：返回 Phase 2，统一 discovery 与 explicit resolver 的 task-root 判定；至少要求目标包含合法 task marker、拒绝 `research`/`reviews` 和分组目录，并补 explicit nested/group/write/force 回归。不要仅按 basename 特判两个已知目录。

### F-002 [P2] 固定文本抽取规则被实现和 durable spec 擅自改写

- 证据：issue #100 固定 `index.problem` fallback 为 `<task.title>；旧行为：历史 artifact 未记录。`，固定 `index.outcome` fallback 为 `<task.title>；非目标：历史 artifact 未记录。`；`search_terms.phrases` 只允许按既定来源和不足 3 条时的 `task.slug`、`task.title`、`历史归档 task` 补齐。
- 实现偏差：`guru_team_trellis.py:1128` 到 `:1139` 改成 `历史问题：...的旧行为未记录。` 和 `历史结果：...；非目标信息未记录。`；`:1090` 到 `:1091` 还会额外加入 `历史归档 task 已完成`。
- 数据影响：44 份新增 summary 中，6 份使用了改写后的 problem fallback，20 份使用了改写后的 outcome fallback，8 份额外包含未在 issue 中定义的 completion phrase。
- Docs SSOT 影响：`.trellis/spec/workflow/data-contracts.md:156` 到 `:158` 把该额外 phrase 固化为 durable 合同，但 planning approval 对应的 `prd/design/implement` 没有这项例外，GitHub comment 也只授权 surface 聚合；这是实现阶段反向改写 SSOT，不是 `ssot_first` 的已批准增量。
- Phase 2 自修复核对：source-issue fallback、绝对路径错误去敏和“只在缺 marker 时添加 phrase”均已进入 committed diff，并有回归；但把无条件补字改为条件补字仍未满足 issue 的固定生成规则，不能视为该 finding 已闭环。
- 影响：历史检索文本不再是 issue 指定的确定性抽取结果，44 份 committed 数据中已有 20 份以上受影响；未来 #98 会消费未经授权的检索词。
- 修订要求：返回 Phase 2，恢复 issue 固定 fallback；移除未授权 phrase 并重建 44 份 summary。若 #97 validator 的 completion-marker 约束确实要求新增 fallback，必须先回到需求/设计层取得明确合同澄清，再同步 durable spec、实现和测试，不能由 checker 自行扩大规则。

### F-003 [P2] 人类可读 dry-run 没有输出必需的 source artifacts 和 missing fields

- 证据：issue #100 要求 dry-run preview 输出待回填 task、skipped task、`source_artifacts`、`missing_fields` 和 `confidence`；`prd.md` R1/R3 要求 JSON 与人类表格表达同一命令事实。
- 实现偏差：`guru_team_trellis.py:1311` 到 `:1327` 的表格只有 status、archive dir、target/reason、confidence，完全丢失 `source_artifacts` 和 `missing_fields`。现有 `test_empty_archive_and_table_renderer` 只断言表头/扫描数量，没有验证 JSON 与表格事实对齐。
- 复现：对 minimal fixture 执行不带 `--json` 的 dry-run，输出只有 `minimal` confidence；同一次 JSON 输出中的 10 个 missing fields 和 source artifacts 均不可见。
- 影响：人工预览无法判断回填证据来源和缺失程度，削弱 `--write` 前的审核能力，未满足 CLI 的主要验收合同。
- 修订要求：返回 Phase 2，为每个 `to_write` 项稳定渲染 source artifacts 与 missing fields（列或明细行均可），并补 JSON/table parity、complete/partial/minimal 的回归测试。

## 阶段二证据与提交后审计

- `phase2-check.json` 记录的 pre-commit HEAD 为 base `920e7f9f...`，当前普通 `check-phase2-check` 在提交后出现 HEAD mismatch 属预期，不应为追平 HEAD 重录 Phase 2。
- 独立展开 `dirty_paths` 前缀后，work commit 的 73/73 changed paths 全部被 pre-commit evidence 覆盖，未发现 post-commit 非 metadata 漏项。
- `checked_artifacts` 与 `checked_specs` 的 SHA-256 当前均匹配；工作树唯一 dirty path 是调度本轮审查产生的 task-local `agent-assignment.json`，属于 Branch Review metadata。
- Phase 2 所述 3 个自修复均存在于 committed canonical/dogfood diff，并有测试；但 F-002 表明 phrase 自修复只收窄了触发条件，未满足上游固定合同。

## 文档单一事实源（Docs SSOT）

- 规划选择 `ssot_first`，durable docs、canonical workflow/README、preset README 与 dogfood workflow 均已更新，canonical/dogfood Python、wrapper 和 workflow byte-equal，overlay drift 为零。
- CLI、preset managed asset、一次性迁移边界和 surface 聚合的主线文档承接完整。
- F-002 是 Docs SSOT 阻断：durable spec 追加了未被 approved planning artifacts 或 GitHub 澄清授权的 phrase 例外，形成“实现先改变合同、文档再追认”的漂移。

## 验证结果

- Canonical unittest：320 passed。
- Preset unittest：36 passed。
- Python compile、全部 canonical/preset bash `bash -n`、task context validate、`git diff --check`：通过。
- 45/45 summary 通过 canonical Python validator 和 Draft 2020-12 JSON Schema；#97 正常 summary 未被修改。
- 44/44 backfill summary 可由当前 builder 确定性重建（忽略生成时间）；44/44 surface path 与 `git.changed_paths` 守恒；写后 dry-run 为 45 scanned、45 skipped、0 errors。
- 44 份 backfill 未出现 `/Users/`、`.trellis/workspace/`、`.trellis/.runtime/`、旧式顶层 `summary`/`keywords`。
- Throwaway：以可达 `gh:castbox/guru-trellis/trellis#main` 为 marketplace 样本时，fresh init、当前 canonical preset apply、installed wrapper dry-run、workflow preview/switch、`trellis update --force`、workflow 重选、preset reapply、sidecar gate 全部通过。
- 默认 `#v0.6.5-guru.3` 当前不可达，远端 `feat/100-backfill-finish-summary` 也不存在；因此当前分支 remote marketplace 尚未验证，必须保持 pending。

## Issue、提交与发布语义

- Work commit subject `feat(workflow): #100 回填历史任务完成摘要` 符合 Conventional Commits；正文包含背景、变更、边界、验证和 `Refs #100`，没有 close keyword。
- Ledger 的 close scope 仅包含 #100；#53、#96、#97、#99 为 related，#98 为 follow-up，未发现错误关闭语义。
- `remote_marketplace_verification` 在 primary/close #100 中均为 `required=true,status=pending`；pending 不满足 publish。修复并重新通过 Branch Review 后，必须先 push reviewed content HEAD，再用真实 remote branch ref 生成 passed artifact 并只按既有 metadata-tail 合同回写。
- 未来 metadata commit 应使用 `chore(trellis): #100 固化任务收尾元数据` 空正文；merge commit 应使用已规划的 `chore(merge): #100 ...` 语义。当前 finding 未清零前不得进入这些步骤。

## 部署与安全影响

- 文档：需要修改且已修改 workflow、两份 README 与 `.trellis/spec/**`；F-002 使文档同步语义仍不合格。
- CI/CD：完整 diff 不含 `.github/workflows/**`、GitLab/Jenkins/Buildkite/CircleCI 资产；本任务不改变 CI 执行方式，无需修改。
- 容器与 Docker Compose：diff 不含 Dockerfile、Compose、entrypoint 或容器配置；CLI 是 repo-local companion，无镜像运行合同变化，无需修改。
- Kubernetes/Kustomize/Helm：diff 不含 K8s、Kustomize、Helm 或 values 资产；无部署拓扑变化，无需修改。
- 数据库 migration：本任务的 backfill 只写 task-local JSON，不连接数据库、不改 schema/seed/migration；无需数据库迁移。名称中的 backfill 不是数据库 migration。
- Makefile：diff 不含 Makefile，也没有新增必须由 Make target 暴露的构建入口；无需修改。
- 安全：白名单读取、protected path 过滤、错误去敏和 44 份数据扫描通过；无 GitHub/mem/workspace/runtime 读取证据。F-001 仍扩大了显式写目标，因此副作用边界未通过最终安全审查。

## 非阻断观察

1. Phase 2 的 source issue fallback 与异常绝对路径去敏修复正确进入 canonical/dogfood，并有有效回归。
2. 44 份当前仓库 backfill 数据在现有算法下完全可重建且 schema-valid；修复 F-002 后需要整体重建而非手改个别文件。
3. `#main` 样本证明 preset install/update/reapply 的本地可恢复性；它不能替代 push 后对当前 branch ref 的 remote marketplace gate。
4. Commit message、issue close/ref/follow-up 划分和未来 metadata/merge commit 计划本身未发现问题。

## 后续候选

- 无。三个问题都属于 #100 当前 scope，不能降级为 follow-up。

## 最终结论

存在 3 个 P2 finding。按照 Guru Team Branch Review Gate“P0/P1/P2/P3 全部阻断”的合同，本轮审查失败，HEAD `4398046075ac0432a11e1d4687c39488723d2df0` 不予最终放行。应返回 Phase 2 修复、补测、重建受影响的 44 份 summary，并由新的最终放行审查覆盖新的完整 diff。
