# #822 五字段启用接续的验证记录

观察基线为 `ffbc25e32e65fa843c0ff0d75a9f16f0e0f0ea8f`。对应 [#822](https://github.com/castbox/guru-trellis/issues/822) AC1、AC2 和 [生命周期测试策略 T822](../../test/current/task-delivery-lifecycle.md#t822-同一任务内的小范围启用)。

## Codex 入口观察

以固定 main 的完整安装投影创建隔离样本。前序计费实现为实际本地 Git 提交，样本通过已安装 Delivery API 保存前序交付。样本 GitHub 回读使用受控替身。

Codex 从 `trellis-continue` 读到 Task 实际绑定和 `no_current_delivery`。它确认前序已交付，读取可定位的规划、验证记录和当前配置，只选择尚未分配的五字段启用条件。它核对前序实现、writer 和索引依赖均未变化，采用资金精度和索引证据。目标模型预算和配置加载仍需检查。

首次创建写入了后续切片，但 Codex 的隔离运行返回 `blocked/delivery_projection_failed`。同一运行中的恢复仍返回该错误。宿主使用同一个 `continuation_id` 经原 `recover_creation` 成功选回已创建的切片，保留同一 DeliveryKey。随后 Codex 回读 `current/planning`，只写后续切片的增量需求。一次 Author 调用遇到旧输出形状缺少 DeliveryKey 的校验错误。Codex 改用当前 schema 后获 `requirements_ready` 并用原合同查询定位 Architecture `candidate_assessment`。

第二次 Codex 会话接到同一切片的实际 `approved` 结果。它复用已审规划和前序证据，激活原切片，只改目标配置文件。它验证了五字段和模型预算，再调用原 TaskCommit，收到 `pre_review_committed`。本地读回提交为 `701f84205ffde248dcf8af0343d061a13e4ccaaf`。从前序已交付提交到本次提交，样本业务文件的变化只有目标配置。观察范围止于样本本地交付，后续审核、合并和部署需要各自的证据。

首次选择失败发生在隔离运行环境中，具体原因未证实。历史 Issue 的耗时和根因仍未知。

## 定向工程验证

- 样本从其依赖声明指定的配置路径重新加载 JSON。实际变化为价格版本、上下文容量、预留量、预算版本和计数方式五项。既有模型身份保留。目标上下文容量与预留量均满足样本声明的上限。
- 当前 Author 接续测试验证新接收会话恢复已存在的选择，并验证已有规划进入 final Architecture、Approval 和 Activation。两个测试都保留原切片身份和规划内容。基线的旧验证测试调用已由 #850 移除的 Wording helper，未能进入 Approval。更新后两项定向测试通过。
- 另一个原有公开 Candidate 测试确认后续切片采用实际前序交付提交，只纳入本次差额。该测试在匹配的 Trellis Fork 脚本与 Guru 受管 Python 下通过。

样本配置检查只覆盖本地去敏配置与预算声明。真实账单、实际 Test 或生产配置采用、远端流水线效果及完整升级发布矩阵不属于样本验证。
