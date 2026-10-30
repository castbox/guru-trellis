# 当前知识读写与晋升测试策略

本次 #649 最终整合的完整前驱：Git `4fea68613de4181d7cb55532b8758515472ba31b:docs/test/current/knowledge-maintenance.md`。贡献、#657 继承及原来源见 [#649 追踪](../../requirements-design-test-contributions/649-stage-result-convergence/traceability.md)。

知识单元：`RDT-TST-KNOWLEDGE`。状态：`current`。authority identity：`guru-trellis-rdt`；精确内容由包含本文的完整 Git revision 与 locator 定位。固定前驱 RDT `.109` / Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`。需求：[RDT-REQ-KNOWLEDGE](../../requirements/current/knowledge-maintenance.md)；设计：[RDT-DES-KNOWLEDGE](../../design/current/knowledge-maintenance.md)。保留 `TST-006 / SCN-006` 三层SSOT、`TST-018/023/024` 的Architecture/并行/晋升关系；当前适用性由ADR-028/034拥有，最终整合时序由ADR-KNOWLEDGE-FINAL-INTEGRATION拥有。

## T331-01..06 与稳定关系

| Test / scenario | Requirement → design | 正常输入、观察与预期 |
| --- | --- | --- |
| T331-01 / V331-A / S331-01/02 | R331-01/04 → D331-01/04 | 从正常入口查询多轮Task/Delivery和后继Architecture规则；完整定义、条件/否定/顺序/替代范围正确可追溯。不能只答摘要或沿日期取最新。历史拼接查询的三次中位文档字节与历史拼接步骤须下降。 |
| T331-02 / V331-B / S331-03/04 | R331-02 → D331-02 | 为Completion插入独立知识条目、拆出Closure不等Finish；受影响R/D/T一致，原ID/前后继/无关ID不变，判断Architecture实际影响，不改API或旧snapshot。每次正确；中位历史拼接或无关维护减少。 |
| T331-03 / V331-C / S331-05/07/08 | R331-02/05 → D331-02/04/05 | 两Task隔离delta依次受控promotion，完整current保留两增量及原全部约束；旧Task仍读B适用authority，新查询按successor。每次正确，晋升后查询的历史拼接减少；兼容子项不强求节省。 |
| T331-04 / V331-D / S331-06/09 | R331-01/03/05 → D331-01/03/05 | 实际generic source/version与project差异；只改project，另给普通source缺失/断链/迁移未完。明确owner/影响/原repair，保留旧源，不将target/inferred当current。语义等价旧新fixture、每次正确，不强求兼容收益。 |
| T331-05 / V331-E | R331-02/04/05 → D331-02/04/05 | 逐条来源迁移inventory、稳定trace、否定/例外/顺序/被替代范围、legacy区；focused tests及package/source检查、Markdown引用、历史字节核对。AI判完整性，机械命令仅其实际证据。 |
| T331-06 / V331-F | R331-04/05 → D331-05 | canonical/dogfood/installed分发、完整apply/drift；一个clean代表安装和旧匹配update/reapply。实际references可读、平台投影/modes一致、用户内容保留、sidecars逐项处置。不等完整Release矩阵或业务采用。 |

R331-06 / D331-06 是上述真实对照方法与结果责任，横切 T331-01..06。完整样本/必答事实/条件/修订范围与次数在实施前的Delivery design第8节已冻结。old/new同语义、预期、模型配置、权限及正常起点；各组各3次独立native Codex，共24次。query read-only、revision workspace-write，双方一致。测试owner的期待表不注入受测Agent，另一侧答案/历史不共享。样本/环境改变则说明原因并双方同口径重跑。

## 成本、错误与证据层次

每次保留repo外临时raw JSON events、实际命令/路径/工具输出字节、最终答案、文件改动与usage。AI逐次判断正确完整，并按navigation、必要正文、重复和无关history分类。总input包含公共注入，cached_input单列，不扣除伪造节省；注入/读取指令也算成本。读取步数和维护paths实报，首次人工迁移/导航维护成本另报，无自动生成器也不能记为零维护。

完整查询正确性先于成本；错误、省略条件或失效引用不能以低token/字节补偿。保留首次失败、修复和未覆盖范围，不以最后retry掩盖失败。legacy范围不全迁移不是当前能力完整性通过依据；若所选能力缺约束，仍须修复。

工程检查按当前package及验证作用域选择。原 `T600` before/after/promotion、`T578` 工程事实适用性和 `TST-006` 三层关系继续，但历史绿色不自动成为本候选结果。真实Agent行为与deterministic/source/installed/live证据分开；去敏两层fixture不证明外部业务采用，完整多平台Release由专门scope拥有。

## 唯一实际结果与缺口

全部24次及迁移/安装实际结果、分类/中位成本、首次失败/修复和限制只由 [#331 test.md](../../requirements-design-test-contributions/331-current-effective-knowledge/test.md) 拥有；当前正文不复制summary为第二结果authority。尚未执行项保持未验证，缺source/安装依赖时沿原repair/blocked，不能用目录/schema/链接成功宣称行为通过。

## T638：稳定身份与最终整合场景

| Test / requirement → design | 正常输入 | 必须观察 |
| --- | --- | --- |
| T638-01 / R638-01/05 → D638-01 | 两Task同B改不同能力，原promotion依次真实读写 | 双方完整正文保留；稳定authority；无总入口必写/版本递增；未命中单元和引用不变 |
| T638-02 / R638-03/04 → D638-03 | 同单元前一Task已晋升，后一Task最终合成 | 原条件/否定/例外、双方改动、关系/导航与受影响未改消费者均被覆盖，真实写入读回 |
| T638-03 / R638-02/04/06 → D638-02/03 | 原begin_check→候选Check→final integration→重新begin_check→最终Check→commit/Review | 公共phase implementing/checking/implementing/checking/reviewing；候选无final gate；实际写入后旧content_ref不能放行，新candidate覆盖全部差额；no-change无空文件/提交 |
| T638-04 / R638-05/07 → D638-04 | matching切换，未晋升/已晋升/已有Review在途，普通mismatch/partial/output-loss | 当前拒旧shape，不转换pass；同key/B恢复不重复写，旧Git引用原义保持；无第二current/长期parser |
| T638-05/06/07 / R638-06/07 → D638-05 | 命中production wrappers、一个clean matching安装/reapply/平台投影及真实native Agents，#636/#637组合 | fixture、source/dogfood/installed、Agent/GitHub分层；真实owner读取完整候选、组合与consumer，不预填pass；无Git整合可晋升 |

实际#638结果仅由 [contribution test.md](../../requirements-design-test-contributions/638-shared-current-promotion/test.md) 拥有。已有T331/T600/T578策略及其历史结果保留，但不作为当前候选已通过证据；不扩完整Release矩阵或Backend生产采用。

## T648：约束、关键前提与跨阶段真实行为

| Test / requirement → design | 原输入与执行owner | 必须观察 |
| --- | --- | --- |
| T648-01 / R648-01 → D648-01 | 原Author native入口读取完整来源条件、否定/例外、实际候选及选中scope | 自主写出具体设计落点和唯一来源处置，区分本批交付承诺与完整来源兼容约束，原wrapper调用真实；host不预写正确正文 |
| T648-02 / R648-02 → D648-02 | 原Architecture semantic_authoring：错误业务默认/未改consumer、原provider事实否定接受前提、合法例外/selector | 原条款和因果被识别；合法来源例外正确保留；当前完整trace和原wrapper不替代具体语义审核 |
| T648-03 / R648-03 → D648-03 | 原跨阶段native：已批准方案内三类冲突、真实当前公共API和原owners | 下一次受影响写入前停、返回条款/候选/影响、自主三分流；冲突解决及受影响规划/审核/候选匹配才恢复；未解决authority保留blocked |
| T648-04 / R648-04 → D648-04 | 原Check semantic_authoring与实际committed Review：设计/源码/绿测试共同错误、真实未改caller | 从有效合同指出共同错误预期及consumer影响，不弱化断言；两阶段正式结果分别发生 |
| T648-05 / R648-05 → D648-05 | 原task-free native：同域A/B缺同资格证据，以及共同错误限制A候选 | 实际A成功且不改不变量；B失败且state保持；说明不变量、最小迁移、不适用理由、阻断范围、owner/consumer；错误前置导致受影响write停下 |
| T648-06 / R648-06 → D648-06 | 同原reviewer两轮：代码/测试不变，新原证据否定关键前提；另给合法无变化事实 | 真实读取新事实并刷新命中判断，保留仍适用事实；影响不明完整评估；不按阶段/身份无因重跑 |
| T648-07 / R648-07 → D648-07 | 原package/runtime/source/installed/native入口及原最终质量链 | matching方法先before再new，同语义/模型/权限/起点；失败保留，已有能力/新增收益分开；分发、行为、安装及GitHub事实分层 |

本项每组各两次before/new，具体输入、观察与样本起点在Delivery design第8节固定；该次数是#648验证安排，不成为其他Task的普遍门槛。host期待表、另一侧答案或轨迹不进入被测上下文。AI逐次审核具体约束、因果影响、预期判断与原owner路由；仅exit、结构、trace顺序或绿色命令不能独立证明检错。普通环境/调用失败保持execution gap，不能记为语义通过或方法漏检。

完整candidate Check、原owners最终整合/读回、实际after重绑、最终Check和独立committed Review继续沿T638。工程检查覆盖命中package/runtime、canonical/dogfood/installed、声明平台、apply/reapply/drift/mode与零未处置sidecar；clean最多一个代表，不扩完整Release/多平台升级矩阵。业务实际采用与生产效果未被fixture证明。

唯一实际结果在[#648 contribution test.md](../../requirements-design-test-contributions/648-constraint-premise-review/test.md)。本单元只拥有策略、输入、owner、观察和结果定位，不复制运行结论为第二authority。#649的阶段成果/Completion组合验收与#651的reviewer载体不在本项。

## T649：当前定义、有限修正与实际晋升

**T649-07 / R649-07 → D649-06**：九个完整 proposed targets 保留原条件、身份及必要关系。限制解除后当前定义、指南及派生说明收敛；历史观察和截止点保留。#637 仅修可证过期项，原失败及未证不升级通过。候选 Check 后原 owner 真实写入读回，再以实际 after 重绑、最终 Check 和完整 committed Review。

**T649-08 / R649-01..07 → D649-01..06**：原 package/runtime、canonical/dogfood/installed、声明平台、apply/reapply/drift/mode/sidecar、一个代表 clean 及正式 Task 交付分别验证。before/new 使用相同事实、运输、模型、权限和起点，AI 逐次审真实原因、维度和 route；保留 execution_error/no-grade、有效漏检及修复，不以 exit 或绿色命令代替语义。

#648 自身完整结果与 #649 连续组合分别核对；本项不启动 #651，不改 Backend 或业务现场。普通定向验证不扩完整 Release／多平台升级矩阵。全部实际结果和 cutoff 唯一由 [#649 Test](../../requirements-design-test-contributions/649-stage-result-convergence/test.md) 拥有，本单元不复制运行结论。

## T-MECH：机制采用的原生对照

| Test / requirement → design | 相同事实与原入口 | 必须观察 |
| --- | --- | --- |
| T-MECH-01 / R-MECH-01..04 → D-MECH-01/02 | V1 Architecture：普通 opaque 分页、已有可信 token 哈希记录、reviewer 新签名提案及真实保密载荷对照 | 区分保密、完整性、范围绑定和签发证明；无缺口不加长期 key 或新会话台账；真实保密无需等待事故 |
| T-MECH-02 / R-MECH-01..04 → D-MECH-01/02 | V2 Architecture：稳定配置的独立账号争用控制记录，真正共享库存对照，首次失败和后续恢复事实 | 核最小协调对象与时间段，保留必要共享约束，首次可用性与重试恢复分开，恢复不自证机制合理 |
| T-MECH-03 / R-MECH-01/03..05 → D-MECH-01/03 | V3 Architecture：新入口采用旧 AES/协调但 Utility 无 diff、已充分论证同类消费者、受审旧条款及删后合同缺口 | 无 diff 仍核适用性，已覆盖简短承接，允许比较替代；缺证不擅删、不默认复用通过、不全局停工 |
| T-MECH-05 / R-MECH-01..06 → D-MECH-01..04 | V5 原 package/adapter tests、source/installed、apply/reapply/平台投影/drift/mode/sidecar | 公共 I/O 和原 routes 保持；一个代表安装验证实际正文可读与用户内容保留；机械结果不代替语义 |

本 Task 在固定 B 的原方法和本批新方法上，每组各一次独立 native 执行；V4 由 Completion 同名单元定义，共八次。事实、host 预期及配置在改方法前冻结，预期与另一侧答案不注入受测 Agent。AI 逐次读实际输入、输出及 wrapper stdout，再核具体语义；两侧均正确记已有能力，执行/模型失败记 execution gap，保留首次失败与修复。一次/侧只支持被观察案例，不推出统计改善、普遍模型纠偏或业务效果。

全部实际结果唯一由 [本批 test.md](../../requirements-design-test-contributions/architecture-mechanism-review/test.md) 拥有。本单元不追写自己的最终 pass；源码、分发、真实行为、业务安装采用和生产效果分开。完整 Release/多平台升级矩阵不在本项范围。
