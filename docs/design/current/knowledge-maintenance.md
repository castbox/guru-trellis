# 当前知识单元与原维护方设计

知识单元：`RDT-DES-KNOWLEDGE`。状态：`current`。authority identity：`guru-trellis-rdt`；精确内容由包含本文的完整 Git revision 与 locator 定位。固定前驱 RDT `.109` / Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`。需求：[RDT-REQ-KNOWLEDGE](../../requirements/current/knowledge-maintenance.md)；测试：[RDT-TST-KNOWLEDGE](../../test/current/knowledge-maintenance.md)。稳定 `REQ-007 / BEH-007` 的design责任沿原RDT/Architecture owners延续。

## 稳定设计身份

`DES-007` 保留RDT/Architecture各自唯一authority与最小spec projection。`DES-026..034` 的双维合同、constitution、责任/check/contribution边界继续由Architecture正文和原package拥有；本单元迁移其日常知识读取/适用性/晋升关系，不改写项目具体架构答案。`DES-027` 的当前晋升顺序由D638/ADR-KNOWLEDGE-FINAL-INTEGRATION承接，`DES-033` 的无条件current推进stale片段按ADR-028/R567替代，其余有效条件保持。

## D331-01 / CON331-01：完整单元与薄导航

原RDT维护Skill的 `references/current-knowledge.md` 单写可复用读取/修订合同，由原package distribution安装。两维护Skill按原职责加载同一通用合同；没有新公共Skill、schema、service或parser。项目根为docs/requirements/current、docs/design/current、docs/test/current；按task-delivery-lifecycle、completion-closure、knowledge-maintenance三个capability/responsibility组织完整正文。

每层current/README仅列identity、alias、status、locator和必要关系，另定位明确legacy范围。单元标明适用版本/状态、完整定义/条件、必要关系、来源和替代范围；目录名current不具有semantic authority。共享根入口使用稳定 authority identity guru-trellis-rdt，仅在关系、身份或状态真实变化时由原promotion owner修改；普通晋升不强制全局递增或总README写入。未切换前candidate保持proposed；不能以新导航或新CURRENT自证正确。当前正文revision用包含其完整内容的Git snapshot，不另造无限版本副本。历史版本和contributions只读来源，普通当前查询不要求拼接它们。

能力正文展开完整行为、异常/否定/继承条件，细粒度公共API仍由canonical package拥有。读者按问题/阶段选单元并展开必要R/D/T/Architecture关系，不机械递归所有链接。navigation中不重复business summary，来源history也不复制成current本文的第二份规则。

## D331-02 / CON331-02：关联修订与结构身份

原task_impact_sync从批准delta及实际适用authority判断no-op、isolated contribution、窄direct sync或revision。每个Task拥有独立contribution目录，默认manifest/requirements/design/test/traceability五件套，互不竞争shared正文。写作owner在本delta准备完整目标内容，主promotion owner再在live current上合并；脚本不推断conflict或最新有效规则。

稳定REQ/BEH/DES/CON/TST/SCN/CASE身份与展示顺序分离。移动/插入保持原ID；替换/删除留旧→后继与历史；真实拆分/合并才分配新身份，并记录前驱/范围。原trace保留；新关系映射不批量重编号无关对象。维护一层时判断其它层和Architecture的真实影响，无影响据实保留，不为格式完整批量修改。

## D331-03 / CON331-03：两层Architecture来源

原Architecture owner在generic source边界维护版本固定通用栈定义，在project边界维护选择/范围/约束/差异。实际generic源为 `trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md`，项目投影为 `docs/architecture/00-foundation/stack-selection.md`。二者在Architecture正文定义适用关系，本RDT只定位，不复制技术条款或独立批准。

项目差异仅修改项目投影；共享变更由源方owner在源范围审查，不隐式升级其它项目或写入Task/branch/客户配置。外部source缺失需说明位置/version/取得方式及受影响结论；去敏fixture证明合同而非外部真实采用。FOUNDATION/CURRENT/TARGET/GAP/PLAN/ADR/EVIDENCE分区、constitution和single-writer不变。

## D331-04 / CON331-04：晋升和阶段适用性

原 RDT/Architecture semantic owners 及四 profiles 保持。RDT impact/promotion2.0、Architecture 非Planning5.0/Delivery3.0、Check private6.0 与直接 consumers 成套采用新时机；Planning3.0/Delivery1.0、bootstrap/repair 不改义。真实 API版本独立于稳定知识身份。精确 source 使用完整 Git revision/locator；局部目标内容一致性不成为 semantic approval或全链 authority。

`D638-02 / CON638-CANDIDATE`：implementation 先以固定 B、实际 HEAD 和全量 paths 调原 candidate/begin_check（implementing→checking）。独立 Architecture phase2 读 immutable before authority、完整 implementation 和 proposed targets，可返回真实 reviewed_candidate。RDT phase2 impact 的 candidate_ready 定位完整隔离贡献，no_change保持实际空影响。原 Check delivery_candidate_check 仍完整检查九维与受影响未改 consumers。通过时其原 role 以 rework(target_role=implementation, affected_results=[readiness]) 返回 implementing，不写 public Check gate，再发 candidate_checked；不清 Planning 或真实历史，不授权旧结果用于当前候选。

`D638-03 / CON638-INTEGRATION`：唯一 workflow consumer 调原两 promotion owners 的 final_integration。一次固定真实目标 branch/commit，只读写命中单元及必要关系/导航；相同单元比较适用 before、本方完整 proposed 和真实 target，保留仍有效条件与双方变化。组合改变原已审内容时按唯一 Candidate Applicability And Coverage 补独立审核全部差额、组合语义及未改消费者，前提/义务变化回最早原owner。没有真实 Git阻塞不 merge/rebase或追目标。original owners 写完整 reviewed组合并读回，不从期望 DTO 推断实际成功。

实际写入后 implementation 以同 B、实际 HEAD 和全部实际差额重新 candidate/begin_check（implementing→checking）。最终 Architecture/Check 使用新 content_ref；旧写前 candidate 不能验证 after bytes。仅最终 Check record_gate（checking→reviewing）供 TaskCommit和完整独立 committed Review消费。no_change也走合法回程，无空贡献、ADR或commit。Ready/Finish不消费候选状态。

partial/output-loss 只恢复同一可唯一 intent：completed读回、pending补写、conflict停原owner。candidate_checked 丢失时按实际 phase/写入事实回原 Check、implementation或maintenance，不从phase补造pass；同 DeliveryKey与B保持。当前语义每次新作，工程事实按R578/ADR-029及唯一候选适用合同核真实定义、依赖、环境、工具链、参数/期望后采用，缺失/未知/变化才补命中检查。无需长期 cache、账本或授权持久化。

`D638-01 / CON638-IDENTITY`：完整单元与关系保持稳定ID，authority identity= guru-trellis-rdt；普通晋升允许同 identity，只校真实目标内容。根导航只在定位/身份/状态改变时写入，不追加每Issue业务摘要。Architecture使用独立稳定 identity guru-trellis-architecture。bootstrap仍要求其真正distinct successor，历史和真实接口版本不改义。

## D331-05 / CON331-05：迁移、恢复与分发

迁移清单逐项定位B的实际predecessor条款、完整目标、继承/替代及尚未迁移范围。未review/切换前保留旧README，候选标proposed。legacy普通读取的consumer是固定旧authority的在途planning/gates，owner不再向旧current双写新能力；Task结束/合法改选/真实依赖变化后退出其旧普通读取，历史仍可追溯。普通源缺失、断链/冲突/未迁完回原repair/Clarify，不能靠推断填confirmed。晋升后correction沿原repair/新successor，不改历史快照。

canonical packages/workflow/spec/preset拥有长期内容，dogfood/installed经完整apply更新；matching update/reapply保留用户修改并逐项处置sidecar/mode/drift。命中公共I/O按MIGRATION-638显式版本化并成套直接迁移，不加长期双reader或额外installer机制。当前代表性clean与旧匹配更新不等于完整Release matrix、外部业务配置重建或业务采用。

## D331-06 / CON331-06：真实对照与结果归属

实施前冻结V331-A..D的问题、必答事实、必要条件、关联修订范围、模型/权限、3次old/new和成本判据。用真实B旧语料与actual新正文；写作实验使用同语义临时副本，双方面对相同正常起点。host期待表不注入受测Agent，另一侧答案/轨迹不预载。

脚本仅收集原生session events/命令/实际输出字节/usage/改动paths，不做semantic评分；AI逐次判完整性和成本类别。总input包含共同注入，cached单列不扣减造收益；必要正文、导航、重复和无关历史分开。读取/定位改善与维护改动均报告，失败保留首次结果及修复，同口径变更须双方重跑。兼容子项不强求节省，错误不以低成本抵消。无需新telemetry平台或长期raw traces。

唯一实际#331结果由 [contribution test.md](../../requirements-design-test-contributions/331-current-effective-knowledge/test.md) 拥有；三层当前Test单元只拥有策略/场景/预期与结果定位。migration核对/定向tests、一个代表性clean+matching update/reapply/drift证明各自层次，真实Agent证据不能由schema/目录通过代替。
