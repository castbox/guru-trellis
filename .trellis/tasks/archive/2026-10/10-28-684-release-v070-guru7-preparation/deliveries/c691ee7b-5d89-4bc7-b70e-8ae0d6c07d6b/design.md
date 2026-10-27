# D1：v0.7.0-guru.7 准备设计

## 1. 设计目标、需求承接与内容基线

本批承接 [Delivery PRD](prd.md) D1-R1..R6、D1-S1..S4、D1-AC1..AC5。选择范围为整体 R-01..R-06、R-08；R-07 的 Closure/Finish/Cleanup 留给 Completion 后的原 owners。Stage 2 的正式发布和两个选定本地目标的最终收敛仍由 #684 拥有。

原 `DeliveryProjection.content_base` 以明确开发起点计算固定 B=`ee48ea9a0d339a7a6523ace44b7b5b67e75db870`。这是首批，没有前序 delivered head。Planning H0 观察值也为该 commit；未来实现 HEAD 不固定为 H0。PR 目标为 `castbox/guru-trellis:main`，目标移动不重定义 B。

适用 Architecture 为该 B 的 `docs/architecture/README.md`，identity=`guru-trellis-architecture`；宪法为 `docs/architecture/00-foundation/design-constitution.md`，identity=`guru-trellis-design-constitution-v1`；项目 change contract 为 `docs/architecture/06-governance/change-contract.md`。原独立 candidate_assessment 已正式返回 `baseline_current / no_architecture_impact`：本候选只修改版本值、公开来源说明和既有安装投影，不改变决策、职责、公共 I/O、状态或兼容退出。该结果不替代 Wording 后的 final_plan，也不证明安装或发布成功。

U-01 采用本链既有 `workflow-defect-recovery` 的有界等价证据路径，执行顺序见第6节。它处理晋升前正式记录的前置成环，保留两轮实质完整独立审核及第二轮真正 public Check/full_review；不修改 #684、私有发布合同或整体 accepted scope。后续规划门禁和方案接受仍由原 owners 执行。

## 2. 当前系统、边界与目标差额

这是首个 Delivery，没有前序切片结果。当前 canonical extension、maintenance target 和 const consumers 为 `.6`。三份公开 README 及项目 public-docs 仍将 `.5` 描述为稳定版本、`.6` 描述为未发布目标。live Release 已确认 `.6` 正式发布，peeled commit 为 `6b3e26b177f747fdde48b43685d8af8827e22614`。

目标为 extension/maintenance `.7`；准备期稳定来源为 immutable `.6`。候选试用必须由 workflow marketplace 和 preset 共同指向同一真实远端完整 SHA。不可把尚未发布的 `.7` tag 写成可用 provider。

版本修改通过现有 manifest、maintenance runtime、schema、examples 与受影响断言直接演进，不增加新版本路由。Fork lock 保持 `79a97ed60fe19e8f287eaddfa74722b5250ced35`，CLI/Core 保持 `0.7.0-castbox.5`，`.trellis/.version` 继续记录 CLI。稳定知识 identity 不随软件版本递增。

当前 Task dogfood 必须由原 tools owner 实际更新。调用 app checkout 与保留主仓是 Stage 2 的发布后目标，不能以本 Task 的安装结果代替它们。

## 3. 来源设计处置（唯一）

| 来源 locator / 条款 | 原承诺 | 处置及具体落点 | 理由、影响与上游处置 |
| --- | --- | --- | --- |
| #684，目标与当前背景；private release contract，Invocation Input | `.7` extension 与 `.5` CLI/Fork 独立；前驱 `.6` | retain；第2、4节按版本 consumer 修改值，保留 lock | 没有升级 Fork 的需求；不改变安装依赖 |
| #684，准备期公开文档；private contract，Reviewed-Content Freshness | stable 与 candidate 使用真实同源 immutable provider，正文变化纳入候选 | retain；第2、4、8节同时覆盖三 README 与 public-docs | 更正当前说明；历史 Test 不回填新结论 |
| private contract，Stage 1 §2 与 preparation installation；tools contract，Forward behavior | 原 `source_locked` owner 更新真实 dogfood；需要干净已提交来源时走既有 early-commit/source-acquisition | retain；第4、6、7节使用完整来源和匹配构建，实际 managed/manifest 变化返回同候选 | 不手改 provenance，不把 throwaway 当真实安装 |
| private contract，Stage 1 §3..7；Check contract，Candidate Check and final integration；本链 `guru-orchestrate-issue-sequence/references/workflow-defect-recovery.md` 的 Recovery Order §3/4、Equivalent Evidence | 晋升前后各有完整 Phase2、真实提交和独立完整 B..H 审查，零开放 P0–P3 后才进入整合；公共 final Check/full_review 只在整合后记录 | retain 实质义务；第6节先固定已提交 Hpre、完成九维 Check 与第一轮独立完整审查，再输出 candidate_checked 进入原整合；第7节仅对成环记录用直接证据 | 保留原 owners、全部实质门禁、真实 typed exits 与缺失 public 记录边界；不修改来源，不将 draft_content_reviewed 改称正式 passed |
| private contract，Stage 1 §8..11 | Architecture publication、Refs-only、expected-head；Completion 后 Closure no_mutation、Finish、Cleanup | retain；第6、7节和 implement 第5节区分本批交付与后续生命周期 | 保持 #684 Open，不使 Finish 反向成为 Completion 前提 |
| private contract，Forbidden Persistence / Independent Mutation Confirmations；AGENTS §2..4/9/10 | AI 判断与脚本事实分层；精确副作用独立确认；不持久化授权或发布状态 | retain；第4..8节只复用原 owners 与其最小结果 | 没有新 schema、ledger、checkpoint、动态 checklist 或正文 handoff |

