# #211 技术设计

## 1. 设计边界

修复 owner 保持在
`trellis/skills/guru-team/packages/guru-create-task-commit/`。Markdown Skill/contract
继续拥有 AI scope、message 与 sufficiency 判断；package runtime 只执行并校验确定性
Git 事务。没有第二个同语义 consumer，因此不把 transaction primitive 提升到 shared
kernel。

## 2. 事务模型

```text
validated candidate + live Git preimage
  -> 创建临时 transaction worktree / isolated index / message file
  -> materialize exact candidate tree
  -> detached HEAD 指向 reviewed parent
  -> git commit --cleanup=verbatim -F message-file
       pre-commit
       prepare-commit-msg
       commit-msg
       create commit + transaction ref
       post-commit
  -> 验证 hook 后 message/index/worktree/tree/operation state
  -> 验证 commit parent/message/path/blob/mode/complete tree
  -> conditional update-ref 发布 live branch
  -> mixed reset exact live index 语义
  -> 验证无关状态并清理 candidate/checkpoint
```

临时 worktree 不是另一个业务 workspace。它只承载本次 transaction 的 reviewed
parent 和 exact candidate 内容，使 hook 的 `PWD`、`HEAD`、index 与 worktree 视图一致。
isolated `GIT_INDEX_FILE` 防止 hooks 直接读写 live index；message file 权限为 `0600`。

## 3. Hook 前后不变量

### Pre-ref gate

在发布 live branch 前必须证明：

- transaction commit 唯一 parent 等于 `pre_commit_head`；
- raw message bytes 等于 candidate message bytes；
- commit tree 等于 pre-hook reviewed tree；
- exact paths 的 blob/mode、committed path set 与完整 tree 均一致；
- transaction index 不包含 hook 新增、删除、rename、stage、unstage 或内容/mode变化；
- transaction worktree 未出现 tracked/untracked mutation；
- live branch、live semantic index entries 与无关工作区状态仍等于 preimage。

`prepare-commit-msg` / `commit-msg` 必须运行，但本合同禁止它们改写 message；
因此任何 bytes drift 都返回 `revision-required`/`blocked` 对应的稳定 executor failure，
不自动吸收。

### Post-commit gate

Git 在 `post-commit` 前已创建 transaction commit。若 hook 非零退出或改变 transaction
index/worktree，executor 返回带 `commit_sha`、`pre_commit_head` 和 failure stage 的
post-ref recovery facts，保留 candidate 与 Phase 2 checkpoint。由于 live branch 尚未
执行 conditional `update-ref`，用户分支不前进；created commit 保留为可核验对象。

## 4. Live state preservation

- transaction index 从 reviewed parent 创建，只 materialize exact paths。
- live index pre/post 使用 `git ls-files --stage -z` 的 `mode/blob/stage/path` 比较；
  不读取或比较 index 文件原始 bytes。
- unrelated staged/unstaged/untracked/gitlink 在 transaction worktree 外保持原状。
- 发布成功后只对 exact paths 做现有语义 reset/refresh，并复核 unrelated entries；
  不 stash、amend、rebase、force update 或自定义 rollback。

## 5. Runtime 与错误接口

优先在 package `runtime/execute.py` 内增加小型 helpers：transaction worktree lifecycle、
semantic index snapshot、worktree snapshot、commit evidence、hook failure normalization。
只有现有 error catalog 无法表达 pre-ref hook rejection 或 post-commit recovery 时，才做
additive error/interface 变更；不得破坏 public DTO 或 typed exit id。

## 6. 测试设计

所有 hook 行为用真实临时 Git repository 与 executable hook files 验证，不用 mock
subprocess 代替核心证据。测试矩阵：

| 场景 | 预期 |
| --- | --- |
| 四 hook 正常通过并记录环境 | commit 发布，记录顺序与 exact index/worktree/HEAD/message 正确 |
| pre-commit / commit-msg 非零 | live branch 不变，checkpoint/candidate/index/unrelated 状态保留 |
| prepare/commit-msg 改写 message | pre-ref fail closed |
| hook stage/unstage/add/delete/rename/modify | pre-ref fail closed |
| hook 创建 untracked path | pre-ref fail closed |
| post-commit 非零或 mutation | 返回 created commit identity 的 recovery，live branch 不发布 |
| unrelated staged/unstaged/untracked/gitlink | 成功/失败均保持 |
| stat-cache-only refresh | semantic index equality通过 |

## 7. 分发与升级

canonical package 修改后通过 preset `apply.sh --repo .` 同步 dogfood installed copy 与
platform projections，再运行 source/installed validators 和 drift checker。throwaway
验证覆盖 initial install、existing repo update/reapply 与 official `trellis update`；任何
`.new` / `.bak` 必须逐项处理。

## 8. Docs SSOT Plan

- Strategy：`ssot_first`。
- Docs state：`partial_docs`，现有 contract/spec 已声明真实 hooks，但实现不满足。
- 需要更新的 durable owners：
  - `trellis/skills/guru-team/packages/guru-create-task-commit/references/contract.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`（若安装/验证命令或声明需补充）
- 无需修改：global workflow phase/typed exits、Finalizer、Extension Verification、#208。
- canonical 文档先更新；preset apply 后检查 installed/platform projection byte parity。
