# #531 Task / Delivery 集成与切换

本文件是 Guru 私有合同迁移的支持边界，不是公共 Delivery 模型的第二定义。
公共合同来自明确的上游安装候选 `.trellis/delivery-contract.md`，
Task schema 2.0 / Delivery API 1.0。当前绑定：

- 产品提交：`castbox/Trellis@1e40014023de53ddfd9368b3fb4d0a7a31e92293`，PR #36 已合入，build CI `38339653228` 成功。
- 当前已审查本地 mixed CLI tar SHA-256：`5aeeb81ca72508081b7dd94ddb7a19f69444714f78b3a38858d908196cc77916`；`185ed1db6865b72138bb10b6d799225721bf50fddfb370f84d8ec330558f472d` 为前驱CLI历史身份。
- Core tar SHA-256：`45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967`。
- 包版本 `0.7.0-castbox.3` 仅用于组合诊断，不能替代这些内容身份。当前mixed CLI包含已审查schema/binding修订；它不是正式source-lock，PR36成功事实也不证明后继PR38 CI或Release通过。

本地 source snapshot fingerprint `17ea37fbfcfe81a7e2c43f223cacdeee6ebd4c90cd28fff74c143a75bebd1a50`
独立于产品提交和 tar；未初始化 gitlink 的 manifest 记录不能冒充 committed tree identity。
前代 `5181ab…` / CLI `6763278…` 的 worktree-copy collision 和停止点保留为历史，
不换包接续其已冻结 Plan2、私有计划或 rollback anchors。

`ce36314b` 是已合入PR #32的历史前代；不能证明当前Guru候选、联合验收或软件发布。
下文“上游D1/D2”仅指接口集成/迁移采用交付阶段，某Task首个和后继Delivery没有激活分叉。

## 安装支持与两步交付

| 目标 | 准入 | 未满足时 |
| --- | --- | --- |
| 受控新 schema-2 安装 | 固定同源 Core/CLI、真实公共模块与 workflow owner declaration、完整 matching Guru candidate | 应用前诊断，不使用版本字符串或模型 fixture 代替能力验证 |
| 已有 legacy 安装 | 上游 D2 已审查公共 Task/session/默认流程迁移，加 Guru 私有迁移及目标组合验证 | 保持原完整固定发行包；不应用新 writer，不先删旧字段 |
| 原业务 Task | 原 owner 对精确来源、Task/Delivery 与资源的迁移和恢复 | 本 Issue 的受控副本验证不授权修改原树 |

开发和新装集成无需等上游 Issue CLOSED。公共 Plan2 `collectMigration2Templates`、
`migration2TemplateCandidate`、`migrate2`、`validateTaskV2Projection` 及公共归档/会话
转换由上游提供，Guru不推测接口或替其实现。上游#31按2026-10-13正文独立验收；
隔离旧SDK/Plan1/legacy workflow的最终退休归后续breaking release，不设为Guru切换前置。
Guru仍须自行完成同一候选对的私有迁移和联合验证。
新包直接演进 controlled consumers，不保留活动 Task-status fallback 或永久双写。
尚未切换的旧安装继续运行自己的完整发行包。

## 身份与规划

Task 保留身份、来源、整体 accepted scope 和完成责任。Task 根 `prd.md` 是整体
需求入口；Delivery 三份规划和 context manifest 解析公共 `planning_root`。
`guru-create-delivery` 在首次规划前创建明确 UUID 并选择切片；其同 owner 恢复不从
inventory 猜 identity。返工和多个 commit 保留同 Delivery，下一切片取得新 identity。

`guru-approve-task-plan` 的 Guru freshness token 仅交 `guru-activate-delivery`。
新 Activation 在当前计划展示/接受后写公共 Planning result；公共 result_id 是
实施及正式 Check 的 predecessor。两个 token 不混用。旧 `guru-activate-task`
的首次 Task 激活、活动 Task resume 和 status writer 退出当前 schema-2 流程；
旧输入不会被静默解释成 Delivery 输入。

既有 Skill 使用独立 `delivery_<existing_profile>` 输入与逐出口 `delivery-1.0`
schema；无 Delivery 的 Completion/Closure/Finish 使用 TaskKey。旧 DTO 缺失
Delivery identity 时必须回原恢复/迁移 owner，不能从 cycle_ref 或邻接字段补造。

## 历史、候选与恢复

迁移先只读盘点旧 active/archived、session、branch/worktree、多个 PR/cycle 与
在途事务。旧 status 和旧 gate 只作线索。Merge/history 原 owner 从 first-parent
trailers 和 GitHub 核验归属；上游迁公共数据，Guru 原 owner 迁自己的最小私有关联。
无法唯一归属时诊断，不重建 Task 或任意指定 D1。

clean已提交业务候选不重复提交。Plan2五规划路径映射由原TaskCommit核验原commit/blob与祖先关系；完整旧安装的真实tracked产品增量由原Upgrade盘点，沿独立Git边界单独处置安装内容，不提交未来五规划/gate或无关文件。安装commit后refresh实际candidate/freshCheck，原committed_reentry验证真实clean并进入首次完整独立Review；零安装增量保留原HEAD、零新commit，待处置不冒充clean。
dirty 必要提交改变 HEAD 后，按当前 Reviewing owner 的合法 rework、实施 begin_check、
Check 适用性重审接续完整 Review。有效测试不因形式上的 phase 变化被迫重跑。

