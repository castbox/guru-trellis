# PRD：#7 finish-work 发布前强制 PR readiness evidence

## 目标

解决 GitHub issue #7：`finish-work` 自动发布 non-draft PR 前，必须使用 AI 已审阅的 PR body source（`--body-file` 或 `--body-artifact`）作为发布前判断证据，不能让脚本生成的 `generated` fallback 替代 PR readiness review。

## 背景与已确认事实

- #17 已关闭，并作为 PR body 内容质量标准的 SSOT：PR body 必须面向不了解 Trellis task 的 GitHub reviewer，包含具体的 `变更摘要`、`影响范围`、`验证结果`、`Review Gate`、`Issue 关闭范围` 和 `安全说明`。
- 当前 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 中 `resolve_pr_body()` 在没有 `--body-file` / `--body-artifact` 时仍返回 `body_source == "generated"`。
- 当前测试仍允许 recovery publish 在只传 `--validation` 时通过并返回 `body_source == "generated"`。
- `finish-work` 会先 archive task、写 journal、提交 Trellis metadata，再内部调用 `publish-pr`。
- `reviewed-pr-body.md` / `pr-readiness.json` 应和 `review.md` / `review-gate.json` 一样属于 task metadata：可在 Branch Review Gate 之后保持未提交，并由 `finish-work` 统一提交。
- 若 reviewed source 写在 active task 目录，archive 后路径会移动到 `.trellis/tasks/archive/YYYY-MM/<task>/...`。真实 publish 应读取 archive 后 artifact，archive 前读取只可作为 preflight。

## 需求

### R1：non-draft publish 必须有 reviewed body source

- `publish-pr` 在 non-draft 模式下必须拒绝缺失 `--body-file` / `--body-artifact` 的请求。
- `body_source == "generated"` 不得作为 non-draft publish readiness evidence。
- draft 或明确允许的 preview/dry-run 场景可保留 generated body 辅助，但不能关闭本 issue。

### R2：finish-work 必须在发布副作用前校验 reviewed source

- `finish-work` 调用内部 publish 前，必须要求 reviewed source。
- 缺失 reviewed source 时应在 archive/journal/push/PR 创建前，或至少在不会产生 publish 副作用的安全点阻塞。
- 本任务优先在 archive 前做 readiness preflight，避免 archive 后才发现 source 缺失。

### R3：readiness artifacts 作为 task metadata

- `reviewed-pr-body.md` / `pr-readiness.json` 属于 task metadata。
- `finish-work` 允许这些文件在 gate 后未提交，但仍阻塞所有非 metadata dirty path。
- `finish-work` metadata commit 应包含 archived task artifacts、review artifacts、readiness/body artifacts 和 journal。

### R4：publish 使用 archive 后 artifact SSOT

- 如果传入 active task 路径，例如 `.trellis/tasks/<task>/pr-readiness.json` 或 `.trellis/tasks/<task>/reviewed-pr-body.md`，`finish-work` archive 后必须把它解析/重写到 `.trellis/tasks/archive/YYYY-MM/<task>/...`。
- 如果 readiness artifact 内 `body_file` 是相对路径，应以 artifact 所在目录解析；archive 后也应指向 archived task 目录中的 body file。
- `publish-pr` 最终读取的 PR body source 应是 archive 后 artifact，而不是 archive 前内存缓存。

### R5：同步文案和可安装 surfaces

- canonical workflow、dogfood `.trellis/workflow.md`、finish-work skill/prompt/command overlays、README、workflow README、preset README 都应描述 #7 新门禁。
- 文案只引用 #17 作为 PR body 内容标准，不重复定义内容质量。
- 修改 preset overlay 后必须同步 dogfood 安装副本，并验证无 drift。

## 非目标

- 不重新定义 PR body 内容质量标准；该标准以 #17 为准。
- 不禁止 `build_pr_body()` 存在于 dry-run preview / draft 辅助路径。
- 不让脚本判断 PR body 是否“真实充分”；脚本只校验 reviewed source 是否存在、artifact 是否 ready、结构/占位/close-ref 等客观条件。
- 不创建新的用户日常 publish 入口；发布仍由 `trellis-finish-work` 接管。

## Docs SSOT

- 本仓库有 durable docs：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- 本任务会更新上述 docs，使其与 canonical workflow、preset overlay 和 companion script 行为一致。

## Middle-platform Knowledge Gate

不适用。本任务修改 Guru Team Trellis workflow/preset/companion scripts，不涉及 go-guru、proto-guru 或其它中台 SDK/framework。

## 验收标准

- [ ] non-draft `publish-pr` 缺少 `--body-file` / `--body-artifact` 时阻塞，不接受 `body_source == "generated"`。
- [ ] non-draft `finish-work` 缺少 reviewed source 时阻塞，且不执行 `git push` / `gh pr create`。
- [ ] `--body-artifact` 校验 `ready: true` 和非空 `body` / `body_file`；`ready: false` 或缺失正文必须阻塞。
- [ ] active task 路径在 archive 后能解析为 archived task artifact。
- [ ] artifact 内相对 `body_file` 在 archive 后按 artifact 所在目录解析。
- [ ] reviewed body source 和 readiness artifact 被视为 Trellis task metadata，metadata-only tail 规则仍阻塞非 metadata dirty path。
- [ ] `publish-pr --dry-run` 输出最终 body、`body_source` 和是否满足 non-draft 门禁，供 AI 审阅。
- [ ] 测试覆盖 generated body 只允许在 draft/preview 场景，不能用于 non-draft publish。
- [ ] canonical workflow、dogfood workflow、README、workflow README、preset README、`.agents/.codex/.claude/.cursor` overlays 同步说明新门禁。
- [ ] 运行相关单测、脚本静态检查、dogfood overlay drift check、task artifact 校验和 `git diff --check`。
