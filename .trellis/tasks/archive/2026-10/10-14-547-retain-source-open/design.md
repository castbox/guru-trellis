# #547 设计：source identity 与本次 Closure 处置分离

## Authority 与方案

需求入口为本 Task [prd.md](prd.md) 的 R547-01..08。当前 Architecture 为 `current-main-0.6.17-guru.87`，constitution 为 `guru-trellis-design-constitution-v1`，change contract 为 `guru-trellis-architecture-change-contract-v1`。独立 candidate_assessment 选择 `architecture_impact / target_native`，决策 refs 为 ADR-013、ADR-024。

采用现有动作枚举的直接演进：新增 `retain_open`，修改 Closure 执行和 Finish 校验；不建立替代事务、scope ledger 或兼容 parser。Task identity、source、generation 与 Completion 的 whole-current-scope 判断保持原职责。软件实现的根因修复证据来自原错误准入与新路径的对照；受控 provider 不能证明原 CMS 业务恢复。

## 唯一 source-design 处置矩阵

以下为本 Task 对来源设计的唯一处置矩阵；PRD 和 implement 只引用此表。Issue #547 是 requirement authority，其目标要求分离来源关系、完成判断与关闭处置。

| 来源 commitment | 处置 | 当前落点与理由 | 影响与上游处理 |
| --- | --- | --- | --- |
| ADR-013 Decision：Completion、Closure、Finish、Cleanup、Reactivate 五个 owner；Delivery 不代表 Completion | retain | D547-01/02/03 保留原 owner、ResultRef 与收尾顺序 | 无新增 owner；Architecture final_plan 审查本贡献 |
| #436 design D436-01：完整 scope 语义判断；fresh completed ResultRef | retain | D547-01 不改变七个 Completion outcome；当前 scope不足仍回原 owner | 测试正常 scope 修订及未完成 work/evidence；不伪造 Delivery |
| #436 design D436-02：source disposition 与 mutation 分离；closed/no_mutation 均有真实 ref | change | D547-02 显式表达具有资格但本次保留 OPEN；修复 exact_source 被强制 close 的执行条件 | additive enum；更新所有当前受控 Closure/Finish consumer；ADR 增量候选 |
| #436 design D436-03/04：Finish 三阶段、exact allowlist、Cleanup 独立 | retain | D547-03 只改 Closure 结果的状态有效性；现有归档/bookkeeping/merge 与 Cleanup 不改 owner | archive 保留 scope/历史/未验证边界；不把本地 move 当 success |
| #436 design D436-07/08：最小 public I/O、私有 recovery、generation 与 rearchive | retain | D547-02/03 使用原 ResultRef/TransactionRef、共享 reader 和原 transaction | 不增加 public output、审查历史或授权字段 |
| ADR-024：公共 Task2/API1/Plan2 属上游，Guru 原 owner 薄投影 | retain | D547-04 以 exact source 动作决定公共 Closure source fact；no_mutation 的 source_result 为 null | 不修改公共 Task 模型；匹配已有 upstream close_task 合同 |
| ADR-024 与 task-delivery-migration“安装支持与两步交付”：完整旧安装固定原包，新候选成套采用 | retain | D547-05 受控新装验证；实际 app 旧模型和原业务采用单列 | 不把 canonical 新 writer 应用到本工程 Task；真实升级仍由原 Upgrade owner |
| #547 范围/AC5：stale/mismatch 回原 owner；blocked 不能被强制关闭条件覆盖 | retain | D547-02 identity/uniqueness 后先返回 semantic blocked，再检查可执行 eligibility | 不跳过身份校验；blocked 不执行 provider mutation、不创建事务 |

## D547-01：Completion 与 scope

正常 scope 修订由现有 Clarify/Author 或公共 Task scope owner 完成。保留 TaskId、generation、exact_source；当前 accepted scope 是 Completion 判断对象。必要工作、未分配责任或必要证据未满足时保持原七 outcome 路由，不能靠源 OPEN/Delivery 全部合入推出 completed。Closure 只消费该 generation 的 fresh completed；Task2 继续核验公共 Completion 的 accepted_scope 与当前 record 一致。

## D547-02：Closure 动作与恢复

