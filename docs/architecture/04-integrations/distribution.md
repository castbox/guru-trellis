# INTEGRATION

- `ARCH-INT-001`：canonical registry/interface/schema/runtime 经 preset inventory 投影到 dogfood 与平台 Skills；version/mode/bytes 必须一致。
- `ARCH-INT-002`：Trellis marketplace 通过 `trellis/index.json` 与 workflow id `guru-team` 暴露；preset 在 workflow 安装后补齐 runtime/platform assets。
- `ARCH-INT-003`：Git/GitHub 是 base、Issue、PR、merge、release live facts provider；Task archive 仅保留 closeout history，不替代 live provider。
- `ARCH-INT-004`：RDT 只消费 Architecture public locator/version/status；Bootstrap 只消费两个 child owner 的 minimal schema-validated result。
- `ARCH-INT-005`：`get_context.py` 从 `.trellis/spec/**/index.md` 提供 Agent 读取入口，但 projection 不复制 authority 正文。
- `ARCH-INT-006`：每个 declared platform cell 同时安装 shared `.agents` public projection 与唯一 selected platform projection；package-private validator scripts 不分发到平台 roots。
- `ARCH-INT-007`：项目 Architecture check 通过 current descriptor/result identity、applicability、rule/decision/GAP refs、before/after、evidence/unavailable reason 与 freshness 接入 semantic owner；公共 runtime 只校验一一绑定和 route consistency，不执行或解释项目语义。
- `ARCH-INT-008`：installed manifest 的 immutable `repo/ref/commit` 只定位 extension source；canonical
  apply 以 `--repo target_reviewed_checkout` 写 target，postimage 分别验证 target lineage 与 extension
  provenance。不得解析 mutable main、PATH/global package、hidden checkout 或 legacy fallback，也不
  引入 verifier lifecycle edge。
- `ARCH-INT-009`：仓库私有正式发布入口通过既有 owner 的 declared typed result 串行连接 preparation
  与 post-merge exact candidate；PR/Release payload 从 live Issue、exact diff、当前验证与 candidate
  identity 即时生成。owner-private lifecycle metadata、授权和阶段状态不进入 tracked handoff，任何
  delivery、durable docs、配置、schema、script 或 test 变化仍使对应 owner evidence stale。
- `ARCH-INT-010`：normal-scenario 与 solution-mechanism qualification 在同一 caller candidate boundary
  分别执行；机制 owner 的 `mechanism_revision_required` 只返回原 owner remove/replace，不能变成 scope
  confirmation。canonical/installed/platform projections 保持同一 package identity。
- `ARCH-INT-011`：Merge 的 `phase2_reentry_required` 只投影最小 PR/task/archive/finding identity 到
  `guru-restore-archived-task`；恢复 owner 不创建替代对象，不复用旧 check/review/publication/finalization
  authority，并只把 `restored_to_phase2` 交给 Phase 2 consumer。
- `ARCH-INT-012`：installer、source/installed validator、compatibility matrix、throwaway、runtime/eval 与
  platform projection 从每个 package Interface 读取唯一 public wrapper path，验证 exact bytes/mode/launcher
  与 private-script leak；`restore-archived-task.sh` 证明该合同不依赖 `invoke.sh` 文件名。
- `ARCH-INT-013`：Finalizer `base_reconciliation_required` output 通过声明的 consumer seed/projection 把
  prior `branch_review_commit` 与 exact task/base identity 投影到 Reconcile；确认后的 package-private executor
  只创建 expected-head local reconciliation commit。Review Branch bounded continuity 分离验证 prior/current
  anchors、base ancestry、candidate tree 与 affected paths，再把 current HEAD 投影给未放宽的 Publication
  reviewed-content gate；task content、scope 或 authority 变化仍回到 Phase 2 与完整 Branch Review。

## Capability 与 installation consistency 边界

- `ARCH-INT-014`：框架与扩展来源分离：`trellis/presets/guru-team/source/trellis-source.json`
  是唯一框架来源记录，preset 仅投影到 `.trellis/guru-team/trellis-source.json`。
  README 准备链与 verifier 使用显式 checkout、固定 SHA 和 Fork 自身构建/Node bin；
  失败不回退到原 npm 包或全局 CLI，不复制 dist、不新增 launcher 或打包分发系统。
  current source record 同时绑定精确 commit 与成功的上游 CI run；CI 证据不替代本地 build marker
  和实际模板/CLI 校验。full 历史验证需独立 predecessor checkout/SHA；focused 只证明当前 candidate 场景。

