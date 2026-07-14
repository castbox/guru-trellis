# #125 Phase 2 Check Report

## 1. 结论

- Status：`passed`
- Logical role：`阶段二检查代理`
- Review mode：Phase 2 check，不是 Branch Review。
- Checked HEAD：`49bf572e6a89bff9c63416bea64254cda0c20bf0`
- Stacked base：`origin/feat/122-guru-create-task-commit`
- Merge base：`49bf572e6a89bff9c63416bea64254cda0c20bf0`
- Findings：1 个已机械修复，0 个未解决 finding，0 个 blocker。
- Recorder sufficiency：本报告覆盖 Issue #125、批准规划、Docs SSOT、代码/Schema/Runtime/Installer/平台副本/测试/升级/安全/部署与 dirty paths，可支撑 main session 记录 passing `phase2-check.json`；本代理未运行 recorder。

## 2. 启动门禁与范围

### 2.1 Workspace 与 planning gate

- `check-workspace-boundary.sh --json --task ...`：通过。
  - expected workspace 与 actual repo root 都是本 task worktree。
  - source checkout 状态为空。
  - `suspicious_source_artifacts[]` 为空。
- `check-planning-approval.sh --json --task ...`：通过。
  - schema 1.2 approval、passed ambiguity review、固定扫描范围、空 `unchecked_normative_hits[]` 与三份 planning digest 均有效。
  - approved HEAD 与当前 HEAD 都是 `49bf572e6a89bff9c63416bea64254cda0c20bf0`。
- 已读取 `check.jsonl` 的 8 个有效条目，以及 `prd.md`、`design.md`、`implement.md`、`implementation-handoff.md`、`issue-scope-ledger.json`、`task-start-context.json`、`task.json`。

### 2.2 Live scope 与 issue ledger

- Live Issue #125 六项需求与批准规划一致：routing independence、完整 runtime dependency、non-portable package、共享 runtime SSOT、缺失/不兼容 fail closed、canonical/docs/installer/platform copies 一致。
- `close_issues=[125]`，`related_issues=[122]`，`followup_issues=[]`，分类正确。
- #122 archive path 相对 `HEAD` 无 diff；未重新打开或修改 #122 task。
- #125 保持 stacked 于 PR #124 的 head/base；未改变 #122 / PR #124 close/ref 语义。
- `acceptance_evidence[]` 仍为空是 publish 前待补的 task metadata，不是当前 Phase 2 实现 blocker；finish/publish 前必须按真实验收证据补齐。

### 2.3 官方与本仓库架构依据

- 已对照 Trellis 官方首页、自定义 workflow、custom spec template marketplace 文档。
- 官方文档确认 workflow 行为由 `.trellis/workflow.md` Markdown 承载，hook/script 只解析或执行确定性动作；spec marketplace 不承载 active task 或平台运行状态。
- 已按 `trellis-meta` 复核 local workflow、generated files、skills/commands 与 update/hash 边界；本实现使用 canonical workflow/preset/package 与生成副本，没有修改上游 Trellis、全局 npm 包或 `node_modules`。

## 3. Requirement / Design Coverage

### R1 机器依赖合同

- Interface schema 升级到 `1.1`，`$id`、contract digest、canonical/fixture/installed schema 同步。
- `workflow.routing=global_workflow`；`standalone.routing=direct_discovery`；mode id 未改变。
- 两种 mode 的 `entry_precondition_ids` 字节顺序一致，并与完整 precondition id 集相等。
- `runtime_dependency` 是 closed object，固定 extension/API/manifest/dispatcher/distribution/portability。
- validator 必须声明 `runtime_command`；source validator 校验其属于 extension `companion_scripts`。
- Extension `0.6.5-guru.6` 发布 `skill_runtime` capability 与 `run-skill-command` command。

### R2 共享 runtime SSOT

- 两个 package wrapper 只解析 audited installed/discovery layout、传 package root、固定 validator id 与原始参数。
- Wrapper 不包含 `validate_commit_message()`、task/gate parser、`git add`、Git transaction/rollback，也不直连 `check-commit-messages.sh` / `create-task-commit.sh`。
- Dispatcher 从 installed runtime 的固定位置推导 repo，以 component-wise `lstat` 检查 runtime、dispatcher、package、interface、manifest 与 mapped command。
- Dispatcher 使用 `validate_skill_installed(..., require_workflow=False)`：standalone invocation 不消费 global workflow route，但仍要求完整 compatible installed inventory。
- `runtime_command` 只接受闭集 id、不得等于 dispatcher、必须由 manifest 发布，最终映射到受管 executable 后才 `os.execv()`。
- 共享 parser、task/gate、snapshot、exact stage、transaction、rollback 与 result validation 仍只在 Guru Team runtime 中。

### R3 Fail-closed 与 remediation

