# #122 第八轮修复后独立 Phase 2 检查报告

## 身份、边界与结论摘要

- 逻辑角色：`阶段二检查代理`。
- 技术身份：`trellis_check_122_round8_fix`。
- 平台昵称：`Check-Agent-122-Round8-Fix`。
- 固定 worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`。
- Task：`.trellis/tasks/07-13-122-guru-create-task-commit`。
- Base：`origin/main=6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Pre-commit HEAD：`163e64168d5d9783c32665da92aebbb4397564a3`，检查与报告写入前后均未改变。
- Source checkout：`/Users/wumengye/Documents/GoProjects/guru-trellis`，HEAD 为
  `6b9495a17dc953c7a54c105e39c23a786edcd8a7`，检查前后 clean。
- Round 8 handoff SHA-256：
  `708376a109229467bd11ce1c4d411eed6a8b12718b6c30ace2ded8cd2b630b33`，
  与委托值精确一致。
- 检查范围：live issue、规划与批准、完整 implementation handoff、Round 6/7 raw
  Phase 2 reports、完整 `origin/main...HEAD` 与当前 dirty diff、R1-R10、AC1-AC14、
  Docs SSOT、canonical/runtime/package/schema/interface/example/tests、五个 installed
  package roots、manifest、workflow/preset throwaway install/update/reapply、历史 commit/
  plan/tree evidence、安全、部署、workspace/staging/source/sidecar，以及 Round 8
  artifact-authorized isolated transaction 的独立攻击。
- 结论：`blocked`。发现 2 个 P1 当前范围 finding。现有 32/32、24/24、514/514、
  source/installed validator 与 clean throwaway 全绿，但它们没有覆盖 candidate
  publication 失败时 index lock 已释放后的并发 index 写入；当前
  `agent-assignment.json` 也不能通过自己的 deterministic validator。
- 操作边界：本代理只新增本 raw report；未修改实现、durable docs、旧 task artifact、
  旧 report、旧 plan、ledger 或 recorder artifact；未运行任何 recorder、当前任务的
  task commit executor、stage、commit、push、PR、finish-work、reset、revert、stash、
  amend、rebase 或 force。所有 executor 攻击均在自动清理的独立 throwaway Git repo 中。

## 输入证据

- Live issue：`castbox/guru-trellis#122`，状态 `OPEN`，标题与 task 一致。
- 规划与批准：完整读取 `prd.md`、`design.md`、`implement.md` 和
  `planning-approval.json`；`check-planning-approval.sh` 返回 `status=ok`，schema 1.2、
  `ambiguity_review`、explicit post-planning confirmation 与三份文档 digest 均匹配。
- 实现交接：完整读取 933 行 `implementation-handoff.md`；Round 8 章节声明 ordinary
  exact paths、candidate self、isolated index/detached HEAD、conditional ref/index/result
  publication 与 rollback。
- 前轮证据：完整读取 `phase2-check-report-round-006-fix.md` 与
  `phase2-check-report-round-007-fix.md`。Round 6 operation/gitlink/workflow closure 和
  Round 7 `PHASE2-R7-01` 的 ordinary/candidate/live-index 根因均纳入复核。
- Agent ledger：逐条读取 `evt-0132-2f8589a51e`、`evt-0135-1a8e9bee22`、
  `evt-0136-d400b5a1f4`、`evt-0141-26f89458ed`、`evt-0142-fd239c40e8`，并读取 Round 7
  failed/resume/terminated/replacement/completed 链。
- 官方 Trellis 文档：`https://docs.trytrellis.app/index.md`、
  `advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md`。当前实现仍
  使用 Markdown workflow/skill 作为流程判断 owner，companion 只执行确定性 Git/校验，
  canonical marketplace/preset 是安装和恢复源头，没有修改 upstream、全局 npm 或
  `node_modules`。
