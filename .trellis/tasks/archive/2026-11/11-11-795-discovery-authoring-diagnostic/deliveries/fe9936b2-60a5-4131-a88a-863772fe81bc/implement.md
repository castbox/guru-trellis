# Discovery 普通字段诊断与 authoring 恢复实施计划

## 1. 输入与引用

| 输入 | 用途 |
| --- | --- |
| `.trellis/tasks/11-11-795-discovery-authoring-diagnostic/prd.md` | 整体 accepted scope、R1-R4 与 AC1-AC5。 |
| `deliveries/fe9936b2-60a5-4131-a88a-863772fe81bc/prd.md` | 本批 D795-R1..R4、场景、验收和边界。 |
| `deliveries/fe9936b2-60a5-4131-a88a-863772fe81bc/design.md` 第 3-8 节 | 唯一来源设计处置、实现边界、失败顺序和验证设计。 |
| `deliveries/fe9936b2-60a5-4131-a88a-863772fe81bc/architecture-contribution.md` | Architecture impact、九 concern 和 project-check 责任。 |
| `.trellis/spec/workflow/{workflow-contract,companion-scripts,data-contracts,skill-package-contract,quality-guidelines}.md` | 当前 workflow、脚本、数据、Skill 和验证规范。 |
| `.trellis/spec/workflow/clear-technical-writing.md` | 所有新增/修改自然语言。 |
| `.trellis/spec/workflow/causal-completion-semantics.md` | 根因修复和验证声明边界。 |

实施开始前完整读取上述文件，并确认 TaskId/generation、DeliveryKey、B=`e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e` 与当前 session selection 未变。

## 2. 有依赖顺序的步骤与文件责任

### I795-1 修复 Git-object owner-result 校验顺序

负责文件：`trellis/skills/guru-team/packages/guru-discover-change-context/runtime/common.py`。

前置：Design D795-R1 与 Architecture candidate assessment 已确认。

行为：

- 在 Git-object binder 中先写入只用于 schema shape 校验的固定 canonical query、history preview 和 result identity placeholders；该步骤不读取 archive、source 或 candidate。
- 在调用 `validate_source_evidence`、读取 candidate bytes、history preview 或访问 `live_change.body_sha256` 前，用现有 owner-result 4.0 schema 校验完整 authoring 结构。
- schema 通过后执行现有 source evidence、candidate、transition、preview 和真实 identity/freshness 校验；不改共享 dispatcher。
- 所有错误继续使用现有 `CommandError`/`validate_json`；不新增字段别名、fallback value 或全局异常分类。

完成观察：source/source_kind 与 observation 缺失均产生字段级 `schema_mismatch`，合法输入仍生成完全相同的 4.0 result 身份。

### I795-2 增加公开入口回归

负责文件：`trellis/skills/guru-team/packages/guru-discover-change-context/tests/test_runtime.py`。

前置：I795-1 的接口行为明确。

行为：

- 新建临时 Git repo 和固定 commit，提供归档 history 索引、Docs/code/test evidence 文件与 origin identity。
- 从真实公开 `record-context-discovery.sh` 入口提交 Git-object envelope。
- 覆盖 source/source_kind、duplicate observation 缺失和修正后原 record/check/invoke 成功。
- 在 source/source_kind case 中加入缺失 evidence path；若 evidence reader 抢先执行，结果会是路径/Git 错误。另加 binder 单元 guard，确保 `preview` 与 `source_blob` 在结构失败时没有被调用。
- 断言错误 code、具体 field_path 与 remediation 不暴露原始 payload、绝对本机路径或 credentials。
- 保留既有 sync-source、freshness、active-task、history 和 no-write 测试。

完成观察：新增测试在没有私有函数替身的情况下实际触达公开 record/check/invoke。

### I795-3 对齐当前 schema、示例与 Interface

负责文件：

- `trellis/skills/guru-team/packages/guru-discover-change-context/interface.json`
- `trellis/skills/guru-team/packages/guru-discover-change-context/examples/`
- `trellis/skills/guru-team/packages/guru-discover-change-context/references/contract.md`
- `trellis/skills/guru-team/packages/guru-discover-change-context/SKILL.md`
- `trellis/skills/guru-team/packages/guru-discover-change-context/tests/test_contract.py`

前置：I795-1 的 current schema 选择确定。

行为：

- 新增 current pre_task 4.0、Git-object owner-result 4.0 和 context_ready 5.0 最小示例。
- 更新 Interface 的 current profile/example/schema/artifact id 与路径；旧 3.0、4.0 文件继续保留并明确标为兼容/历史。
- 修正合同中的 current authoring 版本组合，保留同步来源 owner-result 3.0。
- 新增普通 authoring 纠正与真实 internal_error 维护路由段落。
- 合同测试读取 Interface 实际 profile，校验 schema id/path 与 current example 一致；保留旧 3.0 合法性验证。

完成观察：机器导航与 Markdown 导航一致，无 current example/schema 交叉错配。

### I795-4 对齐受影响共享 workflow specs

负责文件：

- `trellis/presets/guru-team/spec/workflow/data-contracts.md`
- `trellis/presets/guru-team/spec/workflow/skill-package-contract.md`
- `trellis/presets/guru-team/spec/workflow/quality-guidelines.md`

前置：I795-3 的 current/legacy 版本组合确定。

行为：

- Data contract 描述 owner-result 3.0（同步来源）与 4.0（Git-object）的当前 union，不把 3.0 删除或称为唯一 current。
- Skill package contract 更新 Discovery 当前 owner-result 描述、示例选择和测试证据。
- Quality guidelines 增加结构先于 evidence、公开入口诊断、纠正后原链成功和受影响投影验证。

