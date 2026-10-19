# Task / Delivery 生命周期测试策略

知识单元：`RDT-TST-LIFECYCLE`。状态：`proposed`。固定前驱 RDT `.112` / Git `b470580d4f79f61c66d72db97861fe1564b5e746`；更早迁移来源按该前驱保留。需求：[RDT-REQ-LIFECYCLE](../../requirements/current/task-delivery-lifecycle.md)；设计：[RDT-DES-LIFECYCLE](../../design/current/task-delivery-lifecycle.md)。本单元拥有场景/预期和结果定位；历史结果不等于当前候选通过。

## 策略与完整性

以真实公共owner链验证合法正常路径、普通缺失/过期/输出丢失及完整候选。AI审查职责、因果关系和门禁充分性；schema、测试或脚本只证明其客观层次。不制造恶意artifact/伪造hash/对抗绕过、未要求的锁/压力/崩溃负例。实际Agent、runtime/package、source/dogfood/installed、provider/live、Release证据分别说明。

`TST-002/003/004/007`、`CASE-001/002`、`SCN-001..004` 的 orchestration/AI-script/compatibility身份保留；其旧Task级开发入口和Finalizer顺序已由R531/ADR-030替代，不把旧断言作为当前预期。当前完整场景如下。

| 稳定scenario/test identity | 正常起点/动作 | 必须观察 |
| --- | --- | --- |
| T531-02 / R531-01/02 | 同Task建立D1、独立D2，分别写规划 | key/root/文档和历史分开；Task scope持续；唯一Author、独立Wording/Architecture/Approval，Activation是真公共Planning writer。 |
| T154-02/03/04 | 全量、partial、后继和返工；详细来源及规范性承诺 | 真实完整来源被读取；Task与slice正文分明；设计处置唯一且保条件；Policy/Docs Plan不重复；下游实际消费正文。 |
| T531-03 / R531-03 | 同slice scope/方案变化、部分/全部撤回，各真实stage | 原Clarify及最早stage合法rework，身份/PR/history保留；stop/release不冒充delivered；独立工作不因局部provider缺口阻断。 |
| T531-04 / T530-01..05 | dirty精确提交；clean既有候选freshCheck后首次Review；普通stdout loss | 真实内容进入commit，clean零空/重复commit；Review输入绑定实际H；完整独立Architecture/Branch Review；旧gate不冒充current。 |
| T600-01/02/03/04/05/06 | authority变更的完整tracked/untracked候选与proposed targets；无变化控制 | 独立before/after→原owners晋升→写入适用性→最终Check→commit→committed Review；无变更无ADR/空阶段；mismatch/partial/conflict走原owner。 |
| T535-01..04 | 完整Review无候选，或非空全rejected | 真空集[]与分类区分；完整维度/Docs/Architecture/freshness及route仍审，不凭空集自动passed/ready。 |
| T531-05 / T557-01..04 | 原Publish/Merge成功后投影/输出丢失；正式发布后人工双亲merge | 实际成功读回且零重复副作用；历史事实不等新gate；actual head/CI/delta交Completion；不执行第二merge。 |
| BEH567-01..05 / 该源T567链 | 各阶段固定B/H；无关target前进；实际冲突/依赖同步 | 固定候选正常前进、默认零Reconcile；仅真实触发固定一次target，恢复同Delivery，不追赶、不重放无关门禁。 |
| T531-07 / R531-07 | 完整匹配安装及显式旧数据迁移 | canonical/installed/native/reapply一致，旧公共/私有迁移分owner；source修改不证明旧业务/production已采用。 |

## 执行入口与结果消费

