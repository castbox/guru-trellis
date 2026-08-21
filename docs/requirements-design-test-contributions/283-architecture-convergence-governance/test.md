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

- Architecture package contract/runtime：source 与 dogfood installed 均为 `22/22`；source
  package graph 为 `21` active packages / `72` commands，installed graph 为 `21` active
  packages / `72` commands / `20` invokes / `87` exits / `4229` managed files，零
  conflict/sidecar。Architecture public inventory 为 interface `5` inputs / `7` outputs，
  canonical 与 installed manifest 均为 `62` inputs / `85` outputs，Architecture id 无缺失
  且两份 inventory 一致。
- Architecture source/shared 与 installed/shared eval 均覆盖固定 `SCN-024..033` 十个场景并
  全部通过；`guru-approve-task-plan`、`guru-check-task`、`guru-review-branch` 的 source 与
  dogfood installed current contract tests 均分别为 `21/21`、`9/9`、`15/15`。RDT package
  为 `9/9`，package closure 为 `8/8`，finish-family integration 为 `6/6`，semantic
  retrieval contract 为 `4/4`。
- Preset upstream ownership `7/7`、installer apply/reapply `78/78`、upgrade contract
  `20/20` 通过；最终 all-platform reapply 为零增量且零 backup/new/conflict/sidecar，
  dogfood overlay drift 与递归 `.new/.bak` 检查通过。
- 最后的 canonical finding fix 已把三处 workflow current-route 合同同步到
  `.trellis/workflow.md`，并让 `check-dogfood-overlay-drift.sh` 同时比较 canonical 与 dogfood
  workflow；真实临时 fixture 已证明相同 workflow 通过、stale workflow 稳定报告
  `CHANGED .trellis/workflow.md` 并只提示官方 marketplace 恢复；另一个 preset-owned stale
  spec fixture 只提示 preset `apply.sh`。当前仓库增强后的 drift checker 通过。
- 完整 base-to-worktree candidate 共 `429` 个路径（`379` 个现存、`50` 个删除）；其中
  `300` 个 JSON fresh parse、`13` 个 Python 文件 compile，canonical Bash syntax、
  `task.py validate` 与完整 candidate `git diff --check` 通过；task validation 仅保留既有
  大 spec 注入截断 warning。
- 本轮候选已在无 `.git` 的隔离临时目标完成一个代表性 current-version clean
  installation：Trellis `0.6.15`
  从公开 marketplace 初始化基础结构后，明确覆盖为当前 canonical workflow，再应用当前
  all-platform preset；真实 installed public graph、
  installed/shared 固定十场景 public dispatcher、Phase 2 context smoke、Shared/Codex/Claude/
  Cursor parity、frozen reapply 与 recursive zero-sidecar 均通过。package
  `tests/test_contract.py` 是要求 source manifest 与 Git runtime 的 source-oriented unit
  harness，不是无 `.git` 目标声明的 installed public entry；本证据不把该不支持的直接调用
  冒充为 standalone pass。该 targeted 证据证明当前本地 candidate 的安装态，不证明未发布
  branch 的 marketplace ref 或正式 standalone verifier typed exit。
- `guru-check-task` 已对完整 base-to-worktree candidate 完成 schema 5.0 语义检查：九个
  adequacy dimension 全部通过。三项 committed-diff finding 与最终 workflow literal-wrap
  candidate 在修复后的 current supported path 上均为 `rejected_not_reproduced`；clean target
  直接运行 source-oriented unit harness 的观察为 `rejected_unsupported_entry`。open finding
  与 blocking unverified item 均为零，typed exit 为 `passed`。owner-private content token
  不复制到 durable Docs；本段状态同步后从 live content 重录并由 checker 再次确认，最终
  结果只由 fresh private checkpoint 承接。

`guru-trellis-architecture-convergence@1` 因而对当前 Phase 2 candidate 为 `pass` 且
`blocking=true`。以下后续门禁仍未完成且不在本段冒充通过：

- 正式 `guru-verify-extension-installation` 合同要求 source checkout clean 且 requested ref
  解析到当前 HEAD；当前 worktree dirty、branch 尚未发布，因此本轮不具备合法 executor
  entry，也未形成 `verified` typed exit。先前 exact `82f0469` 的
  `blocked(reason_code=requested_ref_not_published)` 只保留为历史边界；不得把本轮 targeted
  clean installation 冒充为正式 verifier pass。
- 原 independent committed full-diff Branch Review 已返回 current-scope findings；对应代码
  修复已进入当前 candidate，但 finding closure 仍须由新 task commit 与 distinct fresh-final
  full-diff review 证明。serialized Architecture/RDT promotion、promotion 后 Phase 2/Branch
  Review 重跑与 next-task consumption smoke 仍为 pending。
- #267 exact-candidate 全平台矩阵、tag、Release 与 immutable smoke 始终不属于 #283。

当前 contribution validation state：
`phase2_semantic_passed_with_fresh_private_checkpoint_after_status_sync_local_public_entry_clean_install_formal_verifier_ineligible_and_post_phase2_gates_pending`。
