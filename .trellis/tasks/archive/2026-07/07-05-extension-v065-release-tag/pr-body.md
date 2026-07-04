## 变更摘要

- 将 Guru Team Trellis extension 的 canonical manifest 版本对齐到 `0.6.5`，并记录已验证的 Trellis CLI `0.6.5`。
- 通过 preset installer 同步 dogfood installed manifest，使 `.trellis/guru-team/extension.json` 可显示当前 installed extension version `0.6.5`。
- 更新顶层 README、workflow README、preset README、需求文档和 `.trellis/spec/`，明确稳定安装使用 repo 级 `vX.Y.Z` tag，例如 `gh:castbox/guru-trellis/trellis#v0.6.5`。
- 调整 throwaway install 验证脚本默认 source 到 `#v0.6.5`，并补充测试覆盖，确保版本/tag 规则和 marketplace schema version 不混淆。

## 影响范围

- 影响 Guru Team Trellis extension 的版本可观测性、release tag 文档、workflow marketplace 安装说明、preset installer 文档和相关测试。
- `guru-team` workflow template id 保持不变，`trellis/index.json.version` 仍是 marketplace index schema version `1`，不会被当作 extension version。
- 不修改 Trellis upstream source、全局 npm package、`node_modules`、CI/CD、容器、K8s/Kustomize、数据库 migration 或 Makefile。
- 本 PR 不创建 `v0.6.5` tag；tag 必须等 PR merge 后在 merge commit 上创建，避免 tag 指向不含 `0.6.5` manifest/docs 的 commit。

## 验证结果

- `python3 -m json.tool trellis/guru-team-extension.json`：通过。
- `python3 -m json.tool .trellis/guru-team/extension.json`：通过。
- `python3 -m json.tool trellis/index.json`：通过，确认 `version` 仍为 `1`。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m py_compile` 覆盖 workflow 与 preset Python helper：通过。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：通过，83 tests OK。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-05-extension-v065-release-tag`：通过。
- `./trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `git diff --check origin/main...HEAD`：通过。
- `.trellis/guru-team/scripts/bash/version.sh --json`：通过，installed version 为 `0.6.5`。
- `.trellis/guru-team/scripts/bash/check-env.sh --json`：通过，status ok，extension version 为 `0.6.5`。
- `verify-throwaway-install.sh` 针对远程 `gh:castbox/guru-trellis/trellis#v0.6.5` 的完整验证未在 PR 阶段执行，因为远程 tag 需要等 merge 后创建。

## Review Gate

- Branch Review Gate 已由独立 `trellis-check` Agent `Beauvoir` 审查 `origin/main...HEAD` 完整 diff。
- 审查覆盖 manifest、docs、spec、task artifacts、验证脚本、测试、dogfood overlay drift、Issue Scope Ledger、部署影响和安全影响。
- 结论为通过，无 P0/P1/P2/P3 findings。
- Gate 记录的 reviewed HEAD 为 `1e498a01804684aa2cf7d5275c5b12c09d5755d9`，与发布前 HEAD 匹配。

## Issue 关闭范围

- Refs #33
- 本 PR 只引用 #33，不通过 GitHub 关闭关键字关联它，因为 #33 仍需要在 merge 后完成 annotated tag `v0.6.5` 创建、tag-pinned `trellis init` / `trellis workflow` 验证，以及确认后退休旧 `guru-team/v0.6.5` tag。
- 当前 `issue-scope-ledger.json` 中 `close_issues` 为空，#33 只作为 `related_issues` 引用。

## 安全说明

- 本次变更不引入凭据、token、private key、签名 URL、`.env` 内容、数据库 URL 或客户数据。
- 变更内容集中在版本 manifest、文档、spec、验证脚本和测试，不改变运行时权限、外部服务访问、部署配置或数据处理路径。
