# #566 设计：单 checkout 工具升级与独立旧任务维护

## D1 当前范围与依赖

需求唯一来源为 [prd.md](./prd.md) 指向的 Issue #566；公共层约束来自配对 Trellis #40。没有额外独立 normative source design。下表是唯一来源设计处置表；PRD 与 implement 只引用本表。

| 来源与原承诺 | 处置 | 本设计落点、理由与影响 |
| --- | --- | --- |
| Issue566：显式目标优先，省略路径按既有显式 base/config 与 dev/develop/main/master/remote-default 选定后绑定 checkout | retain | D3；复用原 resolver 的只读选择，不以 checkout 可用性重排候选，不调用同步 mutation |
| Issue566：工具、任务转换、历史收尾独立；不先要求旧 parser/Identity/Reconcile | retain | D2/D4/D5；完整来源加载两个独立 semantic Skill，原 Task 当前解析仍严格 |
| Issue40：公共模板、Task/Delivery/session、操作恢复归 Trellis；既有 Plan2 独立 | retain | D2/D6；只走公共 CLI maintain／SDK maintenance，不导入内部 dist 算法，不改 full Plan2 |
| ADR-017/018 的旧安装仅完整升级边界、current-only 正常入口 | change（task-owned ADR candidate） | 新增 source-loaded tools/所选旧任务边界；正常 current-only、旧完整升级与其恢复保留。修改通过 task contribution、独立 Branch Review 与原 promotion owner 晋升，不能先改 shared CURRENT |
| ADR-024：公共 Task/Delivery authority 与 Guru semantic/private owners 分离 | retain | D2/D5；不新增 Guru Task2 writer，历史核验不产生当前 gate |
| 现有 managed Python common default＋linked override | change（原 runtime owner 的定向隔离） | D4；tools-only 对 primary 也需 checkout-local override，common default 和 peer 解析不变。普通 preset/full upgrade 原默认行为保留 |
| 既有 source_locked/local_candidate、真实目标验证、用户修改/sidecar | retain | D4/D7；明确本地候选不是正式来源；sidecar/暂存验证不代替目标 runtime |
| Issue566：原始 owner 核实历史，历史归档不制造 Completion/Finish，兼容回退不扩写 | retain | D5/D6；最小只读事实回交、可读归档屏障、固定备份及原生结果分层 |

本设计基于 Guru HEAD `3e8b281c93894cd3df4e704901bda63ca2885f23`。Trellis #40 的实际维护合同见其 CLI root maintenance namespace 和 Core `/task/maintenance`；本地包身份在 PRD，版本号 `.3` 本身不证明能力。正式 `trellis/presets/guru-team/source/trellis-source.json` 当前仍固定 `5c760463680ffc10a3f26957b330c57a4b0c3ff8`；本轮规划不修改它。

## D2 唯一职责与公开步骤

- `guru-upgrade-tools`：新增 standalone/source-loaded semantic Skill，拥有唯一目标选择、Guru 工具资产和真实安装判断；公共模板升级委托 Trellis `tools_install`。
- `guru-maintain-legacy-task`：新增 standalone/source-loaded semantic Skill，拥有选定旧 Task 的目标意图、原 owner 调用、Guru 私有投影、维护顺序与真实续接判断；convert/history_closeout/resume/rollback 各为闭合输入，不创建新 Task 生命周期。
- 原交付/合并 owner：新增只读 `legacy_history_verification` profile。PR 事实由原 `guru-merge-task-delivery` 核验真实 repo/PR、reviewed head/merge、target、归属及证据。原 commit/manual 的事实保留/核验仍由原事实 owner 判断；不能把未验证旧字段导入当前 DeliveryFact。
- Trellis maintenance：正向识别旧记录、完整投影与事实约束、公共 session/binding、raw archive、固定操作恢复及兼容性检查。Guru 不另写这些算法。
- 当前 Identity/branch/checkout/session、Planning、Completion 与 Reconcile：迁移后才消费合法当前输入；原 owner 保留全部语义判断。历史已交付不是当前 gate pass。

两个新 Skill 均遵循 forward → AI gate → 真实选择/写入确认 → executor/validator → 一个 typed exit。普通 read/prepare 不写目标或创建资源；源 package 从完整 canonical checkout 加载，目标 `--root` 不改变执行 runtime。平台发现副本不宣称 self-contained。

## D3 目标选择

显式 checkout 直接校验 exact root、同一目标事实和受支持安装，不以调用时 cwd/current Task/branch 推断。省略 checkout 时只读取用户显式 base、现有 config.base_branch、config.base_branch_candidates（默认 dev/develop/main/master），最后 remote symbolic default；选定分支之后才寻找唯一 registered checkout。remote-default 查询可只读 `git ls-remote --symref`，不 fetch、不改 ref。

