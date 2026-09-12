# #329 Developer-free Trellis adoption Design contribution

状态：`reviewed_candidate`；change path：`target_native`；expected current：
`current-main-0.6.5-guru.48`。本设计不建立兼容分支或第二 identity authority。

- `D329-01`：`trellis-source.json` 是唯一 source lock。固定 Fork checkout 自行安装依赖并 build，
  `packages/cli/bin/trellis.js`、CLI version、package manager 与 `.guru-source-commit` 必须绑定实际 HEAD。
- `D329-02`：Trellis-owned managed assets 只由 `0.6.17` official update/migrate/generation 产生；
  Guru-owned workflow、Skill、runtime、installer、fixture、spec 与平台 overlay 在 canonical source 直接演进，
  再经 preset reapply 投影到 dogfood/installed copies。
- `D329-03`：current task resolution 使用 explicit selector、task metadata、Git common-dir/branch/worktree、
  ignored task/workspace mappings 和 issue ledger；这里的 workspace mapping 仅表示隔离 task
  checkout/worktree，不是 legacy journal workspace。legacy identity、journal、唯一候选与 assignee
  fallback 不参与选择。
- `D329-04`：新 task 的 creator/assignee 由 workspace owner executor 显式传入 official task store；
  Issue 未分配时仅在 repo access preflight 通过后使用 authenticated GitHub login，失败时 write 前停止。
- `D329-05`：update/reapply 在动作前后对 legacy roots 建立 path/mode/byte snapshot；snapshot 只服务
  preservation validator，不成为 semantic authority、authenticity 或 anti-tamper boundary。
- `D329-06`：受控 consumer 按 subtraction-first 同步迁移并删除旧 Guru path；不保留 adapter、fallback、
  dual-read/write 或 hidden global identity。上游 retired stub、negative assertion 和 immutable history
  分别按其现有 owner 保留。
- `D329-07`：三平台 lifecycle matrix 使用 target checkout 的 managed runtime 和 fixture GitHub provider，
  分层验证 source build、generated adoption、focused regression、installed lifecycle 与 legacy preservation；
  未发布 workflow sample 从 bundled `native` 初始化后安装本地 candidate，并显式保留 local-sample boundary；
  每个 installed closeout 从排除 legacy/runtime/task/backup 的 clean committed candidate source reapply；
  capability comparison 以 before observable capability 为 after 的子集，删除/缺失阻塞，纯新增单独记录。
- `D329-08`：task writer 只写 #329 delivery 与 task-isolated RDT/Architecture contributions；shared current
  writer 仅为 serialized RDT/Architecture promotion owners。promotion-created diff 重新进入 Phase 2、
  Task Commit 与 independent full-diff Branch Review。

Architecture inheritance 由
[`architecture-contribution-329-developer-free-trellis-v1`](../../architecture/contributions/329-adopt-developer-free-trellis.md)
拥有。该 candidate 遵循 current design constitution，不改变 23 Skills / 97 exits 的业务图；如实现发现
公共 graph 必须变化，先使本 Planning/Architecture result stale 并重新进入对应 owner。
