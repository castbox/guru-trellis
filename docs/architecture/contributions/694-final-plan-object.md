# #694：独立 final_plan 的评审对象与执行选择

Task `694-architecture-final-plan-object` / generation `0`，Delivery `0982ab15-61b8-41d3-9639-85049e61719e`。来源为[live #694](https://github.com/castbox/guru-trellis/issues/694)。本贡献供本批final_plan、完整候选Architecture/Check、原final_integration及committed Review消费；当前为完整实施与拟写候选，不是shared-current或最终交付事实。

## 适用权威与实际差额

固定before为Git `2dbaf308e6d5137bf640cfe546a078497c1c713a:docs/architecture/`，baseline identity=`guru-trellis-architecture`、constitution=`guru-trellis-design-constitution-v1`、change-contract=`guru-trellis-architecture-change-contract-v1`。实际独立candidate_assessment为architecture_impact/target_native，refs为ARCH-DOM-019/043/045、ADR-024/035；该前置判断不代替final_plan或实现评审。

现有一次性独立final_plan有context时必须持久Bind/Selection，虽然对象完整且没有后续执行consumer。目标将该受限评审对象只读校验与session执行选择分开；原Architecture包拥有入口条件和semantic判断，shared projection只提供原Task/C4/public事实，official session/Delivery writer保持。current(key)和Author/Wording/Approval/Activation及其他Architecture stage不变。

必要职责与具体方案在本Delivery design第4..7节；完整对象校验、不同选择/损坏/真实冲突拒绝、authority-first独立评审和typed消费者都保留。没有新Skill/profile/DTO字段、持久reviewer状态、资源writer或OS业务authority。具体consumer集合包括上述五个Planning原owner、current router的purpose分支及相邻Approval当前输入。

## 必要性、替代与存量

无选择的一次性评审是当前明确需求；原普遍绑定前置不能单独证明在此路径有必要。全局放宽current会扩大其他consumers；自动恢复wrapper仍写没有后续consumer的选择；新增通用框架/大入口增加无当前consumer的复杂度。选原Architecture本地purpose限定，保同对象合法选择和无context原入口。

普通执行和candidate_assessment仍有真实执行consumer，保留原绑定/选择及原writer恢复；这是不同场景中仍成立的职责，不是待迁移债务。独立final_plan旧普遍前置在本批canonical/派发和当前知识中直接退出。旧完整安装在matching workflow/preset采用前保原合同，采用时同key/root/实际义务续接，无双reader或永久旧维护路径。

## 九 concern

| Concern | 判定及责任 |
| --- | --- |
| authority-binding | applicable；原Planning3.0/Delivery1.0 input及B下baseline/change-contract，原Interface和current router保持。 |
| constitution-binding | applicable；完整五原则约束本窄边界，不建立评分或逐原则台账。 |
| boundary-and-decision | applicable；评审对象不等于执行选择，只替代final_plan普遍绑定前置；其他stage保原职责。 |
| owner-and-single-writer | applicable；原Architecture AI判断、原Task/Delivery/session writers不变；无新生命周期写入。 |
| compatibility-and-exit | applicable；现有合法调用保留，无public格式迁移；本批旧final_plan前置直接退出，旧完整安装成套采用。 |
| gap-and-deviation | applicable；不关闭或重开无关GAP，不以此入口实现声称全流程/后端事故解决。 |
| parallel-scope | applicable；本Task只写自身规划/贡献及受审canonical差额，shared current由原owners在final_integration写完整单元。 |
| evidence-and-freshness | applicable；design内容freshness与实际typed stdout保持，源码/集成/安装/AI行为分层；当前实现未验证。 |
| review-and-promotion | applicable；final_plan审本真实贡献/必要ADR；完整candidate Architecture/Check后原owners晋升，实际after重绑并最终Check/committed独立Review。 |

## ADR与完整目标

必要ADR候选为[显式评审对象](./694-final-plan-object/adr-explicit-review-object.md)，目标identity=`ADR-EXPLICIT-REVIEW-OBJECT`。它记录R679/原接收合同的窄替代与普通执行仍保留条件。原final_plan判断该决定是否充分，原promotion才写shared ADR/导航。

完整隔离拟写位于 `694-final-plan-object/proposed/`，镜像 CURRENT/ARCH-DOM-019/043/045、change-contract、ADR及必要导航的最终路径；内部链接按目标路径解释。R679/D679/T679及R/D/T694由配对RDT contribution拥有。各完整单元保留其他条件；shared current尚未写入。

## 证据边界

实际源码/正式wrapper集成及同checkout工具安装观察由配对[#694 Test](../../requirements-design-test-contributions/694-final-plan-object/test.md)拥有。candidate/final Check、shared-current最终整合、committed Review与交付/Completion/Closure/Finish/Cleanup均尚未完成。无额外clean安装、专项eval或完整矩阵要求；不能把source/parity或历史恢复结果当作新入口已验证。
