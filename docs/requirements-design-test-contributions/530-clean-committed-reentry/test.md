# #530 唯一测试结果

状态：源仓实现与代表性 installed 定向验证完成；正式阶段结果仍由各 owner 返回，不由本测试文档代替。

| Test | 观察入口 / 缺陷检测 | 当前结果 |
| --- | --- | --- |
| T530-01 | 实际公开 TaskCommit→post_commit Reconcile→fresh Check→clean committed identity→fresh Architecture→initial full Review；identity 绑定当前 HEAD。 | source 与实际 preset-installed 公开 wrapper 链通过；第二次 base 演进后重复 Reconcile/fresh Check，完整 Review range 绑定最新候选。fixture semantic authoring 不等于本任务真实独立审查。 |
| T530-02 | fresh Check 后正常 dirty 增量，原 exact prepare/invoke 产生当前 commit。 | 通过；只读入口拒绝实际 dirty，原路径新增一个实际提交。 |
| T530-03 | 正常内容、历史、base 或 branch 变化使旧输入 stale；原恢复路径重建。 | 通过；实际内容提交、mode-only 提交、base 前移及 branch 切换分别拒绝旧事实。 |
| T530-04 | active Git operation、finding-fix/fresh-final intent 保留原 owner。 | 实际未结束 merge 被拒绝；原 hook/recovery executor 回归通过。finding-fix/fresh-final caller 合同与 runtime 未改变，静态核对其原 owner；未把本次 fixture initial Review 当作 fresh-final 证明。 |
| T530-05 | 接续前后 HEAD/tree/index/status/commit count，无新提交或推进状态。 | 通过；额外比较 reflog；未执行 pre-commit hook，无新 candidate/receipt/JSON 状态，仅消费原 Phase2 checkpoint。standalone 与 nonpassed 路径通过。 |
| T530-06 | canonical/installed/platform、reapply/drift/mode/sidecar 与一个代表性 clean 安装。 | source/installed graph、ownership、shared/Claude/Codex/Cursor dogfood drift、干净 preset 安装与 reapply 均通过；实际安装包 7 项公开链回归通过，零 `.new/.bak`。 |

