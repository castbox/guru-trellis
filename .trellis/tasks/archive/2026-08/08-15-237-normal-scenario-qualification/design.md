# #237 技术设计：正常场景资格公共 Skill

## 1. 设计目标

把“candidate 是否有资格进入当前阶段判断”收敛为一个 public semantic Skill，
保持以下分层：

```text
caller / worker
  -> 形成 invocation-local candidate refs + live locators
  -> guru-qualify-normal-scenario（唯一 semantic Owner）
  -> workflow profile router
  -> 原 caller 继续阶段专属判断
```

Qualification 只决定 candidate 是否有资格继续；不决定 severity、planning
sufficiency、修复方案、publication route 或最终 pass。

## 2. SSOT 与责任边界

| 层 | 拥有内容 | 明确不拥有 |
| --- | --- | --- |
| `guru-qualify-normal-scenario` package | forward behavior、五项资格判断、scope-first 顺序、安全反向举证、candidate decisions、AI Review Gate、re-entry、四 exits | caller 的 severity、planning/implementation/publication 专属判断 |
| Global workflow | stable Skill mandatory invoke、十 profile 触发/返回点、四 exit consumers、两个 routers、blocked stop | 资格算法正文 |
| Caller Skill/package | profile-specific candidate set、live locators、消费结果后的阶段判断 | 复制资格判断、旧结果复用 |
| Worker/agent | candidate ref、观察行为、locator、最小复现线索 | severity、scenario class、qualification、implementation route |
| Durable specs | public I/O、schema/version、consumer mapping、分层和治理规则 | scope/正常路径/充分性语义 |
| Python/shell/schema | closed shape、identity、freshness、enum、projection、consumer binding | 关键词分类、scope、正常路径、充分性、severity、route |

## 3. Package 结构

新增 canonical package：

```text
trellis/skills/guru-team/packages/guru-qualify-normal-scenario/
├── SKILL.md
├── interface.json
├── commands.json
├── references/contract.md
├── scripts/
│   ├── invoke.sh
│   ├── record-normal-scenario-qualification.sh
│   └── check-normal-scenario-qualification.sh
├── runtime/
│   ├── common.py
│   ├── record.py
│   ├── check.py
│   └── invoke.py
├── schemas/
├── examples/
├── evals/
└── tests/
```

具体命名遵循当前 package patterns；runtime 通过 `run-skill-command` dispatcher
进入，不由 caller import package Python。`record-*` 是 process-local serializer，不是
artifact writer：它只读 stdin、在内存中组装当前 semantic result、写 stdout。
`check-*` 只读 stdin、在内存中校验 shape/identity/freshness/enum/consumer binding、写
stdout。两者均禁止接收 output path、result locator 或 checkpoint path，也禁止写入
repository tracked 文件、gitignored `.trellis/.runtime/**`、其它 qualification artifact
或跨进程临时文件。Public `invoke.sh --invocation -` 通过同一 stdin/stdout pipeline 消费
已检查结果，调用结束后不存在可供下一阶段读取的 Skill state。

## 4. Public input 设计

### 4.1 Aggregate closure

`public-input.schema.json` 仅通过 `oneOf` 聚合十个 profile-specific schema；每个
profile 使用固定 discriminator、固定 caller enum 和 closed `additionalProperties:false`。

新 package 使用 additive `guru-team-skill-interface-1.6`。其
`structured_json` invocation 通过
`profile_selector={source:aggregate_public_input,field:profile}` 只声明由完整 public
input 的 `profile` discriminator 选择 closed profile schema，不携带已选 profile
值。既有 Interface 1.4 fixed `profile_id` 与 Interface 1.5 合同保持原字节和原语义。

### 4.2 Common minimum

所有 profile 的共同字段限定为：

- `profile`
- `mode: workflow|standalone`
- 固定 `caller`
- 当前 target identity
- 非空、唯一、call-local `candidate_refs`
- 支持 live reread 的 repo-relative path、symbol/test id、Issue locator、commit/range
  或 base-pair locator

