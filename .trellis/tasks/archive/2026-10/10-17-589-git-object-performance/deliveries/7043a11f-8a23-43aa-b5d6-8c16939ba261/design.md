# D8 采用与集成设计

## 固定范围与独立架构结论

内容基线 B=`1cee58a6db1b9837054c6ce8582fb6c0bf9e55b8`，即最近真实D7 delivered head；PR target仍为main。D8独立Architecture实际candidate_assessment为no_architecture_impact/.96；本批仅采用既有能力，不产生新ADR、贡献或共享架构版本。

## 唯一来源处置表

| 来源与承诺 | 处置与落点 |
| --- | --- |
| #589 AC06/11/13/14及D7剩余责任 | retain：两个原目标正式采用匹配来源，原native/manual/query2实际验证，最终盘点与整体Completion。 |
| D7 clean canonical H1cee与Fork9f40/CLI-Core.4 | retain：source_locked执行源为本checkout已提交且trellis目录clean的H1cee；普通Task/规划dirty不改变source身份。原transport独立核对实际CLI/Core package bytes、Fork锁及公开API。 |
| 原guru-upgrade-tools/public maintenance | retain：每目标preview→AI审查→prepare一次冻结plan→invoke/同operation恢复；不调用完整Plan2。public tools、custom guru-team workflow与Guru资产分别由原owner安装。 |
| 当前config.yaml与平台选择 | retain：两目标各有一个非必需config冲突，保留真实用户配置；Task声明claude/codex/cursor，代表目标保持其实际codex投影。workflow安装D7 canonical正文、ownership custom及精确commit provider，不能标bundled。 |
| 原Task/session/archive/workspace与peer/common Python pointer | retain：仅原tools写集，写前按原owner检查；两目标自身receipt/native实际读回，309个Task侧peer指针及代表自身common指针保持原bytes。 |
| 真实手动合并恢复和query2 | retain：本批PR在Publication已记录、Delivery尚未记录时，以普通两父merge实际合并。原manual recovery首次重建candidate并写historical_success；同输入恢复返回原事实，query2读取真实七批及本批，无遗漏重复。 |
| D7性能与D1–D6工程证据 | retain：先对实际生产文件和依赖核对适用，承接同输入before/after及原FAIL/SKIP。必要源码/依赖有变化才定向补验证；不为时间数字加优化或重跑无影响矩阵。 |
| RDT/Architecture及最终Completion | retain：原RDT owner维护唯一Test的实际采用结果；原Architecture按当前stage实际适用性判断，无新机制不再晋升。最终全AC及清单只由原Completion判断。 |

## 安装、恢复与证据

两目标串行执行，冻结每目标一次public operation id；部分写入只走同operation resume，不能以重新prepare隐藏失败。普通config保留不妨碍required脚本安装。所有sidecar逐项按原canonical内容或保留用户内容处理；有essential冲突或native缺口则不能tools_upgraded。原Task的脚本与受管投影由此正式动作更新，禁止手工patch。回滚仅由原tools owner按原preimage/Task兼容执行，不reset或改历史。

正式manual recovery必须观察到第一次执行新candidate入口；不能用已记录事实短路代替。真实provider网络与本地自动化耗时分别保留；不从trace构造语义pass。Git Trace2只统计本步骤及其真实子进程，逐对象内容/hash操作量沿原observer规则核对，不复制摘要算法。Completion/Closure/Finish/Cleanup计数在实际发生时采集，不提前填0或成功。

## 边界

工具交付、软件发布和业务仓采用分别报告。本批无业务部署/DB/凭据变更；不发布版本或npm，不扩大#575矩阵，不改同事工作树。
