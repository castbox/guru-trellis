# #589 整体交付与当前证据

## 已交付范围

D1–D8均已实际合入main：PR593–598、604、606。最终开发候选c4e63b708d7915d9e05d2013f8859a2167263147，D8实际merge1c6b68133d29c442ccb1ded2e87b1c9d78b21358。D8完整Check、clean TaskCommit、独立完整B1cee..Hc4e Review与十维DeliveryReview实际通过。GitHub PR606 checks/reviews为空，不声称CI通过。

D1/D7消除manual/history逐路径Git进程及snapshot重复读取/hash；D2消除实际整合bounded的重复body/摘要与整批内存；D3优化Task/branch/checkout解析；D4优化同head Cleanup读取；D5/6及D7/8按原owner正式采用匹配上游。每份输入独立检查、原摘要字节、恢复、错误、mode/删除/gitlink及call-local/actual-root边界保持。

## 当前采用与性能

原Task和代表installed由原source_locked tools实际采用Guru来源H1cee、Fork9f40ec70914f98fce2619560274cc1d0619f2f7e、CLI/Core0.7.0-castbox.4。H1cee到最终Hc4e的canonical trellis无生产差额。两目标native、installed validator、受管bytes/0755、声明平台/workflow/drift/零sidecar、同operation恢复通过；Task/archive/workspace/config独立前后比较一致，原peer/common checks保持。未事前完整快照common session，不声称该层独立全量byte-diff。详细工程事实见D8 validation.md。

D7当前生产适配16cell、before/after各32次fresh plain、after64份独立资源观察，missing0/errors0。原输入保持一致；旧snapshot候选文件读取全为0，内容hash按操作内唯一blob。10000路径4Delivery重复内容样本hash40008→69，snapshot230948905bytes→0；before原已去重Git body，不重复认领。耗时/RSS如实保留，旧百分比FAIL/SKIP不改写。一组RSS增加3440640bytes，资源有界；不以预设性能数字追加改造。原performance-results是样本唯一工程owner。

## 实际后merge公开链

PR606普通两父manual merge实际成功，parents为9a10cb54c4a7eb8016d52b9bd5c3c2ec7de31807与Hc4e。原Publication唯一，调用前Delivery fact为空；未先走正常Merge记录再短路。主owner独立审查完整21路径，包含candidate.paths外的manifest、Task与规划；实际head等于已完整审查候选，authority不变。

首次原delivery_merged_recovery实际返回delivered，使用新公开candidate_content_ref记录historical_success；同入口原结果恢复返回完全相同DTO，没有第二次merge或制造Delivery。真实query2返回result3.0/discovered，固定cutoff1c6b68133d29c442ccb1ded2e87b1c9d78b21358；准确8份Delivery，PR593–598/604/606，key/head/merge归属无遗漏、无重复。该查询为只读业务事实，成功不单独证明整体完成。

| 实际操作 | 总wall秒 | gh/provider边界秒 | Git fetch边界秒 | 其余本地自动化秒 | 全Git | cat-file/show/ls-tree |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 手动merge | 3.583 | 3.530 | 0 | 0.053 | 0 | 0/0/0 |
| 首次manual recovery | 8.430 | 5.881 | 1.512 | 1.037 | 22 | 2/0/0 |
| 同结果恢复 | 5.369 | 4.679 | 0 | 0.690 | 6 | 2/0/0 |
| query2 | 13.922 | 8.849 | 0 | 5.073 | 320 | 1/309/0 |

gh/provider时间含CLI本地开销和provider等待，fetch时间含Git准备/传输开销，均不是纯网络RTT。其余时间是总wall减上述不重叠窗口，包含包装器/客观校验和观察开销。所有操作均rc0。query2的309次show为first-parent历史提交消息%B遍历，按历史增长，非逐候选路径读取；首次recovery缺失merge对象由原owner自身fetch，不由caller补对象。此live观察没有重新采集内容字节/hash/RSS或读取与其他校验CPU拆分；相同production bytes的对应细分由D7原独立observer/profile给出，不把Trace2推测成完整volume证据。本机原始命令输出、Trace2与无敏感参数的provider计时在/tmp/guru-589-d8/live-chain/。

## 全部accepted scope与边界

AC01/02由D3/4/7完整入口库存和D8 workflow-inventory承接，逐项区分优化/必要保留；原Intake当时未挂Trace，计数不可追溯，明确边界而非通过，不新建Task补数。AC03/06/07由D7实际源码、16cell操作量、41consumer与当前真实manual/query2共同证明。AC04由D2对照和D3正式无冲突bounded链，AC05由D3生命周期与上游公开采用证明；当前runtime依赖差额已核对无影响。AC08–10保留全部可比较多规模前后、真实资源与profile以及当前provider/全链观察，不用数字硬门槛。

AC11/12由D1–D7原普通流程、PR后冲突resolved→当前Check→完整Review、无冲突实际整合、合法缺失/失败/刷新及本次手动/同结果恢复/真实query2承接。AC13由正式两目标及平台/mode/drift/sidecar和相同生产字节D7 reapply证明。AC14的候选/来源/实际交付/未验证边界见本文及原Delivery；AC15的上游前置已通过精确9f40公开能力与正式采用解决。不存在通过删除清单来隐藏的同范围残余。

旧D3创建组合24通过+1失败，其exact项独立重验通过；D7writing组合一次环境ERROR后单项通过。原失败日志不改称整套通过。f70测试来源不冒称实际main整树相同。RDT.104与Architecture.96继续适用，唯一Test记录各阶段截至提交的工程事实，当前后merge终态由本文和公开Task事实承接。

本报告供原整体Completion判断和最终归档消费；不提前声称Closure、Finish或Cleanup已执行。它们的真实结果分别由原公开Closure、Finish摘要/目标merge和Cleanup receipt证明。#575完整多平台Release矩阵、Guru/npm正式发布、业务仓采用与业务部署均未执行，不计入本普通Issue完成声明。