- `ARCH-INT-015`：#392 Stage 1 的 repository-private release orchestration 按唯一顺序连接
  pre-promotion fresh Phase 2 / Task Commit / `origin/main...HEAD` Branch Review -> expected `.47`
  serialized Architecture/RDT promotion -> post-promotion fresh Phase 2 / Task Commit /完整 Branch Review。
  第二次 review 通过后才可进入 Publication。preparation merge 后所有 Stage 1 gate identity 失效，
  Stage 2 只接受 fresh `origin/main` exact commit/tree；完整 Release Gate、annotated tag、tag-pinned smoke、
  GitHub Release、Issue close 与 cleanup 各自由其 live owner 独立处理。

- `ARCH-INT-016`：framework generation owner 为 canonical source record 指定的 fixed Fork official CLI；Guru canonical
  owner 直接迁移 workflow/Skill/runtime/installer/spec/platform consumers，并经 preset 投影到 dogfood 与
  installed copies。task resolution 只消费 task metadata、Git common-dir/branch/worktree、ignored mappings
  与 explicit caller authority；creator/assignee 只来自 explicit metadata 或 repository-access-preflight 后的
  authenticated GitHub caller。legacy identity/workspace 数据只由 preservation validator 读取 bytes/mode
  snapshot，不进入 owner、selection、recovery 或 migration authority。

  #408 的正常 authoring 使用完整 installed package 中的现有入口；public input、recorded owner
  result 与 recorder response metadata 不混用。source facts 来自实际读取，owner-local 派生值归原
  recorder，opaque 上游 token 原样承接；任务创建仍由原 executor 写双端 mapping，不增加补写路径。

- `ARCH-INT-017`：Issue-backed task 的 closure authority不通过task-local aggregate交换。
  Publication 基于 current requirement authority、reviewed diff、target/default branch 与 live Git/GitHub facts
  形成唯一 reviewed reference/closure intent；Finalizer 只绑定该 payload并投影 exact body SHA-256。默认
  分支 closing keyword由 GitHub执行，Merge mutation前验证 live body identity，再读取 live PR/Issue facts
  验证结果；non-default-base 当前只引用并由后续进入默认分支的
  Publication fresh判断。no-Issue不制造 Issue identity，remain-open 必须绑定具体 current-authority原因。

- `ARCH-INT-018`：#418 的 `review_refresh_required -> archived_review_passed -> archived_ready`
  经各原 owner 的 Interface projection 连接只读复审，最终由 Finalizer 返回原 `ready_for_merge`。
  原 H 只由 Finalizer 从 committed summary 推导；当前 A、复审 B 与 title/body 快照各服务其直接
  consumer，快照不等于 Publication 批准。三个 consumer 前分别 fresh 调用 Architecture 的
  `branch_review`、`publication`、`acceptance_finish` stage；缺 authority 或需写入时只读链停止。
  普通 profiles、gate 和 Merge expected-head 操作保持原合同；接口正文归 canonical packages，
  决策与证明边界见 `ADR-010` / `EVD-028`。成功退休的 checkpoint 不构成额外复审前置条件。

- `ARCH-INT-019`：#419 continuation通过唯一workflow block连接existing Interface consumers与producer-owned
  recovery。SessionStart、UserPromptSubmit、显式start/continue和自然语言续接加载同一block；upstream
  candidate提供extractor和thin entry，Guru只提供workflow内容与Guru-owned package projection。#410在#419
  merge后的fresh main独立执行install/update/switch/reapply Release Gate，不消费#419定向证据。

- `ARCH-INT-020`：#435 将Delivery Review的reviewed payload投影给Delivery Publish，再将exact reviewed head、
  PR identity与publication state投影给Delivery Merge；Merge通过受控two-parent merge commit trailers记录stable
  task identity、schema version与reviewed head，并从target-base first-parent history结合GitHub PR/merge identity、
  repository/base和parents重建Delivery fact。三个packages已进入canonical、installed与平台投影，但workflow edge
  保持deferred；#434 activation前不得把package存在解释为production route可达，#436也不由该投影实现。

- `ARCH-INT-021`：#436 将 Completion -> Closure -> Finish -> Cleanup/Reactivate 组织为五个独立
  package-level projections；各边只传递 task/receipt/route 所需的最小字段，owner-private recovery 不跨包读取。
  五个 packages 进入 canonical、installed 与 Shared/Codex/Cursor/Claude projections，但 workflow edges 保持
  deferred，#434 activation 前不得把 package 存在解释为 production route 可达。

