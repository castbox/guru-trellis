# #128 分支问题闭环审查报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- 技术代理 ID：`/root/branch_review_findings_issue128`
- 复用决定：`reuse-for-closure`
- 审查来源：独立 Branch Review 问题闭环复核
- 审查 HEAD：`78006a7b643708bf6ecaa7d9f5a1b8ab8a935eb5`
- 审查范围：`origin/main...78006a7b643708bf6ecaa7d9f5a1b8ab8a935eb5`
- 基线 HEAD：`291b57b6c02872320a4dce0626a2f718399b8f56`
- 审查结论：问题闭环通过；本轮 findings_count 为 0

本代理是 round 001 finding owner 的同一技术代理，按 workflow 仅复核既有 finding 的关闭状态以及修复是否引入新的 P0/P1/P2/P3 问题。依据角色隔离规则，本代理不得承担后续最终放行审查。

## 审查范围

本轮重新覆盖 `origin/main...HEAD` 的 46 个 committed path，而非只审查 finding-fix commit。审查内容包括：

- round 001 的 `BR-001`、`BR-002` 原始复现、修订要求及问题生命周期；
- finding-fix commit `78006a7b643708bf6ecaa7d9f5a1b8ab8a935eb5` 的 14 个变更文件；
- 43 条冻结 path/hash identity、active payload、removed tombstone 与 materialized identity 的一致性；
- malformed inventory、extension manifest、Skill registry 的类型归一、错误结构、CLI exit code、stdout/stderr 合同；
- `ssot_first` Docs SSOT、规划 artifact、fresh Phase 2、task commit plan 与 committed tree/blob/mode 绑定；
- ownership、installer、workflow、Skill package、dogfood、throwaway、upgrade/update 与严格非回归面；
- issue scope、部署影响、安全边界及 publish 前仍需完成的远端证据。

## 问题生命周期

### BR-001：已关闭

- 原严重度：P1。
- 原问题：首条 `upstream_owned/removed` 后，active payload、inventory hash 或 removed 历史 hash 可被同步改写并绕过冻结基线门禁。
- 修复承接：validator 新增固定 `FROZEN_LEGACY_IDENTITY_SHA256=0ca84016a32cd496c4a9ff2a6bdc6637a1e6393abd3d60f3bf3388657ebf8350`，分别校验 inventory projection 与 active/removed materialized projection，不再因存在 removed entry 跳过身份约束。
- 独立复核：从 base commit 的 43 个 overlay blob 重算 path/hash identity，mismatch 数量为 0，identity 与 inventory 及 validator 常量一致。
- 负向复核：首条 removal 后同步修改 active payload 与 inventory hash，稳定返回 `frozen_legacy_identity_mismatch` 和 `materialized_frozen_identity_mismatch`；改写 removed 历史 `baseline_sha256` 返回相同错误类别，均未通过门禁。
- 生命周期结论：修订要求已由代码、冻结 identity、结构化 fixture 与独立负向 probe 完整承接，`BR-001` 关闭。

### BR-002：已关闭

- 原严重度：P2。
- 原问题：malformed inventory/manifest 成员会在 `set()` / `sorted()` 触发 `TypeError` traceback，破坏稳定 JSON 错误合同。
- 修复承接：在集合、排序、mapping lookup 前完成成员类型归一；validator 顶层异常也转换为稳定结构化错误，不再向 CLI 泄漏 traceback。
- 独立复核：malformed inventory、extension manifest、Skill registry 三类输入均以 exit code 1 失败；stdout 均为可解析 JSON，每个 `errors[]` 元素只包含 `code`、`path`、`detail`，stderr 不含 traceback。
- 生命周期结论：原始 inventory/manifest 缺口及 fresh Phase 2 同范围发现的 registry 缺口均已关闭，`BR-002` 关闭。

## Findings

| 严重度 | 数量 | 状态 |
| --- | ---: | --- |
| P0 | 0 | 无 |
| P1 | 0 | 无 |
| P2 | 0 | 无 |
| P3 | 0 | 无 |

本轮未发现新的当前范围 P0/P1/P2/P3 问题，`findings_count=0`。

## 验证证据

- `git rev-parse HEAD`：`78006a7b643708bf6ecaa7d9f5a1b8ab8a935eb5`；merge-base 为 `291b57b6c02872320a4dce0626a2f718399b8f56`。
- `git diff --name-only origin/main...HEAD`：46 个 committed path；`git diff --check origin/main...HEAD` 通过。
- `python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`：6 个 test method、14 个结构化 fixture 全部通过。
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：39 tests passed。
- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：292 tests passed。
- `python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'`：67 tests passed。
- Draft 2020-12 schema、`bash -n`、Python compile、JSON parse、task context 与 `git diff --check` 均通过。
- ownership gate：frozen/active/removed=`43/43/0`，clean-init=`37/6`；inventory/materialized identity 均为 `0ca84016a32cd496c4a9ff2a6bdc6637a1e6393abd3d60f3bf3388657ebf8350`。
- `check-dogfood-overlay-drift.sh` 通过，canonical 与 dogfood overlay payload 零漂移。
- 完整 throwaway 验证通过 initial apply、`trellis update --force`、workflow/preset reapply、三次 ownership checkpoint、finish fixtures，且无 `.new` / `.bak` sidecar。
- 两个 workflow、43 个 overlay path/payload、`guru-sync-base`、`guru-create-task-commit` canonical/interface/discovery 均保持零 diff；未新增 mandatory routing。