- 项目规范：完整读取 `trellis-check`、`trellis-before-dev`、`trellis-meta`，以及适用的
  workflow、preset、docs、cross-layer 和 code-reuse 规范。

## Findings

### PHASE2-R8-01（P1）：candidate publication 前已释放 index lock，失败 rollback 会覆盖并发 index，成功也可返回 live-index/commit 不一致

- 位置：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:10866-10935`、
  `:11157-11201`；dogfood runtime 是其 byte-equal installed copy。
- Durable contract：`.trellis/spec/workflow/data-contracts.md:438-476` 要求 real
  branch/index/candidate 作为一个 recoverable transaction 发布；publication failure
  必须恢复 exact preimages；成功时 real branch、commit tree、live index 与 candidate
  committed result 必须一致。
- 事实：executor 先创建并持有真实 `<git-index>.lock`，预写 final index/result，再
  conditional `update-ref`。但 publication 顺序随后为：

```text
conditional update-ref
  -> os.replace(index.lock, live-index)  # index lock 在这里释放
  -> os.replace(candidate.lock, candidate)
```

- `candidate` publication 仍是可失败操作。它失败时，rollback 通过
  `task_commit_restore_index_preimage()` 的另一临时文件无条件 `os.replace(...,
  live-index)`；此时不再持有 `index.lock`，也没有比较 live index 是否仍为本 transaction
  刚发布的 final bytes。因此正常 Git 进程可在两次 replace 之间取得新的 `index.lock`
  并写入 C，而 rollback 会静默覆盖 C。
- 独立失败复现：throwaway 中 entry index=A，reviewed task bytes=B。检查代理在
  candidate replace 失败前用真实 `git add` 写入另一个 tracked path 的 index C；该命令
  exit 0。Executor 随后返回 blocked，并声称
  `Task commit publication failed and the exact entry state was restored.`。实际结果：

```text
real HEAD restored to entry preimage: true
candidate restored to entry preimage: true
live index restored to A: true
concurrent index C preserved: false
index.lock / candidate.lock leaked: false
```

- 这不是“恢复 exact entry state”的充分结论：C 是 transaction 释放 lock 后合法出现的
  并发 live-index preimage，rollback 把它当成本 invocation 污染并覆盖，造成 staged state
  数据丢失。
- 独立成功复现：同一窗口不注入 candidate failure，只在 candidate replace 前真实
  `git add` 写入 C。Executor 返回 `status=committed` / `exit=committed`，真实 HEAD 和
  candidate result 都是 committed，但 `final_live_index_blob != commit_tree_blob`。
  这直接违反 public Success index 与 positive publication 合同。
- 对照：独立 concurrent-ref probe 在 conditional `update-ref` 前把 branch 从 A 改为 D；
  executor 能阻断，保留外部 D，不覆盖 D，index/candidate/operation preimage 均保持。Ref
  compare-and-swap 正确，缺口仅在没有同等级 conditional ownership 的 index publication/
  rollback。
- 现有永久 tests 只有
  `test_index_publication_failure_rolls_back_real_ref_index_and_candidate`；它让 index
  rename 本身失败，此时原 `index.lock` 仍在，不会进入上述窗口。没有 candidate
  publication failure、index publish 后并发写入或 success-return live-index equality
  回归，因此 32/32 无法反证本 finding。
- 影响：并行用户/进程的 staged 状态可被 rollback 丢失；另一分支会错误返回
  `committed`，但 live index 已不等于它声称发布的 validated commit tree。它违反 #122
  R5、R7-R8、AC6-AC7、AC11 和 Round 8 的 conditional publication/rollback 目标。
- 修复要求：真实 index ownership 必须覆盖完整 ref/index/candidate publication 与所有
  rollback 写入，或为 index 建立不会覆盖第三方状态的 conditional compare-and-swap/
  recovery 合同。Candidate publication failure 必须证明 concurrent index C 不被覆盖；
  success 必须在返回前由 publication 原子性本身保证 real ref/tree/live index/candidate
  result 一致，而不是在真实 success 后增加一个可能返回 blocked 的 fallible check。增加
  candidate-publication failure、index-published concurrent write 和 final success equality
  永久回归。
- 处理：本代理按 Phase 2 边界只记录 finding，不修改实现。

### PHASE2-R8-02（P1）：agent-assignment 不是有效 gate artifact，plain-text provenance 校正只能做人类披露

- 位置：
  `.trellis/tasks/07-13-122-guru-create-task-commit/agent-assignment.json` 的
  `evt-0115-af56c79ab7`、`evt-0117-fa1006d803`、`evt-0132-2f8589a51e`、
  `evt-0135-1a8e9bee22`、`evt-0136-d400b5a1f4`、`evt-0141-26f89458ed`、
  `evt-0142-fd239c40e8`；validator 入口为
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:6410-6521`、
  `:7339-7358`。
