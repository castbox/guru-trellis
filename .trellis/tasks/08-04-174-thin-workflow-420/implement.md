# #174 实施计划：thin workflow 420 行预算

## 1. 实现前门禁

- [ ] `prd.md`、`design.md`、`implement.md` 非空且包含 Docs SSOT Plan。
- [ ] `guru-review-contract-wording` 的 planning profile 对三份文档通过；不得跳过
      该 owner。
- [ ] `guru-approve-task-plan` 对 current planning artifacts 返回 checker-passed
      `approved`，再执行官方 `task.py start`；未激活前不修改 workflow。
- [ ] task worktree boundary 指向
      `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/174-thin-workflow-420`，
      branch 为 `codex/174-thin-workflow-420`，base HEAD 为
      `ecb2e918627dd3513976dd1dd52d9af461375c9d`。
- [ ] 实现前重新确认 Issue #174 仍为 open，且没有新的 scope/authority 变化。

## 2. 有序实施步骤

### Step 1：记录 current-HEAD baseline

- [ ] 记录 canonical/dogfood 行数、字节 digest、marker payload 集合、phase context
      读取结果与两个 line-budget assertion 的现状。
- [ ] 记录 runtime suite、Skill suite、README baseline failure 与其它门禁的独立结果。

### Step 2：收敛 canonical workflow

- [ ] 只修改 `trellis/workflows/guru-team/workflow.md` 的重复全局说明或排版行。
- [ ] 不修改或重新编号 machine-readable marker；不删除 #161 stale re-entry、
      fail-closed、Docs SSOT、Issue Scope Ledger、side-effect 或 ownership boundary。
- [ ] 不修改两个 line-budget assertion，不改 Skill package、runtime、preset 或
      upstream overlay。

### Step 3：同步 dogfood

- [ ] 按 canonical source → dogfood copy 同步 `.trellis/workflow.md`。
- [ ] `cmp -s trellis/workflows/guru-team/workflow.md .trellis/workflow.md` 通过；
      重新计算两份行数并确认均 `<= 420`。
- [ ] 若同步产生 `.new`/`.bak`，逐个核对并停止在未解决时继续。

### Step 4：验证语义与安装面

按实际命令入口执行并保留 stdout/exit code；命令通过不替代 AI semantic review：

```bash
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m unittest trellis/skills/guru-team/tests/test_skill_packages.py
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 1.1 --platform codex
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1 --platform codex
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5 --platform codex
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-04-174-thin-workflow-420
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
git diff --check
```

另外验证 canonical/dogfood workflow、source/installed registry graph、ownership 和
managed update/reapply 的结果；若仓库当前 README baseline 仍失败，单独标记为既有
基线，不把它改写为本 Issue 的 workflow 失败或成功。

### Step 5：Phase 2 semantic check 与 current-HEAD review

- [ ] 按 `guru-check-task` 覆盖完整当前 task scope、Docs SSOT Plan、workflow diff、
      graph/ownership/install/update evidence，并只接受其 `passed` exit。
- [ ] 对当前完整 diff 做独立 Branch Review 风格语义审查：确认压缩没有丢失 marker、
      route、唯一 consumer、stop、#161 contract 或 parser anchor；列出 P0-P3 findings
      和未验证边界。
- [ ] 若 source/test/docs 发生任何 post-review 变更，重新生成 current-HEAD check
      evidence，再做独立 review；不能复用旧结果。

## 3. 预期验证结论

- 新增证据：两份 workflow `<=420`、byte equality、完整 graph/ownership/install/update
  regression 与 current-HEAD semantic review。
- 历史证据：#132 combined acceptance 不重跑、不作为本 Issue 的完成证明。
- 非本任务基线：README 基线失败若仍存在，记录为独立 gap，不放宽本 Issue acceptance。

## 4. 发布边界

实现与验证完成后停止，后续明确授权前不执行 commit、push、PR、Issue close、archive、
cleanup 和 merge 不属于本实施计划的自动后续动作。
