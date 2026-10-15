# #569 固定截点查询 Architecture contribution

本文件为task-owned方案贡献，不证明实现、独立committed Review或promotion通过。Identity：architecture-contribution-569-fixed-cutoff-history-query-v1。TaskId 569-fixed-cutoff-history-query / generation0。当前路径target_native，沿原Merge history与Completion owners演进。

## Authority 与职责

baseline：docs/architecture/README.md / current-main-0.6.17-guru.92 / active。
constitution：docs/architecture/00-foundation/design-constitution.md / guru-trellis-design-constitution-v1 / current。
change contract：docs/architecture/06-governance/change-contract.md / guru-trellis-architecture-change-contract-v1；concern set guru-trellis-architecture-change-concerns-v1。
requirement/behavior authority：live #569、docs/requirements/README.md、docs/design/README.md（RDT .98）。

原Merge history owner单写有界准备与事实结果；原public Task parser只读事实；原Completion/standalone/recovery caller拥有cutoff适用性与补证判断。脚本不解释scope或决定Task完成。task-only contributions先由本Task写，shared-current只由原Architecture/RDT promotion owner在独立committed Review后写。

ADR-026保有query1/query2、公有归属与事实≠current gate；ADR-028保有固定对象、相关增量补证及#569数据准备边界。本项以result3.0与temporary context落实这些职责，不改变owner、原则或GAP lifecycle；当前不新增ADR候选。final_plan/真实diff独立owner仍重新判断必要性。

## Required concerns

| Concern | 适用 | 当前候选 |
| --- | --- | --- |
| authority-binding | applicable | Planning3.0 candidate/final目的分开；非Planning2.0保留，适用baseline .92。 |
| constitution-binding | applicable | 读取唯一current authority；变化隔离与最小必要复杂度要求原owner、最小cutoff、无缓存/ledger/新同步Skill。 |
| boundary-and-decision | applicable | repo/base/B1固定；metadata准备与业务只读分开；真实first-parent/PR归属保留。 |
| owner-and-single-writer | applicable | 原query产生事实，consumer判断适用性，public Task不写，promotion仍唯一writer。 |
| compatibility-and-exit | applicable | query1/2输入和归属保持；current输出3.0成套直接迁移，旧1/2仅历史validation asset，无runtime fallback/adapter。 |
| gap-and-deviation | applicable | 不关闭/重开无关GAP，不为正常历史准备引入其它scope；观察真实before/after，未验证不晋升current。 |
| parallel-scope | applicable | 本Task隔离路径、原owner canonical及受管投影；不写其它Task/业务/#566/shared-current或upstream。 |
| evidence-and-freshness | applicable | 真实cutoff/对象/PR、候选bytes与本阶段绑定；API返回与语义gate分开，actual public stdout/consumer分层验证。 |
| review-and-promotion | applicable | 先独立完整committed Review，再expected-current promotion；晋升差额fresh Check/commit/独立完整Review。 |

## Before / after 与项目检查

before：history入口要求local/remote base SHA相等；扫描local ref；result无显式cutoff；query2所有recorded merge必须在该扫描内。正常落后/缺对象或截点后新记录可能中断原consumer。

after implementation candidate：`history.discover` 经 repo-bound provider 只读一次真实 B1，`first_parent_history` 要求完整到真实 root 并拒绝可达 shallow 边界。`HistoryContext` 优先复用 caller 对象，必要时在调用内 bare context 按有限 immutable SHA 获取；切换 context 后同时准备已需目标，后续 merge/parents/head/candidate bytes 均读该实际 context。无 destination ref、FETCH_HEAD、tags 或 shared object/shallow 写入，临时 Git 数据和原 candidate snapshot 随调用结束清理。

query2 先核验既有 public fact 的候选、真实 PR、两父、head、repo/base 和合法 trailers，再按 B1 first-parent 关系融合；真实后继只有完整 first-parent 链包含 B1 才排除，其它归属不符仍具体失败。当前输出统一为 result3.0，仅新增直接 consumer 必需的 cutoff_commit。query1/2 输入及历史事实语义保持，旧 result schema/example 只用于历史验证，MIGRATION-569 明确受控 producer/consumer 成套切换；不存在 current 双读 adapter。

原 Completion/独立/恢复 AI 仍独占公开 repo/base/task/cutoff 的适用性判断。无关 B2 不触发查询；明确本 Task 新交付或所需证据变化才补缺少事实，丢失输出重入原 producer 并取得新操作明确截点。查询不记录 Task/Delivery，不决定 Completion、Closure 或 Finish。与原 manual recovery 共用候选公共 hash，仅增加内部 Git context 参数，未建立第二实现或 authority。

project descriptor：guru-trellis-architecture-convergence:repository:1 / guru-trellis-architecture-convergence@1，entrypoint为当前change-contract；规则ARCH-GOV-006..009，决定ADR-005/009及适用ADR-026/028，GAP引用ARCH-GAP-006/008只作既有协议引用，不改变状态。真实project check及blocking由每阶段Architecture owner本人判断；本贡献不是机械pass或第二descriptor权威。

Phase 2 的项目语义检查实际覆盖：九 concern 的适用性及 authority binding、target_native 唯一路径、原 query/public parser/consumer 职责、before/after 新增或恶化偏移、共享 promotion single-writer 与 parallel scope、ADR 必要性、现有 closed ARCH-GAP-006/008 未重现。新增临时 context 的职责是当前缺对象/浅克隆隔离，新增 cutoff 字段由当前 consumer 使用；删除这些职责会失去 #569 当前所需能力，未加入未来预留。当前未发现新增 owner、长期状态、无退出双写或原则例外；ADR-026/028 已承接决定，未产生新 ADR/GAP lifecycle。

实际代码/installed/public/外部验证结果仅由唯一 `docs/requirements-design-test-contributions/569-fixed-cutoff-history-query/test.md` 记录。独立 Phase 2 owner 在代码优先检查后才读取 live #569、Task design 与本贡献，并亲自读取代表性 installed 原始 delivered/history/Completion stdout、直接检查真实 first-parent/two-parent Git 及无内容 B2 差额。公开 B1 只有首条 Delivery；无关 B2 直接消费和同 Task 第二条 Delivery 的有界补证/丢失输出重入分别有实际结果。58 项最终回归、matching installed validator 与最终 projection/reapply/drift 证据已核对；provider/前序开发 gates 仍为 fixture，不构成真实远端、完整业务开发链或软件发布证明。

本次项目检查未发现阻塞的 Architecture conflict、fitness regression 或缺失 concern，贡献保持 reviewed candidate；shared Architecture .92/RDT .98 未改。该结论不替代原 Check、首次独立 committed Review、promotion 及其新差额 fresh gates；完整 Release 矩阵、远端 marketplace 与业务仓采用仍未验证。无长期 checkpoint、额外审计文件或授权信息。
