# #122 第十一轮修复后独立 Phase 2 检查报告

## 身份、边界与结论摘要

- 逻辑角色：`阶段二检查代理`；技术身份：
  `trellis_check_122_round11_fix`；平台昵称：
  `Check-Agent-122-Round11`。
- 审查 worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`。
- 审查 HEAD：`005c41fa755d4fea2d7c4f2bd8463041ffc7fe32`；base：
  `origin/main=6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- 审查范围：live issue #122、完整 `origin/main...HEAD` 六提交、当前 dirty
  diff、规划/Docs SSOT、Round 8 finding `F-08-01`、Round 10 Phase 2、Round 11
  implementation handoff、canonical/runtime/schema/tests/distribution、安装升级、历史
  candidate 与 Git object、安全、部署和工作区卫生。
- AI Phase 2 结论：`pass`，`findings_count=0`；P0/P1/P2/P3 均为 0。
  `F-08-01` 已关闭，没有新的 current-scope finding。
- 本报告是本代理唯一写入。未修改实现、durable docs、handoff、assignment、旧
  Phase 2/review/plans；未运行任何 recorder、review gate、task commit executor，未
  stage、commit、push、创建 PR、调用 finish-work 或关闭 issue。

## 输入证据与门禁

- Live GitHub：`castbox/guru-trellis#122` 仍为 OPEN，标题与 task 一致；#92、#120
  已关闭但在本 task 仅作为 related contract，不是 close candidate。
- 项目规则：完整读取 live `AGENTS.md`、`trellis-start`、`trellis-before-dev`、
  `trellis-meta`、`trellis-check`，并读取 meta architecture/customization references、
  `.trellis/spec/guides/index.md` 与相关 workflow specs。
- 官方 Trellis：读取 `https://docs.trytrellis.app/index.md`、
  `advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md`；当前实现
  继续遵守 Markdown workflow/skill 拥有流程与 AI 判断、companion script 只验证或
  执行确定性事实的边界。
- 规划：`prd.md`、`design.md`、`implement.md`、schema 1.2
  `planning-approval.json`；workspace boundary 与 planning approval validator 均通过。
- 实现交接：`implementation-handoff.md` SHA-256=
  `70b3c77e5243deba6d596c8c0a2cbbc7db5d0d7e15f6664e0346e78d0e4e0c09`，
  87860 bytes，与派发身份一致。
- Assignment：schema 1.2，3 条 digest-bound correction、2 条 recovery link；本轮检查
  时 live validator `--require-current-head` 通过，记录 28 agents、8 review rounds、
  5 reuse decisions、211 status events / 208 effective events。
- 旧 `phase2-check.json` 正确因 HEAD、dirty snapshot、handoff/assignment/spec digest
  已变化而 stale；本报告独立完成新的 semantic Phase 2 判断，不把旧 recorder pass
  当作当前证据。
- 写报告前 working snapshot：tracked dirty paths=53、untracked task evidence paths=23、
  porcelain rows=69、staged paths=0；本报告自身是随后新增的 task-local evidence。

## `F-08-01` 独立关闭证据

### 生产实现与 schema

- `capture_task_commit_snapshot()` 继续读取 NUL-delimited porcelain v1；对 relation
  record 显式解析 `R -> renamed_from`、`C -> copied_from`，ordinary row 两字段均为
  `null`，同一 record 同时出现 R/C 时 fail closed。
- Public schema 的 `copied_from` 是 optional additive repo path/null；
  `renamed_from` 与 `copied_from` 使用 `not` 约束互斥。Runtime 同时拒绝两字段非空、
  非 repo-relative relation source 与 self-reference。
- `expected_stage_paths` 只从 reviewed destination 的 `renamed_from` 继承 source；
  `task_commit_planned_index_bindings()` 也只把 `renamed_from` 写成 exact absence。
  `copied_from` 不参与 expected stage set、source deletion 或 index binding。
- 因此 copy source 只有在自身作为 snapshot row、独立分类为 `task-reviewed` 且有 fresh
  Phase 2 coverage 时才能进入 exact stage；若是 `unrelated-preserved` staged content，
  executor 在 isolated transaction 前由 unexpected staged-path gate 阻断。

### 真实 Git 行为矩阵

