# #153 验证结果与边界

本文件是本贡献唯一 Test 结果来源。规范正文、教学示例和追踪表不代替实际行为证据。以下分别记录 Codex 实际行为、确定性检查、目标安装与外部结果；正式 Check、Review 和整体 Completion 由其原 owners 另行判断。

## T153-01 修改前调查

已读取四原 owners 的写作、正文/评论操作、固定完整 title/body 审核及创建/回读合同。修改前另从简略工程请求实际执行 Selector、Sync、Discovery、Clarify 草稿更新与刷新、Wording、Readiness：最终返回 `ready`。输入是改进 `check-skill-packages.sh` 人读输出，只写草稿；实际查证 source/installed 模式和现有 JSON，未创建资源。

该结果证明原正向链可用，不能推定所有写作都存在遗漏。差额为共同内容规范和最终正文整理指引的显式性，因此本轮复用原 scanner、executor、freshness、恢复及 public I/O。它不是变更后 V1–V7 或新规范采用证据。

## T153-02/03 变更后实际 Agent

执行者在本 Task 匹配安装上实际完整读取共同 `issue-content.md`、语言规范、原 Author 来源规则及四个更新后的 Skill，并按原职责进行调查、写作和语义审核。输入从“检查写作前完整加载规范、缺失暂停、恢复继续”的简略请求开始，仅作本轮验证，不建立产品 Task、branch 或 worktree。工程来源 #599、缺陷来源 #588、功能来源 #577 均已关闭，只作明确历史身份的写作来源，没有重新实施旧功能、性能测试或业务恢复。

