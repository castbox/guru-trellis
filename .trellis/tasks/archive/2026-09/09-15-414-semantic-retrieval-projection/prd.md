# #414 收敛 semantic retrieval ownership projection

## 1. 目标

按 Issue #414 的 live authority 修复 semantic retrieval 合同与当前 Trellis
ownership 基线之间的漂移，使四个 Guru semantic owners 继续完整消费统一
SSOT，同时保持官方 `trellis-*` skills、agents 与 workers 为 upstream-owned、
byte-unchanged，并解除 #410 新 exact candidate 的前置阻塞。

## 2. 权威与已确认事实

- Requirement authority：GitHub Issue #414 及 2026-09-15 comments
  `5678843409`、`5679841798`、`5680255943`；三者依次完成 13-path authority
  replacement、`guru-reconcile-task-base` 第五 owner 收敛，以及 shared
  skill-package contract 中残留 direct-consumer 声明的最小范围补齐。
- 当前回归基线：`origin/main@0c97afd0abd4c01f8ede3aca97a7f96beaf0e0b0`，
  focused test 共 4 项，其中陈旧的 13-path assertion 产生 13 个 failure。
- Ownership authority：`.trellis/spec/preset/upstream-ownership.md`、当前
  workflow/Skill package contract 和 #329 均要求官方 `trellis-*` 文件不由
  Guru preset patch 或 claim。
- 当前 canonical 与 dogfood semantic retrieval spec 仍把
  `trellis-research`、`trellis-session-insight`、`trellis-implement`、
  `trellis-check` 列为 retrieval owners，已与 ownership authority 漂移。
- 当前测试已经具有四个 Guru owner 的正向约束，以及
  `guru-review-change-request`、`guru-review-contract-wording`、
  `guru-create-task-commit`、`guru-review-task-publication`、
  `guru-finalize-task` 五个 Guru non-owner 的不扩权约束，但仍保留要求
  13 个 upstream-owned 文件引用 Guru spec 的旧测试。
- `guru-reconcile-task-base` 当前 canonical Skill/contract 也直接读取 Guru
  semantic retrieval SSOT 并执行 concept-family、evidence-coverage 判断；这是
  支持路径上的第五个有效 owner，未被原四-owner focused inventory 覆盖。
- Canonical `skill-package-contract.md` 仍要求该 Skill 读取同一 broad SSOT，
  preset reapply 会把此声明投影到 dogfood spec；这会在 package-local wording
  修复后继续保留第五个 direct consumer。

## 3. 功能需求

### R1. Semantic owner 边界

- 唯一 Guru semantic retrieval owners 保持为：
  `guru-discover-change-context`、`guru-clarify-requirements`、
  `guru-check-task`、`guru-review-branch`。
- Semantic retrieval SSOT 必须明确：Guru caller 在直接检索，或消费
  upstream worker/provider evidence 后形成结论时，负责 concept-family、
  evidence coverage 和 sufficiency 判断。
- 官方 `trellis-*` skills、agents、workers 不直接拥有或消费 Guru semantic
  retrieval SSOT，不得因本任务获得 Guru managed ownership。
- `guru-reconcile-task-base` 不得成为第五个 retrieval owner；它继续基于 closed
  caller input、exact old/new base pair、live authority/planning locators、candidate
  delta/validation facts 与 `base_impact_candidate_set` 完成既有 bounded judgment，
  不再直接拥有或消费 broad semantic retrieval SSOT。

### R2. Canonical 与 installed projection

- 长期源头只修改
  `trellis/presets/guru-team/spec/workflow/semantic-retrieval.md` 与
  `trellis/presets/guru-team/spec/workflow/skill-package-contract.md` 中直接描述
  semantic retrieval owner 边界的现有段落。
- `.trellis/spec/workflow/semantic-retrieval.md` 必须由官方支持的 preset apply
  同步，并与 canonical bytes 一致；对应
  `.trellis/spec/workflow/skill-package-contract.md` 也必须由 preset apply 同步，
  不得把 dogfood copy 当作独立源头手改。
- 不修改官方 Trellis 生成文件来恢复已删除的 13 个引用。

### R3. Ownership-aware regression test

- 删除要求 13 个 upstream-owned projection 引用 Guru SSOT 的陈旧正向断言。
- 保留并加强四个 Guru owner 对 SSOT、semantic eval 与 fixture 的现有约束。
- 保留 Guru non-owner 不扩权约束，并增加官方 `trellis-*` 文件不被纳入 Guru
  owner/managed inventory、也不要求 Guru patch 的客观断言。
