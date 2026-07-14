# #122 第九轮修复后独立 Phase 2 检查报告

## 身份、边界与结论摘要

- 逻辑角色：`阶段二检查代理`。
- 技术身份：`trellis_check_122_round9_fix`。
- 平台昵称：`Check-Agent-122-Round9-Fix`。
- 固定 worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`。
- Task：`.trellis/tasks/07-13-122-guru-create-task-commit`。
- Base：`origin/main=6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Pre-commit HEAD：`163e64168d5d9783c32665da92aebbb4397564a3`，检查与报告写入前后均未改变。
- Source checkout：`/Users/wumengye/Documents/GoProjects/guru-trellis`，HEAD 为
  `6b9495a17dc953c7a54c105e39c23a786edcd8a7`，检查前后 clean。
- Implementation handoff SHA-256：
  `7232c2f30e26d49f18ead65ea2aa25ec13eb068f81fb714ca34bb7adc465a79e`，
  与委托值精确一致。
- Round 8 report SHA-256：
  `66109dbf84fa091d73b97accc1c0248e2308b31a2e0585133aec911117e770e3`，
  与委托值精确一致。
- 检查范围：live issue、三份规划与 schema 1.2 approval、完整 implementation
  handoff、Round 8 raw report、`origin/main...HEAD` 五个 work commits、当前完整 dirty
  diff、R1-R10、AC1-AC14、Docs SSOT、canonical/runtime/package/interface/schema/example/
  tests、五个 installed package roots、manifest、workflow/preset clean throwaway
  install/update/reapply、历史 plan/message/tree、安全、部署、workspace/staging/source/
  sidecar，以及 `PHASE2-R8-01` / `PHASE2-R8-02` 的独立攻击。
- 结论：`blocked`。发现 1 个 P1 当前范围 finding。现有 transaction 36/36、
  assignment/liveness 30/30、六 roots 24/24、full 522/522 和 clean throwaway 全绿，
  但没有覆盖 candidate result identity check 与 final live-index rename 之间的
  concurrent candidate atomic-replace 窗口。
- 操作边界：本代理只新增本 raw report；未修改实现、durable docs、旧 task artifact、
  assignment、旧 Phase 2/review、plan、ledger 或 planning docs；未运行 recorder、当前
  task commit executor、stage、commit、push、PR、finish-work、reset、revert、stash、
  amend、rebase 或 force。所有 executor 攻击均在自动清理的独立 throwaway Git repo 中。

## 输入与规范证据

- Live issue：`castbox/guru-trellis#122`，状态 `OPEN`，标题和 R1-R10/AC1-AC14 与 task
  一致；#92、#120 只作 related。
- Planning：完整读取 `prd.md`、`design.md`、`implement.md`、
  `planning-approval.json`；`check-planning-approval.sh` 返回 `status=ok`，schema 1.2、
  ambiguity review、fixed-scope scan、explicit post-planning confirmation 与三份文档
  digest 均匹配。
- Handoff：完整读取 1050 行 `implementation-handoff.md`，重点复核 Round 9 对
  publication linearization 与 assignment provenance recovery 的声明。
- Round 8：完整读取 304 行 `phase2-check-report-round-008-fix.md`，直接重放其两个 P1
  的并发窗口与 machine-gate 根因，不以实现代理摘要替代检查。
- Agent ledger：读取 schema 1.2 的全部 `event_corrections[]` / `recovery_links[]`、
  被修正事件、Round 7 failed/resume/termination/replacement/completed 链，以及检查期间
  新增的合法 liveness events。Live assignment digest 会随主会话 liveness 记录合法变化，
  因此 gate 使用 validator、target digest 和 effective projection，而不是派发时旧 digest。
- 官方 Trellis 文档：`https://docs.trytrellis.app/index.md`、
  `advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md`。当前实现仍由
  Markdown workflow/skill 拥有判断，companion 只执行确定性 Git/校验；canonical
  marketplace/preset 是安装恢复源头，没有修改 upstream、全局 npm 或 `node_modules`。
