# #599 验证与边界

本文件记录本次实际结果。源码、安装投影与实际行为分别验证，不互相替代。

| Test | AC | 方法 | 结果 |
| --- | --- | --- | --- |
| T599-01 | AC1 | 核对 STEMG 官网、About、FAQ、Downloads；逐条核对 GTW 元信息 | 通过。版本为 Issue 9 / 2025-01-15。仅采用已核对公开原则；未取得完整 PDF、编号条款和完整词典，不声明完整实施或认证 |
| T599-02 | AC3/AC4 | 写作 owner 与主会话逐例核对 GTW-001–012、E1–E13 | 通过。保留条件逻辑、否定、例外、顺序、术语、义务强度、literal、授权功能修改与脱敏边界。短句/主动语态为建议；准确性优先 |
| T599-03 | AC2/AC7 | source packages、ownership、完整安装后的22平台入口格式/引用解析、全部 active native Skills 引用 | 通过。40 packages / 124 commands；ownership 22项、native 5项、platform inventory 11项均通过。完整fixture引用/reapply测试通过。仅证明分发和投影 |
| T599-04 | AC5 | 实际 Codex CLI 主会话、native resume、独立 child、缺失/恢复；AI核对实际trace与输出 | 加载与恢复路径通过。详见下文；首次有Task输出发现两处遗漏，经原写作owner自检补齐。不得据此声称模型每次输出均无遗漏 |
| T599-05 | AC6 | 唯一代表完整安装/reapply、AGENTS字节保护、dogfood tools维护与drift、逐项sidecar检查 | 通过。代表安装和reapply均为原installer真实调用；用户区字节不变，重复应用稳定。当前dogfood同步后drift通过，零未解决sidecar |
| T599-06 | AC7/AC8 | 既有审核职责/I/O/typed exits比较、Phase Index/continuation提取、语法/whitespace与精确Delivery validate | 通过。只新增既有职责内加载定位；无语言审批或新I/O。shell语法、Python compile、JSON/TOML入口解析、git diff --check通过；task validate使用确切Delivery UUID |

## 实际 Codex 行为

平台为 codex-cli 0.162.1。以下为实际会话身份，不是人工创建的业务 Task。原始trace留在本机临时验证环境；本文件只保留复核所需身份和结果。

- 无 Task：`01a148c7-ab89-7833-8095-d307b0bfcd43`。目标为唯一代表完整安装。原context查询确认 currentTask=null；上游自动生成的bootstrap Task没有被选中。先输出简短加载提示，再完整读取34192字节正文，随后生成中英改写。AND条件、否定/例外、顺序、建议、接口原文、脱敏标记和未验证说明均保留。
- 原生恢复：对上述确切UUID执行 `codex exec resume`。原完整正文仍在上下文，无compaction；随后按同一用途继续输出，保留原语义。不是第二次普通exec冒充resume。
- 有 Task：`01a148c9-a13a-75a3-8e10-d5c301922ae9`。在当前真实#599 checkout，通过已绑定的当前context读取官方continuation；实际返回 TaskId=599-clear-technical-writing、generation=0、DeliveryId=661412bf-0be8-4c0c-9c05-b82f31cb7160、phase=implementing。首个实质输出前已完整读取同一正文。首次改写遗漏了建议句，并弱化了“必须保留”消息的义务；同一会话原写作owner自检明确指出并补齐，最终正文完整保留。该修订属于原写作职责，不新增审核阶段。
- 独立 child：父会话 `01a148c9-601b-7b91-85df-8fac9adc02df` 实际以 fork_turns=none 创建 `01a148c9-8797-7da1-b80d-c296fb024ae7`。child在自己的trace中调用cat完整读取安装正文（max_output_tokens=20000，无截断），之后才输出。父prompt未复制规范全文。结果保留 `A AND B AND (NOT C OR D)`、Check→Delivery Review顺序、建议强度、`passed` 和线上未验证边界。
- 缺失与恢复：`01a148cb-e615-76a0-b536-34a7e3b2ad12`。在同一专用fixture的普通缺失依赖状态下，实际cat失败后仅报告缺失路径并暂停改写。通过原source-cwd `apply.sh --repo <fixture> --platform codex --json` 恢复正文，返回status=ok；随后对同一UUID执行native resume。它重新完整读取，再继续原改写，无新增审批，无业务Task创建。

完整读取的机械复核比较cat输出与安装正文，确认含E13和正文结尾、没有截断。AI另行比较实际输出和原文。原生projection verifier不计入行为通过。

有Task实验中，系统git启动器导致最初context查询迟缓。改用已有CommandLineTools git的PATH后，官方读取成功；未修改上游文件、hook或全局包。被中断的旧查询不计为通过。

## 安装、定向验证与范围

代表环境使用匹配的CLI/Core 0.7.0-castbox.3；安装包与原tar的739/274个文件bytes/modes已核对。官方custom marketplace固定dev基线完成初始化，再应用当前未发布canonical workflow与完整preset。该证据不声明当前候选已远程发布。未另建第二个代表clean throwaway；单元测试自有fixture不作为额外Release矩阵。

当前dogfood普通apply因228条既有legacy Task记录触发原预检而停止。随后按原 `guru-upgrade-tools` 的 local_candidate 路径执行唯一冻结的tools-only操作，返回tools_upgraded；原归档、Task、会话和peer指针保留。该结果明确包含 formal_fork_source_lock 未验证边界。未迁移或删除历史数据，未伪造安装清单。实际目标自身native入口及installed验证通过，dogfood drift通过。

managed-spec既有4项定向测试涵盖新映射的普通冲突、用户编辑、升级与hash行为；AGENTS4项、native5项、platform inventory11项通过。新增完整fixture测试验证全部22平台及其active Skills的正文引用，并在reapply后检查正文bytes、用户AGENTS和零sidecar。platform inventory旧mock与production关键字不匹配，已仅适配mock的python参数；production行为未改。

首轮独立Check发现 CHK599-F1：新增测试曾使原测试文件2966→3019行，违反本仓库3000行限制。现将新增职责机械迁到 `trellis/presets/guru-team/scripts/python/test_clear_technical_writing.py`（81行），通过composition复用原fixture并保留全部断言。原测试文件恢复2966行，与本分支基线无diff。新模块实际运行1项，116.621秒通过；无旧测试重复发现，语法与whitespace通过。规划D7对installer行数的派生判断不准确：实际installer为2936行；此旧判断不作为豁免，当前修改的非生成源码均未超过3000行。此修复没有改变scope或solution，无需Planning reentry。

完整多平台升级与Release矩阵未执行，不在本次范围。其他平台的实际行为未验证；不由Codex结果推定。源码修改不证明业务仓库已自动采用新规则。ASD完整PDF、受控词典和认证不在已验证范围。
