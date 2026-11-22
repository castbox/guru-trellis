# #883 D1：实施与验证计划

## 1. 输入与引用

读取 [整体范围](../../prd.md)、[D1 PRD](prd.md)、[唯一来源处置](design.md#3-来源设计处置)、[设计 §4–§8](design.md) 和 [#883](https://github.com/castbox/guru-trellis/issues/883)。首个 Delivery 无前序。B 为 `8b92022d6cdf8f9debda09ed68602f1d137e3629`，后续 PR 目标为 `main`。

## 2. 依赖顺序与文件责任

1. 激活后在同一专用工作树内复用 DAG 的源私有测试目录 `trellis/skills/guru-team/packages/guru-orchestrate-issue-dag/tests/`，整理同轮观察、已有委托、失效注册和 Issue 正文修订场景及运行说明。沿用真实 Codex 进程、原 MCP 事实载体和 provider 投影。主持者控制 B 结果可读时点，保留完整事件、原始首失败和缺证口径。
2. 在 canonical `trellis/presets/guru-team/spec/workflow/issue-orchestration.md` 明确具体确认、局部暂停和同轮观察的顺序。同时加入两项免单独确认判定。DAG Skill 与本地合同只引用共享正文；不在 Sequence 或原 Issue owner 复制新判定。保留原会话委托、失败策略和写权限。
3. 通过原安装 owner 同步受管文件。已有正式 Task 的检出由 `guru-upgrade-tools` 按当前 source/location 合同保留 Task 和会话。使用完整候选资产和匹配 CLI/Core；提交前若只能走隔离开发 `local_candidate`，报告正式 source-lock 未验证，由原 owner 在明确写入边界内执行。无完整匹配源先取得该源；不手工覆写投影。核对 reapply、mode、sidecar 和 drift。
4. 执行 V1–V6。由原 Architecture 和 RDT owners 在 TaskCommit 前整合并回读实际差额。后续本地 commit、Branch Review、Delivery Review、Publication 均保留原门禁。到达实际合并前停下并报告确切 PR、预期 head 和合并操作。

## 3. 验证入口、输入和预期观察

- V1：使用 `python3 trellis/skills/guru-team/packages/guru-orchestrate-issue-dag/tests/run_native_orchestration.py` 的源私有场景入口，现行 provider 用 `--source-ref 8b92022d6cdf8f9debda09ed68602f1d137e3629` 固定，候选用完整匹配投影。场景与设置保持相同（`codex-cli 0.167.0`、`gpt-6-luna`、`high`）。各轮使用未占用的外部输出目录。对照 [设计验收](design.md#8-验证设计) 实际事件；运行中不发送用户回复。
- V2：同一公开入口运行委托覆盖场景。核对真实通过原 owner 的指令、执行和回读，不以输出文字替代。
- V3：核对现有恢复与受影响共享消费者；只在变化触及恢复时补实际样例。保持原 Sequence 串行约束。
- V4：运行 `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json` 与 `--mode installed`、`trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`、定向 Python 语法检查及 `git diff --check`。按实际安装路径回读适用 reapply、mode、sidecar。实际 Agent、工程和投影证据分别报告；App 原生、真实远端效果与完整升级矩阵不在本批证明范围。

- V5：为隔离 Git common-dir 建立可复现的缺目录注册，用原 Task 创建入口观察真实阻塞。使用同参数的 Git preview 和严格清单事实。真实协调者及原执行者须无单独确认地核对、执行并回读，再接续同一节点。若 preview 多出条目，不执行并重新核对。所有 fixture 资源与本机八条记录隔离。
- V6：为隔离 GitHub 事实构建完整旧正文、精确目标正文、固定基线上的已定标识和正常 source action。由真实 child 按已有 `issue_body_edit` 的原闭环处理，并追踪受影响的 Readiness 刷新。保持真实 #1944 只读，正常正文变化用真实读取时点表现，未决取舍不能被不冲突证据替代。

## 4. 停止条件与回退点

身份、scope、来源或机制变化时回原 owner。确认请求、B 可读时点或轮次边界缺失时，保留轨迹并定向核对载体，不能宣称通过。所需真实 Agent 与工程证据齐备即停止扩展验证。无数据迁移或特殊回滚；受管文件恢复走原安装 owner，实际会话中断后先回读原身份与副作用结果。

## 5. Delivery Policy

**full。** D1 承接 AC1–AC4 和 R3，交付前完成对应真实 Agent 验证及适用的工程检查。没有留给后续 Delivery 的计划内工作。整体 Completion 在实际向 `main` 交付后按原 Task-wide 门禁判定。

## 6. Docs SSOT Plan

**delta_first。** 原 `guru-maintain-requirements-design-test-ssot` owner 维护 [Requirements](../../../../../docs/requirements/current/issue-orchestration.md)、[Design](../../../../../docs/design/current/issue-orchestration.md) 和 [Test](../../../../../docs/test/current/issue-orchestration.md) 的当前完整定义，分别承接授权分支、两项局部解阻、消息到观察的衔接及各场景的实际验证方法。实施先形成独立拟案。原 owner 在 TaskCommit 前整合、回读，供同一次 committed Review 检查。[架构贡献](../../../../../docs/architecture/contributions/883-dag-local-dispositions/contribution.md) 按 `target_native` 处理单一职责变更和必要 ADR。原 Architecture owner 在提交前整合实际完整定义及 ADR，回读供提交后独立审核。不登记共享导航或加载第二运行规则。
