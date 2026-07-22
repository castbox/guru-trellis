# #145 需求：迁移 Guru Team Stage 0 Skills 到最小 typed handoff I/O

## 1. 目标

把 Guru Team Stage 0 完整 production graph 的六个 active Skills、24 个稳定 typed exits
从 `guru-team-skill-interface-1.2` + `legacy` 原子迁移到
`guru-team-skill-interface-1.3` + `minimal_handoff`。迁移后，普通 Agent 只需要读取
package 的公开 Interface、公开 wrapper 与最小 handoff DTO，不再把 32-150 个 scalar 的
private artifact 当作输入模板，也不读取或 import `guru_team_trellis.py` 计算 projection、
linkage、digest 或 path metadata。

本任务消费 #144 已发布的 Interface 1.3、registry 1.1、contract discovery 与
direct/select/rename/normalize projection 基础，消费 #147 已发布的 eval schema、runner、
grader 与四平台 adapter。#145 当前 GitHub authority 已确认两项 production compatibility
修订：补齐 Interface 1.3 optional scalar，以及补齐真实 semantic package 经既有 eval
runner/adapter 执行的闭环。两项修订均属于完成本任务原有 Stage 0 delivery unit 的必要范围。

## 2. 当前权威与范围修订

权威来源为 [#145 comment 5037168364](https://github.com/castbox/guru-trellis/issues/145#issuecomment-5037168364)，
其内容已按 `exact_source_action_and_scope` 确认并 live reread；action digest 为
`daa17d1458eab48e170fbc9c48b6167152d73018c57d929544690a54b4b6dd2e`。

### D1. #144 Interface 1.3 optional scalar

Proposal digest：`b0f134e6b53061ca4390e45a6dcf79edf020ef43e2fef57e0ed03f08278eb5be`。

- `scalarArgument.required` 的 schema 从常量 `true` 改为必填 boolean；每个 scalar
  argument 仍须显式声明 `required: true|false`。
- `guru-sync-base` 的 `--base-branch` 声明 `required: false`。调用方省略该 flag 时，public
  wrapper 把未指定状态交给 owner resolver，owner 按现有固定顺序解析 base；显式传参的
  语义、优先级和结果保持不变。
- 修改面限制为承接该行为所需的 Interface 1.3 schema、validator、fixtures、public
  invocation/dispatch、tests 与文档；#144 的其它基础设施合同不变。

### D2. #147 production semantic eval runner/adapter 闭环

Proposal digest：`a2c902d92d3650c6431088b3f7e660b5bfb4a6f0123e7af7abcfaf40c5a1504a`。

- Runner 执行真实 package public wrapper。Semantic wrapper 只能从 repo-local、owner
  checker 已通过的 result 取得 actual typed exit，并由 actual exit 选择对应 output schema。
- Case `expected_exit` 只在 wrapper 返回后参与 expected-vs-actual assertion；不得用于选择
  owner result、构造 wrapper 输出、决定实际 route 或选择被测 schema。
- 同一 canonical corpus 覆盖 shared adapter parse/execute、Codex trusted Git context、
  Claude input protocol、Cursor unavailable/unsupported，以及 checker-passed repo-local
  owner result。
- 只修改 production package 执行闭环所必需的 runner、adapter、public dispatch、validator、
  fixtures、tests 与文档；eval schema、grader policy、run evidence contract 与 semantic
  ownership 不变，不生成平台专用 corpus。

## 3. 迁移 manifest

迁移集合必须精确为下表的 6 Skills、24 exits；source、installed、workflow markers、
registry、extension inventory 与 migration manifest 的集合必须完全相同。

| Skill | judgment mode | Typed exits |
| --- | --- | --- |
| `guru-sync-base` | `deterministic` | `synced`、`skipped`、`blocked` |
| `guru-discover-change-context` | `semantic` | `context_ready`、`refresh_base`、`blocked` |
| `guru-clarify-requirements` | `semantic` | `clear`、`needs_context`、`refresh_context`、`retarget_context`、`new_task`、`blocked` |
| `guru-review-contract-wording` | `semantic` | `pass`、`content_changed`、`blocked` |
| `guru-review-change-request` | `semantic` | `ready`、`clarify_requirements`、`review_wording`、`refresh_context`、`blocked` |
| `guru-create-task-workspace` | `semantic` | `created`、`refresh_review`、`cancelled`、`blocked` |

Missing、extra、renamed、unknown、duplicate 或顺序外 activation entry 均失败关闭。

## 4. 功能需求

### R1. Interface 与 registry 原子迁移

- 六个 production registry entries 必须同时声明
  `interface_schema_id=guru-team-skill-interface-1.3` 与
  `io_contract_state=minimal_handoff`。
- 六个 package Interface 必须使用 1.3 `public_contracts`，保留 stable Skill id、mode id、
  judgment mode、ordered stages、entry precondition、typed exit id、consumer id、semantic
  owner、human confirmation 与副作用边界。
- `guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit` 必须继续保持
  `guru-team-skill-interface-1.2` + `legacy`；其迁移由 #146 独占。
- Extension 的 `legacy_skill_ids` 必须精确收敛为上述三个 #146 Skills；active Skill 总数
  仍为 9，reserved/planned lifecycle 不变。

### R2. Public input 与 exact invocation

- 每个 Skill 独立声明 workflow/standalone public input；相同结构可共享 schema/signature，
  结构不同的 mode、profile、target kind、initial、re-entry 与 recovery path 必须使用
  discriminator + closed `oneOf` 或独立 profile schema。
- `guru-sync-base` 使用 scalar CLI input；不得为形式对称新增 input JSON schema。
- Interface 1.3 的每个 `scalarArgument` 必须显式记录 boolean `required`。`base_branch`
  必须记录 `required:false`，public invocation 必须同时覆盖携带和省略 `--base-branch`
  两条路径；省略路径复用 owner 的固定 resolver order，wrapper 不得另建 fallback 逻辑。
- Structured input 只包含 caller-owned request、route、target、profile、confirmation 或
  continuation 值。Git/GitHub/Trellis live facts、digest、hash、size、mtime、绝对 artifact
  path 与 checkpoint 必须由 runtime 读取或派生。
- 每个 structurally distinct input profile 必须有完整 validator-passing example 和真实
  public invocation probe；一次 invocation 只返回一个 declared typed-exit DTO。
- Stable error 必须使用 #144 已发布的 `code`、`field_path`、`remediation` 合同；调用方
  不得读取 private Python source 诊断公开调用。

### R3. Per-exit output 与 consumer input

- 24 个 exits 分别拥有独立 closed output schema、完整 example、唯一 consumer input/stop
  contract、一个 declarative projection 和非空 `consumer_use_ids`。
- Public output 仅包含直接 consumer 完成下一步所需的 route discriminator、caller-owned
  continuation、语义结论或最小 identity/freshness token。
- Audit、完整 scan/history、review metadata、debug、file metadata、runtime-derived digest、
  recorder facts 与 recovery journal 不得进入 public output。
- 每个 output field 必须通过 field-to-consumer-use assertion 证明被目标 consumer 直接
  使用；无人消费字段、只供审计字段或依赖 private artifact 的字段阻断 activation。
- `consumer.kind=skill` 必须绑定目标 package 的 exact public input profile；
  `consumer.kind=workflow` 必须绑定 consumer-owned workflow JSON schema；
  `consumer.kind=stop` 使用最小 stop schema或显式 `zero_payload`。

### R4. Projection 与 re-entry

- Producer output 到 consumer input 的 operation 闭集为 #144 的 `direct`、`select`、`rename`、
  `normalize` operation；不得新增任意表达式、脚本、semantic reconstruction 或 private
  artifact lookup。
- Refresh、retarget、`content_changed`、created-issue refresh、blocked、cancelled 与
  self-reentry 保持当前 stable exit id、唯一 consumer 与 semantic owner。
- `guru-review-contract-wording` 的 `pass`/`content_changed` 必须携带 consumer router
  直接使用的 fixed profile discriminator；router 不重新判断语义。
- Re-entry input 必须重新读取 live facts并验证 freshness；不得从 public output恢复完整
  private artifact。

### R5. Public/private artifact 边界

- 六个 Interface 必须把现有 recorder/checker artifacts 明确登记为
  `runtime_checkpoint` 或 `gate_evidence`，并声明
  `stdout_only_pre_task`、`task_local_tracked` 或 `ignored_runtime` persistence。
- Pre-task 和 standalone 继续 stdout-only/repo side-effect-free；不得新增 repo-level
  cache、tracked runtime、workspace journal 或跨 Skill共享 artifact。
- `context-discovery.json`、`contract-wording-review.json`、`issue-review.json`、
  `task-workspace-plan.json`、`task-workspace-result.json` 这些现有 artifact schema 继续是
  private evidence；迁移不追溯重写 archived task artifacts。
- GitHub issue、worktree、branch 与 Trellis task mutation 继续由
  `guru-create-task-workspace` 独占，且 issue-only 与 workspace/task mutation 仍互斥。

### R6. Versioned activation 与兼容

- 新增一个 closed Stage 0 migration manifest，精确登记 6 Skills、24 exits、Interface
  version、input profile ids、output/consumer/projection ids、eval case bindings 与 activation
  unit version。
- Preset installer 必须在一次 transaction 中安装完整六包 graph、registry、manifest、
  schemas、wrappers 与平台 copies；不得发布 mixed 1.2/1.3 Stage 0 graph。
- 如果 installer 的一次 transaction 无法保证 consumer 全部 current，必须使用显式
  versioned public DTO adapter；adapter 只转换 public DTO，不读取 private artifact、不重放
  semantic judgment，并在六个 registry entries 全部激活 1.3 后删除。
- Existing active state 必须通过受支持的 re-entry/adapter 路径继续；pre-#145 archived
  artifacts 保持只读且可由现有 schema读取。
- 破坏性 schema 变化必须发布新 schema id；不得静默 reinterpret 旧 artifact 或 public
  DTO。

### R7. Package-local behavior cases

- 每个 production Skill 必须维护唯一 canonical `evals/evals.json`，使用 #147 的
  `guru-team-skill-evals-1.0`；eval schema、grader policy、semantic ownership 与 run
  evidence contract保持不变。
- Migration manifest 中每个 24 exit id 绑定一个或多个 current case id，每个 input profile
  绑定一个或多个 case id；同一 case 同时覆盖 profile 与 exit 时不得制造重复 case。
- Cases 只记录 prompt、input profile ref、fixture refs、`expected_exit` 与 load-bearing
  assertions；Interface output schema、consumer projection 与 private artifact只 exact-ref，
  不复制。
- Coverage 必须包含 normal、refresh/re-entry、blocked/stop、retarget、content-changed、
  issue-only creation/recovery 与 workspace/task creation family。
- Shared、Codex、Claude、Cursor adapters 必须读取同一份 package corpus bytes；不得生成
  平台专用 corpus。
- Shared runner 必须解析并执行真实 public wrapper；semantic package 必须使用当前 repo
  中 checker-passed owner result。Runner 先取得 actual exit，再按 actual exit 校验 output
  schema，最后把 `expected_exit` 作为预期断言比较。
- Adapter compatibility 必须覆盖 Codex trusted Git context、Claude input protocol、Cursor
  unavailable/unsupported 与 shared parse/execute。上述兼容修复不得复制 grader policy、
  重判 semantic route 或把 `expected_exit` 传给被测 wrapper。

### R8. 正常 Agent 与 runtime 边界

- 正常 workflow/standalone transcript 与 eval runner trace 均必须证明 Agent 未读取/import
  private runtime source。
- Runtime 自行读取 live Git/GitHub/Trellis facts，生成 projection、digest 与 path metadata；
  Agent 只填写 caller-owned public input和 semantic gate结论。
- Python/shell 继续只做 executor、validator、recorder；不得决定 scope、adequacy、finding、
  semantic pass、human confirmation、route intent 或 PR readiness。

### R9. 分发、upgrade 与文档

- Canonical source、installed `.trellis/guru-team/skills/`、dogfood shared/Codex/Claude/Cursor
  copies、workflow markers、registry、extension、migration manifest 与 package corpus 必须
  byte/identity 一致。
- Preset apply 后必须处理所有 `.new`/`.bak`，运行 dogfood overlay drift、ownership 与
  source/installed validation。
- Clean throwaway 必须验证 workflow marketplace init、preview/switch、preset install、
  Stage 0 normal/refresh/stop/mutation/recovery、`trellis update`、preset reapply 和最终零
  sidecar。
- Durable specs、requirements docs 与三份公开 README 必须同步 Interface 1.3 production
  activation、legacy #146 boundary、eval coverage 与执行命令。

## 5. Issue 范围

- Close：#145。
- Related 且保持 open：#98、#127、#132。
- Related closed authority refs：#144、#147；二者不 reopen、不由本任务再次关闭。
- Follow-up：#146。
- Dependencies：#144、#147 已完成并作为当前实现基线。

## 6. 非目标

- 不修改 #147 的 eval schema、grader policy、semantic ownership 或 run evidence contract；
  runner/adapter/public dispatch 的改动只限于 D2 的 production semantic execution closure。
- 不扩张 #144 的其它基础设施合同；Interface schema/validator/public dispatch 的改动只限于
  D1 的显式 boolean 与 `guru-sync-base` optional fallback。
- 不迁移 `guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit`。
- 不迁移 Branch Review 或 Finish family。
- 不改变需求澄清、措辞审查、readiness 或 workspace semantic judgment。
- 不把 public output恢复为 audit artifact，不要求 Agent 读取/import
  `guru_team_trellis.py`。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 不新增恶意 actor、伪造/篡改、对抗性输入、锁、TOCTOU、并发压力、额外 fault
  injection、crash consistency 或跨 OS 原子性机制和测试。

## 7. Docs 状态

- Docs state：`complete_docs`。
- Strategy：`ssot_first`。
- Requirements impact：本任务改变 production public Skill I/O、consumer contracts、
  registry/extension inventories、preset activation、eval corpus 与 upgrade contract，必须在
  同一 Phase 2 中更新 durable specs、requirements docs 和 public README。
- 权威 Docs SSOT Plan：`design.md` 的 `## 12. Docs SSOT Plan`。
- Middle-platform Knowledge Gate：不适用；本任务不接入 go-guru、proto-guru、Unity3D
  Guru SDK、Flutter Guru SDK 或其它业务中台框架。

## 8. 验收标准

- [ ] AC1：6 Skills、24 exits 在 source/installed/workflow/registry/extension/migration
  manifest 中集合完全一致，missing/extra/renamed/unknown/duplicate 被拒绝。
- [ ] AC2：六个 entries 均为 Interface 1.3 + `minimal_handoff`；#146 三个 entries 仍为
  Interface 1.2 + `legacy`，active 总数仍为 9。
- [ ] AC3：每个 structurally distinct input profile 有 closed schema/signature、完整
  example 与真实 public invocation probe；`guru-sync-base` 没有 input JSON schema，
  `scalarArgument.required` 只接受显式 boolean，携带与省略 `--base-branch` 均通过 public
  invocation，省略路径按既有固定 resolver order 得到 owner-checked base。
- [ ] AC4：24 exits 分别有 output schema/example、唯一 consumer contract/projection，
  每个 output field 均有 direct-use proof。
- [ ] AC5：Public output 不包含无人消费 audit/history/file metadata/runtime-derived
  digest/recovery state；private artifacts 的 kind/persistence 完整。
- [ ] AC6：Complete Stage 0 normal route 与 refresh/re-entry/stop/retarget/content-changed/
  mutation/recovery families 在 clean throwaway repo 执行通过。
- [ ] AC7：Upgrade from pre-#145 installation、atomic activation/versioned adapter、preset
  reapply 与 `.new/.bak` 检查不产生 mixed-contract graph。
- [ ] AC8：Eval coverage manifest 对 6 Skills、24 exits 与全部 input profiles 提供非空、
  current、无重复 case binding。
- [ ] AC9：六份 canonical `evals/evals.json` 通过 #147 schema/runner；shared adapter 可解析
  并执行真实 wrapper，Codex trusted Git context、Claude input protocol、Cursor
  unavailable/unsupported 均有确定结果，四平台读取同一 corpus bytes；semantic case 使用
  checker-passed repo-local owner result，actual exit 决定 output schema，`expected_exit`
  只参与执行后的预期断言。
- [ ] AC10：正常 Agent transcript 与 eval runner trace 均未读取/import private runtime
  source，normal invocation 不加载 eval corpus。
- [ ] AC11：Existing active re-entry、archive read、freshness、issue/workspace recovery
  fixtures 通过，archive 无回写。
- [ ] AC12：Source、installed、dogfood、workflow marketplace、preset install/update/reapply、
  四平台与 drift gates 全部通过。
- [ ] AC13：Docs SSOT Plan 已执行，task delta 已合并到 durable docs，三份 public README
  命令可执行且不依赖本机隐藏状态。
- [ ] AC14：Phase 2 `guru-check-task` 对需求、设计、代码、schemas、tests、distribution、
  docs 与 task artifacts 完整审查且零未解决 finding。
- [ ] AC15：Branch Review 覆盖 intake base `origin/main...HEAD` 完整 diff，PR readiness 只
  使用 `Closes #145`；#98/#127/#132/#144/#146/#147 均不关闭，其中 #144/#147 只使用
  closed authority reference 语义。

## 9. 完成条件

只有 AC1-AC15 全部获得命令、测试或 semantic review 证据，Docs SSOT reconciliation
完成，Branch Review Gate 通过，且 PR body 的部署/安全/issue close 说明真实完整，本任务
才能进入 `trellis-finish-work` 与发布。
