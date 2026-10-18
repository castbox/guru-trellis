# #260 Requirements contribution

本 contribution 将 current source 的 official Trellis 目标从 `0.6.5` 提升到
`0.6.15`，并保持 `current-main-0.6.5-guru.36` 为不可回写的 superseded
历史。目标 current identity 是 `current-main-0.6.5-guru.37`；它不是 stable
tag 或 GitHub Release identity。

- `REQ-016`：兼容门禁必须从 live manifest、ownership、overlay 与 registry
  交叉派生平台，并对 `claude`、`codex`、`cursor` 形成 clean/existing 六个
  隔离 cell；`.agents` 是每个 cell 的 shared projection，不是独立平台。
- `REQ-017`：existing cell 必须以 immutable `v0.6.5-guru.10` / extension
  `0.6.5-guru.36` 为 before-state，经 official `0.6.5 -> 0.6.15` upgrade、
  update dry-run、条件式 migrate、workflow preview/switch 与 preset reapply。
- `REQ-018`：迁移前后 active Skill、interface、schema、exit、command、consumer、
  route、managed path、mode、template-hash 与 Docs authority 的完整投影不得出现
  未审查能力丢失。
- `REQ-019`：#263、#264、#265 installed contracts 与 #266 双 SSOT authority
  必须在升级后保持；`.trellis/spec` 仍是最小 projection。
- `REQ-020`：A/B compatibility fixture 覆盖 `worktree/github_pr` 与
  `current/none` 的隔离、双合并顺序、失败恢复和 cleanup reachability；真实
  GitHub A route 只能在单独副作用确认后执行。

未纳入：#248/#252 public owner 实现、stable tag/Release、#267、生产变更与
Trellis upstream source 修改。
