# #118 Branch Review 汇总

## 门禁状态

- 审查范围：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c...5695f7aab15b5d40660b535948c11c0ef55300f5`
- 审查 HEAD：`5695f7aab15b5d40660b535948c11c0ef55300f5`
- 当前最新轮次：`round-002`
- 语义出口：`implementation_required`
- 当前未解决问题：`1`（P0=0，P1=1，P2=0，P3=0）
- 发布边界：本汇总只支持 Branch Review Gate recorder；不授权 push、PR、archive、finish 或 issue close。

## 审查轮次

| 轮次 | 角色与复用 | 原始报告 | 审查 HEAD | 结论 | 新问题 |
| --- | --- | --- | --- | --- | --- |
| 1 | 最终放行审查代理，fresh `new-agent` | [round-001-final-release.md](reviews/round-001-final-release.md) | `5695f7aab15b5d40660b535948c11c0ef55300f5` | implementation required | P1=1 |
| 2 | 问题发现审查代理，same-agent `reuse` | [round-002-problem-discovery.md](reviews/round-002-problem-discovery.md) | `5695f7aab15b5d40660b535948c11c0ef55300f5` | implementation required | P1=1（同一 finding owner binding） |

## 候选资格化

### `F-FINAL-LEGACY-01`（P1，open）

- Scenario：`normal_required_behavior`。
- Affected behavior：`guru-finalize-task` 无法接管由现有 #105 engine 合法持久化的同月 partial closeout plan。
- Requirement：`prd.md` R2、R11、AC8，以及 `design.md` 的 standalone active/partial/archived recovery profile。
- 正常路径：旧 engine 以 `include_finalization_gate=False` 生成合法 immutable plan；新 finalizer 重用该 projection；semantic recorder 正常写入 `task-finalization-gate.json`；后续 rebuild 因旧 `move_paths` 不拥有 gate 而返回 `unexpected_task_files`，evidence metadata commit 也会因 exact dirty allowlist 阻塞。
- 资格理由：复现不依赖手工篡改、恶意 actor、并发、锁、TOCTOU、fault injection、crash consistency 或跨 OS 原子性；它是已支持的 standalone partial recovery 顺序。
- 修复要求：增加 deterministic、plan-bound 的 finalizer takeover/migration，使新 private gate 被 plan ownership、dirty staging、evidence commit 与 archive move 一致拥有，同时保留 generic #105 unexpected-artifact fail-closed；补同月 legacy partial preview -> recorder -> checker -> transition 生产级回归。

## 证据

- Round 1 raw report：`reviews/round-001-final-release.md`，SHA-256 `fb20ddde215358278b41a2cf0e4516de49f1c03e56b79c2be9fceec278869082`，14348 bytes。
- Finding-owner raw report：`reviews/round-002-problem-discovery.md`，SHA-256 `85fb4589c3b43ae4bd944b88f214dbd6c567df1f7efa98231c202f3f1e6ca3df`，10946 bytes。
- Fresh validation：runtime 611 passed/13 skipped、Skill packages 178 passed、preset 45 passed、finalizer package 4 passed、installed shared real-wrapper eval 8/8 passed。
- Source/installed package validation、contract/eval discovery、dogfood overlay drift、task validation、`git diff --check`、Bash syntax、Python compile 均通过。
- Fresh throwaway exit 0，覆盖 initial install/reapply、official `trellis update`、managed hash、`.new/.bak` recovery、all-platform distribution 与 installed recovery。
- 上述通过项没有覆盖 legacy partial plan -> finalizer takeover 状态迁移；fresh probe 已稳定重现 finding。

## Docs SSOT

- 批准策略：`ssot_first`。
- Durable docs、task planning 与 package/runtime inventory 基本一致，但当前实现未兑现已声明的 #105 transaction compatibility 与 standalone partial-state recovery。
- 本轮不修改文档或实现；修复应优先使实现符合当前合同，若必须改变合同则需先回到 planning/wording gate。

## Scope、安全与部署

- Scope ledger 只关闭 #118；#115 保持 related；#119/#132 保持 follow-up ownership；不改变 #105 已完成事务语义。
- 未发现 credential、token、private key、`.env`、签名 URL、客户数据或敏感原始记录泄漏。
- 无 dependency、CI/CD、container、K8s/Helm、DB migration、Makefile、服务部署或 production data write 变化；存在 extension/preset/package/schema/runtime 的安装与升级影响。
- #119 global Finish-family integration、#132 upstream overlay cleanup 与 hostile/concurrency/TOCTOU 扩张均不进入本 finding。

## 结论

Branch Review 资格化得到一个 open P1 current-scope finding。当前必须返回 implementation，完成修复、fresh Phase 2、新 task commit、finding closure round 和新的 fresh final reviewer 后，才能重新判断 `passed`。
