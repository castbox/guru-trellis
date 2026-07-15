# #128 分支问题发现审查报告

## 审查身份

- 逻辑角色：问题发现审查代理
- 技术代理 ID：`/root/branch_review_findings_issue128`
- 审查来源：独立 Branch Review
- 审查 HEAD：`80367449554307768290af555155612358a3cf40`
- 审查范围：`origin/main...80367449554307768290af555155612358a3cf40`
- 基线 HEAD：`291b57b6c02872320a4dce0626a2f718399b8f56`
- 审查结论：阻塞，发现 2 项未解决问题（P1 1 项、P2 1 项）

## 审查范围

本轮按完整提交范围审查了 38 个变更文件，覆盖：

- `planning-approval.json` 中 schema 1.2、三份规划文档摘要、固定词表歧义扫描与 `explicit-post-planning-review` 用户确认；
- 实现代理、Phase 2 检查代理的 assigned、状态请求/响应、工具活动与 completed liveness 证据；
- `phase2-check.json`、3 项已标记 resolved 的 Phase 2 P2 finding，以及 task work commit 的 tree/blob/mode 结果；
- 已审批 `ssot_first` Docs SSOT Plan、`.trellis/spec/preset/**`、根 README、preset README、workflow README；
- 43 条 ownership inventory、strict schema、source-only validator、Bash 入口、8 个结构化 fixture 与测试；
- installer pre-mutation 顺序、dogfood checkpoint、throwaway initial/update/reapply checkpoint、`.new`/`.bak` 结果；
- `origin/main...HEAD` 下两个 workflow、43 个 overlay payload、`guru-sync-base`、`guru-create-task-commit` 与 platform discovery 非回归面；
- issue scope、安全、部署与 publish 前验证限制。

## Docs SSOT 判断

- 规划策略为 `ssot_first`，durable ownership SSOT 已先写入 `.trellis/spec/preset/upstream-ownership.md`，并与 preset index、installer/overlay spec 及三份公共 README 同步。
- clean-init 调研、规划审批和代理 liveness 保留在 task-local artifact，未混入公共 package state；durable docs 与 task-history-only 边界正确。
- 文档明确要求 active payload 永久匹配冻结基线、removed entry 保留原始 `baseline_sha256` 审计历史。当前 validator 在首条 removal 后不能执行该合同，详见 P1。
- 因此 Docs SSOT 本身完整且一致，但代码未完全承接当前范围 SSOT；本轮判定为“尚未完成 reconciliation”，必须回到实现与 Phase 2 复核，审查代理不执行首次修复。

## 问题汇总

| 严重度 | 数量 | 状态 |
| --- | ---: | --- |
| P0 | 0 | 无 |
| P1 | 1 | 未解决 |
| P2 | 1 | 未解决 |
| P3 | 0 | 无 |

## 发现详情

### P1：首条 removal 后冻结 payload 与历史 hash 可被同步改写并通过门禁

- 路径：`trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py:566`
- 关联路径：`trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py:577`
- 影响合同：issue #128 no-new-patch gate、PRD R2/R3/AC2、durable spec 的 Frozen Baseline 与 Removal Migration。
- 问题：单文件校验把 inventory 中可编辑的 `baseline_sha256` 当作 expected value；全量固定 aggregate 仅在 `not removed_paths` 时比较。一旦任意 entry 合法转成 `upstream_owned/removed`，第 577 行就永久跳过固定 aggregate。此后维护者可同时修改另一个 active overlay 和该 entry 的 `baseline_sha256`，validator 会返回成功；removed entry 自身的历史 `baseline_sha256` 也没有独立的 immutable identity 可供校验。
- 独立复现：在临时最小 source 中删除第一个 overlay，并把对应 entry 改为 `upstream_owned/removed`；随后给第二个 active overlay 追加字节并把 inventory hash 同步改成新值。`validate_repository()` 返回 `status=ok`、`active_count=42`、`removed_count=1`、`errors=[]`。
- 风险：#132 开始第一条 physical removal 后，当前 #128 建立的核心“剩余 active payload 不得漂移”和“removed tombstone 不得改写历史”门禁即失效。绿色 dogfood/throwaway 只覆盖 43 条全 active 基线，无法发现该状态迁移缺陷。
- 修订要求：为全部 43 条 path/hash 建立不随 `migration_state` 或 inventory 同步编辑而变化的 immutable identity，并始终校验每条 inventory `baseline_sha256`；active 文件再与该 immutable hash 比较。增加至少两个负向回归：`首次 removal + active payload/inventory hash 同步漂移`、`removed entry baseline_sha256 改写`，两者都必须返回稳定非零错误。

### P2：strict schema 的错误类型输入会 traceback，破坏稳定 JSON 错误合同

- 路径：`trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py:393`
- 关联路径：`trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py:688`
- 影响合同：设计第 6 节 schema/type 校验、失败输出固定 `code/path/detail`、Bash `--json` maintainer entry。
- 问题：validator 只调用 `validate_schema_contract()` 检查 schema 文件结构，没有先把 inventory 实例按 schema/type 合同安全归一；随后直接对未验证成员执行 `set()` 或 `sorted()`。例如把 `ownership_categories[0]` 改为 object 会在第 393 行触发 `TypeError: unhashable type: 'dict'`；把 extension manifest 的 `active_skill_ids` 加入 integer 会在第 688 行触发字符串/整数排序 `TypeError`。
- 风险：preset apply 仍会在 target mutation 前异常终止，因此未发现写入绕过；但 `check-upstream-ownership.sh --json` 不再返回声明的结构化 facts/error payload，自动化无法按稳定错误码定位 schema/type drift，且 traceback 取代维护者合同。
- 修订要求：在所有集合、排序和映射操作前完成元素类型校验，或使用仓库可保证存在的 Draft 2020-12 实例校验机制并把失败转换为固定 `code/path/detail`。增加 malformed inventory 与 malformed manifest fixture，断言 CLI 非零且 stdout 是可解析 JSON，不得出现 traceback。