- `ARCH-INT-022`：#443 将五个profile/route discriminator投影为`session_resumed`、`session_rebound`、
  `task_switched`、`reactivate_rebound`、`session_manually_recovered`与`binding_blocked`六个exit-specific
  contracts。canonical、installed、Shared/Codex/Cursor/Claude以及当前candidate声明的OpenCode projection
  使用同一package bytes；workflow integration保持deferred，#434 activation前不得把任何binding route解释为
  production可达。#443历史证据只绑定其当时声明的平台，OpenCode由当前#452 combined diff独立验证。

- `ARCH-INT-023`：#452 将平台分发收敛为 upstream inventory 与 target-installed selection 两层；installer
  使用可重复 `--platform`，无参数新安装和 guru-trellis dogfood 使用 Claude/Codex/Cursor，upgrade/reapply
  从目标 manifest/provenance 保留 exact selection。canonical 22-platform descriptors 不等于 dogfood overlay
  数量；OpenCode 的 `.opencode` native projection 只在显式选择时安装并由 representative actual-load 验证，
  package-private `tests/` 不进入任何 public projection。

- `ARCH-INT-024`：#454 shared lifecycle DTO catalog 与 runtime 作为 canonical/installed contract assets
  分发，不新增 Skill、exit 或 production edge。D0 pre-review reconcile 从 fresh selected base 与唯一 merge-base
  派生 pair，compatible route 创建 parents 为 `[prior_task_head, new_base_head]` 的 expected-head-bound local
  merge commit；`post_check` / `post_commit` 必须回 fresh Phase 2。首次/full Branch Review 要求 selected base
  是 review HEAD 祖先；bounded continuity 只允许 post-Branch-Review/Publication/Finalizer caller，并绑定 prior
  full-review commit、new-base ancestry 与 candidate tree identity。

- `ARCH-INT-025`：#454 C3 把四个 checkout DTO 与 live checkout runtime 只加入 canonical shared substrate；
  planned registry row 与 canonical `planned_skill_ids` 预留 `guru-ensure-task-checkout`，但 active selector、
  `active_skill_ids`、active graph、workflow、installed copy 与平台 projection 都保持原字节。raw preset apply
  因该刻意不同步而报告 conflict，是 E434 activation 前的明确未通过边界，不是兼容层或 production route。

- `ARCH-INT-026`：C3 provenance marker只在transaction-created linked worktree的Git administrative
  directory与同一acquisition owner之间流转；public DTO、task/session binding、resource ledger、installed/platform
  projection均不携带marker。Recovery以fresh live facts + exact marker闭合，direct handoff retirement结束恢复窗口。

- `ARCH-INT-027`：C4 将 six-field TaskBranchBinding 与 C5 current ownership 通过 epoch/revision/branch 窄投影
  对齐。Discovery 只消费 registered worktree 与 local `refs/heads/*` live facts并排除 retained
  `refs/heads/guru-task-lifecycle/*` control refs；same-checkout rebind只创建一个 absent ref并保持HEAD/index/worktree
  bytes，existing-target rebind只接受clean exact artifact与ancestor-compatible target。两个planned Skill IDs与
  `guru-ensure-task-checkout` 一样不创建package/interface/active graph/installed/platform projection，E434前
  canonical与installed差异仍是显式未激活边界。

- `ARCH-INT-028`：C5 将 session adapter、resource ledger、Finish seal input 与 Cleanup resolution 仅加入
  canonical shared substrate；官方 schema-2 session store 保持单写，C4 通过 `OwnershipPort` 消费 ledger。
  current binding/ownership/incarnation 只校验已建立的 branch、epoch、revision 与 resource identity；
  自动选择唯一合法 candidate，零/多个由用户选择，显式未发现 target 仍经相同 live validator。
  对 remote delivery 只按当前 incarnation 和 Git 祖先关系推进 HEAD，不引入 ledger-wide transaction token。
  planned registry ID 不创建 package 或 active graph edge；installed/platform projection 和完整 Release matrix
  仍由 E434 或专门 owner 验证，不因 Architecture promotion 宣称已完成。

- `ARCH-INT-029`：C6 只在 canonical shared runtime/schema 与 planned registry/manifest 增加 creation 和
  activation 的组合输入。`new_branch | existing_branch | existing_checkout` 分别投影实际新建或复用的 branch/
  worktree ownership，adopt route 不携带 provision disposition；context key 缺失仍完成 task lifecycle。
  六个 planned IDs 无 package/interface/route/I/O 字段，不进入 active selector、mandatory workflow edge、
  installed/platform projection。C7 证明新增 Phase C 代码不读写旧 mapping/path；E434 独占 predecessor 退休
  与一次性生产切图，#410 独占完整 Release matrix。

