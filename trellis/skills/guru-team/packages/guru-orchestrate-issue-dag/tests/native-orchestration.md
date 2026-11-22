# 真实 Agent 隔离验证

`run_native_orchestration.py` 是两个显式 Skill 入口共用的测试载体。
它不是安装内容，也不是生产调度器。运行需要当前已配置的 Codex CLI、模型和推理设置。
测试不使用真实业务仓库或 GitHub 副作用。

```bash
python3 trellis/skills/guru-team/packages/guru-orchestrate-issue-dag/tests/run_native_orchestration.py \
  --root . --scene dag --output /tmp/orchestration-candidate-dag
```

`--scene sequence` 覆盖严格串行；`--scene blocked` 覆盖单节点外部缺口。
`--scene completion-drift` 补充正常 accepted scope 更新后的过期完整结论。
`--source-ref <commit>` 从同一固定提交投影两个完整运行合同及共享方法，供修改前对照。
模型目录排除 tests、examples 和 forward cases。输出目录必须尚不存在，避免覆盖首失败。
代码不计算行为通过分数，也不按 exit、关键词或动作数量生成通过结论。

## 载体边界

协调器和每个子会话 turn 都由真实、独立的 `codex exec --ephemeral --json`
进程执行。子会话保留同一逻辑 thread/host、Issue、Task、Delivery、分支和工作树身份。
后续 turn 读取其真实既有对话，通过新的隔离进程继续。它不声称是 Codex App 原生
chat continuation 或原生 worktree 创建的集成验证。

启动协调器前，真实 child 先完成一个有限段并停止：DAG 执行当前配置的输入路径一次；
Sequence 回读已失败的原事务；外部缺口场景执行当前配置一次。该段只提供真实结果，
不规定协调器应选择的路由。协调器从显式原身份 resume 接管。

MCP 仅执行 caller 明确选择的动作。自然语言消息由真实 child Agent 理解；
fixture 不按关键词选择回复、产生语义 pass 或自动推进 child。`record_gate`
只存储 child 自己的判断、理由和证据引用，其存储成功不证明正式门禁通过。
目标仓库的 workflow 是合成合同，不是完整 Guru 单 Issue 生命周期的替代实现。

Sequence 场景的原 implementation 入口有有限段边界：成功执行并验证后先结束当前 turn，
后续原 owner 段承接 Check、完整 Review 和 readiness。即使协调指令合并多个阶段，
该入口仍只交付自身结果。审核应从真实 child 报告和仍缺失的 gate 事实判断协调器是否
识别局部完成与整体终点的差额；工具不会替协调器选择后续指令。

`completion-drift` 先让真实原 child 在 scope revision 1 实现、验证、合并，
并独立判断和报告 whole-Task Completion；该段在 Closure/Finish 前停止。
此后 host 模拟正常 authority 更新为 revision 2，增加本场景既定的 checksum 验证义务。
旧声明、门禁和原操作原样保留。协调器只获得当前目标、身份及事实，工具不指定处置。
checksum 工具实际计算当前输出摘要；门禁 recorder 只绑定调用时实际 scope revision。
这覆盖旧完整结论与当前义务的差异，不要求 child 在旧范围下故意说假话。

旧run timer、Git/GitHub 状态、输入目录、外部构建服务和执行器均为合成边界。
`observe_external` 的前三次读取依次提供 running、running、failed 事实；
它不会通知 child、提出后续建议或执行修复。`wait_events` 只作最多两秒的有界进程观察，
仅为隔离测试节省时间，不是生产忙轮询策略。当前协调入口不要求创建timer；旧API只为已有timer的恢复和停止保留，不证明真实App后台执行。

首次给 DAG #101 的后续消息确实启动 child，但工具响应标为 unknown。
原消息和实际进程仍可回读。审核应判断协调器是否查明投递结果而没有重复发送。
旧失败不会被恢复调用改成成功；修正输入后执行会创建新操作并保留旧失败。

