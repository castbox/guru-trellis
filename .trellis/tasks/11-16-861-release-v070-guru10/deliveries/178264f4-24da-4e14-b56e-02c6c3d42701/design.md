# 发布消费者与当前输入清单修复设计

## 1. 设计目标、需求承接与内容基线

承接本批PRD D-R1–D-R6、S1–S7、D-AC1–D-AC7与整体R5/R8–R11、AC6–AC9。当前切片交付完整source及直接consumer修复；真实准备checkout采用是同Task的有序后继，不作为本source可交付的循环前置。

固定development baseline B为 `b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec`，来自同Delivery原constructor的explicit development-base；Planning H0也是该commit。保同一Task/gen1/Delivery与已有增量。原TaskCommit后constructor重新取得完整B..H；PR目标main独立于固定B。Stage2的最终发布候选由全部准备与簿记收尾后的最新main取得。

Architecture authority为 `docs/architecture/README.md` / `guru-trellis-architecture`，constitution为 `docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1`，change-contract为 `docs/architecture/06-governance/change-contract.md`。本轮原独立candidate_assessment实际返回baseline_current/no_architecture_impact：修复既有current合同清单及验证职责，采用分层不变，不需contribution或ADR。该结论不替代完整方案的final_plan。

## 2. 当前系统、边界与目标差额

| 模块 | 已有能力与偏离 | 本批目标差额 |
| --- | --- | --- |
| `test_apply_guru_team_trellis_preset.py` | 真实安装/manifest tests仍要求退役Wording，写死旧schema，未处理conversation输出 | 迁移必要退役consumer，从当前声明取得schema，保exact清单比较且排除不贡献JSON的conversation合同 |
| `verify_trellis_compatibility_matrix.py`及其test | AGENTS旧suffix猜测不能证明原位替换，source equality可掩盖目标漂移 | 首次preset前的真实hash绑定bytes→原renderer精确after；全调用链传递，无新持久状态 |
| `verify_native_platform_load.py`及其test | 每root要求所有active包，误要求不适用平台包 | selected descriptors/supported_platforms求每root expected及union count |
| `trellis/guru-team-extension.json` | current public_input_schema_ids多11项旧独立登记；当前typed outputs已一致 | 只收敛current input登记，保历史schema与被current引用的分支 |
| preset公开说明 | 需说明本次current登记纠正与已有迁移关系 | 新 `trellis/presets/guru-team/MIGRATION-861.md`，在同目录README迁移说明段加入导航 |

本批source共上述八个文件：五个verifier/test，加canonical manifest、MIGRATION-861和preset README。新迁移说明供完整source/仓库读者查阅，不加入MANAGED_SOURCE_PATHS，不新增受管文件或runtime wrapper。manifest被真实installer复制到installed extension的extension/public_api，构成实际分发差额；不能沿用旧“无需实际采用”的结论。

不改生产installer、AGENTS renderer、registry/platform descriptors、runtime selector、历史schema、source lock、CLI、现有Skill I/O或旧provider。gen0 PR #865/#866/#867只作已交付起点，不重复实现。

## 3. 来源设计处置（唯一）

| 来源/条款 | 原承诺 | 处置与落点 | 理由、影响及上游处理 |
| --- | --- | --- | --- |
| 私有release合同Stage1/Complete Source Before Actual Adoption | 完整source先独立交付；干净delivered源才能source_locked | retain；第6–7节及implement Policy | 当前source切片可独立验证；后继实际采用不可省略或提前创建 |
| 私有release合同Stage2/Historical-Task Preflight | 新main精确候选；self-reapply保真实guard及限定替代证据 | retain；第8节及后继 | 本批focused仅工程事实，不是最终候选或主目录采用 |
| installer spec Managed Assets/AGENTS | 原位替换受管块，块外bytes保持；Core hash绑定原模板，Guru不拥有整份AGENTS | retain；4.2 | 实际preimage+原renderer证明合法差额，不改hash或新增snapshot |
| installer spec Platform Overlay Selection及D724-01/03 | exact selection/supported_platforms决定各root投影 | retain；4.3 | 修消费者，不改平台能力、不恢复旧Codex根 |
| data-contracts Public Skill I/O Current Fields | active current JSON input/output exact；instruction-only无JSON贡献 | retain；4.1/4.4 | 纠正错误独立登记；测试不以subset或硬编码排除清单放宽 |
| MIGRATION-812 | qualifier七类Delivery输入2.0/aggregate3.0；旧schema原字节历史验证，旧在途完整provider恢复 | retain；4.4/7 | Root旧登记退出current，历史资产及非Delivery inputs保持 |
| MIGRATION-813 | Create Task profile/aggregate2.0及共享Creation3.0；历史固定provider恢复 | retain；4.4/7 | 只纠正两个旧current登记，不重新创建Task或转换旧成功 |
| MIGRATION-819 | Sync scalar入口/call-local3.0仍引用2.0原分支 | retain；4.4/7 | 退出2.0旧独立登记不等于取消该当前引用，不删schema/分支 |
| Task R6/R7及reference_only来源 | 完整交付、whole Completion/Closure/Finish；正式发布另有边界 | retain；6–8 | 保Refs-only及#861开放，无其他Issue状态依赖 |

