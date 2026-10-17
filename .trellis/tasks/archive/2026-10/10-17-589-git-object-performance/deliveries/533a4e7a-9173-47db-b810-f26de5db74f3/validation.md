# D7 工程结果

## Before 与固定合同

[测量与验收合同](./performance-contract.md)当前首节遵从live#589§6：按不必要读取/计算消除及资源有界验收，不设耗时改善百分比硬门槛。其分隔符后原冻结数值与下面初轮PASS/FAIL仅是未改写的历史观测。before为16cell/32plain及四类独立资源观察，缺失0/错误0；详见原始/tmp/guru-589-d7-before-fixed-python、/tmp/guru-589-d7-before-observations-v2与/tmp/guru-589-d7/before-summary-final。

## 历史初轮 after：未达到当时全部门槛

source为public GitCandidateContent首次适配、metadata尚未收敛的worktree，HEAD865。原始/tmp/guru-589-d7-after-fixed-python（32plain均正常返回）；/tmp/guru-589-d7/first-after-timing-gates.json。11/16链耗时达标，以下完整结果不作为最终候选通过声明：

| cell | before s | 初轮 after s | 改善 | 原门槛 | 结果 |
| --- | ---: | ---: | ---: | ---: | --- |
| source-manual-128-duplicates-d1 | 0.669697 | 0.674199 | -0.67% | 5% | FAIL |
| source-history-128-duplicates-d1 | 0.535389 | 0.512983 | 4.18% | 5% | FAIL |
| source-history-128-duplicates-d4 | 0.994267 | 0.837128 | 15.80% | 10% | PASS |
| source-manual-128-unique-d1 | 0.675595 | 0.685847 | -1.52% | 5% | FAIL |
| source-history-128-unique-d1 | 0.543802 | 0.520529 | 4.28% | 5% | FAIL |
| source-history-128-unique-d4 | 0.992414 | 0.834329 | 15.93% | 10% | PASS |
| installed_template-manual-128-duplicates-d1 | 0.715465 | 0.706461 | 1.26% | 5% | FAIL |
| installed_template-history-128-duplicates-d4 | 1.061362 | 0.854905 | 19.45% | 10% | PASS |
| source-manual-10000-duplicates-d1 | 3.213828 | 1.377458 | 57.14% | 10% | PASS |
| source-history-10000-duplicates-d1 | 2.816496 | 0.980076 | 65.20% | 10% | PASS |
| source-history-10000-duplicates-d4 | 9.986937 | 2.789114 | 72.07% | 10% | PASS |
| source-manual-10000-unique-d1 | 3.309054 | 1.596730 | 51.75% | 10% | PASS |
| source-history-10000-unique-d1 | 3.033269 | 1.183483 | 60.98% | 10% | PASS |
| source-history-10000-unique-d4 | 10.116239 | 3.110022 | 69.26% | 10% | PASS |
| installed_template-manual-10000-duplicates-d1 | 3.193050 | 1.456525 | 54.38% | 10% | PASS |
| installed_template-history-10000-duplicates-d4 | 10.273913 | 2.774743 | 72.99% | 10% | PASS |

此轮manual/history源码原bytes保留/tmp/guru-589-d7/initial-after-source；hash分别为8ec31e31e7ce65ed0b00e2909fa91ad8cd19e5cef86c5084f64a8764a98bde04、ece466ef12d5aea9219a0b348cc6b5dbbef8fe5dd60bf7ef540d98637c184ace。独立诊断profile（不进入plain）在/tmp/guru-589-d7-after-diagnostic-core：manual128dup commit_candidate=.049356s、unique=.059949s，history128dup=.051911s；与before相同精确函数分别改善56.5%、44.6%、24.5%，core20%门槛通过。nested cumulative不求和，profile与plain不能相减冒称精确分解。

实际trace仍有两个same-scope冗余：manual四endpoint中两个相同OID各查两次；query2已经同root重建并逐input比较后的head又做-e。后续只复用相同exactOID或该输入在相同actual root内已证明的存在性；不省PR关系、parent、ancestor、cutoff、expected及候选独立检查。source/owner/SDK生命周期和持久化边界不扩大；仍属已批准的call-local immutable事实复用，Architecture完整candidate阶段另行独立检查。数值、输入、工具及失败样本保持。

## 兼容及来源准备

初次consumer tests：10 caller、9 manual、19 history共38 passed，日志/tmp/guru-589-d7/consumer-*-tests.log。来源定向15 tests及source-update7 tests通过；真实9f source lock与配对包public API无缺项。无明确legacyCLI的旧迁移专项1 SKIP，不代表迁移全链通过。

既有installed manifest测试在old aggregate-1.0 membership断言FAIL：HEAD865测试2289已要求旧ID，而HEAD865 manifest已列aggregate-2.0；D7三处current版本断言之外未改变其public schema inventory或该断言。界定为Issue§3.2排除的无关历史问题，不修改、不计通过、不扩张为当前finding/followup。

上游source-built/Release逐文件与mode转换对照、配对公开安装验证见/tmp/guru-589-d7/package-source-comparison.json及paired-public-install-verification.json。两可执行模板tar0644、原installer正规投影0755，未宣称raw mode全等。

代表candidate：原.3副本上普通update拒绝跨版本（日志/tmp/guru-589-d7/candidate-upstream-update），未动原Task/installed目标。一次clean .4三平台init使用配对Release CLI及Guru marketplace pin865；首次错误-u在写前被CLI拒绝，按实际help去除后同target成功。原preset apply于/tmp/guru-589-d7-clean-installed-candidate成功，package/overlay conflict0/sidecar0；此为source候选代表验证，非最终目标tools维护。

## 当前候选与证据进展

metadata收敛后的consumer回归manual10/history20/content10/provider1共41项通过；原日志为/tmp/guru-589-d7/consumer-*-refinement-tests.log。原source/current版本差额没有再为耗时指标追加生产改动。

第二轮原首cell的两次有效时间.683573542/.675087625、median.679330583仍保留在/tmp/guru-589-d7-after-refined-fixed-python/stopped-at-failed-gate.json，旧5%门槛FAIL不改称PASS，矩阵当时合法停止。旧源码当前环境counterfactual为.740589833/.701269791、median.720929812，原基线未复现；78个production/runtime文件与865相同，业务输入相同。该诊断不能替换基线、定位具体环境成因或证明新的性能通过。

当前完整after plain位于/tmp/guru-589-d7-after-work-acceptance-fixed-python；16cell/32fresh，exit0全部32，逐组paths/mode/type/blob/content_ref与before对照16/16相同。汇总/tmp/guru-589-d7/current-after-timing-observations.json只报告时间与输入事实，不作百分比验收。volume/RSS/profile/hash独立矩阵已实际结束：driver34操作exit0、64份pass summary；完整汇总16/16cell、32plain、missing0/errors0。逐项读取/hash/RSS事实及边界见[performance-results.md](./performance-results.md)，原始/tmp/guru-589-d7-after-work-acceptance-observations-v2全部保留。

原metadata-refined candidate reapply的两份已知bak已逐份核对：备份是初轮canonical、current是收敛后canonical；保留于/tmp/guru-589-d7/candidate-refinement-known-backups及dispositions.json。原apply重新接续成功，package/overlay conflict0/sidecar0。候选安装仍不是正式Task/installed工具采用。

## 当前剩余

RDT及Architecture收敛、完整Check/commit/独立Review/晋升/PR交付未完成。正式Task及代表installed采用、新正式受影响链、最终库存与整体Completion由后继原owner承接。#575完整Release矩阵、Guru正式发布、业务仓采用未声明通过。
