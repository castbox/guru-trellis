# #122 第十轮修复后 replacement 独立 Phase 2 检查报告

## 身份、边界与结论摘要

- 逻辑角色：`阶段二检查代理`。
- 技术身份：`trellis_check_122_round10_replacement`。
- 平台昵称：`Check-Agent-122-Round10-Replacement`。
- 固定 worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`。
- Task：`.trellis/tasks/07-13-122-guru-create-task-commit`。
- Base：`origin/main=6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Pre-commit HEAD：`163e64168d5d9783c32665da92aebbb4397564a3`；检查与报告写入前后均未改变。
- Source checkout：`/Users/wumengye/Documents/GoProjects/guru-trellis`，
  `main@6b9495a17dc953c7a54c105e39c23a786edcd8a7`，检查期间 clean。
- Implementation handoff SHA-256：
  `71a34a134c093aacef6c0431fa3315290c5f4014cfe654817f936d4971184ca9`，
  与委托值精确一致；完整读取 1180 行。
- Round 9 report SHA-256：
  `0e6225e1280bdb123569e5feed766acb7de5cff8b30a5282af23d681f1caba1b`，
  与委托值精确一致；完整读取 259 行。
- Predecessor `trellis_check_122_round10_fix` 因 provider 401 在开始检查前失败，
  没有 raw report 或可消费结论。本 replacement 从 live 文件独立检查，没有复用其
  会话、partial output 或 pass 断言。
- 检查范围：live issue、三份规划与 schema 1.2 approval、完整 handoff、Round 9 raw
  report、完整 assignment、`origin/main...HEAD` 五个 work commits、当前完整 dirty diff、
  R1-R10、AC1-AC14、Docs SSOT、canonical/runtime/package/schema/tests、五个 installed
  roots、manifest、workflow/preset throwaway install/update/reapply、历史 plan/tree、
  安全、部署、workspace/staging/source/sidecar，以及 `PHASE2-R9-01` 的两个独立真实
  Git 并发窗口。
- AI Phase 2 结论：`pass`，`findings_count=0`。`PHASE2-R9-01` 已关闭；没有 P0/P1/P2/P3
  current-scope finding。
- Assignment consumer gate：主会话已追加 digest-bound recovery
  `rec-0002-d8e8fb7c67`，连接 `evt-0174-7898a0712f failed` 到
  `evt-0175-a608825d7a terminated-unfinished`。本报告回传前 live validator 仍按设计因
  当前 replacement 尚无 `completed` terminal row 返回 exit 2；主会话必须在本报告和
  本代理完成回传后记录 `completed` 并重新运行 live validator，只有最终 exit 0 才能
  消费本报告或运行 Phase 2 recorder。该 recorder 后置步骤不由本检查代理冒充已发生。
- 操作边界：本代理只新增本 raw report；未修改实现、durable docs、assignment、旧
  Phase 2/review、plan、ledger 或 planning docs；未运行 recorder、当前 task commit
  executor、stage、commit、push、PR、finish-work、reset、revert、stash、amend、rebase
  或 force。所有 executor 攻击都在自动清理的独立 throwaway Git repo 中。

## 输入、规划与官方边界

- Live issue：`castbox/guru-trellis#122`，状态 `OPEN`；R1-R10、AC1-AC14、范围外项和
  task 规划一致。`close_issues=[122]`；#92、#120 仅 related。
- Planning：完整读取 `prd.md`、`design.md`、`implement.md` 与
  `planning-approval.json`。`check-planning-approval.sh` 返回 `status=ok`；schema 1.2、
  ambiguity review、fixed-scope scanner、`explicit-post-planning-review` 与三份文档
  digest 均匹配。
- Workspace：`check-workspace-boundary.sh` 返回 `status=ok`，expected/actual worktree
  精确相等，source status 和 suspicious source artifacts 为空。Task validate 通过。
- Assignment：完整读取 schema 1.2 的 25 个 agent、全部 raw status history、3 条
  `event_corrections[]`、2 条 `recovery_links[]`、6 个 review rounds 和 4 个 reuse
  decisions；Round 8 三条 provenance correction 和 Round 7 / Round 10 两条
  failed-to-termination edge 都保持 append-only、digest-bound、same-agent。
