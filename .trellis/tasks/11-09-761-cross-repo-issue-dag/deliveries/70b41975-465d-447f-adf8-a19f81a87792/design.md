# D1 跨仓 Issue DAG 设计

## 1. 设计目标、需求承接与内容基线

承接本批 PRD D1-R1..R5、D1-S1..S5 及整体 AC1..AC5。D1 完整交付跨仓编排，不执行真实 Fizz 动议。固定开发基线 B 与 Planning H0 均为 `8c158381b5bdb61fd961cbb89e23c2d1f659c9aa`，来自本次明确的 main；后续内容范围 B..H 与 PR 目标 `castbox/guru-trellis/main` 分开。最终 H 由实际实现/提交确定，不因 main 后续推进而重选 B。

已消费独立 Architecture 正式 `candidate_assessment:baseline_current`，候选 freshness `sha256:3bd5a142d9c5a094a404a44ef09318935f3bee02d1bd72d8d11d0f78d1091655`，结论 `no_architecture_impact`。baseline `docs/architecture/README.md` / `guru-trellis-architecture`，constitution `docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1`，change contract `docs/architecture/06-governance/change-contract.md` 均沿原 authority。修订候选按仓展开既有会话与原事务身份，不新增 scheduler、状态库、semantic owner、authority 或 exit。最终设计仍由原独立 owner 执行 final_plan。

## 2. 当前系统、边界与目标差额

现有 `guru-orchestrate-issue-dag` 是 Codex 显式、instruction-only standalone 包。`references/dag-contract.md` 拥有单仓图、调度、失败与出口；共享 `spec/workflow/issue-orchestration.md` 拥有原生 child、heartbeat、解阻和完成核证。Sequence 消费同一共享方法但拥有自己的单仓串行合同。首次 D1，无前序交付。

本批直接修改 DAG 原输入与其消费者，扩为仓库限定节点；共享方法将目标选择和核证按节点所属仓库执行，Sequence 的单仓选择继续成立。测试载体私有，不随 preset 安装。普通业务仓 workflow 不被协调器替换。

## 3. 来源设计处置（唯一）

Direct Source #761 的既有文件链接是问题证据，不是要求保持旧单仓限制的规范性设计。来源明确规定 AI/Markdown 编排、原生 Codex 工具、单仓兼容、原流程边界和用户信任职责；全部保留在第4–7节。无其它选定规范性来源设计，不创建空处置矩阵。当前共享方法与 RDT 的既有有效语义继续作为实施约束。

## 4. 模块、职责与设计取舍

| Owner / 文件 | 变更与责任 |
| --- | --- |
| DAG `SKILL.md`、`interface.json`、`references/dag-contract.md` | 跨仓成员和图规范化、资格、局部环境阻塞及同 run 恢复；原出口保持 |
| DAG `references/examples.md`、source-only forward cases | 给出跨仓、动议及旧单仓等价调用，解释同号身份和环境路径 |
| 共享 `trellis/presets/guru-team/spec/workflow/issue-orchestration.md` | 每节点 repo/project/base 的事实核验；环境调查/建立/信任、child prompt、heartbeat replay、merge/Completion proof 使用同一绑定 |
| 原 `guru-orchestrate-issue-sequence` | 读取推广后的共享规则，保持一个仓库和严格顺序；只在必要位置说明 per-node 规则对它退化为单仓 |
| README / `MIGRATION-ISSUE-ORCHESTRATION.md` | 用户发现、兼容输入和匹配 provider 更新说明；不复制调度规则 |
| DAG `tests/` | 扩展现有真实 Codex 隔离载体或复用其进程/MCP公共测试支持；事实工具不理解自然语言或替 Agent 选路 |

选择会话中的仓库表和唯一节点键，因为同一仓库多节点共用项目/base，直接消费者是节点创建、恢复与核证。逐节点重复整个环境配置会造成矛盾来源；新增调度脚本/数据库会重复 AI 和原生会话职责，均不采用。统一规范化后只保留原一套调度方法。

## 5. 接口与数据

这是对话合同的兼容增量，不增加 JSON schema、dispatcher command、公共 DTO 或持久状态。

新多仓调用提供 `repositories` 映射，key 为 canonical `owner/repo`，value 可给 `project_path` 与 `base_branch`，缺项由当前项目/remote事实解析。节点为 `{repository, issue, depends_on}`；`issue` 为所属仓正整数，内部会话键为 `owner/repo#N`。`depends_on`、`exclusive_groups` 和 `completion_overrides` 使用同一 qualified ref；canonical Issue URL 等等价输入先在对话规范化。引用不存在的节点按现有 external prerequisite 规则调查，不能静默扩集合。

