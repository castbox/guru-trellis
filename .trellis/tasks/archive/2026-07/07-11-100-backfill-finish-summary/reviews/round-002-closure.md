# 第 2 轮问题闭环审查原始报告

## 审查身份

- 角色：问题闭环审查代理
- 代理标识：`/root/branch_review_100_final`
- 复用决策：`reuse-for-closure`
- 复用边界：仅复核本人第 1 轮提出的 finding 及其修复，不承担最终放行角色
- 基线：`origin/main`（`920e7f9f797efb6356286f638efc1995ffe4075d`）
- 差异范围：`origin/main...HEAD`
- 审查 HEAD：`ec5ac3e0f7752286ca5b17428b713711c1a07758`
- 问题数量：0
- 审查结论：首轮问题已闭环；本结论不是最终 release 放行

## 闭环记录字段

- 技术代理：`technical_agent_id=/root/branch_review_100_final`
- 审查角色：`logical_role=问题闭环审查代理`
- 复用决策：`reuse_decision=reuse-for-closure`
- 审查提交：`reviewed_head=ec5ac3e0f7752286ca5b17428b713711c1a07758`
- 问题计数：`findings_count=0`

## 审查范围与证据

本轮重新读取并独立复核了：

- 第 1 轮原始报告 `reviews/round-001-final.md`、汇总 `review.md` 和失败 `review-gate.json`。
- Live issue #100 全文及 comments `4941094903`、`4941670415`、`4941812435`、`4942002004`。
- 最新 `prd.md`、`design.md`、`implement.md`、`implementation-handoff.md`、`planning-approval.json`、`phase2-check.json`、`issue-scope-ledger.json`、`agent-assignment.json`。
- `origin/main...ec5ac3e0f7752286ca5b17428b713711c1a07758` 完整 committed diff，以及修复提交 `4398046...ec5ac3e` 的 50 文件 patch。
- Canonical/dogfood Python、wrapper、334 个 canonical tests、36 个 preset tests、durable specs、workflow/README、extension manifest、preset installer 和 throwaway verifier。
- 最终 44 份 backfill summary 与 #97 normal finish-work summary。

## 首轮问题生命周期

### F-001 [P2] 已解决：显式 `--task` 的 task-root 边界

- Canonical `resolve_finish_summary_backfill_task()` 现在要求目标含直接白名单 marker 或既有 `finish-summary.json`，并逐级拒绝 archive root 到目标之间已存在 task-root marker 的子目录。
- Discovery 与 explicit resolver 共用 `finish_summary_backfill_task_root_marker()`；discovery 命中 task root 后停止向后代扫描，不依赖 `research`/`reviews` basename 特判。
- 独立复现确认月份分组目录、现有 `research/` 和 `reviews/` 均在 dry-run 扫描前退出 2；Phase 2 的 18 组非法路径在 dry-run/write/force 三种模式共 54 个组合均退出 2。
- 测试覆盖真实 task root、分组目录、task 子目录、symlink escape、绝对/parent/active/repo 外路径和三种执行模式。

### F-002 [P2] 已解决：固定 fallback、phrases 与 retrieval 边界

- `index.problem` 和 `index.outcome` 已逐字恢复为 issue #100 固定 fallback：`<task.title>；旧行为：历史 artifact 未记录。` 与 `<task.title>；非目标：历史 artifact 未记录。`。
- Comment `4941670415` 已明确授权：phrases 先按 #100 顺序生成、去重、补足，仅在仍缺 #97 completion marker 时追加唯一 `历史归档 task 已完成`；当前 8 个历史 task 触发该分支。
- Comment `4941812435` 已明确授权严格 backfill-only title/problem 边界例外。实现要求 generator、exact fallback、helper-derived retrieval 和单一边界同时成立；normal finish-work、非精确 fallback 和其它相邻重复继续失败。
- Exact fallback phrase 的 clause-edge skip 只在已批准的固定来源去重阶段作用于 exact 候选，不改写其它 phrase；它避免在 phrases 尾部制造第二个未获授权的 title/problem 重复。problem/outcome 主字段仍完整进入 helper-derived retrieval，未丢失检索事实。
- Comment `4942002004` 授权的 pr-body-only outcome/behavior 边界例外也被限制为 task-local 来源可重验、无高优先级 outcome/paragraph、outcome 等于第一列表项、完整列表等于 `changed_behavior`、retrieval 未篡改且无其它重复。Normal finish-work 和来源漂移继续失败。
- 44 份 backfill 已由最终 builder 全量重建；#97 normal summary 未被覆盖，SHA-256 保持 `f18370b72df53c720f33e170b2113a6a7958311913f787a4c64279e7d025fd80`。

### F-003 [P2] 已解决：人类 preview 字段一致性

- 默认表格表头和每个 `to_write` 行已包含 `SOURCE_ARTIFACTS`、`MISSING_FIELDS`、`CONFIDENCE`。
- Complete、partial、minimal fixture 的回归逐行从 JSON payload 重建预期表格行并断言存在，避免只检查表头的自证测试。
- Skipped 行保持字段占位，JSON 与表格继续共享同一 payload 决策和退出码。

## 第二轮阶段二自修复复核

