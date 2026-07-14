# #122 实施计划

## 1. 前置状态

- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`
- Branch：`feat/122-guru-create-task-commit`
- Base：`main`，任务创建时与 `origin/main` 同步到
  `6b9495a17dc953c7a54c105e39c23a786edcd8a7`
- Task：`.trellis/tasks/07-13-122-guru-create-task-commit`
- Primary issue：#122
- Related only：#92、#120
- Dispatch mode：`sub-agent`

## 2. Durable docs first

- [ ] 按 `design.md` 的 `Docs SSOT Plan` 更新 requirements、flow、workflow/preset
  specs 与三个公共 README。
- [ ] 明确 `guru-create-work-commit` reserved tombstone 与
  `guru-create-task-commit` active migration。
- [ ] 把 commit flow 图从直接 Phase 3.4 commit 改成 mandatory skill invocation
  与 typed exits。
- [ ] 把 artifact、candidate validator、exact executor、postcondition、re-entry、
  安装/升级合同写入 durable owner。
- [ ] 对无需字节修改的 evidence path 在 implementation handoff 写入复核理由。
- [ ] 在 runtime/schema/installer edit 前完成本节。

## 3. Canonical active package

- [ ] 更新 `trellis/skills/guru-team/registry.json`：保留旧 reserved id，增加新
  active id。
- [ ] 创建 `packages/guru-create-task-commit/` 的 `SKILL.md`、`interface.json`、
  `references/contract.md`、schema、example、thin scripts 与 package test。
- [ ] Frontmatter description 覆盖 task commit、Phase 2 changes、finding fix、
  revision commit 四类 standalone trigger。
- [ ] Interface 声明统一 preconditions、固定 ordered stages、artifact/schema、
  objective validator、三条 exits 与 shared/Codex/Cursor/Claude destinations。
- [ ] Package scripts 只委派 installed companion commands，不实现 parser 或 scope
  判断。

## 4. Candidate validator 与 exact executor

- [ ] 在 canonical Python runtime 增加 task commit artifact constants、schema loader、
  NUL-delimited Git snapshot、plan digest 与 evidence validator。
- [ ] 扩展 `check-commit-messages` argparse，增加与 range mode 互斥的
  `--candidate-artifact`。
- [ ] Candidate mode 复用 `validate_commit_message()`，并验证 task/issue/Phase 2/
  `HEAD`/snapshot/exact stage/message/AI Review/authorization。
- [ ] 修改 `check-phase2-check` 的 dirty comparison，只豁免当前 schema-valid
  candidate artifact。
- [ ] 新增 Python `create-task-commit` subcommand 与 managed Bash wrapper。
- [ ] Executor 使用 literal pathspec、exact index equality、`--cleanup=verbatim -F`、
  raw commit object validation 与 unrelated snapshot comparison。
- [ ] Executor 原子写回 result；failure 保留 Git 现场且返回 `blocked`，不执行
  reset、stash 或 history rewrite。
- [ ] 保持 range mode、metadata/merge validator 与 formatter 兼容。

## 5. Workflow、prompt 与 Branch Review 收敛

- [ ] 在 canonical workflow Phase 3.4 写入唯一 invocation marker 与三条 exit
  marker。
- [ ] Initial commit 和 finding-fix route 都必须经过 Phase 2 后进入同一 skill。
- [ ] 删除 Phase 2 planned message review、Phase 3.4 direct stage/commit、Branch
  Review 的 work message template。
- [ ] 更新 canonical continue overlays，只保留 stable skill load/invoke/exit route。
- [ ] 增加 contract scan，阻塞 workflow/platform entry 再次复制 step-local 正文或
  直接 task work commit。

## 6. Installer、manifest 与 dogfood

- [ ] 把 `create-task-commit.sh` 加入 `MANAGED_ASSET_PATHS` 与 executable list。
- [ ] 把 active package 交给现有 exact managed-hash installer 分发，不新增 overlay
  heuristic。
- [ ] 更新 `trellis/guru-team-extension.json` 到 `0.6.5-guru.5`，登记 skill id、
  artifact/schema 与 executor public API。
- [ ] 更新 preset/workflow README 的 installed files、discovery、upgrade/reapply
  命令。
- [ ] 运行 canonical preset apply `--repo . --all-platforms` 同步 dogfood workflow、
  runtime、installed registry/package、shared/Codex/Cursor/Claude copies 与 manifest。
- [ ] 逐个核对并处理 `.new` / `.bak`；未处理 sidecar 阻塞 Phase 2 pass。

## 7. Test implementation

- [ ] 扩展 `test_guru_team_trellis.py`，覆盖 candidate/executor positive 与 negative
  matrix。
- [ ] 扩展 `test_skill_packages.py`，覆盖 production active package、markers、trigger、
  interface/schema/example/test 与 duplicate-contract scan。
- [ ] 扩展 preset tests，覆盖 active package platform distribution、managed upgrade、
  unknown edit、platform shrink、manifest inventory、wrapper executable。
- [ ] 扩展 throwaway verifier，真实执行 initial commit 和 finding-fix revision commit，
  再执行 update/workflow/preset reapply。
- [ ] 增加 hook extra path、unrelated staged path、message byte mismatch、old artifact
  reuse、path with spaces/Unicode/metacharacter regression。

## 8. Phase 2 implementation/check evidence

- [ ] 主会话重新运行 workspace boundary 与 planning approval validator。
- [ ] 派发 `trellis-implement`；记录 `assigned`、progress 与 `completed` liveness。
- [ ] Implementation handoff 必须记录 `ssot_first` 执行结果、durable docs sync、
  task delta merge、task-history-only 内容、实现输入与剩余风险。
- [ ] 派发独立 `trellis-check`；记录 `assigned`、progress 与 `completed` liveness。
- [ ] Checker 必须覆盖 R1-R10、AC1-AC14、Docs SSOT、public API、candidate/executor、
  security、deployment、install/update/throwaway。
- [ ] Finding 必须由实现代理修复，再由 checker 复核；planning docs 改动必须重新取得
  post-planning approval。
- [ ] AI check 完成后，主会话记录并验证 `phase2-check.json`。

## 9. 使用新 Skill 创建本任务 work commit

- [ ] 通过 canonical mandatory route 加载 dogfood installed
  `guru-create-task-commit`。
- [ ] AI 读取完整 dirty state，写入本任务首个
  `task-commit-plans/<sequence>.json`，完成 AI Review Gate。
- [ ] 当前会话若缺 commit side-effect authorization，展示 exact stage scope 与副作用，
  获得用户确认后记录 authorization source。
- [ ] 运行 candidate validator；plain range `checked_commits=[]` 不得满足该 gate。
- [ ] 运行 exact executor，并验证 `committed` exit、raw message bytes、parent、paths、
  unrelated preservation 与 result artifact。

## 10. Branch Review Gate

- [ ] Work commit 后派发独立问题发现审查代理，审查
  `origin/main...HEAD` 完整 committed diff。
- [ ] 审查报告使用 task-local 中文 `reviews/*.md`，`review.md` 汇总所有轮次。
- [ ] 任一 P0/P1/P2/P3 finding 都返回实现与 Phase 2；每个 finding-fix work commit
  必须再次调用 `guru-create-task-commit`，不得复用旧 artifact。
- [ ] Finding owner 完成 closure review 后，派发 fresh 最终放行审查代理。
- [ ] 主会话记录 agent assignment/reuse 与 Branch Review Gate；0 findings 才能 pass。
- [ ] Gate 后停止，不在 `trellis-continue` 中 push、创建 PR 或调用 finish-work。

## 11. Validation commands

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json \
  --task .trellis/tasks/07-13-122-guru-create-task-commit

.trellis/guru-team/scripts/bash/check-planning-approval.sh --json \
  --task .trellis/tasks/07-13-122-guru-create-task-commit

python3 -m unittest \
  trellis/skills/guru-team/tests/test_skill_packages.py \
  trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py

python3 -m py_compile \
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py

bash -n \
  trellis/workflows/guru-team/scripts/bash/*.sh \
  trellis/presets/guru-team/scripts/bash/*.sh \
  trellis/skills/guru-team/packages/guru-create-task-commit/scripts/*.sh

python3 -m json.tool trellis/index.json
python3 -m json.tool trellis/skills/guru-team/registry.json
python3 ./.trellis/scripts/task.py validate \
  .trellis/tasks/07-13-122-guru-create-task-commit

trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh \
  --json --mode source

trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh

python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.2
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.4
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5

git diff --check
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
```

## 12. Docs SSOT checkpoint

- Strategy：`ssot_first`。
- Runtime/schema/installer edit 前，`design.md` 第 14 节列出的 durable docs 必须完成
  首轮同步。
- Final Phase 2 check 前，implementation handoff 必须证明 task delta 已合并到 durable
  owner，task-history-only 事实没有进入公共 package。
- Durable docs、task artifacts、workflow、runtime、schema、package、tests、installer、
  dogfood copies 出现语义漂移时，Phase 2 不得 pass。

## 13. Rollback points

| Checkpoint | 阻断动作 |
| --- | --- |
| Durable docs 未形成唯一 owner | 不编辑 runtime/schema/installer |
| Source skill validation 失败 | 不执行 preset apply |
| Candidate/executor unit test 失败 | 不同步 dogfood |
| Unknown local skill edit | 保留原文件与 `.new`，暂停并请求处理 |
| Dogfood drift 或 sidecar 未清理 | 不记录 Phase 2 pass |
| Throwaway initial/revision commit 失败 | 不创建本任务 work commit |
| Postcondition 或 hook mutation 失败 | 返回 `blocked`，不自动改写历史 |
| Branch Review 存在 finding | 返回实现和 Phase 2，再次走 commit skill |
| Remote verifier 未通过 | 不创建 ready PR，不宣称开箱即用完成 |
