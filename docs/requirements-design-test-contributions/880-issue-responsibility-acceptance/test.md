# #880 测试提案与观察

状态 `integrated_pending_review`；前驱 Git `76198a53b4da989b66d2e5f135ff4d2b703ca3cf`。以下结果来自实际实施和工程验证，但 TaskCommit 与独立 committed Review 尚待执行。

## T880-01 / SC880-NATIVE：真实 Agent mixed scenario

R880-01..05/07 → D880-01/03/04。使用现有 `standard-intake-authoring-acceptance-boundary` native case 和更新后的 mixed source，事实与 fixture 进入被测 Agent，语义预期和 grade 不进入。观察原 Clarify／Readiness 保留三个独立结果、明确目标 runtime 和业务配置发布，拒绝共享 test 部署、服务部署、消费方 E2E 及同一 CLI 行为的重复场景。独立读取完整 transcript、命令 receipts 和 public output 后判断语义通过；`ready` DTO 或命令顺序不能代替判断。

## T880-02 / SC880-PACKAGE：eval 发现与合同

R880-07 → D880-04。运行 `guru-review-change-request` package contract/runtime tests 和 eval discovery，确认 corpus 形状、case、fixture、native adapter 与 semantic assertions 可被原入口发现。该证据只证明 package 与传输合同，不证明实际 Agent 行为。

## T880-03 / SC880-DISTRIBUTION：真实 writer/reapply

R880-06 → D880-04。运行 `test_issue_content_distribution.py` 和 `test_review_sufficiency_distribution.py`，检查完整正文、`acceptance-boundary` 示例、owner 引用、全部声明平台字节、用户文件保留、reapply 与零 sidecar。该证据只证明分发和结构。

## T880-04 / SC880-ADOPTION：本 checkout 受管采用

R880-06 → D880-04。代码和工程结果稳定后，由原 `guru-upgrade-tools` 从完整 matching source 完成 preview、prepare、invoke、readback/reapply 和 drift。检查 Task/session、配置、peers、resolver、installed/native、平台 bytes/mode 与 sidecar；`local_candidate` 不证明 formal source lock 或 Release。

## T880-05 / SC880-ENGINEERING：定向工程完整性

R880-06/07。运行受影响 Python/bash/JSON、Guru source/installed validation、Task context、canonical/dogfood drift 与 `git diff --check`。只补受影响差额，不执行完整多平台 Release 矩阵。

## 已完成观察

- T880-01：首次 native attempt 因缺少外部隔离 `CODEX_HOME/auth` 返回 `execution_error`，原失败保留。使用 owner-private isolated `CODEX_HOME` 的新 run root 实际运行 323.399 秒并返回 `ready`；独立读取 Clarify/Readiness owner results、完整 command receipts、最终 public output 后，`current-boundary-and-evidence` 与 `reuse-and-targeted-gap` 均判通过，原 runner 同 run semantic grading 返回 `passed`。实际判断保留目标 runtime 4.2、业务配置更新/revision 和 CLI joint delivery，拒绝逐 Issue 共享 test 部署、服务部署、消费方 E2E 及重复 CLI 场景。
- T880-02：managed Python 执行 `guru-review-change-request` contract/runtime 27 tests 通过；source 与 installed eval discovery 均识别 `standard-intake-authoring-acceptance-boundary`，corpus digest 一致。
- T880-03：`test_issue_content_distribution.py` 真实 writer/reapply 通过，耗时 189.574 秒；`test_review_sufficiency_distribution.py` 通过，耗时 67.845 秒。覆盖声明平台 bytes、`acceptance-boundary` 示例、用户文件保留、reapply 与零 sidecar。
- T880-04：原 `guru-upgrade-tools` 以 local_candidate 和同一冻结 operation 返回 `tools_upgraded`，版本 `0.7.0-guru.10`，recovery ref `53e33269-ca2f-47f2-9330-7a9173877f6d`，`unverified=[formal_fork_source_lock]`。目标自身 installed validation 通过 42 active packages、123 commands、9,938 managed files，conflict/sidecar 均为 0；source validation、dogfood drift、ownership 与 native continuation 通过。3,370 个 Task 文件以及现有 config/AGENTS bytes/mode 保持，session 目录保持原缺失状态。
- T880-05：Task context validation 通过（13 implement / 11 check）；404 个 Guru Python 文件内存语法检查、shell 语法、marketplace/affected JSON 与 `git diff --check` 通过。长文注入和 code-file context warnings 保留为非阻塞提示，实际完整正文按原读取合同另行读取。

未执行完整多平台 Release 矩阵、formal source lock、其它业务仓库采用或额外生产效果。TaskCommit 和独立 committed Review 仍为当前后继。
