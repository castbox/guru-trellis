# #376 技术设计

## 1. 设计目标

把“基线已前进”拆成集成事实，把“任务是否仍可按原规划继续”保留为 authority/task-content 判断。这样并行任务可以记录新的 base，而不把无关集成变化升级为规划失效。

## 2. 影响边界

- Canonical：`trellis/workflows/guru-team/workflow.md`、`trellis/skills/guru-team/packages/guru-reconcile-task-base/`。
- Durable spec：`trellis/presets/guru-team/spec/workflow/quality-guidelines.md`。
- Projection：`.trellis/workflow.md`、`.trellis/spec/workflow/quality-guidelines.md`、preset/Agents/Codex/Claude/Cursor 对应同步文件。
- Tests：reconcile package 的 contract/eval/runtime fixtures。

## 3. 状态模型

1. 读取旧 base 与新 base，形成 integration clock delta。
2. 独立比较 live Issue、approved planning assumption、accepted scope 与 task content，形成 authority/task-content clock 结果。
3. 若 authority/task-content 未变：返回既有 `reconciled`，保留原 `resume_target`，允许继续当前阶段。
4. 若 authority/task-content 变更：沿现有 `planning_stale` 或既定 owner route 处理，不由 integration delta 覆盖判断。
5. `post_plan` 只在第 4 步成立时回 Planning。

## 4. 兼容性与 SSOT

- 不新增 exit；沿用现有 typed exits 与 consumer。
- 不把 base digest 当作 planning authority；digest 只用于确定性 freshness/identity 校验。
- canonical Markdown 是流程语义来源，package runtime 仅实现确定性状态读取与结果校验。
- 生成/管理投影需保持字节或合同要求的一致性，避免只修 dogfood 副本。

## 5. 回滚与风险

- 主要风险是把真实 Issue/assumption 变化误判为无关 base delta，导致 stale 被吞掉；通过正反 fixture 同时断言避免。
- 若 projection 或 runtime contract 不一致，停止在 check/branch review，不通过局部绕过。
- 回滚边界为本任务新增/修改的 canonical contract、projection 和测试文件；不触碰其他 dirty 改动。

## 6. 基线演进兼容设计

- 2026-09-08 将 `origin/main@d95f875cc4751c4487444b942901bf5023e44acc` 集成到任务分支。新基线保留 #377 对 `guru-clarify-requirements` 调用与 eval staging 的收敛，不恢复被删除的旧 typed-output 注入路径。
- Branch Review finding `BR-376-NATIVE-ADAPTER-3000` 识别出 `base-unrelated-reconciled` 只是 task-local fixture 别名，没有独立生产消费者，却让 #376 修改 6798 行共享 adapter。按 subtraction-first 合同，`unrelated-base-delta-facts.json` 直接复用已有 `base-reconciled` recipe，并删除 canonical/installed adapter 中 #376 新增的 alias 行。
- `.trellis/guru-team/extension.json` 通过 canonical/installed 组合字节重建：同时承接 #376 reconcile 资产与 #377 clarify 资产，并绑定组合后的 native adapter 哈希。
- 新基线已存在但与 #376 无关的 #108 projection/sidecar 状态不纳入本任务，不通过 reapply 扩张为额外变更；完整 upgrade/reapply/Release 矩阵仍由专门 Issue 负责。

## 7. Branch Review Finding 修复

- Finding：`BR-376-NATIVE-ADAPTER-3000`。
- Replacement：保留无关 base delta 的独立 fixture 场景与 `reconciled` 断言，但 staging 复用现有 `base-reconciled`，不再扩展共享 native adapter recipe 表。
- Diff boundary：当前未提交 worktree candidate 相对 `origin/main` 已不再包含 `trellis/skills/guru-team/adapters/eval/native_adapter.py`；finding-fix commit 后的完整 `origin/main...HEAD` 也必须保持该结果。installed adapter 与 canonical 保持字节一致。
- Provenance：仅按当前 canonical/installed 字节更新 `.trellis/guru-team/extension.json` 的相关 managed file hash、package tree 和 source provenance，保留 #377 与其他基线记录。
