# 技术设计

## 1. 设计原则

Issue #108 是对既有流程 owner 的横向合同增强，不建立新的语义 owner。所有判断仍由 AI 在当前 owner 内完成，确定性脚本只提供事实和校验。实现采用“先收敛 durable contract，再同步 canonical/preset/dogfood，再补定向 runtime/eval/test”的 `ssot_first` 顺序。

## 2. Owner 与承接边界

| 能力 | 唯一 owner | 承接内容 | 明确不做 |
| --- | --- | --- | --- |
| 方案机制 | `guru-approve-task-plan`、`guru-qualify-solution-mechanism` | 直接删改、复用、兼容必要性与具体例外选择 | 新增 subtraction Skill |
| 实施 | 现有 `trellis-implement` caller/平台入口 | approved plan 的退出方案、发现候选后的既有 qualification/owner route | 擅自新增兼容或先改后报 |
| Phase 2 | `guru-check-task` | 完整 worktree 的废弃退出、支持合同、增长复审、code/docs 双维度 | 读取 Branch Review 或脚本代替语义 pass |
| Branch Review | `guru-review-branch` | 完整 committed range 的独立重算与 finding route | 读取 Phase 2 checkpoint、推迟到 Publication |
| RDT | `guru-maintain-requirements-design-test-ssot` | requirement/design/test 退出、traceability、subtraction/promotion | 新建 authority ledger |
| Architecture | `guru-maintain-architecture-baseline` | before/after、compatibility-and-exit、owner、GAP、promotion | 重复 RDT 或 fitness 判断 |

Planning 只在真实 scope/authority/兼容选择时交互；明确属于当前范围的废弃资产退出不重复询问。兼容批准不被 recorder、validator 或 public DTO 表示。

## 3. 语义合同

### 3.0 复杂度、解耦与文件规模边界

长期可维护性与当前验收同等重要。任何新增字段、状态、重试、锁、
fallback、adapter、receipt 或持久化必须指向真实直接 consumer；仅以攻击
防护、无限兼容、并行压力、非常规 crash 或形式幂等为理由的复杂度不进入
正常合同。任务方案还必须检查是否重复既有 owner、污染共享 DTO/schema、
偏移 Architecture 决策或制造 hack-specific 路径；发现时回到既有
qualification/Architecture owner。

本任务建立未来变更门禁：每个被 task 触及的非生成代码文件最多 3000 行，
达到或超过阈值必须做机械式切分或小幅解耦式重构并由 AI 审查；历史未触及
的大文件不纳入本 task 的批量重构。生成文件和 canonical managed projection
不计入该源码阈值，但继续执行其既有生成与 drift 校验。

### 3.1 直接演进决策

每个删除/替换/合并/新增候选从当前入口和责任出发，形成最小候选集合：现有 owner、调用者、注册/配置 consumer、受影响测试和文档。默认路径是删除、原位修改、合并或同步 consumer。只有直接演进不能满足真实合同，或存在明确服务端稳定性责任，才形成兼容候选。

### 3.2 废弃退出判断

检查不以 `rg` 零命中为结论。AI 需结合调用者、注册、反射、依赖注入、外部调用、公共 API、配置/schema 读取者和测试入口判断：独占资产退出；共享资产保留其剩余职责；仅测试调用的未接入生产实现不能冒充 accepted production path；合法局部重复不机械抽象。证据不足走既有 owner/blocked route，不转化为自动兼容保留。

### 3.3 兼容例外

当前支持合同分为：

- `target_native`：直接演进，不保留 dual-read、legacy adapter 或旧执行路径。
- 已有服务端对外稳定性合同：按合同保留，不重复询问，但不得扩大支持范围。
- 新增/扩大/延长的其它兼容：先在对话呈现 consumer、直接演进影响、精确范围、退出和验证，取得针对该方案的明确批准后才可实施。

一次性迁移与运行时长期兼容分开判断；必要迁移继续遵守数据和副作用权限合同。批准不是长期证据，长期只记录支持合同本身。

### 3.4 双 subtraction 维度

Phase 2 与 Branch Review 各自独立判定：

- `code_subtraction`：production/runtime、script、schema、config、dependency、注册项、测试入口是否退出或保留有真实职责。
- `docs_ssot_subtraction`：requirement/product、design、test、operations/navigation 及 RDT/Architecture authority 是否退出旧语义、合并重复权威或保留合法历史。

删除型增长只作为 AI 复审信号，不是机械门槛；必须按 production、test、generated/managed、docs 分类解释必要增长。合法历史、contribution、ADR、release/changelog/migration、canonical 受管副本不视为当前冗余实现。

## 4. 计划中的目标文件分区

实际文件由 live ownership 和 current baseline 在实施前重新确认。预期范围：

