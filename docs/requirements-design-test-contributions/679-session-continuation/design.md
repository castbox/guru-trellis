# #679 设计增量

完整拟写定义见 [design proposed target](proposed/docs/design/current/task-delivery-lifecycle.md)，目标为 `docs/design/current/task-delivery-lifecycle.md`，保持 RDT-DES-LIFECYCLE。proposed 相对引用按最终目标位置解释；来源设计处置仍唯一位于本 Delivery design 第3节。

原 workflow 的 created consumers、唯一 continuation 和 Planning entry 编排原 Identity/Ensure/Bind/Selection。五 Planning Skills 各自核接收事实；Architecture 保 baseline-first。adapter 只读本 context，真正无 context 才 explicit-task，不新增 writer 或恢复框架。

Author/Architecture 原 guard 细化首失败；Author 更早的 LifecycleContractError 保实际安装/API条件。保外层 code、原 DTO/exit/phase与所有拒绝条件，具体字段迁移由 MIGRATION-679 单写。Readiness 保 normalization，原 recipe/runner补 standalone，真实 recorder/checker 承接派生字段。

Human artifacts 由明确调用方传真实 key；Task-only 只展示精确根 PRD；归档用实际 ref/key。package-owned 测试执行真实文案 argv。当前 suite 暴露的旧fixture依赖、独立legacy出口和mutable Git cache/eval inventory断言，均只做本批必要的原测试适配，保留首次失败，不改产品 authority。

Architecture 当前 Planning candidate/final 均为 no-impact；实施实际候选仍需独立 Phase2 判断。RDT 先隔离完整 proposed，原 candidate Check 后 final_integration/readback，再重绑实际 after 进入最终 Check/committed Review；本贡献不是当前晋升或通过声明。
