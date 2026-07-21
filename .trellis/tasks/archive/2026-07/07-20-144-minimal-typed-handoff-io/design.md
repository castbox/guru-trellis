# #144 技术设计：最小 typed handoff I/O 基础设施

## 1. 设计原则

1. 1.2 是已发布 legacy contract，保持文件、id 和语义不变；1.3 使用独立 schema。
2. Registry entry 是 interface version 与 migration state 的唯一显式选择器。
3. Public DTO 只服务下一 consumer；audit、checkpoint 和 gate evidence 保持 private。
4. 1.3 contract 必须可从 package metadata 与公开命令正向发现和调用。
5. Validator 执行确定性 schema/path/projection/invocation 检查，不做 scope 或 semantic
   judgment。
6. Test fixture 验证未来 migration 机制，不进入 production registry 或安装 inventory。

## 2. 所有权与边界

| Owner | 拥有 | 不拥有 |
| --- | --- | --- |
| `skill-package-contract.md` | Public/private I/O 语义、version migration、consumer/projection 原则 | Active task evidence |
| Interface 1.2 schema | 现有 closed-loop package contract | 新 public I/O 字段 |
| Interface 1.3 schema | Public input/invocation/output/consumer/private declarations | 业务 Skill 的 semantic result |
| Registry schema/registry | Lifecycle、exact interface id、`io_contract_state` | 通过 optional 字段猜测 migration |
| Package | Package-local schemas/examples/wrappers/contracts | Extension 全局 inventory |
| Shared runtime | 确定性 discovery、validation、projection、fixture invocation dispatch | AI Gate、scope、finding、route intent |
| Extension manifest | Public command ids、supported/current schemas、production exact inventories | Test fixture ids |
| Preset installer | Canonical → installed/platform distribution 与 provenance | 重新定义 package semantics |

## 3. 版本模型

### 3.1 Interface files

| File | Schema id | 状态 |
| --- | --- | --- |
| `trellis/skills/guru-team/schemas/skill-interface.schema.json` | `guru-team-skill-interface-1.2` | 原文件保持不变，继续服务 legacy packages |
| `trellis/skills/guru-team/schemas/skill-interface-1.3.schema.json` | `guru-team-skill-interface-1.3` | 新增，承载 minimal handoff contracts |

1.3 package 的 `$schema` 固定为
`../../schemas/skill-interface-1.3.schema.json`；1.2 package 继续使用当前相对路径。
Validator 先读 registry entry，再按 `interface_schema_id` 选 exact schema 和 expected
`$schema`/`schema_version`，不从 interface 内容反推。

### 3.2 Registry

`skill-registry.schema.json` 升级为 schema 1.1，schema id 为
`guru-team-skill-registry-1.1`。Active entry 新增两个必填字段：

```json
{
  "interface_schema_id": "guru-team-skill-interface-1.2",
  "io_contract_state": "legacy"
}
```

关系矩阵：

| `io_contract_state` | `interface_schema_id` | 绑定范围 |
| --- | --- | --- |
| `legacy` | `guru-team-skill-interface-1.2` | #144 中明确登记的九个 production active ids |
| `minimal_handoff` | `guru-team-skill-interface-1.3` | 新增/实质修改的 public Skill 与 test fixture |

Reserved/planned entry 的 shape 保持 lifecycle-only，不增加 package、interface 或 I/O
字段。

## 4. Interface 1.3 模型

1.3 保留 1.2 的 identity、mode、precondition、runtime dependency、stage、validator、
external exit、reentry、test 和 platform fields，并新增必填 `public_contracts`：

```json
{
  "public_contracts": {
    "input": {},
    "invocation": {},
    "outputs": [],
    "consumer_inputs": [],
    "projections": [],
    "private_artifacts": []
  }
}
```

所有 object 使用 `additionalProperties: false`，所有 id 与 package-relative path 唯一。

### 4.1 Public input

`input.kind` 闭集：

- `structured_json`：声明 `profiles[]`。每个 profile 有 id、schema id/path、example
  id/path；两个以上 structurally distinct profiles 必须声明 discriminator field/value，
  aggregate schema 必须使用 `oneOf`。
