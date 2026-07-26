# Branch Review 最终原始报告

## 检查完成

### 审查身份与范围

- 审查意图：`fresh_final_review`
- 角色：最终放行审查代理；未参与实现或 `BR-117-F1/F2` closure
- Task：`.trellis/tasks/07-25-117-verify-extension-installation`
- Issue：`castbox/guru-trellis#117`
- Branch：`feat/117-verify-extension-installation`
- Base：`origin/main`
- Merge base：`0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- Reviewed HEAD：`538def79408d417107c3adae61c4466116395d96`
- 完整 diff：`origin/main...HEAD`，325 files，44401 additions，2883 deletions
- 行为边界：只读审查实现；除本 raw report 外未修改实现、stage、commit、push、创建 PR、
  关闭 Issue，未写 `review.md` / `review-gate.json`，未调用 Branch Review
  recorder/checker/public wrapper

Workspace boundary 通过：

- Expected workspace 与 actual repo root 均为
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/117-verify-extension-installation`
- Source checkout 为 `/Users/wumengye/Documents/GoProjects/guru-trellis`，状态 clean
- 审查开始时 task worktree 只有主会话允许的 `agent-assignment.json`、
  `task-commit-plans/002.json` 与 `reviews/002-closure.md`
- Suspicious source artifacts：无

### 已检查文件

- 完整 committed diff：`origin/main...538def79408d417107c3adae61c4466116395d96`
- Live Issue #117 与唯一 `accepted_current` 评论 `issuecomment-5045035361`
- `prd.md`、`design.md`、`implement.md`、`planning-approval.json`
- `phase2-check.json`、`task-commit-plans/002.json`、`issue-scope-ledger.json`
- `review.md`、`review-gate.json`、`reviews/001-final.md`、
  `reviews/002-closure.md` 与 `agent-assignment.json`
- Canonical `guru-verify-extension-installation` package 的 `SKILL.md`、
  `references/contract.md`、`interface.json`、schemas、examples、eval corpus、
  wrappers 与 tests
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 及其全量 tests
- Source/installed registry、extension manifest、workflow markers 与 consumer schemas
- Preset installer、throwaway install/update/reapply、ownership inventory 与 tests
- Canonical、installed、Agents、Codex、Claude、Cursor package/runtime 分发副本
- `.trellis/spec/workflow/{skill-package-contract,companion-scripts,workflow-contract}.md`
- `.trellis/spec/preset/installer.md`、`.trellis/spec/docs/public-docs.md`
- Durable requirements、根 README、workflow README 与 preset README
- Trellis 官方 `custom-workflow`、`custom-spec-template-marketplace` 与首页文档

### 已修复问题

- 无。Branch Review 模式不修改实现；`BR-117-F1` 与 `BR-117-F2` 已由独立 closure
  reviewer 在当前 HEAD 确认关闭，本轮也独立复核了对应 redaction 与 task identity 路径。

### 未修复问题

#### P2 `BR-117-F7`：recorder 未执行已发布输入 schema，并接受不存在的 supersession lineage

文件：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:25170`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:25195`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:25391`

Qualification：

- 结论：`qualified_finding`
- Scenario class：`normal_required_behavior`
- Requirement refs：PRD 3.3；design 5.2、5.3；package contract
  `Private evidence` 与 `Exits and re-entry`
- Scope basis：Recorder 必须校验已声明 schema、identity 与 freshness；checker 必须校验
  supersession freshness。AI-authored semantic review 或 executor facts 的普通结构错误、
  首次调用误带 stale re-entry ref，都是 supported workflow 中的正常 fallible path，
  不依赖恶意篡改、伪造 artifact、对抗输入或非常规并发。

实际行为：

1. Package 发布了 `semantic-review-input.schema.json` 与
   `execution-facts.schema.json`，但 `extension_verification_review_input()` /
   `extension_verification_execution_input()` 只检查顶层 key，没有调用 schema validator。
2. 正常 AI review 若把 `redaction` 写成 string，recorder 在
   `extension_verification_semantic_shape_errors()` 对 string 调用 `.get()`，抛出未捕获
   `AttributeError`；execution `capabilities=null` 同样抛出未捕获 `TypeError`。`main()`
   只捕获 `WorkflowError`，因此不是合同要求的受控 fail-closed error。
3. 当 task 还没有 prior `marketplace-verification.json` 时，recorder 接受任意
   `supersedes_verification_ref`。独立 normal-path fixture 成功写入
   `extension-verification:does-not-exist`，生成新的 checker-valid
   `verification_ref`；只有 prior artifact 已存在时才要求 exact match。

独立复现：

```text
malformed_review_exception=AttributeError
artifact_exists_after_malformed=false
malformed_execution_exception=TypeError
artifact_exists_after_execution=false