- 项目规范：完整读取 `trellis-check`、`trellis-before-dev`、`trellis-meta`，并读取适用的
  workflow、preset、docs、cross-layer、code-reuse 规范与 Trellis meta architecture/
  customize references。

## Findings

### PHASE2-R9-01（P1）：candidate identity check 到 final index rename 仍有未受 guard 约束的 TOCTOU，成功可缺失 committed result

- 位置：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:11343-11353`、
  `:11371-11430`；dogfood runtime 是 byte-equal installed copy。
- Durable contract：`.trellis/spec/workflow/data-contracts.md:440-455` 要求 candidate
  guard 覆盖 committed result publication，final live-index rename 是成功 linearization，
  成功时 real ref、commit tree、live index 与 candidate committed result 一致；
  `:468-470` 要求 concurrent candidate writer block，绝不替换 unowned candidate bytes。
  `.trellis/spec/workflow/quality-guidelines.md:171-176` 也要求 candidate contention 与
  positive four-way equality 的真实回归。
- 事实：executor 创建并持有 `<candidate>.lock`，发布 candidate result 后只在
  `:11423-11426` 做一次 inode/content identity check，随后在 `:11430` rename final
  index。该 `.lock` 只是旁路文件，不是 OS 强制锁；通用 `write_json()` 在
  `:3780-3789` 和 runtime 自身 `task_commit_atomic_replace_bytes()` 都通过临时文件
  `os.replace`，不会读取或遵守 candidate guard。因此另一个 writer 可以在最后一次
  identity check 后、index linearization 前替换 candidate。
- 独立真实 throwaway：检查代理 patch 仅把 writer 注入
  `task_commit_publish_locked_index()` 入口，即生产代码已经完成 candidate identity
  check、candidate/ref/index guards 仍存在且 final index 尚未 rename 的精确窗口。Writer
  使用 runtime 自身 atomic-replace helper 写入第三方 bytes C，再执行原 final index
  rename。结果为：

```text
candidate guard present: true
candidate C written before linearization: true
executor status / exit: committed / committed
real HEAD == returned commit: true
live index tree == commit tree: true
candidate bytes == committed result: false
candidate bytes == third-party C: true
candidate/index lock leaked: false / false
```

- 现有 `test_candidate_concurrent_writer_is_preserved_by_conditional_ownership`
  （runtime test `:1295-1327`）在 writer 写 C 后主动抛出 `OSError`，所以进入 rollback，
  没有覆盖 writer 正常返回且发生在最后一次 identity check 之后的 success-window race。
  `test_success_window_blocks_concurrent_git_add_and_linearizes_at_live_index`
  （`:1205-1293`）只证明真实 Git writer 遵守 `index.lock` / ref lock，并在成功后读取
  candidate；它没有在 check-to-rename 窗口注入 candidate writer。
- 影响：executor 可返回唯一 `committed` exit、发布真实 ref/index，却没有发布与该
  commit 对应的 task-local committed result。后续 metadata capture、fresh sequence、
  audit 和 recovery 看到的是第三方 candidate bytes，而返回 payload 声称事务完整成功。
  这违反 #122 R4、R7-R8、AC7-AC8、AC11，以及 Round 9 的 four-way publication
  linearization 合同。
- 修复要求：candidate ownership 必须真正覆盖最后一次 identity validation 到 final
  index linearization；所有 project/runtime candidate writer 必须共享可执行的 guard/
  conditional CAS 合同，或调整 publication/recovery 设计使 late writer 不能产生成功但
  candidate 不一致。新增永久回归：在 candidate identity 已通过、live index 尚未 rename
  时用正常返回的 atomic-replace writer 写 C；executor 必须 fail closed 且不得覆盖 C，
  或 writer 必须被 objective guard 阻断。成功回归必须在 linearization 时证明 candidate
  仍为 exact committed result，而不是只检查更早快照。
- 处理：本代理只记录 finding，不修改实现。

## `PHASE2-R8-01` 其余 publication 复核

| 场景 | 结论 | 独立证据 |
| --- | --- | --- |
| entry live `index.lock` | 通过 | Executor entry 持锁；candidate failure 和 success-window 的真实 `git add` 均非零，未覆盖 concurrent index。 |
| candidate publication failure | 通过 | 失败时 ref conditional rollback、candidate exact restore、live index entry preimage 保持，无 lock 泄漏。 |
| success-window `git add` | 通过 | `git add` 被 live index lock 阻断；success 后 real HEAD/tree/index 一致。 |
| index publication failure | 通过 | Candidate guard/ref guard 仍持有；candidate/ref 条件恢复，live index 未发布。 |
| concurrent ref before CAS | 通过 | Initial conditional `update-ref` 阻断，第三方 ref D 被保留。 |
| CAS -> ref-lock 窗口 | 通过 | 在 CAS 后、guard acquisition 前用真实 `update-ref` 发布 D；executor blocked，D、entry index、candidate preimage 全部保留，ref/index lock 均清理。 |
| concurrent ref after guard | 通过 | Guarded success window 的真实 `update-ref` 非零，不能覆盖 transaction ref。 |
| packed -> loose ref | 通过 | Packed-only branch preimage 成功 commit，CAS 后 loose ref/guard 正常工作，无 lock 泄漏。 |
| linked worktree ref path | 通过 | 当前 worktree `--git-dir` 位于 `.git/worktrees/...`，但 `--git-path refs/heads/...` 精确解析到 common `.git/refs/heads/...`。 |
| final index 后 fallible check | 通过 | 永久 success test 在 linearization 后让 index preimage checker 抛错，实际没有调用；成功路径 final rename 后只执行 best-effort cleanup/return。 |
| late candidate atomic writer | **失败** | `PHASE2-R9-01`：guard 存在但不约束 normal atomic replace，executor 错误 committed。 |

Ordinary tracked、symlink、delete、delete/recreate、rename、multiple paths、candidate self、
entry-index A/worktree B、Unicode/pathspec、gitlink A/B/C、uninitialized/dirty/unborn
gitlink、7-state operation/真实 cherry-pick、partial isolated cache、rejecting/benign/
content-mutating/mode-mutating/extra-path hook 和 unrelated-staged matrix 均在 36/36 中
通过。它们证明 artifact-authorized isolated index/commit 主体成立，但不能反证最后的
candidate success-window finding。

## `PHASE2-R8-02` assignment correction/recovery 复核

- Live `check-agent-assignment.sh --require-current-head` 返回 exit 0；检查期间 raw/effective
  事件计数随合法 liveness append 增长，但始终保持 `effective = raw - 3`。
- 三条 `event_corrections[]` 分别 digest-bound
  `evt-0132-2f8589a51e`、`evt-0135-1a8e9bee22`、`evt-0136-d400b5a1f4`，same-agent、
  `kind=invalidate-provenance`、`source=main-session`、HEAD/timestamp/reason/evidence 合法；
  effective projection 精确排除这三个误写 progress/status-request event，raw rows 保留。
- 主会话 correction reasons/evidence 具体：逐条说明实现代理误调用 recorder、错误的
  `source=main-session`、主会话时间线没有对应调用，并锚定 `evt-0141` 的独立审计；没有
  把 invalidated event 用于 pass。
- 一条 recovery link 双 digest 绑定 `evt-0117-fa1006d803` failed 到同一 Round 7 agent 的
  later `evt-0118-cd228c71fd` manual/platform termination；有效 traversal 为
  `evt-0115 failed -> evt-0116 resume -> evt-0117 failed -> linked evt-0118 termination ->
  evt-0120 replacement -> evt-0128 completed`，两个 failed rows 均关闭。
- 独立 live-copy 负向矩阵拒绝 unknown correction、duplicate correction id/target、tampered
  target digest、cross-agent correction、terminal invalidation、unknown/duplicate recovery、
  tampered failed digest、cross-agent recovery、backward edge、cycle edge；移除 repair 并降为
  legacy 1.1 后仍同时因 schema 与两个 incomplete recovery rows fail closed。
- `phase2_agent_assignment_errors()` 对当前 live ledger 返回 `[]`；assignment/liveness
  targeted suite 30/30。`PHASE2-R8-02` closed，没有新 assignment finding。

## R1-R10 / AC1-AC14

| 范围 | 结论 | 证据或阻断 |
| --- | --- | --- |
| R1 / AC1 | 通过 | Registry 保留 `guru-create-work-commit` reserved tombstone，激活 `guru-create-task-commit`；public API/manifest 一致。 |
| R2 / AC2 | 通过 | Canonical/dogfood 各 1 mandatory invoke、3 unique exits；finding repeat route 唯一。 |
| R3 / AC5 | 通过 | Planning、Phase 2 inputs、ledger/HEAD/snapshot/message negative matrix 与 assignment repair gate 通过。 |
| R4 / AC3-AC4 | 通过 | Standalone triggers、task-local artifact、candidate mode/empty range、sensitive boundary 通过。 |
| R5 / AC6 | 通过 | Exact artifact path/index、unrelated preservation、literal path 和 live index lock 通过。 |
| R6 | 通过 | AI scope/message/authorization/human owner 保持在 Markdown；runtime 只验证事实。 |
| R7-R8 / AC7 | **阻断** | Shared parser、parent/message/path/tree/blob/mode/index 通过，但 late candidate writer 可导致 committed exit 没有 committed result。 |
| R2/R8 / AC8 | **阻断** | 001-005 fresh sequence/history 均正确；但当前 success-window 可破坏 result evidence，不能保证下一 sequence 的可靠输入。 |
| R9 / AC9 | 通过 | Workflow/platform route-only，canonical package reference 独占 step-local contract，无第二 parser/direct task work commit。 |
| R10 / AC10 | 通过 | Canonical/runtime/package、五 installed roots、manifest、installer/update/reapply 无漂移。 |
| R10 / AC11 | **阻断** | 36/30/24/522、throwaway、validators 全绿，但缺 `PHASE2-R9-01` late-writer regression。 |
| AC12 | 按合同 pending | Remote exact feature-ref verifier 只能在 reviewed content push 后生成；当前 pending 不满足 publish。 |
| AC13 | 通过 | `close_issues=[122]`；#92、#120 仅 related；5 个 history messages 只使用 `Refs #122`。 |
| AC14 | 通过 | Public non-task added-line 与 5 plans 高置信敏感扫描为 0。 |