- Capability-loss gate 只比较 `workflow`、`task_data`、`docs_authority`，用于判断升级前后
  用户可观察 workflow capability 是否丢失。
- `skill_api` 与 interface/schema/command projection、distribution、managed/installed file
  inventory、mode、template hash、sidecar、声明平台 parity 及 extension identity/version
  binding 属于独立 consistency/installation gate。任一不一致仍 fail closed 并阻塞 release，
  但其变化本身不构成 capability loss。

`ARCH-INT-031`（#454 D436）：五个 canonical package 的 schema、interface、consumer、runtime 与
source tests 按 current lifecycle DTO/ledger 闭合。Closure Result/Transaction refs 投影到 Finish，
Finish ResourceSealRefDTO 投影到 Cleanup；manual 与 machine-handoff 各有单独入口及目标 consumer。
这不是 active selector、graph/manifest 或 installed/platform projection；E434/#434 必须原子安装，
#410 独占完整升级/发布矩阵。

`ARCH-INT-030`（#454 D443）：canonical Bind major 以五个保留成功 router 加一个
`explicit_task_mode` 提供 TaskLifecycleDTO 最小 handoff，blocked 投影 ReasonDTO；TaskRef 由直接
consumer fresh 派生。active selector、manifest、managed installed/platform bytes 及 workflow routers
在 E434 前维持旧 production 合同，不用 D443 source tests 冒充平台分发或升级证明。

`ARCH-INT-032`（#434 current）：七个 E434 packages、active registry/Interface selector、
workflow graph、extension manifest、managed installed distribution 与声明的 Shared/Codex/Claude/Cursor
入口以同一候选投影。Completion 选择 Interface 1.7 的两个 evidence-refresh authoring variants；
旧 schema 1.4-1.6 保持历史字节身份。source/installed 的完整旧图、新图和混图负例、reapply/
drift/零 sidecar 与代表性本地 clean install 均为 targeted gate；退休 managed script 仅在
known bytes/manifest hash 匹配时删除，本地未知编辑保留 conflict。远端 marketplace 安装
不是 #434 实际路径，完整多平台 Release matrix 仍由独立 owner 承担。此前 D443/D436
非激活及 planned rows 的叙述仅是 `.65/.66` predecessor 状态。

`ARCH-INT-033`（#454 generation 7 current）：固定 official Fork、canonical Guru package、
dogfood task/session 脚本、installed 和声明平台入口消费同一 TaskId/source 与
五字段 binding 合同。Cleanup 的显式选择只投影 call-local candidate ID，
不创建 mapping、resource ownership 或 session 历史；Reactivate 读取本代
terminal cleaned receipt。`.67` 的旧 Fork pin、Git-ref-safe TaskId 和
六字段 reader 是 superseded 历史，不是 installed current。

`ARCH-INT-034`（#467 current）：canonical extension `0.6.17-guru.43` 投影到
installed manifest，Shared/Codex/Claude/Cursor source 保持同一合同。
从 `v0.6.17-guru.1` 既有安装升级时，installer 按前版本 managed hash 删除
新版本已退役且未被本地修改的 Skill、命令、package 文件和平台投影；本地修改保留并
报 conflict/sidecar。实际退役清理以 exact candidate 的 predecessor existing-install
cell 证明；focused clean cell 与静态投影不能代替该证据。

`ARCH-INT-035`（#481 current）：canonical extension `0.7.0-guru.1`、dogfood Guru
投影、声明的 Shared/Codex/Claude/Cursor 入口及代表性 Codex 新装使用同一无人员
接口合同，Fork source lock 固定 PR #24 的 `64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac`。
旧 `.69` pin 只保留 predecessor provenance。新装、两次 reapply、同候选 update、
模板 hash、session binding 与 drift 已定向验证；`0.6.17` dogfood 的官方
Trellis update 明确拒绝 `0.7.0-castbox.1`，不能据此宣称前驱升级通过。
远端 marketplace、生产安装和完整 Release matrix 均未验证。

`ARCH-INT-036`（#490 current）：canonical source lock、dogfood official template/hash 与 Guru installed/Claude/Codex/Cursor projection 同步采用 `9c36002a324c16a09a85b6aa5a380b74aabf801f`；upstream 所有权不转移给 Guru。183 official files 和声明平台投影通过；代表性 Codex clean/current-update/reapply 使用 local workflow sample，native load 为 projection parity。remote/native-host/full matrix、前驱拒绝无写证明和 release 流程仍由 #489 独立验证。