从 `guru-sync-base/runtime/common.py` 提取实际共用的只读 base 选择事实到小型共享 helper，Sync 与新工具 owner 使用同一实现。Sync 的 clean/fetch/fast-forward 合同保持；tools-only 不继承 Sync 的同步动作或对所有 dirty paths 一律拒绝。安装冲突只由真实受管 preimage、user edit 和 skip/sidecar 决策判定。缺失、重复、prunable 不可用 checkout 或身份冲突给出具体诊断，不降低候选优先级，也不自动创建/切换 worktree/branch。

## D4 工具安装与 Python 隔离

1. 加载完整 Guru 来源及匹配公共 CLI/Core。通过实际 maintain contract/API1.0 与 package bytes 身份核对工具，不仅比版本。`source_locked` 必须包含对应固定正式来源；缺少该能力时写前 prerequisite 阻塞。`local_candidate` 沿用现有隔离开发边界，结果明确 formal-source-lock unverified。
2. 读目标旧 manifest、旧来源、受管 receipt、用户 config/spec/平台选择、公共 tools inspection，以及 runtime pointer 的真实依赖。未知本地改动必须 preserve/replace/create-new 明确选择；不以目标源码哈希代替旧来源，不处理无关业务文件。
3. 公共 tools plan 的 workflow 使用 reviewed Guru canonical 自定义内容/provider；ownership 保持 custom，不把 Guru 当作 bundled native。workflow preview/new 不是激活。公共工具、Guru assets 和 pointer 分别由各自原 owner 备份，展示合并后的准确写集。
4. managed Python 仍使用既有不可变 user cache 与实际能力探针。新 tools-only 路径在目标 checkout 的 ignored `.trellis/.runtime/guru-team/python/active.json` 激活 override；目标新版 resolver 先读该 checkout-local pointer，再按既有 Gitdir/common fallback 解析。源 bootstrap/resolve/check 由原 runtime owner 同步更新；普通 preset/full upgrade 的默认 activation 不改义。链接 checkout 和 primary 都能隔离，common default、所有 peer pointer 与其实际解析出的 runtime 均不变。工具资产实际上与 peer 同源的 whole-.trellis 共享 alias 布局必须写前报告冲突，不能声称已满足单目标安装。
5. 公共 tools_install 与 Guru preset assets 按固定阶段执行。沿用 installer 的 source ownership、staged package、冲突/sidecar 和真实 manifest 生成；处理旧 manifest 的唯一入口为新 source-loaded owner 的受限事务。不能提前伪写 `.version`/declaration，不能放松 ordinary installed/current validators。
6. 真实目标运行 installed/package 验证和自己的 Python resolver、公共原生入口、新模型合法操作；选中旧状态应得到明确维护入口而非成功 current authority。必需 canonical asset 冲突、残留 sidecar 或原生失败返回同 owner resume_required，不返回安装成功。

工具安装的“旧状态保留”包括所有 active/archive Task、planning、workspace、公共/private session/binding；pointer 属于本次明确工具写集，不能隐式改变共享业务状态。新 resolver 诊断必须区分工具未安装、旧状态待维护与用户冲突，不能让用户重复安装来解决数据问题。

## D5 所选 Task 转换与历史收尾

### 独立选择与原 owner

从完整匹配来源用 public inspectTaskTarget 显式指定 root＋TaskKey＋task_ref。正向支持集合沿上游：known preidentity legacy、strict schema1（无字面 schema_version1.0）；schema2 是保留或原操作 recovery，不重新转换。原 branch binding、casefold reservation、继承副本与合法 Task-root alias 由公共 owner 判断；未知/歧义不静默选取。只为确认归属读取 peer，不转换 peer Task copies。

AI 先判断继续开发、补验收、迁移后收尾或仅历史保留。对要导入的新模型历史交付，调用原交付 owner 的明确只读旧事实 profile；该 profile 接受显式旧维护选择而非当前 TaskLifecycle/ready gate，不使用当前 publication/merge executor，不 push/merge/close，也不生成当前 pass。它返回构造公共 projection 必需的最小已核实真实事实；未知/不满足的事实保留在 raw source/note 并说明缺口，不冒充已验证。原 owner 结果和用户授权不形成长期审计链。

### 私有 control 的原 owner 入口与顺序

