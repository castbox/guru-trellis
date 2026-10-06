# #495 旧安装单向迁移 — 设计草稿

状态：实现中的同范围规划修订；本轮受影响 Planning gates 待重新执行。
accepted behavior 见 [prd.md](./prd.md)，本文件拥有机制及职责。

## 机制与取舍

采用独立 migration Skill + Fork 正式迁移入口 + 当前 lifecycle owners。普通 update、preset apply 和正常 task writer 继续严格验证当前合同；只有 migration 阶段可读取固定旧来源。拒绝删除整套 .trellis、修改全局 npm/node_modules、修改业务生成副本绕过拒绝、长期双读，以及把旧 gate 转成 current approval。

框架 core/schema 差异由 Fork 拥有；Guru 拥有 AI 编排、旧 Guru provenance 到当前 ownership 的转换、workflow/preset 安装和 task lifecycle re-entry。迁移 executor 不判断任务来源、Issue closure、计划充分性、PR readiness 或路由语义。

迁移 Skill 应从目标 canonical/source package 加载，不能要求旧安装先通过 current runtime 检查才能获得升级能力。公开 id 拟为 `guru-upgrade-installation`，`judgment_mode=semantic`，standalone 路径；新旧格式隔离在该 package 的 migration 模块中，不进入共享 current identity/source reader。Fork 新增显式 `trellis migrate --from 0.6.16 --plan <core-plan.json> --dry-run` 预览及去掉 `--dry-run` 的执行入口；plan 是 Guru executor 提供的 private、已审查字段与受管动作投影。目标固定候选为 Fork CLI `0.7.0-castbox.2` / Guru `0.7.0-guru.2`，二者当前均无发布 tag；实现及验证完成后文档才把这些拟定命令称为可执行入口。

## 正式来源验收与候选发布顺序

`formal_guru_source` 要求 Guru HEAD 已提交目标 manifest/package 且 canonical source clean；`source_locked` 使用 `gh:castbox/guru-trellis/trellis#<同一 Guru HEAD>`，该 commit 必须远端可读。验证分为本地候选验证与候选发布后的正式同源验收：前者完成正式 Fork lock/CI、本地 package/installed/reapply/drift、隔离 lifecycle/恢复/回退及可执行旧交付状态诊断，后者对固定远端 Guru commit 执行真实 public migration 与 marketplace/provider 验收。`local_candidate` 只提供本地候选证据，不代替正式 `source_locked`。

首个 Delivery slice 交付验收用候选代码与合同。它在完整独立 committed Branch Review 后，先按 expected-current promotion 已实现候选代码/合同与本地证据，再对 promotion-created diff 执行 fresh Phase 2/commit/独立完整 Branch Review；之后才发布 Refs-only PR。候选 knowledge 和 PR 明确列出剩余正式验收和 MIG-495-06 证据，不关闭迁移目标或相关 GAP、不声称正式 source_locked 验收通过。失败返回同一 TaskId 修复并重新执行受影响 gates；所有 MIG-495-01..09 满足前停止在合并及 Completion 门禁。该顺序不新增 runtime 分叉，不放松 provenance/CI，也不执行版本发布或真实业务升级。

## 职责与数据边界

| 责任 ID | Owner | 输入与输出 |
| --- | --- | --- |
| D-MIG-495-INVENTORY | Guru migration package | read-only 旧安装/任务/Git inventory；call-local 预览，持久化仅发生在执行所需 private backup |
| D-MIG-495-CORE | Fork CLI/core | 精确旧 core profile、reviewed task field projections；更新 core managed files 和显式转换旧记录；正常 writer 不接受旧记录 |
| D-MIG-495-GURU | Guru migration package | 校验旧 manifest 与 old managed hashes，迁移 Guru 资产 ownership；按当前 preset 使用正式安装入口 |
| D-MIG-495-LIFECYCLE | 既有 current identity/source/branch/checkout/session/planning owners | 转换后 TaskId/generation/TaskRef 及 live facts；正式 owner 建立当前 bindings、fresh plan review 和接续 |
| D-MIG-495-RECOVERY | Guru migration package，Fork core restoration helper | backup 与逐步完成事实；客观诊断、恢复或回退；不接触 Git history 或远端 delivery |

Skill public input 分 profile 定义简洁合同：initial_upgrade 仅目标 source identity 与支持来源 profile；resume/rollback 仅本迁移所需恢复 reference。目标 repo 绝对路径为 call-local CLI context，不进入公共 package 示例。逐文件计划、完整 inventory、hash bundles、旧记录、session mapping 和 local backup path 是 private，不扩大 handoff DTO。