- `scalar_cli`：声明有序 `arguments[]`、每个 argument 的 flag/type/required 与完整
  `example_argv`；不得声明 input JSON schema/example。

Structured schema/example 均为 package-local regular files，使用 JSON Schema 2020-12、
唯一 `$id`，example 必须通过对应 schema。

### 4.2 Public invocation

`invocation` 固定包含：

- `command_id`：必须存在于 extension `companion_scripts`；representative fixture 使用
  `run-skill-command`。
- `wrapper`：package-local executable regular file，作为调用方 exact entrypoint。
- `input_binding`：引用 structured profile 或 scalar arguments。
- `stdout_contract`：固定 `single_typed_exit`。
- `error_schema` 与 `error_example`：package-local closed error contract，字段固定为
  `code`、`field_path`、`remediation`。
- `example_argv`：不含本机绝对路径或 runtime Python path。

Wrapper 只路由 shared dispatcher，不复制 parser、projection 或 business behavior。

### 4.3 Per-exit output

`outputs[]` 按 `exit_id` 一一对应 `external_exits[]`，每项包含独立 schema、example 和
`consumer_use_ids[]`。Schema 禁止 nullable union 复用 structurally distinct exits。
Aggregate output schema不是必需文件；存在时只能是引用各 per-exit schema 的
`oneOf` index。

### 4.4 Consumer input

`consumer_inputs[]` 是 producer interface 中的引用索引，每项包含独立 id、consumer
identity、owner kind 与 consumer-owned contract locator；producer 不复制 consumer schema：

- Skill consumer：schema/profile 必须定位到 target Skill package 的 public input；
  self-reentry 引用本 Skill不同 profile。
- Workflow consumer：locator 指向 workflow-owned transition contract root；test fixture
  使用 fixture root 的 `consumers/workflow/`，不放入 producer package。
- Stop consumer：locator 指向 workflow-owned 最小 response contract，或
  `payload_kind=zero_payload`；test fixture 使用 `consumers/stop/`，两者互斥。

### 4.5 Projection

每个 output/consumer pair 有且只有一个 projection：

- `direct`：producer output 无需转换即可通过 consumer-owned input schema；producer 与
  consumer schema id 保持各自 ownership，不要求共享 identity；
- `select`：从 public output 选择字段；
- `rename`：选择并重命名字段；
- `normalize`：只执行 schema 声明的确定性规范化操作，首批闭集为 trim ASCII outer
  whitespace、lowercase ASCII enum 和 positive integer canonicalization。

Projection source path 只能引用对应 public output schema properties，target path 只能
引用 consumer input properties。Private artifact、runtime fact、semantic reconstruction、
任意表达式或脚本 path 均不在 grammar 中。

### 4.6 Private artifacts

`private_artifacts[]` 每项声明 id、kind、schema id/path 和 persistence：

- kind：`runtime_checkpoint`、`gate_evidence`；
- persistence：`stdout_only_pre_task`、`task_local_tracked`、`ignored_runtime`。

Public output schema 与 private artifact schema id/path 必须互斥；同一 schema 不能同时
扮演 public output 和 private artifact。

## 5. Representative fixture

现有 `tests/fixtures/representative-active` 演进为 mixed-version fixture，保持 test-only：

```text
representative-active/
  extension.json
  registry.json
  workflow.md
  schemas/
    skill-interface.schema.json
    skill-interface-1.3.schema.json
    skill-registry.schema.json
  consumers/
    workflow/fixture-next.schema.json
    stop/fixture-stop.schema.json
  packages/
    guru-example-legacy/        # interface 1.2 + legacy
    guru-example-action/        # semantic structured 1.3
    guru-example-sync/          # deterministic scalar CLI 1.3
```

`guru-example-action` 使用 `profile=initial|reentry` discriminator 和独立 schemas。
External exits 覆盖：