`ARCH-INT-037`（#495 reviewed exact-source acceptance）：正式 Fork PR28 merge `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c` / main CI `37647767799`，CLI/core `0.7.0-castbox.3`；Guru `0.7.0-guru.3` 未发布候选。official assets 由 Fork 拥有，marketplace/preset 仍是扩展入口。已验证本地来源分组 actual upgrade/recovery/rollback 与 installed/drift；精确远端 Guru `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的 public/source_locked/provider/deferred 与默认AGENTS三格保护通过（EVD-051），软件 Release、真实业务安装、完整累计矩阵未执行。历史 `6a563f5f` / Fork PR27 固定来源结果仅见 EVD-049，不重标为新 source。

## #503 身份职责后继（.76）

`ARCH-INT-037` 的 #503 successor：正式 Fork PR30 merge `5c760463680ffc10a3f26957b330c57a4b0c3ff8`，parents `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c` / `a776a97cd5699f6324582ae57245542f80576a6c`，tree `9f044e4233edc90fd2b3169442ea13e5d1951780`，main CI `37735554354` 成功。official 四脚本及183文件投影、source-lock/build/installed validators、drift/reapply 支撑 EVD-052；CLI/core `.3` 与 Guru `.3` 轴不变，不冒充软件发布。

`ARCH-INT-038`（#382 reviewed candidate）：root package/caller/schema/workflow/spec 经 canonical marketplace/preset 和 installed/shared/Claude/Codex/Cursor 同步；候选 registry36/163/109，声明业务 workflow34/157。一个 Fork 0.7.0-castbox.3 clean published-base marketplace init + 显式本地 candidate projection/preset/update/reapply 已执行；不冒充未发布候选的远端安装。官方扩展面与软件四轴未改变；业务原生接续和完整多平台矩阵未验证。

`ARCH-INT-039`（#383 reviewed）：新增共同 spec 通过原 MANAGED_SPEC_PATHS 进入官方 marketplace/preset 管理；canonical/shared/dogfood/Claude/Codex/Cursor 合同和受管 bytes/modes 同步。一个 owner fixture 上 22 declared platforms 实际 apply/reapply 与 original native wrappers 已定向验证，具体结果见唯一 Test；fixture 缺官方版本标记，不冒充实际完整 init/update。registry36/163/109、business34/157 和软件四轴不变，candidate 远端安装、业务生产效果及完整 Release matrix 未验证。

`ARCH-INT-040`（#468 reviewed）：canonical workflow、activation 2.0 schema/interface/runtime 与原 Check/continuation consumer 经 marketplace/preset、shared/dogfood/Claude/Codex/Cursor 同步；registry36/164/109、business34/158。一个 clean 本地 preset fixture 的实际 Planning→activate→revised Planning→resume→identity-only recover 与 reapply/drift/bytes/modes 已定向验证；具体层次见[唯一 Test](../../requirements-design-test-contributions/468-direct-source-replanning-compatibility/test.md)。不冒充官方远端 init/update、native cognition、Backend 效果或完整 Release matrix，软件版本轴不变。

`ARCH-INT-041`（#453 reviewed）：current runtime、两个 shared schema、36 packages/109 commands 及受控 callers 经原完整 preset 与 shared/dogfood/Claude/Codex/Cursor 同步；public I/O/exit inventory 不变。一个 Codex clean 和完整 predecessor a080da3 的 apply/reapply migration、两套实际 Wording positive/blocked wrapper、当前 projection/drift 已执行；[唯一 Test](../../requirements-design-test-contributions/453-formal-skill-exit-boundary/test.md)拥有结果与边界。其它版本/native hosts、完整官方 init/update、Release matrix 与生产升级未验证。

`ARCH-INT-042`（#250 reviewed）：current Intake schemas、Interface 1.8、registry/manifest、canonical workflow/spec 与 shared/dogfood/Claude/Codex/Cursor 经原 marketplace/preset 同步；registry36/164/109、business34/158 不变。一个代表性临时项目的 clean 与 existing update/reapply、正式 profile/qualifier/relay wrappers、原生来源到当前 Planning、实际 compact 和 no-change resume 已定向验证，首次失败保留于[唯一 Test](../../requirements-design-test-contributions/250-phase0-intake-owner/test.md)。Guru 不 patch/delete upstream brainstorm 或入口，旧 current input 按显式迁移 fresh re-entry，无 dual reader。其它 hosts、真实 external GitHub mutation、候选远端安装、业务安装/部署与完整 Upgrade/Release matrix 未验证；软件四轴不变。

