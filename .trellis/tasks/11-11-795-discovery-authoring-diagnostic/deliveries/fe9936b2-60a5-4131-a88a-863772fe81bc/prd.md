# Discovery 普通字段诊断与 authoring 恢复

## 1. 整体来源与术语

整体 accepted scope 是 `.trellis/tasks/11-11-795-discovery-authoring-diagnostic/prd.md`，其 authority revision 为 `sha256:0352dc119fc4403116b57243f56e636a6239c885c741190121147890f9347f2a`。本 Delivery 的 `planning_root` 是 `deliveries/fe9936b2-60a5-4131-a88a-863772fe81bc`，覆盖整体要求 R1-R4 与 AC1-AC5；首次交付，没有前序 Delivery。

| 来源 | locator 与章节 | 角色 | 本批用途 |
| --- | --- | --- | --- |
| Issue #795 | `issue:castbox/guru-trellis#795`；“根因与证据边界”“目标与范围”“最小验收”“关联与非目标” | 要求与现场证据 | 确定三个差额、验收和排除项。 |
| 整体 PRD | `.trellis/tasks/11-11-795-discovery-authoring-diagnostic/prd.md`；第 2-8 节 | 已接受整体需求 | 本 Delivery 的唯一整体范围和验收基线。 |
| Discovery 当前合同 | `trellis/skills/guru-team/packages/guru-discover-change-context/references/contract.md` | 当前实现合同 | 定位版本导航和恢复语义冲突。 |
| Discovery 当前实现 | `trellis/skills/guru-team/packages/guru-discover-change-context/runtime/common.py` | 当前代码证据 | 修复 evidence 读取与 schema 校验顺序。 |
| 共享 schema 诊断 | `trellis/skills/guru-team/runtime/schema.py` | 当前机制 | 复用 `code`、`field_path`、`remediation`。 |
| Discovery Public Interface | `trellis/skills/guru-team/packages/guru-discover-change-context/interface.json` | 公共 API 导航 | 对齐 profile、schema、artifact 与 example 版本。 |
| #718 迁移合同 | `trellis/presets/guru-team/MIGRATION-718.md` | 已接受兼容约束 | 区分 Git-object 4.0 与同步来源 3.0。 |
| 归档 #295、#421 | `.trellis/tasks/archive/2026-08/08-22-295-sync-discovery-public-handoff/finish-summary.json`、`.trellis/tasks/archive/2026-09/09-16-421-intake-semantic-owner/finish-summary.json` | 历史约束 | 保留合法 3.0 和原 owner 重跑原链的语义。 |

“公共 record 入口”指 `guru-discover-change-context` 的 `record-context-discovery` wrapper。本 Delivery 中的“纠正后原链”固定为同一来源和同一 owner 下的 record、check、invoke。

## 2. 整体与本批目标、非目标

整体问题是 Discovery 对普通 owner-result 结构错误诊断不足，当前版本导航冲突，普通同范围恢复边界不清。本 Delivery 独立交付完整修复：Git-object owner-result 在依赖字段读取前进行结构校验；当前 Interface、合同与示例唯一导航到 4.0；同步来源 3.0 继续明确兼容；普通 authoring 纠正保留首次失败并重跑原链。

本批覆盖整体 R1-R4 和 AC1-AC5，没有剩余未分配能力。整体 Completion 依赖本 Delivery 的规划、实现、完整检查、独立 Review、发布与交付结果，以及 Completion/Closure/Finish 分别成立。

非目标保持整体 PRD：不改全局错误框架，不静默接受 `source_kind` 别名，不放宽 schema/freshness，不删除 3.0 兼容资产，不重演 #793，不处理 #772 或 #363，不新增 public DTO 或完整安装矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

本批从 `main@e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e` 开始，首次交付，没有前序 Delivery。当前分支和 worktree 只承载 Task 管理，未修改实现。

固定基线已经证明：

