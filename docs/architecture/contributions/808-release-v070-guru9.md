# #808 私有发布来源与采用：Architecture 贡献

Identity：`architecture-contribution-808-release-v070-guru9-v1`。状态为 proposed；本文件及完整拟写不构成共享 current、实现通过或发布结果。归属 Task `808-release-v070-guru9` / generation 0，D1 `b40421e8-6213-4f29-bb11-8d3919e533b0`。

## 来源、before 与完整目标

Direct Source 为 [#808](https://github.com/castbox/guru-trellis/issues/808) 的准备及完整后置发布责任，整体范围由 Task 根 PRD 承载。固定内容 B 为 `5c6a4591db7165ece045e6b0eb789c21d06d7d38`；本次选定整合来源为 `29d0c3795ac45f9fc03fbea46c331307cce10b2b`。两个完整 proposed targets 以该来源各自完整单元为基底，仅修订下列有效关系：

- `808-release-v070-guru9/proposed/docs/architecture/03-domains/ownership.md` → `docs/architecture/03-domains/ownership.md`：ARCH-DOM-010 保持私有编排与各原 lifecycle/tools owner，展开来源、采用及整体完成的不同责任。
- `808-release-v070-guru9/proposed/docs/architecture/04-integrations/distribution.md` → `docs/architecture/04-integrations/distribution.md`：ARCH-INT-015 采用 #794 当前逐 Delivery 链、D1 实际 delivered 后的 D2 及完整 Stage2；保留 #392 历史与旧 provider 恢复。

baseline 为 `guru-trellis-architecture`，constitution 为 `guru-trellis-design-constitution-v1`，change-contract 为 `guru-trellis-architecture-change-contract-v1`。现行依据是 GOV/change-contract/ownership 的有效定义与 MIGRATION-794；不以 proposed ADR 证明接受，也不改它的状态。共享 root、索引、全局版本及无关知识不变。

## 原 owner 与采用机制

选择唯一 target_native。私有 release 只编排已有 owners，不成为 task、安装或阶段结果 writer。原 Clarify/Author 分配并规划 D1 完整来源与 D2 实际采用；D1 必须先完成自身来源、真实 producer/consumer、安装和分发验证，之后经 TaskCommit、完整独立 Review/readiness、Publication/Merge 真实 delivered。未实施采用由原 Completion 使用 additional_delivery_required，原 Creation 后建 D2；tools 使用完整干净匹配来源执行 source_locked。D2 的安装 after 进入其自身完整质量链。

这直接复用已存在的 staged Delivery、公开结果与原工具 writer，不引入 early source 提交路线、计划性失败审核、并行 authority、授权状态、额外持久化或恢复框架。临时来源样本只证明其实际层次，旧安装/drift 观察不改写；没有 Stage2 candidate 前不能预填发布通过。

代价为来源与采用两个真实切片各自完整验证和审查。它解除 source_locked 需要已交付来源与来源提交前要求先采用之间的循环，并保留整体完整性。无需新增 ADR、GAP、public API、mode 或 guard。若来源锁定、切片完成条件、原 TaskCommit consumer 或 owner 发生真实变化，返回原 Clarify/Architecture 重评，不能靠此贡献自授新路径。

## 九 concerns 与项目检查

- authority-binding：root accepted scope、D1 anchors、#808、固定 B 与选定来源各自保留。
- constitution-binding：复用既有官方扩展与 owners，以完整来源/实际采用语义、单写职责、最小既有机制和旧重复路径退出承接五原则；不复制原则或打分。
- boundary-and-decision：只维护 ARCH-DOM-010/ARCH-INT-015 的有效关系；Stage2 完整责任不变。
- owner-and-single-writer：Author 写隔离提案；原 Architecture 独占 shared final_integration/readback；原 RDT 保三层知识；原公共 API 写阶段事实。
- compatibility-and-exit：不新开 early Draft 或独立 Check；旧合法在途操作按 matching provider 恢复，已发生事实不重放，pending 新动作先当前审核/readiness。
- gap-and-deviation：不新建 GAP 或例外；真实来源验证失败仍阻塞 D1，不转移给 D2。
- parallel-scope：只写本贡献及两个隔离 proposed targets；不改其他 Task、历史贡献、shared index 或未选本地目标。
- evidence-and-freshness：规划、工程、临时安装、实际 source_locked、独立审核和远端发布分别取证；digest 不代替语义判断。
- review-and-promotion：Planning 两目的仍独立；实施和工程后由原 Architecture 整合两个完整目标，结果仅 integrated_pending_review；TaskCommit 后同一新独立 reviewer 审真实 before/after，才可 reviewed_promoted。

项目检查沿既有 `guru-trellis-architecture-convergence:repository:1` / `guru-trellis-architecture-convergence@1` 的当前语义合同，核实际 owner、状态、采用关系和 unchanged consumers。本文不预填检查结果。原维护 owner 在 final integration 重读真实 shared targets 和全部必要关系，整合后逐文件 readback；真实并发变化不因文本可合并免审。

## 实施、验证与完成边界

版本直接消费者及 active output example 对齐 .9。local sample 使用 matching Fork 的公开 Guru custom workflow 初始化，再由原 sample copy/preset 验证当前本地来源；退出会生成 manual bootstrap 的 native 策略及本批无 consumer 的 native hash 例外。原 guard、bootstrap、未知漂移与安装/验证链保持，不新增 profile 或来源 authority。它们不改变公共 owner 或现行来源/采用关系。实际入口、断言、完整平台源映射和工程结果由 D1 design/implement 与原执行者承担；原失败保留，不新增自证文案测试。

R794/D794/T794 已定义当前质量和完整采用责任，RDT 原 owner 仍须核本批真实差额。两个 proposed targets 只在完整实施/工程事实齐全后，经原 Architecture delivery_promotion(final_integration) 合法整合，随真实 D1 candidate 提交并独立审核。最终准备 Task 完成、Closure no_mutation、Finish/archive、fresh 发布候选、tag/smoke/Release、两本地目标和 #808 关闭仍由各原 owners 后续实际建立；本贡献不记录其过程或结果。
