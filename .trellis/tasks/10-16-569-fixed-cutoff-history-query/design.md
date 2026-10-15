# #569：原历史查询 owner 的固定截点设计

本文件定义方案；不授予实现、验收、Completion、Closure 或 Finish 结论。Architecture 采用当前独立 candidate_assessment 的 target_native 路径。需求见 prd.md；本文件单写来源承诺的设计处置。

## D569-01 原 owner 与调用边界

唯一数据准备/扫描 owner 仍为 guru-merge-task-delivery 的 discover-task-deliveries；query1 输入1.0保持 task_identity/repo_ref/base_ref，query2输入2.0保持同字段及task_ref。query1继续只认合法schema1/2 trailers；query2继续读既有public Task2事实并与trailers融合。原Merge delivered输出及原Task/Delivery模型不变。不新建同步Skill、typed exit、缓存、ledger或交付事实。

脚本执行确定性 Git/GitHub I/O、完整性与身份验证；实际 caller AI 依据公开截点和当前所需证据判断能否消费、是否需要另一次查询。Completion保有全部Task scope与真实Delivery/证据判断，history不是每次Completion的新强制前置。只有现有caller实际需要历史时调用原查询入口。

## D569-02 截点取得与有界 Git 准备

一次discover先验证认证和所选repo，再经repo-bound gh读取指定base的真实commit B1。repository/base响应必须完整，repo身份和完整commit SHA符合当前合同。B1一经取得即作为本操作cutoff，不再为远端B2重读base、重新扫描或追赶。

先尝试使用caller已有Git数据。以B1为起点读取完整first-parent链，检查命令失败及可达shallow边界，并检查随后实际校验所需的merge/head/candidate对象。只有完整到真实root且所需对象可读时直接复用；不能将shallow早停、missing parent或缺blob当成完整成功。缺少必要对象时原owner在调用内建立temporary bare Git context，从所选repo取得固定B1的完整历史；不依赖caller origin ref已存在或与远端SHA一致。

获取使用无destination ref的immutable SHA refspec，明确设置--no-write-fetch-head、--no-tags、--no-recurse-submodules、--no-auto-maintenance。空scratch不继承caller浅边界或移动refs；不使用深度、partial fallback或固定commit数量截断。该Git命令传输B1的祖先闭包，作为本次完整历史的数据准备，不扫描/获取无关refs。本地数据足够时不进行该获取。若后续选定public fact需要B1之外的实际merge/head对象，只为该有限事实集合有界取得对应immutable SHA；每个必要对象目标最多准备一次，失败不循环。

scratch只存在于该查询生命周期。扫描、commit parents/message、candidate trees/blobs均使用实际Git context；GitHub读取和public Task读取仍使用原caller repo。现有manual_recovery.commit_candidate的公共API调用与临时文件快照保持，内部显式接受history所选Git context，原manual recovery调用保持自身原context。不得取完对象却隐含回caller Git校验。

## D569-03 完整性与实际写入

只读含义是“不写业务/Task/Delivery/交付事实”。必要准备真实写入调用内scratch的Git初始化metadata、config、objects/pack；candidate验证沿既有能力写temporary file snapshot。两类scratch均由其原owner在成功和失败离开时清理，不成为可恢复authority或长期证据。

不写caller/其他worktree的HEAD、index、工作文件、Task/Delivery文件、shared refs/objects/shallow、FETCH_HEAD、tags或远端资源；不更新checkout，不merge/rebase、不生成同步commit、不进入Reconcile或业务gate。commands.json将查询准确声明为git_write，并在描述中限定temporary Git数据；该声明不授权caller分支/远端写入。Skill/contract/README与测试采用相同定义。

完整性失败包括：固定cutoff不是可读真实commit；first-parent链有缺对象或shallow截断且准备后仍不完整；匹配merge缺真实两父或parent2与reviewed head不一致；必要candidate对象不可读。fetch失败返回原Git失败分类及history准备field，明确重试本查询的恢复条件，不要求用户先fetch，也不返回discovered/空列表。保留网络/权限/provider、仓库/PR/Delivery身份不一致的现有具体错误，不降级成功。

## D569-04 query1/query2 事实归属与截点外记录

固定B1 first-parent merge序列按原顺序扫描，合法schema1/2 trailer解析、Task identity、exact真实merged PR、repo/base、merge SHA、两父、parent2/reviewed head校验和head/PR/merge去重保持。无trailers且无适用public fact的bookkeeping排除。

query2只读公开Task2 record，核对TaskId、各DeliveryKey、pull_request实际fact、repo/base及immutable candidate。扫描内public fact与trailer必须一致，再融合一次；不得以公开record存在代替PR/父提交/candidate核验，也不得制造Delivery补扫描。

对匹配repo/base但不在B1序列中的public recorded merge M：
1. 原owner验证该fact对应的真实PR/merge/head/two parents/candidate；当M的必要immutable对象不在当前Git context时，有界取得这些对象。
2. 若完整M first-parent链包含B1且M不是B1，则该fact是同base的真实截点后后继，本次不收入deliveries，也不把B1判为遗漏。
3. 若M本应在B1历史内却未扫描到、M与B1不具上述后继关系、必要身份不符或事实无法核验，则具体失败；不按记录时间、当前Task phase、latest base或某个hash猜测并静默省略。

