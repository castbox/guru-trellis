# 第 1 轮最终放行审查

## 审查轮次

- 审查轮次：1
- 审查角色：最终放行审查代理
- review_source：independent-agent
- reviewed head：`137135763fe8f6765d638af639f80bf186e02478`
- diff range：`origin/main...HEAD`
- base head：`afbecdd288101a86b04309cbe248d3c9fe976854`
- findings_count：1
- 结论：不可放行

## 问题生命周期

- F-001：P1，状态 open。本轮发现，Branch Review 只记录不修复；需要回到实现/检查阶段同步 dogfood installed helper/config 后再复审。

## 最终审查

### F-001 P1 dogfood installed `prepare-task` 仍使用旧 `codex/` 默认分支逻辑

当前提交只更新了 canonical helper `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`，但仓库已安装的 dogfood runtime helper `.trellis/guru-team/scripts/python/guru_team_trellis.py` 没有同步。active `.trellis/workflow.md` 指示日常入口运行 `.trellis/guru-team/scripts/bash/prepare-task.sh --json ...`，该 bash wrapper 会使用 `.trellis/guru-team/scripts/python/guru_team_trellis.py`，因此当前仓库的实际 dogfood `prepare-task` 仍会生成 `codex/<slug>`。

证据：

- `.trellis/workflow.md:76` 已声明缺省 `--branch` 时使用 `<branch-type>/NNN-business-capability`，合法类型为 11 个 Conventional Branch type，fallback 为 `chore`。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 已新增 `VALID_BRANCH_TYPES`、`infer_branch_type()`，并在 canonical `prepare_naming_payload()` 中拼出 `<branch-type>/<slug>`。
- `.trellis/guru-team/scripts/python/guru_team_trellis.py:34` 仍是 `branch_prefix: "codex/"`。
- `.trellis/guru-team/scripts/python/guru_team_trellis.py:654-660` 仍用 `branch_prefix` 生成 `suggested_override_flags`。
- `.trellis/guru-team/scripts/python/guru_team_trellis.py:735-743` 仍用 `branch_prefix` 拼默认 `branch_name`。
- `.trellis/guru-team/config-template.yml:26-27` 仍写着 `Prefix for feature branches` 和 `branch_prefix: "codex/"`，没有 `branch_type_default`。
- 行为探针：canonical helper 对同一输入输出 `fix/056-auto-branch-type-prefix`；dogfood installed helper 输出 `codex/056-auto-branch-type-prefix`。

影响：

- 不满足 #56 的核心验收：`prepare-task` 默认分支应为 `<branch-type>/<slug>`，且 `suggested_override_flags` 不应继续建议 `codex/...`。
- 文档和 dogfood runtime 不一致，属于当前范围 Docs SSOT / runtime copy 漂移。
- Phase 2 证据没有覆盖 `.trellis/guru-team/scripts/python/guru_team_trellis.py` 和 `.trellis/guru-team/config-template.yml` 的同步缺口。

建议修复：

- 将 canonical helper/config template 同步到 `.trellis/guru-team/` dogfood installed copy，或通过项目约定的 preset/apply 流程完成同步。
- 复核 `.trellis/guru-team/config.yml` 中 legacy `branch_prefix` 留存是否只作为兼容字段存在，确认同步后的 helper 不再使用它驱动默认分支名。
- 复跑 unit tests、`git diff --check`、Python compile、dogfood runtime 行为探针和 Phase 2 check。

## 证据

### 已检查文件

- `.trellis/tasks/07-09-056-auto-branch-type-prefix/prd.md`
- `.trellis/tasks/07-09-056-auto-branch-type-prefix/design.md`
- `.trellis/tasks/07-09-056-auto-branch-type-prefix/implement.md`
- `.trellis/tasks/07-09-056-auto-branch-type-prefix/planning-approval.json`
- `.trellis/tasks/07-09-056-auto-branch-type-prefix/phase2-check.json`
- `.trellis/tasks/07-09-056-auto-branch-type-prefix/agent-assignment.json`
- `.trellis/tasks/07-09-056-auto-branch-type-prefix/issue-scope-ledger.json`
- `.trellis/tasks/07-09-056-auto-branch-type-prefix/implement.jsonl`
- `.trellis/tasks/07-09-056-auto-branch-type-prefix/task.json`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/guides/code-reuse-thinking-guide.md`
- `.trellis/spec/guides/cross-layer-thinking-guide.md`
- `.trellis/workflow.md`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `.trellis/guru-team/config-template.yml`
- `.trellis/guru-team/config.yml`
- `README.md`
- `docs/requirements/requirement-main.md`
- `trellis/presets/guru-team/README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/workflows/guru-team/config-template.yml`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/workflows/guru-team/workflow.md`

### Workspace boundary

- expected workspace：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/056-auto-branch-type-prefix`
- actual repo root：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/056-auto-branch-type-prefix`
- source checkout：`/Users/wumengye/Documents/GoProjects/guru-trellis`
- source checkout status：空
- task worktree status：初始只有 `.trellis/tasks/07-09-056-auto-branch-type-prefix/agent-assignment.json`；本报告写入后新增 review artifacts
- suspicious source artifacts：source checkout 存在 `.trellis/guru-team/handoff.json`，但 `matches_current_task=false`

### 验证命令

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：通过，203 tests OK
- `git diff --check`：通过，无输出
- `python3 -m json.tool trellis/index.json`：通过
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh` 等价展开：通过
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：通过
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过，overlay copies match；但该命令不覆盖 `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-056-auto-branch-type-prefix`：通过
- Phase 2 stale 复核：`phase2-check.json.head` 为 ancestor `afbecdd288101a86b04309cbe248d3c9fe976854`；`origin/main...HEAD` 20 个 changed paths 均被 `phase2-check.json.dirty_paths` 覆盖，uncovered=[]

### 行为探针

- canonical helper：`prepare_naming_payload(..., "Fix prepare task branch type")` 输出 `fix/056-auto-branch-type-prefix`
- dogfood installed helper：相同输入输出 `codex/056-auto-branch-type-prefix`

### Docs SSOT judgment

- Docs SSOT Plan：`ssot_first`
- 已确认 canonical workflow、dogfood `.trellis/workflow.md`、README、workflow README、requirements、preset README、canonical config template 已改为 `<branch-type>/<slug>` 合同。
- 当前判断：未通过。dogfood installed helper/config template 仍保留旧 `codex/` 合同，且 active workflow 的实际入口会调用该 installed helper，属于当前范围 Docs SSOT / runtime inconsistency。
- `.trellis/spec/`：本轮未发现必须新增 spec 的新规则；现有 spec 已要求 workflow 变更同步 executable/runtime surfaces。

### Deployment impact

- CI/CD workflow：未改 `.github/workflows` 或 CI 配置，不需要同步。
- Docker / Compose：未改容器资产，不需要同步。
- K8s / Kustomize / Helm：未改部署清单，不需要同步。
- DB migration：未改数据库 migration/schema，不需要同步。
- Makefile：未改 Makefile，不需要同步。
- Runtime impact：有。`prepare-task` companion runtime 行为变更，且 dogfood installed runtime 未同步，见 F-001。

### Issue Scope Ledger

- `issue-scope-ledger.json` 将 #56 列为 `close_issues`，并记录实现、测试、Phase 2 evidence。
- 当前判断：F-001 修复前，证据不足以支撑关闭 #56。

## 观察项

无。

## 后续候选

无。

## 结论

findings_count=1。当前分支不可放行；需要先修复 F-001 并重新执行 Phase 2 check / Phase 3 Branch Review。
