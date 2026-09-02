# Implementation: canonical 与 dogfood 投影漂移修复

## 1. 实施顺序

1. 重新确认 #334 worktree boundary、base、Issue authority 和 #333 排除边界。
2. 将 `.trellis/spec/workflow/data-contracts.md` 中仅属于 #325 的四段差异补入
   canonical preset spec，不复制其它无关内容。
3. 保持 canonical Finalizer test 不变；核对它同时包含 #325 manifest-preservation
   断言和 #327 workspace-boundary 回归。
4. 审核首次 apply 生成的 installed test `.new`：校验其 SHA 与 canonical 相同，
   并对照 PR #326/#328 证明 installed-only 差异没有需要保留的新语义。
5. 仅将该已审核 `.new` 替换到对应 installed test 并删除该 `.new`；写入前再次运行
   workspace-boundary guard。其它 `.new`、未知 edit 或额外冲突立即停止。
6. 执行 `apply.sh --repo . --all-platforms --json`，审核所有生成文件和 sidecar，
   确认 current manifest 已重新记录 canonical bytes。
7. 按 known managed-upgrade 规则处理本次 apply 产生且已审核的 `.bak`；任何新
   `.new` 或未知冲突停止并返回 owner。
8. 再次执行同一 apply，证明 reapply 幂等。
9. 运行 installed package test、ownership、source/installed validation、dogfood
   drift、platform parity、task validation、`git diff --check` 与零 sidecar 扫描。
10. 审核完整 worktree diff，确认不包含 #333、Release、部署、runtime/public
   interface/schema 变更。

## 2. 预计变更文件

手工修改：

- `trellis/presets/guru-team/spec/workflow/data-contracts.md`

受控 conflict resolution：

- `.trellis/guru-team/skills/packages/guru-finalize-task/tests/test_contract.py`
- `.trellis/guru-team/skills/packages/guru-finalize-task/tests/test_contract.py.new`
  仅作为已审核临时后像，解决后不得保留或提交。

由 preset apply 生成：

- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/guru-team/skills/packages/guru-finalize-task/tests/test_contract.py`
- `.agents/skills/guru-finalize-task/**`
- `.codex/skills/guru-finalize-task/**`
- `.cursor/skills/guru-finalize-task/**`
- `.claude/skills/guru-finalize-task/**`
- `.trellis/guru-team/extension.json` 中与本次 managed projection 对应的 provenance
  inventory。

实际 stage 范围必须以 apply 后的 reviewed diff 为准，不提交 `.new`/`.bak` 或无关
生成变化。canonical Finalizer test 预期无 diff。

## 3. 定向验证

```bash
python3 trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json
python3 .trellis/guru-team/skills/packages/guru-finalize-task/tests/test_contract.py
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-02-334-canonical-dogfood-projection-drift
git diff --check
find . -type f \( -name '*.new' -o -name '*.bak' \) -not -path './.git/*'
```

同时使用 source/installed validator 的当前仓库入口验证 package inventory、声明
平台字节和 executable modes。完整 Throwaway release matrix 不在本任务运行。

## 4. Phase 2 调度

- Implementation worker 只拥有两处 canonical 手工修改及 apply 生成投影。
- Check worker 独立核对 Issue #334 acceptance、完整 diff、两套 package tests、
  ownership/drift/parity/sidecar 结果和 #333 排除边界。
- 任一 worker 发现超出规划的 runtime、schema、interface 或 release 需求时，停止
  并进入 scope/plan re-entry，不自行扩张。

## 5. 完成门禁

- 只有最新规划经用户确认后才运行 `task.py start` 和实现。
- Phase 2 `guru-check-task` 通过后才进入独立 task commit 确认。
- commit、push、PR、merge 分别使用 fresh preflight 与独立确认。
- 最终报告明确未执行完整 release-wide 多平台矩阵。
