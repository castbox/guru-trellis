# #710：实际观察与验证边界

本页唯一拥有本批实际验证与观察截止点；完整策略见 [proposed Test](proposed/docs/test/current/knowledge-maintenance.md)，稳定关系见 [traceability](traceability.md)。本次观察截止于 candidate/final 第7轮和 finding 第9轮的原正式 semantic grading 均通过、tools9 同步完成，以及本 RDT 隔离提案冻结前。前述失败仍按原案例保留；唯一 clean 样本只证明 tools6 固定源码截止点。本页采用原 owners 的可核验执行事实，RDT owner 未重跑这些命令。两个 native 样本的成功不替代主 Task 的正式候选 Check、共享晋升、最终 Check 或 committed Review。

## 已执行的 RDT 准备

原 RDT owner 已完整读取安装的 clear-technical-writing、RDT SKILL/contract/current-knowledge、适用 spec indexes、R/D/T 根与 current 导航、B 的三层 knowledge-maintenance 完整正文、root 与选定 D1 的 PRD/design/implement，以及 Author shared planning-body/design/implement templates。读取原 Check 合同用于保留九维、语义/客观身份和候选/最终职责边界；官方 Trellis 首页、custom workflow、custom spec marketplace 本轮已读取。此事实仅证明准备及原定义取证，不是源能力或测试通过。

写入范围为本贡献的 manifest、requirements/design/test/traceability 和三个完整 proposed targets。每次写入前运行原 check-task-checkout-boundary.sh 验证专用 checkout；未写 shared current/navigation、Task planning、Architecture contribution 或实现源码。完整 target 保留固定 B 的前驱正文，本批新增 R710/D710/T710。

本轮 RDT 只读核对确认三个 proposed 正文均完整保留 B 原文件前缀；8 个新文件的 UTF-8、行末与 EOF 空白检查通过。目标上下文的本地链接检查仅剩批准计划中的 `trellis/presets/guru-team/MIGRATION-710.md` 尚待原实现 owner 写入，涉及 Requirements 目标和 traceability 的两处引用。该准备检查不证明本批 runtime、native 或安装行为；原实现完成后再核链接。

随后原实现 owner 已建立 MIGRATION-710；原 RDT owner 读取其 consumer 清单、直接输入退出、matching 安装及完整结果恢复合同，确认与本提案目标一致。此前两处本地链接已有真实目标。该观察只确认文档与来源关系。

## 原 package、命令与运输事实

原 core/check worker 日志为 `/Users/wumengye/.codex/sessions/2026/10/31/rollout-2026-10-31T22-00-49-01a19243-57aa-77b0-b822-9e8a993a3823.jsonl`。其 `event_msg.item.aggregated_output` 保留实际命令及 stdout；以下分别采用该日志第209、304、314行的原结果，不能把局部通过说成全部 suite 通过。

| 原检查／观察对象 | 实际结果与证明边界 |
| --- | --- |
| Check package 全套：原匹配 Python/Delivery API 执行 `unittest discover -s trellis/skills/guru-team/packages/guru-check-task/tests -p 'test_*.py'` | 66 tests，65 pass / 1 fail，163.638s。唯一失败是 `test_finish_archive_preserves_public_aggregate_without_task_status` 的 `before == after`：合法归档新增 `artifact_origin`。原协调 owner 对固定 B 路径作资格判断后未复现 #710 回归；保留失败，未改归档或弱化断言。该 suite 保留其余通过项的局部证据，不能报告全绿。 |
| 旧 Phase2 adapter 文件：`unittest discover -s trellis/skills/guru-team/adapters/eval -p 'test_phase2_authoring.py'` | 18 tests，1 failure / 10 errors，366.765s。10 errors 在旧非 stateful host 的 activate→final_architecture 前置，原 Architecture wrapper 报 `stale_identity/worktree`。原协调 owner 比较同 fixed-B 路径后未复现本项回归；这批旧样本不作为本批两个 stateful native 案例的必要起点，也不为全绿扩修。1 failure 是同步前 source/installed package identity 不同，后续原同步及 identity 单测另列。 |
| 改动的 implementation recorder 单测：`test_original_check_recorder_changes_only_its_declared_checkpoint` | 1 test，39.791s，OK。证明该单测实际 record 入口和声明 checkpoint 行为，不是 native 证据。 |
| 原 worker 的 source/package 与静态检查 | source package validator 通过，43 active packages / 127 commands；372 个 Guru Python 文件语法、JSON 及 tracked/untracked 空白检查通过。未发现独立 TypeCheck 配置，未宣称 TypeCheck 通过。这些检查不替代语义门禁或真实 Agent。 |

