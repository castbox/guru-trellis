# D1：Phase 2 authoring 实施与验证计划

## 1. 输入与引用

整体accepted scope见../../prd.md；本批全部九条AC见本目录prd.md。方案及唯一规范性来源处置见design.md第3节，完整命令/consumer/native方案见其第5–8节。B=2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30，Planning H0=B，目标main独立；无前序Delivery。TaskId=710-phase2-recorder-authoring、generation=0、D1=63d55014-9fec-48da-a106-2a7403305977保持。

独立candidate_assessment正式baseline_current，impact=architecture_impact、path=target_native；真实贡献和ADR见../../architecture/phase2-authoring.md、adr-phase2-recorder-input.md。Wording后的final_plan与Approval仍各由原owner执行，规划结果不替代Activation或实现。

实施前实际读原package contract、record/check/invoke/delivery及schemas/phase2-check.schema.json，明确11字段和五派生字段；读companion-scripts回执合同、skill-package-contract的Public Skill I/O、quality-guidelines的Test And Validation Value/Validation Scope Ownership和workflow-contract的Candidate Applicability And Coverage。RDT/Architecture维护依据design第9节各完整单元及项目change-contract，不复制第二接口。官方workflow/marketplace规范本轮已读，后续真实变化才补受影响核对。

## 2. 有依赖顺序的步骤与文件责任

| 步骤／前置 | 原owner与文件 | 可审核产物及完成观察 |
| --- | --- | --- |
| P710-01；规划接受及Activation后 | implementation；guru-check-task现有runtime/tests、adapters/eval、verify_installed_closeout、run_native_causal_eval | 按design第7节逐调用核输入/输出/恢复；在MIGRATION-710.md写真实consumer和明确退役。遇不能同步迁移consumer先回Author/Architecture |
| P710-02；P01兼容路径一致 | 原Check package；SKILL.md、references/contract.md、examples/phase2-authoring.json、完整结果示例、interface.json/commands.json、runtime/record.py/check.py | 可执行唯一authoring正文、真实argv和receipt→artifact_path承接；record退役完整输入；原检查细分字段，code/两token/完整消费保持。invoke/delivery只改实际差额 |
| P710-03；P02能力可运行 | 原package tests/test_contract.py、test_candidate_check.py、test_runtime.py、test_delivery_flow.py及真实消费测试 | 五profiles语义命令链；真实业务stale/metadata连续性/结果恢复/诊断；完整消费者单测仍保留，不用内部摘要声称authoring |
| P710-04；P02/03真实命令可用 | 原eval owner；adapters/eval/phase2_authoring.py、native_adapter.py、test_phase2_authoring.py、evals/evals.json及必要stage transport tests | 同fixture候选→原owners final integration→重绑→最终的原native运输；Planning/Architecture/RDT必需语义前置实际完成。增加native-owner-candidate-final；保留native-owner-finding，不造通用链框架 |
| P710-05；canonical与adapter完成 | 原guru-upgrade-tools及preset owner；完整匹配源及受管投影 | 更新本专用checkout工具/Skill，保留Task/session和用户指令；一个代表clean安装/reapply/平台/drift/mode/sidecar。不能手工覆盖运行副本或借旧Task阻塞迁历史 |
| P710-06；实际安装具备合法native起点 | 原native语义owners与现有eval runner | V06和V07原始输入/命令/结果，外部预期不入模型；先前失败保留，缺能力未验证，不靠补pass取得起点 |
| P710-07；实现和行为证据齐备 | 原RDT task_impact_sync和Architecture；本方隔离贡献及完整proposed targets | delta_first写R/D/T完整定义和trace，Architecture贡献/必要ADR及目标原文完整；candidate前不得写shared current。测试结果只写原验证位置 |
| P710-08；前述完整候选 | 原implementation、独立Architecture、Check、两maintenance owners | 同B candidate/begin_check→独立phase2及完整候选Check→原final_integration/readback→actual after重绑→最终Check。后续commit/Review/PR/merge均另守原权限 |

本D1不延期native、迁移或分发到下一Delivery。新范围/机制超出上表先停受影响写入，走原资格/Architecture/Author。没有业务数据或部署步骤；不修改业务#994及其它Issue状态。

## 3. 验证入口、输入与预期观察

下列命令是实施后的执行计划，当前没有测试通过声明。使用目标安装记录的Python和原wrapper，先核命令帮助及依赖；schema/package pass、原生行为和安装采用分别报告。

