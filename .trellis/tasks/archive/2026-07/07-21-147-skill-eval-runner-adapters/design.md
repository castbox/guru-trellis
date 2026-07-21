# #147 技术设计：Guru Skill 行为评测基础设施

## 1. 设计原则

1. Interface 1.3 继续拥有 public invocation、input profiles、declared exits 与 per-exit output schema；eval case 只引用，不复制。
2. Corpus 是 package-local 行为输入，不是 public Skill I/O 或普通 invocation context。
3. Runner 实际执行公开 wrapper；静态 schema/数量检查不能产生行为通过。
4. Python/shell 只执行确定性验证与汇总；semantic pass 由外部 AI grader 或 human review 提供。
5. 四个平台共享 corpus 和 protocol bytes，adapter 只翻译 native execution，不拥有 policy。
6. 单次 evidence 位于 repo/package 外临时 workspace，不升级成 gate、checkpoint、审计或发布证明。
7. Canonical source、installed runtime、platform copies、dogfood 与 upgrade/reapply 是一个分发合同。

## 2. 所有权与边界

| Owner | 拥有 | 不拥有 |
| --- | --- | --- |
| `skill-package-contract.md` | Eval corpus、public invocation、grader/adapter/evidence 长期语义 | Active task evidence |
| Eval schema | Corpus/version/case/assertion/file/profile 引用 closed shape | Skill public I/O schema |
| Interface 1.3 | Public input、exact invocation、declared exits、per-exit output schema | Eval expected behavior |
| Package `evals/` | Canonical corpus 与 input fixtures | 平台 fork、runner output |
| Eval discovery | Package/corpus/interface identity 与可执行 locator | 执行或 semantic judgment |
| Eval runner | Isolation、公开 invocation、actual exit、schema、deterministic grading、外部 grading 绑定、status aggregation | 生成 semantic pass、解释浮动 refs |
| Adapter | Native context/Skill/prompt/files/public output/trace translation | Corpus、schema、projection、grader policy |
| Semantic grader/human | Semantic assertion judgment 与 feedback | 修改 deterministic facts |
| Temporary run workspace | Transcript、grading、timing、comparison、feedback | Tracked task/package artifact |
| Extension/preset | Public command、schema/adapter inventory、canonical-to-installed/platform distribution | 重新定义 contract |

## 3. Corpus 合同

### 3.1 路径与 schema

- Canonical path：`<skill-root>/evals/evals.json`。
- Canonical schema：`trellis/skills/guru-team/schemas/skill-evals.schema.json`。
- Schema id：`guru-team-skill-evals-1.0`；JSON Schema 2020-12；所有 object `additionalProperties: false`。
- Representative fixture 可把 schema byte-identical 复制到 fixture schema root，但 production extension inventory 不登记 fixture-only Skill ids。

顶层 shape：

```json
{
  "schema_version": "1.0",
  "skill_name": "guru-example-action",
  "evals": []
}
```

`skill_name` 必须与 package/Interface id 完全一致。`evals[]` 非空，case id 为 stable slug-like string 且 package 内唯一。

### 3.2 Case shape

每个 case 必填：

- `id`：稳定字符串 id；
- `prompt`：传给 adapter 的用户请求；
- `expected_exit`：exact-ref `interface.external_exits[].id`；
- `expected_output`：供 semantic grader/human 理解的说明，不进入 deterministic pass/fail。

以下字段仅在其值非空时出现：

- `input_profile_id`：exact-ref structured public input profile；scalar CLI package 不声明；
- `files[]`：normalized Skill-root-relative regular file，且必须位于 `evals/files/`；
- `assertions`：`deterministic[]` 与 `semantic[]` 不得同时为空。

### 3.3 Assertion grammar

`deterministic[]` 使用 `kind` discriminator，首批闭集：

- `json_path`：RFC 6901 pointer + `exists|equals|contains`；
- `file`：isolated run root 内的 normalized relative path + `exists|json_schema|text_equals`；
- `trace`：invariant id 闭集为 `public_invocation_only`、`evals_not_loaded_by_skill`、`private_runtime_not_read_by_agent`。

Expected exit equality和对应 output schema validation 是 runner 固有门禁，不需要每个 case 重复声明。

