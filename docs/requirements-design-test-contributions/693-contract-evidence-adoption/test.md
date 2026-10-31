# #693：合同、历史证据与实际验证

本页拥有本批实际观察及其截止点。完整策略见 [proposed Test 单元](proposed/docs/test/current/knowledge-maintenance.md)，关系见 [traceability](traceability.md)。它不记录其他 owner 的审核过程，不复制原始敏感记录，也不预填自身未来最终 Check/Review 或交付结果。

## V693-01：只读历史分析

固定业务源码为 `castbox/ai-chat-roleplay-backend@eaaf5b3cab3d3202f67956294d11aa6eed46087e`。下列路径均在该 Git tree；源码观察是静态证据，本批没有执行业务测试或复现。

| 观察与来源 | 能证明什么 / 不能证明什么 |
| --- | --- |
| 当时安装的 `.trellis/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage` 已要求未改消费者、原覆盖加真实差额、工程/语义/Git 事实区分。`quality-guidelines.md#test-and-validation-value` 已要求实际执行声明测试层。 | 此次不能归因为完全没有这些规则。规则存在不证明 Agent 当时执行了检查，也不能区分具体执行遗漏与审核能力不足。 |
| `app/ai_chat_roleplay/biz/story_chat/generation_execution_candidates.go:262` 的 `applyGenerationCandidates` 保存 options，更新 succeeded、OptionCount 和完成时间；该更新未承接 ordinary 完成快照 ReadyTexts。`auto_inspire_read.go:14` 的 `readOrdinaryCandidatePair` 对 action 要求有效 ReadyTexts，并逐项比较 option text。后者在该提交无 diff。 | 生产者自己的成功状态没有满足实际读者的原持久前提。Author/Architecture 应追踪原成功合同；Check/Branch Review 应独立核消费者可用。这里证明具体合同失配，不证明历史 reviewer 如何推理。 |
| `generation_preparation.go:412` 的 `captureGenerationRuntimeState` 只有 requiresLegacy 且 IndependentState 时才调用 `independent_state.go:108` 的 `captureIndependentState`。后者 Regenerate 分支把非空 AIMessageID 作为既存消息读取。新准备调用见 `story_chat.go:1761`，传入 actionPlan.AIMessageID；该新输出记录随后才创建。 | 新编排与旧参数对象的存在阶段不匹配；其触发需要上述实际条件，不能推广到纯 structured 路径。`independent_state.go` 本次有其他 fence/history 改动，只是所述既存消息读取分支未改；不能称整个文件无 diff。 |
| `generation_execution_mongo_test.go:525` 的 `TestGenerationExecutionMongoCandidateApplyAndOutboxAreAtomic` 构造 GENERATE_SMART_REPLIES action、调用真实 apply，并观察映射、adoption 和 finalize/outbox。它没有 ordinary 完成快照的 setup 与真实 ordinary reader 观察。 | 它是其声明边界的有效局部证据，不能证明 ordinary 读取链已可用。真实 Mongo 不扩张其分支覆盖。不能由此笼统判定整个原测试无效。 |
| `docs/requirements-design-test-contributions/813-chat-generation-integration/implementation-coverage.md` E30 及“取消独立业务准入的本地证据”明确说明 integration `-run '^$'` 是 `[no tests to run]`，仅编译；未重跑 Mongo/race，E1–E29 保留各自范围。 | E30 的命令不证明本轮集成执行；原记录并没有声称它重跑全部用例。晚期新 Chat 资格/Feature 使用变化扩大可达范围，必须与底层合同失配的引入分开归因。不能预设最终 reviewer 把全部旧事实当作充分证据。 |

原公开 Task 为 `.trellis/tasks/10-28-813-chat-generation-integration/task.json`，Delivery 为 `bad0094d-e0f1-452a-a237-8dfcc1b26d75`。该固定 tree 保存 Planning accepted，plan_ref 指向同 Delivery design、revision `sha256:acbfa18d543fbefa6159d188ad6a6934862f1801d7fbf0e4fff26a7454460da3`；Check passed 的候选 B 为 `3a2042f9bda166b1db11403eada7796596a6722a`、H 为 `cce9bc4bc1ccece8d1666b288ad393d7c31d3751`。该结果证明其绑定对象和阶段结论，不含具体漏检理由。

