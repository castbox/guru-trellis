# #575 准备 v0.7.0-guru.4 发布与正式依赖对齐

## 1. 需求来源与任务边界

直接来源为 [castbox/guru-trellis#575](https://github.com/castbox/guru-trellis/issues/575) 的当前正文，重点承接「正式依赖前置」与「Stage 1：发布准备任务」。仓库私有 `.agents/skills/release-guru-trellis-version/references/contract.md` 是规范性设计约束。Issue 无已选择的评论补充。

本 TaskId 为 `575-release-v070-guru4-preparation`，generation 为 `0`，source disposition 为 `reference_only`。本任务只交付发布准备内容、验证和正常任务收尾；中文准备 PR 使用 `Refs #575`。准备任务完成不关闭发布 Issue，也不表示软件已经发布。

Stage 2 的最终 main 候选冻结、predecessor-to-candidate 完整发布审查、annotated tag、tag-pinned smoke、GitHub Release 和 Issue 关闭由 #575 保留。它们不是本准备任务 Completion 的未完成工作，不得混入准备任务的完成条件。

## 2. 目标与当前缺口

将当前已合入的 Guru Team 能力整理为 `v0.7.0-guru.4` 的可审查准备交付：采用匹配公共 API 的正式 Fork 来源、对齐版本和公开安装说明、验证所声明的来源与正常维护路径，并使长期 Docs authority 能准确承接这些变化。

规划起点的 canonical extension 为 `0.7.0-guru.3`，正式 source lock 为 `castbox/Trellis@5c760463680ffc10a3f26957b330c57a4b0c3ff8`。已发布的 `.3` 仍被公开文本描述为未发布候选。#566 的旧联合验证不能证明本任务目标正式锁已被采用或 `.4` 可发布。

### 版本与来源轴

| 轴 | 本准备任务的目标 |
| --- | --- |
| 仓库 | `castbox/guru-trellis` |
| 发布 Issue | `#575`，保持 OPEN |
| 目标 repository tag | `v0.7.0-guru.4`，本任务不创建 |
| 目标 extension revision | `0.7.0-guru.4` |
| 已发布 predecessor | `v0.7.0-guru.3`，peeled commit `7d20a930341dae3e7dd2d214660ce3b99e28d863` |
| 正式 Fork commit | `2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0` |
| Fork tree | `41ff285d857036324e480e1eb64d08fffd5956e1` |
| Fork main CI | `38851816688`，必须复核成功与 exact source 对应 |
| CLI / Core | 均为 `0.7.0-castbox.3`，相同版本号不代替来源证明 |
| Package manager | `pnpm@10.32.1` |

完整 source lock 的 parents、tree、CI 与 package manager 从同一正式 commit 核实，不根据当前 Fork 分支名或版本字符串推导。目标来源包含上游 #40 的维护能力与 #43 的旧原生 schema-1 会话元数据兼容修复；是否 CLOSED 不是能力前置的替代证据。原 #40 合并点不具备这项会话兼容修复，不能作为本任务最终采用来源。

## 3. 必须满足的行为

### R575-01：采用唯一正式匹配来源

更新 canonical source lock 并通过既有来源解析、构建和安装路径消费上述 Fork commit。CLI/Core 必须来自该同一来源，公共 Task/Delivery 与维护 API 必须与当前 Guru 消费者兼容。验证 source_locked 的实际正常路径；不得以 local_candidate、dirty 包、全局 CLI、版本输出或静态 DTO 成功替代正式来源采用。

上游源码修改、Fork/npm 发布和真实业务仓安装不属于本 Task。发现缺 API、模型或 owner 合同冲突时，将具体缺口交回原 owner 或通过当前 scope owner 处理；不自动增加第二模型、兼容旁路或跨仓修复。

### R575-02：明确区分已发布版本、准备版本和历史证据

canonical manifest、根 README、workflow/preset README、public-docs spec、实际版本断言及安装投影必须一致表达 `.3` 已发布、`.4` 尚待 Stage 2 发布，以及独立的 Fork 版本和来源轴。修订当前生效文字；历史 tag、既有 Release、历史 manifest、归档任务和旧证据不得被改写成新候选验证。

准备阶段的安装样本必须注明其实际来源。对外稳定 `.3` 说明继续使用 `.3` 的原锁；`.4` 准备说明不把尚不存在的 tag 当成可用 provider。正式发布后同一安装的 workflow marketplace 与 preset 必须使用同一 immutable tag；发布前的远端候选采用同一可寻址完整 SHA，这一证明归 Stage 2。

### R575-03：保持已有公共职责与兼容合同

只对齐版本、来源及其真实消费者，不新增公共 Skill、typed exit、schema、控制状态或发布恢复框架。公共模型、模板更新、Task/session/binding 转换与确定性恢复归 Trellis；Guru 继续拥有 Markdown 语义、明确目标、受管资产及原私有 owner 的处理。

复用 #566 的工具更新与所选旧任务维护入口。现有普通 current-only、完整 Plan2、合法版本族、用户定制保留和兼容性回退合同不得因采用新来源被削弱。正常 source/candidate mismatch 必须在声明的写集边界内给出具体诊断。

### R575-04：定向证明准备内容

最小验证集覆盖版本/来源断言、实际公共 API 消费、source 与 installed 校验、声明的 Shared/Codex/Claude/Cursor 投影、ownership、三平台 dogfood apply/reapply/drift、sidecar、权限与 diff hygiene，以及本次变更文件的真实 secret scan。

对新来源执行一个代表性 Codex 隔离 clean 安装，并在定向旧安装样本中覆盖 `.3` predecessor 的工具更新、所选 Task 转换或历史保留、目标原生入口及下一真实 consumer、同操作恢复和不兼容单侧工具回退阻塞。已有公共定向测试和 #566 场景按本次正式来源复核；不把旧候选结果重命名为新证明，不用 mock 或 JSON 解析代替 native 续接。

准备阶段只能声明实际执行的本地/隔离/installed 结果。远端 immutable Guru candidate provider、最终 predecessor 升级、完整发布 diff 和 tag-pinned smoke 必须在 Stage 2 对同一个最终 candidate 重新验证。缺失能力、环境、命令失败或 SKIP 按真实层次记录，不声称通过。

### R575-05：长期 Docs 单一来源与贡献

按当前 RDT 和 Architecture owners 选择并执行一个 Docs SSOT Plan，给出本次行为、机制、测试和 traceability 的唯一长期承接位置；当前测试结果只由本次唯一 Test 拥有。当前 authority 从 `docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md` 和 `docs/architecture/README.md` 获取，不采用落后的 usage projection 版本作为 authority。

是否存在 Architecture impact、贡献或 ADR 由独立 Architecture owner 判定。需要 shared promotion 时，仅在第一轮 committed 全量独立 Branch Review 通过后，由原 owners 串行晋升；晋升后的 diff 重新进入 Phase 2、任务提交与完整独立 Branch Review。规划阶段不得先晋升 shared current。

### R575-06：准备交付与完成条件独立

执行计划必须包含唯一 Delivery Policy。本任务保留完整 Stage 1 范围；若按独立切片分阶段交付，必须明确当前切片、独立条件、剩余工作及最终条件，不因首个 PR 合并而删减整体范围。准备 PR 不包含关闭关键字。Completion 审查全部准备要求和验证边界，reference-only Closure 返回 no_mutation；Finish 通过原 owner 完成归档和独立 bookkeeping 交付。

任何提交、推送/PR、合并、归档、bookkeeping 和资源清理均遵循对应 owner 的精确副作用边界。Task 处于 planning 不构成实现放行；规划 Approval 与当前对话的激活确认完成后才进入实现。

### R575-07：规划和证据保持真实、最小

`prd.md` 定义准备需求，`design.md` 独占 source-design disposition matrix 与机制，`implement.md` 保存稳定执行计划、Delivery Policy 和 Docs SSOT Plan。不得创建 task-local release notes、PR/Release body handoff、动态发布 checklist 或 tracked gate/candidate/tag/Release 状态。用户授权仅存在于当前对话。

## 4. 验收与证明责任

| 验收 | 可观察结果 | 对应需求 |
| --- | --- | --- |
| A575-01 | lock 的 commit/tree/parents/CI/CLI/Core/package manager 一致；实际构建及来源解析消费该 commit 的匹配对 | R575-01 |
| A575-02 | 四版本轴在 canonical manifest、当前公开文档、断言和受管投影一致；已发布 `.3` 与待发布 `.4`、历史结果可区分 | R575-02 |
| A575-03 | 当前公共入口和 Guru 消费者的定向真实调用通过，公共职责、原 Plan2/current-only 与版本族合同未改变 | R575-03 |
| A575-04 | 本次 source/installed、四投影、ownership、三平台 reapply/drift、权限/sidecar、secret/diff 检查覆盖实际改动 | R575-04 |
| A575-05 | 一个代表性 clean 样本及旧安装定向维护样本基于正式来源执行，native/下一 consumer/恢复/兼容回退结果逐层报告 | R575-01、R575-03、R575-04 |
| A575-06 | 本次唯一长期 Test 与双向 requirement/design/test trace 完成；Architecture 按独立结果承接；所需 promotion 经规定的前后独立门禁 | R575-05 |
| A575-07 | 完整 Stage 1 准备交付完成，PR 为 Refs-only；完成与归档不关闭 #575，不创建 `.4` tag/Release | R575-06 |
| A575-08 | 三份规划、官方 context JSONL、Delivery Policy 和 Docs SSOT Plan 无 TBD、无并行 owner，且不持久化授权或动态发布状态 | R575-07 |

上述是要求与验证计划，不是已执行结果。具体命令、前置、失败路由和证据归属由设计及执行计划固定；Stage 2 的 exact-candidate 要求继续引用 Issue 和私有 release contract，不在本任务复制另一份动态发布状态。

## 5. 非目标与未验证边界

不实施真实业务安装/迁移/部署，不修复其它 Open Issue，不修改上游/global npm/node_modules，不发布 Fork/npm，不重写历史 tag/Release/main，不建立新生命周期或发布 owner，不执行累计完整多平台/native-host Release 矩阵，不增加攻击、伪造、竞态压力或非常规加固。

本 Task 的隔离样本、静态检查或准备交付不能声明真实业务验收、生产恢复、最终 candidate gate、tag smoke 或软件发布成功。外部事实改变时，按受影响的原 owner 刷新，不从文件存在、旧 pass 或版本相同推导放行。
