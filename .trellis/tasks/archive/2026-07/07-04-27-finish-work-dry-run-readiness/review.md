# Branch Review Gate 独立审查报告

## 审查范围

- 任务：`.trellis/tasks/07-04-27-finish-work-dry-run-readiness`
- GitHub issue：castbox/guru-trellis#27
- 扩展范围：
  - `finish-work --dry-run --from-trellis-finish-work` 作为无副作用 readiness preview；
  - Codex 默认 dispatch mode 改为 `sub-agent`，`inline` 仅作为显式降级/调试模式；
  - preset / dogfood / overlay / README / workflow 文档一致性；
  - 测试、部署影响、安全风险、CI/CD/容器/K8s/DB migration/Makefile 影响判断。
- 本次审查不修改实现代码、不 commit、不 push、不创建 PR；只写入本 task-local `review.md`。

## Diff Range

- diff range：`origin/main...HEAD`
- merge-base：`adbf5548c6cc40c5eb193cbc65ca359344cad264`
- reviewed HEAD：`68850596ba7dcaaeebed7503378eedd3c798ef6a`
- review 前工作区状态：存在未提交 `.trellis/guru-team/handoff.json`，属于本任务 metadata/handoff 改动；本报告写入后会新增本文件。

## 审查过的关键文件与证据

- 任务 artifact：`prd.md`、`design.md`、`implement.md`、`issue-scope-ledger.json`、`phase2-check.json`。
- live issue：`gh issue view 27 --repo castbox/guru-trellis`，issue 正文已包含 dry-run 无副作用和 Codex 默认 sub-agent 的扩展范围。
- companion helper：
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - `.trellis/guru-team/scripts/python/guru_team_trellis.py`
  - 证据：canonical 与 dogfood Python helper `cmp` 一致；`cmd_finish_work()` 在 gate、dirty path、PR body/readiness 校验后、archive/journal/metadata commit/publish 之前返回 dry-run plan；dry-run 分支不调用 `cmd_publish_pr()`。
- Codex dispatch：
  - `.codex/hooks/inject-workflow-state.py`
  - `.trellis/scripts/common/workflow_phase.py`
  - `.trellis/config.yaml`
  - `.codex/agents/trellis-check.toml`
  - `.codex/agents/trellis-implement.toml`
  - 证据：缺省/非法 `codex.dispatch_mode` 走 `sub-agent`，显式 `inline` 保留；Codex sub-agent prelude 要求先读 dispatch prompt 第一行 `Active task: <path>`，否则运行 `task.py current --source`。
- preset / installer：
  - `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
  - `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
  - `trellis/presets/guru-team/README.md`
  - 证据：preset installer 会 materialize 项目级 `.trellis/config.yaml` 的 `codex.dispatch_mode: sub-agent`，保留显式 `inline`。
- workflow / docs：
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
  - `README.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
  - 证据：workflow 与 dogfood copy `cmp` 一致；文档说明 dry-run 是无副作用 readiness preview，Codex 默认 sub-agent、inline 为降级模式。
- 测试：
  - `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - `.codex/hooks/test_inject_workflow_state.py`
  - `.trellis/scripts/common/test_workflow_phase.py`
  - `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`

## 验证命令证据摘要

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py && python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py && python3 .trellis/scripts/common/test_workflow_phase.py && python3 .codex/hooks/test_inject_workflow_state.py`
  - 结果：通过，`62 + 4 + 4 + 3` tests passed。
- `python3 -m json.tool trellis/index.json && python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json && python3 -m json.tool .trellis/tasks/07-04-27-finish-work-dry-run-readiness/issue-scope-ledger.json`
  - 结果：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`
  - 结果：通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py .trellis/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .codex/hooks/inject-workflow-state.py .trellis/scripts/common/workflow_phase.py`
  - 结果：通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
  - 结果：通过，dogfood overlay copies match canonical。
- `python3 ./.trellis/scripts/task.py validate 07-04-27-finish-work-dry-run-readiness`
  - 结果：通过，`implement.jsonl` / `check.jsonl` 只有种子行但 schema 有效；本次按 fallback 读取 task artifacts 与匹配 spec。
- `git diff --check`
  - 结果：通过。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh $(mktemp -d)`
  - 结果：按设计 fail-closed，原因是当前 branch 不是 public marketplace `main`，脚本拒绝用 public marketplace 冒充当前分支验证；未覆盖完整 throwaway install。

