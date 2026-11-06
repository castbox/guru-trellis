# 审核充分性的设计职责

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
