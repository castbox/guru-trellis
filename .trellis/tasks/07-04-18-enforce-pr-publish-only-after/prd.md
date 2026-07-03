# #18 PR 发布只能发生在 finish-work 之后

## 背景

Guru Team Trellis 的当前目标流程是：

- `trellis-continue` 负责推进规划、实现、验证、提交和 Branch Review Gate。
- `trellis-finish-work` 是唯一 closeout 入口，负责 archive task、记录 journal，然后自动 publish PR。
- `publish-pr` 是内部恢复/调试 helper，不应成为日常用户入口。

用户指出历史 Codex 会话中出现过执行漂移：有时 PR 在 `trellis-continue` 阶段被创建，有时才在 `trellis-finish-work` 阶段创建。用户明确期望：未完成 `finish-work` 前不允许 push 分支并创建 PR。

后续证据补充：Codex 会话 `019f28a8-cc59-75e2-bebb-ab539719a1b3` 显示 `trellis-continue` 语境下继续链式执行了 `finish-work`，当前会话也曾准备在用户只要求提交后继续执行 `finish-work`，被用户终止。这说明边界不只在 `publish-pr`，还必须覆盖 `trellis-continue` 不能自动调用 `finish-work`。

## 目标

本任务要按 Trellis 官方最佳实践和工程最佳实践收敛 PR 发布边界：

1. 由 Markdown workflow / skill / command overlay 明确流程判断：`trellis-continue` 不发布 PR，`trellis-finish-work` 才发布 PR。
2. Companion script 只做确定性门禁：普通 `finish-work.sh` 必须证明来自显式 `trellis-finish-work` 入口，普通 `publish-pr` 调用必须证明来自 `finish-work`，否则拒绝 archive/push/PR。
3. 保留显式 recovery/debug 能力，但必须是刻意选择、可审计、可在 dry-run/测试中验证的路径。
4. canonical workflow、preset overlay、dogfood 安装副本和 README 语义保持一致。

## 用户价值

- 降低 AI 运行时把 `continue` 误解成发布入口的概率。
- 避免未 archive task、未记录 journal、未完成 finish-work 的分支提前出现在 GitHub PR 中。
- 让脚本层成为最后一道确定性防线，而不是替代 AI review / PR readiness 判断。

## 范围

### In Scope

- 更新 `trellis/workflows/guru-team/workflow.md` 和 dogfood `.trellis/workflow.md` 中的 PR 发布边界说明。
- 更新 Guru Team preset overlays 中的 `trellis-continue` / `trellis-finish-work` 入口文案，并同步 dogfood 安装副本。
- 修改 `guru_team_trellis.py` 的 `publish-pr` / `finish-work` 调用合同。
- 更新 README / preset README / workflow README 中日常入口和发布边界说明。
- 为普通 `publish-pr` 被直接调用的失败路径和 `finish-work` 内部调用路径补充测试或代表性 dry-run 验证。
- 更新 issue-scope-ledger 的验收证据。

### Out of Scope

- 修改 Trellis 上游 npm 包、全局安装目录或 `node_modules`。
- 改变 Branch Review Gate 的 AI/human review 职责。
- 改变 `issue-scope-ledger.json` 的 close/ref/followup 语义。
- 改变 GitHub issue intake、worktree 创建、task 创建的 Phase 0 语义。

## 官方与项目规范依据

- Trellis 官方 Custom Workflow 文档：团队流程应通过 `.trellis/workflow.md` / marketplace workflow 的 Markdown 流程合同表达。
- Trellis 官方 Custom Spec Template Marketplace 文档：可复用规范放 marketplace/spec template；active task state 和运行态 PR 状态不进入模板。
- 本仓库 AGENTS 规则：Markdown 控制流程和判断，Python/shell 只做 Executor / Validator / Recorder。
- `.trellis/spec/workflow/workflow-contract.md`：`finish-work.sh` 是 closeout entry；`publish-pr` 不应成为用户可见新阶段。
- `.trellis/spec/workflow/companion-scripts.md`：GitHub 操作需 `gh auth status`，publish 前拒绝非 metadata dirty path，脚本使用 `WorkflowError` 输出可操作失败。

## 需求

### R1: `trellis-continue` 不得发布 PR 或执行 finish-work

- Continue 入口必须明确：到 Branch Review Gate 为止，下一步是 `trellis-finish-work`。
- Continue 文案不得暗示会 push 或创建 PR。
- Continue 阶段如果需要发布，只能停止并提示显式进入 finish-work；不能调用 `finish-work` 或 `publish-pr`。

### R2: `trellis-finish-work` 后才能普通发布

- `finish-work` 必须在通过 Branch Review Gate、archive task、journal 记录、metadata commit 之后调用 publish。
- `finish-work.sh` 裸调必须失败；只有显式 `trellis-finish-work` 入口可携带 intent marker 进入 closeout。
- `finish-work` 内部调用 publish 时要携带脚本可验证的内部标记，证明这是 closeout 后发布。
- `finish-work --dry-run` 仍应能验证 publish payload，但不能产生 push/PR 副作用。

### R3: 直接调用 `publish-pr` 默认拒绝

- 普通 `publish-pr` 直接调用必须失败，错误信息要说明应运行 `finish-work.sh --json`。
- 失败必须发生在 `git push` 和 `gh pr create` 之前。
- JSON 模式下错误 payload 应可被测试断言。

### R4: Recovery/debug override 必须显式

- 如保留直接 `publish-pr` recovery/debug 路径，必须使用明确 flag。
- flag 名称和 help 文案必须说明它不是日常路径。
- Recovery/debug 路径仍必须通过 review gate、issue scope ledger、dirty state、gh auth 等已有确定性校验。

### R5: Source / installed copies 同步

- canonical workflow / scripts / overlays 修改后，必须同步 dogfood `.trellis/` 和平台入口副本。
- preset installer apply 后不应留下 `.new` / `.bak` 未处理文件。
- dogfood overlay drift check 必须通过。

## 验收标准

- [ ] 未带内部标记或 explicit recovery flag 的 `publish-pr --dry-run` 会失败。
- [ ] 未带 explicit `trellis-finish-work` intent marker 的 `finish-work --dry-run` 会失败。
- [ ] 带 explicit recovery flag 的 `publish-pr --dry-run` 在已有 gate/ledger 条件满足时可生成 payload。
- [ ] `finish-work --dry-run` 可以通过内部标记调用 publish dry-run。
- [ ] `trellis-continue` overlay / prompt / command 文案明确禁止 publish 和调用 finish-work。
- [ ] `trellis-finish-work` 文案明确 archive + journal 成功后才 publish。
- [ ] canonical 与 dogfood 副本一致。
- [ ] `bash -n`、`py_compile`、task validate、dogfood drift、`git diff --check` 通过。
- [ ] 如改动 README 或 marketplace 文件，验证相关 JSON/Markdown 安装路径不漂移。

## Docs SSOT

本仓库没有传统 `docs/` 产品文档系统。长期 SSOT 是：

- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `trellis/workflows/guru-team/workflow.md`
- `.trellis/spec/workflow/*`

本任务如改变长期流程合同，需要同步上述相关文件；task artifact 仅保留执行证据，不作为长期唯一来源。

## 中台知识 Gate

本任务不涉及 Guru Team middle-platform SDK、go-guru、proto-guru、Unity3D Guru SDK 或 Flutter Guru SDK；Middle-platform Knowledge Gate 不适用。