## Phase 2 与提交证据

- fresh `phase2-check.json` 已覆盖 round 001 findings、完整基线 diff 与当前 finding-fix dirty delta，并记录 `BR-001`、`BR-002` 及同范围 malformed registry 缺口均为 resolved。
- `phase2-check.json.head` 为父提交 `80367449554307768290af555155612358a3cf40`，原因是 Phase 2 在修复尚未提交时审查其完整 dirty diff；这符合 pre-commit evidence 模型。
- `task-commit-plans/002.json` 随后精确绑定该 Phase 2 dirty snapshot 并提交为当前 HEAD，tree/blob/mode 全部匹配，`unrelated_preserved=true`、`hook_mutation=false`。因此 Phase 2 证据没有因 commit 后 HEAD 变化而 stale。
- 当前 working tree 的未提交内容仅为 task/review metadata；未发现实现、durable docs、schema、脚本或测试的未提交漂移。

## Docs SSOT 判断

- 批准策略仍为 `ssot_first`；`.trellis/spec/preset/upstream-ownership.md` 是 durable ownership SSOT，已补充冻结 legacy identity 与 removal 后双 projection 校验合同。
- inventory、schema、validator、fixture/test 与 durable spec 对 active payload、removed tombstone、稳定 JSON 错误结构的定义一致。
- clean-init 调研、review lifecycle、Phase 2 与 commit evidence 保留在 task-local artifact，没有混入公共 marketplace package state。
- round 001 的“代码未完全承接 Docs SSOT”缺口已消除；本轮 Docs SSOT reconciliation 通过。

## 开箱即用与 Upgrade/Update 判断

- dogfood gate 与完整 throwaway install 均通过，已覆盖 initial install、upstream `trellis update --force`、workflow/preset reapply 和三次 ownership checkpoint。
- 43 个 canonical overlay 与 dogfood 安装副本保持一致，零 `.new` / `.bak`，现有 conflict/sidecar 处理未回归。
- ownership source gate 在 target mutation 前运行；malformed source 输入会 fail closed，并保持机器可消费的 JSON 错误合同。
- 两个 workflow、平台入口与既有公共 Skill package 未发生行为漂移，未发现依赖上游源码、全局 npm、`node_modules` 或一次性 installed-file patch 的实现。

## 部署与安全判断

- 本次改动属于 source maintainer/preset install gate，不安装为业务运行时资产；无需容器、Kubernetes/Kustomize、数据库 migration、CI/CD、Makefile 或业务配置变更，也没有运行时部署步骤。
- 完整 diff 未发现 token、private key、`.env`、数据库 URL、签名 URL、客户数据或本机绝对路径。
- validator 仅读取 source repository facts；malformed 输入以受控 JSON 失败，未发现 target mutation、secret 泄露或错误栈外泄。

## Issue Scope 判断

- `close_issues`：仅 #128；本轮 closure pass 只表示既有 findings 已关闭，不替代后续最终放行与 publish readiness。
- `related_issues`：#127、#112、#119，live 状态均为 OPEN，本 PR 不关闭。
- `followup_issues`：#129、#130、#131、#132，live 状态均为 OPEN，本 PR 不关闭。
- 未发现把 related/follow-up issue 写成 close keyword，scope ledger 仍与 issue #128 的当前交付边界一致。

## 观察项

- exact remote branch marketplace 验证必须在 branch push/publish 后针对精确远端 ref 补证；当前本地 closure review 无法生成该远端证据。这是已声明的 publish 阶段门禁，不构成本轮 finding，也不得在最终放行或 PR readiness 中省略。

## 后续候选

无。本轮未发现需要拆分的新范围，也未把 #128 当前缺陷转移到 #129-#132。

## 结论

round 001 的 `BR-001`、`BR-002` 已由当前 HEAD 完整关闭，完整 `origin/main...HEAD` 复核未发现新的 P0/P1/P2/P3 问题。本轮问题闭环审查判定为 closure pass，`raw_report_complete=true`。

本报告不是最终放行结论。下一步必须由技术代理 ID 未出现在任何早期 review round 的全新“最终放行审查代理”，针对当前完整 HEAD diff 独立审查；本问题闭环审查代理不得承担该角色。
