# 完善长文读取合同：整体需求

## 1. 来源与术语

| ID | 来源与位置 | 角色 | 本 Task 用途 |
| --- | --- | --- | --- |
| S1 | [Direct Source #848](https://github.com/castbox/guru-trellis/issues/848)，当前完整标题、正文 | 要求、约定技术约束及历史实验事实 | 定义读取方法、首读导航、验证与排除范围 |
| S2 | [已接受复审评论](https://github.com/castbox/guru-trellis/issues/848#issuecomment-6891318170)，完整复审结论 | 要求及证据边界 | 保留名义请求与实际显示的区别、初失败和跨调用补显事实 |
| S3 | `trellis/presets/guru-team/spec/workflow/companion-scripts.md`，Reading Required Contracts In Full / Intermediate Command Stdout 1.0 | 当前合同 | 原共享读法 owner；JSON、receipt 和 typed exit 保持原完整消费合同 |
| S4 | `trellis/skills/guru-team/packages/guru-review-change/SKILL.md`，provider 解析与首读入口 | 当前实现证据 | 确定直接独立 Skill 首读导航的真实消费者 |
| S5 | `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`，AGENTS_AI_FIRST_BLOCK | 当前分发证据 | 由原 installer 分发 AI-first 短导航，不让 Python 判断读取充分性 |
| S6 | `trellis/presets/guru-team/scripts/python/test_clear_technical_writing.py` | 当前测试证据 | 复用受管规范、入口引用、用户文字保留和 reapply 测试载体 |

“内层预算”指每条 `exec_command.max_output_tokens`；“外层预算”指一次 `functions.exec` 编排返回的显示预算。二者独立。本文数值是调用请求策略，不能代表宿主实际容量。

Task 身份为 `848-required-contract-reading`、generation `0`，集成与 PR 目标均为 `main`。固定调查来源为 `origin/main@0fb7dc9aac817a684c2f95bebb6570061a5ef868`。本文拥有整体需求；Delivery 规划拥有选定切片的方案与实施安排。

## 2. 背景与问题

S1 的 G02 首轮外层原量 10,734 token，缺省预算 10,000，丢失 734。第二轮虽改为输出 shell 的 `.output` 正文，却合并返回写作规范、contract、review-method、interface，原量 19,147，仍丢失 9,147。另有读取同时发生内外层截断。

直接问题是没有按最终返回总量配置两层预算。完整回执的 JSON 转义增加体积，但不能充分解释第二轮截断。旧版及当前共享方法已有两层预算、连续分段和截断补读规则；当前差额是先要求分段、未展开按单次调用提高外层预算，直接独立入口也未在首次长文前加载方法。入口缺口是促成因素，不能证明它是参数选择错误的唯一原因。

S1 已保留同形只读对照：内层20,000、外层24,000的两个原始结果分别估算8,548和10,599 token，原始正文完整，合并显示仍截断。外层改为40,000后仍在同位置截断，所示缺失量仍为7,159。后续独立调用从第一次已保存的原内存补显10,599 token那组正文成功，没有重跑读取。这些是来源中的既有实验，不是本 Task 已完成的验收。宿主参数是否生效及额外显示限制尚未定位。

## 3. 目标与非目标

使 workflow、standalone、恢复和子 Agent 的必需正文读取先复用完整材料，再按实际工具与显示容量选择足额预算或必要分段，减少可避免的截断返工。当前 AI 仍须实际完整获得并理解所需正文。

整体包含原共享方法修订、AI-first 与直接独立入口的短导航、必要共享入口适配、原受管安装同步、定向回归及真实采用验证。全部责任进入整体 Completion，不能用源码修改或一个 Delivery 合并替代。

非目标：新增读取器、脚本语义判断、公共 Skill、schema、持久读取状态或 gate；取消全文要求；以父聊天已读标记替代子 Agent 上下文；修改宿主全局配置；承诺任意大容量；把全部历史截断或规范重读计为浪费；业务付费调用；完整多平台 Throwaway、升级或 Release 矩阵；实施 #847 或创建其它 Issue。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置与触发 | 行为与可观察结果 |
| --- | --- | --- |
| SC1 首次或恢复读取 | 原 AI owner 需要必需正文，已有完整材料或需要工具读取 | 确认实际范围并复用完整原生注入；缺失正文按实际预算直接读取或分段，获得全文与文件尾 |
| SC2 嵌套调用 | Codex 用 functions.exec 包装 exec_command 读取 Markdown | 内层覆盖各命令，外层覆盖编排总量及载体开销；观察实际显示，参数存在不证明成功 |
| SC3 仅外层截断 | 内层原文完整且保存在平台既有跨调用 owner 内存 | 后续独立调用从原内存缩小批次补显，无新读取命令，不创建文件缓存 |
| SC4 内层缺失或内存不可用 | 原结果缺失、局部变量失效或无法定位缺失范围 | 补读缺失部分；范围不明时重读足额全文或连续覆盖范围，直到文件尾 |
| SC5 直接独立入口 | 无继承历史的新 Agent 从 provider-aware guru-review-change 启动 | 先读原短方法小节，再读必需长正文；不先读整本 companion-scripts，不要求创建 Task 或读完整 workflow |
| SC6 受管采用 | 原安装 owner 从完整匹配 canonical 来源更新安装 | 同步必要规范与入口投影，保留用户文字，按原机制处置 sidecar；结果可核验 |

顺序：确认所需及已有完整正文 → 选择真实工具与预算 → 检查实际全文 → 截断时判断层级和原内存可用性 → 补显或连续补读 → 原 owner 执行依赖该正文的判断。没有新增持久状态转换。

## 5. 行为要求

### R1 实际范围与完整性（SC1）

先确认实际必需材料。复用当前仍完整可用的原生注入与已读正文，不因预算提高扩大范围。shell 成功、完整 raw stdout、路径、行数或参数存在均不证明 AI 已获得全文。充分性仍由当前 AI owner 判断。

### R2 两层预算与直接读取（SC2）

工具能完整承载材料时，显式配置足额内外两层预算并直接读取。内层覆盖每条命令预计实际输出；外层覆盖本次全部输出与载体开销，不能只取最大一条。超过缺省10,000不自动要求拆分。

Codex 初始请求采用内层20,000、外层24,000，按实际材料调整。32,000／40,000只是更大材料示例，不是必经档位或上限。这些不是新固定阈值，不改宿主全局配置，不保证实际显示层采用同值，也不承诺宿主接受任意大请求。其它工具只用真实暴露的接口。

外层参数放在 functions.exec 首行 `// @exec: {"max_output_tokens": 24000}`；内层 `max_output_tokens: 20000` 放在 tools.exec_command 参数。共享方法提供两层位置明确的调用例子。

### R3 正文载体（SC2）

exec_command 读取 Markdown 时输出 `.output` 正文，避免无必要转印完整回执。原生文件工具消费实际正文载体，不假设所有工具都有 `.output`。载体选择不能代替足额预算。同次合并只用于本次确需且总量能完整容纳的材料。

### R4 容量回退与截断分层（SC3、SC4）

超过实际容量、无法确定预算能覆盖预计总量或调整后仍截断时，再按文件或连续相邻范围拆分，覆盖所需全文与文件尾，包括无末尾换行的正文。固定行数不是合规条件。名义预算高于预计总量仍截断时保留事实，不盲目反复调大或据参数宣称完整。

仅外层显示截断、且完整原结果仍在平台既有跨调用 owner 内存时，先缩小批次重新显示，不重跑读取。exec 调用结束后的 const 局部变量不是跨调用内存。内层已截断、原结果丢失或无可用跨调用内存时补读缺失部分；范围不能界定时重读足额全文或连续覆盖范围。

functions.exec 确实暴露 store/load 时，原调用结束前保存完整 output，后续从同一内存按实际容量补显，消费后释放。不得假设其它运行器也有该 API，不新增内存服务、文件缓存、读取 ledger 或持久 checkpoint。

### R5 首读导航与唯一 owner（SC1、SC5）

原共享 Reading Required Contracts In Full 小节是主要修改位置。原 AI-first 条款及直接独立 Skill 的 provider-aware 入口在首次长文前定位该短小节。只加载该小节，不先要求整本 companion-scripts。其它入口根据实际共享关系适配，不复制方法正文，不把完整 workflow 或 Task 创建变为独立操作前置。Python 若参与，只分发导航文字。

### R6 原结果与副作用恢复（SC1—SC5）

producer JSON、recorder/checker receipt 和 typed exit 继续从完整原始 stdout 在内存消费，不按行截取后重构。显示不全不得触发 mutation 重复执行。保留原失败与原 owner 恢复路径，prose 分段不替换这些原合同。

### R7 分发与实际采用（SC5、SC6）

canonical 修订由原受管安装 owner 同步受影响投影。定向 source/installed、声明平台、reapply 和适用 drift 验证承担其实际层级。链接或静态检查不能替代无继承新 Agent 从直接独立入口实际采用的证据。新 Agent 自行满足全文加载，不依赖父聊天已读标记。

## 6. 约束与依赖

- Markdown 拥有方法和充分性判断；脚本只处理原职责中的确定性事实。公共 Skill id、typed exit、schema、DTO 和现有 gate 保持原含义。
- 受管同步采用完整匹配 canonical 来源及原 guru-upgrade-tools 或适用 installer，不手工覆盖 dogfood 作为唯一修复。原 hash、用户改动保留、.new/.bak 和 freshness 规则继续有效。
- 真实 functions.exec／exec_command transport 是预算与补显观察入口。按实际效果报告，不换短材料后宣称原合并场景通过。
- 新 Agent 验证采用无继承上下文、原独立入口与所需长正文；只证明实际执行层级，不隐含完整业务审核或付费调用。
- #847 不是硬前驱。保留并行 Task、worktree、session 和资源；合并前等待协调器的同仓 integration owner。
- 没有业务 API、数据库或数据模型迁移。本项改变 AI 文本读取方法与导航，没有并发、锁、crash 或跨 OS 加固需求。

## 7. 可观察验收与验证方式

| AC | 对应要求/场景 | 输入、入口与预期结果 |
| --- | --- | --- |
| AC1 同形 transport | R1—R4 / SC2 | 用样本第二轮同形四份必要公开材料，在真实 transport 请求内层20,000／外层24,000，观察实际正文与文件尾。完整则记录一次显示；仍截断则保留初失败，证明原内存补显或连续回退补齐。容量允许时观察超过10,000完整显示，不将其变为所有工具硬前置 |
| AC2 内层缺失 | R4 / SC4 | 针对已观察内层超量，确认仅提高外层不能恢复内层丢失正文，连续补读覆盖全文与文件尾；不扩为任意长文压力矩阵 |
| AC3 跨调用补显 | R4、R6 / SC3 | 原调用保存完整结果，实际仅外层截断后，后续独立调用从原内存补显，无新的读取命令。不能只在同一调用引用局部变量证明恢复；无内存则按 SC4 补读 |
| AC4 新 Agent 采用 | R5—R7 / SC5 | 无继承历史的新 Agent 从修订后的直接独立入口开始；观察先读原短小节，再读必要长正文，按实际材料选择预算或分段，不先读整本 companion-scripts。静态引用不替代该观察 |
| AC5 受管分发 | R5、R7 / SC6 | 原 owner 同步 canonical 与必要安装/平台投影，执行定向 source/installed、reapply 和适用 drift，核对用户内容及 sidecar 处置；不声称完成多平台升级或 Release 矩阵 |
| AC6 合同保留 | R1、R6 / SC1—SC5 | 原语义审查和必要定向回归确认全文要求、provider 分离、JSON/receipt/typed exit 完整消费、mutation 恢复及公共接口未弱化；没有新增读取器、持久 ledger 或脚本语义判断 |

整体完成须覆盖 AC1—AC6，并经过原 Check、完整独立 Review、Delivery readiness、整体 Completion、Closure 和 Finish。验收当前均待本 Task 实施验证；既有诊断事实按适用性采用，不能替代修订后的新 Agent 验证。

## 8. 实际未决项

当前需求、来源和范围没有阻塞性未决选择。具体修改位置、必要共享入口集合、测试安排和受管同步方式由原 Delivery Author/Architecture 细化。

宿主名义外层预算为何未改善显示仍未知。本 Task 保留该边界，通过实际容量核验与补显/补读完成既定目标，不承诺定位或修复宿主限制。source 或 scope 真实变化回原 Clarify；本文还须原 Clarify 审核并由公开 accept_scope 建立接受关系。
