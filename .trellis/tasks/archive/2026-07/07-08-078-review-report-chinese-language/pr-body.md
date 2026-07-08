## 变更摘要

- 将 Branch Review 每轮 `reviews/*.md` raw report 和最终 `review.md` rollup 明确列为中文 human-readable task artifacts，补齐标题、字段名、证据、发现、观察项、后续候选、部署 / 安全判断和结论的中文默认规则。
- 同步 canonical workflow、dogfood workflow、preset overlays、Codex / Claude / Cursor / `.agents` / `.trellis/agents` installed copies，确保后续生成链路不会只修当前 task artifact。
- 在 Guru Team companion validator 中新增固定英文模板标题拦截，防止 `Review Rounds`、`Findings Lifecycle`、`Evidence Handoff`、`Deployment / safety impact`、`Follow-up Candidates` 等模板痕迹进入 `review.md` 或 `reviews/*.md`。
- 更新 `.trellis/spec/**` 与 `docs/requirements/**` durable docs，记录 Branch Review review artifact 的中文规则和 validator 边界。

## 影响范围

- 影响 Guru Team workflow 的 Branch Review 生成与 gate 校验路径，包括 `trellis/workflows/guru-team/workflow.md`、preset overlay 入口、dogfood installed copies、`guru_team_trellis.py` 与对应测试。
- 不改变 #70 raw report retention / digest / archive migration 数据模型；脚本只做 path、digest、role、链接和固定模板标题这类客观校验，不替代 AI reviewer 的审查判断。
- 无 CI/CD、Docker、Kubernetes/Kustomize/Helm、数据库 migration、Makefile、依赖或运行时配置变更。

## 验证结果

- `python3 -m json.tool trellis/index.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：152 tests passed
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-08-078-review-report-chinese-language`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `git diff --check`
- `find . -name '*.bak' -o -name '*.new'`：无未处理冲突文件

完整 throwaway install 未运行，因此本 PR 不声明新仓库开箱即用全链路已实测；当前已覆盖 marketplace index JSON、dogfood overlay drift、installed copy 同步和主要脚本/测试验证。

## Review Gate

- Branch Review Gate 已通过，reviewed HEAD：`f6b09f3d2257e9e53c7e59fb8d6d322b36773127`。
- 独立最终放行审查代理 `019f40a5-66e0-76c3-bb6b-4dacb2640f2a` 覆盖 `origin/main...HEAD` 完整 diff，`findings_count=0`。
- Gate observation：完整 throwaway install 未运行，不能声称已完成新仓库安装全链路实测。

## Issue 关闭范围

Closes #78

无 related issue 或 follow-up issue。

## 安全说明

本次变更未写入 token、secret、private key、签名 URL、`.env`、数据库 URL 或敏感原始数据。部署资产未变更，不需要同步 CI/CD、容器、K8s/Kustomize、数据库 migration 或 Makefile。
