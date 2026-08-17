# #220 技术设计

## 根因

当前合同把两个不同条件压成一次 transition：

```text
planning artifacts
  -> guru-approve-task-plan semantic approved
  -> phase-1-task-activation
  -> task.py start
```

`guru-approve-task-plan` 正确地判断计划是否充分，但 workflow 把 `approved` 当成可自动消费的
activation permission，导致用户无法在实现前审阅方向。根因不是 recorder/checker 缺字段，
而是 global workflow 的 interaction boundary 缺失。

## 目标链路

```text
planning artifacts + Docs SSOT Plan
  -> planning wording review
  -> guru-approve-task-plan semantic approved
  -> workflow presents links, semantic conclusion, choices, trade-offs, boundaries
  -> dialogue-local clear affirmative
  -> active-task base pair guard
  -> workspace boundary
  -> task.py start
```

`phase-1-task-activation` 保留为 stable consumer id，避免公共 I/O 迁移。它的 workflow-owned
前置行为扩展为 plan presentation/pause，Skill package不读取、不记录或验证用户确认。

## Owner 边界

### Global workflow

拥有：

- `approved` 后的三文档链接展示；
- AI semantic review 结论、关键选择、替代方案、取舍和未验证边界的用户可见摘要；
- 对当前展示方案的清晰肯定判定；
- 提问、修订、scope change、autonomous execution 的路由；
- 确认后才进入既有 pair guard、workspace check 和 task activation。

### `guru-approve-task-plan`

继续拥有：八维 semantic review、finding、revision、scope proposal、delta classification、
schema 3.0 private checkpoint、recorder/checker 和四个 typed exits。它只把 `approved`
交给 workflow target，不把用户 pause 纳入 Skill 内部 gate，也不产生授权状态。

在判断本 Issue 的九类对话回归前，Planning owner 以
`planning_scenario_set` 调用 `guru-qualify-normal-scenario`。该 Skill 只证明每个候选具有当前
Issue authority、受支持的 Phase 1 workflow entry 和无需伪造即可复现的正常动作序列；其
`classified` 结果回到 `guru-approve-task-plan`，不预先决定 adequacy、finding、revision 或
最终 exit，也不在任务或 runtime 中保留 qualification 状态。

### Deterministic runtime

Workflow/task runtime 保持不变。`task.py start` 仍只是 task status transition；任何 script
都不解析用户回复，也不验证 Phase 1 确认。

Semantic eval 的 production fixture staging 需要一项受限修复：native adapter 当前直接使用
被评测 package runtime 创建通用 task/workspace fixture，但 `guru-approve-task-plan` common 不拥有
fixture-only 的 `write_json`、`load_config` 与 `write_runtime_mappings`。只在 common 增加
`write_json` 会越过首个错误后继续在 runtime mapping 初始化失败。

Canonical native adapter 新增单一 fixture composition owner：在 production owner staging 前，
从现有 `guru-review-task-publication` owner 复用这三个确定性 helper，并仅向缺少对应能力的
eval runtime 注入。该 composition 不进入 public projection，不改变被评测 package 的生产
runtime、recorder/checker/invoke、public I/O、native trace receipt 或业务 workflow。已加入
`guru-approve-task-plan` common 的临时 `write_json` alias 在实施时移除，避免 eval-only 能力污染
production common，也避免复制 workspace mapping 实现。

Fixture 初始化后，planning owner staging 还需要通过安装包自己的 shell wrappers 执行
`record-planning-approval` 与 `check-planning-approval`。这些 bindings 当前已实现，但被嵌套在
`compose_review_branch_eval_runtime`，导致 planning runtime 无法访问。设计把通用
`run_component` 与现有 planning/check/review bindings 提取为独立
`compose_production_owner_command_runtime`：在 production owner staging 前只补缺失 bindings，
继续执行 fixture 中安装包的真实 wrapper，并保留 review-branch 现有行为。它不直接 import
recorder/checker Python、不构造 owner result、不覆盖 package 已有 capability。

真实 `clarify_scope` wrapper 随后暴露既有 projection mismatch：schema 3.0 的
`scope_proposals` 与 public output 的 `proposal_refs` 都是字符串列表，但 `invoke.py` 使用
`[x["id"] for x in ...]`。Canonical runtime 改为
`list(owner["semantic_review"]["scope_proposals"])`；owner result 已先通过 schema validation，
因此无需兼容对象形态或额外解析。四 exits、consumer mapping、schema 3.0 与 public output
schema 均保持不变。

## 交互状态规则

1. **Initial presentation**：必须绑定当前三个 planning 文件与当前 AI semantic result。
2. **Affirmative**：展示后的清晰整体肯定才进入 activation。
3. **Question**：回答后不改计划则保持同一 pause，不消费为肯定。
4. **Revision**：实质计划变化重跑 wording + semantic review，并以新展示使旧确认失效。
5. **Scope/authority change**：进入现有 clarification route，返回后重做受影响链路。
6. **AI finding open**：不得进入可确认 presentation。
7. **Autonomous request**：仅当前请求明确选择时才省略普通 pause；任何 material change 仍暂停。
8. **Later side effects**：Phase 1 确认不能投影到 commit/Finalizer/merge/cleanup owner。

