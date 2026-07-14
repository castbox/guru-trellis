# #122 第七轮修复后 replacement 独立 Phase 2 检查报告

## 身份、边界与结论摘要

- 逻辑角色：`阶段二检查代理`。
- 技术身份：`trellis_check_122_round7_replacement`。
- 平台昵称：`Check-Agent-122-Round7-Replacement`。
- Replacement 来源：前序 `trellis_check_122_round7_fix` 在生成报告前连续平台终止；
  `evt-0117-fa1006d803` 为 failed，`evt-0118-cd228c71fd` 为
  `terminated-unfinished`。前序 partial output 不作为 pass 或完成证据，本报告从 live
  files 独立复核。
- 固定 worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`。
- Task：`.trellis/tasks/07-13-122-guru-create-task-commit`。
- Base：`origin/main=6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Pre-commit HEAD：`163e64168d5d9783c32665da92aebbb4397564a3`，检查与报告写入前后均未改变。
- Source checkout：`/Users/wumengye/Documents/GoProjects/guru-trellis`，HEAD 为
  `6b9495a17dc953c7a54c105e39c23a786edcd8a7`，检查前后 clean。
- 检查范围：完整 `origin/main...HEAD`、当前全部 tracked dirty diff、全部 task-local
  review/history evidence、Round 7 runtime/schema/docs/tests/distribution delta、R1-R10、
  AC1-AC14、F-06-01/02/03、Docs SSOT、installer/update/reapply、安全与部署边界。
- 结论：`blocked`。发现 1 个 P1 当前范围 finding。现有 23/23、24/24、501/501、
  source/installed validator 和 clean throwaway 全绿，但现有测试没有覆盖 ordinary
  content/candidate-self 的 validator-to-stage 并发窗口，也没有证明失败后恢复 index
  preimage。
- 操作边界：本代理只新增本 raw report；未修改实现、durable docs、旧 task artifact、
  旧 report 或 recorder artifact；未运行任何 recorder、当前任务的 task commit executor、
  stage、commit、push、PR、finish-work、reset、revert、stash、amend、rebase 或 force。
  所有 executor 复现都在自动清理的独立 throwaway Git repo 中完成。

## 输入证据

- Live issue：`castbox/guru-trellis#122`，状态 `OPEN`，标题与 task 一致。
- 规划与批准：`prd.md`、`design.md`、`implement.md`、schema 1.2
  `planning-approval.json`；`check-planning-approval.sh` 返回 `status=ok`，三份规划文档
  digest 仍匹配。
- 实现交接：`implementation-handoff.md` 的 Round 7
  `PHASE2-R6-01` 修复交接。
- 前轮证据：`phase2-check-report-round-006-fix.md`、
  `reviews/round-006-final-release.md`，以及 `agent-assignment.json` 中
  `evt-0114-122e17ab15`、`evt-0117-fa1006d803`、`evt-0118-cd228c71fd`、replacement
  assignment/start evidence。
- 官方 Trellis 文档：`https://docs.trytrellis.app/index.md`、
  `advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md`。
  官方合同与本仓库边界一致：Markdown/workflow/skill 拥有过程与判断，companion script
  只执行或校验确定性事实；canonical marketplace/preset 是可安装、可升级源头。
- 项目规范：完整读取 `trellis-check`、`trellis-before-dev`、`trellis-meta`，以及
  `.trellis/spec/workflow/` 五份适用规范和 shared cross-layer/code-reuse guides。

## Findings

### PHASE2-R7-01（P1）：ordinary path 与 candidate self 未把 reviewed 内容绑定到 exact index，并发 C 可被提交且失败恢复不保留 index preimage

