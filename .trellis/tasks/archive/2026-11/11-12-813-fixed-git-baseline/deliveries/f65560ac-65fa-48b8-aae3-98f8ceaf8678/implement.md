# #813 D1 实施与验证计划

## 1. 输入与引用

整体权威：Task根PRD及当前accepted_scope；本批范围为D1 PRD的R1—R6/AC1—AC5。实际方案由同目录design.md单写，第3节拥有唯一来源设计处置。起点B为 `5c6a4591db7165ece045e6b0eb789c21d06d7d38`；首次D1，无前序交付。

实施前加载 `.trellis/spec/workflow/clear-technical-writing.md`、workflow与命中spec的实际正文；公共I/O的版本、投影、错误和历史资产条件读取skill-package-contract的Public Skill I/O第1—6节、Fixed Git Source Compatibility、Distribution And Managed Hashes；兼容取舍读取subtraction-first-compatibility。测试方法使用quality-guidelines的Test And Validation Value与Validation Scope Ownership。原Architecture candidate_assessment、当前constitution/baseline/change-contract及current-knowledge合同限定维护职责和晋升时机。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 原责任与文件 | 行为、可审核产物及完成观察 |
| --- | --- | --- |
| I1 当前合同 | Creation/shared契约：`trellis/skills/guru-team/contracts/task-lifecycle/task-creation-input-3.0.schema.json`；package新版profile/aggregate、interface.json、commands.json及新examples | 新版selected_base_ref与reviewed_base_source明确分工；旧schema/path/id/bytes保留，current只选新版；真实consumer projection可验证 |
| I2 确定性实现 | `runtime/task_lifecycle/composition.py`、`packages/guru-create-task/runtime/invoke.py`及实际命中的原Git事实helper | 共享来源归一化，git_object对象/acquisition校验与synced新建相等条件分开；check/recover同源绑定但不unique扫描、不重复创建；原diagnostic字段恢复 |
| I3 原调用方和说明 | Creation `SKILL.md`、对应shared spec `data-contracts.md`/companion说明、MIGRATION-813；原测试fixture、delivery-chain和实际命中的benchmark | 用实际ready.base薄projection构造新版来源；删除current旧字段reader，保留旧验证资产与完整旧provider恢复说明；不改Sync或上游Trellis |
| I4 独立回归 | Creation package/shared composition与相关Intake tests；新增固定对象完整链及恢复case | 按V1—V4独立观察正确创建、primary保持、字段拒绝和迁移边界；不以自构producer结果替公开链 |
| I5 受管投影 | 原 `guru-upgrade-tools` 从完整canonical source执行，目标仅本App checkout；原installer用于一个代表样本 | 展示真实source/target与写集后沿原边界执行；保Task/session/config/peer；目标自身验证、drift/reapply/sidecar/mode |
| I6 当前知识 | 原RDT和Architecture维护owner；命中runtime-location完整单元及隔离proposal | 完成实际代码/工程验证后，重读真实目标，提交前final_integration整合/readback；所有after纳入同一待审内容 |
| I7 提交后质量与交付 | 原TaskCommit→constructor/begin_check→新独立Review→Delivery Review/readiness→Publish/Merge | 精确本地提交后冻结B/H；独立Architecture before/after与完整Check/full Review一次执行；真实readiness后才远端动作 |

I1—I4实现必须在当前规划接受及Activation后开始。I5保留独立安装副作用边界；I7的commit/push/PR/merge均展示精确对象后按原owner执行。完整Task Completion/Closure/Finish属于后续AC6，不以I7的Delivery事实代替。

## 3. 验证入口、输入与预期观察

执行器采用源码自带受管Python resolver；需要Fork的测试显式使用已验证matching的真实scripts来源。当前本checkout已安装公开Task/schema2 API可作为选定来源，执行前核 `.trellis/.version` 与声明；不从本机未知目录补依赖。

### V1—V4 行为与兼容

```sh
GURU_UPSTREAM_DELIVERY_SCRIPTS="$PWD/.trellis/scripts" PYTHONPATH="$PWD/trellis/skills/guru-team" \
  bash trellis/skills/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime \
  -m unittest discover -s trellis/skills/guru-team/packages/guru-create-task/tests -v

GURU_UPSTREAM_DELIVERY_SCRIPTS="$PWD/.trellis/scripts" PYTHONPATH="$PWD/trellis/skills/guru-team" \
  bash trellis/skills/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime \
  -m unittest discover -s trellis/skills/guru-team/runtime/task_lifecycle/tests -p test_composition.py -v
```

新增完整链回归放在原Creation package测试入口，实际调用Sync read、Discovery、Clarify、Wording、Readiness、Creation的生产wrapper并消费真实stdout；fixture只建立受测边界之前的Git状态和外部GitHub provider。临时仓库原main为旧commit，较新origin/main对象通过正常Git提交/ref setup提供，primary有无关staged及unstaged文件。独立保存并比较refs、index及workfiles；正确Task起点来自既定fixture commit，不复制生产hash算法计算预期。

