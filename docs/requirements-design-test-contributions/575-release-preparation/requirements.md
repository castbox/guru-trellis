# #575 S2/S3：来源准备与来源校验修复需求

本贡献以 RDT `.100` 为前驱，继承 Architecture `.93/active`；[S1](../575-source-adoption/requirements.md)保留正式来源采用与历史公开映射。依据为 #575 Stage 1、Task 整体 R575-01..07 及当前同 Delivery 的来源准备规划。软件发布目标与知识版本独立；实际结果仅由 test.md 拥有。

| Requirement / Behavior | 必须满足的行为 | Design / Test |
| --- | --- | --- |
| R575-S2-01 / BEH575-S2-01 | canonical extension、原 maintenance target、生产结果、schema/example/stop consumers 同步 `.4`；保留合法旧族、predecessor 和原 source 检查，正常 preset resume 使用 managed interpreter | D575-S2-01 / T575-S2-01 |
| R575-S2-02 / BEH575-S2-02 | M 已采用的 installed `.3` 基础图及固定 Fork Task2/session3 与自身 receipt 一致，历史身份、配置和原生资产保持；不声明 `.4` parity | D575-S2-02、03 / T575-S2-02、04 |
| R575-S2-03 / BEH575-S2-03 | 四份当前源码公开映射准确表达 `.4` 未发布、CLI/Core `0.7.0-castbox.3` 和固定 Fork；稳定 `.3` tag、旧锁与历史证据保持原归属 | D575-S2-01 / T575-S2-01、02 |
| R575-S2-04 / BEH575-S2-04 | 最小证明覆盖 source/graph、现存 `.3` receipt、固定 Fork native、版本消费者及模块恢复、ownership/平台入口/卫生/secret scan；source/installed/fixture/外部层次不混用 | D575-S2-02、03 / T575-S2-01、02、04、05 |
| R575-S2-05 / BEH575-S2-05 | 原 RDT owner 在独立 draft 贡献完成当前切片 reconciliation 与双向 trace；完整贡献与 shared promotion 留给 S3，晋升前后分别执行原 committed Review 门禁 | D575-S2-04 / T575-S2-06 |
| R575-S2-06 / BEH575-S2-06 | S2 经 Check/TaskCommit/独立完整 Review、Refs-only Delivery 形成真实 clean committed `.4` source；S3 消费该来源后，Whole Completion 才判断全部准备责任，Closure/Finish 与软件发布独立 | D575-S2-03、04 / T575-S2-03、06 |

## 后继范围与历史边界

旧草案将完整 `.4` 投影与正式维护证明放入 S2；当前规划用 S2 来源→S3 正式消费替换其来源循环，既有身份保留但不将旧草案作为当前验收。原 S3 已按实际来源依赖分为当前来源修复与后续完整安装 Delivery；后者承接全 `.4` packages/runtime/schema/四平台投影、三平台 reapply/drift、focused Codex clean/local-workflow、真实 stable `.3` predecessor 维护、native/下一 owner、同操作 resume、不兼容单侧 tools rollback 和最终 contribution/promotion。其设计与测试定位见 D575-S2-03/04、T575-S2-03/06；这些义务继续归同 Task R575-03..07，不能由 S2 合并消除。

不新增 API/owner/兼容 reader/恢复框架，不纳入 #577/#46 产品实现，不升级真实业务仓或执行累计多平台/native-host 矩阵。最终 main exact candidate、远端 immutable provider、tag smoke、Release 与 Issue 关闭仍归 #575 Stage 2。

## 当前来源修复增量

本轮贡献以 RDT `current-main-0.6.17-guru.101/active` 与 Architecture `.94/active` 为适用 authority；上述 S2 来源、结果及其当时 `.100/.93` 身份保留历史归属。当前 S3 的独立交付不删除同 Task 后续完整安装责任。

| Requirement / Behavior | 必须满足的行为 | Design / Test |
| --- | --- | --- |
| R575-S3-01 / BEH575-S3-01 | `validate_installed=False` 只验证 canonical 来源，不读取 target installed manifest；default/True 继续要求并验证原安装证据 | D575-S3-01 / T575-S3-01 |
| R575-S3-02 / BEH575-S3-02 | 在原 validator 与 preset source-only 调用边界证明同失败点修复，并保留 default/True 对照；模块证据不冒充正式工具安装 | D575-S3-01 / T575-S3-01、02 |
| R575-S3-03 / BEH575-S3-03 | 先经原 Check/TaskCommit/完整独立 Review 交付可消费的真实 source；后续完整安装使用新的 source_locked 操作，不变更旧 recovery/source/preimages | D575-S3-02 / T575-S3-02、03 |
| R575-S3-04 / BEH575-S3-04 | 当前只收敛既有 draft contribution 与双向 trace；完整安装、最终 RDT promotion 前后门禁、Completion/Closure/Finish 留同 Task 原 owners | D575-S3-02 / T575-S3-03 |
