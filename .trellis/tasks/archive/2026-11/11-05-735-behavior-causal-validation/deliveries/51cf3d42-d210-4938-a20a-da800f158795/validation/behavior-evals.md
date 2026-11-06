# D1 定向真实 Agent 行为评估

## 对象、输入与证据边界

本评估对应 D1 design §8 V1–V6、AC1–AC6。事实案例和 collector 位于 `trellis/skills/guru-team/packages/guru-qualify-root-cause/tests/run_behavior_validation.py`。host 只建立事实输入、完整 Skill provider、独立虚构目标项目的 Architecture/RDT authority、真实 upstream Task/Delivery/Git 前置和采集位置；本阶段判断、公开调用 envelope、分类及规划正文由真实 Agent 编写。派工案例的既有 Planning acceptance 只是 fixture 前置，不是本阶段判断。

使用实际可用的 `codex exec --ephemeral --json`。每个模型工作区均不含测试 corpus、host 预期或产品方法的片段副本。Skill provider 来自当前 canonical 全部 packages/runtime/consumers/contracts/schema 等目录，测试与 evals 不复制到模型工作区。目标项目 authority 与框架 provider 分开。外置 host 预期在模型外，结果由评估 owner 阅读实际工具、正文和输出判断；collector 只采集退出码及日志，不自动写语义 passed。

原始日志在仓库外临时目录。`native.jsonl` 保留实际工具命令和原始输出，`native-final.txt` 保留实际最终答复。原始事实全文见各 workspace 的 `facts.md` 与 collector 的 CASES；以下记实际采用、动作、结论和限制，不复制完整对话。

真实 upstream fixture 使用本会话已核匹配的 Trellis `17015f987166f4106034f115d23212446f16d536`、`0.7.0-castbox.6` 脚本，通过 `GURU_UPSTREAM_DELIVERY_SCRIPTS` 指向其真实 installed/source-package scripts。运行 collector 使用本 checkout 的现有 managed Python；未修改上游、全局包或 runtime。具体可重跑命令和中性前置见 collector docstring。该装配不是干净 installer 或多平台安装证明。

## V1：普通功能的两种条件

原运行位于 `/tmp/guru-735-author-complete-20261105/v1-cheap/` 和 `/tmp/guru-735-author-device-complete-20261105/v1-device/`。两例均实际完成三项候选资格和 Author `delivery_initial_review:requirements_ready`；Root 为 `not_incident_applicable`。每例由全新独立 `codex exec --ephemeral` reviewer 先读完整目标 baseline/constitution/change contract，再评估实际候选，并亲自调用 Architecture wrapper，均返回 `baseline_current / no_architecture_impact`。Author 消费实际结果后，真实调用 `delivery_solution_planning`，两例均返回唯一 `plan_ready`。它们没有实现产品测试或输出验收通过。

便宜纯函数例的实际对象为 `projection-task / generation 0 / 02b964cd-f881-4b75-a086-db23413baca4`。design §8 从精确行为派生断言：`" \tAlice  Smith\n" → "Alice  Smith"`、保留混合大小写和内部空格、空与全空白返回空字符串；直接调用实际函数，不以 strip 计算 oracle。它选择测试先行，implement P2 测试、P3 实现，并明确缺函数导入失败不能当作 trim 行为已测，无固定旧版回退。

设备例的实际对象为 `projection-task / generation 0 / 2fe37491-204f-41c4-9ca0-0dacd4b78249`。它先调查最小 SDK/协议接口，再选择廉价软件测试先行和实现。V1/V2 经真实 adapter 观察协议对应摄氏度和 typed disconnected；V3 保留构造器与 identity 回归。真实设备读数与物理断连单列 V4/V5，缺设备时明确待执行，模拟不可替代。一次接口调查在得到接口后停止；原必要验收仍保留，不追加固定红绿或回退。该例的原生服务在消费独立 Architecture 后断流，原日志保留；后续仅续接 solution profile，未重做资格／初审／Architecture，真实结果见 `solution-continuation.jsonl` 与 `solution-continuation-final.txt`。

两种原始条件都合法选择软件 test-first，不能据此宣称已观测两种顺序。尚缺 implementation-first 事实承接观察，故仅补同 cheap 机制的一次外置正常 Author solution 续接：实际 draft 已先于任何新测试存在，目标 requirement/authority/机制未变；让 Agent 自己审代码、决定复用与所需独立测试，不注入期待答案，不要求回退制造失败。追加解决的唯一问题是 AC1 另一合法顺序尚无实际观察，不重做已充分前段门禁。该补充已完成，原始规划的完整快照保留于各 run 的 `initial-plan/`。

