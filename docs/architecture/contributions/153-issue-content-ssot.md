# #153 Issue 内容 SSOT Architecture contribution

Identity：`architecture-contribution-153-issue-content-ssot-v1`。状态：`reviewed_candidate`。Task=`153-issue-content-ssot`，generation=`0`，Delivery=`8eb3bf73-9ecf-4406-bde4-8520d37e27c7`。before authority 为 main commit `ed59e851b6c1257bac6316a9571274427e383c93` 的 `docs/architecture/`，stage-applicable baseline=`current-main-0.6.17-guru.99/active`。来源为 [Issue #153](https://github.com/castbox/guru-trellis/issues/153) R2–R4 及 AC2/6/8/9/10。本文记录本 Task 独占的受审差额；实际晋升状态以当前 Architecture Baseline 和原 owner 正式结果判定，不由本文自证。

## 当前与目标边界

当前原 Clarify 已拥有草稿/正文/评论动作与来源判断，Wording/Readiness/CreateIssue 拥有独立审核及创建/回读。原 Author package 的 Planning 来源规则和既有清晰写作规范已落地。差额是四原owners没有共同加载唯一Issue内容正文规范，也缺明确最终正文整合仍有效必要承诺的目的指引。

目标由原 Clarify package 单写 `references/issue-content.md` 和去敏过程示例。创建与修订共用同一规范，四原owners显式实际读取；原受管递归分发安装规范、示例和入口。内容充分性及语义判断仍在Markdown/AI，脚本只验证分发、引用、字节和既有客观事实。路径为 `target_native`，不新增公开Skill/API/DTO/phase、持久化gate、第二范围/语言/来源authority、锁或兼容reader。

原 candidate_assessment 已实际返回 `architecture_impact/target_native`，refs 为 ARCH-FND-002/005、ARCH-DOM-039/055、ADR-022/024。其理由是四现有Issue责任方新增对原Clarify内容规范的可复用读取依赖。本文细化该真实边界。原 Planning `final_plan` 已独立审查当时的设计和贡献，并返回 `baseline_current / reviewed_candidate`；这是 Planning 阶段事实，不代表当前 Phase 2 评估或共享晋升通过。本轮没有新ADR需求，既有decision与当前constitution已足够。

## Required concerns

| Concern | 适用性、处理与边界 |
| --- | --- |
| authority-binding | applicable：Planning purpose3.0 candidate/final分开；当前baseline99与change-contract-v1绑定。before正文可从上述immutable main commit重新读取；不靠当前文件自证已晋升 |
| constitution-binding | applicable：唯一 `guru-trellis-design-constitution-v1/current`。新正文有四个现存direct consumers和live #153必要性；单写/薄引用满足职责内聚，去掉该职责会丢共同规范要求。不开无consumer机制或机械评分 |
| boundary-and-decision | applicable：Issue内容归原Clarify，Planning来源/正文仍归原Author，语言归唯一managed spec，安装归原preset；采用target_native并引用原ADR-022/024，无新增业务状态或接口 |
| owner-and-single-writer | applicable：Clarify维护内容规范，四原owners保留各自semantic判断；Author仅写本Task规划/本文，原RDT与Architecture promotion owners单写共享current |
| compatibility-and-exit | applicable：public I/O/typed exits/确认/写入/回读/freshness/恢复保持，完整matching采用；无双规范、dual-read或新adapter。旧安装沿原更新/reapply采用，不追改历史Issue/Task |
| gap-and-deviation | applicable：不主张关闭/重开现有GAP，不新增或恶化已知偏移。若实施出现owner扩张或第二authority，回原Architecture处理，不以规范文本覆盖真实偏移 |
| parallel-scope | applicable：允许本Task规划、canonical差额与本贡献；不竞争共享CURRENT、GAP/其它Task ownership。shared promotion继续expected-current单写，不在Planning直接晋升 |
| evidence-and-freshness | applicable：候选、实际设计、实现before/after和最终committed范围各由原owner读取。Agent写作/审核、机械、安装和外部结果分开，由唯一Test更新；不复制通过状态或将教学示例当行为证据 |
| review-and-promotion | applicable：Wording后final_plan审真实design/contribution；按ADR-030由独立Phase2评估完整候选和拟写delta，再原owner执行expected-current promotion；最终Check/TaskCommit/committed完整Review覆盖新写入 |

## 验证与晋升边界

原 project descriptor 为 `guru-trellis-architecture-convergence:repository:1`，check id/version 为 `guru-trellis-architecture-convergence/1`，result contract 为 `guru-project-architecture-check-result-2.0`。原 Architecture owner 已独立评估完整实现、受影响消费者及本次拟晋升的薄增量。本文记录受审内容，不替代原 owner 的正式调用、expected-current 写入及实际写入适用性判断；最终 Check 和 committed 独立完整 Review 仍审实际候选。

真实实现责任与验证计划定位本 Delivery design第2–8节及implement第2–3节。实际结果现由[唯一 Test](../../requirements-design-test-contributions/153-issue-content-ssot/test.md)承接：T153-02/03 记录已执行的 Codex V1–V7 写作、原审核修订及真实创建/正文修改回读；T153-04/05 分别记录确定性检查和代表目标的完整匹配安装、重复应用与漂移检查。具体结果、首次失败、修订及证据限制只在该 Test 维护，不在本文复制。

原 RDT owner 已将本任务增量晋升为 `current-main-0.6.17-guru.109/active`，版本与来源见[贡献 manifest](../../requirements-design-test-contributions/153-issue-content-ssot/manifest.yaml)。RDT 晋升不替代当前 Architecture 评估或后续最终 Check、committed 完整 Review、Delivery 和 Task Completion。`formal_fork_source_lock`、其他平台实际 Agent 行为、完整多平台升级/Release 矩阵、正式软件发布及业务仓采用仍未验证；本地候选安装成功不代表正式远程 source-locked 采用。
