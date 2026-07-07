# #52 详细设计：显式规划审核门禁

## 设计原则

1. **Markdown owns process**：规划审核节点由 workflow / overlay / skill 文案强制主 agent 停下并展示文档链接。
2. **Script records facts**：`record-planning-approval` 只记录已发生的用户确认和文档 digest；`check-planning-approval` 只校验 objective freshness。
3. **Canonical first**：先改 `trellis/workflows/guru-team/` 和 `trellis/presets/guru-team/overlays/`，再通过 preset apply 同步 dogfood copies。
4. **Fail closed before implementation**：默认 `sub-agent` mode 下，任何 implement/check/commit/finish 入口都要依赖有效 planning approval。

## 影响面

### Workflow / overlay

- Canonical workflow:
  - 在 Phase 1 planning artifacts 和 Phase 1.4 之间增加显式“展示三文档链接并等待用户确认”的门禁。
  - 明确 Phase 0 handoff confirmation 不是 planning approval。
  - 明确规划文档在确认后变化时必须重新展示链接并重新确认。
- `trellis-continue` overlays:
  - planning 状态路由中，如果三文档已生成但有效 `planning-approval.json` 缺失或 stale，必须停下，输出三个 task-local absolute links 和阻断说明。
  - 不允许“用户在 Phase 0 回复确认”作为 `record-planning-approval` 的 `--user-confirmation`。
- Implement subagent overlays:
  - 在读取 task artifacts 前先要求主会话已经通过 `check-planning-approval`。
  - Subagent 自身若发现 planning approval 缺失/stale，应报告阻塞并停止，不继续实现。
- Phase 2 / Branch Review text:
  - 保持现有 Phase 2 check 和 Branch Review Gate 边界；新增 planning approval 是更早的 start gate。

### Companion script contract

`planning-approval.json` schema 升级到可兼容读取但强校验的新结构：

```json
{
  "schema_version": "1.1",
  "review_prompt_presented_at": "2026-07-08T00:00:00Z",
  "approved_at": "2026-07-08T00:01:00Z",
  "task_dir": ".trellis/tasks/...",
  "head": "<git sha>",
  "dirty_paths": ["..."],
  "reviewer": "codex-main-session",
  "approval_summary": "中文规划审查结论",
  "user_confirmation": {
    "source": "explicit-post-planning-review",
    "message": "用户在看到 prd/design/implement 链接后确认进入实现。"
  },
  "reviewed_artifacts": [
    {"path": ".../prd.md", "sha256": "...", "size_bytes": 1, "modified_at": "..."},
    {"path": ".../design.md", "sha256": "...", "size_bytes": 1, "modified_at": "..."},
    {"path": ".../implement.md", "sha256": "...", "size_bytes": 1, "modified_at": "..."}
  ],
  "approved_artifacts": [...]
}
```

兼容策略：

- `approved_artifacts` 可保留为 alias 供已有 Branch Review audit 代码复用。
- 新 validator 必须要求 `reviewed_artifacts` 完整包含三份规划文档。
- 旧 `schema_version: 1.0` 且 `user_confirmation.source: workflow` 在 `check-planning-approval` 下失败，防止 Phase 0 confirmation 继续被误用。

CLI 参数建议：

- `record-planning-approval` 新增或使用固定语义：
  - `--review-prompt-presented-at <iso>` 可选；缺省为 recorder 当前时间，但 workflow 必须在用户可见 prompt 后调用。
  - `--confirmation-source explicit-post-planning-review` 可选但默认固定为该值。
  - `--artifact` 仍保留，但默认必须收集三份 `prd.md` / `design.md` / `implement.md`；用户显式只传一份时 validator 仍失败。
- `check-planning-approval` 不判断文档内容充分性，只判断 schema/source/artifact/digest/head/dirty-path freshness。

### Docs SSOT

`docs/requirements/requirement-main.md` 与 `docs/requirements/guru-team-trellis-flow.md` 当前已说明 planning approval，但未明确“必须展示三文档链接并等用户 post-planning 确认”。实现后补充该门禁，避免长期文档仍停留在泛化 planning approval 说法。

## 数据与兼容性

- 已归档历史 task 的旧 `planning-approval.json` 不需要迁移；它们作为历史证据保留。
- 新任务或当前活跃任务从此必须使用 `schema_version: 1.1` 和 `explicit-post-planning-review`。
- Branch Review Gate 对旧归档 artifact 的 archive path normalization 不受影响；它在当前任务 pass gate 时会检查新 artifact。
- `phase2-check.json`、`review-gate.json` 中对 `planning-approval.json` digest 的引用逻辑不变，只是 upstream validation 更严格。

## Fail-Closed 点

- Planning approval 缺失：`task.py start` 前阻塞。
- Approval source 错误：阻塞。
- 三份文档不完整：阻塞。
- 文档 digest/mtime/size 缺失或不匹配：阻塞。
- Approval HEAD 与当前 HEAD 不一致：阻塞；post-commit audit 仍按既有 `--allow-committed-head` 仅用于后续 gate 审计。
- Implement subagent 收到缺失/stale approval：停止并返回阻塞 handoff。

## 测试策略

1. Python unit tests:
   - 有效 post-planning approval 通过。
   - `source=workflow` 或 `phase0-handoff` 失败。
   - 缺少 `design.md` / `implement.md` 或 digest 字段失败。
   - 修改规划文档后旧 approval 失败。
   - `record-phase2-check` / Branch Review Gate 在 planning approval stale 时仍阻塞。
2. Overlay tests / deterministic grep:
   - canonical 与 dogfood `trellis-continue` 文案包含三文档链接要求、阻断说明、Phase 0 confirmation 不能替代。
   - implement agents 包含 `check-planning-approval` 前置条件。
3. Installer / drift:
   - `apply.sh --repo . --all-platforms`
   - `check-dogfood-overlay-drift.sh`
   - installer tests 确认 overlay 分发。
4. Throwaway install:
   - 运行 `verify-throwaway-install.sh`；若环境受限，在 PR body 明确未覆盖。

## 风险与取舍

- 风险：overlay 文案分散在 Codex/Claude/Cursor/shared/channel runtime，容易漏同步。
  - 缓解：先改 canonical overlay，使用 preset apply 同步，再跑 drift check。
- 风险：validator 太宽会继续接受 Phase 0 confirmation。
  - 缓解：显式枚举 `explicit-post-planning-review`，并让旧 source fail closed。
- 风险：脚本新增字段被误解为脚本判断规划质量。
  - 缓解：artifact `notes` 和 spec 文档继续声明 recorder/validator 边界。

## Rollback

如新 validator 误阻塞，可回退本任务对 `guru_team_trellis.py` 和 overlay 的提交；历史 task artifact 不需要迁移。回退后需重新 apply preset 并跑 drift check，避免 dogfood 副本与 canonical overlay 分叉。
