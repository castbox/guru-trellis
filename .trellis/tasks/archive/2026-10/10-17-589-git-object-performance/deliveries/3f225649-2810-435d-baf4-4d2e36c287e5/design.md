# D1 历史候选批量读取设计

## 当前机制与边界

开发基线 B=3676b9ee65834ef3720f2ff5cc0d8330afcea6ed，来源为本Task显式选定的main开发基线；PR目标main独立，H0仅为Planning观察。D1范围见同目录prd.md，整体责任见根prd.md。独立Architecture candidate_assessment已通过no_architecture_impact；无contribution/ADR义务，final_plan仍需独立承接。

## 单一实现路径

直接修改Merge原history/manual_recovery职责。仅因两个真实caller共用候选Git对象读取，提取package-private最小读取能力；不放共享kernel、不新增公开API/schema/config。

元数据按候选路径批量ls-tree -z取得，保留现有候选文件/mode/删除语义。固定按UTF-8 argv字节预算64KiB分块，末块按余量；不得逐路径伪装分块。复用key包含实际Git root、不可变tree/OID与被查询路径；真实移动ref在入口重新解析，不缓存ref/index/worktree。若树枚举对原入口的pathspec/文件类型语义无法保持，先修订本设计，不静默改变合同。

相同blob OID在一次对象读取上下文中只请求一次内容。完整request和response使用普通临时文件；Git完成后逐响应校验OID/type/size和换行，内容以不大于1MiB缓冲复制至临时blob文件，再按每条路径落盘mode。拒绝不完整响应和正常读取失败，沿原CommandError/prepare恢复。仅metadata与offset/临时路径留在内存，不让整批内容常驻。临时状态随调用退出删除，不进入runtime checkpoint或tracked状态。

HistoryContext拥有同一查询的读取上下文，历史对象准备切换实际repo时重建相应上下文。复用内容不能替代每份Delivery独立的结构、身份、归属、祖先、query截点、candidate比较和恢复检查。保留#569隔离准备、合法空结果与实际失败区别，不在调用方common-dir fetch。手动恢复没有共享查询上下文时使用本次调用的独立短生命周期上下文。

原官方candidate_content_ref仍消费按路径落盘的候选快照；不复制其摘要算法。官方逐路径内容hash是上游独立职责，本批不得声称已去除其重复hash或替它添加缓存；须在盘点/证据列明该剩余边界。D1消除的是Guru自有逐路径Git读取与同次调用重复对象内容请求。上游缺口不能计为整体完成。

## 唯一来源承接矩阵

| 来源/原承诺 | 处置 | 落点与理由 |
| --- | --- | --- |
| #589 §3.3历史查询/手动恢复 | retain | 原Merge owner批量元数据、唯一blob读取，保持固定截点与恢复。 |
| #589 §5.2 / #579传输可结束 | retain | 文件request/response、有界解析，禁止双向pipe互等。 |
| #589 §5.3–5.4 | retain | 仅调用内复用不可变事实，每份输入独立检查。 |
| #589 §5.6–5.8 | retain | 两真实caller的package-private读取职责，原摘要/API/错误行为保持；不补丁官方脚本。 |
| #588独立交付 | retain | 基线已包含；不重做Reconcile、不计它的性能收益。 |
| #567 | retain | 不增加默认追赶base、fetch循环或业务重跑。 |
| #589 §6–8 | retain | 先完整before测量，再固定本批数值标准，最后生产修改和对照；未通过项不计完成。 |

## 已固定测量合同

before源码及安装来源为上述B的canonical，代表性installed通过原apply生成；工具/平台版本、样本Git历史与源hash随数据记录。计时包含真实Merge/history公开wrapper、客观校验与公共store，fixture的GitHub响应等待单列为fixture成本；liveGitHub另测，不将fixture作为远端证明。

当前已测1002路径manual入口：24.712/25.021秒，2017/2012 Git（初次记录与stdout丢失重入的固定差额分别保留）。duplicate/unique大档、history路径与Delivery数量对照、installed组及独立RSS/profiling均已取得before。完整before及固定门槛见同目录performance-contract.md；各组公开链和读取阶段至少改善20%，canonical RSS上限100/24MiB、installed/dogfood128/48MiB（runtime/Git），after不放宽。原数据、计时边界、重复/汇总、源码和安装来源及未验证边界由该唯一证据承接。
