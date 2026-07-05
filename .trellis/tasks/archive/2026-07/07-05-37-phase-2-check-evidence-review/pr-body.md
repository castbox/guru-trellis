## 变更摘要

- 修复 Guru Team Branch Review Gate 对 Phase 2 check evidence 的 stale 误判：提交前记录的 `phase2-check.json` 可以在提交后继续作为有效证据，只要后续提交的非 metadata 路径全部被当时的 `dirty_paths` 覆盖。
- 新增 `committed_paths_match_phase2_dirty_paths()` 与路径覆盖判断，使用 `<recorded_head>..HEAD` 审计提交后的路径，并继续阻断未被覆盖的代码、文档、配置、测试或脚本变更。
- 补齐目录 dirty path 的边界语义：`docs/` 这类以 `/` 结尾的记录可以覆盖子路径，普通前缀字符串不会误放行无关文件。
- 同步 Guru Team workflow、`trellis-continue` overlay、Codex/Claude/Cursor installed copies、README、durable requirements docs 和 `.trellis/spec/workflow/*`，避免 AI 在正常流程里用“提交后重录 Phase 2 evidence”绕过真实检查。

## 影响范围

- 影响 Guru Team workflow companion helper：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 及 dogfood 副本 `.trellis/guru-team/scripts/python/guru_team_trellis.py`。
- 影响 Branch Review Gate 的 Phase 2 post-commit audit 规则，但不降低 coverage、validation、artifact digest、P0/P1/P2 finding 或当前 working tree dirty path 的校验强度。
- 影响 `trellis-continue` 文案和平台 overlay，让 Codex、Claude、Cursor 入口都明确 Phase 2 是提交前 gate，Review Gate 只审计提交是否超出已检查范围。
- 不涉及 CI/CD、Docker、Docker Compose、Kubernetes/Kustomize、数据库 migration、Makefile 或运行时部署资产。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：71 个测试通过。
- JSON 校验、`bash -n`、`py_compile`、`task.py validate`、`git diff --check` 均通过。
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 已同步 dogfood installed copies，`check-dogfood-overlay-drift.sh` 通过。
- 临时真实 git repo dry-run 覆盖两条关键路径：已被 Phase 2 dirty path 覆盖的提交可通过 Review Gate；未覆盖的 `README.md` 提交会被 stale 校验阻断。
- 未执行完整干净 throwaway repo marketplace/preset 安装验收；本 PR 已覆盖 dogfood overlay drift 与 helper/workflow 语义一致性，完整新仓库安装验证留给发布前或后续安装验收。

## Review Gate

- 独立 Branch Review Gate 已审查 `origin/main...HEAD` 完整 diff，覆盖 helper、测试、workflow、overlay、installed copies、README、durable docs、`.trellis/spec/workflow/*` 和 task artifacts。
- Review Gate 记录的 reviewed head 为 `9095ea10437d4486c8e3a191d8100defbf7f19c7`，无 P0/P1/P2/P3 finding。
- Docs SSOT 已同步到 `docs/requirements/requirement-main.md` 与 `.trellis/spec/workflow/*`，长期流程语义不只停留在任务 artifact。

## Issue 关闭范围

- Closes #37
- 本次没有关闭其他 issue，也没有记录 related 或 follow-up issue。

## 安全说明

- 未新增 secret、token、private key、签名 URL、`.env`、数据库 URL 或客户数据输出。
- 变更集中在本仓库的 Trellis workflow helper、文档、overlay 和测试，不改变生产运行时服务、权限模型或外部系统集成。
