# #211 实施计划

## 1. 当前身份

- Branch：`fix/211-task-commit-hooks`
- Worktree：`/Users/wumengye/Documents/GoProjects/211-task-commit-hooks`
- Base：`main@8d52f2b5bfa64c29a64deb616e9f5b4a7c4ebce8`
- Task：`.trellis/tasks/08-12-211-task-commit-hooks`
- Issue：#211（唯一 close issue）
- Dispatch：`sub-agent`

## 2. Durable docs first

- [ ] 按 `design.md` Docs SSOT Plan 更新 package contract 与直接相关 durable specs。
- [ ] 明确真实 `git commit`、transaction worktree/index、pre-ref 与 post-commit recovery
  边界，不改变 global workflow exits。
- [ ] runtime 改动前完成首轮 docs sync。

## 3. Package-local executor

- [ ] 在 canonical `runtime/execute.py` 建立临时 detached transaction worktree、isolated
  index 与 `0600` message file。
- [ ] materialize exact reviewed candidate，并绑定 pre-hook tree/blob/mode/path facts。
- [ ] 使用 `git commit --cleanup=verbatim -F` 运行真实 repository hooks。
- [ ] 捕获 hook refusal、message rewrite、index/worktree mutation 与 created commit identity。
- [ ] 在 live `update-ref` 前验证 parent/message/path/tree/blob/mode 和 live preimage。
- [ ] 保持 semantic index-entry comparison，不比较 `.git/index` bytes。
- [ ] 成功后清理 transaction/candidate/Phase 2 checkpoint；失败保留可重试输入。

## 4. 真实 Git regression tests

- [ ] 增加真实临时 repo fixture，覆盖四类 hook 顺序与 exact environment。
- [ ] 覆盖 pre-commit / commit-msg reject、message rewrite、额外 path、exact-path mutation、
  stage/unstage、rename/delete 与 untracked mutation。
- [ ] 覆盖 post-commit failure/mutation 的 created-commit recovery。
- [ ] 覆盖 unrelated staged/unstaged/untracked/gitlink preservation。
- [ ] 覆盖 stat-cache-only refresh 和 parent/message/tree/blob/mode/current HEAD postconditions。

## 5. Canonical / installed / platform convergence

- [ ] 检查 commands/error/interface 是否需 additive 变更；无直接 consumer 则不扩 DTO。
- [ ] 运行 preset apply 同步 `.trellis/guru-team`、`.agents`、`.codex`、`.claude`、
  `.cursor` 目标。
- [ ] 验证 canonical/installed byte parity、source/installed package validators 与 dogfood drift。
- [ ] 处理并清零 `.new` / `.bak` / conflict sidecar。

## 6. 验证命令

```bash
/usr/local/bin/python3 -m unittest \
  trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_runtime.py \
  trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py

find trellis/skills/guru-team/packages/guru-create-task-commit -name '*.py' -type f \
  -print0 | xargs -0 /usr/local/bin/python3 -m py_compile

bash -n trellis/skills/guru-team/packages/guru-create-task-commit/scripts/*.sh
trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-12-211-task-commit-hooks
git diff --check
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
```

- [ ] 运行 clean throwaway initial install。
- [ ] 运行 existing repo update/reapply。
- [ ] 运行 official Trellis update 后重验 hooks 行为与 sidecar。

## 7. Phase 2 与结束边界

- [ ] 使用 `trellis-implement` sub-agent 实现；主会话负责 scope 与 docs reconciliation。
- [ ] 使用独立 `trellis-check` sub-agent 收集完整检查证据。
- [ ] 调用 `guru-check-task` 完成 scope-first semantic check；finding 必须回到实现并全量重跑。
- [ ] 不创建 `implementation-handoff.md`。
- [ ] Phase 2 pass 后，commit 前展示 exact stage paths/message/HEAD 并取得独立确认。
- [ ] 后续 Branch Review 必须覆盖 `origin/main...HEAD` current HEAD 完整 diff且无 P0-P3。
- [ ] 本任务不 push、不创建 PR、不 archive、不 merge，除非后续获得对应明确授权。

## 8. Rollback points

| Gate | 行为 |
| --- | --- |
| docs owner 未收敛 | 不改 runtime |
| hook 环境不能代表 exact candidate | 停止实现，修订设计 |
| pre-ref failure 改变 live branch/index | Phase 2 阻断 |
| post-commit recovery 缺 created commit identity | Phase 2 阻断 |
| source validator 失败 | 不运行 preset apply |
| dogfood drift 或 sidecar | 不记录 Phase 2 pass |
| throwaway/update 未通过 | 不宣称开箱即用完成 |

