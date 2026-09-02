# #330 Requirements contribution

本 contribution 收敛 current Commit、Publication、Finalizer、Merge 正常调用面，
不改变四个 Skill 的 semantic owner、typed exits、独立副作用确认或 #267 Release Gate。

- `REQ-027`：四个 Skill 各自提供唯一 recommended Happy Path，不创建跨阶段 monolith；Agent
  正常路径只读公开 Skill 合同与 public I/O，不读 runtime/schema/eval/test 来拼装流程。
- `REQ-028`：Commit 使用一次 `prepare-task-commit` 加一次确认后的
  `invoke-guru-create-task-commit-happy-path-v1`，保持 exact staging、hooks、expected old ref、
  unrelated preservation 与 stdout-loss recovery。
- `REQ-029`：Publication 使用一次 `review-task-publication` 完成已作出的 AI semantic result
  的 record/check/projection，并在 invocation-local current snapshot 上避免重复完整读取。
- `REQ-030`：Finalizer 使用一次 preview、独立确认和一次 `finalize-task-happy-path`；只有
  same-plan mapped deterministic reprepare/recovery 可自动承接，plan/scope/authority/payload/
  side-effect set 变化必须重新 preview 与确认。
- `REQ-031`：Merge 在 checks pending 时只使用一个 repo/PR/expected-head-bound watcher，
  确认后只调用一次 `complete-task-pr-merge`，完成一次 pre snapshot、一次 expected-head
  mutation 和一次 post snapshot；所有 Merge typed exits 均停止当前 Skill。
- `REQ-032`：旧 commands 保持 compatibility/testing/recovery 可用；同一 fixture 的 public
  exit/DTO、blocker、mutation、recovery 和临时状态生命周期必须等价。正常路径 command
  invocation 至少下降 50%，重复完整事实读取至少下降 70%，terminal 后 operation 为 0。
- `REQ-033`：wall-clock、模型轮次、GitHub API 与外部 CI 时间只作观测并分项报告；未达到
  时间目标不单独判定失败。#330 的硬成败由 correctness、等价性、operation budget、
  distribution 与代表性 installed/throwaway 验证决定。

完整 release-wide 多平台 exact-candidate matrix 继续由 #267 承担。
