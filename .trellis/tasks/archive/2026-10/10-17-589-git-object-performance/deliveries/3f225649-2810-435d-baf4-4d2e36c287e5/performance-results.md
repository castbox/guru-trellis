# D1 性能结果与证据边界

## 范围与结论

本结果承接同目录 `performance-contract.md` 的修复前基线与固定标准。D1 Guru 自有 history/manual recovery 热点及下表代表性本地公开链均达到至少20%改善，所测单进程RSS均低于固定上限；这不是整体#589完成、远端发布、业务采用或完整Release矩阵结论。

manual与installed采用 `after-d1/` 原始数据；最终history.py删除未使用message读取后，history全部采用全新 `after-d1-final-history/` 数据，不沿用旧history数字。修复前仍为开发基线B所测数据，不将#588既有收益计入本次优化。所有文件计数、结果、原错误与快照摘要的等价性由公开链及定向测试承接。

## 原公开wrapper耗时

每组重复两次并取中位数；manual保持初次记录→原结果恢复，history保持固定截点重复只读查询。准备在计时外，wrapper内validators/store/固定命令在计时内，Trace2流式分析在计时外。没有清OS cache或声称cold cache。下面改善率为 `1 - after中位 / before中位`，固定门槛未放宽。

| 组 | before中位秒 | after两次秒 | after中位秒 | 改善 | 20%判定 |
| --- | ---: | --- | ---: | ---: | --- |
| manual 1000 duplicates | 24.866359 | 0.962679 / 0.847295 | 0.904987 | 96.36% | PASS |
| manual 10000 duplicates | 253.844481 | 3.266940 / 2.942854 | 3.104897 | 98.78% | PASS |
| manual 10000 unique | 253.835584 | 3.341739 / 3.071484 | 3.206612 | 98.74% | PASS |
| history 100 | 5.086445 | 0.629109 / 0.625357 | 0.627233 | 87.67% | PASS |
| history 1000 | 46.372875 | 0.757430 / 0.770405 | 0.763918 | 98.35% | PASS |
| history 2 Delivery / 10 assets | 1.676705 | 0.697238 / 0.698989 | 0.698114 | 58.36% | PASS |
| history 4 Delivery / 10 assets | 2.877567 | 0.968229 / 1.003948 | 0.986089 | 65.73% | PASS |
| installed manual 1000 | 26.977111 | 0.953230 / 0.849505 | 0.901367 | 96.66% | PASS |

## Git进程分类

以下为一次原公开操作中的全部Git；分类数是进程数，不是请求对象数。`cat-file`含原有固定commit/可读性检查，不把`-e`算作内容读取。manual初次/恢复的固定5进程差额保留，未从总数中扣除；history相同截点两次计数相同。

| 组 | before Git / cat-file / ls-tree / show | after Git / cat-file / ls-tree / show |
| --- | --- | --- |
| manual 1000 duplicates | 2017/1006/1002/0; 2012/1006/1002/0 | 16/5/1/0; 11/5/1/0 |
| manual 10000 duplicates | 20017/10006/10002/0; 20012/10006/10002/0 | 18/5/3/0; 13/5/3/0 |
| manual 10000 unique | 20017/10006/10002/0; 20012/10006/10002/0 | 18/5/3/0; 13/5/3/0 |
| history 100 | 416/207/204/2; 416/207/204/2 | 10/3/1/1; 10/3/1/1 |
| history 1000 | 4016/2007/2004/2; 4016/2007/2004/2 | 10/3/1/1; 10/3/1/1 |
| history 2 Delivery / 10 assets | 109/53/48/4; 109/53/48/4 | 17/5/2/2; 17/5/2/2 |
| history 4 Delivery / 10 assets | 215/105/96/8; 215/105/96/8 | 31/9/4/4; 31/9/4/4 |
| installed manual 1000 | 2017/1006/1002/0; 2012/1006/1002/0 | 16/5/1/0; 11/5/1/0 |

