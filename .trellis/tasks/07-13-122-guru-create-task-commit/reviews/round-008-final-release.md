# #122 第八轮最终放行审查报告

## 身份、边界与结论摘要

- 逻辑角色：`最终放行审查代理`。
- 技术身份：`trellis_final_review_122_03`。
- 平台昵称：`Final-Review-Agent-122-03`。
- 独立性：本代理在本轮派发前未出现在既有 `review_rounds[]` 或
  `reuse_decisions[]`，没有复用 Round 7 的 closure pass 代替本轮判断。
- Reviewed HEAD：`005c41fa755d4fea2d7c4f2bd8463041ffc7fe32`。
- Base：`origin/main=6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- 完整 diff：`origin/main...HEAD`，6 个线性 task work commits、108 个 changed
  paths、23264 insertions / 474 deletions。
- 固定 worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`。
- Source checkout：`/Users/wumengye/Documents/GoProjects/guru-trellis`，
  `main@6b9495a17dc953c7a54c105e39c23a786edcd8a7`，审查期间 clean。
- 审查模式：完整 Branch Review 最终放行审查，不是 finding closure；命令通过不能替代
  对需求、边界和失败路径的语义判断。
- 本轮结论：`blocked`。发现 1 个 current-scope P1；不得记录 passing Branch Review
  Gate、push、创建 PR、调用 finish-work 或关闭 issue。
- 操作边界：本报告是唯一写入；未修改实现、durable docs、规划、Phase 2、assignment、
  旧 task artifact、旧 raw report 或 rollup；未运行 `review-branch.sh`、
  `check-review-gate.sh`、任何 recorder、task commit executor、stage、commit、push、PR、
  finish-work、reset、stash、amend、rebase 或 force。所有攻击性复现只在自动清理的临时
  Git repo 中执行。

## 输入证据

- Live issue：`castbox/guru-trellis#122`，状态 `OPEN`；#122 是唯一 close candidate，
  #92、#120 只作 related。
- 项目与技能规则：live `AGENTS.md`、`trellis-start`、`trellis-before-dev`、
  `trellis-meta`、`trellis-check`，以及 workflow、preset、docs、cross-layer、code-reuse
  specs 和 meta architecture/customization references。
- 官方文档：`https://docs.trytrellis.app/index.md`、
  `advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md`。当前架构
  仍遵守 Markdown workflow/skill 拥有过程和 AI 判断、companion script 只验证或执行
  确定性事实的官方扩展边界。
- 规划与 Docs SSOT：`prd.md`、`design.md`、`implement.md`、schema 1.2
  `planning-approval.json`、`implementation-handoff.md`。
- Phase 2：`phase2-check.json`、Round 10 replacement raw report、历史 Phase 2 reports/
  findings、checker assignment/correction/recovery/liveness evidence。
- Branch Review：Round 1-7 raw reports、finding artifacts、旧 `review.md`（仅历史入口）和
  当前 assignment ledger。
- 提交：sequence 001-006 的 committed planned bytes、working result、6 个 commit
  objects、parent、raw message、path set、tree/blob/mode evidence。
- 实现与分发：canonical/dogfood workflow/runtime、skill package/interface/schema/example/
  wrappers/tests、registry/manifest、preset installer/overlays/platform copies、requirements/
  README/spec、throwaway verifier。

Workspace boundary 与 planning approval 的 fixed identity/content digest 均有效。当前
assignment 为 schema 1.2，保留 3 条 digest-bound correction 和 2 条 same-agent
failed-to-termination recovery link；本代理仅出现在本轮 assigned/progress 状态中，未出现于
既有 review round 或 reuse decision。

## 需求与验收审查