## 实际命令与归因

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-create-task-commit/tests -p test_committed_reentry.py -v`：7 tests / 61.219s / OK。独立 Architecture reviewer 同定义执行 7 tests / 54.938s / OK。
- 同一命令用 `SOURCE530_TASKCOMMIT_PACKAGE` 指向本轮干净 preset 安装的真实 package，并设置其完整 installed runtime 的 `PYTHONPATH`：7 tests / 53.526s / OK。安装及再应用均为 `status=ok`，installed validator `passed`，managed Python runtime `ok`。
- `test_real_reconcile_clean_reentry_and_initial_full_review` 保留首次失败：同一真实 clean 状态，旧 prepare 返回 `schema_mismatch` / `exact_stage_paths`；新正式入口返回当前 committed identity。该反事实证明候选输入域修复，没有放宽原 dirty 限制或制造推进提交。
- `PYTHONPATH=trellis/skills/guru-team python3 -m runtime.validate --root . --mode source --json`：36 active packages / 109 commands / passed；installed mode passed。ownership、dogfood drift、AST/JSON/Bash syntax、workflow 字节 parity、task context validate、`git diff --check` 通过。
- 完整 TaskCommit package suite 初次 34 tests：2 failures / 4 errors。两个新增 fixture 错误已修正并由上述 7 tests 重跑验证；余下 3 个旧 fixture 方法在 prepare 前被当前 task schema 拒绝。独立旧 `test_new_prepare_retires_previous_recovery_receipt` 仍失败 `unsupported_legacy_task`；fixture、`common.py`、`record.py`、task lifecycle validator 均与 HEAD 一致，按当前任务必要性资格审查排除，未修改历史 fixture，也未声明 suite 全绿。
- `python3 -m unittest discover -s trellis/skills/guru-team/tests -p test_skill_packages.py -v`：20 tests / 101.725s，19 passed / 1 failure。唯一失败为原 `guru-sync-base` discovery 的 `version_state_mismatch`，独立公开 discovery 可复现；其 Interface、registry、discovery runtime 无本任务修改。属于无关历史问题，未弱化断言或扩大本任务。
- 首次 task preset apply 生成 41 个 `.bak`，已逐项证明备份等于 HEAD preimage、当前目标等于 canonical，再处理本次生成的备份并 reapply；最终无 sidecar、漂移或安装冲突。

2026-10-13 已只读核验 live #530 为 OPEN，主 main/远端 main 为 `8b55f624114accb0b19562dee296b582d178a17d`；任务 checkout HEAD 为 `a653c90b064e2435bc147f1bda0e1b7ab632f797`。此为整合前历史状态，不替代 backend #444 重跑。原现场错误和旧 SHA 由 live Issue 持有，不复制为修复通过证据。

未验证边界：当前任务代码尚未提交；完整独立 committed Branch Review、整合后正式 Phase2/独立 committed Branch Review、shared authority promotion、Delivery/merge/Completion/Closure/Finish 尚未执行。Backend #444 实际安装/现场、远端 marketplace、完整多平台 Release 矩阵与软件发布不属于本轮定向证明。机器全局 Trellis 为 0.6.17，尚无已验证的 locked Fork `5c760463680ffc10a3f26957b330c57a4b0c3ff8` / `0.7.0-castbox.3` built CLI；本轮 clean preset/reapply 不证明官方 init/update/upgrade。

## 当前 main 整合与恢复

2026-10-13 本地整合提交 `9535f61b423e52e3945426b29102a8ed7e4059c2` 的两个父提交为 `a653c90b064e2435bc147f1bda0e1b7ab632f797` 和 `8b55f624114accb0b19562dee296b582d178a17d`；提交 tree `09742062e4d97688793bbac9c7d594921c0febff` 与该 main tree 完全一致。未提交 #530 改动由 executor stash 保留；恢复时四个 spec 尾部新增段落与 extension 元数据出现冲突，executor 返回 `reconciliation_failed/worktree`，未产生正式 `reconciled` DTO。四个 spec 已合并保留 #292 与 #530 两项合同，extension 由当前 canonical installer 重建；原 stash `358e414b6de46879629dbc02d6e9e9fee5f30c2c` 保留至核验完成，不把失败 stdout 改写为成功 receipt。

恢复后的正式 `guru-ensure-task-checkout` 返回 `checkout_resolved`，task boundary `ok`；CURRENT SESSION TASK 仍为原 TaskId/generation/branch。旧 Phase2 anchor 为 a653，不能推进整合后 commit；按 continuation 原恢复矩阵重入 fresh Architecture(phase2) 和 Guru Check。当前 RDT 继承 `.88/active`、Architecture `.85/active`；Planning 的原 `.84` 引用保留为当时历史，当前 contribution/门禁重新绑定 live authority。基线身份演进未改变 #530 目标或原 approved mechanism。

整合后 canonical 新增 7 回归由 implement worker 执行：`test_committed_reentry.py`，7 tests / 55.392s / OK；40 个 JSON 与 9 个 Python AST、`git diff --check HEAD` 通过，无需实现兼容修改。当前 preset dogfood apply `status=ok`，source graph 37 active packages / 110 commands、installed validator passed；零 new_copies/managed_backups/sidecars。当前 main 新增 Author 使 graph 从历史 36/109 变为 37/110，该数字来自真实 registry 而非固定断言。

恢复核验：stash 的 59 个 tracked changed paths 与 43 个 untracked file paths 均完整存在；原 implementation additions 与 stash 字节一致，隔离 Docs 更新为本次明确的基线/结果更新；当前 unresolved entries 为空。恢复 stash 保留；后续清理仍是独立动作。

## 整合后当前候选验证

- Fresh 独立 Architecture reviewer 亲自执行 source 新回归：7 tests / 55.463s / OK，dogfood drift exit0；未改原 `test_happy_path.py` 另跑 7 tests，6 passed / 1 error，唯一失败仍为旧最小task fixture 的 `unsupported_legacy_task`。该 test、common.py、shared identity.py 的 a653/current HEAD/worktree 三份字节一致，原 `rejected_out_of_scope` 资格结论对相同机制保持适用。未修改旧fixture，未宣称整包全绿。
- Trellis check worker 在一个实际临时 Git repo 中 clean preset apply/reapply 均 `status=ok`，第二次 manifest 字节不变；installed validator passed，零 `.new/.bak`。使用实际 installed managed resolver、完整 installed `PYTHONPATH` 和 `SOURCE530_TASKCOMMIT_PACKAGE` 执行 7 项公开链回归：53.722s / OK。临时fixture安装证明当前preset投影，不证明 locked Fork 的官方 init/update。
- 原 dirty/hook/recovery 定向 12 tests / 5.211s / OK：成功与 stdout-loss、post-ref 中断同 DTO 恢复、stale HEAD、原 compatibility projection、参数互斥、pre/post/commit-msg hook 失败保留、core.hooksPath、四类 hook 正常执行、command/error schema 与 wrapper mode。
- Current source validator passed（37 active packages / 110 commands）；ownership passed（22 descriptors / 43 claims / 22 overlays）；dogfood drift、task context validate、workflow parity、54 changed JSON、258 Python compile（产物在临时目录）、148 Bash syntax、`git diff --check HEAD` 通过。task context存在原大文件注入截断提示，worker执行child-side适用spec读取；未把提示当全量context证明。
- 主owner逐项检查完整 102 个 changed tracked/untracked 文件：UTF-8、JSON/JSONL、trailing whitespace 与 blank EOF 均无问题；`.trellis/scripts/**` 与官方 Agent definitions 零diff。当前 GitHub main 只读复核仍为 `8b55f624114accb0b19562dee296b582d178a17d`。

当前源仓根因回归与支持的dirty/stale/reentry/install边界已取得scope-required证据。Formal Phase2与本任务真实committed full review分别由原owners执行；测试fixture的semantic authoring不能替代这些门禁。软件版本、backend安装与Release外部边界仍如上。