10000-path元数据采用实际64KiB UTF-8 argv预算，因此after为3次ls-tree；不是逐路径调用。history 4 Delivery仍有4次候选树元数据/独立输入验证，保持每份输入的身份、归属、祖先、截点和候选比较。

## 内容请求与逻辑字节

volume为独立pass：仅捕获scalar `cat-file blob/-p`与普通文件stdin的`--batch`内容请求，metadata `-e`不计；大小探针位于operation timer和Trace2统计外。manual原raw使用逐OID `cat-file -s`大小分析；最终history raw使用一次普通文件式`--batch-check`逐OID解析type/size，仅计真实blob。两者不改变操作读取量或计时边界；当前可复现工具已收敛为单次batch-check，避免大unique样本分析的逐OID进程开销。下表为两次操作合计，每次调用内的重复blob仅请求一次；跨两次调用不会持久缓存。byte为逻辑成功返回内容，不是磁盘物理IO。最大blob均16,777,216 bytes。

| 组 | 内容请求总数 | 两次合计唯一OID | 逻辑返回bytes | 唯一内容bytes |
| --- | ---: | ---: | ---: | ---: |
| volume-manual-1000 | 132 | 66 | 34078736 | 17039368 |
| volume-manual-10000-duplicates | 132 | 66 | 34078736 | 17039368 |
| volume-manual-10000-unique | 20004 | 10002 | 115474448 | 57737224 |
| volume-history-1000 | 132 | 66 | 34078736 | 17039368 |
| volume-history-4 | 30 | 15 | 33636434 | 16818217 |

以上scalar内容请求为0，均由batch请求承载。1000/10000 duplicate每次66个唯一blob（64小blob+16MiB大blob+app）；10000 unique每次10002个。修复前manual每次按1002/10002路径请求内容，逻辑字节20,873,224/57,737,224；after duplicate每次降为17,039,368，unique仍为57,737,224但消除逐路径进程。history 4 Delivery含各自app版本，在一次查询内跨Delivery复用共同资产；两次合计15个不同OID、30次请求，不能把每候选路径数当成唯一请求数。

## 独立函数profiling

下表为另一个独立cProfile pass，保留原dispatcher/客观consumer，不能替代wrapper timing。候选元数据、重建和官方hash的cumulative时间可能嵌套/重叠，禁止相加为互斥阶段；也不把不同pass硬加总。provider为本地CLI响应fixture进程时间，网络等待为0，不能声称真实GitHub网络加速。

| 组 | dispatcher总秒 | history candidate秒 | commit_candidate秒（含hash） | 官方hash秒 | 本地provider秒 |
| --- | ---: | ---: | ---: | ---: | ---: |
| profile-manual-100 | 0.595098 | 0.000000 | 0.095776 | 0.028729 | 0.164509 |
| profile-manual-1000 | 0.971509 | 0.000000 | 0.364469 | 0.198530 | 0.162223 |
| profile-history-100 | 0.417785 | 0.048450 | 0.057097 | 0.027915 | 0.088126 |
| profile-history-1000 | 0.730135 | 0.055915 | 0.327922 | 0.199756 | 0.090901 |

修复前manual100/1000重建为2.587935/24.582535秒，history100/1000 candidate为2.524157/39.459463秒、重建为2.599515/29.298234秒；对应after均改善超过20%，PASS。官方candidate_content_ref原算法保留，其按路径重复hash仍属于上游缺口，未声称本批已优化。剩余dispatcher耗时不能仅从这些重叠函数做减法推导成“其他校验”或网络时间；只能与原wrapper总量、已单独观测的provider及上述函数范围并列理解。

## 独立RSS

macOS BSD time逐个测实际wrapper runtime与各Git命令，单位bytes；不是同时进程组总量，不把controller/安装/准备阶段峰值混入。固定canonical上限100/24MiB、installed/dogfood128/48MiB，MiB=1048576。instrumented pass的elapsed不用于timing对比。

