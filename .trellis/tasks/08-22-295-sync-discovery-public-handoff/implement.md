# #295 实施计划：修复 Sync-to-Discovery public handoff

## 1. Pre-Implementation Gates

- [ ] planning artifacts通过`guru-review-contract-wording:planning_artifacts`。
- [ ] `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`返回fresh
  `baseline_current`，change path为`target_native`。
- [ ] `guru-approve-task-plan`确认requirements、design、tests、Docs SSOT与provenance完整。
- [ ] 用户在最新planning summary后确认实施；此前不运行`task.py start`或编辑产品代码。
- [ ] `trellis-before-dev`加载curated `implement.jsonl`并验证当前task/worktree/base identity。

## 2. Ordered Implementation

### Step 1. Task-owned durable deltas

- [ ] 新增RDT contribution `295-sync-discovery-public-handoff`五文件并闭合traceability。
- [ ] 新增Architecture contribution，绑定`.39`、change contract v1、`target_native`、
  `adr.required=false`和expected-current promotion。
- [ ] 更新直接受影响的workflow/preset specs，保持task contribution与shared current分离。

Checkpoint：task docs、RDT、Architecture和Issue #295 acceptance逐项对应。

### Step 2. Versioned Discovery contracts

- [ ] 保留Sync synced 2.0与base-current 1.0 active shape不变。
- [ ] 新增Discovery pre-task input 2.0 schema/example并更新aggregate、interface、consumer、
  projection与eval绑定。
- [ ] 新增Discovery owner-result 3.0 schema/example，删除active private Sync definitions与
  `base_sync_facts_sha256`。
- [ ] 更新registry、migration/activation inventories及schema/package validators。

Checkpoint：旧id仍指向旧bytes；active graph只能选择2.0 input + 3.0 owner result。

### Step 3. Discovery live base observer

- [ ] 在Discovery package runtime实现`base_current`校验和live authority observation。
- [ ] 调整record/check/invoke identity，使owner evidence只使用`base_observation`。
- [ ] base current时继续semantic evidence；advance返回`refresh_base`；invalid authority返回
  `blocked`。
- [ ] 确认base precondition先于Issue/Docs/code/test/history reads且零Git mutation。

Checkpoint：targeted runtime tests覆盖current/advance/dirty/wrong/missing/mismatch/ambiguous矩阵。

### Step 4. Real public transcript

- [ ] 删除`verify_installed_phase0_transcript.py::base_sync_payload`与所有同义逻辑。
- [ ] fixture调用真实Sync public wrapper并消费actual stdout。
- [ ] 通过interface projection构造Discovery input 2.0 + actual `base_current`。
- [ ] 通过production Discovery recorder/checker/public wrapper取得actual `context_ready`。
- [ ] 将actual output投影到Clarify input并通过consumer schema。
- [ ] 证明no-impact、existing Issue、proposed draft、zero-history和pre-task zero-write。

Checkpoint：static scan对private reconstruction、Sync low-level executor和private import零命中。

### Step 5. Managed Python contract

- [ ] 识别并修复targeted tests/verification中绕过`resolve-python.sh`的产品依赖判断。
- [ ] PATH Python无jsonschema fixture通过真实public wrappers运行。
- [ ] 覆盖missing/stale pointer、missing interpreter、inventory drift的精确errors。
- [ ] 既有bootstrap/apply bootstrap interpreter边界保持不变，不修改global environment。

Checkpoint：managed runtime matrix与真实wrapper chain同时通过。

### Step 6. Canonical distribution

- [ ] 同步canonical workflow、package/interface/schema/example/test/eval与README。
- [ ] 更新preset installer inventory、activation manifest、update/reapply与sidecar assertions。
- [ ] 运行`apply.sh --repo . --all-platforms --json`生成dogfood/installed/platform projections。
- [ ] 核对Shared/Codex/Claude/Cursor bytes、modes、hashes和interface identity。

Checkpoint：source/installed validators、ownership、dogfood drift与recursive zero-sidecar通过。

### Step 7. Targeted validation与代表性throwaway

- [ ] 两个package contract/runtime tests与shared graph/runtime tests通过。
- [ ] installed Phase 0 transcript、managed Python matrix、preset tests通过。
- [ ] 一个clean throwaway完成install、real Sync->Discovery->Clarify、update/reapply和final drift scan。
- [ ] `git diff --check`、task validation、shell syntax、JSON schema与Python compile通过。