`semantic[]` 只包含 stable assertion id、criterion 与 evidence selector。它不包含 pass 字段；外部 semantic grading artifact 按 case/assertion id 单独返回结论。

Human feedback 使用独立 input/result schema，不进入 `assertions`。Legacy `expectations[]` adapter 只把字符串转成待人工确认的 semantic criteria；它不写 canonical corpus，也不自动判定通过。

## 4. Public commands

### 4.1 Discovery

```text
discover-skill-evals --root <repo> --mode <source|installed> --skill <guru-id> --json
```

执行顺序：

1. 使用现有 source/installed package validation；
2. 读取 registry 选择 exact interface schema/state；
3. 要求目标为 Interface 1.3 `minimal_handoff`；
4. 定位固定 corpus path，验证 schema、identity、profile/exit/assertion/file refs；
5. 输出 closed discovery DTO，包含 corpus/schema version、Skill/Interface identity、case ids、public invocation locator、adapter ids 与 capabilities；
6. stable errors 只输出 `code`、`field_path`、`remediation`。

Legacy/no-corpus 返回 stable unsupported contract，不伪造 corpus。

### 4.2 Run

```text
run-skill-evals \
  --root <repo> --mode <source|installed> --skill <guru-id> \
  --adapter <shared|codex|claude|cursor> \
  --run-root <absolute-external-temp-dir> [--case <id>] \
  [--semantic-grading <json>] [--human-feedback <json>] \
  [--current-package <exact-path> --comparison-package <exact-path>] --json
```

`--current-package` 与 `--comparison-package` 必须成对出现，均指向 caller 已解析的 exact package identity；runner 不解析 branch/tag/version alias。

`--run-root` 必须是 repo/package 外的独立目录。Runner 为每个 case/side 创建子目录，不写 package、task 或 repo tracked tree。

## 5. Runner 数据流

```text
registry/interface
       |
       v
discover eval contract ---> validate corpus/profile/exit/files
       |                                  |
       v                                  v
select case ----------------------> immutable adapter request
                                              |
                                              v
                                  shared/codex/claude/cursor adapter
                                              |
                                              v
                             public output + trace + transcript locator
                                              |
                         +--------------------+--------------------+
                         |                                         |
                         v                                         v
             deterministic grader                    external semantic/human input
                         |                                         |
                         +--------------------+--------------------+
                                              v
                                  closed run evidence/status
```

每个 case 的机械顺序固定：

1. 复制 case files 到 isolated context，并保持 corpus bytes 不变；
2. Adapter 加载 exact package，传递 prompt/files；
3. Adapter 调用 Interface 声明的 public wrapper，不读取 runtime source；
4. Runner 解析单一 public DTO，记录 actual exit；
5. Runner 以 actual/expected exit 定位该 exit schema并验证；
6. Deterministic grader 执行 case deterministic assertions 与 trace invariants；
7. 存在 semantic assertions 时，绑定并校验外部 grading；缺失或失败为 `evaluation_failed`；
8. Human feedback 独立附加，不覆盖机械失败；
9. 汇总 status 和 repo 外 evidence。

## 6. Status 与结果模型

### 6.1 Case status

| 状态 | 条件 |
| --- | --- |
| `passed` | Public invocation 成功产生一个 declared exit；exit/schema/deterministic assertions 通过；所有 required semantic assertions 有完整外部 pass |
| `evaluation_failed` | Actual/expected exit mismatch、output/schema/assertion failure，或 required semantic grading 缺失/失败 |
| `execution_error` | Adapter 启动、public invocation、stdout parse、isolation 或 runner execution 失败 |
| `unsupported` | Adapter/native platform 缺失或无法执行声明能力 |

Expected refresh/re-entry/blocked/stop 只要满足 `passed` 条件即为 behavior pass。

### 6.2 Evidence shape

Run evidence 使用独立 closed schema，字段限于：

- case id、corpus/schema version、Skill/Interface version；
- platform、adapter、comparison side/version；
- actual exit、deterministic/semantic assertion results；
- run status、transcript locator、timing、human feedback。

