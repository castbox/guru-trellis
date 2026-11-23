# #917 合并通知的 RDT 隔离贡献

归属 Task 917-reconcile-merge-notification，generation 0，Delivery f24d99c7-b46a-4234-a5cd-e91c93c17fbb。固定起点 8604558695dfd9d8ea2181406a87ece70d9eea63，集成目标 main。来源为 [Issue #917](https://github.com/castbox/guru-trellis/issues/917)。

proposed 目录保留三份完整拟案，文档内相对引用以实际目标为起点。保留原 RDT 单元身份，承接 R917-01 → D917-01 → T917-01 至 T917-03。运行条件由原编排正文和 workflow 承接。原 RDT 负责人在工程验证后整合并回读当前完整单元。

## 工程验证观察

以 Codex CLI 0.167.0、deepseek-v4.1-flash/high 在隔离载体运行三个场景。四个实际 Agent 进程均正常退出。三个 Git bundle 均可重跑。所有场景的起点为 `44e4806a74d54d049c2baef8494495e1d8b0dd97`，固定候选为 `5ee0d28752a57cb785476600185cca82c085a20e`。运行方法及证据文件说明见源私有验证正文。

| 范围 | 实际观察 |
| --- | --- |
| T917-01 | 隔离协调 Agent 读到同仓合并，核对真实 Git 无冲突。两次参数错误后完成核对，实际派发保留条件原文、原候选和已核对事实，并要求继续原审核。 |
| T917-02 | 隔离执行 Agent 先审查固定差额，直接收到通知后继续使用原候选和适用证据。真实 Git 核对无冲突，轨迹没有 Reconcile 调用。 |
| T917-03 | Git 报告 `report.txt` 内容冲突。执行 Agent 固定目标 `8e1fedee2074cbb49117bb5d3323b336b6474399`，调用原 `execute-base-candidate.sh`。原入口返回 `merge_status=conflicted`，场景在该调用后结束。 |
| 定向分发 | 源包和 ownership 检查通过。配对 Trellis CLI/Core 0.7.0-castbox.6 的隔离安装、重应用及 installed 包校验通过，三平台检查未发现 .new 或 .bak。Task worktree 的工具更新在公开写入前被另一已注册 worktree 的 Python 选择指针变化阻塞。当前 dogfood 检查只报告两份受管正文仍不同。 |

GitHub 合并事件和应用消息使用隔离载体。结论覆盖本地 Git 和真实隔离 Agent 的动作。实际应用、业务仓采用及完整升级与 Release 测试属于其各自验证。

同一 Task 的受管更新随后按当前合法 peer 状态重新准备并完成。两份 dogfood 正文与 canonical 源码逐字一致。选定平台及受管分发漂移检查通过，未发现 .new 或 .bak。该工具更新验证采用本地候选模式，正式 Fork 源锁仍属未验证。
