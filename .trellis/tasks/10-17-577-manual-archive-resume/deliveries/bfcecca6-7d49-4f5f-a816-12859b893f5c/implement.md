# D1 实施计划

来源处置、固定 B 和职责只读 [design](./design.md)；要求与验收读 [PRD](./prd.md)。

## Delivery Policy

策略为 `full`。D1 承担整体 R1–R7、AC1–AC6；没有隐藏的后继实现切片或剩余 accepted work。独立交付条件是 archive_resume 从 source-loaded 入口到目标 native 和下一实际 owner 完成，历史与身份保留、兼容/普通恢复通过，文档和受管投影一致。正式 Fork 采用、真实 CMS 恢复和 Release matrix 为来源明确排除的边界，不是本 Task 剩余工作。整体 Completion 由原 owner 在 D1 合并后逐项判断，不能以交付结果代替。

## Docs SSOT Plan

选择 `delta_first`。原 `guru-maintain-requirements-design-test-ssot` owner 维护 `docs/requirements-design-test-contributions/577-manual-archive-resume/{manifest.yaml,requirements.md,design.md,test.md,traceability.md}`，只有 test.md 写实际结果和未验证边界。实现和测试差额在最终 Phase2 前收敛；原 owner 串行晋升共享 Requirements/Design/Test authority。Architecture contribution 及其 expected-current promotion 归原 Architecture owner。Skills 引用 managed spec，不建立第二规则正文。

## 顺序与文件责任

1. 修改 canonical `trellis/skills/guru-team/packages/guru-maintain-legacy-task/` 的 closed profile/schema/example/interface、Markdown AI 合同及原 prepare/apply/resume/observe/finalize。公共任务只由 CLI/Core 写。checkpoint 消费公共 returned identity，原输出保持最小。
2. 原位修改 `trellis/skills/guru-team/runtime/maintenance_transport.py` additive capability/method；原六个私有 owner 的 legacy_maintenance 和其限定 schema/文案承接 archive 物理 source 与 original active attribution。保留 terminal 与未完成 closeout 边界，不由脚本作业务资格判断。
3. 在原 task_lifecycle identity、delivery adapter 和 Bind 的共享公开模块加载边界复用官方 current TaskId resolver。creation/history reservation 不改义；不改 `.trellis/scripts` 上游文件。
4. 同步 canonical workflow、两份 README、preset README、迁移说明与受影响 managed spec。使用原 apply.sh 同步本 worktree dogfood；逐项处理 sidecars，验证三平台/声明平台公开投影、installed runtime 和 drift。不得覆盖其它 worktree 或无关文件。
5. 执行下列定向验证与一个代表性隔离旧安装。若目标需工具更新，实际调用原 tools owner，单列工具写集；不改全局安装或 node_modules 源文件。当前 candidate 只用 local_candidate，核验 source/package/API，而不改正式 lock。
6. 收敛唯一 RDT Test 与 trace，执行独立 Phase2 Architecture/质量审查；原 Architecture owner 晋升已审差额后最终 Check。随后 Task Commit、不同独立 reviewer 对完整 B…H 的 Architecture/Branch Review、Delivery Review、Refs-only PR 发布/合并、整体 Completion/Closure/Finish/Cleanup。

## 验证计划

| 组 | 实际入口与观察 | 验收/缺陷检测 |
| --- | --- | --- |
| profile/transport | canonical 公共 preview/invoke 和真实 matching CLI/Core | 新 capability 可用；缺 capability/digest stale/source_locked 缺口写前阻塞，旧 profiles 不改义。AC3/4/6。 |
| private owners | 各原 owner inspection/freeze/retirement/restore，原路径控制+archive source | 源归属、原字节和 selected write set；Finish terminal/未完成事务保留；无关 controls 不变。AC3–5。 |
| current identity | 目标 installed Identity/C4/C3/Bind + 原生 continuation | 同 ID 原归档可读而 current 只选 active；真实 active ambiguity 仍阻塞；旧记录不可直接冒充 current。AC1/4。 |
| history/current work | 原 Publish/Merge 核验真实历史 PR/commit；执行 AI 调用下一 Guru owner | 保留历史与当前差额；scope补差进入Clarify/Planning或Completion evidence_pending；无空Delivery和旧pass。AC1/2。 |
| ordinary recovery | 同 operation重复/丢输出、普通已写前缀恢复及rollback | 同key/generation/历史一次；原写集、其它Task/session/checkout不变；后续业务改动阻止覆盖。AC5。 |
| representative installed | 一个隔离旧安装拓扑，原 tools owner + preset apply/reapply，目标原生/native-next-owner | 核验实际pair源码/构建/API及installed运行；不能用外部代执行或schema通过代替。AC1/6。 |
| distribution | source/installed package校验、声明平台投影、dogfood drift、sidecar、git diff --check | canonical与dogfood/installed一致；官方更新受管边界保持；不声称完整Release matrix。AC6。 |

采用最小可靠检查集。package regressions 包含旧活动convert/history_closeout、正式Reactivate/合法人工Cleanup、独立完整Plan2受影响边界。验证脚本不创建AI语义结论；实际代表样本的AI审查、native输出和下一owner结果由执行Agent解释。普通错误、stale/mismatch和部分写入来自受支持路径，不加伪造/攻击/锁/TOCTOU/压力或非常规crash测试。

## 恢复与停止条件

每批写入前运行官方 checkout boundary checker。scope、owner、持久化、SDK或兼容机制超出本设计时，在改代码/测试前返回调用级 candidate，交原 qualification/Architecture；不自行扩张。依赖缺失保留只读工作并报告具体原owner，不循环安装。维护操作使用其原 recovery_ref；普通开发修复留在当前阶段，不以新Task、替代generation或旧gate逃逸。
