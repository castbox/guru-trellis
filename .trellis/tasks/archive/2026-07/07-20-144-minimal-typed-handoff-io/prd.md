# #144 Guru Team Skill 最小 typed handoff I/O 基础设施

## 1. 目标

建立 Guru Team public Skill I/O 的版本化、机器可发现、可执行验证基础设施，
让调用方只依赖 `SKILL.md`、`interface.json`、package-local public contracts 与公开
CLI help 即可完成输入构造、调用、typed-exit 解析和 consumer handoff。

本任务只交付基础设施和 representative fixtures，不迁移九个现有 production
Skill 的业务 payload。现有 Skill 在 #145、#146 完成前继续使用 interface 1.2 与
`legacy` 状态。

## 2. 权威来源

- GitHub issue：<https://github.com/castbox/guru-trellis/issues/144>，以
  2026-07-20 二次审核修订后的正文为产品需求权威。
- Durable contract：`.trellis/spec/workflow/skill-package-contract.md` 的
  `Public Skill I/O And Private State`。
- 仓库约束：`AGENTS.md`，包括 Markdown 控制流程、脚本只执行确定性事实、
  honest-but-fallible 正常运行边界和完整安装/升级门禁。
- Trellis 官方扩展合同：workflow marketplace 与 spec template marketplace 只作为
  官方扩展边界依据；本任务不修改 Trellis upstream。
- Scope ledger：`.trellis/tasks/07-20-144-minimal-typed-handoff-io/issue-scope-ledger.json`。

## 3. 当前差距

当前 canonical interface 只有 `guru-team-skill-interface-1.2`。它描述 closed-loop
阶段、validator、artifact 和 external exit，但没有独立声明 caller-owned input、
exact invocation、per-exit output、consumer input/projection 与 private artifact 分类。
当前 runtime 和 validator 因此只能验证 1.2 package，extension public API 也只有单个
`interface_schema_id`。

现有 representative fixture 同样是 1.2，只验证静态 interface/schema/example 与
workflow marker；它没有执行 public invocation，也没有证明 output 字段均被 consumer
使用。

## 4. 功能需求

### R1. 版本共存

- 保留现有 `guru-team-skill-interface-1.2` schema id、文件和语义，不原地扩展或
  reinterpret 1.2。
- 新增独立 `guru-team-skill-interface-1.3` schema id 和文件。
- Validator 依据 registry entry 的 exact `interface_schema_id` 选择 schema，不依据
  optional 字段或文件存在状态猜测版本。

### R2. Registry 显式迁移状态

- Registry schema 发布新版本。
- 每个 active entry 必须声明 `interface_schema_id` 和 `io_contract_state`。
- `io_contract_state` 闭集为 `legacy`、`minimal_handoff`。
- `legacy` 只能绑定 1.2；`minimal_handoff` 只能绑定 1.3。
- 九个现有 active entries 在本任务中统一声明 1.2 + `legacy`，typed exits、runtime
  command 和 workflow route 不变。
- Reserved/planned entries 不得携带或安装 production package contract。

### R3. 1.3 public input

- 每个 1.3 Skill 声明一个独立 public input contract。
- Structured input profile 使用 closed JSON Schema；结构不同的 profile 使用
  discriminator + `oneOf`，不得使用 optional/null mega object。
- Deterministic scalar CLI input 声明 exact arguments 与 invocation example，不强制创建
  JSON input schema。
- Public input 只包含 caller-owned 值；Git、GitHub、Trellis facts、digest、path metadata
  和 checkpoint 由 runtime 派生。

### R4. Exact public invocation

- 每个 1.3 interface 声明一个 package-local exact invocation method，包括 command id、
  wrapper、参数/structured input、stdout typed-exit 规则和 error contract。
- 一次调用只返回一个 declared typed-exit DTO。
- 失败输出稳定 error code、field path 与 remediation，不要求调用方读取或 import
  `guru_team_trellis.py`。
- Representative invocation 必须由 validator 真实执行，静态 JSON validation 不能单独
  形成通过结果。

### R5. Per-exit output