`ARCH-INT-043`（#521 reviewed）：canonical workflow、selector/execution/create 合同、C6 最小 primary 前置及原 Review mode schema 经现有 marketplace/preset 与 shared/dogfood/Claude/Codex/Cursor 投影同步。registry36/164/109、business34/158 与软件四轴不变。一个 Codex local-candidate clean/current-update/reapply、current drift 和真实 persistent native caller已定向验证；旧 current-checkout task-free 在 current contracts 直接退出，没有双模式 fallback。Guru 未修改 upstream start/continue/extractor/hooks；实际 upstream bytes 与模型接续分别证明。实际结果、首次失败和层次由[唯一 Test](../../requirements-design-test-contributions/521-checkout-isolation/test.md)拥有；不推定远端 immutable 发布、业务 #120 采用、完整矩阵或旧 primary Task 逐例迁移完成。

`ARCH-INT-044`：Author package、目的专属 Architecture planning3.0、Clarify scope_ready/private4、qualifier Author input、Wording/Approval revision consumers 与 bound planning Discovery 由 canonical marketplace/preset 投影至 shared/dogfood/声明平台。matching workflow/preset 一同切换；旧 planning2.0 无 purpose runtime 退出，中断调用 fresh Author 重入；非 planning2.0 和 pinned 历史 validation assets 保持。live registry/interfaces 定义 inventory，当前为37 packages/169 exits/110 commands，workflow35 mandatory invokes/163 exits；installer checker 负责派生而不由 prose 数字决定安装。定向 package/installed/drift、一个代表性 clean/existing update/reapply 与实际 native owner 接续的各层结果仅由[唯一 Test](../../requirements-design-test-contributions/292-unique-planning-author/test.md)承接。完整多平台 Upgrade/Release matrix、候选远端软件发布与业务安装/部署保持未验证；软件四轴不变，知识晋升不替代 Release Gate。

`ARCH-INT-045`（#530）：additive committed_reentry profile、runtime/schema/commands/eval/直接 consumer 合同经 canonical marketplace/preset 同步到 shared/dogfood/Claude/Codex/Cursor；原 dirty 与 compatibility invocation 保持，三个参数 shape 互斥。旧安装采用完整匹配 preset 后才调用新 profile，无 dual reader 或 upstream patch。定向 source/实际 installed 公开链、一个 clean preset/reapply、mode/parity/drift/sidecar 的实际层次由[唯一Test](../../requirements-design-test-contributions/530-clean-committed-reentry/test.md)持有；官方 init/update/upgrade、backend #444、远端 marketplace 和完整 Release matrix 未验证，软件四轴不变。

`ARCH-INT-046`（#531）：canonical workflow/Skill/registry/independent delivery I/O/projection、installer managed spec和shared/Claude/Codex/Cursor入口成套演进；22平台声明由原descriptor管理，不覆盖provider bundled参考。实际matching mixed候选通过代表clean安装、受控dogfood、installed owner公开链、native context/continuation、reapply/drift及旧形态副本接续；具体结果和首次失败见[唯一Test](../../requirements-design-test-contributions/531-task-delivery-lifecycle/test.md)。主148注册根保留完整legacy安装，业务原树与旧样本只读，旧active/archived公共数据归上游Plan2、私有发布/收尾事实归原Guruowner。未执行正式source-lock/release、远端immutable marketplace、原业务恢复或完整Release矩阵。

`ARCH-INT-047`（#547）：retain_open 由 matching Closure/Finish、输入/snapshot schema 及原 marketplace/preset 声明平台投影成套采用，不能把新 action 交给旧 consumer。受控新候选的 installed public chain、reapply/drift/sidecar 结果仅由[唯一 Test](../../requirements-design-test-contributions/547-retain-source-open/test.md)拥有；当前 app 完整旧安装与原 CMS 采用/恢复保持未验证，官方远端 init、真实 upgrade 与完整 Release matrix 分列边界。无新 fallback、安装 writer 或软件轴变化。

`ARCH-INT-048`（#548）：此增量须 matching canonical/preset 成套采用；主完整 legacy 安装保留，原业务迁移不由本任务执行。受控安装、native Planning 与 fixture Activation 分层由[唯一 Test](../../requirements-design-test-contributions/548-creation-recovery/test.md)拥有；不证明原 CMS、软件 Release 或完整矩阵。

`ARCH-INT-049`（#557）：manual recovery profile、显式 query2、原 Completion 合同与 workflow/preset/声明平台成套采用，最低组合与 query1 消费者退出见[贡献](../contributions/557-manual-merged-delivery-recovery.md)及 canonical MIGRATION-557；[唯一 Test](../../requirements-design-test-contributions/557-manual-merged-delivery-recovery/test.md)区分 matching installed 与旧完整 source carrier。没有软件轴或旧业务安装切换。

