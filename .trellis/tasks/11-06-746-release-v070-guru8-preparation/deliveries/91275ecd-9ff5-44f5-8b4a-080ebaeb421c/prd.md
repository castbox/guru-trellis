# 合法 Agent Skill 的升级投影验收修复需求

## 1. 整体来源与术语

当前 Task 为 `746-release-v070-guru8-preparation` generation 1，Delivery 为 `91275ecd-9ff5-44f5-8b4a-080ebaeb421c`。公共 scope_ref 选定整体 PRD 的 R8/AC6；planning_root 为本目录。整体定义和非目标见 ../../prd.md。

| 来源 | 章节 | 角色与用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/746 | 唯一候选及验收；准备任务 | requirement：真实前驱升级、入口投影和退休资产验收；准备范围引用该 Issue，不关闭它 |
| .agents/skills/release-guru-trellis-version/references/contract.md | Stage 1 / Stage 2 | design_constraint：准备与最终 exact candidate 分离、原 owner/gate 顺序 |
| .trellis/spec/workflow/skill-package-contract.md | Instruction-Only Standalone Packages | 已有公共合同：agent 使用声明 Markdown entrypoint，无 wrapper |

Agent 包是 Interface 1.9 显式 instruction_only 包；runtime 包沿用脚本 invocation 及 wrapper。字节/模式比较是安装一致性事实，不代表语义 Review。

## 2. 整体与本批目标、非目标

整体目标为完成 .8 发布准备。本批独立目标是让原 existing verifier 正确验证合法 Agent/runtime 两类入口，同时继续拒绝真实入口缺失、漂移或私有脚本泄漏。只覆盖 R8/AC6；R1–R7 的既有交付保持原职责与历史证据。本批不改 installer、公共 Interface、平台支持范围或 Fork，不替 Stage 2 candidate pass，不创建 tag/Release、不关闭 #746。

## 3. 本批起点、前序结果、依赖与剩余责任

前序 Delivery `0b570fe7-3618-4fb4-b40b-f580c3b419f1` 已由 PR #748 合入 ad205e9707f7ef1eb3077419e6489baea3894e94，归档 PR #749 合入 main@62b75465957ad0543803bdbe98e6dc222008040e。本批从该 main 继续。

真实 .7/.5 → .8/.6 existing 安装完成后，验证器 `_assert_platform_projection` 对 guru-orchestrate-issue-dag 报 public wrapper is missing。该包真实声明 invocation.kind=agent、entrypoint=SKILL.md，无 wrapper。本批必须保留该合法包并校验它，不改前驱或过滤输入。最终 clean exact-candidate 全部门禁仍由发布 owner 在准备与归档后重新执行。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置与动作 | 行为与观察 |
| --- | --- | --- |
| S8-A | existing/focused verifier 遍历实际安装的合法 Agent 包 | 按 invocation 声明找到 Markdown 入口，比较包与投影 bytes/mode，不要求可执行 wrapper |
| S8-R | 同入口遍历 runtime 包 | 检查声明 wrapper 存在、可执行、bytes/mode 匹配 |
| S8-E | 普通安装遗漏入口、内容/模式漂移或误带私有脚本 | 原 MatrixError 阻止验收，不跳包或改分类制造通过 |
| S8-U | 发布 owner 从真实前驱安装升级并 reapply | 原 existing 链走到末端，核退休资产退出；当前结果只证明本次来源 |

## 5. 完整行为、条件与约束

R8-A：按 interface.public_contracts.invocation.kind 选择声明入口；agent 使用 entrypoint，runtime 使用 wrapper。对所有遍历包执行匹配检查，不硬编码 Skill id。

R8-R：runtime wrapper 的可执行要求保留；两类入口均核对实际包与公共投影的字节和模式。缺入口、缺声明或正常漂移均失败。私有 scripts 文件不进入公共目录；Agent 无 scripts 目录是合法情况。

R8-C：保留 shared/selected inventory、非选平台检查及 existing 原流程。来源设计处置由本批 design 第3节唯一维护。既有 Codex-only/instruction-only 合同不扩成新平台支持，不新增业务状态、授权记录或脚本判断。

## 6. 本批验收、验证方式与未决项

AC6-A：通过原 `_assert_platform_projection` 输入同时含合法 Agent/runtime 的隔离安装布局，观察成功；删除声明入口、改变其 bytes/mode、移除 runtime 可执行位或带入私有脚本时观察失败。回归只覆盖不同失效行为，不模拟恶意篡改。

AC6-U：同一真实旧失败 target 在修复后完成投影检查；原 `.7/.5 → .8/.6` existing 命令由当前来源重跑，观察完整成功与退休受管资产退出。dirty 实施来源不能声称 Stage 2 clean candidate pass。没有必要未决范围选择；独立 Architecture 仍须评估实际候选。

## 7. Canonical 引用与本轮差额

行为依据为整体 R8/AC6、skill-package-contract 的 Instruction-Only Standalone Packages，以及 docs/requirements/current/issue-orchestration.md 的 R731-06：保留 Codex-only/instruction-only 和原公开入口。设计/测试依据为现有 verifier 与 test_verify_trellis_matrix_capture.py；测试选取遵守 quality-guidelines 的 Test And Validation Value。Architecture 的 docs/architecture/04-integrations/distribution.md 拥有分发和原 owner 边界，本批只修复 verifier 对既有入口的认识，不改分发合同；最终独立判断仍归 Architecture。