- Provenance 判断：`evt-0132/0135/0136` 的 `source=main-session` 不成立。`evt-0141`
  逐一列出三个错误 event id，明确它们“不得作为主会话观察或 gate pass 证据”，并且
  `evt-0142` 只记录主会话独立核对过的 handoff SHA、HEAD/staging/source/sidecar 终态。
  该 append-only 记录足以作为人类审计披露；本检查没有把三个误写事件用于任何 pass
  结论。
- 但它不足以恢复 machine gate：schema/taxonomy 没有 correction/supersedes/invalidates
  关系，三个旧 event 的 `source` 字段仍为错误值，progress/status projection 仍会把它们
  当 active liveness event。`evt-0141.evidence` 的自然语言不能让 deterministic consumer
  自动排除旧事件。因此它不能把错误 provenance 重新变成可消费的 main-session gate
  evidence。
- 更直接的机器阻断：独立运行
  `.trellis/guru-team/scripts/bash/check-agent-assignment.sh --json --task <task>` exit 2，
  报告：

```text
status_events[114] failed 后缺少 same-agent resume 或 replacement 且后续 completed 的完整恢复链
status_events[116] failed 后缺少 same-agent resume 或 replacement 且后续 completed 的完整恢复链
```

- Live ledger 实际序列为 `evt-0115 failed -> evt-0116 resume-same-agent -> evt-0117
  failed -> evt-0118 terminated-unfinished -> evt-0120 replacement-started -> evt-0128
  replacement completed`。`replacement-started.predecessor_event_id` 指向 terminated event，
  没有为两个 failed event 形成 validator 要求的直接可遍历 recovery relation；append-only
  终态叙述不会改变该结构。
- `phase2_agent_assignment_errors()` 强制相同 recovery-chain validator，所以这不是仅供
  观察的 CLI 警告：当前 artifact 不能支持新的 passed `phase2-check.json` recorder。
- 影响：当前 Phase 2 evidence 链无法通过 deterministic gate；同时把
  `evt-0132/0135/0136` 计入主会话 liveness evidence 会违反 #72/#76 的真实 sub-agent
  provenance 边界。它阻断 #122 R3、R10/AC11 的 evidence freshness/gate 完成。
- 修复要求：保持 append-only，但追加机器可验证且真实的 recovery/correction evidence，
  或扩展 durable event contract、recorder、validator 和永久测试，使错误 provenance 可被
  显式失效且 recovery chain 可从 failed 经合法终止/替换到 completed；不得改写旧事件，
  不得仅靠一条自然语言 summary 让 machine gate 猜测。修复后必须重新运行
  `check-agent-assignment.sh` 并得到 exit 0。
- 处理：本代理不运行 recorder、不改写 ledger；按当前机器结果阻断。

## Round 8 transaction 独立闭环矩阵

