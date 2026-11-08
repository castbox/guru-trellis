# 正常完成路径与协调成本：D1 设计

## 1. 设计目标、需求承接与内容基线

完整承接本批 PRD NC-R1—R7、NC-S1—S4、NC-AC1—AC4；通过原唯一方法及两处实际消费明确正常最终完成、主动替代与协调成本判断。

development baseline B 为 `80fc24eed3d4deb2dd0fc63126c0affb9789d365`，来源为本 Task 创建时复核的 `main` 固定提交；Planning H0 同 B。内容范围是本批实际 canonical 与必要 RDT 差额，后续构造 Candidate 用原公开构造器纳入全部真实路径。PR 目标若将来发布为 `main`，不构成本轮发布动作。

阶段 authority 为 `docs/architecture/README.md`（guru-trellis-architecture）、`00-foundation/design-constitution.md`（guru-trellis-design-constitution-v1）、`06-governance/change-contract.md`。首次独立 candidate_assessment 实际返回 baseline_current / no_architecture_impact，freshness `sha256:d8aea3ab6b6b5f60994973b2ce2b9bf2b141629c808f551c9749dad4160eb2f6`；该结论只判断候选，不替代最终设计、实现或验证。

## 2. 当前系统、边界与目标差额

本批无前序 Delivery。Architecture contract 现有 Adopted-mechanism review 已覆盖正常路径、必要性、总体代价和可行替代，但未明确额外协调默认不准入、审核方主动尝试替代，以及异步受理不等于最终完成成本降低。

Root Cause Protection 已要求提出方举证并引用 Architecture，Author 已引用采用机制审核。本批在原段落整合方法，另两处只明确消费顺序及资格边界。Approval、Check、Branch Review 和独立 Review 的有效引用继续使用，不批量改入口。公共 I/O、状态、runtime、installer、五原则及owner不变；不新增项目 Architecture 正文或 ADR。

## 3. 来源设计处置（唯一）

下表定位原来源 `/tmp/codex-architecture-three-layers-20261108/proposal.md` 的规范承诺；本设计已展开必要内容，不依赖临时文件持续存在。

| 来源/原承诺 | 处置与具体落点 | 理由、影响、上游处置 |
| --- | --- | --- |
| §3.1/3.2：唯一方法在原 Adopted-mechanism review；先推导最终完成路径、额外协调默认不准入 | retain；本设计§4的Architecture原段整合 | 保留原适用性/轻量路由，不建新owner或问卷 |
| §3.2：作者先尝试删除/收窄/原子能力/责任边界；reviewer reconstruct a feasible simpler alternative | change；§4写主动尝试并独立判断可行性，原方案已最小则说明依据 | 根NC-R3已由原scope owner接受该修正，避免强迫虚构不存在的可行替代 |
| §3.2：正确性与完成成本共同判断、真实最小例外、存量三分类 | retain；§4/§6展开 | 不按名称禁用，不危险删除未知保护，原scope与生命周期owner保持 |
| §3.3：Root Cause资格不等于Architecture准入；Author路径先行 | retain；§4两处消费 | 不复制唯一方法，保留原qualification与typed exits |
| §7/§8：定向检查、源码与采用/业务效果分开，三层独立职责 | retain；§8/§9及implement Policy/Docs Plan | 不追加完整安装矩阵或生产测试，不升级依赖；backend另仓 |

## 4. 模块、职责与设计取舍

`trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md` 的 Adopted-mechanism review 独占方法。先从支持的可观察最终结果及真实业务、数据、权限、外部约束推导直接可行路径。新增、修改、扩用或复用带来的共享写、串行、等待和独立状态默认不准入；采用方先尝试删除、收窄一致性对象与时间段、已有原子能力或更直接职责。独立审核主动尝试并自行判断，不仅检查作者解释自洽。

共同核正确性和最终完成成本：核本机制增加的I/O、竞争、串行、排队与恢复前提及跨用户、资源和实例范围。提前返回ACCEPTED不自证异步更快。真实例外须有接受要求、较简单方案不能满足的具体理由，并说明最小范围及该范围内的成本；并非每个helper都要性能实验。原方案已最小可保留，不制造必须找到替代的结论。

