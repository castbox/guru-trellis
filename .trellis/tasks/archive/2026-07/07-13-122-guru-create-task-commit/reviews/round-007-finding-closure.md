# #122 第七轮问题闭环审查报告

## 身份与审查边界

- 逻辑角色：`问题闭环审查代理`。
- 技术身份：`trellis_final_review_122_02`。
- 平台昵称：`Final-Review-Agent-122-02`。
- 复用决策：`reuse_decision: reuse-for-closure`。
- 本代理是 Round 6 的 finding owner，本轮只能复核 `F-06-01`、`F-06-02`、`F-06-03` 及其修复引入的相邻回归；本代理永远不得担任后续最终放行审查代理。
- Reviewed HEAD：`005c41fa755d4fea2d7c4f2bd8463041ffc7fe32`。
- Finding-fix range：`163e64168d5d9783c32665da92aebbb4397564a3...005c41fa755d4fea2d7c4f2bd8463041ffc7fe32`，1 个线性 work commit、48 个 committed paths。
- Base evidence：`origin/main=6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`。
- 操作边界：本报告是唯一写入；未修改实现、durable docs、旧 task artifact、旧 raw report 或 rollup；未运行 `review-branch.sh`、`check-review-gate.sh`、`record-agent-assignment.sh` 或任何 `record-*`；未 stage、commit、push、创建 PR、调用 finish-work 或关闭 issue。

## 输入证据

- Live issue：`castbox/guru-trellis#122`，状态 `OPEN`，唯一 close candidate 为 #122；#92、#120 只在 `related_issues`。
- 官方 Trellis 文档：`https://docs.trytrellis.app/index.md`、`advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md`。当前实现保持 Markdown workflow/skill 拥有流程与 AI 判断，companion runtime 只验证或执行确定性事实。
- Round 6 finding source：`reviews/round-006-final-release.md`，包含 2 个 P1 和 1 个 P2。
- 规划与检查证据：`prd.md`、`design.md`、`implement.md`、schema 1.2 `planning-approval.json`、`implementation-handoff.md`、`phase2-check.json`、`phase2-check-report-round-010-fix.md`、`issue-scope-ledger.json`、`agent-assignment.json`。
- Durable owners：README、三份 requirements 文档、五份 workflow spec、canonical/dogfood workflow、workflow README、canonical skill package、runtime、tests、installed/platform copies 与 extension manifest。
- 提交证据：sequence `006` plan 的 committed/working 两种 bytes、真实 commit object、parent、raw message、path set、tree、48 个 blob/mode identity 与 working result。

## Round 6 问题闭环

### F-06-01（P1）已关闭：非普通 Git operation 不再被 task commit 消费

- Runtime 通过 `TASK_COMMIT_GIT_OPERATION_MARKERS` 覆盖 merge、cherry-pick、revert、rebase HEAD、sequencer、rebase-merge 与 rebase-apply/am；`task_commit_git_operation_state()` 只读取 marker，不改写现场。
- Candidate validation 在解析 task/HEAD/snapshot 前记录并检查 operation state；executor entry、message file 提交前和 publication boundary 再次调用 ordinary-state gate。
- 真实冲突 cherry-pick 回归证明 candidate validator 与 executor 均返回 blocked，且 HEAD、`CHERRY_PICK_HEAD` bytes、index、status 与 candidate bytes 保持不变。
- 七类 marker table regression 全部证明 detector 客观、非破坏；isolated `git commit` 不会消费 real checkout 的 sequencer state。

结论：Round 6 复现的“清除 `CHERRY_PICK_HEAD` 并错误返回 committed”路径已不存在，`F-06-01` closed。

### F-06-02（P1）已关闭：gitlink revision 由 artifact OID 授权

- `capture_task_commit_snapshot()` 对 mode `160000` 的非删除 entry 记录 `gitlink_head`、`gitlink_initialized=true`、`gitlink_dirty=false`；目标必须 initialized、以该 exact path 为 submodule root、具有唯一 commit HEAD 且 clean。
- Candidate freshness 会因 B 切换到 C 而改变 snapshot；uninitialized、dirty、unborn 或 root mismatch 均 fail closed。
- `task_commit_planned_index_bindings()` 不再让可变 worktree选择 gitlink staged content，而是直接使用 artifact 中 reviewed `gitlink_head` 与 mode `160000` 构造 isolated index。
- Executor 在 exact staging 前后复核 worktree HEAD，并验证 index OID/mode；A/B/C 回归证明 B->C 在 validation 后发生时不会 index/commit C，恢复 B 后实际 commit tree 精确包含 B。
- 普通文件、symlink、delete、rename、multi-path 与 candidate self 同样使用 artifact SHA-256/mode 或 deterministic candidate bytes，未为修复 gitlink 引入第二条可变 authority。

结论：未审查 submodule revision 无法再通过旧 snapshot 提交，`F-06-02` closed。

### F-06-03（P2）已关闭：workflow 已收敛为 route-only

