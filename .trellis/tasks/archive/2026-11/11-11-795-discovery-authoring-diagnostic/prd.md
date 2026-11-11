# 修复 Discovery 普通字段错误诊断与 authoring 恢复导航

## 1. 来源与术语

| 来源 | 角色 | 本 Task 用途 |
| --- | --- | --- |
| [Issue #795](https://github.com/castbox/guru-trellis/issues/795) 的“根因与证据边界”“目标与范围”“最小验收”“关联与非目标” | 要求与现场证据 | 定义本 Task 的问题、交付边界、验收和排除项。 |
| `main@e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e` | 固定调查基线 | 绑定现场源码、合同、测试和历史事实。 |
| `trellis/skills/guru-team/packages/guru-discover-change-context/runtime/common.py` | 当前实现证据 | 记录 `bind_owner_to_public` 在完整 owner schema 校验前读取 evidence 字段。 |
| `trellis/skills/guru-team/runtime/schema.py` 与 `runtime/command.py` | 现有机制和边界 | 复用结构化 `schema_mismatch` 诊断；真实未知异常继续返回 `internal_error/runtime`。 |
| Discovery `references/contract.md`、`SKILL.md`、`interface.json` 与 `examples/` | 当前文档和导航 | 对齐当前 profile、owner-result 版本、示例及恢复指引。 |
| `trellis/presets/guru-team/MIGRATION-718.md` | 迁移合同 | 确认 pre_task 4.0、context_request 2.0、Git-object owner-result 4.0，以及同步来源 owner-result 3.0 的兼容边界。 |
| 归档 Task `08-22-295-sync-discovery-public-handoff` | 历史约束 | 证明 owner-result 3.0 是同步来源的合法兼容资产。 |
| 归档 Task `09-16-421-intake-semantic-owner` | 历史约束 | 证明当前 AI 完成语义审查后调用原 record/check/invoke，不等待不存在的外部 owner。 |

“普通 authoring 装配错误”指调用方按正常流程组装当前 JSON 时产生的缺字段、错字段、漏 required 字段或使用旧版本导航。它不包括恶意伪造、主动篡改、攻击或故意绕过流程。

## 2. 背景与问题

固定基线的 Git-object Discovery record 入口在完整 owner-result schema 校验前调用 `validate_source_evidence`。该函数直接读取 `history_review.deep_reads[*].source`；当正常 authoring 把 `source` 写成 `source_kind` 时，会触发未捕获 `KeyError`，最终由共享 dispatcher 降级为 `internal_error/runtime`，无法指出实际缺失字段。

Discovery 当前合同和 Interface 同时存在版本导航冲突：Interface 选择 pre_task 4.0、context_request 2.0 和 Git-object owner-result 4.0，但部分当前示例、schema id 与合同段落仍指向 3.0、旧 context_request 或其他历史组合。受支持的同步来源 owner-result 3.0 应继续保留，但不得继续被描述为当前 Git-object authoring。

现场还暴露出恢复指引歧义：普通同范围 authoring 错误可以保留首次失败，由原 owner 核对当前来源、真实上游输出和语义审查后，构造正确输入并重新执行原 record/check/invoke。当前文本没有明确区分该恢复路径与真实未分类内部故障的维护 owner 路由，导致正常纠正被误解为必须停止。

## 3. 目标与非目标

整体目标是让 Discovery 公开 record 入口对普通 owner-result 结构错误返回字段级诊断，统一当前 authoring 的版本与示例导航，并明确原 owner 的普通纠正续接。最终实现应复用现有 schema 错误和恢复机制，使有效输入继续通过原 record/check/invoke 得到 `context_ready`。

本 Task 承担以下整体责任：

- 修复 Discovery Git-object owner-result 的校验顺序和结构化错误定位。
- 对齐当前 Skill、合同、Interface、schema 导航和最小示例。
- 明确首次失败保留、普通纠正重跑原链、真实内部故障维护路由的边界。
- 增加聚焦回归并同步 canonical、dogfood 与声明平台投影。

非目标：

- 不重构全局错误框架，不改变 `internal_error` 对真实未知异常的兜底语义。
- 不把 `source_kind` 静默接受为 `history_review.deep_reads[*].source` 的新别名。
- 不放宽 owner-result 必填字段、freshness、schema 或成功门禁。
- 不删除仍受支持的 owner-result 3.0、旧 profile 或历史示例兼容资产。
- 不重演 #793 的完整 Intake，不扩大为通用 Agent 评测、事故重放或固定案例数量。
- 不处理 #772 的历史预览截断或 #363 的遥测上报。
- 不新增 public DTO、wrapper、缓存、审计账本、授权记录或完整安装/升级/Release 矩阵。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与前置条件 | 触发动作 | 可观察结果 |
| --- | --- | --- | --- |
| S1 结构错误诊断 | Guru Intake 的 Discovery owner，使用固定 Git-object baseline 和正常 record envelope | 将 `history_review.deep_reads[0].source` 错写成 `source_kind` 后调用公开 record 入口 | 返回字段级 `schema_mismatch`，指出缺失/非法字段和纠正方式；不返回 `internal_error`，不产生成功门禁。 |
| S2 observation 回归 | 同一 Discovery owner，使用正常 record envelope | 省略 `duplicate_search.candidates[0].observation` | 返回字段级 `schema_mismatch`，现有诊断能力保持稳定。 |
| S3 普通纠正续接 | 原 Discovery owner，首次 authoring 已失败 | 核对同一来源、真实上游输出与仍适用的语义审查，修正普通字段后重新执行原 record/check/invoke | 首次失败保留；修正后的完整输入得到实际 `context_ready`，无需重复无副作用确认，也不把首次失败改写成成功。 |
| S4 当前导航 | 当前 AI 或维护 owner | 从 Interface 选择当前 profile，继续读取合同、schema 和示例 | 能唯一识别 Git-object owner-result 4.0；同步来源 3.0 只作为明确标注的兼容来源。 |
| S5 真实内部故障 | 包维护 owner | 发生无法分类的真实内部异常 | 继续返回 `internal_error/runtime`，保留命令、退出码、stdout 和 stderr，交维护 owner。 |

## 5. 行为要求

### R1 结构优先校验

Discovery 的 Git-object owner-result record 路径必须在读取 reviewed evidence 文件、派生 query/history identity 或访问嵌套 evidence 字段前，完成足够的 owner-result 结构校验。结构缺失或不合法时，使用现有 `schema_mismatch` 合同返回稳定的 `code`、`field_path` 和 `remediation`。

`history_review.deep_reads[*].source` 继续是必填字段。不得新增 `source_kind` 别名，不得用默认值补字段，不得跳过后续 Git evidence freshness 校验。

### R2 当前版本导航

当前 Git-object authoring 明确使用 pre_task 4.0、context_request 2.0 和 owner-result 4.0。同步来源继续使用 owner-result 3.0；旧 versioned schema、example 和合法消费者保持可用，但合同、Interface 与新增示例必须将其标为兼容或历史来源，不能与当前 Git-object 导航并列。

当前示例必须与对应 schema 的机器身份一致。必要共享引用只更新实际承载 Discovery 当前版本、字段和恢复语义的段落。

### R3 同范围恢复

普通同范围装配错误采用以下顺序：

1. 保留首次命令、退出码、stdout、stderr 和失败身份，不改写为成功。
2. 原 owner 重读当前来源、真实上游 public output、当前 schema/example 和仍适用的语义审查。
3. 构造完整正确输入，重新执行原 record/check/invoke。
4. 只有实际 public invoke 成功才产生对应 typed exit。

该过程不需要为无副作用的同范围纠正重复请求继续确认。真实未分类内部故障、来源变化、语义审查失效或外部副作用仍沿各自原 owner 路由处理。

### R4 验证与分发

定向验证必须通过 Discovery 公开 record 入口覆盖 S1-S3：`source`/`source_kind` 错误不再返回 `internal_error`，`observation` 缺失保持字段诊断，纠正后的原链得到实际 `context_ready`。测试不得通过直接调用私有函数替代公开入口。

合同和 Interface 测试必须验证当前 schema 与当前示例的版本一致性，以及 owner-result 3.0 仍被明确保留为同步来源兼容资产。

受影响 canonical、dogfood 和声明平台投影由原安装 owner 同步。验证使用相关 package、canonical/dogfood/platform、sidecar 和 drift 门禁，不要求完整多平台 Throwaway 矩阵。

## 6. 约束与依赖

- Markdown、Skill 与 Interface 定义语义判断；Python 只执行结构校验、事实读取和 recorder/validator 动作。
- 复用 `validate_json` 的结构化诊断；不另建错误分类器或按异常消息文本猜测输入错误。
- `guru-discover-change-context` 继续是 Discovery owner；Clarify、Wording、Readiness 和安装 owner 的职责不合并。
- 任务内不得修改 Trellis 上游源码、全局 npm 安装、`node_modules` 或 hook 来绕过流程。
- 受影响文件必须沿 canonical source 和原安装/升级机制同步，不能只手改受管副本。
- 真实内部故障的安全诊断、secret 脱敏和既有发布边界保持不变。

## 7. 可观察验收与验证方式

| 验收 | 对应要求/场景 | 入口与输入 | 预期可观察结果 |
| --- | --- | --- | --- |
| AC1 | R1、S1 | 固定 Git-object baseline；通过公开 record 入口提交 `deep_reads[*].source` 缺失且出现 `source_kind` 的 owner-result | 退出为非成功；`code=schema_mismatch`；`field_path` 指向 `history_review.deep_reads[0].source` 或字段级精确等价位置；remediation 指向当前 schema/example；不是 `internal_error/runtime`。 |
| AC2 | R1、S2、S3 | 同一公开入口提交缺失 duplicate candidate `observation`；随后提交纠正后的完整输入并执行原 record/check/invoke | 首次返回 `duplicate_search.candidates[0].observation` 字段诊断；纠正后 check 与 invoke 实际返回 `context_ready`；首次失败记录仍保留。 |
| AC3 | R2、S4 | 审核当前 Interface、合同、schema 导航和最小示例 | 当前 Git-object authoring 唯一指向 4.0 组合；3.0 明确标为同步来源兼容；不存在把历史版本写成当前结果的段落或机器导航。 |
| AC4 | R3、S5 | 审核恢复文本并运行相关合同测试 | 普通纠正重跑原链无歧义；真实未知异常仍保留 `internal_error` 维护路由；测试覆盖两层语义。 |
| AC5 | R4 | 运行 Discovery package tests、相关 preset/distribution tests、安装投影与 dogfood drift 检查 | 聚焦测试通过；canonical、dogfood 和声明平台投影一致；无 `.new`/`.bak`、未处理 sidecar 或无关改动。完整安装/升级/Release 矩阵明确保持未验证边界。 |

## 8. 实际未决项

当前没有阻塞整体需求或验收的产品选择。实现机制、文件拆分、测试编排和具体文案由后续 Delivery Planning、Architecture、Approval 与独立 Review 在其职责内完成。

非阻塞边界是：本 Task 只执行普通 Issue 所需的最小可靠验证。若后续发现验收确实需要代表性 clean throwaway，可在同一 accepted scope 内按验证范围 SSOT 执行一个代表性样本；完整多平台矩阵不进入本 Task。
