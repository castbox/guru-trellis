# Issue #131 Branch Review Round 3 问题闭环原始报告

## 审查身份与固定范围

- 逻辑角色：`问题闭环审查代理`，round 3。
- Technical agent：`/root/issue_131_branch_review_discovery`。
- Continuity：复用 round 2 finding owner，仅闭环
  `F-131-BR2-01`；assignment 已记录
  `reuse-for-closure`、`from_round=2`、`to_round=3`。
- 禁止角色：本代理不是、也不能担任最终放行审查代理。
- Task：`.trellis/tasks/07-23-131-guru-review-branch`。
- Base：`origin/main`。
- Reviewed HEAD：`38a0e8dd2314b086378e0674f4bd377dc5e6f694`。
- 完整范围：
  `origin/main...38a0e8dd2314b086378e0674f4bd377dc5e6f694`。
- Merge base：`ea132e350c4b6861fc955f17e590651a46e890ab`。
- 完整 diff：315 files changed，33022 insertions，933 deletions。
- Finding-fix commit：
  `38a0e8dd fix(workflow): #131 绑定精确闭环轮次`；
  parent 为 `0fdbb708f91296847b5812c3c1b9dd80b6e488a2`。
- Workspace boundary：`status=ok`；expected workspace 与 actual repo root
  均为当前 task worktree；source checkout clean；suspicious source artifacts 为 0。
- 审查开始时仅存在 main-session 已登记的 task metadata tail：
  `agent-assignment.json` 与 `task-commit-plans/003.json`。

本轮只写本 raw report；未修改实现、测试、规划、Phase 2、
`review.md`、`review-gate.json`、assignment、task commit plan，未 commit、push 或
创建 PR。

## 当前权威与证据重读

本轮重新读取而未复用旧 pass 结论：

- live GitHub Issue `castbox/guru-trellis#131` 正文与 accepted-current comments；
- approved `prd.md`、`design.md`、`implement.md`；
- schema 2.0 `planning-approval.json`，其 `typed_exit=approved`，三份 planning
  SHA-256 仍精确匹配；
- current schema 2.0 `phase2-check.json`，其 `typed_exit=passed`，并把
  `F-131-BR2-01` 标记为 resolved；
- round 2 `reviews/02-finding-closure.md`，SHA-256 为
  `013ab622c3281f00264721f4c9f5868bb5d053dd13a403ad5722a26679857ee4`；
- finding-fix Phase 2 raw report、issue scope ledger、current task commit 003
  evidence；
- `guru-review-branch` canonical/installed package、runtime、tests、eval adapter
  与 durable recovery/closure contracts；
- 完整新 committed range，而非只审查 finding-fix commit。

Qualification 继续遵循 Issue #131：只有
`normal_required_behavior`、`explicit_nonstandard_requirement`、
`approved_nonstandard_expansion` 且真实违反当前合同时才赋 P0-P3；未确认扩张、
威胁模型、恶意伪造、TOCTOU、额外 fault injection、crash consistency 与跨 OS
atomicity 不进入 current finding。

## F-131-BR2-01 闭环复核

### 原 finding

Round 2 证明：per-finding lifecycle 在检查某个 resolved finding 的
`closure_evidence` 时，只要同一 finding owner 在最终轮前存在任意合法 replacement
closure，旧 helper 就会返回成功。于是一个合法 round 2 replacement chain 可以替
没有 owner linkage 的错误 round 3 raw report 背书。

这是正常 multi-closure 流程中的引用错误，不依赖恶意伪造、手工错误 digest、攻击
artifact、并发竞态或非常规 failure injection。

### 实现闭环

- `finding_round_has_replacement_closure(...)` 新增内部可选参数
  `expected_closure_round`。
- 当参数存在时，closure candidate 必须满足
  `review_round_number(item) == expected_closure_round`。
- per-finding lifecycle 在完成 report path、task-local identity、digest、role 与
  later-round 检查后，传入当前 `closure_number`；因此 replacement recovery chain
  必须与 semantic finding 实际引用的 raw report 属于同一 closure round。
- branch-wide final-review prerequisite 仍不传该参数，保留“任意一条合法
  replacement recovery chain 可以证明该 finding owner 已先闭环”的既有全局语义。
- public Skill I/O、typed exits、schema、consumer projection 与 durable contract
  均未改变；没有新增第二套 lifecycle helper。

关键实现证据：

