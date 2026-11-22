# #822 D1 实施与验证计划

## 1. 输入与引用

[Task PRD](../../prd.md) R1–R5 和 AC1–AC2、[Delivery PRD](prd.md) DS1、DS2、DAC1 和 DAC2、[设计](design.md) §3–§8。输入包括固定 main、当前 Guru 安装、可定位的前序交付和去敏五字段。验证只消费受支持的 public operations 和当前合同。#850 的已交付阶段顺序用于纠正旧测试。

## 2. 有依赖顺序的步骤与文件责任

1. 使用独立本地样本核对已交付实现、当前 scope 以及去敏配置。执行正常续接入口，保留实际读到的阶段和后续结论。
2. 在本 Task 工作区修复已发现的接续验证缺口。测试文件 `trellis/skills/guru-team/packages/guru-author-task-plan/tests/test_receiving_session.py` 按现行 final Architecture、Approval 与 Activation 链验证同一 Delivery；继续断言 key、规划字节以及 Task 记录行为。
3. 若样本出现实际导航或证据承接缺口，定位其原 owner 和最小源文件，按现有边界修复再复测。若仅有证据缺口，完成验证并把适用结果整合至现有 Test authority。不存在实际缺口的步骤直接采用其观察结果。
4. 工程验证满足后，由原维护 owner 读回相关文档和受影响投影，进入本地 TaskCommit 与独立 committed Review，再进入 Delivery Review 和发布。

## 3. 验证入口、输入与预期观察

执行设计 V1–V4。原定向测试使用匹配的 Trellis Fork scripts 及 Guru 受管 Python。命令为 `python -m unittest -v test_receiving_session.ReceivingSessionTests` 中两项关键行为及 `test_candidate_cli.CandidateCliTests.test_actual_prior_delivered_head_is_used_for_next_pull_request_slice`。设置当前仓库测试模块路径和经核对的 `GURU_UPSTREAM_DELIVERY_SCRIPTS`。Codex 隔离本地样本用于语义行为，不以固定数据校验替代。运行样本模型容量和配置加载检查，保留剩余外部验证边界。必要时用 source/installed discovery、drift 与 sidecar 检查对应变更。

## 4. 停止条件与适用回退点

当实际入口能识别剩余工作、保持同切片恢复、复用明确证据、只补变化影响并进入正确交付阶段，且实际变更通过定向验证，结束诊断。设施失败先核对是否进入被测步骤，再重试实际缺口。未得到关键行为证据保留对应验收缺口。若设计或 scope 实质变化，返回最早受影响 owner。只回退本 Task 工作区实际差额及本任务创建的临时样本。

## 5. Delivery Policy（唯一）

Strategy: full。覆盖整个 #822 的 AC1、AC2。完成条件为样本观察、已发现缺口的最小修复、适用定向检查，以及本 Delivery 的审核、合并与实际交付结果。保留原 Task Completion 对整体证据和源 Issue 结案的独立判断。

## 6. Docs SSOT Plan（唯一）

Strategy: delta_first。原 RDT owner 读取真实工程结果，整合并读回已影响的 `docs/test/current/task-delivery-lifecycle.md` 和相应现有 RDT leaf。当前已知差额为 T850-03 的同规划接续验证以及去敏样本的必要观察。下一位直接消费者是固定提交的独立 Branch Review。改到公开说明时原 tools owner 同步受管投影。Architecture candidate 评估为 no impact，在 final_plan 独立核对。
