# 共同审核规则与阶段职责

Identity：`ARCH-REVIEW-SUFFICIENCY`；状态：`current`。

Guru 的共同审核覆盖与完成语义由 canonical `trellis/presets/guru-team/spec/workflow/review-sufficiency.md` 唯一维护，安装为 provider 的 `.trellis/spec/workflow/review-sufficiency.md`。原 reviewer 直接应用该源；其 entry、对象、独立性、顺序、通过条件、typed exits、恢复和副作用仍归原 Skill。共同规则不成为新阶段、Skill 或运行状态，也不依赖阶段私有结果或 recorder。

原 `guru-review-change/references/review-method.md` 只组合工程审核所需的专业、Architecture、RDT 和专题方法，不再读取 Check/Branch 私有阶段方法。Check/Branch 与其它适用原职责读取同一共同源，保留各自 formal 资格与结果。方法分发属于既有 managed-spec/package 机制，脚本仅执行、记录和校验确定性事实。

完整 Guru provider 与受审 target 分开。provider 提供框架方法；target 提供自己的实际 requirement、Architecture 和工程 authority。Guru 侧消费独立专业标准的证据，外部 `guru-ai-guides` 的独立调用不因本规则增加 target `.trellis/` 前置；该外部接入未在本仓库实现。

本取舍由 [ADR-REVIEW-SUFFICIENCY](../adr/review-sufficiency.md) 记录。首次独立、后继覆盖、工程事实和 formal predecessor 仍沿其原责任适用；本单元只定义 owner/依赖关系，不复制共同方法正文。实际行为、分发和安装效果由对应 RDT/Test 及真实执行证据说明，知识晋升本身不能证明这些效果。


## 正常旅程与交接的审核覆盖

原owner在既有职责及首读顺序内，从适用来源、真实入口和必要消费者推导连续操作及阶段交接问题，再对照候选论证和验证。Architecture仍先读constitution/baseline/change contract及真实设计事实，不预载PRD、验收或通过叙述。新方法不新增审核人、公共状态或跨阶段证明链。

具体正常动作发现由Clarify/Author所属合同承接；验证入口、替身语义、样本代表性及风险匹配的完整旅程顺序由quality-guidelines Test And Validation Value单写。共同review-sufficiency拥有覆盖形成与结论充分性；各原owner继续拥有自身通过、资格和恢复，不从多个Agent同意推导行为已证。