原 eval worker 日志为 `/Users/wumengye/.codex/sessions/2026/10/31/rollout-2026-10-31T21-40-36-01a19230-d494-7fd0-927d-c4cf4fea968e.jsonl`。原 RDT owner 已读取其中第520/536、545/616及949行的原分块输出：

- 首组 8 项定向 transport/recorder 测试在164.291s完成，OK。它们覆盖原字节 authoring、同结果消费、公共输入观察与候选/最终 stage observer，证明相应运输/命令边界。
- 随后两个 observer 单项分别输出 ok；同次运行还包含一个旧 clean host 测试，该项报上述 worktree 前置错误。原总结果是3 tests、115.773s、1 error，不能将这次整体写成通过。
- native-2 失败后，原 eval owner 只修订批准范围内的操作上下文和阶段事实；该次3项定向测试在70.828s完成，OK。测试没有替代真实 native，未改原 terminal wrapper、Architecture 或 checker。修订后的安装与新 native 尝试另作观察，不覆盖原失败。

后续原定向结果均保存在 `/private/tmp/guru710-execution-r7vjr10t/` 对应 `.command.json/.stdout/.stderr`；RDT owner 已读取原 argv、returncode 及测试输出：

| 原检查 | 实际结果与适用边界 |
| --- | --- |
| `eval-context-boundary-tests-4` | 7 tests，67.746s，OK；覆盖 virtual request/Delivery parse 的执行前纠正、真实 recorder 首失败仍终止、原 no_change 路径、实际 candidate 才要求 promotion，以及 after 重绑和匹配最终 Architecture。 |
| `eval-context-boundary-tests-4b` | 4 tests，0.005s，OK；补 observer 将执行前诊断与真正 semantic owner 调用分开，保留原 no_change/promotion/rebind 义务。 |
| `eval-command-discovery-tests-5` | 2 tests，39.809s，OK；未知 command 不执行 owner，原 wrapper 的显式 help 可用，真实 recorder 首失败仍终止。 |
| `eval-observer-help-tests-6` | 3 tests，24.232s，OK；真正 wrapper help 不算 semantic 结果，非 help 的错误结果仍拒绝，原 no_change 和实际 promotion 条件保持。 |
| `native-model-contract-6.stderr` | 模型配置合同单测1项，0.002s，OK。仅证明该配置合同，不证明更换模型后的 native 行为。 |
| `eval-completed-binding-tests-8.command.json/.stderr` | 原 `test_phase2_completed_binding.py` 4 tests，0.214s，OK；覆盖两例实际 producer 的 public fixture 绑定、不同 producer 输入拒绝、model-visible 字节保持和其它变更 fixture 不获取该局部例外。该单测只证明 completed-input consumer，不声称独立 native 或 grading 成功。 |

这些是命令/运输及 observer 的局部结果，不能抵消 native 失败或把旧 adapter 全文件结果改为通过。原独立 Architecture 审核还发现旧 observer 对 no_change 样本强制执行不适用 promotion，与原 workflow 的 no_change 路由冲突。原修订已使 caller/observer 按实际前置输出判断：reviewed_candidate/candidate_ready 才要求其原 owner 的 final_integration；no_change/ssot_current 跳过不适用写入，仍要求原 implementation 重绑和匹配最终 Architecture。定向测试证明这些判断分支，尚无 native 成功来证明完整行为。

