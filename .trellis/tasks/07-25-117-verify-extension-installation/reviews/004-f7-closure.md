# Issue #117 Branch Review Closure Round 5 原始报告

## 检查完成

### 审查身份与范围

- 审查意图：`finding_fix_review`
- 角色：问题闭环审查代理
- Task：`.trellis/tasks/07-25-117-verify-extension-installation`
- Issue：`castbox/guru-trellis#117`
- Branch：`feat/117-verify-extension-installation`
- Base：`origin/main`
- Base HEAD / merge base：`0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- Reviewed HEAD：`3bfbd100c8d75a619da19627e7da276a3f2e367b`
- 完整 committed range：`origin/main...3bfbd100c8d75a619da19627e7da276a3f2e367b`
- 完整范围规模：328 files，49517 insertions，5681 deletions
- F7 finding-fix commit：`538def79408d417107c3adae61c4466116395d96..3bfbd100c8d75a619da19627e7da276a3f2e367b`
- F7 finding-fix 范围规模：18 files，2995 insertions，677 deletions
- 行为边界：只读审查实现、task evidence 与完整 committed range；除本 raw report 外未修改实现、task gate、agent assignment、commit、push、PR 或 Issue，未调用 Branch Review recorder/checker/public wrapper。

本轮是 `BR-117-F7` closure round，不是 `fresh_final_review`，也不能作为 zero-finding final Branch Review pass。

Workspace boundary 通过：

- Expected workspace 与 actual repo root 均为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/117-verify-extension-installation`。
- Source checkout 为 `/Users/wumengye/Documents/GoProjects/guru-trellis`，状态 clean。
- Task worktree 开始时仅有主会话维护的 `agent-assignment.json` 与 `task-commit-plans/003.json` 状态。
- Suspicious source artifacts：无。

### 已检查文件

- `.agents/skills/guru-review-branch/SKILL.md` 与 `references/contract.md`
- `prd.md`、`design.md`、`implement.md`、`planning-approval.json`
- `phase2-check.json`、`issue-scope-ledger.json`、`task-commit-plans/003.json`
- `review.md`、`review-gate.json`、`reviews/001-final.md`、`reviews/002-closure.md`、`reviews/003-final.md`
- 完整 `origin/main...3bfbd100c8d75a619da19627e7da276a3f2e367b` committed diff
- `538def79408d417107c3adae61c4466116395d96..3bfbd100c8d75a619da19627e7da276a3f2e367b` finding-fix diff
- Canonical 与 installed `guru_team_trellis.py`
- Canonical、installed、Agents、Codex、Claude、Cursor 六份 package 与 `tests/test_contract.py`
- Canonical package `SKILL.md`、`references/contract.md`、`interface.json`
- `semantic-review-input.schema.json`、`execution-facts.schema.json`、private evidence schema
- Runtime `ExtensionVerificationRuntimeTest`
- `.trellis/guru-team/extension.json`
- `.trellis/spec/workflow/{skill-package-contract,companion-scripts,workflow-contract,quality-guidelines}.md`
- `.trellis/spec/preset/installer.md`、`.trellis/spec/docs/public-docs.md`
- Durable requirements 与 public/workflow/preset README
- Trellis 官方首页、自定义 workflow 与 spec template marketplace 文档

Planning approval 复核通过：

- Schema `2.0`，`typed_exit=approved`。
- `ambiguity_review.status=passed`，fixed normative scan 无 hit、无 unchecked hit。
- 用户确认来源为 `explicit-post-planning-review`。
- 当前 `prd.md`、`design.md`、`implement.md` SHA-256 分别为 `e8f4402d...`、`24437f24...`、`7922efb0...`，与 approved artifacts 完全一致。

Task commit 003 复核通过：

- Commit 为 `3bfbd100c8d75a619da19627e7da276a3f2e367b`，parent 为 `538def79408d417107c3adae61c4466116395d96`。
- Expected tree 与 actual tree 均为 `6c5e5a2076b7e221371815447fe41458681b467b`。
- F7 runtime、tests、manifest 与 task evidence 的 committed blob/mode 均匹配 plan。

## BR-117-F7 Closure

### Qualification 复核

- Scenario class：`normal_required_behavior`
- Disposition：`qualified_finding`
- 原 severity：P2
- Requirement refs：PRD 3.3；Design 5.2、5.3；package contract `Private evidence` 与 `Exits and re-entry`
- Qualification 仍成立：普通 AI-authored semantic review / executor facts 结构错误，以及首次调用误带 stale supersession ref，均是 honest-but-fallible 支持路径，不依赖恶意篡改、hostile input、竞态、TOCTOU、锁、crash consistency 或跨 OS 原子性。

