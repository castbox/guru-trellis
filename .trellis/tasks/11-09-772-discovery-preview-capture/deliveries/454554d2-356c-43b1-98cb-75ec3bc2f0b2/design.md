# Discovery 大预览捕获与恢复：D1 设计

## 1. 设计目标、需求承接与内容基线

覆盖本批PRD全部R1–R6、S1–S4、AC1–AC3。固定开发B为main@fd52fbd69a8161d037bf6d4548b04b7247b60c03，来源为Intake明确选择；Planning H0同B，最终实现H按实际commit观察，PR目标main。内容范围由完整B..H及当前dirty增量构成，不混入其它Task。

独立Architecture原owner已正式返回candidate_assessment的baseline_current/no_architecture_impact，基线guru-trellis-architecture、constitution guru-trellis-design-constitution-v1，freshness为sha256:ea61b3f4c1bb165a92f8115f6c644300d4e73111de41fb9b40ebf5ce8c782552。该结果只允许方案写作，不能替代后续final_plan。

## 2. 当前系统、边界与目标差额

无前序Delivery。原Skill主入口加载contract，contract正向步骤只说运行一次preview，再AI选择与深读；完整stdout捕获提示在后段。runtime/common.py的preview固定返回最多20个候选及完整manifest，正常大结果超过工具展示预算。共享companion-scripts已有两层工具预算与截断补读规则。

差额只在原Discovery package：SKILL.md前置执行提示，references/contract.md正向步骤和历史读取规则，新examples/history-preview.md提供可执行示例。保留runtime、schemas、commands、interface、评分和所有原出口。若分发规则要求显式例子登记，仅按现有package资源机制声明，不新增API或wrapper。共享规范只引用现行预算合同，不复制或改造其规则。

## 3. 来源设计处置（唯一）

| 来源／承诺 | 处置与落点 | 原因、影响及上游处理 |
| --- | --- | --- |
| Issue #772 行为1：完整捕获后解析receipt.result，数据与展示分开 | retain；第4、6节及示例 | 捕获完整事实，避免解析截断文本；无偏离 |
| 行为2：保留ID、路径、命中和内容，全部候选由AI判断 | retain；第4、5、8节 | 分批与字段补读不裁掉集合；无脚本语义选择 |
| 行为3：展示截断自动同基线同查询恢复 | retain；第6、7节 | 内存存在则复用，丢失则同范围重取；不启动新调查 |
| 行为4：区分shell与外层预算，真实失败原路处理 | retain；第5、6节 | 直接进程字节捕获避免shell返回裁剪；展示仍分批；失败不转pass |
| 行为5：原Gate、record/check/invoke与公开合同保持 | retain；第5–7节 | 不改任一consumer或公开DTO |
| 行为6：原安装owner同步，无新缓存或状态 | retain；第4、7节 | 原工具升级owner保留Task/session；无新增持久化 |

## 4. 模块、职责与设计取舍

SKILL主入口明确当前AI需要执行完整捕获→解析→紧凑分批→补读→原语义链，并链接单一示例。contract的Forward Behavior在现有顺序第8/9步展开捕获及判断，第History Preview节定位示例和恢复规则；删除后段重复的简略指引或改为准确引用。

示例面向持久Node REPL：使用node:child_process.spawn和argv数组执行现有shell wrapper，stdout/stderr以Buffer收集到close；检查真实exit code，成功后统一UTF-8解码并JSON.parse，显式取receipt.result。每次只展示容量足够的小批候选，信息包括candidate_id、finish_summary_path、matched_clues、problem/outcome的有界片段及长度/补读位置。按ID和字段范围读取完整缺失内容；所有候选必须经AI审查，代码不排序筛选或决定相关性。补读工具按原source reader读取AI选中证据。

完整结果、query和source-transition只留当前调用内存。直接捕获子进程stdout没有exec_command返回裁剪这层；若选shell工具载体，先保证其内部返回预算足够，外层编排仍只打印紧凑批次。仅增加外层max_output_tokens不能补回内部截断。

不选提高候选限制、裁剪返回集合、预览缓存或新自动评分器：它们改变行为或增加状态，不能解决模型取得完整事实的本次直接缺口。

## 5. 接口与数据

原pre_task/context_request输入→原公开preview（同query/source-transition）→receipt.result的candidates/manifest→AI选择和深读→原record/check/invoke→实际context_ready/refresh_base/blocked。候选的ID/path/matched_clues/index_projection保持原数据。内存展示函数只投影事实，分批不代表排除。

不新增公共输入、输出、schema字段、command或持久状态。record receipt.result替换owner_result、check receipt只供验证、invoke实际出口继续现行合同。示例不构造派生digest，不解析日志中缺失中段的JSON。

## 6. 状态、顺序、正常与失败流程

先完成当前态调查并固定原基线/query；运行preview一次并捕获完整双输出；退出码非0时保留原失败交原owner，不JSON.parse假结果。成功时解析完整receipt.result，按原顺序展示全部候选索引，AI逐项选择/排除，需要的长字段补读后作判断；选中1–3项按原reader深读，再完成Gate及record/check/invoke。

仅展示截断时当前owner缩小批次/字段范围，自动补齐缺失部分，继续同原调用。输出预算不是业务依赖，不能因截断结束首轮。没有新状态转换或自动语义选择器。

## 7. 恢复、兼容、迁移与集成

完整结果仍在REPL时不重跑preview，仅分批取回。结果丢失时同固定commit/query/source-transition恢复重取，保留恢复性质；不是重新广搜，不将新基线偷偷换入。真实stale/mismatch或来源缺失继续原owner的现行重入/失败出口，恢复不放宽freshness。

这是现行说明的直接补全，无API/schema/数据迁移，无第二执行路径。原guru-upgrade-tools从完整匹配源同步本Task checkout的dogfood及声明平台，保留Task/session、用户内容和peer工具；处理其真实sidecars，再检查drift。若需干净source供安装，沿原TaskCommit早期Draft或其支持的local-candidate源路径，安装owner审查其实际source限制，不手工覆盖受管副本。

## 8. 验证设计

V1/AC1：原Check/Branch reviewer完整读入口、正向步骤和示例，逐项核R1–R6与S1–S4，核不变consumer。静态文本命中不能代替这项语义判断。

V2/AC2：在持久Node REPL执行公开示例；输入当前固定main的大归档真实preview，选定小展示预算。观察完整JSON解析、20项或实际返回数，全部ID一一可定位；分批实际输出不截断，长字段按offset补读得到全部内容。复用Issue两会话已有失败/恢复，不新增native行为评测；本层只证明数据捕获/展示与可执行性，不宣称生产Agent效果重验。

V3/AC3：运行原package source/installed验证、受影响文档/示例检查、声明Shared/Claude/Cursor/Codex投影一致及check-dogfood-overlay-drift.sh；按原owner执行tools同步。必要现有contract tests保留；不新增仅冻结句子的断言。原未变runtime小输出/空候选/错误/record链复用现有适用证据。

证据充分后停止追加实验。只有机制改变、实际检查失败或剩余具体疑问才补验；不跑普通Issue不拥有的完整安装矩阵。

## 9. Canonical 引用、本轮差额与实际未决项

本批PRD第7节给出行为/设计/测试定位；本设计直接补原Discovery合同执行路径。Architecture原评估无影响，不创建空contribution/ADR，不改共享架构导航。RDT的现行local-fix-intake和runtime-location保留既有当前AI、完整输出、固定tree及原owner职责；是否需共享RDT差额由原维护owner在Phase2实际审核，不用本设计代替晋升结果。无方案未决项。
