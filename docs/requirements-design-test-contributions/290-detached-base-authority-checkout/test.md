# #290 Test contribution

- `T290-01`（AC-01/02）：显式与 config scalar `release/1.3.0` 在 clean `main` 存在时
  仍绑定 release authority。
- `T290-02`（AC-03）：ordered `dev -> main` 选择 `dev`；移除 dev checkout 后 blocked，
  不回退 main。
- `T290-03`（AC-04）：detached session + clean registered authority 返回 `synced`，
  handoff/transition locator 均为 authority root。
- `T290-04`（AC-05）：missing、dirty 与 inventory HEAD/branch/ref identity mismatch
  分别 fail closed。
- `T290-05`（AC-06）：invocation checkout 自身绑定 selected base 的既有 wrapper 场景
  继续通过。
- `T290-06`（AC-07）：remote advance 只前进 authority checkout，detached session HEAD
  不变；runtime source 只含 explicit fetch、ancestor probe 与 `merge --ff-only`，不含
  checkout/switch/branch/worktree-add/reset/rebase/stash mutation。
- `T290-07`（AC-08）：既有 schema examples、digest、三个 typed exits、public synced
  schema 与 transition equality assertions 全部通过；schema/interface bytes 不变。
- `T290-08`（AC-09）：package contract/runtime/eval、source/installed package、dispatcher/
  schema/manifest regression、canonical/dogfood/platform parity、preset reapply/drift/mode
  全部通过。
- `T290-09`（AC-10）：installed Codex wrapper 从 detached session 调用，输出 authority
  locator 与 fresh three-way equality；不执行 #267 多平台 Release Gate。
- `T290-10`（AC-11）：recursive `.new`/`.bak` 与 unknown sidecar scan 为零。
- `T290-11`：真实 main/develop/detached 三个 registered worktree 验证 porcelain-z parser
  得到三个独立 record，branch/detached field 不跨 record 混合。
- `T290-12`：workspace consumer package 独立验证 ordered `dev -> main` provenance；
  sync-base detached ordered fixture 把真实 `transition.base` 直接交给该 consumer，并断言
  `fresh=true`、`three_way_equal=true`。
- `T290-13`：config 选择 `dev`、producer 由 explicit `--base-branch main` 选择 `main`
  时，workspace consumer 以 explicit assertion 接受 `main` provenance，不被低优先级
  config 重选覆盖。
- `T290-14`：config scalar 为空且所有 configured candidates 不存在时，producer 与
  workspace consumer 均以 remote HEAD 的 `main` 作为 `remote-default`，完整 candidates
  provenance 和 freshness equality 通过。

证据层级遵循 `DES-008`：两个 package 与 producer-to-consumer test 证明 resolver 和
freshness continuity，installed wrapper 证明
Codex projection normal path，reapply/drift/sidecar 证明 managed distribution；这些证据不
声明 release-wide compatibility。
