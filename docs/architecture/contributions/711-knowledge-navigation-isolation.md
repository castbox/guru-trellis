# #711 知识导航隔离架构贡献（候选）

Task 711-knowledge-navigation-isolation / generation 0；Delivery 92e40c5b-7dd9-48cc-8c44-a5691b31034b。状态 proposed；不构成shared current。范围与精确方案见 .trellis/tasks/11-03-711-knowledge-navigation-isolation/deliveries/92e40c5b-7dd9-48cc-8c44-a5691b31034b/design.md，Direct Source https://github.com/castbox/guru-trellis/issues/711。before authority为Git f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/architecture/README.md；authority identity guru-trellis-architecture；constitution guru-trellis-design-constitution-v1；project contract guru-trellis-architecture-change-contract-v1，required set guru-trellis-architecture-change-concerns-v1；Planning3.0，后续nonplanning5.0/Delivery3.0沿原合同。

采用 target_native，decision ADR-031、ADR-KNOWLEDGE-FINAL-INTEGRATION保持，新增ADR-KNOWLEDGE-NAVIGATION-ISOLATION。当前第一处缺口是独立单元晋升仍汇聚共享登记。目标是根入口稳定发现合同，单元自身保存身份/状态/来源/必要关系；搜索仅定位，原owner判断current与完整语义。无新registry/schema/API/锁或进程协调。

| Required concern | 判定与本批承接 |
| --- | --- |
| authority-binding | applicable；上述阶段authority及原public key；不能以目录/搜索替代 |
| constitution-binding | applicable；原完整宪法由独立owner读取，命中cohesion-change-isolation、concept-semantic-completeness、minimum-necessary-complexity和debt-one-way-convergence；不复制原则或评分 |
| boundary-and-decision | applicable；R711与既有完整知识，目标为共同方法/实际导航消费者；新ADR拥有导航决定 |
| owner-and-single-writer | applicable；RDT三层原owner，Architecture原maintenance writer与独立assessment职责保持，Task准备proposed，最终shared写归原promotion |
| compatibility-and-exit | applicable；target-native无新dual parser；旧Task只保阶段适用读取，最终集成重读真实目标，新写不登记旧共享索引；MIGRATION-711明确switch/恢复 |
| gap-and-deviation | applicable；本批纠正shared navigation汇聚，未覆盖业务迁移和Release保持明确；不关闭无证GAP或建第二台账 |
| parallel-scope | applicable；不同能力正文/局部导航独立路径；同能力/关系真实重叠由原owner语义整合，不取单侧 |
| evidence-and-freshness | applicable；design V711-1..6固定完整事实/两序/Agent/安装/迁移；Planning已实际评估，完整拟写现已准备，尚无本实现候选的Phase2、行为或安装通过声明 |
| review-and-promotion | applicable；本真实贡献、ADR及完整proposed targets现已提供，仍待完整候选的独立Phase2和原候选Check；其后才final integration/readback、actualafter重绑和最终完整质量链 |

## 完整 proposed targets

以下文件是目标的完整拟写正文；路径均相对于 repository 根。副本位于本 Task 隔离目录，尚未写入 shared current，也不因目标正文中的 after 状态成为已接受 authority。独立 Architecture 与原 Check 必须覆盖完整实现、这些全部拟写内容及受影响消费者；候选 Check 后才由原 maintenance writer 最终整合。

| Actual target | Complete proposed body | 本次差额 |
| --- | --- | --- |
| `docs/architecture/README.md` | [README](./711-knowledge-navigation-isolation-proposed/docs/architecture/README.md) | 固定职责目录和限定发现替代逐单元登记；保稳定体系身份、真实历史来源和未迁移边界 |
| `docs/architecture/06-governance/rules.md` | [rules](./711-knowledge-navigation-isolation-proposed/docs/architecture/06-governance/rules.md) | 只修 ARCH-GOV-012 的发现、独立写入与旧索引退出；其它治理条款原样保留 |
| `docs/architecture/06-governance/change-contract.md` | [change-contract](./711-knowledge-navigation-isolation-proposed/docs/architecture/06-governance/change-contract.md) | 承接项目单元/入口维护、原 owner、迁移及在途最终集成；九 concerns/check descriptor/API 不变 |
| `.trellis/spec/architecture/baseline-usage.md` | [baseline-usage](./711-knowledge-navigation-isolation-proposed/.trellis/spec/architecture/baseline-usage.md) | 项目只读 projection 从根取得职责范围再限定检索；只定位原共享方法和采用边界 |
| `docs/architecture/adr/knowledge-navigation-isolation.md` | [ADR](./711-knowledge-navigation-isolation-proposed/docs/architecture/adr/knowledge-navigation-isolation.md) | ADR-KNOWLEDGE-NAVIGATION-ISOLATION 的完整 after 定义、必要性、代价、替代、迁移、旧写退出和重审条件 |

根中被移除的个体导航身份已在原完整正文中定位：ARCH-RUNTIME-LOCATION 位于 `01-current/runtime-location.md`，ARCH-REVIEW-SUFFICIENCY 位于 `03-domains/review-sufficiency.md`，ARCH-FND-STACK-001 位于 `00-foundation/stack-selection.md`，ARCH-GOV-001..012 位于治理正文，ADR-KNOWLEDGE-FINAL-INTEGRATION 位于其原 ADR。历史 locator/version/关系行全部保留在拟写入口；不向另一总表迁移个体登记。

`system.md`、domain/ownership、integration/distribution、stack selection、constitution 和既有 ADR 完整正文未发生本项职责变化，故不为本项追加摘要或登记。`adr/README.md` 作为可解释的旧历史导航保留，不继续登记新 ADR；新 ADR 自身提供稳定 identity 和来源，根按 `adr/` 目录发现。RDT 代表迁移和共同 canonical 方法由原 RDT/implementation owner 承接，本文不写其文件。

`MIGRATION-711.md` 是本批 matching 采用合同的必要关系；实际 Agent、合并和安装结果由本批唯一 Test 贡献拥有。此处只给正文和设计差额，不记录执行通过。当前 before/after 及消费者读写见 design 第4..7节；project-check 仍为 `guru-trellis-architecture-convergence:repository:1`，其当前结果由独立 owner 实际判断。本维护 writer 已参与拟写，不为自身正文填独立 assessment pass。
