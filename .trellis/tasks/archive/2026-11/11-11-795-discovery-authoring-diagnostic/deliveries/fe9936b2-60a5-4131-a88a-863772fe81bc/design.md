# Discovery 普通字段诊断与 authoring 恢复设计

## 1. 设计目标、需求承接与内容基线

本设计承接整体 PRD R1-R4、Delivery PRD D795-R1..R4 与 D795-AC1..AC6。目标是在不改变公共 DTO、错误 taxonomy、成功门禁和 owner 边界的前提下，修正 Git-object owner-result 的校验顺序，收敛当前版本导航，并明确普通同 owner 恢复路径。

Development baseline B 为 `main@e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e`，来源是本次 Intake 的固定只读基线。Planning H0 是当前 Task 分支 `codex/795-discovery-authoring-diagnostic` 在 B 上的 planning 候选；Task/session/runtime 文件不属于 Delivery content range。PR 目标分支为 `main`。

Architecture candidate assessment 由独立 reviewer 返回 `baseline_current / architecture_impact / target_native`，decision refs 为 `ARCH-DOM-038`、`ARCH-DOM-039`、`ARCH-INT-001`。任务级 Architecture 拟写为 [architecture-contribution.md](./architecture-contribution.md)，不需要新 ADR。

## 2. 当前系统、边界与目标差额

当前 Discovery Git-object record 在 `bind_owner_to_public` 中先读取 reviewed evidence，再生成派生字段和校验完整 owner-result。`validate_source_evidence` 直接访问 `deep_reads[*].source`，因此结构错误可能越过 schema 诊断。共享 `validate_json` 已能报告字段级 `schema_mismatch`；共享 dispatcher 的 `internal_error` 仍用于真实未知异常。

当前 Interface 选择 pre_task 4.0、context_request 2.0 和 owner-result 4.0，但当前 artifact/example 中仍有条目指向 3.0 或旧 id。同步来源 owner-result 3.0 仍有真实兼容 consumer，因此保留。恢复文本已有 same-scope 概念，但没有把普通字段纠正重跑原链与真实内部故障的维护路由写成明确步骤。

目标状态：

- Git-object record 先完成 AI-authored owner-result 结构诊断，再观察 Git evidence。
- 当前 Git-object 导航唯一选择 4.0 组合；3.0 保持明确兼容。
- 普通 authoring 纠正沿用原 record/check/invoke；未知异常仍 fail closed 到维护 owner。

不改边界：Clarify、Wording、Readiness、Author、Architecture 和安装 owner；public typed exits；错误 code 集；freshness 规则；业务 Task 数据；Trellis 上游源码或全局安装。

## 3. 来源设计处置（唯一）

| 来源 | 原承诺 | 处置 | 具体落点 | 理由与影响 | 上游处置 |
| --- | --- | --- | --- | --- | --- |
| Issue #795“目标与范围”第 1 项 | 普通结构错误在使用依赖字段前定位，不新增别名、不放宽门槛 | retain | `runtime/common.py` 的 Git-object record 顺序；`tests/test_runtime.py` | 直接修复 first failure，保留 schema/freshness | 无需 scope 变更 |
| Issue #795“目标与范围”第 2 项 | 对齐当前 Skill/合同/schema 导航；保留合法兼容 | retain | Interface、contract、examples、SKILL 与必要 workflow specs | 消除当前导航的并行解释 | #718 迁移合同继续有效 |
| Issue #795“目标与范围”第 3 项 | 保留失败；普通纠正重跑原链；未知异常维护 owner | retain | contract 的 recovery 段与测试 | 保持原 owner 和应用层恢复 | 无新状态 |
| Issue #795“关联与非目标” | 不重做 #793/#772/#363，不扩全局框架或矩阵 | retain | Delivery Policy、implement、Check 范围 | 防止范围扩张 | 独立 Issue 保持 |
| 当前共享 schema 诊断 | `schema_mismatch` 已包含 code/field_path/remediation | retain | 复用 `validate_json` | 避免新增错误框架 | 无 |
| 同步来源 owner-result 3.0 | 旧 consumer 与历史资产仍合法 | retain + clarify | Interface artifact 标签、合同兼容段、示例导航 | 保留兼容但不冒充当前 4.0 | 不删除旧文件 |

