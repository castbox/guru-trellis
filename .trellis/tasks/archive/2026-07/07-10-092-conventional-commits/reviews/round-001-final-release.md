# Round 001 最终放行审查

## 审查身份

最终放行审查代理。Branch Review mode，只读审查；未修改文件，未运行 `record-*`、`review-branch.sh`、`check-review-gate.sh`、`finish-work.sh`、`publish-pr.sh`。

## 审查范围

- worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/092-conventional-commits`
- diff：`origin/main...HEAD`
- source issue：`https://github.com/castbox/guru-trellis/issues/92`
- task：`.trellis/tasks/07-10-092-conventional-commits`
- 已审查：issue #92、`prd.md`、`design.md`、`implement.md`、`check.jsonl` 全部 spec、`planning-approval.json`、`phase2-check.json`、`issue-scope-ledger.json`、`agent-assignment.json`、workflow/dogfood workflow、README/spec、companion scripts、preset installer、tests、完整提交 diff。

## 审查的 HEAD

- 期望：`1b42776abbc037d152fb350528c96b6e93ccbef2`
- 实际：`1b42776abbc037d152fb350528c96b6e93ccbef2`
- 结论：匹配。

## 执行的命令

- `pwd`：确认在目标 worktree。
- `git rev-parse --show-toplevel`：确认 repo root 为目标 worktree。
- `.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task .trellis/tasks/07-10-092-conventional-commits`：通过；expected workspace 与 actual repo root 一致；source checkout 有非当前 task 的历史 handoff suspicious artifact；task worktree dirty 仅为 `.trellis/guru-team/handoff.json` 与 `.trellis/tasks/**`。
- `git status --short --branch`：仅剩 handoff 与 task metadata。
- `git diff --name-only origin/main...HEAD` / `git show --stat --oneline HEAD`：审查 20 个提交文件。
- `.trellis/guru-team/scripts/bash/check-commit-messages.sh --task .trellis/tasks/07-10-092-conventional-commits --json`：通过当前提交。
- `python3 -m unittest ...`：通过，242 tests。
- `python3 -m py_compile ...`：通过。
- `bash -n ...`：通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-10-092-conventional-commits`：通过。
- `.trellis/guru-team/scripts/bash/format-merge-commit.sh ... --json`：通过，生成 `chore(merge): #91 合并 #92 中文 Conventional Commits 提交规范`。
- `git diff --check`：通过。
- `verify-throwaway-install.sh` public marketplace sample：通过；仍不等同于当前分支 push/tag 后 marketplace ref 验证。
- 额外探针：直接调用 `validate_commit_subject()` 验证 subject close keyword 边界，发现缺口。

## 发现项

发现项：1

### P2 - commit subject 未禁止 `Closes/Fixes/Resolves`，未完整实现 `Refs` / `Closes` 分工

文件：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:5624`

问题：durable workflow 与 data contract 明确写明 commit messages 不得使用 `Closes` / `Fixes` / `Resolves`，close 语义只属于 PR body。但 `validate_commit_subject()` 只禁止 GitHub 默认 merge subject、中文 PR title、issue id 位置和非中文描述；未对 subject 本身运行 close keyword 检查。实测以下不合规 subject 返回空错误：

- `docs(workflow): #92 Closes #92 提交规范`
- `docs(workflow): #92 Fixes #92 提交规范`
- `chore(merge): #91 合并 #92 Closes 提交规范`

影响：`check-commit-messages.sh` 可能放行带 close keyword 的 work/merge commit subject，违反 issue #92 “commit message 只使用 `Refs`，PR body 使用 `Closes`”的核心合同。现有测试只覆盖 body 中 `Closes`，未覆盖 subject 中 close keyword。

建议修复：在 subject validator 中对完整 subject 或解析后的 description/summary 禁止 `close_keyword_pattern()` 命中，并补充 work subject 与 merge subject 的反例单测。

## 观察项

- 当前实际提交 `1b42776` 的 subject/body 本身合规，使用 `Refs #92`，未使用 `Closes`。
- Phase 2 post-commit audit 语义满足：`e94f4ab...` 是 HEAD 祖先；提交后的非 metadata 路径全部包含在 `phase2-check.json.dirty_paths`；当前 dirty 仅为允许的 metadata。
- canonical 与 dogfood Python/wrapper/workflow copy 已一致；preset managed asset 列表包含新增 wrapper。
- public main/可变 source throwaway sample 已通过，但当前分支 marketplace install 需 push 或 tag 后复验，任务证据已如实记录该限制。

## 后续候选

- 修复上述 finding 后，补充 subject close-keyword 反例测试并重新运行 242 单测、commit checker、dogfood drift、diff check。
- 分支 push 或 release tag 后，使用可解析的当前分支/tag marketplace source 再跑一次开箱安装验证。

## Docs SSOT

Docs SSOT Plan strategy 为 `ssot_first`。durable workflow、dogfood workflow、workflow README、preset README、README 与 `.trellis/spec/workflow/**` 已合并 issue #92 的长期合同，task artifact 保留规划与证据历史。

但当前代码 validator 与 durable docs 存在 current-scope 不一致：docs 明确禁止 commit messages 使用 close keywords，代码只禁止 body，不禁止 subject。因此 Docs SSOT 当前不能判定完全一致。

## 部署与安全影响

本次变更涉及 workflow/docs/spec、Python/bash companion scripts、preset installer、tests 和 installed dogfood copy。未涉及 CI/CD、Docker/K8s、DB migration、Makefile、runtime config。未发现 token、secret、`.env`、signed URL 或敏感原始数据写入 diff。

## 结论

不能作为 Branch Review Gate 通过证据。当前存在 1 个 P2 finding，需修复并重新进行闭环审查后，才可记录通过型 Branch Review Gate。
