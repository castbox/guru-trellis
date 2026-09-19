# #443 实施计划：task identity-centered multi-session binding

## 1. 实施前门禁

- [ ] `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan 完整非空。
- [ ] planning profile 的 contract wording review 通过；Architecture impact sync 明确记录新 capability 与 #434 boundary。
- [ ] plan approval 通过并得到当前对话 activation confirmation 后，才运行 `start-task.sh --mode initial`。
- [ ] 实现前重新读取 Issue #443、task identity、branch/worktree/base 与 current authority；任何漂移回到 Phase 1。

## 2. 有序实施步骤

1. **Current inventory**：读取 #438 attach、#436 Reactivate/Finish/Cleanup、Trellis session resolver、runtime mapping schemas、registry/manifest 与平台 projection，固定 single-writer 和禁止复用清单。
2. **Public package**：新增 `guru-bind-task-session` Interface、commands、schemas、examples、errors、consumer projections、package-local eval 与 tests；定义 `resume_current_task`、`rebind_missing_session`、`switch_task`、`reactivate_rebind`、`binding_blocked` exits。
3. **Deterministic runtime**：实现 live identity resolver、binding store、generation/freshness validator、idempotent rebind、revoke/route transition 与 zero-write mismatch paths；私有 runtime 只在 ignored namespace 写入。
4. **Semantic owner**：实现 AI review gate 输入合同，明确 resume/rebind/switch/reactivate 的 scope、route、authority 与 blocked 判断；不把脚本结果当作 semantic pass。
5. **Existing owner bridges**：在 #438 创建期 attach 与 #436 Reactivate 输出中增加最小 additive projection；更新 Finish/Cleanup 输入校验以拒绝旧 generation，但不复制 binding owner。
6. **Registry/workflow projection**：注册 canonical package、manifest/production contract、consumer declarations 与 selected platform copies；保持 #434 global graph 未激活，新增 route 只能由 #434 后续消费。
7. **Docs/architecture**：按 Docs SSOT Plan 更新 data/skill/workflow/quality contracts、architecture contribution/ADR、README 与 ownership inventory。
8. **Canonical→installed sync**：运行 preset apply/reapply，检查 `.new/.bak`、dogfood overlay drift、source/installed/platform byte parity 与 executable modes。
9. **Validation**：运行 package tests、cross-package fixtures、registry/graph checks、projection/ownership checks、task validation 与 `git diff --check`；环境缺失证据标记为 blocked/未验证。
10. **Semantic gates**：执行完整 `guru-check-task` 与独立 current-HEAD Branch Review；finding 修复后从 Phase 2 重新跑 check/review。

## 3. 重点验证命令

```bash
python3 -m json.tool trellis/index.json
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-19-443-task-identity-binding
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
git diff --check
```

另执行新增 package contract/runtime/eval、#438/#436 integration、registry/manifest/ownership、platform parity 与 representative A→B→A / cross-session / Reactivate fixtures。完整 throwaway/Release matrix 属于专门兼容性或 #434/#267 owner，不在本 Issue 自动扩张。

## 4. 文件所有权边界

- 新 package：`trellis/skills/guru-team/packages/guru-bind-task-session/**`。
- 现有 owner 的最小 additive bridge：#438 create-task-workspace、#436 reactivate/finish/cleanup 直接输入/输出与测试。
- registry/manifest/spec/architecture/preset projection 由主会话统一收敛。
- 只允许 task-local planning/check artifacts 与 ignored runtime binding 文件；不得写 Issue ledger、全局 lifecycle store、`.trellis/.developer` 或 `.trellis/workspace/**`。

## 5. 完成门槛与发布边界

只有 Phase 2 semantic check、完整 Branch Review、publication readiness 与 Finalizer 通过后才进入 commit/push/PR。实现阶段不自动提交、push、创建 PR、merge、关闭 Issue、激活 #434 或清理 worktree。

## 6.1 Issue revision: manual recovery

- [ ] 扩展 package input/semantic/public schemas，新增 `manual_recovery` profile、`manual_recovery` route 与 `session_manually_recovered` exit。
- [ ] 实现缺失 task/workspace mapping 时的 task-centered preflight：只接受 task.json、有效 worktree/branch/HEAD/base/repository common dir 与当前 session identity 全部一致。
- [ ] 以原有 mapping payload shape 重建 ignored task/workspace mappings，再调用官方 session writer 建立当前 binding；重复 recovery 返回同一 binding，不重复创建资源。
- [ ] 在恢复后重新执行 boundary validator；恢复不改变 task status，不产生 semantic/authorization/lifecycle 事实。
- [ ] 增加缺 mapping、wrong task/worktree、missing session、idempotent retry 与 zero-write mismatch 测试，并重新运行 Architecture/Phase 2 semantic gates。
