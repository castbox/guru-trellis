# #110 `guru-sync-base` 闭环 Skill

## 1. 目标

在 Guru Team 扩展中交付公共 `guru-sync-base` Skill。该 Skill 在任何 issue、Docs、代码、测试或历史语义读取前解析 selected base，刷新 `origin/<base>`，仅执行安全 fast-forward，并证明 local base、remote base 与 decision checkout HEAD 三者 SHA 完全一致。

本任务只关闭 [castbox/guru-trellis#110](https://github.com/castbox/guru-trellis/issues/110)。父 issue #98 与后续 issue #111 保持 open。

## 2. 范围

### 2.1 必须交付

- 激活稳定公共 Skill id `guru-sync-base`，提供 canonical package、`SKILL.md`、interface、contract reference、scripts、result schema、example 与 package tests。
- Workflow mode 消费主会话已经完成的 tool-free route 与 base clues；repo-changing intake 的第一条 repo 或 network action 必须由本 Skill 发起。
- Standalone mode 仅处理 Git/base freshness，不进入 issue intake、context discovery、task 创建或历史检索。
- Base 解析顺序固定为：用户显式 base；Guru Team repo config 中唯一 scalar base；remote default branch；去重后唯一 fallback candidate。
- 零个或多个 fallback candidate 必须返回 `blocked`，不得回退 current branch。
- Fetch 前必须先输出 selected-base resolution evidence，由 AI 确认 invocation intent、resolution source 与 selected base；executor 必须绑定该 resolution digest 并在执行边界重算。
- Decision checkout dirty、local base 缺失、remote 缺失、fetch 失败、local/remote diverged、非 base checkout 无法执行安全 fast-forward、三方 HEAD 不一致均必须返回 `blocked`。
- Local base 落后且 local base 是 remote base ancestor 时，仅在 decision checkout 正位于 selected base 上执行 `git merge --ff-only`。
- AI Review Gate 必须审查 invocation scope、selected-base evidence、Git facts 与真实副作用；deterministic validator 只校验 schema、digest、Git identity 与 freshness。
- 外部出口固定为 `synced`、`skipped`、`blocked`，每个出口只有一个 consumer。
- `prepare-task` planner 与 executor 必须复用同一 base resolver/sync contract；executor 在 issue/worktree/task 副作用前重跑 freshness。
- Workflow `synced` 必须把 repo-external resolution file 与 digest 作为受控 Phase 0 lease 转移给唯一 consumer；同一 lease 必须贯穿后续所有 `prepare-task` planner/executor freshness guard，直到 Phase 0 成功、阻塞、放弃或被新 invocation 取代后确定性释放。
- Standalone 不得转移 resolution lease；result evidence 与 resolution evidence 必须在返回 typed exit 前清理。Workflow mode 的 result evidence 同样必须在 `synced` 前清理，只有 resolution lease 能跨越 typed exit。
- Canonical workflow、preset installer、声明平台、dogfood 副本、durable docs/spec、README、throwaway install 与 `trellis update`/preset reapply 验证必须同步。

### 2.2 不做

- 不实现 `guru-discover-change-context`；#110 只保留稳定 workflow route consumer，#111 再把该 route 的内部实现收敛为独立 Skill。
- 不实现 requirement clarification、contract wording review、change request review 或 task workspace creation。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 不恢复 tracked handoff、workspace journal、repo-level history index 或共享 runtime cache。
- 不改变现有 `.trellis/.developer` 继承合同。

## 3. 行为合同

### 3.1 Workflow mode

1. 主会话在无工具阶段判定 route，并明确本次 invocation 是 repo-changing refresh 还是 non-repo skip。
2. Repo-changing route 必须先调用 `guru-sync-base --resolve-only`，AI 确认 selected-base evidence 后才调用绑定 resolution digest 的 executor。
3. 通过前不得读取 issue、Docs、代码、测试或 archived history。
4. `synced` 进入稳定 workflow route `guru-discover-change-context`。
5. `skipped` 返回原 non-repo route；该出口不得出现在 standalone mode。
6. `blocked` 立即停止，不得继续语义读取或创建 GitHub/worktree/task 副作用。

### 3.2 Standalone mode

1. 用户必须显式要求刷新或验证 base。
2. Workflow/standalone 使用完全相同的 Git preconditions、sync executor、AI Review Gate 和 validator。
3. 成功只返回 `synced`；任何无法证明 freshness 的路径返回 `blocked`。

### 3.3 Side-effect boundary

- Forward behavior 只产生 `git fetch`、安全 `git merge --ff-only` 与临时 evidence 文件。
- Evidence 文件必须位于 repository root 之外；公共 package、repo runtime 与 pre-task tracked 路径不得保存本机 evidence。
- Workflow resolution lease 只能保存在当前 AI invocation 的临时 handoff 中，不得写入 task artifact、repo runtime、shared cache、README example 或 tracked/review log；lease release executor 必须校验外部路径、symlink/component boundary 与 expected digest 后删除并确认无残留。
- AI Gate 或 validator 失败后不得出现 GitHub mutation、history read/write、worktree 创建或 Trellis task 创建。

## 4. 验收标准

- [ ] `guru-sync-base` 在 registry 中是 active public API，workflow/standalone preconditions 完全一致。
- [ ] Workflow 以 stable id 显式 mandatory invoke；frontmatter auto-match 不是唯一调用保证。
- [ ] `synced`、`skipped`、`blocked` 均有唯一 marker consumer，unknown/multiple/unmapped exit fail closed。
- [ ] 所有 repo-changing 语义读取发生在 fresh equality 之后。
- [ ] Base resolver 严格执行四级顺序，current branch 不充当隐式 fallback。
- [ ] Resolve-only evidence 在 fetch/ff-only 前经过 AI 确认，executor 拒绝 stale 或 mismatch resolution digest。
- [ ] Dirty、missing local、missing remote、fetch failure、ambiguous fallback、diverged、unsafe fast-forward 与 HEAD mismatch 测试全部通过。
- [ ] Success evidence 通过 Draft 2020-12 schema、digest 与 live Git freshness validator。
- [ ] `prepare-task` planner 在 issue 读取前复用 sync contract，executor 在副作用前重跑。
- [ ] Workflow `synced -> prepare-task` 使用同一 resolution lease；所有 Phase 0 terminal route 都调用确定性 release，standalone 返回前完成 cleanup，且不存在 repo/runtime/task evidence 残留。
- [ ] Source、installed、package、dispatcher、preset、all-platform dogfood 与 drift validation 通过。
- [ ] 干净 throwaway repo 完成 marketplace workflow 安装、preset 安装、standalone invocation、真实 `synced -> prepare-task` planner/mutation guard/release 链、`trellis update`、workflow reapply、preset reapply、零 evidence 残留与零 `.new`/`.bak` 验证。
- [ ] 三份 public README、requirements 与 `.trellis/spec/` 与实现一致。
- [ ] 安全检查确认 package/example/artifact/log 不含 secret、`.env`、签名 URL、客户数据或本机绝对路径。

## 5. Docs 状态

- `docs_state`: `partial_docs`
- 现有 durable docs 已描述 Phase 0 base freshness 与 closed-loop package infrastructure，但尚未定义 `guru-sync-base` 的四级解析、三方 equality、typed exits 与 standalone contract。
- 权威同步计划位于 [design.md](./design.md) 的 `Docs SSOT Plan`。

## 6. 中台知识门禁

`not_applicable`。本任务修改 Guru Team Trellis extension，不涉及中台 SDK、API 或业务框架合同。
