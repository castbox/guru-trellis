# Sub-agent inline exemption

## 背景

本任务默认使用 Guru Team `sub-agent` mode。用户已确认 planning artifacts 后，主会话连续派发三个 `trellis-implement` 实现代理：

- `019f461b-9b1c-7a31-8d6e-252da463d78e`
- `019f4620-10c3-7442-a504-d491f5a8bcc5`
- `019f4625-c9d3-7c50-88f0-518a885d3172`

三个代理均在等待窗口内没有可见 task/source 进展，收到一次状态请求后仍无状态响应，并由 `check-subagent-liveness.sh` 返回 `stale_allowed`。主会话已按 workflow 记录：

- `stale-assessed`
- `terminated-unfinished termination_reason=stale_cutover`
- replacement-started recovery chain

## 降级范围

为避免任务永久阻塞在不可用的实现代理执行面，主会话在当前 worktree 中接管 Phase 2 implementation 写文件工作。

该降级只覆盖实现写入，不覆盖 Phase 2 check、Branch Review Gate、commit、push、PR 或 issue close。后续仍必须由独立 `trellis-check` / channel `check` 执行 Phase 2 check，并由后续 Branch Review sub-agent 执行最终 review。

## 证据边界

- 前三个实现代理没有任何实现输出可作为 pass evidence。
- 主会话 inline implementation 必须记录为 task-local evidence，并在 `agent-assignment.json` 中闭合前序 stale recovery chain。
- `phase2-check.json` 只能在独立 `trellis-check` 完成后由主会话记录；不能用本文件或主会话自检替代。