完整精确测试命令由受改package的现行tests和其owner选取；公共profiles/DTO以[canonical packages](../../../trellis/skills/guru-team/packages/)为准，不在此固定易漂移计数。历史结果在各原contribution的唯一test中：[#531](../../requirements-design-test-contributions/531-task-delivery-lifecycle/test.md)、[#154](../../requirements-design-test-contributions/154-planning-body-contract/test.md)、[#530](../../requirements-design-test-contributions/530-clean-committed-reentry/test.md)、[#600](../../requirements-design-test-contributions/600-promotion-before-check/test.md)、[#557](../../requirements-design-test-contributions/557-manual-merged-delivery-recovery/test.md)。它们保留原candidate、首次失败和未验证边界，不能由本轮链接宣称重跑。

本轮迁移/查询证据是 T331-01/V331-A、T331-05/V331-E及相关新旧对照；实际全部结果唯一写 [#331 test](../../requirements-design-test-contributions/331-current-effective-knowledge/test.md)。测试owner逐次判断完整性，保留首次失败与修复；当前本文只定义预期。Whole Task实际完成另由Completion，Release完整矩阵和外部业务采用不由此推定。

## #636 早期反馈的新增完整场景

| Test identity | 正常起点与实际入口 | 必须观察与证据边界 |
| --- | --- | --- |
| T636-01 / R636-01/03 | 已激活候选尚无完整 Check/重型结果，经公共 TaskCommit 早期 prepare/invoke，再经原 Publication | 真实非空提交和 Draft 先于完整审核/重型检查；精确 paths/消息/敏感检查/目标正确；正文列待完成，缺最终 gates不能 Ready/Merge。fixture不代替真实GitHub Draft。 |
| T636-02 / R636-03/04 | 同 Draft 发布修订或真实冲突解决候选；同一 Ready PR需先发布未审候选 | 同 PR/key保留；退 Draft 在push之前，最终审核未完成时保持 Draft；完整新证据后再 Ready；旧readiness不能放行新HEAD。 |
| T636-03 / R636-04/06 | 正常 commit、create、push、edit、Draft/Ready已成功但正式输出丢失，从原 producer同调用恢复 | 实际 commit/PR/HEAD/payload/state读回，同操作只补剩余步骤，无第二commit/PR或重复已成功动作；失败/SKIP不变为green。不手改hash/伪造artifact构造安全负例。 |
| T636-04 / R636-02/05 | Draft后固定B/H，独立Agent内容分析与HEAD命中命令并行；期间target前进、冲突/无merge ref/CI未触发 | 审核固定B/H完整内容，HEAD验证仍推进，T/M组合结果分开保留原因/恢复条件。早期结果不写full_review；正式独立Review仍真实Check predecessor。fixture只证明调用/候选逻辑，不证明业务CI。 |
| T636-05 / R636-04/06 | 当前候选准备最终readiness/Ready/Merge；full/partial、默认/非默认目标对照 | 全部 Delivery Refs-only，Closure独占整体关闭；Draft/Ready/一次merge不证明Task完成；实际候选拥有全部适用gates。 |
| T636-06 / R636-07 | matching packages/workflow/runtime、声明平台投影及本仓dogfood的apply/reapply | public input/exit/唯一consumer匹配；installed实际行为、drift、可执行mode和sidecar逐项正确；source parity不代替现有业务采用。非完整Release矩阵。 |
| T636-07 / R636-06/07 | implementing/checking/reviewing/publishing在途任务、旧commit receipt与旧Publication pending/Ready事务 | 由原owner一次性恢复/迁移同key/PR、已执行动作和真实gate义务；无伪造pass、runtime双读或新建Task/Delivery。 |

## #636 当前执行事实与未验证边界

以下最小自检在首次早期提交前由独立 implementation Agent 实际执行：

```bash
TRELLIS_DELIVERY_API_COMMON="$PWD/.trellis/scripts/common" bash trellis/skills/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/packages/guru-create-task-commit/tests -p test_early_draft.py -v
TRELLIS_DELIVERY_API_COMMON="$PWD/.trellis/scripts/common" bash trellis/skills/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/packages/guru-publish-task-delivery/tests -p test_early_draft.py -v
bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
```

结果依次为2 tests/exit0（最后一轮5.221s）、3 tests/exit0（17.577s）、source接口图passed。前者经公共wrapper实际完成无Check精确commit、同receipt输出恢复、clean re-entry零额外commit，并证明早期BranchReview不写full_review、target前进不改变固定B/H。另一个case验证普通参数误选：prepare拒绝clean re-entry profile，保留dirty与HEAD且不写candidate；early prepare的预计出口为draft_committed。Publication通过production provider-port fixtures证明Draft创建输出丢失恢复同PR、ensureDraft先于push、状态转换输出丢失恢复、缺readiness不Ready、Draft不写PublicationFact；原公共Check/Review/readiness wrapper与stateful provider ports完成Ready→Draft→Ready，合法rework保留Planning并清除check/full_review/readiness，新HEAD拒绝旧gate。接口图结果只证明当前schema/注册/consumer客观闭合，不证明语义充分或整任务通过。

后续实际命令、首失败、修复及结果继续在本节单写；current 测试单元只承接策略并定位本结果，不复制执行日志。完整 Release 矩阵和 Backend CI 改造不在本 Task 范围。

### matching 安装的首次失败与恢复

普通 `bash trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 在任何preset写入前返回 `upstream_delivery_migration_required`，原因是本仓保留的历史Task记录。当前Task和session未改变。按原tools-only owner准备matching local_candidate；实际CLI/Core为0.7.0-castbox.5，公共工具目标文件与当前字节一致，保留本仓config，平台为claude/codex/cursor，不迁移Task或归档。

原 `guru-upgrade-tools/scripts/invoke.sh` 完成公共tools步骤后返回 `resume_required`。同操作的原installer详细诊断显示package/overlay无冲突且无sidecar，installed graph因五个Draft router缺少`guru-workflow-target`声明失败。原rollback公共入口随后真实返回`rolled_back`，installed_version为0.7.0-guru.5；Task/archive/session与原pointer的2,701个保留文件字节/mode未变。没有编辑recovery或放宽validator。修正五条canonical声明后再准备新的matching操作；首次失败不计通过。


五条target声明修正后，source校验与原installed workflow图检查均通过（36 invokes、195 exits、129 targets）。新的matching `guru-upgrade-tools` 操作真实返回`tools_upgraded`，installed_version=0.7.0-guru.5、unverified=[formal_fork_source_lock]。原owner已运行目标自己的installed validator、native continuation和隔离内存公共operation probe。再次对照2,701个保留文件无变化；无sidecar，workflow与canonical一致。

随后独立执行 `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 首次失败：仅缺`.trellis/spec/workflow/task-delivery-early-draft-migration.md`。canonical新增locator未加入原installer的显式managed asset映射；原实现owner补齐该映射，保持现有安装机制。此时仅installed工具门禁通过，dogfood drift尚未通过，不计T636-06完整验收。


原installer增加该spec的唯一managed映射后，临时target经原`copy_managed_spec`首次installed、再次unchanged，字节一致、无sidecar，13份canonical workflow spec均有映射。第三次matching公共tools操作真实返回`tools_upgraded`（0.7.0-guru.5，formal_fork_source_lock未验证）。随后dogfood drift命令exit0，实际workflow、选定平台投影及全部workflow spec与canonical匹配；没有`.new/.bak`。全部2,701个保留文件再次无变化。普通apply的历史迁移检查保持；成功安装使用原tools-only入口及实际公共tools operation证明，不改Task/归档或伪造迁移凭据。

以上属于本地 matching 工具与最小分发验证。正式源锁、现有业务采用、完整多平台 Release 矩阵仍未验证；完整 Task 质量门禁与 T636-01..07 整体验收仍待后续实际链。


### 真实早期提交、Draft 与固定候选审核

原 TaskCommit 公共入口实际返回 `draft_committed`，提交 `0ca000aff57159323d1c84e4ba9dbc001ab95fdc`，parent 为固定 B `b470580d4f79f61c66d72db97861fe1564b5e746`。341 个实际提交路径与精确计划一致，提交后工作区干净。原 Publication 公共入口随后返回 `draft_published`，创建 [Draft PR #642](https://github.com/castbox/guru-trellis/pull/642)，远端读回同 head、base=main、OPEN、isDraft=true。正文区分最小自检与未完成工作，使用 Refs #636；没有最终 PublicationFact。真实提交和 Draft 先于完整内容审核及完整风险测试。

Draft 后，fresh 独立 Agent 对固定 B..H 完整内容执行早期 Branch Review，另一个 Agent 并行执行风险匹配验证。早期审核实际返回 `draft_revision_required`。唯一正式 P2 `C636-PUBLICATION-TEST-MIGRATION`：Publication runtime 已使用事务 2.0，而旧测试 fixture 仍写 1.0，另有旧 contract 声明断言。正常场景和机制资格均正式返回 `qualified_current`；因果资格为 `not_incident_applicable`。修复应直接迁移测试消费者，不给 runtime 添加旧格式 fallback。该早期结果未写 public full_review，也不代替最终 Check 或独立正式 Review。

审核期间 target T 快照为 `6f2cd16ab06974ac231cddefb7f04766da5ff074`；没有为追赶 target 执行 Reconcile。PR Actions run `39307613448` 在 H 上的首个快照为 Ubuntu/macOS 成功、Windows 仍运行；本轮 live readback 已确认三个平台均成功。该 CI 默认只选择平台 inventory 测试，不能证明 #636 完整回归；组合 M 未构造或验证。

### Draft 后完整风险验证的首轮结果

独立 implementation Agent 在 H 执行各受影响 package 的 unittest discovery；fixture 使用实际 Fork 公共 Delivery scripts。以下是工程执行事实，不是当前完整 Check pass。

| 范围 | 首轮实际结果与归因 |
| --- | --- |
| TaskCommit | 44 tests，1 failure；旧 committed-reentry Architecture fixture 仍写 delivery-1.0。其余 43 通过。该 fixture 与 Architecture package 在 B..H 无差额，失败依赖在 B 已存在，未自动纳入本项修复。 |
| Publication | 29 tests，2 failures、2 errors；与早期正式 P2 相同，须迁移测试 fixture 和有价值的 consumer 预期。 |
| Branch Review | 58 tests，1 failure；旧 aggregate 2.0/profile/exit 声明未随本项演进。 |
| Check | 54 tests，2 failures；旧 expected exits 缺 legacy_controls_retired，旧 workflow 固定短语已不存在。interface 和测试 B..H 字节未变，B 的实际 blobs 已含同一不匹配，属于本项之外的基线问题。 |
| Delivery Review | 21 tests，exit0。 |
| Merge | runtime 11 tests、contract 10 tests，均 exit0。 |
| Delivery projection | 初次缺 GURU_UPSTREAM_DELIVERY_SCRIPTS；补实际 Fork 路径后 16 tests、exit0（60.852s）。首次环境失败不计通过。 |
| Preset 定向 | 3 tests、exit0（18.008s）；覆盖 managed unknown conflict、backup 及 mode/provenance repair。 |
| family/public graph | 8 tests，15 suberrors；测试错误地把 root-owned consumers 拼在 package 目录下，既有 consumer 和本项五个新 consumer 均受影响。最小修复为测试路径解析，保留 runtime owner 边界。 |

当前 1→2 Publication 迁移仍需专用正常路径 witness；旧 cycle migration 的两项通过不能代替它。修复后的实际命令和结果在下节补充。实际同 PR 修订、GitHub Ready→Draft→Ready 和最终完整 gate chain 尚未完成；现有往返及输出丢失恢复仅有公共 wrappers/provider-port fixture 证据。不能以真实 Draft 或工程测试结果推断 Task Completion。


### 最小测试消费者修正

原 implementation owner 只修改五个 canonical 测试文件：Publication 的事务 fixture、contract 测试和新增 current transaction migration 测试，Branch Review 的当前合同预期，以及 family consumer 路径解析。没有新增 runtime 旧格式 fallback，也未改 Check 或 TaskCommit 的无关基线断言。

Publication 受影响模块实际 22 tests、exit0（14.618s），其中三项 current 1→2 migration 经原 `migrate-delivery-transaction.sh` 的 preview/apply/readback 入口验证：pending 保留 identity/decisions、真实 readiness/stage，Ready 历史成功可在无当前 gate 时读回，pending 缺 gate 仍拒绝。转换前后 Task 记录未变，provider 仅执行 repo/PR view，没有 Git 或远端 mutation。另有 Branch Review 合同命中 1 test/exit0（0.003s）、family 3 tests/exit0（0.078s），source package graph、五文件 AST 和 diff 检查均通过。这些结果只覆盖所列命令，随后完整 Publication package 实际复测 31 tests、33.425s、exit0，完整 stdout/stderr 保留于本次工程日志。

上述 delta 仅为 canonical tests 和任务贡献文档，未改变已安装 runtime、workflow 或 managed spec；matching v3 安装与 drift 事实仍适用于当前可执行投影。tests 不进入安装副本，故本轮不为相同投影重复完整安装。Phase2 Architecture、共享晋升后的最终 Check 和完整 committed Review 仍由各原 owner 执行。


完整复测命令如下；仅执行同 package 的真实测试，不把先前 22 项写成完整 suite：

```bash
GURU_UPSTREAM_DELIVERY_SCRIPTS=/Users/wumengye/Documents/GoProjects/Trellis/packages/cli/src/templates/trellis/scripts TRELLIS_DELIVERY_API_COMMON="$PWD/.trellis/scripts/common" bash trellis/skills/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/packages/guru-publish-task-delivery/tests -v
```

首次 29 tests 的失败与本次修复后 31 tests 通过分别保留，不能覆盖首失败。该 package 通过不证明 GitHub 状态往返或最终完整 Task gate 通过。
