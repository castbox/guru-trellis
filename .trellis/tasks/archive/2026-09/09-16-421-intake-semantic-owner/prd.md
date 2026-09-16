# #421 修复 Intake semantic owner 自阻塞

## 1. 目标与依据

唯一需求来源：[Issue #421](https://github.com/castbox/guru-trellis/issues/421)，正文更新时间为 2026-09-16T06:29:47Z；规划基线为 main@57e8b5df10aedc4f218a4685e819d25a44aa8928。

当前集成基线为 main@78651e2068184e9e52a778fe33eda8b2bd7c8e0b，包含 #417 / PR #422 的 Phase 2 authoring。该能力作为基线保留，不属于本任务实现范围。

当前执行 AI 必须亲自完成现行 standard Intake 的四个 semantic owner 闭环，使清晰请求无需外部 owner、subagent、agent ID、预置 owner result 或人工纠偏 Prompt 即可进入 workspace 创建门禁。真实缺失或冲突继续进入已声明的阻塞或修订路由。

## 2. 当前事实与缺口

- Discovery、Clarification、Wording、Readiness 已分别拥有 semantic 合同和正式 wrapper；runtime 只记录、校验与序列化。
- Issue 记录的正常失败是当前 AI 将“runtime 不能生成判断”误读为“自己不能生成判断”，因缺少尚未执行的 owner result 而停滞。
- 当前四个 Skill 的入口未直接明确 `owner_not_yet_executed` 的执行责任。workspace 拒绝缺失 predecessor inputs 是正确行为。
- `adapters/eval/stage0_fixtures.py:readiness_context` 由 host 构造 Discovery owner，不能作为 native 从零完成四步判断的证明。
- 在初始规划基线中，#415 已提供 `semantic_authoring` 模式，但只支持 Architecture；当前集成基线新增了 #417 的 Phase 2 分支。两者均不能替代本任务四步 Intake 的独立证明。

## 3. 范围与要求

| 编号 | 必须交付的行为 |
| --- | --- |
| R1 | 直接修订四个 canonical Intake Skill 的 SKILL.md 与 contract，明确当前执行 AI 是 owner；`owner_not_yet_executed` 是继续当前审查的内部状态，不是 typed stop。 |
| R2 | 每个 owner 读取完整合同和真实证据，自行形成 scope、finding、pass/block、readiness、route，然后执行原有 record、check、invoke；subagent evidence 不是执行前提。 |
| R3 | 每一步真实 public output 按现有声明投影为下一步 public input；不读取或重构 producer-private result，不改变生产 schema、exit、consumer、owner 或 workspace 门禁。 |
| R4 | 增加 installed/native standard Intake semantic-authoring 回归；不预置 owner result，不向模型投影 expected exit、期望判断或 host 预填 pass。 |
| R5 | 同一个 native Agent 覆盖完整成功链以及一个真实需求冲突导致的 semantic blocker 路由；成功链到达 Readiness 的 ready，产出 workspace 所需 fresh public predecessor inputs，但测试不执行 workspace mutation。 |
| R6 | 同步 canonical、dogfood installed、Shared、Codex、Claude、Cursor 声明投影，验证 package、projection parity、preset reapply、drift 和 residue。 |

## 4. 验收场景

| 编号 | 输入与动作 | 可观察结果 |
| --- | --- | --- |
| A1 | 清晰的事实 fixture，经真实 Sync 后由 native Agent 完成四个 owner | 真实 wrappers 顺序产生 context_ready、clear、pass、ready；每步 owner 语义结果先于 record；public output 连续投影，未预填 predecessor。 |
| A2 | 同一正常入口收到正文内部存在未决交付范围冲突的事实 fixture | native owner 指出冲突并返回现行 blocked 出口；不伪造 scope 答案，不调用 workspace，不把“自己尚未执行”当缺失外部 owner。 |
| A3 | 原有正常 stale、identity、schema 或缺前置证据路径 | 原有定向测试保持 fail-closed；只复用已支持的维护失误案例，不引入人为伪造、攻击、竞态压力或 fault injection。 |
| A4 | 执行 source/installed package 检查与声明平台投影检查，再 reapply | 受管 bytes、mode 与声明投影一致；dogfood drift 为零，无本任务遗留 .new、.bak、__pycache__ 或 .pyc。 |
| A5 | 检查完整 native trace 与模型可见输入 | 四个 Skill/contract 和必要证据有真实 read，record/check/invoke 有真实回执；无预置 owner、期望答案投影、关键词断言冒充语义通过或手工纠偏 Prompt。 |

## 5. 非目标与交付边界

- 不实施 #250、#417、#418、#419、#398、#404，不修改 Phase 2 owner 合同、criteria 或生产测试。
- 不改变生产 public I/O、typed exits、thin projection、duplicate/requirements/wording/readiness/workspace 门禁。
- 不新增生产 wrapper、长期 handoff、tracked ledger、授权 artifact、锁、重试协议或兼容执行路径。
- 不修改 Trellis upstream、全局 Python/npm、业务仓库或生产环境。
- #410 独占 release exact-candidate 重新冻结与完整多平台 Release Gate；本任务的定向证据不替代该矩阵。
- GitHub mutation、commit、push、PR、merge、tag、Release 与资源清理均不由本规划隐含执行。

## 6. 风险与完成口径

native 工具、模型或依赖不可用时如实标记 unsupported/blocked，A1/A2 未通过则本任务不能声称完成。静态字句断言、transport 返回零、host 构造 result 和本会话的 Intake 成功均不能替代自动化 native 回归。

需求不存在未决产品选择。技术实现必须维持现有 owner 分层；发现必须变更生产协议或共享架构时返回规划，不扩大本任务。

## 7. Docs SSOT Plan

| 文档集合 | 决策 | 原因与验证 |
| --- | --- | --- |
| 四个 Intake package 的 SKILL.md、references/contract.md | update | step-local 执行责任发生澄清；contract tests 与 source/installed parity 验证。 |
| trellis/presets/guru-team/spec/workflow/ 下的 skill-package-contract.md、data-contracts.md、companion-scripts.md 及 .trellis/spec/workflow/ 安装投影 | update | canonical 记录 eval-only 多 owner authoring flow、事实投影与 trace 检查边界，再同步安装投影；不复制 Skill 内部流程。 |
| trellis/workflows/guru-team/README.md、trellis/presets/guru-team/README.md | update | 声明 native regression 与安装验证的证明范围。 |
| canonical workflow、平台 launcher、overlay | no_update | 全局顺序和路由未变；检查它们调用同一 Skill，不复制 step-local 规则。受管 Skill 投影由 preset 生成。 |
| docs/requirements、docs/design、docs/test、docs/architecture shared current | no_update | 落实现有 AI/runtime ownership，不新增产品能力、架构决定或 single writer；当前 Architecture owner 必须核对该判断。 |
| 本任务 prd.md、design.md、implement.md、implement.jsonl、check.jsonl | update | 需求、设计、执行计划和直接供实现/check 使用的上下文。 |

Evolution 的 AI-first 与低交接成本方向保持一致；本任务不把未来 Evolution 目标当现行 runtime，不提前激活生命周期迁移。Docs SSOT 决策在本节唯一维护。
