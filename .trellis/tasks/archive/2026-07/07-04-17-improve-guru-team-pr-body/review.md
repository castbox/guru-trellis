# Branch Review Gate 审查报告

## 结论

通过。已按 `origin/main...HEAD` 审查当前分支 `codex/17-improve-guru-team-pr-body`，Reviewed HEAD 为 `803841d4553ffb3fae8556f6c04149706f49c10f`。未发现 P0/P1/P2/P3 finding。

## 审查范围

- Diff 范围：`origin/main...HEAD`
- Merge base：`7a1b006cba4617eb868cd24d3c97fa0896fe49b4`
- 变更文件数：28
- 覆盖文件类型：canonical workflow、dogfood workflow、finish-work overlay、installed dogfood copies、publish helper Python、单元测试、README、preset/workflow README、`.trellis/spec/workflow/*`、task planning artifacts。
- 明确未变更：`.github/workflows/*`、Dockerfile、Docker Compose、Kubernetes/Kustomize/Helm、数据库 migration/seed/backfill、Makefile。

## Findings

无 P0/P1/P2/P3 finding。

## 审查要点

- `publish-pr` 新增 `--body-file` / `--body-artifact` 输入，并在发布前统一校验必填 section、低信息量短语、generated fallback 占位、close/ref issue 语义。脚本只做客观结构和语义校验，不替代 AI readiness 判断。
- 已修正并审查 `--body-file` 优先级：同时提供 body file 和 artifact 时，显式 body file 胜出，符合 README、workflow 与 task design 中“优先使用 reviewed body file”的合同。
- 已修正并审查 generated fallback fail-closed：缺少具体 publish validation、未记录 changed_files 或要求 AI 补充 body file 的 fallback 占位短语会阻塞 non-draft publish，不会伪装成可发布正文。
- fallback body 不再输出“当前 Trellis task / 已提交实现与文档更新”作为摘要；`变更摘要`、`影响范围`、`验证结果`、`Review Gate`、`Issue 关闭范围`、`安全说明` 均进入结构校验。
- Issue Scope Ledger close/ref 语义保持 task-level ledger 为准：close keyword 只能用于 `close_issues`，related/followup 使用 close keyword 会阻塞。
- canonical workflow 与 dogfood `.trellis/workflow.md` 同步了 PR body readiness 规则；finish-work overlays 与 installed dogfood copies 文案一致。
- README、workflow README、preset README 与 `.trellis/spec/workflow/` 已补长期 SSOT，不新增 `docs/` 目录；本仓库长期文档仍由这些既有文件承载。

## 验证

- `python3 -m json.tool trellis/index.json` 通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh` 通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py` 通过。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过，25 tests OK。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-17-improve-guru-team-pr-body` 通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.7` 通过，输出包含新的 PR body readiness 合同。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 通过，dogfood overlay copies match canonical Guru Team overlays。
- `./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` 通过，验证 throwaway 新仓库安装 Guru Team workflow/preset、入口阻塞和 helper 可用性。
- `git diff --check` 通过。
- 官方 Trellis 文档连通性已用 `curl -k -L` 复核 `https://docs.trytrellis.app/advanced/custom-workflow` 与 `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace` 可读取；本任务仍使用 workflow/preset/overlay Markdown 与 companion script 的官方扩展边界。

## Docs SSOT Reconciliation

本任务改变 Guru Team workflow / publish helper 的长期发布合同，已更新长期 SSOT：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/quality-guidelines.md`、`.trellis/spec/workflow/companion-scripts.md`。Task artifact 中的执行细节保留为任务历史。本仓库没有独立 `docs/` durable docs 目录，本任务无需新增 `docs/`。

## 部署影响

本次 diff 只修改 Guru Team workflow/preset/overlay 文档、publish helper 脚本、测试和 Trellis task artifact，不新增 API、CLI 用户入口、后台 worker、runtime config、容器启动、K8s/Kustomize、数据库 migration 或 Makefile。无需同步修改 CI/CD、Docker/Compose、Kubernetes/Kustomize、数据库 migration 或 Makefile。安全审查未发现 token、secret、签名 URL、`.env` 内容或数据库 URL 写入。

## Issue Scope

- Close issue：#17 `Improve Guru Team PR body quality standards`
- Related issues：无
- Follow-up issues：无

Branch Review Gate 覆盖 #17 的验收范围：workflow / finish-work skill 明确 PR body 面向 GitHub reviewer；`publish-pr` 支持 reviewed body file/artifact；低信息量 body 与 generated fallback 占位被阻塞；README / workflow README / preset README / spec 已记录标准；测试和 dry-run 证据覆盖成功与失败路径。