完成观察：共享合同不再把 3.0 写成唯一 active，也不把 4.0 与旧 example 混用。

### I795-5 维护 Architecture 当前责任

负责文件：

- `docs/architecture/01-current/system.md`
- `docs/architecture/03-domains/ownership.md`
- `docs/architecture/04-integrations/distribution.md`

前置：Architecture contribution 经 candidate assessment；实际目标单元和写入边界确认。

行为：

- 只在命中的 `ARCH-CUR-*`、`ARCH-DOM-038/039`、`ARCH-INT-001/044/048` 单元补充 Discovery 当前 4.0/3.0 区分、结构诊断先于 evidence、同 owner 纠正重跑和受影响投影。
- 不新增 ADR、GAP、第二 authority、全局版本或逐 Issue 导航登记。
- 最终 integration 才晋升完整正文；实现阶段保留隔离 contribution 和待审拟写。

完成观察：Architecture current 与实际公共合同一致，没有把设计计划写成已实现事实。

### I795-6 同步 dogfood 与声明平台投影

负责 owner：原 preset installer / `guru-upgrade-tools`。

行为：

- 先修改 canonical `trellis/presets/guru-team/` 与 `trellis/skills/guru-team/`。
- 使用当前适用的完整安装/reapply 或工具升级 owner 同步 `.trellis/guru-team/**`、`.agents/**`、`.codex/**`、`.claude/**`、`.cursor/**`。
- 检查 `.new`、`.bak`、managed hash、sidecar、mode 和 dogfood drift。
- 不手改受管副本作为唯一源头，不改无关 Task/session 或上游 Trellis 源码。

完成观察：canonical 与受影响投影字节一致，drift 检查通过，无未处理 sidecar。

## 3. 验证入口、输入与预期观察

| 验证 ID | 命令/入口 | 预期观察 | 关联 |
| --- | --- | --- | --- |
| V795-1 | `python3 -m unittest trellis.skills...` 或 package 测试实际命令，运行新增 Git-object source/source_kind case | `schema_mismatch`，field_path 指向 `history_review.deep_reads[0].source`，非 `internal_error` 或 evidence 路径错误 | D795-AC1 |
| V795-1U | package 单元 guard | `preview` 与 `source_blob` 在结构失败时未被调用 | D795-AC1 的读取顺序边界 |
| V795-2 | 同一 package test，observation 缺失 case | field_path 指向 duplicate candidate observation | D795-AC2 |
| V795-3 | 同一 test 的纠正后 record/check/invoke | check 成功且 invoke 输出正式 `context_ready` | D795-AC3 |
| V795-4 | `test_contract.py` 与 preset distribution tests | current schema/example 匹配，3.0 兼容仍在 | D795-AC4 |
| V795-5 | `test_discovery_stdin_integration.py` 或替换后的链路测试 | 安装后的记录/检查/调用链通过；普通恢复测试可区分 internal fallback | D795-AC5 |
| V795-6 | `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`、managed projection tests、`git diff --check` | canonical/dogfood/platform 一致，无 sidecar，diff 格式通过 | D795-AC6 |

先运行最小改动包测试，再运行 distribution/dogfood 测试；不为普通 Issue 扩张完整多平台 Throwaway 矩阵。若新增 fixture 无法通过公开 wrapper 到达，先修正测试边界而不是直接调用私有函数。

## 4. 停止条件与适用回退点

- 当前 Task/Delivery selection、B、root/Delivery PRD 或 Architecture authority 变化：停止实现，回到对应 generation/stage owner。
- 修复需要新增 public DTO、typed exit、全局错误框架、字段别名或放宽 current schema：回 Author/Architecture/Clarify，不在实现中扩张。
- 公开入口测试仍返回 `internal_error`，或合法输入被诊断拒绝：保留原始 stdout/stderr，修复当前机制后重新跑完整定向测试，不手写 pass。
- 安装 owner 产生用户修改冲突、旧 Task/session 阻塞或 `.new`/`.bak`：按原 owner 诊断处理，不覆盖、不手删。
- 测试基础设施不可用：保留实际失败和未验证范围；不为制造绿色绕过行为断言。
- 定向证据足以覆盖 AC1-AC6、无新增 finding 时停止验证；不追加相同事实的重复 case。

## 5. Delivery Policy（唯一）

Policy：`full`。

本 Delivery 覆盖整体 R1-R4、D795-AC1..AC6 与全部当前 Task 责任；没有剩余后续 Delivery。Delivery 合并不构成 Task Completion。整体 Completion 仍要求本 Delivery 的 Check、独立 committed Review、Publication、Delivery Review/Merge、Completion、Closure、Finish 与 Cleanup 各自按原 owner 成立。

无临时限制。实际安装验证限于当前 repo 和声明的 canonical/dogfood/platform 投影；完整多平台 Throwaway 矩阵与 Release Gate 不在本 Task。

## 6. Docs SSOT Plan（唯一）

Strategy：`ssot_first`。

本轮先更新 canonical package 合同、Interface、schema/example 导航和 `trellis/presets/guru-team/spec/workflow/` 当前 workflow specs，再由原安装 owner 投影到 `.trellis`、Agent/platform 副本。直接 consumer 是未来 Discovery AI、record/check/invoke wrappers、preset installer 和后续 Review。长期 Architecture 责任由 [architecture-contribution.md](./architecture-contribution.md) 经原 Architecture owner 在 final integration 晋升到命中的 CURRENT/DOMAIN/INTEGRATION 单元。

本 Task 不新增独立 RDT contribution，除非原 `guru-maintain-requirements-design-test-ssot` owner 在 Check/Docs reconciliation 中证明新的长期 requirement/design/test 单元存在直接 future consumer。历史正文保持原观察；不直接改写未命中的 shared README/index/manifest。