`ARCH-INT-050`（#566）：完整 source-loaded maintenance 与 matching CLI/Core 配对；checkout-local pointer 隔离 primary/linked，声明平台与受控 dogfood 成套验证。正式 source lock 保持，旧运行图采用独立。 责任见[贡献](../contributions/566-single-checkout-upgrade.md)与 ADR-027，实际结果和边界见[唯一 Test](../../requirements-design-test-contributions/566-single-checkout-upgrade/test.md)。不表示正式依赖/业务采用、软件发布或 Task Closure。

`ARCH-INT-051`（#567）：canonical workflow/Skills/runtime/schema/eval/preset 的固定候选与阶段适用性同步演进，正常在途采用按 [MIGRATION-567](../../../trellis/presets/guru-team/MIGRATION-567.md)成套切换。ARCH-INT-013/045 的旧默认 base-advance/祖先与全链重跑片段由本条和 ADR-028 替代；原 ordinary/resolved/committed/continuity 与同操作恢复仍由原 owner 承担。旧 Merge gate 和 Finish transaction 只在各自 bounded recovery 中先验证旧格式，再由原 owner 转为当前私有请求；不保留默认 guard 或通用 dual reader。完整 source+matching installed、shared/Claude/Codex/Cursor 与自身 reapply/drift 的实际层次由[唯一 Test](../../requirements-design-test-contributions/567-fixed-development-baseline/test.md)单写。作者 checkout 的完整旧 graph 保留，工具/旧数据采用归 #566；不由受控样本推断真实业务安装、远端 marketplace、live GitHub 策略或完整 Release 矩阵通过。

`ARCH-INT-052`（#569）：原query1/2输入保持，current result3.0与受控consumer按[MIGRATION-569](../../../trellis/presets/guru-team/MIGRATION-569.md)成套演进，旧result1/2仅历史validation assets，无runtime fallback。canonical/shared/声明平台经完整matching preset采用；作者完整旧carrier保留。代表性官方clean init、installed公开链及reapply/drift结果与外部/业务/Release边界只由[唯一Test](../../requirements-design-test-contributions/569-fixed-cutoff-history-query/test.md)承接。

`ARCH-INT-053`（#578）：三 canonical owner contracts、直接冲突派发文案与现有 quality-guidelines 共同按 [MIGRATION-578](../../../trellis/presets/guru-team/MIGRATION-578.md)完整 matching preset 采用；活跃旧 Task 保留原完整安装。当前合法 Delivery installed wrapper 仅证明本地公开绑定，Release/Upgrade矩阵、source-lock精确安装、remote marketplace和业务采用仍以[唯一 Test](../../requirements-design-test-contributions/578-cross-owner-validation-facts/test.md)边界为准。

`ARCH-INT-054`（#599）：现有 managed-spec 映射将唯一清晰写作正文安装到 `.trellis/spec/workflow/clear-technical-writing.md`。有界 AGENTS、canonical workflow 的 Phase Index/continuation、公共 Guru Skills 及 22 个声明平台的 Guru finish 入口引用该正文；不修改官方 `trellis-*` 资产。已有安装通过匹配 workflow 更新和完整 preset reapply 采用，原用户区块与 `.new`/`.bak` 冲突机制保持。实际 Codex 加载、恢复、独立 child 及缺失后恢复与安装投影分别由[唯一 Test](../../requirements-design-test-contributions/599-clear-technical-writing/test.md)记录；不推定其他平台行为、业务安装或完整 Upgrade/Release 矩阵通过。

`ARCH-INT-055`（#589 D7）：source lock、current manifest/ownership、安装能力诊断与原完整安装/升级目标断言成套采用 Fork `.4` 公开 `GitCandidateContent`；稳定 `.3` 发布及其历史来源不变，不保留摘要双路 fallback。canonical source 与代表 candidate 安装仅证明本 slice 准备；本 Task 和代表 installed 的正式完整采用、native/live 受影响链及最终盘点仍由原后继负责。实际来源、定向验证与 Release/业务边界由[唯一 Test](../../requirements-design-test-contributions/589-git-object-performance/test.md)拥有，不由知识晋升推定已升级。

