# #56 Branch Review 汇总

## 审查轮次

- 第 1 轮：最终放行审查代理，raw report：[round-1-final-review.md](reviews/round-1-final-review.md)
  - reviewed head：`137135763fe8f6765d638af639f80bf186e02478`
  - diff range：`origin/main...HEAD`
  - findings_count：1
  - 结论：不可放行
- 第 2 轮：问题闭环审查代理，raw report：[round-2-f001-closure.md](reviews/round-2-f001-closure.md)
  - reviewed head：`65d053a7592dd6bfc6c5407c2c20acf8ece853a5`
  - diff range：`origin/main...HEAD`
  - findings_count：0
  - 结论：F-001 已闭环
- 第 3 轮：最终放行审查代理，raw report：[round-3-final-pass.md](reviews/round-3-final-pass.md)
  - reviewed head：`65d053a7592dd6bfc6c5407c2c20acf8ece853a5`
  - diff range：`origin/main...HEAD`
  - findings_count：0
  - 结论：可放行

## 问题生命周期

- F-001：P1，closed。第 1 轮发现 dogfood installed `prepare-task` helper/config 未同步，active runtime 仍会输出旧 `codex/<slug>`；第 2 轮由同一 finding owner 复核 canonical/dogfood helper parity、config template parity、`.trellis/guru-team/config.yml` legacy/fallback、active wrapper 调用 installed helper 和 behavior probe，确认已闭环。
- 第 3 轮 fresh final review 未发现新的 P0/P1/P2/P3 finding。

## 最终审查

可放行。当前完整 `origin/main...HEAD` diff 满足 issue #56：`prepare-task` 缺省分支名改为 `<branch-type>/<slug>`，11 个合法类型均有确定性映射，unknown fallback 为 `chore`，显式 `--branch` 保持覆盖，legacy `branch_prefix` 不再驱动默认分支，`suggested_override_flags` 不再建议 `codex/`。

F-001 修复后，canonical helper 与 dogfood installed helper 逐字节一致，canonical config template 与 dogfood config template 逐字节一致；`.trellis/guru-team/config.yml` 保留 legacy `branch_prefix` 兼容字段但默认空值，并新增 `branch_type_default: chore`；active `.trellis/guru-team/scripts/bash/prepare-task.sh` 调用 installed helper。

## 证据

- reviewed head：`65d053a7592dd6bfc6c5407c2c20acf8ece853a5`
- diff range：`origin/main...HEAD`
- findings_count：0
- validation：`python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过，203 tests OK；`git diff --check` 通过；`git diff --check origin/main...HEAD` 通过；Python compile、bash syntax、JSON 结构检查通过；canonical/dogfood `cmp` 通过；独立 behavior probe 覆盖 11 类型、unknown -> `chore`、显式 `--branch`、legacy `branch_prefix` 与 `suggested_override_flags`。
- deployment impact：未涉及 CI/CD、Docker/Compose、K8s/Kustomize/Helm、DB migration、Makefile；涉及 Guru Team `prepare-task` companion runtime 行为，canonical/dogfood runtime 与配置已同步。
- Docs SSOT judgment：`ssot_first` 已执行；canonical workflow、dogfood workflow、README、workflow README、preset README、requirements、canonical/dogfood config、代码和测试一致；`.trellis/spec/` 未发现 stale `codex/` 合同，本轮不需要更新。
- Phase 2 evidence：F-001 re-check 的 `phase2-check.json.dirty_paths` 覆盖 `.trellis/guru-team/config-template.yml`、`.trellis/guru-team/config.yml`、`.trellis/guru-team/scripts/python/guru_team_trellis.py` 和 review evidence；当前 metadata tail 仅为 review / agent-assignment 类 evidence。
- Issue Scope Ledger：`close_issues` 只包含 #56，acceptance evidence 足以支撑关闭 #56。

## 观察项

- O-001：当前 HEAD 的公开 `gh:...#ref` throwaway install 未验证，原因是分支未推送且本轮按要求不 push；未将已发布 stable tag 验证冒充为当前分支验证。

## 后续候选

- 发布前候选：分支 push 后或 release tag 前，用指向当前 ref 的 `TRELLIS_WORKFLOW_SOURCE` 补跑 `verify-throwaway-install.sh`，作为 release readiness / PR evidence。

## 结论

findings_count=0。F-001 已闭环，第 3 轮 fresh final Branch Review 未发现 P0/P1/P2/P3 finding；当前分支可放行，`issue-scope-ledger.json` 足以支撑 #56 close scope。