1. `status.renames=copies` + reviewed destination + independently staged
   `unrelated-preserved` source：snapshot 生成 destination `copied_from=source`，source
   row 两 relation 均 null；exact paths 不含 source。Candidate objective validation
   成功，但 executor 在 transaction 前阻断 unexpected staged source；HEAD、完整 index
   bytes、candidate bytes、source worktree bytes、source/destination commit-tree identity
   均保持 entry preimage。
2. Clean copy source：只提交 destination 与 candidate self；commit tree 中 source
   blob/mode 与 parent 完全相同，source 未被删除或自动 staged。
3. Independently reviewed source：source 与 destination 均进入 exact stage；真实 commit
   保留 source path 并写入 reviewed source bytes，同时新增 destination。
4. Existing rename：reviewed rename destination 仍继承 source deletion authority，真实
   commit path set 包含 delete source、add destination 与 candidate self；旧 rename 语义
   未回归。

目标 package + copy/rename 矩阵为 `8/8`。上述用例使用真实临时 Git repo、真实
`git config status.renames copies`、真实 index 和 production executor，不是 mock Git
状态。

### 非 tautology mutation 证明

- 将 production snapshot 输出中的 `C` 重新折叠为 `renamed_from` 后，永久回归在
  destination relation assertion 处失败，旧 authority bypass 无法通过。
- 从 production snapshot row 删除 `copied_from` 后，永久回归在显式 copy provenance
  assertion 处失败。
- 两个 mutation 均被拒绝（`2/2 rejected`）。测试不只是根据被测 runtime 输出再计算
  同一个 expected set，能捕获删除 copy 判别或重新混同 rename/copy 的回归。

### Schema 1.0 backward compatibility

- Schema contract test 删除 ordinary row 的 `copied_from` 后仍通过 Draft 2020-12
  validation；同时 relation 两字段非空会被拒绝。
- Sequence 002-006 的真实 working artifacts 全部是 schema 1.0 且所有 snapshot rows
  缺少 `copied_from`；使用当前 `task_commit_result_validation_errors()` 独立运行仍为
  `5/5`、`errors=[]`。
- 兼容结论因此同时有 public schema 与 current runtime result validation 证据；新
  producer 强制显式输出不等于改写历史 artifact。

## R1-R10 / AC1-AC14

| 范围 | 结论 | 证据与判断 |
| --- | --- | --- |
| R1 / AC1 | 通过 | Production registry 保留 `guru-create-work-commit` reserved tombstone，并激活 `guru-create-task-commit`；public id/interface/schema/executor 未破坏。 |
| R2 / AC2 / AC8 | 通过 | Canonical workflow 保持唯一 mandatory invoke、3 个唯一 typed-exit consumer；finding fix 必须返回新 Phase 2 和新 candidate sequence。 |
| R3 / AC4-AC5 | 通过 | Workspace/planning/Phase2/ledger/HEAD/operation/snapshot/message/digest/authorization 均 fail closed；candidate mode 不以空 branch range 冒充 pass。 |
| R4 / AC3 | 通过 | Task-local artifact 仅记录 repo-relative/digest/structured facts；standalone trigger 覆盖 initial、Phase2 changes、finding fix 与 revision commit。 |
| R5 / AC6 | 通过 | Copy relation 不再给 source stage authority；unrelated staged source 阻断并保持，clean source 不入 stage，reviewed source 独立提交。 |
| R6 | 通过 | Scope/message/confirmation/route 仍由 Markdown skill 与 AI Gate 判断；runtime 不生成业务语义。 |
| R7-R8 / AC7 | 通过 | 唯一 parser、exact executor、ordinary/gitlink/candidate authority、hook isolation、ref/index/candidate transaction 与 copy/rename authority 全部闭环。 |
| R9 / AC9 | 通过 | Workflow/continue/platform entries 只保留 invoke/re-entry/exits/fail-closed；step-local relation 细节由 canonical package contract 独占。 |
| R10 / AC10 | 通过 | Canonical、dogfood runtime、六 package roots、registry/manifest/installer/README 无漂移；source/installed/drift 全部通过。 |
| R10 / AC11 | 通过 | 39/30/24/525、真实 copy/rename、mutation、throwaway、history/object/static 全部通过。 |
| AC12 | 按合同 pending | Local throwaway 通过；remote exact feature-ref verifier 只能由 finish-work 在 reviewed content push 后执行，pending 不满足 publish。 |
| AC13 | 通过 | Ledger 唯一 close issue 为 #122；#92/#120 仅 related；六条 work message 均 `Refs #122` 且没有 close keyword。 |
| AC14 | 通过 | Public non-task added-line 高置信 secret/credential/signed URL/机器绝对路径扫描均为 0。 |

