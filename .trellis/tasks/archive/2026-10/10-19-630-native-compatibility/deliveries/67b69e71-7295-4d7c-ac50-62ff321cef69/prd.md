# D3 Python 与路径脚本验收收敛

## 1. 整体来源与术语

本批为 Delivery 67b69e71-7295-4d7c-ac50-62ff321cef69，沿用已公开修订的 Task accepted_scope，定位整体 prd.md 第4–7节的 S5、AC7、AC10。

| 来源 | 角色与用途 |
| --- | --- |
| https://github.com/castbox/guru-trellis/issues/630 的 CI职责、验证范围与当前状态 | 当前要求；Python runtime、目录脚本和公开 wrapper 足以承担本任务验收，不要求真实 Codex/Agent 会话 |
| 本 Task 根 prd.md | 整体范围；保留路径、URI、编码、解释器、换行、安装与维护行为 |
| PR #634、#639 及其公开 Delivery 结果 | 已交付事实；沿用成功验证，不重做产品或采集器 |
| docs/requirements/current/native-compatibility.md 的 R630-06；docs/design/current/native-compatibility.md 的 D630-06；docs/test/current/native-compatibility.md 的 T630-08 | 当前受影响完整定义，需同步已变更验收边界 |
| docs/requirements-design-test-contributions/630-native-compatibility/test.md | 唯一实际证据 owner；保留原始失败，不将未完成的 Agent 会话改写为通过 |

脚本执行只证明 runtime 与脚本能力。真实 Agent 会话保持独立未验证事实。

## 2. 整体与本批目标、非目标

整体目标仍是三系统路径、编码、解释器与受管文本安装兼容。本批只将文档和验收统一到 Python runtime、目录相关脚本及公开 wrapper，删除实际 Agent 会话的完成阻塞条件。

不改产品 Python、collector、workflow、runner、模型预算或公共 Skill 接口；不运行 GPU、模型或新的三系统矩阵。不执行官方版本发行、tag 或 Release，不写生产业务数据。

## 3. 本批起点、前序结果、依赖与剩余责任

D1 已由 PR #634 合并，结果 delivery:80413052748afecc65622a38cab283aba69352bb。D2 已由 PR #639 合并，结果 delivery:b470580d4f79f61c66d72db97861fe1564b5e746，其 head 为 cf07d082c046b8e5e3c5050a603f22285821b215。D2 PR CI 39284953290 三系统成功。

D1 原生产品、安装与维护证据及 D2 已成功的14项直接回归继续采用；本地9B完整流程仅为 macOS 模型探测，不证明 Windows Agent。Windows run 39285077678 的600秒超时保留为未完成观察。

本批依赖当前源 Issue 和已接受整体范围，不依赖模型或 OpenAI 账号。合并后仍需整体 Completion、Closure、Finish 和本任务资源精确清理；不以本批交付代替 Task 完成。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置、行为与观察 |
| --- | --- |
| DS1 阅读当前要求 | 维护者读取 Issue 与 Task；可确定命令行 runtime/脚本为必需范围，真实 Agent 不阻塞 |
| DS2 阅读当前 RDT 与 CI说明 | 实施与审核 owner 读取完整 native unit；要求、责任和测试一致，脚本通过不冒称 Agent 通过 |
| DS3 采用历史证据 | Check/Completion owner 读取唯一 Test；区分已成功三系统脚本、Windows会话失败与非必需观察，成功项不重跑 |

## 5. 完整行为、条件与约束

DR1：同步当前 R630-06/D630-06/T630-08 与 CI README，保留其余路径、编码、解释器、换行和安装维护条件。

DR2：保留 T630-08 的旧定义和失败历史可追溯性；当前义务明确撤销，不借用旧结果宣称新通过。旧定义通过 cf07d082 的不可变 Git 文件定位。

DR3：唯一 Test 增补 D2 实际合并、Windows CPU超时及本批验收范围变化；已有日志和历史叙述保留，当前状态与历史状态明确区分。

DR4：不新增推理或硬件机制。已创建但从未运行的本任务专用 runner/group 按精确身份清理，不接触默认或无关资源；清理与功能通过分开。

## 6. 本批验收、验证方式与未决项

| 验收 | 入口、输入与预期观察 |
| --- | --- |
| DA1 | 读取 Issue、根PRD与当前RDT完整单元；真实Agent会话不再是完成条件，其余runtime/目录脚本条件保持 |
| DA2 | 审核唯一Test与CI说明的实际diff；D1/D2交付、已有成功与Windows会话超时如实保留，无新增会话或GPU验收 |
| DA3 | 检查差异与范围；产品、CI工作流和collector字节不变，成功验证被采用，无重复工程验证 |

没有未决产品选择。文档一致性、真实证据适用性与完整差异由本批 Check/Review 实际判断，不预填通过。

## 7. Canonical 引用与本轮差额

本批仅修订 R630-06/BEH630-06、D630-06 与 T630-08 及必要来源/证据引用。R630-01..05、D630-01..05、T630-01..07 与其实际验证保持。RDT owner 定向同步当前完整定义，保留 cf07d082 旧义务定位；无需为文档收敛复制全局版本集。Architecture 当前 .103 与五项宪法原则继续适用；独立 Architecture 判断本批实际影响，不预建贡献或 ADR。
