# #397 实施计划

## 顺序

1. 在每次写入前运行当前任务 workspace boundary 检查；读取 live #397、当前代码和 spec。
2. 在 package tests 增加真实未初始化 gitlink fixture。先在未修复函数上运行，证明失败发生在
   validation loop 之前，且 marker 未产生、任务状态保留、临时 worktree 清理。
3. 修改 `index_tree_digest` 的 `160000` 分支，并在 Branch Review `tree_identity` 承接同一行表示。
   保留所有其它 entry 行和现有身份比较；证明 validation marker 产生及下游 continuity 通过。
4. 补充 OID 更新、父仓缺少子模块对象、blob-backed mode 字节一致性、验证非零结果及真实持久整合测试。
5. 在既有跨 owner fixture 中先复现 Branch Review 摘要不一致，再通过实际 producer 输出及
   recorder/checker/invoke 验证修复。更新两包合同，Branch Review 引用 Reconcile 表示；不扩展共享 workflow/spec。
6. 通过 preset 同步本任务 worktree 的 dogfood；执行 reapply、drift 与一次代表性干净安装验证。
7. Phase 2 使用 fresh Architecture stage 与独立 check，核对完整 R1-R7、源码及安装差异。
8. 交付实现与验证结果；commit、push、PR、合并、发布和业务升级不在本阶段执行。

## 写入集合

- `trellis/skills/guru-team/packages/guru-reconcile-task-base/runtime/common.py`
- 同 package 的 `tests/test_runtime.py` 和 `references/contract.md`
- `trellis/skills/guru-team/packages/guru-review-branch/runtime/common.py`
- `trellis/skills/guru-team/packages/guru-review-branch/references/contract.md`
- `trellis/skills/guru-team/tests/test_base_continuity_integration.py`
- 上述 canonical 内容通过 preset 生成的 dogfood/声明平台受管投影及安装 manifest
- 本任务规划文档、`implement.jsonl`、`check.jsonl` 与任务状态

不手改源 checkout，不改其它任务、不改业务仓、不增加永久证据文件。
非生成代码文件保持小于 3000 行。

## 验证命令与观察

从当前任务 worktree 执行：

```bash
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-reconcile-task-base/tests -v
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-review-branch/tests -v
python3 -m unittest discover -s trellis/skills/guru-team/tests -p test_base_continuity_integration.py -v
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
PYTHONPATH=.trellis/guru-team python3 -m unittest discover -s .trellis/guru-team/skills/packages/guru-reconcile-task-base/tests -v
PYTHONPATH=.trellis/guru-team python3 -m unittest discover -s .trellis/guru-team/skills/packages/guru-review-branch/tests -v
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 .trellis/scripts/task.py validate .trellis/tasks/09-12-397-fix-base-candidate-gitlink
git diff --check
```

安装验证使用一个测试专用临时父仓、当前 canonical preset 和已安装的 Trellis 基础文件。
调用安装后的 `execute-base-candidate` wrapper，并断言 validation marker、返回码、
candidate identity 及临时 worktree 清理。该 fixture 只验证本 Issue，不声称完整 Release matrix。
安装版还必须执行含 gitlink 的 Reconcile 到 Branch Review recorder/checker/invoke 链，
不得以两个 helper 的摘要比较代替真实 consumer 调用。
验证 source/installed package inventory 时使用当前 CLI help 给出的原有命令，不发明参数。

测试必须记录旧实现 red 与新实现 green 的差别；命令通过不能替代 marker、Git 状态和身份断言。
安装失败、外部依赖缺失或未执行的检查如实记为失败/未验证，不改写为通过。

安装版共享 runtime 位于 `.trellis/guru-team/runtime`；直接运行 unittest 时显式设置上述
`PYTHONPATH`，真实 wrapper 自行解析安装 runtime。Dogfood 保持既有三平台选择，执行
apply 时附加 `--all-platforms`；代表性干净安装仅选择 Codex。
完整 preset 同步还刷新 `.trellis/guru-team/skills/tests/test_finish_family_integration.py`
到当前 canonical 的 #395 测试字节；本任务不修改该 canonical 文件或 #395 需求。

## 文档与停止条件

Docs SSOT 策略及 owner 见 `prd.md`；候选算法和证据规则见 `design.md`。
规划只完成本阶段文档与门禁，不表示实现、验证、生产或发布完成。
发现必须改变算法的其它 entry 语义、public schema、workflow routing、持久化或 scope 时，
先返回对应 owner，不直接扩写实现。
