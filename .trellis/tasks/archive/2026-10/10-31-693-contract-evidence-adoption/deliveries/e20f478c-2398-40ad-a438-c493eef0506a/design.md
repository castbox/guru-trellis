# D1：合同承接与证据判断方法设计

## 1. 设计目标、需求承接与内容基线

本设计承接本批 PRD 的 D1-R01..06、D1-S01..06 与 D1-AC01..04，对应整体 AC693-01..04。D1 独立交付公共方法、项目方法消费及受管分发；后端正式采用 AC693-05 仍由公共交付后的原 Upgrade/项目指导 owners 承接，Task 尚不能因此完成。

通过原 `DeliveryProjection.content_base` 读取的 B 为 `e514770dfa03711a4606046232593b9bf782695a`，来源是 D1 无前序结果时显式选定的 development baseline。Planning H0 同为该提交；它是观察，不是最终实现 HEAD。PR target 为 main，完整内容范围为固定 B 到最终 H，不能只审最后一个修订。

阶段适用 authority 为 `guru-trellis-architecture`、`guru-trellis-design-constitution-v1` 与 `guru-trellis-architecture-change-contract-v1`。原独立 candidate_assessment 已对精确 Author candidate 正式返回 `baseline_current / architecture_impact / target_native`，decision refs 为 ADR-034、ADR-KNOWLEDGE-FINAL-INTEGRATION。它只允许当前方案写作，不代替 Wording-current final_plan、Approval 或任何实现结果。

## 2. 当前系统、边界与目标差额

现有 Candidate Applicability And Coverage 已要求检查未改消费者、核验旧工程事实适用性，并由每个原 owner 形成自己的当前判断。Test And Validation Value 已要求实际执行声明的测试层。R648 和现行机制审查覆盖完整来源、关键前提、共同错误预期、对象/时序及无 diff 采用。本批没有前序 Delivery，不把这些能力列为新增。

具体差额是把上述规则落到执行链替换的检查动作：沿生产者输出和持久完成状态找到实际消费者的成功前提；复用参数时核对象身份、存在阶段和时序；判断测试 fixture 相对声明边界的位置；在入口/启用范围扩大后只采纳仍适用的旧事实。方法仍由原 AI owners 执行，脚本不根据关键词、数量或 pass 判断语义。

共享方法只在既有 workflow-contract 与 quality-guidelines 中补齐。各 step-local contract 指向该正文，并说明它在自身当前判断中的用途；不复制五套方法。RDT 当前完整单元和 Guru 项目 change-contract 分别由原 owner 承接自身定义与定位。公共接口、状态、schema、recorder、validator 和 workflow 路由没有差额。

## 3. 来源设计处置（唯一）

| 来源与原承诺 | 处置与设计落点 | 理由、影响及上游处置 |
| --- | --- | --- |
| workflow-contract：首轮完整独立评估、后继真实 delta/未改消费者、工程/语义/Git 分层 | retain；§4共享合同方法、§6原 owner 流程 | 在同一覆盖合同中补具体动作；不建立新审核阶段或跨 Skill evidence store。 |
| quality-guidelines：实际执行声明测试层，局部测试不证明全链，最小可靠验证范围 | retain；§4 fixture 边界、§8验证设计 | 明确合法 fixture 与越过被测边界的差别；不要求全部业务测试改成 E2E。 |
| 原 Architecture：采用机制、完整五原则、首次独立读取、原 project-check | retain；§4原 owner 消费、§6判断顺序 | 方法补充不替代机制必要性判断、独立性或当前 check；没有新 descriptor、ADR 决策或原则排名。 |
| current-knowledge：完整单元、隔离拟写、candidate Check 后原 final_integration/readback、actual after 重绑 | retain；§6、§9 | RDT/Architecture 各自单写；Planning 不写 shared current，不靠目录、链接或旧 pass 晋升。 |
| #693：业务证据只读、精确历史归因、公共交付后正式采用 | retain；§7、§8、§9及 implement Policy | 不改领域定义；D1 不承诺后端已采用，后续精确目标写入仍由原 owner 查实。 |
| #694/#695 已交付合同：显式评审对象、原身份/选择、JSON 载体及原合法输入 | retain；§5、§7 | 不修改 runtime/public I/O，不以本项方法重构接入或恢复前项专项验收。 |

固定研究提案为 advisory，历史源码/测试/阶段结果为 evidence；两者不成为新的规范性设计来源。具体约束由上述已适用 authority 和 #693 承担，没有来源设计偏离需要上游改权。

## 4. 模块、职责与设计取舍