| 组 | runtime各次RSS bytes | Git最大RSS bytes | 固定上限 runtime/Git | 判定 |
| --- | --- | ---: | --- | --- |
| rss-manual-1000 | 58720256 / 57769984 | 6111232 | 100/24MiB | PASS |
| rss-manual-10000-unique | 79429632 / 75677696 | 23183360 | 100/24MiB | PASS |
| rss-history-4 | 57278464 / 59441152 | 5718016 | 100/24MiB | PASS |
| installed-rss-1000 | 64552960 / 66437120 | 22200320 | 128/48MiB | PASS |
| installed-rss-10000-unique | 93847552 / 85065728 | 23314432 | 128/48MiB | PASS |

## Native dogfood与正确性测试

真实dogfood公开discover入口查询当前#589 Task，repo为castbox/guru-trellis，固定截点486c4ae0e658b4a677a0bee61ac01a30d5391cdf。原结果为`status=discovered`、`deliveries=[]`，不把空列表当成候选读取命中证明。BSD time为7.59秒，runtime RSS49,414,144 bytes；Trace2共303个Git，其中300个不同commit message的show，另1个cat-file、0个ls-tree。300次message读取属于原遍历的不同提交，不是同OID的无用重复。该native调用包含live provider，网络/远端等待未单独拆分，不能与fake-provider timing作同口径性能对照，也不声称303进程已全被本批优化。

最终Merge package测试日志 `/tmp/guru-589-d1-package-message-read-tests.log`：66 tests / 78.513s / OK，零skip。覆盖批量路径/唯一blob/特殊路径/普通缺失和失败、原history准备隔离与固定截点、手动恢复和结果丢失等本批合同；它不是native AI Gate、真实push/PR/merge或整体Task完成证据。

## 安装、来源与未验证边界

before代表性clean target由匹配Fork CLI init与原preset apply生成；after本地候选通过原apply/reapply复制进真实新Git fixture并调用installed wrappers，raw见installed各目录。当前这些属于local_candidate安装证据；正式source lock绑定的最终安装/发布链未测，不得把本地候选installed通过扩大为版本发布兼容结论。最终源码已由原 guru-upgrade-tools 新操作同步dogfood；同操作 tools-only reapply 为 skill_packages=ok、overlays=ok、installed_validation=0。代表性target原apply发现一份history.py.bak，逐项核对为前版源码且当前文件等于canonical后，可恢复移至诊断备份目录；再apply status=ok、installed validation passed。最终source/dogfood/installed三种package验证及dogfood drift均通过，Codex/Claude/Cursor投影一致。最终installed原公开history100入口两次0.582712/0.588182秒（中位0.585447），结果保持discovered，raw为after-d1/installed-final-history-100；无before配对，不另声称其改善率。原生.trellis/scripts无diff；Task/history数据未作迁移。formal_fork_source_lock仍unverified，完整官方update/upgrade及多平台矩阵不在本批证明范围。

D1只完成Guru history/manual recovery对象读取及本批证据。D2 bounded continuity、D3生命周期解析/全流程计数和联合回归仍剩余。官方Task创建逐路径show、candidate_content_ref逐路径重复hash没有可用公开预计算/批量输入接口，本批不补丁官方脚本、不复制绕过hash、不将不可分离上游前置计完成。整体#589不得由本D1结果关闭；完整多平台Release矩阵仍归专门#575。

## 可复现入口与raw定位

source-private工具及参数说明见canonical `trellis/skills/guru-team/packages/guru-merge-task-delivery/tests/README.md`。同输入使用`--entry manual/history --paths 100/1000/10000 --kind duplicates/unique --deliveries 1/2/4 --repeats 2`；profiling按原独立pass一轮，RSS/volume独立运行，output必须新目录。

本次raw根为 `/tmp/guru-589-diagnostics/`：before保留`formal-before-*.jsonl`、`installed-before-*.jsonl`、`profile-*-duplicates-0.json`及原Trace2；manual和installed after保留在`after-d1/`；最终history timing/profile/RSS/volume保留在`after-d1-final-history/`。每组有`summary.json`、`git.trace.jsonl`，独立pass另有profile JSON、BSD time RSS、batch requests及size-probe文件。原before unique失败样本仍保留，依固定合同未算通过，也不声称优化修复了其API前置错误。
