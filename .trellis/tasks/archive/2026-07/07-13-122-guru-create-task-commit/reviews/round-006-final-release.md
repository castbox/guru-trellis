# #122 第六轮最终放行审查报告

## 身份与审查边界

- 逻辑角色：`最终放行审查代理`。
- 技术身份：`trellis_final_review_122_02`。
- 复用决策：`reuse_decision: new-agent`。
- 审查时间：`2026-07-13T15:07:17Z`。
- `reviewed_head: 163e64168d5d9783c32665da92aebbb4397564a3`。
- Base：`origin/main=6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- 完整 diff：`origin/main...163e64168d5d9783c32665da92aebbb4397564a3`，共 5 个线性 work commits、107 个 changed paths。
- 审查模式：最终全量 AI review，不是 finding closure review；覆盖需求、规划、Docs SSOT、代码、schema、测试、分发、安装升级、任务证据、五个真实提交与发布边界。
- 操作边界：未修改实现、durable docs、旧 task artifact 或旧 raw report；未运行 `review-branch.sh`、`check-review-gate.sh`、`record-agent-assignment.sh` 或任何 `record-*`；未 commit、push、创建 PR、调用 finish-work 或关闭 issue。本报告是唯一写入。

## 输入证据

- Live issue：`castbox/guru-trellis#122`，标题“实现 guru-create-task-commit 闭环 Skill 并收敛 Task work commit SSOT”，状态 `OPEN`。
- 官方 Trellis 文档：`index.md`、`advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md`；官方合同确认 workflow 行为由 Markdown 定义，marketplace/preset 负责可安装分发，脚本只执行确定性事实。
- 规划与任务证据：`prd.md`、`design.md`、`implement.md`、`planning-approval.json`、`implementation-handoff.md`、`phase2-check.json`、`phase2-check-report-round-004-fix.md`、`issue-scope-ledger.json`、`task.json`、`task-start-context.json`。
- Durable owners：README、requirements 文档、`.trellis/spec/**`、canonical/dogfood workflow、canonical skill package、companion runtime、registry/interface/schema、preset installer、overlays、platform entries 与 manifest。
- 提交证据：`task-commit-plans/001.json` 至 `005.json`、五个真实 commit objects、parent/message/path/tree/blob/mode，以及 working-tree post-result。
- Review 证据：Round 1-5 全部 raw reports、当前 `agent-assignment.json` 与旧 `review.md`/`review-gate.json` metadata tail。

## 需求与验收结论

| 范围 | 结论 | 说明 |
| --- | --- | --- |
| R1 / AC1 | 通过 | `guru-create-work-commit` 保持 reserved tombstone；`guru-create-task-commit` active，公共 interface/schema/command 已登记。 |
| R2 / AC2 / AC8 | 通过 | canonical/dogfood workflow 各有 1 个 mandatory invocation、3 个唯一 typed-exit consumer；五次提交使用递增 sequence 与 fresh HEAD/Phase 2。 |
| R3 / AC5 | 阻断 | dirty snapshot 未绑定 unstaged gitlink 的 worktree commit OID；B 切换为 C 后 artifact 仍被判 fresh，见 `F-06-02`。 |
| R4 / AC3 / AC4 | 通过 | standalone trigger、task-local candidate、message bytes/digest、AI review、authorization 与 candidate mode 均已落地。 |
| R5 / AC6 | 阻断 | 普通文件、delete、rename、pathspec 与 unrelated preservation 有覆盖，但 gitlink 可提交未被 candidate 绑定的 revision，见 `F-06-02`。 |
| R6 | 阻断 | executor 未识别正在进行的 Git sequencer operation，未触发确认或 fail-closed，见 `F-06-01`。 |
| R7-R8 / AC7 | 阻断 | shared parser、literal exact stage、tree/blob/mode postcondition 本身成立，但 `CHERRY_PICK_HEAD` 可被错误消费并返回 `committed`，gitlink freshness 也可绕过。 |
| R9 / AC9 | 阻断 | workflow 仍复制完整 work subject/body 模板，回归只扫描平台 entries，见 `F-06-03`。 |
| R10 / AC10-AC11 | 阻断 | 本地 package/install/update/throwaway 命令全部通过，但永久测试没有覆盖 `F-06-01`、`F-06-02`，也没有拒绝 workflow 模板回流；不能形成最终验收。 |
| AC12 | 按合同 pending | remote exact feature-ref marketplace verifier 只能在 reviewed content push 后由 `trellis-finish-work` 执行；当前没有冒充通过。 |
| AC13 | 通过 | `close_issues=[122]`；#92、#120 仅在 `related_issues`；五个 work messages 只使用 `Refs #122`。 |
| AC14 | 通过 | public package/schema/example/manifest/docs 与五个 plans 未发现 secret、客户数据、`.env` 内容、签名 URL或本机绝对路径。 |

