# 实施计划

## 约束核对

- 官方 Trellis 扩展面：使用 workflow Markdown、preset overlay、companion script；不改上游源码或 `node_modules`。
- 中台知识门禁：不适用。
- Docs SSOT：本仓库没有 `docs/` 目录；需更新 README / workflow README / preset README / canonical workflow。
- Codex inline 模式：本轮不派发 implement/check sub-agent，主会话直接实现和检查。

## 执行步骤

1. **现状搜索**
   - 搜索 `review-branch`、`Branch Review Gate`、`finish-work`、`reviewer` 的所有引用。
   - 确认 canonical 与 dogfood copy 的同步边界。
2. **脚本合同**
   - 在 canonical Python companion 增加 `--review-report`、report digest、pass gate reviewer/report 校验。
   - 同步 dogfood installed Python companion。
   - 更新 CLI help 和 artifact notes。
3. **Workflow 与 overlay**
   - 更新 canonical `.trellis/workflow.md` copy。
   - 更新 preset overlays 与 dogfood `.agents` / `.codex` copies。
   - 确认 Claude / Cursor entrypoint 不残留旧示例。
4. **README / spec**
   - 更新 public README、workflow README、preset README。
   - 如形成可复用规则，更新 `.trellis/spec/workflow/*`。
5. **验证**
   - 运行规范中的静态命令。
   - 运行 `review-branch` dry-run 缺失 reviewer/report 的失败用例。
   - 运行有 reviewer / review report 的成功用例。
   - 运行 installer 到临时 repo 的最小验证。
6. **提交与 Branch Review Gate**
   - 提交前记录 Docs SSOT reconciliation 和验证结果。
   - 提交后先执行真实 AI review prompt，形成 review report，再调用 `review-branch.sh` 写 artifact。

## 回滚点

- 如果 report digest / path 校验影响旧 artifact 解析，保留新增字段但只在 passed gate 校验阶段强制。
- 如果 overlay 大量重复导致漂移，缩短 overlay 文案并指向 `.trellis/workflow.md`。

## 验证结果

- [x] 缺少 reviewer/report 的 `review-branch --pass --dry-run` 被拒绝，错误为 `Branch Review Gate passing result needs --reviewer or --review-report from the prior AI/human review.`
- [x] 只有 P3 finding、没有 reviewer/report 的非阻塞通过结论也被拒绝，避免 P3-only gate 绕过 review 身份。
- [x] P3-only 非阻塞通过结论缺少 evidence 时也会被 `review-branch` 提前拒绝；带 reviewer + evidence 时允许记录。
- [x] 提供 `--reviewer codex-main-session` 的 dry-run 通过，并在 `verification_evidence.reviewer` 记录 reviewer。
- [x] 提供 `--review-report .trellis/tasks/07-03-5-require-ai-review-prompt-before/review-dry-run.md` 的 dry-run 通过，并记录 report path、sha256、size 和 mtime。
- [x] 静态检查全部通过：`python3 -m json.tool`、`bash -n`、`python3 -m py_compile`、`task.py validate`、`git diff --check`、phase context 读取。
- [x] preset installer 临时安装验证完成：config preserved、managed scripts / Python companion / `.agents` / `.codex` / `.claude` / `.cursor` overlay installed，scripts executable，continue 文案含 `--reviewer`，finish 文案声明不执行 review。

## Docs SSOT reconciliation

- 本任务改变 Guru Team workflow / preset 的长期流程合同，已更新 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、canonical workflow 和 `.trellis/spec/workflow/*`。
- 本仓库没有独立 `docs/` 目录；task artifact 仅保留任务历史，不作为长期唯一来源。
- 部署影响：本任务不新增服务、CLI 入口、worker、runtime config、容器、K8s、migration 或 Makefile 变更；无需同步部署资产。
