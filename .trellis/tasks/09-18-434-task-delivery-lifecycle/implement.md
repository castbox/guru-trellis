# Implementation Plan: #434 Task Delivery Lifecycle Global Activation

## Preconditions

- [x] Fresh reread #434/#435/#436/#443 live Issue authority；合同版本为 `2026-09-18-r4`。
- [x] #434 branch 于 2026-09-26 fast-forward 至 `origin/main@bab8cfcd534692735b9240b25dd8bc63e40a5cb4`；PR #473/#474 的 D443/D436 canonical majors 均已合并。source inventory 为 32 active packages / 149 exits / 102 commands、旧生产 22/98；六个 #454 IDs 仍 planned，不是可用 package。退役 5 个 predecessor packages（21 exits / 22 commands）并激活 7 个 E434 packages（27 exits / 24 commands）后，目标 inventory 派生为 34/155/104，不将该计数另立为 authority。
- [x] Architecture/RDT current 为 `.66/active`，不是原规划的 `.56`；旧 planning 草稿已恢复，旧 1.0 schema/test 修改仅保留在可恢复 stash，未覆盖新 major。
- [x] Phase E434 六个 reserved ID 与独立 `guru-create-issue` 已有完整 canonical package；七包定向 unittest `19/19`，组合 source validator 为 34 active packages / 155 exits / 104 commands。候选唯一 consumer 测试 `3/3`，D443/D436 定向 package tests 已过；旧 `39/126` 仅是切换前 source-only 快照。
- [x] 旧前驱四类失败已按版本处置：旧 Publication/Merge exit 断言、旧 Finish fixture 改由新图唯一路由/跨代 seal 和退役断言覆盖；eval discovery 与两个旧 terminal eval 执行案例属于 pinned-old Finalizer corpus，不将旧 DTO 移入新图，也不把先前 staging 的 `canonical_package_set_mismatch` 当作 Finalizer pass。固定 `bab8cfcd` 的完整旧图和现行完整新图均通过图检查，两个混图均拒绝；旧 terminal eval 本次未在 pinned-old 安装中运行。旧 #154/PR #156 的 terminal preflight 既有 7 tests 结果不等于业务仓发布证明；本地旧修复 HEAD `0f39af9c` 未 push。
- [x] installer 经三处旧 Finalizer 本地 digest drift 审查后移除待退役文件；511 个 managed backups 经二次 apply 恢复。两个新包的命令/Interface validator 一一绑定后，34 包 installed 校验为 0；22 个 overlay 入口已切新图，3 个 overlay backups 经修复的 recovery 路径清零。仍需完成广义测试、代表性 clean install 和全部图负例，不能据此宣称最终 gate 通过。
- [x] Planning Architecture `baseline_current` 已批准 target-native contribution path。
- [x] 已识别旧链在途实例 `castbox/ai-chat-roleplay-backend#154` / 旧 PR #156；仅提供 pinned compatible old version 完成或按 exact task/PR/remote/local/base/Finalizer facts 逐项人工处置，不扩展 current runtime，也不把 prepared preview 当作可执行证明。业务仓资源保持不变。
- [x] 旧 Finalizer 普通首次发布预览与执行共用 terminal-PR/remote preflight；终态 PR 预览拒绝测试及 recovery suite `49/49` 通过。未在 #154 业务仓执行写入或复现。
- [x] 组合候选：source/installed validator 均通过（34 active、104 commands；33 mandatory invokes、153 production exits），caller inventory、旧/新完整图和混图负例、installer 87/87、lifecycle 137/137、package 20/20、当前集成 18/18、upgrade contract 73/73、#434 图 5/5、task validate、dogfood drift、workflow byte parity、`git diff --check` 通过；reapply 后无 `.new/.bak`。
- [x] 代表性 Codex clean/focused：exact Trellis fork `eb370008` 的临时构建，本地候选 workflow 样本 + preset、原生入口、两次 update/reapply 和 session binding probe 通过。`local_workflow_sample=true`；远端 marketplace 安装不是本任务验收项，完整多平台 Release matrix 与 predecessor upgrade **未验证**。

## Coordinated Planning And Gate Hold

- Planning approval 后 #434 task 已进入 `in_progress`；不得用此状态替代 source package-ready、installed 或 graph gate。
- 不在 #443、#436 或 current authority 不一致时执行 package-ready gate、修改 production workflow 或开始 Step 1。
- #435/#436/#443 历史 capability 与 #454 D443/D436 canonical majors 已合入；在同一个 selected base 核对 exact selector/exit/consumer，不将历史闭环测试误称为现行 major 的安装通过。
- #434 branch 已与 selected base 对齐；组合 package-ready gate 只能在该 checkout 上运行，不能复用 child worktree 或历史 PR 的结果。
- #454 Phase E434 明确由本任务交付 `guru-activate-task`、`guru-create-task`、`guru-ensure-task-checkout`、`guru-establish-task-branch-binding`、`guru-establish-task-identity`、`guru-rebind-task-branch` 的完整 canonical packages。不得以 planned row 代替 package，也不得复制旧 `task_workspace` mapping 语义。
- #435 的当前 merged identity 为 PR #437 head `4b9e65dbfce9ce4ec4299b2085789acc4f12276c`、merge commit `bf7a5213ddb9b4fb258778cb66bf5645551943ff`；这些 identity 是下一轮 freshness 输入，不是长期硬编码的 activation authority。

## #443 Session Binding Activation Dependency

- D443 `guru-bind-task-session` 的六个非阻断 exits：`session_resumed`、`session_rebound`、`task_switched`、`reactivate_rebound`、`session_manually_recovered`、`explicit_task_mode`，以及 `binding_blocked` stop，均必须在 activation inventory 中出现。
- #434 只消费 #443 的 route schema、freshness/lifecycle generation 和唯一 workflow/stop consumer，不复制其 runtime binding/rebind/switch/manual-recovery 语义。
- Session Binding 与 Reactivate/Completion/Finish/Cleanup 的 cross-generation 关系必须在 mixed-graph negative tests 中验证；当前旧 graph 不提前接入任何 #443 marker。
- 任何 #443 exit 缺失 consumer、出现第二 consumer、或其 current authority cardinality 不等于 live registry 时，activation fail closed。