| 范围 | 结论 | 证据与判断 |
| --- | --- | --- |
| R1 / AC1 | 通过 | Production registry 保留 `guru-create-work-commit` reserved tombstone，并激活 `guru-create-task-commit`；public API、schema id、executor command 与 extension `0.6.5-guru.5` 一致。 |
| R2 / AC2 / AC8 | 通过 | Canonical/dogfood workflow 各只有 1 个 mandatory invoke marker 与 3 个唯一 typed-exit consumer；finding fix 返回完整 Phase 2 并创建新 sequence。 |
| R3 / AC4-AC5 | 通过 | Candidate mode 在空 branch range 仍校验；planning/Phase 2/ledger/HEAD/operation/snapshot/message/authorization 与 candidate identity 均有 fail-closed evidence。 |
| R4 / AC3 | 通过 | Standalone trigger 覆盖 task commit、Phase 2 changes、finding fix 与 revision commit；artifact 为 task-local、repo-relative、digest-bound。 |
| R5 / AC6 | **阻断** | Git copy 状态的 source 可在被分类为 `unrelated-preserved` 时仍被无条件加入 exact stage 并提交，见 `F-08-01`。 |
| R6 | 通过 | Scope/message/authorization/human confirmation/route 判断仍由 Markdown skill 与 AI Gate 拥有；runtime 不生成业务语义。 |
| R7-R8 / AC7 | **阻断** | ordinary/gitlink/candidate/ref/index/hook 事务主路径已线性化，但 copy-source 分类绕过让 executor 对未授权 path 错误返回 `committed` 与 preservation success，见 `F-08-01`。 |
| R9 / AC9 | 通过 | Global workflow 只保留 invocation/re-entry/typed exits/fail-closed；详细 work message、candidate、executor、postcondition 只由 canonical package contract 拥有。 |
| R10 / AC10 | 通过 | Source/installed validator、registry/manifest、六 roots、managed installer、workflow/preset reapply 与 drift 均一致。 |
| R10 / AC11 | **阻断** | 522/522 与 clean throwaway 全绿，但没有覆盖 `status.renames=copies` + unrelated staged source；现有 coverage 不能证明 AC6。 |
| AC12 | 按合同 pending | Remote exact feature-ref verifier 只能在 reviewed content push 后由 `trellis-finish-work` 生成；当前 pending 不能满足 publish readiness，但不是本轮 P1 的替代证据。 |
| AC13 | 通过 | Ledger 只有 `close_issues=[122]`；#92/#120 仅 related；6 个 work messages 只使用 `Refs #122`，没有 close keyword。 |
| AC14 | 通过 | Public non-task added-line 与计划 artifact 的高置信 private key/token/credential URL/signed URL/机器绝对路径扫描无命中。 |

## 完整提交审计

| Sequence | Commit | Parent | Message | Planned/actual paths | Result |
| --- | --- | --- | --- | --- | --- |
| `001` | `afcab193` | `6b9495a1` | raw bytes/digest 匹配 | 102/102，集合相等 | Committed blob 为 `planned`；working result 为已披露 legacy committed shape。 |
| `002` | `03e813c5` | `afcab193` | 匹配 | 31/31 | Current result schema/runtime errors=`[]`；tree/blob/mode 匹配。 |
| `003` | `1534b545` | `03e813c5` | 匹配 | 26/26 | Current result schema/runtime errors=`[]`；tree/blob/mode 匹配。 |
| `004` | `ce705679` | `1534b545` | 匹配 | 9/9 | Current result schema/runtime errors=`[]`；tree/blob/mode 匹配。 |
| `005` | `163e641` | `ce705679` | 匹配 | 9/9 | Current result schema/runtime errors=`[]`；tree/blob/mode 匹配。 |
| `006` | `005c41fa` | `163e641` | SHA-256=`4ee6801431b41898ef351b01686588c6e2d41a8d3a4a4c057134a784bef8f4ac`，匹配 | 48/48 | Tree=`6cd8a0cf869f5c8248ca094d14c1e33003e65877`；48/48 blob/mode、planned candidate blob 和 working committed result 匹配。 |

Sequence 006 绑定 fresh Round 10 replacement Phase 2、76-path snapshot、47 个 reviewed
work paths加 candidate self，29 个 task-local metadata/history paths未进入 commit。当前
staging 为空。上述历史对象一致性不能反证新发现的 copy-source 路径分类缺陷。

## Finding 生命周期与 closure-before-final

- Round 1：fresh final reviewer 发现 same-path hook、literal path、result schema 共 3 项。
- Round 2-4：同一 finding owner 只以问题闭环角色复核，继续发现 blocked state matrix、
  永久 7/15/12 matrix 与非掩蔽 assertion 缺口。
