# Issue #118 Phase 2 独立检查报告（Round 6）

## 1. 检查身份与结论

- 角色：fresh independent Trellis Phase 2 check agent。
- Agent：`/root/issue118_phase2_round6_check`。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Checked HEAD：`925007cb6f9b8101360db8fb93f92ef6b35a5b77` 加当前未提交 finding-fix delta。
- 最终语义结论：`implementation_required`。
- Finding inventory：P0=0、P1=0、P2=1、P3=0。
- 外部 blocker：Claude native eval 两次均因无效 API key 返回 `execution_error`。
- 本报告不调用 `guru-check-task` recorder/checker，不写 `phase2-check.json`，不授权 commit、push、PR、archive、Issue mutation、deploy 或 production write。

## 2. Scope 与 authority 复核

- Planning approval checker 返回 `status=ok`、`typed_exit=approved`；approved planning document digests current。
- 重新完整阅读 `prd.md`、`design.md`、`implement.md`、post-finding implementation handoff、Round 7 final review 与 Round 8 finding-owner report。
- Close scope 仍只有 #118。Ledger 中 #115 为 related；#119 拥有 Finish-family integration、combined acceptance 与关闭 #115；#132 拥有 upstream overlay cleanup；#105 transaction semantics 保持不变。
- `issue-scope-ledger.json` 的 `close_issues=[#118]`、`related_issues=[#81,#115]`、`followup_issues=[#119,#132]` 与边界一致；其旧 HEAD acceptance evidence 必须在本轮 finding 修复和新 gate 后刷新，当前不能作为 close evidence。
- `pr-body.md` 只有 `Closes #118`。
- 完整 effective range 没有修改 global workflow、upstream `trellis-finish-work` family、official `.trellis/scripts/task.py` 或 preset overlays；`forbidden_boundary_paths=0`。
- 未引入 hostile actor、forgery、concurrency、lock、TOCTOU、fault injection、crash consistency 或 cross-OS atomicity 机制/测试。

## 3. 已审查文件与维度

### 3.1 Task、spec 与 durable docs

