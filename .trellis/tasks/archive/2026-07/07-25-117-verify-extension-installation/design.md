# #117 技术设计：`guru-verify-extension-installation`

## 1. 设计结论

新增一个 Interface 1.3 semantic package，以 AI-owned closed loop 包裹并重构现有
marketplace deterministic substrate。该 package 独占 applicability、verification
profile、adequacy、finding 与 route；共享 runtime 只负责 remote identity、clean
installation、事实记录、schema/freshness/redaction 检查和最小 DTO serialization。

核心数据流：

```text
workflow seed 或 standalone intent
  -> AI 读取 target/diff/contracts/docs/ownership
  -> AI 判断 applicability 并选择 verification profile
  -> deterministic preflight + clean-install executor
  -> AI 审查 coverage/result/redaction 并形成 adequacy/findings/route
  -> recorder 写 marketplace-verification.json 或 session-only owner result
  -> checker 复验 identity/schema/freshness/route
  -> public wrapper 按 actual exit_id 输出一个最小 DTO
```

生产 eval 数据流与真实安装数据流分离：

```text
package eval fixture -> semantic owner result -> real public wrapper -> typed DTO
remote ref -> clean temporary repos -> installation facts -> AI adequacy -> owner result
```

两条链路分别通过后才满足交付验收。

## 2. 组件边界

### 2.1 Canonical package

新增 canonical root：

```text
trellis/skills/guru-team/packages/guru-verify-extension-installation/
```

目录职责：

- `SKILL.md`：入口、semantic loop、human confirmation policy、re-entry 与 exits。
- `references/contract.md`：applicability、profile、adequacy、private evidence、retry、
  redaction 和 route 的完整合同。
- `interface.json`：Interface 1.3 public inputs/outputs、consumer inputs、projections、
  private artifact 与 platform destinations。
- `schemas/`：两个 public input、四个 public output、aggregate input、invocation error、
  private evidence。
- `examples/`：每个 public contract 的完整正例和 private evidence 示例。
- `scripts/`：`invoke.sh`、recorder wrapper、checker wrapper、executor wrapper。
- `evals/`：workflow/standalone、四 exits、retry/unavailable 的 real-wrapper corpus。
- `tests/`：package discovery、schema/example、public projection、private-state exclusion、
  wrapper 与 redaction tests。

### 2.2 Shared runtime

现有以下逻辑迁入或收敛到 package-owned runtime command：

- `marketplace_verification_required`
- `marketplace_verification_contract_errors`
- `execute_marketplace_verification`
- `verify-marketplace.sh`
- `marketplace-verification.schema.json`

目标职责：

- Changed paths 只输出候选 surface facts，不返回 semantic applicability。
- Executor 接收 AI 已选择的 closed verification profile，不自行删减 command matrix。
- Recorder 接收 AI 已完成的 applicability/adequacy/finding/route，重建 machine facts 后
  写一个 owner result。
- Checker 复验 owner result，但不把 machine pass 翻译为 semantic `verified`。
- Dispatcher 为 package 暴露固定 runtime command id；top-level legacy wrapper 若仍有
  current consumer，只作为同一 runtime 的兼容入口，不保留第二套实现。

### 2.3 Distribution

Canonical package 与 registry 通过 preset installer 分发到：

```text
.trellis/guru-team/skills/packages/guru-verify-extension-installation/
.agents/skills/guru-verify-extension-installation/
.codex/skills/guru-verify-extension-installation/
.claude/skills/guru-verify-extension-installation/
.cursor/skills/guru-verify-extension-installation/
```

安装副本必须与 canonical package byte-identical。平台入口只提供 discovery 和调用，
不复制 step-local loop。#128 ownership inventory 继续作为 upstream/Guru asset
边界；本 task 不新增 upstream entry overlay。

## 3. Public Interface 1.3

### 3.1 Inputs

#### Workflow profile

Profile id 固定为 `verification_required`，由 #117 先拥有 target schema：

```json
{
  "profile": "verification_required",
  "mode": "workflow",
  "task_ref": ".trellis/tasks/<task>",
  "plan_ref": "<opaque-plan-ref>",
  "repo_ref": "castbox/guru-trellis",
  "reviewed_head": "<40-char-sha>",
  "verification_target": "extension-installation"
}
```