## 同 checkout 同步与唯一代表 clean 安装

原工具及安装证据根为 `/private/tmp/guru710-execution-r7vjr10t/`。本页采用该处原执行文件，不从相同版本字符串推断内容一致或正式发布。

| 原结果 locator | 实际观察与边界 |
| --- | --- |
| `tools-execution.json` | 第一次原工具操作返回 `tools_upgraded / 0.7.0-guru.7`。使用 local candidate，`formal_fork_source_lock` 仍未验证；不声明正式 source-lock 或 Release 通过。 |
| `installed-packages.json`、`dogfood-drift.stdout` | 安装检查 passed，声明平台为 claude/codex/cursor，conflict、sidecar均为0；dogfood 原命令核 workflow、选定平台和 spec 与 canonical 一致。只证明当次受管投影。 |
| `source-installed-identity.stderr` | 同步后 identity 单测1项，0.024s，OK。它闭合此前同步前 identity mismatch 的局部观察，不改写旧 adapter 的红结果。 |
| `installed-native-context.json` | 原生 `get_context.py` 实际读取当前 checkout、Task `710-phase2-recorder-authoring`、generation0、D1 `63d55014-9fec-48da-a106-2a7403305977` 及 implementing；Planning accepted，Check/full_review/readiness 仍缺失。上下文可读不是 formal Check。 |
| `tools-execution-3.json` | 上下文修订后的第二次工具同步返回 `tools_upgraded / 0.7.0-guru.7`；formal source-lock 缺口仍保留。对应本轮同步的三个文件是 `phase2_candidate_final.py`、`phase2_authoring.py`、`test_phase2_authoring.py`；此前将第三个文件记为 `implementation_authoring.py` 的名称错误在此纠正。此同步不补造新 native 结果。 |
| `tools-execution-4.json`、`tools-execution-5.json`、`tools-execution-6.json`、`tools-execution-7.json` | 各次原操作均返回 `tools_upgraded / 0.7.0-guru.7`，均保留 `formal_fork_source_lock` 未验证。tools6 采用当时的 observer/help 与模型配置；tools7 采用最后两条操作上下文说明。RDT owner 在 tools7 后实际比较上述三个文件，canonical 与根 checkout installed 字节一致。这里只证明各次实际采用，不宣称原失败已修复或 clean 已采用 tools7。 |
| `tools-execution-8.json`、`tools-execution-9.json` | 各次返回 `tools_upgraded / 0.7.0-guru.7`，formal source-lock 仍未验证。source8 补终端 wrapper 后不再发送 cleanup 的说明，以及原 completed-input consumer 对两个 stateful 案例的实际 public fixture 绑定；后者在 selected-skills 解释器加载 adapter，不让 launcher 父进程误 import。source9 仅定位实际 workflow 的 owners[owner_role]，区分 execution owner 与 coordinator/route，没有硬编码 owner_id。它们是根 checkout 的后续工具采用，不能扩张 clean 的源码截止点。 |

唯一代表 clean 目标为该根下 `clean-repo/`，Trellis 为 `0.7.0-castbox.6`。原命令、argv/cwd/returncode 和首次 stdout/stderr 全部保存在 `clean-install-evidence/`，RDT owner 已读取这些原结果及 `12-clean-readback-summary.json`。该样本先 init `native-delivery-v1`，再经官方 maintain prepare/preview/apply 安装实际 Guru workflow，随后完整 preset apply、同源 reapply、installed package check 和原 context 入口均返回0。

初次 `12-clean-readback-summary.json` 确认 shared 与 claude/codex/cursor 投影没有 missing/extra/byte drift，2535个 package 文件没有 byte/mode drift；三个 overlay 与 workflow 匹配，158个 shell mode 检查无失败，用户 note 保留，reapply 无 changed paths，sidecar为空。这些事实只适用于当次源码截止点，不证明完整多平台 Release/Upgrade 矩阵或业务采用。

