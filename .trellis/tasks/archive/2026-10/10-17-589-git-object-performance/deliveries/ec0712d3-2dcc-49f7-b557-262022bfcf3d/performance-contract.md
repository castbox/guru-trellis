# D2 实施前固定性能合同

## 输入、来源与测量

before源码HEAD=924f293821e1e3031b7efdbfc3b0868ef9d02011（D1已交付、含#588）；被测Review common/record仍为本批未修改的原实现。main开发基线与当前内容B见design.md，不把D1/#588收益计入。计时内受测dispatcher及原timing/RSS/volume链的依赖与D1相同：macOS27.0.1 arm64、managed CPython3.14.8、Apple Git2.54.0，Fork2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0 / CLI-Core0.7.0-castbox.3。

source原正式raw根/tmp/guru-589-diagnostics/d2-before-pr，12组均使用实际支持的pull_request profile；其中混合计数profile现降为探索，不参与热点计时验收。纯profile补证根/tmp/guru-589-diagnostics/d2-before-plain，见下文。installed正确PR组保留原/tmp/guru-589-diagnostics/d2-before/installed-timing-1000-duplicates-pull-request和installed-rss-10000-unique-pull-request；原target由匹配Fork真实init+原apply建立，原fixture复制到fresh Git后原apply，不patch副本。旧source local_commit探索12组和installed unsupported_delivery_profile准备失败不计验收；未称性能改造修复了它。

每组一个新临时Git历史，两轮相同准备候选，取中位。既有public完整Review→main正常前进→实际merge→当前Check后，计时内完整执行原review-branch.sh、check-review-gate.sh、invoke.sh并单列各次耗时。candidate_tree_sha256、fixture准备和结果分析在timer外；不跳wrapper/validator，不将bounded通过当完整Review。GitHub/provider与semantic均fixture，网络等待0，不是native AI或live发布/生产效果证明。无cold cache声明、不清OS cache、无并行性能压测。

Trace2薄Git入口覆盖全部子进程，统计timer外流式完成；volume捕获普通文件batch stdin并在操作后用一次batch-check求大小。timing、volume、RSS、纯cProfile与hashes独立pass，不能硬加总。RSS为macOS BSD time各实际wrapper runtime和每个Git的单进程bytes，不是同时进程组总量，不混controller/installer/准备。profile为原dispatcher独立归因（绕launcher），tree_identity cumulative包含其内部工作，不能再加嵌套validate时间；blob SHA与最终tree SHA分别记录，after须随真实hash落点承接，不能用旧源码行零调用冒充零hash。

## 完整原链before与固定after门槛

| 组 | 两次总秒 | before中位秒 | 最低改善 | after中位最高秒 |
| --- | --- | ---: | ---: | ---: |
| source1000 duplicates | 1.948980 / 1.959552 | 1.954266 | 5% | 1.856553 |
| source10000 duplicates | 4.444185 / 4.434230 | 4.439208 | 5% | 4.217248 |
| source10000 unique | 3.237896 / 3.200181 | 3.219038 | 3% | 3.122467 |
| installed1000 duplicates | 2.296435 / 2.436270 | 2.366352 | 5% | 2.248035 |

source每次原链62 Git / cat-file4 / ls-tree8；counts逐wrapper保存在summary。保留独立checker/invoke必要重读，不要求固定少量Git为0，after新增必要immutable-tree解析或分块须如实单列，不能改名隐藏进程。

## 读取热点before与固定after门槛

热点为同一个profile pass中record/checker/invoke各tree_identity累计时间之和，内部validate不再另加。

| source组 | 两次tree累计秒 | 中位 | 最低改善 | after最高中位秒 |
| --- | --- | ---: | ---: | ---: |
| 1000 duplicates | 0.323086083 / 0.317922792 | 0.320504438 | 20% | 0.256403550 |
| 10000 duplicates | 1.673586124 / 1.681799832 | 1.677692978 | 20% | 1.342154382 |
| 10000 unique | 0.483089626 / 0.497921875 | 0.490505751 | 10% | 0.441455175 |

纯profile原dispatcher两轮累计分别1.769297501/1.746600166、5.844039250/5.820910749、4.635369334/4.696731542秒；tree份额约18%、29%、10.5%，其余为保留的dispatcher/身份/校验成本。unique没有资产OID重复，主要消除record同次调用的一轮计算；独立checker/invoke必须保持。因此完整链不能机械套D1的20%；本批分别固定上述仍可观察的改善目标，不能把profile份额跨pass硬减成plain秒数或网络时间。原百分比与全部完整链/RSS门槛在生产修改前已固定。随后实现已开始但尚无after时发现旧profile同时启用constructor observer，无法与流式hash探针作相同时间对照；已暂停并经同D2原owner回规划。上述三组在精确固定B的独立/tmp clone补测，canonical新harness位于clone外，以--source选择该clone、--profile-mode plain，未修改before生产源码；仅原bootstrap建立.git runtime pointer，结束tracked/dirty clean。身份核对补充：clone原bootstrap默认选择Python3.12.8，只用于timer外fixture准备；纯profile driver由本Task工作树原resolver启动，helper使用该driver的sys.executable直接运行clone dispatcher，实际为3.14.8，并不使用clone launcher。原driver命令、早于测量的f0b89指针快照和3.14.8 traceback支持此身份；不得声称整个clone环境相同。此澄清不改变计时内依赖、热点before数值或通过标准。每组两轮，无hash observer；raw为profile-1000-duplicates-plain、profile-10000-duplicates-plain、profile-10000-unique-plain，命令与汇总见该根runner.py和plain-source-report.json。before补证及本次合同修订均没有after数据；百分比不降，绝对秒上限仅按纯profile before重新计算，旧混合profile不参与验收。

## 规模、内容与资源

每组asset固定4KiB，duplicate为64内容池；另有一个16MiB大blob。source tree实际1044/10044 blob路径，含固定fixture和Task；unique OID分别105/105/10041。每次路径内容总bytes21400795/59146795/59146795，唯一内容17566885/18448885/59146741。最大blob16777216bytes。两轮原读取tree共8次（每轮record2+checker1+invoke1），blob内容请求8352/80352/80352、成功返回bytes171206360/473174360/473174360，scalar为0。官方Task候选清单自身随路径增长形成的正常metadata成本保留。

installed有真实受管文件：1000档7163 blob路径/2623unique、41649891路径bytes；10000unique档16163路径/12559unique、79395891路径bytes，不能与source当作相同整树直接比较。各自before/after保持同安装fixture与原wrapper。

固定资源上限：source runtime<=128MiB、Git<=24MiB；installed/dogfood runtime<=160MiB、Git<=48MiB，MiB=1048576bytes。source before runtime最大111001600/209633280/210665472bytes，Git6193152/7815168/23674880；installed10000unique runtime284770304、Git32571392bytes。上限结合小档常驻+元数据余量，要求流式后大档明显减内存；Git保留当前实际量级与安装额外tree余量。不是生产拒绝阈值，也不声称进程组峰值。

结构门槛独立于时间：单调用每个blob OID只请求/内容hash一次，record内相同immutable tree同规则只算一次；原路径贡献、摘要、类型/mode/删除/错误和每输入检查保持。after独立hashes pass观测实际构造/update/finalization及helper来源；纯profile不附计数探针。不能按旧行号零调用声称零hash。

## 当前边界

D2只交付原连续性技术热点。D3全流程/生命周期与联合回归、官方Task创建及重复内容hash上游前置仍待完成。local_candidate安装未证明formal_fork_source_lock、完整update/upgrade或Release矩阵（#575），也未证明业务仓采用。