Issue authority 固定的 producer seed 是后五个业务字段；`profile` 与 `mode` 是 target
profile discriminator。Schema 使用 closed object。该 target 没有 fresh caller
AI-owned required field，因此 future #118 edge 使用纯 DTO projection，不声明
`skill_input_authoring_seed`。

#117 提供 schema、example、fixture 和 public-wrapper eval。#118 后续提供 producer
output、projection 与 edge activation；#117 不构造 #118 output。

#### Standalone profile

Profile id 固定为 `standalone_verification`：

```json
{
  "profile": "standalone_verification",
  "mode": "standalone",
  "repo_ref": "castbox/guru-trellis",
  "remote": "origin",
  "ref": "refs/heads/<branch>",
  "caller_intent": "verify-extension-installation",
  "task_ref": ".trellis/tasks/<task-or-null>"
}
```

`task_ref` 使用 schema 分支表达有 task 与 session-only 两种形态，不与 workflow
profile 共享 nullable 总对象。Standalone 输入不接收 verification profile、command
matrix、adequacy 或 expected exit。

### 3.2 Outputs

所有 output schema 使用 `exit_id`。

| Exit | 最小字段 | Consumer |
| --- | --- | --- |
| `verified` | `exit_id`, `task_ref`, `plan_ref`, `reviewed_head`, `verification_ref` | planned `guru-finalize-task` |
| `not_required` | `exit_id`, `task_ref`, `plan_ref`, `reviewed_head` | planned `guru-finalize-task` |
| `return_to_task_work` | `exit_id`, `task_ref`, `finding_refs`, `resume_target=phase-2` | workflow `trellis-continue` route |
| `blocked` | `exit_id`, `reason_code`, `remediation` | stop target |

每个 exit 只发布一个 output schema；schema 内以 closed `oneOf` 区分 workflow
handoff 与 standalone session report。Standalone 分支使用 `repo_ref`、resolved
remote HEAD 和 opaque session verification identity，不携带虚假的 `task_ref` 或
`plan_ref`。有 task standalone 的 `return_to_task_work` 投影到
`trellis-continue`；无 task standalone 不产生该 exit，安装或覆盖失败返回带
`reason_code`、finding refs 与 remediation 的 `blocked` session report。Interface
和 eval 必须证明每个 mode 分支仍只包含其实际 consumer 使用的字段，不退回大而全
DTO。

### 3.3 Consumer 与 projection

- `verified` 和 `not_required` 指向 registry 中 planned `guru-finalize-task`。
- `return_to_task_work` 使用 workflow-owned consumer schema。
- `blocked` 使用 stop-owned consumer schema。
- Standalone 调用将对应 output 的 standalone 分支直接呈现给调用者，不新增第二个
  graph consumer，也不触发 workflow transition；Interface 中每个 exit 仍只有上表
  一个 named consumer。
- Projection operation 限定为 `direct|select|rename|normalize`。
- `verification_ref` 是 opaque current identity，只供 #118 校验 current owner result；
  不编码 artifact body、command inventory 或 review history。
- Workflow/stop target marker 只声明路由存在，不复制 Skill 内部判断。
- #117 激活时不新增虚假的 `guru-finalize-task` invocation。#119 才拥有完整
  `#118 verification_required -> #117 -> #118 verified|not_required` graph integration。

## 4. Semantic owner contract

### 4.1 Entry preconditions

每次调用必须复验：

1. Compatible Guru Team extension、dispatcher、active package 和 manifest。
2. Public input profile 与 mode。
3. Repo/remote/ref locator 和 credentials-safe URL。
4. Workflow mode 的 task、plan、reviewed content HEAD 与 future finalizer seed。
5. Standalone caller intent 与 task/session-only persistence boundary。
6. Current remote HEAD 与 reviewed/requested HEAD。
7. Current extension surface、diff、public docs 与 ownership inventory。
8. Prior verification identity 与 re-entry freshness。

### 4.2 Applicability

AI 必须读取并说明以下证据是否改变用户可安装的 extension surface：

- marketplace index 或 workflow package；
- preset、overlay、installer、managed manifest；
- public schema、config template、runtime command；
- Shared/Codex/Claude/Cursor Skill/command/prompt/agent entry；
- install/update/upgrade contract；
- 用户公开执行的 README command。

