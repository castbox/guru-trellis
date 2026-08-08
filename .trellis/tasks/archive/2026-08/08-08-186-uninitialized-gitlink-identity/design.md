# 技术设计

## 设计原则

将 Gitlink identity 分成两层：

1. superproject-recorded identity：来自 reviewed commit/index/合法 overlay 的 `160000` OID，是 reviewed-content tree 的身份来源。
2. initialized worktree validation：仅在 submodule worktree 实际初始化或路径存在变化时，验证 exact root、HEAD、dirty 与既有 binding。

deinitialized-clean 只跳过“必须存在独立 submodule Git root”这一不适用前提；不会放宽 overlay、dirty、drift、删除或替换检查。

## 影响边界

- Canonical runtime：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- Canonical tests：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- Installed dogfood copy：由 preset `apply.sh --repo .` 从 canonical source 同步，不手工形成第二套逻辑。
- Durable docs：现有 `.trellis/spec/workflow/companion-scripts.md` 已定义 deterministic executor/validator、标准库与 fail-closed 边界；本次属于既有合同内的 correctness 修复，不新增公开合同。

## 状态判定

| 状态 | identity 来源 | 结果 |
| --- | --- | --- |
| Gitlink 路径缺失或为 deinit 后空目录，且无 index/worktree overlay | superproject 记录的 OID | 通过 |
| 已初始化、exact root、HEAD 可解析、clean，且与当前 reviewed binding 一致 | 当前合法 Gitlink binding | 通过 |
| 已初始化但 dirty | 无 | 失败 |
| 已初始化但出现未绑定 HEAD/pointer drift | 无 | 失败 |
| Gitlink 有合法 reviewed overlay | 既有 overlay/binding 规则 | 按现有候选绑定处理 |
| 文件/符号链接替换、非空 root mismatch、删除或歧义状态 | 无 | 失败 |

## 实现方案

1. 为 reviewed-content Gitlink 增加一个窄 helper，输入当前 tree/index 记录的 OID以及该路径是否存在 overlay。
2. helper 先识别可证明的 deinitialized-clean：路径不存在，或为不承载独立 Git root 的空目录；该路径必须没有 overlay。此时返回 recorded OID 与 `initialized=false`。
3. 其他状态复用严格的 `task_commit_gitlink_worktree_identity()`，继续检查 exact root、HEAD、dirty。
4. `reviewed_content_identity()` 在处理 `160000` entries 时调用该 helper；不得在其他消费者复制 fallback。
5. 变化路径继续由现有 NUL-safe porcelain overlay 与 task binding 逻辑约束，并在 reviewed-content 边界执行 expected OID/binding 比较，确保未绑定 drift 不会被当作 deinitialized fallback。

## 兼容性与风险

- 输出算法 id 不变；同一已初始化 clean 状态的 digest 应保持不变。
- deinitialized-clean 的新 digest应与相同 Gitlink OID 的 initialized-clean digest 一致。
- 最大风险是把非空 root-mismatched 目录误判为未初始化，或误伤合法 Gitlink overlay；测试必须单独锁定这两个边界。
- 不需要数据迁移、配置迁移或 public schema 变更。

## 回滚

代码与测试为局部 companion runtime 变更，可通过回滚该提交恢复旧行为；没有外部数据或持久化格式迁移。