- Pr-body-only outcome/behavior：第一列表项成为 outcome，完整列表保留为 behavior；两处严格 backfill-only 重复例外可共存，负向来源和篡改测试充分。
- Commits 优先级：实现按 `task.json.commit`、`review-gate.json.head`、`pr-readiness.json.commits[]` 取首个非空有效来源，不再 union 低优先级来源；非法高优先级值 fail closed。
- Complete branch：`complete` 明确要求非空 `git.branch`；缺 branch fixture 降为 partial。
- Minimal semantic-source：artifact/base/branch/commit、issue/PR、review outcome、完成 checklist、contract table 等任一非标题证据都会至少成为 partial；纯空字段 marker 仍可生成 minimal。
- 上述四项没有重新打开 F-001/F-002/F-003，也没有修改 #97 schema、通用 retrieval helper 或 normal finish-work builder。

## 文档单一事实源（Docs SSOT）

- 策略保持 `ssot_first`。`companion-scripts.md` 固化 task-root marker/ancestor、preview parity；`data-contracts.md` 固化 commits、fallback/phrases、两类窄 retrieval 例外和 confidence 规则。
- Canonical 与 dogfood Python byte-equal，canonical/dogfood workflow byte-equal，overlay drift 为零且无 `.new`/`.bak` sidecar。
- Canonical workflow/README 与 preset README 保持高层一次性迁移边界，durable specs 承载可复用的详细编码合同；未发现相互冲突。
- Planning approval 和 Phase 2 checked artifacts/specs 的 SHA-256 当前匹配，未发现实现后反向改写未批准合同。

## 阶段二提交后审计

- 最新 `phase2-check.json` 记录 pre-commit HEAD `4398046075ac0432a11e1d4687c39488723d2df0`，当前 HEAD 为其后修复提交 `ec5ac3e...`；普通 HEAD mismatch 属预期。
- 独立展开 `dirty_paths` 后，修复提交的 50/50 changed paths 全部被 Phase 2 pre-commit evidence 覆盖，无非 metadata 漏项。
- 当前 working tree 的变更仅为 task-local planning/check/review/assignment metadata；canonical、preset、spec、测试和 44 份 summary 均无未提交漂移。

## 验证结果

- Canonical unittest：334 passed。
- Preset unittest：36 passed。
- Python compile、全部 canonical/preset bash `bash -n`、task context validate、`git diff --check`：通过。
- 45/45 summary 通过 canonical Python validator 和 Draft 2020-12 JSON Schema。
- 44/44 backfill 可由最终 builder 确定性重建；44/44 surface paths 与 `git.changed_paths` 守恒；写后 dry-run 为 45 scanned、45 skipped、0 errors。
- 44 份 backfill 无 `/Users/`、`.trellis/workspace/`、`.trellis/.runtime/` 和旧式顶层 `summary`/`keywords`。
- 以可达 `gh:castbox/guru-trellis/trellis#main` 为 marketplace 样本的 fresh init、当前 preset apply、installed wrapper dry-run、workflow preview/switch、`trellis update --force`、workflow 重选、preset reapply 和 sidecar gate：通过。

## Issue、提交与发布语义

- 两个 work commits 均为中文 Conventional Commits，正文有固定背景/变更/边界/验证和 `Refs #100`，没有 close keyword。
- Ledger 仅关闭 #100；#53、#96、#97、#99 为 related，#98 为 follow-up。
- Remote marketplace evidence 仍为 `required=true,status=pending`；当前分支尚未 push，本轮闭环通过不能替代 push 后真实 branch ref 验证。
- 后续仍需新的 technical agent 作为 fresh 最终放行审查代理；本代理不得从问题闭环角色切换为最终放行角色。

## 部署与安全影响

- 文档：workflow/README/durable specs 的必要同步已覆盖，未发现新缺口。
- CI/CD：完整 diff 不含 GitHub Actions、GitLab CI、Jenkins、Buildkite 或 CircleCI 资产，无需修改。
- 容器与 Docker Compose：无 Dockerfile、Compose、entrypoint 或容器配置变更，无需修改。
- Kubernetes/Kustomize/Helm：无 Kubernetes、Kustomize、Helm 或 values 资产变更，无需修改。
- 数据库 migration：该 backfill 只写 task-local JSON，不访问数据库，不修改 schema/seed/migration；无需数据库迁移。
- Makefile：diff 不含 Makefile，也没有新增构建 target 合同，无需修改。
- 安全：task-root、symlink、protected path、错误去敏和白名单读取边界均通过；未发现 GitHub/mem/workspace/runtime 读取或敏感数据落盘。

## 非阻断观察

1. 44 份当前历史数据全部为 partial；pure minimal 分支由临时 fixture 覆盖，当前仓库没有对应历史产物。
2. `#main` throwaway 证明当前本地 preset/update/reapply 可恢复，但不等价于当前未 push branch 的 remote marketplace gate。
3. 第 2 轮 Phase 2 的 pr-body-only、commits、complete、minimal 四项自修复均有正负回归，未发现测试复制业务逻辑后自证。

## 后续候选

- 无。首轮 finding 已在当前 scope 内闭环；remote verification 和 fresh final review 是既有发布门禁，不是新增 follow-up。

## 闭环结论

第 1 轮 F-001、F-002、F-003 均已在 HEAD `ec5ac3e0f7752286ca5b17428b713711c1a07758` 闭环，本轮问题数量为 0。该结论仅证明 finding owner 的问题闭环，不是最终 release pass；必须由从未参与前两轮的新 technical agent 对当前完整 diff 执行 fresh 最终放行审查。