| Exit | Consumer | Projection |
| --- | --- | --- |
| `completed` | workflow-owned `fixture-next` contract | direct |
| `delegate` | skill `guru-example-sync` | select + rename |
| `retry` | self `guru-example-action:reentry` | normalize |
| `blocked` | stop-owned `fixture-stop` contract | zero payload |

`guru-example-sync` 使用 scalar `--base`、`--remote`，不创建 input JSON schema。它的
wrapper 执行 fixture deterministic handler，stdout 返回一个 declared exit DTO。

Fixture extension 的 production-like inventories 非空并与两个 1.3 packages 一致；
production `trellis/guru-team-extension.json` 的 public/private package schema inventories
保持空数组，因为九个 production active packages 尚未迁移。

## 6. Discovery 与 invocation 流程

```text
caller
  -> discover-skill-contract --mode source|installed --skill <id> --json
  -> registry exact entry
  -> select interface schema by interface_schema_id
  -> validate interface/package-local paths
  -> legacy variant OR minimal_handoff contract index
  -> caller invokes package-local wrapper with documented input
  -> shared dispatcher revalidates extension/package/runtime identity
  -> package handler emits one typed-exit DTO
  -> runtime validates exit schema and declared consumer projection
```

Discovery 只输出 metadata/index，不执行 semantic Skill。Legacy variant 明确报告
`io_contract_state=legacy`、interface identity 和 migration issues `#145/#146`；它不构造
不存在的 input/output contracts。

## 7. Runtime 与 validator 变更

Shared runtime 增加以下确定性能力：

1. `SKILL_INTERFACE_SCHEMAS` version table，包含 1.2 与 1.3 exact id/path/version。
2. Registry 1.1 validation 与 version/state relation check。
3. 1.3 package asset reader，使用现有 lstat/no-symlink/package-boundary helpers。
4. Public input/output/error/private schema dialect/id/path/example validation。
5. Exit ↔ output ↔ consumer input ↔ projection 的全覆盖与唯一性检查。
6. Output field direct-use coverage，拒绝 schema properties 中无 consumer use 的字段。
7. Declarative projection shape/type check，不执行 semantic reconstruction。
8. Representative wrapper execution，捕获 stdout/exit code，按 typed exit 选择 output
   schema复验。
9. `discover-skill-contract` source/installed command 与 stable error object。
10. Legacy allowlist 与 extension inventory consistency check。

`run-skill-command` 保持现有 production behavior。九个 legacy package 不触发 1.3 asset
或 invocation validation，除通用 registry/interface/runtime identity 检查外不改变路径。

## 8. Extension public API

Production `public_api.skill_contracts` 增加：

```json
{
  "interface_schema_id": "guru-team-skill-interface-1.2",
  "supported_interface_schema_ids": [
    "guru-team-skill-interface-1.2",
    "guru-team-skill-interface-1.3"
  ],
  "current_interface_schema_id": "guru-team-skill-interface-1.3",
  "registry_schema_id": "guru-team-skill-registry-1.1",
  "legacy_skill_ids": ["...九个现有 active ids..."],
  "public_input_schema_ids": [],
  "typed_output_schema_ids": [],
  "private_artifact_schema_ids": []
}
```

`public_api.companion_scripts` 增加 `discover-skill-contract`。Installed manifest 必须携带
相同 public API bytes，managed inventory 必须包含 executable discovery wrapper。

Migration timeline：

1. #144：supported = 1.2 + 1.3；current = 1.3；compat scalar = 1.2；九个 legacy。
2. #145：迁移六个 Stage 0 entries，inventory 按 production 1.3 schemas 更新。
3. #146：迁移其余三个 entries，`legacy_skill_ids=[]`，compat scalar 切换为 1.3。
4. Scalar 移除：只能由未来明确 breaking issue 和 extension API version migration 执行。

## 9. Installer 与 dogfood

Preset installer 的 canonical source list 增加 1.3 schema 和 discovery wrapper。它继续：