- Canonical `trellis/workflows/guru-team/workflow.md` 与 dogfood `.trellis/workflow.md` 字节一致。
- 两份 workflow 已删除 work commit 的 type/scope、固定 `背景/变更/边界/验证` body 与 `Refs` 详细模板；只保留 shared branch validator 引用、metadata/merge 的全局合同，以及 Phase 3.4 的 mandatory invocation、3 个 typed exits、repeat route 和 unknown/multiple/unmapped fail-closed。
- Phase 3.4 各有且只有 1 个 `guru-create-task-commit` invoke marker；`committed`、`revision-required`、`blocked` 各有唯一 consumer/stop。
- `test_platform_entries_and_workflows_only_route_task_commit_skill` 现在直接扫描 canonical/dogfood workflow，拒绝完整 work template、direct `git commit` 和第二套 parser；永久回归已通过。

结论：step-local message/candidate/executor/postcondition 正文只属于 canonical skill package，`F-06-03` closed。

## Publication transaction 审查

- Executor entry 读取完整 live index preimage并以真实 `index.lock` `O_EXCL` sentinel 阻止并发 Git index writer；isolated transaction 使用独立 `GIT_DIR`、detached transaction HEAD 与 isolated index，真实 hook 链不会直接移动 live branch/index。
- Ordinary path 只在 bytes/mode 仍匹配 artifact 时 `hash-object -w`；gitlink 只使用 artifact OID；candidate self 使用已验证 plan 的 deterministic bytes。
- 真实 branch 只通过 compare-and-swap `update-ref(old=pre_commit_head)` 推进；推进后立即取得并验证 loose-ref lock。并发 ref writer在 advance 前、advance/guard 间或 rollback 前发生时，conditional update 保留第三方 state。
- Candidate result 与 final index 都先写同目录独立 temp；candidate guard、ref guard 与真实 `index.lock` 持续存在。Final index 使用独立 temp `os.replace()` 到 live index，不消费 sentinel。
- Final candidate inode/content identity read 是唯一 success linearization point。Read 前 candidate C 会使 executor blocked，只回滚 transaction-owned ref/index 并保留 C；read 后 C 是 later operation，immutable commit blob 与 returned result digest 仍授权 committed。
- Final read 后只有 best-effort fd/guard/temp cleanup 与返回，没有能把成功追溯为 blocked 的 fallible check。

未发现 publication、rollback ownership、hook isolation、candidate/ref/index guard 或 linearization 的新缺陷。

## Sequence 006 审计

| 项目 | 结果 |
| --- | --- |
| Commit / parent | `005c41fa755d4fea2d7c4f2bd8463041ffc7fe32` / `163e64168d5d9783c32665da92aebbb4397564a3`，与 plan 精确一致 |
| Message | raw commit message SHA-256=`4ee6801431b41898ef351b01686588c6e2d41a8d3a4a4c057134a784bef8f4ac`，与 plan 一致；只含 `Refs #122`，无 close keyword |
| Path set | 真实 commit 48 个 paths；与 `exact_stage_paths` 数量和排序后集合 digest `560769ee5e3d7457e9211991528bbe6712888a7e99302bb220b1f2e0af7febf5` 精确一致 |
| Tree | commit tree、expected tree、actual tree 均为 `6cd8a0cf869f5c8248ca094d14c1e33003e65877`，`actual_source=commit` |
| Blob/mode | 48/48 path 的 expected/actual blob 与 mode 精确相等，aggregate `matches=true` |
| Candidate blob | commit 中 `task-commit-plans/006.json` 保持 `result.status=planned`；blob=`57c2fde78f71b502dfa56830b95d5d4b8cec5538`、mode=`100644`，与 tree evidence 一致 |
| Working result | 当前 task-local plan 为 `status=committed` / `exit=committed`，绑定同一 commit、parent、message、48 paths、tree 与 `unrelated_preserved=true` |
| Preservation | 29 个 Phase 2/review/liveness/handoff/旧 plan metadata paths 未进入 work commit；staging 仍为空 |

Sequence 006 的 subject/body、47 个 reviewed work paths 加 candidate self、无部署变更、无 push/PR/close 边界与真实对象一致。

## Docs SSOT

- Approved strategy=`ssot_first`，docs state=`partial_docs`。
- README、`docs/requirements/{README,requirement-main,guru-team-trellis-flow}.md`、`.trellis/spec/workflow/{companion-scripts,data-contracts,quality-guidelines,skill-package-contract,workflow-contract}.md`、workflow README 与 canonical package contract 已一致记录 ordinary operation gate、gitlink artifact authority、isolated transaction、index sentinel、conditional rollback 与 final candidate read 线性化。
- Global workflow 已删除 step-local work message 模板；platform continue entries 仍只负责加载/调用/路由。未发现 durable owner 与 runtime/schema/tests/installed copies 漂移。
- Task-local correction/recovery rows、单次测试输出、临时 throwaway SHA 与本报告保持 task history，不进入公共 package。

Docs SSOT 满足当前 closure 范围，没有 current-scope inconsistency。

## Assignment schema 1.2