唯一外部对象为 [#619](https://github.com/castbox/guru-trellis/issues/619)，必要评论为 [局部完善输入](https://github.com/castbox/guru-trellis/issues/619#issuecomment-6248993513)。实际创建通过原 CreateIssue；评论、正文修改通过原 Clarify；每次修改都实际回读，并按原 `refresh_context` 返回重新审核。

| 场景 | 实际输入、行为与观察 |
| --- | --- |
| V1 简略输入 | 原 Discovery 调查可查事实，Clarify 实际写工程草稿并更新/刷新，随后 Wording `pass`、Readiness `ready`；原 CreateIssue 返回 `created`。回读完整标题及正文与已审内容加原 marker 一致。没有编造用户回答。 |
| V2 详细来源 | 实际读取 #588/#577 全文并整理详细历史样例。最终正文保留不可变树复用/变化重算/无跨进程缓存/摘要字节兼容与正式链路边界，以及归档路径、TaskId、generation、历史、无替代任务/空 Delivery 和依赖 owner 条件。它不宣称重跑旧验收。 |
| V3 评论整合 | 选定评论中的必要内容进入最终正文；装饰图标保持未采用建议，来源 CLOSED 保持历史事实。未将评论回读当正文完善。 |
| V4 正常遗漏 | 原入口支持的明确未完成追加稿将缺陷条件缩成“摘要可以复用”，功能条件缩成“能够续接”。原 Wording 审完整正文及来源后实际 `blocked`，指出条件、验收和证据边界遗漏。原 Clarify 补齐后真实写入/回读/刷新，fresh Wording `pass`、Readiness `ready`。未篡改已接受结果，也未宣称 Readiness 曾产生该负向 finding。 |
| V5 只读与完整正文 | 完整 postimage 的只读审核没有形式重写；审核前后 title/body/updatedAt 一致。恢复后的同一只读请求也没有写正文。 |
| V6 两条路径 | 创建草稿与已有正文修订都实际消费同一两规范。逐项比较：写前完整加载、语言缺失暂停/恢复、四原职责及回读/刷新、只读不写和不建 Task 的条件保持；新增历史样例不替代工程基线。两条写入均有真实回读。初稿漏写共同内容不可读恢复句属于 V4/V7 后续发现与补齐，首轮 `ready` 不被描述为永无遗漏。 |
| V7 局部与完整审核 | 请求只追加历史样例，但原审核检查完整正文，另发现范围外既有遗漏：核心段只写语言规范缺失，没写共同内容不可读的恢复。原审核先说明影响并保留阻塞；最终选定修订范围包括必要恢复句、两个样例及对应验收，未静默扩写无关段落。修后完整 postimage 重审，旧有效要求保持。 |

真实正文修改回读与精确 payload 逐字相同，更新时间为 `2026-10-18T10:59:11Z`；随后 fresh Sync/Discovery/Clarify、完整 Wording 和十维 Readiness 依次取得原正式输出。语言检查限本轮文本与必要上下文，内容审核覆盖完整标题、正文及来源。实际过程已去敏整理进 revision 教学示例；示例本身不供应任何后续任务的通过结果。

AC9 暂缺观察使用同一只读请求：安装语言文件暂不可读时，实际读取 exit 1，Agent 仅报告具体缺失并暂停，没有用旧摘要生成结论。原文件恢复后完整重读，继续同一请求。中间最终示例 reapply 与恢复复核排期重叠，使共同正文短暂未就位；Agent 继续保留暂停，原安装完成后完整读取共同正文和来源规则，再复核完整 live 正文。该执行排期事实没有扩大为并发、故障矩阵或产品缺陷。两规范最终与 canonical 字节一致，语言文件权限保持，恢复后无新增审批或正文写入。

验证结束仅关闭 #619，live 回读为 `CLOSED / COMPLETED`，closedAt=`2026-10-18T11:07:36Z`。关闭前后标题、正文和评论不变，记录保留。#153 仍由本 Task 原 Completion/Closure 后续处理。

## T153-04 确定性验证

- `test_issue_content_distribution.py` 首轮通过，耗时 119.640 秒；实际 revision 示例更新后重跑通过，耗时 108.739 秒。测试调用真实 preset writer，覆盖完整 installed 及22个声明平台投影的受影响规范、示例、四入口/三个合同链接、Author 来源依赖、语言规范、重复应用、用户文件保留与零 sidecar。它证明分发和引用，不能证明22个平台的实际 Agent 行为。
- source package 检查通过：40 packages、124 commands。upstream ownership 检查通过，测试文件内存语法检查与 `git diff --check` 通过。
- 首次测试因执行者传入不存在的 Fork scripts 路径，在 fixture 先决检查处停止。改为匹配 CLI 的 `dist/templates/trellis/scripts` 后通过；没有通过修改产品代码掩盖该输入错误。

## T153-05 匹配目标安装

代表环境为本 Task 隔离 checkout 的 Codex 安装，声明平台选择 Claude/Codex/Cursor。普通 `apply.sh --repo .` 被历史归档的 `upstream_delivery_migration_required` 前置阻止，不算成功。随后由原 `guru-upgrade-tools` local_candidate 完成 tools-only 安装，返回 `tools_upgraded`，installed extension=`0.7.0-guru.4`。

CLI/Core 都为 `0.7.0-castbox.4`，使用当前 Fork 构建的干净临时副本与正常依赖布局，未修改上游或全局包。最初直接使用含 Python 缓存的构建目录时，维护传输摘要与公开 SDK 候选摘要不一致，预检停止；干净副本消除该输入差额后才安装。未将此诊断扩张为本 Issue 的 runtime 修改。

初次安装、同候选 reapply 及实际 revision 示例的最终同步均由原 tools-only owner 完成。最终安装前后2,585个 Task/session 文件、309个 peer 指针内容保持不变，配置冲突选择保留。最终 source/installed package 检查通过（40 packages、124 commands、零 conflict/sidecar），dogfood drift 检查确认 workflow、所选平台与 spec 匹配 canonical。目标自己的 Python resolver 可执行，原生 `get_context.py --mode continuation` 成功返回当前调用方续接合同。规范、示例和四入口已由完整安装更新，未手补生成副本。

分发测试与代表目标均已实际执行重复应用。T153-02/03 记录代表目标的实际行为、最终完整性审核与真实 GitHub 写入；不以安装成功代替这些证据。`formal_fork_source_lock` 未验证；本地候选成功不代表正式远程 source-locked 采用。

## 未验证边界

未执行其他平台的实际 Agent 行为、完整多平台升级/Release 矩阵、正式软件发布或业务仓采用。当前变更不改变 installer 布局与算法，未额外增加 clean throwaway；定向分发 fixture 与代表现有目标分别提供其实际层级证据。这些结果不单独建立 Task Completion；最终 Check、独立完整 Review、交付及收尾各由原 owner 依据当前事实判断。