## 五个提交审计

| Sequence | Commit | Parent | Message | Exact paths | Tree | Blob/mode 与 result |
| --- | --- | --- | --- | ---: | --- | --- |
| `001` | `afcab193` | `6b9495a`，匹配 | raw bytes/digest 匹配 | 102/102 | `756b92b6` | 102 个 snapshot-to-commit path identity 全匹配；working result 是已披露的 pre-tree-evidence legacy shape。 |
| `002` | `03e813c5` | `afcab193`，匹配 | raw bytes/digest 匹配 | 31/31 | `3ee42799` | 31 个 expected/actual blob+mode 与真实 tree 匹配，result validator 无错误。 |
| `003` | `1534b545` | `03e813c5`，匹配 | raw bytes/digest 匹配 | 26/26 | `ea1a7b39` | 26 个 expected/actual blob+mode 与真实 tree 匹配，result validator 无错误。 |
| `004` | `ce705679` | `1534b545`，匹配 | raw bytes/digest 匹配 | 9/9 | `3fe4c13a` | 9 个 expected/actual blob+mode 与真实 tree 匹配，result validator 无错误。 |
| `005` | `163e641` | `ce705679`，匹配 | raw bytes/digest 匹配 | 9/9 | `a7da3914` | 9 个 expected/actual blob+mode 与真实 tree 匹配，result validator 无错误。 |

五个 commit 中的 candidate blob 均保持 `result.status=planned`，committed plan digest 匹配；当前 working-tree plan 记录真实 post-result。`check-task-commit-plan.sh --range origin/main..HEAD` 对 5/5 messages 返回 `errors=[]`。当前 HEAD 保持 `163e641`，staging 为空，source checkout `main...origin/main` clean。

## 问题生命周期

- Round 1：`trellis_final_review_122_01` 发现 1 个 P1、2 个 P2，成为 finding owner。
- Round 2：同一技术身份仅以 `问题闭环审查代理` 复用；关闭 hook same-path 与 literal path finding，但发现 result state matrix 的新 P2。
- Round 3：确认 schema/runtime 行为修复，但发现永久测试缺少完整 7/15/12 cross-product 的 P2。
- Round 4：确认共享 7/15/12 matrix 落地，但发现 path/aggregate tamper 可被其它错误掩蔽的 P2。
- Round 5：同一 finding owner 仅做 closure，`findings_count=0`，C-01-T1/C-01-T2 均关闭；该技术身份没有成为最终放行代理。
- Round 6：本代理 `trellis_final_review_122_02` 此前未出现于任何 `review_rounds[]`，满足 fresh new-agent 条件；本轮对完整当前 diff 新发现 3 个阻断 finding。因此本代理成为新的 finding owner，不能作为后续最终放行代理。

Round 1-5 在派发本轮前满足 closure-before-final；本轮新 findings 使 Branch Review Gate 必须重新进入 implementation、完整 Phase 2、fresh sequence commit 与 closure 流程。

## 阻断问题

### F-06-01（P1）：executor 会把正在进行的 cherry-pick 错误消费为普通 task commit