## Docs SSOT 与脚本边界

- Approved Docs SSOT strategy=`ssot_first`，docs state=`partial_docs`。
- 顶层 README、requirements README/main/flow、workflow README、五份 workflow specs 与
  canonical package contract 已先记录 relation separation、rename-only inheritance、copy
  source 独立分类和真实 Git 回归；runtime/schema/tests 随后承接同一合同。
- `interface.json`/schema/example/contract/test、canonical runtime/test 和 installed copies
  语义一致；global workflow、continue prompt/command/breadcrumb 没有复制 step-local
  candidate/relation/executor 正文，也没有第二套 parser 或 direct task work commit。
- AI owner 仍决定 path classification、scope、message sufficiency、human confirmation、
  typed exit 与 review pass/block；script 只解析 objective Git state、校验 schema/digest/
  identity 并执行 exact side effect，符合 AGENTS 和官方 workflow 扩展边界。
- Task delta 已合并回 durable docs。代理身份、临时 repo、测试耗时、单次命令输出、
  assignment correction/recovery 与 raw reports 保持 task-history-only，没有进入公共
  package。

## 事务与既有 finding 非回归

- `TaskCommitCandidateExecutorTest`：`39/39`，33.583s，`OK`。除本轮 3 个 copy
  case 外，继续覆盖 ordinary/symlink/delete/rename/gitlink/candidate-self、ordinary Git
  operation markers、hooks/isolated detached commit、literal path、partial cache、
  `index.lock` sentinel、ref/index/candidate guards、conditional rollback、candidate final
  identity-read 线性化和 failure state matrix。
- `index.lock` 继续只作为 live index sentinel 持有到 transaction 结束；final index
  使用独立同目录 publication temp。Final candidate inode/content read 是 success
  linearization point：read 前 writer C 触发 owned ref/index rollback 并保留 C，read 后 C
  视为 later operation，immutable commit candidate blob/result digest 仍是 committed
  authority。
- Round 10 的 `PHASE2-R9-01`、更早 ordinary/gitlink/candidate authority、operation-state、
  hook/path/result-state、assignment 1.2 correction/recovery findings 均有原测试继续覆盖；
  本轮没有删除或弱化旧 case。

## 历史提交与 candidate 审计

| Sequence | Commit | Parent/message | Actual exact paths | Direct tree evidence |
| --- | --- | --- | --- | --- |
| `001` | `afcab193` | 匹配 | 102/102 | Legacy committed result shape 已披露；不伪造新 tree rows。 |
| `002` | `03e813c5` | 匹配 | 31/31 | 31/31 blob/mode 与真实 commit tree 相同。 |
| `003` | `1534b545` | 匹配 | 26/26 | 26/26 blob/mode 相同。 |
| `004` | `ce705679` | 匹配 | 9/9 | 9/9 blob/mode 相同。 |
| `005` | `163e641` | 匹配 | 9/9 | 9/9 blob/mode 相同。 |
| `006` | `005c41fa` | 匹配 | 48/48 | 48/48 blob/mode 相同。 |

- 六提交 parent、raw message SHA-256、`--no-renames` committed path set 均与 plan
  直接相等；sequence 002-006 共 `123/123` result tree rows 又逐项对照真实 Git tree。
- Shared parser 对 `origin/main..HEAD` 为 `6/6`、`errors=[]`；没有 metadata/merge
  commit 被 task-work parser 错误接管。
- 当前下一 candidate 必须使用新 sequence `007`；本轮未创建、修改或执行 candidate。

## 验证、分发、安装与升级

| 检查 | 结果 |
| --- | --- |
| Copy/rename targeted | Canonical package 4 + runtime copy/rename 4=`8/8`；mutation `2/2 rejected`。 |
| Transaction | `TaskCommitCandidateExecutorTest`=`39/39`。 |
| Assignment/liveness | `AgentAssignmentArtifactTest + SubagentLivenessStateMachineTest`=`30/30`。 |
| 六 package roots | Canonical + `.trellis`/shared/Claude/Codex/Cursor 各 `4/4`，合计 `24/24`。 |
| Full suite | Canonical package `4/4` + skill infrastructure `58/58` + runtime discovery `427/427` + preset `36/36` = `525/525`，全部 `OK`。 |
| Clean throwaway | Exit 0；public marketplace discovery + local unpublished workflow sample、fresh workflow/preset install、initial/finding-fix task commit、old-plan reject、update、workflow/preset reapply、source/installed/drift、closeout/archive/ready equality、recursive sidecar 全通过。 |
| Source/installed | Source passed；installed passed，Claude/Codex/Cursor，managed=43、conflict/removal/sidecar=0。 |
| Equality | Canonical/dogfood runtime byte-equal；canonical package 8 assets 到五 roots共 40 次 byte comparison 相同。 |
| Static | Branch/working/cached `git diff --check`；changed union Python AST 12、JSON parse 35、Bash syntax 15；task validate 与 phase 2.2/3.4/3.5 parsing 全通过。 |