## 4. 模块、职责与设计取舍

### Discovery runtime

在 `trellis/skills/guru-team/packages/guru-discover-change-context/runtime/common.py` 中调整 Git-object `bind_owner_to_public`：

1. 写入由 public transition 决定的 repository/mode/change_input/base observation。
2. 在 schema-only 副本中填入固定 schema-valid 的 `canonical_query`、`history_preview` 和 `result_identity` placeholders；该副本不调用 canonical query、history preview、source reader 或 candidate reader，也不访问任何 reviewed evidence。
3. 在读取 `validate_source_evidence`、candidate bytes、history preview 或最终 identity 之前，使用现有 4.0 schema 校验完整 AI-authored 结构。
4. schema 通过后执行现有 evidence、candidate、transition 和 freshness 校验，并生成真实 canonical query、history preview 与 result identity。
5. 写入真实 result identity 并再次校验完整结果。

固定 placeholders 只用于 owner-result schema 的字段形状检查，不读取来源、不生成派生身份，也不会进入成功结果或放宽任何必填字段。实现复用 `canonical_query`、`preview`、`validate` 和现有 `validate_json`，不修改共享 dispatcher。

### Discovery 文档与 Interface

- 新增 current owner-result 4.0 最小示例，使用 Git-object repository 形态和实际 current profile。
- 新增或修正 pre_task 4.0 输入示例与 context_ready 5.0 输出示例的机器导航；旧 3.0/4.0 asset 保留。
- 修正 `interface.json` 中 current profile 的 example/schema id/path，使机器选择与当前合同一致。
- 修正 `references/contract.md` 与 `SKILL.md` 中当前 authoring 的版本组合和恢复说明。

### 共享 workflow specs

同步实际承载 Discovery 版本和验证要求的 `.trellis/spec` canonical sources：

- `trellis/presets/guru-team/spec/workflow/data-contracts.md`
- `trellis/presets/guru-team/spec/workflow/skill-package-contract.md`
- `trellis/presets/guru-team/spec/workflow/quality-guidelines.md`

只改 Discovery 当前 owner-result 版本、示例导航、测试范围和普通纠正恢复边界。包合同、数据合同、质量检查各自拥有自己的段落，不做跨文件复制。

### 测试与安装投影

- `tests/test_runtime.py` 通过公开 record 入口覆盖 source/source_kind、observation 缺失和纠正后原链成功。
- `tests/test_contract.py` 验证 current Interface 的 profile/schema/example 版本组合，并确认 3.0 仍被保留为同步来源兼容。
- preset、distribution tests 验证 canonical、dogfood、声明平台投影和 sidecar/drift。
- dogfood 使用原安装 owner 同步，不手工把 `.trellis/guru-team` 或 `.agents` 当源头。

设计取舍：复用现有 schema 错误和固定 placeholder shape view，而不是新增字段检查函数、错误分类器或全局异常捕获。这样最早移除 first failure，同时保持 `internal_error` 作为未知故障兜底。

## 5. 接口与数据

公共 record 入口、check 入口、invoke 入口、public profile 名、typed exit、schema id 和错误 code 集不新增。当前 Git-object 数据组合固定为：

- public input：`pre_task` 4.0 或 `context_request` 2.0；
- owner-result：Git-object `4.0`；
- context_ready public output：`5.0`；
- 同步来源 owner-result：保留 `3.0`。

record 的中间 receipt 和正式 invoke 输出保持现有 schema。`schema_mismatch` 诊断继续使用 `code`、`field_path`、`remediation`；成功 result 仍使用同一 owner-result 4.0 和 result identity 算法。

## 6. 状态、顺序、正常与失败流程

### 正常流程

1. 公开 record 读取 envelope 和独立 base transition。
2. binder 写入当前 mode、change input、repository 和 base observation。
3. binder 在 schema-only 副本中写入固定 query/history/result placeholders，不读取 evidence。
4. owner-result schema 校验成功。
5. reviewed Git evidence、candidate bytes、transition candidate 和 freshness 校验成功。
6. binder 写入真实 result identity 并再次校验。
7. record 返回规范化 owner result；check 与 invoke 继续现有流程。

### 普通结构错误

