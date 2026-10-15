# #557：手动合并的正式 Delivery 恢复设计

状态：Phase 1 solution candidate；候选 Architecture 为 architecture_impact / target_native，当前 Architecture .89 与 ADR-024 保持；尚无 final_plan、Approval、实现或晋升结论。

## D557-01 原 owner 与公共入口

保留 guru-merge-task-delivery 作为唯一合入结果语义 owner。新增独立闭合 profile delivery_merged_recovery，输入仅 profile/mode/task_ref/delivery_key/repo_ref/pr_number。task_ref 是 locator，delivery_key 是公开稳定身份，repo/PR 定位已发生外部事实；不要求旧 Merge gate、旧 Publication DTO、expected-head receipt、授权或消息模板。

恢复只接受真实 MERGED。OPEN/CLOSED-unmerged 返回原 merge_blocked，并给准确原因；不进入 merge executor。delivered 复用现有最小 TaskRef+TaskKey 输出与唯一 Completion consumer。不新增 Skill、外部出口、公共模型或永久 ledger。

语义 review 与该 profile 的 objective validator 各有闭合合同。AI 审查公开身份/唯一Publication关联、真实终态、actual candidate影响、真实验证状态和Completion责任；局部 recorder/validator 只在这些判断之后校验实际身份/内容并调用公共记录。不将原“合并前所有checks通过”的review-schema用于已发生事实，不追建gate或授权。当前会话真实判断与最小public fact足以承接；恢复不生成tracked review artifact。

## D557-02 唯一归属与真实 Git/GitHub

通过安装目标的公共 DeliveryProjection/API1读取选定Task2 record与DeliveryKey，校验TaskId/generation/Delivery关系和pull_request profile。对该Task当前公开Deliveries的Publication事实检查 repo/PR/target唯一关联；明确选择与事实冲突仍阻止记录。必须有该Delivery的精确existing PublicationFact；没有它不创建或导入Delivery。

用authenticated repo-bound gh读取该PR的实际repository/base/head/mergedAt/merge SHA/CI和reviews，再读取immutable merge commit/two parents及target base ref。原branch被删除不要求branch ref仍存在；Task当前HEAD不作historical terminal identity。
commit.sha等于PR实际merge SHA。
parent2等于PR实际head；parent1从实际commit读，不重构合并前expected-base。
merge commit在当前target base上的ancestor/first-parent身份可由真实Git或GitHub compare核验；base推进不要求HEAD恰等于merge。

本版明确支持普通two-parent merge commit，包含用户GitHub UI merge和gh --merge；这是当前Guru同源可验证合并方式。squash/rebase/无两父身份返回unsupported_manual_merge_method；不改写历史补父链，不自动fallback。Guru新远端merge继续保留原expected-head、中文精确message/schema2 trailers路径。

缺public relation、multi-association、repo/base/head/merge/ancestry普通mismatch或缺必需provider字段留在原Merge并说明原owner下一步；不按title/branch/worktree或单trailer归属。provider读失败保留原适用错误事实，不用MCP/浏览器fallback。

## D557-03 真实 candidate、差额和验证

PublicationFact绑定原published candidate与原reviewed head；actual merged head来自真实PR/parent2。头、内容或scope不同不抹去可靠归属。原Merge先比较原published候选与actual head的完整Git/PR差额及当前accepted authority，AI判定same-content/equivalent证据是否仍适用，并定位差额触及的Planning、Implementation、Check、Review或scope owner。

DeliveryFact记录actual head与其candidate：沿原published candidate.paths读取actual immutable commit的bytes/modes/删除状态，形成普通temporary file snapshot并调用安装目标的公开candidate_content_ref；head_ref绑定actual SHA。完整PR差额和原publication→actual-head compare是独立证据，不能因为candidate.paths相同而忽略范围外新增/变化。snapshot是调用内scratch，消费后删除，不是workspace或业务authority。

字段reviewed_head沿上游现有Fact wire合同绑定actual candidate head；历史事实里的该字段不授予该head任何Check/Review pass。原Publication、Planning/Check/Review/readiness事实保留原身份，不改造旧pass、candidate或scope来迎合实际合入。public historical_success=true按原API记录DeliveryFact；candidate/authority差额由后续owner明确比较，不能仅从原d.candidate的gate-applicability断言actual merge仍已审。

CI全绿、pending、cancelled/missing、failed都保留读取时的真实状态。可靠MERGED恢复不要求重跑CI或current readiness。checks空集表示missing，不是green；failure不转success。PR/merge与可用check运行身份通过最小evidence locator承接，当前call-local观察交原Completion且由其fresh reread；只有真正不可重新推导且Completion直接需要的证据才进入既有evidence渠道，不另建CI ledger或完整扫描缓存。

原Completion读取实际DeliveryFact、原Publication、适用门禁、actual PR/CI、current accepted scope和scope-required证据：无需影响的同内容结果复用；必要证据不足evidence_pending，实际剩余工作remaining_work/适用implementation_revision_required，authority改变requirements_revision_required；completed只由其整体判断产生。需要新业务修复时沿原meaningful Delivery/rework职责，不为补记录/补证据造空Delivery。原Closure/Finish职责不变。

## D557-04 输出丢失与 history