各 schema 不接收 caller-authored decision、severity、expected exit、授权文字、旧结果、
共享 artifact、raw worker output、完整日志或 normal-path 结论。

### 4.3 Profile identities

| Profile | Target identity 与最小 locator |
| --- | --- |
| `task_free_pre_write` | current checkout HEAD、bounded path set、request locator |
| `task_free_evolution` | current checkout HEAD、已批准 path set、新 candidate locators |
| `requirements_scope_set` | live issue/draft/active-task identity、proposed scenario locators |
| `change_request_candidate_set` | reviewed issue/draft identity、readiness evidence locators |
| `planning_scenario_set` | task ref、planning files、scope ledger、scenario locators |
| `implementation_discovery` | task ref、approved plan identity、current HEAD/diff、worker candidate locators |
| `base_impact_candidate_set` | task ref、exact old/new base heads、task head、impact locators |
| `phase2_candidate_set` | task ref、current HEAD、planning identity、full candidate locators |
| `branch_review_candidate_set` | task ref、base/head/range、review commit、candidate locators |
| `publication_candidate_set` | task ref、review commit、publication payload identity、candidate locators |

## 5. Semantic closed loop

每次 invocation：

1. 校验 profile、caller、target identity、candidate completeness 和 live reread 能力。
2. 直接重读 current authority、planning、caller/consumer、code/diff/tests 和 repository
   contract。
3. 对每个 candidate 按固定顺序判断 requirement authority、supported entry、honest
   action sequence、current defect、scope provenance。
4. 对安全/攻击叙事执行反向举证；severity 和历史/worker 压力先隔离为无 authority
   观察文本。
5. 为每个 candidate 形成恰好一个 AI-authored decision 与最小 reason；新 Skill 内的
   decision、mapping、witness 和 typed result 只保留在当前 process 内存与 stdout。
6. AI Review Gate 检查 candidate set 完整、每项证据充分、已排除场景未升级为确认、
   qualified 结果未越权决定下游阶段判断。
7. 只有真实新 scope choice 才返回 clarification；mechanism remove/replace 返回原 Owner
   修订；缺失 live evidence 则 blocked。
8. Semantic judgment 完成后，process-local recorder/checker 通过 stdin/stdout 串联，
   只验证结构、current identity、freshness、enum 和 consumer binding。
9. `invoke.sh --invocation -` 返回一个最小 typed exit；整个 pipeline 不创建 tracked、
   ignored runtime、临时 cross-process locator、checkpoint 或共享结果文件。

## 6. Decisions 与 exit 聚合

- 所有 candidate 均为 qualified/rejected，且无确认、机制修订或 blocked：`classified`。
- 存在任一 `scope_confirmation_required` 且无 blocked：
  `scope_confirmation_required`；不得与 qualified 结果并行推进。
- 存在任一 `mechanism_removed|mechanism_replaced` 且无 blocked：
  `mechanism_revision_required`。
- 任一 target/authority/candidate/evidence 无法可靠判断：`blocked`。

四种 rejected decision 都是非阻塞 candidate disposition，不进入确认、finding、
implementation 或 required follow-up。

## 7. Workflow routing

Global workflow 增加一个 stable Skill invocation marker，并在十个 caller/Phase 2
coordinator 的精确触发点声明 profile-specific mandatory invocation。现有 package graph
validator 仍以 registry/interface 为 authority，拒绝重复或未映射 marker。

新增 targets：

- `guru-normal-scenario-classified-router`
- `guru-normal-scenario-mechanism-router`
- stop `normal-scenario-qualification-blocked`

Router 只基于 validator-confirmed fixed profile 返回原 Owner，不解析 reason 或 witness，
不做第二次语义判断。

## 8. Caller 集成

