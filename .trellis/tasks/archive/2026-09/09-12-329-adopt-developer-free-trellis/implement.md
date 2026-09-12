# #329 实施计划

## 执行顺序

1. 完成 Planning wording、normal-scenario、solution-mechanism、RDT/Architecture planning impact 和
   `guru-approve-task-plan`；展示本计划并取得后续明确实施确认后才运行 task start。
2. 准备固定 `castbox/Trellis@a2003296...` checkout，核验 CLI `0.6.17`、pnpm lock 和 source
   marker；运行上游 build/test 的最小 source admission，不使用全局/npm fallback。
3. 建立 legacy absent/present-A/present-B、用户修改、三平台和 current task-worktree 的 before
   snapshot；分类 active production、negative fixture、generated migration stub、current docs 与 history
   中的旧机制引用。
4. 将 canonical source lock 和所有直接 version/source consumers 更新到 `a2003296...` / `0.6.17`；
   保持 Guru extension/repository release 轴独立，不创建新 tag/Release。
5. 使用固定 CLI 的正式 update/migrate/generation 替换 Trellis-owned dogfood 文件；审查 managed
   removals、`.new/.bak`、用户修改和 retired stub，禁止手工生成文件补丁成为最终来源。
6. 直接演进 Guru installer/runtime/contracts：移除 identity/journal/index/session-recording/`--mine`
   的 active consumer；task creation 显式传 creator/assignee；保留并澄清 task checkout/worktree
   mapping authority；同步必要 schema consumer migration。
7. 更新 canonical Guru tests/fixtures 和 Docs SSOT Plan 列出的 durable specs/README；历史 archive、
   superseded authority 和 legacy data 不修改。
8. 运行 preset apply 同步 dogfood 和 Codex/Claude/Cursor 投影；逐个处理 sidecar，执行 ownership、
   source/installed validation、manifest/graph parity 和 drift。
9. 运行完整 Issue matrix：clean install、existing update、第二次 update/reapply、linked worktree、
   new session、resume、task creation、planning、implementation/check、commit/review/publication/
   finalization/archive 代表链路，以及 legacy bytes/结果一致性验证。
10. 由 RDT/Architecture owner 审核 contribution；仅当审核结论要求更新 shared current 时执行
    serialized promotion。promotion-created diff 重新执行 fresh Phase 2、
    task commit 和独立 full-diff Branch Review，再进入 Publication/Finalizer。commit、push、PR、merge、
    tag、Release 均使用各自后续确认。

## Phase 2 Dispatch Ownership

- Worker A：固定 source build、Trellis-generated update/migration 与 upstream-owned diff 审核。
- Worker B：Guru canonical runtime/installer/Skill consumer cleanup 与 focused tests。
- Worker C：Docs SSOT contribution、README/spec/version projection 和 historical-boundary audit。
- Checker：独立执行完整 task scope、三平台 installed matrix、legacy preservation、subtraction 与
  canonical/dogfood/installed parity，不复用 implementation 结论。

各 worker 写入范围在 Phase 2 dispatch 前按实际文件 inventory 划分为不重叠集合；不得修改其他
worker 的文件或回退并行改动。

## 关键验证命令

```bash
python3 -m json.tool trellis/presets/guru-team/source/trellis-source.json
bash trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-12-329-adopt-developer-free-trellis
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
git diff --check
```

定向与完整 matrix 使用现有 preset verifier/test runner，由实现后的 live inventory 决定精确测试文件；
不得用少量 grep 或 unit PASS 代替 Issue 明确要求的 clean/update/reapply/platform/lifecycle 证据。

## 实施 checkpoint

- [ ] source checkout HEAD/version/package-manager/source marker 一致，无 fallback。
- [ ] Trellis-owned 文件来自固定 `0.6.17` 正式 generation/update。
- [ ] Guru active consumers 不再读取或写入旧 identity/workspace/journal/index。
- [ ] explicit creator/assignee 与 task-worktree current-task resolution 通过。
- [ ] legacy absent/present-A/present-B 结果一致且 present bytes/modes/paths 不变。
- [ ] canonical/dogfood/installed/Codex/Claude/Cursor 一致，无 unresolved sidecar。
- [ ] RDT/Architecture contribution 与实现、测试、version/source mapping 对齐。
- [ ] Phase 2、commit 后独立 Branch Review 和 Publication 均重新读取完整当前证据。

## 风险文件与回退点

- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：installer 与 managed
  migration 主路径，修改前后必须跑 transaction/update/reapply regression。
- `trellis/presets/guru-team/scripts/python/verify_installed_parallel_finish.py` 及完整 verifier：旧
  journal/session fixture 需重写为 task-only lifecycle，不能只删除断言。
- `trellis/skills/guru-team/packages/guru-create-task-workspace/**`：creator/assignee adapter 与 result
  schema consumer 必须同批迁移。
- upstream-managed `.trellis/scripts/**` 和平台 stock hooks：只由固定 CLI 生成；失败时恢复本 task
  candidate 或重新生成，不手工混合版本。

## 未授权动作

本计划不授权 task start、产品代码修改、commit、push、PR、merge、tag、Release 或清理临时/历史
资源。最新规划摘要经用户再次明确批准后才进入 Phase 2。