- `deep_reads[*].source` 缺失或写成 `source_kind`：在第 4 步停止，返回 `schema_mismatch` 与 source 字段路径。
- duplicate candidate `observation` 缺失：在第 4 步停止，返回 observation 字段路径。
- 错误输入不生成 `context_ready`，不进入 Git evidence 读取，也不写入任何成功身份。

### 纠正后重跑

保留首次失败。原 owner 重读同一来源、上游 public output 和仍适用的语义审查，重建完整 owner result，再执行原 record/check/invoke。成功只来自最终 public invoke，首次 stdout/stderr 不被覆盖。

### 真实内部故障

未被合同分类的异常继续由 dispatcher 返回 `internal_error/runtime`，记录命令、退出码和输出，交包维护 owner；不得归类为普通字段错误或通过改 runtime 掩盖。

## 7. 恢复、兼容、迁移与集成

- 普通同 owner 纠正是当前合同的既有步骤，不新增 checkpoint、授权或审计记录。
- owner-result 3.0 是同步来源的兼容合同，保留原 schema/example/消费者；当前 Git-object 4.0 不 dual-write。
- 新示例只提供当前 authoring 形状，不创建当前 Gate 或成功证据。
- canonical 修改后通过原 preset/upgrade owner 同步 dogfood 与声明平台；不得手工覆盖受管副本。
- 无数据库、业务数据、Kubernetes 或部署迁移。
- 若安装 owner 产生 `.new`/`.bak`、用户修改冲突或旧 Task/session 阻塞，按原机制停止或恢复，不强行覆盖。

## 8. 验证设计

| ID | 要求/场景 | 层级与入口 | 输入 | 预期观察 | 边界 |
| --- | --- | --- | --- | --- | --- |
| V795-1 | R1/S1/AC1 | Discovery 公开 record；临时 Git-object repo | reviewer-owned 完整输入，`source` 改为 `source_kind`，同时放入只会在结构通过后读取的缺失 evidence path | `schema_mismatch`，field_path 指向 source；不是 `internal_error` 或 evidence 路径错误 | 公开入口证明结构错误先于 evidence reader |
| V795-1U | R1/AC1 的读取顺序 | binder 单元 guard | 对 `preview` 与 `source_blob` 安装 fail-if-called guard，再提交缺 source 结构 | schema 诊断成功且 guards 未被调用 | 作为公开入口测试的补充，不替代公开入口证据 |
| V795-2 | R1/S2/AC2 | 同一公开 record 入口 | 删除 duplicate candidate observation | 字段级 observation 诊断 | 只证明既有 schema 行为保持 |
| V795-3 | R2/S3/AC2 | 公开 record → check → invoke；临时 Git-object repo | 修正后的完整 owner result | record/check 通过，invoke 实际 `context_ready` | 不重演 #793 |
| V795-4 | R2/S4/AC3 | package contract tests | 读取 Interface、schema、example | current 4.0 组合一致；3.0 兼容保留 | 不要求所有历史资产重写 |
| V795-5 | R3/S5/AC4 | 合同测试与文本审查 | 普通纠正/未知异常边界 | 两条路径可区分，无授权记录 | 不声称消除所有错误 |
| V795-6 | R4/AC5 | preset/distribution/drift | canonical、dogfood、声明平台 | 投影一致，无 sidecar；新增测试与受影响测试通过 | 不跑完整矩阵 |

已有成功 record/check/invoke 和 sync 来源测试继续有效；新增测试只补 Git-object 早期结构错误与恢复差额，避免重复脚本覆盖。测试 fixture 必须通过公开 wrapper 进入被测路径，不能直接调用私有函数冒充。

## 9. Canonical 引用、本轮差额与实际未决项

Canonical diff 由 Architecture contribution 记录，完整拟写位于其 `architecture/proposed/docs/architecture/`：

- `01-current/system.md` 新增 `ARCH-CUR-077`；
- `03-domains/ownership.md` 新增 `ARCH-DOM-061`；
- `04-integrations/distribution.md` 新增 `ARCH-INT-064`。

三份拟写以固定 B 的完整目标文件为 preimage，仅插入 Discovery 当前关系。无需新 ADR。

Requirement/behavior/test authority 继续由 Issue #795、root/Delivery PRD 与现有 workflow specs 承担。implementation 必须读取这些引用和完整关联条件。当前无阻塞设计选择；具体实现和测试结果尚未产生。
