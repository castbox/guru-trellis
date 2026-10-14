# #548 明确 Delivery 的无 context 接续

状态：task-owned candidate。preimage：current-main-0.6.17-guru.88；constitution：guru-trellis-design-constitution-v1/current；change-contract：guru-trellis-architecture-change-contract-v1 / concerns-v1。路径：target_native。ADR-024保留适用，无新ADR/GAP。

Before：C6正式无key支持explicit_task_mode；C7在已创建D1后仍要求session，Planning readers也要求session。旧完整安装不受本增量替换。
Candidate：原DeliveryProjection在官方context resolver无key且caller明确提供DeliveryKey时，读取原C4 current checkout与官方public parser/applicability/profile，投影call-local current/terminal事实。明确key不是selection store；无key query不推断。已有context仍官方current/select，无missing/stale fallback，不覆盖不同合法current。原Creation pending无key保持至匹配Author消费，由原Creation端口退休；只延长本owner原operation恢复输入的直接consumer周期。

Owner transition：官方Task/Delivery identity/store/session仍唯一；原Creation写create，Author只消费key并调用producer retirement端口；原Wording/Architecture/Approval/Activation分别保留门禁。Qualification沿原明确planning_paths，无新增DTO。当前受控样本成套重应用preset；主完整legacy安装仍待原每root迁移。

| Concern | 具体承接 |
| --- | --- |
| authority-binding | .88 / ADR-024；固定CLI/Core真实公共模块，explicit key必须是当前generation |
| constitution-binding | 唯一v1；薄读取和原owner退休避免第二selection authority与通用恢复框架 |
| boundary-and-decision | session仅有context才适用；其他stage仍由原consumer检查 |
| owner-and-single-writer | 官方公共模型，Creation原operation，Author不读private字段 |
| compatibility-and-exit | 无public I/O版本变更；无新增legacy运行reader；旧完整安装按原迁移边界保留 |
| gap-and-deviation | 既有closed GAP不重开；本次修复明确supported D1自阻塞 |
| parallel-scope | 只本任务product/contribution和受控样本；不触业务repo/其他Task资源 |
| evidence-and-freshness | 当前sample首次失败与原operation/key恢复；当前实施验证与未验证边界唯一位于RDT Test |
| review-and-promotion | fresh final-plan/Phase2/committed完整独立Review；expected-current原owner晋升，新diff再审 |

设计责任：概览由本文承接before/after和ownership；详细行为由canonical Creation/Author及其planning消费者合同拥有。证据与未验证边界唯一见 [RDT Test](../../../docs/requirements-design-test-contributions/548-creation-recovery/test.md)。原CMS恢复、完整矩阵、软件Release不由本贡献证明。

Project-check：guru-trellis-architecture-convergence:repository:1，入口为当前change-contract的AI语义协议；实际评估由独立Architecture owner，不以测试green代替责任判断。专属贡献不是当前shared authority；只在首次完整committed Review后晋升。