## Docs SSOT

- Approved strategy 为 `ssot_first`，docs state=`partial_docs`。顶层 README、三份
  requirements、workflow README、五份 workflow specs 与 canonical package contract/
  interface/schema/example 已同步 Round 9 的 index/ref/candidate guard 设计；runtime/test 与
  installed copies byte-equal。
- Preset installer、overlay guidelines、public docs 与 preset README 的 no-byte-change
  成立：本轮没有改变 managed path、platform route 或安装命令；clean throwaway 已覆盖
  install/update/workflow reapply/preset reapply。
- `PHASE2-R9-01` 证明 durable docs 的 candidate guard、concurrent candidate writer 和
  success four-way equality 声明强于真实可达行为。该 current-scope Docs SSOT 不一致不能
  降级为 observation；修复时必须先收敛 data/companion/quality/package contract，再同步
  runtime/tests/installed copies。
- Assignment schema 1.2 contract 与 runtime/recorder/validator/tests/live ledger 一致；没有
  把 active task correction/recovery rows放入公共 package。

## 分发、历史与验证结果

| 检查 | 结果 |
| --- | --- |
| Planning / workspace / task | Planning approval、workspace boundary、task validate、phase 2.2/3.4/3.5 parse 全部通过。 |
| Transaction matrix | `36/36`，30.523s，`OK`；独立 late-candidate probe 仍复现 finding。 |
| Assignment/liveness | `30/30`，1.339s，`OK`；live validator 与 Phase 2 assignment consumer 均通过。 |
| 六个 package roots | Canonical + `.trellis`/shared/Claude/Codex/Cursor 各 `4/4`，合计 `24/24`。 |
| Full suite | Canonical package + skill/runtime/preset 单次集合 `522/522`，151.834s，`OK`。 |
| Clean throwaway | Exit 0；public discovery + local unpublished sample、fresh install、initial/finding-fix commit、old-plan reject、`trellis update --force`、workflow preview/switch/reapply、preset reapply、source/installed、drift、update 前后 closeout、recursive sidecar 全通过。 |
| Source/installed validator | 均 passed；reserved=1、active=1、invoke=1、exit=3；Claude/Codex/Cursor managed=43，conflict/removal/sidecar=0。 |
| Canonical/installed equality | Workflow/runtime byte-equal；canonical package 到五 installed roots exact compare 无差异。 |
| Dogfood drift | `check-dogfood-overlay-drift.sh --repo .` passed。 |
| Runtime/package/manifest hashes | 与 handoff 列出的 runtime、test、八 package assets、canonical/installed manifest SHA-256 全部一致。 |
| History messages | `origin/main..HEAD` 5/5 shared parser `errors=[]`，均为 issue-bearing Chinese work messages。 |
| History plans/tree | Sequence 001-005 commit/parent/message/path 5/5；sequence 002-005 的 75/75 blob/mode rows 与真实 commit tree 一致；001 是 tree-evidence contract 前的历史 plan。 |
| JSON / syntax / diff | Branch+untracked union 39 JSON parse、12 Python AST parse、15 Bash syntax、branch/dirty/cached `git diff --check` 全通过。 |
| Official boundary | 未修改 upstream/global npm/node_modules；marketplace/preset/canonical/dogfood 分层符合官方文档。 |