Publish/Merge 真实成功而公共投影失败时，原事务 owner 核验同 PR/candidate/result，
接续公共记录，不重复 push、建 PR 或 merge。`historical_success` 只恢复真实事实，
不创建当前 Planning/Check/Review/readiness pass；继续执行由当前原门禁判断。
旧publication保留到新事实已验证并投影成功，不另加历史ledger。archived store拒绝重复record；原语义owner为prospective Plan2目标记录给出完整PublicationFact+DeliveryFact，原Merge消费已转换exactfacts并核验真实PR/commit/parents/base后只读恢复；缺facts回原转换，不reopen或私写schema。

## 退出与整体收尾

### #547 Closure 保留 OPEN 的增量合同

Closure input `guru-complete-task-closure-input-2.0` 与 Finish snapshot
`guru-finish-task-closure-result-snapshot-2.0` 在原 action disposition 中增补
`retain_open`。字段、既有枚举、ResultRef/TransactionRef 和 typed exits 不变。
`exact_source` 是来源关系与关闭资格，不是本次必须关闭的决定。Task scope
经原 owner 正常修订并完整完成后，Closure 审查源剩余责任，选择 retain_open，
冻结同一 source/generation，观察 OPEN、零 close；Finish 消费同一 frozen action
set，重验 retain=OPEN、close/already_closed=CLOSED，并保留 scope/历史/未验证边界。
状态漂移回原 Closure owner，语义 blocked 在 identity/uniqueness 后、执行资格前返回。

本增量直接演进受控 producer/consumer：使用新枚举前必须成套安装匹配 Closure
package、Finish package、schema 和声明平台投影。旧 consumer 不理解新枚举；
不能单独更新 Closure 然后把新事务交给旧 Finish。没有新枚举的既有输入和事务
仍按原动作恢复；含 retain_open 的事务由该匹配新组合恢复，不降级解释。
不添加 reader fallback、第二公共模型或 authorization 字段。

aggregate closed 表示集合含 close/already_closed 动作；公共 Task2 source_closed
只由 exact source 的动作决定。源 retain、另一 Issue close 时 aggregate closed，
公共源结果为 no_mutation/source_result=null，不能从另一个 Issue 推出源 CLOSED。
公共上游 Task2/API1 原合同和最小 Closure-to-Finish ResultRef 不变。

受控新 schema-2 安装与未迁移完整旧安装仍遵守前述支持表。本增量的源/投影测试
不自动升级实际旧安装，也不证明原 CMS Task 恢复；真实采用由原 Upgrade/业务
owner 完成公共与私有迁移后运行正式收尾。当前 app 旧模型继续固定整套运行包。

部分 scope 修订在同 Delivery 返工；全范围撤回由 scope owner 判断后由当前阶段 owner
停止并释放选择，保留 Task、commit、PR 与身份。PR 关闭和资源清理各走原副作用边界。
全部已知 Delivery 交付也不能推出 Task completed；Completion 还须判断未分配 scope
和证据。仅补证据、Reactivate-only validation 和 closeout 不创建空 Delivery。
Closure、Finish、Cleanup 分离；新 generation 不复用旧 gate/收尾结果。

## 切换与验收

更换最终来源须fresh prepare；旧077模板/checkpoint只在原来源same-plan恢复，不换包继续或刷新rollback anchors。最终schema2 create/start不创建Delivery，custom隐式reinit保留workflow/mode/receipt。所有registered workspace及common/local session参与盘点，prunable sibling判断交上游。安装commit改变Git事实，恢复/rollback重新验证适用条件且不rewind Git。

公共 Plan2 的 `branch_bindings` 只接收原 binding 的 TaskId、generation 与 raw snapshot。
唯一 active authority 的选择和继承副本组合法性由公共 executor 验证；Guru 不指定
binding target/action/path，不复制 group 判定或新增 binding writer。全部 eligible
registered roots、occupied archives、各分支五规划与 common/local sessions 保留完整盘点；
unique active Task 的 live binding 同样必须纳入。`defer` peers 保留 Task、规划及 modes，
不创建 Delivery、Guru 私有迁移关联或另一状态 authority。普通 source/binding/topology
变化回原 prepare；同 plan 输出丢失和 rollback 仍消费原来源及原 anchors。

应用前验证支持组合；原 owner 恢复既有事务事实；公共和私有迁移各自完成后成套应用
新 reader/writer。用公共 query 核验 identity/selection，再验证 native continuation。
用户修改按官方 template-hashes / `.new` / `.bak` 合同保留，未解决冲突不算 reapply 成功。
历史 reader 只服务其明确迁移/恢复 consumer，最后 consumer 退出后删除。

本次迁移的实际交付结果由 [Guru #531](https://github.com/castbox/guru-trellis/issues/531)
及其仓库内唯一 Test 记录；该记录不属于安装包的公共合同。
canonical、dogfood、installed、声明平台、reapply/drift、#149/#444/#155 类旧断点、
多 Delivery、返工/退出与结果丢失分别记录。受控样本与真实 GitHub、上游原生与 Guru
joint、设计/实现/原会话恢复分别报告；本 Issue 不执行完整 Release 矩阵。


The delivered #530 clean-candidate owner is preserved through the explicit
Delivery input. A missing selected Task base remains a precise
`stale_identity/base_branch` diagnosis; migration does not invent `main`.
Current public Check applicability and exact candidate HEAD replace the legacy
Phase 2 capture checkpoint. Stable committed identity and the bounded five-blob
planning source bridge handle actual Plan2 relocation; neither admits tracked
installation increments, changed planning, nor a missing full Review.