[PR #953](https://github.com/castbox/ai-chat-roleplay-backend/pull/953) 已合入 dev，公开 HEAD 为 `c4ab506218fa4227f6b0d96d33b6bfe2e1589ba5`，merge 为 `1f920f0e47685810c915a89681af8b575e508f20`。正文保留 E30 仅编译、未重跑 Mongo/race及未部署/环境联验的边界。因此不能把上述较早 Check 的候选直接当作最终 PR 全覆盖。GitHub reviews 为空不能证明没有独立 AI Review；固定 Task snapshot 中空的后续槽位也不能证明从未审核。原 Architecture、最终 Branch Review 和交付判断的具体放行依据、实际采用的旧事实范围未完整恢复，保持未知；不跨读退休 private checkpoint。

有证据的结论是具体生产者/消费者和参数生命周期合同没有承接，以及所列局部测试和 E30 不能单独证明这些正式路径。当前记录不支持把原因进一步确定为规则冲突、某个 reviewer 从未执行、统一能力不足或错误采纳全部旧结果。本项补具体方法与使用指导，不宣称已证明这些改动根治历史漏检或业务事故。

业务处置仍由 [#955](https://github.com/castbox/ai-chat-roleplay-backend/issues/955)、[#961](https://github.com/castbox/ai-chat-roleplay-backend/issues/961) 的原 owner 负责。已读 #955 关闭评论只证明其所述合入事实，并保留 provider/部署/联合验证未知；#961 的 helper overlay 只证明该 helper 的输入行为，不证明正式编排或真实环境。本批不重跑、不重开、不写业务实现、测试、数据或环境。

## V693-02..06：当前实施与剩余验证

截至首次 canonical 实施：两个共享方法和五个原消费合同已写入；三层完整 proposed targets 与 Architecture proposed change-contract 均保持隔离，shared current 尚未晋升。源文件变更只证明正文存在。

后续原 Check/独立 Review 应核对实际合同追踪、参数前提、fixture 边界和旧证据适用性；source/installed、完整 apply/drift、sidecar、语法与上下文检查分别报告。candidate Check 后原 owners 才 final_integration/readback，actual after 重新绑定并完成最终 Check/committed Review。实际结果在本页追加其观察范围；晚到最终结果从原公共结果和 Git/PR 读取。

后端正式采用 AC693-05 尚未执行，业务效果、部署/QA及完整多平台矩阵未验证。D1 和整体 Task 完成条件分别保留。没有新增业务回归、专项 replay/A-B/native eval、固定案例数或额外安装。

### 当前工程与同 checkout 分发观察

- source `check-skill-packages.sh --root . --mode source --json` 返回 passed；40 个 active packages、125 个 commands 的完整来源结构通过。这不是139项单元测试已执行的声明，输出中的 package_test_count 是受管测试资产计数。
- 现行 in-memory compile 检查363个 Guru Python 文件通过；marketplace JSON、逐文件 Bash syntax、Task context validate及 `git diff --check` 通过。上下文校验对两个大 spec 提示注入截断；Agent 实际读取命中完整条款及必要条件，不能把注入视为完整读取。
- 普通完整 apply 在写入前返回 `upstream_delivery_migration_required`，阻塞对象是既有历史归档。未迁移或改写这些档案。按原 tools-only owner 在同一 checkout 同步相同受审 Guru 投影，没有扩大为全安装/Task转换。
- 原 `guru-upgrade-tools` 使用本机已有、核对实际字节的 `.6` CLI/Core `local_candidate`。最先预览的 Fork 主 checkout 虽同版本，但会额外更新两个 upstream 目标，因此未执行。最终冻结计划的212个 public tools目标没有字节变化，显式保留用户 config和AGENTS正文。首次 prepare 因把公共平台id `claude-code` 用于installer flag而拒绝；改用明确的 claude/codex/cursor后冻结并执行成功。该入参修正没有写目标或改变本批机制。
- 原工具执行返回 `tools_upgraded / 0.7.0-guru.7`，`unverified=[formal_fork_source_lock]`。原 writer 负责保留Task/Delivery/session/archive及peer/common pointers；本批实际Git差额没有upstream工具或业务文件变更。此结果是本地候选工具证据，不是正式source-lock、发布或后端采用证明。
- 目标 runtime resolver 实际调用本 checkout的原生 `get_context.py --json`，exit0。installed package校验返回 passed、selected_platforms为claude/codex/cursor、conflict_count和sidecar_count均为0。原dogfood drift检查通过，Shared及三个声明平台的合同、workflow和spec与canonical一致。受管surface递归扫描无.new/.bak。

以上命令证明各自客观层，不能代替原Architecture/Check/Branch Review的当前语义判断。当前接续是完整候选检查；共享当前正文实际整合与最终质量结果仍由其原owners产生，不把本页的较早截止点改写为未来结果。
