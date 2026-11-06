# 行为测试与因果验证的测试策略

Identity：RDT-TST-BEHAVIOR-VALIDATION；别名 T735/SC735。原语义 owner：guru-maintain-requirements-design-test-ssot。来源 Issue #735，状态 current。变更起点 main@b78edbbdc32e77392bc3775366473971050ccb4b；精确当前定义由包含本文件的 Git revision 绑定。晋升依据：原 candidate_checked 后，原 RDT owner 完成 final integration 写入与读回。

## T735-01..06 / SC735-NATIVE

R735-01..03 → D735-01..03。从正常完整 Author、根因资格与实施派工入口，给事实而不注入预期答案，观察以下实际行为：明确普通功能自主选顺序；有效失败与修后证据复用并停止；新回归触达存疑先查路径再按真实缺口选择检出验证；异步未知原因进行有界诊断且准入不先要修后绿；设施失败与目标缺陷、有效预期错误测试区分；无具体缺口的固定红绿/阶段重跑被收敛而必要验收与回归保持。

host 在运行前持有事实与期待，collector 记录实际输入、工具、动作、结论及限制，AI逐例判断。无触达依据不能宣称测试有效，结构和出口不能替代语义证据。设施执行失败保留首轮事实，修设施或采用能回答同一问题的观察；受影响验收未完成不得记通过。不将本次案例转为所有任务固定次数或旧版本回退义务。

## T735-07 / SC735-DISTRIBUTE

R735-03 → D735-03。命中 package contract/runtime、source/installed/实际平台投影、tools maintenance/reapply/drift/mode 与 sidecar 分别检查。普通本项不扩完整多平台Upgrade/Release矩阵，不证明外部项目采用、统计改善或业务生产效果。

## 结果定位与关系

本批实际输入、动作、结论和证据边界唯一由 TaskId 735-behavior-causal-validation、generation0、DeliveryId 51cf3d42-d210-4938-a20a-da800f158795 的 validation 正文承担，Task 活动或归档路径由原身份解析；本单元不复制执行记录为第二结果authority，不预填最终pass或自身最终HEAD。需求R735位于 docs/requirements/current/behavior-validation-method.md，设计D735位于 docs/design/current/behavior-validation-method.md。正式 Check、Review、Delivery、Completion 仍读取原公共结果与实际 Git/PR事实。

## T-JQ-NATIVE / SC-JQ-01..04：旅程方法实际观察

承接 BEH-JQ-JOURNEY → D-JQ-JOURNEY。适用来源为 Task `user-journey-quality` generation 0、Delivery `9edfdfc4-9f0b-4a1c-bfc7-88a70f26abad` 的验证计划 V1—V4；本次 V1—V4 已取得原生 Agent 只读方法执行观察；既有 T735 结果保持其原观察范围。本次 JQ 定义由该 Delivery 的实际 candidate_checked 后，原 RDT owner 在 final integration 整合并读回；当前定义由包含本文件的精确 Git revision 绑定。方法实现、有限行为观察与受管采用分别判断，最终 Check、Review、Delivery 和 Completion 仍由原 owner 的实际结果建立。

V1 从实际原生 Agent 的 Clarify/Author 方法入口读取中性多阶段编辑事实，观察连续正常动作、实际阶段、交接缺口和真正未决产品选择。V2 从原 Phase2 派工职责读取已有可运行入口、分层测试及未执行旅程事实，观察验证顺序和直接方法/替身的证明边界。fixture 观察不冒充正式 Check。

V3 从原审核职责读取相同容器不同编码、冷缓存/解码就绪及内存同实例材料，观察其独立推导必要验证，而非预填全部格式/设备矩阵。V4 用只有 trim 字符串合同的纯函数作合法对照，观察便宜直接单测足够，不扩大为 UI/设备或固定回退。

执行前冻结中性材料，预期由独立评价者持有，不向被测 Agent 提供缺陷答案或通过叙述。使用受支持实际执行入口，保留真实输入、工具和输出。评价者比较完整语义及未证范围；执行失败保留原结果，只修真实装配错误。示例、预写转录、关键词和命令出口均不能代替行为通过，有限样本不证明业务缺陷率或成本下降。

## T-JQ-DISTRIBUTE / SC-JQ-05..06：结构与实际采用

承接 BEH-JQ-JOURNEY → D-JQ-JOURNEY。V5 复用 planning-body/review-sufficiency 分发及受影响 package 测试，核安装/reapply 后正文、引用及用户文件保持；只证明结构与分发。V6 沿原 upgrade-tools 的 local_candidate 同步本执行 checkout，检查 ownership、dogfood drift、sidecar 和原生维护 smoke；不能手改受管副本。

Task/session 和其它会话内容保持。local_candidate 不证明 formal source lock、完整 Release 矩阵或业务项目采用。本次 V5/V6 已取得定向分发、reapply、tools maintenance、ownership 和 dogfood drift 证据。V1—V6 的完整实际观察和局限由本 Delivery 的 validation/behavior-evals.md 与 validation/implementation.md 承接；后续正式质量/交付读取原公共结果，不建立第二运行账本。


## JQ 当前观察与证明边界

实际结果由 TaskId `user-journey-quality`、generation `0`、DeliveryId `9edfdfc4-9f0b-4a1c-bfc7-88a70f26abad` 的 `validation/behavior-evals.md` 与 `validation/implementation.md` 唯一承接，Task 活动或归档路径由原身份解析。V1—V4 使用完整 canonical provider 和执行前冻结的中性材料，记录实际原生 Agent 的输入、工具及输出。观察支持本组材料中的连续操作与交接推导、真实未决选择保留、局部证据范围限制及纯函数低成本对照；独立预期未提供给被测 Agent。

该执行使用原职责的方法进行只读推导，没有运行四组正式公开 owner 的完整生命周期链或 formal Check/Branch Review，也没有操作真实业务应用。不能将方法观察提升为正式门禁通过、业务验收、任意未知缺陷检出或统计收益。V5/V6 的实际定向分发/reapply 和本 checkout tools 更新支持受管正文采用；`local_candidate` 保留 `formal_fork_source_lock` 未验证，完整 Release 矩阵、业务项目采用和 QA 缺陷率改善也未验证。知识晋升本身不补足这些证据。
