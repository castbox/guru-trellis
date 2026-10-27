# D1：v0.7.0-guru.7 准备实施与验证计划

## 1. 输入与引用

整体输入为 [Task PRD](../../prd.md) 的 selected R-01..R-06、R-08；本批行为与验收为 [Delivery PRD](prd.md)；实际机制和唯一来源设计处置为 [design 第3节](design.md#3-来源设计处置唯一)。首批起点 B 为 `ee48ea9a0d339a7a6523ace44b7b5b67e75db870`，没有前序交付。PR 目标 main 与该内容基线分开。

实施前加载 private release contract 全文、`guru-upgrade-tools` 的实际 install/source_locked contract、Architecture change contract 与 RDT current-knowledge 合同、版本/安装文档当前段落、命中 package 测试及其真实消费者。原 Author/Wording/Approval 使用 planning-body 与三份 Delivery 模板。官方 context 只定位实际文件，不创建第二正文。

U-01 使用 design 第6、7节的唯一有界恢复路径。必要来源另含本链 `guru-orchestrate-issue-sequence/references/workflow-defect-recovery.md` 的 Recovery Order §3/4 和 Equivalent Evidence。以下是稳定的待执行责任，不记录阶段进度、用户授权、Gate 结果或候选 HEAD。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与原 owner | 实际文件、动作和可审核产物 | 完成观察 |
| --- | --- | --- | --- |
| S-01 | 原 Author → Wording → 独立 Architecture final_plan → Approval | 按 design 第6、7节审当前稳定规划和直接证据恢复边界；不修改 #684、私有 release contract 或 accepted scope | 原当前规划门禁齐备，未以恢复结论代替方案接受 |
| S-02 | Wording-current final_plan、Approval、用户接受后原 Activation | 保持同 Task/DeliveryKey、selected scope 和 planning_root；每次写入先跑 task checkout boundary | 原公共 phase 合法进入 implementing；不是文件存在即接受 |
| S-03 | 实施 owner，读取当前 consumer | canonical manifest、upgrade-installation TARGET_GURU、两个 output const schema、两个 package examples、命中 test fixtures；`.6→.7` 只改当前目标语义 | 源码目标与消费者一致；Fork/CLI/历史 fixtures 未误替换 |
| S-04 | 公开文档 writer 与原 RDT impact owner | 三 README、项目 public-docs 当前 release/install 段收敛 stable `.6`、target `.7`；真实知识差额只建本 Task 完整隔离提案 | 公开来源真实、同 immutable 来源；历史证据保留；没有空贡献/全局版本 |
| S-05 | 原 TaskCommit/source-acquisition owner；先完成 Planning-selected minimum self-checks | 若 tools 所需 `.7` source 尚未完整干净已提交，走原 early commit；精确 paths/message 与来源资源另在该操作边界展示 | 可证明的完整已提交 source 与 source lock；early DTO 不能冒充 final committed/Review |
| S-06 | 原 tools owner，独立安装边界 | 针对本 Task checkout 的只读 preview、一次 prepare、source_locked invoke、native/postvalidation/preservation；原 installer 生成 installed manifest 和完整受管副本 | target 实际可用、来源与 matching Fork build正确，用户/Task/session/peer状态保留；所有实际 managed changes 回同候选 |
| S-07a | 原 early TaskCommit、原 draft router/Publication；S-03..06 完成 | 将完整实际准备内容及拟晋升 targets 固定为非空 B..Hpre；early 的 push/PR 边界仍由原 owner 独立承接，不将 Draft 当 Ready | 真实已提交范围、实际 managed 内容和来源可核；没有伪造 final committed DTO |
| S-07b | 原 implementation / Architecture phase2 / RDT impact / Check | 正常 begin_check，原 Check 审完整候选与未改 consumers、真实验证及九维；record/check 真实 candidate_checked 语义，暂不 formal invoke | 原候选 Check 判断完整且无阻塞，不写 public final Check |
| S-07c | 原独立 Architecture committed assessment 与独立 Review owner | 同一 B/Hpre/字节执行完整 committed Architecture 和完整 B..Hpre Review；按 design 第7节给直接证据及全部 findings 状态；调用原 delivery_draft_content_review | 两轮之一的完整实质独立审核，零开放 P0–P3；真实出口 draft_content_reviewed，晋升前 public full_review 缺失照实说明 |
| S-07d | 第一轮完整且内容未变；原 Check / integration router / Architecture / RDT | 原 Check formal invoke 产出 candidate_checked，立即交唯一 consumer 合法 rework/串行最终整合；原 owners 审实际 targets、expected-current、trace/subtraction，写入读回；no-change 跳过写入 | 不插假 gate 或空 promotion；真实 after 内容返回同 Delivery |
| S-07e | 原 implementation / Architecture / final Check / TaskCommit / 独立 Review | after return/rebind、candidate/begin_check、正式 Check、精确原提交或合法 clean reentry、HEAD 变化时 fresh Check，以及第二轮完整正式 delivery_branch_review | 真正 public Check/full_review 覆盖最终 B..H；没有空提交或以第一轮 DTO 改名替代 |
| S-08 | 原 publication Architecture 与 Delivery Review | 审当前完整候选、实际验证、scope/剩余 Stage2、安全/部署影响，生成中文具体 Refs-only payload | current readiness；不创建 task-local PR body handoff |
| S-09 | 原 Publish 与原 Merge，各自独立边界 | 推送/绑定/Ready 与 expected-head merge；输出丢失先恢复同操作 | 本批准备 PR 合入 main；#684 仍 Open |

S-09 后由 Task Completion 评整体准备范围，再依原 Closure/acceptance-finish Architecture/Finish/Cleanup 收尾。这些不是本批实现步骤或额外空 Delivery，也不反向成为 Completion 前置。Stage2 在准备和归档合并后 fresh 开始。

## 3. 验证入口、输入与预期观察

每个写入 batch 前运行 `.trellis/guru-team/scripts/bash/check-task-checkout-boundary.sh --json --task .trellis/tasks/10-28-684-release-v070-guru7-preparation`。必须返回当前唯一 Task checkout 且无错误；失败回原 Ensure/Bind owner，不换工作树猜测执行。

| 验证 | 实际入口 / 输入 | 预期观察及对应 AC |
| --- | --- | --- |
| V-01 | 对实际候选版本/const/examples、README 当前段和 source lock 作语义审查；`git diff --check` | D1-AC1：`.7` 目标、stable `.6`、CLI `.5` 独立；候选使用真实远端 SHA；无 whitespace 错误。版本读取只证明映射 |
| V-02 | 用原 managed Python 执行 `python -m unittest discover -s trellis/skills/guru-team/packages/guru-upgrade-installation/tests -p test_contract.py` 和 `-p test_delivery_upgrade.py`；执行前由原测试 owner只选本次命中正常行为 | D1-AC1/3：真实 owner目标选择、输出/schema consumer一致。jsonschema、CLI/Core 或匹配 build 前置缺失时保留阻塞或 SKIP；历史数据与敌对输入不扩为新测试范围 |
| V-03 | `./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`；`./.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json` | D1-AC3：source 与真实 installed package各自有效；不以 source成功替代 target native |
| V-04 | source validator 分别使用 `--platform-root .agents/skills`、`.codex/skills`、`.claude/skills`、`.cursor/skills`；核受影响 package实际字节与 mode | D1-AC3：Shared/三平台声明投影匹配；不是四平台实际 Agent 验收 |
| V-05 | `./trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json`；原 `apply.sh --repo . --platform claude --platform codex --platform cursor`；`check-dogfood-overlay-drift.sh --repo .`；审实际 sidecars | D1-AC3：原 ownership/mode、受管 reapply/drift成立或如实保留 guard stop。历史 Task preflight 不得改造、不能假称成功，也不能代替 S-06 |
| V-06 | 原 `guru-upgrade-tools` 的 preview/prepare/invoke + target自身 runtime resolver、installed validator、真实 native-entry 和 preservation | D1-AC2：完整 source_locked provenance/build、target installed revision/CLI/managed set正确；旧 Task 诊断不转换历史数据；同操作恢复由原 owner执行 |
| V-07 | S-07a..e；第一轮固定已提交范围、完整九维/独立Review与真实验证，原 candidate_checked→最终整合/no-change→after 重绑→正式质量链 | D1-AC4：完整差额、未改 consumers、两轮独立完整审核及零开放 findings；第一轮只直接证据/真实 early 出口，第二轮真实 public Check/full_review；最终 gate不消费 candidate-only DTO |
| V-08 | 原 Delivery Review/readiness/Publish/Merge；读取 live PR/body/expected head | D1-AC5：真实中文 Refs #684，无关闭关键字；验证、安全、部署/配置影响与 Stage2边界完整 |

这些验证均未在本计划中预填 pass。工程结果只有在定义、依赖、输入、工具链、环境、参数和预期仍适用时由当前 owner采纳；semantic Gate始终由当前 owner实际判断。没有覆盖需求所要求的层次时，只能报告对应缺口。

不在准备 Task 运行 Stage2 fresh exact-candidate、focused/existing predecessor安装、退休清退、secret scan、tag/smoke/Release或两选定目标的发布后收尾。它们由 release Issue保留。完整累计多平台矩阵、所有 native hosts、真实业务升级、Himora/生产同因证明未覆盖。

## 4. 停止条件与适用回退点

第一轮缺少固定已提交 B..Hpre、完整九维/独立 Review、真实测试或存在开放 P0–P3 时，停在原 Check/Review，不得进入整合。Review 发现问题后，原 Check 以实际 findings 重审并走 implementation_required；修复、原 early TaskCommit 新提交后刷新当前候选和受影响完整审查。直接证据不能补造失败验证或缺失语义判断。

必要 source/build/API缺失、source dirty/lock不匹配、未解决 managed conflicts/sidecars、native或preservation失败：停原 tools owner；只使用同 operation recovery，不再 prepare新计划，不手改 provenance，不自动转全量安装或旧Task迁移。rollback为原 owner单独审核的 write，不借用安装确认。

scope、来源义务或机制实质变化返回 Clarify/Author/Architecture；只有实现或断言错误则由实施/Check修复。FAIL、SKIP、stale、未知结果不能成为后续pass；原 mutation结果未知时先同操作读回，避免重复提交/发布/合并。

本批无业务数据迁移、生产部署或 tag/Release mutation，故不新增生产回滚协议。无关 dirty/untracked、历史Task/archive/workspace/session/user config、peer工具和其它worktrees始终保留。

## 5. Delivery Policy（唯一）

Policy=`full`，针对本 Task 选定的业务准备范围 R-01..R-06、R-08。一个 Refs-only PR交付版本/公开来源、真实Task dogfood、命中的受管内容及知识收敛，并以原 owners完成可执行的完整质量链和双独立Review。没有把未完成的同批实现留给后继空Delivery。

本批独立交付条件为 D1-AC1..AC5全部满足、实际候选和final gates匹配、准备PR被expected-head合并。Delivery合并不等于 Task Completion；整体Completion随后核R-01..R-06及R-08。R-07的Closure/Finish/Cleanup是Completion之后的独立生命周期责任。

剩余 release Issue责任为准备/归档合并后的唯一fresh candidate、全部Stage2 gates、tag、smoke、正式Release、两个真实本地目标收敛及最后Issue关闭；owner为当前release owner与其调用的原local tools owners。这些不是本准备Task的延期验收。U-01 仅处理正式结果记录前置，不能降低本批两轮完整实质审核或第二轮正式质量结果要求。

## 6. Docs SSOT Plan（唯一）

strategy=`delta_first`。真实可见文档差额为三README和项目public-docs的stable/target/provider/CLI映射及本次能力来源。Author/公开文档writer维护这些命中段；实现前读取完整当前条件，历史验收与cutoff保留，不顺手清理无关旧章节。

RDT原writer为 `guru-maintain-requirements-design-test-ssot`。命中authority为 `docs/requirements/current/knowledge-maintenance.md` R331/R638/R648，`docs/design/current/knowledge-maintenance.md` D331/D638，`docs/test/current/knowledge-maintenance.md` T638。它们的行为没有因版本递增自动变化；原task_impact_sync从实际完整候选判断no-change或真实isolated proposed delta。no-change不创建空manifest/贡献或全局版本。

Architecture沿 `docs/architecture/README.md`、当前constitution和change-contract；独立candidate_assessment无影响，因此不预建Architecture contribution/ADR。真实新影响返回原owner，不能沿原no-impact结果继续。

直接consumers为原RDT/Architecture最终整合、当前Check和完整BranchReview。真实 shared delta 在第一轮完整实质审核及 candidate_checked 之后，由原 owners 串行 reconciliation/promotion 并 readback，再纳入 after candidate 和最终 Phase2。无差额时原 router 跳过写入并保留 return/rebind；不制造空贡献、空晋升或全局版本。delta_first 不授权提前修改 shared authority。