- Canonical runtime SHA-256=
  `383ccbb80b73dbfbb6bae8a6b0dad9b0559a3c998cddb29a3dcc13f2e908d252`；
  test SHA-256=
  `b36a286df53ab67bb3638d0b60cd3db2687268fe16a648e6939e35a30228fae7`。
- Interface/contract/schema/example/package-test SHA-256 分别为
  `237e2395128aae16748ee5ea1002cd15b9dc4666c9803d17b9eac768a2315152`、
  `d125236e341c5c33cb6d791065f07a8abd5131f04aa2fb634d89f0658adcf35d`、
  `8a7f2dce07f7f4b2723ac9ccae23d41636c362e5daa699c2afaca6fa570514e3`、
  `89a3de2235eed74f1fbbb51d8b7db67fb51c1953ee314e9898dc4c62735c4954`、
  `0f8015a0bf07208bcd06a6221e4b6fff2017afc91031783215da9e7a335780cb`。
- Manifest SHA-256=
  `0e2b51ead574eec2b4aec7ae805b2e2788a079e6197c89a0ed2e0a380c4f80a9`；
  installer source/installed validation 与 dogfood overlay drift 均 passed。
- 未 push feature branch 时，throwaway 首次无 override 正确拒绝把 public `main` 冒充
  current branch。随后按 verifier 合同使用
  `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 验证 public discovery + local unpublished
  sample 并通过；这不冒充 remote exact feature-ref publish evidence。

## Issue Scope、安全、部署与卫生

- `issue-scope-ledger.json` 的 primary/唯一 close candidate 均为 #122；#92/#120 只作
  related，followup 为空。`F-08-01` 属于 #122 明示的 exact stage/unrelated
  preservation 范围，现已在当前 scope 内关闭。
- Public non-task added-line 对 private key、GitHub/AWS/Slack token、credential URL、
  signed query 与 `/Users/<name>/` 机器路径扫描均为 0；task history 的本机 worktree
  路径没有进入公共 package/schema/example/manifest。
- Branch+dirty paths 未触及 GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、
  Helm/chart、database migration 或 Makefile；未新增 service、worker、queue、scheduler、
  runtime config 或数据迁移，无部署资产同步要求。
- Source checkout 为 clean `main==origin/main@6b9495a`；task worktree staged paths=0。
  Recursive `.new/.bak`=0，transaction/candidate/ref/index locks 和 publication temps=0；
  throwaway 自动清理。

## 观察项与后续边界

1. Remote exact feature-ref marketplace verifier 仍为 pending，必须由
   `trellis-finish-work` 在 reviewed content push 后执行；它不是本轮 Phase 2 finding，
   也不能由 local throwaway 替代。
2. Compatibility target 仍为 Trellis CLI `0.6.5`；本轮没有扩大版本基线。
3. 本报告通过后，主会话仍必须使用 recorder 记录 fresh `phase2-check.json`，再创建新
   sequence `007` candidate；本代理不执行这些副作用。

## Findings 与最终结论

- `findings_count: 0`。
- 严重度：P0=0、P1=0、P2=0、P3=0。
- AI Phase 2：`pass`。
- `F-08-01` 已由独立生产代码审查、四类真实 Git 行为、两个 mutation probe、
  schema/runtime backward compatibility 与完整 525-test suite 关闭。
- 没有 current-scope blocker；可以由主会话记录 fresh Phase 2 evidence，随后按
  mandatory `guru-create-task-commit` 创建新的 finding-fix work commit。Branch Review
  仍需先由 Round 8 finding owner仅作 closure，再派从未参与 review 的 fresh final
  reviewer；不得跳过 closure-before-final，也不得在 `trellis-continue` 中 push/PR。
