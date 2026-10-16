# ADR-029：跨 owner 工程执行事实与独立语义判断

状态：`accepted`；来源：#578 已独立完整审查的 task-owned ADR candidate。按 expected Architecture `.93` 晋升 `.94`；承接 ADR-019 与 ADR-028。

## 决策
独立 reviewer 必须自行建立当前完整候选、消费者、风险和检查集合，再核查合法可访问的原始工程执行事实。检查定义/版本、真实依赖、工具链、参数、环境和期望仍适用且结果可核查时，由当前 reviewer 解释采用理由并通过原 recorder/checker绑定当前结果；执行来源必须真实。
独立性的对象是当前语义判断，不要求重新执行每条已有工程命令。当前 project-check judgment/freshness 不由旧命令事实代替。变化、未知、缺失、新风险/新义务仍执行受影响检查。

## 责任与取舍
保留 ADR-019 的 fresh generic reviewer、读取顺序和下游 eligibility、ADR-028 的固定候选和阶段适用性、原 phase/Skill/exit/公共DTO和 private checkpoint退休。仅替代“本人执行”被解释为无条件命令重跑及 Check same-owner-only 的限制；无新authority存储、cache、ledger或审批链。
完整安装是采用边界，当前开发Task不热替换。首次独立完整 committed Review 范围为 `404d3f4d7635b19fb2c9f0d6aa642e2f1bf925b4...5ba72ba9ca40d990d8250fbc0c174475bc3d98f4`；晋升差额仍须 fresh Phase2/TaskCommit/不同 reviewer 完整 Review。实际结果由 RDT 唯一Test拥有，不因本候选文档存在声称实现或发布完成。


实际运行结果与未验证边界由[唯一 Test](../../requirements-design-test-contributions/578-cross-owner-validation-facts/test.md)单写。本 ADR 不证明软件发布或真实业务采用。
