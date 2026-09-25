# #454 C6/C7 Task Creation And Phase C Validation Design Contribution

状态：`reviewed_promoted`；immutable predecessor `.63`、current successor `.64/active`。关联
`architecture-contribution-454-task-lifecycle-state-model-c6-c7-v1`，采用 `target_native`。以下是
owner/contract design；C6 shared runtime/schema 已在非激活 slice 交付，完整 package 或 production projection 未交付。

- `D454-C6C7-01`：task creation composition 只消费 reviewed target/source 与 C2 TaskLifecycle DTO、C3 checkout
  acquisition/resolution、C4 branch association、C5 ledger/session adapter。Issue creation 返回 live Issue 后先走
  Sync/fresh Intake；create owner 不执行 Issue mutation，也不从 free-text scope 恢复 source。
- `D454-C6C7-02`：adopt path 使用当前 invocation registered checkout 与 reviewed decision head，复核 base、
  repo common dir、live branch、clean state、head 和 exclusivity。base drift 与 feature-head drift 分别投影
  refresh-review/blocked；不自动 provision 第二个 worktree。
- `D454-C6C7-03`：provision path 将调用期审查的 branch、decision head、target path 与 C3
  `CheckoutAcquisitionPlan.provision_disposition` 的 `new_branch | existing_branch | existing_checkout` 绑定为
  本次 acquisition；live pre-state 变化须重新审查，不另设 create/reuse enum 或 alias。`new_branch` 创建 branch
  与 linked worktree，二者 Guru-owned；`existing_branch` 只新建 linked worktree，branch caller-owned、worktree
  Guru-owned；`existing_checkout` 精确复用已注册 linked checkout，二者 caller-owned。adopt primary/linked
  checkout 不带此字段，现存资源 caller-owned。新/旧混合资源逐项归属，不按存在性事后反推。
- `D454-C6C7-04`：official task primitive 写入稳定 TaskId、source、generation 0 与普通 scope；C4 初始化
  binding revision 0，C5 写入同 generation/current branch/epoch/revision 的 resource inventory。仅在两者
  建立后形成 task-created result；mutation 失败恢复同 owner pre-state，不改写 caller-owned resource。
- `D454-C6C7-05`：完成 task mutation 后调用 C5 session adapter。有效 context key 写 path-free record；
  无 key 投影 `explicit_task_mode`；写失败独立报告，不反向撤销 task。输出丢失时从 exact task identity、
  binding、ledger 与 live facts 只读 rematerialize同一 creation result，不重跑 create。
- `D454-C6C7-06`：activation input 是 current planning approval/TaskLifecycleKey 与待激活 task status 的
  fresh projection。`guru-activate-task` 未来独占 status mutation及同 owner只读result recovery；C6
  不创建该 Skill package，不把 `task.py start` 或 approval 当作 semantic gate。
- `D454-C6C7-07`：六个 stable IDs 仅放 planned inventory；planned rows 只含 ID/state 与非路由说明，manifest 仅列
  `planned_skill_ids`。active selector、canonical package directory、workflow、installed/platform bytes
  均保持 predecessor。完整 package I/O、typed exits、consumer closure 和 workflow/standalone parity 在 E434
  package composition 时完成，不由空目录或占位 interface 冒充。
- `D454-C6C7-08`：C7 subtraction proof 限定于新增 Phase C substrate，逐项查 mapping/path legacy read/write；
  predecessor 的退休在 E434 原子 activation 内进行。验证报告分别列出 focused runtime/schema、Fork source、
  active/planned inventory、preset/sidecar/managed Python、task/quality checks 与未验证边界，不把条件性
  throwaway 或局部 tests 投影为 Release Gate。

`ADR-015` 已负责 TaskId 与 framework-extension ownership；本提升不新增 ADR 或第二持久状态存储。