- 安装 `.trellis/guru-team/skills/` registry、两份 interface schema 和 active packages；
- 安装 `.trellis/guru-team/scripts/bash/discover-skill-contract.sh` 与 shared runtime；
- 安装 active package 到 shared/Codex/Cursor/Claude roots；
- 不安装 `tests/fixtures/**`；
- 对 known upgrade 写 `.bak`，对 unknown local edit 写 `.new` 并 fail closed；
- 写入 installed provenance 后由 installed validator重建 exact inventory。

Canonical 修改完成后运行 preset apply 同步当前 dogfood，再执行 overlay drift 和
`.new/.bak` 检查。Generated installed copies 不作为手工语义源。

## 10. 测试设计

### 10.1 Passing tests

- 原 1.2 schema hash/identity 和九个 active interface contracts 保持可验证。
- Mixed registry 同时验证 legacy 1.2 与 minimal 1.3。
- Semantic structured initial/reentry profiles 与 discriminator `oneOf`。
- Deterministic scalar CLI package 无 input JSON schema。
- 四个 consumer/projection cases 与三类 consumer。
- 每个 output example/schema 和每个字段 direct-use coverage。
- Representative invocation 固定执行两个不同 exits。
- Discovery legacy/minimal variants 与 public help。
- Source/installed facts 对 version/state/schema inventories完全一致。

### 10.2 Negative tests

- 每项 R11 negative matrix 使用独立 fixture mutation，断言稳定 error code。
- Invocation unknown field、wrong profile、handler invalid stdout、multiple/unknown exit、
  output schema mismatch 均失败。
- Discovery unknown skill、mixed version、missing asset、installed drift 均失败。
- Test fixture 出现在 production registry/manifest/install inventory 时失败。

### 10.3 Distribution tests

- Installer unit tests覆盖 managed asset、executable mode、known/unknown upgrade 和
  fixture exclusion。
- Source/installed/dogfood/platform checks 覆盖新 schema、registry fields、command。
- Throwaway install 首轮与 update/reapply 后各执行 discovery legacy smoke、source/
  installed validation 和 mixed fixture contract tests。

## 11. 兼容、失败与回滚

- Legacy compatibility：validator 不要求 1.2 package 新增 public contracts；现有
  wrapper/runtime commands 不变。
- Normal stale/mismatch：schema/manifest/registry/package 任何 identity drift 立即非零，
  error 只含 repo-relative field path 与 remediation。
- Rollback checkpoint 1：1.3 schema/fixture未通过时，只回退 1.3新增文件和 validator
  delta，1.2不受影响。
- Rollback checkpoint 2：installer/dogfood未通过时，不提交 installed copies，修复
  canonical source后重新 apply。
- Rollback checkpoint 3：throwaway/update失败时阻止发布，不用跳过门禁或删除用户未知
  修改。
- 不引入锁、原子写、hostile-input defense 或跨 OS recovery。

## 12. Docs SSOT Plan

### 12.1 状态与策略

- Docs state：`complete_docs`。
- Strategy：`ssot_first`。
- Reason：本任务修改 public interface/registry schema、runtime command、extension API、
  installer 和 migration contract；durable contract 必须先稳定，代码和 generated copies
  再承接。

### 12.2 Durable targets

| Contract | Durable paths |
| --- | --- |
| Product requirements | `docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`、`docs/requirements/README.md` |
| Skill I/O/version/consumer | `.trellis/spec/workflow/skill-package-contract.md` |
| Registry/artifact data | `.trellis/spec/workflow/data-contracts.md` |
| Public commands/runtime | `.trellis/spec/workflow/companion-scripts.md` |
| Validation/fixture/gates | `.trellis/spec/workflow/quality-guidelines.md` |
| Navigation | `.trellis/spec/workflow/index.md` |
| Public installation/use | `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` |

### 12.3 Merge checkpoint

Phase 2 check 前必须完成：durable docs → canonical schema/runtime/fixture → registry/
extension/installer → dogfood copies → source/installed/platform/throwaway/update-reapply
证据的一致性核对。

Task history only：Phase 0 临时 evidence、plan confirmation digest、sub-agent liveness、
逐轮 finding、命令原始输出。它们不合并进 durable docs。

## 13. 安全与部署影响