typed exits 拟为：`upgraded` → stop/report 当前安装及任务级接续结果；`resume_required` → 同 Skill recovery；`rolled_back` → stop/report；`blocked` → stop/具体处置。每个出口拥有独立最小 output schema/唯一 consumer，不能用一个总 artifact 冒充输入/输出。任务接续在 Skill 内显式调用 current owners；报告 DTO 不让 consumer 理解旧 manifest、backup 或内部 digest。若实现需要独立可复用 owner，按完整闭环判断拆分，不制造一条脚本的 wrapper Skill。

## 正向流程

1. 从支持清单校验 source core/Guru 版本、Fork 来源、旧安装 provenance 和实际 schema；目标 candidate 必须包含 Fork 正式迁移能力。
2. read-only inventory：core hashes/config/platforms、Guru old managed hashes/entries、workflow bytes、业务 spec/定制、dirty/untracked、active/archive、session/branch/worktree/PR 状态。只读 Git/GitHub，不因 35 份任务存在而断言 35 个活动会话。
   core current preview 的 actions 不等于完整旧 ownership inventory；AI 必须直接比较旧 template-hashes 与目标 current template paths，对退役旧路径逐个明确 remove/preserve。旧 receipt、精确旧 bytes 与 reviewed decision 共同约束动作，不做目录级自动删除。Guru 旧 managed hash 缺字节时仅从 old manifest exact source.commit 获取；正规 source history 前置缺失先补该 OID 再预览，不依赖隐藏常驻历史。
3. AI 审查受管路径、本地修改处置、每个任务字段投影与来源/branch 选择、实际会话协调、恢复/回退范围。显示真实命令和每个写入目标；确认在当前对话发生且不持久化。
4. 建立 backup 和最小执行 checkpoint；调用 Fork 迁移更新 core 与 active task schema。迁移动作只按已审查投影和客观前置条件执行。
5. workflow 用 marketplace create-new 预览，核对旧修改、目标 identity 和 sidecar，再显式 force 应用；Guru 专用迁移转换旧 provenance 并调用 current preset。不要给普通 apply 增加自动 legacy fallback。
6. 处理受管修改和 sidecars，验证 source/installed/runtime/inventory/platform parity；选择 task 时按当前 identity/source/branch/checkout/session owners re-entry。旧 gate 不进入新路径。
7. 分别报告安装结果、每个任务接续/处置结果、剩余验证边界。current-only 验证成功才称安装升级；两个最低 task 路径真实执行后才称最低接续完成。

步骤不是 approval state machine。checkpoint 只保存 restoration/recovery 必需的路径、旧/目标 identity、已完成文件动作和可重读的阶段结果引用；不保存用户授权、审查过程或全链 audit。

## 任务转换合同

| 旧事实 | 明确转换/接续规则 |
| --- | --- |
| 合法 id/name/TaskRef | id 原值不变，不要求 UUID；TaskRef 不重命名；检查同 common-dir 的同一任务多副本与历史防复用，不能把复制 task 文件当作独立新身份 |
| 缺 lifecycle_generation | 初始迁移 generation=0；已有可验证 generation 保留；与当前 control state 冲突须诊断，不能自动提升 generation 消除冲突 |
| creator/assignee | 不进入新 active schema；backup 保留旧字节；.developer/journal/traces/archive 原地不变 |
| 缺 source | AI 从当前 requirement authority 与 live Issue facts 作 source 决定；GitHub disposition 逐项明确，无关闭意图推断；无 GitHub 来源（含 TAPD）使用 no_issue，同时保留业务来源在原 description/meta/规划文件 |
| 已有 source | 按当前 source owner 校验真实 source 与 disposition，不能因为 JSON 外形相符跳过语义审查 |
| 旧 branch/base/worktree_path | 仅线索；从 git refs/merge-base/registered checkout/actual task artifact 查证，由当前 binding owner 建立 C4/C5；过期路径不成为 authority；branch 缺失的 planning 可在真实下一步经选择建立 |
| children / parent / subtasks | 现有有效关系保留；空 subtasks 退役；非空时确定是否与 children 相同语义，AI 明确同语义去重映射；无法无损表示时保留旧原始记录并给出 task 级 blocked，不添加没有当前 consumer 的 legacy 字段、不静默丢弃 |
| 精简旧记录缺字段 | 缺 children/relatedFiles 使用 []，缺 meta 使用 {}，缺 nullable 字段使用 null，缺 priority 使用 P2，缺 description/notes 使用空字符串；createdAt 从明确原始记录/规划读取，没有可证明日期时使用当前 schema 的空字符串并在迁移报告标为 unknown；不能把迁移日期称旧任务创建日期 |
| 未知额外字段 | 精确诊断和 AI 字段处置；脚本不得自动丢弃或万能搬运掩盖语义冲突 |
| status planning | 保留规划及身份，建立选择任务的当前 binding/focus；进入 fresh current Planning，不要求先新建替代任务 |
| 未发布 in_progress | 保留 commit/未提交改动；旧 planning/gates 无效，fresh review 后进入当前 dev/check；current owner 不强迫清空合法 dirty task work 才能建立迁移后绑定 |
| PR/merge/Finalizer/Finish | 分开读取 live PR/ref/merge 与旧事务；只接受当前 owners 可承接的明确路径，其他逐案处置；不复制旧 gate 或自动执行发布、merge、归档 |

