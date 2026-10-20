# #637 D1 候选审核与验证复用需求

## 1. 整体来源与术语

整体authority为公共Task accepted_scope，定位[整体PRD](../../prd.md)及其当前sha256 revision；本批scope_ref覆盖AC637-01..10。Direct Source为[castbox/guru-trellis#637](https://github.com/castbox/guru-trellis/issues/637)完整正文和无评论，updatedAt=2026-10-19T16:24:30Z。本DeliveryKey=5499bb2d-86d7-4a5c-9747-9b06e00f4ef9，planning_root=deliveries/5499bb2d-86d7-4a5c-9747-9b06e00f4ef9。工程事实、语义判断、Git/PR事实及Task/Delivery术语按整体PRD第1节，不混为通过。

## 2. 整体与本批目标、非目标

本批是首次完整D1，承担整体八项要求、十项验收。已有#567固定候选/整合差额和#578事实采用正确能力；本批统一跨Architecture、Check、TaskCommit、BranchReview、DeliveryReview/Publication、Merge及continuation的失效与复用合同，清除无条件全新完整重审。后继候选须以真实原覆盖、已审差额及受影响依赖形成精确当前结论，保留首次独立完整审核。

排除Backend业务/现场、#638/#635实现、队列前置、完整Release矩阵、tag/Release、恶意伪造/绕过、锁/压力/非常规crash。禁止新审计链、全链digest、他人私有读取、重建退休checkpoint、长期review/test账本和持久化授权；不跳过真实失败或降低断言。

## 3. 本批起点、前序结果、依赖与剩余责任

本Task尚无前序Delivery。本批起点main@39169628f5f79cb48673eae96a36670e73f4dbbb；内容基线B与PR target main分开，H0为该起点，实际实现HEAD由原owner后续固定。#636业务PR642及归档PR643已MERGED并可达该main；本批作为后交付项完成双方实际已安装接口组合。#638尚未交付组合接口，明确未验证并由后项负责，不作关闭前置。

本批完成后整体未交付业务范围应为空；Completion仍核全部要求、证据与所有satisfying PR，Closure/Finish/Cleanup保留各自原owner。静态、Agent、命令、安装、远端和生产效果分别表述，#693历史总耗时不冒充优化收益。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置与触发 | 处理行为与可观察结果 |
| --- | --- | --- |
| S637-01 首次完整审核 | 首次候选进入独立 Architecture/Branch Review | 未参与实现的实际职责完成完整审核；Planning及自检不替代 |
| S637-02 同树与定位变化 | 原 owner 接续同树提交、引用/导航/版本对齐或无关目标前进 | 核实际语义和依赖，仅刷新必要绑定或差额，无无因全链重审、重测或整合 |
| S637-03 文档冲突整合 | 已有完整覆盖，正常解决冲突产生新候选 | 检查双方语义、组合影响及未修改消费者；形成当前完整覆盖正式结果 |
| S637-04 依赖变化 | Runtime/事务或检查输入、环境、期望改变 | 扩到受影响消费者，补跑命中检查并检出具体缺陷 |
| S637-05 证据与恢复 | producer checkpoint 已消费删除，换会话/reviewer或原证据不足 | 从合法来源取得最小依据，缺哪段补哪段；影响无法界定则完整审核 |
| S637-06 finding修正 | 原finding owner或真实替代者复核修订 | 验证闭合及受影响覆盖，无无条件全新完整相同审核 |
| S637-07 发布合并 | 已审当前内容进入Publication/Merge | 核自身payload、Issue语义、候选及live事实，消费既有适用内容审核 |
| S637-08 早期Draft组合 | 经#636实际安装入口创建/更新同一Draft | 固定内容审核和HEAD验证接续，保留同Task/Delivery/PR及最终门禁 |

首次完整候选保持原独立审核。后继同Delivery候选先判断实际变化、合法原证据、受影响依赖与保留/失效/补充范围；当前owner完成真实语义并走其原正式结果。证据不足补缺，影响无法界定则完整审核。真实需求/设计前提变化回最早受影响owner；普通阶段或身份变化不自动失效工程事实。

## 5. 完整行为、条件与约束

R637-01..08按下列来源顺序展开，并关联整体PRD第4节S637-01..08。规范性来源设计在本批design第3节单独处置；本文不自选新API。

1. 首次候选取得完整独立审核。后继候选由审核 owner 读取原覆盖证据、真实差额和受影响依赖，说明保留、失效和补充范围，对精确当前候选形成结论；不能机械复制旧 pass。
2. 统一区分工程执行事实、语义判断和 Git/PR 事实。同树提交仅刷新提交绑定；无关基线前进不触发整合或业务门禁失效；实际冲突解决检查双方语义、组合影响及未修改消费者，不限于冲突几行。
3. 输入、依赖、工具链、环境、参数、检查定义和期望未变且原证据可验证时复用工程事实；变化、证据缺失或适用性不明时补跑命中检查。文档改变行为时按实际影响检查，不按文件后缀豁免。
4. Architecture 与质量审核的独立性以未参与当前实现的实际职责为准。一次合规独立审核支持先形成架构判断，再完成完整实现审核；无新架构事实时不额外启动串行独立评估来重建同一理解。不得让作者自批，也不以 reviewer 身份变化自动失效原工程事实。
5. 解决整合或 finding 后，审核修订及受影响范围。取消无条件更换全新 reviewer、重新执行完整相同审核的要求；原覆盖不足或影响无法界定时扩大审核，明确依据。
6. Publication 与 Merge 核对各自当前交付内容、Issue 语义、候选及 live 合并事实；无实质变化时消费已完成的内容审核，不重复业务设计评审。
7. 审核中的 base 前进不改换固定对象；明确需求、设计前提或依赖变化仍返回最早受影响 owner。支持同一 Delivery 的中断恢复，不强制新建 Delivery、空提交或证明账本。
8. 将失效与复用规则收敛到唯一合同并贯通 producer/consumer，清除相互抵消条款。必要公共 API 变更提供版本和在途迁移；不新增审计链、全链 digest 或持久化授权。

复用优先读取现有 public Task/Delivery 结果、精确 Git 对象、当前正文及仍可核验的原始命令结果。不得为了复用而读取其它 owner 的私有 checkpoint、重建已消费 checkpoint，或新增全套长期 review/test 账本。若现有正式结果没有保留下一 consumer 确实必需且无法重新推导的最小覆盖结论，本项负责明确该 consumer 与最小兼容迁移；不能只写“复用原证据”而没有合法读取来源。

原审核 Agent 仍可接续时，保留其已经建立的理解，重新判断实际差额。换会话或 reviewer 时，先确认现有证据是否足以承担当前判断；缺失哪段覆盖就补哪段。最终组合影响无法界定时执行完整审核，不把身份变化本身当作充分失效原因。

Planning 的方案判断、实现者自检与首次独立内容审核继续区分。一次独立审核者能够依次承担 Architecture 与 Branch Review，不代表用实现者自检冒充独立判断。删除的是没有新事实却重建同一评估的流程要求；原 owner 对当前职责的适用性判断与正式结果仍须真实完成。

引用对齐、版本与导航文本也须核其行为含义。“同树”只解决内容相同的绑定问题，不自动证明环境、依赖或 required check 未变。

初次独立判断、Plan和作者自检保持职责区别；可由合规独立审核者依次完成Architecture和BranchReview。引用/导航/版本按行为含义判断；同树不证明工具链/环境/required check不变。Publication/Merge核自身payload、Issue语义、HEAD/live事实，不能消费旧pass替代新候选判断。

## 6. 本批验收、验证方式与未决项

AC637-01..10与整体同序，本批全部承担；从真实标准owner入口和#636已安装接口观察，不预填通过。对应场景与预期：首次完整独立审核；同树/定位/无关目标无无因重审重测；文档冲突原覆盖加差额形成当前正式结果；共享依赖改变扩审检错；退休checkpoint后合法来源；缺证据补缺；finding闭合命中范围；#693同构分阶段耗时；#636组合及#638未来边界；canonical/runtime/platform/install/reapply/drift/在途恢复。

- [ ] AC637-01： 真实标准 owner 调用链证明首次完整审核仍成立。
- [ ] AC637-02： 同树提交、纯定位对齐及无关目标前进，不发生无依据的完整重审或无关重测。
- [ ] AC637-03： 原完整审核加文档冲突解决差额，能够形成覆盖当前最终候选的正式结果。
- [ ] AC637-04： 实际共享 Runtime/事务依赖改变时，扩大到受影响消费者并检出具体缺陷。
- [ ] AC637-05： 原 producer 已消费并删除其私有 checkpoint 时，下一 owner 仍从声明的合法来源取得最小适用证据；不读取私有状态，也不新增证明账本。
- [ ] AC637-06： 原证据不可获得或覆盖不足时，补齐真实检查，不直接继承通过。
- [ ] AC637-07： finding 修正后验证闭合及受影响覆盖，不无条件重建全套独立审核。
- [ ] AC637-08： 对 #693 同构样本记录各阶段语义工作、命令执行、正式记录和远端等待耗时，证明删除了重复工作；不预设固定性能提升比例。
- [ ] AC637-09： 与 #636/#638 中已实际可用接口完成命中组合回归；尚未交付的接口明确为未验证，由后交付项完成组合验证，不把缺失接口或另一 Issue 的关闭状态作为本项全部验收的替代。
- [ ] AC637-10： canonical/runtime、平台投影、dogfood/reapply/drift 和在途恢复通过。

验收记录分别标注语义工作、命令执行、正式记录及远端等待。需要实际Agent判断与正式结果的项目不能由fixture/scanner自证；未执行、失败、SKIP及外部缺口诚实保留。当前没有产品选择缺口；最小公共覆盖来源、兼容迁移和测试机制交Author/Architecture细化，必须在solution完成前收敛。

## 7. Canonical 引用与本轮差额

[现行需求](../../../../../docs/requirements/current/task-delivery-lifecycle.md)、[现行设计](../../../../../docs/design/current/task-delivery-lifecycle.md)、[现行测试](../../../../../docs/test/current/task-delivery-lifecycle.md)分别承接Task/Delivery固定候选及#636早期Draft；本轮增加统一适用性/复用，保留其既有职责和首次完整审核。

[Architecture](../../../../../docs/architecture/README.md)当前.104、[constitution](../../../../../docs/architecture/00-foundation/design-constitution.md) v1、[change-contract](../../../../../docs/architecture/06-governance/change-contract.md)九concern与project-check为本批authority。独立candidate assessment在方案正文前，final_plan在Wording后；Phase2晋升和committed Review时机保持。canonical扩展位于trellis/workflows/guru-team、trellis/skills/guru-team、trellis/presets/guru-team；配套安装副本经原installer同步，不单改dogfood。
