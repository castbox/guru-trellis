# #793：原 qualifier 条件调用贡献

Task `793-conditional-qualifiers` / generation0，Delivery `55d0c98b-a483-4ee3-b8ff-7ad547ef3ee9`。来源是[Issue #793](https://github.com/castbox/guru-trellis/issues/793)。这是实际规划贡献，供原 final_plan、实现、完整候选 Architecture/Check、final_integration 与 committed Review 消费，尚非 shared-current 或交付事实。

## Authority、边界与决定

固定 before 为 Git `e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e` 的 `docs/architecture/`；baseline=`guru-trellis-architecture`、constitution=`guru-trellis-design-constitution-v1`、change-contract=`guru-trellis-architecture-change-contract-v1`。原独立 candidate_assessment 实际返回 architecture_impact/target_native，refs ADR-008/020；本贡献不代替 final_plan 或实现判断。

当前三 owner 已分离，Check 空候选已不调用，root 已有仍适用结论采用。真实差额是非空候选的固定 normal/solution 调用及 root 的两上游结果前置。采用 [design 第4—7节](design.md) 的 owner-owned 短条件、原 caller 轻量触发、真实原 Skill 闭环与 root 条件前置。普通计算不自动成为 business authority；真实诊断/缓解/修复/保护不能改名绕过。

必要性来自本 Task 已接受的减少不适用加载/装配/形式调用要求。只删 global 文字不能解除原 caller/root 前置；新 wrapper/脚本分类器会复制三个 owner；把条件全放 SKILL 全文后不能实现加载前判断；统一大问卷或资格账本没有当前 consumer。选每个原包独占短条件，原caller依当前事实作是否触发判断，原qualifier仍独占正式资格 verdict。没有新 Skill/profile/DTO/exit、第二authority、存储或OS业务机制。

## 九 concerns

| concern | 适用判定与责任 |
| --- | --- |
| authority-binding | applicable；绑定上述当前authority、原Planning3.0目的及Delivery1.0输入，后续原非Planning合同不变 |
| constitution-binding | applicable；完整五原则共同约束当前必要性、职责和变化隔离，不设逐原则评分 |
| boundary-and-decision | applicable；target_native；caller仅判触发，三个owner独占资格，窄改ADR-008/020调用前置 |
| owner-and-single-writer | applicable；Author写本规划，实施写canonical，原RDT/Architecture分别final_integration；script只验事实，安装owner单写投影 |
| compatibility-and-exit | applicable；wire/id/consumer保持，matching调用语义迁移。旧完整安装采用前固定原合同；采用后不保新旧双reader |
| gap-and-deviation | applicable；本Task仅修固定调用差额，不重开/关闭无关GAP，不承接#736其他拆分。实际未验证项保持明确 |
| parallel-scope | applicable；本Task隔离规划/贡献与canonical明确改动；不竞争shared当前定义/导航/其他Task状态 |
| evidence-and-freshness | applicable；新invocation保当前facts校验，语义采用按材料变化；source/runtime/native/安装分开，不以digest当语义authority |
| review-and-promotion | applicable；final_plan审本真实贡献与必要ADR；完整实现/隔离proposed经candidate Architecture/Check，原owner晋升readback，再actual after重绑和最终质量链 |

没有当前legacy运行时适配层或新增兼容数据，故不新增legacy owner/删除期限字段。旧完整安装的固定合同由原升级owner处理，合法在途恢复保持相同Task/key/实际阶段；缺失或实质变化判断回原producer。

## 真实目标与晋升

必要 ADR 候选为[条件加载与调用](adr-conditional-qualification.md)，目标 `docs/architecture/adr/conditional-qualification.md`，identity=`ADR-CONDITIONAL-QUALIFICATION`。只窄替代固定调用/上游前置与普遍重复规则，保三职责及原拒绝、修订、诊断、范围选择和blocked。

实施原owner完整读取ADR-008/020、ARCH-CUR-019/052、ARCH-DOM-011/035及必要真实引用，准备隔离完整proposed；不向shared列表新增登记。原RDT维护配对完整793单元和382前置的必要更新。shared写入只在完整candidate Architecture/Check之后，由原final_integration拥有，保写前authority、expected-current和实际readback。

## 实施隔离拟写

完整 proposed root 为 `docs/architecture/contributions/793-conditional-qualifiers/proposed/`，
镜像六个最终目标：`docs/architecture/adr/{008-solution-mechanism-qualification,020-root-cause-qualification,conditional-qualification}.md`、
`docs/architecture/01-current/system.md`、`docs/architecture/03-domains/{ownership,qualifier-applicability}.md`。
上述旧单元保有效语义和历史观察，只更新真实调用职责/必要关系；新domain与ADR
拥有本批决定和边界。内部相对链接按最终目标解释。现阶段shared targets未写。

配对完整RDT拟写位于 `docs/requirements-design-test-contributions/793-conditional-qualifiers/`，
不回写旧immutable版本或历史Test。实现及实际验证由其test.md承接，原独立
Architecture/Check审完整实现与上述全部拟写后，才由原维护方晋升。

## 当前证据限制

当前实现与V1—V5观察由配对Test单元单写。共享晋升、最终质量链与目标业务采用仍须各自证据；本贡献不声称成本降低、完整平台矩阵、Release或Task Completion。
