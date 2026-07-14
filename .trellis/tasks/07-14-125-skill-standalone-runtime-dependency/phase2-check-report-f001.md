# Issue #125 F-001 修复后 Fresh Phase 2 Check Report

## 1. 结论

- Status：`passed`
- Logical role：`阶段二检查代理`
- Technical identity：`/root/trellis_check_125_f001`
- Review mode：F-001 修复后的 fresh Phase 2 check，不是 Branch Review 或 recorder。
- Checked HEAD：`e4937dfe19c9e3d889144ca5ef9d7afd42a429b5`
- Stacked base：`origin/feat/122-guru-create-task-commit`
- Base HEAD / merge base：`49bf572e6a89bff9c63416bea64254cda0c20bf0`
- 完整 committed diff：78 paths，5279 insertions，326 deletions。
- Findings：0 个 open finding，0 个 blocker。
- F-001 closure readiness：`ready-for-finding-closure-review`。
- Recorder sufficiency：本报告覆盖 Issue #125 六项需求、批准设计、Docs SSOT、Round 001
  F-001、完整 stacked-base diff、当前 finding fix、schema/runtime/installer/platform copies、
  tests、upgrade、security、deployment 与 dirty paths，足以供 main session 重录 fresh passing
  `phase2-check.json`。本代理未运行 `record-phase2-check.sh`、`check-phase2-check.sh` 或任何
  review/assignment/commit recorder。

## 2. 启动门禁与审查范围

### 2.1 Workspace、planning 与 live scope

- `check-workspace-boundary.sh --json`：`status=ok`；actual repo root 等于批准 worktree，source
  checkout clean，`suspicious_source_artifacts[]` 为空。
- `check-planning-approval.sh --json`：`status=ok`；schema 1.2、ambiguity review、fixed scan
  scope、空 `unchecked_normative_hits[]` 与 `prd.md` / `design.md` / `implement.md` digest 均有效。
- `task.py validate`：通过；`implement.jsonl` 6 entries，`check.jsonl` 8 entries。
- Live Issue #125：`OPEN`，六项需求与批准规划一致。
- Live PR #124：`OPEN / MERGEABLE / CLEAN`，head
  `feat/122-guru-create-task-commit@49bf572e6a89bff9c63416bea64254cda0c20bf0`，stacked base
  未漂移。
- Issue ledger：`close_issues=[125]`、`related_issues=[122]`、`followup_issues=[]`，分类正确；
  #122 archive/task 未修改。

### 2.2 已读取证据

- `.agents/skills/trellis-check/SKILL.md`。
- Task `prd.md`、`design.md`、`implement.md` 与 `design.md` 中唯一 Docs SSOT Plan。
- `implementation-handoff.md`、原 `phase2-check-report.md`、`phase2-check.json`、
  `phase2-findings.json`。
- Round 001 `reviews/001-final-review.md`、`review.md`、`review-gate.json`。
- `finding-fix-handoff-001.md`、`issue-scope-ledger.json`。
- 完整 `origin/feat/122-guru-create-task-commit...HEAD` committed diff 与当前 uncommitted
  F-001 fix。
- Applicable specs、durable requirements、public README、canonical workflow/package、schema、
  extension manifest、runtime/dispatcher、installer、tests 与受管平台副本。

## 3. Dirty Paths 与边界

### 3.1 F-001 functional fix

