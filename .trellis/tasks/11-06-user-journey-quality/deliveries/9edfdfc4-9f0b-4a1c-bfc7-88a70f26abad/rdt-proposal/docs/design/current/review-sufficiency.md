# 审核充分性的设计职责

导航别名：`R717/D717/T717`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/design/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

Identity：`RDT-DES-REVIEW-SUFFICIENCY`；状态：`current`。需求来源：[R717](../../requirements/current/review-sufficiency.md)。

## D717-01 / CON717-COMMON：规则与阶段的依赖方向

`trellis/presets/guru-team/spec/workflow/review-sufficiency.md` 是共同正文；原审核 Skill 是执行语义判断的 consumer。shared `guru-review-change/references/review-method.md` 只组合工程审核的专业/Architecture/RDT 方法，退出对 Check/Branch 私有阶段方法的读取。阶段保留自己的 formal entry、通过、结果、资格和副作用；共享规则不调用生命周期，也不读取阶段 private artifacts。

专题方法继续由其原 SSOT 拥有。重复共同段在同一候选内删除改引用；仍有独立阶段职责的内容保持原位。当前检查集合和迁移差额由本 Task 规划及真实验证承接，不建立长期扫描/维护列表。

## D717-02 / CON717-PROVIDER：读取和专业证据

canonical provider 的 workflow-spec root 是 `trellis/presets/guru-team/spec/workflow`，installed provider 为其 `.trellis/spec/workflow`。原入口定位当前完整 provider 后加载正文，target authority 另行读取。缺源或真实适用性缺口由原 owner 处理，不能回退到 target 中另一版本的框架副本或伪造专业覆盖。外部专业 Skill 仍独立维护；本项只实现 Guru 侧加载与证据消费。

## D717-03 / CON717-OBSERVE：行为采集与验收

现有 eval/观察能力采集真实 Agent 对同一或严格等价对象的原生产入口、工具调查、findings 和结论。具体样本和可比条件在执行前固定，期待由验收侧持有。collector 只运输输入和保留实际输出，AI 逐例判断语义；没有评分器替代充分性。后继候选沿实际会话恢复，检查完整增量与实际影响，保留仍有效覆盖。

## D717-04 / CON717-DISTRIBUTE：受管采用

沿现有 managed-spec/package/preset 机制分发；已有 checkout 使用原 tools maintenance owner 保护 Task/session 和用户内容。源、安装投影和模型行为各自提供本层证据。新配置、公共字段、兼容双读或状态协调不属于该设计。

完整架构归属由 [ARCH-REVIEW-SUFFICIENCY](../../architecture/03-domains/review-sufficiency.md) 定义；本单元不复制宪法或原 Architecture 判断方法。历史固定版本沿其原适用合同使用，不向旧 current 双写新能力。

## D-JQ-INDEPENDENCE / CON-JQ-INDEPENDENCE：原首读顺序内的问题推导

承接 BEH-JQ-INDEPENDENCE；来源为 Task `user-journey-quality` generation 0 的已接受 D1 方案及 Issue #747 说明。新增方法已落实于 canonical 共同正文，D717 的依赖方向和证据复用保持。本次 JQ 定义由该 Delivery 的实际 candidate_checked 后，原 RDT owner 在 final integration 整合并读回；当前定义由包含本文件的精确 Git revision 绑定。方法实现、有限行为观察与受管采用分别判断，最终 Check、Review、Delivery 和 Completion 仍由原 owner 的实际结果建立。

共同 review-sufficiency 的覆盖形成段补充原 reviewer 从有效 authority 独立形成问题，再对照候选论证的方法。它只拥有审核覆盖方法，不新增审核阶段，不读取另一 owner 私有结果或改变原 formal entry。Clarify/Author 继续分别拥有正常动作与阶段交接展开；Test And Validation Value 拥有验证入口、替身、样本和顺序。

原 Architecture 的 authority-first 独立评估与其它 owner 的现有首读规则优先。检查者可复用适用事实，不能继承实施者的通过叙述作为语义结论。所属正文保留必要结论，原始观察与阶段结果由原消费者承接，不另造账本。

本设计的维护成本为共同正文、真实受影响引用和定向行为观察。若新方法与原隔离顺序冲突、引入新 owner 或扩大验证义务，应返回原设计/Architecture 判断；不能增加第二审查层。Architecture 归属由 ARCH-REVIEW-SUFFICIENCY 的原 owner 在本次晋升与后续阶段判断。

关系：BEH-JQ-INDEPENDENCE → CON-JQ-INDEPENDENCE → SC-JQ-INDEPENDENCE；入口/替身证明边界仍由 D-JQ-JOURNEY 单写。


## 当前同批方法与证据差额（完整拟晋升，未生效）

适用基础为 Git `7b14b6f83f274bd3b08e2721be8624516374b73d` 的原完整单元；现有 identity、历史晋升和原观察保持。本节是 Task user-journey-quality、generation 0、同一 Delivery 的 proposed 差额，尚未共享晋升。

共同review-sufficiency的Form and cross-check coverage原段拥有条件等价及同对象连接的独立核对。reviewer先从自身适用authority形成必要条件，再与候选具体场景比较，检查结果是否被新增前置或更窄对象改变；分别存在的接口/状态不能替代consumer获得匹配内容与前提。缺读取/恢复/结果合同写清具体缺口、依赖分支和原责任，保持已确认承诺。此方法复用原读取顺序和隔离，不新增reviewer、轮次、identity/version协议或台账；canonical方法继续单写细节。
