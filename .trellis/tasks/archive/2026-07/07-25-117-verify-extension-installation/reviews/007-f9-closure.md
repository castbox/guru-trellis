# Issue #117 `BR-117-F9` 问题闭环审查原始报告

## 检查完成

### 审查身份与范围

- 角色：`问题闭环审查代理`
- Agent：`/root/issue117_f9_closure2`
- Review intent：`finding_fix_review`
- Task：`.trellis/tasks/07-25-117-verify-extension-installation`
- Base：`origin/main` =
  `0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- Reviewed HEAD：
  `a47e1fbd7bedb001649814969096076bb70157db`
- 完整 diff range：
  `origin/main...a47e1fbd7bedb001649814969096076bb70157db`
- Merge base：
  `0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- 完整范围：336 个 changed files，54,535 additions，5,689 deletions。
- 本轮性质：只执行 `BR-117-F9` closure 与完整范围的新 candidate
  资格化；这不是 fresh final pass，不能产生 Branch Review `passed`。

### Workspace boundary

- Expected workspace：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/117-verify-extension-installation`
- Actual repo root：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/117-verify-extension-installation`
- Source checkout：
  `/Users/wumengye/Documents/GoProjects/guru-trellis`
- Boundary validator：`status=ok`
- Source checkout status：空。
- Suspicious source artifacts：空。
- 审查开始时 task worktree 仅有当前 task 的
  `agent-assignment.json` 与 `task-commit-plans/005.json` metadata tail；
  二者符合 Branch Review entry 允许范围，未修改实现候选。

### Entry evidence

- `planning-approval.json` 为 schema `2.0`、`typed_exit=approved`；
  `ambiguity_review.status=passed`，固定 planning scope 没有
  `unchecked_normative_hits`，确认来源为
  `explicit-post-planning-review`。
- `prd.md`、`design.md`、`implement.md` 当前 SHA-256 分别为
  `e8f4402d93bbd7bd141bd6fa0e493a452a5e4f71ec25f5fb82a8a5b48c25d714`、
  `24437f24e32d194d8ac86759aa1f0af8fba0aeb03395df07c2a8dac7f66b9d9d`、
  `7922efb0ec9d5995370f2868ea69a1eef46aef56d53007d6b39325b43cab9102`；
  均与 planning approval 的 reviewed/approved digest 一致。
- `contract-wording-review.json` SHA-256 为
  `6f4665ab122d725c08d10f8628770b7b70d5819815f725f60911db331993194f`，
  `typed_exit=pass`。
- `phase2-check.json` 为 schema `2.0`、`typed_exit=passed`，独立
  F9 Phase 2 报告
  `phase2-worker-report-f9.md` SHA-256 为
  `7893a37806dceda76b4b09ff0d62ea8b0c8dc018f5d90d63538f00af3223490b`。
- Current `task-commit-plans/005.json` 为 `status=committed`，绑定
  commit `a47e1fbd...`、parent `3281db77...`；`expected_tree` 与
  `actual_tree` 均为
  `8d39df400583d0eb987eb917afc5159bccbb7e01`，26 个 committed path
  的 expected/actual blob 与 mode 全部一致。
- `issue-scope-ledger.json` 仍以 #117 为唯一 `close_issue`；
  #115/#109/#116/#144/#146 仅 related，#81/#118/#119/#132 保持
  follow-up，不被本轮关闭。
- 已读取 Round 1-7 lifecycle、`reviews/001-final.md` 至
  `reviews/006-final.md`、current `review.md` 与 `review-gate.json`。
  Current gate 保留 Round 7 在 `3281db77...` 登记的 open
  `BR-117-F9`，这是 closure recorder 前的正确旧状态，不是 final pass。
- Current assignment 已把本 Agent 作为 fresh
  `问题闭环审查代理` 绑定到 `a47e1fbd...`；没有 replacement 或
  same-agent continuity 缺口。

### 已检查文件

- 规划与任务证据：
  `prd.md`、`design.md`、`implement.md`、`planning-approval.json`、
  `contract-wording-review.json`、`implementation-handoff.md`、
  `phase2-check.json`、`phase2-worker-report-f9.md`、
  `issue-review.json`、`issue-scope-ledger.json`、review lifecycle 与
  task commit plan。
- Branch diff：完整
  `origin/main...a47e1fbd7bedb001649814969096076bb70157db`，不是只审查
  task commit 005。
