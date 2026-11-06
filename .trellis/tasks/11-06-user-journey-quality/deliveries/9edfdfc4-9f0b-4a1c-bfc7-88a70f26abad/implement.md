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