- canonical workflow/README 与 preset README：`trellis/workflows/guru-team/`、`trellis/presets/guru-team/`。
- workflow/preset/docs durable specs：`.trellis/spec/workflow/`、`.trellis/spec/preset/`、`.trellis/spec/docs/`。
- canonical package contracts/prompts：`trellis/skills/guru-team/packages/guru-approve-task-plan`、`guru-check-task`、`guru-review-branch`、必要的 qualification/relevant caller 文案。
- 平台入口与安装投影：`trellis/presets/guru-team/overlays/`，随后由现有 apply 同步 `.agents/`、`.codex/` 与其他声明平台的 dogfood 副本。
- 定向 tests/evals：上述 package 的 contract/runtime/eval tests，以及代表性 synthetic semantic scenarios。

不修改 `.trellis/agents/check.md`、上游 `trellis-*` Skill/Agent、全局 npm/node_modules；不为增长或调用图建立通用报表/索引。

## 5. 流程与 freshness

Planning 完成后先运行 planning wording route，再调用 `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`，最后由 `guru-approve-task-plan` 重读当前 requirement、三份 planning artifact、Docs SSOT Plan、RDT/Architecture authority 与 scope ledger。实施发现扩展 scope、owner、持久化、外部或架构边界时，按现有 `implementation_discovery` route 重新取得 Architecture 结果。

Phase 2 先做 `phase2_candidate_set` 与 solution mechanism qualification，再由 `guru-check-task` 执行完整九维检查；Branch Review 先做 `branch_review_candidate_set`，再由 `guru-review-branch` 独立审查完整 `origin/<base>...HEAD`。两者均只保存既有最小 owner-private 结果，不跨阶段传递 subtraction transcript 或授权。

## 6. Docs SSOT Plan

- `docs_state`: `complete_docs`。证据为当前 Requirements、Design、Test、Architecture 入口及 `.trellis/spec/workflow/`、`.trellis/spec/preset/`、`.trellis/spec/docs/`；当前仓库已有 workflow/skill/package/architecture/RDT durable authority，不把 active task 当作 authority。
- `strategy`: `ssot_first`。Issue #108 是跨 planning、implementation、Phase 2、Branch Review、RDT/Architecture 与 docs contract 的边界变更，先更新 durable source 可避免 task artifact、canonical package 和 dogfood 投影分叉。
- 预期 durable docs/spec 影响：`docs/requirements/evolution/` 的 current contract/traceability（如 live owner 判定为 target-only 则只写 contribution）；`docs/design/evolution/` 的 owner/contract/decision/traceability；`docs/test/evolution/` 的 semantic fixture/strategy/traceability；`.trellis/spec/workflow/semantic-retrieval.md`、`workflow-contract.md`、`skill-package-contract.md`、`quality-guidelines.md`；`.trellis/spec/docs/public-docs.md`；`.trellis/spec/architecture/baseline-usage.md` 与 Architecture change-contract 相关引用；canonical/preset/workflow README。
- RDT/Architecture 策略：先调用两个 `task_impact_sync`，由 owner 判断 contribution、direct sync、ADR 和 promotion；本 task 不直接竞争 shared current authority。若 owner 判定无影响，不新增文档，只保留明确理由。
- task artifact delta：本文的 owner 分区、双 subtraction 维度、兼容例外交互、历史边界、验证矩阵和非目标需在实现完成后 merge 到对应 durable authority；不复制完整 task history、搜索过程、授权过程、逐轮 evidence 或路径/hash bundle。
- merge checkpoint：任何 package/schema/runtime/test 编辑前，必须确认 durable source/spec 的最小合同已完成并被实施计划定位；实现后 Phase 2 必须重读并检查 durable docs、canonical package、installed projection、tests 与行为一致。若 durable authority 不完整，走 RDT/Architecture `revision_required`、`baseline_incomplete`、`contract_incomplete` 或既有 owner route。
- overlay/dogfood：canonical overlay 修改后运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 与 `check-dogfood-overlay-drift.sh`；逐个处理 `.new/.bak`，不静默覆盖用户修改。
- knowledge gate：本任务仅修改 Guru Team Trellis extension，不涉及中台 SDK/API；`guru-knowledge-center` 为 `not_applicable`。

## 7. 设计追踪

| 需求 | 设计承接 | 计划承接 | 主要验证 |
| --- | --- | --- | --- |
| R1-R2 | 第 2、3.1-3.2 节 | implement 1-3 | planning scenarios、Phase 2、Branch Review |
| R3-R5 | 第 2、3.3 节 | implement 4-5 | exception dialogue eval、contract tests |
| R6-R7 | 第 3.4 节 | implement 6-7 | diff category review、docs/RDT/Architecture checks |
| R8 | 第 5-6 节 | implement 8-10 | runtime/schema/drift/throwaway |