active task 结构转换与 execution focus 恢复是两个独立结果；每个需接续的 task 明确 re-entry。暂不可接续旧 active 可经逐项诊断后在原 TaskRef 保留原字节；它只占用 TaskId/TaskRef，不成为 current candidate 或恢复 authority。迁移缺少明确处置的旧 active 仍阻塞；已诊断残余须逐项报告原因与影响，不能隐藏未迁移条目或宣称 all-converted。

### 混合 current / known-legacy inventory

复用当前严格目标解析和 raw identity reservation，不新增生命周期 writer。扫描先正向区分已知旧形状与 current 形状：known legacy 只读取合法 id 与 canonical ref 用于占用/冲突；正常 `task_inventory` 输出只含 current candidate。直接选择旧目标仍返回不受支持；current 目标与同 id/casefold 的旧记录冲突仍阻塞。不能根据 `unsupported_legacy_task` 错误码笼统跳过，因为坏 current generation/source、未知额外字段也可能产生该码；有 current source/generation 的记录自身错误、坏 JSON 和缺 id 继续 fail closed。

独立 Fork migration 的私有 core plan 增加最小 `deferred_tasks: [{task_ref, expected_sha256}]` 投影，由 Guru AI 已审查任务处置产生。它只供执行/安装 inventory 的原字节保留校验；不得创建 current binding、session、gate 或公开恢复 DTO。planned converted 与 deferred refs 明确互斥，deferred hash 绑定被保留的原始记录，resume 再读仍需匹配；遗漏旧 active 或普通 drift 继续诊断并阻塞。Guru installed-inventory validator 同步消费已审查处置，普通 runtime 保持 current-only。这是旧数据占用与候选排除，不是 runtime 双读或自动转换。

### 迁移后尚未提交的 task 与 dirty binding

当前 branch establishment 从已提交 task 读取 id、generation（缺失按 0 处理）和 status；current ensure 从实际 checkout 的当前 task 解析身份，未把 dirty 视为接续否决条件。主来源的已有 id/status 和迁移 generation=0 与此合同一致。因此直接使用现有 establish → ensure → bind-session owners，现存资源恢复为 caller-owned；无须为 schema 转换先提交或清空业务工作。

checkout acquisition 的 clean 要求仅用于获取新 checkout，不能错用于已建立 binding 的 ordinary dirty resume。若 task 尚未出现在分支 HEAD（例如仅 untracked 的旧任务），该 branch 不是现有 establishment 的有效候选；须给出该具体 task 的 acquisition/当前 binding 建立处置，由当前 owner 与 Git 副作用规则承接，不能暗中 commit 或绕过 owner写 store。本 Issue最低样本使用实际已提交旧任务及未提交业务改动，task-only untracked 状态单列诊断。

## 保留、部分写入与回退

备份对象为实际会写/删的 managed 文件、manifest/version/hash、active task 原字节及实际会变更的 control/session state；记录新增文件，以便回退时仅删除本迁移新增且未被新版工作修改的文件。业务、历史大目录不被改写；为保留验证只生成必要对比，不复制为 current authority。

普通部分写入错误用已完成步骤和当前 bytes 判断下一步：old bytes → 可执行该动作；target bytes → 已完成，不重复转换；其它 ordinary drift → 明确诊断并重新预览。失败不把 .version/manifest 单个文件当成整体成功。使用已完成 core 更新而 Guru 阶段因普通受管本地修改/未解决 sidecar 停止的实际场景，恢复后执行剩余步骤；不用额外 fault injection。

rollback 适用于 managed update 与 task conversion 已发生、且尚未开始新版本业务工作。比较迁移后基线与当前 task/control/managed/Git 业务状态，AI 判断是否出现新任务、新交付、业务工作；有新增工作则禁止覆盖式回退并给出保留/另案处置。备份恢复只写清单路径、保留无关 dirty/untracked；还原被改 session/control，删除本迁移新增受管文件，执行旧 runtime smoke 和原字节比对。rollback 不 reset branch、不 rewind commit、不删除远端 PR。