旧单仓 `repository + project_path + base_branch` 与整数节点/边保留为同一规范图的简写。消费者为实际已有用户调用和 sequence；维护 owner 为 DAG 原包。没有旧 parser 或双调度器。该简写按 #761 的持续兼容要求保留；未来取消需明确 breaking 需求、实际调用迁移和同范围验收，不能在本项退出。

多仓输入中未限定的整数引用仅在唯一仓库上下文可确定时解释；不同仓同号或顶层/节点环境矛盾时先解决该具体选择，不任意取当前仓。所有图元素规范化后再判唯一性、cycle、自边、依赖和资源组。

动议选择提供明确 authority locator，回读正式成员表/绑定和职责。正式成员之外的链接是证据，不自动成为节点。产品总控若负责需求已就绪和最终验收，则初始就绪是前置事实，最终总控节点依赖实际工程完成；不能因工程引用产品需求而制造工程↔总控循环。来源真的规定冲突时停在原 scope/authority owner。

每仓解析得到当前 saved project/primary repo、remote、selected base/source、环境状态；每节点持有其原 child/host/pending/Task/PR 关联，仅在协调会话保留。新多仓 base 明确按仓配置，未给的仓用其 live default；旧单仓 base 保持原优先级。不能把协调仓或一个仓的 main/dev 自动套到其他仓。重复仓库配置矛盾须在受影响 admission 前解决。

## 6. 状态、顺序、正常与失败流程

1. 严格只读 preflight 规范化显式/动议集合，回读各 Issue、仓库流程、已有 owner、环境能力、base、依赖和 accepted completion gates。dry-run 只报告可执行计划和缺口，绝不创建环境、child 或 heartbeat。
2. live/auto 完成原语义 Gate 后，在当前动作边界内先建立实际可建立的缺失环境。检查当前工具 schema/官方 UI、权限与目标路径；可 clone 时使用正确 remote 和不覆盖现存路径的创建，项目登记必须用真实支持入口。不得把 LaTeX project、云环境或 projectless chat 当作本地 repo 项目登记。
3. 建立后通过原生项目列表和 Git 事实回读 primary repo、路径、base、checkout suitability。应用要求项目或 prompt/hooks 信任时，给用户目标和审阅步骤并暂停该环境，不修改 trust/private app state、不代点信任。setup 仅在实际缺失依赖、未追踪运行文件或构建前置有事实依据时按目标仓规则配置，复用已有设置。
4. 无能力或权限时，说明 exact repo、缺失条件及用户步骤：取得 checkout、在 App 新增/编辑本地项目并选择正确 primary folder，完成应用显示的信任审阅；确有运行依赖才到本地环境设置配置 setup。步骤必须适配当前 UI/官方文档，不虚构按钮或 API。约定复查条件后保留同一 run。
5. 初始环境缺口与依赖不等同图结构无效。`continue_independent` 可启动其余已就绪独立节点；`stop_dispatch` 遵守原无新 admission 策略。受影响节点及依赖保持 blocked/waiting；干扰全 run 的真实工具或 authority 缺口按实际影响处理。已有 admitted child 仍观察至安全边界。
6. 原生 heartbeat 记录最小多仓选择/qualified graph 与模型设置，不记授权。按节点所属项目和 selected source 创建 child，先预留 pending 槽位，立即非阻塞观察。全局执行槽位保持。每仓选择一个 integration owner，绑定该仓选定 base 和原合并事务；同仓未知结果及紧邻必要 shared-base closeout 先由原 owner 恢复。不同仓没有硬前驱或实际共享资源约束时，各自按自身 fresh gate 推进合并，不因另一仓结果待定而等待；跨仓仍遵守真实依赖与共享资源约束。
7. 每轮观察/解阻、原事务恢复与 merge/Completion proof 按既有共享方法执行，所有 GitHub/remote/base事实都用该节点 repo/base。一个仓成功不证明另一仓成功。只有前驱整体完成才释放边。
8. 环境补齐后重新列项目、核 primary/remote/base/trust和受影响依赖，恢复同一 run/原 child；未创建的节点首次 admission，已有 child 不重建。全图完成或真正无可推进工作时沿原 settlement 停妥 child/heartbeat并返回原出口。