## 安全、部署与工作区卫生

- Public non-task added-line 扫描未命中 private key、GitHub/AWS/Slack token、credential
  URL、signed URL marker、secret query/assignment 或机器用户绝对路径。
- 五个 task commit plans 同类扫描为 0；public artifact 不保存 dirty file body、operation
  marker 内容、secret、客户数据或本机绝对路径。
- Branch+dirty union 没有 GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、
  Helm/chart、database migration 或 Makefile 变更。本任务只改变 Trellis workflow/
  preset/runtime/package/docs/tests，不新增 service、worker、queue、runtime config 或
  migration，无需应用部署资产同步。
- 报告写入前：55 tracked modified + 19 untracked files，0 staged。报告写入后预期只新增
  本报告，即 55 tracked modified + 20 untracked files，0 staged。
- Recursive `.new/.bak=0`；task candidate/ref/live-index locks=0；executor transaction/
  message 临时文件由 throwaway teardown 清理。
- Source checkout clean；没有 `.trellis/workspace/**`、`.trellis/.runtime/**`、`.env`、
  `node_modules/**` 或 source misplaced task artifact 进入 diff。

## 观察项

1. Remote exact feature-ref marketplace verifier 继续按合同 pending；本报告不把 local
   mutable workflow sample 或 clean throwaway 冒充 remote reviewed-ref evidence。
