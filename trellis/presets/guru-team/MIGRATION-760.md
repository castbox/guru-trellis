# #760 配置生成的 worktree 路径迁移

本合同修复新位置生成的配置承接。正式 Task 保留原 acquisition、身份、binding 和恢复；
task-free 保留原普通 Git owner。没有 Task 数据迁移、位置映射或自动搬移。

## 新建输入与旧调用

`guru-create-task` 的 acquisition 加性提供 `path_source=configured|explicit` 与
`worktree_name`。对 `provision_linked_worktree` 的 `new_branch|existing_branch` 新目录：

- AI 自行生成位置必须使用 `configured`，提供一个已审单目录名 `worktree_name` 及绝对
  `checkout_root`。runtime 从确证 primary 的配置解析 root/name，并在创建 branch、
  worktree 或 Task 前核对计划；不一致时报告诊断，由原 owner 修正后重入，不静默换路径。
- 调用方真实指定新位置使用 `explicit`，沿原绝对 `checkout_root` 合同执行。
  该位置可在生成 root 外。AI 自行填入的绝对值不能证明调用方显式选址。
- 已发布输入省略新增字段时，仍沿原绝对 `checkout_root` 语义，由同一公开 schema 和
  executor 消费。实际旧 consumer 是已安装 create-task 的公开输入及其创建/恢复脚本。
  原 create-task owner 维护此兼容边界；调用方切换新策略字段后，该调用退出省略用法。
  当前 canonical AI 合同直接使用新策略，不借省略字段生成新位置，不新增另一 executor。

`adopt_invocation_checkout`、`existing_checkout` 和 `recover_created_task_result` 保留
各自的合法身份、绑定、clean 与位置适用性检查。生成 root 不是已有 checkout 的 allowlist。
恢复按已验证绑定找原位置，配置变化不重定位、不另建 Task 或 worktree。

## 配置与环境输出

primary 是同一 common-dir 下由 live Git topology、实际 toplevel 和 gitdir/common-dir
事实确证的主仓库。不能盲信 porcelain 首行，也不能假设 common-dir.parent 是 primary；
separate-git-dir 尤其需要实际核对。不能唯一确证时报告 `primary_anchor_unavailable`。

配置来源为 primary 的 `.trellis/guru-team/config.yml`。空 `worktree_root` 解析为
`<primary-parent>/<primary-name>-worktrees`；相对值相对 primary，绝对值直接使用。
同一配置不因 primary/linked/detached 调用而改变 root。linked 的空模板不表示独立选址；
调用 checkout 非空 root 解析后与项目配置不同则诊断冲突，不能自动覆盖配置。

`check-env.sh` 的 `worktree_root` 从旧的调用位置回退/未解析配置值改为项目解析后的绝对 root，
并提供 primary/config 来源事实。直接 consumer 是两个新建 owner 的 AI 计划与预检，
不是 selector 的 typed DTO 或持久路径 authority。其他调用方不得继续自行拼接调用 cwd。

公开 `--worktree-name <name>` 生成新目标；配合 `--checkout-root <absolute-plan>`
核对配置生成计划。后者需要前者。task-free 原 owner 先分流已有采用/continuation，
新建时消费实际预检目标执行普通 `git worktree add`，创建后读回目录、Git 注册及位置适用性。
它不调用 Task acquisition，不引入 TaskId、binding、session 或新路径台账。

## 安装、退出与证据边界

受影响资产为 create-task/task-free/环境查询合同、公开 schema/commands/errors、共享解析及
原创建 consumer、配置模板和使用说明。当前源成套更新；已有安装继续其 matching 版本，
采用新能力通过原 `guru-upgrade-tools` owner 更新完整工具投影，保留用户配置、Task/session、
peer 和原冲突/sidecar处理。不能手抄受管文件或以普通 apply 的旧 Task 阻塞为由绕过维护。

本项不恢复 `workspace_mode: current` 的 primary 写入，不改 Codex 清理，不恢复业务工作区，
不处理 #759、暖池或完整 Release 矩阵。定向行为结果、实际安装与分发结果由 Test 单元记录；
源码和合同变化本身不表示已有安装、真实 Agent 业务链或生产效果通过。