| 落点与原 owner | 实际输入、行为与输出 |
| --- | --- |
| `trellis/presets/guru-team/spec/workflow/workflow-contract.md` 的 Candidate Applicability And Coverage | 输入为当前入口、新旧链及真实 consumer。补一个合同承接方法小节：定位输出、持久事实和成功含义，追踪读者所需前提；参数复用核实际对象、存在阶段、状态和顺序。差额回最早受影响原 owner；结果仍在原 gate 的现有说明中。 |
| 同目录 `quality-guidelines.md` 的 Test And Validation Value | 输入为测试声明边界及正式路径。补对照入口/context/配置/依赖/状态/分支/观察点的方法；边界前 fixture 和外部替身合法，边界内代产出/修正输出/绕过关键条件不能证明该边界。复用现有证据适用性规则，不另写测试台账。 |
| 原 `guru-author-task-plan`、`guru-maintain-architecture-baseline`、`guru-check-task`、`guru-review-branch` 的 `references` 方法正文 | Author 在当前候选/方案中实际承接，Architecture 核真实消费者与参数生命周期，Check/Branch Review 从原合同独立判断当前结果可用性及验证边界。只增加必要的加载和消费指导；阶段结果、finding 资格与原路由保持。 |
| 原 `guru-review-task-delivery/references/contract.md` | 在原证据/PR payload 真实性判断中消费同一方法，核声明是否超过已证 consumer/入口/安装范围；生产者成功、公共源码、dogfood 与目标采用不能互相代替。不新增 payload 字段或全链门禁。 |
| RDT：`docs/{requirements,design,test}/current/knowledge-maintenance.md` | 原 RDT owner 在三个已有完整单元承接本项行为、方法归属及风险匹配测试关系。使用新的 R693/BEH693、D693/CON693、T693 稳定身份，保留 R648/R-MECH 的全部原条件与历史结果；不改无关导航或全局版本。 |
| Architecture：`docs/architecture/06-governance/change-contract.md` | 原 Architecture owner 只补本项目九 concerns/project-check 对原共享方法和测试边界的消费定位。完整方法仍在原 canonical spec，业务定义仍在业务所属设计。 |
| 原 preset 分发 | 完整 reapply 同步受管 spec、完整 package 及声明平台的发现投影；原 drift/ownership/sidecar 检查核实际安装。本 Task 不修改 installer 或平台 launcher。 |

不选择新 Skill、跨阶段 schema、脚本 reviewer、逐测试证明文件、统一审核台账或专项评测器：它们没有原职责之外的当前 consumer，并扩大维护面。也不以一段新原则替代执行说明：现有规则已经存在，净差额须能指导实际追踪和证据判定。原 owner 的当前对话/gate 说明足以承接结果。

## 5. 接口与数据

原接口仍为：Author 当前 candidate → Architecture `candidate_assessment` → Author `solution_planning` → Wording → Architecture `final_plan` → Approval → 原 Activation。独立 reviewer 对对象及当前选中事实按原合同校验，不取得写规划或 shared authority 的职责。

实施、Check、Branch Review、Delivery Review 的 public inputs、typed exits 和唯一 consumers 保持；新增指导不进入 DTO。实际证据说明使用原现有 summary/evidence 字段，不增字段、摘要缓存或跨 owner checkpoint 读取。没有业务字段、状态或 API 变更，因此无业务数据迁移和新外部接口。

## 6. 状态、顺序、正常与失败流程

1. 当前 Planning 只写本 Delivery 的规划/上下文及真实 task-owned Architecture contribution；Wording 对三份文档完成固定范围审核，原独立 Architecture 对最终设计及贡献作 final_plan，再由 Approval 判断方案充分性。正常标准路径展示方案后接受才进入实施。
2. 实施 owner 先保留原历史证据，对照当时规则和当前可复用能力，再修改命中的 canonical 方法。原 RDT/Architecture owners 准备各自完整隔离 proposed targets；此时 shared current 未晋升。
3. 原 preset 完整 reapply 后检查分发、声明平台、sidecar 和 drift，执行§8命中检查。原独立 Architecture phase2 与完整 candidate Check 评估实现、所有拟写和未改 consumers。
4. candidate Check 通过后合法回 implementing，原 Architecture/RDT owners 分别在 final_integration 固定真实目标、比较完整组合、写入并读回。implementation 以同一 B 和实际所有 after paths 重建 candidate/begin_check。
5. 最终 Architecture/Check、精确 TaskCommit、独立 committed full-range Branch Review、Delivery Review/PR readiness 和原发布/合并链覆盖实际 after。D1 只交付选中公共范围；剩余采用交回原 Upgrade/项目指导 owners。

