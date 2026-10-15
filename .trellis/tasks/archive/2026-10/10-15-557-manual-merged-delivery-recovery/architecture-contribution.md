# #557：已有正式 Delivery 的手动合入事实

状态：candidate；identity：architecture-contribution-557-manual-merged-delivery-recovery-v1；change_path：target_native；expected current：current-main-0.6.17-guru.89/active。源为#557，decision为ADR-024 + ADR-026 candidate；constitution guru-trellis-design-constitution-v1与project change contract v1保持。尚未Phase2、独立committed Review或promotion。

Before：原Merge terminal recovery/message校验与history依赖Guru trailers/gate；已发布正式PR被普通用户merge后缺少这些bytes，公共Delivery不能记录真实事实。After candidate：原Merge用唯一现有public Task/Delivery/Publication relation和真实Git/GitHub归属，调用既有historical_success记录actual candidate事实，再回原Completion；versioned query2只读原owner已记录事实。原expected-head远端路径保持，schema1/2具名历史职责保持。具体step-local行为由canonical Merge/Completion合同拥有，不在本贡献复制流程。

| Concern | Applicability / 当前候选判定 |
| --- | --- |
| authority-binding | applicable：planning3/candidate与final purpose、current .89及current project合同绑定；原public API1/Task2是唯一authority。 |
| constitution-binding | applicable：current constitution；public relation替代trailers作为唯一必要身份前置，没有第二模型/ledger/授权记录。 |
| boundary-and-decision | applicable：原Merge拥有terminal归属/记录，history只读；ADR-026澄清手动事实与旧gate适用性，原Completion判断actual内容/证据及整个scope。 |
| owner-and-single-writer | applicable：公开模型/合法转换上游单写，Guru原Merge语义、原Completion/Closure/Finish各自负责；task contribution只有本Task writer，shared promotion归原Architecture owner。 |
| compatibility-and-exit | applicable：新增闭合manual profile/query2必须matching组合采用；原expected-head/schema1/2历史职责保持。旧完整安装固定原包，由原Upgrade+业务owner成套迁移后退出，绝不从旧checkpoint制造新pass。既有query1只服务原具名历史/standalone consumer，不扩成manual importer；退出归其最后真实consumer完成后的原migration owner。 |
| gap-and-deviation | applicable：收敛当前正常manual恢复缺口，不自动新增/关闭/reopen既有GAP；ARCH-GAP-006/008现有owner与closure condition保持。若实际实现新增authority/双writer/owner扩张，由原fitness_regression路由阻止。 |
| parallel-scope | applicable：本Task/isolatedcontribution/matchingtestsample允许；竞争shared current、backend#149/PR526/resources、另一Issue、上游/全局包与Release矩阵禁止。 |
| evidence-and-freshness | applicable：设计D557、before/after/actualcandidate/CI及完整publicchain；结果层级与未验证边界由本Task唯一RDT Test拥有。临时Git诊断不冒充formal/remote证据。 |
| review-and-promotion | applicable：freshfinal-plan审查realcontribution/ADR；Phase2检查before/after；首次不同reviewer完整origin/main...HEAD Review后原owner按expectedcurrent决定promotion，新diff重进原gates。 |

Task-local writer与设计责任：D557-01原Merge profile；D557-02公关系与真实immutable终态；D557-03actualcandidate/证据/原Completion；D557-04history/recovery；D557-05workflow/分发。允许的确定性事实primitive不得解析需求/判断充分性，公开结果不携带审计历史或授权。

project-check identity：guru-trellis-architecture-convergence:repository:1，entrypoint docs/architecture/06-governance/change-contract.md，result contract guru-project-architecture-check-result-2.0；规则ARCH-GOV-006..009、decisions ADR-005/009/024/026 candidate，GAP006/008保持原责任。各stage由原Architecture semantic owner亲自执行该协议、判断applicability/blocking/before-after；不把表或validator通过当semanticpass。

无原则例外、无新GAP lifecycle、无第二公共writer。promotion前本文件不作为shared current；软件四轴、Release、oldsource采用、真实业务恢复各自独立，不能由知识晋升证明。
