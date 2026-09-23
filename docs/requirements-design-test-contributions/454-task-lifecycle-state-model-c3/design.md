# #454 C3 Checkout Substrate Design Contribution

状态：`reviewed_promoted`。采用 `target_native`，关联
`architecture-contribution-454-task-lifecycle-state-model-c3-v1`，expected current 为
`current-main-0.6.17-guru.59`，promoted successor 为 `current-main-0.6.17-guru.60`。

- `D454-C3-01`：`task-lifecycle-dtos.schema.json` 从 35 个扩展到 39 个 named DTO。四个 C3 DTO
  使用 closed object 与 exact consumer projection；path-bearing fields 只存在于本次 acquisition 调用，
  不进入 TaskLifecycleDTO 或 durable authority。Candidate schema 用 conditional constraints 绑定 valid live facts；
  resolution 用互斥 shape 消除 selected id 与 candidate list 的重复 identity，zero-candidate recovery 仍由
  `selection_required` 表达。
- `D454-C3-02`：`git_facts.py` 从 `git worktree list --porcelain -z` 与当前 Git common-dir 派生 live
  repository/worktree facts；不读取 workspace mapping、历史 checkout path 或 installed runtime state。
- `D454-C3-03`：`checkout_resolution.py` 先统一验证 raw candidates，再形成 closed resolution。
  Pre-task validation 独立检查 task artifact 与 active task authority；selection 不能把 authority conflict、
  invalid candidate 或 multiple candidate 降级为 usable。
- `D454-C3-04`：`checkout_acquisition.py` 只实现 adopt 与 provision 两条 transaction route。两条 route
  在 mutation 前后复用同一 live validator；primary checkout 命中 provision 时返回 adoption remediation，
  不创建 linked worktree。
- `D454-C3-05`：provision transaction 记录 call-local expected identity。失败 rollback 只删除本 transaction
  创建且 identity 仍匹配的资源；output-loss recovery 只重建结果，不重复 mutation。Caller-owned resource
  永不由 C3 删除或改写。
- `D454-C3-06`：shared identifier primitive 同时约束 schema 与 runtime；checkout runtime error 使用 dispatcher
  共享的 `code`、`field_path`、`remediation` contract，避免第二 error vocabulary，并作为 E434 public package
  的唯一错误词汇输入。
- `D454-C3-07`：`guru-ensure-task-checkout` registry row 保持 `state=planned`，extension manifest 分离
  `active_skill_ids` 与 `planned_skill_ids`。Ownership validator 只要求 active IDs 对应 canonical package
  directories，并明确拒绝 planned ID 对应 package directory；E434 负责同时创建完整 package 并激活。
- `D454-C3-08`：inactive boundary 通过负向 surface contract 固定：active selector、workflow、active graph、
  installed copy 与 platform projection 均不消费 C3 planned ID。Canonical/installed 暂时不相等是 E434 前的
  明确状态，不是 C3 compatibility layer。
- `D454-C3-09`：验证分为 focused candidate evidence 与 deferred release evidence。Focused evidence 可以通过；
  raw preset apply 的 installed-copy conflict 必须保留为 unpassed suite result，并在后续 E434 activation 后由
  对应 owner 重新验证，不得在 C3 越权修改 projection。

本设计不新增 ADR。`ADR-015` 已拥有 TaskId/lifecycle 与 framework-extension boundary；C3 只实现其下一段
checkout substrate，不改变 owner、兼容策略或 activation 决策。

Promotion 只建立 `.60` current Design authority；promotion-created diff 的 fresh gates、C4-C7、D443、D436、
E434、production activation 与完整 Release matrix 仍须各自 owner 独立完成。
