# Issue #97 Branch Review Round 3 问题闭环审查

## 审查身份

| 字段 | 值 |
| --- | --- |
| `logical_role` | `问题闭环审查代理` |
| `agent_id` | `/root/issue97_closure_round2` |
| `reviewed_head` | `017b9f351bfbb90fcfca3a3935a9167de645b97c` |
| Diff 范围 | `origin/main...HEAD` |
| `round` | `3` |
| `from_round` | `2` |
| `reuse_decision` | `reuse-for-closure` |
| `findings_count` | `0` |

本轮由 round 2 finding owner 以同一技术身份返回，只验证其唯一 P2 的修复和完整分支无回归。`agent-assignment.json.reuse_decisions[]` 已记录 `from_round=2`、`to_round=3`、相同 `agent_id`、当前 HEAD、`reuse-for-closure` 与非空原因。本代理仍是 finding-owner/closure 身份，不得转任 `最终放行审查代理`。

## 审查范围

- 复读 `reviews/round-002-closure.md`、post-planning-approved `design.md` 4.4、fresh `phase2-check.json`、`implementation-handoff.md`、第三个 commit 与该 commit 的三文件 diff。
- 核对 canonical/dogfood companion 的完整 snapshot-unavailable fixed fact，与批准 design 的逐字段值完全一致。
- 核对 initial `git diff`、initial `git ls-files --others`、final/recovery `git diff` 三类失败测试是否走真实 snapshot 分支，并锁定完整对象、双空 paths、无 filtering、不披露、retrieval 重派生与 path fail closed。
- 复核完整 `origin/main...HEAD`、前三轮已确认的 round 1 五项修复、Phase 2 两个 P3、Docs SSOT、workspace 删除、canonical/dogfood equality、部署、安全和 publish 前 remaining gate 无回归。

## Round 2 P2 闭环

状态：`PASS`。

批准版 `design.md` 4.4 定义的完整对象为：

```json
{
  "contract": "finish-summary git path snapshot unavailable",
  "before": "Git 变更路径快照未成功完成。",
  "after": "完成摘要已使用空路径集合，未写入未验证路径。",
  "source_artifact": ""
}
```

canonical `FINISH_SUMMARY_PATH_SNAPSHOT_UNAVAILABLE_CONTRACT` 与该对象逐字段相等，dogfood companion 与 canonical SHA-256 相同；旧 English/替代文案定向扫描无命中。

### 三类失败路径

- initial diff failure：`build_finish_summary()` 的 `rev-list` 成功后，真实 `finish_summary_git_path_snapshot()` diff 命令返回非零；partial stdout、workspace basename、stderr 和 secret ref 不进入 summary。
- initial untracked failure：diff 成功但 `git ls-files --others --exclude-standard` 返回非零，之前得到的 safe/partial paths 被整体丢弃；错误输出不进入 summary。
- final/recovery diff failure：`update_finish_summary_for_pr()` 真实调用 snapshot helper，diff 返回非零，旧 filtering fact 被移除并替换为唯一 unavailable fact。

三类路径共用对象级 assertion，证明：

- `git.changed_paths=[]`；
- `index.search_terms.paths=[]`；
- unavailable fact 完整等于批准对象且恰好一次；
- protected filtering fact 不存在；
- partial stdout path、受保护 basename、stderr 与 ref 不出现在序列化 summary；
- `retrieval_text` 从最终 index 重新派生并全值相等；
- 人工注入 `.trellis/workspace/**` 后，`git.changed_paths` 与 `index.search_terms.paths` 两个 validator 都继续 fail closed。

因此 round 2 P2 已按修复要求完整闭环，不再存在 design/code/test 的 Docs SSOT 冲突。

## Fresh Phase 2 证据

