# 合法 Agent Skill 的升级投影验收修复设计

## 1. 设计目标、需求承接与内容基线

承接本批 PRD 的 R8-A/R8-R/R8-C、S8-A/R/E/U 与整体 R8/AC6。开发基线及内容范围 B 为 main@62b75465957ad0543803bdbe98e6dc222008040e；原 construct-delivery-candidate 已实际返回该 base_ref。Planning H0 同为 62b754659，最终实现 HEAD 另由原 constructor 构造；PR target 为 main。generation 0 的版本准备不重复进入本批范围。

独立 Architecture 原 candidate_assessment 已实际返回 baseline_current、no_architecture_impact，baseline identity guru-trellis-architecture，constitution guru-trellis-design-constitution-v1。适用 authority 为 docs/architecture/00-foundation/design-constitution.md 与 docs/architecture/06-governance/change-contract.md；最终 Wording 后另取 final_plan。

## 2. 当前系统、边界与目标差额

verify_trellis_compatibility_matrix.py 的 `_assert_platform_projection` 遍历 shared/selected roots，读取 installed package Interface，却无条件要求 wrapper。真实旧升级 target 的 guru-orchestrate-issue-dag 声明 agent/entrypoint=SKILL.md，因此安装成功仍在验收时失败。

本轮只修改此函数及 test_verify_trellis_matrix_capture.py。不改包集合、installer、平台描述符、公共 Interface、Fork 或 workflow。实际 installed manifest 的 install/overlays/skill_packages 均未声明该 verifier 源路径，因此本轮没有受管投影或 tools 重装差额。

## 3. 来源设计处置（唯一）

| 来源/条款 | 原承诺 | 处置与落点 | 理由、影响与上游处置 |
| --- | --- | --- | --- |
| release contract / Stage 1 | 原 Author/Check/TaskCommit、两次独立 Branch Review、串行晋升后重验 | retain：implement第5节由原生命周期owners继续 | 本批修复准备范围，不缩短正式质量链 |
| release contract / Stage 2 | 准备与归档后冻结新clean candidate，独立重跑最低门禁 | retain：implement V4 与第5节明确发布owner后继 | dirty实施结果不继承为发布pass，不变更上游 |
| skill-package-contract / Instruction-Only Standalone Packages | 显式agent使用Markdown entrypoint，无wrapper；旧Interface原要求保留 | retain：本设计第4–7节 | 修正消费端错误假设，不新增包类型或迁移合同 |

## 4. 模块、职责与设计取舍

原 verifier 仍只判断客观投影事实。明确 `invocation.kind == agent` 时选择 entrypoint；否则沿原 runtime wrapper 合同。旧 runtime 未声明 kind 仍受支持，不能把缺 wrapper 推断为 agent。共用入口路径的既有相对路径检查、存在性、bytes 与文件权限模式比较。runtime 另外检查公共 wrapper 可执行。

私有 scripts 检查对两类都执行：目录不存在时无脚本泄漏，存在时检查其中文件，runtime只排除其声明的公共wrapper。Agent 不要求创建空 scripts 目录。保留原 inventory 与未选平台检查。直接修正源函数优于跳过 instruction_only 包或伪造 wrapper；两种后者均不验证原入口且违反已有合同。

## 5. 接口与数据

输入保持 `(target: Path, platform: str)`，返回成功 None 或原 MatrixError。生产者为 installed Interface 的 public_contracts.invocation：agent声明entrypoint；原runtime声明wrapper。消费者是 `_assert_platform_projection`，再由原 existing/focused verifier 消费结果。没有新API、字段、状态、持久化或公共输出变化。

## 6. 状态、顺序、正常与失败流程

先核shared/selected inventory，再逐包读Interface。选择声明入口后校验其相对路径及文件；runtime要求可执行。随后比较package与projection字节及stat.S_IMODE权限模式，再核scripts私有文件。最后核未选平台目录。入口缺失、字节/模式不一致或私有脚本出现均抛MatrixError，保持原调用链失败传播。

## 7. 恢复、兼容、迁移与集成

直接演进原函数，不保留新旧双实现。合法runtime无kind、合法agent无scripts目录分别保留。没有数据迁移或业务恢复协议。原失败target保留为诊断输入，修复后对同target重跑投影；真实前驱existing由原入口重新建立完整target，保留实际前驱lock与包集合。外部下载/工具故障保留首次诊断并回原owner，不改包或跳过验收。

## 8. 验证设计

V1长期回归：用隔离布局直接调用原函数，混合agent/runtime成功；入口缺失、bytes漂移、权限模式漂移、runtime不可执行和私有scripts泄漏失败。每组观察独立失效机制，fixtures由公开Interface与安装布局定义，不复制函数算法计算期望。

V2临时因果验证：同一真实旧失败target，原代码已观察到public wrapper is missing；修复后原函数完整通过，不改target。

V3原existing全链：真实v0.7.0-guru.7/.5安装升级至当前.8/.6，原Fork构建及main provider保持，观察安装、update/reapply、投影与退休资产退出。此层不能由V1或V2替代。实施dirty来源由source_state绑定HEAD+完整delta，不声称发布candidate通过。

V4最终发布：准备/归档后发布owner从新clean exact candidate重跑Issue最低门禁。当前不执行tag/Release。V1–V3充分且无新缺口即停止重复验证。

## 9. Canonical 引用、本轮差额与实际未决项

沿本批PRD第7节的RDT/分发authority。已读skill-package-contract的Instruction-Only Standalone Packages、quality-guidelines的Test And Validation Value、review-sufficiency与causal-completion-semantics。本轮为现有合同的validator修复，无新Architecture定义、ADR或共享RDT导航写入。最终原Architecture/RDT owners仍审查真实差额；必要未决项为后续门禁结果，不是当前需求选择。