| disposition | 资格/条件 | executor 与终态 |
| --- | --- | --- |
| close | exact_source 审查已完成源 Issue 的全部关闭责任；执行前观察 OPEN 或同事务已完成 CLOSED | 原确认边界后执行 close，重读 CLOSED；原恢复不重复 close |
| already_closed_at_review | exact_source；观察 CLOSED | 不发 close；需要 CLOSED |
| retain_open | exact_source；当前 Task 已完成，源 Issue 仍承接 Task scope 外的明确责任；观察 OPEN | 不发 close；需要 OPEN；纯 retain 集合返回 no_mutation |
| no_close_authority | reference_only 的无资格来源关系 | 保留既有不要求 CLOSED 的行为；no_issue 使用空 action set |

semantic owner 读取 current scope、源 Issue 当前正文/状态和剩余责任，选择处置；脚本不根据 OPEN、exact_source 或 scope 摘要代替此判断。exact_source 禁用 no_close_authority，reference_only 禁用 close/already_closed_at_review/retain_open。源 action 唯一，已支持的 exact_source 多 Issue 集合保留，每个 action 的实际资格由 Closure 语义 owner 审查。

校验顺序：schema、Task/generation/current source、Completion/binding/evidence identity、来源 action 存在及 action identity 唯一；随后 semantic blocked 原因直接返回；成功执行路径再验证 source/action eligibility 和 reviewed_action_set 一致。blocked 不受可执行关闭资格条件覆盖。

原 private frozen transaction 加入枚举值，自有动作直接消费；不新增 persistence。retain_open 重读 OPEN，状态缺失回 resume_closure，CLOSED 回 external_change_conflict；close/already_closed 继续要求 CLOSED，正常 reopen 回 conflict。原 output-loss 恢复复用 frozen/ref/verified 并重读所需状态，不重复 close。冲突后的新处置由原 owner 审查并通过原 external_change_conflict re-entry 接续。

transaction terminal 仅根据 `close` 或 `already_closed_at_review` 动作存在决定 closed；否则 no_mutation。多 Issue 集合中，关闭另一 Issue 时 aggregate terminal=closed，但 Task2 public `source_closed` 仅由 exact source 的 close/already_closed 动作决定；源 retain_open 时公共 disposition=no_mutation、source_result=null、evidence 引用当前 accepted_scope。共享 reader 原样返回完整动作集，不能把 aggregate terminal 当源 CLOSED。

## D547-03：Finish 有效性与收尾

Finish snapshot schema接受 retain_open，并按真实关闭动作检查 aggregate terminal。共享 read_terminal_closure_result 仍是唯一 terminal读取路径。Finish逐个动作重读：retain_open 要求 OPEN；close/already_closed_at_review要求 CLOSED；no_close_authority保留原不核验关闭的行为。源 relation漂移或所需状态改变返回 closure_refresh_required，不擅自 reopen/close 或沿用旧决定。

有效结果继续现有 archive projection、bookkeeping publication、expected-head merge 三阶段。丢失 stdout 后原 Finish事务恢复，不重复归档、提交、PR或merge。archive保留规划、真实当前scope与delivery历史、原业务联调/验收未验证界限。success必须以远端目标含唯一archive且无active副本为证据。Cleanup仍由独立 owner审查具体资源；调用方拥有本 app checkout/branch时不得冒充已删除。

## D547-04/05：API 与安装边界

公共增量只有 Closure action disposition 和 Finish snapshot disposition 的 `retain_open`，同步 semantic reviewed_action_set/schema、package contract/interface/examples和迁移说明；保持既有字段、exit和refs的语义。旧输入仍按原动作执行；旧 consumer不支持新枚举，不能向其发送 retain_open。生产使用必须匹配更新 Closure producer、Finish consumer及当前 installer/platform投影后再采用新值。既有事务无新枚举时仍由同 owner恢复；新枚举事务不交给旧消费者。

当前 schema2 canonical使用公共 TaskKey/close_task/archive及正常 accepted_scope owner；完整旧安装仍使用它自己的整套 Task模型。定向验证在受控 checkout中安装匹配候选，不全量reapply到当前工程Task，不保留活动 dual-read/writer。旧发行包真实升级/原 CMS迁移及恢复由原 owner另行处理；本设计不新增永久 legacy adapter 或宣布该边界已退出。

## Architecture 与文档承接

Task-owned [architecture-contribution.md](architecture-contribution.md) 和 [architecture-adr.md](architecture-adr.md) 拥有九 concern、before/after、owner与ADR增量候选；它们不是 shared CURRENT。RDT delta和 reconciliation由 implement 的唯一 Docs SSOT Plan指定。Architecture promotion需首轮独立 committed full-diff review后执行；promotion新增diff重跑fresh Phase2/commit/independent review。验证方法与工作顺序由 implement拥有。
