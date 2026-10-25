# #669 已有实现分支恢复

## 明确入口与旧消费者

`guru-reactivate-task` 的 Interface 1.6 选择
`public-input-selected-2.0.schema.json`。aggregate 只索引两个独立入口：原
`delivery_reactivate_shared_archive`，以及新增
`delivery_reactivate_existing_implementation`。原 clean-base 消费者仍用于从当前
base 的干净 checkout 开始新工作；原 public input、semantic result 和 transaction
2.0 保持原义及字节，不把旧输入重标为已有实现。

新 public input 只增加原 Draft PR 的 repository/number locator。准确 checkout、
逻辑内容和实现 HEAD 由同一 AI owner 的独立 semantic schema 承接。原四个 typed
exits、最小 DTO、Planning/Bind/resume/stop consumers 保持。snapshot 不流入公共
handoff，不保存授权。

## 调用与接续

先由原 owner 读取准确前驱、公共终态、bookkeeping merge 与实际后继。已有合法
后继时继续真实 key/ref；receipt 缺失不能触发第二次增代。没有后继时，AI 读取
真实实现提交、完整 staged/unstaged/untracked 差额与原 PR，分别审核 base HEAD
和实现 HEAD。只读 `scripts/observe.sh` 提供同 owner 的客观比较输入，其
intermediate receipt 不是语义通过。实际 wrapper 仍是 `scripts/invoke.sh`。

新入口只采用准确已存在的 primary/linked checkout。原 public reopen/formal
operation 和 C3/C4/C5 继续单写；不增加另一个生命周期。事务 3.0 保存下一次同
操作恢复必需的单一 `implementation_state`。其比较范围由已有 stage 决定：
`public_prepared` 时仅在 worktree 摘要中排除原冻结 plan 的精确文件写集，完整
index 与其余内容仍须一致；原只读公共 preview
另核自身文件／目录的前态或目标，随后才 recover/resume。这样可恢复实际已写入
但调用方只收到 pending 或丢失输出的操作，同时拒绝其余业务差额变化。public
writer applied 后覆写同一个值，在 `public_applied`／`bound` 阶段使用准确完整
的 after-state，避免把自己刚写入的 Task metadata 当作外部漂移。它不 restage 本地差额，不改变实现
提交，也不 push/create/edit/merge/close 原 PR 或清理资源。

原 2.0 在途操作使用原 clean-base profile；3.0 仅由新 profile 读取。profile 与
transaction 版本不匹配时停止。现有合法公共后继无 receipt 时仍经原 owner 核
identity/source/history 与当前事实，随后交原环境/Task/Delivery owner。历史结果
不成为当前 Planning、Check 或 Review 通过。

## 安装与验证边界

从完整 matching Guru source 成套 apply preset，包含 registry、Interface、
commands、schema、runtime、workflow 和平台投影。原 tools owner 继续核 Fixed
Fork source lock 和目标安装；不单独复制新 wrapper 或修改全局 Trellis。按原
installer 处理 `.new/.bak`，再运行 source/installed package、reapply/drift 检查。
旧安装不会因文件名相同而自动获得新语义。

源码回归与真实 Git/受控 provider 测试只证明各自层次。代表性完整安装后的
实际 Agent 从 installed 入口读取事实、author semantic result 并调用 wrapper，
才构成原生恢复证据。受控 provider 不证明真实 GitHub/backend/生产恢复；完整
多平台 Release 矩阵仍由其原 owner 承担。