## Step 0. Complete #454 Phase E434 Package Owners

- `guru-create-issue` 独立消费已审核 `proposed_draft`，创建后 live reread，再经 Sync/fresh Intake；只读恢复不得重复创建 Issue。
- `guru-create-task` 只消费 `existing_issue | standalone_request`，复用 C6 creation composition，审查 adopt/provision、source、TaskId、generation 0、branch/ownership 与 session result；不创建 Issue，结果丢失只读恢复。
- `guru-establish-task-identity` 只处理 legacy TaskId/source 需要 fresh judgment 的边界；`guru-establish-task-branch-binding` 使用 C4/C5 candidate 与 owner-preserving transaction；`guru-ensure-task-checkout` 消费已有 binding、live Git 和唯一 checkout resolution；`guru-rebind-task-branch` 只在已审核 stable boundary 调用 C4 rebind transaction。各自不得读取旧 mapping 作为 authority。
- `guru-activate-task` 只在 Planning approval 的 current input 与 C6 `prepare_activation_inputs` 通过后执行 `planning -> in_progress`，结果丢失只读重建，不让 Approval 顺带改变 status。
- 当前 Fixed Fork `task.py start` 的 `_record_start_state` 仍同时填充 legacy `task.json.branch`；新激活 owner 不得调用它来实现 status-only transition。候选切换时定向验证不写入 legacy branch 字段，并保留官方 session pointer 的独立边界。
- 六个 reserved IDs 加独立 Issue owner 各有完整 public input/typed exits、consumer/projection、schema/example、命令、封闭 runtime、package-local tests、source validation；正常创建、no-Issue、唯一/多候选、output loss、跨 generation stale、repo/HEAD mismatch 的定向测试证明不制造重复副作用。没有完整 package 时保持 `planned`，不提前改 active selector 或安装投影。

验证：七包定向测试、34/155/104 source validator 和候选唯一 consumer 检查已通过。已进入单一 activation change set 的实现与验证阶段；任何广义测试或安装负例未闭合时不得提交为已激活版本。

## Step 1. Freeze Activation Inventory

- 从 live registry 派生 current package/exits/commands/workflow targets 基线。
- 读取 #435/#436/#443 每个 `interface.json`，固定精确 Interface selector、profile、exit、consumer、projection 和 command ids。
- 建立 activation inventory fixture，包含 expected new active set、retired set 和唯一 graph edges。
- 验证所有 child packages（含 #443 binding package） 在 canonical `trellis/**`、installed `.trellis/**`、Shared/Codex/Claude/Cursor 均存在且内容一致。
- 六个 #454 stable IDs、独立 Issue owner 及 D443/D436 canonical major 现已投影到同一 candidate；34/0 active/planned、33/153 workflow 是本次组合候选的派生计数。其可发布性仍取决于完整定向验证。

验证：package-local contract tests、registry/interface closure、manifest source identity、platform actual-load smoke。

## Step 2. Add Task-Owned RDT And Architecture Contributions

- 新增 `docs/requirements-design-test-contributions/434-task-delivery-lifecycle/` 的 requirements/design/test/traceability/manifest。
- 新增 Architecture contribution，覆盖 before/after、owner、edge retirement、compatibility exit、project-check concerns。
- 按 Architecture owner 结论新增或更新 ADR 候选；不直接写 shared current identity。
- 将 task planning 中的 graph/interface/acceptance ids 映射到 contribution traceability。
- contribution 必须继承 `.66`，并追踪旧 archive 按来源 Issue 发现和 #154 旧终态 PR 在途处置的明确边界。

验证：RDT contribution schema/trace closure、Architecture change-contract concern coverage、无 shared-current 并行写入。

## Step 3. Rewrite Canonical Global Graph

- 修改 `trellis/workflows/guru-team/workflow.md`，接入 Delivery、Completion、Closure、Finish、Cleanup、Reactivate owners。
- 为 Completion 和 Reactivate exits 增加唯一 workflow/stop targets，写明真实 owner 行为。
- 删除旧 Publication -> Finalizer -> Merge -> Restore 生产 markers 和 archived read-only closeout chain。
- 更新 Phase/continuation/confirmation/docs/Architecture routing 文字，使 task 在 Delivery cycles 中保持 active。
- 更新 `trellis/workflows/guru-team/README.md` 的图、入口、恢复和迁移说明。

验证：workflow marker parser、unknown/multiple/unmapped/dangling consumer negatives、new graph exact-edge fixture。

## Step 4. Activate Registry And Extension Bundle

- 将 #435/#436/#443 packages 纳入 integrated active registry。
- 从 active registry 移除 `guru-create-task-workspace`、`guru-review-task-publication`、`guru-finalize-task`、`guru-merge-task-pr`、`guru-restore-archived-task`。
- 同步 canonical extension manifest、schema/example/command inventories、production-current manifest 和 derived cardinality assertions。
- 删除旧 current-only consumer schemas、fixtures、adapters 与 manifest entries；历史 docs/evidence 保留。
- 确认每个新 exit 只有一个 consumer，每个 consumer input 只由声明 projection 产生。

验证：source registry/interface/extension closure；旧 active id/exit/schema selector 零命中（历史目录除外）；new package closure 全通过。

## Step 5. Update Existing Cross-Phase Owners

- 应用 #435 已交付的 Planning/Check/Commit/Branch Review delivery-policy contracts，不复制第二 owner。
- 更新 Branch Review success projection 到 Delivery Review。
- 更新 Reconcile 的 resume targets，使多个 Delivery cycle 和 delivery 间 base evolution 回到正确 owner。
- 更新 Architecture stage table：Delivery Review/Publish/Merge、Completion/Finish 必须消费对应 current/no-change 或 promoted authority；Cleanup 不重新做 Architecture judgment。
- 更新 manual Git/GitHub boundary，确保独立操作不伪造 Delivery/Completion/Finish result。

验证：A/B first-slice chain、base-advance chain、finding routes、semantic output-loss fresh rerun、deterministic output-loss owner recovery。

## Step 6. Install And Project