`ARCH-INT-056`（#600）：Architecture 非 Planning4.0/Delivery2.0 以最小 before_authority/candidate 承接原 current router 与最终 Check；完整拟写内容和局部校验只归原 owner。Branch Review 显式 promotion-reference alignment profile 绑定原真实 passed、全部 Git 差额与最终 Check，输出原 passed DTO给 Delivery Review。canonical workflow、完整 preset、consumer、runtime/schema 和声明平台投影按 [MIGRATION-600](../../../trellis/presets/guru-team/MIGRATION-600.md)成套安装。源码、投影、真实 AI 行为和 Release/业务边界由[唯一 Test](../../requirements-design-test-contributions/600-promotion-before-check/test.md)分开记录。

`ARCH-INT-057`（#577）：maintenance transport 在原 API1.0 基础能力之上接受 additive `task_resume` 并转发公开 `prepareArchivedTaskResume`，归档 profile 写前核实实际能力。actual pair digest、source_locked 的正式 lock/build/mode 与完整匹配 source 保持；本增量不 repin。Identity/Bind 复用目标 installed 公共模块，canonical Skill/runtime/workflow/spec 经原 preset 成套投影。原 upgrade owner 对 receipt 明确记录 dirty 的真实 source commit 只保留逐路径候选资格；clean metadata mismatch、缺对象、未知 preimage 和原 bytes 检查均不放宽。受控 `local_candidate`、正式依赖采用、业务安装和 Release 矩阵分别报告；实际 reapply/drift/sidecar、代表性旧安装和未验证边界由 [唯一 Test](../../requirements-design-test-contributions/577-manual-archive-resume/test.md) 单写，不以知识晋升补齐。责任与迁移读 [贡献](../contributions/577-manual-archive-resume.md)、ADR-027 和 [MIGRATION-577](../../../trellis/presets/guru-team/MIGRATION-577.md)。

`ARCH-INT-058`（#154）：四类正文资产与嵌套过程示例沿既有 recursive preset 分发到 installed Author package 和声明平台；入口引用同一正文，不复制语言规范或模板规则。已有安装通过匹配 workflow/preset 采用并处理正常冲突；上游 seed/generator/hook/official agents 不变。代表性实际 Codex 写作、平台投影、reapply/drift、用户内容及安装边界分别由 [唯一 Test](../../requirements-design-test-contributions/154-planning-body-contract/test.md) 记录；不推定其他平台实际行为、软件发布或完整矩阵通过。

`ARCH-INT-059`（#153）：共同正文、三个过程示例及四个既有入口沿原 recursive package/preset 分发至完整 installed 和声明平台投影。跨 package 引用指向同一 Clarify 正文及原 Author 来源规则，不复制内容或语言 authority，不改变 public I/O、scanner、mutation executor、freshness 或恢复协议。现有项目完整采用 matching preset/packages 后沿原 reapply、用户内容与 sidecar 机制验证；源码变化不证明旧安装采用。代表 Codex 实际写作/创建/修订及定向分发、目标安装分别由 [唯一 Test](../../requirements-design-test-contributions/153-issue-content-ssot/test.md) 记录；不推定其他平台实际行为、正式 source-lock、软件发布或完整矩阵通过。

`ARCH-INT-060`（#630）：canonical runtime、installer、原source lock与声明平台经完整matching preset分发；本项目固定Fork来源采用`7f050fa11ddd8569e5db4f728ea1b745b7500a98` / `.5`，实际build与目标采用分别验证，替代ARCH-INT-055中本版本继续固定`.4`的来源选择，历史`.4`结果保留。Guru文本属性从实际inventory派生，精确EOL恢复后仍原raw validation；unknown编辑和sidecars按原合同处理，不覆盖上游`trellis-*`。新进程update/maintain、同provider preview/force、同recovery_ref recover/resume后再Guru reapply及真实入口是集成验收。三系统脚本/安装、Windows实际Codex、source/dogfood/projection、软件Release分层记录，不互相替代；实际结果唯一见[#630 Test](../../requirements-design-test-contributions/630-native-compatibility/test.md)。

`ARCH-INT-061`（#636）：TaskCommit早期输入/输出与局部candidate/receipt、Publication Draft/Ready事务、BranchReview早期分析profile及workflow唯一consumer按 [MIGRATION-636](../../../trellis/presets/guru-team/MIGRATION-636.md)成套直接演进。旧完整安装固定；原owners一次性恢复/迁移同key/PR、实际已执行动作和真实gate义务，不从旧意图制造pass，不保留runtime双读。canonical workflow、完整preset/packages/runtime/schema、声明平台和dogfood同步；workflow与preset分别按各自正式支持面应用并保留用户修改/sidecar语义。local matching、真实远端反馈、业务采用与Release矩阵分层报告，实际结果只见 [#636 Test](../../requirements-design-test-contributions/636-early-draft-pr/test.md)。