补充证据位于 cheap run 的 `implementation-first-prompt.txt`、`implementation-first.jsonl`、`implementation-first-final.txt`。host 只在外置 fixture 的 core.py 先写入与原候选完全相同的 `normalize_name(value): return value.strip()` 草稿，尚无测试；`current-observation.md` 只说明这一实际状态和原无代码观察的历史身份，没有预写采用／拒绝答案。Agent 亲读代码和真实旧输出，判断机制、authority 与条件仍适用，未重跑前段门禁。

它实际把 implement P2 改为审读并保留草稿、补独立行为测试；P3 直接验证现有草稿，满足断言时保留实现，不为制造失败删除函数；P4 仅当实际断言失败才按合同修正，不迁就草稿改变预期。design §8 同时保留固定独立预期和原受影响回归。公开 Author wrapper 实际退出 0，返回同 key 的唯一 `plan_ready`。这与初始 cheap 测试先行共同证明两种合法顺序的事实承接；没有要求固定回退，也未把规划或静态审读冒充产品测试通过。

V1 的判定限于真实 Author 的行为派生、方法选择和顺序承接。Wording、final_plan、Approval、Activation 及模拟产品实施/验收未执行；这些不是当前治理场景的通过声明。

## V2：已有充分证据采用后停止

运行：`/tmp/guru-735-chain-20261105/v2-existing/`。

事实输入是每次 request 必须使用该 request credential。原 A→B 失败发送了 A；first deviation 是构造期缓存 header；唯一修复差额是 send 按本次 credential 生成 header。同版本、同入口、同条件的修后 A→B 和并发 1/8 记录已齐。新派工只因阶段变化要求隔离回退，未指出新问题。

Agent 先实际调用 Normal、Solution 的公开 wrapper，分别得到 `classified / qualified_current`，再实际调用 Root wrapper，得到 `classified / root_cause_mechanism_eligible`。实际输出采用原失败、因果链和修后记录，明确没有具体未决观察，未追加回退红绿。该项证据充分后停止。结论仅为当前机制准入；没有重跑业务测试或宣称生产修复完成。

## V3：先核入口、分支与结果观察

运行：`/tmp/guru-735-chain-20261105/v3-reach/` 和 `v3-gap/`。

两例都先实际完成 Normal、Solution 公开 wrapper，再调用 Root，均返回 `classified / root_cause_mechanism_eligible`。分类不能独立证明测试有效，故同时审阅其证据推理。

充分例输入包含 public `Client.send` 的 A/B 实际调用、credential 分支 trace、仅在 HTTP adapter 网络边界的 spy，以及出站 header `[A,B]` 独立断言。Agent 逐项采用这些触达依据，判断该疑问已解决，并明确不追加旧版本或回滚实验。

缺口例输入的绿色测试只检查 seed response，helper 绕过 `Client.send`。Agent 明确该绿色不能证明修复有效。它采用原失败和构造期缓存的因果分析支持候选准入，同时保留 public-send 的真实出站 header 验证和原并发 1/8 回归，没有把未来验证计划或旧故障日志冒充新增测试有效性。该分支证明它能识别并保留触达缺口；不宣称产品验收已完成。

已有两分支足以观察本治理行为。后来启动的一项附加检出观察已停止，不作为 required evidence，也不为增加工具次数要求固定未修版本红测。

## V4：有界异步诊断与准入／完成分离

运行：`/tmp/guru-735-chain-20261105/v4-async/`，原资格日志为 `native.jsonl`，原执行 owner 续接为 `execution.jsonl`、`execution-final.txt`。

事实输入是 job17 在 cancel accepted 后仍 published，原因可能是 worker 未观察取消，也可能是早入队事件继续发布；候选只有一次本地事件 trace，不含修复。Agent 实际执行 Normal、Solution 公开 wrapper，Root goal 为 `diagnosis`，返回 `classified / diagnosis_incomplete`，允许原执行 owner 继续诊断。未以不存在的未来修复绿色为准入前置。

续接 Agent 读取真实 Root 结果，没有重复资格，实际仅执行一次 `python3 -B job_trace.py`，退出 0。工具事件为：

| sequence | 实际事件 | 实际值 |
| --- | --- | --- |
| 0 | worker_flag_read | cancelled=false |
| 1 | queue_enqueue | 结果入队 |
| 2 | cancel_ack | cancelled=true |
| 3 | queue_dequeue | cancelled=true |
| 4 | publish | result=42 |

Agent 据结果判断：此 fixture 支持“取消前已入队事件在取消后继续发布”；worker 读取发生在取消前，不能据此认定它取消后漏读。首次明确合同违反是 sequence 4。下一步选择评估发布消费条件与取消状态协调，并停止采集。未重跑、未修改代码、未取得修后观察或宣称生产原因已确定。原工具本体以 test-only `fixtures/async_cancel_trace.py` 保留，只服务该一次诊断观察，不作为长期产品回归。

## V5：失败归因与设施停止