- 运行 Guru preset apply 同步 `.trellis/workflow.md`、`.trellis/guru-team/**`、`.agents/.codex/.claude/.cursor` 投影。
- 更新 preset README、overlay inventory、extension version/release notes 和 template hashes。
- 处理所有 `.new`/`.bak`，不得将其留作通过状态。
- 运行 dogfood overlay drift 和 source-installed byte/interface parity。

验证：preset apply/reapply、zero drift、executable mode、four-platform actual-load、workflow source/dogfood byte equality。

## Step 7. Lifecycle Integration Matrix

### Delivery cycles

- first PR、existing PR、Draft/Ready、equal-head binding loss、merge result loss、provider blocker解除。
- A/B scope 先 A 后 B，第一次 Delivery 后 active/Open，第二次后 Completion。
- base evolution/conflict、resolved merge commit、remote branch 删除/重建、历史 PR 跨 branch discovery。
- 所有 Delivery PR Refs-only，bookkeeping PR 不进入 discovery。
- 旧归档按 Issue 检索先发现候选再校验 TaskId/source/Git archive identity；旧 Finalizer residue 不是已完成 archive。

### Completion and finish

- 七个 Completion exits 逐一到唯一 consumer。
- Issue close/no-mutation/output-loss。
- Finish bookkeeping allowlist、expected head、目标基线 archive identity、无业务代码夹带。
- Cleanup retry 不撤销前序结果，旧 Finish success 不能清理 Reactivate 后资源。

### Reactivate

- 原资源复用与新资源准备。
- `reactivated_to_planning` 到当前 Planning owner，以及 session recovery、same-transaction resume、source correction 与 blocked 四个现行出口；受影响的需求/实现/验证在 Planning 后按 fresh judgment 路由，不从 Reactivate 直接伪造旧五路 DTO。
- 有业务变更的新 Delivery；只补验证无空业务 PR。
- 同月 archive 更新、跨月旧 archive 删除+新 archive、旧格式正常 archive。
- duplicate task、active/archive 双副本、旧 PR 复用、未正常结束 residue 均 fail closed。
- schema 1 与旧 schema 2（task metadata 尚无 `lifecycle_generation`）正常完成的 archive 以当前基线中的唯一 Git 归档提交、TaskId/代次/终态及未完成 Finalizer residue 校验；有显式代次的新 schema 2 必须经过 C5 Finish seal/manual receipt。旧 `scope` 来源通过共享 `task_source()` 读取，审核后的 source correction 与后续事务恢复均需重验，不能把 `status=completed` 单独当作 seal。

## Step 8. Atomicity And Migration Tests

- 对每个 required package/interface/consumer/manifest/projection 分别制造缺失或旧版本 fixture，确认 activation fail closed。
- 验证旧完整图 fixture 仍可运行；新完整图 fixture 可运行；所有 old/new mixed edge fixture 均失败。
- 验证没有旧 DTO -> 新 lifecycle result projector、adapter、dual-reader 或 fallback。
- 验证 legacy in-flight 文档只给 pinned old version/manual route，不生成 runtime migration state。
- 对 #154 的 merged old PR、旧 remote head 与本地 reviewed head 分叉、Finalizer prepared preview/terminal PR 执行拒绝做一致性案例；只记录业务仓 live facts，不修改业务仓资源。

## Step 9. Durable Authority Reconciliation

- RDT owner 审查 task contribution并 serialized promotion 到 current RDT authority。
- Architecture owner执行 Phase 2/Branch Review contribution review、必要 ADR acceptance 和 expected-current promotion。
- 更新 `.trellis/spec` 最小 projection、architecture current/domain/integration/GAP/roadmap/evidence 和 RDT version docs。
- Promotion-created diff 必须重新执行 Phase 2、Task Commit 和独立完整 Branch Review。

## Step 10. Validation Commands

实现时从 repository current scripts 发现具体命令；最低集合：

- package-local tests：所有新增/修改 packages；
- source/installed registry-interface-extension closure；
- workflow graph/consumer/target/cardinality checks；
- production-current manifest tests；
- Delivery/Completion/Finish/Reactivate/Session-Binding integration suites；
- canonical/dogfood/installed parity；
- Shared/Codex/Claude/Cursor actual-load；
- preset apply + reapply + dogfood drift；
- task validation；
- `git diff --check`；
- 一个代表性 clean throwaway 安装，验证本地 canonical workflow 样本与 preset 开箱即用；不验证远端 marketplace。

完整多平台 clean/existing/update/reapply/release-candidate matrix 不属于普通 #434，记录为专门 Release Gate 的未验证边界。

本轮 finding-fix 候选：Reactivate 25/25、两个资格包分别 23/23 与 24/24、Release Skill 8/8、当前 Delivery/Finish 集成和图检查 25/25、source/installed validator 与 dogfood drift 通过；installed-entry canonical/本地投影 2/2。五份 canonical workflow spec 已把旧 Publication/Finalizer/PR Merge/Restore 约束标为 pinned-old，并重新投影 dogfood；`test_434_workflow_prose` 对当前规范图与 #443 身份边界新增回归。installer/upgrade 160/160、throwaway Python routing 45/45、当前 checkout-boundary launcher 2/2 分别通过；后两套原先仍以退役 Finalizer/start-task 入口为当前 fixture，现已改为当前资产及明确历史边界，未用 skip 伪造通过。连续两轮新鲜独立审核仍待完成，未提交候选不得称正式 Branch Review pass。

首轮新鲜只读审核发现两项正常路径 P2，连续无 finding 计数归零：linked worktree 新任务仅写入 acquired checkout 时，`guru-ensure-task-checkout` 从调用者 checkout 过早读取 TaskId；项目级 `.trellis/spec/workflow/index.md` 把旧图称为当前。现行 resolver 改为先按共享 binding/ownership 定位唯一 registered checkout，再从该 checkout 校验 TaskId、代次和状态；共享 identity helper 保留自身 `task_not_found` 错误码。正常跨 checkout 正例与缺失 artifact、stale generation 负例均通过。项目级索引保留本仓 Checklist，改为当前 owner/计数和明确历史边界；它不是 preset managed spec，未将其覆盖到其他项目索引。组合 installer/upgrade/routing/launcher 单次 207/207，修复后 checkout 4/4、shared lifecycle 137/137、#434 图/规范 10/10、apply/reapply、source/installed、dogfood drift、零 sidecar 与 `git diff --check` 通过；两轮全新审核仍待重新开始。