### Step 8. Semantic gates与promotion

- [ ] `guru-check-task`审核完整scope、tests、Docs SSOT与normal-scenario边界；修复全部P0-P3 finding。
- [ ] `guru-create-task-commit`创建精确task commit。
- [ ] independent `guru-review-branch`覆盖`origin/main...HEAD`完整committed diff。
- [ ] RDT/Architecture owners按expected`.39` serialized promotion并重跑fresh check/commit/review。
- [ ] publication/finalizer/merge分别遵循自己的live gate与confirmation；PR只`Closes #295`。
- [ ] merge后验证Issue CLOSED、live main reviewed identity、archive/history与三向收敛；不开始#286。

## 3. Primary Surfaces

- Canonical packages：`trellis/skills/guru-team/packages/guru-{sync-base,discover-change-context}/**`
- Stage 0 contracts：`trellis/skills/guru-team/consumers/workflow/stage0/**`
- Runtime/graph：`trellis/skills/guru-team/{registry.json,runtime/**,tests/**,migrations/**}`
- Transcript/runtime verification：`trellis/presets/guru-team/scripts/{python,bash}/**`
- Workflow/preset：`trellis/workflows/guru-team/**`、`trellis/presets/guru-team/**`
- Durable docs：`.trellis/spec/{workflow,preset}/**`、task-owned RDT/Architecture contributions
- Generated projections：`.trellis/guru-team/**`、`.agents/skills/guru-*/**`、
  `.codex/skills/guru-*/**`、`.claude/skills/guru-*/**`、`.cursor/skills/guru-*/**`

## 4. Validation Commands

所有Python产品测试通过managed resolver或仓库已声明的managed wrapper执行。实现阶段先发现当前
public test entry，再固定最终argv；禁止用bare PATH Python的import结果宣告dependency PASS。

```bash
.trellis/guru-team/runtime/resolve-python.sh "$PWD" .trellis/guru-team/runtime \
  trellis/skills/guru-team/packages/guru-sync-base/tests/test_contract.py
.trellis/guru-team/runtime/resolve-python.sh "$PWD" .trellis/guru-team/runtime \
  trellis/skills/guru-team/packages/guru-discover-change-context/tests/test_contract.py
trellis/presets/guru-team/scripts/bash/verify-managed-python-runtime.sh
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
python3 ./.trellis/scripts/task.py validate \
  .trellis/tasks/08-22-295-sync-discovery-public-handoff
git diff --check
```

最终validation记录每条命令、managed interpreter identity、PASS/FAIL/SKIP与未验证边界。

## 5. Acceptance Mapping

| Acceptance | Evidence |
| --- | --- |
| A1-A2 | Sync contract tests、interface projection、real wrapper transcript |
| A3-A5 | Discovery 3.0 schema/runtime matrix、Clarify consumer validation |
| A6-A8 | transcript static scans、protected-path/Git zero-write snapshot |
| A9 | managed Python routing/error matrix |
| A10 | source/installed/platform/preset/update/reapply/throwaway evidence |
| A11-A12 | Phase 2 gate、full-diff Branch Review、publication/merge/live-main closeout |

## 6. Rollback Points

| Point | Trigger | Action |
| --- | --- | --- |
| RP1 | Discovery需要Sync private result才能判断current | 停止runtime改动并重新划分public consumer contract |
| RP2 | new input/owner schema形成dual-active graph | 保留旧active graph，修复version inventory后重试 |
| RP3 | live observer需要fetch或shared mutation | 回退observer，保持fail closed并修订planning |
| RP4 | managed test仍依赖PATH Python | 停止PASS声明，修复wrapper/resolver contract |
| RP5 | preset产生mixed bytes或sidecar | 停止activation，保留用户bytes并修复canonical/provenance |
| RP6 | scope触及#286/#287/#250或后续Issue | 停止实现并进入scope clarification |

## 7. Completion Conditions

- [ ] R1-R7与A1-A12均有current code/test/docs/live evidence。
- [ ] public handoff不含private Sync result或reconstruction。
- [ ] canonical/dogfood/installed/platform/update/reapply/throwaway全部收敛。
- [ ] Issue ledger只关闭#295；无tag/Release；不开始#286。
