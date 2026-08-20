# #283 Test contribution

以下条目是 #283 candidate 的 required validation contract。当前 Phase 2 证据只在文末按
实际执行范围更新；每个结果必须绑定 expected current
`current-main-0.6.5-guru.37`、candidate tree/committed diff 与 fresh project-check identity；
不可访问的 external evidence 保持 `unverified`。

- `TST-018`：验证 Planning、implementation discovery、Phase 2、Branch Review、
  Publication、Acceptance/Finish 的 mandatory invocation、freshness 与唯一 typed consumer；
  Phase 2 首次检查，Branch Review 从 committed full diff 独立重算，promotion 后两者重新执行。
- `TST-019`：验证 constitution locator + version/content identity 与恰好五个稳定
  identity/short name；公共 schema、fixture 和 contribution 不含原则正文、score、required
  verdict 或机械 checklist，no-impact 不创建 contribution/ADR。
- `TST-020`：验证 `target_native|legacy_boundary_convergence|dedicated_refactor_slice`
  三路径互斥且 `no_architecture_impact` 独立；#283 只接受 `target_native`。
- `TST-021`：验证 Guru public identity + project baseline/change-contract identity、required
  concern applicability、owner/single-writer、compatibility exit、parallel scope、deviation、
  evidence、review/promotion 与 expected-current 字段闭合；missing/empty/stale 或无依据
  `not_applicable` fail closed。
- `TST-022`：验证项目检查 `pass|fail|unverified`、rule/decision/GAP linkage、before/after、
  evidence/unavailable reason、freshness 与 applicability + task dependency 导出的
  `blocking`；blocking 缺口阻断，non-blocking 缺口保持显式且不能证明 GAP/例外/完成。
  新增或恶化偏移、owner 扩张、无退出双写和 closed GAP 重现均返回
  `fitness_regression`。
- `TST-023`：验证 contribution 与 shared current 隔离；只有指定 ADR trigger 创建 ADR
  candidate；reviewed promotion 绑定 expected current 并由唯一 owner 串行执行，未 review、
  未 promotion 或 live current 已推进均不能写 shared authority。
- `TST-024`：验证两个 task 使用不同 contribution locator，允许独立 scope，禁止竞争同一
  GAP/owner/current 文件；task A promotion 后 task B 返回 `sync_required` 并重做 impact、
  satisfaction 与 parallel-scope 判断。
- `TST-025`：验证 Architecture 2.0 schema、runtime、canonical/dogfood/installed、
  Shared/Codex/Claude/Cursor 与所有 consumer 原子一致；旧/缺失 schema 明确拒绝，不保留
  legacy selector、dual-read 或 compatibility adapter，stable Skill/profile/exit ids 不变。
- `TST-026`：验证 package/contract/runtime/eval、project-neutral 10-scenario corpus、preset
  apply/reapply、drift/sidecar 与一个代表性 clean installation；报告必须明确未执行 #267
  exact-candidate 全平台矩阵、tag/Release/immutable smoke 与 business-repository 验证。

## Fixed scenario coverage

| Scenario | Expected result |
| --- | --- |
| `SCN-024 no-impact` | fresh minimal current result；零 contribution/ADR |
| `SCN-025 target-native` | target boundary + unique owner；新增 legacy authority 被阻断 |
| `SCN-026 legacy-boundary-convergence` | decision/GAP、局部收敛、remaining debt、compatibility exit 与 forbidden scope 完整 |
| `SCN-027 dedicated-refactor-slice` | 行为/API/规则不变，单一主写，小切片可验证、观测、回滚并有旧实现删除条件 |
| `SCN-028 scope-expansion` | persistence/SDK/owner/boundary 扩大使 Planning result stale 并 re-entry |
| `SCN-029 fitness-regression` | 第二 authority、legacy owner 扩大、无退出双写或 closed GAP 重现返回 `fitness_regression` |
| `SCN-030 parallel-stale` | task A promotion 后，task B 旧 identity 返回 `sync_required` |
| `SCN-031 unpromoted-contribution` | 实现/测试通过但 contribution/ADR/review/promotion 缺失时 Publication/Finish 阻断 |
| `SCN-032 next-task-consumption` | successor identity、decision/GAP/owner 状态成为下一 task 唯一 current input |
| `SCN-033 missing-external-evidence` | 保持 `evidence_gap|unverified`，不虚构通过、GAP 关闭、排期或发布 |

## Current Phase 2 validation evidence

当前 complete worktree candidate 已 fresh 通过以下 current-scope 验证：

- Architecture package contract/runtime：`16/16`；source package graph 为 `21` active
  packages / `72` commands，installed graph 为 `21` active packages / `20` invokes /
  `87` exits / `4232` managed files，零 conflict/sidecar。
- Architecture source/shared 与 installed/shared eval 均覆盖固定 `SCN-024..033` 十个场景并
  全部通过；`guru-approve-task-plan`、`guru-check-task`、`guru-review-branch` 的 contract/runtime
  consumer tests 分别为 `21+4`、`9+9`、`15+4` 通过；package closure 为 `8/8`。
- Preset upstream ownership `7/7`、installer apply/reapply `78/78`、upgrade contract
  `20/20` 通过；两次 all-platform reapply 均为零增量且零 backup/new/conflict/sidecar，
  dogfood overlay drift 与递归 `.new/.bak` 检查通过。
- `301` 个受影响 JSON fresh parse、Python compile、Bash syntax、`task.py validate` 与
  `git diff --check` 通过；task validation 仅保留既有大 spec 注入截断 warning。

`guru-trellis-architecture-convergence@1` 因而对当前 Phase 2 candidate 为 `pass` 且
`blocking=true`。以下后续门禁仍未完成且不在本段冒充通过：

- `guru-verify-extension-installation` 只接受 clean source checkout；当前全部 candidate 尚未
  commit，且本次恢复边界禁止创建新的 Git/Trellis 资源，因此代表性 clean standalone
  install 延后到 reviewed commit 后、Publication 前执行。
- independent committed full-diff Branch Review、serialized Architecture/RDT promotion、
  promotion 后 Phase 2/Branch Review 重跑与 next-task consumption smoke 仍为 pending。
- #267 exact-candidate 全平台矩阵、tag、Release 与 immutable smoke 始终不属于 #283。

当前 contribution validation state：`phase2_current_scope_passed_with_post_commit_gate_pending`。