部分 core/task 成功时，即按 `coreplan.tasks` 固定 task-content token，并绑定相关非 preset control 的初始基线；它只有 rollback 直接 consumer，不能在 resume 时重新取当前 task 作为可覆盖基线。普通冲突暂停期间通过 native task writer 产生的新 meta/业务事实必须保留，且阻止 resume 后覆盖式回退。无需全链 audit、独立长期 control-capture 步骤、锁或额外 fault injection。

保留比较按各自 ownership：历史/journal/业务/spec/规划执行原字节与 mode 对比；有效 config 与用户设置按语义保持，允许正式 owner 添加必需 `dispatch_mode` 等设置，不用整个 config 原字节相等否定合法官方添加。Planning 接续样本必须有真实脱敏项目 Architecture baseline、actual normal-scenario/solution-mechanism invokes、Architecture/wording/Planning 语义 owner gates；record/check/invoke 只证明结构与客观绑定。

## Architecture 与 Docs SSOT Plan

current Architecture/RDT 为 `current-main-0.6.17-guru.71`；constitution 为 `guru-trellis-design-constitution-v1`，change contract 为 `guru-trellis-architecture-change-contract-v1`。此任务有 architecture impact：选择 `legacy_boundary_convergence`，真实旧来源的解析仅在一次迁移边界，成功出口 current-only；可重复服务其它同来源仓库不意味着普通 runtime 兼容。

维护单写：Fork core/schema writer、Guru migration/preset writer、既有 C4/C5/session owners 各自独占职责；当前 shared authority 仅 serialized promotion 更新。ADR 候选用于显式修订 #481 不迁移决策，保留原无人员/current-only决策。无需机械逐原则评分；最小 DTO/private backup 和复用 owners 控制新增复杂度。

实现阶段创建 isolated RDT contribution，链 `MIG-495-* → D-MIG-495-* → S-MIG-495-*`；创建 task-owned Architecture contribution/必要 ADR 候选；当前 README/spec 中不迁移条款改为普通 runtime 拒绝与独立迁移支持的清晰边界，历史 release/tag/归档保持 immutable。promotion 前由 Phase 2 和独立完整 Branch Review审查；不得提前覆盖 shared current。

canonical 更新后通过正式 apply 同步 dogfood，逐个处理 .new/.bak 并运行 drift。业务样本在隔离副本运行；真实 downstream checkout/worktrees 只读。

### Planning Architecture contribution

task-owned contribution identity：`architecture-contribution-495-legacy-installation-upgrade-plan-v1`；本节是 Planning candidate，后续代码及独立 Branch Review 后形成 `docs/architecture/contributions/495-legacy-installation-upgrade.md`。expected current：`current-main-0.6.17-guru.71`。当前 gate 仅审查设计，不把目标描述标为已实现。

| Required concern | Applicability / decision |
| --- | --- |
| authority-binding | applicable：Guru Architecture 2.0、current .71、project v1 与 live #495 accepted delta 同时绑定；历史 #481 不迁移条款由 #495显式修订 |
| constitution-binding | applicable：官方扩展面、完整 task identity、职责隔离、最小私有恢复状态与单向收敛对应 current constitution五个 identity；无原则例外 |
| boundary-and-decision | applicable：D-MIG-495-CORE / GURU / LIFECYCLE 按原 writer拆分；继承 ADR-015；ADR 候选明确旧安装迁移决策的变化 |
| owner-and-single-writer | applicable：Fork 独占 core/task schema，Guru migration独占旧 Guru转换，C4/C5/session仍由既有 owners写；shared current只经 promotion |
| compatibility-and-exit | applicable：固定旧来源只在独立 migrate解析；安装及current schema验证后退出至current-only；旧 parser不注册为普通runtime fallback，backup由 rollback直接消费 |
| gap-and-deviation | applicable：关闭旧业务仓无法更新及接续的 #495缺口；不关闭其他 ARCH GAP；全平台矩阵/真实业务安装仍由独立owner承担 |
| parallel-scope | applicable：task规划、isolated contributions与scoped canonical/Fork实现；禁止并行改shared current或无关business文件；base/authority变化后refresh |
| evidence-and-freshness | applicable：before为固定 .1 Fork/current拒绝及真实旧安装；after设计要求 S-MIG-495-*实际命令；各 gate绑定当轮task内容/候选，planning不宣称runtime通过 |
| review-and-promotion | applicable：Planning→implementation→Phase2→完整独立 committed Branch Review→expected-current promotion；promotion-created diff再次独立check/review |

项目检查 `guru-trellis-architecture-convergence:repository:1` 须针对本轮混合库存及恢复细化重新执行 Planning owner：保持唯一 writers/current-only，known-legacy 只保留身份占用，deferred 不成为恢复 authority。先前 Planning 结论不代替本轮审查；实现态 before/after、项目 runtime 验证、ADR finalization 和 promotion 仍待执行。
