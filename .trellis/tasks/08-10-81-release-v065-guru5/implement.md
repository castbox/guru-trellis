# #81 v0.6.5-guru.5 执行计划

## Phase A：Release preparation 实现

1. 重新读取 task worktree 的 live issue/main/tag/release/manifest facts，确认未漂移。
2. 搜索所有 current stable `.3/.4`、extension revision `0.6.5-guru.25` 与 release identity 断言；区分 durable stable mapping、历史说明和 fictional fixture。
3. 将 canonical extension revision 提升到 `0.6.5-guru.26`。
4. 更新 workflow/preset README 的 `.5` pinned install、workflow switch、preset clone/apply、update/upgrade/reapply 和版本轴说明；删除对历史 `.3` 的 current-stable 声明。
5. 更新直接依赖 current stable source/revision 的 examples、assertions 和 tests；不把未知 future candidate SHA 写成常量。
6. 运行 canonical preset apply，同步 dogfood installed manifest/copies；逐项处理 `.new/.bak`，禁止静默覆盖未知 local edits。
7. 运行针对性 tests、package/registry/interface/schema/ownership/overlay/dogfood/sidecar 检查和 `git diff --check`。

## Phase B：Guru Team task 闭环

1. 使用 Trellis implementation sub-agent 实现 Phase A；主会话负责 scope、canonical/installed 协调与修正。
2. 使用独立 Trellis check sub-agent 检查完整 current task diff，再由主会话执行 `guru-check-task` semantic gate。
3. 自动创建 scoped local task commit；执行 independent current-HEAD Branch Review 和 publication readiness。
4. Finalizer 前展示 exact push/remote verification/PR/archive/Ready 计划并取得确认。
5. Preparation PR 必须中文且只 `Refs #81`；Finalizer 返回 Ready 后单独展示 merge plan 并取得确认。
6. Merge 后只读验证 PR=MERGED 且 #81 仍 Open。Task archive/merge 不视为 release 完成。

## Phase C：Post-merge candidate freeze

1. 从 source checkout 重新执行 `guru-sync-base`，读取 remote `main`、#81、PR、tags/releases。
2. 冻结唯一 candidate OID，记录 release-owned tree/content identity。
3. 使用 exact remote candidate ref 执行完整 clean throwaway pre-tag matrix：
   - workflow init；
   - existing workflow preview/switch；
   - preset initial apply；
   - 15 Skills / 57 exits / 33 targets 与 registry/interface/public contracts；
   - source/installed schemas、inventory、hashes、modes、sidecars；
   - representative workflow/standalone probes；
   - #180 Finalizer/PR Merge happy/recovery fixtures；
   - official `trellis update` 后 workflow/preset reapply；
   - `.4 → candidate` upgrade/reapply；
   - dogfood drift 与 README command execution。
4. 任一 required gate 非 PASS 时停止在 tag 前。

## Phase D：Tag 与 tag-pinned gate

1. Live revalidate candidate、远端 tag absence、annotated tag message/target。
2. 展示 exact `git tag -a v0.6.5-guru.5 <candidate>` 与 `git push origin refs/tags/v0.6.5-guru.5` 计划并取得确认。
3. Push 后读取 tag object 与 peeled commit，验证 peeled commit 等于 candidate。
4. 使用 `gh:castbox/guru-trellis/trellis#v0.6.5-guru.5` 重跑 Phase C 的完整 matrix；额外证明 installed manifest revision、source tag object/peeled commit 与 package/runtime inventory 一致。

## Phase E：Release 与 Issue closure

1. 基于 tag-pinned PASS 编写中文 Release notes，包含 #180 用户可见变化、`.4 → .5` 命令、精确版本映射、验证范围/限制、安全/部署影响与 #195 非目标。
2. 展示 exact `gh release create` target/title/body 和副作用，取得确认后发布非 draft、非 prerelease Release，并 live reread。
3. 生成去敏 evidence summary，展示 exact #81 comment 与 close plan，取得确认后先 comment、再 close。
4. Live reread #81=Closed、Release=published、tag/release/candidate identity 一致；仅此时报告 #81 完成。

## 验证命令族

- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-10-81-release-v065-guru5`
- `python3 trellis/skills/guru-team/tests/test_skill_packages.py`
- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- `python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`
- `trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`，通过 `TRELLIS_WORKFLOW_SOURCE` 绑定 candidate/tag source
- `git diff --check`

完整 matrix 的实际命令、exit code、精确 ref/OID、通过项和未验证边界在执行时从 live scripts/contracts 生成，不在计划中伪造预期 PASS。

## 风险文件与回滚点

- `trellis/guru-team-extension.json`：extension revision SSOT。
- `trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`：公开 stable source/upgrade SSOT。
- verifier examples/tests：不得把 future candidate SHA 或 pre-tag evidence 固化为错误 authority。
- `.trellis/guru-team/extension.json` 与平台 installed copies：只能由 canonical apply 同步。
- Tag push 是不可移动边界；push 前以完整 pre-tag PASS 为最终 stop condition。
