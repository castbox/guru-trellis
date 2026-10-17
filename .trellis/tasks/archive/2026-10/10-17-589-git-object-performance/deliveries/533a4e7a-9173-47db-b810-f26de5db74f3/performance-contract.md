# D7 当前读取工作验收

当前来源：[Issue589 §6](https://github.com/castbox/guru-trellis/issues/589#6-基准要求)。以尽量消除不必要读取、逐路径进程放大与同调用同规则重复hash为完成目标，不设耗时改善百分比硬门槛。每份候选的独立结构/身份/关系/祖先/expected/cutoff/恢复检查保持；保留项逐项说明必要consumer。

沿用下列原测量的相同入口、输入、工具和方法；源码/依赖差额明确报告。完整source/代表installed矩阵报告内容请求及唯一OID/bytes、snapshot文件读取、内容hash次数/输入、独立aggregate、Git进程/分块、真实whole-wrapper时间及RSS范围。不得全批内容常驻、持久缓存或改变摘要算法。资源必须有界，异常按实际机制分析。

旧百分比与RSS数值界限、原FAIL和所有cohort均作为历史观测保留，不改称通过，也不作为当前完成门槛。下方全文为原冻结合同的历史快照；current Check按本节及live Issue判断。原冻结全文SHA256=7f8141e5f023d28150c0fa7bd4744f01cc1b9bf9ac66d9eb42c19bd5efb5d630，可对分隔符之后原字节复核。

<!-- original-frozen-contract-begins -->
# D7 实施前固定性能合同

状态：完整 before 已取得，after 尚未执行。唯一 consumer 为 D7 Check/Delivery Review 及整体 Completion。

## 来源与方法

生产 B=865f4a9576eabc85cb3b91e74ecd856785095510；Fork c7bd746b42d75f73534c85e263cd6b51fe0e5287 / CLI-Core 0.7.0-castbox.3。after 只承接设计锁定的9f40ec70914f98fce2619560274cc1d0619f2f7e / CLI-Core.4及本批consumer替换；c7→9f生产差额仅delivery_store.py/git_objects.py，保留#588状态。

Python 3.14.8；git version 2.54.0 (Apple Git-157)；macOS27.0.1 arm64；managed interpreter=/Users/wumengye/Library/Caches/guru-team/python/f0b89dabd24ef812b1244b8b/venv/bin/python。PATH显式以其bin优先；before/after保持。已有OS缓存，fixture准备先于测量，不清缓存、不声称cold-cache。各cell串行两次fresh公开wrapper调用，每次repeats1，取两数median；manual计first_record，history计recorded_history_query，stdout丢失恢复另验证不混median。完整本地链包含原wrapper、客观validator/store及fixture provider进程；fixture网络等待=0，不代表live provider/native AI证明。准备、观察和操作外步骤不纳入plain。原Github正式链另报告实际总耗时与网络等待边界，不把fixture冒称正式交付。

volume、RSS、profile、hash独立于plain。history资源四pass复用一次真实prepare_history，各pass仍为独立原public wrapper进程/context，无Task回滚、跨操作缓存或结论复用。manual四pass各自fresh准备。before/after同bundle及顺序。Git按一次操作全部子进程计数，show/ls-tree/cat-file分列；batch-command info/contents/flush分别计metadata/body/control。只probe实际root，缺失/未捕获/失败必须为0。body量和真实hash输入分别计，不能仅计cat-file。profile精确模块+qualified函数，各cumulative独立列出，禁止嵌套相加或与plain相减后冒称精确分解。

RSS bytes：BSD time所测wrapper及其后代的最大单进程RSS（非纯Python、非同时进程组总量），Git另取逐进程最大。wrapper每cell上限=before×1.25+8MiB；Git统一上限=37408768bytes，依据相同16MiB大对象在before各cell出现5.6–23.2MB单进程波动，采用全部before最大23,216,128×1.25+8MiB。不是事后容差。无全批内容常驻、无限缓存或跨调用缓存。

## 固定数值门槛

各cell chain改善至少如下；热点为原commit_candidate累计profile（history按其处理全部实际Delivery，old递归calls不重复求和），after同函数至少改善20%。依据：before小档该核心约0.069–0.184s、四Delivery约0.312–0.337s；大档约3.02–3.74s、四Delivery约12–13.25s。完整链保守要求5%/10%，不把固定验证都设为需同倍加速。下表是实施前界限，after失败不得放宽。

| cell | before链s | 链最低改善 | before核心s | wrapper上限bytes | Git上限bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| source-manual-128-duplicates-d1 | 0.669697167 | 5% | 0.113425709 | 60407808 | 37408768 |
| source-history-128-duplicates-d1 | 0.535388876 | 5% | 0.068758167 | 60182528 | 37408768 |
| source-history-128-duplicates-d4 | 0.994266625 | 10% | 0.325415125 | 60366848 | 37408768 |
| source-manual-128-unique-d1 | 0.675595145 | 5% | 0.108186917 | 59035648 | 37408768 |
| source-history-128-unique-d1 | 0.543802251 | 5% | 0.076896416 | 60510208 | 37408768 |
| source-history-128-unique-d4 | 0.992414355 | 10% | 0.337016500 | 60510208 | 37408768 |
| installed_template-manual-128-duplicates-d1 | 0.715464979 | 5% | 0.184455916 | 62005248 | 37408768 |
| installed_template-history-128-duplicates-d4 | 1.061362437 | 10% | 0.311736083 | 62701568 | 37408768 |
| source-manual-10000-duplicates-d1 | 3.213828250 | 10% | 3.690780708 | 77283328 | 37408768 |
| source-history-10000-duplicates-d1 | 2.816495771 | 10% | 3.584891375 | 79392768 | 37408768 |
| source-history-10000-duplicates-d4 | 9.986936563 | 10% | 12.219312000 | 117792768 | 37408768 |
| source-manual-10000-unique-d1 | 3.309054105 | 10% | 3.741035125 | 86151168 | 37408768 |
| source-history-10000-unique-d1 | 3.033268730 | 10% | 3.021327292 | 75030528 | 37408768 |
| source-history-10000-unique-d4 | 10.116238541 | 10% | 13.251827458 | 114515968 | 37408768 |
| installed_template-manual-10000-duplicates-d1 | 3.193050396 | 10% | 3.680638000 | 86765568 | 37408768 |
| installed_template-history-10000-duplicates-d4 | 10.273913458 | 10% | 11.998720875 | 109498368 | 37408768 |

## 输入、读取及摘要门槛

路径增长单独128/10000 assets，实际候选各130/10002路径（另app与16MiB large）。duplicates资产unique=65，unique档资产unique=129/10001；加app分别66/130/10002个blob。每资产4096bytes，path bytes=17,301,504或57,737,216，加app实际bytes见原始样本。Delivery增长单独1/4，其余保持。source12cell，installed-template4cell；后者为代表原安装复制+canonical reapply fixture，非最终Task工具采用。

每cell前后完整paths、mode/type/blob、content_ref必须等价，不要求或声称完整HEAD/tree相同。before body已去重（duplicates66或69，unique130/133或10002/10005），after不得为相同blob重复请求内容。同一操作同算法内容hash一次；不同路径摘要贡献完整，各候选独立结构、Task/Delivery/PR关联、祖先、expected、cutoff及恢复检查不减。before snapshot filesystem/hash输入D1=17,301,512或57,737,224 bytes，D4=69,206,057或230,948,905bytes；after snapshot filesystem读为0，blob hash输入等于操作内唯一实际blob bytes，不复制hash算法。aggregate同serialized entries仅一次；不同app版本形成独立摘要不强行统一。

公开context批量上限4096（首批commit info占1），与旧Task/local_commit128资源批次区别报告。必要metadata存在性与每份输入验证保留，不要求Git数量归零。特殊路径、mode、删除、unsupported目录/symlink/gitlink、正常缺对象/读取失败、准备切root关闭与重试、相邻操作刷新、恢复与stdout丢失必须通过真实caller验证。

## 已执行证据及失败边界

完整before计时：/tmp/guru-589-d7-before-fixed-python；完整V2观察：/tmp/guru-589-d7-before-observations-v2；汇总：/tmp/guru-589-d7/before-summary-final/summary.json及summary.md。16/16完整、32plain、missing0/error0；各sample有实际命令、trace、原始stdout/stderr和候选身份。

plain工具V1与观察V2差额仅profile/hash runtime定位及其失败raw记录/定向test；plain instrument_wrapper提前return，main/setup/计时/trace/volume/RSS未改变，因此32plain可承接。after使用冻结V2，功能计时路径保持同方法。

原/tmp/guru-589-d7-before的两次installed setup因PATH选其他Python导致dependency_install_failed，未进入有效计时；fixed-python完成32plain后第33个冗余观察被明确取消，不算观察失败或有效样本。V1观察installed profile曾因runtime路径定位失败，保留/tmp/guru-589-d7-before-observations-v1；V2完整重采，未删改失败。上游旧Mac/Ubuntu FAIL及后改口径不改变本合同。

## 冻结工具

- benchmark_git_objects.py: 689e93c2a0599fe60c5176bf0c32f0e60ba44d0ed83fc389ab1942134325487c
- benchmark_profile.py: 64b2ac4cd6ac6cbba9fa48908f1eb9482da62b751ab6856ea869884b167b08e3
- benchmark_observer.py: 4a29f97ad4b3bfa1bb25e85afe0f52b6ab3b0a358673678762c7c494b19ff143
- test_benchmark_observer.py: aecf0fdd14af6bd2de95cdb9eed7fd38aeb2af2c11d86e2a818e6de63895b08d
- observe_bundle.py: e444f436bfe02b0b496cce459e7c194f4568088132d102095ead920f4a548f3d

源码差额、代表candidate安装、正式目标采用及native/正式链分别取证。本批仅partial source/consumer preparation；后继原tools owner从clean committed source正式采用两目标。#575完整Release矩阵、Guru正式发布、业务仓采用不由本合同宣称通过。