## 命令证据

- `git rev-parse HEAD`：`80367449554307768290af555155612358a3cf40`。
- `git rev-parse origin/main` 与 merge-base：均为 `291b57b6c02872320a4dce0626a2f718399b8f56`。
- `git diff --name-status origin/main...HEAD`：38 个 committed path；`git diff --check origin/main...HEAD` 通过。
- workflow/overlay/public Skill 定向 `git diff --quiet`：两个 workflow、43 个 overlay、`guru-sync-base`、`guru-create-task-commit` 均返回 0；overlay path count 为 43。
- `python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`：6 tests passed。
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：39 tests passed。
- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：292 tests passed。
- `python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'`：67 tests passed。
- Draft 2020-12 schema check 与当前 inventory instance check：通过。
- `check-upstream-ownership.sh --repo . --json`：当前全 active 基线通过，frozen/active/overlay=`43/43/43`，clean-init=`37/6`，errors 为空。
- `check-dogfood-overlay-drift.sh --repo .`：通过，canonical 与 dogfood payload 一致。
- `verify-throwaway-install.sh`：通过 initial apply、`trellis update --force`、workflow/preset reapply、三次 ownership checkpoint、finish fixture 与最终 drift；零 `.new`/`.bak` sidecar。
- `bash -n`、Python compile、task context validate：通过，`implement.jsonl` 与 `check.jsonl` 各 6 条。
- 临时 removal-transition probe：错误返回 `status=ok, active_count=42, removed_count=1, errors=[]`，确认 P1。
- 临时 malformed-input probe：分别复现 `TypeError: unhashable type: 'dict'` 与 `TypeError: '<' not supported between instances of 'int' and 'str'`，确认 P2。

## 非回归、部署与安全判断

- 非回归：两个 workflow 文件无 diff；43 个 overlay path/payload 无 diff；既有 `guru-sync-base`、`guru-create-task-commit` package/interface/discovery 无 diff；未新增 mandatory Skill routing；validator 字样未进入 workflow、现有 Skill 正向行为或 platform runtime entry。
- 更新/升级：throwaway 已证明本地 source gate 在 initial apply、upstream `trellis update --force` 后、reapply 后执行，现有 target conflict 处理与 `.new`/`.bak` 检查未回归。P1 仅在后续出现首条 removed state 后暴露，但属于 #128 当前承诺的迁移状态合同，不应推迟到 #132 才修。
- 部署：变更是 source maintainer/preset install gate；validator/schema/inventory 未被安装为业务运行时资产。未变更容器、Kubernetes、数据库 migration、CI/CD、Makefile 或业务配置；没有运行时部署步骤。
- 安全：提交 diff 未发现 token、private key、`.env`、签名 URL、客户数据或本机绝对路径；validator 仅读取 source repository facts，pre-mutation ordering 已由代码和测试确认。P2 的 traceback 会降低错误输出可控性，但未发现 secret 泄露或 target mutation。

## Issue 范围判断

- `close_issues`：仅 #128，ledger 正确；由于本轮存在阻塞 finding，当前不得关闭。
- `related_issues`：#127、#112、#119，均保持关联且 live 状态为 OPEN。
- `followup_issues`：#129、#130、#131、#132，均保持后续范围且 live 状态为 OPEN。
- 未发现把 related/follow-up issue 错写为 close keyword 的提交内容；work commit 使用 `Refs #128`。

## 观察项

- 当前标准测试、dogfood 与 throwaway 均为绿色，但只验证 43 条 entry 全部 active 的初始状态；这解释了 P1 未被现有 6 个测试捕获。
- `phase2-check.json` 的三项 P2 修复与 committed blob 一致，规划文档、实现 handoff、Phase 2 checked artifact 摘要可追溯；本轮 finding 是独立 post-commit 状态迁移审查的新发现。
- 当前 tracked working tree 的 post-commit tail 仅包含 `agent-assignment.json`、`task-commit-plans/001.json` 和本原始 review report，均为 task/review metadata；未发现 implementation 或 durable docs 的未提交改动。
- exact remote branch marketplace 尚未验证；commit、Phase 2 与 README 均明确约定在 publish/push 后补证。这是当前无远端 branch 时的已披露限制，不单独列为 finding。

## 后续候选

- 两项 finding 都属于 #128 当前 ownership validator 合同，应在当前 task 内修复、补负向回归，并重新执行 Phase 2 与 task work commit；不建议新建 follow-up issue 或转交 #132。
- finding 修复后，后续独立 Branch Review 应重新覆盖新的 `origin/main...HEAD` 完整范围，而不是只看 finding-fix commit。
- publish 阶段继续补 exact remote branch marketplace evidence，不改变 issue close ledger。

## 结论

本轮原始问题发现审查已完整完成。尽管当前全 active 基线、installer、dogfood、throwaway 及严格非回归面均通过，validator 在合法 removal 状态出现后会失去对核心冻结身份的约束，且 malformed strict-schema 输入不能稳定返回 JSON 错误。P1/P2 共 2 项均未解决，Branch Review Gate 必须阻塞并返回实现修订。
