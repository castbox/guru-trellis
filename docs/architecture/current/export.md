# 导出职责

Identity: SAMPLE-ARCH-EXPORT。状态: current。Owner: export-owner。

导出调用方从唯一导出需求与设计取得行为。导出与查询没有数据或状态依赖。当前定义允许导出产生任务完成状态；新增通知条件时，由 export-owner 更新这一完整单元及对应 R/D/T。导出入口不接管查询行为。

关系：[需求](../../requirements/current/export.md)、[设计](../../design/current/export.md)、[验证](../../test/current/export.md)、[未改调用方](../../consumers/export.md)。
