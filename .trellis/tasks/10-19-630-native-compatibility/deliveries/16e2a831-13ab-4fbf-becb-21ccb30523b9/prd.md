# D1 原生失败诊断与包级用例精确选择

## 1. 整体来源与术语

整体 authority 为 Task 根 `prd.md` 及公共 accepted_scope。本批 Delivery `16e2a831-13ab-4fbf-becb-21ccb30523b9`，planning_root 为 `deliveries/16e2a831-13ab-4fbf-becb-21ccb30523b9`。

| 来源 | 章节与角色 | 本批用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/630 | CI 接入与验收 AC9–AC10；要求 | 补文件+用例精确选择；取得正常安装的底层返回码与输出 |
| https://github.com/castbox/guru-trellis/issues/631 / PR #632 | 已交付证据 | 复用 targeted-ci.yml 的三系统 runner、目标隔离和 artifact |
| 整体 PRD 第5–7节 | 全部行为与验收；要求 | 保留后继产品修复、三系统与 Agent 责任 |
| docs/ci/README.md | 当前 driver 使用合同 | 扩展选择语法，保留旧选择方式和失败语义 |

本批的诊断成功指观察并记录原始调用结果，不能表示被测产品通过。baseline、candidate 和 driver 是独立身份。

## 2. 整体与本批目标、非目标

整体目标仍是 #630 全部三系统兼容修复和验收。本批独立目标是让后继修复能精确选择包级用例，并取得 Windows clean 安装的真实首偏差。

本批只修改仓库私有 CI driver、其回归和维护说明。不修改 Guru runtime/manifest/hash、TaskCommit、source lock 或上游 hooks。全部平台累计 Release Gate、产品修复、真实 Agent 验收和软件发布不属于本批通过结论；这些仍由后继 Delivery 和 Task Completion 承担。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 无前序 Delivery。开发基线为 main `0543731bf52aa80842fde5db47332380de513cf0`。现有 #631 Windows artifact 的 smoke-preset 只给出 managed_runtime_check_failed，未保留内部公开 wrapper 的返回码和输出。现有 unittest_report 支持文件或模块名，不能精确加载包外文件中的单个用例。

本批依赖现有 hash-locked Python 环境和 Git for Windows Bash，复用现有三系统 CI。后继负责路径、URI、编码、传输、换行、上游 #53 来源采用、所有产品回归、Windows Codex 会话和正式发布；没有产品验收被取消或转交 #631。

## 4. 本批调用方、场景与流程

| 场景 | 调用方与前置 | 动作与可观察结果 |
| --- | --- | --- |
| DS1 | 维护者，包外测试文件已存在 | 选择 `path/to/test.py::Class.test`，只执行指定真实用例；未选中的无关失败不参与结果 |
| DS2 | 维护者，原文件或模块选择 | 继续使用旧语法，保留原结果；缺文件、类、用例和导入错误保持非零 |
| DS3 | CI，目标依赖环境已建立 | 在目标实现上运行其 bootstrap public-wrapper capability check，记录真实子进程 argv、返回码和 stdout/stderr；不替换产品实现 |
| DS4 | CI，一个目标测试或安装失败 | 继续其他独立阶段及另一个目标；最终产品/基础设施失败保持原非零，artifact 区分诊断和产品结果 |

## 5. 完整行为、条件与约束

- DR1：选择器新增文件与用例的明确组合；路径包含空格时按一个 argv 传递。只从指定文件加载所选类/方法，不在全仓 discover 后过滤。旧文件和 unittest ID 选择保持可用。
- DR2：驱动与目标分离。测试文件来自明确被测目标；诊断驱动来自本次 driver。不得复制候选产品代码进基线或将 ImportError/runtime 未激活/WinError 193 算缺陷命中。
- DR3：诊断执行目标自身 bootstrap_check 及真实 Bash→managed Python wrapper。仅观察已声明 fixture 的调用和结果，保持调用参数和产品返回行为。普通 schema 不完整输入也执行，不能只验证成功情况。
- DR4：目标 checkout、Python/Bash/OS、driver 与目标 SHA 分别记录；日志只包含本 fixture 的非敏感命令和输出，不收集环境变量、凭据或业务数据。
- DR5：诊断失败、产品失败、环境缺口分别保留；不给 expected_test/expected_message 增加“任意安装失败即预期”的含义。候选失败和未执行不能变成通过。
- DR6：沿原 targeted-ci.yml 接入，不建第二套 runner；macOS/Linux/Windows 各取得原生诊断结果。继承的产品缺陷仍由后继修复，本批不可声称 #630 完成。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 入口、输入与预期结果 |
| --- | --- | --- |
| DA1 | DR1/DS1 | 真实临时包外测试文件含一个选中通过用例和一个未选中失败用例；文件::用例入口只跑选中项，tests_run=1 |
| DA2 | DR1/DS2 | 旧文件与模块选择保持结果；不存在用例与真实导入错误非零并记录 error |
| DA3 | DR2–4/DS3 | 现有三系统 CI 使用独立目标实现执行真实 capability fixture，报告两种声明用例的实际调用结果，Windows 底层失败可定位 |
| DA4 | DR5–6/DS4 | 现有 driver 集成测试及实际 run 证明失败继续、独立目标身份和原始产品失败不被诊断成功覆盖 |
| DA5 | DR4–6 | docs/ci 说明精确选择、diagnostic artifact 和证据边界；不勾选整体产品验收 |

无未决产品选择。Windows 安装根因是本批要取得的技术事实，不是本批先验通过结论。若目标资产/解释器/Bash 缺失，保留环境失败并修复本批必要 fixture 前提，不能伪造调用记录。

## 7. Canonical 引用与本轮差额

`docs/ci/README.md` 是本批直接维护说明；.trellis/spec/workflow/quality-guidelines.md 的 Test And Validation Value/Validation Scope Ownership 约束测试层和范围。`.trellis/spec/preset/upstream-ownership.md` 保持产品与上游资产边界；本批不写它们。Architecture authority 为 docs/architecture/README.md（current-main-0.7.0-guru.102）、constitution 和 change-contract；候选评估已返回 no_architecture_impact，最终方案仍由独立 final_plan 审核。RDT 当前知识入口 docs/requirements/current/README.md、docs/design/current/README.md、docs/test/current/README.md，本批 CI 私有扩展不改变其生命周期行为。