- 项目技能与规范：完整读取 `trellis-check`、`trellis-before-dev`、`trellis-meta`，以及
 适用 workflow、preset、docs、cross-layer、code-reuse spec 和 meta architecture/
  customize references。
- 官方文档：重新读取 `https://docs.trytrellis.app/index.md`、
  `advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md`。当前实现
  仍由 Markdown workflow/skill 拥有流程与 AI 判断，companion 只校验/执行确定性 Git
  事实；canonical marketplace/preset 是恢复源头，没有修改 upstream、全局 npm 或
  `node_modules`。

## `PHASE2-R9-01` 独立关闭证据

### 生产实现审查

- `task_commit_acquire_index_lock()` 从 executor entry 创建真实 `index.lock`；该 fd/path
  在 publication、rollback 和 cleanup 前持续持有。
- `task_commit_publish_validated_transaction()` 不再把 `index.lock` rename 成 live index。
  Final index bytes 写入同目录独立 `.<index>.*.publication` temp，再在 sentinel 仍存在时
  `os.replace()` 到 live index。
- Candidate committed result 先发布，branch ref conditional advance 后立即取得并复核
  loose-ref guard，final index 随后发布。Runtime 再验证 open index/ref guards、real ref、
  live index inode/content 和 candidate guard。
- 最后一次 `task_commit_file_matches_identity(candidate_path, committed-result identity,
  bytes)` 是 success linearization point。它之后没有 success-to-blocked 的 fallible check
  或 publication write；只剩 best-effort fd/guard/temp cleanup 和预构造 payload return。
- Success payload 在 publication 前构造并绑定 `candidate_result_sha256`；immutable commit
  tree 中 candidate path 的 planned blob 与 committed-result bytes digest 是成功后的
  authority。合同没有声称任意后续 mutable candidate file 永久与 result 相等。

### 独立真实窗口一：pre-read writer C

检查代理在全新临时 Git repo 中使用 production executor，并只在 production
`task_commit_publish_locked_index()` 入口注入正常返回的 atomic writer：

- Candidate guard 和真实 `index.lock` sentinel 都已存在；writer 不靠主动抛错进入失败。
- 同窗口执行真实 `git add src/task.txt` 返回非零，证明 sentinel 在 index publish/
  rollback 全程阻断 Git writer。
- Writer 使用 production `task_commit_atomic_replace_bytes()` 把 candidate 替换为 C，
  然后原 final-index publish 正常完成。
- Final candidate identity read 检出 C；executor 返回 `blocked`。
- Real branch ref compare-and-swap 回到 entry HEAD，live index 恢复 entry preimage；C 原样
  保留，没有被 planned/result preimage 覆盖。
- Candidate/ref/index guards 和 candidate/index publication temps 全部清理，泄漏数为 0。

该窗口关闭 Round 9 原始复现：C 不再能在 final index publish 附近导致
`committed` 但 candidate result 缺失。

### 独立真实窗口二：post-read writer C

第二个全新临时 Git repo 在 final candidate identity read 已成功读取 exact committed
result 后立即用 production atomic replace 写 C：

- Final read 时 candidate guard、ref guard 和 `index.lock` sentinel 均存在；同窗口真实
  `git add` 返回非零。
- Writer C 被保留为 later operation；executor 仍返回
  `status=committed / exit=committed`，不会把已经线性化的成功追溯改成 blocked。
- Real branch ref 等于 returned commit，live index tree 等于 immutable commit tree。
- Commit tree 中 candidate path blob 精确等于 pre-commit planned artifact bytes，mode 为
  `100644`；C 没有进入 commit。
- Returned `candidate_result_sha256` 精确等于 final read 读取的 committed-result bytes
  digest；result 中 `commit_sha` 等于 payload commit。
- 注入一个“linearization 后调用即抛错”的旧 index-preimage checker，执行过程中没有
  命中，证明 final read 后不存在 late fallible success check。