Evidence 不携带 public consumer projection、gate/checkpoint、review readiness、release/checksum/provenance 或审计声明。Corpus byte identity 在 adapter request/trace invariant 中机械验证，不扩展为 authenticity boundary。

## 7. Adapter protocol

### 7.1 Shared request/response

四个 adapter 消费 byte-identical closed request：exact package root、Interface discovery DTO、prompt、case files、isolated workdir、corpus version与目标 platform。Response 仅返回 capability status、public stdout/stderr locator、trace events、transcript locator 和 timing。

Adapter 不返回最终 eval pass；grader 和 runner拥有 status 汇总。

### 7.2 Adapter 实现

- `shared`：使用 caller 提供的 shared execution command；缺失时 `unsupported`。
- `codex`：调用已安装 Codex 非交互入口并显式加载 exact Skill package；CLI/能力缺失时 `unsupported`。
- `claude`：调用已安装 Claude Code 非交互入口并显式加载 exact Skill package；CLI/能力缺失时 `unsupported`。
- `cursor`：调用已安装 Cursor agent 非交互入口并显式加载 exact Skill package；CLI/能力缺失时 `unsupported`。

Native argv 和环境组装留在各 adapter；corpus/schema/grading 位于 shared runtime。测试用 injected fake executable 验证 request/response、byte identity 和状态分类，不依赖开发机已安装全部 CLI。

Canonical adapter descriptors/wrappers 位于 `trellis/skills/guru-team/adapters/eval/`，preset 安装到 `.trellis/guru-team/skills/adapters/eval/`。含 eval corpus 的 Skill package仍按 `platform_destinations` 分发到 shared、Codex、Claude、Cursor roots，测试逐文件验证 corpus bytes 相同。

## 8. Validation 与错误合同

沿用 stable public error shape：

```json
{
  "code": "eval_fixture_outside_root",
  "field_path": "evals.case-id.files[0]",
  "remediation": "Use a normalized Skill-root-relative file below evals/files/."
}
```

Error code family 固定覆盖：schema/version/identity、case duplicate、profile/exit refs、assertion kind/shape、fixture boundary、legacy migration、adapter capability/bytes、comparison pair、external grading binding、run-root boundary、public invocation/output/trace。

## 9. Representative fixture

扩展现有 test-only `representative-active`：

- `guru-example-action`：semantic structured input；normal、repeat/re-entry、blocked cases；
- `guru-example-sync`：deterministic scalar CLI；normal 与非成功 family cases；
- 两个 package 各自持有 `evals/evals.json` 和必要 `evals/files/`；
- fixture extension 登记 eval commands/schema/adapter inventory；production registry 不加入 fixture ids；
- fake shared/Codex/Claude/Cursor executables 执行同一 corpus request，覆盖 passed/evaluation_failed/execution_error/unsupported；
- negative mutations覆盖 PRD 5.2 全矩阵。

## 10. Compatibility 与迁移

- Interface 1.2 bytes/id/legacy semantics 不变。
- Interface 1.3 public I/O 不因 eval case 重复或改写；新增 eval schema/commands 是独立 extension API。
- 九个 production active packages 在 #145/#146 前继续无 corpus、1.2 + `legacy`。
- #145/#146 复用本任务 schema/runner/adapters，为 production packages 添加 corpus并完成 coverage closure。
- Factory `expectations` 仅由 migration adapter 单向读取；不承诺 factory package/release/provenance 兼容。

## 11. Rollout 与 rollback

### Rollout

1. 先落 canonical schema、fixtures 与 validator；
2. 再落 discovery/run runtime、adapter protocol 和 tests；
3. 更新 extension/preset inventory；
4. 同步 dogfood/platform copies；
5. 完成 durable docs 与 full install/update/reapply validation。

### Rollback

- 在 extension public API/version 发布前，可整体移除新增 eval schema/commands/adapters/fixtures，保留 #144 Interface 1.3 不变。
- 若 adapter 存在平台兼容问题，返回 `unsupported` 并阻断对应平台通过，不回退为平台专用 corpus。
- 若 preset reapply 产生 `.new`/`.bak`，停止交付，逐项解决后重新完整验证；不得静默覆盖用户修改。
- 不通过删除 existing Interface/public contract 或修改 production Skill behavior 来回滚 eval infrastructure。

