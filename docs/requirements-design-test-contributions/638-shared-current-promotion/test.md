# #638 实际验证结果

状态：实施中。本文是本Task唯一长期结果文档；只记录实际执行及明确未验证项，不预填正式Check、Review、晋升或安装通过。

本worker已完成来源读取、canonical合同修改及完整proposed正文准备；其确定性验证结果将在下方追加。完整拟写存在不等于shared current已写入。

待主会话汇总：production promotion/Check/RDT wrappers与实际公共phase/content_ref链、Arch/Check/RDT及直接consumer定向测试、source selector/registry一致性、dogfood/installed投影、一个matching clean安装和reapply/sidecar/mode、真实native双Task/同单元/no-change/#636/#637组合，以及本D1正式最终Check/Review/交付及整体终态。未执行者均保持未验证。完整多平台Release矩阵、Backend采用与生产部署不在本accepted scope。

## 本worker实际局部结果

- `PYTHONPATH=trellis/skills/guru-team managed-python -m runtime.validate --root . --mode source --json`：通过；实际40 active packages、124 commands、144 package tests。这里只检查source合同/库存，不证明安装或Agent行为。
- `runtime.tests.test_runtime -k production_phase2_inputs_close_schema_6`：1 test通过；Check6生产authoring payload各既有最终出口满足当前schema。
- `runtime.tests.test_qualification_eval.QualificationEvalTests.test_current_manifest_binds_real_ten_profile_matrix_without_private_artifact`：1 test通过；选定v5结构与current alias一致，旧历史manifest未改。
- `runtime.tests.test_runtime.QualificationNativeIsolationTests.test_current_delivery_publication_inputs_match_active_interface`：1 test通过。
- Architecture staging命中测试`QualificationNativeIsolationTests.test_architecture_semantic_authoring_stages_facts_without_owner_result`：1 ERROR，测试950行仍读`docs/architecture-eval/public-input.json`，当前producer写`.trellis/tasks/architecture-evidence/public-input.json`；本worker未修改该locator。B原两处已由git show确认。主会话将其判为命中adapter直接consumer的必要机械修正，现reader消费facts.public_input_locator，不再硬编码旧路径；仅重跑该项，实际1 PASS（20.844s）；这是source fixture的producer/consumer定位验证，不是实际Agent行为。最初将两个测试指定到错误class导致loader errors，改为实际class后得到上述真实结果；不是product行为失败。
- 4份本worker改动Python以AST内存解析通过，均≤3000行；21份隔离Markdown按最终target路径解析相对链接通过；`git diff --check`通过。root导航保留历史精确Git来源。

本次descriptor按40个selected Interfaces对齐input/output/private库存，包含原已有Draft/维护/终态schema差额；这是分发库存校正，不证明这些既有功能通过。未运行apply、drift、clean安装、真实Agent或GitHub写入，未产生正式Check/Review结果，未修改真实shared current。以上结果不能代替主会话后续唯一完整验证汇总。

## 主会话执行的source fixture结果

下列结果由主会话实际执行并传回，本worker只记录其对象与层次。命令均使用managed Python：`-m unittest discover -s <测试目录> -p <文件名> -v`，并在fixture关闭Git gc.auto/maintenance.auto。

| 受检对象 | 实际结果 | 环境与边界 |
| --- | --- | --- |
| runtime/delivery_projection/tests/test_fixed_candidate.py | 3 PASS，2.526s | GURU_UPSTREAM_DELIVERY_SCRIPTS指向匹配Trellis dist templates/trellis/scripts；固定candidate source fixture |
| packages/guru-create-task-commit/tests/test_early_draft.py | 2 PASS，4.365s | TRELLIS_DELIVERY_API_COMMON指向同scripts/common；早期提交source fixture |
| packages/guru-review-task-delivery/tests/test_runtime.py | 14 PASS，66.718s | 同TRELLIS_DELIVERY_API_COMMON；当前readiness source fixture |
| packages/guru-check-task/tests/test_delivery_flow.py | 16 PASS，49.749s | 同TRELLIS_DELIVERY_API_COMMON；真实公共wrapper的Check、Review、Draft、恢复和终态投影fixture |