本次在原 `guru-publish-task-delivery`、`guru-merge-task-delivery`、`guru-finish-task` 分别新增闭合的 `legacy_control_retirement` profile；它们与只读历史核验分开，也不复用普通 current lifecycle、ready、Closure 或现有 migration 输入。完整来源 package 执行，目标旧工具保持不动。每个入口仅接受 explicit target、selected legacy TaskKey/task_ref、preserved_source_ref（公共转换备份或已读回归档）、该 owner 的精确 control_refs 与原维护 recovery_ref；AI 在当前调用核实归属和 external disposition，executor 仅校验固定 preimages、保存源可读、准确删除集。输出 `legacy_controls_retired` 的最小 owner/TaskKey 结果交回维护 owner；`blocked` 保留具体未决项，不能触发业务完成。

| 原 owner | 此次 profile 的唯一写集与限制 |
| --- | --- |
| Publish | `.trellis/.runtime/guru-team/guru-publish-task-delivery/` 内已归属本 Task/gen 的 transaction 与 gate；未完成 PR/push 的外部事实先由该 owner 只读回查并写入原维护 note，不能重放 publication |
| Merge | `.trellis/.runtime/guru-team/merge-task-delivery/` 中本 Task/gen 的 gate及该 owner 已识别的旧 merge gate；不接受 `current_input/legacy_gate` migration 冒充退役，不执行 merge |
| Finish | `.trellis/.runtime/guru-team/finish/` 中本 Task/gen 的 transaction，并承接该原 owner 历史 Finalizer 的明确控制文件；原 source inventory 给出历史具体路径与结构，未被该 inventory/内容证明归属的路径写前阻塞。终态 Finish result、封存资源账本与真实 completedAt 保留，不运行正常 Finish/Closure/资源清理 |

其他 private gates 按真实旧 source inventory 确定各自的原 Check/Review/Planning owner，并在该 owner 增加同一语义的闭合 retirement profile，采用独立最小输入；没有该 carrier 的正常样本不制造空入口或输出。不可归属/无对应入口在任何目标写入前阻塞，维护 owner不能用通用目录删除替代。

确定顺序：prepare只读枚举并由各 owner核实精确控制文件、归属及外部未决事实；真实写入前在固定 Guru recovery checkpoint 保存这些文件的原 preimages 和 note。公共 conversion/closeout执行后，维护 owner通过其真实结果读取 preserved raw source/归档及 note；读回成功才依次调用 Publish → Merge → Finish → 已选其他 gate 原 owner。各 owner只依赖 preserved source和固定 preimages，不再读取已移除的活动树。退役失败保持同次 operation的resume_required，已退役项只读回结果，不重备份、不补造 current pass。所有被选control退役及真实 native验证完成之后才返回task_resumed/history_archived。转换使用公共 conversion backup屏障，历史使用公共archive屏障；两者都不以正常 Completion作替代。

### 转换

AI 明确 authored 完整 Task2 projection、五份 Delivery planning artifact 的 preserve/write 映射、旧事实 dispositions 和精确 session/binding 决策；固定 Delivery/result IDs 后 public prepare 分配一次 operation_id。原 TaskId/source/generation/scope、原 planning/raw tree、真实历史与未完成责任保留；过期 gates 不变成当前成功。

需要目标工具升级时独立准备 D4 tools operation，审查准确组合写集再执行；不能因为“维护”隐式升级其他 checkout。公共 task apply 后原 Guru 私有 owner 仅处理已正向归属本 Task/gen 的旧私有 control；不扫描后自动清空所有 gate/Finalizer/Finish 状态。原私有 publication transaction 不能投影成新事务，保留其证据或按原 owner 的明确终止处置退役。

转换后重新进入当前 branch/checkout/session owner，再运行目标自己的正常入口及下一实际 owner。planning 进入 fresh current Planning；in-progress 未发布保留业务改动和实际 commit；已交付待验收进入 Completion evidence_pending 路径，不创建另一 Delivery。必要 Git 基线整合由原 Reconcile owner 对组合候选、冲突、accepted scope 与续接点做完整语义审查；无冲突或 parser 可用都不代表 Reconcile pass。

### 仅历史保留

原 owner 写明历史交付和外部待补义务；公共 legacy_closeout 先持久化并读回 raw archive/note，再精确退役其公共 active carriers，最后移除活动树。Guru 私有状态必须处于相同“archive 已可读”屏障之后，由各原 owner 限定退役，禁止使用正常 Completion/Closure/Finish 模拟旧任务完成。公共 owner 保留空目录、模式及合法 alias 恢复语义；不清理 worktree/branch 或外部 backing resources。