原 `10-platform-drift` 命令 exit1，报告 clean 目标缺 canonical registry。该命令是 dogfood validator，普通 installed clean 目标不携带 source。原协调 owner 判定这是对象不支持该入口，保留 `10-platform-drift.stdout`，没有修改 validator 或伪造 canonical；实际采用原 installed 检查与上述目标字节/mode readback。失败与可用安装证据分别保留。

随后仍在同一 clean 目标，以 `13-final-source-cutoff.json` 固定 tools6 对应的源码字节重新应用。记录中的 source HEAD 是开发 B `2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30`，同时明确记录 dirty 文件内容；它不是已提交的可获取交付 commit。原 `13-preset-final-apply` 首次返回 conflict/exit2，并列出8个既有生成 `.bak`，该失败 stdout 保留。原安装 owner 按 `14-generated-backup-moves.json` 将这些备份保留到 repo 外 `retained-generated-backups/`，核对前后 bytes/mode 未变，然后原 `15-preset-final-apply` 返回0。`16-preset-final-reapply` 返回0且 changed paths 为空，`17-final-installed-check` passed，`18-final-context-entry` 返回0。

`19-final-clean-readback-summary.json` 证明该固定截止点下2535个 package 文件、44个 adapter 文件及 shared/claude/codex/cursor 投影没有 byte/mode drift，overlay/workflow 匹配；158个 shell mode 检查无失败、用户 note 保留、目标 sidecar为空，8个备份保留完整，原第10及13项失败没有改写。该 readback 没有运行 native，也不证明 formal Fork source-lock 或完整矩阵。

clean 的适用源码截止点是 tools6。tools7 在 `phase2_candidate_final.py` 新增两条上下文说明：原 delivery-api 的 `--input` 接受 inline JSON/文件而不接受 `-`，以及等待同一个 independent-review shell session 完成后再发下一 helper 请求。当时 RDT owner 比较 cutoff 记录与源码，仅该文件在五个记录对象中已变化。source8/9 此后还有上述局部说明和 completed-input consumer 修订，均未在 clean 再次采用。因此不能将 clean 的 fixed-cutoff 安装事实描述成 exact current 安装验证，仍可保留它对其它未变安装面及既定 clean/reapply 范围的局部价值。

## Native 第1、2次失败及修订案例边界

两类案例分别为 `native-owner-candidate-final` 和 `native-owner-finding`。原 run 根依次为上述证据根下 `native-{candidate-final,finding}-1/` 与 `native-{candidate-final,finding}-2/`。每个根的 `guru-check-task-codex-run.json` 及 `current/<case>/adapter-transcript.json` 保留原状态和轨迹；RDT owner 已读取原 run summary、transcript 与其所定位 native trace。

| 实际尝试 | 首个可核验失败与结果 |
| --- | --- |
| 第1次，两案例 | 模型执行前缺少外部隔离 `CODEX_HOME`，原 transcript 为 `isolated Codex authoring requires one external isolated CODEX_HOME`；timing为0，run均为 execution_error，没有 Check。后续补齐环境后的案例不改写这次失败。 |
| 第2次 candidate/final | 实际模型为 `gpt-5.6-sol`。第一个错误 command 是 `skill_id=delivery-api, command=delivery.py, arguments=[--help]`，returncode2。后续空响应/JSONDecodeError不是更早失败的替代根因。run为 execution_error，没有 candidate_checked 或最终 passed。 |
| 第2次 finding | 同模型；原 Author requirements_ready 已实际发生。Planning candidate_assessment 使用了未来 phase2 模板的 freshness，独立 Architecture 原 wrapper 返回 `stale_identity`、`field_path=input.freshness_identity`，要求绑定当前 design facts。后续 FIFO 空响应/JSONDecodeError不替代这一原始错误。run为 execution_error，没有匹配 Architecture 或下游 Check，不构成 finding 路由验收。 |