- checker：`/root/issue97_phase2_round2`；fresh artifact 不复用旧 Phase 2 结论，覆盖 round 2 P2、完整 `origin/main...HEAD` 与第三个 commit 的三个 tracked paths。
- canonical full suite：302 tests 在 compile 前后各通过一次。
- preset full suite：36 tests 在 compile 前后各通过一次。
- `PublishBoundaryTest + FinishSummaryContractTests`：79 tests PASS。
- `python3 -S FinishSummaryContractTests`：31 PASS，1 项仅因 optional `jsonschema` 缺失而 skip。
- public-main throwaway：preview cleanup、switch、update、workflow reapply、preset reapply、no-workspace sentinel 与 final sidecar gate PASS。
- compile、Bash、260 JSON、task/planning/workspace boundary、commit message、all-platform apply、overlay drift、六组 equality、sidecar、workspace tracking、Docs SSOT、部署与 added-line secret review 均通过。

审查代理独立重跑 canonical 302、preset 36、定向 79、`python -S` 31+1，结果与 fresh Phase 2 artifact 一致。

## 完整分支回归

- 第三个 commit 只修改 canonical companion、dogfood companion和 canonical tests，提交 body 含背景、变更、边界、验证与 `Refs #97`，未使用 close keyword。
- canonical/dogfood companion SHA-256 均为 `568f28b22a9244eaa359d847e01aaa45ff876c2310165e80d4c09b648d3386c5`。
- `git diff --check origin/main...HEAD` 通过；recursive `.new/.bak` 扫描为空。
- `git ls-files '.trellis/workspace/**'` 为空；base-to-HEAD 仍保留三个预期删除记录。
- round 1 的 no-workspace context、immutable readiness/recovery、durable requirements 与 throwaway sidecar 修复，以及 Phase 2 的 workflow reapply / pycache 修复均未被第三个 commit 改动或回退。
- issue ledger 与 `pr-body.md` 的 close/ref/follow-up 语义不变；#97 是唯一 close issue。

## Findings

无 P0、P1、P2 或 P3 finding。

## 观察项

- `phase2-check.json.head` 为提交前 HEAD `0abdc0f`，其 `dirty_paths` 精确覆盖第三个 commit 的三个 tracked paths；符合 Branch Review Gate post-commit audit 合同。
- 当前分支尚未 push，真实 current-ref remote marketplace verification 仍为 publish 前 fail-closed 门禁；本地/public-main sampling 不替代该证据。默认 pinned tag 尚未发布且不属于本任务创建范围，PR body 已如实说明。

## 后续候选

- #98、#99、#100 保持 live #97 已定义的非目标。
- 未发现需要新增 issue 的当前独立范围。

## Docs SSOT 判断

- 结论：`PASS`。
- approved design 4.4、canonical/dogfood fixed fact、三类 failure tests、workflow/spec/README/requirements 对 snapshot-unavailable 的行为描述一致。
- Task artifacts 继续只保存审批、实现交接、Phase 2 与 review 历史，不替代 durable docs。

## 部署与安全判断

- 第三个 commit 未修改 CI/CD、Docker/Compose、Kubernetes/Kustomize、Helm、数据库 migration/seed/backfill、Makefile、API、服务、worker、定时任务、队列或业务运行时配置。
- 完整分支仍只影响 Guru Team workflow/preset/context/finish-publish metadata 控制面；remote verifier 在 publish 前 fail closed。
- 未发现新增 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或 workspace journal 内容迁移；fixed fact 与测试修复不需要部署步骤或 release tag。

## 结论

Round 3 closure：`PASS`，`findings_count=0`。Round 2 的唯一 P2 已完整闭环，完整分支未发现新 current-scope finding。Finding closure 链已具备 `round 2 -> round 3` 的同 agent `reuse-for-closure` 证据；下一步只能派发此前未参与任何 review round 的 fresh `最终放行审查代理` 对当前 HEAD 完整 diff 做独立审查。本代理因 finding-owner/closure 身份不得成为 final reviewer，也不对 Branch Review Gate 作最终放行结论。