| 场景 | 结论 | 证据 |
| --- | --- | --- |
| ordinary tracked B->C | 通过 | 永久回归 blocked，真实 HEAD/完整 index/candidate/operation 保持，C 不 commit。 |
| symlink target B->C | 通过 | Artifact target/mode authority 阻断 C，真实 transaction preimages 保持。 |
| reviewed delete 后 recreate C | 通过 | Artifact absence authority 阻断 C，不把 recreate 写入真实 index/commit。 |
| delete/add rename destination B->C | 通过 | Source absence + destination blob authority 阻断 C。 |
| multiple paths 第二条 B->C | 通过 | 整体 invocation blocked，没有 partial real publication。 |
| candidate self raw mutation | 通过 | Validated in-memory plan 是 staged authority；raw C 保留但不发布。 |
| entry index A / worktree B->C | 通过 | B/C 不进入 live index，完整 A bytes 保持。 |
| partial isolated cache write | 通过 | 只污染临时 index，真实 ref/index/candidate 保持。 |
| rejecting pre-commit hook | 通过 | 真实 hook chain 被调用；失败不发布 real state。 |
| same-path content/mode mutating hook | 通过 | Isolated tree mismatch 阻断；真实 ref/index/candidate 保持，hook worktree side effect 可见。 |
| 7-state operation / real cherry-pick | 通过 | Candidate/executor fail closed，marker bytes、HEAD、index、candidate 保持。 |
| gitlink entry A / reviewed B / switch C | 通过 | Pre-stage blocked；恢复 B 后真实 commit tree 只能为 `(B,160000)`。 |
| index publication 自身失败 | 通过 | 原 index lock 尚在，conditional ref rollback 与 preimage 保持。 |
| candidate publication 失败 + concurrent index C | **失败** | PHASE2-R8-01：lock 已释放，rollback 覆盖 C 并误报 exact restore。 |
| success publication + concurrent index C | **失败** | PHASE2-R8-01：返回 committed，但 live index 与 commit tree 不一致。 |
| concurrent branch ref D | 通过 | Conditional update-ref 阻断且不覆盖 D；index/candidate/operation 保持。 |
| transaction temp / message / lock cleanup | 通过 | 检查结束后 temp dir=0、message file=0、candidate lock=0、index lock=0。 |

Detached transaction Git admin 使用临时 `GIT_DIR`/HEAD/index，并通过真实
`GIT_COMMON_DIR` 共享 objects/config/hooks；真实 rejecting/benign/mutating hooks 与 commit
object/tree 读取均通过。该设计主体正确，Finding 只否定最后的 live publication 原子性。

## Round 6 / Round 7 closure

- `F-06-01`：closed。7-state operation detector 与真实 conflict cherry-pick 均保持
  fail closed，marker 不被读取内容或修改。
- `F-06-02` / `PHASE2-R6-01` gitlink：closed。Artifact OID 直接写 exact mode160000
  index，B->C 窗口不能提交 C；ordinary legacy 与 deliberate gitlink delete 兼容。
- `F-06-03`：closed。Canonical/dogfood workflow byte-equal，只保留 1 个 mandatory
  invoke、3 个 typed exits、finding repeat 与 fail-closed route；无 task-work template/
  direct `git commit`/第二 parser 回流。
- `PHASE2-R7-01`：ordinary/candidate-self 的 artifact content authority 与 isolated
  staging/hook commit 已修复；但其“可恢复 real publication”闭环被
  `PHASE2-R8-01` 阻断，不能宣称整个 transaction finding closed。

## R1-R10 / AC1-AC14

