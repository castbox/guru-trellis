# 第 3 轮最终放行审查原始报告

## 审查身份

- 角色：最终放行审查代理
- 代理标识：`/root/branch_review_100_release_round3`
- 复用决策：`new-agent`
- 基线：`origin/main`（`920e7f9f797efb6356286f638efc1995ffe4075d`）
- 差异范围：`origin/main...ec5ac3e0f7752286ca5b17428b713711c1a07758`
- 审查 HEAD：`ec5ac3e0f7752286ca5b17428b713711c1a07758`
- 问题数量：1
- 审查结论：失败；不得记录 passed Branch Review Gate

固定记录字段：`technical_agent_id=/root/branch_review_100_release_round3`，`logical_role=最终放行审查代理`，`reuse_decision=new-agent`，`reviewed_head=ec5ac3e0f7752286ca5b17428b713711c1a07758`，`findings_count=1`。

## 审查范围

本轮由未参与前两轮的新 technical agent 独立读取并审查：

- Live issue #100 及 comments `4941094903`、`4941670415`、`4941812435`、`4942002004`。
- `prd.md`、`design.md`、`implement.md`、`implementation-handoff.md`、`planning-approval.json`、`phase2-check.json`、`issue-scope-ledger.json`、`agent-assignment.json`。
- 前两轮原始报告、失败 gate 与汇总；round 1 的 3 个 finding owner、round 2 `reuse-for-closure` 身份和闭环链均完整。
- 四份 Phase 2 checked specs、适用 spec index、workflow contract、quality guideline、public docs guideline，以及完整 `origin/main...HEAD` 73 文件 committed diff。
- Canonical/dogfood Python、wrapper、workflow，preset installer、manifest、两份 README、durable specs、334 个 canonical tests、36 个 preset tests、44 份 backfill 与 #97 normal summary。

## Findings

### F-004 [P3] Phase 2 报告记录了不可执行的 preset 测试命令

- 位置：`phase2-check.json:140`。
- 记录值为 `python3 -m unittest trellis/presets/guru-team/scripts/python/test_installer.py`，并声称结果为 `36 passed`。
- 仓库不存在 `test_installer.py`；原样执行该命令退出 1，报 `ModuleNotFoundError`，因此它不能产生所记录的结果。
- 实际测试文件是 `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`；本轮独立执行正确命令得到 36 passed，所以该问题不表示 preset 运行时代码失败，但表示 Branch Review 所依赖的 Phase 2 gate evidence 不可复现且陈述不真实。
- Guru Team 要求 gate artifact 记录真实验证命令与结果，任何 P0-P3 都阻断。应返回 Phase 2，用真实命令和对应执行证据修正/重录 `phase2-check.json`；本报告不得直接补写该证据。

## 首轮问题生命周期复核

- F-001 已闭环：explicit `--task` 与 discovery 共用 direct marker + ancestor 判定；archive root、月份分组、task 子目录、`research/`、`reviews/` 和 symlink escape 均在扫描/写入前拒绝，不依赖 basename 特判。
- F-002 已闭环：problem/outcome 固定 fallback 为 6/6；completion fallback 仅在缺少 #97 marker 时出现，恰好覆盖 8 个历史 task；title/problem 与 pr-body-only outcome/behavior 两个例外都要求 backfill generator、确定性 helper 文本和窄来源条件，normal finish-work、非精确 fallback、来源漂移及其它重复继续失败。
- F-003 已闭环：人类表格每个 `to_write` 行显示 `source_artifacts`、`missing_fields`、`confidence`，complete/partial/minimal 与 JSON payload 同源。
- Round 2 的 `technical_agent_id=/root/branch_review_100_final`、`logical_role=问题闭环审查代理`、`reuse_decision=reuse-for-closure`、`findings_count=0` 与 round 1 finding owner 一致，closure 链有效；本轮 agent id 未出现在 earlier `review_rounds[]`。

## 实现与数据证据