- 位置：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:10183`、`:10578`、
  `:10643`、`:10649`、`:10654`、`:10666`、`:10676`、`:10809`；dogfood runtime
  是其 byte-equal installed copy。
- 根因：candidate validator 在 `10183-10186` 只在入口比较一次当前 snapshot 与
  artifact snapshot。它返回后，executor 在 `10643-10665` 对 ordinary files、symlinks、
  deletes、delete/add rename 形态和 candidate self 调用 live `git add`，重新读取当时可变
  worktree bytes/mode/existence。stage 后只比较 path set；除 mode `160000` gitlink 外，
  没有把 artifact 中 reviewed content identity 约束为 exact index blob/mode。随后
  `10676` 又把已经含 C 的 live index 写成 `expected_tree`，postcondition 因而只证明
  commit 等于 stage 后的 C，而不是等于 AI/Phase 2 审查过的 B。
- Candidate self 受同一根因影响：它被排除在 recursive snapshot content digest 外，
  executor 在 `10649-10651` 无条件从当前文件重新 stage；入口 validation 之后新增的 raw
  bytes 可以进入 commit，而内存中的 B plan 仍驱动 message/result，最终错误返回
  `committed`。
- 并发状态一致性复现：每个 case 都先证明 candidate validation 对 reviewed B
  `errors=[]`，再在 executor entry validation 返回后、首次 exact stage 前受控改为 C。
  结果如下：

| Throwaway case | Reviewed state | 并发 state | 实际结果 |
| --- | --- | --- | --- |
| ordinary tracked file | bytes B | bytes C | commit C，exit=`committed` |
| symlink | target B | target C | commit target C，exit=`committed` |
| reviewed delete | path absent | recreate bytes C | commit C 而非 delete，exit=`committed` |
| delete/add rename 形态 | destination B | destination C | commit destination C，exit=`committed` |
| multiple exact paths | B1 + B2 | 第二个 path=C2 | commit B1+C2，exit=`committed` |
| candidate self | validated JSON bytes B | 追加未审查 raw byte | commit C bytes，exit=`committed` |
| 入场 index=A / reviewed worktree=B | A+B | worktree C | restage/commit C，exit=`committed` |

- 对照 case：入场 index 已是 reviewed B 且 snapshot worktree 也为 B 时，窗口内 worktree
  变为 C 不会把 C stage；executor 先真实 commit B，随后 postcondition 因 planned path
  仍 unstaged 才返回 `blocked`。这证明行为取决于入场 index/worktree 组合，并未建立一个
  稳定的 artifact-to-exact-index 内容合同。
- 失败恢复复现：
  - 受控 partial `git add` failure 在一个 exact ordinary path 已进入 live index 后返回
    `blocked`，HEAD 不变，但 index preimage 未恢复，留下该 path staged。
  - 真实 rejecting pre-commit hook 返回 `blocked`、HEAD 不变、
    `hook_mutation=false`、tree match；但 index preimage 仍未恢复，留下 ordinary path 和
    planned candidate staged，而 working candidate 已被 recorder 改成 blocked result。
  - `10809-10827` 只观察并记录失败后的 live state，没有恢复或隔离 staging transaction。
    因此同一个“直接操作 live index、没有完整 artifact content authority/transaction”根因
    同时破坏并发状态一致性、artifact 到 exact index 内容绑定和失败恢复；不拆成多个
    重复 finding。
- 影响：未经 AI/Phase 2 审查的 C 能获得真实 commit、`result.status=committed` 与
  `exit=committed`，随后 workflow 会进入 Branch Review/finding closure。它违反 #122
  R3-R5、R7-R8、AC5-AC7、AC11，并使 task-local artifact、exact index、真实 commit 的
  证据链在最关键的副作用边界失真。Candidate self 的 committed bytes 还可能与实际执行的
  in-memory plan/result lineage 不一致。
- 修复要求：为所有 ordinary exact paths 和 candidate self 建立 artifact-authorized
  blob/mode/delete/rename/raw-byte identity，不能只把 path list 交给 live `git add`。stage
  过程必须在任何 commit 前验证 exact index identity 等于 reviewed identity，并设计为
  原子/可恢复 transaction，使 partial staging 或 hook failure 后 index 精确回到入场
  preimage，或在正式副作用前完全隔离。新增永久真实回归覆盖 ordinary tracked、symlink、
  delete、rename、multiple paths、candidate self、入场 staged 组合、partial staging
  failure、hook failure 与 index preimage；每个 B-to-C case 必须 blocked 且不把 C 写入
  index/commit，或只能提交 artifact-authorized B。
- 处理：本代理按 Phase 2 边界只记录 finding，不做语义修复。

## Round 7 gitlink 与 Round 6 findings 独立闭环

### F-06-01：通过

- 7-state detector 覆盖 merge、cherry-pick、revert、rebase-head、sequencer、
  rebase-merge、rebase-or-am；targeted suite 的真实 conflicted cherry-pick 证明 candidate
  与 executor 均阻断，HEAD/index/worktree/candidate/marker 不变。
- Runtime 只观察 marker/directory，不消费或修复 operation state，符合 script boundary。

### F-06-02 / PHASE2-R6-01 的 mode `160000` gitlink 专项：通过

- 独立真实 A/B/C probe：artifact 在 B 生成且 validator `errors=[]`；executor entry
  validation 后、pre-stage revalidation 前切 C，结果 `blocked`。HEAD、完整 index bytes、
  candidate bytes、operation state 均不变；index 仍为 A/mode `160000`，不是 C。
- 同一 plan 恢复 worktree B 后执行正向路径，真实 commit tree gitlink 精确为
  `(B, 160000)` 且不为 C，证明 executor 消费 artifact OID，而不是只重复 freshness
  check。
- Schema 1.0 ordinary legacy entry 不要求 gitlink-only fields；mode `160000`
  non-delete 缺 identity 被 schema 拒绝，完整 identity 通过；deliberate gitlink delete
  保留兼容路径。
- 结论仅关闭 Round 6 的 gitlink 专项；它不能反证本轮 ordinary path/candidate-self 的
  `PHASE2-R7-01`。

### F-06-03：通过

- Canonical 与 dogfood workflow byte-equal，task work 只保留唯一 mandatory invoke、
  三个 typed-exit consumer、finding repeat 与 fail-closed route；未恢复 task work
  subject/body 模板或直接 `git commit` owner。
- 五个平台 continue entry 仍只负责 stable skill routing；package reference 是 step-local
  SSOT。

## R1-R10 / AC1-AC14

| 范围 | 结论 | 证据或阻断 |
| --- | --- | --- |
| R1 / AC1 | 通过 | Registry 保留 `guru-create-work-commit` reserved tombstone，激活 `guru-create-task-commit`；public API/manifest 一致。 |
| R2 / AC2 / AC8 | 通过 | Canonical/dogfood 各 1 invoke、3 exits；finding re-entry 与 5 个历史 sequence/commit freshness 通过。 |
| R3 / AC5 | 阻断 | Snapshot 只在 validator 瞬间 fresh；validator 返回后的 ordinary/candidate-self C 不会 stale。 |
| R4 / AC3-AC4 | 部分通过、总体阻断 | Standalone trigger、candidate mode/empty range 通过；candidate self raw bytes 未绑定，artifact lineage 可与 commit 分离。 |
| R5 / AC6 | 阻断 | Path set exact，但 ordinary content 不 exact；C 被 stage/commit，partial/hook failure 不恢复 index preimage。 |
| R6 | 通过 | AI scope/message/authorization/human owner 仍在 Markdown；script 未新增语义判断。 |
| R7-R8 / AC7 | 阻断 | Shared parser、gitlink OID、message/tree/result matrix 通过；ordinary postcondition 把 stage 后 C 当 expected tree并错误返回 committed。 |
| R9 / AC9 | 通过 | Global workflow/platform route-only，canonical package reference 独占 step-local 合同。 |
| R10 / AC10 | 通过 | Canonical/runtime/package、5 installed roots、manifest、installer/update/reapply 无漂移。 |
| R10 / AC11 | 阻断 | 23/23、24/24、501/501 与 throwaway 通过，但永久 suite 未覆盖本轮并发内容/失败恢复矩阵。 |
| AC12 | 按合同 pending | Remote exact feature-ref verifier 只能在 reviewed content push 后由 `trellis-finish-work` 生成；当前 pending 不满足 publish。 |
| AC13 | 通过 | `close_issues=[122]`；#92、#120 仅 related；5 个 work commit 使用 `Refs #122`。 |
| AC14 | 通过 | Public/task-plan 高置信敏感扫描为 0；artifact 只保存 repo-relative path/digest/结构化事实。 |