- Candidate/ref/index guards 与 publication temps 全部清理，泄漏数为 0。

### 永久回归

- `test_candidate_writer_before_final_identity_read_rolls_back_and_is_preserved` 固化
  pre-read normal-return C、真实 `git add`、owned ref/index rollback、C preservation 和
  cleanup。
- `test_success_window_blocks_git_writers_and_linearizes_at_final_candidate_read` 固化
  post-read C later-op、ref/tree/index equality、planned candidate blob、result digest 和
  no-late-fallible-check。
- Transaction suite 保持 `36/36`，没有靠删除 ordinary/gitlink/operation/hook/
  publication case 降低覆盖率。

## 既有 finding 与非回归

| 范围 | 结论 | 独立证据 |
| --- | --- | --- |
| F-06-01 operation/sequencer | closed | 7-state marker 与真实 conflict cherry-pick 保持 fail closed，candidate/HEAD/index/marker 不被消费。 |
| F-06-02 / PHASE2-R6-01 gitlink | closed | A/B/C、uninitialized/dirty/unborn、artifact OID exact-index authority 与 B-to-C window 保持通过。 |
| F-06-03 workflow SSOT | closed | Canonical/dogfood workflow byte-equal；global route 无 work message template、direct task work commit 或第二 parser。 |
| PHASE2-R7-01 ordinary authority | closed | tracked、symlink、delete、rename、multi、candidate-self、entry-index A/worktree B、Unicode/pathspec、partial cache 与 hook matrix 保持通过。 |
| PHASE2-R8-01 publication | closed | candidate/index failure、CAS 前/后 ref contention、loose-ref guard、packed/linked worktree ref、real `git add`、conditional rollback、final equality 均通过；本轮补齐最后 candidate window。 |
| PHASE2-R8-02 assignment | closed | 3 corrections、2 recovery links、live-copy negative matrix 与 30/30 suite 证明 unknown/duplicate/tampered/cross-agent/backward/cycle fail closed。 |
| PHASE2-R9-01 candidate TOCTOU | closed | 两个独立真实窗口和两条永久回归证明 final read 前 C blocked/rollback/preserve，read 后 C later-op/committed。 |

## R1-R10 / AC1-AC14

| 范围 | 结论 | 证据 |
| --- | --- | --- |
| R1 / AC1 | 通过 | Registry 保留 `guru-create-work-commit` reserved tombstone，激活 `guru-create-task-commit`；public API/manifest 一致。 |
| R2 / AC2 | 通过 | Canonical/dogfood 各 1 个 mandatory invoke、3 个 unique exits；finding-fix repeat route 唯一。 |
| R3 / AC5 | 通过 | Planning、Phase 2/ledger/HEAD/snapshot/message、operation 与 assignment repair negative gates 覆盖。 |
| R4 / AC3-AC4 | 通过 | Standalone triggers、task-local sequence artifact、candidate mode/empty range、sensitive boundary 通过。 |
| R5 / AC6 | 通过 | Artifact-authorized exact index、unrelated preservation、literal paths、sentinel 与 conditional rollback 通过。 |
| R6 | 通过 | Scope/message/authorization/human confirmation/route 判断仍在 Markdown；runtime 只验证事实。 |
| R7-R8 / AC7 | 通过 | Shared parser、parent/message/path/tree/blob/mode/ref/index/result 全部匹配；pre/post-read C 语义成立。 |
| R2/R8 / AC8 | 通过 | Sequence 001-005 历史 fresh chain 正确；新 commit 仍要求 sequence 006+、fresh Phase 2/HEAD/snapshot/authorization。 |
| R9 / AC9 | 通过 | Step-local contract 只在 canonical package reference；workflow/platform route-only，无第二 parser/direct task work commit。 |
| R10 / AC10 | 通过 | Canonical/runtime/package、五 installed roots、manifest、installer/update/reapply 无漂移。 |
| R10 / AC11 | 通过 | 36/30/24/522、两个独立窗口、throwaway、validators、static/history 全绿。 |
| AC12 | 按合同 pending | Remote exact feature-ref verifier 只能在 reviewed content push 后由 `trellis-finish-work` 生成；当前 pending 不满足 publish，但不伪装成本地 Phase 2 失败。 |
| AC13 | 通过 | `close_issues=[122]`；#92、#120 仅 related；5 个 history messages 只使用 `Refs #122` 语义。 |
| AC14 | 通过 | Public non-task added-line与 5 个 plans 高置信敏感扫描 0 命中。 |

