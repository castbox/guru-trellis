# #331 D1 当前知识读写与兼容迁移需求

## 1. 整体来源与术语

整体 authority 是 Task root `prd.md` 的 accepted_scope；本批是 Delivery `d9698141-1db0-444b-a43d-6fe6ccdf6b65` / generation 0，scope_ref 包含 AC331-01..10。完整 Direct Source 为 https://github.com/castbox/guru-trellis/issues/331 （2026-10-18T13:15:08Z）。已读取完整来源及 root PRD 的 R331-01..06、S331-01..09、约束和非目标。

来源角色：Issue 和 root PRD 是要求；两套维护 Skill 的 `references/contract.md` 是已有职责、阶段适用性、隔离贡献和晋升约束；当前 RDT `.109`、Architecture `.100` 与 ARCH-GOV-008/#600 后继是迁移证据；constitution 和 change-contract 是架构约束。未选择知识库产品或新外部服务。当前有效知识、必要关联和稳定标识保持 root PRD 第1节定义。

## 2. 整体与本批目标、非目标

当前查询需要跨版本贡献解释规则，修订也易牵连无关历史。本批全量交付当前知识的组织、按问题读取、一致修订、两层架构来源、兼容迁移、真实对照和安装更新，不只交付导航。

本批覆盖整体 R331-01..06 和 AC331-01..10。保留所有整体非目标：不预选产品/目录、不建立第二 owner/审批/遥测、不以摘要删约束、不改历史或强制升级在途任务、不迁移业务生产仓或重建外部服务、不增加攻击/锁/压力加固。完整多平台 Release 矩阵和其他业务采用另列边界。

## 3. 本批起点、前序结果、依赖与剩余责任

首次 Delivery，无前序交付。开发基线 `main@bdb5185c673c91b2fb5cfc66ffbb33849904a69c`；当前公共 Task 整体 scope 已接受，尚无实施或验证通过结论。RDT 和 Architecture 已有唯一维护方和受管分发。

输入为真实现有版本、稳定追踪、贡献与后继定义。本批须在实施前核对通用基线的实际位置/版本及维护边界，固定多次对照样本和成本判据。来源不可取得时不得冒充外部验证。本批不计划延期功能或验收；未完成任一 AC 就不能报告全量交付。Delivery 合并后仍须整体 Completion、Closure、Finish。

## 4. 本批调用方、场景与流程

| 场景 | 触发与完整行为 | 结果 |
| --- | --- | --- |
| S331-01/02 | 开发 Agent 以能力、行为、接口、职责或稳定 ID 查询；原维护方先判断阶段适用版本，读取当前正文及必要关系，存在后继时区分替代范围与继承条件 | 获得完整适用定义，历史按需追溯，不回放全链作为普通当前查询前置。 |
| S331-03/04 | 正常新增、修改、插入、移动、替换、删除、拆分或合并条目；判断 R/D/T/Architecture 影响并一致修改 | 稳定引用与历史保持，无关对象不重编号。 |
| S331-05 | 两个 Task 分别写隔离贡献，原 owner 依次受控晋升 | 当前正文包含完整一致结果，不永久依赖贡献拼接。 |
| S331-06 | 查询/修订通用栈定义与项目选择、约束、差异 | 明确来源版本、适用关系与不同 owner；项目变更不越界写共享基线。 |
| S331-07/08 | 本仓库迁移代表性正文；旧 Task 继续使用原适用版本，新查询使用其适用版本 | 迁移保持完整知识和追踪，无关共享推进不强制重写。 |
| S331-09 | 缺来源、断链、范围冲突或迁移未完成 | 指明受影响结论与缺口，进入原澄清/repair，原来源仍可读，无虚假完成。 |

## 5. 完整行为、条件与约束

