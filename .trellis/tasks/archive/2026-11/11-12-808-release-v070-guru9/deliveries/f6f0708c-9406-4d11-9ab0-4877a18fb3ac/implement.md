# Sync 普通兼容实施与验证计划

## 1. 输入与引用

整体范围见[根 PRD](../../prd.md)，本批需求见[PRD](prd.md)，唯一来源设计处置见[design §3](design.md#3-来源设计处置唯一)。当前 key 为 Task808-release-v070-guru9/gen2/Delivery f6f0708c-9406-4d11-9ab0-4877a18fb3ac；固定 B 与 Planning H0 均为139626ac1e860ee67c03196ce664c4a2a7145152，PR目标main。

实施前加载 Sync完整contract的 ordinary/qualification/Interface 小节、MIGRATION-811 §2.1、MIGRATION-819公共选择器与消费者及design第4至8节，确认真实分支与原字段条件。质量方法采用 `.trellis/spec/workflow/quality-guidelines.md` 的 Test And Validation Value / Validation Scope Ownership。独立 candidate assessment 实际 no_architecture_impact，后续 final_plan/Approval/Activation 必须真实成立。

前序 gen0/D1/D2、gen1 的实际结果见本批 PRD §3；它们不是本修复的通过。当前 canonical与已安装来源存在计划差额，正式采用在后继阶段解除。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、owner与文件 | 动作、产物及完成观察 |
| --- | --- | --- |
| G2-I-01 | 原Author→Wording→独立Architecture final_plan→Approval→Activation | 完整规划及当前独立判断，展示三正文后由原Activation进入implementing |
| G2-I-02 | trellis-before-dev及当前checkout boundary；配置implement Agent | 仅改 canonical Sync runtime/invoke.py，按design §4把两项封闭校验移回原return_identity分支；不改变专用校验、字段处理或输出 |
| G2-I-03 | 同implement Agent；Sync tests/test_contract.py | 实读既有覆盖，只补裸ordinary/default及严格结构化边界的真实缺口；不给原普通fixture补版本、不复制实现、不预填输出 |
| G2-I-04 | 实现后配置check Agent；原package和必要consumer | 执行G2-V-01/02；判断断言实际到达拒绝点、Git行为与消费者，不用数量替代充分性；失败回当前owner修复 |
| G2-I-05 | 工程结果足够；原installer与source validator | 执行G2-V-03，一个临时完整分发目标检查受影响平台与managed runtime；保本checkout正式采用未完成边界 |
| G2-I-06 | 原RDT及Architecture owners；当前完整知识单元与真实after | 按§6判断差额，必要整合/readback；无差额不制造文档。整合不能自称独立pass |
| G2-I-07 | 原TaskCommit→constructor/begin_check→新独立完整committed Review | 精确提交本批源码、测试、规划和原Reactivate必要metadata。review含Architecture before/after与完整范围；零开放finding后原readiness→Publication→expected-head Merge，中文Refs #808 |
| G2-I-08 | 本批实际delivered后原Completion | 保留后继正式采用义务，additional_delivery_required→Creation→新slice Planning/Activation；不提前创建或以样本代正式采用 |

实施与check Agent职责分离，独立reviewer不参与实现。所有Agent共享checkout，必须保留他人工作。每批写入前运行原check-task-checkout-boundary。Python入口设PYTHONDONTWRITEBYTECODE=1；共享resolver串行。

## 3. 验证入口、输入与预期观察

按design G2-V-01至04执行；下列是计划入口，不是通过声明。

1. G2-V-01：使用匹配Python对 `trellis/skills/guru-team/packages/guru-sync-base/tests/test_contract.py` 执行unittest。优先现有公开invoke skipped/synced/unresolved/invalid及detached authority方法，并执行本次新增真实缺口；普通carrier/default达到原分支，字段错误/Git阻塞不变。若全文件成本适当可一次运行，不重复同样证明。
2. G2-V-02：执行Sync `test_read_baseline_chain.py` 及Discovery `tests/test_qualification_context_chain.py` 的受影响方法。先用实际文件/方法发现命令，不猜不存在入口。观察当前结构化read/确认与Issue专用返回、原schema缺字段拒绝及固定对象不变；局部fixture不证明live Issue mutation或实际Agent。
3. G2-V-03：通过原source validator验证完整源码；按原installer在一个临时目标安装本来源及Claude/Codex/Cursor声明投影，运行该目标自己的installed validator，检查受影响runtime bytes、workflow/lock、CLI、mode、provenance、sidecar与reapply。若来源dirty，明确local sample限制；正式source_locked目标采用仍由后继slice承担。不得在当前目标普通apply、手抄managed runtime或扩完整矩阵。
4. G2-V-04：原工程check、RDT/Architecture必要after完成后TaskCommit，constructor原样提供完整B..H Candidate，begin_check后一次新独立Review。原Delivery readiness对剩余采用责任和中文Refs-only payload作判断，发布后实际CI/expected-head Merge分别报告。

必要行为与受影响回归先执行，再做分发和交付；代码/局部、安装、真实Agent和远端证据分别报告。已有证据足够回答兼容原因与修复到达时，不追加旧版本回退或重复红绿。未到达行为的设施错误不算缺陷反例或通过。

## 4. 停止条件与适用回退点

当前输入、scope、机制或source lock实质变化，回最早原owner刷新相关规划/资格/架构判断。结构化合同放宽、普通字段诊断变化、真实Git行为回归或分发不完整均停止TaskCommit/发布，先修复；不把自身来源缺陷延期给采用slice。

设施反复失败时检查真实入口和依赖，选择必要设施修复或同问题的直接观察；无法证明时保留明确缺口，不放宽断言。完成必要行为、受影响回归与分发观察后停止可选实验。

当前无数据库或生产发布迁移，无新增回滚协议。源码修复用普通工作区编辑；保留无关dirty。安装临时目标失败由原installer处置，真实后继tools部分操作仅沿原同operation恢复，不重复prepare或改私有状态。历史失败candidate不可编辑或重标通过。Git/GitHub副作用仍逐次展示精确范围再由原owner执行。

## 5. Delivery Policy（唯一）

选择 **staged**。阶段1（当前切片）交付完整canonical兼容修复、必要行为回归、来源分发、知识判断及正式Refs-only交付，覆盖本批AC-01/03/05/06。进入条件为当前Planning/Activation真实成立；退出为来源无开放finding、readiness通过、原Merge actual delivered。

阶段2由原Completion识别剩余实际采用，经Creation建立独立slice并完成自己的Planning/Activation，从阶段1完整干净已交付来源执行原source_locked tools；核当前target原Task/gen/session/config及peer保留、实际runtime/provenance/CLI/lock/mode/sidecar、installed/native入口和必要文档after，再完整质量交付。未达到阶段1退出前不预建key或安装事务。

临时限制仅为当前实际安装未含本次runtime修复，原因是完整来源先交付的既有合同；解除条件是上述后继实际采用和验证，不是版本字符串一致或临时安装通过。整个Task只有全部准备业务和所有slice通过后才由原Completion判定，再Closure no_mutation、acceptance-finish Architecture、Finish/bookkeeping与Cleanup。fresh main candidate、全部Release gates、tag/smoke/正式Release、两个选定本地目标及最终#808关闭继续由Stage2发布owner承担。

## 6. Docs SSOT Plan（唯一）

选择 **no_docs_update_needed**：本批恢复Sync contract与MIGRATION-811/819已明确承诺的普通兼容，不新增要求、公共shape、selector或架构机制。命中当前单元为docs/requirements/current/qualifier-applicability.md、docs/design/current/qualifier-applicability.md、docs/test/current/qualifier-applicability.md的REQ/DES/TST-811，以及issue-content配对三单元；Architecture命中ownership/distribution和qualifier/Issue Intake领域。当前历史观察与原晋升状态保持。

真实工程事实齐全后，由原RDT maintenance owner读取完整命中单元核此判断及必要关系，直接consumer为本批独立committed Review和后继采用/Completion。原Architecture owner按既有无impact合同核after。若发现真实知识差额，回Author受影响Docs Plan并由原owners在TaskCommit前整合/readback；不直接改共享索引或制造状态提交。独立reviewer审核实际after，不用结构检查替代语义。

本PRD拥有本批需求，design拥有方案与唯一来源处置，本文件拥有执行/Policy/Docs Plan。没有task-local release notes、动态checklist、发布ledger或授权记录。