- `event_corrections[]` 只能 append digest-bound `invalidate-provenance`，target 必须是 same-agent progress/status-request event；terminal、assignment、stale、resume、termination、replacement、completion、failure 与 workspace boundary event 均不能失效。
- Correction validator 拒绝 unknown/duplicate target、duplicate id、cross-agent、target digest tamper、非 `main-session` source、不可解析 HEAD/UTC timestamp 与占位 reason/evidence；raw history不删除，只从 effective projection 排除已验证 target。
- `recovery_links[]` 只能连接 earlier same-agent `failed` 到 later `manual_or_platform_terminated_unfinished`，绑定两个 immutable event digests；unknown/duplicate/backward/cross-agent/tamper/cycle 均 fail closed。
- Recovery link 本身不构造 pass；`status_event_completion_errors()` 仍沿现有 resume/replacement predecessor 链遍历到真实 later `completed`。缺少 replacement completion 的永久负向测试继续 blocked。
- Review gate 的 finding-owner closure 与 fresh final reviewer 规则未被 normalization/correction/recovery 路径改写；本代理仍被明确禁止成为最终 reviewer。

结论：schema 1.2 是 append-only machine repair 合同，没有弱化旧 liveness、Phase 2 或 Branch Review gate。

## 验证结果

| 检查 | 独立结果 |
| --- | --- |
| Transaction / operation / gitlink / hook / race | `TaskCommitCandidateExecutorTest` 36/36，30.556s，`OK` |
| Assignment / liveness | `AgentAssignmentArtifactTest` 12/12 + `SubagentLivenessStateMachineTest` 18/18，合计 30/30，`OK` |
| 六 package roots | canonical + `.trellis`/shared/Claude/Codex/Cursor 各 4/4，合计 24/24，全部 `OK` |
| Full suite | skill/runtime/preset 518/518，145.118s，`OK`；另加 canonical package 4/4，对应 522/522 |
| Clean throwaway | Exit 0；public discovery + current unpublished local workflow sample、fresh init/install、initial/finding-fix 两次真实 task commit、old-plan reject、update、workflow preview/switch/reapply、preset reapply、两次 closeout、source/installed/drift 与 recursive sidecar 均通过 |
| Source/installed | 均 `passed`；reserved=1、active=1、invoke=1、exits=3；installed managed=43、sidecar/removal/conflict=0 |
| Canonical equality | Workflow/runtime 2 对 byte-equal；canonical package 到 5 个 installed/platform roots exact diff 为空 |
| Static | branch/working/cached `git diff --check`；branch changed Python compile、Bash syntax、40 个 branch/untracked JSON parse 全部通过 |
| Security | Public non-task added-line 高置信 private key/token/credential URL/signed URL/机器绝对路径扫描 0 命中 |
| Deployment | `.github/workflows`、Docker/Compose、Kubernetes/Kustomize、Helm/chart、migration、Makefile changed path 0；无需部署资产同步 |
| Workspace hygiene | Boundary/planning approval `status=ok`；HEAD 未变、staging=0、source checkout clean、suspicious source artifact=0、repo-local `.new/.bak/.publication/.lock=0` |

审查过程中两组无效 harness invocation 未被计入通过证据：一组误把 `unittest -k` 当正则且把隐藏目录当模块路径，另一组在 zsh 循环误用特殊变量名 `path` 导致 `PATH` 被覆盖。两组均用正确的独立命令和 `set -e` 重跑，遗留临时目录已清理；它们不是产品失败或 coverage 缺口。

## 安全与部署影响

- Public package/artifact 不保存 dirty file content、operation marker content、secret、客户数据、credential、签名 URL或本机绝对路径。
- Message temp 仍使用 `0600` 并在 `finally` 删除；executor 不 push、不 reset/rebase/amend/stash、不改写已发布历史。
- 本轮只涉及 Trellis workflow/runtime/package/schema/docs/tests 与 task plan，不新增 service、worker、queue、scheduler、runtime config 或 database migration。
- Remote exact feature-ref marketplace verification 尚未执行；它按合同只能在 reviewed content push 后由 `trellis-finish-work` 生成，当前 local throwaway 不冒充该 publish evidence。

## 观察项

1. `remote_marketplace_verification` 继续保持 `pending`。这不阻断当前 finding closure，但必须在 publish 前由 finish-work 对 exact pushed feature ref 完成，否则 PR readiness 必须 fail closed。
2. Extension compatibility target 仍为 Trellis CLI `0.6.5`；本 issue 未授权把本地可见更新版本纳入兼容承诺。

## 后续候选

无。Round 6 三项 finding 均属于 #122 当前范围且已关闭，没有需要降级或外移的缺陷。

## 结论

- `findings_count: 0`。
- 严重度：P0=0、P1=0、P2=0、P3=0。
- `closure pass: 是`。
- 结论：`F-06-01`、`F-06-02`、`F-06-03` 全部 closed；Round 7 闭环通过。
- 本结论只关闭 Round 6 findings，不是最终放行。下一步必须由此前未出现在任何 review round 的 fresh `最终放行审查代理` 对当前 `origin/main...005c41f` 完整 diff 执行新的最终审查；本代理及所有 finding owner/closure agent 均不得担任该角色。
