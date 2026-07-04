# Branch Review Gate Review：#7 PR readiness source 门禁

## 审查结论

- 结论：通过。
- Findings：无 P0/P1/P2/P3。
- Reviewed HEAD：`d5c333e160817857d1bc202668cafa110a6d9823`
- Base：`origin/main` at `2e9f775a224bfb17f2904f6ba2dec2e7fb569553`
- Diff range：`origin/main...HEAD`
- 审查时间：2026-07-04 14:08 CST

## 审查范围

- 检查了 `origin/main...HEAD` 完整 diff，共 28 个文件，1 个提交：`d5c333e fix(trellis): require reviewed PR body source`。
- 覆盖 canonical runtime：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、`test_guru_team_trellis.py`、`workflow.md`、workflow README。
- 覆盖 preset / overlay：`trellis/presets/guru-team/README.md` 和 `.agents/.codex/.claude/.cursor` finish-work overlays。
- 覆盖 dogfood copies：`.trellis/workflow.md`、`.trellis/guru-team/scripts/python/guru_team_trellis.py`、平台 finish-work 入口。
- 覆盖 task artifacts 与 Issue Scope Ledger：`prd.md`、`design.md`、`implement.md`、`issue-scope-ledger.json`、`implement.jsonl`、`check.jsonl`。
- 覆盖 durable docs / specs：`README.md`、`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/companion-scripts.md`。

## 关键判断

- non-draft `publish-pr` 现在要求 `body-file:*` 或 `body-artifact:*`，`generated` 只能用于 draft/preview；真实 publish 在 `gh auth`、`git push`、`gh pr create` 前阻塞缺少 reviewed source 的请求。
- `finish-work` 在 archive/journal/publish 副作用前做 readiness preflight，缺少 reviewed source 时阻塞；archive 后会把 active task 下的 `body_file` / `body_artifact` 参数重写到 archived task path。
- `--body-artifact` 要求 `ready: true`，并要求非空 `body` 或 `body_file`；相对 `body_file` 以 artifact 所在目录解析。
- `publish-pr --dry-run` payload 包含 `reviewed_source_required`、`reviewed_source_ok` 和 `reviewed_source_errors`，可以让 AI 在真实发布前看到 non-draft source 门禁状态。
- 脚本只做客观校验和执行，不替代 AI 对 PR body 是否真实充分的判断；workflow、README、spec 与 finish-work overlays 已同步该边界。

## 验证记录

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：通过，32 个测试。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m json.tool trellis/index.json` 与 `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-7-require-pr-readiness-review-before`：通过，`implement.jsonl` / `check.jsonl` 各 5 条。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过，dogfood overlay copies match canonical。
- `git diff --check origin/main...HEAD`：通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase`、`--step 3.5`、`--step 3.7`：通过。

## Docs SSOT 与发布影响

- Durable docs 已更新：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- Workflow/spec 已更新：`trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md`、`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/companion-scripts.md`。
- 本次变更修改 companion script、workflow、preset overlays 和 task artifacts；未修改 `.github/workflows/*`、Dockerfile、Docker Compose、Kubernetes/Kustomize、数据库 migration、Makefile 或 runtime config。
- 部署影响判断：不新增服务、CLI 顶层入口、后台 worker、队列、migration 或 runtime 配置；不需要同步 CI/CD、容器、K8s/Kustomize、数据库或 Makefile 资产。
- 安全判断：未引入 secret、token、private key、数据库 URL、签名 URL 或 `.env` 输出；PR body/readiness artifact 规则明确禁止依赖低信息量或不可审计来源。

## Issue Scope Ledger 覆盖

- `close_issues`：#7。
- `related_issues`：无。
- `followup_issues`：无。
- #7 的 acceptance evidence 已覆盖：non-draft publish reviewed source 门禁、finish-work archive 前 preflight、archive 后 artifact SSOT、`ready: true` artifact 校验、相对 `body_file` 解析、dry-run source 状态输出、测试和文档/overlay 同步。

## Findings

无 P0/P1/P2/P3 findings。