### 逐项 closure evidence

1. Schema-before-nested-access：`extension_verification_recorder_input_schema()` 读取 `semantic-review-input.schema.json` / `execution-facts.schema.json`，解析其 package-private `$ref`，合并 private `$defs` 并先执行受支持 schema grammar 校验；`extension_verification_review_input()` 与 `extension_verification_execution_input()` 在 `cmd_record_extension_verification()` 访问嵌套字段前完成 instance validation。
2. 受控错误：malformed `redaction`、`capabilities`、missing `typed_exit`、invalid semantic/execution enum 均抛出 exit code 2 的 `WorkflowError`；CLI `main()` 返回 2 且无 traceback，artifact 不写入。
3. No-prior 拒绝：不存在 task-local prior owner 时，任何 `supersedes_verification_ref` 都在 payload 构造和 `write_json()` 前以 `supersession requires an existing prior owner result` 拒绝。
4. Wrong-prior 拒绝：prior owner 存在时，supersession 必须等于该 owner 的 exact `identity.verification_ref`；不匹配 ref 在写入前拒绝。
5. Exact-prior owner 自校验：runtime 先用 private schema、machine/semantic/final digests 与 derived `verification_ref` 校验 existing prior owner，再允许读取 exact prior ref。独立 probe 将 prior `facts_sha256` 改为错误值后，即使传入原 exact ref 也得到 `prior owner result is invalid`。
6. Changed-plan exact-prior re-entry：prior `plan_ref=closeout-plan:prior` 的 blocked owner 可由 `plan_ref=closeout-plan:current` 加 exact prior ref 完整重入；新 owner 保留 supersession lineage，同时绑定 current plan。
7. 新 payload current-input binding：新 payload 从 current `public_input` 构造，并在写入前调用 `extension_verification_payload_errors(..., expected_public_input=public_input)`；独立 probe 对 current input 为零错误，对旧 input 明确产生 `public_input does not match the invocation`。
8. 测试覆盖：runtime 新增四组回归，覆盖 malformed nested type、missing/invalid enum、no-prior、wrong-prior、exact-prior 和 changed-plan re-entry；package contract test 验证两个发布 schema 的 external `$ref` 可解析、正例有效、malformed review/execution 无效。
9. 六处分发一致性：Canonical、installed、Agents、Codex、Claude、Cursor 各 44 个 tracked package files，relative inventory 完全一致；六份 `tests/test_contract.py` SHA-256 均为 `bd909b8a928386953fc1a5029e11bce75ab3c0d2ad0989697d8fdab520022f16`。
10. Runtime 与 manifest 一致：canonical/installed runtime SHA-256 均为 `e7d9dc1db835ffb5ac53512ff6662703cd2d0225dbf297b56bdd775486ad0cdf`；installed extension manifest 已绑定新测试 digest，source/installed validator 均通过。

### F7 结论

`BR-117-F7` 可以关闭，状态建议更新为 `closed`。当前 `review.md` / `review-gate.json` 仍保留 Round 4 的 open F7 状态是 recorder 尚未消费本 closure report 的预期 lifecycle 状态，本代理未改写 gate。

## 新 Candidate 资格审查

### `BR-117-F8`：committed review report 使 full-range lint 失败

Affected path：

- `.trellis/tasks/07-25-117-verify-extension-installation/reviews/002-closure.md:189`

Evidence：

```text
$ git diff --check origin/main...3bfbd100c8d75a619da19627e7da276a3f2e367b
.trellis/tasks/07-25-117-verify-extension-installation/reviews/002-closure.md:189: new blank line at EOF.
```

Qualification before severity：

- Requirement / invariant：`implement.md:171` 明确要求 `git diff --check` 通过；`.trellis/spec/workflow/quality-guidelines.md:57` 将同一命令列为 required validation；Branch Review 必须对完整 committed range 运行 lint。
- Supported reproduction：直接对未篡改的当前 committed range 执行标准 Git lint 即稳定复现。
- Scenario class：`normal_required_behavior`
- Disposition：`qualified_finding`
- Qualification reason：当前 HEAD 新增并提交了 `reviews/002-closure.md`，其 EOF 多余空行使明确的 full-range validation 非零退出；不依赖任何恶意修改或排除场景。
- Severity：P3
- Status：`open`
- Impact：不改变 runtime、public API、安装、部署或安全行为，但当前 committed branch 不能真实声明 `git diff --check` 通过，也不能形成 zero-finding final pass。
- Required closure：删除该报告 EOF 多余空行，重新运行 full-range `git diff --check`；变更后按 Branch Review lifecycle 生成 fresh Phase 2 / task commit evidence，再进入 closure/fresh final routing。