accepted=extension-verification:does-not-exist
verification_ref=extension-verification:0783830f97dd7dff25585b3c
```

影响：

- 普通 malformed AI/executor input 会使 recorder 以 traceback/非合同错误中断，而不是
  返回稳定 `WorkflowError`。
- 首次调用可持久化指向不存在 predecessor 的 supersession lineage，削弱 private gate
  的 retry/stale 审计与 freshness 可信度。
- 当前成功 corpus 未覆盖 malformed recorder input 和 no-prior supersession 负例，因此
  全量 tests 与 eval 均可通过。

修复要求：

- Recorder 入口必须使用 package 声明的 execution/review schemas，在访问嵌套字段或写
  artifact 前把所有结构错误转换为受控 `WorkflowError`。
- `supersedes_verification_ref` 只能在 exact prior owner artifact 存在并匹配时出现；
  无 prior artifact 时必须拒绝。
- 增加 malformed nested type、missing/invalid enum 与 no-prior/nonmatching/exact-prior
  supersession 回归；修复后重新执行完整 Phase 2、task commit 和 fresh final review。

### 验证结果

- Lint：通过，`git diff --check origin/main...HEAD`
- TypeCheck：不适用；canonical/installed Python runtime 与 adapters `compileall` 通过
- Runtime tests：588 passed，13 skipped
- Skill package tests：175 passed
- Preset installer tests：45 passed
- Ownership + extension contract tests：16 passed
- Source validator：通过，12 active Skills / 46 exits / 27 targets
- Installed validator：通过，2322 managed files，0 sidecar，0 removal，0 conflict
- Dogfood/ownership：43/43 frozen ownership，13/13 managed claims，overlay drift 通过
- Shell syntax：canonical、installed 与 preset scripts 全部 `bash -n` 通过
- Shared production eval：source 7/7、installed 7/7 passed
- Codex native eval：source 7/7、installed 7/7 passed
- Full local-source throwaway：exit 0；覆盖 clean init、preview/switch、preset
  apply/reapply、`trellis update`、ownership checkpoints、sidecar、platform copies、
  package validation、production eval 与 no-developer fixture
- Remote feature ref：`git ls-remote --heads origin
  refs/heads/feat/117-verify-extension-installation` exit 0、空输出；exact pushed-ref clean
  install 尚不可执行，仍是后续 post-push publication gate，未被 local sample 冒充

所有既有自动化通过，但不反证 `BR-117-F7`；该 finding 由未覆盖的正常 recorder 输入和
supersession 路径稳定复现。

### 证据交接

- Planning approval：schema `2.0`、`typed_exit=approved`、ambiguity review passed、
  fixed-scope scanner 无 unchecked normative hit、`source=explicit-post-planning-review`，
  三份规划 digest current。
- Commit handoff：`task-commit-plans/002.json` 绑定当前 HEAD；expected/actual tree 均为
  `492f6ba19fb12d59ec4d2d5a4e9642348e980b05`。
- Finding lifecycle：旧 `BR-117-F1/F2` 在 `reviews/002-closure.md` 已关闭；本 fresh final
  reviewer 身份独立，但发现新的 current-scope `BR-117-F7`，因此本轮不能成为
  zero-finding final round。
- Docs SSOT：strategy 为 `ssot_first`。Package contract、workflow specs、durable
  requirements、README、registry/manifest、installer 与分发副本总体同步；但 durable
  contract 明确要求 recorder/schema/supersession freshness，当前 runtime 未完整承接，
  所以 current-scope Docs SSOT 与实现仍不一致。
- 部署/安全：完整 diff 未修改 CI/CD、容器、Compose、K8s/Kustomize、DB migration、
  Makefile、dependency manifest 或生产数据面。F1 credential redaction 已关闭；F7 影响
  recorder correctness 与 gate lineage，不扩大 production/data 副作用。
- Follow-up：exact pushed feature-ref clean install 只在后续授权 push 后执行；它不是
  `BR-117-F7` 的替代验证，也不是本地 Branch Review finding。
- 本报告可作为 Branch Review Gate 的 `implementation_required` raw evidence，不能支持
  `passed`。

### 结论

- 新 qualified finding：`BR-117-F7`，P2，open
- Scope proposal：无
- 其它新 candidate：无
- 最终 typed recommendation：`implementation_required`

当前分支不能通过 Branch Review Gate。实现 owner 修复 `BR-117-F7` 后，必须重新完成
`guru-check-task`、fresh task commit、finding closure 与独立 fresh final review。