没有change/reject规范性来源设计，不新增兼容例外、双读、第二writer或状态账本。

## 4. 模块、职责与设计取舍

### 4.1 Installer测试消费者

在原两真实installer tests迁移Wording wrappers/artifact/commands/schema要求，检查实际目标文件、manifest及inventory缺席，不仅比较常量。删除仍调用已退役 `wording_change_request_source` 的孤立测试，不恢复其生产helper。保留真实用户修改保护用例。

原manifest test中的可变schema版本改从当前owner声明读取：phase2 schema用其实际 `$id`，current输入/输出由active Interface独立遍历。structured_json收集aggregate/profiles；scalar_cli不贡献JSON input；Interface1.9 conversation无JSON input/output，不能把每个conversation output当作schema-bearing输出。输出收集区分合同类型，保所有结构化输出的exact集合与重复登记检查，不改成subset。已由完整Interface集合比较覆盖的旧版本固定单项断言退出，历史文件/具体支持行为不由这些常量决定。

### 4.2 AGENTS精确变换

`_run_cell` 与 `run_focused` 在init完成、首次preset前读实际目标AGENTS bytes，并核SHA256等于目标Core `.template-hashes.json` 的AGENTS行；缺失/不匹配按原MatrixError停止。沿 `_assert_template_hashes`、`validate_cell` 与focused两次update/reapply传同一调用期bytes。

实际AGENTS只能仍匹配原hash，或完整bytes等于原 `render_agents_ai_first_principles(preimage)`。不从source仓库用户AGENTS推断前像；删除suffix猜测及AGENTS source-equality fallback。保块外prefix/suffix、原hash bytes、追加/幂等及未知正常编辑失败。其他文件既有hash规则不变；不持久化preimage、改hash或新建renderer。

### 4.3 Native每root平台集合

对每个实际root，用原descriptor求selected flags中哪些声明该root。registry包supported_platforms包含shared，或与该root flags相交，才纳入expected。实际与expected比较保持missing、unexpected public projection及package-private tests检查。skill_count使用适用集合union；OpenCode后继catalog继续取经parity验证的原生root，不退回全active。合法fixture明确shared/Codex-only，测试三平台包含/排除及真实missing/extra，不mock被修判定。

### 4.4 Current input登记及必要兼容说明

canonical manifest是该字段唯一生产者；installer复制它，原manifest test和matrix `capability_projection`/`installed_capability_projection`读取实际声明。先对active Interface的current structured inputs独立求集合，核仅下表11项多登记、无缺项；typed outputs保持原exact集合。只移除旧独立登记，不对所有旧schema做按版本号清理。

| 退出current独立登记的schema id | 当前入口及保留用途 |
| --- | --- |
| `guru-create-task-input-delivery-1.0` | 当前aggregate `guru-create-task-input-delivery-2.0`；旧schema保历史验证/完整原provider恢复 |
| `guru-create-task-input-delivery-task-creation-1.0` | 当前profile `guru-create-task-input-delivery-task-creation-2.0`；旧schema同上 |
| `guru-root-cause-input-aggregate-2.0` | 当前aggregate `guru-root-cause-input-aggregate-3.0`；旧schema保MIGRATION-812历史用途 |
| `guru-root-cause-input-author-candidate-set-1.0` | 同profile当前2.0；旧schema历史用途 |
| `guru-root-cause-input-base-impact-candidate-set-1.0` | 同profile当前2.0；旧schema历史用途 |
| `guru-root-cause-input-branch-review-candidate-set-1.0` | 同profile当前2.0；旧schema历史用途 |
| `guru-root-cause-input-implementation-discovery-1.0` | 同profile当前2.0；旧schema历史用途 |
| `guru-root-cause-input-phase2-candidate-set-1.0` | 同profile当前2.0；旧schema历史用途 |
| `guru-root-cause-input-planning-scenario-set-1.0` | 同profile当前2.0；旧schema历史用途 |
| `guru-root-cause-input-publication-candidate-set-1.0` | 同profile当前2.0；旧schema历史用途 |
| `guru-stage0-sync-base-input-current-2.0` | Interface当前scalar_cli，call-local选择3.0；**3.0仍引用2.0原普通/资格确认分支，必须保留** |

MIGRATION-861明确上述三类来源，链接MIGRATION-812/813/819，区分current caller重新装配、已完成事实和原旧provider在途恢复。它说明本次登记纠正，没有新decoder/compatibility parser，也不承诺“旧schema无人消费”。README只导航唯一完整说明，不复制支持规则。