原协调 owner 按当前正常路径、机制与根因合同准入操作上下文/阶段 facts 修订：补原 API 调用语法及 Planning freshness 的实际适用对象，不代产语义结果、不补私有摘要、不改原 Architecture/checker。准入只允许相应修订，不证明修复效果。原第1、2轮失败保持；后续各轮使用独立 run 根，不能把重试说成前两轮首次成功。

## Native 第3至6轮与模型变化

原 run 根延续为证据根下 `native-{candidate-final,finding}-{3,4,5,6}/`。每例均有原 `guru-check-task-codex-run.json` 和 `current/<case>/adapter-transcript.json`；RDT owner 已实读这些原状态、模型、输出及其定位的 command trace。八个 run summary 全部是 execution_error，均没有完成 Check。

| 轮次／模型 | candidate/final 的实际观察 | finding 的实际观察 |
| --- | --- | --- |
| 第3轮，`gpt-5.6-sol` | 首个不受支持虚拟请求是 `implementation-authoring --help`。新 relay 将尚未执行原 owner 的 request_error 也设为 terminal，随后 inspect 被拒绝；没有 Check。 | `implementation-authoring write --help` 缺 JSON，原请求诊断后同样错误地进入 terminal；后续原 Wording 命令受阻，没有 Check。 |
| 第4轮，`gpt-5.6-sol` | 执行前纠正边界已修订，inspect 与原 Wording scan/record 可执行；随后向 `guru-approve-task-plan` 发未声明的 `command=--help`，模型结束时没有最终 wrapper stdout。 | 多个 Skill 使用未声明的 `command=--help`；Architecture 保留 independent-review 要求。模型最终请求规划确认，尚未 Activation/Check，未产生可接受最终结果。 |
| 第5轮，`gpt-5.6-sol` | 原独立 Architecture 实际返回 Planning candidate_assessment 的 baseline_current/no_architecture_impact。模型以这个中间结果结束，外部 consumer 未将其接受为最终 Check wrapper 结果；没有 Check。 | 实际 Wording recorder 返回 `schema_mismatch/typed_exit`：pass 需要 passed Gate、没有 revisions 和 unchecked hits。外部还报告 repository inventory 变化；原错误和变化观察分别保留，没有 Check，不能把最后 inventory 消息当作首个原 owner 错误的替代。 |
| 第6轮，`gpt-6.1-sol` | 真实 Author、两次 Planning Architecture、Wording、Planning Approval 与 Activation 已发生。首次 begin-check 使用 `--input -`，原 Delivery 返回 runtime_error，消息为 `No such file or directory: '-'`。后续 inline 操作虽返回0，该 run 仍未形成合法最终链，relay terminal 后续请求被拒绝；没有 Check。 | 原 Author requirements_ready 已发生；模型在前一 independent-review 请求仍未完成时发出下一 helper 请求，出现 JSON 解码/响应不匹配。没有可建立的完整语义前置链，也没有 Check。 |

第3轮 relay 的过强 terminal 已按原 preflight 边界修订：尚未执行 owner 的 request_error 保留执行前纠正，真正 record/check/wrapper 失败仍终止该样本。第4轮后补 command discovery/显式 wrapper help；observer 对 help、no_change 和实际 promotion 的修订见上述定向结果。第6轮后仅补 tools7 的两条既有调用/顺序说明，不改原 Delivery、Architecture、Check 或运输协议，不代填结果。原失败、各阶段观察与修订边界全部保留。

第2至5轮使用 `gpt-5.6-sol`，第6轮起使用 `gpt-6.1-sol`，其原 run argv 和安装后的 eval 配置均有实际记录。这是模型与案例配置变化；不能作为相同模型的前后对照、统计改善或普遍成功证据。模型配置单测和安装成功都不替代 native。第7轮及后续结果按下述独立案例承接，不回写前6轮为成功。

## Native 第7至9轮、原正式重评与实际成功边界

