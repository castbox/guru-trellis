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

## H 候选的真实分发与样本进展

早期提交 H=`ea8fb296a87e554b9dd6e92004e354cd777f508c` 已通过原 TaskCommit/Publication 发布到 Draft PR [#646](https://github.com/castbox/guru-trellis/pull/646)。本次 live 读回仍为 OPEN/Draft、base=main、head=H；Ubuntu、macOS、Windows 三项 targeted CI 均 SUCCESS。它们只覆盖 H，不覆盖下方未提交修复，不证明最终 Check/Review 或整项完成。

本轮已从匹配 Fork commit `7f050fa11ddd8569e5db4f728ea1b745b7500a98` 完成 frozen-lockfile 安装和正常构建；CLI/Core 均为 `0.7.0-castbox.5`。原 `validate_fork_source` 通过，212 份模板得到核对，锁定来源的 CI `39215935088` 为 SUCCESS。该精确构建的 formal source-lock 缺口已补齐；不改写早期 PR 发布时仍未验证的事实，也不据此声称完整 Release 矩阵通过。

单个代表样本由该 Fork 的正式 bin launcher 原生 init Codex，并从 GitHub 精确 H 安装 Guru workflow，再以干净 H source 完整 apply。实际 installed validator 通过，workflow 与 H canonical 字节一致，零 `.new/.bak`。后续复用这个安装创建 linked worktree，没有新增第二个 clean-install 矩阵样本。

V638-07 查询 A 已经原 Sync→Discovery→Clarify→Wording→Readiness→Task 创建→Author 整体 PRD→Clarify accept_scope→Delivery 创建与选择。原 Sync 最初因无 origin blocked；配置真实 repository 和实际验证分支后，local/remote/decision 三方均为样本 B=`f18737f5c6cb2cfc8f37761f8e97154703e06878`。没有用 source main 或虚构 GitHub identity 代替样本 base。

在 Task `v638-query-a` / generation 0 / Delivery `94337b7b-6cfd-4367-9200-423eed7cdff2` 的 Planning 稳定边界执行完整 reapply。首次默认 PATH Python 3.15 在依赖安装阶段返回 `dependency_install_failed`，15 个保留文件未变；该失败不计通过。改用初次安装的 Python 3.12 后 apply 成功。默认平台参数曾展开三平台，随后通过原 installer 显式 `--platform codex` 收敛；最终 Task/workspace/session/用户配置共15个快照文件、Git-common/checkout Python pointers 和 HEAD 均保持，零 sidecars，installed 验证通过。父会话的 current 查询没有样本绑定，未将其当作 selection 丢失；原 actor 会话实际读回相同 Task/Delivery、scope/planning_root 和 Planning 阶段，四个 gate 仍 missing。

查询 A 的首次独立 Planning Architecture 调用曾因新 reviewer 会话未绑定/未选择该 Delivery 返回 `stale_identity(delivery_key)`。沿原 EnsureCheckout、Bind 和既有 Delivery 显式 selection 恢复后，新语义轮正式返回 `baseline_current/candidate_assessment`。这不证明完整 V638-07：不同能力双 Task、同单元双 Task、no-change、最终合成/实际写入及完整消费者质量链仍待完成。

## 在途 local-clone receipt 的定向修复

实际 execution checkout 的原 tools preview 首先在写前返回 `Missing legacy Guru source provenance`。原 installer 会原样记录本地 clone origin；该旧目录已删除，而 receipt 的 exact commit `fd16444370c3eceed68c02dc1fc344114bc2ae7e` 仍可从明确选定的完整 source 读取。修复沿原 installation owner 与共享 callers 承接，不改 receipt，不用 H 代替旧来源。原独立 Architecture、Author、Wording、Approval/Activation 已完成受影响规划返工；它们不作为实现或安装通过的替代证据。

| 受检对象 / 原入口 | 实际结果与限制 |
| --- | --- |
| installation `test_local_source_receipt.py` | 4 PASS，1.138s。真实 installer provenance producer、Git clone/object 和原 reader；验证旧目录删除后精确旧 bytes、浅 clone 缺失 old object、clean metadata mismatch、dirty per-path。后续 HEAD/tag 不能替代旧 preimage |
| installation `test_dirty_source_provenance.py` / `test_contract.py` | 分别 3 PASS（0.474s）、34 PASS（17.081s）；保留原 dirty/GitHub/metadata/hash/preimage 与恢复职责 |
| tools `test_recovery.py` | 4 PASS，0.026s；原恢复 preimage、后续工作和 public rollback 边界 |
| 原 source reader 对实际 #638 receipt 的只读调用 | `old_manifest(root, selected_source)` 与 `old_paths` 通过；9870 managed hashes、0 unknown preimage，receipt 字节未变。只证明原 reader，不冒称完整 tools preview/prepare/install |
| 独立定向 source quality | 重读新增机制、所有 root/workspace/begin callers 与测试，无新缺陷候选；另实际执行 11 项定向用例通过。不是正式 Phase 2 或完整 B..H Review |
| source validator、语法与上下文 | 原 source wrapper PASS：40 packages、124 commands、151 package tests；349 份 Guru Python 内存 compile 通过，改动代码均低于3000行。两份19-entry context 经原 task.py validate 通过；注入截断/代码路径警告仍需 Agent 手动读取 |

`test_delivery_upgrade.py` 的20项因缺 `GURU_UPSTREAM_DELIVERY_CLI` / `GURU_UPSTREAM_LEGACY_CLI` 全部 SKIP；`test_native_install.py` 的1项因未提供 original-writer legacy fixture 与 matching maintenance pair SKIP。没有把 exit 0 的 SKIP 当通过，也没有伪造对应环境。实际 #638 完整 tools preview/prepare/install/recovery 尚未执行，dogfood 原受管切换、最终候选/晋升/质量链和终态仍未完成。完整 Release 矩阵和生产采用边界保持。

## 精确候选 2c772b5 的实际 tools 升级与恢复

本地来源修复已形成提交 `2c772b515ae7aca51b2338848d6fee8b2763c422`，经原 Publication 返回 `draft_published` 并更新同一 Draft PR #646。live 读回 HEAD、中文标题及正文均精确匹配；新 run `39379714642` 的 Ubuntu、macOS、Windows targeted CI 全部 SUCCESS。它们覆盖该提交，不覆盖下方安装产生的未提交 dogfood 投影，也不代表最终质量门禁。

原 canonical `guru-upgrade-tools` 从完整精确 source 执行 `source_locked` preview，9870 个旧受管文件均有已知 preimage；公共 tools 为208 unchanged、1项可选用户 config 冲突，后者显式 preserve。原 prepare 冻结 SDK 操作 `aa2a7a6c-af67-4c44-bb1f-b3a649694062`；其212个公共 action 只有 workflow 存在 bytes/mode 差额，provider 绑定精确2c772b5。原 installer 完成三平台的成套安装，未局部热拷贝 runtime，也未手改 receipt 或 checkpoint。

原 invoke 实际返回 `tools_upgraded`、`installed_version=0.7.0-guru.5`、`unverified=[]`，recovery_ref 为 `cccb50bc-8447-4d4e-a74c-606ac9adcf6f`。该结果表示已使用匹配 Fork 与 Guru 精确来源，不表示完整 Release 矩阵通过。随后用同一 recovery_ref 执行原 `resume`，返回完全相同的正式结果；前后 HEAD 和完整 Git status 相同。这里验证的是已完成操作的结果恢复，未模拟中途 crash 或证明所有故障分支。

- 原 owner 执行目标自己的 Python resolver、installed validator、native continuation 和隔离内存中的公共 operation probe，全部通过；主会话再从目标 resolver 调用实际 native context/continuation 和公共 Delivery current，均成功。
- 当前 chat 仍绑定原 Task/generation0 与 D1；原 EnsureCheckout 返回 `checkout_resolved`，唯一 checkout 未变。Delivery 仍 `implementing`，Planning `planning-accepted:9d8efec4-205f-4103-b351-5e8b3467cc67` applicable，Check/full_review/readiness 仍 missing；没有把安装写成质量通过。
- 396个实际 Git status 路径均属于冻结写入集合，Task、docs 和 canonical trellis 当时无差额。三个 peer/common pointer 的 bytes/mode 与 prepare 前相同，零 `.new/.bak`，两个用户配置保持原处置。receipt 由原 installer 生成，精确 commit 为2c772b5；由于同 checkout 的安装投影已有变更，诚实记录 `tree_state=dirty`。
- 原 `check-dogfood-overlay-drift.sh` exit0：workflow、selected native/shared platform projections 和 spec copies 与 canonical 一致。此前0 missing/6 changed的门禁在本次真实受管切换后已解除；没有执行历史受阻的全量 legacy-archive apply，也不将其改写为本轮通过。

这次 tools 维护未创建提交或修改 PR，未写 shared current，未转换/完成 Task。21项专用 fixture SKIP 仍保留；真实样本全组、主 Task 最终候选/晋升/Check/Review/readiness、交付和整体终态仍待完成。主执行 checkout 的 dogfood 投影与本文新增结果尚待后续正式质量链及独立提交。
