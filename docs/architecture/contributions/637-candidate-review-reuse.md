# #637 候选适用性架构贡献候选

状态：Planning proposed，尚未晋升。TaskId=`637-candidate-review-reuse`，generation=0，Delivery=`5499bb2d-86d7-4a5c-9747-9b06e00f4ef9`。唯一详细方案是该Task所选Delivery的design.md；必要决策候选是同目录architecture-adr.md。本文归本Task隔离所有，不是共享CURRENT。

## Authority、职责与前后变化

比较起点：Git `39169628f5f79cb48673eae96a36670e73f4dbbb:docs/architecture/`，baseline `.104`，constitution `guru-trellis-design-constitution-v1`，change-contract `guru-trellis-architecture-change-contract-v1`。Guru Planning绑定3.0/Delivery1.0；非Planning沿4.0/Delivery2.0；project descriptor1/result2.0保持。需求/行为与设计authority为当前RDT `.113`的完整生命周期单元，变更来源是Issue #637八项行为及合法证据边界。

选择 `target_native`。当前已有固定B/H、整合差额和工程事实采用，但finding修正后的distinct fresh完整重审等条款冲突。目标直接修订现有Markdown控制面，七owner共同读取workflow-contract唯一适用性定义。首次完整独立审核继续；后继用可核验原覆盖、全部实际差额和受影响依赖形成当前完整结论。没有新架构事实时不因身份或阶段重建同一评估。同合规独立reviewer可先Architecture后Branch Review，各自结果仍实际完成。

current/target owners不变：各Skill独占阶段语义，workflow只编排，原runtime只executor/validator/最小recorder，官方Trellis拥有Task/Delivery公共状态。Task writer只写本Task；RDT/Architecture各原owner单写共享晋升，平台入口不复制业务步骤。新增通用覆盖字段、reviewer状态、cache、审计链或第二store均无必要直接consumer，不采用。

## 九个required concerns

| Concern | Applicability、拟实现与边界 |
| --- | --- |
| authority-binding | applicable：上述阶段适用`.104`与原Guru/project identities，晋升另读live expected-current；无关版本不使在途候选失效。 |
| constitution-binding | applicable：current constitution v1；最小复杂度通过原结果/Git/当前正文承接，不加账本或判断脚本。其它原则按实际职责、概念与单向收敛判断，不建立第二评分表。 |
| boundary-and-decision | applicable：单一共享规则和七个原职责；ADR-019/028/029/030/033仍有效，必要ADR窄替代无因fresh重审及后继架构重建片段。 |
| owner-and-single-writer | applicable：原语义owner、官方状态owner及RDT/Architecture晋升single-writer不变；独立性是未参与当前实现的实际责任。 |
| compatibility-and-exit | applicable：直接演进受控Markdown及matching consumers；保留fresh_final_review wire但显式迁移其窄含义，无新reader/adapter。完整旧安装固定或成套升级，同key回原owner，旧结果不转换为pass。 |
| gap-and-deviation | applicable：不新建GAP或宣布关闭ARCH-GAP-006/008；修正当前重复审核偏移。首次完整覆盖、独立性和真实质量缺失仍阻塞相应门禁，closure condition是命中证据与原owner当前判断。 |
| parallel-scope | applicable：允许本Task隔离source/贡献/验证；禁止写其它Task贡献、抢写共享CURRENT/GAP或热改其它安装。shared晋升按原owner序列化。 |
| evidence-and-freshness | applicable：原公开GateResult/调用对象、精确Git和当前正文、原始工程命令结果；当前候选独立判断绑定。计划ref不证明命令。private退休后不重建或跨owner读。实际Agent/fixture/installed/remote分别报告。 |
| review-and-promotion | applicable：本贡献及ADR候选随final_plan审核；独立Phase2审完整候选/拟写targets和before authority，原owner expected-current晋升并核读回适用性；最终Check/commit/独立committed Review覆盖全部差额。 |

## 拟晋升完整职责和兼容退出

拟更新Architecture current/domain/integration/governance中原独立评估与候选复用的完整定义，保留ADR-028固定范围及ADR-030晋升顺序、ADR-033 Draft非最终结果。原finding闭合与最终完整覆盖可由同合规reviewer完成，不能把修复/旧pass投影为新通过；覆盖不足补审，影响不明完整审。Publication/Merge核自身payload/Issue/candidate/live事实并消费适用内容判断，不另重做无变化业务设计。

首次implementation_required没有passed full_review，其refs只定位；需要真实原调用/公开结果/Git/正文支持覆盖，否则补审。原GateResult shape足够，不更改public I/O。MIGRATION-637负责matching切换/旧条款退出，原owner消费退休private，开发Task不隐式热迁移。历史ADR/归档不是继续维护旧runtime的理由。

Planning不写共享目标或accepted ADR。实施阶段由原owner准备完整proposed target内容，独立Phase2前与真实candidate一并评估；此时不能预填reviewed/promoted。原评估descriptor为change-contract中的guru-trellis-architecture-convergence:repository:1，逐次判断当前适用性，不复用旧semantic pass。

实际验证仅由未来本轮唯一RDT Test维护，计划见Task implement V637-01..08。首次独立、冲突差额、共享依赖检错、private退休、命令补缺、finding闭合、同构耗时、#636组合和安装恢复均待执行。#638未来组合、外部业务采用/生产效果及完整Release矩阵未验证。
