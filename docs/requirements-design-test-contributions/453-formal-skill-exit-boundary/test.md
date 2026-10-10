# #453 Test contribution

候选，未晋升。继承 Test `.81/active`。客观 transport 与真实 Agent 行为分开报告；下列是本次实际 candidate 的定向验证，不能代替后续 committed review。

- T453-01：current source registry/interface 的 36 packages/109 commands 分类与闭合 receipt schema；dispatcher 测试覆盖 owner、checker、typed-shaped atomic intermediate 和不变的正式正向/非通过输出。内部返回与旧 commands 1.0 历史 schema 不变。
- T453-02：各 package 的 current regression，实际 Wording record/check/invoke 正向、blocked 与 content_changed；Planning、Phase2、Branch Review、Reconcile、normal/root/solution qualification、Activate、session/identity/binding、task-free 和 deterministic Base Sync 定向回归。原 atomic/恢复能力由其原 owner 的测试及真实 wrapper 继续验证。
- T453-03：Intake semantic authoring、Phase2 authoring、Stage0 caller、实际 Wording stdin integration；测试 fixture 明确携带当前 shared schemas，不添加旧格式 fallback。trace 留真实外层 stdout。
- T453-04：一个 codex clean complete preset 和 HEAD `a080da3` 的完整 predecessor 安装再 apply/reapply；当前 dogfood 声明的 Claude/Codex/Cursor 投影与 reapply/drift/hash/mode/sidecar 检查。每个应用备份与实际 preimage 一致并另存后退休。完整官方 marketplace init/update、多平台 Release matrix、其它旧版本及业务生产升级未验证。
- T453-05：本机 native `codex-cli 0.160.1` 两次真实业务规划接续。checker-only 已持有真实 owner result；record+check 使用真实两条 stdout，均由当前 AI 完整审查三份规划与源后经原 recorder/checker 生成。正向场景为明确 30 天订单保留，非通过场景为产品未定期限。AI 审查完整 command/action/message transcript：两者在 invoke 前都明确尚无正式出口；无重复确认、重做已完成动作或提前执行 downstream；真实 invoke 分别为 `pass/planning_artifacts` 与 `blocked`。正向组消费 workflow router 并读取下一 owner entry，阻塞组消费 `contract-wording-blocked` stop。native harness 只 replay 和保存 transcript，不 author/grade gate。

本地证据由 Phase2 owner 消费：`/tmp/guru453-native-positive-transcript.jsonl`、`/tmp/guru453-native-blocked-transcript.jsonl` 及对应 fixture 中实际 invoke stdout；临时日志不进入公共 package。两次 run 证明本机这两个正常路径，不声称所有模型/业务仓都消除了误报。

当前全范围回归曾检出旧 caller/schema fixture，已迁移后重跑受影响集合。前置 HEAD 可复现的生命周期 fixture 缺口与本次变更分别比对；历史失败不计 pass、不扩张本任务修复。实际最终结果：source 与 clean/migration installed validator 均通过（36 packages/109 commands）；Solution 24、adapter 27、Rebind 实际 wrapper 3、Wording stdin integration 1 个测试通过。Runtime 原 4 个失败修正当前 count/schema fixture 后定向重跑通过，未重复无变化的全套。Cleanup/Closure/Finish/Reactivate/Completion pytest 合计 149 passed、14 Closure failures；相同 14 项在前置 HEAD 复现。Create Task Commit、Merge、Publish 的当前失败已按具体 test/首次诊断与前置 HEAD 对照，均为既有 fixture 失败，不计通过。Discovery 的 binding error locator assertion 在前置 HEAD 同样失败；其实际 CLI integration 另有本次遗漏 result projection 导致的新 KeyError，已由独立 Branch Review 记录 BR453-DISCOVERY-PROJECTION，并在 finding-fix 中迁移，二者不能合并归因。代表安装实际 Wording 正向与 blocked invoke 都通过。最后等价 Skill 文案同步及 candidate hygiene 只刷新受影响的 source/projection/drift 验证，不重复无变化的 native 行为 run。

独立完整 committed review `a080da3...b0a02dd` 返回 `implementation_required`：P2 BR453-DISCOVERY-PROJECTION。修复只对真实 CLI test helper 的中间成功 stdout 验证/投影 result，formal invoke 与非零 error 保持原输出；workflow/standalone record→check→invoke 的相同既有用例验证修复。finding closure 与 fresh final full-range review 尚待修复提交后执行，原 pass 不代替新 gates。
