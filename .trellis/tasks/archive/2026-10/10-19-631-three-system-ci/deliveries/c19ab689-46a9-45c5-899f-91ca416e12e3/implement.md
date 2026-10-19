# 三系统 CI D1 实施与验证计划

## 1. 输入与引用

读取 [整体需求](../../prd.md)、本目录 PRD 与 design；来源技术承诺只由 design 第3节处置。必要规格为 clear-technical-writing、quality-guidelines 的 Test And Validation Value / Validation Scope Ownership、preset installer、upstream-ownership、docs/public-docs。实际 source lock 定位 `trellis/presets/guru-team/source/trellis-source.json`，构建沿根 README 当前来源段；不使用历史同版本 tarball。没有前序 Delivery。

## 2. 有依赖顺序的步骤与文件责任

1. 主会话完成 Author、Wording、Architecture final_plan、Approval 与计划展示，再由原 Activation 激活精确 D1。
2. Trellis implement 子代理负责 `.github/workflows/targeted-ci.yml`、`ci/`、`docs/ci/README.md` 和 README 导航。先读现有测试、installer 与源码构建入口，再实现单一驱动、测试 outcome、双目标隔离/继续、真实失败/报告/上传。保留所有并行改动；不能改产品 runtime 或 source lock 来使 CI 通过。
3. 子代理补必要的真实临时 Git 集成测试，验证驱动的正常目标选择、失败继续、原始结果和 summary。执行现有真实测试及新驱动测试，修正本次基础设施问题。不得添加防攻击、锁或额外故障注入测试。
4. 主会话与独立 Check 按完整候选检查，再 TaskCommit、独立全量 Review、Delivery Review。经原 Publish 发布 PR 后获取真实三系统运行。基础设施错误在本切片修复；产品失败按具体入口归 #630 并保持红色结果。
5. 合并 main 后验证正式 push 与手动两个 commit 对照；下载自然失败 artifact，核对三系统及目标继续、报告和未验证项。原 Completion/Closure/Finish 记录整体完成，独立归档 bookkeeping；不发布版本。

## 3. 验证入口、输入与预期观察

- V0：`python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p test_guru_platform_inventory.py`，已有11项执行；记录真实结果。
- V1：新驱动集成测试、YAML 解析、`git diff --check`；按 design V1/V4 验证正常失败不吞退出码及目标独立。静态不等于 Actions 通过。
- V2：真实 PR、main、workflow_dispatch 三入口。每系统 Ubuntu24.04/macOS15/Windows2025，Python3.12、Node22，Fork package manager 从目标 lock 读取；测试与 clean smoke 均尝试。AC1/AC2。
- V3：dispatch baseline=`71f432f22acc78df7194a818c27b8e467ceb3048`、candidate=实际已发布 D1 commit，driver=运行入口的真实 SHA。保留各自结果，不预设产品修复。AC3。
- V4：`gh run view <run> --repo castbox/guru-trellis` 与 `gh run download <run> --repo castbox/guru-trellis --dir <diagnostic-dir>`，核对自然失败的具体断言、原始退出码、候选及其他系统继续、artifact保留期。AC4。
- V5：文档说明及实际运行链接、产品失败定位、#630/#53、Agent/编码/解释器用例未验证边界。AC5/AC6。

本计划不宣称命令已经通过。首次本机 V0 的事实保留在会话，不用它替代原生运行。

## 4. 停止条件与适用回退点

依赖、runner、调用或上传失败阻塞基础设施验收；继续其余独立系统/目标并保留错误。新增产品修复需求不在当前范围，原 owner #630 承担；不覆盖失败样本。计划/范围/架构真实变化回最早受影响 owner。只修改本 Task 文件，不 reset/stash/清理其他 worktree。无业务部署或数据迁移，所以不造发布回滚协议；CI 问题用本分支普通修订恢复。

## 5. Delivery Policy（唯一）

full：D1 覆盖 R1–R8、AC1–AC6，没有本 Task 未分配的需求。交付条件是可运行 CI、真实目标身份和测试/安装结果、失败诊断及维护说明。产品失败按 #631 条款可保留，但基础设施自身必须正常。main 与 dispatch 证据只能合并后取得，属于整体 Completion 的必需证据；PR 合并本身不是整体完成。#630 和上游 #53 保留原缺陷修复与真实 Agent 验收，不构成本 Task 延期 scope。

## 6. Docs SSOT Plan（唯一）

strategy=ssot_first。本批 durable_paths 为 `docs/ci/README.md` 与 README 导航。实现 owner 先写清运行、依赖、报告与故障定位合同，再让实际代码和运行证据对齐同一正文。直接 consumer 是维护者和 #630 的回归接入方。现有 RDT current 的 Task/Delivery 语义不变，Architecture 独立评估为 no_architecture_impact；不改共享版本/导航或建立空 contribution/ADR。最终 Phase2 前由原 RDT owner reconciliation 判断上述无公共语义变化及新运维正文一致性；实际扩大边界时回原维护 owner。preset/workflow/overlay 产品文件不修改，故不要求重新应用 dogfood；clean smoke 是本 Issue 自己的原生验证，不宣称完整升级/Release Gate 矩阵。
