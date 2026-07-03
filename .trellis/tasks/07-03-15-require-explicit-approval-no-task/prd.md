# Issue 15：no_task current-checkout direct edit 显式批准

## 目标

补齐 Guru Team workflow 在 `no_task` 状态下的文件修改边界：当用户请求会修改文件、修复 bug、实现功能或改变 workflow / preset / script 行为时，默认必须先进入 GitHub issue intake 和 Git base/worktree preflight；如果用户确实想跳过 issue/task/worktree/branch，在当前 checkout 直接修改，必须先明确批准这个 direct-edit override。

## 背景与证据

- GitHub issue：`https://github.com/castbox/guru-trellis/issues/15`。
- 现有 `trellis/workflows/guru-team/workflow.md` 已要求 issue-backed、task-like 或 file-changing request 先走 intake/preflight，并要求创建 GitHub issue、worktree、branch、Trellis task 前取得 consent。
- 当前缺口是：workflow 没有明确禁止 AI 在 `no_task` 下静默把文件修改降级为“当前 checkout 小修复”，也没有要求 direct-edit override 必须说明跳过 issue/task/worktree/branch。
- 官方 Trellis `custom-workflow` 文档说明 `workflow.md` 控制 phase、skill routing 和 per-turn breadcrumb，运行时会读取 Markdown；因此流程判断应写在 workflow / overlay / skill 文案中，而不是写进 Trellis upstream 或 hook 分叉。
- 官方 Trellis `custom-spec-template-marketplace` 文档说明 spec template 适合放可复用工程规范、review checklist 和去敏示例，不应放 active task / runtime state；因此本次 spec 更新只加入可复用审核规则，不写 task 私有状态。

## 范围

### 必做

- 更新 canonical `trellis/workflows/guru-team/workflow.md`：
  - `no_task` 文件修改默认走 Phase 0 intake/preflight。
  - current-checkout direct edit 只允许在用户显式批准后发生。
  - 批准语义必须包含跳过创建/复用 GitHub issue、Trellis task、worktree 和 branch。
  - direct-edit override 不等于 commit/push 批准。
  - 编辑前 AI 必须说明副作用和 changed-file scope。
- 同步 dogfood `.trellis/workflow.md`。
- 更新 `trellis-start` canonical overlays 和本仓库 dogfood 安装副本：
  - `.agents/skills/trellis-start/SKILL.md`
  - `.codex/prompts/trellis-start.md`
  - `.codex/skills/trellis-start/SKILL.md`
- 检查 README / workflow README / preset README 是否会把 direct edit 描述为 AI 可自行选择的默认捷径；必要时补充 direct-edit override 说明。
- 更新 `.trellis/spec/workflow/workflow-contract.md` 和 `.trellis/spec/workflow/quality-guidelines.md`，让 review checklist 能审核 `no_task` direct edit 是否有 Phase 0 evidence 或用户显式 override evidence。
- 若实现 validator，仅检查客观证据存在与否，不让脚本判断 scope 是否合理。

### 非目标

- 不禁止所有 `no_task` direct edit。
- 不要求每个极小对话都创建 Trellis task。
- 不把一次 direct-edit override 扩大解释为后续 commit / push / PR 批准。
- 不修改 Trellis upstream 源码、全局 npm 包或 `node_modules`。
- 不把业务仓库私有规则写入通用 workflow / spec template。

## Durable Docs SSOT

本仓库没有业务 `docs/` 目录。长期可读的文档面是：

- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `.trellis/spec/workflow/*.md`

本次如果改变长期 workflow 行为，需要同步上述文档/规范面；task artifact 只保留 issue 15 的执行证据，不作为长期 SSOT。

## Middle-platform Knowledge Gate

不适用。本次不涉及 Guru Team middle-platform SDK、go-guru、proto-guru、Unity / Flutter SDK 或业务 framework 行为。

## 验收标准

- [ ] `workflow.md` 明确 `no_task` 文件修改默认走 intake/preflight。
- [ ] `workflow.md` 明确 current-checkout direct edit 只允许在用户显式批准后发生。
- [ ] `workflow.md` 明确批准必须覆盖“跳过 GitHub issue、Trellis task、worktree、branch”，且 commit/push 仍需单独批准。
- [ ] `trellis-start` overlays 和 dogfood 安装副本同步 direct-edit override 规则。
- [ ] README / workflow README / preset README 不暗示 AI 可自行选择 direct edit 捷径。
- [ ] specs / quality checklist 可审核 `no_task` direct edit 是否有 Phase 0 preflight evidence 或 explicit override evidence。
- [ ] 如实现 validator：无 active task + 非 metadata 改动 + 无 evidence 时，commit/push 前阻塞或强提醒；脚本不替代 AI/human 判断。
- [ ] overlay 修改后运行 preset apply 到本仓库 dogfood copy，并通过 dogfood overlay drift check。
- [ ] 运行 workflow/preset 相关最小验证，并记录无法覆盖的开箱即用或 upgrade/update 门禁风险。
