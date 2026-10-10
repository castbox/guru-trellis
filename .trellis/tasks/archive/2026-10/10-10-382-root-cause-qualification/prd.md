# #382 根因候选资格审查需求

## Authority 与交付边界

唯一变更需求是 `castbox/guru-trellis#382` 合同 `2026-10-10-r1`。本文是该任务的执行投影，不替代 live Issue。当前 RDT 与 Architecture 为 `current-main-0.6.17-guru.78/active`，设计原则读取 `docs/architecture/00-foundation/design-constitution.md`。

本任务在现有资格链上增加 AI-owned 根因候选资格。#404 的独立 Architecture 方法保持；#383 独占共同因果完成语义及 Check、Branch Review、Delivery Review、Completion 的完成声明；#468 不在本任务执行范围。业务仓与生产只读，业务证据不能被通用包的通过结果替代。

## 当前缺口与目标

真实故障候选通过 normal-scenario 与 solution-mechanism 后，仍可能通过提前拒绝、扩大 retry、partial fallback、error mapping 或排除样本隐藏原始失败。现有两 owner 分别证明场景资格与机制 authority 归属，均不负责 first failure、因果链、反事实和失败再分布。

新增能力按 accepted scope 和机制实际行为判断目标，分清诊断、缓解、根因修复与独立保护。普通 feature 返回稳定不适用结果。测试绿色、既有实现、独立 reviewer、最佳实践或安全压力不代替因果依据。

## 需求

| ID | 当前行为与可观察结果 |
| --- | --- |
| R382-01 | 在 requirements、change-request、planning、implementation discovery、Phase 2、base reconciliation、Branch Review，以及 Delivery 新机制边界调用新 owner；只有正常场景已合格的候选进入，机制 authority 归属复用现有 owner。 |
| R382-02 | 真实故障和有界调查成立时，根因未知的诊断继续规划、取证和假设验证；缺 first failure/因果链记录为待调查内容，不能阻塞调查准入。 |
| R382-03 | 缓解证明自身效果、风险、合法输入/消费者影响、适用条件、owner、期限与退出条件，根因未知诚实保留；输出 mitigation disposition，不能称为根因修复。 |
| R382-04 | 根因修复候选须有 first-failure causal evidence、机制改变的真实状态/行为、反事实与同输入或严格等价样本验证计划；不足返回诊断补证并暂停该修复资格。 |
| R382-05 | 保护机制须绑定保护对象、可证明损害、直接 owner、current RDT/Architecture authority 与当前层阻断必要性；合法 credential/permission/integrity/ownership/lease/fence 保护保留。 |
| R382-06 | 分清 root_cause_mechanism_eligible、mitigation_only、protection_invariant_eligible、symptom_suppression_rejected、diagnosis_incomplete、not_incident_applicable、blocked；抑制只返回机制 remove/replace，不能转无关 scope clarification。 |
| R382-07 | 同一机制在后续阶段保持适用时消费已有最小结论，阶段 owner 仍独立审当前实现和证据；新机制或实质变化才重审，caller/stage 改变本身不触发重复认知。 |
| R382-08 | Markdown 拥有语义判断；runtime 仅校验闭合结构、identity/freshness、集合覆盖与唯一 consumer；正常调用零 tracked/ignored qualification residue，不持久化授权。 |
| R382-09 | canonical、installed/shared 与 exact selected native platforms 一致；focused eval、runtime、clean install、update/reapply、drift/sidecar 与真实业务 dogfood 分层报告。 |

## 验收矩阵

以下病例来自 live Issue；它们是可独立观测的语义行为，不是关键词分类。合法与不合格机制必须以相同技术词、不同事实作成对对照。

| Case | 输入事实 | 要求的结果 |
| --- | --- | --- |
| C01 | Provider 故障由配置范围 gate 提前替代，没有修复/缓解/保护依据 | symptom_suppression_rejected → 当前机制 remove/replace；原样本仍在验证范围。 |
| C02 | 稳定 logic/schema 失败只增加 retry budget | 不认定修复；原 first failure 与后续重试分开观测。 |
| C03 | fallback 返回不完整成功 | 缺独立缓解合同则拒绝；存在明确降级缓解依据则 mitigation_only，终态不能冒充完整成功。 |
| C04 | 只改变 error mapping | 未改变结果不能证明根因修复；合法诊断观测改进按诊断目标审查。 |
| C05 | 从 fixture/candidate set 排除失败样本 | 无 current scope依据的排除不能成为通过证据。 |
| C06 | credential/permission/integrity/ownership/lease gate 有真实保护依据 | protection_invariant_eligible，保留保护 owner。 |
| C07 | 缓解有效果证据、期限与退出，根因仍未修复 | mitigation_only → 原阶段继续，根因后续 owner 留在现有 authority。 |
| C08 | 声称修复但因果/反事实不足 | diagnosis_incomplete → 诊断补证，当前未证明修复暂停。 |
| C09 | 真实故障、有界诊断，根因未知 | diagnosis_incomplete 分类但诊断可继续；不形成调查准入循环。 |
| C10 | 根因未知的紧急缓解，效果与风险有依据 | mitigation_only，生产副作用仍走既有权限边界。 |
| C11 | 同一机制跨阶段；随后机制实质改变 | 前者复用适用结论且阶段重审；后者返回资格 owner，不能复用旧结论。 |
| C12 | 普通 feature | not_incident_applicable，原阶段继续，无调查表单或额外确认。 |
| C13 | already implemented/tested/reviewer/best practice/security pressure framing | 相同事实得到相同分类与路由，不把 framing 当 authority。 |
| C14 | 实际 wrapper、安装投影与合法 stale/re-entry | 分类到正确唯一 consumer；stale 自动重读；成功后 tracked/ignored qualification residue 均为零。 |

## 非目标与未验证边界

不创建第二完成 SSOT、旧 Finalizer、incident 数据库、签字/assignment 流、未来通用规则引擎或机制缓存；不修改 Trellis 上游/global npm/node_modules/hooks。恶意伪造、攻击、TOCTOU、锁协议、并发压力和额外 crash/fault injection 不进入 scope。

完整多平台 Release/升级矩阵由专门 owner 承担。业务历史只读回放证明 Guru 判断行为，不能证明生产故障修复。真实业务仓原生 Agent dogfood 若环境或写权限未具备，记为未验证边界并返回现有 evidence route，不能用 fixture 或静态检查替代。

## Delivery policy 与 Docs SSOT Plan

本任务只选择一份完整交付切片 R382-01..09；任务内无留待后续的 accepted work。可独立交付条件是全部候选路由可运行、目标感知分类可验证、零 residue、分发一致；#383 尚未实施时不要求完成声明新规则才可使用 qualification。

Durable requirement/design/test 增量写入 `docs/requirements-design-test-contributions/382-root-cause-qualification/`，通过各层 owner 独立审查及 expected-current-bound promotion 承接；不直接竞争 shared current。Architecture 影响由独立 assessment 决定其 contribution/ADR路径。Skill package 独占准入合同，workflow 只编排；spec 与 README 只保留各自消费规则/导航。唯一共同因果完成语义未来定位到 #383 的 `trellis/presets/guru-team/spec/workflow/causal-completion-semantics.md`，本任务不创建该文件或占有完成判断。
