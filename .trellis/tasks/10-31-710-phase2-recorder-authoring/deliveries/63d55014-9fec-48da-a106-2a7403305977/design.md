# D1：Phase 2 正常 authoring 设计

## 1. 设计目标、需求承接与内容基线

本设计完整承接本目录PRD的D1-R01至D1-R07、D1-S01至D1-S06及AC710-01至AC710-09。原Check AI继续九维语义审查，只author语义内容；原recorder生成结果身份，原checker和invocation消费同一完整结果。首次候选和最终native执行、finding、兼容和分发均属于本D1。

原DeliveryProjection.content_base以明确development_base计算B=2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30；这是首个Delivery，无前序。Planning观察H0=B，不约束未来实现HEAD。PR目标main与固定内容范围分开；后续candidate沿同B覆盖B..实际HEAD和完整dirty增量，不能换成移动origin/main。

独立原Architecture candidate_assessment已正式返回baseline_current、architecture_impact、target_native。适用authority为guru-trellis-architecture、guru-trellis-design-constitution-v1及guru-trellis-architecture-change-contract-v1，locator为docs/architecture/README.md、00-foundation/design-constitution.md及06-governance/change-contract.md。decision refs为ARCH-FND-002/004、ARCH-INT-016、ARCH-DOM-053和ADR-KNOWLEDGE-FINAL-INTEGRATION。该结果允许方案写作，不证明实施或native成功；Wording后仍需实际final_plan。

## 2. 当前系统、边界与目标差额

canonical为trellis/skills/guru-team/packages/guru-check-task。contract引用Recorder Authoring但没有正文；phase2-check.json是完整6.0结果。record.py已有封闭11字段语义输入，可生成五个身份字段；完整6.0分支直接采用输入。check.py读取原Task checkpoint，将task_ref、摘要、dirty覆盖不匹配合并定位artifact。invoke/delivery仍拥有真实public profiles、候选回程与最终gate。

production_fixtures.production_phase2_input已返回语义输入；delivery_production、owner_runtime及phase2_authoring.execute调原record/check/invoke。现有test_candidate_check及部分runtime/delivery测试从完整结果或内部content_identity开始，不能证明authoring。现有fixture/native通过不抵扣本轮验收。

本轮补齐原合同和语义示例，显式退出recorder完整输入并迁移本仓调用，细分原比较诊断，扩展原定向命令/native适配器及受管投影。完整6.0输出、checker/invoke结果消费、两token算法、五profiles、出口、身份与阶段顺序保持。排除#713完整生命周期、#711/#712、业务#994状态、历史Task迁移和发布矩阵。

## 3. 来源设计处置（唯一）