这些状态由 Markdown workflow 与 AI 当前对话判断表达，不创建状态机 schema 或确认 artifact。

## 影响面

### Canonical contracts

- `trellis/workflows/guru-team/workflow.md`
- `trellis/skills/guru-team/packages/guru-approve-task-plan/SKILL.md`
- `trellis/skills/guru-team/packages/guru-approve-task-plan/references/contract.md`
- `trellis/skills/guru-team/packages/guru-approve-task-plan/tests/test_contract.py`
- `trellis/skills/guru-team/adapters/eval/native_adapter.py`
- 扩充 package eval，覆盖用户可见 pause 的语义场景，但不改变 public exit contract。

### Durable docs/specs

- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `trellis/presets/guru-team/spec/workflow/workflow-contract.md`
- `trellis/presets/guru-team/spec/workflow/data-contracts.md`
- `trellis/presets/guru-team/spec/workflow/quality-guidelines.md`

### Generated/installed copies

Preset apply 同步：

- `.trellis/workflow.md`；
- `.trellis/spec/**` managed copies；
- `.agents/skills/guru-approve-task-plan/**`；
- `.codex/skills/guru-approve-task-plan/**`；
- `.claude/skills/guru-approve-task-plan/**`；
- `.cursor/skills/guru-approve-task-plan/**`；
- `.trellis/guru-team/skills/packages/guru-approve-task-plan/**` 与 manifest inventory。

不修改 overlay tree 中不存在的 `trellis-continue` 所有权；平台 entry 继续在运行时读取
`.trellis/workflow.md`。

当前基线已包含 #237 的 18-Skill / 17-invoke / 71-exit graph，以及 #236 的 managed Python
throwaway 路由。#220 必须在这些合同之上做 additive merge：保留 qualification owner 和
现有 graph 数量，只改变 `phase-1-task-activation` 的 workflow-owned 交互前置行为。

## 兼容性与公共 API

- `approved -> phase-1-task-activation` mapping 不变。
- `guru-planning-approval-3.0`、public DTO、commands 和四 exits 不变。
- confirmation boundary 数量会增加：existing Open Issue happy path 从 3 次变为 4 次，
  新建 Issue路径从 4 次变为 5 次；新增的一次只属于 Phase 1 当前方案。
- 既有 planning task 在升级后会停在 Phase 1 presentation；不迁移或读取历史用户确认。
- `task_free` 不经过该 target，因此行为不变。

## 测试设计

1. Workflow/static contract：验证 Phase 1 presentation、三链接、AI summary、非确认输入、修订、旧确认失效、autonomous 与 scope-change 规则。
2. Package contract：验证 Skill 文案不再声明自动激活，仍保留四 exits、schema 3.0、零授权字段和 workflow-owned consumer。
3. Semantic eval：覆盖 Issue #220 Acceptance 11 的九类对话场景；assertion关注 route/pause 行为，不让 deterministic script 解析自然语言。
4. Distribution：preset apply 后检查 canonical/dogfood/shared/Codex/Claude/Cursor bytes 和 manifest。
5. Upgrade：reapply、drift、sidecar 扫描和 clean throwaway install/update。
6. Representative context：`get_context.py --mode phase` 与 Phase 1 step 输出新停点。
7. Normal-scenario compatibility：九类候选使用 `planning_scenario_set` 完成 call-local
   qualification；测试确认未产生 qualification artifact，且 `guru-approve-task-plan` 仍独占
   planning semantic judgment。
8. Eval fixture composition regression：直接验证 composition 从现有 owner 复用
   `write_json`、`load_config`、`write_runtime_mappings`，且不会覆盖 package 已拥有的能力；
   直接验证 owner-command composition 复用现有 package wrapper bindings、不会覆盖已有
   command capability，且 review-branch 与 planning staging 均使用提取后的单一实现；
   source/installed Shared、Codex、Claude adapter 分别运行四个 `guru-approve-task-plan` exits，
   断言越过完整 fixture/owner-command staging 并继续验证真实 recorder/checker/public-wrapper
   trace、exit schema 与 assertion。
   Cursor 维持当前未认证 `unsupported` 路径。
9. Clarify-scope projection regression：以 schema-valid 字符串 proposal refs 通过真实
   record/check/invoke 链，断言 public `proposal_refs` 精确相等；对象形态继续由 schema 拒绝，
   不增加 runtime 兼容分支。

## 回滚

回滚 canonical workflow、Skill wording、spec/docs 和对应 tests，然后重新 preset apply。
由于没有 schema 或持久化数据迁移，回滚不需要转换 task artifact；回滚 native adapter 的
fixture composition 后 semantic eval 会恢复为已知 staging failure，但业务 workflow 不受影响。
已存在的对话确认没有可清理状态。
