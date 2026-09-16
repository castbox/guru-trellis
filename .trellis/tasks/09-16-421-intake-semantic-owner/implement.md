# #421 实施与验证计划

## 范围与状态

仅承接 live [Issue #421](https://github.com/castbox/guru-trellis/issues/421) 的四步 standard Intake。Task Commit 已暂停，旧提交候选和 Phase 2 checkpoint 已移除。当前对本轮观察到的 Wording receipt 承接失败修订原 step-local 执行说明及真实 wrapper 回归，不改生产 I/O/runtime/harness、allowlist 或 Intake-only 补评分边界。修正前的 native、测试及 Phase 2 结论不作为新一轮验收证据。

本轮工作：
1. 撤出 guru-check-task 的 canonical、installed、Shared/Codex/Claude/Cursor 全部任务改动，保持其 HEAD 基线合同、criteria 和测试。
2. completed-run 两阶段补评分只消费声明 native_authoring_flow=standard_intake 的 case。未声明 flow 保持 HEAD 原执行语义；不新增通用 post_owner、Architecture 或 Phase 2 saved-run 生命周期。
3. 保留显式最小资产投影、封闭读取清单和 examples/evals/private runtime 不投影；保留真实拒绝额外读取的测试。
4. 修正后重新运行 source/installed tests、平台 parity、all-platform reapply、dogfood drift、secret/residue hygiene，以及两个新 run-root 的 Intake native、独立语义评分和同次正式评分消费。
5. 基于最终工作树执行 fresh Architecture phase2 与完整 guru-check-task，之后等待独立复审，不创建提交候选、提交、push 或 PR。

## 文件边界

| 集合 | 责任 |
| --- | --- |
| 四个 Intake package SKILL.md、contract、tests | 当前 AI 亲自履行 owner 职责与生产公共输出承接 |
| Readiness eval corpus 与两份 source facts | 完整成功链与真实 scope conflict，无预填语义结果 |
| adapters/eval 下 Intake staging、projection、trace 及必要 caller | 事实与原命令转发，不生成判断 |
| runtime/eval_runner.py 与 Intake/评分定向测试 | flow 专属同次执行评分；未声明 flow 原行为保护 |
| eval corpus/request/trace schemas | eval-only closed flow，不改变生产 I/O |
| canonical specs/README 与受管副本 | 复用 prd.md 唯一 Docs SSOT Plan |
| 当前 task 六文件 | 范围、设计、实现与 check 上下文 |

## 验证矩阵

| 组 | 当前通过条件 |
| --- | --- |
| V1 | 四个 Intake package tests、Intake adapter/allowlist/semantic-grading tests、受影响 shared adapter/runner 定向回归全部通过 |
| V2 | 两条 fresh installed/native Intake 完成实际 owner authoring；首次缺评分不通过，独立审查后原同 run-root 正式补评分，无模型重跑 |
| V3 | 未声明 flow 的 focused/full/saved run 不进入 completed-run 补评分；混合集合不影响 non-flow case；原 #415/#417/post_owner 行为仅作边界回归 |
| V4 | source/installed packages、四个 owner 平台 bytes/mode 一致，guru-check-task 各投影与 HEAD 相同 |
| V5 | apply.sh --repo . --all-platforms 后 drift 为零；逐个核对本任务备份，无 .new/.bak/bytecode/credential residue |
| V6 | task.py validate、完整 dirty diff scope、whitespace、fresh Architecture/Phase 2 通过 |

使用 managed Python 和 PYTHONDONTWRITEBYTECODE=1。不以 transport/mock/schema 通过代替 native 语义审查。失败保留真实结果；未完成验证明确阻塞。完整多平台 clean/update/exact-candidate Release Gate 属于 #410，不在普通 Issue 内扩张。任何其它 owner 或通用 eval 生命周期问题需独立 Issue/task，本任务不创建这些资源。

## 当前结果

2026-09-17 receipt 承接修正后的 fresh 验证：

- 本轮仅增改 Wording SKILL.md、contract、test_contract.py 及受管投影；明确实际 checker_response.validation_receipt 承接与封装错误处理。真实 wrapper 测试覆盖错误外层拒绝、正确 receipt 后 pass/blocked，不改变 runtime、schema、模型 prompt/facts 或 Gate。
- source 四包测试 88 项、installed 四包测试 88 项均通过（相同测试的两种布局，不相加宣称独立用例数）；Intake 13、projection 3、grading 12 项复跑通过。独立只读源码审查无新增 candidate，Wording source16/installed16及边界测试通过。
- fresh complete：`/private/tmp/guru421-receipt-complete-0hBCW3`，实际 context_ready/clear/pass/ready 连续承接，独立 native-four-owner-review 通过；原 runner 同 run-root 正式消费为 passed。
- fresh conflict：`/private/tmp/guru421-receipt-conflict-PWfFDF`，实际 Clarification blocked，下游零执行，独立 native-conflict-review 通过；原 runner 同 run-root 正式消费为 passed。
- 两次 raw run 缺评分时均 evaluation_failed；独立完整 transcript/source/receipt 审查后才正式补评分，没有重跑模型。transcript/trace/request/receipts、实际出口、确定性结果和耗时均未改变。成功链含 Discovery/Clarification 与 Readiness 输入错误并自行修正，不宣称首次无错误；Wording 本轮一次承接正确 receipt。
- 两次投影均为 69 合同、6 仓库事实、1 case 事实，共 76 文件，无多余/缺失资产或 examples/evals/private runtime。临时 auth.json 已删除；旧 scopefix-complete-LVAcXK 失败原样保留，不参与本轮验收。
- 23 source/installed packages、全平台 reapply/parity、dogfood drift 通过。11 个本轮 backup 与 preimage 一致后清理，无 sidecar/bytecode/credential residue。25 Python AST、26 JSON、diff check 与 task validate 通过；保留大型 spec 注入截断警告并直接读取所需完整合同。
- guru-check-task canonical、installed、四平台仍与 HEAD 相同；Intake-only completed grading 和 non-flow 原执行路径保持，runtime/adapter/schema 本轮前后聚合哈希一致。没有通用 retry、shared saved-run lifecycle 或其它阶段扩张。
- receipt 修正后的 fresh Architecture Phase 2 返回 baseline_current/no_architecture_impact，完整 guru-check-task 正式返回 passed；两条上述新运行与最终工作树的 execution binding 已重新校验，原始缺评分返回与独立评分顺序已核对。旧 scopefix 失败不作为当前验收证据。继续等待独立复审，未 stage/commit/push/PR，不创建 Task Commit 候选；完整多平台 update/upgrade/exact-candidate Release Gate 未执行，仍归 #410。