后继校验不是追赶：不更换cutoff、不把M当新扫描root收集其它Delivery；它只验证已读public记录是否属于本次应覆盖集合。真实同Task后继事实的出现不改变B1结果含义；下一动作仍由原consumer决定。

## D569-05 最小 public result 与直接迁移

当前输出统一选用delivery-history-result-3.0：schema_version=3.0、status=discovered、task_identity、repo_ref、base_ref、cutoff_commit、deliveries。cutoff_commit为完整B1 SHA；deliveries沿原行结构保留可用DeliveryKey及真实PR/head/merge/base。成功空数组仅表示已完整扫描B1而没有匹配事实。没有新增时间戳、review历史、写入报告、excluded ledger、checkpoint或授权字段。

直接consumer字段用途：repo_ref/base_ref/task_identity与caller明确query选择核对；query2的task_ref由原public input context定位并由TaskId核对；cutoff_commit确定本结果覆盖边界；deliveries提供截点内真实事实。独立/恢复caller没有邻近Merge stdout也能识别该结果。consumer不读取producer私有数据。

MIGRATION-569.md明确同一组合切换Merge package、schema/interface/commands、Completion正文及声明平台投影；输入query1/query2及其历史语义不改，当前输出直接演进到3.0。旧1.0/2.0 result schema仅保留为已有历史验证资产，不再作为当前输出选择或运行时fallback；受控消费者同步迁移，不增加双读适配或无人消费版本。工具安装/旧Task采用仍由其原owner负责，本项不操作#566资源。

输出丢失时，原producer用明确query身份正常再查询；该新操作从自己的远端观察取得并返回明确cutoff，不能承诺复原未被consumer取得的旧B1。已持有B1公开result的consumer保留其真实事实；恢复既不从私有state推导B1，也不把新结果冒充旧截点。

## D569-06 consumer 与真实验证

原Completion、独立及恢复owner读取公开result，按repo/base/task/cutoff判断适用性。B2只有其它Task/bookkeeping前进时直接消费B1，不自动重查、不整合或重签旧业务gate。明确同Task新增Delivery或required evidence变化时由原owner另作有界查询，补缺少事实并重判受影响结论；不能以B1宣称当前整体齐全，也不重跑已交付业务gate。

验证分层：真实local Git的unit/组件覆盖精确cutoff、缺对象、shallow、public fact、真实错误和隔离；matching installed公共wrapper链保留每个producer实际stdout并薄投影；实际AI consumer亲自读公开结果并执行原Completion判断。外部provider fixture与真实GitHub事实分列，不用fixture预写pass冒充AI语义。原Merge delivered、query返回、Completion判定分别观察。fixed-cutoff consumer与结果丢失恢复必须在正式公开调用链中执行，单独schema/unit不够。

## 来源承诺唯一处置

| 精确来源 | 原承诺 | 处置、落点、理由与影响 |
| --- | --- | --- |
| #569 行为1/6 | 同repo/base/commit准备扫描及完整归属 | retain；D569-02/04。固定B1和真实PR/parents/head/trailers，不删除完整性。 |
| #569 行为2/3 | 原owner自动有界准备、不推进shared ref | retain；D569-01/02。scratch隔离，无新同步Skill/状态库。 |
| #569 行为4/5 | 业务事实只读、实际Git写入准确、无checkout整合 | retain；D569-03。temporary metadata明确且caller Git数据不写。 |
| #569 行为7 | B1完成不追B2、最小public身份和截点 | retain；D569-02/05/06。schema3.0仅加必要cutoff。 |
| #569 行为8 | 获取/完整性/身份失败不可冒充空成功 | retain；D569-03/04。错误分层且不循环。 |
| #569 行为9 | query1历史语义、query2归属去重及后继区分 | retain；D569-04/05。只排除已核验真实后继。 |
| #569 行为10 | 复用publicI/O、明确兼容迁移、无新ledger | retain；D569-05。matching受控切换，无新双读。 |
| #569 行为11 | AI判断适用性、脚本事实、有界补取、合法空 | retain；D569-01/03/06。查询不授予后续gate。 |
| #569 验收1..7 | installed实际接续、恢复、cutoff消费、隔离和投影 | retain；D569-06及implement.md验证计划；只按实际观察层声明。 |
| #569 关联与范围边界 | #566/#567独立、#557保留、无其它资源/矩阵扩张 | retain；D569-01/05/06及prd.md。无来源范围修订。 |

来源没有另指定规范性DTO或算法；以上编号行为本身仍是规范性约束，不作为advisory丢弃。无需修改Issue正文或请求产品scope选择。

## Architecture 落点

任务隔离贡献：architecture-contribution.md。沿用ADR-026/028与既有owner，新增数据准备及结果边界为target_native；不改变owner、single-writer、GAP lifecycle或原则例外。当前无需单独ADR候选；final_plan独立owner仍核对这一适用性。shared Architecture/RDT只有在首次独立完整committed Review后才由原owner按expected-current晋升，晋升新差额重新经过Check/commit/完整独立Review。
