# #295 Design contribution

## Public contract migration

- `D295-01`: 保留 Sync synced 2.0、`base_current` 1.0 和 private sync result 1.0；Sync interface 的 consumer projection 只提供 Discovery 2.0 的确定性 seed，`change_input` 由 Discovery caller authoring，base facts只由 transition 提供。
- `D295-02`: 新增 closed Discovery pre-task input 2.0 与 aggregate active selector；旧 1.0 files 保持 immutable，active interface、consumer、eval 和 installation inventory只选 2.0。
- `D295-03`: 新增 owner-result 3.0 schema/example/runtime identity；`base_observation` 只包含 Discovery live consumer需要的 repo/locator/base/remote/branch/HEAD/clean/current fields，public output不投影它。

## Live observation and owner runtime

- `D295-04`: Discovery invocation先验证 public input 2.0 与 `base_current` schema、mode、continuation 和 stage，再解析 transition repo locator；任何后续 semantic authority read 均依赖此 precondition。
- `D295-05`: package-local observer通过 Git public commands读取 repo identity、symbolic branch、HEAD、local selected-base ref、remote-tracking ref、worktree inventory和clean status，不 fetch、checkout、merge或写 ref。
- `D295-06`: current observation进入 recorder/checker；正常 advance返回 `refresh_base`，结构/authority错误返回 `blocked`。Owner identity仅绑定 Discovery-owned base/head freshness，不保留 Sync private digest。
- `D295-07`: record/check/invoke 保持 AI semantic gate 与 deterministic validation分层；history preview、duplicate search、current-state和Clarify transition语义不变。

## Runtime, distribution, and evidence

- `D295-08`: installed transcript从 actual Sync wrapper获取 stdout，按 live interface projection加 caller-authored change clues构造 Discovery envelope，通过 production recorder/checker/public wrapper取得 actual `context_ready`，再按 interface投影到 Clarify。
- `D295-09`: targeted Python entry经 `runtime/launch.sh -> resolve-python.sh` 或声明 managed test launcher；PATH隔离只构造环境，不直接运行 product module判定 dependency。
- `D295-10`: canonical registry/package/consumer、workflow/preset docs、installer inventory、activation/migration、eval adapter和sidecar assertions同步；preset all-platforms apply只生成 managed projections，unknown local edit仍 fail closed。
- `D295-11`: validation分层为 package/runtime、actual public transcript、managed Python error matrix、canonical/installed/platform parity、reapply/drift/sidecar和一个 clean throwaway；不声称 release gate。
- `D295-12`: task-owned RDT/Architecture contributions保持 candidate；shared current仅在 committed full-diff independent review 后由 expected `.39` serialized promotion更新并触发 fresh gates。