```bash
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-check-task/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/adapters/eval -p 'test_phase2_authoring.py'
python3 -m unittest discover -s trellis/skills/guru-team/adapters/eval -p 'test_implementation_authoring.py'
python3 -m unittest discover -s trellis/skills/guru-team/adapters/eval -p 'test_stage_result_authoring.py'
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

package suite对应V710-01至05，检查真实record/check/invoke和结果恢复，不为源文件变更重复无关矩阵。adapter三组只跑被改动职责，若未命中implementation/stage运输则保留原可核验事实并说明适用性，不无因全跑。必要PYTHONPATH/runner差异以原tests说明为准，不能direct import私有runtime来替代正式命令测试。V710-02各profile正式public前置通过原fixture/owners建立；期望及层次见design第8节。

V710-06使用原eval CLI及实施登记的新case。RUN_ROOT是repo外临时绝对目录，每次run独立；CODEX_MODEL在执行时从当前CLI支持能力选择并记录准确值，不沿用过期eval配置。指定模型、权限、实际安装source和正常public起点后执行：

```bash
.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-check-task --adapter codex --codex-model "$CODEX_MODEL" --case native-owner-candidate-final --run-root "$RUN_ROOT"
.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-check-task --adapter codex --codex-model "$CODEX_MODEL" --case native-owner-finding --run-root "$FINDING_RUN_ROOT"
```

CLI需支持原参数且新case已登记后才执行。V06从完整合法candidate前置开始，同fixture两次Check之间必须保存原final integration/no-change、rebind/begin_check公开结果；模型外验收分别比较candidate_checked/passed，AI再读首次输入、真实命令及理由。V07核真实finding和合法原owner回程。若需要独立semantic grading，按原--semantic-grading入口消费已完成run，不重跑模型掩盖首次失败。setup失败、装配失败、模型/执行能力缺失如实保留为不同证据缺口。

V710-08先由guru-upgrade-tools原完整合同更新本checkout；dry-run/变更清单、执行、恢复均归原owner。确需clean证明时，使用唯一代表性临时repo从同canonical source安装完整workflow/preset，再同源reapply；具体临时路径、source revision和受管差额在操作前展示。核Codex/Claude/Cursor声明投影、可执行mode、用户指令保留、.new/.bak逐项owner处置及零未处置sidecar。普通apply current-only前置不满足就回工具owner，不迁旧Task。未执行完整Release/多平台升级矩阵，不能宣称通过。

V710-09是本Task后续正式质量链；eval样本和规划不是其证据。#713采用所需固定commit、安装来源、profiles、命令及run-root定位在原Test结果给出；可核验工程事实按适用性复用，#713仍亲自做当前Check。

## 4. 停止条件与适用回退点

身份/选择/checkout错配回原Identity/Ensure/Bind/Selection，不新建Task或覆盖其它选择。每批写前跑check-task-checkout-boundary.sh。scope/source变化回Clarify；方案前提或兼容consumer变化回Author/Architecture；已批准实现/断言错误留implementation/Check。真实问题先走normal/solution/root资格，不能因severity扩大范围。

原命令报错保留首个stdout/stderr及code；依赖/模型/mandatory语义前置缺失停止该验证并报告未验证。native装配失败不得删记录、发纠偏Prompt或将重试称首次。真实语义finding走原rework，不视为输入失败；业务变化不自动刷新旧结果。

受管安装发生冲突沿原tools/preset恢复同操作，保留用户修改与Task/session。共享promotion仅原owner在candidate Check后读live expected-current、真实写入和readback；冲突停原owner。没有DB/部署回滚。未授权不stage/commit/push/PR；任何merge另停待协调者处置。保留并行资源和无关dirty，不自动清理。

## 5. Delivery Policy（唯一）

policy=full。本批task_scope与delivery_slice同为D1-R01至D1-R07和AC710-01至AC710-09，remaining_work为空表示没有延期分配，不表示已完成。独立可交付条件为：唯一正常authoring和真实命令可用；完整结果消费者和迁移出口明确；真实stale/metadata与五profiles保持；首次candidate/final native及finding真实满足；canonical/dogfood/installed及定向分发验证完成；本任务原完整质量链完成。验证边界为V710-01至09，完整发布矩阵和业务采用不在范围。

不得把native或分发交给#713完成本D1。native能力缺失只阻塞相应AC，不删要求或改partial。#713拥有从本项固定可获取候选及匹配安装开始的完整跨步骤链，自行执行其当前Check。Task Completion独立核全部accepted scope及真实Delivery，合并不等于完成；交接不新增DTO、长期台账或外发消息。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。唯一RDT writer为guru-maintain-requirements-design-test-ssot，真实差额为原正常Check authoring/结果消费边界、兼容退出、候选/最终native验证层次。命中RDT三层knowledge-maintenance完整单元，稳定关系沿R331/R638/R648/R693及D/T对应单元；精确字段/argv仍由Check package单写，不复制成第二接口。实施时由原writer建立docs/requirements-design-test-contributions/710-phase2-recorder-authoring/的实际manifest、requirements、design、test、traceability及完整proposed目标；不在规划造空五件套。

Architecture writer为guru-maintain-architecture-baseline，Planning的真实task-owned材料见../../architecture/。实施时在本方隔离贡献补齐完整拟写ownership/distribution和必要ADR目标；基线identity保持，导航仅真正定位/关系变化才写。原ADR记录输入退出的理由/替代/兼容边界；不将source或CLI可用写成native成功。

直接consumer是原独立Architecture/候选Check、final-integration owners、after重绑/最终Check和完整Review。完整isolated proposed先进入candidate检查；仅原owners在final_integration晋升并读回，之后全部实际after进入重绑与最终Check，不能用一次文档commit补完质量链之后的缺口。历史失败、Issue现场及旧版本观察保持原义；当前指南退出过期双authoring指令。实际结果在原Test贡献唯一记录，#713只引用固定来源和证据，不另立结果台账。