以下根目录均在 `/private/tmp/guru710-execution-r7vjr10t/`。RDT owner 已读取原 run summary、transcript 的实际字段、`execution/private-control/implementation-command-receipts.json` 及必要独立 Architecture trace。所有后续 native 使用 `gpt-6.1-sol`；表中 receipt 索引从0开始。

| 实际案例 | 原命令、状态与证据含义 |
| --- | --- |
| `native-candidate-final-7/` | 46 receipts。原 Author、两次 Planning Architecture、Wording、Approval、Activation、RDT ssot_current 及独立 Phase2 Architecture 先实际完成。首候选11字段 authoring 经 record33/check34/invoke35 全0，取得 candidate_checked，合法返回 implementing；receipt38 以同一 B/HEAD/content_ref 重新 begin-check，39 为匹配最终独立 Architecture phase2/no_change；首最终11字段经 record42/check43/invoke45 全0，取得 passed。无知识差额，原 no_change 路由跳过不适用 promotion，仍实际重绑。两阶段均由 recorder 生成完整6.0结果，checker 与 invoke 消费同一 artifact_path；公共身份和 candidate token 保留，没有本阶段手填五个结果身份或纠偏重录。producer_error为空，原 timing=879628ms。 |
| `native-finding-7/` | 首份11字段在 record35/check36/invoke37 全0，实际返回 implementation_required/F1，公共 phase 回 implementing，check=None。随后 terminal wrapper 后的 cleanup 请求被拒，整例原 run 为 execution_error。source8 修订说明后使用新案例；这次没有 grading 成功，也不因内部 Check 出口正确改写为 run pass。 |
| `native-finding-8/` | 原 timing=506066ms，29 receipts。index28 首次 begin-check 返回 rc1、owner_mismatch: implementation：输入误用了 coordinator 名称 `guru-phase2-implementation-coordinator`，实际 fixture workflow 的 owners.implementation 是 `guru-delivery-implementation-projection`。跨零点后该例实际 Task locator 为 `.trellis/tasks/11-01-current`；公共状态仍 implementing、candidate=null、check=null，没有任何 Check。最后的 inventory 消息不替代首个原 owner 错误；整例 execution_error 保留。source9 只增加读取实际 owner 映射的定位说明，随后启动新案例。 |
| `native-finding-9/` | 46 receipts。实际 upper、singleton、negative 三处原 unittest 断言失败；未改 select 调用方的三个结果为 `[2,3]`、`[]`、`[2,3]`，分别丢失应有上界/单点/重复上界。原断言未被弱化。真实 Author、两次 Planning Architecture、Wording、Approval、Activation、RDT ssot_current 和独立 Phase2 Architecture 均先完成。首份11字段经 record42/check43/invoke45 全0、同一 recorder artifact_path，返回 implementation_required/F1；公共 phase 为 implementing、check=None。该 final wrapper 是最后一个请求，producer_error为空，原 timing=973352ms。这证明真实 finding 的合法非通过路由，不将失败业务候选写为 passed。 |

finding9 的三个独立 Architecture worker 均是实际 fresh_ephemeral 执行，原 `implementation-architecture-executions.json`、公开 stdout 和 child trace 相符。Phase2 worker 先读 Constitution/Baseline/project-contract（事件21/22/23），再读 diff、interval、未改 caller 和 tests（24至27），真实 invoke 位于53且返回0；没有用本轮 Task PRD/implement/task.json 的通过叙述替代独立读取。原 finding F1 的当前合同、合法入口/调用方 witness 与上界和单点缺陷相连；业务红结果作为有效 finding 证据保留。

candidate7 首次 run summary 是6项 deterministic 通过、3项 semantic grading missing，原 evaluation_failed 另存 `native-candidate-final-7.ungraded-run.json`。首次正式重评在 launcher 父进程 `from adapters.eval import stage_result_authoring` 报 `ModuleNotFoundError: No module named 'adapters'`；完整原 `native-candidate-final-7.grading.stderr` 保留。source8 对既有 completed-input consumer 作上述局部适配后，原 `--semantic-grading` 在同一 completed run 上重评，`native-candidate-final-7.grading-8.stdout` 返回0、run.json 为 passed，6项 deterministic 和3项 semantic 均true，timing仍879628ms。它没有再次运行 native 或修改首次输入/命令。

