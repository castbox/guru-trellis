# ADR-025：exact_source 资格与本次源 Issue 处置分离

状态：`accepted`；来源：[#547 已独立审查贡献](../contributions/547-retain-source-open.md)；expected `.87` 晋升至 `.88`。增补 ADR-013/024 的处置语义，其 owners、identity 与公共模型职责继续继承。

同 TaskId/generation 的正常 accepted_scope 修订可能完整完成当前 Task，而真实源 Issue 仍承接范围外责任。exact_source 表示来源关系和可审查关闭资格，不能决定本次必须 close，也不能为归档改写成 reference_only/no_issue。

Completion 独占 whole-current-scope 完成判断；Closure 独占关闭责任审查、冻结动作和 provider 执行。retain_open 要求 OPEN、零 close，纯 retain 集合产生原 no_mutation ResultRef；close/already_closed 保留原语义。aggregate closed 只说明集合有关闭动作，公共 source_closed 仅由 exact source 自身动作决定。Finish 消费原冻结 snapshot，retain 要求 OPEN、关闭动作要求 CLOSED；漂移返回 Closure，不自行 close/reopen。Cleanup 保持独立。

动作枚举与 Finish consumer/schema 成套直接演进；旧完整安装在匹配迁移前固定原包，不向旧 consumer 发送新枚举。复用原事务、reader、refs 与 typed exits，不建立第二 ledger、store、DTO、writer 或授权持久化。constitution 无例外，GAP 与软件四轴不变。

验证观察与外部未验证边界由贡献的唯一 Test locator拥有。晋升新 diff 必须 fresh Phase2、TaskCommit 与不同 reviewer 完整 BranchReview；本决定不证明软件发布、业务安装或源 Issue 保留责任已完成。