调用原public record_delivery(historical_success=true)，result_id沿原immutable merge结果命名。已有相同DeliveryFact时只校验并返回同一delivered；成功记录后输出丢失或正常projection返回丢失，重入读取同PR/merge/Key的exact fact，不再次merge或换result。不同fact不覆盖既有成功记录。archived/旧generation读取遵守上游能力边界；已存在exact fact可只读恢复，缺fact走原prospective migration前置，不能reopen/私写aggregate制造成功。

discover-task-deliveries新增明确versioned query2.0，携带既有task_identity/repo_ref/base_ref及task_ref。通过公开Task2 parser读该Task已存在的terminal pull_request DeliveryFact，验证stable TaskId、generation、repo/base和真实PR/head/merge/two parents/base ancestry，按target-base实际顺序返回。该入口只读，不写任何关联，不为扫描到的PR创建Delivery。

既有query1.0保持原trailer-only历史读取与其具名legacy/migration/standalone消费者；schema1/2合法trailers和Guruexpected-head恢复保持。query2.0融合已公开记录的manual事实与合法trailer事实，按PR/merge/Delivery去重并校验一致性，普通mismatch阻止假归属；bookkeeping无public DeliveryFact且无Delivery trailers，始终排除。Completion本身已从公共aggregate读取全部facts，不靠Git消息重新发现后才能完成。

MIGRATION-557定义新增profile/query2.0的最低matching package/consumer/workflow组合；新入口无旧query/旧private checkpoint fallback。旧完整安装继续固定原整套版本，业务采用须原Upgrade/业务owner独立执行。query1的原支持边界不扩为任意historical importer，新manual事实的history consumer必须显式迁到query2。公开输出、TaskKey与Delivery API1不变，不悄改query1含义。

## D557-05 流程和投影

canonical workflow的Manual Git/GitHub Operations保留独立手动动作与真实residue报告。已发布的正式Delivery在真实MERGED、无当前formal merge result时，按明确public Key/Publication relation进入原Merge新profile；不先机械重跑pre-mergeCheck/Review/readiness。跨回合/newchat实际public当前selection或显式Task/Delivery定位仍须由原identity/checkout/session owners核验，不从inventory选替代Task。

success→原Task-wide Completion；missing relation/mismatch→原Merge stop；未合并不执行远端动作。原Guru正常Publish→Merge链不改行为。仅有task/evidence-only/recovery不创建Delivery。

所有step-local正向行为、semantic judgment和script边界仅由原canonical Skill定义；workflow只编排、消费typed exits与fail-closed。同步对应canonical spec/README/interface/commands/schema/examples、声明平台discovery投影。源旧dogfood作为本Task完整工程载体，不单拷新公共writer：按普通apply/drift真实记录模型迁移前置；matching clean样本完整apply/reapply，检查bytes/modes与sidecars/drift。不能将旧source拒绝当作current安装PASS，也不能用旧snapshot冒充新公开链。

## 来源规范承诺唯一处置

| Source locator / commitment | Disposition / landing / rationale / impact |
| --- | --- |
| #557 当前合同定位、目标与范围：原Merge+公开稳定关系+真实Git/GitHub | retain，D557-01/02；不新增import owner、Skill、ledger或第二authority。 |
| #557 合并事实与验证责任：已发生事实无需重建旧授权/gate/receipt；所有CI状态真实；不自动完成Task | retain，D557-01/03；保留原Completion/Closure/Finish与独立证据职责。 |
| #557 覆盖正常场景：base推进、branch删除、跨回合、输出丢失、same-content复用、changed head/content/authority影响 | retain，D557-02/03/04/05；旧pass不追认，新事实不消失。 |
| #557 验收1/9：正式公开全链、代表性installed与真实provider/Git，非validator单测 | retain，implement验证方案；fixture/static与实际provider证据分列，缺项不close。 |
| #557 验收2/6：缺关联/歧义/mismatch、稳定history、bookkeeping排除 | retain，D557-02/04；只读原owner公开事实，无任意import。 |
| #557 验收7/8：不重写/重复merge/空Delivery/改identity，原expected-head/schema1/schema2/正常恢复保持，API明确版本 | retain，D557-01/02/04；新增闭合profile/query2，原query1具名职责保持，不混旧checkpoint。 |
| #557 范围：具体GitHub合并方式由Planning确定 | retain，D557-02选择普通two-parent；squash/rebase明确未支持，不声称全部GitHub方法。 |
| #557 独立范围与关联：只#557，backend#149/PR526/owners禁止操作，非Release矩阵 | retain，PRD精确边界与implement；不移交业务责任、不发消息、不创建另一Issue。 |

未change/reject任何source需求。source只给机制owner/证据/兼容约束，未预设字段、新Skill或通用importer；本设计将其落实为原owner的bounded public profile。新事实所需schema字段均有原Mergevalidator或直接Completion/history consumer，不设reserved/未来字段。

## Architecture contract

target_native；task-owned contribution为.trellis/tasks/10-15-557-manual-merged-delivery-recovery/architecture-contribution.md，identity architecture-contribution-557-manual-merged-delivery-recovery-v1；formal Architecture输出绑定该实际文件内容。必要ADR candidate为docs/architecture/adr/026-manual-merged-delivery-recovery.md。当前shared .89不在Planning改写或晋升；九concern/before-after、GAP责任与project-check由该contribution拥有。首次独立完整Review后，原promotion owner才将已审贡献承接到durable docs/architecture/contributions/557-manual-merged-delivery-recovery.md。RDT的唯一delta_first contribution/trace/Test按implement由原RDTowner写作、调和、在首次独立完整Review后决定promotion，新diff重进原gates。