## Docs SSOT

- Approved strategy=`ssot_first`，docs state=`partial_docs`。顶层 README、三份
  requirements、workflow README、五份 workflow specs 与 canonical package
  contract/interface/schema/example 均一致声明：`index.lock` 是持有到事务结束的
  sentinel；final index 使用独立 temp；final candidate identity read 是成功线性化点；
  read 前 C rollback/preserve，read 后 C 是 later operation；commit blob/result digest
  是 immutable authority。
- 全局 workflow 只保留 mandatory invocation、finding repeat、typed exits 和 fail-closed
  transition；candidate/review/confirmation/executor/postcondition 没有回流到 workflow 或
  platform entry。
- Preset installer、overlay guidelines、public docs 与 preset README 的 no-byte-change 理由
  成立：Round 10 没有改变 managed path、installer 算法、platform route 或公共安装命令；
  clean throwaway 已覆盖 install/update/workflow reapply/preset reapply。
- Active task correction/recovery rows、401 channel 事实、单次测试输出、临时 Git SHA 和
  本报告保持 task-history-only，没有进入公共 package。
- 未发现 durable docs、task planning、runtime、schema、tests 或 installed copies 间的
  语义漂移。

## 验证结果

| 检查 | 结果 |
| --- | --- |
| 独立 pre/post-read C probes | 2/2 通过；真实 Git repo、真实 `git add`、production executor、ref/index/candidate/result assertions 全部成立。 |
| Transaction matrix | `TaskCommitCandidateExecutorTest`：`36/36`，29.942s，`OK`。 |
| Assignment/liveness | `AgentAssignmentArtifactTest + SubagentLivenessStateMachineTest`：`30/30`，1.358s，`OK`。 |
| 六 package roots | Canonical + `.trellis`/shared/Claude/Codex/Cursor 各 `4/4`，合计 `24/24`。 |
| Full suite | Canonical package + skill/runtime/preset：`522/522`，154.163s，`OK`。 |
| Clean throwaway | Exit 0；public discovery + local unpublished sample、fresh workflow/preset install、initial/finding-fix task commit、old-plan reject、`trellis update --force`、workflow preview/switch/reapply、preset reapply、source/installed、drift、update 前后两次 closeout、archive/ready equality、recursive sidecar 全通过。 |
| Source/installed | 均 `passed`；reserved=1、active=1、invoke=1、exit=3；dogfood Claude/Codex/Cursor managed=43，conflict/removal/sidecar=0。 |
| Canonical equality | Workflow/runtime 2 对 byte-equal；canonical package 8 assets 到五 roots 共 40 次 exact compare 无差异。 |
| Dogfood drift | `check-dogfood-overlay-drift.sh --repo .` passed。 |
| Runtime/package hashes | Runtime=`21f097...3379`、runtime test=`12ad21...624c`；interface/contract/schema/example/test、canonical/installed manifests 与 handoff 精确一致。 |
| History messages | `origin/main..HEAD` 5/5 shared parser `errors=[]`，均为 issue-bearing Chinese work messages。 |
| History plans/tree | Sequence 001-005 parent/message/path 5/5；sequence 002-005 的 75/75 blob/mode rows 与真实 commit tree 一致。 |
| Static | Branch+dirty+untracked union 39 JSON parse、12 Python compile、15 Bash syntax；branch/working/cached `git diff --check` 全通过。 |
| Workflow parsing | Phase index、2.2、3.4、3.5 均可读取；task validate、workspace、planning 均通过。 |

## Assignment live gate 的终态边界

