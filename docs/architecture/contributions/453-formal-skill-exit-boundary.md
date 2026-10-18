# #453 公共 intermediate transport 候选贡献

Identity：architecture-453-intermediate-transport-v1；状态：task-owned candidate；path：target_native。
本文件保留晋升前 Architecture change contract；下列历史阶段陈述仍绑定原候选对象。当前状态仅由末尾「晋升状态」定义，实际执行证据归唯一 Test。

## Authority / constitution binding
Concern authority-binding：applicable。Guru 合同为 guru-maintain-architecture-baseline:2.0；baseline 为 docs/architecture/README.md 的 active current-main-0.6.17-guru.81；expected current identity 同为 .81。
项目合同为 docs/architecture/06-governance/change-contract.md：guru-trellis-architecture-change-contract-v1；concern set 为 guru-trellis-architecture-change-concerns-v1。
Concern constitution-binding：applicable。唯一 current authority 为 docs/architecture/00-foundation/design-constitution.md / guru-trellis-design-constitution-v1。
实际适用 refs：concept-semantic-completeness、cohesion-change-isolation、minimum-necessary-complexity、debt-one-way-convergence、mature-practice-applicability。适用理由是明确三层结果、保持 semantic/serialization owner 隔离、一个具名当前 stdout consumer 所需 envelope、current-only 直接迁移和官方 preset 扩展；不复制原则正文、不生成逐原则评分。

## Boundary / decision
Concern boundary-and-decision：applicable。Requirement authority 为 live castbox/guru-trellis#453 r1；behavior/decision authority 从 docs/design/README.md、docs/architecture/01-current/system.md 与当前 Skill package contract 读取。
Before：command metadata 只声明 single_json_object；部分 CLI recorder 直接返回闭合 owner object，checker 返回含 status/typed_exit 的内部 receipt，atomic helper 返回 typed 形状。IntakeCommands.forward 将真实 recorder stdout 直接设为 recorded，并直接从 checker stdout 读取 validation_receipt。
After：commands 1.1 显式声明 intermediate_receipt / single_typed_exit；dispatcher 将中间 stdout 包为 schema_version=1.0、formal_exit=false、result=原完整 payload。current CLI owner/eval caller 经验证后固定投影 result；trace 保留真实 stdout。正式 invoke 的 DTO、exit/consumer 与语义判断不改。
Change path 只采用 target_native，不增加第二运行路径。现有规则 refs 为 ARCH-GOV-006..009；决定 refs 为 ADR-005 的 baseline lifecycle、ADR-009 的 source/Closure owner 边界。该贡献不改变 source identity 或 Closure 责任。

## Owner / single writer
Concern owner-and-single-writer：applicable。当前/目标 semantic owner 均为原 Skill；AI 读取 authority、评估 scope、充分性、finding 和 route，dispatcher 不判断阶段通过。
原 package 继续拥有 owner/checkpoint schema、digest、record/check/execute/recover 与 supported atomic 能力；共享 dispatcher 只拥有 metadata 驱动的 CLI stdout 序列化和 receipt schema 客观校验。
当前具名消费者包括 CLI owner 的 owner_result/validation_receipt 投影、IntakeCommands.forward 和读取中间 stdout 的 native authoring/integration caller。原 public workflow consumer 只接 public invoke 输出。
本 task owner 单写 task-owned contribution/canonical 变更；shared Architecture/RDT current 仅由对应 promotion owner 按 expected current identity 单写，不引入新 store、writer 或持久化授权。

## Compatibility / exit
Concern compatibility-and-exit：applicable。commands 1.0 -> 1.1 与裸 intermediate stdout -> receipt envelope 是显式直接迁移。全部当前受控 metadata/caller/fixture 同步迁移；public Skill input/output 不改。
旧完整安装通过支持的 complete preset reapply/upgrade 同步 runtime/schema/packages/platform projection。混合版本沿已有 installed validator 阻塞；未覆盖的旧版本/update 路径在交付中保留 unverified。
没有旧 metadata runtime fallback、dual-read、旧格式 parser 或永久 adapter。旧 current selector 与直接读 intermediate stdout 字段的生产路径在同步 caller 迁移后退出；历史 schema/archive/ADR 只保留历史身份，不成为 runtime consumer。
退出验证由 task owner 完成：真实 record/check/invoke caller、digest bytes、atomic result/recovery、source/installed 与旧完整安装迁移。确认所有当前 consumers 已投影并通过后，旧 current 读取实现必须在本交付删除。

## GAP / deviation
Concern gap-and-deviation：applicable。该贡献修复当前 intermediate/public 边界缺口，不借此审计无关技术债；不重新打开已 closed GAP、不新增 lifecycle authority 或双写。
ARCH-GAP-006、ARCH-GAP-008 的当前状态与 owner 仍由 current baseline 维护；本 task 不声称关闭它们。缺真实 native 行为证据时 #453 完成仍受阻。
软件 Release、完整多平台矩阵、业务生产安装未验证边界保留；与本 task 无关的 historical debt 不转为阻塞或新 Issue。

