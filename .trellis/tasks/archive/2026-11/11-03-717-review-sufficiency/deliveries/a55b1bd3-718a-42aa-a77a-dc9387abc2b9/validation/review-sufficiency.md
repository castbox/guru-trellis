# 审核充分性真实行为观察

## 范围与条件

本观察对应 D1 的 V3、AC3/AC4，不替代正式 Check、Branch Review 或 Completion。
旧 provider 固定为 `404c841e9ca917b4680831aa0becd2e26d72fa0c`；新 provider 使用本批完整 canonical 候选。
被测入口保留原 Skill、合同、公开 wrapper、前置和出口。没有使用方法片段、预填当前语义结果或纠偏提示。

验收侧在首次运行前固定 A–E 的对象、已知问题、合法配置和必要缺口。具体预期没有进入被测提示或 fixture。
代码对象 B、D、E 均实际执行三名不同独立子 Agent；首次架构 carrier 使用 `fork_turns=none`。
原始 session 记录确认主 owner 和这些子 Agent 都使用 `gpt-6.1-sol`、`medium`；没有指定模型覆盖。
CLI 为 `0.162.1`，两侧保持同一配置，关闭 hooks/apps/memories/MCP，使用 `--no-daemon`。

有效比较使用相同 `danger-full-access` 执行条件，原请求仍明确只读。每轮比较根目录受审 Markdown/Python 文件字节，全部为无变化。
没有观察到自行修复或 Task/Delivery 推进。原 installer 使用匹配 Core 文件和显式 Python 3.14 建立完整 provider；这些是评测前置，不是完整安装或 Release 矩阵证据。

## 逐例实际结果

| 案例与原入口 | 旧侧实际观察 | 新侧实际观察 | 结论与边界 |
| --- | --- | --- | --- |
| A：Issue 草稿，Clarify `standard_intake`，`mode=standalone` | 真实 Discovery ready 输入后，发现收件边界、筛选/数据时点、取消结果三项预定缺口；另指出角色范围和验收细化。原 record/check/invoke 返回 `blocked` | 同样发现三项预定缺口；另审查 CSV 内容、邮件交付、异步失败反馈和可观察验收。原 invoke 返回 `blocked`，明确本轮审查完成而需求尚未澄清 | 两侧没有编造产品答复、修改草稿或创建资源。都明确保留两种 UTF-8 配置。旧侧另将编码验收可观察性记录为 P2，详见下文；不能把所有额外 finding 都默认为改善 |
| B1：分散代码缺陷，独立 `working_tree` | 找到 total 使用页长度、取消误改其他任务、UTC 转换丢失 instant 三项预定缺陷；追到 HTTP/CLI；5 项测试中4项失败后仍返回 `reviewed` | 同样检出三项，保留共享入口影响和失败测试，返回 `reviewed` | 两侧均继续覆盖完整对象，没有找到少量问题后丢弃剩余范围；合法 HALF_UP 和条件性 CSV 缺席没有成为实现缺陷 |
| B2：真实同 thread 后继 | 核实分页已修复，保留取消/时区缺陷；发现新增 CSV 列序错误，补查共享 formatter 对 CSV 的影响 | 同样核对完整增量及未改消费者，承接适用原覆盖和原三名 carrier；实际5项测试中3项失败，仍 `reviewed` | 没有只核修复点；没有将旧分页问题继续作为未修复 finding；测试自身缺少目标取消/完整 adapter/CSV 观察的额外问题亦保留 |
| B3：同 thread、候选无变化 | 重新 capture/read，采纳上轮实际测试，没有重跑测试或更换 reviewer；完整报告后 `reviewed` | 同样复用有效覆盖与实际证据，完整报告剩余问题后 `reviewed` | 当前审核能在缺陷未修复、测试未全绿时有限结束；没有要求固定轮数或持续找新问题 |
| C：设计/实施文本，Wording `explicit_paths` | 检出提交/通知顺序倒置、取消状态扩大、总尝试次数变额外重试三项预定冲突；原 scan/record/check/invoke 返回 `blocked` | 同样完整报告三项，明确只读审查完成，原出口 `blocked` | 可选字体链接缺失没有全局阻塞；未修文件。本例仅证明固定文本语义/措辞审核，不证明正式 Planning Approval 或任意设计质量 |
| D：本地确定缺陷与必要来源缺失，独立 `working_tree` | 报告 `[3,4]` 求和得3的实际缺陷及失败测试；供应商时间格式合同缺失只限制相关结论；最终 `blocked` | 同样保留独立可证的本地缺陷，将 R2 的缺证与 R1 的实现错误分开；最终 `blocked` | 没有因缺一份合同而丢弃本地结论，也没有猜供应商格式或声称整个范围已完成 |
| E：正确本地实现与合法配置，独立 `working_tree` | 修正 fixture 自身测试缺口后，5项实际测试通过，原公开入口 `reviewed`，未发现可行动问题 | 同样无可行动问题，完整读取与三视角后有限结束，原公开入口 `reviewed` | HALF_UP、带偏移输入与未提供的条件性 CSV 均按来源接受；未制造默认偏好或外部部署门禁 |