## Findings 分级

### P0 / P1 / P2

未发现 P0/P1/P2 阻塞 finding。

### P3

1. P3 - 当前分支完整 throwaway install 未实际执行。
   - 证据：`verify-throwaway-install.sh` 返回 `throwaway install would sample the public marketplace, not the current branch workflow source`。
   - 判断：脚本 fail-closed 符合本仓库开箱即用门禁要求，避免把 public `main` 验证误当作当前分支验证；但当前 branch 的新仓库安装仍未被完整实跑覆盖。
   - 影响：非阻塞；最终发布说明应明确该项未覆盖，或在 branch 可作为 marketplace source 后补跑。

2. P3 - dry-run 无副作用主要由 mock/unit test 覆盖，未发现完整真实 task fixture 的端到端 dry-run 证据。
   - 证据：`test_finish_work_dry_run_returns_plan_without_archive_journal_commit_or_publish` 断言未调用 archive、journal、metadata commit、publish，并验证 plan payload；`phase2-check.json` 声称临时 repo fixture 已验证，但 branch diff 中未包含该 fixture 脚本或可复跑 artifact。
   - 判断：实现代码路径清晰，targeted unit test 足以覆盖主要副作用调用点；真实 fixture 可提升回归信心但不是当前 gate 的阻塞条件。
   - 影响：非阻塞；建议后续把真实 fixture dry-run 无副作用验证沉淀成可复跑测试或脚本。

## 一致性与风险判断

- 需求/设计/实现一致性：通过。实现与 issue #27、`prd.md`、`design.md` 的核心语义一致：finish-work dry-run 在副作用前返回 readiness plan；正式 finish-work 路径保持 archive/journal/metadata commit/publish 链路。
- dry-run 无副作用：通过。代码分支位于副作用调用前；测试断言 `task.py archive`、`add_session.py`、`commit_if_metadata_dirty`、`cmd_publish_pr` 均未被 dry-run 调用。
- review gate 前置语义：通过。workflow/docs 仍要求 Branch Review Gate 先于 finish-work，`finish-work --dry-run` 只做 readiness preview，不替代 review 判断。
- Codex dispatch 默认值：通过。hook、phase parser、dogfood `.trellis/config.yaml`、README/workflow 文案均改为默认 `sub-agent`，显式 `inline` 保留为降级。
- preset/dogfood/overlay 同步：通过。`check-dogfood-overlay-drift.sh` 通过；workflow 与 dogfood copy、canonical helper 与 dogfood helper 内容一致。
- README/workflow 文档一致性：通过。top-level README、workflow README、preset README、canonical workflow 与 dogfood workflow 均描述了 dry-run preview 和 Codex dispatch 语义。
- 测试覆盖：通过，有针对 dry-run 副作用、Codex hook banner、workflow phase dispatch、preset config materialization 的测试。
- 部署/CI/CD/容器/K8s/DB migration/Makefile 影响：通过。本 diff 未修改 `.github`、Docker/Compose、Kubernetes/Kustomize/Helm、DB migration、Makefile 或应用运行服务；变更集中在 Trellis workflow/preset/helper/docs/tests，无需部署资产同步。
- 安全风险：通过。未发现 token、secret、private key、签名 URL、`.env`、数据库 URL 或敏感客户数据写入 diff、task artifact、文档或测试。
- `.trellis/spec/` 同步：可接受。本次改变属于 workflow/preset 既有规则的具体实现；现有 spec 已覆盖 dry-run、companion script、preset installer、Branch Review Gate、Codex dispatch 边界，未发现必须新增 spec 的长期规则缺口。

## 结论

无 P0/P1/P2 阻塞 finding。当前分支可通过 Branch Review Gate。

通过条件说明：本报告仅代表独立 Agent review 结论；后续仍需由 main session 用 `review-branch.sh --review-source independent-agent --review-report .trellis/tasks/07-04-27-finish-work-dry-run-readiness/review.md` 记录 gate artifact，并在 finish/publish 前明确完整 throwaway install 未覆盖当前分支 marketplace 的风险。
