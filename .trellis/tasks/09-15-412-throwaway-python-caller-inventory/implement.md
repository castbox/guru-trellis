# #412 实施与验证计划

## Phase 1

- [x] 完成 fresh base、live #412/#410、duplicate、clarification、wording 和 readiness intake。
- [x] 创建唯一 task、branch 和 worktree，并保持 task 状态为 `planning`。
- [x] 编写 `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan。
- [x] 在原 caller-inventory scope 上完成 wording、Planning Architecture、scenario/mechanism qualification 与 `guru-approve-task-plan`；该结果因 Phase 2 发现 projection stale 和 live Issue scope change 而失效，不再作为当前 approval。
- [x] 通过 live Issue #412 body edit接纳六处 `.52` projection repair，并 fresh 回读 external authority。
- [x] 基于 fresh `origin/main@6b97d4c7d659105a7a0d443946f89ba42866b72b` 完成 Discovery Refresh；`context_ready` result 为 `46a7f9704c2d889173808a05d8a91e0fe812e2e0f1f9f3e8745dad1618594f60`。
- [ ] 校验 active-task scope update 与 task planning identities，完成 `guru-clarify-requirements` 的 current re-entry。
- [ ] 对扩展后的三份 planning artifacts 重跑 wording review，要求 retained hit 有确定性分类且 unchecked hit 为 0。
- [ ] 分别完成 Architecture/RDT `repair` semantic owners，并验证六个 projection/README 导航的精确 repair contract。
- [ ] 重跑 Architecture 与 RDT `task_impact_sync(stage=planning)`，仅消费 fresh current typed exits。
- [ ] 对扩展后的 acceptance、projection stale scenario 和两个实现机制运行 fresh qualification owners。
- [ ] 重新完成 `guru-approve-task-plan` 八维审查并展示 approved plan；取得新的明确确认后才继续 projection 实现。

## Phase 2 实现

1. 由 RDT owner 基于 reviewed #410 contribution、`.52` Requirements/Test 正文、Architecture `.52/active` 和 release contract 决定唯一 D410/T410 投影；不得预设编号集合。
2. 只在授权的 authority 文件内统一 contribution Design/Test/traceability、`.52` Design main、三层 `.52/traceability.md` 与 manifest 的 identifier 集合、Architecture inheritance、双向 trace closure 和唯一 promotion state，并运行 RDT repair checker。
3. authority checker 通过后，以收敛后的 live `.52` authority 为 source，精确修复六个 stale projection/README 导航：
   - Architecture usage projection 的 version/source binding；
   - RDT usage projection 的 version、Architecture inheritance、source binding 与 freshness wording；
   - public-docs 的 current knowledge authority；
   - Requirements README 的 current source/manifest/trace wording及 `.52 active` / `.51 superseded` 导航；
   - Design README current table 的 `.52 active` / `.51 superseded` 导航；
   - Test README 的 #410 source wording及 `.52 active` / `.51 superseded` 导航。
4. 从当前 worktree 重新运行 source inventory discovery/check，记录完整新旧 identity。
5. 解析 canonical JSON，通过旧 `id` 与完整旧 `anchor_sha256` 唯一定位 object，并保存其非目标字段及数组索引作为前后比较基线。
6. 只替换该 object 的 `id` 和 `anchor_sha256`，并将完整同一 object 从 registered index 9 移到 discovery index 7；保持其他 object 相对顺序，不格式化无关 JSON、不修改 verifier/helper。
7. 使用 JSON parser 和精确断言验证旧值 0 次、新值 1 次、目标 object 位于 index 7、非目标字段未变化且其他 object 相对顺序未变化。
8. 运行 preset apply/reapply；只保留 canonical installer 合法生成且在 Issue 范围内的 projection，拒绝未知 tracked/sidecar mutation。
9. 对历史边界运行定向 diff review：仅授权的 `.52` authority/current projection 改变，`.51` 与更早版本化 authority 文件零修改，合法 predecessor/released-history 文字保留。

## Phase 2 验证

以下命令的精确参数在执行前从当前 `--help`、Issue #412 和 release contract 重新读取：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 trellis/presets/guru-team/scripts/python/verify_throwaway_python_routing.py check-inventory --repo-root . --inventory trellis/presets/guru-team/tests/throwaway-python-callers.json --json
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
git diff --check
git status --short
```

完整验证集合：

- source caller inventory tests 与 installed caller inventory tests。
- Shared、Codex、Claude、Cursor 四平台 projection parity。
- focused clean throwaway initial install。
- existing-project update/reapply、workflow preview/switch 和 preset reapply。
- dogfood drift、ownership、unexpected mutation 与 `.new/.bak` 检查。
- changed-file secret scan。
- 递归 bytecode/residue hygiene；只报告预存 residue，不擅自删除非任务资源。
- fresh Architecture `task_impact_sync(stage=phase2)` 与 `guru-check-task`；P0-P3 finding 必须全部关闭。
- fresh RDT authority repair 证明 contribution、`.52` Design/Test/traceability 与 manifest 对 D410/T410、Architecture inheritance、三层 trace closure 和 promotion state 无冲突。
- fresh Architecture/RDT projection `repair` 结果与已收敛的 live `.52` authority 一致；Phase 2 不得消费 scope-change 前的 freshness、approval 或 release evidence。

## Phase 3

1. 展示 exact staged paths、HEAD、中文 Conventional Commit message 和 commit 命令，取得独立确认后调用 `guru-create-task-commit`。
2. 对提交后的完整 `origin/main...HEAD` diff 调用独立 Branch Review；不得以主会话自审替代。
3. 如有 finding，回到 Phase 2 修复、重新 commit 并对完整新 HEAD 重做 Branch Review。
4. 完成 Publication、Finalizer 和 preparation PR；PR 标题/正文使用中文，并按 live authority 决定 #412 的关闭语义。
5. push、PR create、merge 均在展示精确目标后分别取得确认。

## Post-Merge #410 交接

1. 回到 release authority checkout，fresh fetch `origin/main` 并验证 local/remote/GitHub main。
2. 冻结新的 exact candidate commit 与 tree；不得沿用 `6b97d4c7` 的任何 release evidence。
3. 在该 candidate 上从零执行 #410 当前 release contract 的 lineage、mapping、source/installed、四平台 parity、ownership、focused install/update/reapply、secret 和 residue gates。
4. 到此停止：不创建 tag、GitHub Release，不关闭 #410。

## 回滚与停止

- 未 commit 时只撤销本任务明确修改的行或 installer 生成的本任务 projection，不触碰用户/其他 task 改动。
- commit 后的任何修订通过新 finding-fix commit 完成，不重写已发布历史。
- Issue/base/HEAD/authority 漂移、范围扩大、验证 `FAIL`/`SKIP`、未知 sidecar 或 secret 命中均立即停止并报告。
