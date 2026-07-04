# #20 设计说明

## 设计原则

- 官方 Trellis 文档确认 workflow 行为由 `.trellis/workflow.md` 这类 Markdown 运行合同承载，不需要 fork Trellis upstream 或修改 hook 代码；spec marketplace 只放可复用规范，不放 active task/runtime state。
- AI/human review 的判断仍由主会话执行并写入 `review.md`；companion script 只验证 `review.md` 文件存在、非空、可计算 digest，并把 digest 记录进 `review-gate.json`。
- `--reviewer` 保留身份字段，但 passed gate 的 evidence 必须来自 `--review-report`。
- `trellis-continue` 的职责边界是 task work commit + Branch Review Gate artifact 产出；metadata commit 和 PR publish 属于 `trellis-finish-work`。

## 代码边界

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - `cmd_review_branch()`：passed gate 强制要求 `--review-report`。
  - `validate_review_gate()`：passed gate 必须有 `review_report.path`、`sha256`、`size_bytes`、`modified_at`。
  - `cmd_finish_work()` / `cmd_publish_pr()`：继续使用 `allow_metadata_after_gate=True` 的 finish/publish 内部路径，允许 reviewed HEAD 之后的 Trellis metadata-only tail。
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - 增加 reviewer-only pass 失败、review report digest 成功、旧 gate 校验失败、metadata-only tail 放行、非 metadata tail 拒绝、finish-work 以 metadata-after-gate 校验的测试。
- Markdown surfaces
  - canonical workflow、dogfood workflow、preset overlays、README、spec 同步改为 `review.md` 必填、`--review-report` 必填、continue stop、finish-work metadata commit/publish。

## 兼容性

- 新规则会拒绝旧的 reviewer-only passed gate。这是 issue #20 的预期行为；需要重新执行 Branch Review Gate 并生成 `review.md`。
- `review-gate.json` schema 仍保持 JSON object 兼容，没有额外 schema 文件强制收窄 handoff。
- `review.md` 作为 task-local artifact 属于 Trellis metadata，finish-work 会在 gate 后 metadata-only tail 中提交它。

## 风险与缓解

- 风险：某个平台 overlay 仍给出旧命令。缓解：修改 canonical overlay 后运行 preset apply 和 dogfood drift check。
- 风险：finish-work 因 gate 后 `review.md` 未提交而误判 HEAD stale。缓解：`finish-work` 使用 `allow_metadata_after_gate=True`，只允许 Trellis metadata tail。
- 风险：脚本被误认为 reviewer。缓解：workflow/README/spec 均保留 recorder / validator 边界。