首次后两组只有GURU_UPSTREAM_DELIVERY_SCRIPTS而缺其实际所需TRELLIS_DELIVERY_API_COMMON，2项/14项全部SKIP；补正确实际环境后全部真实执行通过。首次skip保留，不算通过。上述目录均相对trellis/skills/guru-team；这些结果不证明installed或真实AI/GitHub采用。主会话fresh读取#638仍OPEN、updatedAt=2026-10-19T16:24:34Z、无评论；这只说明本轮source authority观察。

Check整组首次观察为39 PASS / 20 SKIP。test_delivery_flow.py因缺TRELLIS_DELIVERY_API_COMMON而skip；补匹配COMMON后，该文件16项全部实际执行通过。原整组其余skip未逐项重跑，仍保持SKIP；不概称pinned-old，不将fixture结果扩大为installed或实际Agent证明。

## Package实现及独立quality结果

以下均为source层结果，使用匹配managed Python和上述fixture依赖。调用环境关闭临时仓库Git自动维护；没有修改fixture来跳过业务断言。

| 受检对象 | 实际结果及范围 |
| --- | --- |
| Architecture tests/test_promotion.py | 修正后11项全部通过，24.343s。覆盖稳定identity的leaf晋升、首次`.105`到稳定identity实际入口写入、partial/output-loss，以及promotion→原repair薄stage投影→原promotion回程 |
| Architecture独立quality补充5个contract行为 | 全部通过，11.273s；覆盖Planning双purpose、sync和repair/bootstrap身份恢复。完整contract suite未完成，不称全组通过 |
| Check新tests/test_candidate_check.py | 5项通过；真实record/check/invoke及公共phase、bytes/mode候选失配、no-change/output-loss、历史gate适用性。payload中的语义结论为fixture，不证明AI判断 |
| RDT tests/test_contract.py | 11项全部通过，9.628s；当前impact/promotion2.0、candidate_ready和原no-change投影 |
| adapters/eval/test_architecture_authoring.py与test_phase2_authoring.py命中测试 | 2项通过，52.544s。首次2项产生3个schema_mismatch errors：测试reader仍选Delivery2.0；改用当前Delivery3.0 schema后重跑，保留原断言 |
| Guru Python语法与diff | 351文件内存compile通过；本次改动代码均不超过3000行；git diff --check通过。没有单独配置的lint/type-check，不将语法检查当类型检查 |

独立quality首先实际复现final_integration的sync_required送旧repair stage被拒绝。修正采用原maintenance的phase2入口，原promotion上下文只留本轮调用，maintenance结果返回原final_integration，不生成promotion通过。另一修正使首次identity切换只有在本次完整受审baseline目标实际变化且读回后才能输出真实after identity；普通leaf无需改根入口。两项均未新增公共API字段或长期状态。原独立quality reviewer复核修正代码、sync/current/bootstrap三处路由及新增测试，确认两项finding解除，未发现新增阻塞缺口；该结论只覆盖source quality。

基线B的promotion行为断言通过，但临时.git清理报Directory not empty；另archive全字节比较差异定位为.git自动打包对象与索引，未发现业务路径变化。关闭自动维护后定向promotion测试通过；未把中断的完整suite写成通过。独立control quality机械修正一个proposed证据链接归属，未发现其它控制面阻塞项。实际shared current、matching安装、真实Agent合成和正式质量链仍未验证。

当前source validator复核通过：40 active packages、124 commands、144 package tests。Task上下文validate通过（两份15-entry manifest）；超出注入上限的规范仍需Agent自行完整读取，警告不代表已注入全文。

本轮首次dogfood drift实际退出1：0 missing、6 changed，分别是`.trellis/workflow.md`和五份workflow spec。它们尚未通过受管切换同步，故本阶段dogfood未通过；不能用source成功替代。ownership/schema与三平台入口定位子检查通过，只覆盖原安装的这些客观部分。后续须按原matching安装/Tools合同切换并重新检查，保留普通legacy-archive reapply边界。