除 `BR-117-F8` 外，没有发现新的 candidate、scope proposal、rejected candidate 或 observation。

## 验证结果

- Focused runtime：`ExtensionVerificationRuntimeTest`，19/19 passed。
- Canonical package contract：8/8 passed。
- Installed package contract：8/8 passed。
- Independent prior/current probe：prior-owner self-validation=true；changed-plan exact-prior accepted=true；current-plan bound=true；old input rejected=true；current input errors=[]。
- Python compile：canonical/installed runtime 与 canonical/installed package contract tests 通过。
- Source validator：passed，12 active Skills / 46 exits / 27 targets。
- Installed validator：passed，2322 managed files，0 sidecar，0 removal，0 conflict。
- Dogfood/ownership：overlay drift passed，frozen ownership 43/43，managed claims 13/13。
- Sidecar scan：0 个 `.new` / `.bak`。
- Distribution：六份 44-file package relative inventory 一致；runtime 与测试 digest 一致。
- Lint：失败；`git diff --check` 仅命中 `reviews/002-closure.md:189` 的 EOF 多余空行。
- TypeCheck：不适用；本范围为 Python/shell/Markdown/JSON，相关 Python compile 通过。
- Fresh Phase 2 evidence：runtime 592 passed / 13 skipped、Skill 175、preset 45、ownership 9、target runtime 19/19、canonical/installed contract 各 8/8、validators 12/46/27、full local-source throwaway exit 0。
- Exact pushed feature-ref clean install：未执行；remote feature ref 尚不存在，仍是授权 push 后的 publication gate，local throwaway 未冒充该证据。

## Docs SSOT

- Plan strategy：`ssot_first`
- Durable docs、package contract、runtime contract、registry/manifest、installer 与平台分发对 F7 的 schema、public-input identity、retry/stale/supersession freshness合同保持一致。
- F7 修复是对既有 durable contract 的实现纠偏，没有新增 semantic contract，因此无需首次追加 durable docs；task artifacts 只保留 finding、Phase 2、commit 和 review lifecycle history。
- Canonical package contract继续规定 private evidence 绑定 public input、plan/supersession freshness、digests 与 `verification_ref`；changed plan/ref/HEAD 仍要求完整 re-entry。
- `BR-117-F8` 仅影响 task-local raw report 格式，不制造 Docs SSOT semantic delta。
- Existing follow-up/PR limit 不变：真实 pushed feature-ref clean install 必须在后续 push 后独立完成。

## Deployment、Upgrade 与 Security

- Deployment：F7 修复与 F8 candidate 均未修改 CI/CD、容器、Compose、K8s/Kustomize、DB migration、Makefile、dependency manifest 或生产数据面。
- Upgrade/update：F7 不改变 public Skill id、Interface/schema id、typed exits、consumer mapping、workflow markers或 #118/#119 activation；manifest 仅同步测试文件 digest。Source/installed validation、dogfood drift、ownership freeze 与零 sidecar均通过。
- Security：F7 不新增安全边界或 hostile-input scope；malformed normal input现在受控 fail closed且不产生 traceback/artifact。既有 credential redaction closure 未回归。F8 没有 runtime 或敏感数据影响。

## 证据交接

- `BR-117-F7`：closure evidence 完整，可供主会话记录 `closed`。
- 新 qualified finding：`BR-117-F8`，P3，`open`。
- 当前 open finding：仅 `BR-117-F8`。
- Branch recommendation：`implementation_required`，原因是 full-range lint 仍失败；本报告不能支持 `review.md` / `review-gate.json` 的 `passed`。
- 在 F8 closure 后，仍必须由未参与本 closure round 的独立 reviewer 对最终完整 range 执行 fresh final review。

## 结论

`BR-117-F7` 已在 `3bfbd100c8d75a619da19627e7da276a3f2e367b` 上完成闭环，可以关闭。

但本 closure round 新发现并资格化了 `BR-117-F8` P3：committed `reviews/002-closure.md` EOF 多余空行使完整范围 `git diff --check` 失败。因此当前分支仍有一个 open finding，不能进入 fresh final pass 或 publication。本报告是 closure round raw evidence，不是 fresh final Branch Review pass。