重新开始的首轮审核又发现两项有效问题，连续计数仍为零：真实旧 schema-2 归档（如本仓 #333）无 C5 ledger，被 Reactivate 当作新 Finish 阻断；installed Skill Package 规范仍称退役 Workspace 为当前 Intake owner。Reactivate 现仅将缺失 `lifecycle_generation` 的旧 schema 2 与 schema 1 走 committed unique archive/terminal/old Finalizer residue 验证；显式代次 schema 2 仍要求 C5 seal 或 manual receipt。schema-1/2 正负与 source-correction/recovery 测试 31/31，#333 真实归档的只读 `archived_identity` 成功；canonical Intake 条款已标 pinned-old 并投影，#434 图/规范 11/11、source/installed 与 dogfood drift 通过。新一轮连续独立审核尚未开始；本候选没有提交或推送。

下一轮首位全新只读审核确认一项 P2，计数再次归零：本仓真实 #237 旧 schema-2 归档的 `scope: GitHub Issue #237` 非 URL 格式，原 `task_source()` 使按 Issue 检索和 Reactivate 来源修正被跳过。共享解析现只在明确仓库上下文下接受精确 `GitHub Issue #N`，按 Issue 检索须匹配 GitHub origin；来源修正及跨 checkout 恢复携带经审核的旧来源仓库。identity/source/Reactivate 50/50，真实 #237 的只读 Issue 发现返回唯一归档；两次 apply 后零 sidecar/backup、source/installed 与 drift 通过。修复后的 installer/upgrade/routing/launcher 207/207、shared lifecycle 138/138、#434 图/规范 11/11、task validate 和 `git diff --check` 通过。连续两轮全新只读审核仍待重新开始；本候选未提交或推送。

重新开始的首位全新只读审核确认一项 P2，连续计数归零：目标 TaskRef 尚未创建时，checkout resolver 误把无关活动任务 A 视为任务 B 的 authority conflict，挡住 A 的首轮 Delivery 后另开 B 的正常路径。移除该泛化阻断，仅校验目标 TaskRef 不存在；`prepare_creation_inputs()` 继续校验所有注册 checkout 的目标 TaskId/TaskRef 与未解决 ledger 唯一性。adopt/provision 和 creation 定向回归 49 通过、1 项 Fixed Fork 显式源环境跳过。managed 旧 resolver backup 经二次 apply 恢复，source/installed、dogfood drift 和零 sidecar 通过；修复后 installer/upgrade/routing/launcher 207/207、shared lifecycle 138/138。重新两轮独立审核待开始。

下一轮首位全新只读审核又确认新 Issue owner 的两项 P2，连续计数归零：不确定创建结果只按内容检索会认领审核前同内容旧 Issue；合法标签名经 GitHub 规范大小写后回读会误拒。`guru-create-issue` 现以 UTC `reviewed_at` 限定创建/恢复的 `createdAt`，同一 review 时间用于只读恢复；标签按大小写无关集合身份匹配。包本地 5/5，未新建真实 GitHub Issue。二次 apply 消费 18 个旧 managed backup 后，source/installed、dogfood drift、零 sidecar 通过；修复后 installer/upgrade/routing/launcher 207/207、lifecycle 加 Issue 143/143。重新两轮全新只读审核待开始。

再一轮首位全新只读审核确认时间精度 P2，连续计数仍为零：亚秒 `reviewed_at` 与 GitHub 秒级 `createdAt` 直接比较会拒绝实际创建成功的同秒 Issue。创建动作现在等到审核后的下一整秒，再对创建回读和只读恢复统一使用该下界；未来审核时间在立即窗口之外先刷新 review，不能盲等或创建。旧同秒 Issue 不可认领，同秒审核后下一秒新 Issue 可认领，定向包测试 8/8。组合 gate 和投影重验仍待执行，未创建真实 GitHub Issue。

本轮组合重验：preset apply 第一次生成的 11 个 managed `.bak` 经逐项 diff 确认为本次 Issue 包旧候选，第二次 apply 消费；最终 installed/source validator、dogfood drift、四平台本地 Skill/Interface 与 installed runtime 字节一致、零 sidecar、task validate、`git diff --check` 通过。installer 87/87、upgrade 73/73、routing 45/45、launcher 2/2 合计 207/207；#434 图/规范 11/11、共享 lifecycle unittest 138/138、广义 lifecycle/Issue/Reactivate pytest 199 pass/1 个源环境 skip。现行集成宽扫初次 69 项出现旧图测试漂移（退役包、23 包计数、旧 Finalizer 文案和旧 ownership inventory 字段），两份 contract tests 已按新图/descriptor owner 更新，分别 5/5 与 4/4；复跑当前集成 69 pass/1 skip。旧 predecessor corpus 在新源树无法收集，仅能 pinned-old；未以失败或跳过冒充新图通过。连续两轮全新只读审核待执行；未提交、推送、创建真实 Issue 或更改 #154 业务资源。

第一位全新只读审核发现两项正常 P2，连续无 finding 计数归零：迟到数小时的重复检索仍可创建 Issue；Completion current standalone 接受旧 closeout/restore lineage 并可生成 `completed`。前者创建限制为审核后 60 秒内，过期/未来刷新，恢复仍可沿原 review 时间只读检索；后者从 current public schema/runtime 去除旧 lineage，仅接受 Delivery merge result 和当前三个证据槽，旧链仍 pinned-old/manual。Issue 10/10、Completion 16/16 定向通过；组合门禁与安装投影重验待执行，未提交或远端写入。

两项 finding 修复后的组合重验：27 个旧 managed `.bak` 经 diff 确认为本次两包旧候选，二次 preset apply 清零；source/installed validator 34 active/104 commands、153 production exits、dogfood drift、#434 图/规范 11/11、task validate、`git diff --check`、零 `.new/.bak` 通过。installer 87/87、upgrade 73/73、routing 45/45、launcher 2/2 合计 207/207；当前集成 69 pass/1 skip，lifecycle/Issue/Reactivate/Completion pytest 217 pass/1 个源环境 skip。需重新取得连续两位全新只读审核无 finding；未把本地修复或旧 #154 事实称为远端/完整 Release 证明。

