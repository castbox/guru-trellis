# #20 强制 Branch Review Gate 每次产出 review

## 背景

Issue #20 指出 Guru Team Branch Review Gate 目前存在两条 pass 路径：

- `--reviewer + --evidence`
- `--review-report`

这会导致有些任务有 task-local `review.md`，有些任务只有 `review-gate.json`，跨会话审计体验不一致。用户本轮进一步明确：`trellis-continue` 可以执行审查并产出 `review.md` / `review-gate.json`，但不能提交这些 Trellis metadata，也不能 push 或创建 PR；剩余 metadata commit 和 PR publish 必须由显式 `trellis-finish-work` 负责。

## 需求

- Branch Review Gate 每次都必须产出当前 task 目录下的 `review.md`，作为 AI/human review 判断主证据。
- `review-branch.sh --pass` 必须要求有效 `--review-report`，裸 `--reviewer` 只能记录身份，不能替代 review report。
- `review-gate.json` 必须记录 `review_report.path`、`sha256`、`size_bytes`、`modified_at`。
- `check-review-gate.sh` / `finish-work.sh` 必须拒绝缺少有效 `review_report` digest 的 passed gate。
- `trellis-continue` 必须明确：提交 task work 后执行 review、写 `review.md`、记录 `review-gate.json`，然后停止；不得提交 `review.md`、`review-gate.json`、handoff、journal、archive 等 Trellis metadata，不得 push/PR。
- `trellis-finish-work` 必须明确拥有 metadata-only tail commit 和 PR publish，并允许 gate 后只出现 Trellis metadata commit；如果 gate 后出现代码、脚本、schema、preset、CI/CD、部署等非 metadata 变更，仍然阻塞。
- workflow、skill、prompt、README、spec、tests、dogfood overlay 必须保持一致。

## 验收标准

- 不带 `--review-report` 的 `review-branch.sh --pass --reviewer ... --evidence ...` 失败。
- 带有效 `review.md` 的 `review-branch.sh --pass --review-report ...` 成功，并在 `review-gate.json` 记录 digest 四字段。
- `check-review-gate.sh` / `finish-work.sh` 拒绝历史 reviewer-only passed gate。
- `finish-work` 对 reviewed HEAD 之后的 Trellis metadata-only tail 放行，对非 metadata tail 拒绝。
- `trellis-continue` 文档和各平台 overlay 明确先写 `review.md`，再用 `--review-report` 调用 recorder，之后停止等待 `trellis-finish-work`。
- canonical workflow、dogfood workflow、preset overlay、README、spec 与测试一致。
- preset apply 后 dogfood overlay 无漂移。

## 非目标

- 不修改官方 Trellis upstream、全局 npm 包或 `node_modules`。
- 不把 AI review 判断写进 Python/shell；脚本只校验 review report 文件、digest、HEAD、metadata tail 等确定性事实。
- 不改变 PR body 生成质量规则，除非为说明本次 review gate 证据最小同步文案。

## Docs SSOT 与中台知识

- 本仓库没有 `docs/` 目录；长期团队流程 SSOT 是 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`.trellis/spec/`、canonical workflow 与 overlay。
- 本任务修改 workflow/preset 机制，不涉及 Guru middle-platform SDK 或框架；Middle-platform Knowledge Gate 不适用。
