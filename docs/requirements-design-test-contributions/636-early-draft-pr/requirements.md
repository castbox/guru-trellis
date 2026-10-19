# Task 与 Delivery 生命周期

知识单元：`RDT-REQ-LIFECYCLE`。状态：`proposed`。候选继承 RDT `current-main-0.7.0-guru.112`，固定前驱为 Git `b470580d4f79f61c66d72db97861fe1564b5e746`；更早迁移来源按该前驱保留。只有三层共享入口完成原 owner 晋升后，本单元才作为 successor 的当前正文；旧阶段仍使用其适用版本。

## 身份、整体责任与入口

`REQ-001/003/004/005/008/010`、`BEH-001..006`、`R531-01 / BEH531-OWNERS` 保持身份。Task 承担整个 accepted scope 的要求、来源和完成责任。Delivery 承担一个明确切片的独立规划、候选、检查、审核和交付结果。D1 与 D2 使用同一种公共 Delivery 模型；D2 不能覆盖 D1 的文档、历史或结果。公共 Task/Delivery 状态归官方 Trellis API，Guru 不另建状态机，也不写 schema-2 Task 的开发 `status`。

新变更先由原 mode owner 判断 standard intake 或 task-free；Issue 的存在、文件数和路径不能单独决定模式。标准 Intake 依次同步所选 base、发现当前变更上下文、澄清来源/要求、审查措辞及独立可交付性，再由原 Creation 创建 Task 和绑定的执行位置。信息查询不创建 Task。已绑定 Task 的变化走原当前 owner，不从 Intake 重建身份。缺失、重复或不唯一的公共身份、出口、consumer、安装合同或 checkout 关系须停止或进入其原恢复路线，不能由 inventory 的唯一候选猜选。

AI 判断 scope、来源、关联、finding、充分性和路线。确定性工具只执行明确动作、读事实或校验结构/内容绑定。mandatory step 由 global workflow 以稳定 Skill id 调用，step-local Skill 独占完整内部行为。semantic Gate 的脚本成功不代替语义判断。只处理诚实协作中的合法正常路径、普通错误与过期状态，不增加对抗伪造或未要求的并发/崩溃机制。公共 Skill/exit/schema/path 的破坏变化必须有显式迁移。

## 切片建立与唯一 Planning

`R531-02 / BEH531-PLAN` 与 `R292-01..12/14/15` 保留。原 Clarify 接受整个 Task 要求后，原 `guru-create-delivery` 在首次 Planning 前建立或明确选择 DeliveryKey、scope_ref 和上游 planning_root。创建只建立 Delivery，不另建 Task/branch/worktree。方案返工、base 变化或同一 PR 更新保留同 Delivery；确有后续独立工作才建立下一切片。局部 provider 缺口仅阻塞实际依赖它的场景，已经确认必要且独立的工作继续，consumer 不接管 provider。

唯一 `guru-author-task-plan` 写 Task 整体 PRD，以及选定 Delivery 的 PRD、design、implement 和 context manifests。Task 整体文档不冒充 D1 计划。Author 先充分读取真实来源，区分要求、已有规范性设计、建议、实现证据和历史；无法取得必要来源时说明缺口并沿原澄清路线。不能通过省略条件或把技术细化当需求改变来制造通过。

`R154-01..05 / BEH154-01..05` 保持。Task PRD 陈述整体要求；Delivery PRD 陈述本批目标、起点、前序事实、依赖及剩余责任。design 展开真实职责、契约、行为、条件、失败、兼容、来源承诺处置和可验证设计；唯一逐项规范性来源设计处置只在 design 维护。implement 明确有依赖顺序、验证、停止/恢复、唯一 Delivery Policy 与唯一 Docs SSOT Plan。full、partial、后续和返工均保留整体与本批区别；已有 detailed 承诺不能缩成标题或链接。章节、适用字段、裁剪和深度由 Author 的现行 planning-body/templates 定义。

Planning 在实质 solution 写入前先取得真实 candidate 的独立 Architecture assessment；Author 消费实际结果完成方案。最终文档经过独立 Wording、Architecture final_plan 和 Approval。无真实 candidate 不产生候选通过。Architecture/Wording/Approval 不代写 Author 正文；Brainstorm 仅在原 owner 之下复用方法。Approval 的当前正式结果交原 Activation；文件存在或 public phase 不是批准。

原 `guru-activate-delivery` 读取三份当前中文规划、明确切片及相邻 Approval 实际 freshness，完成当前计划展示/接受边界后，唯一使用公共 planning writer 记录真实 Planning 结果。调用方不能从文件重算 token 冒充 Approval。恢复读回同 operation/result，不重复公共写入；真实计划变化回最早受影响 Planning owner。授权仅存在会话，不写入任何 artifact。