重新计数的首位全新只读审核又发现一项 P2：结果不明时，几分钟后协作者创建的同内容 Issue 可能被本次只读恢复错误认领。Issue owner 现对经审核 target identity + UTC review time 生成稳定、非敏感隐藏 body comment；创建回读和只读恢复都要求完整原正文加精确尝试标识，后来的普通同内容 Issue 或不同尝试标识不得认领。Issue 定向 11/11；组合门禁和安装投影重验待执行，连续无 finding 计数仍为零。

尝试标识修复后的组合重验：11 个本次 Issue 包旧 managed `.bak` 经核对由二次 apply 清零；source/installed validator 34 active/104 commands、153 production exits、dogfood drift、#434 图/规范 11/11、task validate、`git diff --check`、零 `.new/.bak` 通过。installer 87/87、upgrade 73/73、routing 45/45、launcher 2/2 合计 207/207；当前集成 69 pass/1 skip，lifecycle/Issue/Reactivate/Completion pytest 218 pass/1 个源环境 skip。两轮全新只读审核须再次从零开始；未创建真实 GitHub Issue 或宣称远端 marketplace/完整 Release matrix 通过。

最新只读审核又确认两项正常路径 P2，连续计数归零：跨上海午夜的 TaskRef 创建可能落到不一致日期目录；Finish bookkeeping 只拒绝旧 trailer 而接受现行 Delivery identity trailer。Create Task 对 reviewed TaskRef 做上海日期预检，并把完整日期前缀交给 Fixed Fork，由官方 create 在日期变化时于建目录前拒绝；结果恢复保持跨日只读。Finish 将现行三种 trailer 纳入旧两种的拒绝集。定向 61 pass/1 源环境 skip，广义 lifecycle 251 pass/1 skip，当前集成 70 pass/1 skip，组合 installer/upgrade/routing/launcher 207/207；source/installed、drift、task validate、零 sidecar 均通过。两轮独立只读审核从零开始。

第一轮新鲜只读审核又发现两项正常路径 P2，连续计数归零：Finish 在 `pr_open` 重入时绕过了 bookkeeping payload 校验，且初次 archive 投影发生在该校验之前；installed graph 只检查声明 marker 是否存在，不拒绝额外的旧 exit/invoke marker。现将 payload 校验前移至任何成功路由的副作用之前，并对每条 parsed invoke/exit 反查当前 registry/interface；定向 Finish 52/52、图候选 6/6。二次 apply 核对并消费 8 个本轮旧 managed backup，最终零 sidecar；组合 installer/upgrade/routing/launcher 207/207、广义 lifecycle 277 pass/1 skip、当前集成 71 pass/1 skip、图/规范 42 pass/1 skip，source/installed、drift、task validate 和 diff check 通过。两轮全新审核重新从零开始。

重新计数的首位全新只读审核又确认两项 P2，连续计数归零：真实 #435 旧归档的 summary Issue 索引为空但已提交 task scope 明确指向来源 Issue，旧候选发现过早排除；真实 #443 旧 schema-2 归档带显式 generation 0 和 retired `archive_dir`，却被当作新 Finish 要求 C5 ledger。发现路径现以已提交 task source 为准、summary index 仅提示；Reactivate 对匹配旧 locator 的显式零代次走唯一 Git 归档与旧 Finalizer residue 校验，其他显式代次仍需新 Finish seal/manual receipt。identity 10/10、Reactivate 35/35；真实 #435 候选与 #443 终态只读探针通过。二次 apply 核对并消费本轮 8 个 managed backup，source/installed、drift、task validate、diff check、零 sidecar 通过；组合 installer/upgrade/routing/launcher 207/207、广义 lifecycle 279 pass/1 skip、当前集成 71 pass/1 skip、图/规范 42 pass/1 skip。两轮全新审核重新从零开始。

随后独立审核再发现两项 P2：旧归档按 Issue 发现只识别 HTTPS 和 scp-style SSH origin，遗漏合法的 `ssh://git@github.com/owner/repo.git`；quality guide 后段仍把退役的 32/142/102 与 22/98 计数称为当前图。identity helper 已补标准 SSH URL，旧归档测试覆盖；canonical quality guide 改为现行 34/155/104、33/153，并补文案回归。定向 17/17 通过，两个 managed `.bak` 核对后由二次 apply 清零。远端 marketplace 非本 Issue 验收；连续无 finding 审核计数从零重新开始。

下一轮全新只读审核确认两项正常路径问题，连续无 finding 计数归零：Approval 在正常投影后删除私有 `planning-approval.json`，Activation 却再读该文件；Reactivate 后仅补验证的新代次没有业务 merge，Completion 又强制同代 merge。Activation 改从当前三份 planning 文档计算审核身份，Approval record/check/invoke -> checkpoint 删除 -> Activation 定向 4/4 通过。Completion 新增受限 `reactivation_validation`，以已核实的上一代终态归档和本代 reactivation/validation evidence 为依据，`evidence_pending` 以同一锚点刷新；普通 Delivery 入口仍绑定同代 merge，旧 closeout/restore/merge 不转入新代次。Completion/Finish 定向 46/46 通过；canonical 尚待统一投影与组合回归。两轮全新独立审核须从零开始。

本轮统一投影后，首次 apply 产生 33 个 Activation/Completion 旧 managed 备份，二次 apply 收敛为 0；dogfood workflow 本地候选字节同步。组合测试识别一个 Completion interface authoring 清单遗漏、一个 recovery matrix 行数断言和一个已改名的 unittest `-k` 夹具；修复后 234 个 lifecycle/包/图、27 个 continuation/package 合同、179 个 installer/upgrade/native-load、47 个 routing/launcher、21 个当前集成及一个源环境 skip 通过。固定 Fork `eb370008` 正常重建并标记构建来源，本地 Codex clean/focused 样本、两次 update/reapply、实际加载与 session-binding probe 通过，`local_workflow_sample=true`；远端 marketplace 与完整 Release matrix 均不属于 #434 验收。

