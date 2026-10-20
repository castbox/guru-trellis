# 共享入口职责

Identity: SAMPLE-ARCH-SHARED。状态: current。Owner: shared-entry-owner。

有历史数据时不得覆盖已有条件。缺少来源时必须返回原 repair 路由，不推断来源或继续正常处理。允许新增的入口必须保留这两个前置条件；尚未批准查询和导出新增入口。查询和导出调用方引用本文，不复制当前规则。

关系：[需求](../../requirements/current/shared.md)、[设计](../../design/current/shared.md)、[验证](../../test/current/shared.md)、[查询调用方](../../consumers/query.md)、[导出调用方](../../consumers/export.md)。