## 固定内容范围、实施与返工

`BEH567-01..05`、`R531-03/08 / BEH531-REWORK/DEPENDENCY` 保持。开发基线、每个 Delivery 的固定内容 B..H 和 PR integration target 分离。原 owner 从真实 Delivery facts 选择 B；D2 消费实际前序交付结果。恢复保持同 B 和 DeliveryKey。候选覆盖 B..HEAD 全部提交内容及实际 dirty 增量，不用随 fetch 漂移的 origin ref 代替固定 B。

实施只在已核验的当前 Task checkout 写入。每个写批次前重新检查 TaskId/generation、branch binding、注册 worktree 和 cwd；不修改无关 dirty。source/test/task 文件均受同一边界约束。

whole-scope 变化先回原 Clarify；受影响 Delivery 的实际当前阶段 owner 读取新的整体 authority，合法 rework 后交同一 Author。仅清除受影响结果，不以旧 gate 资格阻挡 scope 修订，不改历史已交付事实。整个切片撤回由实际当前 owner 执行公共 stop/release，保留 candidate/commit/PR/history；停止不是交付或整体完成。PR 关闭及资源删除各有原 owner。

远端 ref、无关共享 CURRENT、archive 或工具版本前进，不强迫换源、同步、重写贡献或整链重审。实际冲突、必需检查具体集成失败、原 Merge 确认的既有服务端更新要求、明确依赖纳入或用户主动同步，才进入原 Reconcile；一次固定目标，按真实差额恢复原阶段，不追赶新目标或制造空提交。立即适用规则、scope、依赖和方案的实质变化仍回原 owner。

## 早期提交、Draft 反馈与并行候选验证

`R636-01..07 / BEH636-01..07` 由 #636 增加。TaskCommit 在已激活且处于实施阶段的当前 Delivery 中，以有界 AI 内容审查、最小自检、敏感内容检查、精确 staging 和目标核验形成早期真实提交。该提交仍执行原 hook/事务和同提交输出恢复，但不把完整 task Check、最终 Branch Review、全部编译或重型集成/race 作为统一前置。最小命中命令由当前 Planning 按风险选定。早期提交输出不证明任何最终 gate。

原 Publication 在同 Task/Delivery 的唯一同仓 Open PR 上创建或更新 Draft；正文准确区分已执行、失败、SKIP、未执行和待完成项目。冲突解决或问题修正形成新候选后，经原提交/发布 owner 更新同 PR，不在本地等待最终审核才能先发布反馈，不造空提交或新 Delivery。所有 Draft 和最终 Delivery 正文均 Refs-only；即使 full/default target，Issue 关闭仍由整体 Closure 独占。

同 PR 已 Ready 而需要发布未最终审核的修订时，由原 Publication 先读回真实状态/HEAD，合法 rework 失效受影响的 Check/full_review/readiness，并确保远端退回 Draft 后才推送新候选。身份、planning、固定 B、PR 与已发生历史事实保留。新候选取得全部适用最终证据后，才可沿原最终 Publication 再转 Ready；旧 HEAD 的 readiness 不放行新 HEAD 或 Merge。

Draft 后在同一固定 B/H 并行启动独立完整内容分析和风险匹配验证。目标分支前进不中断该内容审核。分支 HEAD H 的验证与目标 T/组合候选 M 的验证分别标识；文本冲突、没有 PR merge ref 或 pull_request CI 未触发不阻止固定分支内容审核和受支持 HEAD 命中检查。组合检查保留具体缺口及恢复条件，Draft 的存在不证明远端 CI 已执行。业务 CI 入口缺失由业务 owner处理，Guru 不因此接管业务 CI。

原 Branch Review 的早期分析结果只供当前实现/Check 判断和修正，不写 public full_review，不自动复用为正式 pass。正式 full_review 保留真实 Check predecessor；Check、完整独立 committed Review、readiness、Ready/Merge 各自判断实际候选。早期反馈不推迟、取消或降低完整最终质量义务。

原 producer 恢复已成功但输出丢失的 commit、Draft 创建、push、metadata 和 Draft/Ready 转换，先读回同操作实际状态/HEAD/payload，再接续剩余动作。不能创建重复 PR、空提交或以历史 Ready 冒充新通过。公共 I/O、阶段和受控 producer/consumer 必须显式成套迁移，canonical/workflow/platform/dogfood 同步；Draft 不是新公共 phase 或最终 PublicationFact，也不产生第二状态 authority。