首轮全新只读审核确认一项 P2，连续无 finding 计数归零：Reactivate 只补验证返回 `evidence_pending` 时，interface 的单一 consumer authoring 仅允许 `merge_result`，没有声明 `reactivation_anchor`；此前单元测试手工组装后者而绕过接口。保持单一 exit/consumer，给该 authoring seed 增加独立的 Reactivate 变体元数据，并让投影测试分别组装/验证两种完整输入。相关包与 interface 47/47 通过；修复后的 installed 统一投影、组合重验和两轮新鲜只读审核仍待完成。

当前稳定候选：Approval 的 `approved` DTO 投影已审核 `planning_result_id`，Activation 在 checkpoint 删除后按该值与现行 planning 文件比较；Completion 的 Reactivate `evidence_pending` 备用 authoring 已同步四平台。旧归档与 Stage 0 前驱 eval 固定在旧版本执行，现行图拒绝旧包；Phase 2 和 Qualification eval 的 source/installed package digest 均排除未安装的私有 `tests/`。二次 preset apply 后零 `.new/.bak`、source/installed 34 active/104 commands、33 invokes/153 exits、dogfood drift、task validate 和 diff check 通过。installer/upgrade/native-load 167/167，qualification runtime 20/20、eval adapter 16/16 通过；此前当前集成 21 pass/1 源环境 skip、routing/launcher 47/47 和代表性本地 Codex clean/focused 样本通过。远端 marketplace 和完整多平台 Release matrix 不属于本 Issue 验收。正式 Phase 2、当前候选两轮全新无 finding 审核、提交后完整 Branch Review 与 shared authority 晋升仍待完成；连续计数为零。

最新独立只读审核又指出两项正常路径 P2，连续无 finding 计数归零：Delivery Review 后 `post_publication` Reconcile/Branch Review 仍引用退役的 `task_finalization` target；两个资格包的四个 publication consumer schema 仍只接受旧 Publication owner。canonical 已统一到 `delivery_publication` 和 `guru-review-task-delivery`，并补 unchanged/new-pair/continuity 与生产 profile schema 正反例测试；Reconcile 30/30、Branch Review 35/35 通过。投影首次 apply 产生 69 个本轮 managed `.bak`，尚待二次 apply 消费与组合门禁重验；正式 Phase 2、完整 Branch Review 与两轮全新审核均未完成。

组合测试发现 Completion 为两种 `evidence_refresh` authoring 直接扩展已发布 `skill-interface-1.4`，违反 pinned 旧 schema 字节身份。已恢复 1.4，新增 1.7 并只迁移 Completion 及 current registry/manifest/discovery/eval references；两个资格包的旧 schema 身份测试分别 23/23、24/24 通过。新投影两轮 apply 后零 sidecar，source/installed validator 通过。先前 installer 宽测在 canonical 编辑与旧投影混合时复制 fixture，出现的一次冲突不是稳定候选结果；需要重新跑该夹具及组合 gate。当前连续全新无 finding 审核计数仍为零。

第一位新鲜独立审核确认 P1：preset shared schema 白名单漏掉 1.7，旧 installed 脚本检测还曾让 source-only pass 被误读为安装通过。已补白名单、重投影 extension manifest 与 installed schema，新增从 active registry 推导 schema 文件和 manifest 的安装断言，直接 source-runtime installed validator 通过；先前轮次的审核计数归零。稳定候选的完整 installer/update 回归、正式 Phase 2 和连续两轮全新独立审核须重跑。

修复 1.7 installed 分发后，稳定候选的 installer/upgrade/native-load 181/181、focused gate 62/62、lifecycle/Completion/Finish 217/217、当前图/qualification 宽测 95 passed/1 个源环境 skip 均通过。source/installed 为 34 active、104 commands、33 invokes、153 production exits，零 sidecar；dogfood drift、task validate、diff check 和代表性 fresh Git 本地安装样本通过。两位全新只读 subagent 串行审核当前未提交候选，均未发现 P0-P3（连续 2/2）；这只支持修复质量判断，不替代正式 Phase 2、提交后的完整 Branch Review 或 shared `.66 -> .67` 晋升。旧前驱 corpus 留在 pinned-old 版本，本任务不在新图运行其已退役终态 eval；旧 #154/PR #156 仍只允许 pinned-old 或逐项人工处置，业务仓未写入。远端 marketplace 不属于使用场景或验收，完整多平台 Release matrix 保留给专门 gate。

首次 `origin/main@bab8cfcd...a6b6d633` 完整提交范围的全新只读审核发现两项正常路径问题，连续无 finding 计数归零：Finish 在 Guru-owned linked task worktree 后直接调用 Cleanup，会触发调用目录自删保护；公开 extension manifest 漏报 active Completion Interface 1.7。修复保留 Cleanup 保护，由 global workflow 与 Skill 在同一 Git common-dir 的非删除目标 checkout 调用，缺少保留 checkout 时停止人工处置；manifest 增加 1.7 并同步 data-contracts、installed manifest 和回归断言。直接从 task checkout 调用被阻断、改用 retained checkout 清理成功的正反例通过；定向 installer/图/Cleanup 125/125、qualification eval 48/48、source/installed 及 dogfood drift 通过，两次 preset apply 收敛零 sidecar。此前 Phase 2 与两次未提交候选清洁审核不覆盖新修复，须重新正式 Phase 2、提交、完整 Branch Review 和两轮连续全新只读审核；shared `.66 -> .67` 晋升仍未执行。

下一轮全新完整提交范围只读审核发现一项 P2：Reconcile `post_publication` eval 输入已是 `delivery_publication`，断言却仍指向旧 `task_finalization`。Architecture live authority 回读另发现候选 ADR-012 与 #435 已接受决定重号。已将 eval 与其五份 installed/platform 投影修正，新增覆盖每个 eval resume 断言（保留 post-check/post-commit 的 `phase2` 归一化）的回归；候选决定重编号 ADR-016，保留 shared ADR-012..015，并新增文件名/标题/ID 唯一性回归。两次 preset apply 消费本次五份旧 managed backup，零 sidecar、source/installed、dogfood drift、定向 24/24、图/集成 35/35、Completion 27/27、Reactivate 35/35、Identity 3/3、installer/upgrade 162/162 通过。连续无 finding 计数为零；新的正式 Phase 2、提交后完整 Branch Review 与两轮全新独立审核尚未完成。

