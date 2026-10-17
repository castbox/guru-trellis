# D3 性能与兼容验证结果

## 候选与口径

固定before B=c422692bca2d385a264da4db0030612b1b306fe1；after是本Delivery尚未提交的已冻结生产工作树，不把当时仍为B的HEAD冒称after代码。开测和结束的实际生产字节核对见原始candidate.json/input-equivalence.json；后续精确提交与完整分支Review绑定这些生产实现。Fork仍2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0，CLI/Core0.7.0-castbox.3，source/installed实际managed CPython3.14.8。环境沿用同会话D1/D2记录的macOS27.0.1 arm64、Apple Git2.54.0，并在本轮结束复核一致；原D3各summary没有逐份重复OS/Git版本，不声称44份sample分别采集过这些版本。

原固定合同performance-contract.md未降低门槛。source16+installed6组，各两轮fresh fixture；timing/profile/RSS/volume独立pass，恢复单列；安装和fixture准备在timer外，原公开wrapper/validator/官方writer完整保留。原工具和Task池未改，canonical source-private工具两个模式的AST分别与冻结工具相同。before/after source与installed合法tree不同，分别比较。

## 耗时

| 完整本地操作 | before中位秒 | after中位秒 | 改善 | 固定最低 | 结果 |
| --- | --- | --- | --- | --- | --- |
| create10 | 2.166481583 | 1.980555833 | 8.58% | 5% | PASS |
| create100 | 5.143998750 | 3.073512500 | 40.25% | 20% | PASS |
| binding10 | 0.973383437 | 0.517656895 | 46.82% | 20% | PASS |
| binding100 | 4.772066375 | 0.520967230 | 89.08% | 50% | PASS |
| installed-create100 | 5.708641979 | 3.642049958 | 36.20% | 20% | PASS |
| installed-binding100 | 4.920641417 | 0.663990396 | 86.51% | 50% | PASS |

| source原始after两轮 | 秒 |
| --- | --- |
| create10 | 2.029883083 / 1.931228584 |
| create100 | 3.142433333 / 3.004591667 |
| binding10 | 0.518161041 / 0.517152750 |
| binding100 | 0.521591667 / 0.520342792 |

| 独立profile热点累计 | before中位秒 | after中位秒 | 改善 | 结果 |
| --- | --- | --- | --- | --- |
| create10 | 0.446664958 | 0.200208583 | 55.18% | PASS |
| create100 | 2.363133604 | 0.242919167 | 89.72% | PASS |
| binding10 | 0.713713438 | 0.222699855 | 68.80% | PASS |
| binding100 | 4.551114542 | 0.227543916 | 95.00% | PASS |

profile是prepare_creation_inputs或两次discover_branch_candidates的累计总和，不是CPU时间，不再叠加内部函数，也不从完整链扣除官方writer。create10的5%仅低置信度工程门槛，两轮不足以证明统计显著。恢复原入口返回原事实，单列raw，不混入首次中位。16项固定数值检查全部PASS。

## 一次操作的Git与内容量

| source规模 | Git before→after | show before→after | cat-file before→after | ls-tree before→after | 成功内容请求 before→after | 返回bytes before→after |
| --- | --- | --- | --- | --- | --- | --- |
| create10+ensure | 137→117 | 30→10 | 0→1 | 3→2 | 30→20 | 17250→11500 |
| create100+ensure | 407→207 | 300→100 | 0→1 | 3→2 | 300→200 | 172500→115000 |
| binding10 | 67→24 | 24→0 | 22→1 | 0→2 | 2→1 | 944→472 |
| binding100 | 427→24 | 204→0 | 202→1 | 0→2 | 2→1 | 944→472 |

create唯一blob10/100、unique bytes5750/57500、max575B；binding唯一blob1、472B/max472。installed100档命令/volume与source对应档一致，两轮相同。旧binding内容尝试24/204、missing22/202；after只请求实际存在唯一blob，missing内容请求0。metadata -e不计内容，missing不计成功。

Guru创建reader同head树只枚举一次，同OID只读一次；官方writer另一个原调用仍逐unique head/path读取N次，因此整个create操作仍2N成功请求。不能声称完整操作所有内容已去重。ensure固定18Git保留。branch两次resolve仍独立刷新refs/worktree/ownership/唯一候选/expected head，单reader只复用immutable facts；两个head树枚举是必要成本，不是逐缺失路径启动Git。官方writer是剩余上游责任。

## 内存与原Merge资源回归

