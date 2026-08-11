# #156 修复 Phase 0 跨 Skill 编排闭环与 source-preserving freshness 传递

## 1. Goal

让以下六个 mandatory Phase 0 Skills 在 clean 安装仓库中只依赖已声明的 public DTO、
workflow-owned 短生命周期 transition state 和当前 Skill 的 semantic authoring input 完成真实
producer-output -> consumer-input 链路，同时保留 source-preserving base freshness，并确保正常
路由只执行一次 authoritative sync：

```text
guru-sync-base
-> guru-discover-change-context
-> guru-clarify-requirements
-> guru-review-contract-wording
-> guru-review-change-request
-> guru-create-task-workspace
```

Live authority：<https://github.com/castbox/guru-trellis/issues/156>。

## 2. Confirmed Facts

- Issue #156 当前为 Open，close scope 仅包含 #156；#98、#132、#145 只作为关联或已完成
  authority，不由本 task 关闭。
- 本 task 基于 clean `main` commit `3bafc6c840e868a352f7820f42b287ca67e61ce2`
  创建。由于 #156 自身阻断正常 public Intake，用户已确认一次精确 bootstrap 例外；该例外只
  创建 branch/worktree/task/ledger，不构成实现或后续发布授权。
- Trellis 官方文档确认 `.trellis/workflow.md` 是 workflow 行为入口；流程分叉不得通过修改
  upstream、全局 npm 或 `node_modules` 实现。Spec marketplace 只承载可复用工程约定，不承载
  active task 或 runtime state。
- `guru-sync-base:synced` 当前只投影 repo/base/mode/continuation，但 Discovery owner result
  schema/checker仍要求完整 `guru-base-sync-result-1.0` base evidence。真实 public output 无法
  构造其 consumer 所需 freshness evidence。
- Discovery 已支持 `--owner-result -`，其余 semantic Phase 0 wrappers 仍通过 repo-local
  `--owner-result`，Readiness 还要求 `--owner-prerequisites` 与
  `--owner-change-request`，Workspace 还要求 `--owner-plan`。这些 supporting locators 没有由
  上游 public DTO 或正式 transition contract 产生。
- Clarification `clear` 当前只进入 workflow router；Wording `pass` 同样只进入 router，二者
  没有向 Readiness 交付 target/clarity/wording 的 checker-bound 最小 projection。现有测试会先
  写 repo-local owner/prerequisite 文件再调用 wrapper，因此只证明孤立 package，不证明完整
  public-only graph。
- `guru-sync-base` Markdown owner contract仍要求 AI 先运行低层
  `resolve-only -> execute -> check`，而 public wrapper内部再次运行同一 deterministic loop；
  这形成双轨 authoritative sync。
- Compatibility `prepare-task` 依赖 digest与声明为 `required:false` 的 `base_branch`。仅有 digest不能重建原始
  resolution source/ordered candidates；显式 base provenance在后续省略参数时可能退化为
  `config-candidate`，从而把表示差异误报为 base drift。
- #144 定义 Interface 1.3 public/consumer/projection基础合同；#145要求六包作为一个原子 graph
  激活；#178要求正常 pre-task 路径使用 stdin/stdout，只有真实中断恢复才可创建最小 ignored
  checkpoint。这三项历史合同继续作为实现基线，不重新实现或重开其已完成 scope。

## 3. Requirements

### R1. 阶段化 public transition contract

- 为完整 Phase 0 graph 定义 workflow-owned、versioned、阶段化 transition schema family；
  每个阶段只包含下一 consumer 直接需要且不能单靠 live reread恢复的最小 identity/freshness
  projection。
- `base_current`、`context_current`、`clarity_current`、`wording_current`、
  `readiness_current` 分别使用 closed schema；不得用一个含大量 optional/null 字段的总对象。
- 每条 typed exit -> unique consumer edge必须能由 producer public output、当前 transition
  state 与目标 Skill声明的 authoring fields确定性构造。unknown、multiple、missing、stale或
  unmapped transition必须 fail closed。
