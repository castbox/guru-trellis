# #312 Implementation Plan

## 1. Entry Gates

- 当前 task status 保持 `planning`；本文件获用户最终确认后才运行 `task.py start`。
- 实施前重新核对 `origin/main`、#311 并行状态、两个 owner 的 current bytes 与 extension revision；如
  base 演进，先走 `guru-reconcile-task-base`。
- 从本 task worktree 运行 workspace boundary；source checkout 不得收到本 task 写入。
- 读取 `prd.md`、`design.md`、本文件、Docs SSOT Plan、`implement.jsonl` 与清单列明的规范。

## 2. Ordered Implementation

1. **Durable spec first**
  - 更新 `.trellis/spec/workflow/companion-scripts.md` 的 artifact 分类与
    `--allow-source-clean` 边界。
  - 更新 `.trellis/spec/workflow/quality-guidelines.md` 的真实 Git 回归矩阵。
  - 不修改 shared RDT/Architecture current authority；若发现不对齐，停止并回 Phase 1。
2. **Finalizer owner**
  - 在 `guru-finalize-task/runtime/owner.py` 增加只读的 source Git path-state helper。
  - 调整 collector：tracked-clean 普通 task 文件跳过；review metadata、untracked/dirty 与
    `reviews/**` 保持 suspicious。
  - 保持 `workspace_boundary_errors()`、public snapshot、CLI 与 `--allow-source-clean` 不变。
3. **Publication owner**
  - 对 `guru-review-task-publication/runtime/owner.py` 应用同构 helper 与 collector 控制流。
  - 逐项比较两个 owner 的常量、放行条件、失败策略和 snapshot kind。
4. **Focused real-Git tests**
  - 为两个 package 增加 source main + task worktree + runtime mapping fixture。
  - 覆盖 tracked-clean 全集、untracked、staged、unstaged、deleted/renamed、tracked-clean review
    metadata、`reviews/**`、unrelated dirty 与 wrong identity。
  - 增加 CLI `--allow-source-clean` negative regression 和两 owner 一致性断言。
5. **Managed projection**
  - 按 current base 解析下一非冲突 extension revision；不得覆盖并行 #311 的 manifest/version delta。
  - 运行 canonical all-platform preset apply，生成 dogfood installed package、preset spec/docs、
    extension manifest 与声明平台投影。
  - 只在 current operator wording 不足时最小更新 workflow/preset README。
6. **Validation and finding closure**
  - 运行 focused package tests、installer/reapply/drift、throwaway install/update、compile、task validate、
    `git diff --check` 与 sidecar-zero。
  - 派发独立 `trellis-check` 子代理做完整 Phase 2 semantic check；P0-P3 finding 均在当前 branch 修复并
    fresh rerun。
7. **Delivery and downstream proof**
  - task commit 与 fresh current-HEAD Branch Review 通过后，再进入 Publication/Finalizer。
  - push、PR、merge、候选发布/安装分别使用届时展示的精确目标和授权。
  - 安装修复候选到 Chengtuo #252 当前 worktree 后，重新运行原 checker；通过后才返回 #252 Phase 2。

## 3. Validation Commands

实施时按 current package inventory 修正精确命令；最低集合：

```bash
python3 -m unittest discover \
  -s trellis/skills/guru-team/packages/guru-finalize-task/tests \
  -p 'test_*.py'

python3 -m unittest discover \
  -s trellis/skills/guru-team/packages/guru-review-task-publication/tests \
  -p 'test_*.py'

python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py

python3 trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py \
  --repo . \
  --all-platforms \
  --json

bash trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh

find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages \
  -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile

python3 ./.trellis/scripts/task.py validate \
  .trellis/tasks/08-27-312-workspace-boundary-merged-active-task

.trellis/guru-team/scripts/bash/check-workspace-boundary.sh \
  --json \
  --task .trellis/tasks/08-27-312-workspace-boundary-merged-active-task

git diff --check
```

Downstream live proof 从
`/Users/wumengye/Documents/GoProjects/chengtuo-resume-worktrees/252-full-reparse-root-cause`
执行其 installed checker，并同步核对 source checkout `git status`、worktree identity 与 runtime mapping。

## 4. Risk And Rollback

- 主要风险是把“tracked”误当成“clean”或把 review metadata 一并放行；真实 Git fixture 和分层矩阵
  必须同时锁定 index、HEAD 与 worktree state。
- 两 owner 重复实现存在漂移风险；同一 case matrix 与 generated parity 是合并门禁。
- preset apply 会产生较大 managed diff；只接受 manifest 声明的生成范围，意外文件或 sidecar 立即
  阻断并调查。
- #311 可能演进相同 Finalizer owner/manifest；不覆盖、不 cherry-pick 猜测版本，先做 base
  reconciliation。
- 回滚只移除本 task 未提交 delta；不得删除 task/worktree、改 runtime mapping 或用
  `--allow-source-clean` 掩盖回归。

## 5. Phase Transition Stop

本规划获用户新一轮明确批准前：

- 不运行 `task.py start`；
- 不修改 runtime/spec/test/product code；
- 不提交、push、创建 PR、合并、发布、安装或重试 Chengtuo 错误文件。
