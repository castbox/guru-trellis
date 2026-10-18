# 当前适用知识的读取、修订与晋升

知识单元：`RDT-REQ-KNOWLEDGE`。状态：`current`。前驱 RDT `.109`、Architecture `.100`；固定迁移源 Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`。候选正文须经原 owners 晋升才进入共享 authority，不因目录名 current 自动生效。

## 唯一 authority 与完整知识

`REQ-007/019/027..035`、`BEH-007` 保留身份，并按下述阶段适用性和 ADR-030 替代旧冲突片段。RDT 由唯一 `guru-maintain-requirements-design-test-ssot` 管理一个 Requirements/Design/Test repository authority。每个活动 requirement/behavior 均有 owning design responsibility/contract 和至少一个 test strategy/scenario/case，双向关系保持。Architecture 独占项目 FOUNDATION/CURRENT/TARGET/GAP/PLAN/ADR/EVIDENCE、constitution/决策/owner/兼容/历史；RDT 只继承其公开 locator/version/status，不读 private state，不复制架构正文。task-local PRD/design/implement 是 Task planning，不能冒充 repository authority。

`R331-01 / BEH331-01`：读者先按问题、Task、阶段和候选选择真正适用来源，再按能力/行为/接口/职责或稳定 ID 到完整单元。当前有效要求、已接受目标、未确认、历史和 superseded 内容分开；target 不冒充当前实现。读取必要关联（条件、否定、例外、顺序、依赖、设计、测试、Architecture），不无限展开所有链接。导航仅存 identity/alias/status/locator/关系，不是另一份业务摘要。搜索排名、日期和编号不决定 authority，命中标题或摘要不替代正文。解释旧决定或原因时按需读历史；普通当前查询不要求重放全部版本/贡献。

当前单元是原 owner 在已声明能力范围内合并的完整定义，历史 contribution 保留来源责任；晋升后后续查询不能仍靠贡献链补出遗漏规则。精确 public API/schema 仍由 canonical package 单写，单元展开能力行为并指向必要完整接口，不复制接口成第二来源。单元 revision 可由完整 Git snapshot 定位，避免维护无限重复版本正文。

## 一致修订、身份与隔离

`R331-02 / BEH331-02`：原 maintenance owner 先读变更和受影响完整单元，判断 R/D/T/Architecture 关联、新增/修改/替换/删除/拆分/合并，再由对应 owner 写本 Task 隔离贡献。正常并行 Task 使用不同 `docs/requirements-design-test-contributions/<TaskId>/` 和 Architecture contribution locator，不互写对方，不竞争 shared current。必要时可由原 owner 判断窄 direct sync，但不能由 caller 自封同步。

展示顺序、移动或插入不改变既有身份。替换/删除保留旧 identity 的变更关系、历史和 successor；拆分/合并给真正新对象新 identity，保留前驱及各继承/替代范围。无关 ID 不批量重编号。只更新真实相关对象；无影响层说明依据，不为形式一致改全部文档。来源冲突由 AI 判断，不能脚本按最新 wins。完整 trace 是 requirement/behavior → design responsibility/contract → test strategy/scenario/case；关系表存 identity/locator，不重复来源 prose。

## 四 profiles、日常闭环与晋升

RDT 的四 profiles 保留：bootstrap_foundation 建立/复用/迁移兼容三层 authority；task_impact_sync 对批准 delta 判断 no-op、isolated contribution、窄 direct sync 或 revision；promotion 审查 contribution、subtraction、trace、版本历史与 Architecture inheritance；repair 修复具体 authority/navigation/version/迁移缺陷，不扩需求或改无关历史。

Planning、实施、最终 Check、Branch Review、Delivery Review、Completion、Finish 都实际加载阶段适用的完整正文和必要关系。Planning 选择唯一 ssot_first、delta_first、bootstrap_or_repair_docs 或 no_docs_update_needed；Phase2 执行该策略。delta_first 的最终 Check 之前完成 reviewed contribution 合并；Branch Review 核验 reconciliation，不能首次补晋升。

`R331-04 / BEH331-04` 与 `R600-01..06`：fresh 独立 Phase2 Architecture assessment 先读晋升前 authority 和完整 tracked/untracked candidate/proposed targets，再由原 owners 对真实 live expected-current 晋升。后继正文吸收所有受影响仍有效条件与新 delta，并更新薄入口/关系；实际写入后核对适用性。随后完整最终 Check、精确 commit、fresh committed Architecture/完整 Branch Review。无变化不制造 ADR/贡献/阶段，不能拿新 CURRENT 自证旧约束。finding 修复/义务变化回最早 owner；只改引用/状态仍须原合同下覆盖最终候选的正式结果，不循环记录最终 Review SHA。

两个贡献先后晋升时，第二个 owner 比较真实 current 和自己的 base，保留第一个的全部有效定义再合第二个，不能覆盖成第二份 delta。expected-current mismatch 回原 promotion/review，不自动判所有旧 Task 过期。partial/output-loss 由原 owner 读取同一明确 intent，仅完成 pending targets；真实冲突或不唯一停止，不另建状态机。

## 阶段适用版本与实际变化

`BEH567-02/03` 保持，窄替代旧 `REQ-034` 的“一切 current 前进强制 sync”。原 owner 选择 Task plan/候选/阶段适用 RDT 和 Architecture，可以用 immutable version 或 Git history。无关共享 CURRENT、navigation、archive、remote ref 或 tool 前进不替代它，不强制贡献重写、业务门禁重跑或 branch 同步。明确适用于该 Task 的规则、失效假设、scope/dependency/solution 改变，仍回原 revision/assessment。promotion 自己仍读 live current 并校验本次写边界，两种时钟不能混淆。

`R578-01..04 / BEH578-01..04`：当前 semantic judgment 和工程命令事实分开。每次 owner 都新作当前完整判断并绑定当前 invocation；合法、可核查且实际 check定义、依赖、参数、预期、工具链和环境仍适用的工程事实可跨 owner/stage 使用。unknown/missing/真实变化才重跑受影响命令。不能借旧 semantic pass、同路径或相同 code tree 免当前判断，不读退休 private checkpoint 或造 cache/ledger。采用结果说明原来源和适用依据，不声称自己执行。

## Architecture 维护的既有判断边界

原 Architecture owner 在 Planning、合格的 implementation discovery、Phase2、独立 committed Branch Review、publication 和 acceptance_finish 判定阶段适用性。项目正文唯一声明 constitution locator/version；Guru 只消费其五个 identity/short names，不复制原则正文、逐项评分或 verdict。无 Architecture 影响保持 no-impact/no_change 快速结果，不制造 contribution、ADR 或 project-check负担；有影响必须恰好选择 target_native、legacy_boundary_convergence、dedicated_refactor_slice 之一。

项目 change contract 必须承接真实 requirement/behavior、baseline/constitution、domain/integration/decisions/GAP、required concerns、current/target owners、single-writer、compatibility exit、parallel scope、偏离/删除条件、design responsibility、before/after、checks/evidence和promotion写边界。普通Task只写本方contribution；改变decision、原则例外/权衡、GAP lifecycle、owner/single-writer或compatibility exit才需要ADR candidate。Phase2读取完整candidate，Branch Review对完整已提交范围独立重算，不能拿前次pass替代。

项目check的适用性、规则/decision/GAP关系、结果层次和证据缺口由该owner新判。适用blocking check失败或未验证不支持baseline_current；非blocking缺口明确保留，不用于关闭GAP或批准例外。新/恶化责任偏移回fitness_regression；authority冲突回architecture_conflict；缺必要合同/来源回contract_incomplete或原bootstrap/blocked；stale本次晋升写边界回sync_required。具体descriptor/DTO仍由Architecture canonical合同拥有，RDT不复制成第二判定器。

## 两层 Architecture 来源

`R331-03 / BEH331-03`：通用技术栈 baseline 有独立正文 owner 和明确 source locator/version；项目 Architecture 维护选择、范围、约束及差异。项目变更不授权修改共享定义或升级别的项目，项目私有 Task/分支/配置不能进入公共源。通过原 Architecture maintenance Skill 分别在各自边界写作，不引入第二 owner。真实 generic source 和项目投影分别由 [technology baseline](../../../trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md) 与 [stack selection](../../architecture/00-foundation/stack-selection.md) 定义；本层不重复其技术选择。

外部源须明确位置/版本/取得方式和缺口。来源明确的去敏副本/临时 fixture 可验证读取合同，不能冒充外部采用。缺必要源、断链、authority conflict 或未完成迁移时，说明具体对象、缺口与受影响结论，保留可读原源，进入原 Clarify/repair/blocked；推断不成为 confirmed/current。

## 迁移、退出与分发

`R331-05 / BEH331-05`：切换前明确 predecessor/版本/文件、稳定关系、替代范围、保留条件、失败恢复和 legacy inventory。完整性/追踪/真实场景核对未满足则旧 shared entry 保持，新正文 proposed，不宣称 current。正常恢复不改旧快照；晋升后 correction 走原 repair/新 successor，不回填不可变版本。

旧在途 Task 的实际 planning/gates 仍读原适用版本/Git authority；兼容只保留必要旧读取，不向旧 current 双写新能力。Task 完成、合法 Reactivate 改选或真实依赖改变后，该 Task 的旧普通读取退出；历史追溯可永久保留。尚未迁移主题必须明确走旧完整源，不能在导航中写已完成迁移。

canonical workflow/Skills/spec/preset 是长期源；dogfood 与 installed 是受管投影。matching installer/update/reapply 迁移必须处理用户修改、`.new/.bak`、mode 与漂移，不将 source 改动等同业务安装采用。公共 I/O 保持兼容；破坏变化需新版本/迁移。完整 Release/Upgrade matrix 由其专门 scope 负责，普通知识变更只做本 accepted scope 的最小可靠证据。

`R331-06 / BEH331-06`：实际采用必须有真实 Agent 同问题、同语义/预期、同模型/权限/起点、多次 old/new 对照。样本/必答事实/关联修订范围/次数/成本判据在实施前固定。导航/必要正文/重复/无关历史及注入/工具指令均计成本；总 input 与 cached 分列。报告逐样本正确性、读取量/步数、维护改动量、首次失败和修复。历史拼接查询须有实际收益；修订减少拼接或无关维护；兼容只要求正确。不能以更少字节抵消错误或漏条件，不能用静态链接/schema 或一次成功代替行为验证。

## 关系与完整规格

设计：[`RDT-DES-KNOWLEDGE`](../../design/current/knowledge-maintenance.md)。测试：[`RDT-TST-KNOWLEDGE`](../../test/current/knowledge-maintenance.md)。[迁移追踪](../../requirements-design-test-contributions/331-current-effective-knowledge/traceability.md) 定义来源和未迁移范围。原 [RDT Skill](../../../trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/SKILL.md)、[Architecture Skill](../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/SKILL.md) 和本轮共享 current-knowledge 合同拥有各自公共规格与方法，不复制 private artifact。