## Docs SSOT

- Approved strategy：`ssot_first`，docs state=`partial_docs`。README、requirements、
  workflow README、五份 workflow specs、canonical package contract/interface/schema/
  example、runtime/tests 与 installer/distribution 是 durable owners。
- Round 7 对 operation state 和 gitlink artifact OID 的 durable contract 已同步，且与当前
  gitlink runtime/probe 一致；canonical/installed copies 无漂移。
- `PHASE2-R7-01` 证明 durable docs 只定义了 gitlink 的 artifact-to-index OID authority，
  没有为 ordinary tracked/symlink/delete/rename/candidate-self 定义同等级内容 authority、
  并发一致性和 index preimage 失败恢复合同。Approved `ssot_first` 因而尚未覆盖最终可达
  runtime 行为，Phase 2 不能通过。
- 修复时必须先扩展 durable package/data/runtime/quality contract，再同步 runtime/schema/
  tests/canonical-installed copies。Agent 身份、临时 SHA、probe 输出、单次耗时和 sidecar
  remediation 仍是 task-history-only，不应进入公共 package。

## 验证结果

| 检查 | 结果 |
| --- | --- |
| Planning / workspace / task | Planning approval `ok`；workspace boundary `ok`；task validate 通过；source suspicious artifact=0。 |
| Targeted executor/candidate | `23/23`，`OK`；含 7-state、真实 cherry-pick、gitlink A/B/C、ordinary/hook/result 既有矩阵。 |
| 六个 package roots | Canonical + dogfood/shared/Claude/Codex/Cursor 各 `4/4`，合计 `24/24`，全部 `OK`。 |
| Full suite | Package/runtime/preset `501/501`，138.922s，`OK`。 |
| 独立 ordinary/candidate probe | 7 个 false-committed 组合稳定复现；2 个失败恢复组合均未恢复 index preimage。 |
| 独立 gitlink probe | B-to-C `blocked` 且 HEAD/index/candidate/operation 不变；正向 commit tree=`(B,160000)`。 |
| Source/installed validator | 均 passed；reserved=1、active=1、invoke=1、exit=3；dogfood managed=43，conflict/removal/sidecar=0。 |
| Canonical/installed equality | Workflow/runtime byte-equal；canonical package 到 5 installed roots 的 40 个 managed file comparison 全部相等。 |
| Clean throwaway | Exit 0；fresh install、initial/finding-fix commit、old-plan reject、`trellis update --force`、workflow preview/switch/reapply、preset reapply、source/installed、drift、update 前后 installed closeout smoke、recursive sidecar 全通过。 |
| History | `origin/main` 是 HEAD ancestor；5 个线性 work commits；message validator 5/5；5 个 plan 的 parent/message/path/planned-blob digest/result binding 5/5，带 tree rows 的 75 个 path identity checks 通过。 |
| Static | Canonical/dogfood Python compile、相关 Bash syntax、全部 changed JSON parse、branch/dirty `git diff --check` 全部通过。 |
| Security / deployment | Public added-line private key/token/credential URL/signed URL/machine-user path/secret assignment 全为 0；5 个 task plan sensitive pattern=0；deployment path hit=0。 |
| Workspace hygiene | 报告写入前 55 modified + 17 untracked、0 staged；`.trellis/workspace`/runtime status=0；recursive `.new/.bak`=0；source clean。 |