- Round 5：原 finding owner 以 `findings_count=0` 关闭 Round 1-4 链，但未担任下一轮 final
  reviewer。
- Round 6：新的 final reviewer `trellis_final_review_122_02` 对完整五提交 diff 发现 Git
  operation、gitlink authority、workflow SSOT 共 3 项并成为 finding owner。
- Round 7：同一技术身份只执行 closure，确认三项均 closed、`findings_count=0`，并明确
  永久禁止自己成为最终 reviewer。
- Round 8：本技术身份独立重读 live evidence、完整六提交 diff并执行新负向 probe；
  closure-before-final 顺序合规，但新发现 `F-08-01`，因此本代理成为新的 finding owner，
  不得担任后续最终放行代理。

## Docs SSOT

- Approved strategy=`ssot_first`，docs state=`partial_docs`。
- README、requirements、workflow/preset/docs specs、canonical package contract、runtime、
  schema、tests 与 installed copies已一致记录 ordinary-operation gate、普通 path/gitlink/
  candidate authority、isolated hooks、`index.lock` sentinel、conditional rollback 和 final
  candidate identity-read 线性化。
- Global workflow 与 continue entries 保持 route-only，没有第二套 parser 或 direct task
  work commit 路径；canonical/dogfood workflow byte-equal。
- `F-08-01` 不是已有 durable contract允许的行为：R5/AC6 和 package contract明确要求
  `unrelated-preserved` 不进入 exact stage。当前 runtime 对 Git copy relation 的实现与该
  SSOT 冲突，必须返回 implementation/Phase 2 修复，不能降级为观察项。
- Assignment correction/recovery rows、provider 失败、测试耗时、临时 repo SHA和 review
  reports仍是 task-history-only，没有进入公共 package。

## 代码、测试、安装与升级

- Skill package六个 roots各 8 个 assets字节一致；workflow/runtime 2 对 byte-equal，
  42 次 exact copy comparison 全部通过。
- Source validator：reserved=1、active=1、invoke=1、exits=3，passed。
- Installed validator：Claude/Codex/Cursor，managed=43，conflict/removal/sidecar=0，passed。
- Dogfood overlay drift passed；`.new/.bak` 为 0。
- 精确 full suite：canonical package 4/4、skill infrastructure 58/58、runtime discovery
  424/424、preset 36/36，合计 522/522。
- 六 package roots standalone：24/24。
- Clean throwaway exit 0：覆盖 public marketplace discovery + local unpublished workflow
  sample、fresh init/preset、initial/finding-fix task commit、old-plan reject、
  `trellis update --force`、workflow preview/switch/reapply、preset reapply、source/installed/
  drift、更新前后 closeout、archive/ready equality 与 recursive sidecar。
- Static：branch/working/cached `git diff --check`、12 个 changed Python AST、changed Bash
  syntax 与 JSON parse全部通过。
- 上述测试没有配置 `status.renames=copies` 并把 copy source 分类为
  `unrelated-preserved`，所以全绿结果不能覆盖 `F-08-01`。

## Phase 2 复核

- Round 10 replacement raw report与 `phase2-check.json` 绑定 pre-commit HEAD `163e641`，
  checker=`trellis_check_122_round10_replacement`，当时 findings=0；assignment terminal gate
  后置完成，sequence 006 evidence digest与实际提交匹配。
- Phase 2 已覆盖 transaction 36/36、assignment/liveness 30/30、六 roots 24/24、full
  522/522、throwaway、history/tree、安全、部署和卫生。
- 本轮独立 probe覆盖的是 Phase 2/Round 7 未枚举的 Git copy relation组合。它稳定反证
  R5/AC6 的完整性，因此不能用 fresh digest 或原 checker pass 覆盖新的 current-scope
  finding。

## 阻断问题

### F-08-01（P1）：Git copy source 即使分类为 unrelated-preserved 仍会被加入 exact stage 并提交

