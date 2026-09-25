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