- `bind_owner_to_public` 在完整 owner schema 校验前调用 `validate_source_evidence`，缺失 `deep_reads[*].source` 时抛出未捕获 `KeyError`，公开 wrapper 最终返回 `internal_error/runtime`。
- 缺失 duplicate candidate `observation` 当前已经返回字段级 `schema_mismatch`；本批需要回归保护。
- 当前合同和 Interface 的 3.0/4.0 导航仍冲突；同步来源 owner-result 3.0 是合法兼容资产。
- 当前恢复文本仅概括 same-scope recovery，未清楚区分普通结构纠正重跑原链与真实未知 runtime 故障。

实现依赖现有 schema validator、错误投影、record/check/invoke 入口、canonical package 和 preset 安装机制。安装投影由原 owner 同步，不在本批手工维护业务数据。能力完成后，本 Delivery 直接支撑整体 Completion；没有延后到后续 Delivery 的实现或验证责任。

## 4. 本批调用方、场景与流程

| 场景 | 调用方与前置条件 | 触发动作 | 处理行为 | 可观察结果 |
| --- | --- | --- | --- | --- |
| D795-S1 | Intake Discovery owner；固定 Git-object baseline | 通过公开 record 入口提交缺失 `deep_reads[*].source`、出现 `source_kind` 的 owner-result | 先校验 owner-result 结构，停止依赖字段读取 | 返回 `schema_mismatch`，定位 source 字段并提供当前 schema/example 纠正说明。 |
| D795-S2 | Intake Discovery owner；正常 record envelope | 省略 duplicate candidate `observation` | 执行同一 owner-result schema 校验 | 字段诊断保持可定位，不被泛化为 runtime 错误。 |
| D795-S3 | 同一 Discovery owner；首次普通 authoring 已失败 | 核对同一来源、真实上游输出和语义审查，修正输入后重跑原 record/check/invoke | 每次使用完整当前输入；首次失败保留 | check 与 invoke 实际得到 `context_ready`；首次失败不被改写。 |
| D795-S4 | 当前 AI 或维护 owner | 从 Interface 导航当前 Git-object authoring | 选择 pre_task/context_request 与当前 schema/example | 唯一得到 owner-result 4.0；3.0 只作为同步来源兼容。 |
| D795-S5 | 包维护 owner | 遇到真实未知异常 | 不将其归类为普通字段错误 | 保留 `internal_error/runtime` 与维护方向。 |

## 5. 完整行为、条件与约束

### D795-R1 结构诊断先于证据读取

当 Git-object owner-result 进入公开 record 流程时，实现必须先完成足以覆盖 AI-authored 结构与必填字段的 owner schema 校验，再读取 reviewed blob、history deep-read locator 或生成 result identity。失败返回现有结构化诊断；通过后才执行现有 Git evidence、history、candidate、freshness 和 identity 校验。

`history_review.deep_reads[*].source` 继续是必需 discriminator。`source_kind` 只作为错误输入证据，不获得别名兼容。缺失 `duplicate_search.candidates[*].observation` 继续由同一 owner schema 诊断。任何结构失败都不产生 check pass 或 public success。

### D795-R2 当前导航与兼容资产

当前 Git-object authoring 导航组合是 pre_task 4.0、context_request 2.0、owner-result 4.0。当前 Git-object 示例必须与 4.0 schema 匹配；当前 public output 示例和 schema id 必须与 5.0 输出一致。

同步来源 owner-result 3.0、公开旧 profile 和旧示例继续保留在明确命名的兼容/历史位置。Interface 继续暴露其合法 consumer，但当前 profile 的 example/schema 不得指向彼此不匹配的版本。

### D795-R3 普通纠正恢复

首次普通 authoring 失败先保留。原 owner 重读同一来源和上游输出，确认仍需的语义审查未失效，然后构造完整正确输入，重新执行原 record/check/invoke。该同范围、无外部副作用的纠正不要求额外确认；只有实际 invoke 成功产生正式 typed exit。

