# D8 工具采用验证

## 实际范围与来源

本节记录两个原目标的正式工具采用，不替代 Check、Branch Review、Delivery Review 或整体 Completion。执行源为完整 canonical `1cee58a6db1b9837054c6ce8582fb6c0bf9e55b8`，Fork 为 `9f40ec70914f98fce2619560274cc1d0619f2f7e`，CLI/Core 均为 `0.7.0-castbox.4`。两次操作均使用原 `guru-upgrade-tools` 的 `source_locked`，结果 `unverified=[]`。没有手工修改上游脚本。

执行时 `trellis/` 无未提交改动。两份原安装 receipt 的 source ref/commit 均为上述 H1cee；`source.tree_state=dirty` 如实包含本 Task/规划的未提交内容，不能据此声称整个 checkout clean，也不能据此推断 canonical 生产源码有变更。

## 两目标的实际结果

| 目标 | 原 public operation | tools recovery_ref | 结果与平台 |
| --- | --- | --- | --- |
| 原 Task checkout `guru-trellis-worktrees/589-git-object-performance` | `5e6b8a87-8b5d-49d9-939e-7f2c8615d857` | `1de29d04-b8e3-4f16-be52-8a8884756461` | `tools_upgraded` / Guru `0.7.0-guru.4`；claude/codex/cursor |
| 正式代表 `/tmp/guru-589-installed-20261017` | `105f3b0e-cf97-4d8e-851a-ab220f65efe5` | `a32b4dd2-fa6e-471a-bd00-9fb97a5b5081` | `tools_upgraded` / Guru `0.7.0-guru.4`；codex |

Task 消费原已冻结 plan，未再次 prepare。代表只 prepare 一次。两目标原 public receipt 均为 `phase=applied`；之后分别以原 recovery_ref 调用 `profile=resume`，都返回与首次结果完全相同的 DTO。此恢复没有另建 operation。

两目标均由自身 `.trellis/guru-team/runtime/resolve-python.sh` 实际解析到 managed Python `f0b89dabd24ef812b1244b8b/venv/bin/python`，并从该目标执行 `runtime.validate --mode installed --json`，结果均 `passed`。原工具执行中的目标 native continuation 与隔离内存 public-operation 能力检查亦通过。

Task 自身 `get_context.py --json` 返回 session 绑定的 Task589/gen0。其 `delivery.py current --json` 返回当前 D8 key、准确 planning_root、`phase=implementing` 和实际 accepted planning 结果 `planning-accepted:f5e1b44f-c69c-4323-b747-951f01c62e77`。这进入原 implementation owner，不推导后续 Check 通过。代表自身 native 返回 `currentTask=null`、`delivery.kind=no_current_task`，未创建 Task。两目标 runtime-contract 均声明 Delivery API `1.0`、Task schema `2.0` 及原 owner graph。`--mode continuation` 实际 rc0；该模式输出 caller 合同，不能单独代替前述 current/context 验证。

## 字节、模式、投影和保留

两目标 required `common/git_objects.py` 与 `common/delivery_store.py` 的实际字节均等于各自冻结 public plan 的 **target** 内容，实际 mode 均为 `0755`。source/preimage 是旧字节，不能用它作为候选比较对象。D7 已记录的 tar 模板 `0644` 到 installed `0755` 归一化边界继续适用。

两目标 `.trellis/workflow.md` 均逐字节等于 H1cee canonical。原 plan 的 workflow 均为 `template_id=guru-team`、`ownership=custom`，provider 为 `gh:castbox/guru-trellis/trellis#1cee58a6db1b9837054c6ce8582fb6c0bf9e55b8`。两份安装 manifest 的选定平台与目标一致；其 companion managed hashes 均无 mismatch，完整 package/平台投影由各自 installed validator 校验通过。Task 的 `check-dogfood-overlay-drift.sh --repo WORK` 实际 rc0，三平台 native roots 与 canonical workflow/spec 均匹配。代表没有 canonical 源目录，因此不伪造 dogfood 检查；其安装包及 codex 投影由目标 installed validator 负责。

两目标原 installer 均实际重新安装当前 Guru 受管投影；同 operation 恢复完成后，递归扫描均为零 `.new`/`.bak`。没有未知 Guru edits、essential 冲突或遗留 sidecar。两个非必需 `config.yaml` 冲突均按原冻结 preserve 决策保留，required 脚本仍安装成功。未另起完整 installer/Release 矩阵；D7 相同 Guru 生产字节的 reapply 证据继续保留。

Task 安装及恢复期间暂停并行 Task 写入，事前/事后 2599 个文件摘要一致，覆盖实际 Task（含 archive）、workspace、config 与已存在的 common Python 指针。代表的四个对应文件亦未变。原 tools checkpoint 的完整 peer/common 集合按原 owner 状态逐项读回：Task 309 个状态（包含合法缺失项），代表 1 个 common 状态，均无变化或意外创建。两目标只启用各自 checkout-local Python override。

Task/session/private control 不在 public/Guru 写集。本轮对 Task/archive/workspace/config 有上述独立字节比较；未在执行前另建完整 common session 快照，不能把写集排除扩大为单独全量 session byte-diff 证据。未迁移历史 Task、改业务记录、改 common 默认指针或改 peer 工具。

## 命令与实测边界

原命令为 canonical `guru-upgrade-tools/scripts/prepare.sh`（代表一次）、`invoke.sh --root TARGET --input INPUT --plan FROZEN_PLAN`，以及同 wrapper 的 `profile=resume`。输入、原 receipt、结果、目标 native/installed 输出和 Trace2 位于本机 `/tmp/guru-589-d8/`；这些是本轮工程诊断位置，不是长期公共 handoff。

| 实际操作 | 全部 Git 进程 | show | cat-file | ls-tree | Trace2 首末事件窗口（秒） |
| --- | ---: | ---: | ---: | ---: | ---: |
| Task invoke | 1587 | 71 | 3 | 0 | 60.848519 |
| Task 同 operation resume | 647 | 2 | 1 | 0 | 14.103073 |
| 代表 prepare | 145 | 68 | 2 | 0 | 12.828894 |
| 代表 invoke | 201 | 71 | 3 | 0 | 39.828549 |
| 代表同 operation resume | 31 | 2 | 1 | 0 | 6.105160 |

Trace2 按本次命令实际继承的环境采集，未混入后续独立 native/drift 检查。五个 trace 均无 Git 网络命令；未据此宣称所有非 Git provider 网络耗时为零。Task invoke 中 1465 个 rev-parse，resume 中 634 个 rev-parse，包含原 owner 对多 peer 指针的解析，不隐藏为零。这些数字描述工具采用，不是业务链性能对照。Trace2 窗口不是完整墙钟；本轮未采集 RSS、batch 请求体、唯一 blob 或实际读取字节，不从 Trace2 猜测这些数值。D7 原 observer 与同输入基线/历史 FAIL/SKIP 不改写。

本轮曾用 JSON parser 读取纯文本 continuation 输出，得到本地 `JSONDecodeError`；随后按该命令的实际文本合同读取，并以独立 context/current JSON 验证目标状态。该失败没有触发重复安装或重新 prepare。官方文档站本次读取三个指定 Markdown 页面均返回 HTTP 403；此轮没有修改扩展机制。

## 尚未发生的后续步骤

本节不预填本批真实 manual merge、首次 `delivery_merged_recovery`、query2、Completion、Closure、Finish 或 Cleanup 通过。它们由原 owner 在实际发生后记录。#575 全平台 Release 矩阵、软件/npm 发布和业务仓采用未执行。