D3 source wrapper最大38,092,800/Git7,061,504bytes；installed wrapper39,419,904/Git20,692,992bytes。全部通过固定wrapper64MiB、source Git16MiB、installed Git32MiB。BSDtime是每wrapper invocation的单进程max，不能拆父Python与同步官方child，也不是同时进程组总和；Git单进程另测，包含正常status，恢复另列。

共享提取后用原D1 ManualRecovery公开wrapper各两轮执行RSS回归：

| 组 | runtime最大bytes | Git最大bytes | 原D1上限 | 结果 |
| --- | --- | --- | --- | --- |
| source1000 duplicate | 58474496 | 6111232 | 100/24MiB | PASS |
| source10000 duplicate | 77758464 | 9273344 | 100/24MiB | PASS |
| source10000 unique | 76218368 | 23199744 | 100/24MiB | PASS |
| installed10000 unique | 79773696 | 23281664 | 128/48MiB | PASS |

保留16MiB大blob、原snapshot、记录/输出丢失恢复及原installer reapply；不重复计D1改善。共享spool仅metadata/offset驻留，JSON逐对象读取，snapshot<=1MiB复制；不构造整批bytes字典。大档ls-tree3块来自原64KiB argv边界，cat-file固定5（含原独立检查），不是每path一进程。

## 功能、正常失败与联合链

最终Lifecycle160、Merge66、Branch5、Identity4测试通过，零skip。Create原25项中24项通过，新增shared文件缺原validator exact inventory使1项安装失败；补齐该必要consumer后原失败项单独重验通过（22.957秒），不伪称整套重新执行。原缺fixture环境111项报错不计pass；按明确GURU_UPSTREAM_DELIVERY_SCRIPTS补环境后的最终160绿测才采信。新真实Git oracle覆盖普通/exec/symlink blob、tree/nonblob原show、missing path/blob、缺commit、唯一OID复用、逐对象读取、移动ref及两次resolve独立检查。旧固定少量commit_path_bytes caller不改，实际传输截断不当成功。

PR后冲突fixture经原Check/完整Review/Readiness/public publication形成PR9，随后实际base冲突→解决/暂存→原resolved wrapper提交→同输入恢复原commit→publication owner合法rework→当前公开Check→原projection→完整BranchReview。12个真实wrapper通过，保留同Task/Delivery/public PR fact及parent顺序。测试时发现resolved wrapper仅四级launcher，canonical完整包被误判不完整；按其他原wrapper加入三级canonical优先并保留四级fallback后实际全链通过。原脚本已收敛为source-private tests/joint_resolved_flow.py；初次准备错误与rework owner错误保留，不算成功。source正式结果根d3-joint-conflict-v4。此链的provider/semantic是fixture，不是live GitHub冲突证明。

无冲突实际整合后bounded continuity仍单独走原pull_request用例，不能当冲突后的完整Review；结果见d3-bounded-continuity.log。D2原流式树摘要/memo代码未改，D1原history/manual/cutoff/对象准备回归由当前66项承接，不用底层函数测试替代公开链。

## 安装与边界

原guru-upgrade-tools完成当前worktree tools-only同步，installed_version0.7.0-guru.4；上游211个工具action source/target bytes/mode相同，305个peer pointer保留。普通apply在本仓混合历史Task前置即拒绝，未改历史来通过；实际本仓工具同步由原tools-only owner完成。代表installed原apply产生8个bak，每个核对B原值和current目标后移到可恢复目录，随后reapply statusok、package/overlayok、installed validation0；dogfood overlay drift通过。新增shared模块同时进入installer与source validator的原exact inventory。原.trellis/scripts零源码diff，无旁路安装。完整矩阵/formal_fork_source_lock仍归#575，local_candidate不证明发布或业务采用。

原始before/after根分别/tmp/guru-589-diagnostics/d3-before与d3-after；aggregate、installed-aggregate、comparison、input-equivalence、method及各sample保留。Merge资源汇总为d3-merge-resource-comparison.json。native根正式调用有独立Trace2和wall；GitHub等待未拆分的native wall不参与上述本地改善。fixture网络为0，不冒称remote proof。

## 剩余整体责任

Cleanup同head旧Task快照refs在原select_explicit_cleanup_targets dry入口复现10/100资源63/513Git、12/102show、10/100ls-tree，已通过正常场景资格；这是新增同scope热点，后续独立Delivery承接，不计D3已优化。官方task_store逐路径writer与delivery_store重复hash前置也未解决。整体AC、Completion、Closure和Issue关闭仍受这些责任约束；本批仅Refs #589。工具交付不等于正式版本发布或业务仓采用。