同一样本丢失首结果后走原check/recover，独立核身份、generation、source及branch/checkout数量不变，不重复创建C4/C5。采用原session回归并核新版来源入口仍保留：同Task/generation/ref保持、缺record由原owner attach、不同或无效session阻塞、缺context为explicit-task。错对象、非commit、错误source/acquisition及common-dir输入各检测不同拒绝边界；同步来源保留原新建stale以及结果恢复语义。旧schema实例原样验证，并通过实际current entry拒绝旧输入；不能把fixture/setup失败当目标行为失败。

已存在的acquisition/session/配置路径回归按适用性采用；受影响新增测试补差额。只有剩余入口、因果或consumer疑问时追加诊断，并说明预期观察如何改变判断。不强制反复旧版回退或红绿轮次。

### V5 结构、实际安装与抗漂移

- 受管Python从canonical执行 `-m runtime.validate --root . --mode source --json`；新增schema/Interface/command声明必须通过真实parser，不只比字符串。
- 按quality-guidelines既定脚本在内存compile Guru源码及命中测试，解析新增JSON，执行 `git diff --check` 和必要Bash syntax。
- 当前Task存在，使用完整源码的 `guru-upgrade-tools` preview→prepare→invoke；不以普通apply绕过Task阻塞，不手工复制受管文件。冻结计划后由目标自身installed validator、native current/continuation和公开Creation入口核投影与身份保持。
- 执行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .`。逐项核manifest、声明shared/Claude/Codex/Cursor投影、执行模式及全部sidecar的原owner处置；不静默覆盖本地编辑。
- 完整public输入迁移需要一个代表性clean throwaway安装，复用V1样本做原installer reapply与真实wrapper观察；至多一个clean样本，不执行完整多平台Release/upgrade矩阵。

### V6 实际Agent与证据边界

本Agent在同一个隔离代表样本读取修复后的公开合同，按实际语义完成原owner判断与record/check/invoke，走到Creation及原恢复结果。可以隔离外部GitHub读取provider，不向产品仓库创建Issue或写远端。实际Agent结论、确定性fixture、模块测试、source/installed结构和Release资格分别报告；任一层成功不替代其它层。

当前上述验证均为计划，不预填通过。

## 4. 停止条件与适用回退点

- 来源、accepted_scope或真实机制变化：停在原Clarify/Author/Architecture，刷新受影响判断，不把新增内容偷偷放进实现。
- public schema、安装或Fork API不匹配：保留真实入口、输入与首个诊断，从原安装/创建owner恢复；不能手造transition、context key、通过或跳过门禁。
- 原调用方残留旧字段、source/acquisition校验在某入口缺失、链路未到创建终点：修复原职责再验证，不以局部绿色收尾。
- tools发生冲突/sidecar或源/目标不一致：保持原状态，沿原事务resume/rollback；不改peer或手抄managed副本。源码改动只能按精确本项路径回退，保留其它工作；不stash或reset primary。
- 必要行为验收/受影响回归/安装观察充分后停止额外实验。反复设施失败时重评样本与入口，具体缺口保持未验证，不扩展攻击、压力或Release矩阵。

## 5. Delivery Policy（唯一）

Policy为 **full**：D1完整覆盖R1—R6和AC1—AC5，不将固定对象、恢复、同步兼容或实际投影留给后继修补。完成条件是实现、原入口/恢复验证、完整知识整合、精确提交后的独立完整Review、真实readiness及本PR交付。没有人为临时能力限制或延期实现责任。

Task仍有AC6：在live main验证merge可达，原Completion判断整体充分性，Closure处理#813，Finish完成必要归档；这些在合并后按原链继续。D1合并不等于整体完成，不触发后续串行Issue提前执行。

## 6. Docs SSOT Plan（唯一）

strategy为 **delta_first**。RDT原writer是guru-maintain-requirements-design-test-ssot；Architecture原writer是guru-maintain-architecture-baseline。

| Canonical完整单元 | 本轮实际差额与直接consumer |
| --- | --- |
| `docs/requirements/current/runtime-location.md` R718-07—11 | 原Creation/Intake调用方读取固定对象创建、真实mismatch、旧输入退出与primary保持定义 |
| `docs/design/current/runtime-location.md` D718-04/05/07 | 原Creation/composition和公开调用方读取新版source投影、新建/恢复条件及matching更新 |
| `docs/test/current/runtime-location.md` T718-04/05/07/08 | 实施、Review、Completion读取创建终点/恢复/primary保持验证与实际观察截止 |
| `docs/architecture/01-current/runtime-location.md` ARCH-RUNTIME-LOCATION | Author/Architecture/Review读取固定来源贯通Creation的完整责任与代价；原环境及#760/#769条件保留 |
| `trellis/presets/guru-team/spec/workflow/data-contracts.md` 原Creation旧字段条款 | 公共contract consumer读取新版字段、薄projection和退出；同步到受管spec，不改历史schema含义 |

隔离RDT完整proposal放在 `docs/requirements-design-test-contributions/813-fixed-git-baseline/`，Architecture贡献及完整拟写按design第9节。实现和真实工程结果具备后，原owners在TaskCommit前重读live target、整合/readback，结果只表明integrated_pending_review。随后固定committed before/after由独立Review判断。Planning不直接写shared current/index；不新增根版本登记、空贡献或审计ledger，不改无关历史观察。
