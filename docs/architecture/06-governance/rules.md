# GOVERNANCE

- `ARCH-GOV-001`：Architecture 变化按 `bootstrap_foundation`、`task_impact_sync`、`promotion` 或 `repair` 进入唯一 semantic owner。
- `ARCH-GOV-002`：CURRENT 条目必须有 current code/config/test/release evidence；`inferred`/`unverified` 不能晋升为 CURRENT。
- `ARCH-GOV-003`：每次 gate 读取 live authority，由原语义 owner 选择并重读明确阶段适用的 locator/version/status 与真实 task delta。无关整体 CURRENT/ref/version 前进不改变已选适用性；真实立即适用规则变化须明确对象和承接要求并回原 owner。unknown/multiple/真正 stale exit 继续 fail closed；ADR-028 定义本条的适用边界。
- `ARCH-GOV-004`：Architecture/RDT/projection 三者 locator 与 traceability 必须一致；projection 只能包含读取规则、identity 与 freshness。
- `ARCH-GOV-005`：普通并行 task 使用隔离 contribution，不共同写 shared current；这是 ownership 规则，不引入锁、TOCTOU 或共享协调状态。
- `ARCH-GOV-006`：每个标准 task mandatory 进入 Architecture semantic owner；`architecture_impact` 恰好选择 `target_native`、`legacy_boundary_convergence` 或 `dedicated_refactor_slice`，`no_architecture_impact` 只返回 current identity 与可审核理由。
- `ARCH-GOV-007`：Guru public identity 与项目 baseline/change-contract identity 只在 task-local Architecture change contract 相交。明确阶段适用的 concern、owner、GAP、before/after、project check、evidence、review 或 freshness 缺失、过期或冲突时 fail closed。digest/ref 只服务本地事实一致性；无关整体版本推进不代替适用性判断，也不使旧 pass 自动适用于真实新候选。
- `ARCH-GOV-008`：普通 Task 先写 task-owned contribution，原独立 Phase2 Architecture reviewer 比较晋升前 authority、完整 tracked/untracked candidate 及全部拟写内容。原 Architecture owner 随后按 live expected-current 在当前执行分支串行晋升，核对实际写入和结论适用性，再进入最终 Check、Task Commit、committed 独立 Architecture 及完整 Branch Review。新 CURRENT 自身是受审差额，不能自证实现正确。expected-current 错配由原 promotion owner 返回 `sync_required` 并判断实际差额，不使无关在途 Task 失去开发资格。部分写入只由原 owner 在相同唯一 intent 下恢复，冲突时停止。未晋升 contribution 不得进入最终 readiness/Ready 发布或 Finish；原 Publication 的早期 Draft 只是反馈，不写最终 PublicationFact，最终仍须在完整 Check 前完成本条晋升顺序。晋升不能代替后续质量门禁或 Task 完成。ADR-030 窄替代 ADR-005 的 committed-review-first 时机，保留 authority、single-writer、独立性和 finding lifecycle。
- `ARCH-GOV-009`：Delivery Review 判断当前 slice 与真实 PR readiness；Publish 拥有同 PR 的早期 Draft 创建/更新、未审修订 push 前退 Draft、最终 Ready及其事务恢复；早期反馈不证明最终 gate，Merge 核验 live eligibility、expected-head 和实际合并结果，并通过当前 Interface 的正式出口接续。每个 Delivery PR 只使用 `Refs`，合并不关闭整体 Task 或 source Issue。Completion 独立判断全部 accepted scope 和实际 Delivery/证据；Closure 随后独占 exact-source Issue disposition，可按当前合同冻结关闭或保留 open 的动作。Finish 核验冻结结果并归档/bookkeeping，Cleanup 独占资源删除。其他 owner 不补偿调用 Issue close API。no-Issue 不制造 Issue identity；reference-only、non-default-base 与 source 剩余责任必须按真实 authority 判断。退休 Publication/Finalizer/closing-keyword 自动关闭链只用于其 pinned 历史安装，不能作为当前 lifecycle。ADR-013/024/025 及各 current Interface 拥有具体接口。
- `ARCH-GOV-010`：active-task continuation先消费current adjacent DTO；output丢失时回最近合法原owner。任何status、Git shape、旧摘要、旧确认或retired checkpoint都不能重建semantic pass。确认仅存在于当前对话，新的副作用或authority变化必须重新展示。
- `ARCH-GOV-011`：一个 active Task 可以产生多个独立 Delivery。每个 Delivery 含 D1 都有选定的独立 Planning 与原质量门禁，沿公共 Task/Delivery identity、selection 和转换执行；任何文件存在或旧历史都不能生成当前 semantic pass。`delivered` 唯一交给 Completion，Task 在整体完成前保持 active，不得表达或触发 Issue closure、archive、Finish、Cleanup 或 Reactivate。旧 #435 additive/deferred graph 仅属历史切换阶段；当前只使用一套匹配的公共 graph，不提供 retired lifecycle adapter。
- `ARCH-GOV-012`：当前知识按完整能力单元读取和维护，保留稳定 ID、条件、例外、顺序与必要 R/D/T/Architecture 关系。导航只定位正文和状态，不拥有第二语义定义。原维护方把隔离贡献合入完整当前正文；历史 contribution 保留来源，普通查询无需重放已迁移对象的全链。未迁移对象仍明确指向原完整来源；缺来源、断链、冲突或不完整迁移回原 repair，不推断完整性。FOUNDATION 的[技术基线选择](../00-foundation/stack-selection.md)固定通用源/version 与项目差异，各自原 owner 在自身边界维护；源接受、项目选择和 CURRENT 实现证据是不同事实。

完整项目 change contract 与 project-check descriptor 见 [`change-contract.md`](./change-contract.md)。

## 来源与历史边界

`ARCH-GOV-003/007/008` 的阶段适用性来自 [ADR-028](../adr/028-fixed-content-baseline.md)，晋升时机来自 [ADR-030](../adr/030-promotion-before-final-check.md)。后者的实际验证及边界由 [#600 唯一 Test](../../requirements-design-test-contributions/600-promotion-before-check/test.md)拥有。正常顺序直接读上文，不先执行已被替代的旧顺序；不为补最终 Review pass 或最终 SHA 循环写正文。

旧 `.100` 完整 authority 可在 immutable Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c:docs/architecture/` 读取。历史 ADR、contribution 和证据保留其原对象；在途 Task 仍按阶段适用版本读取，不因本文件收敛而强制重写。知识正文更新不证明 Delivery、Completion、软件 Release 或业务采用。