- Canonical unittest：334 passed；preset 正确测试命令：36 passed。
- Python compile、canonical/preset Bash `bash -n`、task validate、`git diff --check`、manifest JSON、dogfood overlay drift 与 sidecar 扫描：通过。
- Canonical/dogfood Python、wrapper、workflow byte-equal；wrapper 均为 executable。
- 45/45 Python validator 与 Draft 2020-12 schema 通过；44/44 backfill 可由当前 builder 去时间字段确定性重建；44/44 surface paths 与 `git.changed_paths`、`search_terms.paths` 守恒。
- 写后 dry-run 为 45 scanned、45 skipped、0 errors；四个真实非 task-root 目标 dry-run 均退出 2。
- 44 个 backfill 的 problem/outcome fallback 为 6/6、completion fallback 为 8、pr-body-only outcome 为 13；44 份均无 workspace/runtime/绝对本机路径和旧式顶层字段。
- #97 normal summary SHA-256 为 `f18370b72df53c720f33e170b2113a6a7958311913f787a4c64279e7d025fd80`，与 `origin/main` 字节一致。
- 两个 work commit 均通过 `check-commit-messages`，使用中文 Conventional Commits、固定正文段和 `Refs #100`，无 close keyword。

## Phase 2 提交后审计

- Phase 2 记录 HEAD 为 `4398046075ac0432a11e1d4687c39488723d2df0`；修复提交 `4398046...ec5ac3e` 的 50/50 changed paths 均被已记录 `dirty_paths` 覆盖。
- `checked_artifacts` 5/5、`checked_specs` 4/4 当前 SHA-256 与记录值一致；planning approval 仍通过。
- 当前未提交路径全部位于本 task 的 planning/check/review/assignment metadata；没有未提交源码、spec、preset、测试或历史 summary 漂移。
- 普通 `check-phase2-check` 因提交后 HEAD 和 review metadata 变化报告 mismatch 属既有 post-commit 场景；F-004 与该预期 mismatch 无关，它是报告内部命令/结果不一致。

## 文档单一事实源

- Docs SSOT 策略为 `ssot_first`。Task-root/preview 合同已进入 `companion-scripts.md`；fallback/phrases、两个窄 retrieval 例外、commits 优先级、confidence 与 surface 守恒已进入 `data-contracts.md`。
- Canonical workflow、workflow README、preset README、installer managed asset 与 extension manifest 对一次性 backfill 入口的描述一致；dogfood 同步无漂移。
- 未发现实现先行后文档追认、task artifact 替代 durable SSOT 或 README/workflow 冲突。F-004 是 gate evidence 记录错误，不是 Docs SSOT 合同漂移。

## 开箱即用与升级验证

- 使用可达公开样本 `gh:castbox/guru-trellis/trellis#main` 完成 fresh init、当前本地 canonical preset apply、installed wrapper empty-archive dry-run、workflow preview/switch、`trellis update --force`、workflow 重选、preset reapply 与最终 sidecar 检查，全部通过。
- 上述验证证明本地当前 preset 能安装并在 update 后恢复 backfill 资产，但不等于当前未 push branch 的 remote marketplace verification。Ledger 保持 `required=true,status=pending` 正确；发布仍须 push reviewed content HEAD 后执行真实 branch ref verifier。

## Issue、部署与安全影响

- Ledger 仅关闭 #100；#53/#96/#97/#99 为 related，#98 为 follow-up，close/ref/follow-up 语义正确。
- 文档：已同步 workflow、README 与 durable specs；无额外缺口。
- CI/CD、Docker/Compose、Kubernetes/Kustomize/Helm、数据库 migration、Makefile：完整 diff 不含对应资产，也未引入对应运行合同变化，无需修改。
- 安全：固定 task-local 白名单、repo-relative task-root、symlink/protected path 处理、错误去敏和敏感路径扫描通过；未发现 backfill 读取 GitHub、`trellis mem`、workspace/runtime 或泄露 secret/绝对路径。

## 观察项

1. 44 份真实历史 backfill 均为 `partial`；pure `minimal` 和 `complete` 分支由临时 fixture 覆盖。
2. 当前分支 remote marketplace verification 尚未执行且必须保持 pending；这是发布门禁，不是本轮 finding。

## 后续候选

- 无。F-004 属于 #100 当前 release evidence，不能降级为 follow-up。

## 最终结论

本轮 `findings_count=1`。虽然实现、数据、Docs SSOT、安装升级和前两轮 finding closure 均通过独立复核，但 Phase 2 报告包含不可执行却声明通过的验证命令。按照 P0/P1/P2/P3 全部阻断的 Branch Review Gate 合同，HEAD `ec5ac3e0f7752286ca5b17428b713711c1a07758` 本轮不予最终放行。