## 12. 中台知识依据

本任务不涉及 go-guru、proto-guru、Unity3D Guru SDK、Flutter Guru SDK 或其它业务中台框架。`middle_platform_knowledge` gate 不适用，不需要 Guru Knowledge Center 检索。

## 13. Docs SSOT Plan

### 13.1 Docs state

`complete_docs`。已检查：

- `.trellis/spec/workflow/skill-package-contract.md`：public Skill package、Interface 1.3、public/private I/O SSOT；
- `.trellis/spec/workflow/companion-scripts.md`：public command、executor/validator/recorder 边界；
- `.trellis/spec/workflow/data-contracts.md`：extension/schema/artifact contracts；
- `.trellis/spec/workflow/quality-guidelines.md`：source/installed/negative/distribution 门禁；
- `.trellis/spec/preset/installer.md`、`.trellis/spec/preset/overlay-guidelines.md`、`.trellis/spec/preset/upstream-ownership.md`：安装、漂移、upgrade 与 ownership；
- `.trellis/spec/docs/public-docs.md`：公开文档同步规范；
- `docs/requirements/README.md`、`requirement-main.md`、`guru-team-trellis-flow.md`：durable requirements SSOT；
- 根 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`：公开安装/使用入口。

### 13.2 Strategy

`ssot_first`。原因：本任务新增长期 public schema、commands、adapter/evidence 与 distribution/upgrade contract，不能只留在 task artifacts。

### 13.3 Affected durable docs

- 更新 `.trellis/spec/workflow/skill-package-contract.md`：corpus ownership、runner/grader/adapter/evidence 与 normal invocation zero-impact。
- 更新 `.trellis/spec/workflow/companion-scripts.md`、`data-contracts.md`、`quality-guidelines.md`：commands、schemas、stable errors、test matrix。
- 更新 `.trellis/spec/preset/installer.md`、`overlay-guidelines.md`；当新增 adapter/schema 路径改变 ownership inventory 时，同时更新 `upstream-ownership.md`。
- 更新 `.trellis/spec/docs/public-docs.md`：三份 public README 的 eval 命令与边界。
- 更新 `docs/requirements/README.md`、`requirement-main.md`、`guru-team-trellis-flow.md`：#147 durable requirement 和 #145/#146 migration sequence。
- 更新根 `README.md`、workflow README、preset README：可执行 discovery/run 示例、安装 inventory 与验证说明。

### 13.4 Task delta merge checkpoint

实现子代理在修改 runtime/schema 前先依据本 plan 更新上述 durable contract；同一 Phase 2 提交中完成代码、测试、安装与文档。`trellis-check` 在 Phase 2 结束前核对 task R1-R12/AC1-AC15 已映射到 durable docs，不把首次 SSOT merge 推迟到 Branch Review 或 finish-work。

### 13.5 Task-history-only content

Intake snapshots、具体 planning approval、逐轮测试命令输出、review findings 生命周期和临时 runner evidence 只保留为 task/runtime evidence，不复制到 durable docs。

### 13.6 Reconciliation evidence

Phase 2 handoff 与 `phase2-check.json` 必须列出：实际更新的 durable docs、task delta 已合并内容、未合并且仅属历史的内容、source/installed/platform/throwaway 验证，以及无 `.new`/`.bak` 结果。

## 14. 关键取舍

| 方案 | 结论 | 原因 |
| --- | --- | --- |
| 复制 factory schema | 拒绝 | 宽松字段、integer id、静态 expectations 无法承载 Interface/typed exit/grader 边界 |
| 把 evals 加入 public input | 拒绝 | 污染普通 invocation 与 consumer contract |
| 平台各持一份 corpus | 拒绝 | 无法保证跨 Agent 行为输入一致 |
| Runner 自动判定 semantic pass | 拒绝 | 违反 AI judgment 与脚本边界 |
| 新增 eval authenticity/provenance | 拒绝 | 超出 honest-but-fallible 正常一致性范围 |
| 用 fake executables 覆盖 adapter integration | 采用 | 能稳定验证 protocol/status/byte identity，同时 native CLI 缺失走 `unsupported` |
