# 当前流程合同连续性：D1 实施与验证

## 1. 输入与引用

读取 Task accepted_scope、当前 D1 PRD 全文及 design 第3节唯一来源设计处置。实际加载原 Author planning-body 与三模板、三个受影响 package 当前合同、Architecture constitution/change-contract、RDT current task-delivery-lifecycle 和其必要关系。固定 B 和完整候选由 design 第1节拥有。没有前序交付输入。

## 2. 有依赖顺序的步骤与文件责任

S1：原实现 owner 在 live checkout boundary 通过后修 Bootstrap Interface、投影、contract 与正式组合测试，保留同 owner 的 caller context。

S2：在 Branch Review 原例子删除过期字段；增加从 Interface example 填真实 archive 的 recorder/checker/invoke 回归。

S3：Architecture 原 runtime 校验 fixed-B absent_locators，active input/output/owner/consumer schemas 同步；保持旧合法省略及严格普通 missing/mismatch。补首次建立与原有 authority 两类完整链。

S4：原 whole-task/Delivery Bootstrap schema/contract 对齐 phase2 maintenance，补 final producer→Bootstrap→同 promotion 和 repair 对照。没有新 stage 或路由状态。

S5：canonical 全图组合回归覆盖 profile/aggregate examples 和 output→projection→consumer。已有旧 test fixture 若阻塞受影响验证，只修已确认的当前字段/版本，不把 fixture drift 当新业务缺陷。

S6：原 RDT/Architecture owners 形成真实隔离完整 proposed targets、trace 与 ADR，candidate Check 前不写共享 current。原实现完整 candidate/begin_check 后，独立 Architecture 及完整 candidate Check；随后两原 maintenance owners final_integration 写入/读回，重新 candidate/begin_check，最终 Architecture/Check。

S7：canonical apply 同步 dogfood/完整安装包/平台，执行定向 reapply/drift 和一个 clean 安装及 native 样本。所有产品改动仅本 worktree；不改上游或无关资源。

S8：原 TaskCommit→独立完整 committed Architecture/Branch Review→Delivery Review/Refs-only PR→Publish/Merge→whole Task Completion→Closure→Finish bookkeeping→原 Cleanup，分别核真实结果。

## 3. 验证入口、输入与预期观察

- T1/T2：Bootstrap 与 Branch Review package 定向 pytest，以 matching Fork、受管 Python 和真实隔离 Git/public API 运行。覆盖 design §8 的 repair 和正式 archive example，可观察原 consumer 正常结果及只读边界。
- T3/T4：Architecture tests/test_contract.py、test_promotion.py 及 affected TaskCommit fixture；同一对象的 B/H 与阶段保持，whole-task/Delivery maintenance 和 repair 均闭合。另由真实 AI owner 执行 V7 完整样本，受控输入不算原生审核。
- T5：全图 public contracts 组合测试与 source package checker，独立/profile aggregate 均校验；实际 current 数量从 registry 读，不写固定数量断言。
- T6：现有 apply.sh --repo .、check-dogfood-overlay-drift.sh、source/installed checker、Python in-memory syntax、bash -n、git diff --check；一个 clean 代表安装及 reapply/mode/平台/sidecar。真实 owner 在同安装继续 repair，报告实际改动与 stdout。
- 所有命令先采用仍适用且可核查工程事实，受影响代码或环境改变才重跑命中项；缺依赖是未验证，不是通过。完整多平台 Release、业务旧安装及生产没有本批验收入口。

## 4. 停止条件与适用回退点

必要 source/API/runtime 缺失时停对应 consumer并由原 owner 恢复；真实 scope/authority 变化回 Clarify，机制变化回 Author/Architecture，实施遗漏留原 implementation。新候选先资格审查，不直接加代码、测试或 finding。每次写入前核当前 task checkout boundary。普通验证失败修同一 key，不移动 B 或换身份掩盖失败。无业务数据库或部署副作用，因此不新增数据/部署回滚协议；Git/GitHub 操作由原 owner 精确执行。

## 5. Delivery Policy（唯一）

选择 full：本 D1 覆盖整体 R1–R6/V1–V8。只有四项原 consumer/后继闭合、全图检查、真实 native 样本、分发验证及完整当前质量链满足后才独立可交付。没有预定剩余实现；未满足验收仍归本 Task，不能把未完成项标成外部 deferred。完整 Release 矩阵和业务采用从始至终不在整体范围。Delivery 合并后仍由 Completion 审整体、Closure 处理 source、Finish 归档。

## 6. Docs SSOT Plan（唯一）

选择 delta_first。canonical packages/workflow/reference/MIGRATION-663 承担精确公开接口；原 RDT owner 在 `docs/requirements-design-test-contributions/663-contract-continuity/` 准备完整 task-delivery-lifecycle R/D/T proposed bodies 与 trace，保留原单元所有有效条件；新增当前四类正常衔接及分层验收定义。直接 consumer 是候选 Check、final-integration promotion 和后续 current 读者。原 Architecture 任务贡献/ADR 和 change-contract 完整 proposed target 由其 owner 评估，candidate Check 后串行晋升；不以 Planning contribution 代替 current。

最终 Phase2 前两原 owners 对真实 targets reconciliation、写入并读回；更新必要关系/导航且不递增全局版本、不追加总 README Issue 摘要。Check/Review 检查实际 after 与全部产品/文档差额。细粒度 package 合同不复制为第二 schema，历史归档和固定旧版本不回写。
