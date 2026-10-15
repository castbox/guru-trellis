# #566 Architecture contribution（task-owned candidate）

本贡献承接 current-main-0.6.17-guru.90，不是shared CURRENT。机制唯一正文在当前Task design.md D2-D7；晋升时移至durable RDT Design并更新locator，不把active Task路径变成长期authority。

## 边界与变化

change_path=legacy_boundary_convergence。before：ADR-017/018 source-loaded完整升级以core_plan整仓处置为唯一旧安装边界；公共/私有角色仍分离。after：两个独立source-loaded semantic维护闭环，公共执行只委托Trellis maintain；旧完整Plan2与普通current-only保持。原交付owner新增只读旧事实入口，原runtime owner提供primary/linked目标隔离。

## 适用 concerns

| Concern | applicability 与真实处置 |
| --- | --- |
| authority-binding | applicable；Planning3.0 candidate/final分离，baseline.90与currentchange-contract-v1 |
| constitution-binding | applicable；唯一constitution-v1；最小必要复杂度、职责隔离与有界legacy退出用于实际新能力，无评分表 |
| boundary-and-decision | applicable；ADR-017/018旧维护入口需显式变更，ADR-024公共Taskauthority保留；ADR candidate同目录 |
| owner-and-single-writer | applicable；AIsemantic、公共model执行、Guruprivateasset/state、runtimepointer、Reconcile与Completion分别原owner；Author只写planning |
| compatibility-and-exit | applicable；真实0.6/0.7来源一次性转换/历史保留，旧Plan2是独立现存consumer；新入口无currentdualread；legacyprofile退出由后续明确migration删除 |
| gap-and-deviation | applicable；只处理本次新入口耦合与sharedpointer影响，不关闭ARCH-GAP-006/008或把上游localcandidate晋升正式能力 |
| parallel-scope | applicable；只写Task隔离贡献和本任务source；禁止并行共享CURRENT/GAP/业务target/其他Task改写 |
| evidence-and-freshness | applicable；before/after绑定actualdesign与publiccandidate；目标native、peerbytes/runtime、原owner输入及恢复组合需实现期证明，目前unverified |
| review-and-promotion | applicable；当前仅reviewedcandidate供Planning；首次独立committed full-diff Review后由原owner按expectedcurrent晋升，再fresh Phase2/commit/Review |

## 当前证据与限制

Planning 时尚无本任务实现证据；以下 Phase 2 当前事实取代该阶段的待验证陈述。上游公共层通过不独立关闭 Guru 联合证据。source_locked 仍绑定原正式锁，缺公共 API 时写前阻断；local_candidate 不成为正式来源。工具升级、数据转换、原生续接、历史交付核验、业务完成分别报告。无新锁、通用事务框架、授权 artifact 或 reviewer ledger。

私有退役具体入口、写集、preserved-source输入与Publish→Merge→Finish→其他已选gate顺序由design D5独占；公共保存源后不再依赖active tree。新profiles仅由所选维护consumer调用，不制造Completion或资源清理。

## Phase 2 当前候选的架构事实

独立读取 current constitution、Architecture 与 change contract 后，从完整 tracked/untracked 候选的控制边界、受影响调用者、公共模型调用与真实恢复路径形成判断：`architecture_impact`，唯一路径 `legacy_boundary_convergence`。旧 Task 的当前安装仍使用原 `task_impact_sync:2.0/phase2`；不为调用新安装的 Delivery profile 伪造公共 Delivery。

before：旧工具更新与 Task 处置由完整 Plan2 组合；primary Python 默认指针可被多个 checkout 消费。after：两个独立 source-loaded semantic owner 各有具名消费者，公共 Task/session/binding 与恢复继续由 Trellis 单写；Guru installer、原控制 owner 与 managed Python owner分别处理自身资产。工具模式只增加 checkout-local override，普通 activation 后续更新同一 effective path；Sync 继续要求 clean 且保留其同步职责。既有 binding 的未提交合法转换由原 Identity 读取，不把旧 HEAD 当转换后的 Task authority。

现有九项 concerns 均适用：原 authority/constitution 绑定、单一兼容路径、公共模型与私有控制的原 owner、可读 preserved source 后退役、固定 operation/preimages、隔离任务贡献与 shared-current promotion，以及阶段 freshness 均有当前 consumer。两项新增能力分别承担工具独立更新和原 Task 真实续接/历史保留，删除其职责会恢复当前耦合；无需通用策略引擎、第二 Task writer、普通旧格式双读或另一审批链。ADR candidate 必需，因为它明确修订 ADR-017/018 的完整升级唯一入口限制；ADR-024 的公共 authority 与业务完成边界保持。ARCH-GAP-006/008/012 不因本候选重新开启或额外关闭。

亲自执行的当前证据：source runtime validation 通过（40 packages / 125 commands）；tools 定向 9 tests 通过，真实共享 fixture 写入 harness 未重放而 skip；matching packed public candidate 的 legacy maintenance 5 tests 全通过；matching public Python assets 的 branch substrate 37 tests 全通过。对实际已安装目标只读执行 installed/native/public operation 校验均通过。对受控三平台安装目标，亲自经其 managed resolver 执行 installed validator：40 active IDs / 125 commands，conflicts、sidecars、removals 均为零；只读检查原 source-first apply、fixture-own reapply 和原 dogfood drift 日志，drift 报告 canonical workflow、平台投影和 spec copies 一致。首次 self-apply 缺失旧 manifest 及误以文件运行 Python 模块的诊断保留为验证过程限制，均不当作正确调用的产品回归。

剩余边界：完整 tools 安装/peer preservation 的端到端写入沿实际执行 owner 的原始证据，本评估不重放共享 fixture 的写入；第二解释器 effective-pointer、full-upgrade-pointer 与 C4 专项只读检查原实际日志，未在本轮重跑。正式 Fork source lock、真实业务采用、外部 GitHub 历史链和完整 Release matrix 未在本评估验证。官方首页、自定义 workflow 与 spec marketplace 文档已在线读取；当前候选使用 Markdown 控制面、公共 maintenance SDK 与 preset installer，未修改上游 framework/hooks。上述限制不用于关闭兼容 GAP、批准正式安装或发布。独立 committed full-diff Branch Review 与 expected-current-bound promotion 均仍待执行，本贡献不是 shared current。
