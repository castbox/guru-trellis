# #227 移除 finish-summary 变更路径数量的任意上限

## 目标

让 Publication Review 与 Finalizer 接受完整的大型变更路径集合，不再因固定 2000 项阈值阻断合法任务。

## 需求

- `git.changed_paths` 与 `index.search_terms.paths` 不得设置固定数量上限。
- 两处路径集合必须继续完整相等，并保持安全、唯一和排序约束。
- Publication Review 与 Finalizer 必须使用相同合同，不能只修复其中一个入口。
- canonical source、installed/dogfood projection 与平台公开投影必须保持一致。
- 不改变公开 DTO、typed exit、错误分类、提交数量限制或其它 finish-summary 字段合同。

## 验收标准

- [ ] 2001 个以上合法、唯一、已排序路径可通过 canonical schema。
- [ ] Publication Review owner 接受同一大型路径集合。
- [ ] Finalizer owner 接受同一大型路径集合。
- [ ] 重复、乱序、不安全路径或两处集合不一致仍 fail closed。
- [ ] canonical/installed equality、managed inventory、dogfood drift 和相关测试通过。
- [ ] 新 immutable source 安装到业务仓 #182 工作树后，其 2130 路径 Publication/Finalizer preflight 不再被固定上限阻断。

## 边界

- 不截断、采样或压缩 changed paths。
- 不修改业务仓 #182 的业务实现与既有测试结论。
- 不执行生产部署、业务数据写入、push、PR 或 merge。

## Docs SSOT Plan

- 当前 workflow/preset 文档已规定完整路径与一致性语义，本任务不新增长期概念或用户配置。
- 若实现检索发现公开文档明确宣称 2000 上限，则同步删除该陈述；否则保持 Docs SSOT 不变并在 Phase 2 记录 `not_applicable`。