本轮正式 Architecture Phase 2 对 `.66` 返回 `baseline_current/reviewed_candidate`；九维 Phase 2 对当前 dirty candidate 依次 recorder/checker/wrapper 返回 `passed`。本段与 RDT/Architecture 状态说明是随后写入的证据文字，必须刷新 Phase 2 的 content identity 后才能进入 Task Commit；独立完整提交范围 review 与 shared 晋升仍待执行。

随后完整提交范围审核发现 Reconcile 的旧任务身份残留及 pre-review 未提交 Planning 内容的正常路径问题；本轮再发现 Create Task Commit、Change Context、Delivery Review、Publish、Merge 五个活跃消费者仍读退休的 `task.json.branch/worktree_path`。已统一到 TaskId/generation、Git common-dir branch binding 和注册 checkout，并为本 #434 旧任务建立精确 generation 0 binding；未修改业务仓。新增共享模块首次在临时干净安装漏发，installer 3 项失败，经显式分发清单和安装回归修复后完整 installer 89/89 通过。Reconcile 37/37、五消费者 27/27、18/18、13/13、20/20、21/21；共享生命周期 138/138、当前集成 20/20、#434 图 17/17、upgrade 73/73、本地路由 45/45、native load 5/5。source/installed、drift、diff check 与两次 preset reapply 通过，零 sidecar。此前所有正式 Phase 2/Branch Review 不绑定这份候选，连续无 finding 计数归零；需重新取证、提交、完整独立审核及串行 `.66 -> .67` 晋升。

本轮连续审核第二位又发现两项 P3，计数归零：Change Context canonical/平台指令仍将活跃任务绑定到已退休 `task.json.branch`；旧安装重应用保留可执行的 `start-task.sh`，合法新任务调用会因旧字段缺失被拒。现已改为 TaskId/代次、branch binding 与注册 checkout 的一致合同，并将 `start-task.sh` 连同 17 个退役 companion 脚本纳入受管旧资产退出：只删已知受管 hash 或旧 manifest 对应的原字节，本地未知修改保留并阻断；只对当前分发脚本设置可执行位。当前 dogfood apply 后 source/installed、drift、零 `.new/.bak` 通过，installer 旧候选 92/92；最终清单变更后仍需完整重跑。连续两轮全新无 finding 审核、正式 Phase 2、提交后 Branch Review 和 shared 晋升均未完成。

下一轮全新只读审核又发现两项正常问题，连续计数仍为零：更早的受管安装 `1092865f...` 在旧 manifest 缺少逐文件 hash 时有两个脚本不同于现行已知字节，导致重应用误判为本地冲突；未知旧脚本二次冲突会覆写用户修改的 `.new`。已补这两个历史受管 hash，用该真实旧提交的 18 个脚本和缺 hash manifest 验证全部安全退出；已有 `.new` 在重复冲突时原样保留。定向 5/5，完整 installer 与后续正式门禁仍须对稳定候选重跑；两轮无 finding 审核从零重新开始。

再一轮全新审核指出更早的受管脚本字节未全被退役白名单覆盖，连续无 finding 计数仍为零。现从仓库 Git 历史枚举 18 个受管旧脚本版本，补齐摘要并新增逐版本覆盖测试；三个更早提交的无逐文件 hash 安装重应用样本已通过，未知本地编辑仍需保留冲突。定向 2/2；完整 installer、组合门禁、正式 Phase 2、提交后完整 Branch Review 和 shared 晋升仍待本候选重跑。

历史摘要修复后 installer/upgrade/native-load 174/174、生命周期/图 155/155、路由 45/45、当前集成 25/25，source/installed 34 active/104 commands/33 invokes/153 production exits、二次 apply、dogfood drift、零 sidecar、task validate 和 diff check 均通过。首位全新只读审核又发现 quality guide 与本仓 installer 规范仍将退役脚本和旧 Workspace/Publication/Finalizer 图称为现行，连续无 finding 计数归零；已改为当前 Intake/Delivery/终态 owner 并把旧合同标 pinned-old，定向文案 9/9。新投影和正式门禁仍需重跑，不将前一候选的 174/174 当成新状态结果。

修订后第一轮全新审核仍发现 installer 首页及 manifest 把 Finalizer/Publication 握手写作当前。已统一首页、原子包清单、manifest 消费者和三份终态 Skill 的激活提示；旧合同限定 pinned-old，现行 Intake/Delivery/Completion/Closure/Finish/Cleanup/Reactivate 唯一图和 Interface 1.7 显式。文案回归 10/10；重新投影、组合门禁、连续两轮无 finding 审核和正式 Phase 2/Branch Review 均未完成，计数重置为零。

## Expected File Areas

2026-09-27 提交后首次独立 Branch Review 的两项 P2 已修复：canonical 与 installed extension manifest 补齐 Completion 的 `reactivation_validation` 输入并将 Approval `approved` output 更新为 3.0；安装测试从全部 34 个 active Interface 精确推导公开输入/输出 ID，防止固定计数掩盖缺漏。同步过程中发现 installer 曾将 ignored `.pytest_cache` 纳入包资产，现排除缓存并加定向回归；误投影留下的缓存删除记录已从本轮生成的 installed manifest 移除。两次 reapply 均零 backup/sidecar，source/installed、dogfood drift、图/文案 20/20、Delivery 集成 5/5、manifest 定向 2/2 和 diff check 通过。installer 宽测 96 项通过；同一命令尾部的三个模块路径写错导致导入错误，已分别按文件发现重跑图/集成，不能将导入错误算作产品失败。连续无 finding 审核、正式 Phase 2/提交后 Branch Review 与 `.66 -> .67` 晋升仍待重新执行；远端 marketplace 不纳入验收。