## 4. 模块、职责与设计取舍

| 模块 / 原 owner | 输入、实际文件与行为 | 输出及边界 |
| --- | --- | --- |
| 版本维护 | `trellis/guru-team-extension.json`；`trellis/skills/guru-team/packages/guru-upgrade-installation/runtime/owner.py` 的 TARGET_GURU | 目标改为 `0.7.0-guru.7`；TARGET_CORE 和 source lock 保持现值 |
| 受控 consumers | upgrade-installation 的 `schemas/public-upgraded-output.schema.json`、`consumers/stop/production/upgrade-installation-upgraded.schema.json`、`examples/public-upgraded-output.json`；upgrade-tools 的 `examples/public-tools_upgraded-output.json` | const 与示例同目标演进；旧历史 fixture 按场景保留，不能全仓替换 `.6` |
| 已有测试 | upgrade-installation 的 `tests/test_contract.py` 与 `tests/test_delivery_upgrade.py` | 只调整真实目标 fixture/预期；测试仍运行原 owner 行为，不新增只比较固定版本字符串的用例 |
| 公开文档 writer | `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`.trellis/spec/docs/public-docs.md` 的当前发布身份/安装段 | stable `.6`、target `.7`、CLI `.5` 和各自 lock；完整能力集最终以 `.6..candidate` diff 为准；#678/#679/#666 按实际来源说明，#657 不冒充本次新增实现 |
| 原 tools owner | `guru-upgrade-tools`，`dependency_mode=source_locked`，本 Task checkout 为 target | 由完整干净来源生成真实 installed manifest、受管脚本/schema/平台投影；原 native/preservation 结果有实际证明 |
| 原 RDT / Architecture owners | 阶段适用完整知识、实际差额、真实目标 | 无影响保留 no-change；有真实知识差额才写隔离完整 proposed targets；第一轮完整独立审查后才由原 final-integration owners 串行写入 |
| 原质量/发布 owners | 规划、完整候选、原工具与工程结果 | Check、TaskCommit、独立 Review 和 Delivery/Publish/Merge 各自判断，脚本不选择流程或 adequacy |

直接演进维护值和现有消费者，不建立并行 `.6`/`.7` runtime，也不添加新的 release orchestrator。公共 Skill id、typed exits、input/output shape、Task/Delivery 状态均无设计差额。

## 5. 接口与数据

本批没有新业务 API、数据字段或数据库迁移。已有链为 canonical extension.version → maintenance TARGET_GURU/const consumers → 原 installer 生成 installed extension.version/source → 原 tools owner 验证实际 target。`.trellis/.version` 属于 CLI；不能写成 Guru revision。

tools 接口沿原 `install` input、只读 preview、一次 prepare、原 invoke 与同操作 recovery。`source_locked` 使用来源 commit 的正式 lock 和实际匹配 CLI/Core package roots。现有 Fork checkout 只是待原 owner 核验的来源线索；相同版本号不证明实际 build。source-acquisition 的精确 path/ref/命令在该副作用边界展示，不提前创建资源。

知识 owners 的 `candidate_ready` 不是 shared-current；Check 的 `candidate_checked` 不携带 final `check_result_id`，不能进入 final TaskCommit 或 formal Branch Review。第一轮使用真实 early TaskCommit 的 Git 提交和直接证据；其已有内容审查出口保持 `draft_content_reviewed`，不写 public full_review。第二轮使用原正式 profiles 和真实 public IDs。

## 6. 状态、顺序、正常与失败流程

1. 完成规划、原 Wording、独立 final_plan、Approval 后，展示当前方案并等待用户接受；原 Activation 才进入 implementing。
2. 实施版本/consumer/当前公开文档差额。原 owners 判断知识影响，保留 before authority，只有真实差额才形成隔离完整候选。
3. 原 TaskCommit 的 early route 为 tools 所需完整已提交来源提供可审核内容。来源 checkout 的取得与真实 tools 安装各自按原副作用边界执行。early DTO 只交原 draft router/Publication；原 Draft 发布的精确 push/PR 边界单独展示和承接，不能当成最终 Ready。
4. 原 tools owner 在当前 Task target 实际更新、native 验证并核保留状态；将全部实际 changed managed paths 和 manifest 纳入本批。失败/输出丢失回同一原 owner，不重复 prepare 或手改 manifest。
5. 将全部实际准备内容、managed 变化和完整拟晋升 targets 经原 early TaskCommit 固定为真实非空 B..Hpre。Hpre 尚未生成，不预填 SHA。implementation 对同一候选正常 begin_check；原 Architecture phase2、RDT impact 和原 Check 读取完整候选、来源及未改 consumers，实际完成九维判断与真实验证。Check 的 record/check 保留真实 candidate_checked 语义结果，暂不 formal invoke，公共 phase 保持 checking。
6. 在同一 B/Hpre/字节上，由独立原 Architecture owner 执行 stage=branch_review 的完整 committed-range 评估，source_exit 如实使用 draft_committed，不虚写 committed。随后独立 Review owner 审完整 B..Hpre、原门禁维度、真实测试、未改 consumers、兼容与双 subtraction，以及 findings 资格和关闭证据。不得只做较浅 Draft 反馈。只有九维通过、完整独立审核完成、零开放 P0–P3 且无阻塞证据缺口，才返回真实 draft_content_reviewed 并报告直接语义结论；晋升前仍没有 public full_review。
7. 第一轮完成且内容未变后，原 Check 才 formal invoke。真实 candidate_checked 的合法 rework 返回 implementing，立即交唯一 integration consumer。Architecture/RDT 原 owners 串行审 expected-current、真实 targets、trace/subtraction 后写入并读回；实际 no-change 由原 router 跳过写入，不调用空 promotion。
8. implementation 对实际 after 内容 return/rebind、重新 candidate/begin_check；原 Architecture/final Check、原 TaskCommit 和第二轮独立完整正式 delivery_branch_review 覆盖全部最终内容。TaskCommit 改变 HEAD 时保留原 fresh-Check 回程。无写入且保留已提交候选时使用合法 clean committed reentry，不造空提交。第二轮必须取得真实 public Check/full_review，不能用 alignment、continuity 或第一轮证据改名替代。
9. 最终质量结果全部 current 后，原 publication Architecture、Delivery Review 和中文 Refs-only readiness → 原 Publish 将同 PR 转 Ready → 独立 expected-head Merge。每个未知 mutation 结果先恢复原操作。
10. 原 Completion 判断整个准备 accepted scope。通过后 Closure=no_mutation，再 acceptance-finish Architecture、Finish 和精确 Cleanup。Stage 2 由发布 owner 在准备与终态归档合并后重新开始 fresh candidate gate。

第一轮 Review 发现问题时，原 Check 从真实 finding 与证据重新判断，走 implementation_required 的合法回程。修复、原 early TaskCommit 生成新 Hpre 后，重做受影响的完整当前 Check 和独立审查。候选、来源、验证义务或未改 consumer 的真实影响变化时，旧直接证据不得放行新内容。

普通 stale/mismatch、缺失匹配构建、managed conflict、sidecar、native failure 均阻断其直接依赖动作；不把旧 Gate、版本字符串或 retry 成功扩为完整证明。没有攻击模型、竞态压力、锁或 crash-hardening 新场景。

## 7. 恢复、兼容、迁移与集成

U-01 只采用本链恢复合同允许的下层入口和直接 Git/测试/文件证据。可用的 early TaskCommit、Architecture phase2/committed assessment、RDT impact、Check record/check/candidate_checked、draft_content_reviewed 与全部 after 正式入口均照常执行。晋升前 final Check 的 passed/check_result_id 及依赖它的 final TaskCommit 路由、public full_review 确实不能合法记录；仅该记录缺口由实际完整语义工作和直接证据承接。不得补造 gate、public ID、输入前序或出口，不得将 FAIL/SKIP 写为 PASS。

完整九维为 requirements、design、implementation、tests、docs_ssot、cross_layer、compatibility、deployment_and_operations、verification_completeness。第一轮直接证据须说明精确已提交 B..Hpre、全部范围与未改 consumers、实际命令/输入/结果、逐维判断、独立 Review 结论、每个真实 finding 的状态和零开放项。reviewer 自定当前检查集并核工程事实适用性，不读取 Check 私有结论代替独立判断。证据留在当前会话及各原 owner 允许的短期状态，不新建 tracked report、发布 ledger 或跨 owner 私有 checkpoint。

公共 wire shape 保持。maintenance 当前目标值与受控 consumers 成套更新；历史版本、archive、旧失败和当时未知保留原含义。不新增兼容分支或转换历史 Task。真实 old Task native 诊断交其独立维护 owner，不能为了 tools 成功而修改旧数据。

完整 Guru source 和匹配 Fork build 由原 tools owner核验。需要构建时使用当前 pnpm，不固定执行版本或修改源码 package-manager 声明，不复制 dist/重造 launcher/全局安装上游包。实际 tools native-entry 与 preservation 是单独证据；source validators 不替代它们。

ordinary apply/reapply 的历史 Task guard 仍如实保留。没有满足私有合同 Historical-Task Preflight Observation 全部条件时，不能声称替代验证覆盖；该 Stage 2 例外尤其不能替代本批真实 tools 更新。所有 `.new/.bak` 逐项按原 owner 处置，不批量删除。

版本源码、公开说明和受管投影在同一准备交付集成。最终来源允许按原合同使用真实已审查且 managed set/source lock 等价的已提交来源，不追逐自引用 HEAD，不增 release-status commit。回滚只由原 tools 的独立 rollback 边界处理，不执行 Git reset 或清理无关资源。

## 8. 验证设计

| 验证 | 需求 / AC | 层次、入口与输入 | 预期观察与限制 |
| --- | --- | --- | --- |
| V-01 | R1/R2；AC1 | 对实际候选 manifest、target/const/schema、文档、CLI record/source lock 作语义与 diff 审查 | `.7`、稳定 `.6`、CLI `.5` 各自唯一；historical `.6` 不误改；不能证明安装 |
| V-02 | R1/R3；AC1/3 | 原 managed Python 执行 upgrade-installation 命中行为测试，再 source package validator | 正常目标识别、实际安装输出与 schema consumer 一致；不以固定字符串自比新增测试 |
| V-03 | R3；AC3 | source/installed validators；Shared/Codex/Claude/Cursor source parity、ownership、原 apply/reapply、drift/mode/sidecar | canonical、受管副本和实际 installed inventory 匹配；历史 guard 单独记录，不伪称 PASS |
| V-04 | R2/R3；AC2 | 原 tools owner在本 Task target 执行 source_locked，核匹配 build、实际 native-entry、managed set 与用户状态前后 | 实际安装版本/provenance/CLI 可证明且状态保留；不是 throwaway 或所有平台 Agent 证明 |
| V-05 | R4/R6；AC4 | 第6、7节恢复顺序；完整九维 Check、原 TaskCommit 与两轮完整独立 Review | 第一轮固定已提交 B..Hpre 和直接证据充分，真实出口为 draft_content_reviewed、无 public full_review；原 candidate_checked 后串行整合/合法 no-change，after 重绑后第二轮取得真实 public Check/full_review；零开放 P0–P3，无空贡献/空提交 |
| V-06 | R5/R6；AC5 | 原 Delivery Review/readiness、Publish 和 expected-head Merge | 中文具体 Refs-only，实际验证/安全/部署边界完整；#684 不关闭 |

命令细节和前置见 implement 第3节。Stage 2 的 fresh predecessor-to-candidate、focused/existing installer、退休清退、真实 secret scanner、tag/smoke/Release 和两真实本地目标收尾留给 #684；本批不预填其 pass，也不运行累计多平台矩阵。

## 9. Canonical 引用、本轮差额与实际未决项

本批引用 `docs/requirements/current/knowledge-maintenance.md` 的 R331/R638/R648，`docs/design/current/knowledge-maintenance.md` 的 D331-02/04、D638，`docs/test/current/knowledge-maintenance.md` 的 T638，以及本文件第1节 Architecture 和第3节来源。它们规定隔离候选、no-change、最终整合、after 重绑和当前语义判断；本批没有改变这些公共机制。public-docs 仅修改命中的当前软件版本与来源说明，不清理其它历史 prose。

Architecture candidate assessment 无影响，不创建 contribution、ADR 或全局知识版本。原 RDT 在 Phase2 仍须根据实际候选判断；当前没有依据预建空 RDT 贡献。如果发现真实 knowledge delta，它须由原 owner 写完整 isolated proposal，再经合法最终整合，不能直接改 shared-current。

U-01 的当前处置是第6、7节的有界等价恢复；没有需要用户选择的产品或 Architecture 变化。实际执行仍可能出现来源、工具链、安装、测试或语义 finding 缺口，须在对应原 owner 停止并处理，不能预填通过。第一轮完整实质判断与其正式记录缺口、第二轮真正 public 结果必须分别如实报告。
