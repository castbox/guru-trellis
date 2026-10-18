# #443 Task Identity Session Binding Design contribution

状态：`reviewed_promoted`。采用 `target_native`，关联 Architecture contribution `architecture-contribution-443-task-identity-session-binding-v1`，successor 为 `.57`。

- `D443-01`：`guru-bind-task-session` 是 lifecycle-aware bind/rebind/switch/resume/manual-recovery 的唯一 semantic owner 与 deterministic writer/validator；official Trellis task/session store继续拥有底层 identity 与 persistence。
- `D443-02`：public input 以五个 profile/route discriminator 对形成闭集；semantic AI Gate先选择合法 route，runtime 再执行 schema、identity、freshness 与 side-effect validation，脚本不生成语义判断。
- `D443-03`：resolver 组合 task.json identity、artifact locator、repository common dir、live branch/worktree/HEAD、base provenance、task/workspace mapping、session id 与 lifecycle generation。任何缺失或冲突返回 `binding_blocked`，不猜测候选。
- `D443-04`：resume/rebind/switch/reactivate 使用 official active-task writer；同一 identity 重试复用现有映射。manual recovery 只在 `allow_missing_mappings` 的受控分支写入既有 mapping payload shape，并在写后重新运行 boundary validator。
- `D443-05`：base provenance 只能来自 task metadata 或既有 mapping，不得从调用时 live base HEAD 反推历史边界；generation、current route 与 active-task identity 共同阻止旧 binding/receipt 跨生命周期复用。
- `D443-06`：public output 排除 runtime binding id、绝对路径、完整 live snapshot、authorization、semantic pass 与 recovery internals；五个成功出口和一个 blocked exit各自绑定独立 schema/example与唯一 consumer。
- `D443-07`：package、registry、manifest、shared/platform projection 与 preset reapply保持 additive；workflow integration 保持 deferred。#438 继续拥有创建期 attach，#436 owners继续拥有终态 lifecycle，#434独占 global route cutover。
