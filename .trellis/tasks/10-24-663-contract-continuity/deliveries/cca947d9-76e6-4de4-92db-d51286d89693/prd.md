# 当前流程合同连续性：D1 需求

## 1. 整体来源与术语

整体 authority 为 Task 根 `prd.md` 的公共 accepted_scope；本 Delivery 选择 R1–R6 和 V1–V8 全部 anchors。Direct Source 是 [#663](https://github.com/castbox/guru-trellis/issues/663) 的完整问题、四项断点、修复约束和验收，角色为要求；扫描轮次为历史证据。Authority、B/H 和 producer/consumer 的定义由整体 PRD 第1节拥有。

## 2. 整体与本批目标、非目标

本批独立交付当前四项正常流程承接修复，以及全图组合检查和分发回归。修复让原 caller 能从真实出口构造原 consumer 的合法输入，继续原维护或审核职责。排除已修复项、业务旧安装、#802、#649、#656、完整 Release 矩阵及通用恢复框架；不扩大为安全攻击、竞态或故意篡改场景。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首次且全量 D1，没有前序 Delivery。起点是选定 main 的当前三个 package 和 workflow；现有正式 wrapper 复现及对照说明当前缺口，不代表本批已通过。使用匹配固定 Fork、受管 Python、当前 public API 和安装机制。无预定后续切片；若四项验收或当前全图确认的同类正常断点未完成，整体 Completion 不成立。Release 与真实业务采用证据继续由其专属 owner 拥有。

## 4. 本批调用方、场景与流程

F1：原 Bootstrap 调用者在检查后收到 repair_required，使用正式出口及自己的原调用上下文薄投影，进入同 owner repair，并继续实际基线修复。

F2：归档 Review caller 从 Interface 指定例子填写真实 schema2 archive/key/HEAD/PR snapshot，经原 recorder/checker/invoke 返回只读结果，保持原 disposition stop。

F3：Delivery 的固定 B 不含必要 architecture authority。原 Planning/Bootstrap 建立后提交 H；Architecture 使用 B 的真实存在/缺失事实，完成 Phase 2、TaskCommit、committed Architecture 和完整 B..H Review。B 已有文件的现有路径保持。

F4：原 final promotion 判定需 Bootstrap 后，caller 保留原 profile/stage、Task/DeliveryKey/root 和 continuation。Maintenance 使用正式接受的 stage，完成后 fresh 回同一次 promotion。Whole-task 与 Delivery 都需闭合，原 repair 分支保持。

## 5. 完整行为、条件与约束

R1：公开声明明确 source_exit、mode、continuation 及必要上下文来源；保留 same-owner profile/identity 检查。不读 producer 私有结果，不要求用户手拼缺字段。

R2：移除 archived example 的过期当前 Check 字段，保留严格 schema 和只读职责；不得恢复 active gate、当前 Check、Task 重开或阶段推进。

R3：原 Architecture owner 明确表示并验证固定 B 中的真实 before absence，完整审核当前新增文件。不得移动 B、以 H 替代 before 或作通用 freshness 豁免。

R4：原 promotion → Bootstrap → 原 promotion 的 stage、身份和原 context 一致；maintenance success 不能当 promoted、final Check 或业务阶段完成。

R5：按当前 registry/workflow/Interface 检查前进、返工、恢复和 stop，公开 input examples 同时匹配 profile/aggregate schema。只将已证实的支持正常路径断点纳入当前修复。

R6：canonical、完整 installed、dogfood、声明平台一并同步；公共合同变化有明确兼容迁移。保留字段/身份/freshness 和普通缺失、profile/continuation mismatch 阻塞，不放宽成任意输入。

方案选择由独立 candidate_assessment 后的 design 第3节拥有；本需求不预先批准具体新字段。AI 判断语义，脚本仅校验和执行事实。没有业务数据持久化迁移。

## 6. 本批验收、验证方式与未决项

V1：正式 repair_required 经声明投影进入同 owner repair，原 mode/continuation/context 保持。V2：一个隔离代表性安装由真实 AI owner 消费并继续实际基线修复，结果与事实一致；受控 wrappers 单列。

V3：new/existing/standalone repair 和既有出口保持，普通 missing/mismatch 仍提前阻塞。V4：全图投影与公开 input examples、profile/aggregate schemas 组合检查，包括 F1–F4、stage 和 before absence；报告动态分支边界。

V5：定向 clean install、reapply/drift、sidecar、权限和平台完整分发一致；最多一个代表性 throwaway。V6：正式 archived example 填真实 schema2 archive 身份，经 recorder/checker/invoke 返回合法只读结果，archive/Completion/Closure/planning/range/PR snapshot 与 stop 不变。

V7：B 缺 authority 的样本实际经 Planning/Bootstrap、Phase 2、TaskCommit、committed Architecture 和完整 Review，保留 B..H；另做 B 已有 authority 对照。原生 owner 与受控证据分开。

V8：正式 final promotion 出口经 Bootstrap 回同一次原 promotion，whole-task/Delivery/repair 对照均覆盖；身份/context 保持，不把维护当晋升。没有必要用户选择；具体机制由原 Author/Architecture 在本要求下细化，未通过证据不能预填。

## 7. Canonical 引用与本轮差额

- 行为与接口：`trellis/skills/guru-team/packages/guru-bootstrap-repository-ssot/` 的 Interface/repair schema；`guru-review-branch/` 的 archived example/schema/record；`guru-maintain-architecture-baseline/` 的 before authority/promotion/Bootstrap 合同。本轮只修对应真实失配及其必要 consumers。
- 架构：`docs/architecture/00-foundation/design-constitution.md`、`03-domains/ownership.md`、`06-governance/change-contract.md` 的 authority、single-writer、兼容及 nine-concern 约束。原 owner 边界保持，必要真实差额由原贡献/晋升路径收敛。
- 验证与分发：`.trellis/spec/workflow/quality-guidelines.md` 的 Validation Scope Ownership、`skill-package-contract.md` 的 Public Skill I/O And Private State，以及现有 package tests、apply/drift。新增实际组合覆盖，不能只做 marker parity。
