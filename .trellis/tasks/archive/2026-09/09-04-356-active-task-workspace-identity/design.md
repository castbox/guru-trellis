# Design

## Boundary And Ownership

修复分为两个相互配合的 Guru-owned 边界：

1. `guru-create-task-workspace` 的 executor/checker 负责创建事务的完整身份闭合、
   final boundary 和本次新建对象的可回滚记录。
2. Guru workflow 与 active-task route 的 package-local resolver 负责先验证
   active task，再决定是否进入 Intake；官方 Trellis `task.py`、`active_task.py`
   的上游生命周期实现不作为 preset 的 canonical source，不复制到 Guru package，
   也不通过 patch 改写官方文件。

## Identity Model

定义一个 package-local、只读的 `validated_active_task` 视图，输入为当前 checkout
与 session pointer，输出仅包含下游路由需要的 task locator、task id、status、
branch/base 和当前 phase。验证顺序固定为：

1. session/runtime pointer 存在、格式正确，并解析到 repository 内的 task 目录；
2. `task.json` 是 regular file，id、status、branch、base 和 locator 一致；
3. 当前 checkout 与 `git worktree list` 唯一绑定到 task branch；
4. Issue Scope Ledger 存在且通过现有 schema/trackability 检查；
5. task mapping 与 workspace mapping 存在、唯一、非 symlink，且字段与 task、
   branch、workspace path 完全一致；
6. session pointer 指向的 task locator 与上述闭合 identity 相同。

任一步骤缺失或冲突返回 `invalid_task_state`。session pointer 不被视为独立的
状态事实，也不允许通过单 session fallback 猜测一个可消费 task。

## Creation Transaction

创建 executor 保持现有 Issue-only 与 workspace/task-only 互斥模型，并扩展为：

1. 读取并锁定 reviewed plan 和当前 base/target facts；
2. preflight 检查所有目标对象和既有对象 disposition；
3. 创建 branch/worktree；
4. 写入 planning 状态的 `task.json`、ledger、Guru task/workspace mappings；
5. 执行 session/runtime 定位写入，但不把它单独作为 active authority；
6. 对完整闭合身份执行最终 boundary check；
7. 仅在最终 check 通过后，生成 `created` 结果并允许后续 activation。

异常处理使用 invocation-local created set，按反向顺序删除本次新建的 mapping、
artifact、task directory、worktree 和 branch；对 `reuse_exact`/既有对象只读不删。
回滚失败本身返回 `invalid_task_state`，并保留明确 stop reason，不尝试第二次自动
修复、迁移或重建。

`task.json` 在 planning 阶段保持不可消费的 planning 状态；若现有官方激活命令
仍需把它变为 `in_progress`，则 activation 前必须再次通过 validated boundary，
并保证 session pointer 写入失败不会留下可被识别的 `in_progress` 半成品。

## Workflow Routing

在 `workflow.md` 的 current-task route 中增加明确优先级：

- no active task：才允许 Phase 0 selector/standard Intake；
- complete active task：按 task status/phase 继续 Phase 2 或 Phase 3；
- invalid task state：进入唯一 stop target `invalid-task-state`，输出 remediation
  所需的最小事实，不进入 Intake/restore/rebuild/cleanup。

`guru-create-task-workspace` 的 Interface 增加 `invalid_task_state` typed exit、
独立 stop consumer schema 和唯一 workflow marker/route；已有 `created`、
`refresh_review`、`blocked` 语义不被静默改写。若 Interface 版本必须变更，则新建
明确版本 id 并同步 registry/manifest，不复用旧 schema 冒充兼容。

## Projection And Compatibility

Canonical 修改集中在 `trellis/workflows/guru-team/`、
`trellis/skills/guru-team/packages/` 和必要的 preset overlay/spec 文件；随后用
`apply.sh --repo .` 同步 `.trellis/workflow.md`、`.trellis/guru-team/` 与平台
projection，并运行 drift 检查。官方 Trellis-owned paths 不写入 preset ownership。

既有合法 task/runtime identity 的字段和 public handoff 保持最小；新增的
`invalid_task_state` 只携带唯一 stop consumer 所需的 task locator/state reason，
不携带授权、完整扫描、绝对路径或内部 checkpoint。旧任务格式不迁移：不符合新
闭合合同的对象只会被拒绝。

## Rollback And Risk

主要风险是创建顺序、回滚对象集合与 session pointer 生命周期不一致。测试必须在
真实临时 Git worktree 上注入每个正常失败点，比较 refs、worktree list、task/ledger
和 runtime/session 文件快照，确认既有对象不变、本次对象全部移除。若变更触及官方
task.py 生命周期、Finalizer 业务或需要迁移旧任务，则停止并回到规划重新审查。