## 5. 接口与数据

没有新增public字段、schema/id、Skill/typed exit、runtime selector、数据库或持久协议。既有manifest字段的值纠正为实际current集合；它是公开声明差额，须明确说明和完整matching源采用。AGENTS preimage只在原Python调用期流向hash helper。native/matrix原CLI与结果外形不变。所有touched非生成代码≤3000行；若逼近阈值先按原职责评估机械拆分，不借本批扩张重构。

## 6. 状态、顺序、正常与失败流程

1. 同key原Clarify/Author接受root范围后，由实施owner合法rework到planning；本轮candidate、solution、final_plan、Approval和当前计划展示/接受依次完成，再由原Activation写公共Planning。
2. 原三项增量与新增manifest/consumer/说明一起实施；先完整核实际source集合和producer/consumer，再按implement验证。范围外旧断言原失败保留，不因模块红自动改生产或弱化测试。
3. 原RDT/Architecture owners处理必要整合/readback；本地TaskCommit后constructor/begin_check，再由一个新的独立完整Check/Branch Review审固定B..H及知识before/after。readiness/Publish/Ready仍由原owner与各自边界执行；Merge是独立后续动作。
4. 当前source实际delivered后，原Completion将未实施采用路由additional_delivery_required；原Creation才建立后继采用Delivery。它从该完整干净源source_locked更新准备checkout，并取得完整existing。
5. 全Task责任完成后才Completion/no_mutation Closure/Finish；Stage2从最新main重冻结，另外执行发布/主目录收尾。

缺失/过期/来源不符/sidecar或原必需验证失败保留真实错误，回最早原owner。未提交源不能formal source_locked；不能改成local_candidate宣称采用，不能提前安装主目录或修改被冻结旧候选。

## 7. 恢复、兼容、迁移与集成

同Delivery返工保Task/gen1、固定B、真实已完成事实和已有增量。旧schema文件及current引用分支字节不变；旧provider恢复只按MIGRATION-812/813/819，不把旧input塞进新runtime，不改Task身份或模拟pass。

manifest改变后原准备checkout的installed provenance/清单保持历史采用事实，不能手改以消除差额。当前source可先在throwaway证明完整安装；原tools在干净已交付源可用后正式采用并处理冲突。真实采用失败回原同操作resume/rollback，不用普通apply绕过历史Task guard。没有业务数据迁移或新rollback协议。

## 8. 验证设计

| 验证 | 对应 | 层级、实际入口与独立观察 |
| --- | --- | --- |
| V1 | D-R1/D-R5/D-AC1/6 | 原两真实installer tests与Phase0 owner-binding必要consumer；installed current input/output对active Interface exact，conversation不贡献JSON；核旧登记不在current而原schema/引用/selector不变 |
| V2 | D-R2/D-AC2–3 | 原AGENTS/hash回归及调用链tests：合法旧块替换/追加/幂等、块外bytes、原hash、late capture拒绝、source equality单独不能放行、未知正常编辑失败 |
| V3 | D-R3/D-AC4 | 完整native module：mixed shared/Codex-only、三选择各root、真实missing/extra/private tests |
| V4 | D-R4/D-AC5–6 | 采用原三平台focused在verifier/平台行为上的未变覆盖；新manifest后用一个新的Codex focused证明实际after clean/two update/reapply及installed current清单。对原Claude/Cursor目标用当前源正常reapply，完整核所有selected bytes/modes/current manifest/lock/workflow和零sidecar。旧结果不冒充新分发证明 |
| V5 | D-R6/whole AC3/7/9 | 后继采用Delivery使用当前source实际合main的干净C，原source_locked与真实 `.9→.10` existing完整链；未实施采用不能用evidence_pending代替业务工作 |
| V6 | R5 | source package/installed targets、ownership、dogfood drift、in-memory compile、diff-check、全量sidecar/residue；repair checkout尚待实际采用的manifest差额如实区分 |

V1–V3采用仍适用的原回归事实；只为被本轮改动影响的观察补测。原完整受影响模块结果保留，范围外固定计数/旧文本断言不改为pass。达到本批合同足够覆盖后停止可选实验，不重复惯例旧版红绿/回滚。公开版本、CLI/source lock不变；临时安装不证明实际Agent或最终Release门禁。

## 9. Canonical 引用、本轮差额与实际未决项

原R724/R630完整RDT单元、data-contracts current清单规则及MIGRATION-812/813/819已有合同承接本差额；不新增产品能力或知识语义。原RDT owner在实施后复核真实差额，必要完整target整合/readback后同次提交；无差额不建空contribution。Architecture no-impact在本轮candidate成立，完整final_plan仍必须独立执行。

没有未决需求或技术选择。source交付、后继实际采用、完整existing及whole Completion边界已明确；尚未执行的门禁和业务工作不能预填通过。当前计划不分配后继Delivery，也不把其他Issue加入依赖。
