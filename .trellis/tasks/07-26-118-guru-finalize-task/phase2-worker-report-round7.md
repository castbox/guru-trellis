# Issue #118 Phase 2 独立检查报告（Round 7）

## 1. 检查身份与最终结论

- 角色：fresh independent Trellis Phase 2 check agent。
- Agent：`/root/issue118_phase2_round7_check`。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Checked HEAD：`925007cb6f9b8101360db8fb93f92ef6b35a5b77` 加当前未提交 finding-fix、distribution、task evidence 与本轮机械 Docs SSOT delta。
- 独立性：本 agent 未实现 `F-NOT-REQUIRED-EDGE-01` 或
  `P2-R6-STANDALONE-REF-BINDING-01`，且不复用 Round 6 checker 身份。
- Finding inventory：P0=0、P1=0、P2=0、P3=0。
- 最终语义结论：`passed`。
- 外部残余：Claude native eval 真实调用因 `401 Invalid API key` 返回
  `execution_error`；当前分支未 push，clean throwaway 不能证明 exact feature-ref
  marketplace install。两项均如实保留，不声称通过，也不替代 formal #117 remote gate。
- 本报告不调用 `guru-check-task` recorder/checker，不写 `phase2-check.json`，不授权
  commit、push、PR、archive、Issue mutation、deploy 或 production write。

## 2. Scope、规划与 authority 复核

- 完整读取并按顺序复核 `prd.md`、`design.md`、`implement.md`，以及批准的
  `design.md` Docs SSOT Plan。
- 完整读取：
  - `implementation-handoff-not-required-fix.md`；
  - `implementation-handoff-ref-binding-fix.md`；
  - `phase2-worker-report-round6.md`；
  - `reviews/round-007-final-release.md`；
  - `reviews/round-008-problem-discovery.md`。
- `check-planning-approval.sh` 终态 `status=ok`、`typed_exit=approved`，approved
  planning document digests current；`task.py validate` 通过。
- Close scope 仍只有 #118。`issue-scope-ledger.json` 为
  `close_issues=[#118]`、`related_issues=[#81,#115]`、
  `followup_issues=[#119,#132]`；`pr-body.md` 只有 `Closes #118`。
- #119 继续拥有 Finish-family workflow/platform integration、combined acceptance
  与关闭 #115；#132 继续拥有 upstream overlay cleanup；#105 transaction semantics
  保持 completed。
- Ledger 中旧 acceptance evidence 仍绑定旧 HEAD/旧 gate；这是 Phase 2 后由主会话在新
  task commit、finding closure 和 final Branch Review 后刷新的正常下游证据，不能作为
  当前 closeout 证据，但不构成本轮 implementation finding。

## 3. 审查文件与完整 effective scope

### 3.1 Task、spec 与 durable docs

- Task planning/evidence：上节所列三份 planning artifacts、两份 implementation
  handoff、Round 6 report、Round 7/8 review evidence、scope ledger 与 PR body。
- Specs：
  - `.trellis/spec/docs/{index.md,public-docs.md}`；
  - `.trellis/spec/preset/{index.md,installer.md,overlay-guidelines.md,upstream-ownership.md}`；
  - `.trellis/spec/workflow/{index.md,companion-scripts.md,data-contracts.md,quality-guidelines.md,skill-package-contract.md,workflow-contract.md}`；
  - `.trellis/spec/guides/` 中由 workflow index 指向的跨层与复用检查规则。
- Public docs：`README.md`、`trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`。

### 3.2 Package、runtime、adapter、tests 与 distribution