- Canonical runtime：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- Runtime tests：
  `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
- Canonical package：
  `trellis/skills/guru-team/packages/guru-verify-extension-installation/**`，
  包括 `SKILL.md`、Interface、contract、schemas、examples、evals、
  wrappers 与 tests。
- Installed/platform copies：
  `.trellis/guru-team/skills/packages/`、`.agents/skills/`、
  `.codex/skills/`、`.claude/skills/`、`.cursor/skills/` 下的同名 package，
  以及 canonical/installed runtime。
- Registry、manifest、consumer/target schema、workflow marker、
  preset installer、ownership inventory、throwaway installer 与 eval adapter。
- 相关 specs：
  `.trellis/spec/workflow/{companion-scripts,skill-package-contract,
  workflow-contract,quality-guidelines,index}.md`、
  `.trellis/spec/preset/{installer,upstream-ownership,
  overlay-guidelines}.md` 与 `.trellis/spec/docs/public-docs.md`。
- Durable docs：
  `README.md`、workflow/preset README、
  `docs/requirements/{README,requirement-main,guru-team-trellis-flow}.md`。
- Deployment/security surfaces：CI/CD、container、Compose、K8s/Helm/
  Kustomize、DB migration、Makefile、dependency manifest、credentials、
  public/private evidence 与 post-push installation boundary。

## `BR-117-F9` Closure

### 原 finding 资格

- Finding：`BR-117-F9`
- Owner round：7
- 原 reviewed HEAD：
  `3281db77b8f829e850064a33190838eb17ca4c31`
- 原 severity：`P2`
- Scenario：`normal_required_behavior`
- Requirement refs：
  - `prd.md` 3.3、3.5 与 remote-ref clean-install acceptance；
  - `design.md` 6.1 的 clone 后 checkout HEAD 复验；
  - package Interface `remote_identity`；
  - package contract `Entry`、`Semantic loop`、`Private evidence`；
  - `.trellis/spec/workflow/companion-scripts.md` 的 exact checkout
    commit contract。

README 默认 stable source 是 annotated tag `v0.6.5-guru.2`。Fresh
remote probe 仍稳定返回：

```text
direct_tag_object=77ced9be88fd15bc50f3b22f889ccefe0f8a11ea
peeled_commit=c2d4b0395c78f8af6b1a21fc99a6bb31e04f1d6f
```

该差异是正常 Git annotated-tag 路径，不依赖恶意伪造、篡改、竞态、
TOCTOU、锁或其它已排除场景。

### Closure evidence

1. `guru_team_trellis.py:17961` 新增 exact remote query：
   `git ls-remote <remote> <ref> <ref>^{}`。
2. `guru_team_trellis.py:17968` 的 closed parser：
   - branch/lightweight tag 使用 direct commit；
   - annotated tag 使用 peeled commit；
   - malformed、duplicate、unknown 或缺少 direct row 时返回 unresolved，
     不猜测 identity。
3. `guru_team_trellis.py:18034` 在 clone 前冻结 resolved commit；
   workflow `reviewed_head` 与 compatibility `expected_head` 都和该 commit
   比较。
4. `guru_team_trellis.py:18128` 按 frozen resolved commit 执行 detached
   checkout；`guru_team_trellis.py:18140` 随后执行并记录
   `git rev-parse --verify HEAD^{commit}`。
5. `guru_team_trellis.py:18157` 只有 actual checkout commit 是合法
   lowercase 40-hex 且精确等于 frozen commit 时，才运行 throwaway；
   mismatch 在任何 install/`passed` 前 fail closed。
6. `guru_team_trellis.py:25750` 的 checker freshness 使用同一
   direct/peeled parser；remote ref 漂移或解析变化使旧 evidence stale。
7. `guru_team_trellis.py:25869` 的 standalone public projection 只发布
   owner `repository.remote_head`，其当前合同语义是 resolved checkout
   commit；direct tag-object 不进入 DTO。
8. Canonical Interface `interface.json:23`、`:64` 与 package contract
   `references/contract.md:47`、`:81` 已同步该语义；schema version、
   public fields、typed exits 与 consumer mapping 未发生破坏性变化。
9. 新增 regression：
   - `test_guru_team_trellis.py:15354` checker/public annotated-tag
     projection；
   - `:15869` branch/lightweight/annotated resolution；
   - `:15979` post-checkout mismatch；
   - `:16046` workflow reviewed-commit binding。
10. Task commit 005 的 tree evidence 证明 Phase 2 已审查的 runtime、
    tests、Interface、contract、manifest 与六处分发 bytes 精确进入
    `a47e1fbd...`，没有 pre-commit/pass 后内容漂移。

### Closure conclusion

`BR-117-F9` 在 reviewed HEAD
`a47e1fbd7bedb001649814969096076bb70157db` 状态为 `closed`。
Required closure 的 direct-versus-resolved identity、post-checkout evidence、
mismatch fail-closed、private/public field semantics 与正常路径 regressions 均已满足。

## Candidate 资格化

### Qualified closure

- `C9` / `BR-117-F9`：
  `normal_required_behavior`；原 finding 的 supported stable-tag 场景可复现，
  current evidence 证明实现已满足合同，disposition 为 `closed`。

### Rejected candidates

- `RC-007-1`：
  - Scenario：`normal_required_behavior`
  - Affected behavior：remote parser 可能对 branch、lightweight tag、
    annotated tag 或异常 `ls-remote` rows 产生模糊 identity。
  - Qualification result：current parser 只接受 exact direct/peeled rows，
    拒绝 duplicate/malformed/unknown rows；真实 stable-tag probe、三类 ref
    regression 与 checker projection 均一致。
  - Disposition：`rejected_candidate`。证据未显示 current contract violation。
- `RC-007-2`：
  - Scenario：`normal_required_behavior`
  - Affected behavior：F9 Phase 2 在 pre-commit HEAD 上执行，task commit 后
    可能发生 candidate/tree 漂移。
  - Qualification result：task plan 005 的 expected/actual tree、26 个
    path blob/mode 与 current commit 全部匹配；fresh full-range tests 与
    validators 也在 `a47e1fbd...` 上通过。
  - Disposition：`rejected_candidate`。没有 stale Phase 2 或提交内容漂移。

以上 rejected candidates 不携带 severity、finding ref 或其它 finding-only 字段。

### Observations

- `OBS-007-1`：exact pushed feature-ref clean installation 尚未执行。
  当前 feature ref 未获 push 授权；Phase 2 的 full local-source throwaway 只证明
  committed bytes 对应的 unpublished source。该 post-push gate 已明确保留，
  没有被本轮冒充为 remote publication evidence，属于后续 publication/release
  observation，不是 local implementation finding。
- `OBS-007-2`：Cursor source/installed eval 按 package contract 返回
  `unsupported`，没有伪造 native pass；package/corpus bytes、public wrapper
  contract 与 installed distribution 已由 validators/tests 覆盖。
- Earlier Claude transient 已由 F9 Phase 2 clean-auth source/installed 首轮
  `7/7` supersede；没有稳定 source、schema、route 或 distribution mismatch。

### 新 finding 与 scope route

- 新 qualified finding：0
- Scope proposal：0
- Current-scope follow-up candidate：0
- 现有 Issue ledger 变更：不需要。

## Docs SSOT

- Plan strategy：`ssot_first`
- Durable primary owners 已在完整 task diff 中先完成：
  workflow/spec/requirements/README、canonical active package、
  Interface/schema、registry、manifest、runtime 与 tests。
- F9 task delta 已合并到 canonical
  `interface.json` 与 `references/contract.md`：direct/peeled ref、
  frozen resolved commit、post-checkout `HEAD^{commit}` comparison、
  mismatch fail closed，以及 private `remote_head` / public
  `resolved_head` 的 resolved-commit 语义。
- `.trellis/spec/`、workflow、schema、overlay 与 README 对 F9 无需新增
  规则：既有 durable owners 已要求 clone 后 commit verification、
  canonical-first distribution、minimal public DTO、update/reapply、
  ownership 与 zero-sidecar；F9 没有新增 field、exit、consumer、route、
  install command 或 platform capability。
- Canonical、installed、Agents、Codex、Claude、Cursor package fresh
  `diff -qr` 全部相同；canonical/installed runtime `cmp` 相同。
- Task-history-only：
  `BR-117-F9` provenance、真实 direct/peeled OID、实现/Phase 2/commit/
  closure 审计过程与本报告。
- Current PR limitation：exact pushed feature-ref clean installation 仍须在
  push 后绑定 exact remote ref/HEAD 独立执行。
- Docs SSOT conclusion：durable docs、task artifacts、runtime、public/private
  contract、tests 与 distribution 一致；没有 current-scope Docs SSOT blocker。

## Deployment 与 Security

- 完整 336-file range 没有 CI/CD、Docker/Compose、K8s/Helm/Kustomize、
  DB migration、Makefile、dependency manifest 或 production data-plane
  变化。
- F9 是 extension verification provenance/correctness 修复；不改变部署
  transaction、配置键或数据库状态。
- Public DTO 没有新增 direct tag-object、command、log、digest inventory 或
  private artifact body；`remote_head`/`resolved_head` 继续是既有字段，
  语义收敛为实际 checkout commit。
- Remote locator、command evidence 与 retained logs 继续使用 credentials-safe
  locator、sanitized argv、digest 与 size。
- F9 Phase 2 redaction scan 覆盖 112 个 captures、4,633,226 bytes，
  high-risk token/credential/userinfo match 为 0；本报告没有记录 remote URL、
  credential、endpoint 或 native transcript body。
- 未发现新的 secret persistence、权限边界或 hostile-input security finding。

## Install / Update / Reapply

- F9 Phase 2 对与 current commit tree 完全相同的 candidate 执行 full
  local-source throwaway，exit 0；覆盖 new repo、marketplace discovery、
  init、preview/switch、preset apply/reapply、`trellis update`、
  ownership/sidecar/contract/eval，尾部 20/4/20 tests 通过。
- 本 closure round 没有重复生成 3.6 MB throwaway transcript；可消费该证据的
  原因是 task plan 005 逐 path blob/mode 证明 candidate 与
  `a47e1fbd...` commit tree 精确相同，并且本轮重新执行了 full runtime、
  package/preset/ownership、source/installed validators、dogfood drift、
  distribution equality 与 sidecar scan。
- Fresh source/installed validators 均为：
  12 active Skills、46 exits、12 invokes、27 targets、0 legacy。
- Fresh installed manifest：
  2,322 managed files，0 sidecar，0 removal，0 conflict；selected platforms
  为 Claude/Codex/Cursor。
- Fresh ownership：
  43 frozen/active legacy entries、13 managed claims、54 managed assets、
  0 errors。
- Fresh non-fixture `.new`/`.bak` recursive scan：0。
- Exact pushed feature-ref remote matrix 保持 post-push gate，未被 local
  throwaway 或 production eval替代。

## 验证结果

### Lint

- `git diff --check origin/main...a47e1fbd...`：通过。
- Canonical/installed runtime 与 preset/eval Python `py_compile`：通过。
- Marketplace/extension/Interface JSON parse：通过。
- Workflow/preset/package shell `bash -n`：通过。
- Canonical/installed/platform package equality 与 runtime equality：通过。

Lint：通过。

### TypeCheck

仓库没有配置 `mypy`、`pyright` 或等价独立 type-check contract。
生产 Python 入口由 `py_compile`、schema validators 与 full unittests 承接。

TypeCheck：不适用。

### Tests

- Full runtime：
  `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  -> 596 passed，13 skipped。
- Skill packages：
  `python3 -m unittest trellis/skills/guru-team/tests/test_skill_packages.py`
  -> 175 passed。
- Preset + ownership：
  54 passed。
- Canonical package contract：8 passed。
- Installed package contract：8 passed。
- Source validator：passed。
- Installed validator：passed。
- Dogfood overlay drift：passed。
- Upstream ownership：`status=ok`。
- Stable annotated-tag live probe：direct tag-object 与 peeled commit
  精确匹配原 finding reproduction，修复后的 resolved commit 为
  `c2d4b0395c78f8af6b1a21fc99a6bb31e04f1d6f`。

Tests：通过。

## 未修复问题

没有无法自修复的 current-scope implementation finding。本轮为 Branch Review，
按合同未修改实现、gate metadata 或 review summary。

仍需后续 workflow 完成的不是本地 finding：

- 主会话记录本 closure round，更新 `review.md` / `review-gate.json` lifecycle；
- 分派未参与本 closure 的 fresh final reviewer，重新覆盖最终完整
  `origin/main...HEAD`；
- 获得 push 授权后执行 exact pushed feature-ref clean installation；
- 只有 fresh final zero-finding round 与后续 gate 全部通过后，才能考虑
  publication、PR 或 Issue #117 closure。

## 证据交接

### Branch Review

- Reviewed range：
  `origin/main...a47e1fbd7bedb001649814969096076bb70157db`
- Reviewed HEAD：
  `a47e1fbd7bedb001649814969096076bb70157db`
- Closure：`BR-117-F9=closed`
- New findings：0
- Scope proposals：0
- Current-scope follow-up candidates：0
- Deployment/security：无新部署面或 secret/permission finding。
- Docs SSOT：`ssot_first` 一致，F9 durable delta 已合并且六处分发 current。
- 本 raw report 可供主会话记录 finding closure round；它不能作为
  `review.md` 的 fresh final pass，也不能让 `review-gate.json` 返回 `passed`。

### 推荐 route

`fresh_final_review`

下一 reviewer 必须：

1. 未参与本 closure；
2. 覆盖最新完整 `origin/main...HEAD`；
3. 重新读取 current planning、Phase 2、Docs SSOT、ledger、完整 diff 与
   本 closure report；
4. 只有 final round 最后、current、zero-finding 时才允许进入 Branch Review
   `passed` 语义。

## 结论

本问题闭环审查覆盖 336 个 changed files 与完整 committed range。
`BR-117-F9` 的 required closure 已由 code、contract、tests、Phase 2、
task-commit tree 与 fresh post-commit validations 充分证明，状态可更新为
`closed`。没有发现新的 qualified finding、scope proposal 或 current-scope
follow-up。

本轮不是 fresh final pass，不授权 recorder 直接写入 Branch Review `passed`，
不授权 push、PR、publication、Issue #117 closure、release tag 或
`finish-work`。建议主会话记录 closure 后，立即路由到独立
`fresh_final_review`。