规范性来源为[Issue #710](https://github.com/castbox/guru-trellis/issues/710)行为要求1–5及交接/非目标。下表逐项retain；没有改变accepted scope的change/reject。PRD和implement只引用本节。

| 来源及原承诺 | 处置、设计落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| §1 原Check独占实际正文、封闭字段、参数与consumer | retain；第4/5节，原contract和最小示例 | 修原owner说明，不建新DTO/schema/wrapper；无范围变更 |
| §1 无私有摘要/HEAD/结果身份占位，AI保留完整判断 | retain；第5/6节 | 原recorder已具备能力；脚本不生成semantic pass |
| §2 三命令真实argv、载体、读取位置、回执及同一完整结果 | retain；第5节命令与V710-02 | checker无--input；receipt不能替代owner result |
| §2 Task/Delivery/Planning身份和合法上游token原样承接；五profiles保持 | retain；第5/6节 | 候选token正常存在，不禁传、不重算或误填私有字段 |
| §3 authoring/结果分开，盘点完整输入consumer，无consumer显式退出 | retain；第7节清单及MIGRATION-710 | 同步迁移本仓调用；完整输出/合法消费保持，独立Architecture已判impact |
| §3 两token职责独立，不自动刷新旧结果 | retain；第5/7节与V710-03 | 保留原freshness，不建全链digest authority |
| §4 原错误合同、字段和原owner诊断，不猜根因 | retain；第4/6节与V710-04 | 仅辅助诊断，不当根治或首次行为证明 |
| §5 语义命令测试、消费者单测证明边界、真实正文/引用检查 | retain；第8节V710-01至05 | 不以host预填私有摘要证明authoring |
| §5 正常安装native、完整合法前置、无本阶段答案及纠偏 | retain；第6节和V710-06/07 | mandatory语义前置由原owner实际完成，host只给事实/运输 |
| §5 候选→原最终整合→重绑→最终、finding及失败保留 | retain；第6节 | #710自身验收，不反向要求#713从创建跑完整链 |
| §5 分发/platform/reapply/drift/sidecar/mode | retain；第7节和V710-08 | 原安装owner，最多一个必要代表clean，不扩发布矩阵 |
| 交接：固定commit、匹配安装、profiles、命令、native定位交#713 | retain；第7节及implement Policy | #713 fresh亲自Check，不新建DTO/台账，不自动外发 |

## 4. 模块、职责与设计取舍

| 原模块／文件 | 本轮行为与边界 |
| --- | --- |
| Check SKILL.md、references/contract.md、examples、interface.json、commands.json | 实际Recorder Authoring正文及可执行配方；新增phase2-authoring.json语义示例；完整示例标明输出/消费用途。只登记实际资产和准确命令描述 |
| runtime/record.py | 既有11字段作为唯一authoring输入；生成五字段和原checkpoint；完整6.0输入按迁移退出，沿既有schema_mismatch定位input，不增compat开关 |
| runtime/check.py | 拆开已存在task_ref、reviewed_content_sha256、reviewed_paths比较；仍用stale_identity和原capture ancestry检查。恢复指向原Check fresh语义轮次，不自动重录 |
| invoke.py、delivery.py、project.py、legacy_maintenance.py | 完整结果消费/恢复、原profiles及出口保持；只有发现真实装配差额才改，不为文件数量制造diff |
| package tests、adapters/eval/phase2_authoring.py、native_adapter.py及evals | authoring从语义输入；复用原semantic_authoring和公开阶段操作扩展同fixture候选到最终，不建通用生命周期框架 |
| 原preset、guru-upgrade-tools | canonical经完整受管owner同步dogfood/installed/声明平台，保留Task/session和用户修改 |
| 原RDT/Architecture maintenance | 各自独占隔离完整拟写和最终晋升；规划不写shared current |

直接演进现有recorder可完成职责，无需新producer。只补文字并长期保留无consumer双入口会留下输入选择；统一token会改变两类consumer；新增wrapper、版本schema、长期台账均无直接consumer，因此不采用。必要测试迁移仍在本批完成，不能以最小diff省去兼容出口。

## 5. 接口与数据

语义authoring保持封闭字段：mode、reviewed_paths、validation、docs_ssot、delivery_policy、candidate_classifications、semantic_review、typed_exit、route、reason、consumer。嵌套定义由原schemas/phase2-check.schema.json单写，最小示例展开九维与空候选，仅作教学，不代表当前pass。AI按事实填写；reviewed_paths由AI完整审查决定，recorder只验证dirty覆盖。

recorder生成schema_version=6.0、skill_id=guru-check-task、task_ref、phase2_capture_commit、reviewed_content_sha256。定位来自--task，HEAD和Phase2 token由原owner从live事实生成；算法仍guru-phase2-worktree-content-2.0。public candidate的guru-reviewed-content-1.0仍由implementation/public API提供并消费，不能互换。public input里的实际Task/Delivery/Planning/candidate及profile-specific字段从真实producer原样承接。

正式配方在目标repo root执行：GURU_CHECK_PACKAGE=.trellis/guru-team/skills/packages/guru-check-task；TASK_REF来自当前public Task；PUBLIC_INPUT是合法profile JSON文件；AUTHORING是本轮11字段JSON文件。两短期文件放owner-private runtime，消费后退休，无授权信息。

```bash
"$GURU_CHECK_PACKAGE/scripts/record-phase2-check.sh" --root . --task "$TASK_REF" --input "$AUTHORING"
"$GURU_CHECK_PACKAGE/scripts/check-phase2-check.sh" --root . --task "$TASK_REF"
"$GURU_CHECK_PACKAGE/scripts/invoke.sh" --input "$PUBLIC_INPUT" --owner-result "$RECORDED_RESULT"
```

按companion-scripts的intermediate-command-stdout-1.0校验recorder回执，再取result.artifact_path为RECORDED_RESULT。该regular JSON文件才是recorder已写完整结果；不能使用含artifact_path/dry_run的stdout对象、checker状态回执或手工重组对象。checker不收--input/stdin，读同Task checkpoint；其回执artifact_path须指向同一结果。invoke按已声明argv，不猜--task；若改用--invocation -，只能提供其闭合public_input/owner_result envelope，不能混用文件参数。

只有invoke发formal exit。candidate_checked交唯一最终整合router；passed交TaskCommit；finding/planning/blocked/resolved按原interface唯一consumer。resolved profile要求的验证回执原样按字段传递，project-resolved-reconciliation仍按原独立authoring和真实Git事实处理。scope revision/withdrawal及历史maintenance不是本次authoring入口。

## 6. 状态、顺序、正常与失败流程

五profiles共用语义authoring与原客观生成能力，分别保留delivery_candidate_check、delivery_initial_check、delivery_finding_fix_rerun、delivery_planning_reentry、delivery_resolved_reconciliation的前置和出口。先完成九维、实际candidate资格、Architecture/RDT和验证判断，再record→check→invoke。真实finding不得为首次passed省略；mandatory证据缺失用原blocked/Architecture路线。

native复用inclusive integer range fixture及正常安装投影。host提供事实、代码、测试、public profile/身份和确定性环境，candidate token正常存在。Task/Delivery的起点事实由官方fixture建立；必须作语义判断的Planning adequacy/Activation、RDT和独立Architecture前置由原owners实际完成并消费公开stdout，不能用production fixture的host-authored pass替代。复用现有planning/architecture semantic_authoring运输与正式wrappers；准备缺口保存为setup gap，不能补假pass。

合法candidate准备好后，implementation以固定B构造完整candidate并begin_check进入checking，原Architecture phase2和RDT candidate/no-change真实执行。native Check自己读安装SKILL/contract/示例，首次authoring和命令取得candidate_checked；原Check合法rework回implementing。唯一router调用原Architecture/RDT final_integration，真实no-change也由原owner判断，不造空贡献。implementation以同B、实际HEAD和所有after路径重建candidate/begin_check；消费匹配最终Architecture后，native首次author最终Check取得passed。此验收无需TaskCommit、push、PR或merge。

从现有native-owner-clean、native-owner-finding和delivery-candidate-check扩展同stateful fixture案例，拟定case id为native-owner-candidate-final，在原evals/evals.json登记。host期待只保存在模型输入外；Prompt仅供当前profile/合法身份/前置事实/文件和工具，不含本阶段owner result、私有摘要、指定内部authoring选择或应选出口。adapter只执行Agent真实请求并保存原字节，不能删字段、换摘要、修参数或发送纠偏Prompt。

每阶段保存profile、candidate、前置公开事实、首次输入、argv/stdin及stdout/stderr、同结果承接和出口。使用已有repo外run-root，不新增长期状态。装配失败使该案例不满足首次正确，原失败保留；修订后新run写清来源和边界，不把重试称首次成功。真实finding仍应返回implementation_required或planning_stale并合法rework，其语义返工不算装配失败。

普通错误保留原code：schema_mismatch指出input；task_ref/摘要/路径覆盖分别指原字段；capture非祖先仍指phase2_capture_commit。摘要不同只证明当前绑定不符，不能断言算法、内容或编码原因。真实业务改变拒旧结果，fresh语义轮次后才可录新结果；metadata遵守原排除，不制造摘要循环。

## 7. 恢复、兼容、迁移与集成

trellis/presets/guru-team/MIGRATION-710.md明确完整matching source切换和retirement；package contract链接它。不猜未来release号。命令id/argv保持，退出的是record接受完整6.0输入；输出schema6、完整结果checker/invoke消费及原stale恢复保持。旧完整安装成套采用前保持原义，新安装不留双reader/compat flag，也不自动刷新旧结果。

| 当前已发现consumer族 | 实际入口与本批处置 |
| --- | --- |
| test_candidate_check、test_runtime、test_delivery_flow的record调用 | authoring测试改11字段正式示例，不填内部摘要；专门完整输入测试改验证显式退出，不能继续作为正常路径 |
| test_execution_consumption及schema/checker/invoke单测 | 真实入口是完整结果消费者，保留其构造结果及合法/拒绝/恢复验证；不宣称authoring/native |
| production_fixtures、delivery_production、owner_runtime、phase2_authoring、stage/implementation运输 | 当前production input已是语义；保留Agent原字节，只补必要引用、authoring校验和候选到最终延续 |
| test_phase2_authoring、test_stage_result_authoring、test_implementation_authoring | 已投影语义者保持，仍向record发完整结果者迁正式语义示例；mock成功仅证明运输 |
| verify_installed_closeout及preset命令注册 | 透明--input转发保持；调用说明统一语义输入，核回执和mode |
| guru-review-task-completion/tests/run_native_causal_eval.py | 原record消费模型semantic文件；核模板，含完整身份则同步改语义输入，只验证受影响装配，不重跑该Issue native矩阵 |
| legacy_maintenance/recover及已录checkpoint | 经原checker/invoke/maintenance消费已有结果，不经record重新包装；保持原schema诊断和stale，不迁历史Task |

实施前通过调用、输入模板和结果消费三类定向检索完成清单。当前未发现必须长期保留record完整输入的生产consumer；若发现不能同步迁移的真实支持consumer，在退出该输入前回原Author/Architecture修兼容方案，不能静默破坏或自行保留长期桥。既有checkpoint继续按原freshness消费，不能改其HEAD/token延续旧判断。

分发走guru-upgrade-tools完整源合同更新此checkout工具/package/Skill，保留Task/session；不因apply旧Task阻塞扩大历史迁移，不手工复制受管副本。一个确有必要的clean临时repo验证新正常安装和reapply、用户指令、Codex/Claude/Cursor投影、sidecar及mode。source、安装和native分别报告，不扩完整Release矩阵。

没有业务数据迁移或部署。安装冲突由原owner恢复同操作。#713交接在原验证结果给固定可获取commit、匹配安装、profiles、实际命令和native定位；当前无实现commit，不填虚假SHA，不外发消息，不替#713作当前Check。

## 8. 验证设计

| ID／AC | 入口、输入及必须观察 | 证明边界 |
| --- | --- | --- |
| V710-01／01、08 | contract tests核实际heading/anchor/引用、11字段示例与record相符、结果示例用途清晰 | AI另亲读可执行性，关键词不证明 |
| V710-02／02、05、08 | 安装真实record/check/invoke，五profiles合法前置、语义输入、正确同结果承接及原成功/finding/planning/blocked/resolved出口 | 命令测试，host无私有摘要，不称native |
| V710-03／06、07 | 原已录完整结果恢复；普通业务字节改变后拒旧结果；metadata更新不造循环 | 不重新record旧结论，不删合法完整消费 |
| V710-04／06、07 | 原普通locator、漏reviewed path、真实内容/历史改变；保原code且field_path准确 | 辅助诊断，不造伪造/攻击负例 |
| V710-05／05、07、08 | package消费者单测与受影响adapter tests，验证输入退役、schema/消费/恢复保持 | mock只证明运输，完整结果单测只证明自身入口 |
| V710-06／03、08 | installed native同fixture候选→原整合/no-change→重绑→最终，当前可用codex模型与CLI | 第一authoring/命令分别candidate_checked和passed；原owners真执行，无答案/纠偏；缺能力未验证 |
| V710-07／04、08 | 现有native-owner-finding真实缺陷、当前语义与合法rework | 核实际理由和implementation_required/planning_stale，不只比exit |
| V710-08／09 | source/dogfood/installed、原升级、声明平台、一个代表clean/reapply/drift/sidecar/mode | 实际受管正文/argv一致、用户内容保留，无未处置sidecar；不证明发布或业务采用 |
| V710-09／全部 | 本任务原独立Architecture/候选Check→原晋升/readback→after重绑→最终Check→独立完整committed Review | 后续正式质量链；本规划不执行，不拿eval代替 |

## 9. Canonical 引用、本轮差额与实际未决项

package contract/schema单写精确接口；本轮补正常调用、兼容退出及诊断，九维职责不变。workflow-contract的Candidate Applicability And Coverage、quality-guidelines的Test And Validation Value/Validation Scope Ownership、skill-package-contract的Public Skill I/O And Private State约束本方案。

RDT命中docs/requirements/current/knowledge-maintenance.md的R331/R638/R648/R693、docs/design/current/knowledge-maintenance.md的D638/D693、docs/test/current/knowledge-maintenance.md的T638/T693；原owner按delta_first在实施准备完整隔离拟写，只承接能力及证据边界，不复制package字段。Architecture独占输入退出/兼容、single-writer和分发关系，真实贡献为[本Task架构设计](../../architecture/phase2-authoring.md)，必要ADR为[输入退役候选](../../architecture/adr-phase2-recorder-input.md)。不预建空贡献或写共享导航。

没有未决产品或scope选择。实施需完成既定consumer核对与原native前置调度；前提冲突回Author/Architecture，不能host补pass。CLI可用不证明native；全部V710为计划，首次行为、目标安装、reapply/drift及完整发布矩阵当前未验证。
