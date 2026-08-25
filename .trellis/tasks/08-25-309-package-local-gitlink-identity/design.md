# Design

## Boundary

最小行为缺口位于 `guru-check-task/runtime/common.py` 的 Phase 2 worktree
snapshot builder。修复只扩展这个私有 identity builder 及其 package-local
测试，并同步必要的 canonical spec/installed projection；不修改 public Skill
I/O、typed exits 或 Task Commit executor。

## Gitlink Resolution

1. 通过 `git ls-files -s -z -- <path>` 读取 stage-0 index entry；要求唯一、
   mode `160000`、合法 OID。
2. 通过 `git ls-tree HEAD -- <path>` 校验当前 commit 仍在同一路径记录同一
   mode/OID，拒绝 pointer/index drift。
3. 路径不存在或仅为未初始化 submodule 占位目录时，不读取内容，直接绑定
   index OID。
4. 路径是已初始化 submodule 时，验证其 top-level root 等于精确路径，读取
   `HEAD^{commit}` 和 clean status，并要求 submodule HEAD 等于 index OID。
5. 非 Gitlink directory、替换、删除、dirty 或歧义状态统一转换为
   `CommandError(stale_identity, reviewed_paths, ...)`。

Identity entry 使用固定字段表达 Gitlink，例如
`{"path": path, "kind": "gitlink", "mode": "160000", "oid": oid}`，并继续
按 UTF-8 path bytes 排序后进入现有 canonical JSON digest。

## Compatibility

算法 id 保持 `guru-phase2-worktree-content-1.0`。理由：旧算法在任何 Gitlink
路径上都失败，因而不存在可被误接受的旧 Gitlink checkpoint；对既有支持的
file/symlink/missing entry 不改变字段或排序。测试必须锁定这一兼容判断。

`guru-create-task-commit` 继续要求实际提交的 Gitlink initialized、clean、
HEAD 与 index OID 一致。Phase 2 identity 只证明完整 reviewed worktree 未漂移，
不授予 staging 权限。

## Validation Strategy

- 在临时 superproject + local submodule repository 上构造真实 Gitlink。
- 直接覆盖 `content_identity()` 与正常 recorder/checker wrapper，避免仅 mock
  `lstat()`。
- 复用 preset installer 创建 installed package，执行相同关键 fixture 或
  byte/parity validation。
- 运行 package tests、shared tests、dogfood overlay reapply/drift、ownership、
  syntax/compile 和定向 integration/eval。
