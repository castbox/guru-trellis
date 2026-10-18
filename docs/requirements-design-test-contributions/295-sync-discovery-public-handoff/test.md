# #295 Test contribution

- `T295-01` (`R295-01..03`): Sync contract/assertions证明 synced 2.0 与 `base_current` 1.0 bytes/shape不扩张，Discovery active input只选择2.0并拒绝mixed legacy input。
- `T295-02` (`R295-03..05`): actual Sync wrapper stdout经声明 seed + caller change clues进入Discovery public wrapper；输入、transition、mode和continuation exact binding通过。
- `T295-03` (`R295-04..06`): owner-result 3.0 schema/runtime覆盖current observation，并静态断言active owner/checker不存在Sync private result、`base_sync_facts_sha256`或private schema definitions。
- `T295-04` (`R295-05..06`): clean current authority返回 `context_ready`；local/remote normal advance返回 `refresh_base`；dirty、wrong branch/ref、missing ref、repo mismatch和ambiguous worktree分别返回 `blocked`。
- `T295-05` (`R295-05..08`): observer在Issue/Docs/code/test/history read前失败，Git status、refs、worktree inventory、task/branch和protected pre-task paths前后零写入。
- `T295-06` (`R295-07`): installed transcript不存在 `base_sync_payload` 或同义 reconstruction，不调用 `sync-base.sh`/`check-base-sync.sh`，不 import Sync package runtime，并把actual Discovery output继续投影到Clarify schema。
- `T295-07` (`R295-08`): existing Issue、proposed draft、zero-history与no-impact路径保持通过；Discovery history/search预算和语义无扩张。
- `T295-08` (`R295-09..10`): PATH Python不能 import `jsonschema`时真实public wrappers和targeted tests经managed interpreter通过；missing/stale pointer、missing interpreter、dependency/inventory drift返回精确错误。
- `T295-09` (`R295-11`): source registry/interface/schema/runtime/package/eval、consumer和workflow marker验证通过，legacy assets存在但不进入active graph。
- `T295-10` (`R295-11`): preset all-platforms reapply后canonical、dogfood installed、Shared/Codex/Claude/Cursor bytes/modes/hash一致，ownership/drift/recursive `.new`/`.bak`/unknown sidecar为零。
- `T295-11` (`R295-11..12`): 一个representative clean throwaway完成marketplace/preset install、actual Sync->Discovery->Clarify、managed Python、update/reapply和final drift scan。
- `T295-12` (`R295-12`): task validation、JSON/schema、shell syntax、managed Python compile与`git diff --check`通过；完整 release/multi-platform matrix明确不在本次PASS声明中。
