# #454 C4 Branch Association Test Contribution

状态：`reviewed_promoted`。以下是 C4 focused acceptance；它们不构成 promotion-created diff 的 Phase 2、Branch Review、Publication、
production activation 或 Release Gate 证明。

- `T454-C4-01`（R454-C4-01/02）：Draft 2020-12 与 runtime 同时验证 six-field binding、new epoch revision 0、
  same-epoch strict increment、stale epoch/revision 与 no-op rejection，以及 path/HEAD/session/ownership payload/
  refs namespace/reserved ref rejection。
- `T454-C4-02`（R454-C4-03/05）：隔离 Git fixtures 覆盖 binding+ownership 均存在、仅 binding、仅 ownership、
  两侧均缺失四象限；断言已有一侧不被改写且缺失侧沿用相同epoch/revision/branch，两侧均缺失才生成new
  epoch/revision 0并把pre-existing资源保守投影caller-owned。
- `T454-C4-03`（R454-C4-04）：覆盖 unique、zero、multiple candidate，registered/local branch 去重，exact task
  artifact/status/generation、wrong repository、registration mismatch、other-task binding 与 unresolved incarnation；
  unique local-only branch 在 provision 前返回 `checkout_acquisition_required`；retained
  `refs/heads/guru-task-lifecycle/*` refs不形成candidate。
- `T454-C4-04`（R454-C4-06）：dirty same-checkout fixture 同时包含 staged、tracked dirty 与 binary untracked bytes；
  换绑前后 binding epoch、HEAD、真实 index hash、worktree hash、status hash 与逐文件 bytes 必须相等。
- `T454-C4-05`（R454-C4-06/07）：existing-target 覆盖 clean exact artifact 与 ancestor-compatible success；artifact
  mismatch 阻塞，不相关历史返回 `rebind_reconcile_required`；source或target expected HEAD drift在mutation前阻塞。
- `T454-C4-06`（R454-C4-08）：target ref 存在 unresolved resource incarnation 时，candidate/prepare 均拒绝复用。
- `T454-C4-07`（R454-C4-09）：post-mutation failure 恢复 checkout branch、target ref absence、binding bytes 与
  ownership snapshot；caller-owned existing target 保持不变。
- `T454-C4-08`（R454-C4-09）：establishment/rebind output-loss recovery 可重复只读调用，结果 revision 不再次递增，
  ownership mutation 调用次数不增加；recovery必须匹配原epoch与expected HEAD，candidate label/id不是恢复凭据。
- `T454-C4-09`（R454-C4-10）：canonical ownership 与 preset tests 断言 32 active + 3 planned，两个新 ID 无
  package/interface/active graph/installed/platform projection。
- `T454-C4-10`（R454-C4-01..10）：完整 lifecycle runtime、两个 schema/registry/manifest JSON parse、Python compile、
  preset focused suite、task validation、`git diff --check` 与 touched non-generated file 3000-line check 只构成
  supporting evidence，不替代以下新增独立语义用例。

本 finding-fix 另以 `TST-032/SCN-044` 的执行级回归承接 Finalizer provenance binding：真实 Git predecessor/reviewed
graph 覆盖 strict historical ancestor，executor composition 断言 replacement transaction 写入 exact
`pre_push_remote_head`，后续 pre-mutation preflight 使用同一 remote identity，并确认 push/PR/archive/Issue mutation
均未发生。该用例不改变 `T454-C4-01..10` 的 scope，也不把 Finalizer 或 promotion-created diff 宣称为完成。

本次 Branch Review finding-fix 的新增独立覆盖固定为：

- association 与 surviving ownership 分别单侧丢失时，各自恢复同一 `binding_epoch`；
- association 与 active ownership 全部丢失时建立不同于旧值的new epoch/revision 0；
- same-checkout 与 existing-target rebind 分别保持source epoch，lost-output recovery拒绝epoch不匹配；
- candidate label/id保持相同时，source/target expected HEAD drift仍使mutation与recovery fail closed；
- discovery对registered checkout与local ref两条来源都跳过retained `guru-task-lifecycle/*` control ref。
- `git switch -c`因`post-checkout` hook非零返回失败但已经创建并切换target ref时，rollback仍恢复source branch、
  control state与checkout bytes，并安全删除本transaction新建的target ref。
- rebind transaction只从`source_binding.binding_epoch`派生unchanged epoch，不再接受第二份
  `target_binding_epoch`；成功rebind后target HEAD前进时，lost-output recovery必须拒绝。

上述七项必须由独立test method/fixture直接断言；四象限循环、schema循环、aggregate runtime count与broader suite
结果不能单独作为这些行为的覆盖声明。

完整 installer/upgrade/workflow-switch/multi-platform Release matrix 保持 deferred；broader suite 的既有失败必须
如实报告，不得通过越权同步 installed/platform bytes 将 C4 宣称为 production-ready。

Fresh finding-fix targeted evidence 为 task-lifecycle runtime `93/93`、Python compile、task validation、
`git diff --check` 与 touched non-generated file 单文件 line limit 均通过；task validation 将不存在的可选
`implement.jsonl`、`check.jsonl` 标记为 skipped。真实 common-dir 中 generation 2 binding 仍不存在，因此这些测试
没有写入 live task control state。此前 Preset Python suite 为 `85/86`，唯一错误是 raw apply clean-fixture 检测到
E434 前故意未同步的 installed task-lifecycle README/schema/registry sidecars；该 broader suite 未在本轮 narrow
finding-fix 重跑，也不授权同步 installed/platform projection。

RDT 与 Architecture current 已由 expected `.61` 串行提升为 `.62/active`。Independent Branch Review 绑定
`origin/main@77fa1a2...c7fab600` 且 P0/P1/P2/P3 为 `0/0/0/0`；promotion-created diff 必须 fresh 重走
Phase 2、Task Commit 与完整 Branch Review。C5-C7、D443、D436、E434、#434 activation 与完整 Release matrix
保持未验证。
