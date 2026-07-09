# #73 实施计划：Trellis 官方文档链接改为 markdown 端点

## 前置检查

1. 确认工作区位于目标 worktree：

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task .trellis/tasks/07-10-073-trellis-doc-markdown-links
```

2. 确认 task 仍处于 planning，并且 `prd.md`、`design.md`、`implement.md` 已完成规划审查。
3. 规划确认后写入 `planning-approval.json`，再运行：

```bash
.trellis/guru-team/scripts/bash/check-planning-approval.sh --json --task .trellis/tasks/07-10-073-trellis-doc-markdown-links
python3 ./.trellis/scripts/task.py start 073-trellis-doc-markdown-links
```

## 实施步骤

1. 读取 `AGENTS.md` 的“官方 Trellis 优先”小节。
2. 将 3 个 URL 字面量替换为以下 markdown 端点：
   - `https://docs.trytrellis.app/index.md`
   - `https://docs.trytrellis.app/advanced/custom-workflow.md`
   - `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`
3. 保持链接说明文字和章节内容不变。
4. 不编辑其他文件，除非验证发现同一域名下仍有未改的 HTML 形式链接。

## 验证计划

1. 全仓库链接扫描：

```bash
rg -n "https://docs\\.trytrellis\\.app" .
```

2. `AGENTS.md` HTML 形式链接检查：

```bash
rg -n 'https://docs\.trytrellis\.app/($|[[:space:]])|https://docs\.trytrellis\.app/advanced/(custom-workflow|custom-spec-template-marketplace)([^.]|$)' AGENTS.md
```

该命令必须无输出。

3. 目标 markdown URL 内容类型检查：

```bash
for url in \
  https://docs.trytrellis.app/index.md \
  https://docs.trytrellis.app/advanced/custom-workflow.md \
  https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md
do
  curl -I -L -s "$url" | sed -n '1,12p'
done
```

每个 URL 必须返回 `200`，并且 `content-type` 必须包含 `text/markdown`。

4. Markdown diff 基础检查：

```bash
git diff --check
```

## Phase 2 check 重点

- 核对 `AGENTS.md` 只发生 URL 字面量变化。
- 核对 `docs/requirements/guru-team-trellis-flow.md` 的既有 `.md` 链接没有被误改。
- 核对本任务没有改变 workflow/preset/overlay 行为，因而无需运行完整安装门禁。
- 核对安全边界：diff 中不得出现 secret、token、`.env`、数据库 URL 或签名 URL。

## Branch Review Gate 重点

- 审查 `origin/main...HEAD` 全 diff。
- 确认 Issue Scope Ledger 中 `close_issues` 只包含 #73。
- 确认 Docs SSOT 方案已执行：durable source `AGENTS.md` 完成链接更新，task artifact 只保留审计证据。
- 确认部署、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile 均无变更需求。