- Transition state只在当前调用链 stdin/stdout或调用者内存中存在；正常 pre-task 不写
  `.trellis/tasks/**`、`.trellis/workspace/**` 或 `.trellis/.runtime/**`，不进入 archive。

### R2. Call-local semantic owner transport

- 六包 public invocation必须正式声明调用期 envelope/transport，区分 public consumer input、
  workflow transition state与当前 Skill owner result；owner result不成为跨 Skill public DTO。
- 正常链路不得要求 AI 手工保存、发现或解析 repo-local `--owner-*` 文件，也不得读取/import
  `guru_team_trellis.py` 来组装输入。
- Recorder/checker/public wrapper继续复用现有 semantic gate结果并客观复验；脚本不得生成
  semantic pass、选择 route或把 expected exit当 actual exit。
- 旧 locator调用若为兼容需要保留，必须被声明为 compatibility-only、具有明确生命周期与
  removal condition；production happy path、workflow与端到端测试不得使用它。

### R3. Source-preserving base freshness

- `guru-sync-base:synced` 向其唯一 consumer交付最小 base provenance：resolution source、
  selected base、remote、ordered candidates、decision/base HEAD与
  `post_sync_resolution_sha256`；完整 private sync result不进入 DTO。
- Discovery和后续 refresh/workspace边界按该 provenance与 live Git验证所需 base identity；
  不因 caller漏传显式 base而切换 resolution source。
- Compatibility `prepare-task` 不得成为正常 Phase 0 hop。显式调用时必须继承同一 reviewed
  provenance；缺失时在 query本地返回稳定 blocked/diagnostic，且在 GitHub读取、fetch或
  semantic re-intake前停止。
- selected branch、ordered candidates、remote、HEAD、clean state或 authoritative content
  真正变化时继续 fail closed，并只进入声明的 refresh consumer。

### R4. 单一 authoritative sync

- `guru-sync-base` public invocation是正常 Phase 0 唯一 authoritative sync入口；workflow、
  platform prompt/command和 Skill Markdown不得先编排一遍低层 sync。
- Resolver、executor、checker继续作为该 Skill内部 deterministic components，可被单元测试或
  query-only diagnostic直接调用，但不得被描述成正常 AI workflow步骤。
- 同一 transition中每次 refresh只启动一轮新的完整 public sync，不复用或并行维护旧结果轨道。

### R5. 真实 public graph 验证

- 从 clean throwaway安装 canonical workflow和preset后，使用安装后的 public packages执行
  existing open issue happy path直至 workspace/task creation。
- 同一 harness覆盖 reviewed draft -> create issue -> refresh/re-entry、duplicate retain、
  duplicate retarget、wording `content_changed`、freshness refresh与每个 stop/re-entry family。
- 测试必须把 producer实际 stdout作为下一 edge输入；semantic owner payload必须先经过对应
  production recorder/checker，不得手工合成隐藏 prerequisite locator或 expected exit。
- 增加显式 `main` sync后 compatibility prepare省略 base仍保留 `explicit` provenance的回归，
  并覆盖 HEAD/content真实变化拒绝旧 evidence。

### R6. Canonical、安装副本与抗漂移闭环

- 同步修改 durable Specs、canonical workflow、六个 package、consumer/transition schemas、
  shared runtime、evals/tests、extension/registry/migration manifest、preset installer、README
  和声明支持的平台入口。
- 六包及其 transition graph作为一个 versioned activation unit安装；禁止 mixed old/new graph。
- Preset apply后必须处理全部 `.new`/`.bak`，验证 dogfood无漂移、clean install、existing repo
  workflow preview/switch、Trellis update/reapply、Codex、Claude、Cursor和manifest声明的其它入口一致。

### R7. Scope 与安全边界