- `.trellis/tasks/07-26-118-guru-finalize-task/{prd.md,design.md,implement.md}`。
- `implementation-handoff-not-required-fix.md`。
- `reviews/round-007-final-release.md`、`reviews/round-008-problem-discovery.md`。
- `.trellis/spec/docs/{index.md,public-docs.md}`。
- `.trellis/spec/preset/{index.md,installer.md,overlay-guidelines.md,upstream-ownership.md}`。
- `.trellis/spec/workflow/{index.md,companion-scripts.md,data-contracts.md,quality-guidelines.md,skill-package-contract.md,workflow-contract.md}` 的 task-finalization、verification、eval、distribution、quality 与 script-boundary sections。
- `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。

### 3.2 Canonical/package/runtime/eval/tests

- `trellis/skills/guru-team/packages/guru-finalize-task/**`：Skill、contract、Interface、七个 profile、六 exits、schemas/examples、private gate、eval corpus、wrappers 与 tests。
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/**`：保持的 public schemas、reachable standalone `not_required` output、consumer projection、private contract 与 tests。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 和全量 transaction/runtime tests。
- `trellis/skills/guru-team/adapters/eval/native_adapter.py` 和 `test_skill_packages.py`。
- `trellis/guru-team-extension.json`、throwaway verifier、preset installer tests。
- Installed shared、Agents、Codex、Claude、Cursor 两个 package copies；canonical/installed runtime 与 eval adapter。

### 3.3 语义维度

- #117 public output schema compatibility 与 reachable standalone producer edge。
- `standalone_verification_not_required` 的 seed/authoring partition、no-overwrite merge、closed target schema。
- Public DTO 是否泄露 `plan_ref` 或 owner-private plan/PR/archive/recovery facts。
- Private task/repo/HEAD/verification-ref/plan binding 与 same-plan recovery。
- Real #117 wrapper -> declared projection -> target authoring merge -> real #118 wrapper production eval。
- Actual-exit schema selection 是否先于 `expected_exit` assertion，且 native request 不含 `expected_exit`。
- Shared/Codex/Claude/Cursor corpus、protocol、trusted-root、unsupported/unavailable 与 parsing coverage。
- #105/#119/#132/no-write boundaries、Docs SSOT、security/deployment、install/update/reapply/sidecar/hygiene。

## 4. 精确 dirty diff scope

检查开始时相对 `HEAD` 为 95 个 tracked modified paths 和 21 个 untracked paths；本报告新增后 untracked 为 22。完整 `base...HEAD + dirty + untracked` effective scope 为 516 个 unique paths（写报告前为 515）。当前 dirty delta 精确分组如下。

### 4.1 95 个 tracked modified paths

- 48 个 platform package copies：`.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.cursor/skills/` 各 12 个：
  - `guru-finalize-task/evals/evals.json`
  - `guru-finalize-task/evals/files/not-required-reentry-published-facts.json`
  - `guru-finalize-task/evals/files/verification-not-required-input.json`
  - `guru-finalize-task/interface.json`
  - `guru-finalize-task/references/contract.md`
  - `guru-finalize-task/schemas/public-input.schema.json`
  - `guru-finalize-task/schemas/task-finalization-gate.schema.json`
  - `guru-finalize-task/tests/test_contract.py`
  - `guru-verify-extension-installation/examples/public-not-required-output.json`
  - `guru-verify-extension-installation/interface.json`
  - `guru-verify-extension-installation/references/contract.md`
  - `guru-verify-extension-installation/tests/test_contract.py`
- 15 个 installed shared/runtime paths：`.trellis/guru-team/extension.json`、runtime、eval adapter，以及上述两个 installed package 的相同 12 个 package paths。
- 6 个 durable specs：`.trellis/spec/docs/public-docs.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/workflow/{index.md,quality-guidelines.md,skill-package-contract.md,workflow-contract.md}`。
- 4 个 main-owned task metadata paths（本 agent 只读、未改写）：`agent-assignment.json`、`review-gate.json`、`review.md`、`task-commit-plans/003.json`。
- 1 个 repository doc：`README.md`。
- 21 个 canonical/distribution paths：
  - `trellis/guru-team-extension.json`
  - `trellis/presets/guru-team/README.md`
  - `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
  - `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
  - `trellis/skills/guru-team/adapters/eval/native_adapter.py`
  - 上述两个 canonical packages 的相同 12 个 package paths
  - `trellis/skills/guru-team/tests/test_skill_packages.py`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/workflows/guru-team/scripts/python/{guru_team_trellis.py,test_guru_team_trellis.py}`

### 4.2 22 个 untracked paths（含本报告）

- 六个 package layouts（canonical、installed shared、Agents、Codex、Claude、Cursor）各新增以下 3 个 `guru-finalize-task` files，共 18 个：
  - `examples/public-standalone-verification-not-required-authoring.json`
  - `examples/public-standalone-verification-not-required-input.json`
  - `schemas/public-standalone-verification-not-required-input.schema.json`
- Task-local evidence 4 个：
  - `implementation-handoff-not-required-fix.md`
  - `reviews/round-007-final-release.md`
  - `reviews/round-008-problem-discovery.md`
  - `phase2-worker-report-round6.md`

## 5. Findings

### P2 `P2-R6-STANDALONE-REF-BINDING-01`：standalone not-required owner evidence 没有绑定 private plan remote/ref

- Status：`open`。
- Scenario：`normal_required_behavior`。
- Route：`implementation_required`。
- Scope basis：#118 standalone `not_required` producer edge 的 owner-private same-plan/ref/HEAD currentness；不是 #119 global integration 或 #132 overlay cleanup。
- Affected code：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 的 `finalization_standalone_not_required_owner_is_current` 与 downstream `finalization_current_verification_owner_result`。
- Contract basis：finalizer verification re-entry 必须绑定 same task/private plan/ref/reviewed HEAD；#117 evidence 的 `remote/ref/remote_head` 是 private currentness facts。

正常复现使用：

- plan：`repo=castbox/guru-trellis`、`remote=origin`、`head_branch=feat/118-guru-finalize-task`、`reviewed_work_head=<same SHA>`、`marketplace.required=false`；
- task-bearing standalone #117 evidence：相同 task/repo/HEAD/verification ref，但 `remote=secondary`、`ref=refs/heads/main`；
- `secondary/main` 在正常 multiple-remotes/branches 状态下解析到与 feature branch 相同 SHA，不涉及篡改、伪造、恶意输入、并发或 fault injection。

Probe：

```python
finalization_standalone_not_required_owner_is_current(
    payload_with_secondary_main,
    checked_not_required,
    private_feature_plan,
    task_ref=".trellis/tasks/current",
)
# actual: True
# expected: False
```

原因：helper 当前比较 task、normalized repo、`repository.remote_head`、marketplace flag 与 verification ref，但不比较 `repository.remote` / `repository.ref`（或 owner input 对应字段）与 `plan.git.remote` / `refs/heads/{plan.git.head_branch}`。Compatibility augmentation 虽会重新解析 evidence 自己声明的 remote/ref 并确认其仍指向 recorded HEAD，但没有证明它就是 private plan 的 remote/ref。

影响：正常同 SHA 的错误 remote/ref provenance 可以被视为 current same-plan evidence。精确内容 SHA 降低即时数据破坏风险，核心 producer edge 也已可达，因此定为 P2 而非 P1；但它违反 current accepted owner-private ref binding，不能以 test green 或 exact SHA 等价替代合同。

Required closure：

1. 在 finalizer-private checker 中绑定 #117 private evidence remote/ref 到 immutable plan remote/head branch，同时保持通用 #117 checker 与 public DTO 不变。
2. 新增 same task/repo/HEAD 但 remote mismatch、ref mismatch 的正常负例，以及 exact matching remote/ref 的正例。
3. 同步 canonical/installed runtime 与 tests，重跑 focused/full suites、两-wrapper eval、Phase 2 与后续 Branch Review finding closure。

## 6. 本 agent 的机械修复

发现 `guru-verify-extension-installation/references/contract.md` 开头仍称 finalizer 是 future、producer edge 未激活，与同文件后文、active registry/interface 和 durable docs 冲突。本 agent 只把两句状态改为：active `guru-finalize-task` target 已存在，global Finish-family route 仍由 #119 deferred。

精确同步路径 6 个：

- `trellis/skills/guru-team/packages/guru-verify-extension-installation/references/contract.md`
- `.trellis/guru-team/skills/packages/guru-verify-extension-installation/references/contract.md`
- `.agents/skills/guru-verify-extension-installation/references/contract.md`
- `.codex/skills/guru-verify-extension-installation/references/contract.md`
- `.claude/skills/guru-verify-extension-installation/references/contract.md`
- `.cursor/skills/guru-verify-extension-installation/references/contract.md`

首次 all-platform reapply 为 5 个 installed/generated copies 生成 `.bak`。逐个确认 5 个 backup byte-identical，且相对 current canonical 的唯一 diff 就是上述两句机械修正；没有用户独有内容。随后精确删除这 5 个可重建 backup，第二次 reapply 为 `installed=0`、`updated=0`、`backup=0`、`new=0`、`sidecar=0`。除此之外，本 agent 未修改代码、schema、tests、main-owned task metadata 或 review evidence。

## 7. 验证结果

### 7.1 Focused 与 full suites

- Finalizer package：5 passed。
- Verifier package：10 passed（机械 docs sync 后 fresh rerun亦为 10 passed）。
- Focused runtime owner binding：2 passed。
- Real producer-edge regression：1 passed；执行 installed #117 wrapper、declared projection/no-overwrite authoring merge、installed #118 wrapper，actual exit=`published`。
- Runtime full：617 passed，13 skipped，exit 0。
- Skill package/full production eval suite：179 passed，exit 0。
- Preset installer full：45 passed，exit 0。
- TypeCheck：仓库无独立 configured type checker；用 Python AST、JSON/schema/package validators 与 full unittest 覆盖适用静态/合同检查。

### 7.2 Static、contract、distribution

- Planning approval checker：`status=ok`、`typed_exit=approved`。
- `git diff --check 7820a9e..working-tree`：passed。
- Effective changed files：397 JSON parse、39 Bash `bash -n`、23 Python AST parse 全部 passed。
- Source/installed package validators：passed；13 active、0 planned、12 invokes / 46 exits / 27 targets。
- Installed inventory：2659 managed files、0 sidecar、0 removal、0 conflict。
- `apply.sh --repo . --all-platforms --json`：passed；最终 idempotent reapply 零写入/零 sidecar。
- Upstream ownership：passed；43 frozen transitional overlays、13 active Skills，inventory/frozen identity current。
- Dogfood overlay drift：passed。
- Canonical、installed shared、Agents、Codex、Claude、Cursor 的 finalizer/verifier package bytes 与 modes：identical。
- Canonical/installed runtime 与 eval adapter bytes：identical；wrappers executable。
- Global workflow、upstream Finish family、official `task.py`、preset overlays no-diff：passed。
- Sensitive/deploy surface query：无 dependency、CI/CD、container、Compose、Kubernetes、Helm/Kustomize、DB migration、Makefile 或 production data-write diff；未发现 credential/secret/private key/signed URL/raw customer payload。

### 7.3 Production eval 平台矩阵

- Shared source：not-required edge passed，actual exit=`published`。
- Shared installed：not-required edge passed，actual exit=`published`。
- Codex installed native：passed，actual exit=`published`；trusted Git root path由完整 suite覆盖。
- Cursor installed native：stable `unsupported`；完整 suite覆盖 unauthenticated/unavailable parsing，没有伪造 pass。
- Claude installed native：两次均为 `execution_error`（约 185s、187s）；第二次脱敏 transcript 明确 `Invalid API key`。没有 public output/actual exit，不能声称通过。
- Full Skill suite确认 native/adaptor request 不含 `expected_exit`，实际 `exit_id` 先选择 per-exit schema，之后才执行 expected-exit assertion；Shared parsing、Claude safe input protocol、Codex trusted root、Cursor unsupported/unavailable 均有自动测试。

### 7.4 Clean throwaway

Fresh `verify-throwaway-install.sh` 终态 exit 0，覆盖：

- public workflow marketplace discovery；
- initial preset install 与 reapply；
- official Trellis update 与 preset reapply；
- managed hash、`.new/.bak` normal recovery；
- Shared/Agents/Codex/Claude/Cursor distribution、bytes/modes 与 wrapper smoke；
- source/installed contract validation、ownership/drift、installed package/eval smoke；
- no-developer/no-workspace fixture 与开箱运行入口。

当前 feature branch 未 push 且 working tree dirty，无法从 remote exact feature ref 安装。本轮按 verifier 明示的 release-validation path 使用 public marketplace bootstrap 加 local canonical unpublished workflow sample；输出明确记录该限制。之前实现 handoff 中的 registry timeout 本轮没有复现，fresh throwaway 已通过，因此 registry 当前不再是 blocker；该结果仍不替代后续 pushed exact-ref #117 verification。

## 8. Docs SSOT reconciliation

- Strategy：`ssot_first`。
- Durable package/workflow/preset/docs SSOT 现在一致声明 active finalizer 为七个 distinct profiles、六 exits，reachable task-bearing standalone `not_required` seed 为 `repo_ref/resolved_head/verification_ref`，target authoring 为 `profile/mode/task_ref`，plan identity private。
- #117 workflow-shaped `not_required` schema 保持兼容但 workflow applicability conflict 不可产生；workflow `verified` 与 reachable standalone `not_required` 分别进入 finalizer。
- README 仅描述导航、安装、active status 与 #119/#132 handoff，没有复制 recovery algorithm。
- Approved planning artifacts 保留原六-profile设计的历史快照；post-finding correction 由 `implementation-handoff-not-required-fix.md` 明确记录，durable SSOT 已完成七-profile delta。未修改 approved planning bytes 或伪造重新审批。
- 本 agent 已修复 verifier contract 开头的 stale future wording；`rg` 不再发现 future producer edge 或 six-profile durable wording。
- Docs SSOT 在 profile/projection/distribution 状态上 reconciled；但 P2 private remote/ref binding 仍是代码与 accepted currentness合同之间的 open implementation finding，故整体 Phase 2 不能 pass。

## 9. External blocker、hygiene 与剩余工作

### External blocker

- Claude：真实外部认证失败，`Invalid API key`，两次合理尝试均失败。属于环境/credential blocker，不是当前 implementation defect；在可用 Claude auth 环境中必须重新运行该 native case 后才能声称 Claude native success。
- Registry：之前 timeout 本轮 fresh throwaway 未复现，当前无 registry blocker。
- Exact remote feature ref：当前分支未 push，因此本轮 clean throwaway 只证明 local unpublished candidate install；正式 finalization 前仍需 #117 对 pushed exact content HEAD 执行 remote clean-install verification。

### Hygiene

- Source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis`：`git status --short` 为空，HEAD=`7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Issue worktree：HEAD=`925007cb6f9b8101360db8fb93f92ef6b35a5b77`，dirty paths 只包含本 task implementation、generated distribution、main-owned review metadata与本报告。
- Worktree/source `__pycache__`、`.pyc`、`.pyo` residue：0。
- `.new` / `.bak` sidecars：0。
- Throwaway work root 与 eval run roots 已清理。

### Required remaining work

1. Implementation owner 修复 `P2-R6-STANDALONE-REF-BINDING-01` 并补精确 normal-path regression。
2. Fresh Phase 2 agent 对修复后的完整 effective diff 重新检查，并由主会话记录新的 `guru-check-task` evidence。
3. 新 task commit 后，由 qualified finding-closure reviewer 关闭本 finding及原 `F-NOT-REQUIRED-EDGE-01`，再由不同 fresh final Branch Review agent覆盖新 HEAD。
4. Publication review 与 formal finalization 前刷新 scope-ledger/PR readiness evidence到同一 HEAD。
5. Claude auth 恢复后补跑 native eval；push exact content 后运行 #117 remote verification。

## 10. 最终 verdict

`F-NOT-REQUIRED-EDGE-01` 的主要 reachability 修复是实质有效的：#117 public schema兼容、七-profile partition、no-overwrite merge、private plan DTO boundary、真实两-wrapper eval、actual-exit schema ordering、四平台 corpus、distribution 与 clean throwaway 均有 fresh evidence。

但 standalone #117 evidence 的 private remote/ref 尚未绑定 immutable plan remote/head branch，正常 same-SHA wrong-ref path 会被当作 current；另有未解决的 Claude external auth failure。因此本轮不能返回 `passed`。

**Final semantic verdict：`implementation_required`。**
