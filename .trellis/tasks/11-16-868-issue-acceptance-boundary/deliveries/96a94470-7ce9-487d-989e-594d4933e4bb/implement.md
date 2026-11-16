# D1 实施与验证计划

## 1. 输入与引用

完整读取根PRD、同Delivery PRD与design。来源设计唯一处置见design第3节，不重复矩阵。消费实际Architecture candidate_assessment（no_architecture_impact），完成当前final_plan与Approval后才能实施。开发B固定 `b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec`；TaskKey/DeliveryKey/当前scope_ref与planning_root由原公共API核对，不从文件名猜选。

规范输入为安装的clear-technical-writing、共享planning-body、quality-guidelines Test And Validation Value／Validation Scope Ownership、review-sufficiency、current-knowledge及本层相关spec。实现修改canonical源，投影只由原安装owner生成。

## 2. 有依赖顺序的步骤与文件责任

1. **I1 共享规则：**主会话负责 `trellis/presets/guru-team/spec/workflow/quality-guidelines.md` 与 `review-sufficiency.md` 的实际差额。先读完整相关段落，集中定义验证边界、去重与复用，在原审核规范加薄引用，不复制Issue方法。
2. **I2 原内容owner：**Trellis implement worker负责canonical Clarify issue-content、Clarify/Readiness/Create Issue的必要SKILL/contract/issue-intake薄引用。保留原门禁/出口/创建器，不改生产runtime/schema。核对workflow、README与平台入口实际路由，正确既有路径复用。
3. **I3 例子与eval：**另一Trellis implement worker负责原examples/issue-content、相关evals/evals.json和files、必要既有测试fixture。复用原native runner/adapter，事实输入与独立预期隔离；如需测试装配仅登记既有确定性fixture，不创建新平台。已识别的必要测试装配文件为 adapters/eval/intake_authoring.py、eval_support.py 及对应projection/transport测试：只补当前必读公开方法及其必要依赖的固定装配/allowlist和字节观察，不新增语义判定、flow回环或runner状态。创建前修订与后续审核关键差额另由匹配原Skill真实Agent会话观察，停在外部写入前，不能用该case的出口代替完整行为。两worker不编辑对方文件，不覆盖并行改动。
4. **I4 分发与本目标采用：**主会话原tools owner从完整matching source执行preview、精确计划审查、prepare一次、invoke及原恢复，readback本checkout投影、源/安装校验、resolver/native、sidecar/drift和Task/session/peer保持；同操作重应用采用已有证据，不重置Task。
5. **I5 行为与工程核验：**执行V1/V2的真实Agent路径与独立评估，采用worker真实测试结果，运行V3–V5实际差额检查。保留首错与普通返修，不用补丁回写旧运行结果。
6. **I6 知识整合与交付：**主会话原RDT owner形成实际贡献，工程ready后final_integration整合current并readback；原Architecture按no-change当前适用路线承接。再原TaskCommit固定候选，进入一次独立committed Review及后续Delivery Review/Publish/Merge。整体Completion、Closure、Finish及Cleanup由原owner分别完成。

无临时功能限制或预留后继实现；外部业务仓采用与完整Release矩阵保持非目标。

## 3. 验证入口、输入与预期观察

V1/V2按design第8节，用既有Skill eval运行器 `trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh` 的当前public CLI，选择本次实际新增case和仓外run-root；native能力、模型与事实fixture按该机制现行合同，不改全局配置。原生Agent必须亲自判断并消费真实前序；不得把post-owner预填输入当判断证据。独立评估者读取完整候选输出、轨迹和源事实，区分写作、门禁、回程与写前动作。

V3执行：
```bash
python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p test_issue_content_distribution.py
python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p test_review_sufficiency_distribution.py
```
使用项目managed Python与所需既有测试环境；失败按实际设施/行为归因，不为通过而锁定政策措辞或修改被测Skill。

V4由原tools owner按design第7节执行本checkout匹配采用；最后运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 和目标自身installed/native入口。保留local_candidate限制，不执行完整throwaway矩阵。

V5使用原package/source与installed验证、实际受影响package测试、eval discovery、JSON/bash语法、quality-guidelines规定的内存Python语法、官方Task context validate、`git diff --check`。不因规划模板列名而对无差额资产重复测试。

## 4. 停止条件与适用回退点

来源/范围/技术承诺实质变化回Clarify及最早受影响规划；原owner、public I/O、状态或生产runtime扩张回Author/Architecture，未经实际审查不进入编辑。工具更新冲突或部分写入只由原tools owner用同一frozen plan恢复；不手改manifest或清旧checkpoint。

原生行为未覆盖、首次写入先于合规审核、后续仍引入越界重复义务，均保持AC1未通过并修复原原因；静态/分发成功不补足。设施失败先判断是否到达被测行为，选择既有可用观测或保留具体缺口，不无限扩建设施。证据覆盖当前要求后停止额外实验。

本批无数据迁移、生产部署或release操作，不新增回滚协议。仅处理本任务文件，保留其他checkout与用户并行修改。

## 5. Delivery Policy（唯一）

**full**：D1覆盖整体R1–R7、AC1/AC2，当前无后继实现或隐藏延期责任。独立可交付条件为：共享方法与原owner完整采用；真实Agent行为及写前/后续审核约束有充分证据；受管分发和本目标采用完成；必要RDT/Architecture原owner结果与固定完整候选Review成立。

此Policy不预填任何检查通过。D1合并后仍由本Task保留整体Completion及源Issue处置责任；外部仓采用、正式source lock/发布与完整矩阵不在本Task。没有消费者接入/E2E等边界外前置。

## 6. Docs SSOT Plan（唯一）

strategy=`delta_first`。原writer为 `guru-maintain-requirements-design-test-ssot`，主会话执行；直接consumer是当前内容/审核/创建owner、后续Check/Review/Completion和知识读取者。命中current issue-content三层完整单元及其R153/R818/R819/R850、D/CON、T/SC责任，新增本次精确R868/D868/T868关系，不覆盖旧来源与观察截止。

实际task-owned贡献位于 `docs/requirements-design-test-contributions/868-issue-acceptance-boundary/`，包含manifest.yaml、requirements.md、design.md、test.md、traceability.md。只写真实已变定义/关系与工程事实，不复制unchanged authority或提前声明current。工程验证后、TaskCommit前由原owner对实际current目标与固定B重读、整合、逐项readback并正式invoke；保留integrated_pending_review与独立committed Review的边界。

共用验证方法本次有跨阶段差额时，维护真实命中的现有current责任单元及其必要关系；无需改总入口/current README或全局版本。Architecture依据当前独立评估为no-impact，不制造空贡献/ADR；实际设计若变化由原owner重新判断。TaskCommit包含全部整合、源码、示例、测试和受管投影，提交后一次独立完整Review判断before/after，不追加记录自身最终pass的文档提交。
