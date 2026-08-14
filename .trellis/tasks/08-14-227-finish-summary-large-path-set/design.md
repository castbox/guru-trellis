# 设计

## 现状

固定限制存在于 canonical `finish-summary.schema.json` 的两个数组，以及 Publication Review、Finalizer 两份 package-local owner runtime。受管 installed/dogfood 与 Shared/Codex/Claude/Cursor 投影必须与 canonical 保持字节一致，但本 Issue 禁止通过 preset apply/reapply 生成这些副本。

## 方案

1. 从 canonical schema 的 `git.changed_paths` 与 `index.search_terms.paths` 删除 `maxItems: 2000`，保留 `type`、`uniqueItems` 与安全路径定义。
2. 在两个 owner runtime 中仅移除固定数量拒绝；继续逐项检查安全路径、唯一性、排序，并验证 `index.search_terms.paths` 与 `git.changed_paths` 完全相等。
3. 在 schema、Publication Review 和 Finalizer 直接测试中构造至少 2001 个确定性安全路径，验证完整集合通过。
4. 对非法、重复、未排序和集合不一致分别保留或补齐负例，证明放宽仅影响容量。
5. 使用精确文件编辑同步 canonical 与仓库中已存在的 installed/dogfood、Shared/Codex/Claude/Cursor 受管投影源；通过静态 byte equality、manifest 和 drift checker 验证，不运行 installer 或 apply。

## 兼容性

- Schema 版本、字段形状、公开 DTO、typed exits、错误分类和 workflow route 均不变。
- 历史合法摘要不需要迁移；大型摘要由固定拒绝变为接受。
- 内存与摘要体积随真实 diff 线性增长，这是完整 changed paths 既有合同的直接成本，不引入截断或摘要替代。

## 风险与控制

- 只修一个 owner 会造成 Publication 与 Finalizer 行为分裂：以对称 runtime 正向与负向测试约束。
- 容量放宽可能误伤路径约束：用非法、重复、未排序和集合不一致回归隔离行为边界。
- 手动同步可能产生受管漂移：逐一执行 byte equality、manifest 声明一致性、dogfood drift 和零 sidecar 检查。
- 安装态与原业务阻断不在本任务证明范围：PR 明确交由 #222 在 #227 合并后验证。
