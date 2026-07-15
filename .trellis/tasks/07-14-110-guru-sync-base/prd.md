# #110 `guru-sync-base` 闭环 Skill

## 1. 目标

在 Guru Team 扩展中交付公共 `guru-sync-base` Skill。该 Skill 在任何 issue、Docs、代码、测试或历史语义读取前解析 selected base，刷新 `origin/<base>`，仅执行安全 fast-forward，并证明 local base、remote base 与 decision checkout HEAD 三者 SHA 完全一致。

本任务只关闭 [castbox/guru-trellis#110](https://github.com/castbox/guru-trellis/issues/110)。父 issue #98 与后续 issue #111 保持 open。

## 2. 范围

### 2.1 必须交付

- 激活稳定公共 Skill id `guru-sync-base`，提供 canonical package、`SKILL.md`、interface、contract reference、scripts、result schema、example 与 package tests。
- Workflow mode 消费主会话已经完成的 tool-free route 与 base clues；repo-changing intake 的第一条 repo 或 network action必须由本 Skill 发起。
- Standalone mode 只处理 Git/base freshness，不进入 issue intake、context discovery、task 创建或历史检索。
- Tool-free route classification 与 standalone 用户意图识别属于 caller-side routing，不进入 Skill 的 deterministic entry contract；Skill 只接收可机器校验的 `invocation_mode` 与 route id。
- Base 解析顺序固定为：用户显式 `--base`；Guru Team repo config 中非空 scalar `base_branch`；按 `base_branch_candidates` 配置顺序选择首个存在的 exact local 或 remote-tracking branch；候选均不存在时使用 remote default branch。
- `base_branch_candidates` 缺省顺序为 `dev -> develop -> main -> master`；同名候选去重后保留首次出现顺序。所有来源都无法选定 base 时必须返回 `blocked`，不得回退 current branch。
- Workflow 在调用 Skill 前由 AI 完成 tool-free route classification；Skill 内的 resolver 通过 stdout 输出 selected-base resolution facts 与 pre-sync digest，executor 必须重算并绑定该 digest，不再插入 selected-base AI confirmation。
- Execute 成功后必须基于同步后的 decision checkout 生成 stdout-only post-sync resolution digest；validator 校验 live Git 与该 post-sync identity 后，workflow 和 `prepare-task` 只能把 post-sync digest 传给下一次 freshness guard。每次 guard 如发生 fast-forward，必须返回新的 post-sync digest供下一副作用边界使用。
- Decision checkout dirty、local base 缺失、remote 缺失、fetch 失败、local/remote diverged、非 base checkout 无法执行安全 fast-forward、三方 HEAD 不一致均必须返回 `blocked`。
- Local base 落后且 local base 是 remote base ancestor 时，只能在 decision checkout 正位于 selected base 上执行 `git merge --ff-only`。
- Skill interface contract 升级到 schema `1.2` 并新增必填 `judgment_mode`：`semantic` 保持五阶段闭环，`deterministic` 使用 `forward_behavior -> recorder_validator -> typed_exit` 三阶段闭环。
- `guru-sync-base` 必须声明 `judgment_mode=deterministic`；其输入、状态转换、副作用和 pass/block 条件均由 executor/validator 机器验证，Skill 内不得保留 selected-base AI confirmation、post-execution AI Review Gate 或 conditional human confirmation。
- 当前 active `guru-create-task-commit` interface 同步迁移为 `judgment_mode=semantic`，行为不变；Phase 2 `trellis-check`、Branch Review Gate 与 PR readiness 三类语义门禁不得借此例外降级。
- 外部出口固定为 `synced`、`skipped`、`blocked`，每个出口只有一个 consumer。
- `prepare-task` planner 与 executor 必须调用同一 base resolver/sync core；executor 在 issue/worktree/task 副作用前重跑 freshness。
- Canonical workflow、preset installer、声明平台、dogfood 副本、durable docs/spec、README、throwaway install 与 `trellis update`/preset reapply 验证必须同步。

### 2.2 不做

- 不实现 `guru-discover-change-context`；#110 只保留稳定 workflow route consumer，#111 再把该 route 的内部实现收敛为独立 Skill。
- 不实现 requirement clarification、contract wording review、change request review 或 task workspace creation。
- 不把 repo-external result/resolution 文件、evidence lease、release executor、quarantine、replacement cleanup 或 terminal zero-residue 定义为 #110 合同。
- 不防御恶意同 UID 进程持续竞争文件系统 namespace；本任务的安全边界是 Git 状态与 ref 操作，不是临时文件取证系统。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 不改变现有 `.trellis/.developer` 继承合同。

### 2.3 Requirement provenance

| 合同 | 分类 | 来源与边界 |
| --- | --- | --- |
| Public Skill、workflow/standalone mode、`fetch`、`ff-only`、三方 HEAD equality、validator 与三个 typed exits | `explicit_requirement` | Live issue #110 的定位、闭环、外部出口与验收标准 |
| Base resolution 依次使用显式 `--base`、scalar `base_branch`、有序 `base_branch_candidates`、remote default；候选缺省顺序为 `dev -> develop -> main -> master` | `confirmed_scope_correction` | #110 前 `prepare-task` 的 config 与 `resolve_base_branch()` 按列表顺序选择首个 existing ref；用户确认 #110 必须保留该既有语义，[GitHub correction comment](https://github.com/castbox/guru-trellis/issues/110#issuecomment-4976030247) 明确覆盖 issue body 中 remote-default-first 的旧表述 |
| `prepare-task` planner/executor 复用相同 resolver/sync core，并在副作用前重跑 | `explicit_requirement` | Live issue #110 的 Scope 与 Acceptance Criteria |
| Resolution/result 使用 stdout facts、executor 绑定 resolution digest、validator 重读 live Git facts | `necessary_implementation_choice` | 用户在 #110 scope correction 中确认保留；用于完成 AI/script 分层和 freshness 证明，不扩张产品或威胁边界 |
| Resolve-to-execute 使用 pre-sync digest；成功同步后产生 post-sync digest，`prepare-task` 与后续 mutation guard 逐次消费上一 guard 的 post-sync digest | `phase2_design_correction` | 独立 Phase 2 F-004 证明同一 digest 同时绑定同步前 HEAD 和同步后 prepare 不可成立；该修正保留 digest binding，只分离连续状态转换的 identity generation |
| Skill interface schema `1.2` 增加 `semantic` / `deterministic` 双 profile；`guru-sync-base` 省略形式化 AI Review Gate，既有语义 Skill 保持五阶段 | `confirmed_scope_expansion` | 用户确认完全机器可验证 Skill 可使用显式 deterministic 例外，并要求将 `AGENTS.md`、workflow/spec、interface schema、validator 与 tests 纳入当前 task；[GitHub scope comment](https://github.com/castbox/guru-trellis/issues/110#issuecomment-4976105007) 记录了适用条件与不放宽边界 |
| 不建立 repo-external result/resolution evidence file、lease、release、quarantine 与 replacement cleanup | `confirmed_scope_boundary` | Live issue #110 未要求该机制；用户确认删除先前 review 引入的错误扩张 |
| 恶意同 UID actor、namespace race、fault injection 与跨 OS 原子删除 | `out_of_scope_proposal` | 未被 live issue 触发且未获专用 scope expansion confirmation，不得成为当前 P0-P3 finding 或实现项 |

## 3. 行为合同

### 3.1 Workflow mode

1. 主会话在无工具阶段判定 route，并明确本次 invocation 是 repo-changing refresh 还是 non-repo skip。
2. Repo-changing route 必须先调用 `guru-sync-base --resolve-only`；该命令用 stdout 输出 selected-base facts 与绑定同步前 decision checkout 的 `resolution_sha256`。
3. Executor 接收 resolver 输出的 expected pre-sync digest，在执行边界重新解析相同输入；digest 或重算 facts 不匹配时直接返回 `blocked`。
4. Executor 完成 already-equal 或安全 fast-forward 后，基于同步后的 decision checkout 输出 `post_sync_resolution` 与 `post_sync_resolution_sha256`；发生 fast-forward 时该 digest 必须区别于 pre-sync digest。
5. Validator 重读 live Git facts并校验 schema、pre-sync resolution digest、post-sync resolution digest、facts digest 与三方 equality；通过后直接产生 typed exit，不执行 Skill 内 AI Review Gate 或 human confirmation。
6. `synced` 只携带 validator-passed post-sync digest 进入稳定 workflow route `guru-discover-change-context`；`prepare-task` 的第一条 guard 消费该 digest。
7. 通过前不得读取 issue、Docs、代码、测试或 archived history。
8. `skipped` 返回原 non-repo route；该出口不得出现在 standalone mode。
9. `blocked` 立即停止，不得继续语义读取或创建 GitHub/worktree/task 副作用。

### 3.2 Standalone mode

1. 用户必须显式要求刷新或验证 base。
2. 平台入口在 Skill 调用前完成该显式意图识别；Skill 内只校验 normalized standalone mode，不重新判断用户意图。
3. Workflow/standalone 使用相同的 Git preconditions、deterministic sync executor 与 validator，不在 standalone mode 补回 AI Review Gate 或 human confirmation。
4. 成功只返回 `synced`；任何无法证明 freshness 的路径返回 `blocked`。

### 3.3 Side-effect boundary

- Forward behavior 只能产生 `git fetch` 与安全 `git merge --ff-only`。
- Resolution/result facts 通过命令 stdout 传递；pre-sync 与 post-sync digest 分别绑定相邻状态转换，不引入跨步骤临时文件生命周期。
- Resolver、executor 或 validator 失败后不得出现 GitHub mutation、history read/write、worktree 创建或 Trellis task 创建。

## 4. 验收标准

- [ ] `guru-sync-base` 在 registry 中是 active public API，workflow/standalone preconditions 完全一致。
- [ ] Skill interface schema `1.2` 强制 `judgment_mode` 与 `ordered_stages` 匹配：`semantic` 只能使用五阶段，`deterministic` 只能使用三阶段；所有 active interface 与 source/installed validator、fixtures 同步迁移。
- [ ] `guru-sync-base` 使用 deterministic profile；`guru-create-task-commit` 继续使用 semantic profile，Phase 2 check、Branch Review 与 PR readiness 的 AI 判断责任不变。
- [ ] Workflow 以 stable id 显式 mandatory invoke；frontmatter auto-match 不是唯一调用保证。
- [ ] `synced`、`skipped`、`blocked` 均有唯一 marker consumer，unknown/multiple/unmapped exit fail closed。
- [ ] 所有 repo-changing 语义读取发生在 fresh equality 之后。
- [ ] Base resolver 严格执行四级顺序；`dev` 与 `main` 同时存在时选择 `dev`，`develop` 与 `main` 同时存在时选择 `develop`，候选均不存在时才读取 remote default，current branch 不充当隐式 fallback。
- [ ] Resolve-only stdout facts 的 pre-sync digest 直接绑定 executor；executor 拒绝 stale 或 mismatch identity，成功后生成 post-sync digest，validator 重读 live Git facts，Skill 内无 selected-base AI confirmation、post-execution AI Review Gate 或 conditional human confirmation。
- [ ] 真实 behind-base 链路完成 `resolve -> execute ff-only -> validate -> prepare`；prepare 消费 post-sync digest，不复用同步前 digest。后续 planner/mutation guard 每次消费上一 guard 输出并返回下一 post-sync digest。
- [ ] Dirty、missing local、missing remote、fetch failure、ordered-candidate precedence、candidate-to-remote-default fallback、diverged、unsafe fast-forward 与 HEAD mismatch 测试全部通过。
- [ ] Success result 通过 Draft 2020-12 schema、digest 与 live Git freshness validator。
- [ ] `prepare-task` planner 在 issue 读取前调用 shared sync core，executor 在副作用前重跑；config、branch、dirty 或 digest drift 均在对应 fetch/mutation 前阻塞。
- [ ] Source、installed、package、dispatcher、preset、all-platform dogfood 与 drift validation 通过。
- [ ] 干净 throwaway repo 完成 marketplace workflow 安装、preset 安装、behind base 的真实 `resolve -> execute ff-only -> validate -> prepare`、already-equal 链、`trellis update`、workflow reapply、preset reapply 与零 `.new`/`.bak` 验证。
- [ ] 三份 public README、requirements 与 `.trellis/spec/` 与实现一致。
- [ ] 安全检查确认 package/example/artifact/log 不含 secret、`.env`、签名 URL、客户数据或本机绝对路径。

## 5. Docs 状态

- `docs_state`: `partial_docs`
- 现有 durable docs 已描述 Phase 0 base freshness 与 closed-loop package infrastructure，但尚未完整定义 `guru-sync-base` 的四级解析和 deterministic Skill 例外，且 #110 当前实现未保留 `prepare-task` 原有的 `dev -> develop -> main -> master` 有序候选语义。
- 权威同步计划位于 [design.md](./design.md) 的 `Docs SSOT Plan`。

## 6. 中台知识门禁

`not_applicable`。本任务修改 Guru Team Trellis extension，不涉及中台 SDK、API 或业务框架合同。
