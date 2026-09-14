# #408 Design 增量

状态：`draft`，不替代 shared `.50`。本任务设计细节见 [task design](../../../.trellis/tasks/09-14-408-nightly-session-binding-manual-fallback/design.md)；这里只定义可提升的 responsibility/contract 增量。

| Identity | Owner / contract | 不变边界 |
| --- | --- | --- |
| D408-01 | `trellis-source.json` 与现有 source validator 绑定 target commit、ci_run_id、实际 build/CLI；CI 记录不替代本地构建 | 无全局npm、无可变ref、无授权digest |
| D408-02 | 固定 Fork 正式生成并安装 session/runtime/hook，preset只复制Guru source record与owned assets | 不手改上游resolver，不扩大ownership inventory |
| D408-03 | canonical workflow拥有自动停止与独立手动请求的全局边界；既有Skill/平台入口只引用该owner | 不修改Skill图或Finalizer事务，不制造恢复产物 |
| D408-04 | preparation/session/package/finish-family/focused installed分别验证来源、行为与分发 | 不以mock或文本断言充当实际installed/远端执行证明 |
| D408-05 | Agent入口给出真实installed package位置；Clarification/Readiness recorder落实既有派生职责；正常authoring真实stdout接续到创建、双端mapping、boundary与受控激活 | 语义判断仍归AI；不改workspace writer或公开图，不引入补mapping恢复路径 |

source pin 直接演进；predecessor测试继续使用其历史source合同。shared-current更新由RDT/Architecture各自promotion owner单写，独立review之前不提升candidate。

D408-05 是原 R408-03/04 的覆盖补漏，不是新的产品功能。现有wrapper链带预先构造的私有数据能通过，不能证明正常Agent authoring可执行；当前实现以既有recorder计算/检查自身派生值，测试不再用调用方重建private plan替代该职责。
