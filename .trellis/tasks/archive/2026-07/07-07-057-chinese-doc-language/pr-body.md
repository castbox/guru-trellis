## 变更摘要

- 将 Guru Team workflow 的业务项目文档语言规则调整为默认中文，覆盖 `.trellis/spec/**`、`.trellis/tasks/**`、`docs/**`、`00-bootstrap-guidelines` docs SSOT 文档，以及 workflow 运行 artifact 中面向人类阅读的摘要、证据、finding、review 结论字段。
- 保留 literal token、命令、路径、schema key、API name、错误码、外部系统字段和引用原文可使用英文的边界，并明确 `guru-trellis` 源码仓库自身可按公共 Trellis marketplace / preset / script 语境保留英文。
- 更新 canonical workflow、preset README、workflow README、README、docs requirement、`.trellis/spec`、dogfood workflow 和各平台 overlay，使 Codex、Claude、Cursor 入口的语言规则一致。
- 在 preset installer 中加入确定性的 `language_guidance` 迁移逻辑，替换 `.trellis/spec/**/*.md`、workspace index 和 `.trellis/tasks/00-bootstrap-guidelines/**/*.md` 中已知 Trellis 英文文档语言规则，不扫描普通历史 task 或业务 `docs/**`。

## 影响范围

- 影响 Guru Team Trellis workflow、preset installer、overlay、dogfood 安装副本、公开 README / requirement 文档、`.trellis/spec` 约定和 installer 单测。
- 不修改 Trellis 上游源码、全局 npm 包、`node_modules`、hook 分支逻辑或业务项目私有 PRD。
- 不涉及 CI/CD workflow、Docker / Compose、Kubernetes / Helm / Kustomize、数据库 migration、Makefile、运行时配置、服务、worker 或生产部署资产。

## 验证结果

- `python3 -m json.tool trellis/index.json`
- `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`，23 个测试通过
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-07-057-chinese-doc-language`
- `git diff --check`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- `rg` 检查 overlay、dogfood 副本、README、workflow / preset docs、`.trellis/spec`、workspace 和 bootstrap task 范围，未发现旧英文文档语言规则残留。
- 开箱验证已覆盖 stable workflow source sample + 当前本地 preset；PR 发布后追加运行 `TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#codex/057-chinese-doc-language trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`，current-branch marketplace throwaway install 通过。

## Review Gate

- Branch Review Gate 已通过，reviewed head 为 `c19b9e2af89399f2b7fbd8f0f0ef26bc44b83dc8`，diff range 为 `origin/main...HEAD`。
- 独立最终审查代理 `019f3c3f-497f-7780-a8c4-12a9eb1e7c7a` / `Closure Agent` 审查了 issue #57、完整 diff、task artifacts、workflow / preset / overlay / dogfood / docs / spec / installer / test 触点，P0/P1/P2/P3 findings 均为 0。
- Gate 记录包含 review report digest、agent assignment digest、issue scope、验证证据、部署影响判断，以及 gate 执行时 current-branch marketplace 尚未验证的 observation；该 observation 已由 PR 发布后的追加 throwaway install 验证补齐。

## Issue 关闭范围

Closes #57

本 PR 只关闭 #57：统一业务项目 Trellis 文档语言默认为中文，并同步 workflow、preset installer、overlay、dogfood 副本、文档和验证规则。没有声明关闭 related issue 或 follow-up issue。

## 安全说明

- 本次变更不接触 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或业务原始记录。
- PR body、review evidence 和 task artifact 未记录敏感凭据；变更内容限于 Trellis workflow / preset / overlay / docs / spec / deterministic installer 逻辑和测试。
