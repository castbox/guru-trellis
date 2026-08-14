# #227 移除 finish-summary 变更路径数量的任意上限

## 目标

让 Publication Review 与 Finalizer 接受任意规模、完整、安全、唯一且排序一致的变更路径集合，不再因固定 2000 项阈值阻断合法任务。

## 背景与发布顺序

- Live authority：`castbox/guru-trellis` Issue #227，当前无评论。
- 已确认 #219、#217、#218 依次合并关闭，当前基线为 #218 的 merge commit `f109285e7b691f5f4f2c516f1a95095dcd5d2035`。
- 固定顺序为 `#219 -> #217 -> #218 -> #227 -> #222 -> 发布`。
- #222 是 #227 合并后唯一 exact candidate 的累计 Release Gate；本任务不启动 #222，也不声明发布就绪。

## 需求

- 删除 canonical `finish-summary` schema 中 `git.changed_paths` 与 `index.search_terms.paths` 的 `maxItems: 2000`。
- 删除 Publication Review 与 Finalizer owner runtime 对超过 2000 个 changed paths 的拒绝。
- 两处集合必须继续完整、安全、唯一、排序一致且完全相等，不得截断、采样或压缩。
- 增加 2001 个以上路径的 schema、Publication Review、Finalizer 正向测试。
- 保留非法路径、重复、未排序及两处集合不一致的 fail-closed 回归。
- 同步 canonical、当前 installed/dogfood、Shared/Codex/Claude/Cursor 受管投影源文件，并保持公开 DTO、错误分类与 workflow 路由不变。

## 验收标准

- [ ] 2001 个以上合法、唯一、已排序路径可通过 canonical 与 installed schema 校验。
- [ ] Publication Review 与 Finalizer runtime 接受同一完整大型路径集合。
- [ ] 非法、重复、未排序或两处集合不一致继续 fail closed。
- [ ] 直接 schema、Publication Review、Finalizer package/runtime tests 通过。
- [ ] canonical/installed 及 Shared/Codex/Claude/Cursor 静态 byte equality、manifest 声明一致性和 dogfood drift 检查通过。
- [ ] `git diff --check` 通过，当前 checkout 递归检查为零 `.new`、`.bak` 与未知 sidecar。
- [ ] PR 只关闭 #227，并明确安装型验证与原 2130 路径业务场景由 #222 承接。

## 明确禁止

- 不运行 `guru-verify-extension-installation`、clean throwaway、marketplace 或 official Trellis update。
- 不运行 preset installer tests，不执行 preset apply/reapply，包括 targeted reapply。
- 不把修复安装到真实或隔离业务仓，不重放原 2130 路径业务场景，不执行业务仓 upgrade smoke 或 tag-pinned install。
- 不处理 #223，不启动 #222，不创建 tag/Release，不声称当前 `main` 已可发布。
- 不修改业务仓 #182 的代码、测试结论或远端状态，不执行生产部署或业务数据写入。

## Docs SSOT Plan

- 本任务放宽容量限制但不改变完整性、安全性、唯一性、排序或集合相等合同。
- Step-local schema/runtime/tests 是本次行为 SSOT；若 durable docs 存在 2000 上限陈述则同步删除，否则不新增重复说明。
- 安装、升级、发布和原 2130 路径的真实闭环证据只由 #222 持有。