- 单目录 package copy、missing manifest、missing dispatcher、API mismatch、dependency mismatch、runtime command mismatch、discovery drift 均由测试证明 exit 2 / blocked。
- Package-only wrapper stderr 同时包含 non-self-contained/portable 与完整 preset install/upgrade remediation。
- 所有 runtime block 使用同一 remediation，要求处理 `.new` / `.bak`、重跑 source/installed validation 后重试。
- 无 legacy companion command fallback；失败发生在 mapped target companion command 执行前。

### R4 Canonical、installer 与平台分发

- Canonical source 位于 `trellis/skills/guru-team/`、`trellis/workflows/guru-team/`、`trellis/guru-team-extension.json`。
- Dispatcher 已进入 `MANAGED_ASSET_PATHS`、executable handling、extension companion inventory、installed-file README 与 throwaway assertions。
- Installed manifest：`status=ok`，selected platforms 为 Claude/Codex/Cursor，43 个受管 Skill 文件，sidecar/removal/conflict 均为 0。
- Canonical package 与 audited installed、shared、Codex、Cursor、Claude 五个副本均为 8 files，bytes 和 executable mode 完全一致。
- Canonical 与 dogfood Python runtime/dispatcher bytes 一致，mode 均为 `0755`。
- `check-skill-packages --mode source|installed`、dogfood overlay drift、recursive sidecar scan 全部通过。

### R5 Durable docs 与公开文档

- Docs SSOT 的 routing/runtime/non-portable/remediation/upgrade 语义已写入四份 `.trellis/spec/**`、三份 durable requirements、canonical workflow/package contract、根 README、workflow README、preset README。
- 三份 public README 与 durable docs 均说明：`standalone` 只代表 direct discovery，不代表单目录 portable；完整 preset/runtime/inventory 仍是前提。
- 安装清单包含 `run-skill-command.sh`。
- 公开版本矩阵最终统一为已发布 stable `.2`、本分支待发布 canonical `.6`。

## 4. Docs SSOT Reconciliation

- Docs state：`partial_docs`。
- Strategy：`ssot_first`。
- Durable docs input：
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/docs/public-docs.md`
  - `docs/requirements/README.md`
  - `docs/requirements/requirement-main.md`
  - `docs/requirements/guru-team-trellis-flow.md`
  - `README.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
- Task delta 已回写：schema 1.1、mode routing、runtime dependency/capability、non-portable 边界、dispatcher、remediation、installer/update/reapply 验证矩阵。
- Task-history-only：stacked base 决策、Phase 0/1 输出、sub-agent liveness/replacement、临时测试日志与 exact-ref 未 push 结果。
- 结论：durable docs、task artifacts、schema/runtime/installer/tests 最终一致；没有 current-scope Docs SSOT blocker。

## 5. 已修复问题

### F-01 Public workflow README 版本矩阵陈旧

- 文件：`trellis/workflows/guru-team/README.md`
- 问题：canonical manifest 与根 README 已是待发布 `0.6.5-guru.6`，但 workflow README 仍写“本分支 canonical `.4`”。这违反批准设计的 version matrix 同步要求。
- 修复：把该行机械更新为“本分支 canonical `.6`”；已确认没有残留 canonical `.4` / `0.6.5-guru.4` / `0.6.5-guru.5` 声明。
- 影响：仅公开文档版本说明；不改变 stable `.2` 安装命令、runtime、schema 或 installer 行为。
- 状态：closed。

## 6. 验证结果

### 6.1 Tests

| 命令 | 结果 |
| --- | --- |
| `python3 trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py` | 5 tests passed |
| `python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'` | 64 tests passed |
| `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` | 36 tests passed |
| `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` | 275 tests passed |

64-test suite 覆盖 schema/source negative matrix、extension capability drift、missing manifest/dispatcher、API/dependency/command mismatch、discovery drift、unrelated active workflow 下 standalone resolver，以及 installed/platform inventory。5-test package suite覆盖单目录 wrapper fail-closed 与 thin-wrapper 边界。275-test runtime suite保留 task commit/transaction 与 finish/closeout smoke。

### 6.2 Static / contract validation

| 命令 | 结果 |
| --- | --- |
| `python3 -m json.tool`（canonical/installed manifest、schema、active interface） | 通过 |
| `bash -n`（canonical workflow/preset/package 与 dogfood bash） | 通过 |
| `python3 -m py_compile`（runtime 与 installer） | 通过 |
| `check-skill-packages.sh --json --mode source` | passed；1 active、1 reserved、1 invoke、3 exits |
| `.trellis/.../check-skill-packages.sh --json --mode installed` | passed；43 managed files，三平台，0 sidecar/removal/conflict |
| `task.py validate <task>` | 通过；implement 6 entries、check 8 entries |
| `git diff --check` | 通过 |
| `check-dogfood-overlay-drift.sh` | 通过 |
| `.agents/.../check-task-commit-plan.sh --help` | 通过 shared dispatcher 进入现有 companion command |
| Canonical/installed/runtime/platform hash+mode audit | 通过 |
| Recursive `.new` / `.bak` scan | 0 |

