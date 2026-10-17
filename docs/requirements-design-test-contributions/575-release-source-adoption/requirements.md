# 正式发布来源采用需求

本增量承接 #575 的准备前置，不改变已完成准备 Task 或 #577 历史。来源 disposition 为 reference_only。完整 Task scope 以本次已接受 PRD 为准。

| 需求 / 行为 | 要求 |
| --- | --- |
| R575-SA-01 / BEH575-SA-01 | 正式锁定 PR52 merge7bcbeaad 的完整 Git/CI/CLI/Core/pnpm 身份，公开直接映射和受管来源一致；保留严格 source_locked 与历史 local_candidate 边界。 |
| R575-SA-02 / BEH575-SA-02 | 原 Plan2 从所选 CLI 的真实 Node 依赖解析 matching Core，同时支持 workspace 和 npm 布局；缺依赖、版本不配对仍拒绝，不改公共算法。 |
| R575-SA-03 / BEH575-SA-03 | predecessor CLI 从同一 tag manifest/lock 推导，与 predecessor Fork 配对；当前 CLI 仍是独立版本轴，发布输入仍六项。 |
| R575-SA-04 / BEH575-SA-04 | 正式 source_locked 工具与 Plan2 代表性隔离旧安装实际采用、history_only、reapply、目标 native/下一 consumer 按层次验证；历史数据和原写集保持。原tools首次apply前合成公开AGENTS最终target与Guru-owned block，正常upgrade后的原source rollback不得因合法第二writer变化失败；不改source/guard/compat或既有checkpoint。 |
| R575-SA-05 / BEH575-SA-05 | 准备切片经完整 Check/Review 和正常终结；Refs #575，不创建 tag/Release 或关闭发布 Issue，最终 main candidate 由 Stage2 重新验证。 |

不修改上游、全局包或 node_modules，不把 tarball 权限差异改写为已修复。测试事实仅由 test.md 维护。