| 范围 | 结论 | 证据或阻断 |
| --- | --- | --- |
| R1 / AC1 | 通过 | Registry 保留 `guru-create-work-commit` reserved tombstone，激活 `guru-create-task-commit`；public API/manifest 一致。 |
| R2 / AC2 / AC8 | 通过 | Canonical/dogfood 各 1 invoke、3 exits；finding re-entry 与 5 个历史 sequence freshness 通过。 |
| R3 / AC5 | 阻断 | Candidate/blob materialization freshness通过；agent-assignment machine evidence 无效，publication index concurrency 未被 fresh gate 阻断。 |
| R4 / AC3-AC4 | 通过 | Standalone trigger、task-local artifact、candidate mode 与 empty checked range 行为通过。 |
| R5 / AC6 | 阻断 | Exact artifact index 构造通过，但 publication rollback 可覆盖并发 staged C。 |
| R6 | 通过 | AI scope/message/authorization/human owner 保持在 Markdown；runtime 没有新增语义判断。 |
| R7-R8 / AC7 | 阻断 | Shared parser、isolated parent/message/path/tree/blob/mode 通过；live index/result publication 不能保证成功一致性或失败 preservation。 |
| R9 / AC9 | 通过 | Global workflow/platform route-only，canonical package reference 独占 step-local 合同。 |
| R10 / AC10 | 通过 | Canonical/runtime/package、5 installed roots、manifest、installer/update/reapply 无漂移。 |
| R10 / AC11 | 阻断 | 32/24/514 与 throwaway 通过，但缺 candidate-publication concurrency 回归，且 assignment validator exit 2。 |
| AC12 | 按合同 pending | Remote exact feature-ref verifier 只能在 reviewed content push 后由 `trellis-finish-work` 生成；当前 pending 不满足 publish。 |
| AC13 | 通过 | `close_issues=[122]`；#92、#120 仅 related；5 个 work commits 均只用 `Refs #122`。 |
| AC14 | 通过 | Public added-line 与 5 个 task plan 的高置信敏感扫描均为 0。 |

## Docs SSOT

- Approved strategy 为 `ssot_first`，docs state=`partial_docs`。README、三份
  requirements、workflow README、五份 workflow specs 与 canonical package contract/
  interface/schema/example 已同步 Round 8 ordinary/gitlink/candidate/isolated transaction
  设计；runtime/test 与 installed copies byte-equal。
- Preset installer、overlay guidelines、public-docs 与 preset README 的 no-byte-change
  理由成立：Round 8 未改变 installer 算法、managed path、platform route 或公开安装命令。
- `PHASE2-R8-01` 证明 durable docs 的 Success index、publication failure exact restore、
  recoverable transaction 声明与真实最后三步 publication 存在差异。因此当前
  `ssot_first` 仍未形成可达行为闭环；修复时必须先收敛 data/companion/quality/package
  contract，再同步 runtime/tests/copies。
- Agent 身份、临时 blob、单次 probe 输出、测试耗时、sidecar remediation 与本报告仍是
  task-history-only，不进入公共 package。

## 分发、历史与验证结果

| 检查 | 结果 |
| --- | --- |
| Planning / workspace / task | Planning approval `ok`；workspace boundary `ok`；task validate 与 phase index/2.2/3.4/3.5 parse 通过。 |
| Targeted executor/candidate | `32/32`，17.895s，`OK`。 |
| 六个 package roots | Canonical + dogfood/shared/Claude/Codex/Cursor 各 `4/4`，合计 `24/24`，全部 `OK`。 |
| Full suite | Canonical package + skill/runtime/preset 单次集合 `514/514`，145.405s，`OK`。 |
| Clean throwaway | Exit 0；fresh workflow/preset install、initial/finding-fix commit、old-plan reject、`trellis update --force`、workflow preview/switch/reapply、preset reapply、source/installed、drift、update 前后 installed closeout smoke 与 recursive sidecar 全通过。 |
| Source/installed validator | 均 passed；reserved=1、active=1、invoke=1、exit=3；selected platforms=Claude/Codex/Cursor；managed=43，conflict/removal/sidecar=0。 |
| Canonical/installed equality | Runtime/workflow byte-equal；canonical package 到 5 installed roots 排除非资产 `__pycache__` 后全部 byte-equal。 |
| Dogfood drift | Passed。 |
| Runtime/package digests | Runtime=`402b752e...93b5`；interface/contract/schema/example/test 与 handoff 的 5 个 SHA-256 全匹配；package tree digest 由 installed validator 匹配 manifest。 |
| History messages | `origin/main..HEAD` 5/5 commits 通过 shared parser，均为 issue-bearing Chinese work messages。 |
| History plans/tree | Sequence 001-005 的 parent/message/path/planned-candidate binding 5/5；带 tree evidence 的 75/75 path blob/mode rows 与真实 commit tree 相等。 |
| JSON / compile / syntax / diff | Branch+dirty union 39 个 JSON 全部 parse；canonical/dogfood Python compile、相关 Bash syntax、branch/dirty `git diff --check` 全部通过。 |
| Independent probes | 3 组：candidate failure concurrent-index 与 success concurrent-index 复现 PHASE2-R8-01；concurrent ref probe 正确 fail closed。 |
| Agent assignment | **失败**：deterministic validator exit 2，两个 failed recovery chain errors，见 PHASE2-R8-02。 |
| Official extension boundary | 未修改 upstream/global npm/node_modules；workflow marketplace/preset/canonical/dogfood 分层符合官方文档。 |