- 位置：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:10556`、
  `:10794`、`:10467`。
- 根因：snapshot parser把 `R` 和 `C` 都写入同一个 `renamed_from` 字段；candidate
  validator对所有 `renamed_from` 无条件扩充 `expected_stage_paths`；index binding又把该
  source当作 exact path处理。代码没有区分 rename 与 copy，也没有要求一个本身存在于
  snapshot且被单独分类的 copy source必须是 `task-reviewed`。
- 独立真实复现：在临时 repo 设置 `git config status.renames copies`，基线存在
  `src/source.txt`；复制为 `src/copy.txt`，同时 stage source 的独立修改。Git status为
  `C  src/source.txt -> src/copy.txt` 加 `M  src/source.txt`。AI plan只把 copy分类为
  `task-reviewed`，把 source分类为 `unrelated-preserved`。
- 实际结果：candidate validator返回 `errors=[]`；`exact_stage_paths`错误包含 copy和
  source；executor返回 `committed`；真实 commit同时包含两个路径；payload仍把
  `src/source.txt`列入 `unrelated_preserved_paths`，commit后该 staged source变为 clean。
- 影响：一个明确未授权、应保持原 staged/unstaged状态的并行修改被静默纳入 task work
  commit，同时生成虚假的 preservation success。这直接违反 R5、AC6、AI path
  classification与 exact executor边界，风险与此前 same-path/gitlink authority bypass
  同级。
- 修复要求：snapshot和 schema/runtime必须显式区分 rename/copy relation。只有 rename
  source可作为 destination 的删除 authority继承 exact stage；copy source不得因 relation
  自动进入 stage。若当前版本不支持 copy，应在 candidate validation前 fail closed。
  Validator还必须拒绝任何本身存在于 snapshot、分类不是 `task-reviewed` 却进入 exact
  stage的 path。
- 永久回归要求：使用真实 `status.renames=copies` repo覆盖 staged copy + independently
  modified source；当 source为 `unrelated-preserved` 时，candidate必须阻塞现有 unrelated
  staged content，或仅在 source未进入 staged plan时保持其 index/worktree bytes exact；
  不得提交 source或声称虚假 preservation。另保留 rename source的既有正确行为。

## Issue Scope、安全与部署

- `issue-scope-ledger.json` 的 `primary_issue` 与唯一 `close_issues` 都是 #122；#92、#120
  只作 related；没有 followup close语义。
- `F-08-01` 属于 #122 明示的 unrelated staged blocking、exact path和preservation验收，
  不能外移到 follow-up来放行当前 PR。
- Public non-task added-line对 private key、GitHub/AWS/Slack token、credential URL、signed
  URL、机器用户绝对路径的高置信扫描均为 0。
- 变更路径没有 GitHub Actions、Docker/Compose、Kubernetes/Kustomize、Helm/chart、
  migration或 Makefile；无需应用部署、容器发布或数据迁移同步。
- Executor仍不 push、不 reset/rebase/amend/stash/force；本轮 finding是本地提交内容授权
  与 preservation完整性问题。

## 观察项

1. Remote exact feature-ref marketplace verifier继续按合同 pending；它必须在 reviewed
   content push后由 finish-work完成，不能替代本轮修复和新的 Branch Review。
2. Compatibility target仍为 Trellis CLI `0.6.5`；本 issue未授权扩大 baseline。
3. 直接执行 runtime test文件只运行其中 `unittest.main()` 之前的 272 项；本轮已改用
   `unittest discover` 运行完整 424 项，并以 522/522作为正式 full-suite证据。该测试入口
   差异不是产品 finding。

## 后续候选

无。`F-08-01` 是 #122 当前 R5/R7-R8/AC6-AC7/AC11 的直接缺陷，不得降级为
observation或独立 follow-up。

## Findings 与最终结论

- `findings_count: 1`。
- 严重度：P0=0、P1=1、P2=0、P3=0。
- 当前结论：`blocked`。
- Round 8不能作为最终放行证据。必须返回 implementation，修复 copy/rename relation与
  unrelated staged preservation，完成新的完整 Phase 2，以 fresh sequence 007 或更高
  candidate创建 finding-fix work commit，再由本 finding owner仅执行 closure review。
- Closure findings归零后，仍必须派发此前未参与任何 review round的 fresh
  `最终放行审查代理` 对新的完整 `origin/main...HEAD` 执行最终放行审查；本技术身份不得
  再担任该角色。