## Parallel scope
Concern parallel-scope：applicable。允许本 task-isolated 规划、贡献、canonical 输出合同及它们的受控安装/平台投影；声明平台投影按当前 complete preset 同步。
禁止直接竞争 shared current、跨 task 的 GAP/owner、其他工作区改动与 #396/#250/#292 实现。当前 app worktree/branch 为 caller_owned；清理不推断删除权限。

## Evidence / freshness
Concern evidence-and-freshness：applicable。当前设计对象为 design.md 的真实完整 bytes，Architecture public invocation freshness 由独立 owner 与它读取的当前候选绑定；content token 不充当 approval 或授权。
设计责任为 command 分类、stdout boundary、闭合 owner payload 保留、消费者 projection、完整安装迁移与真实 Agent 接续。Before/after 以本文件边界段和实际实现/diff 为证据；Planning 审查机制与可验证性；Phase2 独立 owner 审查实际完整 worktree candidate。
后续客观 evidence 包括真实 dispatcher output schema、public exit/consumer、未污染的 owner/checkpoint/digest bytes、atomic 功能与单次恢复、副本/hash/mode/drift、一个 representative clean install 和旧完整安装 reapply/update。
后续行为 evidence 包括 checker-only 与 record+check 尚未 invoke 的两个真实 native Agent transcript，合法真实生成的 owner/checker output、声明和下一动作，覆盖正向与 non-pass route。Python/helper/keyword checks 不替代行为 evidence。
当前实现、source/installed 36 packages/109 commands 验证、真实 atomic Rebind wrapper、两个 native Codex 0.160.1 正向/blocked 接续以及代表 clean/predecessor migration/reapply 已执行。真实 trace 中 invoke 前均明确尚无正式出口，invoke 后消费唯一路由。current-only caller projection、内部 owner bytes/正式 DTO 不变与声明平台 drift 由定向测试和安装 validator 验证。既有生命周期 fixture 失败在前置 HEAD 复现，不计 pass。最后等价 Skill 文案/证据更新刷新独立 Phase2 identity；committed review 与 promotion 尚未执行。以上不把 Planning gate 投影成实现证据。

## Project-check protocol
当前 descriptor identity 为 guru-trellis-architecture-convergence:repository:1；check id/version 为 guru-trellis-architecture-convergence / 1；entrypoint 是 docs/architecture/06-governance/change-contract.md 的 AI 语义协议。
结果合同为 guru-project-architecture-check-result-2.0；适用范围为 stage invocation、authority binding、path exclusivity、required concern completeness、before/after regression、single-writer、parallel stale、contribution/ADR review 与 promotion freshness。
Rule refs ARCH-GOV-006..009，decision refs ADR-005/ADR-009，GAP refs ARCH-GAP-006/ARCH-GAP-008；独立 owner 亲自评估 Planning candidate 的 applicability、blocking 与 before/after，author 对应 descriptor-bound result。该文件不预填 project check pass。

## Review / promotion / ADR
Concern review-and-promotion：applicable。贡献 identity 为 architecture-453-intermediate-transport-v1；当前状态 candidate，committed review/promotion 尚未发生。Phase2 独立评估完整候选；Branch Review 独立评估精确 origin/main...HEAD。
独立 committed review 完成后，Architecture owner 按 expected current .81 串行 promotion；若 baseline 已变，走 sync_required 原路，不覆盖。晋升产生新 diff 后重新 Phase2、Task Commit 与独立 full-diff Branch Review，再进入 Publication/Completion。
ADR necessity：当前候选不提出新增 ADR，因为复用现有正式入口、semantic/执行分层、current-only 直接迁移和 baseline promotion 决策，没有新 owner、原则例外、GAP lifecycle 或长期 compatibility exit。独立 owner 仍需检查实际 before/after；若 discovery 出现该类变化，回到对应 Architecture assessment，不把此候选理由充当未来豁免。

## 晋升状态

Identity：architecture-453-intermediate-transport-v1；状态：reviewed_promoted；expected_current_identity=current-main-0.6.17-guru.81；promoted_identity=current-main-0.6.17-guru.82。完整实现范围 `origin/main@a080da319147fc9ccd6f85b10df60f3ce2e07e36...49c3e11ae9ce26fa391c038b6ba351adac25ff04` 已独立完成 committed Architecture 与完整 Branch Review，分别调用原公共 wrapper，Branch 实际出口为 passed。ADR necessity=false，既有 owners、GAP lifecycle、constitution 和软件版本轴保持。

本次按 expected `.81` 串行知识晋升；`.81` 为不可变 preimage，`.82` 是当前 authority。历史 candidate/pending 陈述不是当前 gate 状态；晋升新 diff 仍须 fresh Phase2、TaskCommit、不同 reviewer 完整 Branch Review，之后才能进入 Delivery。唯一 [Test](../../requirements-design-test-contributions/453-formal-skill-exit-boundary/test.md)保留实际验证、首次失败与未验证边界，不把原执行重标为后继文档候选重跑。
