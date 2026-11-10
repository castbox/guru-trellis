# 用户旅程与交接验证方法实施与验证计划

## 1. 输入与引用

整体root PRD及本批prd.md拥有JQ-R1至R6/AC1至8，design第3节是唯一来源设计处置。实际加载Clarify Questions And Convergence、Author planning-body及模板、quality-guidelines Test And Validation Value、review-sufficiency和原架构/分发约束。来源及原子所有权不变。

## 2. 有依赖顺序的步骤与文件责任

1. 原RDT/Architecture owner准备design第9节隔离完整拟写，保共享current不变。
2. trellis-implement负责Clarify/Author合同、quality-guidelines、review-sufficiency、必要模板/workflow引用及去敏例子；不改runtime、公共schema、上游agent/hook或其他Task。
3. 先用中性材料执行V1/V2最小完整方法观察，发现路径不通先修该真实缺口；再执行V3/V4独立边界，不先铺大参数矩阵。
4. 独立trellis-check按当前原范围读取实际diff和V1-V4原始输出并判断，不预置成功答案；保留失败及未证范围。
5. 原upgrade-tools同步本checkout受管dogfood，运行V5/V6；原candidate Check及独立Architecture后，由原RDT/Architecture final integration晋升，重新绑定真实after并完成最终检查。提交发布不在本次授权中。

## 3. 验证入口、输入与预期观察

V1-V4按design第8节，使用已可用codex exec --ephemeral CLI，在独立外部fixture目录读取当前完整provider或原职责的read-only证据入口，采集实际输入/输出/工具。沿#735既有collector模式，固定输入后评价者独立判断，不把关键词或出口当语义pass。简单纯函数对照验证不泛化；不承诺统计收益。

V5使用现有test_planning_body_distribution.py与test_review_sufficiency_distribution.py以及受影响Clarify/Author package contract测试。V6运行check-upstream-ownership和check-dogfood-overlay-drift及工具维护原生smoke。精确argv按现有受支持--help确定；命令成功只证明其声明边界。整体候选继续按原Check语义判断。

## 4. 停止条件与适用回退点

需求/范围变化回原Clarify；机制或基线真实冲突回原Architecture；provider不完整、工具维护冲突或实际Agent不可执行时停止依赖验收并继续独立工作，不改runtime绕过。测试设施故障与产品行为失败分开，不放宽断言。已有证据充分后停止当前实验，阶段/worker变化不重跑仍适用覆盖。

仅本地可逆文本及受管投影，无生产数据迁移或部署回滚。保其他会话和Task内容，工具维护恢复沿原事务；不reset、不清理他人资源。

## 5. Delivery Policy（唯一）

full。Task scope与Delivery slice均为JQ-R1至R6。remaining_work为空；不表示当前已完成。独立交付条件为方法正文和必要消费者一致、真实Agent观察与定向分发验证充分、共享知识由原owner合法整合。validation boundaries为V1-V6及实际受影响回归，不包含全平台Release/业务采用或真实缺陷率统计。整体Completion仍由Task原owner判断，不从Delivery合入推定。

## 6. Docs SSOT Plan（唯一）

delta_first。RDT writer准备并在final integration整合docs/requirements/current/behavior-validation-method.md、docs/design/current/behavior-validation-method.md、docs/test/current/behavior-validation-method.md和实际命中的review-sufficiency单元；不为填充复制所有层。Architecture writer维护docs/architecture/03-domains/review-sufficiency.md的职责定义，无新ADR。隔离候选位于本planning_root的rdt-proposal与architecture-proposal；shared目标写入前重读expected-current。直接consumer为后续原规划/实施/检查和本Task最终Check，不更新根导航或全局版本。


## 本轮同批执行与验证差额

### 执行顺序与责任

本轮以 design 的“本轮同批修订”为当前差额；此前步骤和结果保留其历史身份。先经本轮 Author、Wording、独立 Architecture final_plan、Approval 与正式 Activation；之后实施 owner 才修改 design 列明的三个 canonical 文件。没有新的用户范围选择，也不重建 Task/Delivery。

实施后经原 upgrade-tools 同步受管投影。先执行 E2 当前 H 基线，再以正式激活后实际修订候选冻结运行；同一域、事实和标准保持，评价者独立持有标准。不因看到输出不理想而改事实、标准或旧结果。E1 已运行及盲评，结果无单向优胜，不为改出单向结论而重跑。原 V1—V6 仍适用的证据复用；只运行三个方法文件与生成投影真正影响的分发/package 检查及必要行为验证。

### 本轮验证入口与停止条件

E1/E2 沿受支持 codex exec --ephemeral 原生执行入口，在仓库外 fixture 采集真实输入、读取轨迹、分阶段产物与输出。E1 对照只改变材料加载方式；E2 比较当前 H 与修订候选，按 design 的行为标准评价。fixture 不调用伪造正式门禁。缺 API 合同保持依赖缺口，真实产品问题只阻塞依赖分支；独立明确的普通最终结果仍须进入计划与验证。

本轮 validation/behavior-evals.md 和 validation/implementation.md 在实际结果产生后由原执行/检查职责承接。未执行、失败和证据不足逐项保留。现有证据足以回答对应实验问题后停止；没有新证据缺口不追加轮次。原 A/B 与 E1 无单向改善应如实披露，不以字数、词法命中或 gate 命令成功代替语义结论。

### Delivery Policy 与 Docs SSOT Plan 的当前差额

第5节 full Policy 保持：本轮修订与验证是同一完整 slice 的未完成责任，不产生新 partial/staged 交付。当前仍待正式激活、实施、候选行为观察与受影响验证，不能用历史结果覆盖这些差额。

第6节 delta_first 和原 writer 保持。RDT owner 在现有 docs/requirements/current/behavior-validation-method.md、docs/design/current/behavior-validation-method.md、docs/test/current/behavior-validation-method.md 的 JQ 单元维护最终结果反推、原承诺保全、分支依赖和当前真实验证限制。旧 V1—V4 已晋升观察原样保留；新 E1/E2 只增加当前实际差额及限制，未发生结果不写成事实。原 A/B 结论由 validation 正文承接，不复制到 SSOT 成本或逐轮日志。

Architecture owner 核对 docs/architecture/03-domains/review-sufficiency.md 的当前职责和关系；当前 candidate_assessment 无架构影响，无须新增 ADR 或职责。如 final_plan 仍确认无差额，则记录该依据，不为形成文档改动制造贡献。涉及 review-sufficiency 的 RDT 单元同样只维护真实命中差额。隔离 proposal 与实际共享 current 比较后，由原 RDT/Architecture final integration 在原合法阶段整合，保留历史结果和其它会话改动。