A 的旧侧 owner-result 将两种编码列入 `confirmed_facts`，`open_questions=[]`、`clarification_rounds=[]`，没有要求重新选择编码。
但其 Gate 确实记录了 `encoding-acceptance / P2 / open`，理由是验收仅列类别而未逐格式描述观察结果。
因此不能将该项简写成“只有建议、没有 finding”。它针对验收细化，不是否认合法配置；是否过度提升须依据原验收合同判断，不能从更多问题数推出更好效果。
新侧在 CSV 验收建议中明确两种格式都须保留，没有把它们当作未回答的编码选择。

按预先固定的三项 Issue 缺口、三项初始代码缺陷、后继增量、三项文本冲突和必要缺证判断，旧侧已经表现正确。
本样本没有证明普遍召回率提升、少调查次数或任意对象的缺陷发现保证。新侧观察支持当前规则下的覆盖、诚实结束及原出口保持；问题数量不构成门禁。

## 保留的首次失败与同范围恢复

- 首次 A–E 启动因本机 MCP `invalid transport` 在 `thread.started` 前失败。通过单次 `mcp_servers={}` 排除无关连接，未改模型/provider/推理配置。原结果保留。
- 下一次旧侧运行遇到 macOS read-only sandbox 无法解析 managed Python cache；原 wrapper 返回 `runtime_dependency_missing`。这些原停点不是成功代码审核。完整安装与相同 wrapper 在原宿主条件下可执行，随后两侧统一为上述有效比较权限。
- 最初无 remote 的 A fixture 在真实 Sync/Discovery 仓库身份前置处停止。恢复到真实源码克隆后，native `standalone_review` bootstrap 仍在 transition 装配/历史预览处停止；没有将它改称产品缺证或语义通过。
- 最终 A 使用原合同声明的 `pre_task → standard_intake`：另一实际 owner 在每个真实克隆执行 Sync、Discovery 的调查、Gate、record/check/invoke。被测新调用只收到真实 `context_ready` 公共 DTO 和其薄 input projection，不读取上游私有 Gate。两侧草稿字节、B、模型与权限相同。独立 `standalone_review` 的首次 bootstrap 未被证明可用，也未修复该路径。
- A 的两个克隆均为真实 `castbox/guru-trellis` 源码，HEAD 为 B，origin 为真实 GitHub URL；没有给合成业务仓库添加虚假 remote。原 tools owner 分别返回 `tools_upgraded`，保留历史 Task、workspace 和用户配置，无 `.new/.bak`；formal Fork source lock 仍未验证。
- 最初 E 业务实现正确，但 fixture 测试未断言目标确实取消，也未精确检查 HTTP 金额和 CLI 时间。两侧实际 reviewer 都合理报告这两项测试缺口；首次输出保留，不算误报。经原候选资格流程后，只修 E 测试观察，B 的原 TESTS 保持不变。内存反事实检查确认：正确 E 通过，空取消、错误 HTTP 金额、原偏移 CLI 时间分别被检出。随后两侧按原期望重新运行，没有重写“正确完整候选应无成立 finding”的预期。

## 原始证据定位

完整 prompt、argv、events、stderr、执行状态、原 provider/target 和实际 root/child session 记录位于仓库外：`/tmp/guru-review-sufficiency-717/`。
技术 `execution_complete=true` 只表示 native turn 结束；上表按实际语义与公开出口区分了成功审查和入口失败。

| 有效比较 | 旧侧目录 / thread | 新侧目录 / thread |
| --- | --- | --- |
| A | `old-A-ready-entry` / `01a1a0ac-51bb-73a2-9f2c-48d7d034f779` | `new-A-ready-entry` / `01a1a0ab-7514-73d2-995c-05c8496bc03d` |
| B 三轮 | `old-B-attempt3` / `01a1a091-1bff-7100-8497-f54ee2bde48a` | `new-B-attempt1` / `01a1a091-1ad7-7810-8558-73ffedd9642f` |
| C | `old-C-attempt3` / `01a1a091-1ad7-7363-b382-04bb4a587894` | `new-C-attempt1` / `01a1a091-1ad7-70a1-bffd-0b56475d97e6` |
| D | `old-D-attempt3` / `01a1a091-1b06-79e3-af58-981f0c89a4ab` | `new-D-attempt1` / `01a1a091-1ad7-7972-9abb-f7c41fc201b0` |
| E 修正后 | `old-E-attempt4` / `01a1a09d-0431-7df0-84ef-c52d2e1ae357` | `new-E-attempt2` / `01a1a09d-0431-76e2-af02-f81199d0c7f1` |

A 原上游公共结果及调用记录分别在 `/tmp/guru717-A-old-upstream-ung4c58k/`、`/tmp/guru717-A-upstream-65fpl_to/`。
旧新源码克隆维护记录在主结果根的 `A-tools-old`、`A-tools-new`；此前所有 `old-*`、`new-*` 首次结果均保留，没有覆盖。
原始目录是本次本地观察材料，不是公共 Skill output、工作流状态或新的长期 ledger。

采集器机械检查3项通过；E 正确/反事实检查通过；新增 Python 内存语法检查及 scoped `git diff --check` 通过。
本观察不证明业务生产、完整多平台 installer/upgrade/Release 矩阵、外部专业 Skill 独立接入，或所有 provider/target 组合的实际 Agent 行为。
实际 dogfood、受管投影和 drift 结论由原安装 owner 的独立结果承接。
