# #575 S2：来源准备需求

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

旧草案将完整 `.4` 投影与正式维护证明放入 S2；当前规划用 S2 来源→S3 正式消费替换其来源循环，既有身份保留但不将旧草案作为当前验收。后继 S3 承接全 `.4` packages/runtime/schema/四平台投影、三平台 reapply/drift、focused Codex clean/local-workflow、真实 stable `.3` predecessor 维护、native/下一 owner、同操作 resume、不兼容单侧 tools rollback 和最终 contribution/promotion。其设计与测试定位见 D575-S2-03/04、T575-S2-03/06；这些义务继续归同 Task R575-03..07，不能由 S2 合并消除。

不新增 API/owner/兼容 reader/恢复框架，不纳入 #577/#46 产品实现，不升级真实业务仓或执行累计多平台/native-host 矩阵。最终 main exact candidate、远端 immutable provider、tag smoke、Release 与 Issue 关闭仍归 #575 Stage 2。
