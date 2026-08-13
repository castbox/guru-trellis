# 设计

## 现状

同一任意限制存在于 canonical `finish-summary.schema.json` 的两个数组，以及 Publication Review、Finalizer 两份 package-local owner runtime。Preset 将 canonical 内容投影到 dogfood installed tree；只改单一副本会造成 drift。

## 方案

1. 从 canonical schema 的 `git.changed_paths` 与 `index.search_terms.paths` 删除 `maxItems: 2000`，保留 `type`、`uniqueItems` 与安全路径定义。
2. 将两个 owner runtime 的校验改为只要求 list，再逐项校验路径并验证 `sorted(set(paths))`，保留 search terms 与 changed paths 完全相等检查。
3. 在两个 owner package 的合同测试中构造 2001 个确定性安全路径，直接验证各自 `finish_summary_errors` 返回空结果。
4. 在 schema 回归中用同一有效 payload 验证 canonical schema 接受 2001 路径，并增加不一致/重复或乱序的负例，避免放宽非数量合同。
5. 通过 preset 官方 apply 同步受管 projection，再运行 source/installed、dogfood 与安装验证。

## 兼容性

- Schema 仍为当前版本 2；这是放宽任意容量限制，不改变字段形状或 consumer 行为。
- 历史 schema version 1 由同一 validator 接受更大完整路径集，不需要迁移已有摘要。
- 内存与摘要体积随真实 diff 线性增长，这是“完整 changed paths”既有合同的直接成本；本任务不引入静默截断。

## 风险与控制

- 风险：只修一份 owner 导致 Publication 与 Finalizer 行为分裂。控制：两包使用对称回归测试。
- 风险：手改 installed tree 形成不可复现差异。控制：canonical 修改后运行官方 preset apply 与 drift 校验。
- 风险：误删其它界限。控制：精确断言 commits 等现有上限仍存在，diff 仅覆盖路径数量限制。