- 位置：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:9861`、`:10345`、`:10447`。
- 事实：candidate validation 与 executor 在 staging/commit 前没有绑定或拒绝 Git operation/sequencer state；只检查 branch、HEAD、dirty snapshot 与计划证据。
- 独立复现：在有效 `CHERRY_PICK_HEAD` 存在的 throwaway repo 中创建 schema-valid、AI-reviewed candidate。candidate validation 返回 `errors=[]`；executor 调用 `git commit --cleanup=verbatim -F` 后返回 `status=committed` / `exit=committed`，创建单父 commit，并清除 `CHERRY_PICK_HEAD`。
- 影响：Skill 会接管并终止用户正在进行的 cherry-pick，把 sequencer state 误判为普通 task work commit。它绕过 R6 的 dangerous-operation confirmation/fail-closed 边界，可能破坏原 cherry-pick 意图与恢复现场，同时给出虚假的成功 typed exit。
- 修复要求：candidate artifact 与 executor 必须在任何 stage side effect 前、以及 `git commit` 前重新绑定 objective repository-operation state；对 merge/cherry-pick/revert/rebase/sequencer 等非普通提交状态返回 `blocked` 或按 Markdown human-confirmation policy 停止，不得直接消费。新增真实 Git operation state 的永久负向回归，证明 HEAD、sequencer marker 与 index 均保持未被 executor 改写。

### F-06-02（P1）：unstaged gitlink 的 worktree OID 未进入 dirty snapshot，可提交未审查 submodule revision

- 位置：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:9768`、`:9783`、`:9821`、`:10417`。
- 事实：`task_commit_worktree_identity()` 对目录直接返回 `(None, None)`。对于 mode `160000` 的 submodule path，snapshot 只记录旧 index gitlink OID，`worktree_sha256=null`，没有记录当前 submodule HEAD。
- 独立复现：superproject index 指向 A，AI candidate 在 submodule worktree 指向 B 时生成；随后只把 submodule checkout 切到 C。切换前后 `dirty_snapshot` 字节和 digest 完全相等，candidate validator 返回 `errors=[]`，executor 最终提交 C，而非 AI-reviewed B，并返回 `committed`。
- 影响：完整 dirty snapshot、evidence freshness 与 exact stage content binding 对 gitlink 不成立。并行进程或用户可以在 AI review 后替换 dependency revision，Skill 仍提交未审查的 submodule commit；这是依赖完整性与供应链边界上的错误成功。
- 修复要求：识别 index mode `160000`，确定性读取并绑定 worktree gitlink HEAD 及必要的 initialized/dirty 状态；无法取得唯一安全 identity 时 fail closed。executor stage 前必须重新比较该 identity。新增 A/B/C 真实 submodule 回归，要求 B->C 变化使 candidate stale，且不得 stage/commit C。

### F-06-03（P2）：workflow 仍复制 work commit 详细模板，R9/AC9 的 SSOT 收敛未完成

- 位置：`trellis/workflows/guru-team/workflow.md:164`、`.trellis/workflow.md:164`、`trellis/skills/guru-team/tests/test_skill_packages.py:103`。
- 事实：canonical 与 dogfood workflow 的 `Commit Message Contract` 仍在 `164-214` 完整定义 work subject shape、type/scope、固定 `背景/变更/边界/验证` body 与 `Refs` footer。Phase 3.4 同时声称 global workflow 只拥有 mandatory invocation、typed exits 与 repeat route。
- 合同冲突：live #122 的“SSOT 收敛与删除重叠实现”和 task R9 明确要求从 canonical/dogfood workflow 删除 work subject/body 详细模板，只保留 mandatory invocation、typed-exit route、repeat/fail-closed 与最终 branch validator 引用。现状保留两个语义 owner：workflow 模板与 canonical package/reference。
- 测试缺口：`test_platform_entries_only_route_task_commit_skill` 只扫描五个 platform continue entries，没有扫描 canonical/dogfood workflow，所以模板回流不会导致 regression failure。
- 影响：后续修改 work-message contract 时 workflow、package reference 与 shared parser 可能漂移；当前 AC9 的“contract tests 拒绝 workflow 重新复制模板”并未实现。
- 修复要求：从 canonical workflow 移除 work-commit step-local format prose并同步 dogfood；只引用 stable skill/durable validator contract。保留 metadata/merge 的独立全局 owner时也应清晰分界。扩展永久测试，直接拒绝 canonical/dogfood workflow 出现完整 work template、direct task `git commit` 或第二套 parser。

## 文档单一来源（Docs SSOT）

- Approved strategy：`ssot_first`，docs state=`partial_docs`；requirements、README、workflow/preset/spec、package contract、runtime/schema/test 与 installer 是本任务 durable owners。
- Initial 与 Round 1-5 task deltas已写入 durable docs，failure-stage 7/15/12 matrix、derived mutation、managed-hash distribution 与 upgrade/reapply 证据一致。
- `F-06-01`、`F-06-02` 是当前 task 的 entry/snapshot/executor/postcondition 范围，不是 out-of-scope follow-up；当前 durable docs/tests 尚未定义并证明这两个边界。
- `F-06-03` 直接否定 implementation handoff 与 Phase 2 对 R9/AC9 的“workflow 只路由、不复制正文”结论。Docs SSOT 因此不是当前可放行状态，必须在实现修复时按 approved strategy 同步 durable owner与回归。

