# 用户旅程与交接验证方法设计

## 1. 设计目标、需求承接与内容基线

承接JQ-R1至R6、JQ-S1至S5及AC1至8。D1覆盖整体方法能力，无前序Delivery。development baseline B为main@3a4b65ab08cdfe05d97f68e7f2e7512254d728f1，源为原Sync固定基线；Planning H0同B，不冒称最终实现HEAD；未来PR目标main，本轮不发布。

独立Architecture候选实际返回baseline_current / architecture_impact / target_native，基线guru-trellis-architecture、constitution guru-trellis-design-constitution-v1。decision_refs为ARCH-REVIEW-SUFFICIENCY、ARCH-DOM-041/055、ARCH-INT-058/059。按该结论在现有review-sufficiency单元准备局部贡献，无新ADR或根登记；正式final_plan另核实际正文。

## 2. 当前系统、边界与目标差额

Clarify已有具体例子与歧义分类，Author已有场景和状态展开，quality-guidelines已有测试触达与替身边界，review-sufficiency已有完整覆盖、终止及证据复用。本批把这些原则转为正常连续操作的具体方法，不新增审查阶段。首次D1，无前序已交付结果。#734/#736预算/并发/流程减负不实施，#735/#717现有约束保留。

## 3. 来源设计处置（唯一）

| 来源与原承诺 | 处置及落点 | 理由与影响 |
| --- | --- | --- |
| JQ-R1/2：原owner内展开旅程与交接 | retain，第4/6节 | 无新范围writer，不要求产品提供事务实现 |
| JQ-R3/4：风险匹配顺序和有效证据 | retain，第4/8节 | 不固定测试先后，不把简单任务升为设备验收 |
| JQ-R5：原首读顺序内独立推导 | retain，第4/6节 | 原Architecture隔离保持，不增加审核人 |
| JQ-R6：所属正文与最小结果 | retain，第7/9节 | 不新建场景库或状态账本 |

## 4. 模块、职责与设计取舍

- Clarify contract的Discover the actual choices补连续正常动作推导：阶段、等待期间再次动作、完成/失败/放弃结果；真实歧义仍确认。
- Author planning-body第3节补本任务实际阶段和交接条件，原requirements/design/implement分别拥有行为、机制、顺序；不复制测试标准。
- quality-guidelines的Behavior, evidence and experiment selection内新增一组方法：按风险和依赖先取最小完整旅程反馈；实际入口证明相应行为；替身保留其边界内必要语义；样本对应实际接受范围及交付组件。不另增测试gate。
- review-sufficiency的Form and cross-check coverage补原owner独立问题推导；读取顺序与隔离优先，不改变架构规则。
- delivery-implement模板和Phase2已有验证选择段仅引用共同方法，不复制正文。Approval/Check已有引用可直接承接，仅在发现实际消费缺口时调整必要句子。
- 在Author已有examples下提供去敏过程例子，覆盖交接、输入手势、异步任务、媒体样本及简单API裁剪。实际行为collector复用既有#735 native执行模式，只采输入、工具及输出，原审核owner独立评价，不自动判语义。

选择直接增强原正文，避免新Skill、新统一表格或每项测试理由文件。新例子仅教学，不作为当前用户回答或验收结果。

## 5. 接口与数据

公共profile/DTO/schema/typed exit和Task/Delivery状态均不变。原profile→现有方法正文→原出口/consumer保持。collector只在外部临时目录记录本次真实输入与结果，不保存授权或引入长期运行协议。没有业务存储/API变化。

## 6. 状态、顺序、正常与失败流程

既有Clarify→Author→Architecture→Wording→Approval/Activation→Implement/Check顺序不变。模型在各原职责内先核有效来源和真实入口，再推导连续操作/交接问题，对照候选和验证证据。真实未决产品选择回原Clarify；实现细节由Author/Architecture处理。入口具备运行条件后优先完整正常旅程；高风险下层规则先定向验证，外部依赖缺失只阻塞相应声明。

不变量示例：已被表单或编辑稿引用的源必须持续可用；局部确认不能代替最终保存；异步任务变更持有者不能丢失结果。只对本任务实际需要的条件作判断，不引入压力并发、锁或异常crash协议。例子不是新增业务要求。

## 7. 恢复、兼容、迁移与集成

无公共数据迁移或双读兼容。文本变更沿现有package/spec受管分发；通过原guru-upgrade-tools local_candidate同步本执行checkout dogfood，保Task/session及用户内容。未知冲突走原owner，不手改副本、不更新业务仓库。source_locked发布和完整多平台矩阵不在本批。

复用#735/#717仍适用的合同与分发测试；新增规则不得使已有测试先行、模块证据、实际缺口披露或停止规则失效。规范未安装不宣称采用。shared RDT/Architecture只在原candidate_checked后的final integration晋升，计划及候选不抢写共享正文。

## 8. 验证设计

| ID | 覆盖与入口 | 输入及预期观察 | 边界 |
| --- | --- | --- | --- |
| V1 | AC1/2，实际原生Agent按Clarify/Author方法读取中性fixture | 普通多阶段编辑事实；输出实际阶段、连续动作及交接缺口，真实未决选择保留 | 不提供缺陷答案，不以预写转录代输出 |
| V2 | AC3/4，原Phase2派工职责的原生Agent | 已存在入口、分层测试与未执行旅程事实；优先足够旅程并限制直接方法/替身证据 | 不调用正式Check冒充当前fixture门禁 |
| V3 | AC5/6，原审核职责按当前方法读fixture | 容器相同编码不同、冷缓存/解码就绪和内存同实例事实；独立推导必要验证 | 不把全部格式或设备矩阵列为默认义务 |
| V4 | AC3/6，简单纯函数对照 | 仅trim字符串的明确合同；采用便宜直接单测，不追加UI/设备或固定回退 | 用于检查规则没有过度扩张 |
| V5 | AC7，现有planning-body/review-sufficiency分发测试及相关package测试 | 实际安装/reapply后正文/引用可读，用户文件保持 | 只证明分发与结构 |
| V6 | AC7，原upgrade-tools与dogfood drift/ownership检查 | 实际受管after与canonical一致，无无关Task/session变化或未处理sidecar | local_candidate不证明发布锁或业务采用 |

V1-V4材料在执行前冻结，独立评价者拥有预期，不由实施者修改预期来使输出通过。执行失败保留原结果；只修真实装配错误。样本不是完整统计试验，不推断QA缺陷率或成本下降。

## 9. Canonical 引用、本轮差额与实际未决项

RDT在本Task的rdt-proposal下准备behavior-validation-method与review-sufficiency实际命中单元的完整after，原RDT owner于final integration整合。Architecture在architecture-proposal下准备docs/architecture/03-domains/review-sufficiency.md完整after，保ARCH-REVIEW-SUFFICIENCY身份与原关系，无新ADR或总索引。共享定义仍由canonical方法正文单写，长文档只解释职责和对应测试。

对应Evolution EVO-001需求忠实、EVO-002架构治理、EVO-003跨层一致性及EVO-004低开销执行，保持原目标及非目标。当前没有必要产品未决项；实际Agent、CLI/Core工具维护能力与目标分发的执行结果仍待发生。
