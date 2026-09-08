# #376 实施计划

## Ordered Checklist

1. 对照现有 `guru-reconcile-task-base` contract、workflow、quality guideline 与 test fixture，确认 integration/authority/task-content 三类事实的现状。
2. 在 canonical workflow/spec 与 reconcile package 中收敛独立时钟语义，保持现有 typed exits、consumer 和无关 base delta 的 `resume_target`。
3. 更新 dogfood、preset 及声明平台投影，确保 canonical source 与安装副本一致。
4. 增加/修订正向 fixture：无关 base delta 保持 `reconciled`；真实 authority/planning assumption 变化返回 `planning_stale`；`post_plan` 不因单纯 base 更新回退。
5. 运行 package contract/runtime/eval 定向验证和 source/projection 一致性检查。
6. 通过 Phase 2 check 后，再执行 commit、完整 Branch Review 与 publication readiness；本规划阶段不执行这些动作。

## Validation Commands

```bash
python3 -m json.tool trellis/index.json
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-07-376-reduce-base-interference
git diff --check
```

追加执行 `guru-reconcile-task-base` 的 canonical unittest、runtime subset、eval/contract discovery，以及 preset projection drift 检查。

## Risk Points

- 不能把 base freshness digest、integration delta 或 recorder 输出当作 semantic planning decision。
- 不能把无关 base delta 误路由为 `planning_stale`，也不能放宽真实 authority 变化的 stale 路径。
- 不能覆盖当前 workspace 之外的 `main` dirty 文件、既有 sidecar 或其他 task workspace。

## Pre-start Gate

- 规划文档完成且无阻塞 open question。
- `implement.jsonl` 与 `check.jsonl` 各有真实研究/验证条目。
- 用户明确批准本规划摘要后，才允许 `task.py start` 和实现。

## 2026-09-08 Base Reconciliation

1. 已将精确新基线 `d95f875cc4751c4487444b942901bf5023e44acc` 以 no-commit merge 方式集成，未创建 commit、未 push、未更新 PR。
2. 已保留新基线删除的 clarify-requirements 旧 eval typed-output 注入逻辑；Branch Review finding `BR-376-NATIVE-ADAPTER-3000` 要求移除 #376 的 task-local recipe alias，改由 fixture 复用已有 `base-reconciled`。
3. 已从 Git 三阶段 manifest 重建组合结果，并将 native adapter 哈希更新为当前 canonical/installed 一致字节。
4. 验证范围增加：reconcile package contract/runtime/eval、clarify package 回归、source/installed manifest 与 adapter identity、overlay drift、task/JSON/Python/diff/sidecar 检查。
5. 既存 #108 `.bak` sidecar 与 projection 漂移不属于 #376；不清理、不提交，也不把其全量 reapply 结果纳入本任务。

### Validation Result

- PASS：canonical 与 installed `guru-reconcile-task-base` 各 20 项单测。
- PASS：canonical 与 installed `guru-clarify-requirements` 各 11 项回归测试。
- PASS：reconcile source eval discovery 与 shared adapter 全 7 case；新增 `unrelated-base-delta-reconciled` 保留原 `resume_target`。
- PASS：source package closure（23 packages / 77 commands）、4,729 个 installed manifest 声明文件哈希、reconcile installed/四平台投影字节、workflow/spec/adapter identity、overlay drift、JSON/Python/task/scoped diff 检查。
- BLOCKED BOUNDARY：installed eval discovery 被 #376 范围外的既存 #108 installed projection/`.bak` sidecar 漂移阻断；未清理或吸收该状态。
- SUPERSEDED EVIDENCE：基线集成后的早期全候选 `git diff --check` 曾命中 #377 archive Markdown 的 EOF 空行；当前 finding-fix worktree 已重新执行全量 `git diff --check` 并通过，未修改 #377 归档内容。

## 2026-09-08 Branch Review Finding 修复计划

1. 将 canonical、installed 与 Agents/Codex/Claude/Cursor 的 `unrelated-base-delta-facts.json` staging recipe 从 `base-unrelated-reconciled` 改为已有 `base-reconciled`。
2. 从 canonical/installed `native_adapter.py` 删除 #376 新增的 alias 行，使完整 `origin/main...HEAD` 不再触碰该 6798 行共享文件。
3. 使用仓库现有确定性 manifest 计算/校验规则，更新 `.trellis/guru-team/extension.json` 中受影响文件哈希、`guru-reconcile-task-base` package tree、managed tree/provenance；保留 #377 与其他基线字段。
4. 定向验证 fixture JSON、六份 fixture 字节一致、canonical/installed adapter 字节一致、reconcile eval/contract、installed manifest、task artifact、scoped `git diff --check`，并确认 39 个 `.bak` 数量和内容未被修改。
5. 以 `git diff --name-only origin/main...HEAD` 和 adapter scoped diff 验证 subtraction-first 结果；不执行会吸收范围外 sidecar 的全量 reapply，不执行 commit、push、PR 或 cleanup。

### Branch Review Finding 修复结果

- PASS：六份 `unrelated-base-delta-facts.json` 已统一复用 `base-reconciled`；canonical/installed adapter 已删除 task-local alias，当前 worktree candidate 相对 `origin/main` 的 adapter diff 为空。
- PASS：canonical 与 installed `guru-reconcile-task-base` 各 20 项单测；canonical 与 installed `guru-clarify-requirements` 各 11 项回归测试。
- PASS：source contract discovery、7-case eval discovery 与 shared 7-case production eval；`unrelated-base-delta-reconciled` 仍返回 `reconciled` 并保留 `resume_target=task_activation`。
- PASS：source package closure（23 packages / 77 commands）、4,729 个 installed manifest 声明文件哈希、六份 fixture 与 canonical/installed adapter 字节一致、overlay drift、JSON/Python/task 与全候选 `git diff --check`。
- BOUNDARY：installed 全量 package validation 仍仅被既存 #108 Claude projection 与 39 个 `.bak` provenance drift 阻断；本任务未修改、删除或吸收这些 sidecar。
- BOUNDARY：未执行完整多平台 throwaway、upgrade/update、reapply 或 release-candidate 矩阵；其 owner 仍是专门兼容性或 Release Issue。

## 2026-09-08 Finalizer Base Reconciliation 结果

- Finalizer preview 对 `29ef6d482bb7c13bf65d23b1ffdb806c4afdc531` 返回 `base_reconciliation_required`，新 base 为 `81657210f5508186ed0f09098fdc63c927fdc307`；preview 无副作用。
- 已以 no-commit merge 集成新 base，唯一冲突 `.trellis/guru-team/extension.json` 按 JSON 结构解决：保留两侧 package/file inventory，保留 #376 当前 dirty provenance preimage，不运行全量 preset reapply。
- PASS：canonical reconcile 20/20、installed reconcile 20/20；canonical Discovery 16/16、installed Discovery contract/runtime 7/7 + 9/9。
- PASS：reconcile 与 Discovery package tree digest 和当前 manifest 精确一致；source package validation 23 packages / 77 commands；ownership、overlay drift、task artifact、JSON、Python compilation 与 `git diff --check` 通过。
- BOUNDARY：installed full validation 仍仅被 Issue #108 既存 approve/check/review Claude projection 与 digest provenance drift 阻断；39 个 `.bak` 未修改、未删除、未提交。
- ROUTE：不重新规划或重新实施 #376 业务行为；对本次 tracked manifest composition 运行 fresh Phase 2、Task Commit、完整 Branch Review 与 Publication 后恢复 Finalizer。