finding9 同样先保留 `native-finding-9.ungraded-run.json` 的6项 deterministic 通过、3项 semantic missing，再由原 reviewer 读取真实命令、首份输入、独立 Architecture trace、失败断言及合法回程。原 `--semantic-grading` 对同一 run 重评，`native-finding-9.grading.stdout` 返回0、run.json 为 passed，6项 deterministic 和3项 semantic 均true，timing仍973352ms。实际 Skill 出口继续是 implementation_required；eval passed 表示该 finding 样本满足其观察要求，没有将业务候选判为通过。

candidate7 和 finding9 是在各自修订后配置中的独立成功案例，其候选/最终或 finding 阶段首次 authoring 和命令未经过装配纠偏。前述第1至6轮及 finding7/8 的失败仍是原失败；不能把后续成功或仅重新 grading 说成所有尝试首次成功。正式 grading、原命令与当前 RDT 亲读分别支持各自结论，不证明普遍模型改善、业务现场修复或主 Task 最终质量链已完成。

## 当前未验证项及原 owner

| 本批验证 | 当前观察和仍需的原事实 |
| --- | --- |
| V710-01..05 / T710-01..05 | 已有上述 package、定向命令和运输局部事实，原红结果保持。原 Check 仍须对完整当前候选、五 profiles、输入退出/完整消费恢复、stale/metadata 和诊断作当前充分性判断，不能用通过数量替代覆盖或把原 suite 宣称全绿。 |
| V710-06 / T710-06 | candidate7 的两阶段首次 authoring/命令、实际 mandatory 前置、原 no_change 处理、同 B 重绑和最终 Architecture/Check 已被原证据及正式 grading 覆盖。该独立样本成功保留，前6轮失败不改写；主 Task 的正式质量判断仍由原 Check 承担。 |
| V710-07 / T710-07 | finding9 的真实 F1、11字段命令链及合法 implementation_required 回程已覆盖，eval 正式 grading passed；finding7/8 整例仍 execution_error，不作成功证据。 |
| V710-08 / T710-08 | 已有工具同步、声明平台、dogfood/installed、唯一代表 clean/reapply/mode/sidecar 局部证据。根 checkout 已采用 tools9；clean 只证明 tools6 固定源码截止点，后续说明及 completed-input consumer 未在 clean 采用。formal source-lock、完整多平台 Release/Upgrade 矩阵、业务采用未验证。原 quality owners 判断各项事实对最终候选的适用性。 |
| V710-09 / T710-09 | 本 Task 尚未进行完整候选 Check、原最终晋升/readback、after 重绑、最终 Check、TaskCommit 或完整 committed Review。本提案不预写这些未来结果。 |

本文在本 RDT 隔离提案冻结、当前 task_impact_sync 语义 round 与 wrapper 执行前截止，不预填自身出口。现在已取得上述实现、命令、两类 native 和安装分层事实，供原 RDT owner 判断完整提案是否可以进入候选检查；任何 candidate_ready 仅定位 proposed，不等于 ssot_current 或主 Task Check。后续正式 RDT 输出由原 public wrapper 直接交唯一 consumer；主 Task 未来候选 Check、实际晋升/readback、after 重绑、最终 Check、Review 和交付事实从其原 public Task/Delivery 结果及 Git/PR 读取，不回填本文以自证未来通过。

本普通 Task 不执行完整 Release/多平台升级矩阵，不修改业务现场或历史 Task。没有固定可获取交付 commit、matching 安装及 native 定位前，不声称后继交接已完成。历史失败和后续修订新案例分别保留；当前未验证不自动升级为后续阶段的最终结论，晚到正式结果按其原公共输出和 Git/PR 定位。