## 验证结果

| 检查 | 结果 |
| --- | --- |
| Targeted executor/candidate | `18/18`，7.280s，`OK`。 |
| 六个 package roots | 各 `4/4`，合计 `24/24`，全部 `OK`。 |
| Package/runtime/preset full suite | `496/496`，129.436s，`OK`。这些现有 tests 未覆盖本轮 3 个 findings。 |
| 独立边界 probes | Cherry-pick state 被错误消费并返回 committed；gitlink B->C snapshot 相等且实际提交 C，均稳定复现。 |
| Source/installed validation | 均 passed；reserved=1、active=1、invoke=1、exit=3；dogfood managed files=43，conflict/removal/sidecar=0。 |
| Canonical/dogfood/platform equality | 6 个 package roots x 8 files 无 mismatch；canonical/dogfood runtime 与 workflow byte-equal。 |
| Clean throwaway | exit 0；覆盖 public discovery + local unpublished sample、fresh install、initial/finding-fix commits、old-plan reject、`trellis update`、workflow/preset reapply、source/installed、drift、closeout smoke 与 recursive sidecar。 |
| Commit objects | 5/5 parent/message/path/planned plan digest 通过；所有 177 个逐路径 identity 检查通过。 |
| Static | branch/dirty `git diff --check`、Python compile、changed Bash syntax、changed JSON parse 全部通过。 |
| Workspace hygiene | Reviewed HEAD 未变，staging=0，source checkout clean，recursive `.new/.bak=0`；本报告前只有 23 个 task-local metadata dirty paths。 |

## 安全与部署影响

- Public added-line scan：private key、credential URL、高置信 token、机器用户绝对路径、signed URL 均为 0；五个 task plans 的机器路径与 secret-like field 均为 0。
- 当前 107-path diff 未修改 `.github/workflows`、Dockerfile/Compose、Kubernetes/Kustomize、Helm/chart、database migration 或 Makefile；5 个带 `overlays/` 的路径都是 Guru Team 平台 prompt/skill overlays，不是部署 overlay。
- 无需应用部署、容器发布或数据迁移同步。当前阻断属于 task-commit Git 状态、dependency identity 与 workflow SSOT 完整性；在修复前不得 publish。

## 观察项

1. Remote exact feature-ref marketplace verifier 仍按合同保持 pending。它必须在 reviewed content push 后由 `trellis-finish-work` 完成，当前既不是本地 finding 的替代证据，也不能满足 publish readiness。
2. Sequence `001` 由 tree-evidence public contract 收紧前的旧 executor 生成，working result 不符合当前 result schema；既有 Phase 2/Review 已明确保留该历史事实而不伪造 post-hoc expected tree。本轮使用原 snapshot 与真实 commit object 重建 102 个 path 的 blob/mode，全部匹配。这是已披露的 task-history limitation，不新增为本轮 finding。
3. 本地兼容基线仍为 Trellis CLI `0.6.5`；throwaway 显示 npm 可用更新版本，但 #122 未授权扩大 compatibility target。

## 后续候选

无。`F-06-01`、`F-06-02`、`F-06-03` 全部属于 #122 已批准的 R3-R10 / AC5-AC11 范围，不能降级为 observation 或另开 follow-up 来通过当前门禁。

## 结论

- `findings_count: 3`。
- 优先级：P0=0、P1=2、P2=1、P3=0。
- `final release pass: 否`。
- 结论：`blocked`。
- 本轮通过的 unit/full/throwaway/source/installed/drift 结果不能反证未覆盖的 Git operation、gitlink freshness 与 workflow SSOT 缺口。
- 必须返回 implementation，修复 3 个 findings，完成新的完整 Phase 2，以 fresh `task-commit-plans/<sequence>.json` 创建后续 work commit，再由 finding owner执行 closure review。由于本代理已发现问题并成为 finding owner，本代理及任何 closure agent均不得成为后续 `最终放行审查代理`；所有 findings关闭后必须再派发此前未参与 review rounds 的 fresh new-agent，对新的完整 `origin/main...HEAD` 执行最终放行审查。
