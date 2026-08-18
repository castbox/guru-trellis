# #263 建立 Requirements/Design/Test SSOT 原子闭环 Skill

## 目标

在当前 Trellis 0.6.5 / Guru v0.6.5-guru.9 source、dogfood 与 installed surface 上交付并激活公共 semantic Skill `guru-maintain-requirements-design-test-ssot`。该 Skill 是 repository 级 Requirements、Design、Test 长期 authority 的唯一原子 owner，供 Bootstrap、Intake、Planning、Phase 2、Branch Review、Publication、Acceptance 与 Finish 复用，同时保持 AI 语义判断与确定性 runtime 严格分层。

## 已确认事实

- live Issue #263 是本 task 唯一 authority；Issue #264 已通过 PR #268 合入当前 `main@86eadd47`，其 `guru-maintain-architecture-baseline` 公共合同是 Design/Test inheritance 的直接先例。
- 当前仓库只有 Planning/Check/Review 中的 stage-local Docs SSOT 决策，没有 repository 级 Requirements/Design/Test 原子 owner、四 profile 公共合同或五出口 consumer graph。
- live source inventory 为 19 个 active package、70 个 command、19 个 complete command、80 个 package exit；业务 workflow 为 18 个 invoke、78 个 exit、28 个 workflow target、19 个 stop target。#263 接入后目标分别为 20/71/20/85 与 19/83/31/20；实现和测试必须从 live inventory 校验这些值，不得从旧文案中的 18/73、17/71 或 throwaway 脚本中的 18/65 机械递增。
- task-local `prd.md`、`design.md`、`implement.md` 只承接本次工作 delta，不得在任务结束后成为第二套长期 authority。
- 验证范围由 live Issue 与 `quality-guidelines.md` 的 `Validation Scope Ownership` 决定：定向 package/runtime/canonical/dogfood/installed/platform/reapply/drift 检查，加一个代表性 clean throwaway；不运行 #260/#267 所属完整矩阵。
- 正常 honest workflow、普通 stale/mismatch、遗漏和实现错误属于范围；hostile input、锁、TOCTOU、压力竞态、fault injection 与跨 OS 加固不属于范围。

## 需求

### R1 公共 Skill 与闭环所有权

新增 stable id `guru-maintain-requirements-design-test-ssot`，`judgment_mode=semantic`。Skill 独占 authority、充分性、版本归属、跨层冲突、task delta、promotion/repair、revision action 与 route 判断；脚本只校验结构、locator、版本、引用、diff、traceability 与 AI 已给出的 typed exit。

### R2 四个互斥 profile

必须实现独立简洁的 `bootstrap_foundation`、`task_impact_sync`、`promotion`、`repair` input schema、example 与 eval。workflow 和 standalone 使用相同 entry preconditions、semantic gate、freshness 与 typed exits，不提供弱化旁路。

### R3 Repository authority

标准 authority 为 `docs/requirements/`、`docs/design/`、`docs/test/` 下的 README、version matrix/current entry、versioned 主定义、decisions、traceability 与 changes；已有兼容 authority 时复用，迁移时显式定义 redirect、tombstone、historical boundary 或 migration plan。`.trellis/spec/**` 只保存概要、索引与使用规则。

Requirements 只拥有 why/what/behavior/constraint/acceptance；Design 只拥有 organization/component/contract/sequence/state/failure；Test 只拥有 strategy/plan/scenario/case/fixture/mock/expected result/coverage。跨层只通过稳定 id 与 locator 追踪，不复制正文。

### R4 版本、状态与 provenance

每个版本具有 `draft`、`active`、`superseded` 或 `historical` 状态，以及 current entry、继承/差异和历史边界。初始恢复内容区分 `source_confirmed`、`code_recovered`、`inferred`、`unverified`；代码存在不能自动生成产品 requirement。

### R5 Task delta 与并行边界

Bootstrap 可在业务任务并行前执行一次受控 shared-doc 建设。此后普通 task 只能写自己的 task-local planning 和唯一 contribution locator；不同 task 不修改彼此 contribution，也不直接并写 shared README、version matrix、manifest、current doc 或 `.trellis/spec` index。仅 `promotion` owner 在 review 后投影 canonical current authority；promotion/repair 失败只使当前 contribution 重入，不使其它 task evidence stale。

公共合同把 `contribution_locator` 视为 task-owned 唯一目录，不把本机路径、用户身份、shared ledger、workspace journal、cross-task cache 或授权写入公共/私有持久状态。

### R6 五个 typed exits

- `ssot_current` -> `guru-requirements-design-test-ssot-current-router`
- `sync_required` -> 本 Skill 的 `promotion` 或 `repair` authoring seed
- `revision_required` -> `guru-requirements-design-test-ssot-revision-router`
- `baseline_incomplete` -> `guru-requirements-design-test-ssot-bootstrap-router`
- `blocked` -> `requirements-design-test-ssot-blocked`

