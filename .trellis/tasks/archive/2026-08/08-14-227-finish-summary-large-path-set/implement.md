# 实施计划

## 1. 重新绑定当前范围

- 以 live #227 正文和无评论状态为唯一需求 authority。
- 以 `main@f109285e7b691f5f4f2c516f1a95095dcd5d2035` 为基线，确认 #219、#217、#218 已依次合并关闭。
- 审查现有 `origin/main...HEAD`，旧提交只能作为候选实现，不作为当前验收证据。

## 2. 合同与实现

- 删除 canonical 与 installed schema 的两处 `maxItems: 2000`。
- 删除 Publication Review 与 Finalizer owner runtime 的固定 2000 项拒绝。
- 保持路径完整、安全、唯一、排序一致以及两集合完全相等。
- 不修改其它字段上限、公开 DTO、错误分类或 workflow route。

## 3. 测试与受管投影

- 增加 schema、Publication Review、Finalizer 的 2001 个以上路径正向测试。
- 保留或补齐非法、重复、未排序和集合不一致负向测试。
- 精确同步 canonical、installed/dogfood、Shared/Codex/Claude/Cursor 受管投影源，不调用 preset installer 或 apply/reapply。

## 4. 验证

- 运行直接 schema、Publication Review、Finalizer package/runtime tests。
- 运行静态 byte equality、manifest 声明一致性、dogfood drift、`git diff --check`。
- 递归检查当前 checkout 零 `.new`、`.bak` 与未知 sidecar。
- 明确跳过所有 installer、throwaway、marketplace、update、业务仓安装/upgrade、tag-pinned 和原 2130 路径重放。

## 5. 收口

- 执行 `guru-check-task` 语义门禁，发现问题则回到实现修复。
- 后续 commit、push、PR 分别在精确副作用边界取得用户确认。
- PR 只使用 `Closes #227`；将 #222 列为安装型与原 2130 路径验证的唯一承接，不处理 #223，不声明发布就绪。
