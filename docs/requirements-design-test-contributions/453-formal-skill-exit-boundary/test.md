# #453 Test contribution

候选，未晋升。继承 Test `.81/active`。客观 transport 与真实 Agent 行为分开报告；下列是本次实际 candidate 的定向验证，不能代替后续 committed review。

- T453-01：current source registry/interface 的 36 packages/109 commands 分类与闭合 receipt schema；dispatcher 测试覆盖 owner、checker、typed-shaped atomic intermediate 和不变的正式正向/非通过输出。内部返回与旧 commands 1.0 历史 schema 不变。
- T453-02：各 package 的 current regression，实际 Wording record/check/invoke 正向、blocked 与 content_changed；Planning、Phase2、Branch Review、Reconcile、normal/root/solution qualification、Activate、session/identity/binding、task-free 和 deterministic Base Sync 定向回归。原 atomic/恢复能力由其原 owner 的测试及真实 wrapper 继续验证。
- T453-03：Intake semantic authoring、Phase2 authoring、Stage0 caller、实际 Wording stdin integration；测试 fixture 明确携带当前 shared schemas，不添加旧格式 fallback。trace 留真实外层 stdout。
- T453-04：一个 codex clean complete preset 和 HEAD `a080da3` 的完整 predecessor 安装再 apply/reapply；当前 dogfood 声明的 Claude/Codex/Cursor 投影与 reapply/drift/hash/mode/sidecar 检查。每个应用备份与实际 preimage 一致并另存后退休。完整官方 marketplace init/update、多平台 Release matrix、其它旧版本及业务生产升级未验证。
- T453-05：本机 native `codex-cli 0.160.1` 两次真实业务规划接续。checker-only 已持有真实 owner result；record+check 使用真实两条 stdout，均由当前 AI 完整审查三份规划与源后经原 recorder/checker 生成。正向场景为明确 30 天订单保留，非通过场景为产品未定期限。AI 审查完整 command/action/message transcript：两者在 invoke 前都明确尚无正式出口；无重复确认、重做已完成动作或提前执行 downstream；真实 invoke 分别为 `pass/planning_artifacts` 与 `blocked`。正向组消费 workflow router 并读取下一 owner entry，阻塞组消费 `contract-wording-blocked` stop。native harness 只 replay 和保存 transcript，不 author/grade gate。

本地证据由 Phase2 owner 消费：`/tmp/guru453-native-positive-transcript.jsonl`、`/tmp/guru453-native-blocked-transcript.jsonl` 及对应 fixture 中实际 invoke stdout；临时日志不进入公共 package。两次 run 证明本机这两个正常路径，不声称所有模型/业务仓都消除了误报。

当前全范围回归曾检出旧 caller/schema fixture，已迁移后重跑受影响集合。前置 HEAD 可复现的生命周期 fixture 缺口与本次变更分别比对；历史失败不计 pass、不扩张本任务修复。实际最终结果：source 与 clean/migration installed validator 均通过（36 packages/109 commands）；Solution 24、adapter 27、Rebind 实际 wrapper 3、Wording stdin integration 1 个测试通过。Runtime 原 4 个失败修正当前 count/schema fixture 后定向重跑通过，未重复无变化的全套。Cleanup/Closure/Finish/Reactivate/Completion pytest 合计 149 passed、14 Closure failures；相同 14 项在前置 HEAD 复现。Create Task Commit、Merge、Publish 的当前失败已按具体 test/首次诊断与前置 HEAD 对照，均为既有 fixture 失败，不计通过。Discovery 的 binding error locator assertion 在前置 HEAD 同样失败；其实际 CLI integration 另有本次遗漏 result projection 导致的新 KeyError，已由独立 Branch Review 记录 BR453-DISCOVERY-PROJECTION，并在 finding-fix 中迁移，二者不能合并归因。代表安装实际 Wording 正向与 blocked invoke 都通过。最后等价 Skill 文案同步及 candidate hygiene 只刷新受影响的 source/projection/drift 验证，不重复无变化的 native 行为 run。

独立完整 committed review `a080da3...b0a02dd` 返回 `implementation_required`：P2 BR453-DISCOVERY-PROJECTION。修复只对真实 CLI test helper 的中间成功 stdout 验证/投影 result，formal invoke 与非零 error 保持原输出；workflow/standalone record→check→invoke 的相同既有用例验证修复。该 finding 在 `225fe80` 闭合，原 installed integration 再次通过；closure 不代替 fresh final full-range review。

fresh final 完整 committed review `a080da3...225fe80` 返回 `implementation_required`：P2 BR453-WORDING-SKILL-PROJECTION。原 Skill 仍写 checker_response.validation_receipt，与真实 receipt 和已更新详细合同冲突；真实 checker stdout 按该表达式会触发 KeyError。修复只更新原 Skill 的 recorder/checker receipt 校验与 result 投影指令，经原完整 preset 同步五个安装/平台副本，不修改 runtime、owner schema、正式 DTO 或业务条件。Wording 既有 28 tests 通过；dogfood reapply/installed/drift 通过，五个 managed backup 的原 HEAD 字节已保留，最终零 sidecar/conflict。

修复后通过原 native replay runner 实际运行 Codex 0.160.1 两条接续，使用原合法生成且业务 scope bytes 未变化的 owner/checker seed，完整 preset 更新到当前候选。checker-only 正向 run 在 invoke 前明确 formal_exit=false，原 invoke 实际返回 pass/planning_artifacts，消费 guru-contract-wording-pass-router 并读取 Planning owner entry；record+check blocked run 区分 checker 校验通过与语义 blocked，原 invoke 实际返回 blocked 并消费 contract-wording-blocked。两条真实 transcript 的声明、命令和 stdout 已审阅，无重复确认、重执行已完成动作或提前执行 downstream；证据只证明这两个本机正常路径。修复提交后的 finding closure、fresh final 完整 review 和 Architecture/RDT promotion 尚待完成。

## Finding closure 与晋升前状态

BR453-WORDING-SKILL-PROJECTION 在 `49c3e11ae9ce26fa391c038b6ba351adac25ff04` 完成 finding-owner closure；introduced 为 `225fe80afbee5f43f1ceeb2076cc795ece514c68`。closure 核验 committed 指令及五份副本、两组真实 recorder/checker stdout 的校验与 unchanged result 投影、native fixture/current bytes 一致，以及 positive/blocked 正式 invoke 与唯一 consumer。closure 仅关闭此 finding，不替代完整独立审查或晋升后 gates。

完整 fresh final review `origin/main@a080da319147fc9ccd6f85b10df60f3ce2e07e36...49c3e11ae9ce26fa391c038b6ba351adac25ff04` 已完成独立 Architecture 与 Branch 原 recorder/checker/invoke，实际公共出口分别 baseline_current/reviewed_candidate 与 passed，541 paths，无开放 P0–P3 finding。source/installed、receipt3、Wording28、adapters28/40subtests、Rebind3、drift、compile/context/diff 由该完整审查实际执行；历史失败按逐测试首次诊断对照，未计 pass。上述 native/安装仍绑定原执行对象，不因文档晋升而声称重跑。

Architecture/RDT 按 expected `current-main-0.6.17-guru.81` 串行晋升 `.82/active`，source/preimage 与历史结果保持。当前知识晋升 diff 的 fresh Phase2、TaskCommit、独立完整 Branch Review 仍待完成；原晋升前 pass 不支持 Delivery。软件发布、完整官方 update、其他版本/native host/model、完整 Release 矩阵与业务生产升级未验证。