- helper exact-round filter：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:7236-7265`；
- per-finding exact binding：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:12790-12883`；
- branch-global final path 保持默认调用：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:7498-7528`。

### 独立正常路径复现

本轮独立执行 6 个精确回归：

1. round 1 owner 有 finding；
2. round 2 存在完整
   `failed -> replacement-started -> completed` recovery chain、精确
   `from_round=1` / `to_round=2` 的 `replace` decision 与真实 raw report；
3. round 3 是另一个 closure agent，其 relation 只从 round 2 指向 round 3，不与
   round 1 owner 建立关系；
4. final reviewer 位于 round 4；
5. resolved finding 错误引用 round 3 report。

当前 runtime 对错误引用返回两个预期 lifecycle errors：

```text
closure round lacks an explicit same-agent, new-agent, or replacement recovery linkage
resolved finding has no current bound closure_evidence
```

同一 fixture 把 `closure_evidence` 改为精确、合法的 round 2 report 后返回空错误
列表。其余回归同时证明：

- same-agent prior-head closure 仍通过；
- explicit new-agent closure 仍通过；
- chained new-agent closure 仍通过；
- replacement closure 后的 branch-global fresh final validation 仍通过；
- final reviewer 与 closure reviewer 的角色隔离保持不变。

Focused 结果：6/6 passed。

### Closure 结论

`F-131-BR2-01` 已在 Reviewed HEAD 精确关闭。修复既拒绝错误、未链接的
closure report，又保留 exact replacement、same-agent、new-agent 与 branch-global
final 的支持路径。

## 完整范围语义复核与新 finding

本轮按 approved planning 与 Issue #131 对
`origin/main...38a0e8dd2314b086378e0674f4bd377dc5e6f694` 完整范围重新复核了：

- workflow 与 Skill-first closed-loop 分层；
- semantic AI Gate、human confirmation 与 deterministic
  recorder/validator 边界；
- public Skill input/output、typed exit 与 consumer projection；
- finding qualification、closure evidence、replacement recovery 与 fresh-final
  agent separation；
- canonical/installed/package/platform mirror 一致性；
- preset/overlay、upgrade/update、ownership 与开箱即用证据；
- Docs SSOT、测试、安全、部署与仓库卫生。

未发现新的、可在受支持正常路径中复现的 P0/P1/P2/P3 current-scope finding。
没有 scope proposal。

Round 1 历史 findings 保持 closed：

- `F-131-BR-01`：closed；
- `F-131-BR-02`：closed；
- `F-131-BR-03`：closed；
- `F-131-BR-04`：closed。

Round 2 finding：

- `F-131-BR2-01`：closed。

## 验证结果

| 验证项 | 本轮结果 |
| --- | --- |
| `git diff --check origin/main...38a0e8dd...` | passed，exit 0，无输出 |
| Focused closure/compatibility regression | 6/6 passed |
| `guru-review-branch/tests/test_contract.py` | 8/8 passed |
| Runtime full suite | 566 passed，13 skipped |
| Skill package full suite | 167/167 passed |
| Preset installer suite | 45/45 passed |
| Upstream ownership suite | 6/6 passed |
| Source package validator | passed；10 active Skills / 39 exits / 23 targets |
| Installed package validator | passed；10 active Skills / 39 exits / 23 targets；1903 managed files，0 sidecar/removal/conflict |
| Source shared real-wrapper eval | 7/7 passed |
| Installed shared real-wrapper eval | 7/7 passed |
| Canonical/installed runtime byte parity | passed |
| Canonical/installed `guru-review-branch` package parity | passed |
| Dogfood overlay drift | passed；43 frozen/active paths，0 removed |

Lint：

- 完整 committed range 的 `git diff --check`、repo package/runtime/preset/
  ownership validators 均通过；
- 仓库未声明独立 `ruff`、`shellcheck` 或统一额外 lint gate。

TypeCheck：

- 仓库未声明独立 `mypy` / `pyright` gate；不适用。

开箱即用 / upgrade-update：

- 本轮独立重跑 package validator、preset installer、ownership、source/installed
  real-wrapper eval 与 dogfood drift，全部通过；
- fresh Phase 2 已在同一 finding-fix implementation tree 上完成 full throwaway：
  默认因禁止 public `main` 冒充当前 feature ref 而按预期 exit 2，显式设置
  `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 后 exit 0，覆盖 fresh init、
  existing preview/switch、平台入口、package smoke、wrapper/eval、
  `trellis update --force` 与 workflow/preset reapply；
- Round 3 未重复执行耗时 full throwaway，不能把 fresh Phase 2 的该项证据表述为
  本轮独立重跑。当前 branch 尚未发布，exact remote feature-ref marketplace install
  仍是发布前限制。

## Docs SSOT、部署与安全

- Docs strategy：`ssot_first`；task delta 已合并。
- 本轮修复使 runtime 追平既有 exact closure evidence / lifecycle contract，不产生
  新的 durable wording 需求。
- public Skill I/O、schema 与 typed exit 无变化；source/installed package、runtime
  与平台入口保持一致。
- 本 range 没有 CI/CD、container、Kubernetes、database migration、Makefile 或业务
  service deployment变更，无部署迁移要求。
- 未观察到 secret、credential、客户数据、`.env` 或签名 URL 泄露。Task-local
  workspace evidence 不属于公共 package。

## 结论

- Round 1 四项 finding：全部 closed。
- Round 2 `F-131-BR2-01`：closed。
- Round 3 新 findings：
  - P0：0
  - P1：0
  - P2：0
  - P3：0
- Scope proposals：0。
- 问题闭环审查已完成，可以 dispatch 一个从未参与问题发现或闭环的全新 technical
  agent，对当前 HEAD 与完整 `origin/main...HEAD` 执行 fresh final review。
- 本报告只证明 historical findings 已闭环，不替代 fresh final review，也不能单独
  支持 Branch Review Gate `passed`。