2. Compatibility target 仍为 Trellis CLI `0.6.5`；本任务未授权扩大 baseline。
3. Live assignment digest 在检查期间因主会话合法 liveness/status-request append 更新；
   correction target digests 与 effective projection 未漂移，validator 保持通过。

## 后续候选

无。`PHASE2-R9-01` 直接位于 #122 已批准的 candidate concurrent writer、transaction
publication、post-commit result 与 AC7/AC8/AC11 范围，不能拆到 follow-up 后放行当前任务。

## 最终结论

- `findings_count: 1`。
- 优先级：P0=0、P1=1、P2=0、P3=0。
- `PHASE2-R9-01`: open。
- `PHASE2-R8-01`: index/ref 部分 closed；candidate late-writer success window 未 closed。
- `PHASE2-R8-02`: closed。
- `F-06-01`、`F-06-02` / `PHASE2-R6-01`、`F-06-03`: closed。
- `PHASE2-R7-01`: artifact-authorized isolated staging/commit closed；最终 publication 仍被
  `PHASE2-R9-01` 阻断。
- Phase 2：`blocked`。
- 下一步必须返回 implementation，修复 candidate identity-check 到 final index
  linearization 的 concurrent writer ownership，补永久 late-writer regression，并重新同步
  Docs SSOT/runtime/tests/installed copies。完成新的 fresh Phase 2 后才能创建 sequence 006
  或更高 plan；不得复用旧 Phase 2、sequence 001-005、旧授权或现有 Branch Review Gate。