- 每个 structurally distinct typed exit 独立拥有 output schema 和完整 example。
- Aggregate `oneOf` 只作为 validator index，不作为 authoring template。
- Public output 仅包含其直接 consumer 完成下一步所需字段。
- 每个 output field 的 direct consumer use 引用必须非空，且每个引用均有测试；
  无人消费字段阻断 package activation。

### R6. Consumer input 与 projection

- `consumer.kind=skill` 绑定目标 Skill 的独立 input contract。
- `consumer.kind=workflow` 绑定唯一 workflow transition-input contract。
- `consumer.kind=stop` 绑定最小 stop-response contract或显式 zero-payload stop。
- Self-reentry 绑定同一 Skill 的独立 re-entry input profile。
- Projection operation 闭集为 direct pass-through、字段选择、重命名、规范化。
- Projection 不得读取 private artifact、重建 semantic judgment 或读取/import runtime
  source。

### R7. Public/private 分层

- 1.3 interface 显式区分 public input、public invocation、typed outputs、consumer
  contracts/projections 和 private artifacts。
- Private artifact kind 闭集固定为 runtime checkpoint 与 gate evidence。
- Persistence boundary 显式覆盖 stdout-only pre-task、task-local tracked artifact 和
  ignored runtime state。
- Audit、checkpoint、debug、完整 live snapshot、review history 和 recovery journal 均归入
  private；只有已命名 consumer 无法完成下一步时所需的最小 identity/freshness token
  才进入 public DTO。

### R8. Contract discovery

- Extension public API 注册 exact command id `discover-skill-contract`。
- 安装 wrapper 提供稳定 help：
  `discover-skill-contract --root <repo> --mode <source|installed> --skill <guru-id> --json`。
- 1.3 discovery output 定位 input、invocation、每个 exit output、consumer contract、
  projection、examples 和 private artifacts。
- 1.2 discovery output 显式返回 `legacy` variant 和迁移状态，不伪造 1.3 contract。
- Unknown skill、version mismatch、路径/schema/example 错误返回稳定 code、field path 和
  remediation。

### R9. Extension public API migration contract

- `supported_interface_schema_ids` 同时列出 1.2、1.3。
- `current_interface_schema_id` 为 1.3，表示新建或实质修改 Skill 的目标合同。
- 兼容 scalar `interface_schema_id` 在 #144 保持 1.2；#146 完成 active registry 零
  `legacy` 后切换为 1.3；移除 scalar 只能由未来独立 breaking-change issue 执行。
- `registry_schema_id` 指向新 registry schema。
- `public_input_schema_ids`、`typed_output_schema_ids`、
  `private_artifact_schema_ids` 是 production active package 的 exact inventories。
  #144 阶段九个 active packages 全部 legacy，因此三个列表为空；test-only fixture 的
  schema ids 只进入 fixture extension，不泄漏到 production manifest。

### R10. Representative mixed fixture

Test-only fixture 集合同时包含：

- 一个 1.2 legacy package，证明迁移期兼容；
- 一个 1.3 semantic structured-input package，覆盖 discriminator/`oneOf`、Skill、
  workflow、stop consumers、self-reentry、direct 与 thin projection；
- 一个 1.3 deterministic scalar-CLI package，证明无 input JSON schema 的合法路径；
- stdout-only pre-task 和 task-local private artifact 分类；
- public invocation 的 passing、不同 exit 和 stable-error cases。

Fixture 不进入 production registry、active Skill ids、platform installation inventory 或
workflow mandatory route。

### R11. Fail-closed negative matrix

Validator 必须拒绝：

- missing per-exit schema/example；
- unknown interface/public I/O field；
- nullable aggregate authoring template；
- unconsumed output field；
- missing consumer input；
- projection 引用 private field 或未知 operation；
- private artifact schema 冒充 public output；
- package public contract 读取/import runtime source；
- 1.2/1.3 identity 与 `io_contract_state` 混用；
- registry/interface/manifest version mismatch；
- 新 active entry 以未授权 legacy 状态进入 production registry；
- reserved/planned entry 安装 package。

### R12. 分发与升级

- Canonical schema、runtime、wrapper、registry、extension manifest、fixture 和 tests 先在
  `trellis/` 下完成。
- Preset installer 分发两个 interface schemas、新 registry、discovery wrapper/runtime 和
  manifest fields。
