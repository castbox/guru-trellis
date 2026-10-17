# #589 最终采用批次的全步骤盘点

本清单承接D3、D4、D7原workflow-inventory的入口、caller、增长因素和工程计数。D1–D7（PR593–598、604）均已合并。D8只完成正式采用与实际受影响链，不新增性能算法，不以预设耗时百分比判断完成。

## 优化与保留

| 步骤/增长因素 | 已消除的不必要工作 | 必须保留的读取、consumer及证据 |
| --- | --- | --- |
| Intake/创建；历史Task、分支数 | D3批量Task/branch/checkout事实；上游#47正常创建批量读取，D5/6来源采用 | source、mutable refs、重复身份和归属独立判断。原Intake未挂Trace，精确历史计数不可追溯；不重做Intake。D3创建原25项为24通过、1失败，该exact失败项独立重验通过，不称原组合全绿。 |
| Planning/Activation；规划与拓扑规模 | 调用内不可变身份按原owner复用 | 当前规划、可变工作区和session独立读取。D3历史native计数及D8真实Author/Wording/Architecture/Approval/Activation保留，不将旧绝对计数称当前after。 |
| Implementation/Check/Commit；候选规模 | D3调用内Git元数据复用 | index/worktree/HEAD、候选、parent/tree与恢复结果各有consumer；当前Check/Commit必须实际发生。 |
| 完整Review/实际整合bounded；路径/唯一blob | D2按OID去重和流式摘要；同调用相同树/规则摘要复用 | 完整B..H与bounded语义分开；D3冲突resolved→当前Check→完整Review、独立无冲突整合链仍适用。D8未改这些runtime字节。 |
| Delivery Review/Publish/Merge；PR/候选规模 | D1逐路径Git进程已移除；D7旧CandidateObjects物化退出，直接消费公开GitCandidateContent | exact candidate/PR/target/CI、事务与恢复归属保留；D8新PR发布和手动merge后首次recovery不能提前记通过。 |
| manual recovery/query2；路径及Delivery分别增长 | D7 snapshot候选文件读取为0，内容hash按操作内唯一blob；相同endpoint prepare与已重建head重复-e消除 | 每份输入结构/身份/关系/ancestor/expected/cutoff和actual root独立检查；历史遍历按真实H增长。41consumer与16cell对照见D7，不重复认领before已去重body收益。D8在实际新PR上验证。 |
| Completion/Closure/Finish；全部Delivery历史 | 继承批量历史内容读取及调用内复用 | 每个Delivery、source、Publication、commit/PR、first-parent和cutoff保留。当前589收尾尚未发生，原terminal fixtures只证明对应层，不预填成功或零。 |
| Cleanup；资源数量 | D4同head immutable reader复用 | 原10/100资源preview/delete/recovery及逐资源live检查保留。当前Task适用Cleanup由原owner执行，不删除peer资源。 |
| Tools采用；安装文件及peer位置数 | 原公共owner固定读集和同operation恢复 | D8两目标source_locked、目标native、receipt/平台/mode/drift/sidecar/保留见validation.md。真实Git计数已逐操作列出，含peer解析rev-parse；不将工具采用窗口称性能收益。 |

## 全部验收映射

| AC | 当前事实及剩余 |
| --- | --- |
| AC01/02 | 上表与原D3/4/7完整盘点形成优化/保留清单；原Intake不可追溯计数明确保留。当前收尾发生后由最终Completion消费。 |
| AC03 | D1批量读取已交付；D7公开candidate适配已交付。D8新PR实际manual/query2待后merge。 |
| AC04 | D2原对照及D3正式bounded链；源码相同，适用承接。 |
| AC05 | D3生命周期和上游task_store优化已正式采用；D8未改其生产字节。 |
| AC06/07 | D7 16cell/32plain/64资源观察missing0/errors0；旧snapshot读0，唯一blob hash，流式及actual-root/call-local边界，41consumer通过。10000路径4Delivery hash40008→69，snapshot230948905bytes→0。 |
| AC08/09 | 原可比较before/after、两档路径/Delivery/Task增长、大对象与unique/repeated输入保持；旧数字FAIL/SKIP不改写。耗时/RSS如实报告，一组RSS增加3440640bytes，不作为预设数字阻塞。 |
| AC10 | D7全部Git/请求体/唯一blob/读取/hash/RSS分层观测；D8工具Trace2实际计数见validation，不冒称完整wall/RSS。后merge真实provider/本地/全链按真实采集报告，不能以fixture网络零代替。 |
| AC11/12 | D1–D7语义/正式链及合法缺失/删除/mode/gitlink/错误/刷新测试适用。D8待真实新PR手动merge、首次recovery、同结果恢复、固定cutoff query2；每输入检查和公开摘要字节不变。 |
| AC13 | Task与代表正式安装完成，声明平台、0755、受管字节/native/drift、零sidecar；相同生产字节reapply承接D7。无事前完整common session快照，独立快照与原write-set/native证据分层。 |
| AC14 | 各Delivery原工程证据与当前采用来源明确；本批尚需交付/实际后merge与整体完成，不以切片合并替代。 |
| AC15 | Fork9f40精确公开API已存在且正式采用；未patch上游、复制hash算法、导入private observation或用inode作authority。 |

## 证据适用与未执行边界

D2 runtime相对原c422、D3生命周期/create相对dc57、D4 Cleanup相对875没有生产差额。Fork c7→9f的task_store/core task/v2无差额，只公开delivery_store/git_objects能力变化。D1旧snapshotafter已被D7替换，不能当当前after。D6旧c7安装不冒充D8当前采用。D7writing原组合含一次环境ERROR，后单项1/77.251s通过；不改原组合退出码。

D8 Guru来源H1cee，Fork9f40ec70914f98fce2619560274cc1d0619f2f7e，CLI/Core0.7.0-castbox.4；实际目标结果见validation.md。Architecture.96、RDT.104适用；D8不产生新架构责任。#575完整Release矩阵、npm/Guru正式发布和业务仓采用均未执行，保留原owner。
