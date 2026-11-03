# D1：共同审核充分性 SSOT 与依赖收敛

## 1. 设计目标、需求承接与内容基线

本批覆盖 D1-R1–R6、S1–S6 和整体 AC1–AC5。development baseline B 是用户选定的 `main@404c841e9ca917b4680831aa0becd2e26d72fa0c`；没有前序 Delivery，内容范围从 B 开始。Planning H0 同为该 commit，最终实现 H 尚未形成。PR 目标为 `castbox/guru-trellis:main`，与固定内容基线分开。

适用 Architecture 为 `guru-trellis-architecture`，constitution 为 `guru-trellis-design-constitution-v1`，change-contract 为 `guru-trellis-architecture-change-contract-v1`，均由 `docs/architecture/README.md` 及其 current 正文定位。实际 candidate_assessment 返回 `baseline_current / architecture_impact / target_native`，决策 refs 为 ARCH-FND-002、ARCH-GOV-012、ADR-034，候选 freshness 为 `sha256:251ecd8ee3780c0fedcecbe17a3afc108ea0bf26cfdd0f28c8a30e88bf3ae91b`。该结果只允许方案写作，不证明最终规划、迁移或行为效果。

## 2. 当前系统、边界与目标差额

当前 `review-method.md` 组合 Check/Branch 内部方法，Check/Branch 又加载该组合。`workflow-contract.md#candidate-applicability-and-coverage` 已拥有候选承接、工程事实与 formal range 规则；`quality-guidelines.md` 已拥有专业标准与测试价值。共同规则存在重复与缺失，阶段规则和专题正文不能因收敛而丢失。

目标依赖为：原审核入口 → provider 的共同充分性规范；工程审核入口另读薄 `review-method` → 同 provider 的专业/Architecture/RDT 方法。共同规范不读取 Check/Branch 的内部合同、artifact、recorder 或出口。原阶段合同只保留其真实 entry、顺序、资格、通过与执行职责。新规范位于 `trellis/presets/guru-team/spec/workflow/review-sufficiency.md`，安装到 provider 的 `.trellis/spec/workflow/review-sufficiency.md`。

本批没有前序。公共 API、schema、typed exits、阶段通过和副作用边界不变；不添加运行状态、充分性 gate 或跨仓库安装要求。

## 3. 来源设计处置（唯一）

| #717 原承诺 | 处置 | 本设计落点、理由与影响 |
| --- | --- | --- |
| 当前对象审查完成与对象通过、修复验收分开 | retain | 第4、6节：共同规范只定义当前审查充分性，原阶段继续决定 pass/block、修复和出口 |
| 固定 source 界定规则/消费者，不追无关新增 | retain | B 固定于第1节；第4节逐项集合，交付前只核真实 delta 与必要消费者 |
| 从来源、入口、消费者建立并反查覆盖 | retain | 共同规范“范围与覆盖”；不能以文件/维度齐全、实现测试相符或数量代替判断 |
| 按剩余覆盖推进、同机制补查、完整报告、充分后停止 | retain | 共同规范“调查与结束”；保留所有成立 findings、同根因触发/影响、缺口及其影响；不固定轮数或追求全绿 |
| 后继候选承接有效覆盖，不接管修复调度 | retain | 第4节迁移表中的共同承接正文；formal range/predecessor 与原 rework/closure 仍留原 owner |
| 旧定义迁出并删除，专业及专题规则不复制 | retain | 第4节迁移表；新源没有阶段反向读取，薄组合仍负责工程审核方法组合 |
| provider/target 分开，外部专业独立调用无隐含 Trellis 前置 | retain | 第4、5节：Guru 读取完整 provider，target authority 独立解析；外部 Skill 未修改、未宣称接入 |
| 公共 I/O/出口保持，不增 gate/台账/字段 | retain | 第5、7节：仅 Markdown 行为及分发/测试差额，现有公共记录器不获得语义职责 |
| 真实 Agent、验收方持有预期、首次旧新可比观察 | retain | 第8节 V3，生产 owner 入口和完整 provider；不以方法片段或机械结果冒充实际入口 |
| canonical/dogfood/installed/平台与 reapply/drift | retain | V1、V4；使用原安装 owner，保护用户文件及 Task/session，报告未跑完整矩阵 |

没有 change/reject，也没有需要上游改写的承诺。

## 4. 模块、职责与设计取舍

### 4.1 规则迁移与唯一 owner