- 同步 `.trellis/guru-team/` 与 shared/Codex/Claude/Cursor dogfood copies。
- Source、installed、dogfood、selected-platform、clean throwaway、update/reapply 与
  `.new/.bak` 门禁全部通过。

## 5. 范围边界

### 5.1 当前范围

- Interface/registry schemas 与 validator/runtime 基础设施。
- Exact discovery command 与 1.3 representative public invocation。
- Test-only mixed fixtures、negative fixtures 和 distribution tests。
- Extension/preset inventory、durable spec 和 public README 同步。

### 5.2 非目标

- 不迁移 Stage 0、planning、Phase 2、task commit、Branch Review 或 Finish payload。
- 不改变九个现有 active Skill 的 typed-exit 语义或 runtime behavior。
- 不删除现有 task-local gate evidence。
- 不修改 Trellis upstream、全局 npm 包、`node_modules` 或 upstream-owned overlay。
- 不把 semantic judgment 写入 Python/shell。
- 不增加恶意 actor、伪造/篡改、锁、TOCTOU、压力、fault injection、crash consistency
  或跨 OS 原子性机制和测试。

## 6. Issue 处置

- Close：#144。
- Related：#98、#109、#115、#127、#131、#132，只保留引用。
- Follow-up：#145、#146，不在本任务迁移或关闭。

## 7. Docs 状态

- Docs state：`complete_docs`。
- 本任务修改 public schema、registry、runtime command、installer 和 compatibility
  contract，采用 `ssot_first`。
- 权威 Docs SSOT Plan 位于 `design.md` 的 `## 12. Docs SSOT Plan`。
- 需求影响：durable spec、requirements docs、workflow/preset/root README 必须同步
  1.2/1.3 共存、discovery、public/private inventory 和 #145/#146 migration boundary。

## 8. 验收标准

- [ ] AC1：原 1.2 schema id、schema body、九个 active package typed exits 与 runtime
  behavior 保持兼容。
- [ ] AC2：新 1.3 schema 对 public input、exact invocation、per-exit output、consumer
  input/projection、self-reentry 与 private artifacts 使用 closed declarations。
- [ ] AC3：新 registry schema 要求 active entry 显式声明 schema id 与
  `legacy|minimal_handoff`，九个 production entries 为 1.2 + legacy。
- [ ] AC4：1.2 legacy 与 1.3 representative packages 在同一验证运行中通过且被准确区分。
- [ ] AC5：semantic structured input、deterministic scalar CLI、discriminator/`oneOf`、
  三类 consumer、self-reentry、direct/thin projection 全部有 passing fixture。
- [ ] AC6：每个 1.3 output example 通过独立 schema，且每个字段存在 direct consumer
  use；negative unconsumed field 被拒绝。
- [ ] AC7：Representative public invocation 被真实执行，stdout 只含一个 declared
  typed-exit DTO，并由对应 exit schema 复验。
- [ ] AC8：Stable invocation/discovery errors 包含 code、field path 与 remediation。
- [ ] AC9：Projection 不读取 private artifact 或 runtime source；未知或 semantic
  reconstruction operation 被拒绝。
- [ ] AC10：Public/private schema ids 与 persistence boundaries 在 interface、fixture
  manifest、production extension、installed manifest、README 和 durable spec 中一致。
- [ ] AC11：`discover-skill-contract` 进入 extension API、wrapper inventory、source/
  installed validation 和 throwaway/update-reapply smoke。
- [ ] AC12：新 active entry 不能以非 allowlisted legacy 状态激活，reserved/planned
  entry 不能安装 package。
- [ ] AC13：Canonical → installed → selected platform copies byte/mode 一致，dogfood
  drift 为零。
- [ ] AC14：Clean throwaway init、workflow preview/switch、preset install、`trellis update`
  与 reapply 后均通过，最终没有 `.new`/`.bak`。
- [ ] AC15：README 给出的 discovery、source/installed 与 throwaway 命令可执行，不依赖
  本机隐藏状态。

## 9. 完成条件

只有 AC1-AC15 全部获得测试或命令证据，Phase 2 semantic check 无未解决 finding，
Branch Review 覆盖 `origin/main...HEAD` 完整 diff，PR readiness 仍只关闭 #144 时，本任务
才可进入 finish/publish。