1. `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
2. `.trellis/guru-team/scripts/python/guru_team_trellis.py`
3. `trellis/skills/guru-team/tests/test_skill_packages.py`
4. `finding-fix-handoff-001.md`

Canonical 与 dogfood runtime bytes 相同。Production interface、extension manifest、installer、
throwaway verifier、durable docs 与 public README 相对 reviewed HEAD 均未变化。

### 3.2 Existing task/review metadata

- `agent-assignment.json`
- `task-commit-plans/001.json`
- `review-gate.json`
- `review.md`
- `reviews/001-final-review.md`

这些路径记录前序 commit/review/finding 分派事实，不是 F-001 功能实现。本代理未修改、覆盖、
清理或重新记录它们。未出现 #122 archive、workspace journal、全局 npm、`node_modules`、
deployment asset、secret 或 customer-data dirty path。

## 4. 六项需求与设计承接

### R1 Direct discovery routing

- `workflow` / `standalone` mode id 未改变。
- `workflow.routing=global_workflow`；`standalone.routing=direct_discovery`。
- 两种 mode 的九个 `entry_precondition_ids` 顺序和集合完全一致，typed exits 仍为
  `committed`、`revision-required`、`blocked`。

### R2 完整 runtime dependency

- Interface schema 1.1 强制闭集 `runtime_dependency` 和 validator `runtime_command`。
- Production dependency 与 extension `skill_runtime` 一致：extension `guru-team`、API `1.0`、
  dispatcher `run-skill-command`、installed manifest path 与 preset distribution 均匹配。
- Fresh source/installed validation 均通过；installed inventory 为 43 managed files、三平台、
  0 sidecar/removal/conflict。

### R3 Non-portable boundary

- Canonical package contract、Skill、spec、durable requirements 与三份 public README 均明确：
  `standalone` 只移除 global routing，不提供单目录 self-contained/portable 分发。
- 5 个 package tests 证明 package-only wrapper exit 2，并包含完整 preset 安装/升级与
  sidecar/source/installed remediation。

### R4 Shared runtime SSOT

- Package wrappers 只定位 audited `run-skill-command`、传 package root、固定 validator id 与
  原始参数；没有旧 companion fallback。
- Parser、task/gate 解析、Git snapshot/staging/transaction/rollback/result validation 继续只在
  shared Guru Team runtime。
- F-001 新增 `skill_runtime_command_maps_to_dispatcher()`；source validator 与 runtime resolver
  共用同一机械判定，没有复制第二份 dispatcher self-mapping 规则。

### R5 Fail closed 与 remediation

- 缺失 manifest/dispatcher、API/dependency/command mismatch、managed discovery drift 与
  package-only copy 仍在目标 companion command 和业务副作用前 blocked。
- Fresh `.agents/.../check-task-commit-plan.sh --help` 经 shared dispatcher 成功进入
  `check-commit-messages`，证明当前 production standalone direct discovery 正常。

### R6 Canonical、分发、docs 与安装清单一致

- Canonical package、audited installed、shared、Codex、Cursor、Claude 五个副本各 8 files，
  忽略测试产生的 untracked `__pycache__` 后 bytes 相同；installed validator 同时验证
  executable mode 与 manifest hashes。
- Canonical/dogfood Python runtime、Bash dispatcher、interface schema bytes 一致。
- Dispatcher 存在于 extension companion inventory、`MANAGED_ASSET_PATHS`、executable handling、
  installed-file README 与 throwaway probes。
- Dogfood overlay drift 通过；recursive `.new` / `.bak` 为 0。

## 5. F-001 精确复现与修复判断

Round 001 finding 指出：`runtime_command=run-skill-command` 同时满足 schema pattern 和 extension
published membership，原 source validator 会通过，但 runtime resolver 会拒绝 dispatcher
self-mapping。

Fresh 精确 probe 结果：

- JSON Schema errors：`[]`。
- Dispatcher published membership：`true`。
- Source validation status：`failed`。
- 完整 `errors` 数组只包含：
  `interface for guru-example-action validator result_validator runtime_command must not equal runtime_dependency.dispatcher`。

永久 regression 精确断言相同的单元素 `errors` 数组。Production mappings 保持：

- `candidate_validator -> check-commit-messages`
- `exact_executor -> create-task-commit`
- dispatcher：`run-skill-command`

因此 source/installed distribution gate 与 runtime invocation 对 dispatcher self-mapping 的机械
结论已一致，F-001 的 root cause 已修复，并具备交给 finding owner 进行独立 closure review 的条件。

## 6. Docs SSOT Reconciliation

- Docs state：`partial_docs`。
- Strategy：`ssot_first`。
- 原实现已把 mode routing、runtime dependency、non-portable boundary、dispatcher、remediation、
  installer/update-reapply matrix 写入四份 `.trellis/spec/**`、三份 durable requirements、
  canonical workflow/package contract 与三份 public README。
- F-001 只让 source validator 承接既有“command mapping mismatch 在分发/调用前 fail closed”机器
  合同，没有改变 public mode、schema、runtime API、installer、remediation、typed exit、upgrade
  或 deployment 语义。
- 本轮无 durable docs、planning artifact 或 public README 更新需求；修复过程和逐轮 finding 只保留
  task history。`ssot_first` no-change judgment 成立，没有 current-scope Docs SSOT blocker。

## 7. Tests 与静态验证

### 7.1 独立完整测试

| Suite | 结果 |
| --- | --- |
| Canonical package contract | 5 passed |
| Skill package/source/distribution/runtime dispatcher | 65 passed |
| Preset installer | 36 passed |
| Shared runtime | 275 passed |
| 合计 | 381 passed |

### 7.2 Contract、static 与 sync

- 精确 F-001 probe：schema valid、published membership true、唯一 self-mapping error。
- `check-skill-packages --mode source`：passed；1 active、1 reserved、1 invoke、3 exits。
- `check-skill-packages --mode installed`：passed；43 files、三平台、0 sidecar/removal/conflict。
- JSON parse：9 个受影响 canonical/installed/fixture schema/interface/manifest 通过。
- Bash `bash -n`：canonical workflow/preset/package 与 dogfood wrappers 通过。
- Python `py_compile`：canonical/dogfood runtime、installer 与 skill tests 通过。
- `git diff --check`：committed range、current dirty delta、base-to-worktree 三种范围均通过。
- Package copies/runtime/schema byte audit：通过。
- `check-dogfood-overlay-drift.sh`：通过。
- Recursive `.new` / `.bak`：0。

仓库没有独立 `pyproject.toml` / `setup.cfg` / `tox.ini` / `.ruff.toml` / `mypy.ini` 项目级
lint/type-check runner；本轮以 JSON/Bash/Python static、contract validators 与完整 tests 为门禁。

## 8. Upgrade / Update 与开箱判断

- 原 clean throwaway evidence SHA-256 仍为
  `661b0a9c3523079476d1f0cbfe4490b08c0f18341d97ea0e7f3aea0579daba5f`，记录初装、standalone
  probe、`trellis update --force`、workflow re-selection、preset reapply、第二次 probe、
  source/installed validation、recursive sidecar scan 与 closeout smoke 通过。
- F-001 后 installer、throwaway verifier、extension manifest 与 production interface mappings
  相对 reviewed HEAD 未改变。变化只是在被安装 runtime 中复用一个纯 dispatcher equality helper
  并提前拒绝无效 mapping。
- Fresh 65 skill tests、36 installer tests、275 runtime tests、source/installed validation、
  direct discovery probe、managed bytes/modes 与 dogfood drift 证明修复不影响前序 clean throwaway
  的安装/update-reapply 结论，因此本轮合理复用该 throwaway evidence，无需重复网络 canary。
- Exact feature-ref remote marketplace verification 仍未完成；reviewed content push 后必须由
  `trellis-finish-work` 生成 immutable evidence。Public marketplace sample 不能替代。

## 9. 安全与部署

- Sensitive literal scan 未发现 token、private key、签名 URL、数据库 URL 或 credential 被引入。
- F-001 helper 只比较已解析 interface 的稳定 string id，不接受任意路径，不改变 `os.execv`
  target 形成方式，不增加 fallback；fail-closed 时机提前到 source validation。
- Component-wise `lstat`、closed validator id、published command membership、managed executable
  path 与 installed inventory 校验均保留。
- 无服务、API、CLI 业务入口、worker、schedule、queue、DB schema/migration、CI/CD workflow、
  Dockerfile/Compose、Kubernetes/Kustomize/Helm 或 Makefile 变更；不需要部署资产同步，部署形态
  不变。

## 10. Remaining Risks 与后续门禁

1. 本报告不是 finding closure review 或 Branch Review。Main session 重录 fresh
   `phase2-check.json` 并创建新 task commit sequence 后，应由 F-001 finding owner 仅执行问题闭环
   审查，再派发从未参与前序 review 的全新最终放行审查代理。
2. #125 仍 stacked 于 PR #124；若 #124 合并并 retarget 到 `main`，必须按新 base 重跑所有
   freshness-sensitive Phase 2、Branch Review 与 remote marketplace gate。
3. Issue #125 的 `acceptance_evidence[]` 仍须在 publish 前依据真实 evidence 补齐；#122 继续
   related-only。
4. Exact feature-ref remote marketplace verification 留待 reviewed content push 后的
   `trellis-finish-work`，当前不得声称远端门禁已通过。

## 11. Final Gate Judgment

Issue #125 六项需求仍由 durable docs、schema 1.1、extension runtime API、shared dispatcher、
thin wrappers、installer、managed platform copies、negative tests、standalone probe 与前序 clean
throwaway/update-reapply evidence完整覆盖。F-001 的 source/runtime 语义漂移已由共享判定和精确
regression 关闭，fresh 381 tests 与所有 static/distribution/drift/sidecar gate 通过。

最终结论：`passed`。当前 findings_count 为 0，足以供 main session 重录 fresh passing
`phase2-check.json`；后续仍须遵守 finding closure、fresh final review 与 finish-work remote gate。