## 安全、部署与开箱/升级结论

- 107-path tracked branch+dirty union 未修改 GitHub Actions、Dockerfile/Compose、
  Kubernetes/Kustomize、Helm/chart、database migration 或 Makefile；`overlays/` 路径是
  Guru Team 平台入口分发，不是应用部署 overlay。无需应用部署、容器发布、配置或数据迁移。
- Clean throwaway 已覆盖新仓库安装、已有项目 workflow preview/switch、官方
  `trellis update --force` 后 workflow/preset reapply、source/installed validator、
  dogfood drift、真实 initial/finding-fix task commit 与 installed finish-work smoke；因此
  本地开箱即用/upgrade-update 机械门禁有真实通过证据。
- Remote exact feature-ref marketplace verification 仍按合同 pending；本报告不把本地
  mutable sample 或 throwaway 结果冒充远程 reviewed ref evidence。

## 观察项

1. Sequence `001` 是 tree-evidence public contract 收紧前的历史 plan，current result 没有
   `tree_evidence.matches`。本轮仍验证其真实 parent/message/path、committed planned-plan
   digest；未伪造 post-hoc expected tree。该已披露历史限制不新增 finding。
2. 本地兼容目标仍为 Trellis CLI `0.6.5`；#122 未授权扩大 compatibility target。

## 后续候选

无。`PHASE2-R7-01` 属于 #122 已批准的 exact staging、snapshot freshness、postcondition、
failure handling 与 AC5-AC7/AC11 范围，不能降级为 observation 或另开 follow-up 来通过门禁。

## 最终结论

- `findings_count: 1`。
- 优先级：P0=0、P1=1、P2=0、P3=0。
- `F-06-01`: closed。
- `F-06-02` / `PHASE2-R6-01` gitlink 专项：closed。
- `F-06-03`: closed。
- 新 finding：`PHASE2-R7-01`，open。
- Phase 2：`blocked`。
- 下一步必须返回 implementation，建立 ordinary/candidate-self 的 artifact-to-exact-index
  内容 authority 与可验证失败恢复，并补齐并发/partial/hook/staged 永久矩阵和 durable
  Docs SSOT；完成 fresh Phase 2 后才能创建新的 task commit sequence。不得复用旧
  Phase 2、sequence 001-005、旧授权或现有 Branch Review Gate。