来源、基线、目标或语义审查变化，真实未知内部异常，以及任何外部副作用各自保留原 owner 路由。不得修改 runtime 或手写 pass 以掩盖失败。

### D795-R4 聚焦验证与安装投影

通过公开 record 入口复现 S1/S2，修复后核对字段路径与错误码；用纠正后的完整输入执行 S3 并得到 `context_ready`。合同测试核对当前 schema/example 和 3.0 兼容说明。原安装 owner 同步 canonical、dogfood、声明平台和必要共享 spec；运行 package tests、distribution tests 与 dogfood drift。

本 Delivery 不要求完整 Throwaway 多平台矩阵、升级/Release 或 #793 重演。若实现中发现当前 accepted scope 必须依赖一个代表性 clean install，则只执行一个定向样本并记录边界。

## 6. 本批验收、验证方式与未决项

| 本 Delivery 验收 | 整体 AC | 验证入口与输入 | 预期观察 |
| --- | --- | --- | --- |
| D795-AC1 | AC1 | 公开 record 入口；Git-object envelope 中 `deep_reads[0].source` 改为 `source_kind` | 非零结构失败；`schema_mismatch`；字段路径精确指向 source；不出现 `internal_error`。 |
| D795-AC2 | AC2 | 公开 record 入口；删除 duplicate candidate observation | 返回 observation 字段路径；当前诊断能力保持。 |
| D795-AC3 | AC2/AC4 | 同一公开入口；纠正后完整 owner-result 执行 record/check/invoke | record/check 成功，public invoke 实际返回 `context_ready`；首次失败仍为独立事实。 |
| D795-AC4 | AC3 | Interface/合同/schema/example contract tests | 当前 GitHub-object 路径唯一指向 4.0 组合；3.0 被标为同步来源兼容；旧资产仍存在且合法 consumer 未删除。 |
| D795-AC5 | AC4 | 合同测试和代码审查 | 普通纠正重跑原链写清；真实 internal_error 维护路由仍在。 |
| D795-AC6 | AC5 | package、preset 与 distribution tests，以及 drift 检查 | 聚焦测试通过；投影一致；无未处理 sidecar；未验证矩阵边界明确。 |

当前没有阻塞需求或验收的产品选择。具体 schema 预校验实现方式已由 readiness 的 solution-mechanism qualification 判定为应用层合同；精确代码结构、测试 fixture 和安装文件清单在后续 design/implement 中完成。

## 7. Canonical 引用与本轮差额

| Canonical authority | 位置 | 本批用途 | 本轮差额 |
| --- | --- | --- | --- |
| Skill package contract | `trellis/presets/guru-team/spec/workflow/skill-package-contract.md` 的 Discovery current contract 段 | 约束 Interface、schema、owner-result、public DTO 和安装投影 | 修正 3.0/4.0 当前导航；保留合法兼容。 |
| Data contracts | `trellis/presets/guru-team/spec/workflow/data-contracts.md` 的 Change Context Discovery Result 段 | 约束 Discovery owner-result 版本和输入事实 | 对齐 current 4.0 与同步来源 3.0。 |
| Companion scripts | `trellis/presets/guru-team/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` | 约束中间 receipt、正式 typed exit 与错误分类 | 记录普通 authoring 校正与未知 runtime 故障边界。 |
| Quality guidelines | `trellis/presets/guru-team/spec/workflow/quality-guidelines.md` 的 Discovery test contract 段 | 约束定向验证和分布证据 | 更新当前版本选择并增加错误顺序、原链恢复覆盖。 |
| Architecture current system | `docs/architecture/01-current/system.md` 中 Discovery/Skill package ownership 单元 | 确认 owner、consumer 和公共合同边界 | 只维护真实受影响的 Discovery 当前关系，不新增全局版本。 |
| Architecture distribution | `docs/architecture/04-integrations/distribution.md` 中 Discovery and managed projection 单元 | 确认 canonical/dogfood/platform 分发边界 | 更新受影响投影；完整矩阵保持未验证。 |
