# #589 D7 当前优化与保留清单

## 证据和责任边界

本表承接D3 workflow-inventory.md的完整入口/caller/增长因素和实际历史计数，以及D4同名清单。历史样本不改写成当前候选after。D1–D6合并事实分别为PR593–598；本批D7尚未交付。当前整体验收按live#589§6以不必要读取/计算消除为目标，不以旧耗时百分比判断完成。

## 优化项

| 入口与机制 | 当前处置与证据 | 剩余责任 |
| --- | --- | --- |
| manual recovery/history逐路径Git进程 | D1已消除逐路径进程。D7继续移除旧CandidateObjects snapshot/helper及无consumer专属tests，直接消费公开GitCandidateContent。 | D7完整gates/交付、后继正式目标采用与live受影响链。 |
| manual/history snapshot文件重复读取及hash | 本批16cell完整对照见performance-results.md。Git body原已去重，本批不重复认领；snapshot候选文件读从每cell17.3–230.9MB降至0，内容hash按操作内唯一blob计算。原逐输入候选/归属/ancestor/expected/cutoff检查保持。 | 同上，不能以source fixture替代最终目标采用。 |
| manual重复endpoint existence；query2已重建head再-e | 同一exactOID terminal endpoint仅prepare一次；query2只在同输入、同actual root已完整重建比较时省重复-e。未记录输入或root变化仍按原prepare。41项consumer回归及真实fixture原wrapper保留相应检查。 | D7source完整Review和后继正式链。 |
| 实际整合bounded continuity重复body/hash | D2/PR594已按OID去重、流式处理、调用内树摘要复用；D3独立无冲突整合公开链保持其consumer边界。D7未改该owner。 | 最终目标采用后核对适用性，不混入PR冲突后的完整Review或#588收益。 |
| Guru Task/branch/checkout/history读取 | D3/PR595已批量和调用内事实复用。official task_store正常创建及normal local_commit由上游#47和D5/D6正式来源采用承接；c7→9f当前生产差额不改task_store与默认128批路径。 | D7匹配来源及后继正式.4采用后核对原入口。 |
| Cleanup手动同head资源读取 | D4/PR596已复用immutable reader；原10/100资源preview/delete/recovery及逐资源live检查事实保留。D7未改其owner。 | 最终整体盘点按依赖承接，不伪称当前Task已Cleanup。 |

## 保留项与计数口径

| 全步骤入口 | 保留对象、consumer与实际证据 |
| --- | --- |
| Intake/Sync/Discovery | source、mutable refs、Task/branch/worktree归属仍由原owner确认。原Intake没有挂Trace，精确当时计数不可追溯；保留明确unverified boundary，不重做Intake或造第二Task补数。后续真实生命周期入口量化不冒称当时计数。 |
| Planning/Activation | 三份worktree规划与当前身份属于可变输入，每次原semantic gate独立读取。D3表列实际历史native命令计数；D7已实际执行本轮scope→Author→Wording→Architecture→Approval→Activation，工程trace保留。拓扑数量变化时不借旧绝对计数声称当前after。 |
| Implementation/Check/Commit | 当前index/worktree/HEAD和候选、五份规划/上下文、parent/tree/result恢复各有直接consumer。保留原固定检查，不以加速数字删除。D3有实际Check/Commit样本；D7当次完整gates发生后再消费其事实。 |
| 完整Branch Review与bounded | 完整B..HEAD/dirty/mode/gitlink/Check与bounded输入身份分开；D3冲突resolved→当前Check→完整Review和单独无冲突bounded链为历史工程证据。D7不替代其语义或将旧pass当新gate。 |
| Delivery Review/Publish/Merge | 原exact candidate、PR、target、CI和事务/结果恢复consumer保留。D3表有实际原native样本；本批尚未发生的交付不填成功或0计数。 |
| Completion/history | 每份Delivery结构、Task/source/Publication/commit/PR关联、固定cutoff、first-parent和expected均独立校验。当前public API对缓存OID的metadata/type/可用性验证保留；不是重复body读取。不同app的aggregate独立保留。历史遍历本身按真实H增长，不声称总Git常数。 |
| Closure/Finish/Cleanup | D3原公开terminal fixtures及D4 Cleanup原计数保持其声明边界；当前589尚未整体完成，真实Closure/Finish/Cleanup不能提前执行。最终原owner发生后补实际结果。 |
| 少量资格/恢复检查 | 明确commit存在性、PR parent、first-parent ancestry、完整unfiltered delta与原结果确认各有独立用途。原少量cat/show/tree不能仅按命令名视为热点。调用内同目的重复metadata已按上表去除。 |

## 当前整体剩余

D7 source/consumer准备的Check、commit、独立完整Review、适用知识晋升和Refs-only交付仍未完成。随后原tools owner必须从clean committed D7来源正式更新Task与代表installed，保留Task/session/peer，取得匹配receipt、native、平台/mode/reapply/drift/sidecar及真实恢复/history链证据。原Completion再核对全部AC、历史交付的适用性及这份最终清单；只有整体完成才Closure/Finish/适用Cleanup。

上游#47残余修复已存在于精确9f40来源；其存在不等于本Task已正式采用。f70测试来源与实际main额外增量的边界保持，不声称整树相同。#575完整Release矩阵、Guru正式版本发布和业务仓采用各由原owner负责，不进入本普通Issue完成声明。