| 规则 | 固定 B 上的现状 | 目标和具体退出 |
| --- | --- | --- |
| 对象/目的、来源到行为覆盖 | review-method 的 business coverage/remaining methods；quality 的通用选对象段 | 共同充分性源拥有通用覆盖与反查。旧共同段删除改引用；工程实现覆盖与专业选择仍由原组合/专题负责 |
| 分批推进、数量/篇幅不能结束、同根因补查 | 现有完整范围要求，没有独立完整共同定义 | 新源明确剩余覆盖驱动、同机制必要消费者和 findings 不丢弃，不添加计数器 |
| 发现判断、报告与充分性结束 | review-method 的 Complete current judgment 与报告共同段；阶段有自身 pass 条件 | 通用结束/局限迁出；原组合保留工程报告项目，阶段 pass、fix 和前置阻断保持 |
| 后继覆盖与无因重扫 | workflow-contract 的 Original coverage/current judgment，以及 review-method、Check/Branch 的共同复述 | 通用有效/失效/补审原则迁到共同源；原 anchor 保留 formal B..H、独立性、public result/predecessor、窄 alignment 与 owner recovery 条件并引用共同原则；删除重复正文 |
| 工程执行事实与 Git/语义区分、消费者契约连续性 | workflow-contract 的唯一充分定义 | 保持原 owner 并准确引用，不另写副本；实际 formal 约束不迁成通用完成条件 |
| 检索、测试价值、因果和完整知识 | semantic-retrieval、quality Test And Validation Value、causal-completion-semantics、RDT current-knowledge | 原源不变；共同源与原 caller 定位适用专题，不能把它们合并进本文件 |
| 工程审核维度及阶段特例 | Check/Branch semantic sections 与共享组合 | 迁出二者实际重复的通用方法；保留九维结果字段、Qualification、Architecture 独立顺序及各 profile 特例。组合不再读 Check/Branch 内部实现 |

这张表是本批迁移说明，不是长期清单系统。实施须核每段完整条件，不能机械按关键词删段。

### 4.2 固定消费者与合法阶段差异

以下 package 均位于 `trellis/skills/guru-team/packages/`。每个实际审核入口在读取自己的对象前加载同 provider 的共同规范；不新增运行时 Skill 调用。

| Package | 本职责对象与保留的差异 |
| --- | --- |
| guru-clarify-requirements | 当前 Issue/来源/scope 的内容与选择；原 Questions/Convergence、duplicate snapshot 和 source actions 保持，不做代码审核 |
| guru-review-change-request | 当前 Issue/draft 的十维就绪；原 prerequisites 与独立交付判断保持 |
| guru-review-contract-wording | 固定完整 title/body、三份规划或 explicit_paths；scanner/hit 分类、受控 rewrite、前置与七项规划语义保持 |
| guru-approve-task-plan | 当前 Delivery 三份规划的八维充分性；只消费实际 adjacent final_plan，不接管 Architecture 或写规划 |
| guru-review-change | 当前指定代码/文档/测试对象；保留只读、多独立视角和终止出口，finding 未修复不妨碍 reviewed |
| guru-check-task | 完整当前候选与九维 Check；保留原 Qualification、fix/current Check、candidate/final 区分与阶段通过条件 |
| guru-review-branch | 固定完整 committed range、合法 continuity/alignment；保留 finding ancestry、closure、首次独立性和正式结果 |
| guru-review-task-delivery | 一个独立切片及 PR payload/readiness；不扩成完整 Task 审核，不接管 Completion |
| guru-review-task-completion | 整体 accepted scope 与所有实际 Deliveries；保留未交付工作/缺证、观察层及 Completion 条件 |
| guru-maintain-architecture-baseline | 真实 stage/purpose 的独立架构判断；保留 authority-first、project checks、贡献与晋升单写 |
| guru-maintain-requirements-design-test-ssot | 本职责完整知识单元、关系与晋升结果审查；保留三层 authority/Architecture 继承、proposed/current 与 writer 边界 |
| guru-verify-extension-installation | 安装证据充分性与范围审查；保留 source-only、throwaway、矩阵的实际适用与 verified/blocked 条件 |

Discovery 的检索充分性由原 semantic-retrieval 定义；Create Issue/Commit/Publish/Merge 的实际执行前门禁继续由原 owner 承接，不自动扩展成新的全面审核消费者。外部 `guru-ai-guides` 不在本仓库可修改集合。RDT/Architecture 项目正文仅定位唯一共同规则，不复制正文。

选择 managed-spec 是因为这十二项属于完整 Guru provider，已具有同一分发机制。把正文留在独立审核 package 会使其它职责依赖该步骤；新增 wrapper Skill 或运行时 gate 会增加无必要状态和路由。本方案不引入第二执行路径。

## 5. 接口与数据

调用关系是“原 profile/输入 → 同 provider 共同规范及适用专题 → 原对象审查 → 原 recorder/validator → 原 typed exit/consumer”。provider 为 canonical source 时读取 `trellis/presets/guru-team/spec/workflow/`，安装时读取 provider 的 `.trellis/spec/workflow/`；不能把 target 的旧规范副本当成 provider。target 自有 AGENTS、需求、架构和工程标准仍独立读取。

本批没有新 API、DTO、schema、状态或公共字段；不改变已有退出语义。检查进度留会话或原有必要结果。eval 的实际输入、trace、模型条件、报告与验收侧预期只服务本项实验，存于现有 eval 外部临时结果目录；它们不是业务 gate 或新的长期运行记录。

## 6. 状态、顺序、正常与失败流程

原 owner 确定对象、范围和版本，加载共同规则及必要标准，形成/反查覆盖，再按剩余范围调查。对发现核证据、适用性和影响；存在真实同机制关联则补查。覆盖充分时完整报告并结束当前审查；有 findings 继续沿原阶段条件决定 pass 或返工，独立只读审核不自行修复。

