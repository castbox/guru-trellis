# #332 Original-entry correction Requirements contribution

本 contribution 承接 live Issue #332、用户对 #330 产品意图的当前澄清，以及 task
`332-release-matrix-public-wrapper-contract` 的 planning。它继承唯一 active
`current-main-0.6.5-guru.44` Requirements/Design/Test 与 Architecture authority，只形成
task-isolated candidate，不修改 shared current。

- `R332-ENTRY-01`：Commit、Publication、Finalizer、Merge 必须继续使用既有
  `scripts/invoke.sh` public wrapper 和稳定 command id；#330 的性能优化不得要求 caller 切换到
  第二套 Happy Path wrapper 或 command。
- `R332-ENTRY-02`：PR #341 已实现的 invocation-local snapshot、事务执行、mapped recovery、
  stdout-loss recovery、watcher 和 terminal stop 必须直接并入原 command；不得简单回退到 PR #341
  之前的多命令慢路径。
- `R332-ENTRY-03`：同一 `invoke.sh` 只根据互斥参数形态选择一次执行模式。正常参数直接进入
  Happy Path；只有检测到旧参数形态时才进入 compatibility branch，正常路径不得先运行兼容检查、
  双写状态或重复读取相同 live facts。
- `R332-ENTRY-04`：删除 PR #341 新增的四个 facade command/wrapper：
  `invoke-guru-create-task-commit-happy-path-v1` / `invoke-happy-path-v1.sh`、
  `review-task-publication` / `review-task-publication.sh`、
  `finalize-task-happy-path` / `finalize-task-happy-path.sh`、
  `complete-task-pr-merge` / `complete-task-pr-merge.sh`。
- `R332-ENTRY-05`：record、check、execute、preview 与 helper 继续是 package-private 诊断、测试或
  有界恢复能力；平台 public projection 对每个 Skill 只包含 Interface 声明的唯一 wrapper。
- `R332-ENTRY-06`：installer、source/installed validator、compatibility matrix、throwaway verifier、
  generic eval/runtime 和 platform projection 必须从
  `interface.json.public_contracts.invocation.wrapper` 读取 wrapper path，不得全局硬编码
  `scripts/invoke.sh`。
- `R332-ENTRY-07`：`guru-restore-archived-task/scripts/restore-archived-task.sh` 保持其原 public
  identity，并作为非 `invoke.sh` 的正向回归样本；本任务不重命名或重新设计该 Skill。
- `R332-ENTRY-08`：不得在 `.trellis/guru-team/scripts/bash/**` 补建 Finalizer 或其它 Skill 私有
  wrapper。README、manifest、ownership inventory 与 installed files 只能声明真实 shared assets。
- `R332-ENTRY-09`：Commit、Publication、Finalizer、Merge 的 semantic gate、freshness、expected-head、
  独立副作用确认、Issue disposition、恢复和 fail-closed 边界保持不变；性能优化只删除正常路径的
  重复编排与无 consumer 检查。
- `R332-ENTRY-10`：successor current authority 必须为
  `current-main-0.6.5-guru.45`，其 live graph 从 `.44` 的 23 Skills / 97 exits / 81 commands 收敛为
  23 Skills / 97 exits / 77 commands。旧 exact-candidate evidence 因 delivery bytes 和 authority
  变化而失效，preparation 合并后必须从 fresh `origin/main` 重新建立 candidate 并从零运行 Release Gate。

本 contribution 不发布版本、不执行实现、不授权 shared-current promotion，也不记录动态 Gate、
Git/GitHub mutation、时间或用户授权。