Runtime 只提供 changed paths、manifest、digests 与 ownership facts。AI 输出
`required` 或 `not_required` 以及理由。Workflow input 的
`verification_target=extension-installation` 与 future plan-required intent 冲突时，
`not_required` 必须进入 blocked/review route，不能静默跳过。

### 4.3 Verification profile

AI 从一个 closed profile catalog 选择本次执行矩阵。Catalog 以 capability id 表达：

- `marketplace_index`
- `new_repo_init`
- `existing_repo_preview_switch`
- `preset_initial_apply`
- `preset_reapply`
- `trellis_update_reapply`
- `managed_conflict_sidecars`
- `skill_contract_discovery`
- `platform_equality`
- `ownership_inventory`
- `readme_commands`
- `redaction`

完整 extension package/installer/workflow 变更必须选择全部 capability。较窄的 schema、
docs 或 platform-only diff 仍由 AI 给出 capability-to-change 映射；缺少受影响
capability 时 adequacy 不得通过。Catalog 是 package contract，不由 caller input 或
runtime path prefix推断。

### 4.4 AI Review Gate

Executor 完成后，AI 审查：

1. Applicability 结论与 diff/contract 一致。
2. Chosen profile 覆盖每个受影响 surface。
3. Remote HEAD 与 requested/reviewed HEAD 相同。
4. 每个 required capability 都有执行事实和资产证据。
5. Initial install、preview/switch、update/reapply、ownership 与 sidecar 结果满足合同。
6. Platform corpus 与 installed package bytes 一致。
7. Artifact、stdout summary、eval trace 和 retained logs 完成 redaction。
8. Findings 的 scope、evidence、route 与 closure state 完整。
9. Retry 或 stale route 绑定 current plan/ref/HEAD。
10. Exit 与 consumer 唯一匹配。

Gate 结论域固定为一个值：`verified`、`not_required`、
`return_to_task_work`、`blocked`。Human confirmation 仅在 standalone caller
intent 与 AI applicability 发生需要用户选择的产品语义冲突时触发；workflow
plan-bound required 不以 human override 跳过。

## 5. Private evidence

### 5.1 Persistence

- Workflow mode 与有 task standalone：写
  `{TASK_DIR}/marketplace-verification.json`。
- 无 task standalone：生成 session-only owner result，wrapper 返回后不写 repo
  tracked/ignored cache。
- 临时 checkout、temp repo 与 raw logs 在执行结束后删除；只保留去敏 machine facts。

### 5.2 Schema

Private schema 升级为 package-owned版本，固定包含：

- generator/schema/skill/mode/profile；
- task、repo、remote、ref、plan、reviewed HEAD、remote HEAD identity；
- applicability evidence 与 AI reason；
- selected capability catalog 与 selection reason；
- command facts：sanitized argv、exit code、stdout/stderr digest/size；
- installed workflow/preset/schema/skill/platform asset digests；
- ownership inventory、frozen `transitional_legacy` comparison、`.new/.bak` facts；
- AI adequacy dimensions、findings、conclusion；
- retry/supersession/freshness identity；
- actual exit、consumer 与 opaque `verification_ref`；
- redaction scan facts。

AI reason 不进入 machine-fact digest 的逐字 identity；machine identity 与 semantic
section分别计算后在 owner result 中绑定。

### 5.3 Findings 与 routes

- Task 内 code/docs/tests 修复：open finding route 为 `task_work`，exit 为
  `return_to_task_work`。
- Auth/network/remote unavailable：open finding route 为 `external_blocker`，exit 为
  `blocked`。
- `verified` 要求所有 required capability passed、adequacy dimensions passed、
  current-scope findings closed、redaction passed。
- `not_required` 要求 applicability evidence 完整、AI reason 非空、没有执行 profile
  或伪造 pass facts。

## 6. Executor 设计

### 6.1 Remote identity

1. 将 remote locator 规范化为安全 repo/ref identity。
2. `git ls-remote` 获取 requested ref 的 HEAD。
3. Workflow mode 要求 remote HEAD 与 `reviewed_head` 相同。
4. Standalone mode 将首次解析 HEAD 冻结为 requested identity。
5. Clone 后复验 checkout HEAD。
6. Evidence 中 remote URL 使用 `<remote-url>` 或 canonical repo locator。

### 6.2 Clean installation matrix