来源/范围选择变化回 Clarify；方法机制或职责变化回 Author/Architecture；普通实现或定向检查失败回原 implementation/Check。真实缺证据只限制其依赖判断，不把历史未知变成已确认漏检原因，也不跳过当前门禁。

## 7. 恢复、兼容、迁移与集成

方法修订通过当前原 Skill/spec 分发，无 public I/O 或 parser 迁移。旧安装保持其实际合同，不能因公共源码变更就报告已采用；目标正式升级使用公共交付后的完整精确 source 与原安装合同，保留用户定制、Task/Delivery/session 和工作区，并逐项处理 conflict/sidecar。

同 owner 输出丢失只用其正式恢复/重入；不读其他 owner 私有 checkpoint，不从 phase/文件存在重造 pass。不改变含义的文案修订刷新实际依赖，真实方法变化重新评估候选。共享 authority 的组合冲突回原 maintenance owner，不覆盖并行改动。

本批无业务数据、环境或部署写入，所以没有新增业务回滚协议。未提交的本 Task 文件可在其明确范围内修订；commit/push/PR/merge 与清理各由原 owner 显示精确副作用，当前方案不代替后续操作边界。

## 8. 验证设计

| 验证 | 要求/AC、入口与输入 | 预期观察及实际边界 |
| --- | --- | --- |
| V693-01 | D1-R01/D1-AC01；只读固定事故源码、当时安装规则、原计划/public 结果、E30 和 PR #953 | 可定位 producer/consumer 合同、参数/时序及测试条件；当时规则已存在和 E30 仅编译保留原义。具体历史放行理由不可恢复时明确未知；不执行业务复现或修改业务测试。 |
| V693-02 | D1-R02..05/D1-AC02/03；原 Check/独立 Branch Review 阅读完整变更与真实方法 consumers | 共享方法、各 owner 消费和项目投影有直接用途；fixture 合法前提与边界内代产出可区分；旧事实采纳范围和新可达条件没有被绿测替代。此为本批现行质量链的实际语义判断，不是专项行为评测或“永不漏检”证明。 |
| V693-03 | D1-R05/06/D1-AC04；source/installed `check-skill-packages.sh` | 完整 package、原接口/路由、发现投影与受管内容客观一致；schema/路径检查不证明语义效果。 |
| V693-04 | D1-R06/D1-AC04；`trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 后 `check-dogfood-overlay-drift.sh --repo .` | canonical/dogfood/完整包与声明平台保持原受管闭合；`.new`/`.bak` 按实际前像逐项处理。只验证当前实际安装，不扩完整矩阵或额外 throwaway。 |
| V693-05 | D1-AC04；原 in-memory Python syntax、marketplace JSON、Bash syntax、Task context validate、`git diff --check` | 现行必需客观检查通过，未动接口/脚本时不新增镜像实现的断言或文案锁定测试。 |
| V693-06 | D1-R05/D1-AC04；原 candidate Check → 原 final_integration/readback → 同 B actual after → 最终 Check/committed Review | 完整拟写、真实 shared 写入和最终内容各由原 owner 判断，candidate 结果不冒充最终 pass；所有实际新增/生成/晋升 paths 都在最终覆盖中。 |

后端正式采用、真实业务效果、部署/QA、Release 及完整多平台矩阵没有本批证据，保持各自范围。当前只形成验证设计，不预填以上执行结果。

## 9. Canonical 引用、本轮差额与实际未决项

当前 RDT-REQ/DES/TST-KNOWLEDGE 的 R648/D648/T648、R-MECH/D-MECH/T-MECH 继续成立。原共享方法新增具体合同承接与 fixture/路径判定；配对 R693/D693/T693 只承接该能力及原消费关系，不重复完整方法正文或历史评测要求。

Architecture 采用真实隔离贡献 `docs/architecture/contributions/693-contract-evidence-adoption.md`，完整项目 proposed target 位于同名目录的 `proposed/docs/architecture/06-governance/change-contract.md`。原九 concerns、descriptor/check/result identity 与 ADR-034、ADR-KNOWLEDGE-FINAL-INTEGRATION 继续适用；不改变长期 owner、GAP 生命周期、兼容退出或原则例外，因此本候选无需新增 ADR。final_plan 和实施期发现这些事实变化时由原 Architecture 重新判断。

原 RDT owner 在实施期创建 `docs/requirements-design-test-contributions/693-contract-evidence-adoption/` 的真实三层完整拟写与追踪；原 final_integration 才写共享 authority。没有需要用户补做的产品选择。历史审核理由仍有记录缺口；方法效果仅由本批实际质量链和后续采用覆盖，不承诺根治全部未来漏检。
