# 三系统定向 CI 整体需求

## 1. 来源与术语

Direct Source：[castbox/guru-trellis#631](https://github.com/castbox/guru-trellis/issues/631)，完整正文的实施范围、职责、验收与边界均为要求。#630 是产品兼容性修复 owner；castbox/Trellis#53 是上游解释器命令修复 owner。两者只作为必要职责引用，不把其修复加入本 Task。baseline/candidate 是独立被测 commit；driver 是执行测试的 CI 来源 commit。产品测试失败与 CI 环境/执行失败须区分。

## 2. 背景与问题

维护者没有本地 Windows 环境。当前仓库没有 `.github/workflows`，无法从 Guru 仓库取得原生 Windows、macOS、Linux 的持续测试和安装证据。已有 unittest、preset installer 与 focused 安装验证能力可复用，但本机或 fixture 结果不证明三系统实际运行。

## 3. 目标与非目标

交付可运行的原生三系统 CI、独立 commit 对照和失败证据读取能力。整体完成包含真实 PR、main 和手动 Actions run 的入口验证。

不修复 #630 产品问题，不代替上游 #53，不承担全部平台/历史版本/installer 组合的 Release Gate 矩阵。不发布版本、部署或配置分支保护。不修改 Guru AI 判断或业务 Task 状态。没有付费 Agent 凭据要求；脚本/hook 不证明 Agent 自动加载。攻击模型、竞态压力、锁协议和额外 fault injection 均不在范围内。

## 4. 真实调用方、场景与流程

- S1：PR 作者修改本次 runtime、installer、测试、依赖或 workflow；自动运行候选定向检查，并分别得到三系统结果。
- S2：维护者合并 main 变更；同一自动入口验证正式 main，不因触发路径遗漏跳过。
- S3：维护者手动提交同仓库 baseline/candidate commit；分别解析真实 SHA，在独立目标仓库执行，用同一明确 driver 报告两个目标。基线失败后仍执行候选；不预设一失败一通过。
- S4：测试或安装自然失败；保留命令、报告、原始退出码和可下载诊断。一个系统失败不取消另外系统。取消或环境不可用记未完成。

## 5. 行为要求

- R1：PR、main push 和 workflow_dispatch 三种入口，触发覆盖本次纳入的全部 canonical runtime、installer、测试、依赖及 workflow 路径。
- R2：使用明确 OS 标签的 GitHub-hosted 原生 Windows、macOS、Linux。记录实际镜像、Python/Git/Bash、依赖版本及 UTF-8/locale 设置。Windows 使用原生 Python 和 Git for Windows Bash。依赖与安装步骤可复现，不依赖本机隐藏状态。
- R3：每系统执行当前适用的最小可靠现有真实测试，并实际尝试一个代表性 clean 安装 smoke。按行为选择用例，不静默跳过失败，不用 continue-on-error、无条件成功或 expected failure 把候选缺陷改记通过。不把断言复制进 YAML。
- R4：手动支持同仓库两个 commit。记录解析 SHA、driver 身份、独立目标路径、命令、断言和退出码。旧目标缺测试时可使用候选驱动，但不能混入候选实现。PR 自动只跑候选。只有具体缺陷断言匹配且候选通过才报告失败/修复对照成立；依赖失败或无关报错不是复现。
- R5：保留 Windows 定向案例未来接入边界：控制解释器可见性时使用真实解释器/launcher 并验证子进程解析；不能由 runner 其他 Python 掩盖“仅 python3”或“仅 py -3”。编码案例不能被默认 UTF-8 掩盖。具体案例由 #630/#53 接入，本次不虚报已验证。
- R6：matrix 不 fail-fast；基线失败不跳过候选。每个目标保留原始退出码和真实汇总，区分已命中指定基线缺陷、候选失败、环境/执行失败。候选/基础设施失败不能被基线预期失败抵消。
- R7：普通失败也上传已有脱敏命令、报告、目标/driver 身份、实际依赖版本及必要差异。说明 artifact 保留期与下载方式，不上传凭据、私有数据或完整环境变量。取消、未执行、缺环境不能声明通过。
- R8：维护说明覆盖自动触发、手动重跑、定向选择、定位和读取证据；给出三系统真实 run、artifact 与未验证边界。

## 6. 约束与依赖

复用现有测试和依赖约束。CI 基础设施独立完成不依赖 #630 修复；真实产品失败保留非零并定位到入口/断言和 #630 对应项。runner、依赖、调用配置等基础设施失败仍阻塞本 Task，不能转交 #630。未编写缺陷专属回归列待接入，不用空 job 或整体跳过替代执行。

WSL、模拟 platform、mock subprocess 仅辅助。真实 Agent 验证仍由原缺陷 Issue 承担；Windows + Codex CLI 的付费凭据与实际自动加载不在本 Task 验证范围。无数据库、业务数据模型或 schema migration。

## 7. 可观察验收与验证方式

- AC1（R1）：实际 PR、main 和 dispatch run 链接证明入口及相关路径覆盖。
- AC2（R2/R3）：三系统各有现有真实测试执行和 clean 安装尝试，runner/依赖/调用/退出码/上传正常。产品失败定位具体入口/断言及 #630 项；基础设施失败或未执行不满足。
- AC3（R4）：手动指定两个实际 commit，报告各自 SHA、driver、独立目标、结果。即使相同也保留，明确是否满足指定缺陷失败/修复对照；不要求制造已修复产品案例。
- AC4（R6/R7）：正常失败 run 的 artifact 可下载且定位具体断言；基线失败后候选仍执行，单系统失败不取消其他系统，保留原始退出码。无需额外故障注入。
- AC5（R8）：无 Windows 电脑的维护者可按说明重跑，查三系统 run/artifact 和未验证项。
- AC6（R5/职责）：#630 与上游 #53 的具体缺陷与 Agent 验收保持原 owner，不因本 Task 完成而宣称通过。

本节定义期望，不是已通过结果。

## 8. 实际未决项

没有阻塞需求选择。测试子集和依赖细节由 Delivery Author 按当前源码细化；原生执行后的产品失败按实际结果归类，尚未执行前不预判通过。
