# #330 Test contribution

- `SCN-024`：去敏 #118 fixture 固化 Commit 14、Publication 35、Finalizer 23 次历史命令观测、
  1,188,000 ms 外部 CI 等待、非默认 `dev` closure mismatch 与 terminal 后继续调用。
- `SCN-025`：四个 package 各只有一个 recommended facade validator，legacy commands 仍注册；
  source/installed package contract、command graph、wrapper executable mode 与 public projection 一致。
- `SCN-026`：Commit 覆盖 success、hook failure、dirty/staged drift、unrelated preservation、active
  Git operation、candidate freshness 与 stdout-loss recovery，成功路径只 prepare+invoke。
- `SCN-027`：Publication 覆盖 ready、metadata-only revision、content/durable drift、external
  blocker 与 ledger mismatch；同 invocation 的 record/check/projection 只建立一次完整 snapshot。
- `SCN-028`：Finalizer 覆盖 ready、provenance tail、same-plan reprepare、publication stale、existing
  PR adoption、stdout-loss recovery 与 changed-plan reconfirmation；无新选择的完整读取/调用由 5 降至 1。
- `SCN-029`：Merge 覆盖 checks pending/success/failure/head change、base/policy/mergeability drift、
  default/non-default/refs-only closure、mutation-output recovery 和 terminal cleanup；禁止 `gh run watch`
  与 Agent polling 叠加，terminal 后 operation count 为 0。
- `SCN-030`：共享 integration fixture 断言 command invocation 至少下降 50%、重复完整读取至少
  下降 70%、typed exit/DTO/mutation order/recovery lifecycle 等价。wall-clock 只输出观察结果。
- `SCN-031`：preset initial/reapply、dogfood zero drift、旧 installed compatibility 与一个代表性
  clean installed/throwaway closeout Happy Path 通过；完整 release matrix 明确不计入本 task。
