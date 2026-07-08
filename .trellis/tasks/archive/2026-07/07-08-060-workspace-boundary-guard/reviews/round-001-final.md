# 第 001 轮最终放行审查报告

## 基本信息

- 审查角色：最终放行审查代理
- task：`.trellis/tasks/07-08-060-workspace-boundary-guard`
- reviewed_head：`1e2e78ae1259165c61a5dfdb4826abd6edc730a5`
- diff 范围：`origin/main...HEAD`
- close issue：#60
- follow-up issue：#76，不关闭
- raw report：`.trellis/tasks/07-08-060-workspace-boundary-guard/reviews/round-001-final.md`

## 启动边界验证

- `pwd`：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/060-workspace-boundary-guard`
- `git rev-parse --show-toplevel`：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/060-workspace-boundary-guard`
- `git rev-parse HEAD`：`1e2e78ae1259165c61a5dfdb4826abd6edc730a5`
- `check-workspace-boundary.sh --json --task .trellis/tasks/07-08-060-workspace-boundary-guard`：`status=ok`；`expected_workspace` 与 `actual_repo_root` 均为 task worktree；`source_checkout_status=[]`；`task_worktree_status` 只包含 `.trellis/guru-team/handoff.json` 与当前 task artifact 目录。
- source checkout `git status --short --branch`：`## main...origin/main`，无工作区改动。
- boundary snapshot 记录了 source checkout 中存在 `.trellis/guru-team/handoff.json`，但 `matches_current_task=false`；本轮作为观察项记录，不构成当前 task artifact 误写。

## 已检查范围

- task artifacts：`prd.md`、`design.md`、`implement.md`、`check.jsonl`、`planning-approval.json`、`phase2-check.json`、`phase2-findings.json`、`agent-assignment.json`、`issue-scope-ledger.json`
- companion scripts：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、`.trellis/guru-team/scripts/python/guru_team_trellis.py`、新增 `check-workspace-boundary.sh` wrapper
- tests：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`、`trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- preset installer / manifest：`apply_guru_team_trellis_preset.py`、`trellis/guru-team-extension.json`、`.trellis/guru-team/extension.json`、`trellis/presets/guru-team/README.md`
- workflow / overlays / dogfood copies：`trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md`、`.agents/**`、`.codex/**`、`.cursor/**`、`.claude/**`、`.trellis/agents/**`
- docs / specs：`README.md`、`trellis/workflows/guru-team/README.md`、`docs/requirements/**`、`.trellis/spec/workflow/**`
- deployment/CI/container/K8s/DB/Makefile：本 diff 未修改 `.github/workflows`、Docker/Compose、Kubernetes/Helm/Kustomize、DB migration、Makefile 或运行时部署资产。
- 官方 Trellis 对齐：复核 custom workflow 与 custom spec template marketplace 文档，当前方案仍把流程判断放在 Markdown workflow / overlay 中，把脚本限制为 deterministic fact collector / validator。

## Phase 2 Evidence 复核

- `phase2-check.json.head` 是提交前 `a27b82c31db74be502d9a65807a200c1c0fc88eb`，当前 `HEAD` 是其后续提交。
- 手动比对 `git diff --name-only a27b82c31db74be502d9a65807a200c1c0fc88eb..HEAD` 与 `phase2-check.json.dirty_paths`：提交后的非 metadata 文件全部被 `dirty_paths` 覆盖。
- 当前工作区只剩 `.trellis/guru-team/handoff.json` 与当前 task-local artifacts；没有非 metadata dirty path。
- Phase 2 记录了 1 个 P1 finding 已由阶段二检查代理修复，并补充回归测试；当前没有 Phase 2 开放 finding。
- `verify-throwaway-install.sh` 在 Phase 2 中未完全通过，原因是已发布 tag 旧 workflow 文案与当前分支 marketplace source 不可直接验证；本轮保留为 residual risk，未声称开箱即用验证已完全通过。

## 验证命令

