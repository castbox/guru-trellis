# #468 需求增量

状态：`candidate`；strategy：`delta_first`。继承 `current-main-0.6.17-guru.80 / active`，不替代三个 `docs/**/README.md` 指向的 current authority。
唯一来源：[live Issue #468](https://github.com/castbox/guru-trellis/issues/468)，本轮读取 `updated_at=2026-10-09T18:55:52Z`。
本增量按任务已审规划承接 #454、#434/#435、#436、#464；不重建其 source、lifecycle、Completion、Closure 或恢复机制。

| Requirement / behavior | 来源场景与结果边界 |
| --- | --- |
| R468-01 / BEH468-SOURCE | 场景 1/2/11/15：唯一 portable Direct Source 或合法 no-Issue；执行仓库、协调链接、Related Work、Follow-up 不产生 source 或拓扑 authority。保持 exact_source/reference_only/follow_up/parent 的既有含义。 |
| R468-02 / BEH468-DEPENDENCY | 场景 3..10：current owner 重读实际需求与明确必要外部事实；实质修订回最早受影响 owner。纯信息变化和未同步协调变化不自动失效；scope 外 Follow-up 不阻塞 Completion。缺工作或证据消费既有回程。 |
| R468-03 / BEH468-REPLAN | 场景 16：current 活动重规划获批、展示并在当前对话接受后正式恢复执行；原 TaskId/generation/branch/checkout/in_progress 不变。首次 activation 与真实首次输出丢失恢复语义保持；正常上下文丢失使用唯一 continuation 和原 producer/recovery，不持久化接受。 |
| R468-04 / BEH468-LIFECYCLE | 场景 12/13/14：no-Issue 保留原生命周期；Issue 重开按 active、未完成 closeout、正常完成 archive 分流。Completion 检验实际适用长期 SSOT 的必要更新或有依据的不适用，不强加统一 Baseline 类型。 |
| R468-05 / BEH468-DISTRIBUTION | 专项验收：canonical、dogfood、installed、声明平台投影及适用 reapply/drift/sidecar/mode 同步；精确说明观察层与未验证边界。 |

上游实现不证明 Backend #148 安装或业务重试。Production、官方 init/update 全链、远端候选安装和完整 Upgrade/Release 多平台矩阵仍归独立 owner。本贡献不新增项目拓扑、第二 source、第二 Completion owner、授权字段或跨 Skill digest 链。