- 输出不得包含 token、secret、private key、`.env`、数据库 URL、签名 URL、本机绝对
  路径或用户数据。
- 本任务不新增服务、数据库 migration、queue、schedule、容器、Kubernetes、
  Dockerfile、Compose、Kustomize 或 Makefile 行为。
- CI/CD 发布流程保持不变；测试运行时间增加来自 mixed fixture invocation 与 throwaway
  discovery smoke。
- Middle-platform Knowledge Gate 不适用：本任务不涉及 go-guru、proto-guru、Unity、
  Flutter 或中台 SDK/framework contract。

## 14. Provenance matrix

| ID | Load-bearing contract | Covered requirements/acceptance | Class | Authority / choice |
| --- | --- | --- | --- | --- |
| P1 | 保留 1.2 并新增独立 1.3 | R1；AC1、AC2 | `explicit_requirement` | Issue #144 二次修订“Interface 与 registry 分阶段迁移” |
| P2 | Registry exact version/state，九个 active 保持 legacy | R2；AC3、AC4 | `explicit_requirement` | Issue #144 二次修订与 #145/#146 boundary |
| P3 | Structured/scalar caller-owned minimal input | R3；AC2、AC5 | `explicit_requirement` | Issue #144 目标 1、6 与 public invocation 修订 |
| P4 | Exact invocation真实执行并返回单一 exit | R4；AC7、AC8 | `explicit_requirement` | Issue #144“Public 正向调用方法” |
| P5 | Per-exit output 与 direct consumer use | R5；AC6 | `explicit_requirement` | Issue #144 目标 2、4 与验收 |
| P6 | 三类 consumer、self-reentry、projection闭集 | R6；AC5、AC9 | `explicit_requirement` | Issue #144“Consumer contract 类型” |
| P7 | Public/private artifacts 与 persistence 分层 | R7；AC10 | `explicit_requirement` | Issue #144 目标 4、5 与 fixture要求 |
| P8 | Exact discovery command | R8；AC8、AC11、AC15 | `explicit_requirement` | Issue #144 目标 7 与增补验收 |
| P9 | Extension migration fields与scalar timeline | R9；AC10 | `necessary_implementation_choice` | 选择 supported/current + legacy scalar；替代原地切换或立即移除，保持1.2 consumer兼容且不扩张产品scope |
| P10 | Mixed test-only fixture，不进入production registry | R10；AC4、AC5、AC7、AC12 | `necessary_implementation_choice` | 选择扩展现有 representative fixture；替代新增production Skill或只做动态临时fixture，满足完整验证且不扩张产品scope |
| P11 | Fail-closed negative matrix | R11；AC6、AC8、AC9、AC12 | `explicit_requirement` | Issue #144“基础设施 fixture 与负例” |
| P12 | Canonical/install/platform/throwaway/update完整门禁 | R12；AC11、AC13、AC14、AC15 | `explicit_requirement` | Issue #144验收与仓库AGENTS开箱即用门禁 |
| P13 | Production schema inventories在#144保持空，fixture manifest非空 | R9、R10；AC10 | `necessary_implementation_choice` | 选择production exact inventory；替代泄漏test ids或伪报legacy schemas，保持manifest真实性且不扩张产品scope |
| P14 | Docs采用 `ssot_first` | Docs SSOT Plan；AC10、AC15 | `necessary_implementation_choice` | 选择先稳定durable public contract；替代delta-first，降低跨schema/runtime/docs漂移且不扩张产品scope |
| P15 | #145/#146迁移与异常加固不进入当前实现 | Scope 5.2；AC1、AC3 | `explicit_requirement` | Issue #144非目标、scope ledger与AGENTS正常运行边界 |

当前 matrix 无 `approved_scope_expansion` 或 `out_of_scope_proposal` entry。P1-P15 覆盖
全部 R1-R12、AC1-AC15、实现顺序、兼容、验证、Docs SSOT 和 rollback obligations。
实施中发现新的 load-bearing contract 时，先更新三份 planning artifacts、matrix 与 wording
evidence，再重新取得 post-planning approval。