## 安全、部署与工作区卫生

- Public non-task added-line 高置信扫描：private key、GitHub/AWS/Slack token、credential
  URL、signed URL marker、secret assignment 与机器用户绝对路径均为 0。
- 五个 task commit plans 的 private key/token/credential URL/signed URL/机器用户路径命中
  为 0；public artifact 不保存文件正文、operation marker 内容或本机路径。
- Branch+dirty union 没有 GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、
  Helm/chart、database migration 或 Makefile 变更。命中的
  `trellis/presets/guru-team/overlays/` 是平台入口分发，不是应用部署资产；无需应用部署、
  容器发布、配置变更或数据迁移。
- 报告写入前：55 tracked modified + 18 untracked，0 staged。报告写入后只应新增本报告，
  即 55 tracked modified + 19 untracked，0 staged。
- Recursive `.new/.bak=0`；transaction temp dir、message temp file、candidate lock 与
  live index lock 均为 0。
- Source checkout clean；没有 `.trellis/workspace/**` 或 source misplaced artifact。

## 观察项

1. Remote exact feature-ref marketplace verifier 继续按合同 pending；本报告不把 local
   mutable workflow sample 或 clean throwaway 冒充远程 reviewed-ref evidence。
2. Sequence 001 是 tree-evidence public contract 收紧前的历史 plan；本轮验证其真实
   parent/message/path/planned-candidate digest，不伪造 post-hoc tree evidence。
3. 公开兼容目标仍为 Trellis CLI `0.6.5`；本任务未授权扩大 compatibility baseline。

## 后续候选

无。两个 finding 都直接位于 #122 已批准的 exact publication、failure preservation、
evidence freshness 与 Phase 2 gate 范围，不能降级为 observation 或另开 follow-up 来通过。

## 最终结论

- `findings_count: 2`。
- 优先级：P0=0、P1=2、P2=0、P3=0。
- `PHASE2-R8-01`: open。
- `PHASE2-R8-02`: open。
- `F-06-01`: closed。
- `F-06-02` / `PHASE2-R6-01`: closed。
- `F-06-03`: closed。
- `PHASE2-R7-01`: ordinary/isolated 部分修复，但 transaction publication closure 被
  `PHASE2-R8-01` 阻断。
- Phase 2：`blocked`。
- 下一步必须返回 implementation 和 main-session evidence repair：修复完整
  ref/index/candidate publication ownership、补 candidate-publication concurrency 永久回归，
  并让 append-only assignment/recovery artifact 通过 deterministic validator。完成新的
  fresh Phase 2 后才能创建 sequence 006 或更高的 task commit；不得复用旧 Phase 2、
  sequence 001-005、旧授权或现有 Branch Review Gate。
