# #760 配置驱动新建位置：Architecture 贡献

Task `ad6d8fa0-4a68-496f-9b43-f6a57f914dc0`，generation 0，Delivery `0c1737fc-2d2e-426e-9edc-ecae8c6ca923`。来源为 https://github.com/castbox/guru-trellis/issues/760 完整正文。方案由本Delivery design.md单写。

## Authority 与完整拟写

适用 baseline= guru-trellis-architecture，constitution= guru-trellis-design-constitution-v1，change contract= guru-trellis-architecture-change-contract-v1。固定 before 为8c158381b5bdb61fd961cbb89e23c2d1f659c9aa。独立candidate_assessment选择architecture_impact/target_native，继承ARCH-FND-002、ARCH-FND-004、ARCH-DOM-022与ADR-RUNTIME-LOCATION，不新增平行ADR。

唯一目标是docs/architecture/01-current/runtime-location.md的ARCH-RUNTIME-LOCATION。完整拟写在同名目录proposed/docs/architecture/01-current/runtime-location.md；保留原环境、身份、来源、迁移与原owners的完整定义，只增加新建位置配置承接。共享根身份和导航不变。

## 责任与代价

共享runtime提供位置事实，AI保留策略与副作用，Task/task-free保留各自执行入口。三个当前consumer复用事实，不引入Task-free Task身份、目录allowlist、锁、映射或额外清理机制。旧绝对输入与新配置生成的兼容由原create-task及MIGRATION-760承接；旧错误生成语义从当前AI入口退出，合法显式/已有/恢复保留。

## Required concerns 与晋升

authority/constitution绑定上述阶段来源；boundary/decision与owner/single-writer保持事实、语义、执行分层；compatibility/exit按design第7节；无新GAP或宪法偏移；parallel-scope只写本隔离拟写；evidence/freshness区分固定before、实际candidate和写后；review/promotion在独立phase2及完整candidate Check后由原Architecture owner final_integration读真实target、整合、写回并读回。实现随后绑定actual after，最终Check与committed Review覆盖。

本文保留晋升前的隔离拟写与判断来源。原 Architecture owner 已在实际 candidate_checked 后，将完整拟写整合到[当前单元](../01-current/runtime-location.md)，并读回确认一致。知识晋升不代表最终 Check、Review、Task Completion 或 Release 通过。完整多平台矩阵、业务恢复和 Codex 清理均不属于本项。
