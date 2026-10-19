# 三系统 CI D1 需求

## 1. 整体来源与术语

整体 authority 为 [Task PRD](../../prd.md) 的 R1–R8、AC1–AC6。Direct Source 为 [#631 全文](https://github.com/castbox/guru-trellis/issues/631)，角色为要求。公共 scope_ref 绑定整体 PRD 的 sha256 revision，planning_root 为本目录。driver 指 CI 测试来源，target 指独立被测 commit；baseline/candidate 各有独立目标树和 clean 安装目录。

## 2. 整体与本批目标、非目标

维护者需要在没有 Windows 电脑时复跑原生兼容性验证。D1 完整交付三系统 CI 与对照报告，覆盖整体 R1–R8。排除产品兼容修复、上游解释器修复、全部 AI 平台矩阵、版本发布部署、分支保护、付费 Agent 凭据与实际 Agent 自动加载验收。

## 3. 本批起点、前序结果、依赖与剩余责任

没有前序 Delivery。起点是 main `71f432f22acc78df7194a818c27b8e467ceb3048`，当前没有 Actions workflow。依赖现有 unittest、preset installer、source-locked Trellis Fork 及 GitHub-hosted runner。首次验证须配置真实依赖，不使用本机已有安装。D1 完成后没有本 Task 未分配需求；#630 和上游 #53 保留自己的产品回归与验收责任。整体 Completion 还须核对 PR/main/dispatch 真实运行和失败 artifact，不仅看代码合并。

## 4. 本批调用方、场景与流程

- D1-S1：PR 或 main 修改本次运行时/安装/测试/依赖/CI 路径后，在三个原生 runner 执行候选测试和代表性 clean 安装，并逐系统输出结果。
- D1-S2：维护者手动提供两个实际同仓库 commit；driver 解析 SHA 后为 baseline 和 candidate 各自准备独立目标仓库，先基线再候选，基线失败不终止候选。
- D1-S3：真实测试或安装失败时，保存报告和退出码并上传已生成诊断；matrix 不取消其他系统。环境错误、产品错误、未完成分别如实说明。

## 5. 完整行为、条件与约束

自动入口覆盖 pull_request 和 push main；手动入口支持 workflow_dispatch。触发路径包含新增驱动、依赖和文档及纳入的 canonical runtime、installer、测试、workflow。

使用明确版本的原生 Windows/macOS/Linux 标签，记录实际镜像与 Python/Git/Git for Windows Bash、依赖、UTF-8/locale。每系统真正执行现有适用测试并尝试 clean 安装。测试行为由原测试定义，YAML 只编排。不能跳过失败或用 continue-on-error、expected failure、无条件成功掩盖候选失败。

两个手动目标分别报告解析 SHA、driver 身份、独立目标路径、命令、断言和原始退出码。可以使用新驱动检查旧目标，但不能把新实现复制进旧树。缺陷对照必须匹配指定断言；没有指定或没有命中时不能宣称复现/修复。依赖或无关报错不能算基线命中。

每个目标失败仍完成已有诊断写入；候选和基础设施非零均保持非零。取消、缺环境和未执行标未完成。artifact 保留期与下载命令在维护说明中给出，不上传完整环境或凭据。具体 Windows 解释器可见性、非 UTF-8 案例和真实 Codex 启动测试由 #630/#53 后续接入；本次只记录实际运行配置，不声称这些缺陷已通过。

## 6. 本批验收、验证方式与未决项

- AC1：真实 PR、main push 和 dispatch run 证明触发路径与入口。
- AC2：三个原生 runner 均执行真实现有测试与安装 smoke；基础设施正常，产品失败定位具体入口/断言与 #630。
- AC3：手动选择两个实际 commit，观察独立执行和身份/结果报告，不能预设对照结果。
- AC4：从正常失败 run 下载 artifact，定位具体断言；确认基线失败后候选仍执行、单系统失败不取消另两个系统，并核对原始退出码。
- AC5：维护者按文档可以选择测试、复跑、下载证据和查边界。
- AC6：保持 #630/#53 职责，真实 Agent 与具体缺陷未验证项单列。

当前无产品选择缺口；实现前确定的测试子集须有源码行为依据，真实运行后再报告通过/失败。

## 7. Canonical 引用与本轮差额

整体要求由本 Task PRD 与 #631 定义。`docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md` 定位 current RDT；本次新增 CI 运维能力，不改变 Task/Delivery 公共合同。`docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md` 约束职责与最小必要复杂度，候选由原 Architecture owner 独立评估。`.trellis/spec/workflow/quality-guidelines.md` 的 Validation Scope Ownership 限定本次三系统定向验证；不扩成累计矩阵。后续 design 第3节记录来源技术承诺的唯一处置。
