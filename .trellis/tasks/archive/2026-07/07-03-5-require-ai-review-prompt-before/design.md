# 设计：AI Review 与 Gate Artifact 分层

## 目标模型

Branch Review Gate 拆成两个明确层次：

1. **AI review prompt / code-review stance**：主会话或支持的平台 reviewer agent 读取完整 `origin/<base>...HEAD` diff，按 P0/P1/P2/P3 输出 findings、审查覆盖面、部署/文档影响判断。
2. **`review-branch.sh` recorder / validator**：只把已完成 review 的 summary、evidence、findings、reviewer 或 review report 写入 `{TASK_DIR}/review-gate.json`，并校验 reviewed head、diff range、deployment evidence、issue ledger 覆盖。

脚本不承担“判断分支没有缺陷”的 reviewer 角色。

## 变更边界

### Workflow canonical 与 dogfood copy

- 更新 `trellis/workflows/guru-team/workflow.md`：
  - Phase 3.5 增加 `3.5.1 AI Review Prompt` 与 `3.5.2 Gate Artifact Recorder`。
  - 明确 `review-branch.sh` 不是 review 本身。
  - 示例命令加入 `--reviewer` 或 `--review-report`。
- 同步 `.trellis/workflow.md`，保证当前 dogfood 仓库 phase 注入一致。

### Companion script

- 在 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 中新增 review report 支持：
  - `review-branch` 接受 `--review-report <path>`。
  - pass gate 必须提供非空 `--reviewer` 或有效 `--review-report`。
  - 如果提供 report，校验文件存在、非空，并记录路径、sha256 digest、size、mtime。
  - gate artifact 的 `metadata` 或独立字段记录 review identity/report 信息。
  - `validate_review_gate()` 对 passed gate 执行同样校验，阻止旧式空 reviewer + 无 report gate 发布。
- 同步安装副本 `.trellis/guru-team/scripts/python/guru_team_trellis.py`。
- 不增加复杂 YAML 配置；默认所有安装都强制执行该约束，避免旧 config 漏洞。

### Overlay 与文档

- 更新 preset overlay：
  - `.agents/skills/trellis-continue/SKILL.md`
  - `.codex/skills/trellis-continue/SKILL.md`
  - `.codex/prompts/trellis-continue.md`
  - `.claude/commands/trellis/continue.md`
  - `.cursor/commands/trellis-continue.md`
  - finish-work 相关入口说明只说验证已通过 gate，不说脚本完成 review。
- 同步 dogfood `.agents` / `.codex` 安装副本。
- 更新 README、workflow README、preset README，补充 recorder / validator 角色边界。

## 数据合同

`review-gate.json` 继续保持向后兼容，新增字段允许 older consumers 忽略：

```json
{
  "review": {
    "reviewer": "codex-main-session",
    "report": {
      "path": ".trellis/tasks/.../review.md",
      "sha256": "...",
      "size_bytes": 1234,
      "modified_at": "..."
    },
    "notes": "review-branch records the prior review; it does not perform review judgment."
  }
}
```

`metadata.reviewer` 保留，但 passed gate 校验不再允许空 reviewer 且无 report。

## 兼容与升级

- 旧的 passed gate 如果没有 reviewer/report，将在 `check-review-gate.sh` 或 `finish-work.sh` 阶段失败；这是本 issue 要求的安全收紧。
- 未升级 config 的业务仓库也会得到默认强制行为，因为逻辑在 script 默认路径中。
- preset installer 的 managed asset 列表无需新增文件；只更新已有 managed script 和 overlay。

## 验证策略

1. 静态验证：
   - JSON / Bash / Python compile。
   - `task.py validate`。
   - `git diff --check`。
2. 行为验证：
   - 构造当前 task 下的 dry-run 调用：`review-branch --pass` 缺少 `--reviewer` / `--review-report` 必须失败。
   - 有 `--reviewer` 的 dry-run 应成功。
   - 有 `--review-report` 的 dry-run 应记录 report digest。
3. 安装验证：
   - 运行 preset installer 到临时 Trellis-like repo，确认 overlay 和 managed script 可安装且脚本可执行。
   - 若时间不足无法完整 `trellis init` throwaway 安装，最终报告必须标明未覆盖风险。
