# #419 执行计划

状态：Phase 1 已完成，当前处于 `in_progress`。实现与定向验证已完成主体，正在按 live #419 r7 收敛 exact-upstream 定向验证与 Phase 2；尚未提交或发布。Release Gate 由 #410 独立拥有。

## 1. 实施顺序

1. 在每次写入前运行 workspace boundary validator，重新读取 live #419、task identity、current diff 与 exact upstream candidate。
2. 先增加 Guru canonical workflow 的唯一 continuation 区块，并把 Phase Index/active breadcrumbs 收敛为 broad guidance；同步 workflow README。
3. 对 Phase 1 activation 与 Phase 2 `passed` output 做 producer capability audit；只为确实缺失的 output-loss 场景增加最小 owner-owned recovery/rematerialization。
4. 保持现有 Task Commit candidate/receipt recovery；只补 continuation route 与正式 wrapper integration，不新增 commit resolver。
5. 增加 planning、in-progress、completed、invalid、adjacent DTO、lost DTO、natural-language、confirmation 与 side-effect failure 的 native integration tests。
6. 绑定 exact upstream candidate `43fffc170927c85d9f7fc106cc5a059e80d4530b`，验证 candidate identity、continuation extractor、`get_context.py --mode continuation` 与 start/continue 薄入口合同。
7. 运行 current source/installed package、runtime、eval、workflow integration 与真实 Git/task fixture，覆盖 continuation 与 owner-preserving recovery。
8. 校验 current source、installed、dogfood、声明平台 projection parity，以及 upstream ownership、dogfood drift、当前工作树 sidecar/residue hygiene 与 `git diff --check`。
9. 收敛 canonical specs/docs，并在 task-owned Architecture/RDT contribution 与 draft ADR 中保留当前 continuation authority；serialized promotion 后清除 shared-current 中不属于当前合同的旧声明。不能直接把未审查候选写成 shared current；immutable superseded/history 只保留历史事实。
10. 运行 preset apply 同步 dogfood及声明平台 Guru-owned projections；逐项处理所有 `.new/.bak`，清理测试产生的 bytecode residue。
11. 使用 Trellis implement/check worker完成实现与独立验证；发现 plan 外 candidate 时先回主 owner fresh qualification，不自行扩 scope。
12. 完成 Phase 2、Task Commit、independent full-diff Branch Review；如需要 promotion，serialized promotion 后对新增 diff fresh 重跑 Phase 2/commit/review。

## 2. 需求—设计—测试映射

| Requirement | Design | Verification |
| --- | --- | --- |
| R419-01 | D419-01 | T419-01..03 |
| R419-02 | D419-02 | T419-04..09 |
| R419-03 | D419-03 | T419-10..16 |
| R419-04 | D419-04 | T419-17..20 |
| R419-05 | D419-05 | T419-21..24 |
| R419-06 | D419-06..07 | T419-25..26 |

## 3. 验证集合

| ID | 场景 | 客观通过条件 |
| --- | --- | --- |
| T419-01 | continuation结构 | canonical与dogfood各恰有一个非空区块；上游 extractor成功返回完全相同body |
| T419-02 | state分发 | planning/planning-inline/in_progress/in_progress-inline/completed各进入声明owner family |
| T419-03 | invalid state | invalid identity/status只返回`invalid-task-state`，零替代task选择 |
| T419-04 | created attach | current created DTO直接消费；lost DTO由原owner恢复，零第二workspace/branch/task |
| T419-05 | partial planning | 基于live authority补齐三份planning，不由文件存在推断gate |
| T419-06 | wording stale | fresh planning wording owner被调用，旧结果不可用 |
| T419-07 | Architecture stale | fresh planning task_impact_sync被调用，旧baseline result不可用 |
| T419-08 | Approval/confirmation loss | Approval fresh重跑；plan重新展示；旧确认不复用 |
| T419-09 | activation output loss | task已in_progress时原activation owner重物化成功，`task.py start`不重复执行 |
| T419-10 | Phase 2 fresh | 缺/stale output执行fresh Architecture + checker |
| T419-11 | Phase 2 adjacent | current正式DTO直接进入Task Commit |
| T419-12 | Phase 2 lost | 仅原checker合法重物化current DTO，否则fresh rerun |
| T419-13 | Task Commit loss | 同一candidate/receipt恢复同一commit；ref只前进一次 |
| T419-14 | Branch Review adjacent/lost | adjacent直达Publication；lost对完整current range fresh复审 |
| T419-15 | Publication adjacent/lost | adjacent直达Finalizer；lost fresh重审live payload |
| T419-16 | drift | base/HEAD/content/Issue authority漂移回最早受影响owner |
| T419-17 | natural language | “继续”和无pending plan的“确认继续”加载同一区块 |
| T419-18 | current side effect | 确认只执行展示payload；成功typed exit自动映射 |
| T419-19 | new side effect/choice | 自动续接在新副作用、真实选择或stop处暂停 |
| T419-20 | side effect failure | 不生成成功exit，不进入consumer |
| T419-21 | upstream ownership | preset inventory/overlay不含upstream entries，本任务diff不修改upstream-owned入口 |
| T419-22 | Guru distribution | source/dogfood/installed/声明平台Guru-owned bytes与modes一致 |
| T419-23 | sidecar hygiene | recursive `.new/.bak` 数量为0 |
| T419-24 | bytecode hygiene | recursive `__pycache__/.pyc/.pyo` 数量为0 |
| T419-25 | exact upstream dependency | full SHA、tree、ordered parents、source lock匹配；extractor、continuation mode与start/continue定向测试通过 |
| T419-26 | real wrappers | source/installed package、runtime、eval、真实Git/task fixture与正式wrappers覆盖adjacent/lost路径，无fake pass/手写DTO |

## 4. 计划命令

写入前：

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --root . --task .trellis/tasks/09-17-419-active-task-continuation --json
```

定向包与集成测试从 live `commands.json` /现有 test modules 解析。基础一致性命令包括：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

Exact upstream candidate 只运行其 checkout 内的 continuation extractor、continuation mode、`trellis-start` 与 `trellis-continue` 定向测试，并校验 commit/tree/parents/source lock/build identity。#419 不调用 Release Gate executor；#410 独立执行其 live 合同。

## 5. Docs SSOT checkpoint

- strategy：`delta_first`；
- durable docs：workflow/README、preset README、workflow/preset specs、Architecture/RDT contribution、draft ADR；
- no-update boundary：upstream-owned start/continue/hooks/platform/meta只由 exact candidate提供，不在Guru docs/projection中复制其正文；
- Phase 2前：canonical、dogfood、installed与测试合同同步；
- Branch Review后：Architecture/RDT按expected current串行promotion；
- Publication前：promotion-created diff已fresh Phase 2/commit/review，零sidecar/residue；
- release boundary：#410必须基于包含#419的最新main重新冻结Guru release candidate，并从零执行其live Release Gate。

## 6. 风险与回滚点

- workflow block、producer recovery与integration tests是一个行为单元，不能只提交该集合的任一真子集。
- 若 producer capability audit证明现有正式recovery已满足r5，删除对应新增profile计划，复用原owner并补测试。
- commit、push、PR、merge、release和cleanup均不在本次Phase 1确认授权内。