每个 exit 使用独立 output schema、唯一 consumer 与可执行 projection。public output 只携带直接 consumer 需要的最小 authority locator、active version/status、scope/contribution locator 和 freshness identity；scan、全文、diff、review narrative、hash bundle、授权与 recorder 状态保持 owner-private。

### R7 Consumer 接入与兼容性

- #265 通过 `bootstrap_foundation` 建立 locator；#250 Intake 只消费 current locator/status。
- 新 workflow router 把本 Skill 的最小 output 投影给 Planning、Phase 2、Branch Review、Publication、Acceptance/Finish 的 live-docs 读取边界；这些既有 Skill 继续自行重读其直接 authority，不读取本 Skill 私有 result，也不在 #263 原地扩展既有 public DTO。若实现证明确需新增 DTO 字段，只能发布新版本 contract 并保留旧版本行为。
- #265 消费 `bootstrap_foundation`；#250 只读取 current locator/status；#108 消费跨层 traceability 与 subtraction scope；#154 继续拥有 task-local planning 模板。
- 引用 #264 Architecture Baseline 的 locator/version/status，不复制 Architecture authority 或改变其 public API。
- 保留 task index/history、semantic naming、base sync/reconciliation、Planning、Phase 2、Branch Review、semantic commit、publication/merge、Finish、cleanup 与 #262 Draft PR recovery 现有能力。

### R8 Distribution 与公共 API

canonical source 位于 `trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/`。同步 registry、Interface 1.4、extension/package inventory、workflow markers/routers、preset managed paths/README、dogfood installed copy，以及 Agents、Codex、Claude、Cursor 声明平台投影。Skill id、profile、schema、exit 和 consumer mapping 均作为版本化公共 API；不静默改写既有 Docs SSOT Plan schema 语义。

## 验收标准

- [ ] 新 Skill 为 active semantic package，四 profile、五 exit、consumer projection、error、example、eval 与 runtime wrapper 完整闭合。
- [ ] clean new repo 与已有 docs repo 的 bootstrap 能建立或复用唯一 authority，并保留版本/current/traceability 导航。
- [ ] 初始 provenance 不把 `code_recovered`、`inferred`、`unverified` 冒充 confirmed/current requirement。
- [ ] task-local planning 与 repository authority 分离；两个并行 task 使用不同 contribution locator，且不修改相同 shared authority 文件。
- [ ] promotion/repair 只重入当前 contribution；Requirements -> Design -> Test 的新增、替换、删除、拆分、合并均同步 traceability 与历史边界。
- [ ] 五出口只有唯一 consumer；public DTO 无无消费者字段、巨型 aggregate 或跨 Skill 私有 checkpoint 读取。
- [ ] #264 inheritance 与 Planning/Check/Branch Review/Publication/Acceptance/Finish 的最小 consumer contract 可执行且不复制语义判断。
- [ ] canonical、dogfood、installed package 与所有声明平台逐文件一致；preset reapply、dogfood drift、recursive zero `.new/.bak`、script executable mode 通过。
- [ ] package/contract/runtime/registry/workflow/consumer regression 通过，所有既有 atomic Guru Trellis 能力保持通过。
- [ ] live inventory 目标为 20 active package、71 command、20 complete command、85 package exit，以及 19 business invoke、83 business exit、31 workflow target、20 stop target；陈旧固定计数不得继续作为当前 authority。
- [ ] 一个代表性 clean throwaway 验证当前版本 package 安装、workflow entry 与公开 runtime 入口；完整多平台与 exact-candidate 矩阵明确留给 #260/#267。

## 非目标

- 不实现 #264 Architecture Baseline、#265 Bootstrap 编排、#260/#267 installer/release matrix 或 stable release。
- 不把 `.trellis/spec` 变成产品文档仓库，不无边界重写业务文档，不删除有版本边界的历史、ADR、release 或 migration 记录。
- 不修改 Trellis upstream、全局 npm、`node_modules`；不增加锁、TOCTOU、攻击模型或额外 repair Issue。

## Docs SSOT Plan

- `strategy`: `ssot_first`
- `canonical_authority`: 新 Skill 的行为/公共合同由 canonical package、registry、workflow consumer 与 preset inventory 共同承接；目标业务 repository 的具体 Requirements/Design/Test 正文仍只在其 `docs/` authority 中。
- `task_delta`: 本 task 的 `prd.md`、`design.md`、`implement.md` 只记录 #263 实施 delta，完成后不得成为公共合同的长期来源。
- `sync_scope`: package contract、profile/output schemas、consumer schemas、workflow routing、registry/extension/preset inventory、README 与平台投影。
- `subtraction_scope`: 删除重复定义、无 consumer 字段、过时示例/marker 和旧 authority 引用；不删除无关历史或既有 atomic capability。
- `completion`: Phase 2/Branch Review 验证 canonical 与所有投影一致，并在 Publication/Finish 使用最小 final sync status；无额外 shared tracked handoff。