- 将 `guru-reconcile-task-base` 纳入 non-owner 回归约束，防止其重新获得对 Guru
  semantic retrieval SSOT 的直接依赖。
- 增加 shared canonical skill-package contract 的 non-owner 断言，防止该公共
  wording 再次要求 reconcile 直接读取 broad SSOT。
- Canonical 与 installed semantic retrieval spec 的 byte identity 继续受测。

### R4. 验证与发布边界

- 运行 focused semantic retrieval source test、source/installed
  `check-skill-packages.sh`、preset apply tests、upstream ownership validator、
  preset reapply 和 dogfood drift。
- 运行一个与本变更相称的 clean throwaway install/update/reapply，并验证
  installed semantic retrieval contract；不扩张为完整 release 多平台矩阵。
- 运行 secret scan、`.new`/`.bak` 与临时 runtime/cache residue hygiene、
  `git diff --check` 和 task/workspace validation。
- 按标准 Phase 2、task commit、完整 Branch Review、Publication、Finalizer、
  preparation PR 与 Merge 顺序推进。
- PR 只交付 #414，并仅 `Refs #410`。#410 必须保持 OPEN；本任务不创建 tag、
  GitHub Release，也不关闭 #410。
- #414 合并后，#410 必须基于新的 `origin/main` 冻结全新的 exact candidate；
  不得复用 `0c97afd0...`、`6b97d4c7...` 或任何 pre-merge release evidence。

## 4. 验收标准

- [ ] AC1：canonical SSOT 只声明四个 Guru semantic owners，并明确 Guru caller
  对 upstream worker/provider evidence 的 concept-family 与 sufficiency 责任。
- [ ] AC2：官方 `trellis-*` skills、agents、workers 保持 upstream-owned，任务
  diff 不恢复 13 个 Guru spec 引用，也不修改这些官方文件。
- [ ] AC3：focused contract test 不再包含陈旧 13-path positive assertion；四个
  Guru owners 的 reference/eval/fixture 约束、`guru-reconcile-task-base` 与其它
  non-owner 不扩权约束全部通过，shared skill-package contract 不再保留第五个
  direct consumer 声明。
- [ ] AC4：preset apply 后 dogfood spec 与 canonical spec byte-identical，
  installed/source validators 和 dogfood drift 通过，无未处理 sidecar。
- [ ] AC5：focused clean throwaway install/update/reapply 在 fresh 与 reapply 后均
  验证当前 owner contract，并且没有 repo-local 或 throwaway residue。
- [ ] AC6：secret scan、residue scan、`git diff --check`、task validation 与
  workspace boundary 检查通过。
- [ ] AC7：完整 Branch Review 覆盖 `origin/main...HEAD`，Publication 保持
  #414 delivery 与 `Refs #410` 边界，PR/merge 不创建 release 副作用。
- [ ] AC8：合并后的 #410 后续流程只从新 `origin/main` 创建全新 candidate，
  旧 candidate evidence 不进入新 release gate。

## 5. 非目标

- 不恢复或 patch 13 个 upstream-owned Trellis 文件。
- 不实现 stock suppression、quarantine、caller-bound adapter 或 Evolution 中
  尚未 current 的机制。
- 不新增 Skill、typed exit、public API、schema、semantic owner 或并行 contract。
- 不改变 `guru-reconcile-task-base` 的 public inputs/outputs、typed exits、workflow
  routes、executor、pair identity 或 reconciliation 行为。
- 不修改 #408 session-binding 行为、Architecture owner、release version axis、
  Trellis upstream、全局 Python/npm、业务仓库或生产环境。
- 不执行 tag、GitHub Release、#410 closure 或旧 candidate evidence migration。

## 6. Docs 状态

- Docs state：`complete_docs`。
- Strategy：`task_delta_only`。
- 本任务修正现有 durable semantic retrieval spec 自身的 ownership wording；
  不新增产品能力、公共 API/schema 或 Architecture/RDT contribution。
- Phase 1 Architecture impact owner 仍须在 plan approval 前给出 fresh
  `no_architecture_impact` 或其它受支持 route；如 live authority 证明存在直接
  durable contribution，再返回 planning 修订，不在此预先扩张范围。

## 7. 阻塞问题

无。实现机制、ownership 边界、验证范围和 release 边界均由 live authority
闭合。
