# D3 安装采用实施计划

## 1. 输入与引用

读取整体 PRD、当前需求、设计第3节、私有发布合同 Stage 1 及 canonical `guru-upgrade-tools` 合同。源为 #926 已交付干净提交 `b77923c4`，匹配 Fork 是 source lock 验证的 `0.7.0-castbox.6`。

## 2. 步骤

1. 在 canonical source 运行原 `preview.sh`。核对目标、正式源、平台、managed preimage、用户文件、peer 和保留范围。
2. 根据 preview 回执和核对后的目标状态，按 canonical `guru-upgrade-tools/references/contract.md` 的 Forward behavior 编写 `private-prepare` 输入。调用一次 `prepare.sh`，取回 `result.plan`。
3. 展示实际目标、源码、写入和删除集合。按原工具合同把冻结的 `result.plan` 原样交给 `invoke.sh`。部分完成时使用同一事务的恢复引用。
4. 读回最终状态并执行验证。仅提交实际安装涉及的受管投影和正式 Task 规划，先独立审核，再以 `Refs #924` 交付。

## 3. 验证

- V1：原 tools owner source_locked invoke 及 target native 验证。核对结果 .12、无 formal_fork_source_lock 限制、选定工作区和安装来源。
- V2：目标 `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json`，canonical ownership、`check-dogfood-overlay-drift.sh --repo .`、本会话 continuation。核对受管文件、用户配置和 Task 保留事实。
- V3：验证 actual manifest、目标 CLI、源锁、无新增 `.new/.bak`、`git diff --check`。安装和源码身份以实际已验证目标为准。

## 4. 停止与恢复

未完成的安装只能从原 tools 事务接续。确认预览发现的 `.trellis/config.yaml` 可保留，若出现必要文件冲突或源变更，回原 owner 刷新，继续保留原操作事实。

## 5. Delivery Policy

`staged`。当前交付 AC02，是最后一个准备业务切片。AC01 和 AC02a 已合并。合入真实安装后进入整体 Completion、Closure 和 Finish。发布候选、tag 与 Release 由后续发布阶段负责。

## 6. Docs SSOT Plan

`no_docs_update_needed`。分发、安装、恢复和 Task 保留的现行 RDT 与 Architecture 定义继续适用。本批交付现有文档和工具的实际受管投影。