- `git diff --stat origin/main...HEAD`：53 files changed, 1314 insertions, 115 deletions
- `git diff --check origin/main...HEAD`：通过
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过，dogfood overlay copies match canonical Guru Team overlays
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：通过，158 tests
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：通过，27 tests
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`：通过
- `python3 -m json.tool trellis/index.json`、`trellis/guru-team-extension.json`、`.trellis/guru-team/extension.json`：通过
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-08-060-workspace-boundary-guard`：通过
- `find . -name '*.bak' -o -name '*.new'`：无输出

## 发现的问题

### P2：新增 extension public API 但未更新已发布版本号，破坏 release / upgrade 可观测性

- 文件：`trellis/guru-team-extension.json:5`、`trellis/guru-team-extension.json:42`
- 问题：当前分支新增 `check-workspace-boundary` companion script，并把 `record-agent-assignment` / `check-agent-assignment` 补入 `public_api.companion_scripts`，但 `version` 仍是 `0.6.5-guru.1`。
- 证据：
  - `trellis/guru-team-extension.json:5` 仍为 `"version": "0.6.5-guru.1"`。
  - `trellis/guru-team-extension.json:42-56` 的 public API 已包含 `check-workspace-boundary`、`record-agent-assignment`、`check-agent-assignment`。
  - `origin/main:trellis/guru-team-extension.json` 同版本 `0.6.5-guru.1` 的 public API 只有旧脚本集合，不包含这些新增项。
  - `git show-ref --tags -d | rg 'v0.6.5-guru.1'` 显示本地已有 tag `v0.6.5-guru.1`，并解析到 commit `662bc4730999f81efd0b815ce5a9310ba2032e4c`；`git ls-remote --tags origin 'v0.6.5-guru.1'` 也显示远端 tag 已存在。
  - `.trellis/spec/workflow/data-contracts.md:48-62` 要求 release tag 与 `trellis/guru-team-extension.json.version` 对应，并在 merge 后创建对应 annotated tag 再验证 tag-pinned marketplace install / workflow。
- 影响：安装或升级后的 `.trellis/guru-team/extension.json` / `version.sh --json` 会把包含 workspace boundary guard 的新扩展报告成旧稳定版本 `0.6.5-guru.1`。由于该 tag 已发布，后续不能用同一 tag 唯一标识当前 public API；用户无法从 version/provenance 判断目标 repo 是否真的安装了 #60 guard，upgrade/update gate 也无法形成可复现的稳定证据。
- 建议：在同一变更中把 Guru Team extension revision 升级为新的唯一版本，例如 `0.6.5-guru.2`，同步更新 `.trellis/guru-team/extension.json`、README / workflow README / preset README 中的 stable tag 示例和 release note 口径；或明确把当前分支标记为 canary 且不宣称稳定 release，但这需要调整 public docs 和发布计划。修复后重新运行 dogfood apply / drift check / installed manifest 验证。

## 观察项

- workspace boundary core path 本身未发现代码级 blocker：wrong cwd、缺失 handoff、source checkout 同名 task artifact、错误 `--review-report` / `--agent-assignment` / `--review-round-report` / `--checked-artifact` 路径均有回归测试覆盖。
- `check-workspace-boundary` 当前启动快照显示 source checkout 有非当前 task 的 historical handoff；source checkout git status clean，未构成本轮误写，但后续维护时应避免把该 artifact 误读为当前 task evidence。
- `issue-scope-ledger.json` 已把 #60 放入 `close_issues`，把 #76 放入 `followup_issues`；#76 未被关闭。#60 的 `acceptance_evidence` 仍为空，finish/publish 前需要补充本次 review/gate 可引用的验收证据。
- Phase 2 已明确 throwaway install 未完全通过；最终发布说明不能声称完整开箱即用验证通过。

## 后续候选

- #76 heartbeat / workspace-aware liveness 策略继续作为后续能力；本任务只建立 workspace boundary fact layer。
- 后续可以为 `--allow-source-clean` 增加显式集成测试，确保它只用于 clean source checkout fact probe，且不会放行 source checkout task artifacts。

## 结论

本轮审查发现 1 个 P2 finding。Branch Review Gate 不应放行，直到 extension version / stable tag / public docs 发布口径与新增 public API 收敛并重新验证。除该发布版本合同问题外，#60 的 workspace boundary 代码路径、overlay 同步、测试覆盖、Docs SSOT 和 #76 follow-up 分类未发现新的阻塞缺陷。
