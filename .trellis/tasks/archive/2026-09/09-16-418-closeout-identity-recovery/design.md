# #418 技术设计：归档只读复审

状态：新增profile/exit已实现，新基线与投影验证已完成；正式门禁结果由各owner当前输出承接，promotion尚未完成。此前D418-03的原profile重放方案已撤回。当前修改不恢复业务任务到active，不改写归档历史。

## 1. 来源、边界与已知缺口

需求来源为 [Issue #418](https://github.com/castbox/guru-trellis/issues/418)。任务初始基线为 `57e8b5df`；主检出的 `main` 已同步到 `78651e20`，已无提交快进到任务分支，原未提交改动保持。

原方案失败的直接证据：

- Publication `runtime/_owner_part_02.py:453` 与 `_owner_part_03.py:1735` 要求 `in_progress`；正常归档任务为 `completed`。
- Branch Review `runtime/record.py:67` 将新 review 绑定当前 HEAD，即 archive commit。
- Finalizer `runtime/_owner_part_05.py:482,565` 要求原 active locator 和归档前 review anchor，不能用 archive HEAD 替换。
- 成功 Branch Review 会退休 checkpoint；缺失 checkpoint 的同一 stale 文案不证明旧审查失效。正常 Ready 路径不得新增私有文件读取。

本修订保留 D418-01/02，替换 D418-03。涉及新 profile/exit/consumer，Architecture 影响为候选 `architecture_impact/target_native`，不再使用原 `no_architecture_impact` 结论。

## 2. D418-01：映射收敛

Finalizer 原归档 executor 在精确 archive commit 校验后、push 前收敛同一任务的 source/target `task_artifact_dir`；既有 archived/Ready executor 用同一规则重入。完整校验双端 task/workspace mapping 和真实 branch/worktree 后再写任一映射；其它字段不变，已收敛状态零写入。

仅接受精确旧 active 或当前 archived projection，不重建缺失 mapping，不猜测 source，不覆盖其它 task。preview 与 boundary validator 保持只读。正常归档必须直接留下可用映射；历史 stale mapping 只能由已有 Finalizer executor 的受控恢复收敛，不能借下述只读复审入口偷偷写映射。

## 3. D418-02：错误传播

Merge 所有原入口从发生点生成明确的 code/field/remediation，经共享 `CommandError` 传播。保留 provider 分类和 `stale_identity`；未知异常仍为 `internal_error`。不按异常文本做语义判断，不输出 stderr、PR body、凭据或绝对本机路径。

preview 的 diagnostic 不是 Skill typed exit。未形成当前有效输入和 AI review 时不得制造 gate；正式 semantic invocation 才返回声明出口。

## 4. D418-03：新增只读复审链

### 4.1 唯一链路

```text
Merge archived_review_request
  -> review_refresh_required
Branch Review archived_review
  -> archived_review_passed
Publication archived_publication_review
  -> archived_ready
Finalizer archived_review_refresh
  -> ready_for_merge (原 DTO)
Merge ready_for_merge
  -> 原 merge gate 与独立 expected-head 操作
```

新增四个 target-owned profile、三个独立 exit；复用四个现有 Skill 与原 command/wrapper，不新增 Skill、shell entry、全局恢复 ledger 或并行 transaction engine。每个新 exit 只有表中唯一 consumer；其它出口仍按原合同停止。不能将原 `merge_blocked` 静默重映射。

第一次已知 stale/缺失诊断的 remediation 指向 Merge 的 `archived_review_request`。当前 AI 先核实是需要当前复审结果，而不是成功退休后的正常缺失，再调用该 profile。不得自动递归调用自己或无条件重审。新入口也支持没有旧 Publication handoff、但现有已归档任务和 Ready PR 能被精确验证的恢复请求。

### 4.2 Public I/O 与直接消费者

表中 payload 字段之外，input 含固定 `profile/mode`，output 含固定 `exit_id`；Merge input还保留该包现有的 `schema_version=2.0`。其余三个owner沿用现有无schema_version字段的public input风格，schema id独立版本化。这些discriminator不传递私有审查记录。

| Owner/profile | Input payload | 唯一成功输出及 consumer |
| --- | --- | --- |
| Merge/archived_review_request | task_ref（archive）、repo_ref、pr_number、expected_head_sha | review_refresh_required：task_ref、branch_review_commit、pr_payload_snapshot_sha256 -> Branch Review |
| Branch Review/archived_review | task_ref、branch_review_commit、pr_payload_snapshot_sha256 | archived_review_passed：task_ref、branch_review_commit、pr_payload_snapshot_sha256、reviewed_base_head -> Publication |
| Publication/archived_publication_review | task_ref、branch_review_commit、pr_payload_snapshot_sha256、reviewed_base_head | archived_ready：task_ref、branch_review_commit、reviewed_base_head、pr_title、pr_body -> Finalizer |
| Finalizer/archived_review_refresh | task_ref、branch_review_commit、reviewed_base_head、pr_title、pr_body | 原 ready_for_merge DTO -> Merge |

字段来源与用途：

- `task_ref` 必须是 archive 下的精确任务。每个 owner 从 task/summary 验证身份、branch/base、repository 与唯一 PR，不消费其它 owner 的私有 artifact。
- Merge 校验 `expected_head_sha == local HEAD == remote branch HEAD == live PR head`；`branch_review_commit` 是该当前 archive HEAD。Branch Review 用它绑定完整本轮范围；Publication 用它验证新复审与当前 candidate；Finalizer 用它区分新复审锚点 A 与原归档锚点 H。
- `repo_ref/pr_number` 只用于入口锁定目标，与committed summary.pr_url、既有configured publish remote和任务branch/base交叉校验；publish.remote空值沿用origin，runtime_root空值沿用原默认目录。下游从immutable archive和GitHub live facts重读，不重复传递可推导字段，不新增remote输入字段。
- `pr_payload_snapshot_sha256` 来自新入口首次 live PR 的 `{title,body}` 对象，以 UTF-8、sorted keys、compact separators、无尾部换行的 JSON 计算 SHA-256；字符串bytes不做trim或换行归一化。它只绑定复审期间的 PR 快照。Branch Review 和 Publication 各自核对它；Publication 消费后不再向下游传递。它不是旧 Publication 批准，也不是授权。
- Publication 输出的 `pr_title/pr_body` 必须是当前实际存在且重新审查通过的精确 bytes；Finalizer 与 live PR 再次比较，并生成原 `publication_body_sha256`。到这一点才重新建立当前 Publication-reviewed handoff。
- `reviewed_base_head` 是 Branch Review 实际审查范围 `B...A` 的 B，由 Publication 和 Finalizer 逐步核对当前同一base ref；两者必须匹配B，包括B仍为A祖先的正常快进也使本轮旧B结果失效。Finalizer消费后结束该token生命周期，不扩展原Merge DTO；其后Merge按原live gate独立检查，不新增并发协议。
- 禁止 public output 携带原 gate、完整 review、scan、history、文件 hash bundle、用户确认或 recorder locator。input/output 均使用独立 closed schema，不能扩展成 optional recovery bag。

### 4.3 三个独立 Architecture stage

全局workflow在每个新consumer前调用原Architecture owner，不能共享一个stage结果：

| 原producer exit/source_exit | Architecture task_impact_sync stage | current后的唯一consumer |
| --- | --- | --- |
| review_refresh_required | branch_review，精确B...A | Branch Review/archived_review |
| archived_review_passed | publication，绑定A/B和当前authority | Publication/archived_publication_review |
| archived_ready | acceptance_finish，绑定A/B和当前authority | Finalizer/archived_review_refresh |

使用既有 `source_exit` 字段的三个新值表达只读调用来源，不新增含optional开关的input。Architecture Skill/contract及validator同步定义该闭合来源集合的语义：其AI只能在当前只读范围内完成审查并返回 `baseline_current`，或因缺少current authority/必要evidence、需要promotion/repair/implementation写入而返回原 `blocked` 并说明受限原因。不会在此调用中执行promotion、修改contribution或重建业务状态。普通source_exit的原七出口行为保持。

这不是caller把sync_required改写成blocked：选择受限条件下的blocked仍由Architecture semantic owner完成，runtime仅验证该来源/stage下的结果子集。若实现误返需写出口，则是该新增调用合同不合格，必须在调用边界fail closed，不能自动进入写入consumer。专用回归必须验证此条，不得以遗漏Architecture调用来达成零写入。

### 4.4 Merge：请求复审而不是提前批准 merge

`archived_review_request` 是独立只读 profile，不接受 `publication_body_sha256` 或旧 semantic result，不执行 merge。AI 从原诊断、当前需求与 live facts 判断复审必要性；正常 Ready handoff 继续走原路径。

要求 task completed、archive committed/clean、准确 branch/base/repo/Ready Open PR。原命令记录当前六维 review；在该 profile 中只审查复审入口条件，不能选 `merged`。满足条件返回 `review_refresh_required`，不满足返回 `merge_blocked` 或入口 diagnostic。不得把 external CI/权限失败或真实内容缺陷伪装为 fresh-review 成功。

原 `ready_for_merge` 与 `standalone_merge` 不变。新 profile 的唯一作用是获取受控复审快照，没有远端 mutation authority。

### 4.5 Branch Review：独立审查 A

先从task.base_branch解析B，要求本地selected-base ref与live GitHub base ref指向同一已存在Git对象；不fetch或更新ref，缺对象或不同步则停止。向Architecture传入精确B...A并消费当前branch_review结果，再审核该完整committed diff、live requirement、归档规划和现有测试证据。B不在A ancestry、branch/PR/title-body snapshot改变、dirty或归档结构不合法时停止，不更新base/branch。Publication与Finalizer同样核对本地及live base ref，不仅比较分支名。

旧 checkpoint 不能投影为新 pass。当前 AI 重新完成独立审查，通过原 record/check/invoke 产生该 profile 的新结果并退休其临时 checkpoint。现有普通 Branch Review 的当前 HEAD/ancestry/finding 规则不放宽。

成功DTO包含本轮B；Publication/Finalizer前若base ref不再指向B，返回明确stale并停止本轮，只能从新Branch Review获得新B的真实结果，不后台合入新base。

新 profile 仅有 `archived_review_passed|blocked`；真实 content finding、scope 不足或未知状态保持 blocked，不自动恢复 task、不修改归档文件、不制造空 commit。finding 不被吞掉，原 owner 负责记录当前最小结论。

### 4.6 Publication：只读重审现有 payload

新增 profile 明确接受 completed archive；普通两个 profile 仍要求 in_progress。复用十维语义审查，但使用专属只读 entry/preflight，不能调用 active `prepare_closeout` 或生成新 archive plan。

重新判断当前 Issue authority、测试声明、Docs、PR title/body、Issue closing effects。核对 A 与 PR body snapshot，读取当前 PR title/body；只有现有 bytes 已正确充分才输出 `archived_ready`。需要修改 title/body、代码、范围或声明时返回 blocked，不能在此 profile 自动 metadata revision、PR edit、Issue mutation 或返回 active-task work 路由。

私有semantic result采用按profile区分的独立variant，不复用普通Publication的“blocked必须external_blocker”约束：

- `archived_ready`：十维与结论全部passed，零open finding，A/B/snapshot/现有payload均current。
- `blocked`：至少一个真实open finding和非passed维度，携带具体reason/remediation。内容/metadata问题保留原 `task_work|metadata_revision` 分类并使用finding维度；provider/authority evidence缺失保留 `external_blocker` 分类并使用blocked维度；每项finding必须引用对应维度。总体停止结论不将内容问题改名为外部问题。
- 新variant没有 `return_to_task_work` 出口，不执行metadata revision loop；普通两profile继续用原semantic union及路由约束。

### 4.7 Finalizer：H 与 A 分离，零 transaction mutation

新 profile 只接受新 `archived_ready` 投影。A 必须是当前 archive HEAD。Finalizer 从该 commit 的 finish-summary 读取原 active locator、archive locator、branch/base 与原 commit 集合；从集合中以 Git ancestry 找到唯一支配其余 commits 的顶点 H。当前 producer 使用 `rev-list --reverse base..review_commit` 生成该集合，因此 H 是原 review tip，不依赖数组最后位置或时间排序。无唯一 H、空集合、对象缺失或不满足原约束时停止，不能猜测或沿用旧 checkpoint。

复用原 archive validator，以 H 校验归档前 ancestry、reviewed-content equality、精确 archive move/blob/metadata continuity；以 A 校验本次复审、local/remote/PR HEAD 和 clean archive，并检查当前base head仍为B。H 不能被 A 覆盖，summary 不能被改写。

与新 Publication 传来的 title/body 精确一致、PR仍 Ready/Open、repo/branch/base unchanged 后，原 invoke 直接投影 ready_for_merge。此 profile 不进入执行 archive/push/PR/Ready 的 transaction loop，不要求 mutation confirmation，不写 mapping、task 或 summary。原 recorder/checker按其生命周期创建并退休 owner-private短期审查结果；不生成长期 recovery checkpoint。旧 transaction 尚未完成时先返回原恢复诊断，不将半完成 closeout 当作 completed archive。

## 5. 失败与副作用矩阵

| 条件 | 结果 | 禁止 |
| --- | --- | --- |
| 旧审查不可用但精确 completed archive/Ready PR 可核实 | 新只读复审链 | 自动复用旧 pass |
| 已成功退休 checkpoint 且当前 Ready handoff 可用 | 原 Merge 路径 | 多余复审 |
| snapshot/A/repo/branch/PR 状态变化 | 当前 owner typed blocker/diagnostic | 换 head、body、任务继续 |
| 新复审发现 content/authority 缺口 | blocked，保留 finding | 编辑业务文件、自动 restore |
| H 不唯一或 archive continuity 不成立 | Finalizer blocked | A 冒充 H、改 summary |
| 新 Publication 判断现有 PR payload不正确 | blocked | PR edit、重新关闭 Issue |
| 正常旧 mapping 可精确收敛 | 原 Finalizer executor | readonly profile 写 mapping |
| 缺 mapping 或不同 task identity | fail closed | 重建/覆盖未知映射 |

## 6. 架构、迁移与维护性

本修订是 target_native 的隔离只读能力，不是将旧 gate 迁移为 pass。既有 profiles/DTO/exit 的语义与路径保持；新增 profiles/exits 用新独立 schema id。aggregate schema 新版本包含原 profile references 与新增 profile；旧私有结果不升级，新 profile 必须 fresh authoring。被当前 reader认定为 stale 的旧 schema 仍拒绝，不增加 dual-read shim。

新分支使用原 package invocation，根据 profile 选择严格独立的校验与无远端写入路径。不得仅通过一个 writable flag 复用 active preparation。复用中立 Git/content 校验，package-specific 行为不放共享 dispatcher。

预期 graph 增量为 0 Skill、0 command、3 exit、4 profile；Architecture既有profile增加上述闭合只读source_exit语义，不增加第五profile或修改普通来源路由。以实施时 live registry/interface 派生总数并校验所有 output 的唯一 consumer，不把当前旧计数硬编码到新状态。三个新出口均纳入 canonical workflow、Interface、consumer schema、production/eval inventory 与声明平台投影。

Architecture contribution 与 draft ADR 位于本任务专属文件；shared current 不在普通 task 中直接修改。需要 independent full-diff review 后按 expected current 串行 promotion，promotion-created diff再进入 Phase 2/Commit/Review，随后才进入 Publication。

## 7. Docs SSOT Plan

策略：delta_first。canonical 四个 closeout owner 与 Architecture 的 Skill/contract/interfaces/schemas/commands/evals、workflow与README、受影响的 data/companion/quality/skill-package specs 必须在最终 Phase 2 前收敛。spec源位于 `trellis/presets/guru-team/spec`，dogfood由 preset apply同步。所有 `.new/.bak` 必须逐项验证处理。

RDT需追加隔离 contribution，记录 `R418-04/05 -> D418-03 -> T418-05/08/09/10`；Architecture current现有四-exit陈述通过受控promotion变更，不伪称新图已 current。不能扩大到 #398/#419/#421 的完整生命周期、会话恢复或 Intake 改造。

## 8. 替代方案与风险

- 放宽普通 Publication status：混淆 active preparation 与 archived validation，拒绝。
- 把 A 当 H：破坏原历史与祖先约束，拒绝。
- 整体恢复 task 到 active：产生任务/归档写入及重复发布风险，不采用。
- 只改善错误文案：不能完成 R418-04，不作为最终方案。
- 专用只读profiles增加接口和验证成本，但隔离现有 mutation path，并能测试零远端副作用。

现有151项测试只证明D418-01/02局部行为。新链、真实wrapper联接、分发、new-main候选兼容及原业务实例均未验证；本修订不宣称已解决原线上故障。
