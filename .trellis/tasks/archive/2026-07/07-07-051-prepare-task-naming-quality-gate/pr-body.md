## 变更摘要

本次修正 Guru Team `prepare-task` 的 slug / branch / worktree / task 命名门禁，避免在中文 issue 或语义不足标题上静默创建 `issue-52`、`52-issue-52` 这类低信息名称。

- `prepare-task --json` 输出新增 `naming_quality`，包含 `ok`、`reason`、`requires_semantic_name`、`current_slug`、`suggested_override_flags`，并在 handoff schema / handoff payload 中保留。
- 保留英文标题的确定性自动 slug，但新增质量判定，识别 `issue-<n>`、`<n>-issue-<n>`、纯编号、仅通用词、过短或业务 token 不足的名称。
- 中文或非 ASCII issue title 不做拼音 / transliteration；只读 planner 可以输出计划，但标记需要 agent 显式提供语义英文 short-name。
- `--create-worktree` / `--create-task` 在任何 worktree、branch、task 副作用前阻断低信息命名，并提示使用 `--short-name`、`--workspace-slug`、`--task-slug`、`--branch` 覆盖。
- 同步 canonical workflow、dogfood 副本、schema、README / workflow README / preset README、overlay 和 durable requirements 文档。

## 影响范围

影响范围限于 Guru Team Trellis 扩展：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 及 dogfood 安装副本；
- `intake-handoff.schema.json` canonical / dogfood schema；
- `trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md`、README、workflow README、preset README；
- `trellis/presets/guru-team/overlays/` 中的 `trellis-start` 入口文案；
- `docs/requirements/` durable requirements 总览；
- `test_guru_team_trellis.py` 回归测试。

未修改 Trellis 上游源码、全局 npm 包、`node_modules`、CI/CD、Docker、Kubernetes、数据库 migration 或 Makefile。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：123 tests OK。
- `python3 -m py_compile ...`：通过。
- `python3 -m json.tool ...`：canonical / dogfood schema、handoff、task metadata 校验通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-07-051-prepare-task-naming-quality-gate`：通过。
- `git diff --check`：通过。
- CLI probes：planner 对低信息 / 中文语义不足命名标记 `naming_quality.ok=false`；create 路径对低信息命名 exit 2；显式语义覆盖生成预期 slug / branch。
- local preset smoke：当前 checkout 的 preset installer 可安装 `.trellis/guru-team/`、Codex / shared overlays、schema 与可执行脚本。
- 未声称 current HEAD 的远端 marketplace install 已验证；该分支在 publish 前尚未存在于远端，无法用 `gh:...#<branch>` 验证远端 marketplace 源。

## Review Gate

Branch Review Gate 已通过，审查范围为 `origin/main...HEAD`，reviewed HEAD 为 `4981f15082c8c7ca4a7425253bc9c5949ac1c68c`。

审查过程包括一轮 P3 Docs SSOT finding：`docs/requirements/` 未同步 #51 命名质量门禁。该问题已由 `4981f15` 修复，并由原问题发现代理闭环为 0 findings；随后 fresh 最终放行审查代理完整复审当前 HEAD，P0 / P1 / P2 / P3 findings 均为 0。

## Issue 关闭范围

Closes #51

本 PR 完整解决 #51：`prepare-task` 不再静默创建低信息 slug / branch / worktree / task 名称；中文或非 ASCII 标题必须由 agent 显式传入语义英文 short-name；低信息显式覆盖在 create 路径同样被阻断。

无 related issues，暂无 follow-up issues。

## 安全说明

本次未涉及 token、secret、`.env`、签名 URL、客户数据或 provider 原始响应。新增逻辑只在本地 deterministic companion script 中做命名质量校验，并在 create 路径副作用前 fail closed，降低错误 worktree / branch / task 名称进入长期 Git / Trellis 历史的风险。

部署影响：无需部署资产更新；未改 CI/CD、容器、K8s / Kustomize / Helm、数据库 migration 或 Makefile。
