# #186 修复未初始化 Gitlink 的 task-bearing 验证

## 目标

修复 task-bearing extension verification 在目标仓库存在“未初始化且未修改”的 Git submodule 时，被 reviewed-content identity 前置校验错误阻断的问题。验证流程必须在无需初始化、下载或读取 submodule 内容的前提下，使用 superproject 已记录的 Gitlink OID 继续 isolated target/source checkout 与 throwaway installation。

## 背景与当前缺口

- 当前 `reviewed_content_identity(..., include_worktree=True)` 会遍历最终树中的每个 `160000` entry，并无条件调用 `task_commit_gitlink_worktree_identity()`。
- 该函数只接受已初始化、可解析为独立 Git root 的 submodule worktree；deinitialized submodule 留下的空目录会解析到 superproject root，从而返回 `uninitialized or root-mismatched`。
- 未初始化并不等于身份不确定。路径没有 worktree/index overlay 时，当前 commit/index 已提供稳定、credential-free 的 Gitlink OID。
- 该前置失败会阻断 task-bearing verification、Publication 和 Finalizer；taskless standalone 路径不会触发同一 task-worktree identity 前置条件。
- Issue 评论中的真实仓库证据表明，要求调用方初始化 submodule 不是可靠绕过：历史 Gitlink OID 可能已无法从 submodule remote 获取。

## 需求

### R1 未初始化且未修改的 Gitlink

- 当 Gitlink 路径未初始化，且未出现在 worktree/index overlay 中时，reviewed-content identity 必须保留 superproject 当前 commit/index 记录的 `160000` OID。
- 不得为完成 identity 计算而运行 `git submodule update --init`、下载对象、读取凭证或访问 submodule remote。
- 同一 superproject 状态必须产生稳定、可复算的 reviewed-content identity。

### R2 已初始化与变化路径的严格校验

- 已初始化的 submodule 仍必须验证 exact Git root、可解析 HEAD 和 clean worktree。
- dirty submodule 必须失败。
- HEAD、index、commit Gitlink pointer 的变化只有在现有 reviewed overlay/task binding 合法覆盖时才能进入候选；未绑定或捕获后的 drift 必须失败。
- 删除、文件/符号链接替换、非空 root-mismatched 目录或其他无法唯一识别为 deinitialized-clean 的状态必须失败。

### R3 共享消费者一致性

- task-bearing extension verification、Publication 和 Finalizer 共用的 reviewed-content identity 必须采用同一行为，不增加旁路实现。
- taskless standalone verification 的既有行为不得回归。

### R4 分发一致性

- 修改 canonical companion runtime 后，必须通过 Guru preset installer 同步 dogfood 安装副本。
- canonical source、installed `.trellis/guru-team/**` 与 extension manifest 的受管资产必须无漂移，不产生未处理的 `.new` / `.bak`。

## 验收标准

- [ ] deinitialized-clean Gitlink 不再触发 `uninitialized or root-mismatched`，reviewed-content identity 使用 superproject 记录的 OID且重复计算稳定。
- [ ] task-bearing verification 能继续到 isolated target/source checkout 与 throwaway installation。
- [ ] 生成并通过 schema 3.0 `marketplace-verification.json`。
- [ ] initialized-clean Gitlink 继续通过并使用一致 OID。
- [ ] initialized-dirty Gitlink 继续失败。
- [ ] 未合法绑定的 initialized HEAD drift 继续失败。
- [ ] index/commit pointer drift 或 capture 后 drift 继续失败。
- [ ] 删除、替换、非空 root mismatch 与其他歧义状态继续失败。
- [ ] 回归测试覆盖 deinitialized-clean、initialized-clean、initialized-dirty、HEAD-drift、pointer-drift。
- [ ] preset apply、dogfood overlay drift、source/installed package validation、目标 Gitlink 测试类及完整 `test_guru_team_trellis` suite 通过。

## 非目标

- 不初始化、修复或迁移业务仓库的 submodule。
- 不获取私有 submodule 凭证，不修改 `.gitmodules` 或 remote。
- 不改变公开 Skill id、schema id、typed exit 或 public DTO。
- 不重构无关 task commit transaction、Publication 或 Finalizer 流程。
- 不新增恶意输入、并发竞态、TOCTOU、锁、fault injection 或跨 OS 原子性加固。

## 开放问题

无。Issue、当前代码和测试已提供实现所需的全部 load-bearing 信息。
