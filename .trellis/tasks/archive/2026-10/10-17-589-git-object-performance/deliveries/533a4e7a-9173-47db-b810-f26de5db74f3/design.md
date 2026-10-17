# D7 公开不可变摘要消费设计

## 固定范围与来源

内容基线 B=865f4a9576eabc85cb3b91e74ecd856785095510，来自实际上一 Delivery D6 head；开发基线3676b9e已含#588，PR target main独立，不默认追赶main。D7仅来源/consumer准备，整体责任与D1–D6事实见根PRD。本设计是本批唯一source-design disposition matrix。

| 具体来源与原承诺 | 处置 | 实际落点、理由及上游处理 |
| --- | --- | --- |
| #589§5–8：消除重复读取/hash，保留每份输入检查、摘要和恢复 | retain | manual_recovery/HistoryContext只替换内容取得；Task/Delivery/PR/祖先/expected/cutoff检查仍在原caller。以实际读取/计算去重及必要独立校验完整性验收；耗时如实观测，不以预设改善数字驱动额外改造。 |
| Fork9f40ec7 public-adoption：GitCandidateContent实际root+完整commit+paths，操作内复用，no_lazy_fetch | retain | standalone recovery拥有context并关闭；history一次discover共享、在prepare/retry内调用；切换隔离bare root前关闭重建。仅public接口，无private observation或复制hash。 |
| 原CandidateObjects：物化临时snapshot再调用filesystem candidate_content_ref | change | 移除两个生产caller及无consumer的helper/专属tests；公开GitCandidateContent直接取得摘要。仍有其他consumer的git_object_batch保留。可变candidate_content_ref及通用projection.candidate不改。 |
| source_locked tools完整来源、原Task/session/peer保留和安装receipt | retain | 固定9f40/treeed56/ordered parents0e3b、5366/mainCI39013710371、CLI/Core.4、pnpm10.32.1；source构建与配对包bytes/mode独立核对。最终两目标由后继clean committed source原tools owner安装，不手写receipt、不patch上游。 |
| current目标版本及完整安装/升级入口 | change | source lock、extension manifest、ownership/schema/validator、delivery_installation能力诊断和upgrade-installation current目标断言同步.4；检测公开class。保留Guru版本.4、Plan2/迁移算法、旧来源支持与历史fixtures，不全局替换.3。 |
| #589§6当前读取工作验收与上游PR50 | retain | 上游与下游既有FAIL、旧门槛及其未通过结果原样保留为历史观测。当前直接来源§6以消除不必要读取/hash、资源有界及逐input检查为验收，不再要求预设耗时改善百分比。D1–D6交付与工程结果仍为历史事实。 |
| #575完整Release/多平台矩阵 | retain boundary | 本批source/代表candidate定向验证；后继正式两目标采用。无正式Guru发布或业务仓采用，不承接#575矩阵。 |

## 数据与资源生命周期

manual commit_candidate接受操作内公开content context；无外部context时创建并在返回/异常退出时关闭。每次通过projection._call(content.content_ref, exact_head, paths)转换原上游错误，返回原candidate字段及actual head/content_ref。禁止先snapshot/read再调用新API。

HistoryContext持有当前actual root的公开context；candidate摘要计算放入prepare(head, reader)内。原缺对象准备可切换root，必须先关闭旧context再清空；重试用新root重建。一次query中的相同blob/hash可复用，各候选仍执行自己的完整业务检查。退出关闭context和临时bare。路径、mode、删除、gitlink、排序/编码摘要规则完全由上游拥有。

新公开context批次上限4096，首批含commit控制，至多4095内容；不同于原Task/local_commit128，不能混算。批量文件传输和流式处理由上游提供；Guru不新增缓存store/进程/算法。对象准备仍由原History owner执行，不隐式移动caller的ref/common-dir。

## 测量与验证设计

先完善现有benchmark observer：按实际argv/root识别batch、batch-check和batch-command；info与-e不计内容，contents才计body，flush只计控制。保留每样本命令/退出码、路径、unique blob、请求数/字节和最大blob。旧snapshot→filesystem hash与新hash分别做独立观察pass，不混入plain timing；profile按精确代码位置拆分，避免嵌套cumulative重复相加。

路径规模128与10000 assets（真实candidate另含app及16MiB blob），重复/unique各一组；manual固定Delivery数量。query2在相同候选规模下单独改变Delivery1/4，不把两个增长因素混成一组。source完整公开fixture链和代表installed-template链均明确wrapper、状态与依赖。每cell两次fresh invocation，每次repeats1；首次record和恢复分列，不混median。GitHub fixture网络为零，真实provider网络不算本地收益。plain时间、Git volume、RSS、hash/profile独立pass；BSD time最大RSS是所声明wrapper后代单进程最大值，Git独立记录，均非同时进程组总和。数值矩阵可限定local-complete，scratch获取单独正确性验证且size按actual root。

本Delivery performance-contract记录原始样本、工具/input身份、缓存/预热、汇总方法和资源测量范围。旧数值合同及全部样本保留为历史；当前验收按同调用唯一blob读取/hash、无snapshot重复读取、必要独立检查和资源有界判断。耗时/profile/RSS仍完整报告，不挑样或将旧指标FAIL改称PASS。source与installed-template前后common/receipt分别匹配，candidate fixture不冒称最终目标安装。测试覆盖摘要等价、特殊路径/mode/删除/gitlink、missing/error、准备切root/关闭、相邻操作刷新、恢复/stdout丢失和多Delivery。正式安装/native及最终链由后继负责。

## 兼容、文档与回滚

唯一长期来源为canonical，定向更新current三份README及项目public-docs、版本断言和API能力诊断；历史文档/fixture保留。受管副本只通过原installer投影；旧archive导致普通apply阻塞时不能迁移历史来过关。本批可用source fixture/代表candidate安装证明clean source准备，最终完整投影由后继工具维护消费。

任务贡献位于本planning_root/architecture-contribution.md，遵从ADR-024/027、ARCH-FND-001/002和current.94。无新架构决策，无新ADR。完整committed独立Review后由原Architecture owner按live expected-current晋升，新增diff重新Check/commit/完整Review后才能Publication。失败回原Check/Planning；回滚采用完整匹配旧source/pair及原维护owner，不混装.3/.4，不修改历史已交付事实。