首位全新独立审核又发现一项 P1，连续无 finding 计数归零：Merge `delivered` 的六字段 seed 缺失 Completion 必填 TaskId、generation、result ID。当前 Merge 输出升为 2.0，从已验证 active checkout 提取身份，以 merge commit 派生稳定结果 ID；接口投影九字段，跨包测试把投影送入 Completion 当前 schema。Merge 包 22/22、图/文案 20/20、Delivery 集成 5/5 通过；第一次 reapply 的受管差异经第二次收敛，source/installed、dogfood drift、零 sidecar 和 diff check 通过。上一轮审核与 Phase 2 不覆盖该变更；新的组合测试、两轮全新无 finding 审核和正式门禁仍待执行。

下一位独立审核发现 P2，连续无 finding 计数再次归零：成功 merge 的输出丢失后，如果目标 base 有正常后续提交，恢复误要求 base HEAD 恰好等于原 merge SHA。终态恢复现通过 GitHub compare 校验原 merge 是当前目标 base HEAD 的祖先，PR、merge commit、reviewed head 与双亲仍按原合同精确核对；非祖先拒绝。恢复无第二次 merge，原 result ID 不变，Merge 包 23/23。改动后的 projection 和连续两轮无 finding 审核、正式 Phase 2/Branch Review 以及 shared authority 晋升尚待执行。

其后首位全新只读审核无 P0-P3（1/2），但广义 runtime pytest 325 pass/8 fail：六项是退休 owner/23 包计数/旧 branch 字段/缺少 Delivery policy 的测试夹具，两项是标准 Intake eval 的本地 bare clone 在临时对象复制时失败。当前 fixture 已以 34 包 manifest、真实 branch binding、现行 Publish Interface 和 Phase 2 policy 修正，静态定向 5/5；eval fixture 改用非本地 bare transfer 并关闭临时 Git 自动 maintenance，Intake 13/13 和 Qualification 6/6 两次通过。新编辑使 1/2 审核失效，计数归零；广义套件正在重跑，不能把先前 8 项失败称为通过。

2026-09-27 审核修复候选：quality guide 的 #389 Workspace 长段已收为 pinned-old 历史，不再向当前 checkout 下达旧 mapping、route 和脚本测试要求；Cleanup Skill 改为当前 Finish 后路由。新增 T434-31 与文案回归。此前审核 finding 使连续无问题计数归零；本次投影、组合门禁、两轮全新审核及正式 Phase 2 尚待执行。

2026-09-27 广义 runtime 333/333、installer/graph 117/117、Merge/Delivery 28/28 与 source/installed/drift 通过。首次 installer fixture 曾因三个 eval canonical 文件尚未投影而产生受管备份，二次 apply 后零 sidecar，失败单例与完整套件均通过。随后全新完整范围审核发现 Merge `delivered` 仍以 `planned_skill_input_seed` 扁平字段交给 Completion；已将未发布的 2.0 结果改为嵌套 `task_artifact`/`merge_result`，声明现行 `completion` profile 的 authoring seed，定向 Merge 23/23。该 edit 使先前测试和审核不能代表新候选；重新投影、组合验证、连续两轮全新无 finding 审核、正式 Phase 2/Branch Review 与 `.66 -> .67` 晋升仍待完成。

嵌套 handoff 修复后的 runtime 333/333、installer/graph 117/117、source/installed/drift 均通过。下一轮完整审核发现终态集成测试的 installed 模式将共享 `runtime` 导入路径错误设成 `.trellis/guru-team/skills`；修正为 `.trellis/guru-team` 后 source 与 installed 各 6/6，并在默认 #434 candidate gate 内执行完整 installed 终态 suite。新增 T434-34；此编辑之后组合 gate、两轮全新无 finding 审核及正式 Phase 2/Branch Review 仍需刷新。

随后的全新审核发现 Merge 的必读 `references/contract.md` 仍声明生产未激活、旧扁平 `delivered` 与 base HEAD 必须等于原 merge commit。现改为当前 active graph、TaskId/generation/branch binding、嵌套 Completion authoring seed 和已验证祖先的 read-only output-loss 恢复；新增 T434-35/合同文案回归。canonical/installed/平台经二次 apply 收敛零 sidecar，Merge + #434 candidate 34/34、source/installed 和 drift 通过。完整 installer 首次快照只得 117 pass/1 个投影备份失败，不能视作本候选通过；新的组合 gate、两轮全新审核与正式 Phase 2/Branch Review 待做。

2026-09-27 本候选完整 installer/graph 重跑 118/118，Merge/Completion/Finish/Issue/runtime 定向 132/132，source/installed 34 active/104 commands、dogfood drift、task validate 与 diff check 通过，最终没有受管 `.new/.bak`。两位互不依赖的全新只读 reviewer 串行覆盖 `origin/main...d7f57ce1` 加全部未提交/未跟踪 #434 改动，连续两轮均无 P0-P3；此结果只证明提交前候选修复，不替代最新内容身份的正式 Phase 2、Task Commit、独立 committed full-range Branch Review。旧 #154 仍限定 pinned-old 或逐项人工处置，完整多平台 Release matrix 仍由专门 gate 承担。

- `trellis/workflows/guru-team/` 与 `.trellis/workflow.md`
- `trellis/skills/guru-team/` 与 `.trellis/guru-team/skills/`
- `trellis/presets/guru-team/`、extension manifests、overlay/platform projections
- `.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.cursor/skills/`
- `.trellis/spec/workflow/` 与对应 preset spec projection
- `docs/requirements-design-test-contributions/434-task-delivery-lifecycle/`
- `docs/architecture/contributions/`、必要 ADR 和 promoted authority files
- graph、installation 与 integration 的直接 tests/fixtures

## Stop Conditions

- #435/#436/#443 任一 required capability 尚未合入 selected base，或 live cardinality/current authority 仍不一致。
- child Interface 的 exit/consumer 与本计划表不一致且需要 requirement choice。
- 无法证明 old/new graph 原子切换，或必须引入双图/adapter 才能继续。
- Architecture/RDT authority conflict、promotion stale 或 project check regression。
- 发现旧链在途实例需要通用 runtime migration，而非 pinned-old/manual disposition。
- 任何实现发现超出 #434 graph activation 范围时，先回 scope/Planning owner，不直接扩张。
