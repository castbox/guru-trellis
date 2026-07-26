# Issue #117 Branch Review Round 7 最终原始报告

## 检查完成

### 审查身份与范围

- 审查意图：`fresh_final_review`
- 角色：最终审查代理 `/root/issue117_final_after_f8`
- 独立性：未参与 Issue #117 implementation，也未参与
  `BR-117-F1`、`BR-117-F2`、`BR-117-F7` 或 `BR-117-F8` closure
- Task：`.trellis/tasks/07-25-117-verify-extension-installation`
- Issue：`castbox/guru-trellis#117`
- Branch：`feat/117-verify-extension-installation`
- Base：`origin/main`
- Base HEAD / merge base：
  `0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- Reviewed HEAD：
  `3281db77b8f829e850064a33190838eb17ca4c31`
- 完整 committed range：
  `origin/main...3281db77b8f829e850064a33190838eb17ca4c31`
- 完整范围规模：332 files，51571 insertions，5681 deletions
- 行为边界：只读审查完整实现、task evidence 与 committed range；除本 raw
  report 外未修改 implementation、tests、durable docs、`review.md`、
  `review-gate.json`、`phase2-check.json`、`agent-assignment.json` 或 task commit
  plan，未 commit、push、创建 PR、关闭 Issue 或调用 finish-work

Workspace boundary fresh 通过：

- Expected workspace 与 actual repo root 都是当前 Issue #117 worktree。
- Source checkout 为 `/Users/wumengye/Documents/GoProjects/guru-trellis`，状态 clean。
- 写报告前 task worktree 只有主会话维护的 `agent-assignment.json`、
  `task-commit-plans/004.json` 与 `reviews/005-f8-closure.md` lifecycle 改动。
- Suspicious source artifacts、未处理 `.new` / `.bak` 和其它 untracked file：无。

### 已检查文件与证据

- `.agents/skills/guru-review-branch/SKILL.md` 与
  `references/contract.md`
- Live Issue #117 与 accepted-current
  `issuecomment-5045035361`
- `prd.md`、`design.md`、`implement.md`、planning approval 与 issue scope
  ledger
- Current Phase 2、F8 worker report、implementation handoff 与 task commit plan
- `review.md`、`review-gate.json`、`reviews/001-final.md` 至
  `reviews/005-f8-closure.md`
- 完整 `origin/main...HEAD` file inventory、diff hunk/function inventory、
  四个 commits、风险面与 whitespace
- Canonical 与 installed `guru-verify-extension-installation` Skill、
  package contract、Interface、全部 schema/example/eval、tests 与 wrappers
- Runtime executor、recorder、checker、public wrapper 与 native eval adapter
- Source/installed registry、manifest、workflow markers、consumer schema、
  preset installer、ownership inventory、throwaway 与 Docs SSOT
- Canonical、installed、Agents、Codex、Claude、Cursor 分发副本
- Trellis 官方首页、custom workflow 与 spec template marketplace 文档

Planning approval fresh checker 通过：schema `2.0`、
`typed_exit=approved`，三份 planning artifact 与审批 digest 保持一致。

Current Phase 2 semantic conclusion 为 `passed`，绑定当前 code tree 与
`3281db77b8f829e850064a33190838eb17ca4c31`：

- Runtime 592 passed、13 skipped
- Skill package 175 passed
- Preset 45 passed
- Ownership 9 passed
- Canonical/installed package contract 各 8/8 passed
- Source/installed graph 各 12 active Skills、46 exits、12 invokes、
  27 targets、0 legacy
- Shared/Codex/Claude 最终 source+installed 均 7/7；Claude installed 前两次
  6/7 transient 与第三次 clean-auth 7/7 均保留在 evidence
- Cursor 按当前 adapter contract 返回 `unsupported`
- Full local-source throwaway exit 0

### 既有 Finding Closure 链复核

1. `BR-117-F1`：Round 1 发现 credential URL redaction 缺口；Round 2 对
   authority userinfo shapes、artifact absence 与 generic error surface 完成
   closure，状态 `closed`。
2. `BR-117-F2`：Round 1 发现 task/worktree identity 缺口；Round 2 对 active
   task、archived task、branch/repository/worktree mapping 完成 closure，状态
   `closed`。
3. `BR-117-F7`：Round 3 发现 recorder schema 与 supersession lineage 缺口；
   Round 4 对 schema-first fail-closed、no-prior/nonmatching/exact-prior
   supersession 完成 closure，状态 `closed`。
4. `BR-117-F8`：Round 4 发现 committed raw report 的 EOF 多余空行使 full-range
   lint 失败；Round 6 对 exact blob、commit tree 与三个 whitespace gate 完成
   closure，状态 `closed`。

Round 6 只授权派发未参与 closure 的 fresh final reviewer，不是 final pass。本轮已
重新覆盖当前完整 `origin/main...HEAD`，没有把任一 closure report 当作零 finding
放行结论。

## 未修复问题

### P2 `BR-117-F9`：annotated stable tag 未绑定或复验实际 checkout commit identity

文件：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18025`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18100`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18166`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:15824`

Qualification：

- Disposition：`qualified_finding`
- Scenario class：`normal_required_behavior`
- Severity：P2
- Status：`open`
- Requirement refs：
  - `prd.md` 3.3 的 remote HEAD / reviewed HEAD / ref binding
  - `prd.md` 3.5 与 acceptance 的真实 remote-ref clean installation
  - `design.md` 6.1 第 5 项“Clone 后复验 checkout HEAD”
  - Package Interface `remote_identity` 的
    `ls-remote HEAD and cloned checkout HEAD`
  - Package contract `Entry`、`Semantic loop` 与 `Private evidence`
  - `.trellis/spec/workflow/companion-scripts.md` 的
    `checks out that exact HEAD`
- Scope basis：README 明确把 repo release tag 作为稳定、可复现的默认安装 source，
  并明确 release tag 为 annotated tag。对该 stable tag 执行 clean verification 是
  当前产品合同中的正常路径，不是 nonstandard proposal，也不依赖恶意篡改、伪造、
  hostile input、竞态、TOCTOU、锁或其它排除场景。

当前实现：

1. Executor 对 requested ref 执行
   `git ls-remote <remote> refs/tags/<tag>`，把 direct ref OID 写入
   `remote_head`。
2. Clone 后执行 `git checkout --detach <remote_head>`，但 checkout 成功后没有执行
   `git rev-parse --verify HEAD^{commit}`，也没有记录或比较实际 checkout HEAD。
3. `status=passed` 只要求 clone、checkout、throwaway command return code 为 0，
   以及 asset/ownership/sidecar checks 通过；它不要求 cloned checkout HEAD
   evidence 存在或匹配 resolved commit。
4. Execution facts、private owner artifact 与 standalone public
   `resolved_head` 因而都可能继续使用 annotated tag object OID，而不是实际 checkout
   commit identity。
5. 现有 executor test 只 mock `git checkout --detach` return code；没有 annotated
   stable tag、lightweight tag 或 post-checkout HEAD mismatch regression。

Fresh normal-path reproduction：

```text
requested_ref=refs/tags/v0.6.5-guru.2
ls_remote_direct_oid=77ced9be88fd15bc50f3b22f889ccefe0f8a11ea
checkout_head=c2d4b0395c78f8af6b1a21fc99a6bb31e04f1d6f
peeled_commit=c2d4b0395c78f8af6b1a21fc99a6bb31e04f1d6f
direct_oid_equals_checkout_head=no
checkout_head_equals_peeled_commit=yes
```

Local tag inventory independently confirms `v0.6.5`、`v0.6.5-guru.1` 与
`v0.6.5-guru.2` 都是 annotated tags。该差异是标准 Git tag peeling 行为；checkout
本身成功不能证明 recorder 所发布的 `remote_head/resolved_head` 就是实际 checkout
commit。

影响：

- Stable tag 的 private evidence 缺少合同要求的 cloned checkout HEAD，AI adequacy
  review 无法从 owner facts证明被验证 source 的实际 commit identity。
- Standalone verified output 可把 tag object OID 当成 `resolved_head` 交给 consumer，
  与实际 checkout HEAD 的语义不一致。
- 若 workflow 将 reviewed commit SHA 与 annotated tag ref 绑定，当前 direct tag OID
  comparison 还会在 clone 前错误阻塞；若改用 tag object OID 则仍缺少实际 checkout
  commit binding。
- 自动化全绿不反证该 finding，因为现有成功 corpus 没有覆盖当前 README 默认的
  annotated stable-tag identity path。

Required closure：

1. 将 requested ref 的 direct object identity 与其 resolved checkout commit identity
   明确区分；正确处理 branch、lightweight tag 与 annotated tag。
2. Clone/checkout 后执行 `git rev-parse --verify HEAD^{commit}`，记录 sanitized
   command evidence，并将 actual checkout commit 与 frozen resolved commit 比较；
   mismatch 必须在任何 install/verified 结论前 fail closed。
3. 让 execution facts、private artifact 与 standalone `resolved_head` 的字段语义和
   schema/contract 保持一致；如需迁移字段，遵守现有 public API 与 schema compatibility
   合同，不静默改变既有语义。
4. 增加 annotated stable tag、lightweight tag、branch、post-checkout mismatch 与
   workflow reviewed commit binding 的正常路径回归。
5. 修复后重新执行完整 `guru-check-task`、task commit、finding closure 与独立 fresh
   final review。

## 其它 Candidate 与 Observation

### Rejected candidate：post-commit 普通 Phase 2 checker stale

Round 6 已以 `RC-F8-1` 保留该 candidate，并由 current evidence 否定：
Branch Review 使用 committed-head audit profile，fresh
`review_branch_entry_precondition_errors(...)` 为 `[]`；普通 checker 的非 audit
profile 不是 post-commit Branch Review consumer。该 candidate 不升级为 finding。

### Observation：Claude clean-auth native eval

Claude installed eval 前两次 6/7 是认证来源切换期的 transient；明确 unset
`ANTHROPIC_AUTH_TOKEN` 与 `ANTHROPIC_BASE_URL` 后，第三次 source+installed 均为
7/7。用户随后确认 Claude CLI 已恢复。该历史已透明记录，不构成 current code finding。

### Observation：Cursor adapter

Cursor 按当前 package adapter contract 返回 `unsupported`；没有伪造 pass，也没有
违反 Issue #117 已批准范围，不构成 finding 或 scope proposal。

### Observation：exact pushed feature-ref gate

Exact pushed feature-ref clean installation 尚未执行，因为当前 feature ref 尚未获授权
push。Current full local-source throwaway 只证明 unpublished current source 的
install/update/reapply，不冒充 remote publication evidence。

该 post-push gate 仍须在后续授权 push 后绑定 exact remote ref 与 reviewed HEAD 独立
执行；它不是 `BR-117-F9` 的替代验证，也不应被误报为本地 pass。

除 `BR-117-F9` 外，没有新的 qualified finding、scope proposal、current-scope
follow-up 或 rejected candidate。

## Fresh 验证结果

- Lint：通过
  - `git diff --check origin/main...HEAD`
  - `git diff --check origin/main`
  - `git diff --check`
- Commit message validation：通过；4 个 #117 work commits，0 error
- Workspace / planning / assignment：fresh checker 全部通过
- Assignment：20 agents、6 个既有 review rounds，当前 fresh reviewer 未参与 closure
- Branch Review entry：committed-head Phase 2 audit 与 13 项 entry
  preconditions 均无 error
- Focused extension runtime：19/19 passed
- Canonical package contract：8/8 passed
- Installed package contract：8/8 passed
- Source validator：passed，12 Skills / 46 exits / 12 invokes /
  27 targets，0 legacy
- Installed validator：passed，2322 managed files，0 sidecar，
  0 removal，0 conflict
- Dogfood overlay drift：passed
- Ownership：43 frozen、13 claims、54 managed assets，0 error
- Distribution：canonical、installed、Agents、Codex、Claude、Cursor 六处分发
  byte-identical
- JSON、canonical/installed Bash syntax 与 Python compile：通过
- Unhandled `.new` / `.bak`：0

本轮没有再次运行 592-test、175-test、45-test、9-test、全平台 native eval 与 full
local-source throwaway 长矩阵。Current code tree 与绑定这些结果的 fresh F8 Phase 2
之间没有 implementation 变化；本轮重新执行 focused runtime、package contracts、
validators、ownership、drift、distribution、compile/syntax 与 whitespace gates，并
对 annotated stable tag 另做独立 public remote clone/checkout probe。长矩阵结果可
精确复用，但它没有覆盖 `BR-117-F9` 的 annotated-tag identity assertion。

## Docs SSOT、Deployment、Upgrade 与 Security

- Docs SSOT strategy：`ssot_first`。
- Package Interface、package contract、approved design 与 durable runtime contract
  已一致要求 cloned checkout HEAD；F9 是 runtime/tests 未完整承接既有 SSOT，不需要
  通过弱化文档关闭。
- F1/F2/F7/F8 closure 后，其对应 runtime、tests、manifest 与 task evidence 保持 current；
  F9 修复必须同步 canonical、installed 与平台分发副本，并重新通过 dogfood drift。
- 完整 committed range 未修改 CI/CD workflow、Docker/Compose、
  Kubernetes/Helm/Kustomize、DB migration、Makefile、dependency manifest 或
  production data plane；F9 是 extension verification provenance/correctness 问题，
  不要求部署资产或数据迁移。
- Current source/installed validators、ownership freeze、零 sidecar 与分发一致性均
  通过；F9 修复后仍须重新执行 clean install、update/reapply 与 upgrade/update
  抗漂移门禁。
- F9 不扩大 hostile-input/security scope，也未发现新的 credential 或 secret
  persistence；既有 F1 redaction closure 保持有效。
- 本报告未记录 token、secret、credential URL、endpoint、native raw transcript、
  临时 clone 本机路径或敏感输出。

## 结论

- 既有 findings：`BR-117-F1`、`BR-117-F2`、`BR-117-F7`、
  `BR-117-F8` 均 `closed`
- 新 qualified finding：`BR-117-F9`，P2，`open`
- Scenario class：`normal_required_behavior`
- Scope proposal：0
- 新 rejected candidate：0
- 最终 typed recommendation：`implementation_required`

当前分支不能通过 Branch Review Gate。实现 owner 修复 `BR-117-F9` 后，必须重新完成
`guru-check-task`、fresh task commit、finding closure 与独立 fresh final review。

本报告是 fresh final review 的 raw evidence，不更新或冒充
`review.md` / `review-gate.json`，不授权 publication、push、PR、Issue #117 closure
或 finish-work。