## 最终检查、提交和独立审核

`R531-04 / BEH531-CANDIDATE`、`R530-01..05`、`R600-01..06 / BEH600-01..06` 保持。实施 owner 先完成受选 Docs 策略。需要晋升时，fresh 独立 Architecture Phase2 reviewer 对比晋升前 immutable authority，读取完整 tracked/untracked 候选、实际 consumers 与 proposed targets，形成真实 assessment。原 RDT/Architecture owners 核对 live expected-current 后，在本执行分支写入完整 reviewed successor，并核对实际内容和适用性；随后最终 Check 覆盖所有晋升写入。无变化不增加 contribution、ADR 或空阶段。

最终顺序是：独立 Phase2 assessment → 原 owners 晋升 → 实际写入适用性核对 → 完整最终 Check → 精确 Task Commit → fresh 独立 committed Architecture / 完整 Branch Review。ADR-030 仅替代旧“先 committed Review 再首次晋升”时序；独立性、expected-current、职责和后续审核义务保留。新 CURRENT 自身不能证明对晋升前约束的符合性，也不为补最终 SHA/Review 状态循环写正文。

Check 审查当前完整 scope、需求/设计/测试/兼容/Docs/Architecture 及实际 consumer；若产生真实候选问题，按正常场景/机制/因果准入，不能用恶意篡改构造范围。完整审查没有候选时使用真正空集，不制造占位finding；空集或全 rejected 均不自动等于通过。工程命令结果只证明其实际层次。

dirty 候选由原 Commit 精确 stage/commit；clean 已提交候选在 fresh Check 和当前公共适用性下直接进入首次完整 Review，不制造空提交或重复提交。Branch Review 读取固定 B..H 全部 diff，包含晋升和非本次最后提交；Phase2 pass 不代替独立 committed 判断。finding 修复回最早受影响 owner；修复后的最终结果覆盖实际最终候选。窄 promotion-reference alignment 只在原 Review 明确合同内采用，不能代替未执行的完整审查。

## 交付事实与整体完成

`R531-05 / BEH531-FACT`、`R434-01`、`BEH-557-01..04` 保持。Delivery Review 判断本切片 readiness、真实中文 PR 载荷、验证层次、安全和部署影响。所有业务 Delivery PR 使用 Refs-only；即使目标是默认分支且本批 full，也不提前关闭源 Issue。Publish/expected-head Merge 仅执行其已审查事务，实际远端成功、公共投影和当前 gate 适用性相互区别。输出丢失从原事务恢复同一实际结果，不重复 push/PR/merge；历史成功不制造新 pass。

已正式发布的 Delivery 后来被人工合并时，只能由原 Merge 的显式 recovery 读已有公共 Task/Delivery/Publication 关系、真实双亲合并及实际 head，记录事实并进入整体 Completion。事实不要求伪造 trailers，也不要求第二次 merge。实际内容变化、CI、gate 适用性和未覆盖范围由 Completion/受影响原 owners 判断，不能凭 MERGED 推断完成。

Delivery 合并只产生 slice 结果。Task 未分配范围、未完成要求和缺失必要证据仍归整体 Completion。Completion、Closure、Finish、Cleanup、Reactivate 的完整能力定义在 [completion-closure](../../requirements/current/completion-closure.md)。

## 关系和来源边界

设计：[`RDT-DES-LIFECYCLE`](../../design/current/task-delivery-lifecycle.md)。测试：[`RDT-TST-LIFECYCLE`](../../test/current/task-delivery-lifecycle.md)。知识 owner/适用性：[`RDT-REQ-KNOWLEDGE`](../../requirements/current/knowledge-maintenance.md)。来源及精确替代范围见 [迁移追踪](../../requirements-design-test-contributions/331-current-effective-knowledge/traceability.md)。公共 profile/DTO/exit 的完整规格仍由 [canonical workflow](../../../trellis/workflows/guru-team/workflow.md) 和对应 [Skill packages](../../../trellis/skills/guru-team/packages/) 独占；本单元拥有上述能力行为，不复制 schema。

## #636 拟晋升范围

本文件是受影响生命周期单元的完整 proposed resulting definition，继承 RDT `.112` 的其他仍有效条件；只增加上述早期反馈时机及必要迁移，不改变整体 Completion/Closure 或晋升时机。未受影响的 completion、knowledge、native 单元不复制。来源为 [#636](https://github.com/castbox/guru-trellis/issues/636)、当前 accepted Task/D1 计划；追踪关系见本目录 traceability.md。共享晋升与实现验证仍待原 owners 完成。