CLI 使用当前配置的模型与 provider，仅为本次 fixture MCP 设置工具许可；
其它已配置 MCP 被逐一禁用，不修改用户配置。该配置项来自
[官方 Codex 配置参考](https://developers.openai.com/codex/config-reference/)。
source snapshots、进程 argv/ID、实际 prompt、JSONL、stderr、最终消息和场景状态均留在外部输出目录。
不要把这些原始文件安装或提交到公共包。

## Host-only 审核口径

本节不进入模型目录。独立审核必须读实际消息、工具调用、结果和终点，
不能用初始 facts 中的 declaration 字段代替真实 child 行为。

| 场景 | 必须从实际轨迹判断的行为 |
| --- | --- |
| 修改前对照 | 两显式入口加载固定同 provider；记录真实首失当处置，或明确不复现/环境缺证。 |
| DAG | 已停止 child 无建议时，协调器实际调查、讨论或请求原 owner 动作，并跟进结果。独立项继续；依赖项在前项全部完成前不启动；未知消息先回读。 |
| 外部等待 | running 不变时轻量观察；外部操作结束且失败后，即使 child 没有新文字也重新处置，跟进至结果。 |
| Sequence | 保留旧失败和同身份，判断合法后续执行；当前项完整完成后才开始下一项。必须核不足的局部完成声明或必要 review/Completion 缺口，不能仅看到两个最终 exit 就判覆盖。 |
| 过期完整结论 | 读真实旧 scope 完整声明及随后 authority 更新；核协调器是否识别现行义务仍缺、质疑旧结论的适用性，并交原 owner 补验证/刷新至完整终点后才推进下一项。 |
| 真阻塞 | 实际调查当前入口、原 owner 修正或等价路径；明确最小必需 producer 输出及责任方。保留原身份和结果，核 child inactive、操作安全边界及已有旧timer的停止（新run无此项）。 |
| 终点 | 成功场景的每个选定节点到完整终点；真阻塞到安全终点。遗漏分支保留为未验证，不能自动降格为通过。 |

这些轨迹证明隔离载体中的 Agent 判断与动作闭环。真实 App 调度、生产业务、
实际 GitHub 合并及完整多平台升级矩阵均不在证明范围内。

## 局部授权与处置场景

使用同一个 runner。每次给出新的输出目录。复跑 #883 的 AC2 对照时使用
Codex CLI 0.167.0 和相同 provider，并显式指定相同的模型和推理级别：

```bash
python3 trellis/skills/guru-team/packages/guru-orchestrate-issue-dag/tests/run_native_orchestration.py \
  --root . --scene permission-local-hold --model gpt-6-luna --effort high \
  --output /tmp/orchestration-permission-candidate
```

对照场景只加 `--source-ref 8b92022d6cdf8f9debda09ed68602f1d137e3629`，
并换用新的输出目录。不改用户输入或发布规则。人工观察
`coordinator.jsonl` 和 `carrier.jsonl`：协调者在轮内向用户明确请求确认 A
的 Draft 发布、B 的原 Test 仍在运行，且协调器仍在同一轮时，在输出目录创建空文件
`release-web-result`。这只让夹具 Test 服务提供结果；不给用户回复。
只陈述 A 的权限规则或已暂停，以及最终答复中的确认请求，均不触发释放。
若协调者结束轮次时 B 仍运行，保留原状态和轮次记录。
审核对照 `result_available`、该轮的原 Test 回读和 B 的实际下一步，以及 A 的发布状态。
无法确认轮内消息、前置、结果可读时点或轮次边界时，记录缺证。

| 场景 | 原操作和行为证据 |
| --- | --- |
| `delegated-action` | 查看原 owner 的 Draft 提案、协调者的精确执行指令、原 owner 的 `publish_draft` 和后续协调者回读。用户已委托此项，目标规则允许协调者发出指令。 |
| `stale-registration` | 在输出目录内创建实际 Git 仓库和失效注册。原 `acquire_task_checkout` 先返回真实 Git 阻塞。查看协调者指令、原 owner 的完整 dry run、路径和 owner 事实、匹配清理、差额回读以及同一原操作的重试。清理不会移除 branch refs。 |
| `stale-registration-extra` | 完整预览含另一条关联保留 Task 的失效注册。核对回读与 hold，检查未执行会一并移除两条记录的命令。 |
| `settled-issue-edit` | 使用取材于 Backend #1944 的合成旧正文和固定外部标识。核对原审核者提案、协调者指令、原 owner 写前回读、精确写回、写后回读和同一 Intake 的新 revision。 |
| `unsettled-issue-edit` | 注册表未见冲突但缺少已经接受的标识合同。查看协调者保留的选择和未改动的正文。 |
| `issue-edit-preimage-change` | 原审核后，另一编辑者增加正常追踪说明。核对旧 preimage 未被用于覆盖新正文；如有新处置，需基于当前正文重新审核并保留说明。 |

`run.json` 记录实际启动模型和轮次时间。协调器和子会话各有 JSONL 与最终消息；
`carrier.jsonl` 提供带时间的工具调用及原结果，`state.json` 保留结果状态。
证据只来自实际轨迹。夹具未启动协调器、模型不可用、超时、脚本退出码或最后总结
均不能单独证明行为。Git 只写输出目录内的独立仓库；Issue 写回只更新合成状态。
