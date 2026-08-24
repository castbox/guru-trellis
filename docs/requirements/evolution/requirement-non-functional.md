# Guru Trellis Evolution 非功能需求

版本：`evolution-requirements-draft-2026-08-24`；状态：`requirements_draft`。

本文件是 Evolution Requirements 非功能约束的唯一主定义。功能范围与场景见
[`requirement-main.md`](./requirement-main.md)，验收 fixture 与执行成本证据规则见该文件第 5 章。

## 1. 执行效率、安静性与上下文治理

以下约束以 `requirement-main.md` 第 5.2 节的 action/consumer 与 correctness trace 为依据。
流程耗时、rounds、bytes、compression 次数及相对 baseline 改善比例可用于诊断，不作为
Requirements、candidate 或 Release 的验收门槛；不得通过删减能力、隐藏失败或跳过 gate 获得
表面上的短路径。

- `EVO-NFR-001`：正常路径必须尽最大可能合并同一 owner 可连续完成的读取、判断和验证，避免
  没有新 authority、finding、选择或副作用变化时重复执行 semantic gate 或阶段往返。
- `EVO-NFR-002`：同一 unchanged authority 正文、累计 stdout、完整 scan/review history 或
  producer-private evidence 不得重复注入；每轮只提供当前判断需要的 locator、必要片段、delta
  和无法重建的最小结果。
- `EVO-NFR-003`：脚本、validator、recorder、文档重读和外部状态查询只有在存在直接 consumer、
  freshness 需要或 correctness 责任时才执行；不得为了合同形式完整或留下过程证明而运行。
- `EVO-NFR-004`：`EVO-FIX-FULL-NORMAL` 必须覆盖 request-to-cleanup 的完整正常生命周期，并为
  每项保留的 handoff、读取、脚本、gate、validation 和 transition 说明不可替代的责任；无法说明
  直接 consumer 或 correctness 价值的动作必须删除，不设置相对耗时或交互轮次门槛。
- `EVO-NFR-005`：正常 Planning 不得主动制造 continuation capsule 或非 durable 中间交接文件；
  平台自动 context compression 只作为诊断信号，不作为 PASS/FAIL 条件。发生 compression/resume
  时仍须按 `EVO-NFR-009` 恢复 current 工作。
- `EVO-NFR-006`：clear/no-finding 正常路径只向用户展示真实问题、选择、实质 finding/block、
  必要长等待状态、阶段结果和副作用确认；内部读取、projection、recorder、validator 与 locator
  搬运保持安静。
- `EVO-NFR-007`：任一 public handoff/result 的字段都必须有唯一直接 consumer；无 consumer
  字段、可 live 重建事实、process metadata、授权和完整 evidence 不进入 public output。
- `EVO-NFR-008`：支持的 normal fixture 中 invalid handle wait、decision-relevant truncation、
  duplicate cumulative stdout、unconsumed user intent 和 orphan artifact 均为 0；workflow 主动
  生成但没有直接恢复 consumer 的 continuation capsule 也属于 orphan artifact。

## 2. 可靠性、恢复与可用性

- `EVO-NFR-009`：resume/interruption fixture 必须 100% 保留最新用户意图、current phase、已发生
  副作用、未解决 finding 和唯一下一 route；不得只恢复压缩前的旧目标。
- `EVO-NFR-010`：外部服务不可用、认证缺失、base/provider 变化必须产生明确 current
  blocked/recovery 边界；不得把 `unverified`、`skipped` 或历史结果冒充 PASS。
- `EVO-NFR-011`：两个正常并行 task 不得写同一 task-local resource；shared authority 只经
  serialized promotion 前进，任一 task 失败/cleanup 不影响另一个 task 的资源和历史。
- `EVO-NFR-018`：parent repository 的正常 mode selection、Intake、RDT/Architecture Planning、
  Implementation、validation、Finish 与 Cleanup 不得依赖无关 Git submodule 的初始化、可访问性、
  clean/branch 状态或命令成功；默认路径的 submodule I/O 与 validation 为 0。显式 submodule
  repository scope 必须隔离运行，不能扩大 parent task 的 authority、artifact 或验证集合。

## 3. 兼容、分发与可维护性

- `EVO-NFR-012`：Shared/Codex/Claude/Cursor 与 canonical/dogfood/installed 的 scenario、
  semantic result、re-entry/stop 和 capability inventory 必须一致。
- `EVO-NFR-013`：clean install、existing repository migration、official Trellis update/upgrade、
  preset reapply 与 workflow switch 后只存在新合同，且 Requirements/Design/Test/Architecture
  current authority 与用户本地修改按官方语义保留。
- `EVO-NFR-014`：正常路径的 semantic owner 数量、持久 artifact 数量和 public data volume
  必须由直接业务责任/consumer 证明；不得为了“合同完整”新增 wrapper、schema 或 checkpoint。
- `EVO-NFR-015`：同一事实在 Requirements/Design/Test/Architecture/workflow/Skill 中只有一个
  semantic owner；projection 只引用 identity/locator/version/status，不复制正文。

## 4. 安全与隐私

- `EVO-NFR-016`：prompt、log、artifact、Issue、PR、history 与测试证据不得泄露 secret、token、
  private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。
- `EVO-NFR-017`：Git/GitHub/Trellis 副作用只能发生在用户已确认的 exact target/scope 上；
  unrelated dirty/untracked files、worktree、branch、task 和远程资源必须保持不变。

## 5. 非功能范围豁免

| `waived_item` | `scope_refs` | `waiver_reason` | `risk_statement` |
| --- | --- | --- | --- |
| 服务端 QPS/并发吞吐 | 全局 | 本产品是本地/Agent 驱动的交互 workflow，无常驻服务端 API；本轮只治理 workflow 内无 consumer 动作、重复读取/注入和不必要交接，不设置替代性的吞吐或相对性能指标 | 不代表外部 GitHub/Trellis 服务性能；流程耗时与工具量可用于诊断，但不决定 PASS/FAIL |
| 恶意 actor、对抗输入、artifact 人为伪造、额外锁/TOCTOU | 全局 | 产品假设 honest-but-fallible 协作，按仓库 current 安全边界执行 | 普通 stale/mismatch、错误 recorder/validator 和 secret/副作用边界仍必须处理 |
| 旧 Guru workflow 合同兼容 | `REQ-UC-EVO-034..035` | 用户明确要求重构后只保留新合同 | existing repository 仍必须通过一次受支持迁移进入新合同；不能静默留在旧路径 |