需要修改以下语义 Owner 的 canonical SKILL/reference/interface/runtime/evals/tests：

- `guru-execute-task-free-change`
- `guru-clarify-requirements`
- `guru-review-change-request`
- `guru-approve-task-plan`
- `guru-reconcile-task-base`
- `guru-check-task`
- `guru-review-branch`
- `guru-review-task-publication`

Phase 2 implementation coordinator 通过 workflow 与 implement/research worker contracts
接入 `implementation_discovery`。Caller 只 author candidate set、调用 Skill、验证 mapped
profile 返回并继续自己的阶段判断。

## 9. Worker 与平台投影

官方 implement/check/research、channel runtime 与平台 `trellis-*` agent definitions
保持 upstream-owned bytes 不变。Guru-owned workflow/caller 在每次 dispatch prompt 中
只授权 approved-plan work；planning-external observation 只能返回 candidate ref、观察、
locator 与最小复现线索，禁止在 fresh qualification 前 edit、补 test、self-fix、赋
severity、classification 或 route。平台 agent 不直接调用资格算法，除非被明确委派为
本次 Skill Owner 或完整 mandatory caller Owner。

Preset installer 从 canonical package 投影 shared、Codex、Claude、Cursor 的
`guru-qualify-normal-scenario` package；不新增复制算法的 overlay。现有三个
`guru-finish-work` overlay 保持唯一显式 overlay 集合。

## 10. Existing owner gate witness 迁移

Phase 2、Branch Review、Publication 的语义 Owner 在各自当前 round 中直接把 direct
consumer 所需的最终 classification/witness 写入该阶段既有 owner-private gate。写入数据
来自该 Owner 对当前 Skill stdout 的即时消费，不保存或引用 Skill result、artifact、
locator、checkpoint、digest chain 或前次 invocation。若既有 gate schema shape 改变：

- 发布新 schema version；
- 当前 writer/checker 只接受新版本；
- 旧 owner gate checkpoint 明确 stale，重新运行对应阶段 Owner 生成；
- 不把 witness 投影到 public DTO；
- 不为历史 owner gate 建立长期迁移或共享读取路径；
- 不新增 qualification 专用 tracked/ignored state。

`normal_path_reproduction` 自由文本不再作为充分证明，可保留为人类说明或被新 witness
替换，但 validator 不能把非空文本当 semantic pass。

## 11. Eval 架构

### 11.1 Production corpus

在新 Skill package 的 `evals/evals.json` 声明由以下维度形成的 closed matrix：

- 10 profiles；
- rejected scenarios：#113 F-001、#236 alias/wrapper/shell scanner；
- pressure framing：neutral、attack/security、severity、independent reviewer、already
  implemented、already tested、best practice、theoretical bypass；
- paired legitimate scenarios：wrong recorder digest/payload、real caller wrong runtime、
  explicit redaction、explicit permission/destructive confirmation、normal stale/mismatch、
  incorrect executor output/maintenance omission。

每个 case 的 expected decision 与 route 由 canonical corpus 在执行边界外提供；native
invocation 不接收 expected exit/decision。每个 case 由 runner 对 GPT-5.6 Sol 发起 5 次
fresh invocation，任何一次偏差即失败。

### 11.2 Real production path

四个平台 adapter 必须具备读取已安装 package、执行真实 `scripts/invoke.sh` public
entry 并形成可验证 trace 的能力。Deterministic/no-model gate 验证该 dispatch、trace、
sandbox 与 wrapper boundary；不能用关键词扫描或手写 result 替代产品合同。

Production control map 的 `input_profile_id` 只存在 host grading 边界。Adapter request、
native request、model context 和 public invocation 均不得携带 `profile_id` 或
`input_profile_id`；模型生成的完整 stdin 原样进入 installed wrapper。Adapter 只从同一
stdin envelope 观察 `semantic_result.public_input.profile` 并在 owner-private transcript
记录最小 `public_input_binding` receipt，runner 在模型返回后再与 host control 对照。