必要访问、authority 或执行证据缺失时，报告已查/剩余及影响，沿原 blocked 或前置停止合同执行，不新增 partial 出口。当前审核不等待修复。原流程发起新候选后，审核完整增量和受影响路径，保留有效原覆盖、补齐失效部分；组合影响不明才做所需完整审查。没有新证据/影响时不无因反复扫描。

新源不可读、provider 混用或真实来源变化，沿原缺失安装/原 authority owner 恢复。恢复不是新批准，也不放宽原 formal 条件。

## 7. 恢复、兼容、迁移与集成

同一 source 变更中完成共同正文、旧定义删除、十二消费者与 managed 投影，保留原 paths/anchors 的必要引用，避免并行定义。历史 archives/ADR/固定版本不回填；现有项目读取原适用版本仍沿原生命周期退出，不新增双读机制。

dogfood 是已有 checkout，含 Task/session，因此使用 `guru-upgrade-tools` 的完整源合同、`dependency_mode=local_candidate` 和明确目标 checkout，同步实际 managed assets；不能用普通 apply 的旧 Task 阻塞扩大成历史迁移。preserve 真实用户改动，逐个处理 sidecar；不手工覆盖安装副本。代表 clean 仅在实际变更需要时最多一个；平台 projection 定向测试不等于多平台安装矩阵。业务项目不升级。

没有数据库迁移、部署或新恢复状态。代码/文档修订按真实依赖回原阶段；同源普通构造错误自动修复。未验证真实行为、必需安装或迁移退出时不能声称整体完成。

## 8. 验证设计

| 验证 | 层与入口 | 预期及证据限制 |
| --- | --- | --- |
| V1 规则/消费者 | 源码审查、共同定义迁出对照、实际加载引用、同 provider 读取与原 package contract/runtime 定向测试 | AC1/AC2；无阶段反向依赖，旧共同正文退出，公共 I/O/出口原语义；仅静态/机械证据 |
| V2 测试有效性 | 原受管 installer projection/reapply 测试扩展；真实 writer 将新 spec/package 投影后实际读取并验证 local edits/sidecar | AC5；不能只断言源文件有关键词，不能以分发证明 Agent 已读 |
| V3 真实 Agent | 原 native eval/观察框架，完整旧/新 provider 及真实生产 owner 入口；相同 fixture、CLI 配置/模型/权限和入口条件，保留每侧首次结果 | AC3/AC4；验收侧持有预期并逐例核实际调查/findings/完成；不是业务生产或发布证据 |
| V4 实际安装 | 原 tools owner 同步本 checkout；installed discovery/validation、声明平台 projection、`check-dogfood-overlay-drift.sh`、适用 reapply；核 `.new/.bak` | AC2/AC5；明确 local-candidate/source-lock 与完整 Release/远程矩阵未验证 |
| V5 最终质量 | candidate Check → 原 RDT/Architecture final_integration → 实际 candidate 重绑 → final Check → commit → 独立完整 B..H Review | 全部 AC；原阶段结果不能由 V1–V4 或本计划代替 |

V3 的案例在首次执行前由验收侧固定为：Issue 内容的分散缺口与合法对照；代码候选的分散缺陷/共享机制多入口/失败测试且不修复；正确实现与合法配置差异；必要证据不可访问；规划/设计对象的职责/顺序/约束承接；同一代码对象的后继候选。后继沿真实 thread resume 保留可验证原覆盖。每例的具体应发现问题、合法控制、必要缺口在验收侧、被测 fixture 之外持有。不得向 Agent 提供期待 findings 或生产入口外纠偏。

验收读取首次原始输出及工具轨迹：是否覆盖未查范围、检查实际同机制入口、保留所有成立问题、未修复/失败测试时能否诚实结束、合法差异是否误报、缺口影响是否准确、后继是否审完整增量且复用有效覆盖、充分后是否结束。没有通用计数或召回门槛；旧侧全部检出也记录已有能力，未改善不编造统计收益。method-only fixture 不满足本项生产入口验证。超时/未完成/工具不可用保留首次结果与具体缺口，由原 owner 修复真实执行问题后同例重入，不隐藏失败。

## 9. Canonical 引用、本轮差额与实际未决项

共同规则的唯一可编辑正文是新 managed spec；本批规划只记录迁移和验收，不成为运行时规则副本。专题来源见第4节。RDT 按现有完整知识单元维护必要 requirement/design/test 关系，原 owner 准备隔离完整 proposed definitions，再于 candidate Check 后晋升；不复制共同规则正文或建立长期消费者清单。

Architecture 隔离贡献为 `docs/architecture/contributions/717-review-sufficiency.md`，必要 ADR 候选在其 task-owned proposed targets 中；它们承接共同规则 owner、依赖方向与分发边界。原 Architecture owner 评估完整 proposed/实现后，在 final_integration 写入并读回真实 current，保持稳定 baseline identity，不递增全局版本。Planning 不晋升 shared current。

当前没有未解决产品问题。实际 source 分发、真实模型行为、安装回读与最终质量结果仍待实施验证；不能把本设计写成已经交付的结论。