1. 当前知识正文必须保留条件、否定、例外、顺序及跨文档约束。当前、目标、未确认、历史与被替代内容分明。AI 判断适用性，不按日期、编号或排名决定 authority。导航/摘要不能替代必要正文。
2. 定义组织单位、唯一正文、入口和历史边界。查询命中后读取正文与必要关系；维护后入口与正文保持一致。来源缺失或不确定范围沿原维护方处理，不另建事实流程。
3. RDT 保持稳定 `requirement/behavior -> design responsibility/contract -> test strategy/scenario/case` 追踪；结构调整保留前驱/后继。Architecture 的 FOUNDATION/CURRENT/TARGET/GAP/PLAN/ADR/EVIDENCE 分区保持，ADR 不成为当前基线替代品。
4. 并行贡献互不覆盖。晋升输出当前完整定义，保留贡献作为来源。Planning、实施、最终 Check、Review 和晋升都消费新维护合同，不能出现新入口配旧维护方式。
5. 通用栈 owner 保持共享正文，项目 owner 保持选择、范围、约束和差异；本项目修订不自动改通用源或其他项目。外部源记录位置/版本/取得方式和缺口，去敏样本不冒充真实外部采用。
6. 迁移前明确文件、版本、切换条件和恢复；保留原 authority 直到新正文语义、引用和追踪核对完成。历史冲突由 AI 处理，不自动确认。旧 Task 阶段适用版本不强制切换；旧读取路径有真实 consumer、范围和退出条件，不新增无限期双写。公共 API 如有破坏变化，必须明确迁移版本。
7. canonical workflow/Skills/spec/preset 同步 dogfood/installed；匹配更新路径保留用户修改、处理 `.new`/`.bak`。原维护 Skill 拥有语义，脚本只做确定性读取/生成/校验。具体规范性设计承接仅在本批 design 第3节单写。
8. 实施前固定每个样本的必答事实、必要约束、关联修订范围、执行次数及汇总/成本判据。新旧同问题、语义、答案、模型、权限和任务起点；从各自正常入口读，不预载另一方答案。上下文注入和读取指令计成本；必要正文、导航、重复和无关历史分别统计。变更环境/样本须同口径重跑双方。

## 6. 本批验收、验证方式与未决项

AC331-01..08 分别通过正常入口验证当前完整查询、架构后继、一致修订、结构 ID、并行晋升、两层来源、实际迁移、旧 Task 与缺口处理；对应 root PRD 第7节的输入和预期结果保持。AC331-09 要求覆盖全部约定样本的多次真实 Agent 执行，报告正确性、读取量/定位步数、维护改动量、首次失败与修复。历史拼接查询须实际降低读取成本；修订须减少拼接或无关维护；兼容样本只要求正确，错误不能由节省抵消。

AC331-10 验证 canonical/dogfood/installed、reapply、drift 和匹配更新迁移；完整 Release 与业务采用不由本批推定。计划、目录、schema、字符串或链接通过不能替代 Agent 行为证据。现无产品范围未决项；机制、来源定位、样本重复次数和成本门槛由后续 Author/Architecture 在首次实施前完成。

## 7. Canonical 引用与本轮差额

- `trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/{SKILL.md,references/contract.md}`：保留四 profiles、唯一维护方、三层追踪与阶段适用性；补当前正文读取和晋升后的完整定义维护。
- `trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/{SKILL.md,references/contract.md}`：保留独立评估与分区；补当前知识和通用基线/项目投影适用关系。
- `trellis/workflows/guru-team/workflow.md` 与 canonical spec/preset：原 owners 的日常流程接入并分发，禁止复制其内部语义。
- `docs/requirements/versions/current-main-0.6.17-guru.109/requirement-main.md`、`docs/architecture/README.md` `.100`、`docs/architecture/06-governance/rules.md`：实际迁移与前后对照，旧快照保持。
- `docs/architecture/00-foundation/design-constitution.md` 与 `06-governance/change-contract.md`：当前架构约束和检查；实际增量由原 owner 审查/晋升，最终候选再通过 Check 和独立完整 Review。