- 不改写六个 Skills 已有 semantic ownership、问题分类、finding或human confirmation边界。
- 不把 public DTO/transition扩展为审计 artifact、完整 private checkpoint或用户授权记录。
- 不修改 Trellis upstream源码、全局 npm包或 `node_modules`；不引入无独立闭环的 wrapper Skill。
- 不处理恶意 actor、故意伪造/篡改、对抗性输入、并发压力、锁、TOCTOU、fault injection、
  crash consistency或跨 OS原子性。

## 4. Acceptance Criteria

- [ ] A1 / R1：六包全部 typed exits到唯一 consumer的 projection可机器验证，normal happy path
  只消费声明的 DTO、阶段 transition与当前 authoring input。
- [ ] A2 / R1-R2：pre-task完整链路不创建 owner-result/prerequisite/transition repo文件，不依赖
  对话隐式 private path，也不读取/import shared runtime source。
- [ ] A3 / R2：所有 production semantic wrappers支持正式 call-local transport；legacy locator
  如保留则只在明确 compatibility测试出现，normal workflow零引用。
- [ ] A4 / R3：sync provenance包含 source/candidates/HEAD/digest的最小 current identity，
  Discovery与后续 consumer能从其 public input完成 live freshness验证。
- [ ] A5 / R3：显式 `main` sync后 compatibility prepare省略 base不会因
  `explicit`/`config-candidate`表示差异触发 semantic re-intake；缺失 provenance在 query本地
  返回稳定 diagnostic。
- [ ] A6 / R3：selected HEAD、authoritative issue/content或其它声明 freshness identity真实变化
  时拒绝复用旧 transition并进入唯一 refresh route。
- [ ] A7 / R4：workflow、Skill contract和平台入口只调用一次 `guru-sync-base` public wrapper；
  低层 resolver/executor/checker仅为内部 component/diagnostic。
- [ ] A8 / R5：clean throwaway真实运行 existing issue、draft create/re-entry、duplicate retain/
  retarget、wording change、readiness/workspace和 stop/refresh分支，不使用隐藏 prerequisite文件。
- [ ] A9 / R5：每个 structurally distinct typed exit均有 production wrapper transcript、目标
  consumer schema复验与 expected-vs-actual事后断言。
- [ ] A10 / R6：source/installed package validation、dogfood drift、ownership、clean install、
  workflow preview/switch、update/reapply、platform parity及最终零 `.new/.bak`通过。
- [ ] A11 / R7：AI semantic check明确确认本 task只修复正常路径 correctness，未引入已排除的
  threat/concurrency hardening，且无未关闭 P0-P3 finding。
- [ ] A12：独立 Branch Review覆盖完整 `origin/main...HEAD` diff，PR readiness只使用
  `Closes #156`，#98/#132/#145均不关闭。

## 5. Docs SSOT Plan

Strategy：`ssot_first`。

- 先更新 `.trellis/spec/workflow/skill-package-contract.md`、`workflow-contract.md`、
  `data-contracts.md`、`companion-scripts.md`、`quality-guidelines.md` 与 `index.md`，明确阶段
  transition、call-local owner transport、single sync和 prepare compatibility规则。
- 再修改 canonical package/runtime/workflow/consumer schema，并同步
  `docs/requirements/{README.md,requirement-main.md,guru-team-trellis-flow.md}`。
- 最后通过 preset installer同步 dogfood和平台副本，更新根/workflow/preset README；生成副本
  不是语义 source。
- 本 task三份 planning文档只记录任务范围与执行计划，不替代 durable SSOT。

## 6. Out of Scope

- 修改六个 Phase 0 Skills的产品语义判断或用户确认策略。
- 把 #98 umbrella、已关闭 #132或已关闭 #145纳入 close scope。
- Finalizer、Phase 1/2/3其它 public transition的泛化重构。
- 历史 archive迁移、恶意篡改防御、并发/锁/原子性加固。
- 未经后续独立授权的 commit、push、PR、merge、issue closure或 cleanup。

## 7. Open Questions

无。Live Issue、当前 canonical/runtime/tests、官方 Trellis文档与 #144/#145/#178历史合同已足以
确定本次交付边界。