## 7. 恢复、兼容、迁移与集成

所有 pending、模型、host/cursor、scope与历史事实沿原会话恢复；身份增加 repository namespace，禁止用裸 Issue 号回读跨仓 child/PR。环境恢复不要求已运行 worktree重新满足初始 clean/equal 条件；只刷新真实变动和受影响 gate。

单仓是规范化输入的直接简写，不保留平行执行路径。Sequence 继续单仓；共享 base、prompt、heartbeat与proof规则使用它唯一仓库。公共 skill/exit id 不变。更新须使用完整匹配 provider，经原 installer/`guru-upgrade-tools` 同步 dogfood，保留 Task/session、用户内容、mode并处理 `.new/.bak`；不得手工覆盖受管副本。没有业务数据迁移、发布或生产回滚协议。

官方事实依据已实际读取：[Projects](https://learn.chatgpt.com/docs/projects) 的 primary folder/Git/worktree边界；[Local environments](https://learn.chatgpt.com/docs/environments/local-environment) 的 setup运行与设置入口。当前可见工具支持 list_projects/create_thread，未暴露通用本地项目登记或信任 mutation；具体运行仍必须重新检查工具/UI，不能固化当前不可用为永久能力限制。

## 8. 验证设计

| ID | 要求/AC | 层级、入口与输入 | 预期观察与界限 |
| --- | --- | --- | --- |
| V1 | R1/R3/R4、AC1 | 真实 Agent 显式 DAG 入口、独立 provider/协调仓、多仓同号和跨仓边、不同 base | 实际 create参数、跨仓顺序、每仓交付与完成核证；工具事实不能代选下一步 |
| V2 | R2、AC2 | 同入口动议 authority、正式总控/工程成员与信息链接 | 只选择真实成员，按真实职责/硬依赖推进，无虚构环或自动扩集合 |
| V3 | R5、AC3 | 受控原生能力有创建入口/无入口或权限/需用户信任，以及用户使环境就绪后的同run继续 | 观察能力调查、真实创建/回读、准确步骤、局部暂停及独立进度、信任不代办、同身份恢复 |
| V4 | R1/R4、AC4 | 原单仓 DAG 和 sequence 原生隔离场景 | 原槽位/观察/解阻/顺序/整体完成不回退；已有覆盖可采用，补真正受影响路径 |
| V5 | R3/R5、AC5 | source/installed package validator、原 tools更新与同候选 reapply/drift、私有tests排除 | 对话合同、Codex-only/explicit元数据与实际投影一致，无 sidecar；不是行为证明 |

现有 `tests/run_native_orchestration.py` 已提供独立 coordinator/child Codex 进程、事实 MCP 和外部 trace。优先复用其进程/隔离支持，跨仓状态按仓库+Issue寻址；原测试边界不扩大成生产调度器。host-only 预期不进入 Agent prompt，fixture不按消息关键词推进、不代写 semantic pass。

行为测试为长期源私有回归；必要临时诊断只为具体疑问服务。先完成合同与工具边界，再运行跨仓/环境行为和受影响回归，最后检查分发。核行为轨迹而非计数/exit关键词。证据足够后停止附加实验；设施失败必须保留首失败并重新评估，不能降低断言制造通过。真实 App 后台调度、业务仓生产操作及 Release 全矩阵仍为明确未验证边界。

| V6 | R4、AC1 | 真实 Agent 同入口、两个独立仓ready PR；A原merge结果pending、B自身gate通过 | B在A结果仍未知时沿自身原owner合并；A原事务继续回读且不重复；同仓单owner保留。事实carrier仅供pending状态/原操作结果，不代选路；这是机制收窄差额，原跨仓/动议/环境与单仓事实按实际适用性采用 |

## 9. Canonical 引用、本轮差额与实际未决项

RDT 当前 `docs/{requirements,design,test}/current/issue-orchestration.md` 的 R731/D731/T731 保持；新增跨仓/环境完整定义由原 RDT owner 在 `docs/requirements-design-test-contributions/761-cross-repo-issue-dag/` 提供隔离完整拟稿，经 candidate Check 后 final_integration 晋升到同一能力单元。无 root/current索引登记或无关版本递增。

Architecture candidate no-impact，无 contribution/ADR负担；独立 final_plan、Phase2和committed审查仍判断实际差额。暂无未决产品选择。若实施发现新 owner、持久化、工具权限或机制边界变化，回原 Author/Architecture，不直接扩范围。