- `rec-0002-d8e8fb7c67` 的 failed/termination target SHA-256 分别为
  `f9c3d93174baca601973cc0f7c46550edba0a36c581b220ee17738fddc787e79` 和
  `9f20dc9ef1b6c20b95ad7d721db26d60b00619f6b852c7234f80d5c03efe0d9a`；kind、same-agent、
  forward edge、reason/evidence 与 channel seq5/6/7、evt-0178/0179 replacement chain
  一致。
- 本报告写入时 assignment 有 3 corrections、2 recovery links，Round 10 failed row 已有
  正确 recovery edge，但 replacement 仍是正在运行的本代理，因此 live validator 正确
  报告 failed/terminated chain 尚未到 later `completed`。
- 这不是可由检查代理写入的 finding fix。主会话必须在收到本报告和完成回传后，用
  `record-subagent-liveness-event.sh` 记录本 technical `agent_id` 的真实 `completed`，再运行
  `check-agent-assignment.sh --require-current-head`。只有 `errors=[] / exit 0` 后，才能运行
  `record-phase2-check` 或把本报告作为通过证据。
- 若主会话未记录 completed、记录了错误 agent/head/provenance，或最终 validator 非零，
  则 workflow 必须 fail closed；本报告的 AI 语义结论不能绕过该 deterministic consumer
  gate。

## 安全、部署与工作区卫生

- Public non-task added-line 扫描 14927 行，private key、GitHub/AWS/Slack token、
  credential URL、signed URL marker 和机器用户绝对路径均 0 命中。
- 五个 task commit plans 同类扫描均为 0；公共 artifact 不保存 dirty file body、Git
  operation marker 内容、secret、客户数据或本机绝对路径。
- Branch+dirty union 没有 GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、
  Helm/chart、database migration 或 Makefile 变更。本任务只改变 Trellis workflow/
  runtime/package/docs/tests，不新增 service、worker、queue、scheduler、runtime config
  或 migration，无需应用部署资产同步。
- 报告写入前：55 tracked modified + 20 untracked files，0 staged。报告写入后预期只新增
  本报告，即 55 tracked modified + 21 untracked files，0 staged。
- Recursive `.new/.bak=0`；task candidate/ref/live-index locks 和 publication/transaction
  temps=0；throwaway 自动清理。
- Source checkout clean；没有 `.trellis/workspace/**`、`.trellis/.runtime/**`、`.env`、
  `node_modules/**` 或 source misplaced task artifact 进入 diff。

## 观察项

1. Remote exact feature-ref marketplace verifier 继续按合同 pending；local throwaway 不
   冒充 reviewed remote-ref publish evidence。
2. Compatibility target 仍为 Trellis CLI `0.6.5`；本任务未授权扩大 baseline。
3. Live assignment digest 在检查期间因主会话合法 progress/recovery append 变化；所有
   correction/recovery target digests 和 effective projection 语义未漂移。最终 terminal
   validator 必须使用主会话记录 completed 后的最新 artifact，而不是本报告中的中间 hash。

## 后续候选

无。Round 10 没有发现需要拆分的新问题；remote verifier 属于已声明的 publish-time gate，
不是 follow-up issue。

## 最终结论

- `findings_count: 0`。
- 优先级：P0=0、P1=0、P2=0、P3=0。
- `PHASE2-R9-01`: closed。
- `PHASE2-R8-01`: closed。
- `PHASE2-R8-02`: closed。
- `F-06-01`、`F-06-02 / PHASE2-R6-01`、`F-06-03`: closed。
- `PHASE2-R7-01`: closed。
- AI Phase 2：`pass`。
- Consumer 前置条件：主会话记录本 replacement `completed` 并使 live
  `check-agent-assignment --require-current-head` 最终 exit 0；在此之前不得运行 recorder、
  创建 sequence 006+、task commit、Branch Review 或 publish。
- Consumer gate 通过后，下一步可由主会话记录/验证 fresh Phase 2，再创建 sequence 006
  或更高 candidate；不得复用旧 Phase 2、sequence 001-005、旧授权或旧 Branch Review
  Gate。
