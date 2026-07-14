# #122 第四轮问题闭环审查报告

## 身份与边界

- 逻辑角色：`问题闭环审查代理`。
- 技术身份：`trellis_final_review_122_01`。
- 复用决策：`reuse_decision: reuse-for-closure`。
- `reviewed_head: ce7056793ff49a82bf8275340986225af5b4c868`。
- Reviewed parent：`1534b545ad6777852cd6d588568a46bedb14bf9c`。
- Base：`origin/main=6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Branch：`feat/122-guru-create-task-commit`。
- 审查范围：只判断 Round 3 finding `C-01-T1` 的永久 package/runtime 正负矩阵是否在当前提交完整关闭；不执行最终全量放行审查。
- 操作边界：未修改实现、durable docs、Phase 2、assignment、`review.md`、`review-gate.json` 或旧 raw report；未运行任何 Guru Team recorder/validator、`review-branch.sh` 或 `check-review-gate.sh`，未 commit、push、创建 PR、调用 finish-work 或关闭 issue。

## 输入与提交证据

- Live issue：`castbox/guru-trellis#122`，标题为“实现 guru-create-task-commit 闭环 Skill 并收敛 Task work commit SSOT”，状态仍为 `OPEN`。
- Round 3 finding 来源：`reviews/round-003-finding-closure.md`；其 Reviewed HEAD 为 `1534b545`，结论为 `C-01-T1` P2 open。
- Finding-fix commit：`ce705679`，parent 为 `1534b545`，共 9 个 committed paths：8 个 test/provenance work paths 与 sequence 004 candidate。
- Fresh Phase 2 输入：`phase2-check-report-round-003-fix.md` 与 `phase2-check.json`；后者绑定 pre-commit HEAD `1534b545`，SHA-256 为 `e35dac52a960c494909f6218c9603c9b6ceece83a4bf9ecfa51ba605f5d63a4f`，size 为 8714，当前 bytes 与 sequence 004 evidence 仍完全匹配。
- Durable SSOT：`.trellis/spec/workflow/companion-scripts.md` 与 `.trellis/spec/guides/cross-layer-thinking-guide.md`；本提交没有修改其既有合同。
- Source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` 在审查前后均 clean，HEAD 与 `origin/main` 一致。

## 提交 004 证据

- Committed candidate 为 `result.status=planned`；working-tree candidate 为唯一 post-result `committed/committed`，符合 planned-bytes/working-result 合同。
- Raw commit message、planned message 与 working result 的 SHA-256 均为 `c43f92fc9f2d7d705a55a220848596ef5e93c8aee30669939900d1f3b5d7e964`，raw bytes 完全相等。
- Planned exact paths、working result committed paths、实际 commit diff paths 与 tree evidence paths 均为 9 个，集合相等且 tree evidence path 唯一。
- Expected tree、actual tree 与真实 commit tree 均为 `3fe4c13aa44726f292ff051e3786ee8bfadca0e8`，`actual_source=commit`、`matches=true`。
- 9 个 path 的 recorded expected/actual blob 与 mode 均与对应 tree object 相等；working result 的 runtime validation 返回 `errors=[]`。
- Plan 的 27 个分类路径唯一并完整覆盖 dirty snapshot 加 candidate self：9 个 `task-reviewed`、18 个 `unrelated-preserved`。

## C-01-T1 生命周期

### 第三轮状态

Round 3 证明 schema/runtime 当前行为正确，但永久 tests 没有承接完整状态矩阵，尤其缺少 `commit + changed HEAD` producer row 和 12 个 schema-bypass runtime tamper，因此记录 `C-01-T1` P2。

### 当前完成项

- Canonical package test module 新增唯一共享 builder，实际产生 7 个合法 producer rows、15 个 schema negative cases 与 12 个 runtime tamper cases。
- 7 个合法 rows 包含 pre-commit tree 未绑定/已绑定、commit unchanged HEAD clean/mutated、commit changed HEAD、postcondition clean/mutated。
- Package public-schema test 接受 7/7 producer rows并拒绝 15/15 schema negatives。
- Runtime test 通过 `importlib` 直接加载 canonical builder，没有维护第二份 matrix；正常 schema 与 mock-schema 路径都接受 7/7 producer rows，15/15 schema negatives 在 mock schema 后仍由 runtime 拒绝，12/12 runtime tampers 也在 mock schema 后被拒绝。
- 6 个 package roots 各 8 个 tracked files 字节一致，test SHA-256 均为 `b69224e54da83612b1d92958471a6a0029da42192d62a451beeec963e196ff31`；canonical/dogfood runtime 字节一致。

### 当前闭环状态

结论：`C-01-T1` **尚未完整关闭**。

共享矩阵、changed-HEAD row 与 case 数量已经补齐，但两个 runtime tamper 没有保持单变量，且 runtime test 只断言错误列表非空。目标 validator 回退时，这两项仍会由其它交叉字段错误代为拒绝，不能提供 Round 3 要求的独立永久回归保障。

## 开放问题

### C-01-T2（P2）路径与聚合匹配篡改仍被其它错误掩蔽

- Builder 证据一：`trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py:212` 的 `path match flag contradicts blob equality` 同时修改 `actual_blob`，但保留 path `matches=true`、tree `matches=true` 与 `hook_mutation=false`。
- 实际 runtime errors 为 3 个：path match flag contradiction、aggregate tree match contradiction、derived `hook_mutation` contradiction。删除 path match flag 校验后，该 case 仍会因后两项返回错误，test 保持通过。
- Builder 证据二：同文件 `:215` 的 `aggregate tree match flag contradicts tree facts` 修改 `actual_tree`，但保留 tree `matches=true` 与 `hook_mutation=false`。
- 实际 runtime errors 为 2 个：aggregate tree match contradiction 与 derived `hook_mutation` contradiction。删除 aggregate tree match flag 校验后，该 case 仍会因 hook contradiction 返回错误，test 保持通过。
- Runtime test 在 `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:877` 复用 12 个 cases，但 `:884` 只执行 `assertTrue(errors)`，没有断言每个 case 的精确目标 error，因此无法发现上述 masked regression。
- 独立单变量证明：从 matching postcondition row 只翻转 path `matches` 时，runtime 仅返回 path match flag error；只翻转 aggregate tree `matches` 时，仅返回 aggregate tree match flag error。当前 runtime 实现正确，缺口只在永久 regression payload/assertion。
- Phase 2 报告 `phase2-check-report-round-003-fix.md:82` 和 `:163` 声称所有目标均为非掩蔽回归；上述错误集合直接反证该结论在 path/aggregate 两项上不成立。
- 影响：未来删除或回退 path-level/aggregate-level match consistency validator 时，496 项 suite 仍可能全绿，`C-01-T1` 的 equality/aggregate 永久保障没有闭环。
- 修复要求：把 path case 改为 identity 相等但仅 `path.matches=false`，把 aggregate case 改为 tree/path facts 相等但仅 `tree_evidence.matches=false`；runtime test 对这两项至少断言精确单一 error，或对全部 12 项维护 expected error contract，避免任意其它错误代为通过。

## 永久矩阵核对

| 范围 | 当前结果 | 闭环判断 |
| --- | --- | --- |
| 合法 producer rows | 7/7，包含 `commit + changed HEAD`；schema/runtime 与 mock-schema runtime 全部接受 | 通过 |
| Schema negatives | 15/15 被 public schema 拒绝，mock schema 后 runtime 也全部拒绝 | 通过 |
| Runtime tampers 数量 | Canonical builder 12 个，runtime 直接复用并全部拒绝 | 数量通过 |
| Path uniqueness/full coverage | Duplicate 通过追加 entry 保持 exact set，missing 单独删除 entry；各自只触发 coverage error | 通过 |
| Derived mutation 双向 | Clean evidence + hook true 与 mode mutation + hook false 均只触发 derived mutation error | 通过 |
| Path match flag | Builder payload 同时触发 3 个正交错误，断言只检查非空 | 未通过 |
| Aggregate tree match flag | Builder payload 同时触发 2 个正交错误，断言只检查非空 | 未通过 |

## 文档单一来源与分发

- Docs strategy 仍为 `ssot_first`。Durable contract 已要求 public schema 与 runtime 共享完整状态矩阵，并在 `.trellis/spec/guides/cross-layer-thinking-guide.md:307` 要求完整正负 cross-product、在 `:309` 要求 derived boolean 双向测试。
- 本提交只修改 test/provenance，不需要新增 public field、runtime behavior、schema rule、workflow route 或 durable contract；不更新 durable docs 的方向正确。
- Canonical builder 与 runtime direct reuse 已消除矩阵双写；分发到 installed/shared/Claude/Codex/Cursor 的 test bytes 完全一致。
- `C-01-T2` 表明 test assets 尚未完整证明既有 SSOT，而不是 SSOT 文本缺失或 runtime/schema 再次漂移。

## 开箱即用与升级

- 本轮按问题闭环代理边界没有重跑 source/installed/drift recorder 或 validator。
- 同一 reviewed content 的 fresh Phase 2 已记录：clean throwaway、fresh install、initial/finding-fix commits、old-plan rejection、`trellis update`、workflow/preset reapply、source/installed validation、all-platform apply、dogfood drift、closeout smoke 与 recursive sidecar 均通过。
- Fresh Phase 2 同时记录 6 roots x 8 package files、installed manifest 43 managed files、conflict/removal/sidecar 为 0；本轮独立字节检查与 sequence 004 tree evidence一致。
- Remote exact feature-ref marketplace verification 仍需 reviewed content push 后由 finish-work verifier 完成；当前没有宣称远端门禁通过。这是 publish pending evidence，不是本轮新增 finding。
- 由于 `C-01-T2` 仍开放，既有 throwaway/update evidence 不能把当前分支推进到最终放行。

## 安全与部署

- `1534b545..ce705679` 的 9 个路径仅涉及 package/runtime tests、installed manifest provenance 与 task commit candidate；没有扩大 executor、network、GitHub 或 history-rewrite 副作用。
- Diff-added-line 安全扫描未发现 private key、access token、credential URL、签名 URL、客户数据或本机用户绝对路径。
- 变更路径不包含 GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、Helm、migration 或 Makefile；无需应用部署、数据迁移或部署资产同步。

## 验证命令与结果

| 检查 | 结果 |
| --- | --- |
| `TaskCommitCandidateExecutorTest` | 18/18，7.392s，`OK`。 |
| 六个 package roots | 各 4/4，共 24/24，全部 `OK`。 |
| Package/runtime/preset full suite | 496/496，126.947s，`OK`。 |
| Builder/runtime probe | 7 producer rows、15 schema negatives、12 runtime tampers；正常与 mock-schema 路径结果符合现有断言。 |
| 反掩蔽 probe | Path builder case 返回 3 个错误，单变量 path payload 只返回目标 1 个；aggregate builder case 返回 2 个错误，单变量 aggregate payload只返回目标 1 个。 |
| Sequence 004 commit-object audit | parent、raw message、9 path set、tree、9 个 blob/mode 与 working result 全部一致；runtime result errors 为空。 |
| Canonical/dogfood/platform equality | 6 个 package roots x 8 files 无 mismatch；canonical/dogfood runtime 相等。 |
| Static checks | Python compile、JSON/schema read、`git diff --check HEAD^ HEAD` 全部通过。 |
| Scope/security/deployment | #122 仍 open；added-line security scan passed；deployment asset changes=0。 |
| Workspace hygiene | Reviewed HEAD 保持 `ce705679`；source checkout clean；review worktree staged paths为空；recursive `.new/.bak` 为 0。 |

一次将六个 package 文件作为单个 `python -m unittest` 参数列表执行的命令因点号开头路径被解释为模块名而在 discovery 前失败；改为逐文件直接执行后 24/24 全部通过。该调用错误不是产品 finding，也没有修改文件。

## 问题、观察项与后续候选

- 最终开放问题：P0=0、P1=0、P2=1、P3=0；唯一开放项为 `C-01-T2`。
- 观察项：remote exact feature-ref marketplace verifier 按合同保持 pending；它不替代本地 closure review，也不是当前开放 finding。
- 后续候选：0。`C-01-T2` 是 `C-01-T1` 的直接 test-isolation 缺口，属于 #122 当前范围，不应外推新 issue。
- Finding owner：继续由技术身份 `trellis_final_review_122_01`、逻辑角色“问题闭环审查代理”在下一轮复核。

## 结论

- `C-01-T1`：`open`；共享 7/15/12 矩阵已落地，但 path/aggregate 两项仍缺少非掩蔽永久回归。
- `C-01-T2`：`open`（P2）。
- `findings_count: 1`（P0=0、P1=0、P2=1、P3=0）。
- 结论：`blocked`。
- 本报告只代表 Round 4 问题闭环审查，不代表最终放行。
- 下一步必须修正两个 builder payload并增加精确目标错误断言，完成 fresh Phase 2、创建新 sequence 与 finding-fix commit，再由同一 finding owner 复核；`findings_count=0` 后仍需全新最终放行代理审查完整 `origin/main...HEAD`。