### 11.3 Model evidence boundary

本 Issue 不产生 live model evidence。若后续另行运行，evidence 必须绑定 model id、关键
prompt/corpus identity、package identity 与 case matrix，且不得反向补写为本 Issue 的
release gate pass。
模型或关键 prompt 变化后旧结果失效。这里只保留测试/gate evidence，不新增跨 workflow
public artifact。

### 11.4 Zero-residue contract

Package unit、installed wrapper、十 profile、typed-exit、error 和 re-entry tests 在 clean
throwaway repository 中记录调用前完整 file inventory，调用后重新记录并逐项比较。
预期差异集合为空；测试同时扫描 tracked、ignored `.trellis/.runtime/**` 与 repository
内临时文件，断言不存在 qualification result/report/checkpoint、candidate/rejection
ledger、跨进程 result locator 或残留 sidecar。Static tests 还拒绝 recorder/checker 的
output-path/result-locator/checkpoint-path 参数和 repository file-write API。

## 12. Docs SSOT Plan

策略：`ssot_first`。

1. Canonical SSOT：
   - `trellis/workflows/guru-team/workflow.md`
   - `trellis/skills/guru-team/packages/guru-qualify-normal-scenario/**`
   - `trellis/skills/guru-team/registry.json`
   - current production contract/eval bindings
   - `.trellis/spec/workflow/{workflow-contract,skill-package-contract,data-contracts,companion-scripts,quality-guidelines}.md`
2. Caller package contracts 在各自 package 中只保存 invocation/consumer 规则。
3. Public docs 更新 workflow/preset README 与必要顶层 README，描述可安装能力和真实
   验证边界，不复制判断算法。
4. 通过 preset apply 同步 `.trellis/workflow.md`、`.agents/skills`、`.claude/skills`、
   `.cursor/skills` 和 installed `.trellis/guru-team` copies。
5. Task planning/delta 只保存在本 task；Phase 2 在提交前把 durable contract 完整合入
   canonical docs，Branch Review 只验证已完成 reconciliation。

## 13. 兼容性、官方升级路径与回滚

- 新 Skill id、profiles 和 exits 是 additive public API；不复用旧 id 改语义。
- Caller 新依赖必须与 package/registry/extension manifest 一次安装，mixed graph fail
  closed。
- 官方当前合同存在两个独立命令：`trellis upgrade` 只升级全局 CLI package，
  `trellis update` 只把当前项目同步到本地 CLI 版本；完整升级顺序固定为 CLI upgrade
  后 project update。
- Upgrade gate 在 disposable npm prefix/container 中安装 pre-upgrade CLI，执行
  `trellis upgrade --tag latest` 并核验 binary/version 已切换；开发机 global npm 不变。
- 同一 clean/existing throwaway project 随后执行 `trellis update --dry-run`。只有输出
  `MIGRATION REQUIRED` 才执行 `trellis update --migrate --skip-all`，其它情况执行
  `trellis update --skip-all`。`--skip-all` 保留已有修改并非交互继续；不得使用
  `--force`。随后执行 marketplace workflow `--create-new` preview、active switch、
  canonical preset reapply，再验证 package、registry、platform projection、ownership、
  executable mode 与零 `.new`/`.bak`。
- 安装/upgrade/update/reapply 出现 `.new`/`.bak`、missing package、profile mismatch 或旧
  owner gate checkpoint 时停止，不猜测下一步。
- 回滚以单个 task commit/revert 为单位；不修改 upstream Trellis 或外部业务仓。

## 14. 安全与发布边界

本设计不削弱 secrets、redaction、权限和破坏性确认。它只阻止未获 authority 的攻击
类扩张。发布说明必须限定为当前 GPT-5.6 Sol、当前 prompt/package、十 profiles 与
当前 eval matrix 的通过结论。