- `trellis/skills/guru-team/packages/guru-finalize-task/**`：Skill、唯一完整 contract、
  Interface 1.3、七 profiles、六 exits、schemas/examples、private artifacts、wrappers、
  eval corpus 与 package tests。
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/**`：既有两
  profiles/四 exits、workflow-compatible `not_required` branch、新的 reachable
  standalone producer edge、private owner evidence 与 tests。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 及完整 tests。
- `trellis/skills/guru-team/adapters/eval/native_adapter.py` 与
  `trellis/skills/guru-team/tests/test_skill_packages.py`。
- `trellis/guru-team-extension.json`、preset verifier、preset installer tests。
- Installed shared、Agents、Codex、Claude、Cursor 的两个 package copies，以及 installed
  runtime/adapter。
- 写本报告前完整 `base...HEAD + dirty + untracked` 为 517 个 unique paths；本报告是第
  518 个 task-local Markdown evidence path。静态批处理覆盖写报告前全部 517 个路径。

## 4. Findings 与关闭证明

### 4.1 `P2-R6-STANDALONE-REF-BINDING-01`：closed

先按 Round 6 同 SHA、不同 remote/ref 的正常场景独立重放 helper probe：

```json
{
  "exact": true,
  "same_sha_wrong_ref": false,
  "same_sha_wrong_remote": false
}
```

当前 finalizer-private checker 同时要求：

- `repository.remote == plan.git.remote`；
- `repository.ref == refs/heads/{plan.git.head_branch}`；
- task、normalized repo、reviewed/remote HEAD、`required=false` 与 verification ref
  继续匹配 private plan/evidence。

Focused augmentation regression 证明 exact remote/ref 成功，remote mismatch 失败、ref
mismatch 失败、stale remote HEAD 失败，并断言非 eval 路径真实执行：

```text
git ls-remote origin refs/heads/main refs/heads/main^{}
```

Focused 两个 tests 均通过。Downstream owner/currentness helper 同样拒绝 wrong remote/ref，
same-plan resume 仍保持有效。因此 Round 6 finding 已完整关闭。

### 4.2 原 `F-NOT-REQUIRED-EDGE-01`：closed，无回归

Source 与 installed shared eval 均真实执行：

1. installed #117 public `scripts/invoke.sh`；
2. declared `project_not_required` projection；
3. seed=`repo_ref/resolved_head/verification_ref`；
4. target authoring=`profile/mode/task_ref`；
5. no-overwrite merge；
6. installed #118 public `scripts/invoke.sh`。

两边 actual exit 都是 `published`。Native trace 证明 #118 wrapper 被调用；不存在直接
finalizer verification-facts injection。Actual `exit_id` 先选择并通过 per-exit schema，
随后 `expected_exit` assertion 通过；adapter/native request 均不含 `expected_exit`。

### 4.3 本轮机械修复

发现 `.trellis/spec/preset/upstream-ownership.md` 的 active finalizer 状态仍写
`six-profile, six-exit`，与七-profile Interface 和全部其他 durable SSOT 冲突。本 agent
只把该短语机械改为 `seven-profile, six-exit`。

该文件是 project-local durable spec，不是 preset managed/generated copy；all-platform
apply 仍为零写入、零 sidecar。`rg` 复核 public/durable surfaces 不再存在 six-profile
active wording。除此之外本 agent 未修改代码、schema、tests 或 main-owned metadata。

## 5. Public/private 与兼容性结论

- #118 Interface SHA-256 保持
  `3cc7291ba7fe6f3f425134fc4f452546f04caff238f1f61c27a0352b5d1949a8`。
- #117 Interface SHA-256 保持
  `768d1dd1ecba21fe1f23406d33c8732049517d27ebb413c56bb9e389212b64f7`。
- #117 workflow-shaped `not_required` schema branch 仍保留原
  `task_ref/plan_ref/reviewed_head`；workflow applicability conflict 仍不能发出该 exit。
- Reachable standalone branch 只发出
  `exit_id/mode/repo_ref/resolved_head/verification_ref`。
- #118 standalone target input只含
  `profile/mode/task_ref/repo_ref/resolved_head/verification_ref`，closed schema 禁止额外字段。
- 本轮新增的 `remote/head_branch` 只存在于 private immutable plan 与 eval private
  `finalization-context.json` staging；它们不进入 #118 native public request、#117
  standalone typed exit 或 #118 typed exits。
- Finalizer eval/private checker 继续执行 live remote HEAD currentness；新增 identity binding
  没有把相同 SHA 误当成 remote/ref provenance 相同。
- Source/installed same-plan-resume eval 均返回 `resume_finalization`，per-exit schema 与
  route assertion 均通过。

## 6. 验证命令与结果

### 6.1 Focused 与 full tests

- Finalizer package：5 passed。
- Verifier package：10 passed。
- Remote/ref focused runtime：2 passed。
- Runtime full：617 passed，13 skipped，exit 0。
- Skill package / production eval full：179 passed，exit 0。
- Preset installer full：45 passed，exit 0。
- `task.py validate`：passed。
- 仓库无独立 configured type checker；使用 full runtime/package suites、Interface/schema
  validators、Python AST、JSON parse 与 Bash syntax 作为适用静态合同检查。

### 6.2 Production eval 与平台

- Shared source not-required edge：passed，actual `published`。
- Shared installed not-required edge：passed，actual `published`。
- Shared source/installed same-plan resume：passed，actual `resume_finalization`。
- Codex installed native：passed，actual `published`；真实 trusted Git root invocation。
- Cursor installed native：稳定 `unsupported`；没有 public output 或伪造 success。Full
  suite 另覆盖 unauthenticated/unavailable parsing。
- Claude installed native：一次有界真实调用约 181 秒，终态 `execution_error`；脱敏
  envelope 为 `api_error_status=401`、`Invalid API key`、0 tokens、无 permission denial。
  未重试，不能声称 Claude native success。
- Full 179-test suite 使用受控 native executable 覆盖 Claude non-interactive stdin/file
  protocol、`--safe-mode`、精确 allowed tool、single-JSON envelope、Codex trusted root、
  Cursor unsupported/unavailable、shared parsing、trace receipt 与 private-runtime exclusion。
  因此当前候选的协议/adapter Phase 2 coverage 充分；真实 Claude success 仍是外部环境残余。

### 6.3 Distribution、ownership 与 static

- `apply.sh --repo . --all-platforms --json`：exit 0；`installed=[]`、
  `updated_managed=[]`、`managed_backups=[]`、`new_copies=[]`、`sidecars=[]`。
- Source/installed package validators：passed；13 active、0 planned；global markers
  12 invokes / 46 exits / 27 targets。
- Installed inventory：2659 managed files，0 sidecar、0 removal、0 conflict。
- Upstream ownership：43 frozen/current entries、0 removed、13 active Skills，passed。
- Dogfood overlay drift：passed。
- Canonical、installed shared、Agents、Codex、Claude、Cursor 的 finalizer/verifier package
  bytes 与 executable-mode relative sets：identical。
- Canonical/installed runtime SHA-256 为
  `3d9211630c33ce4cfda0bad57e8fb22dcdd4defe5f2e53f02cc34350855f0f6e`；
  eval adapter 为
  `834f07870bed612de06be6af243f7866a7cda4023a1655dd46200007a6418a02`；
  两组 canonical/installed bytes identical。
- Static：517 effective paths 中 397 JSON、39 Bash、23 Python 全部 parse/syntax passed；
  `git diff --check 7820a9e...working-tree` passed。
- 第一次 static aggregation harness 错用了 zsh tied parameter `path`，导致该 shell 的
  `PATH` 被覆盖、命令不可用；这是检查命令自身错误，没有形成 candidate evidence。
  改用 `candidate_path` 后对完整 517-path set 重跑通过。

### 6.4 Clean throwaway

Fresh `verify-throwaway-install.sh` terminal exit 0，覆盖：

- public workflow marketplace discovery；
- initial preset install 与 idempotent reapply；
- official Trellis 0.6.5 update、workflow preview/switch 与 preset reapply；
- managed known-version `.bak`、unknown local edit `.new`、显式 sidecar resolution；
- Shared/Agents/Codex/Claude/Cursor package bytes/modes 与 wrapper smoke；
- source/installed validation、ownership freeze、dogfood drift、real-wrapper eval；
- no-developer/no-workspace fixture、pre-146 upgrade 与 out-of-box entrypoints；
- final recursive zero `.new/.bak`、0 sidecar/removal/conflict。

终态明确记录：

```text
Verified public marketplace discovery plus local unpublished workflow sample
```

当前 feature branch 未 push，故脚本按明确 release-validation path 使用 public marketplace
bootstrap 加 local canonical unpublished workflow/package sample。本 task 未修改 global
workflow，该运行完整验证当前 local preset/package/runtime candidate；但不能替代 pushed
exact feature-ref marketplace verification。Formal finalization 前仍需 #117 对 content push
后的 exact remote HEAD 执行验证。

## 7. Boundary、Docs、security 与 deploy

### 7.1 Explicit no-diff boundary

- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`：no diff。
- Upstream `trellis-finish-work` Skill/Command/Prompt/Agent family：no diff。
- `trellis/presets/guru-team/overlays/**`：no diff。
- Official `.trellis/scripts/task.py`：no diff。
- Global package markers继续为 12/46/27；没有 #119 combined acceptance 或 #115 close。
- Frozen overlay inventory继续为 43；没有 #132 cleanup。
- Full #105 runtime/recovery matrix仍包含在 617-test pass 中；没有 issue mutation。
- 未引入 hostile actor、forgery、concurrent finalizer、lock、TOCTOU、new fault
  injection、incidental crash consistency 或 cross-OS atomicity 机制/测试。

### 7.2 Docs SSOT reconciliation

- Strategy：`ssot_first`。
- Durable package/workflow/preset/docs SSOT 一致声明 active finalizer 为七 profiles、六 exits、
  owner-private plan/evidence/recovery、#117 standalone minimal seed 与 target-owned authoring。
- `guru-finalize-task/references/contract.md` 仍是 step-local behavior SSOT；README 只描述
  discovery/install/status/boundary，没有复制 recovery algorithm。
- Workflow-compatible `not_required` 与 reachable standalone `not_required` 分工一致；
  private plan 不进入 producer DTO。
- Approved planning artifacts中的原六-profile设计保留为已批准历史快照；两个 finding
  handoff 记录 post-planning correction，durable SSOT 已收敛到七 profiles。本轮没有改写
  approved planning bytes 或伪造重新审批。
- 唯一发现的 durable stale wording 已在
  `.trellis/spec/preset/upstream-ownership.md` 机械修复。

### 7.3 Security 与 deploy

- Changed-path scan 无 dependency、CI/CD、container、Compose、Kubernetes、Helm/Kustomize、
  DB migration、Makefile、production config 或 production data-write surface。
- Secret pattern scan 未发现 credential、token、private key 或 signed URL。唯一 literal hit
  是既有 task review evidence 对 secret-validator denylist fixture 的说明，不是秘密材料。
- Logs/evidence 未记录 API key；Claude 只记录安全的 `401 Invalid API key` 状态。
- 本 task 不执行 deploy、production write、PR/Issue mutation 或 remote push。

## 8. Hygiene、残余风险与下游动作

- Source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` clean，
  HEAD=`7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Issue worktree HEAD=`925007cb6f9b8101360db8fb93f92ef6b35a5b77`；dirty paths 只包含当前 task
  implementation/distribution、main-owned review metadata、finding handoffs/reports，以及本轮
  mechanical durable-doc fix/report。
- Worktree/source `__pycache__`、`.pyc`、`.pyo`：0。
- Worktree `.new` / `.bak`：0。
- 六个验证生成 cache 与八个本轮命名的 repo-external eval/throwaway roots已精确移入系统
  Trash，可恢复；未删除其他目录或用户内容。
- Claude auth 恢复后可补一条 native success trace；在此之前只能声明协议/adapter
  automation coverage 与真实 auth failure，不能声明 Claude native success。
- 分支 push 后仍必须运行 #117 exact remote clean-install verification；local throwaway 不
  替代该 gate。
- 主会话下一步应记录 fresh `guru-check-task` evidence，创建新的 reviewed task commit，
  运行 Round 6 finding closure、原 `F-NOT-REQUIRED-EDGE-01` closure，再由不同 fresh final
  Branch Review agent覆盖新 HEAD。之后才进入 publication review/finalization。

## 9. 最终 verdict

Round 6 P2 remote/ref provenance 缺口已被精确关闭，原 not-required producer edge 继续由
真实 #117 wrapper、declared projection/no-overwrite authoring 和真实 #118 wrapper证明；
public Interface/DTO 保持兼容，private plan/ref boundary、live currentness、same-plan resume、
#105 recovery、四平台分发与 clean install/update/reapply 全部有 fresh evidence。

没有未解决的 P0/P1/P2/P3 current-scope finding。Claude 401 与未 push exact-ref 是诚实保留
的外部/后续 gate 限制，不削弱当前 Phase 2 source candidate adequacy，也未被改写为 pass。

**Final semantic verdict：`passed`。**