Executor 使用临时目录建立独立 source checkout、new project 和 existing project：

1. 从 remote ref shallow clone canonical source。
2. 验证 `trellis/index.json` 的 id/path/type。
3. 在 new project 执行 README 对应的 `trellis init ... --workflow guru-team`。
4. 在 existing project 执行 `trellis workflow ... --create-new`，校验 preview。
5. 执行实际 switch，校验 active workflow。
6. 执行 preset initial apply，校验 manifest、modes、packages、platform destinations。
7. 注入受支持的 managed-file local change，执行 reapply，校验 `.new/.bak` 合同。
8. 执行 `trellis update`，校验 upstream ownership 未被 Guru package替换。
9. 再执行 workflow select 与 preset reapply，校验 Guru assets 恢复。
10. 执行 source/installed Skill package validator、platform corpus/eval probes、
    ownership inventory 和 README command assertions。
11. 执行 redaction scan并生成 digest/size evidence。

现有 `verify-throwaway-install.sh` 保持 repository-wide release regression owner；
Skill executor 复用其确定性组件或调用一个参数化 verification profile，不复制第二套
安装语义。Production eval 不从 normal transcript import
`guru_team_trellis.py`，也不读取 private runtime构造 public invocation。

## 7. Eval 与测试设计

### 7.1 Package-local production corpus

Eval cases固定覆盖：

- workflow required -> `verified`
- workflow applicability conflict -> `blocked`
- standalone non-extension target -> `not_required`
- install/coverage finding -> `return_to_task_work`
- auth/network/remote unavailable -> `blocked`
- same plan/ref/HEAD transient retry -> current success
- stale plan/ref/HEAD -> fail-closed re-entry

每个 case 使用 repo-local checker-passed owner result，调用 real public wrapper。
Actual exit 先决定 output schema；`expected_exit` 只在 wrapper 返回后比较。Expected
non-success exit 是正常通过的行为验收。

Adapters 固定验证：

- shared adapter parsing；
- Codex trusted Git root；
- Claude input protocol；
- Cursor unavailable/unsupported；
- 四个平台 corpus bytes 与 canonical package一致。

### 7.2 Runtime 与 failure matrix

测试固定覆盖：

- 两个 structurally distinct inputs；
- 四个 per-exit schemas/examples/projections；
- wrong/missing/multiple exit；
- remote HEAD mismatch；
- private fields 泄漏到 DTO；
- changed-path facts 不拥有 applicability；
- exit code 0 但 adequacy blocked；
- partial/early executor failure 仍产出 schema-valid owner result；
- retry 与 superseded stale evidence；
- task-local 与 session-only persistence；
- URL/argv/output redaction；
- `.new/.bak`、ownership 和 frozen legacy inventory；
- source/installed registry/manifest/package closure；
- dogfood apply/drift；
- clean throwaway initial install/update/reapply。

#105 transaction failure matrix 保持独立现有 owner；本 task 只运行并确认不回归，不把
该 matrix 重写进 extension Skill。

## 8. Workflow、registry 与 manifest

- Registry 新增 active `guru-verify-extension-installation` entry。
- `guru-finalize-task` 保持 planned。
- Extension manifest 更新 active Skill inventory、package files/hashes 与 runtime
  command inventory。
- Interface discovery发布 inputs、outputs、consumer inputs、projections、private
  artifact和 eval bindings。
- Workflow canonical 与 dogfood copy 只增加 contract graph 所需的 invocation/exit/
  target markers及 route说明；不复制 semantic loop，不提前实现 #119 integration。
- Source/installed validator 基于 live registry 计算 closure。测试按实现后的实际 graph
  断言 counts，不把当前 `11/42/25` 作为永久常量。

## 9. Docs SSOT Plan

### 9.1 Docs state

`partial_docs`

证据：

- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md` 已定义 global
  phase/typed-exit contract，但没有 #117 active package route。
- `.trellis/spec/workflow/skill-package-contract.md` 已定义 Interface 1.3 与 private
  state原则，但没有 extension verifier 的 target bootstrap 和四出口映射。
- `.trellis/spec/workflow/companion-scripts.md` 已描述现有 deterministic verifier，
  但仍混合旧 monolithic finish behavior。
- `docs/requirements/requirement-main.md` 与
  `docs/requirements/guru-team-trellis-flow.md` 已描述 Guru workflow，却没有独立
  extension verification semantic owner。
- Workflow/preset README 已提供安装入口，但未说明新 Skill discovery、standalone
  invocation 与验证边界。

### 9.2 Strategy

`ssot_first`

原因：本 task 新增公共 Skill id、Interface 1.3 I/O、runtime command、private evidence
和安装/升级行为合同。实现必须先更新 canonical package、workflow/spec/manifest 与
durable requirements，再同步 dogfood/platform copy；task artifact 只保留本次决策与
验证证据。

### 9.3 Durable docs owners

- Global phase、marker、typed consumer：
  `trellis/workflows/guru-team/workflow.md`
- Dogfood active workflow copy：
  `.trellis/workflow.md`
- Skill package完整 step-local SSOT：
  `trellis/skills/guru-team/packages/guru-verify-extension-installation/SKILL.md`
  与 `references/contract.md`
- Public Skill I/O、private state、projection 通用规则：
  `.trellis/spec/workflow/skill-package-contract.md`
- Executor/recorder/validator 与 marketplace runtime边界：
  `.trellis/spec/workflow/companion-scripts.md`
- Global phase ownership：
  `.trellis/spec/workflow/workflow-contract.md`
- 产品需求与流程导航：
  `docs/requirements/README.md`、
  `docs/requirements/requirement-main.md`、
  `docs/requirements/guru-team-trellis-flow.md`
- 安装、切换、preset 与 standalone用法：
  `trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`
- Machine contract：
  registry、Interface/schema、`trellis/guru-team-extension.json`

### 9.4 Task delta merge

实现阶段必须把以下 task delta 合并回 durable owners：

- Applicability/profile/adequacy semantic loop -> package contract。
- Interface 1.3 input/output/consumer/projection -> interface/schema/spec。
- Private evidence/retry/stale/redaction -> package contract、private schema、
  companion script spec。
- Remote clean install、update/reapply、ownership/sidecar -> README、requirements、
  runtime tests。
- Production eval 与真实安装双验收 -> Skill package contract、requirements、test
  plan说明。

Phase 2 check 必须逐项核对上述 durable owner 与实现 diff。未合并内容只能是本次 issue
的 provenance、审查过程、验证结果和 follow-up 记录。

## 10. Rollout、回滚与兼容

### 10.1 Rollout

1. Canonical package、registry、schema、runtime、workflow/spec/docs 同一 commit 激活。
2. Preset apply 同步 dogfood installed copy 和四个平台 package copy。
3. Source/installed validators 与 production eval 通过。
4. Dogfood drift 通过且无未处理 sidecar。
5. 推送当前 reviewed content HEAD 后，从该 remote ref 运行 clean installation。
6. #117 完成后，#118/#119 通过独立 task激活 producer/finalizer graph。

### 10.2 Rollback

任一 gate失败时，回滚 #117 整个 activation unit：registry active entry、package、
runtime command、manifest、workflow markers、distribution与 docs 同步撤回到同一
pre-activation state。不得保留 registry active 但 package/consumer/eval缺失的中间态。

已有 monolithic verifier 在 #117 activation 完成前保持 current baseline。完成后若保留
兼容 wrapper，它必须 dispatch 到唯一新 runtime；不得保留独立 route owner。Rollback
不得删除用户修改的 installed file；installer 按 managed hash 与 `.new/.bak` 合同处理。

## 11. 设计风险

- 旧 verifier 将 path prefix 当作 applicability，若未解除 route ownership，会形成双
  semantic owner。Gate：测试证明该函数只产生 facts。
- Workflow 与 standalone output identity不同，若塞入同一 nullable DTO，会违反最小
  handoff。Gate：schema 分支或独立 per-mode output均保持 closed shape。
- #118 尚未实现，若提前激活 producer edge，会形成 dangling reverse dependency。
  Gate：registry、manifest 与 graph test要求 #118 保持 planned。
- Production eval容易被误当作 remote install证明。Gate：验收报告分别记录两条链路。
- Installer/update 可能覆盖 upstream entry。Gate：#128 ownership inventory与 frozen
  `transitional_legacy` comparison必须通过。
- Raw command output可能含 credential。Gate：只持久化去敏 argv、digest、size，并扫描
  artifact/wrapper/eval输出。
