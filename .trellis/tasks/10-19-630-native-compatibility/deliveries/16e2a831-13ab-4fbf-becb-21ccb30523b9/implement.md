# D1 实施与验证计划

## 1. 输入与引用

读取整体 Task PRD 和本批 PRD、design 全文。来源处置只由 design 第3节维护。本批命中 #630 的 CI 精确选择与底层失败诊断；docs/ci/README.md 为直接维护合同，quality-guidelines 的 Test And Validation Value/Validation Scope Ownership 为测试范围。起点为 main `0543731bf52aa80842fde5db47332380de513cf0`，无前序交付。

## 2. 有依赖顺序的步骤与文件责任

- I1：CI implement worker 负责 ci/unittest_report.py 及其真实加载回归；先验证现有包外选择缺口，再新增 file::selector，保留旧入口结果。
- I2：同 worker 负责 ci/runtime_diagnostic.py 与直接相关测试；加载目标原 bootstrap_check 和实际依赖环境，观察固定 capability wrapper，不改变产品 argv/输入/encoding/返回行为。
- I3：I2 后接入 ci/targeted_ci.py 的原目标生命周期与 artifact，保持独立 baseline/candidate 和安装尝试；collector 错误、产品观察与安装状态分开。
- I4：主会话更新 docs/ci/README.md；独立 Check/Architecture reviewer 读取完整候选，完成定向验证与设计符合性审核。若需要改产品 runtime/source-lock/hash，回后继 Delivery 或原规划 owner，不扩张本批。
- I5：精确提交、完整 committed Review、Draft PR/原生 CI、Ready/Merge。原生诊断结果可作为后继修复证据；整体 Issue 保持打开。

## 3. 验证入口、输入与预期观察

V1/V2：`python3 -m unittest discover -s ci -p 'test*.py' -v`，并由真实子进程运行 unittest_report 的 file::selector、旧文件/模块、缺方法/import 错误案例。通过条件为选择与报告满足 DA1/DA2，不以用例数量代替语义检查。

V3/V4：原 `.github/workflows/targeted-ci.yml` 的 PR 或 workflow_dispatch，在 ubuntu-24.04、macos-15、windows-2025 运行。每个目标保存 driver/target SHA、OS/Python/Git/Bash、诊断 JSON、原返回码和安装日志。原生 fixture 失败也须保留真实底层输出。现有 Windows 产品安装失败不能被记为本批产品已修复；本批必须证明 diagnostic collector 和精确选择本身可用。

V5：核对 docs/ci 的新语法与 artifact 位置；不声明 Agent 启动、完整上游集成或 Release Gate 已通过。无 product/preset 改动，因此本批不跑完整 throwaway 发布矩阵或更新 dogfood；若实际写集变化，回原 owner 重新判断。

## 4. 停止条件与适用回退点

缺少目标依赖/Bash/资产则记录真实环境缺口，不填诊断通过。诊断入口改变目标调用或覆盖失败时修复本批设计/代码。首偏差证明需要产品修复时形成后继明确候选；不改全局 npm、node_modules 或上游文件。保留并行工作区内容。源码可在本分支正常返工；本批没有业务数据/DB 迁移，无需创造生产回滚协议。

## 5. Delivery Policy（唯一）

Policy=partial。本批独立交付：包级文件+用例选择和复用原 CI 的固定 runtime capability 诊断。可交付条件为 DA1–DA5 满足，三系统取得真实诊断记录，且既有产品失败和证据边界如实保留。

剩余责任属于同 Task 后继 Delivery：两个参考提交逐项处置，路径/URI/编码/跨进程传输/解释器/换行修复，固定上游 .5 集成，三系统完整产品回归和 Windows Codex 实际会话。Task Completion 仍须整体 AC1–AC10 满足并完成正式发布；D1 合并只证明本批，不关闭 #630，不将整体工作移交 #631。

## 6. Docs SSOT Plan（唯一）

Strategy=delta_first。本批实际差额是 CI 选择语法与诊断证据读取，由 docs/ci/README.md 的主会话 writer 维护，直接 consumer 为 CI 维护者和后继修复者。原 guru-maintain-requirements-design-test-ssot 在最终 Phase 2 前判断该操作文档 delta 的收敛；不为无 lifecycle 行为变化制造空 RDT contribution 或新 current version。Architecture 仍由原独立 owner 评估/必要时晋升；no-impact 时不制造 contribution/ADR。整体 runtime、installer 和 source-lock 文档差额由后继产品 Delivery 维护。