不要求为历史归档升级目标工具。归档后运行目标原有正常 context/current，证明不再选择该 Task；其他任务/会话、peer、业务文件、原 completedAt/历史责任保持。若旧 runtime 仍因未退役的确定关联 carrier 选择它，返回原维护 owner；若归属不能证明则阻塞，不能删除未知状态。

## D6 固定操作与恢复

公共工具与 Task 操作各保留自身 upstream recovery_ref；Guru checkpoint 只包含下一 resume/rollback consumer 无法重新推导的固定 source/target、原 Guru asset/pointer/control preimages、upstream operation refs 和未完成阶段。无用户授权、reviewer 元数据、完整扫描历史或全仓 hash bundle。prepare 不创建目标 checkpoint；实际写前冻结且不会因 resume 扩大原备份。

同次 resume/read-only recovery 使用同一 upstream plan、Delivery/result/operation 身份；已完成外部动作只回读结果。后续 owned-path edits 不被覆盖，unrelated business files 不在写集。tools rollback 必须先由公共 owner 验证真实 Task/session 与原工具兼容，再由 Guru 原 owner 核对 private control/工具组合；Task conversion 后的旧工具单侧回退会被阻塞。不能先恢复 Guru 半边再发现公共不兼容，不能把后续任务迁移加进原工具备份。需要组合恢复时重新展示确定范围，不创建全局事务/锁或第二 lifecycle。

## D7 最小公开 I/O 与兼容切换

| Owner / profile | 最小调用输入 | 唯一输出与直接 consumer |
| --- | --- | --- |
| guru-upgrade-tools / install | 当前 source_ref、既有 dependency_mode、target selection（explicit checkout 或 baseline resolution）；实际 file/workflow/pointer 决策为 owner-private reviewed plan | tools_upgraded：installed version、recovery_ref、正式依赖边界 → 安装结果 stop；不携 Task/session inventory |
| guru-upgrade-tools / resume、rollback | 各自独立 profile＋原 recovery_ref | resume_required 仅 ref → 同 owner；rolled_back 实际恢复版本 → 结果 stop；blocked 具体原因 → stop |
| guru-maintain-legacy-task / convert | source_ref、dependency_mode、explicit checkout、TaskKey、task_ref；真实 projection/映射由 semantic owner 审查并私有持有 | task_resumed：当前最小 TaskLifecycle handoff → 其原正常 continuation owner；只在真实目标 native＋下一 owner 验证后出现 |
| 同 owner / history_closeout | 独立 source/target/TaskKey/ref；原 note/精确 dispositions 为 private plan | history_archived：TaskKey＋archive_ref → 历史保留 stop，不调用正常 Finish |
| 同 owner / resume、rollback | 独立 profile＋原 recovery_ref | resume_required → 同 owner；rolled_back → 结果 stop；blocked → stop |
| 原交付/合并 owner / legacy_history_verification | 显式旧选择＋待核实原真实 fact refs；不用 current ready/lifecycle DTO | verified_legacy_history：仅公共 projection 直接消费的已核实 facts；unverified → 维护 owner 处理证据缺口；无当前发布/合并动作 |

具体 schema 在实现时与声明的唯一 consumer 同时定义；profile 不共用一个大量 nullable 字段总对象。Producer/consumer 使用薄且可验证的 projection；不得把私有 checkpoint/hash bundle 交给下一 Skill 理解。只有现有 local_candidate 源边界可作开发验证，不增加版本白名单或自动成功开关。

`MIGRATION-566.md` 明确新增 skill/profile/exit/schema、原独立 Plan2 API 保持及 canonical package/registry/workflow/overlay/spec/installed graph 成套安装；不改旧输入含义，也不增加 permanent dual-read/write。历史 profile 只在旧数据维护期间有 consumer；退出由原维护 owner 负责：支持集合耗尽后通过后续明确 migration 删除，不靠运行时猜测无旧数据便自动删公共 API。

## D8 Architecture 与文档

候选独立 Architecture 返回 impact、legacy_boundary_convergence，关联 ADR-017/018/024、ARCH-CUR-013、ARCH-DOM-034/043、ARCH-INT-046。贡献与 ADR candidate 位于 `.trellis/tasks/10-15-566-single-checkout-upgrade/architecture/`；这是 task-owned 方案，不是 CURRENT promotion。shared-current 仅在首次 committed full-diff independent Branch Review 后由原 Architecture owner 晋升，再 fresh Phase2/commit/Branch Review。

implement 独占 Delivery Policy 与 Docs SSOT Plan。各层测试与真实 native owner、upstream package、业务/外部/Release 边界分开，不能把 #40 已通过的 fixture 记成本 Issue 已通过。