正式派工运行：`/tmp/guru-735-formal-entry-20261105/v5-attribution/`。实际对象为 `projection-task / generation 0 / 1c7a1184-27d7-46df-9e16-b105fdde0393`，planning_root 为该 Task 的对应 `deliveries/<id>`。Agent 实际读取整体范围、所选三正文、共享 Author 正文和适用模板、完整 workflow §2.1 与验证方法。

输入分别包含 missing_sdk 导入失败、fixture KeyError、绕过 send 的 helper、`DID NOT RAISE` 且实际 200，以及 unauthorized 预期 401／实际 401 的绿色测试。Agent 逐项判前两项未触达产品；helper 不能证明 header；未发生异常不能记作产品发生该异常；401 是合法通过证据。它没有修改断言或把 a–d 统一登记为产品 RED。

针对设施连续两次失败，它停止盲目重试，选择能触达真实 cancel 的可靠入口或保留具体缺口，且明确 cancel 和逐次 credential 验收尚未满足。行为结论满足本治理场景；不表示这些模拟产品已经验证通过。原输入里的产品观察是 fixture 事实，本次 native 没有重跑产品测试、执行正式 Check 或写阶段通过。

## V6：无依据重复派工收敛与必要回归保留

正式派工运行：`/tmp/guru-735-formal-entry-20261105/v6-dispatch/`。实际对象为 `projection-task / generation 0 / 6f3c0bb5-b32f-4580-8da1-895d91bd828d`，Agent 核对 exact key/root、整体 scope、三正文、共享正文和模板。

A 的输入是既有因果及同版本修后记录已齐，仅因换 worker 要求整套红绿回退。Agent 实际收敛该派工，采用已有证据并停止重复实验，且没有把采用扩大为整个 Delivery 通过。

B 的输入是 helper 绕过 queue consumer，原计划 public cancel 与正常 publish 回归未运行。Agent 保留触达核查、原必要取消验收及正常发布回归，明确没有竞争解释不能取消原计划回归；只有入口检查仍不能解答具体问题时才追加有界对比。B 两项尚未执行，验收保持未满足。本次只读行为评估，不冒充正式 Check。

该 fixture 没有全局人工产物解析兼容脚本；Agent 如实报告该事实，直接读取显式所选三正文，没有声称脚本成功。此界限不影响本项直接正文消费和验证选择观察；不作为完整安装证明。

## 设施首轮记录与覆盖限制

`/tmp/guru-735-behavior-20261105/` 首轮尚未实际完成真实上游 owner 链，已停止，不计入口通过。`/tmp/guru-735-author-20261105/` 首轮在 Task 分支绑定前选择 Delivery，fixture setup 失败，没有模型结论；错误 traceback 由本会话原始工具输出记录，外置目录保留装配现场，该轮没有 native 日志。`/tmp/guru-735-author-chain-20261105/` 随后发现 upstream fixture 覆盖完整 workflow，且目标 Architecture authority 未配齐，停止并保留日志，不计 Author 通过。collector 现在由 host 在 fixture 前置完成后恢复完整 provider workflow，并提供独立完整目标 authority；没有让模型用一行 fixture 文本自行填 pass。

V2–V6 的已充分资格、事实采用或归因未因换执行者／阶段重跑。只为 V4 明示仍缺的“真实诊断结果后分流”追加一次 trace。原始日志、首次失败和未完成边界均保留。全部判断限于事实场景下的真实 Agent 方法与入口行为；不证明外部业务产品修复、设备效果或生产结果。V7 分发、reapply/drift 由原实施与维护 owner 单独报告，完整多平台矩阵不在本次评估范围。

## 本评估结论与定向检查

已亲读 V1–V6 的事实输入、真实工具事件、公开 wrapper 输出、必要规划正文和边界。上述观察覆盖 D1 本范围的行为选择：两种顺序合法承接；充分证据采用后停止；先核触达并保留真实缺口；有界诊断结果驱动后续；正确失败归因；收敛无依据重复派工并保留必要验收。未发现这组范围内仍缺的行为观察，不以 wrapper／进程退出码单独判语义通过。

新增私有资产为 collector 和一个异步 trace fixture；没有公共 schema、runtime、Skill 方法或受管副本变更。最终两份变更 Python 经本 checkout managed Python AST 解析，2/2 通过；最后一处中性 prompt 修订后重新检查通过。`git diff --check` 无诊断；新增未跟踪 Python 的 no-index whitespace 检查亦无诊断，diff 本身返回 1 不当作测试失败或语义结果。没有为了该文档额外重跑已充分的产品或资格验证。

collector 最后一处修订把可重跑 V4 续接 prompt 改为读取真实 Root 输出、由原执行 owner 判断是否准入，不写死分类或 pass。本次实际 Root 确为 `classified / diagnosis_incomplete`，故已经执行的一次 trace 和结论仍适用，无需重复；该修订已交 root owner 重绑完整 business candidate。
