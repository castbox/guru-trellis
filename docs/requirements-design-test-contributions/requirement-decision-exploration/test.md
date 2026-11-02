# 需求探索与确认验证观察

观察截止：首个完整实施候选、共享 current 尚未晋升。B 为 a4feadd99683e006580ef16b078c44e3ad3648a7。策略见 [T-DEC/SC-DEC](proposed/docs/test/current/requirement-decisions.md)。本记录区分实际执行事实与 AI 对语义的判断，不循环记录自身最终通过。

## 原问题记录与驱动

实现 worker 以完整匹配 Fork `.6` source scripts 执行 Clarify `tests/test_contract.py`，21项通过。新增真实原 record/check 清单完整接受、逐项修正/部分回答和未答记录案例；原 schema 拒绝 partial 关闭问题。公共 schema 和 runtime 未修改。

既有 contract 描述 `open_questions = opened - closed` reducer，但当前 runtime 检查范围没有证明该 reducer 的 close-before-open/reopen 语义。此处仅报告原 wrapper 实际验证的形状、内容绑定及 partial 约束，不称机器已验证全部生命周期。本次没有新增 reducer；未答不默认及逐项语义由下面真实 Agent 行为另行观察。

对话采集器6项单元测试通过，证明后续回复及 review_focus 不提前进入 fixture、实际 thread_id 恢复、非零/缺完成事件/超时/身份不匹配停止后续输入，以及原诊断保存。这是双替身工具测试，不是模型效果证明。

## 实际 native 多轮方法试验

使用本机可用 Codex CLI 默认模型配置，不覆盖模型。临时 fixture 只提供从当前 canonical 提取的方法和合成仓库事实；后续合成用户答复仅在对应轮次提供。关闭 hooks/apps/memories、daemon及明确列出的无关 MCP。沿既有本机凭证机制运行，未读取或复制凭证。实际 events 证明模型先读取 methods 与 facts。

五个案例合计10轮均实际完成，所有轮次退出码0且有完成事件；这只证明执行结束。主会话与独立检查 Agent 另读实际对话判断以下行为：

| 案例 | 轮数 | 实际语义观察及限制 |
| --- | --- | --- |
| lightweight-partial-correction | 3 | 提出独立Q1/Q2推荐清单；用户只修正文案时保留键盘未决；最终采用“没有找到”和清空收起键盘，不重复问这两项。模型另外提出的显示条件/列表恢复等配套行为未被用户接受，诚实保留待确认，因此不能称全部需求已收敛。 |
| clear-repository-facts | 1 | 自查已提供事实，保留dist、已有目录错误和原parser，只提出help展示最小方案，无制造提问。未修改或测试真实业务代码。 |
| material-cache-choice | 2 | 解释缓存速度/新鲜度取舍并等待；用户拒绝旧数据后不再采用缓存先展示，明确不能消除已知网络等待。新增加载/空态/失败重试仍是方案草稿，不计为已确认要求或已实施。 |
| ui-preservation-new-ambiguity | 2 | 保留旧失败消息/重试，不因新稿漏画删除；询问本机/云端清理范围。用户选择本机后继续询问重新登录展示的新歧义，未重问重试，且区分未知实际同步事实和产品选择。 |
| unanswered-is-not-acceptance | 2 | 用户未决定时两项均保持未决；继续调查后如实报告没有页面源码，索取材料，不把“先继续看看”作为接受或开始实施。 |

本次实际输出保存在本机临时采集目录 `guru-decision-native-jfZW7E`，各案例含真实prompt/events/stderr/execution。持久记录只保留必要观察，不复制原始对话或凭证。本项是 question_method_only：不证明 Guru 自动入口、完整正式 owner调用或生命周期、多平台效果，也没有旧/新受控A/B，因此不宣称相较旧版提升比例。

独立检查将15份实际方法快照与最终canonical比较：14份字节一致；轻度清单案例的Interaction Budget首句仍是先前“missing intent”，最终改为“unresolved requirement intent”。新增的轻度确认、清单、部分回答与实现自主规则一致；该等义收窄未改变本例受测分支，保留当前观察的适用性，但不称全部快照字节相同。

## 安装与工程观察

普通 `apply.sh --repo . --json` 实际被旧归档触发的 `upstream_delivery_migration_required` 拒绝，未转换历史Task，也未把失败算通过。使用原 `guru-upgrade-tools` 的 local_candidate tools-only入口同步本独立工作区；匹配Fork源码来自固定source-lock commit 17015f987166f4106034f115d23212446f16d536的完整临时归档并构建CLI/Core `.6`。未修改已有Fork仓库或全局CLI。

实际preview无未知Guru local edit；public tools计划所有源/目标相同，保留用户config及AGENTS，仅原Guru资产按当前canonical安装。原public invoke实际返回tools_upgraded、version0.7.0-guru.7，unverified保留formal_fork_source_lock；这是development candidate证据，不是正式发布锁定验证。

本工作区实际 installed runtime验证在原维护入口完成；随后dogfood drift检查通过，Shared/Claude/Codex/Cursor、workflow和spec副本与canonical一致；受管根递归.new/.bak为零。共享main和业务项目没有修改。原上下文validate在指定实际Delivery后通过，规范超注入上限warning保留，各执行Agent须补读完整内容。

定向分发测试实际完成首次安装、声明平台投影的新增方法/教学资产核对、同fixture重复apply、用户文件保留及零sidecar检查，1项通过，196.019秒。首次运行在重复apply时installed validation返回2，未获完整诊断；运行期间源码有变化，可能引发sidecar，但不将该推测当成已证实根因。冻结方法后定向重跑通过；测试说明的非语义标签修订仍须最终同步核对。

独立检查已审五例实际对话，没有发现漏问、把未答当接受或替用户实现的当前缺陷；指出新RDT策略中对原reducer验证的表述过强，已将本项证据收窄到显式记录与partial schema约束，不新增runtime修复。当前共享RDT仍是隔离完整proposed，不是已经晋升；后续由原candidate Check/final integration/实际候选重绑与最终质量链承接。

独立检查实际重跑driver6项、Clarify21项均通过；内存语法370文件、案例与index JSON、canonical Bash和diff检查通过。首次PATH Python缺jsonschema，首次managed测试缺匹配Fork环境，均是具体执行依赖错误；按声明完整环境重跑通过，不修改测试来掩盖失败。source package validator通过（41 active packages、127 commands）；其发现的141个package test只是inventory，不是执行计数。修订上述新文档的证据措辞及eval测试用途标签后，独立检查未发现剩余可操作的本范围缺陷。