原 Root Cause contract Protection 仅补明确资格成立不自动成为Architecture批准，并指回上述唯一方法。原 Author authoring在原消费段明确先推导完整完成路径、再筛选额外机制。两处不抄具体成本清单。

保留必要短事务、内存临界区和容量控制的依据判断。已有机制区分必要性已证、无必要成本已证、证据不足；已证问题沿原owner有界修订及消费者适配；缺证不危险删除、不批准扩用，限定调查而不全局停工。

拒绝新增统一准入Skill、评分、机制注册或所有入口重复规则：原消费者足够，新增层没有直接职责。也不按锁/guard/queue关键词禁止，以免破坏真实正确性约束。

## 5. 接口与数据

没有API、DTO、schema、配置或持久字段变化。现有 Author profile/当前来源→原qualification→实际候选→Architecture candidate_assessment→Author solution_planning→Wording→Architecture final_plan→Approval/Activation 的输入出口保持。

实现阶段原 RDT owner 写完整隔离拟写；原Architecture无影响判断不产生空贡献。原候选Check、RDT final_integration/readback及全部实际after重绑仍保持，不能因纯规范修改跳过原门禁。

## 6. 状态、顺序、正常与失败流程

本设计不新增状态转换。方法消费顺序是：识别承诺完成→建立直接路径→定位实际额外机制→主动尝试删除/收窄/替代→独立判断必要性与成本→按原出口处理。Protection只承担原资格；真实保密/权限不以事故为前置。

候选不满足接受要求时由原设计/实现owner修订机制；真实范围冲突回Clarify。已有保护缺证时保留必要现状且不扩大采用结论；已有理由覆盖当前对象时简短承接，不因阶段变化重复全部实验。

## 7. 恢复、兼容、迁移与集成

直接修改唯一当前方法，无新旧双reader、兼容开关或第二文档authority；原公共输入输出和受管分发机制保持，因此无数据迁移或运行恢复协议变化。已安装项目不因源码变化自动更新，本批不实施安装更新。

业务整改和生产效果由backend及原Issue owner处理；Guru通用方法不带业务ID或私有技术规则。RDT历史观察保持原含义，不将旧八次native安排扩为本批验收。后继安装采用另沿原完整matching更新owner，不能用本地检查替代。

## 8. 验证设计

| ID | 对应范围、入口与输入 | 观察及限制 |
| --- | --- | --- |
| V1 | AC1/AC2；独立审核实际新方法，审共享写、持锁慢I/O、整批等待及必要短事务/容量/证据不足/最小方案对照 | 核是否得出本批要求的有条件结论，主动寻找规则漏项及误禁；推理样例是临时诊断，不把期望文本自比较当行为证明 |
| V2 | AC3；逐段读canonical diff及实际Author/RootCause/Approval/Check/Review引用 | 正文唯一、两处明确消费，无新增公共状态或重复准入层；引用命中本身不证明语义 |
| V3 | AC4；原三个package的test_contract.py及git diff --check；实际命中引用本地存在检查 | 证明源合同及机械边界，现有适用测试复用；不新写固定文案断言，不宣称完整安装/真实业务效果 |
| V4 | RDT真实完整拟写与本批变更比较 | 承诺/追踪/证据边界准确，历史事实不改写，原candidate/final链覆盖真实after |

按Test And Validation Value先完成实现及直接语义检查，再运行命中已有合同检查。必要检查通过且具体语义缺口已解决即停止；失败先归因入口/设施/候选，不把工具失败冒充业务根因或无限追加实验。真实未解问题才补定向观察。

## 9. Canonical 引用、本轮差额与实际未决项

命中RDT同名 `knowledge-maintenance.md`：Requirements R-MECH-01—05、Design D-MECH-01—03、Test T-MECH。原RDT owner补方法承诺、原消费关系及本批验证边界的真实差额，完整单元保留仍有效前驱；唯一方法正文仍在canonical Architecture contract。

独立Architecture已判本候选不改变项目架构决定，无Architecture贡献或ADR义务；项目change-contract现有委托关系有效，不补空句/共享导航或版本流水。RDT隔离拟写和最终晋升按implement Docs Plan。当前无待决产品问题；新机制、范围或authority事实变化回最早原owner刷新，不靠当前候选结论自动通过。
