# #254 v0.6.5-guru.9 执行计划

## Phase 1：规划与激活

- [ ] fresh reread Issue #254、#220/#251/#253 merge facts、tags/Releases、canonical workflow/preset/overlay/spec 与 Claude installed inventory。
- [ ] 完成 `prd.md`、`design.md`、`implement.md`、Docs SSOT Plan、planning wording review 与 `guru-approve-task-plan`；只消费 `approved` exit。
- [ ] 取得任务 start confirmation 后运行官方 task start；保持 branch/worktree/task identity 与 fresh base 绑定。

## Phase 2：release preparation 实现

- [ ] 按 `trellis-before-dev` 重新读取当前 `.trellis/spec/` docs/preset/workflow 约定。
- [ ] 新增根目录 `CLAUDE.md`，逐字节复制 `AGENTS.md`；确认两者 mode/size/hash 一致。
- [ ] 将 canonical extension/release identity 与 public README、workflow/preset README、verifier fixtures/tests 收敛到 `v0.6.5-guru.9` / `0.6.5-guru.34` / CLI `0.6.5`。
- [ ] 核对 Claude canonical overlay、hooks/agents/skills/commands 与 Shared/Codex/Cursor projection；仅在当前 diff 证明存在 release-owned 缺口时做 additive 修正。
- [ ] 运行 preset apply、ownership、inventory、mode、registry/workflow graph、overlay drift、byte equality 与 zero sidecar checks。
- [ ] 新增 task-local `release-notes-zh.md`，准确披露 payload、升级路径、安全/部署影响、空 assets 与无 live GPT-5.6 Sol production semantic evidence。
- [ ] 运行 manifest/schema/package/runtime/integration/eval targeted suites、#220/#251/#253 installed regressions、deterministic/no-model/fake-production、sandbox/schema/route、linked worktree/closeout 和双 PATH verifier；不运行 live model matrix。

## Phase 2 gate 与 Finish

- [ ] 使用独立 Trellis implement/check work，执行 `guru-check-task`；finding 修复后按影响范围重跑。
- [ ] 展示精确 stage/commit message/paths，取得当前确认后运行 `guru-create-task-commit`。
- [ ] 对完整 `origin/main...HEAD` 做 fresh-final Branch Review，不复用旧 review/evidence；完成 PR readiness、Refs #254 body 与安全/部署/验证边界。
- [ ] 分别取得 push、PR create、merge 的当前确认；merge 只接受精确文本“合并PR”。

## Post-merge candidate 与发布

- [ ] merge 后 fresh fetch/freeze candidate commit/tree、累积 commits/paths、payload mapping 与唯一 `.34` revision。
- [ ] 重新运行完整 source/installed/throwaway initial/update/reapply、Claude discovery、ownership/drift、zero sidecar/bytecode、deterministic/no-model/fake-production 与 independent review gate。
- [ ] 展示 annotated tag object/message/commit/refspec，取得确认后创建并 push immutable `v0.6.5-guru.9`，live 回读 peeled commit/tree。
- [ ] 展示 fresh clone tag-pinned smoke 的临时目录和命令，取得独立确认后真实执行 install/update/reapply smoke。
- [ ] 展示中文 GitHub Release title/body/target/assets，取得独立确认后创建非 draft/非 prerelease Release 并 live 回读。
- [ ] 展示 `gh issue close 254` exact command，取得独立确认后关闭；最终回读 tag、peeled commit、Release、Issue state 与 excluded/follow-up 资源。