仓库没有 `pyproject.toml`、`setup.cfg`、`tox.ini`、`.ruff.toml` 或 `mypy.ini`，因此没有独立项目 lint/type-check runner；本轮以 JSON、Bash syntax、Python compile、contract validator 与测试作为静态门禁。

### 6.3 Clean throwaway / update-reapply

- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 verify-throwaway-install.sh`：通过。
- 覆盖：public marketplace discovery、当前未发布 workflow/preset local sample、初次 preset 安装、初次 standalone wrapper probe、source/installed validation、`trellis update --force`、workflow preview/switch、preset reapply、第二次 standalone probe、recursive sidecar scan、initial 与 after-update installed closeout smoke。
- 默认 `verify-throwaway-install.sh`：按设计 exit 2，因为 feature branch 尚未 commit/push，当前 exact feature ref 不能由官方 marketplace 解析；输出明确要求 push 后以 `TRELLIS_WORKFLOW_SOURCE` 指向 exact branch ref。
- 该 exit 2 是 remote gate 的正确 fail-closed 结果，不是本地 clean throwaway 失败。

### 6.4 Version / environment

- `trellis --version`：`0.6.5`。
- `which -a trellis`：`/opt/homebrew/bin/trellis`。
- global npm：`@mindfoldhq/trellis@0.6.5`。
- npm latest 在 throwaway 输出中为 `0.6.7`；批准范围明确以 Guru Team `0.6.5` compatibility baseline 实现，本任务不升级官方 CLI 基线。

## 7. Dirty Paths

当前 task worktree dirty scope 与批准范围一致，分为：

1. Canonical/runtime/schema/tests：`trellis/guru-team-extension.json`、`trellis/skills/guru-team/**`、`trellis/workflows/guru-team/**`、`trellis/presets/guru-team/**`。
2. Dogfood installed/runtime：`.trellis/guru-team/extension.json`、`.trellis/guru-team/scripts/{bash/run-skill-command.sh,python/guru_team_trellis.py}`、`.trellis/guru-team/skills/**`。
3. Platform discovery copies：`.agents/skills/guru-create-task-commit/**`、`.codex/skills/guru-create-task-commit/**`、`.cursor/skills/guru-create-task-commit/**`、`.claude/skills/guru-create-task-commit/**`。
4. Durable docs/workflow：四份受影响 `.trellis/spec/**`、`.trellis/workflow.md`、`README.md`、三份 `docs/requirements/**`、workflow README、preset README。
5. Task-local evidence：当前 task 的 planning/context/ledger/assignment/handoff/check manifests 与本报告。

未出现 archive #122、`.trellis/workspace/**`、全局 npm、`node_modules`、secret/data、CI/CD、Docker、Compose、Kubernetes/Kustomize/Helm、DB migration 或 Makefile dirty path。

## 8. 安全与部署影响

- Security：未发现 token、secret、private key、签名 URL、`.env`、数据库 credential 或客户数据；runtime errors 使用稳定公开 remediation，不输出本机绝对路径。
- Command safety：validator id 与 runtime command 均来自 closed metadata；不接受任意 runtime path；路径逐组件 `lstat`，不存在 legacy fallback。
- Deployment：不新增/修改服务、API、worker、schedule、queue、数据库、容器、Kubernetes、CI/CD 或 Makefile；部署形态不变。

## 9. Remaining Risks / Phase 3 Requirements

1. Remote exact feature-ref marketplace verification 尚未执行，因为本轮禁止 commit/push。Reviewed content push 后必须由 finish-work remote marketplace gate 生成 immutable evidence；public marketplace sample 不能替代该证据。
2. #125 仍 stacked 于 PR #124。PR #124 合并后，#125 必须 retarget 到 `main`，重新检查 `origin/main...HEAD`，并按当时 HEAD 重新执行需要 freshness 的 Phase 2、Branch Review 与 remote marketplace gate。
3. Publish 前必须为 Issue #125 的 ledger 补齐真实 `acceptance_evidence`；#122 保持 related，不得使用 close keyword。
4. 本报告不是 Branch Review。Commit 后仍必须由独立 Branch Review agent 审查完整 base-to-HEAD committed diff。

## 10. Final Gate Judgment

Issue #125 的六项需求与全部验收口径已由 durable docs、schema、runtime、installer、generated copies、negative tests、standalone probes 与 clean throwaway/update-reapply 证据覆盖。唯一发现的公开版本矩阵漂移已修复并复验。当前无 P0/P1/P2/P3 finding 或 Phase 2 blocker，足以记录 passing `phase2-check.json`。
