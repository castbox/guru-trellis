# D1 跨仓 DAG 完整能力需求

## 1. 整体来源与术语

整体 authority 是本 Task 根 `prd.md`，当前 accepted_scope revision 为 `sha256:52097a2ff17bf73768b3230ea60aa4aba15da7a938c6f120d3f6c7849403b4a9`。本批 scope_ref 选择 R1–R5、AC1–AC5；planning_root 是当前 Delivery `70b41975-465d-447f-adf8-a19f81a87792`。Direct Source 为 [Issue #761](https://github.com/castbox/guru-trellis/issues/761) 完整正文；没有额外选定来源设计。

节点身份、协调者、provider、业务仓的定义由整体 PRD 第1节单写。跨仓引用须能够区分不同仓同号 Issue；环境 readiness 包括项目、正确 primary 仓、worktree/base 与实际信任状态，不等同目录存在。

## 2. 整体与本批目标、非目标

D1 完整交付从其他仓会话发起多仓 Issue DAG 的能力。现有单仓输入不能表达跨仓成员与依赖，本批使各节点进入其所属仓流程并按真实完成证明推进。覆盖整体 R1–R5 和 AC1–AC5，没有另行延后的产品责任。

保留整体第3节非目标：不执行 Fizz 动议，不增加调度器、数据库、协调 Task、授权状态或非常规加固，不发布软件版本。共享 sequence 仍为原单仓串行入口。

## 3. 本批起点、前序结果、依赖与剩余责任

首次 D1，无前序 Delivery。固定开发基线 B 为 `8c158381b5bdb61fd961cbb89e23c2d1f659c9aa`，来自本次 main 选择；PR 与完成目标为 castbox/guru-trellis/main。现有独立 worktree 和正式 Task 已建立。单仓调度、原生观察、解阻及 whole-Task 核证方法继续复用。

本批依赖当前原生 Codex 项目/会话/心跳能力及目标仓自己的 workflow；环境缺口必须产生 R5 的具体建立或用户步骤。合并后仍由原 Completion/Closure/Finish owners 核整体验收、关闭来源和归档；Delivery 合并不代替整体完成。

## 4. 本批调用方、场景与流程

| 场景 | 条件与输入 | 必须观察的结果 |
| --- | --- | --- |
| D1-S1 多仓同号 | 任意协调/provider 仓，两个业务仓都有 #7，提交跨仓依赖 | 两个独立节点及正确仓/base/project 的执行；前驱完整完成后才启动后继 |
| D1-S2 动议 | 当前动议正式绑定产品总控与工程项，另有信息链接 | 回读职责和验收得到真实成员及依赖；不从链接或仓名强加工作/顺序 |
| D1-S3 环境可建 | 仓库缺项目或可运行 checkout，但当前存在受支持入口且权限足够 | 按实际操作边界建立，回读项目与 remote/primary/base，信任仍独立核验 |
| D1-S4 环境待用户 | 无创建入口/权限，或应用要求用户信任 | 暂停受影响节点和依赖，给具体目标与用户操作；按 failure policy 推进独立工作，条件满足后恢复同 run |
| D1-S5 兼容恢复 | 旧单仓整数输入，或已有跨仓 pending/child/PR | 单仓确定归属；跨仓恢复按仓库+Issue 及原 child/host/base，不重复创建、不串仓 |

## 5. 完整行为、条件与约束

- **D1-R1 → R1**：每个节点和边使用无歧义的仓库/Issue 身份；重复、外部前驱、self-edge 和 cycle 的判断沿用现有语义，跨仓同号不当重复。旧单仓的 repository/project_path/base_branch 与整数节点保持可调用。
- **D1-R2 → R2**：显式集合与动议正式绑定集合均可进入同一 DAG。成员、产品总控和工程职责以当前来源为准。工程依赖和总控最终验收不能被机械转换成相互依赖的环；真实冲突回原 authority，普通信息链接不入集合。
- **D1-R3 → R3**：为节点解析所属仓的已保存 Codex 项目及正确 primary repository，选择该仓实际 base。子会话从适当源创建独立 worktree，PR、merge ancestry、source Issue、Task Completion 均按该节点仓/base 核验。发起会话或 provider 路径不决定目标仓。
- **D1-R4 → R4**：保持现有并行槽位、pending 预留、排它资源、failure policy、轻量观察、主动解阻和原事务恢复。硬前驱完整完成才释放边；不同仓的独立工作可继续。共享资源事实可限制并行，不凭同仓或文件重叠制造依赖。
- **D1-R5 → R5**：环境缺口先检查本轮原生工具/受支持 UI 与权限。能建立则执行并回读；缺入口或权限时明确 repo、缺口、具体用户步骤和复查条件。信任由用户审阅，禁止通过修改私有 app state、信任配置或代点确认替代。setup 只在目标运行前置实际需要时配置，不默认新增 hooks/scripts。

不引入公共结构化 schema 或持久运行状态；本批 design 第3节记录对当前来源设计的判断和兼容选择。各仓自己的语义门禁、操作边界与原 Skill typed exits 保持。

## 6. 本批验收、验证方式与未决项

整体 AC1–AC5 全部由本批承担，输入、入口及预期观察沿整体第7节，本批具体观察覆盖上表五个场景。真实 Agent 必须从公开 DAG Skill 入口执行多仓同号、跨仓边、动议职责、环境建立/用户阻塞/信任/恢复；观察实际工具参数和终点，不用字符串断言证明行为。

保留单仓 DAG 及共享 sequence 定向回归。验证源码结构、实际 managed 安装/reapply、dogfood drift 与 sidecar/mode；隔离工具边界和真实 App 证明分开报告。不要求生产 Fizz 或完整 Release 矩阵。

需求阶段没有未决产品问题。方案需调查当前 Codex native API 和官方项目/setup 文档并给出可执行环境路径，不能虚构创建或信任 API。

## 7. Canonical 引用与本轮差额

- Requirements `docs/requirements/current/issue-orchestration.md` R731-01..06：保持整体完成、主动解阻、合法恢复和真实行为验证；增加跨仓节点与环境就绪要求。
- Design `docs/design/current/issue-orchestration.md` D731-01..05：保留共享方法单写、包本地调度与原生事实工具，推广 per-repo 身份/base/环境消费。
- Test `docs/test/current/issue-orchestration.md` T731-01..07：采用既有真实 Agent 载体及证据边界，增加跨仓身份、依赖、成员和环境恢复的独立可观察行为。
- Architecture 从 `docs/architecture/README.md` 进入当前 baseline；遵守 `00-foundation/design-constitution.md` 和 `06-governance/change-contract.md`。本轮候选经独立 Architecture 判断，不以已有共享机制证明其适用性。
