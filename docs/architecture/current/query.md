# 查询职责

Identity: SAMPLE-ARCH-QUERY。状态: current。Owner: query-owner。

查询调用方从唯一查询需求与设计取得行为。查询和导出没有数据或状态依赖。当前定义允许查询返回数据或失败；新增明确错误来源条件时，由 query-owner 更新这一完整单元及对应 R/D/T。查询入口不承担导出或通知职责。

关系：[需求](../../requirements/current/query.md)、[设计](../../design/current/query.md)、[验证](../../test/current/query.md)、[未改调用方](../../consumers/query.md)。
