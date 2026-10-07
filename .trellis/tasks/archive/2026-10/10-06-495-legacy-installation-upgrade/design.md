# #495 版本系列原地升级 — generation 1 设计

状态：Planning 已批准；实施候选。行为 authority 见 [prd.md](./prd.md)；本文只拥有机制和职责，不把拟定入口标成已有实现。

## 单一升级机制

直接演进既有 `guru-upgrade-installation` 与 Fork `migrate`，复用受管 updater、marketplace、preset 和 current lifecycle owners。Guru Markdown 负责来源适用性、逐任务处置、充分性与 gate 判断；executor 只消费明确计划和可校验前置事实。普通 `update` 同版本路径保持，跨版本升级不通过删版本文件、伪造 manifest 或 patch node_modules 解锁。

目标候选为 Guru `0.7.0-guru.3` / Fork `0.7.0-castbox.3`；正式 merged Fork OID/tree/parents/成功 CI 固定后接入 source lock。目标 Guru source 必须包含本轮实现；最终 public/provider 证据使用同一远端可读、canonical clean 的精确 commit。

| 责任 | 唯一 owner | 修改边界 |
| --- | --- | --- |
| D-MIG-495-INVENTORY | Guru upgrade package | source tag/extension/core/provenance、managed receipts、本地修改、task/control inventory；preview stdout |
| D-MIG-495-CORE | Fork CLI/core | 读取实际 installed core；显式 migrate plan 更新 core-owned 文件；只转换指定旧 task，保留已验证 current task；复用正式模板/hash collectors |
| D-MIG-495-GURU | Guru upgrade package/current preset | exact old source bytes 与 managed ownership 映射、Guru assets 更新、workflow 同 provider preview/force；不使普通 apply 接受旧 manifest |
| D-MIG-495-LIFECYCLE | current identity/source/C4/C5/session/Planning owners | current task 校验与保留；缺失/旧格式 binding/control 的精确转换与正式 owner re-entry；不新增第二 writer |
| D-MIG-495-RECOVERY | 既有 private backup/checkpoint 与 Fork restore helper | 读取真实来源和旧字节；普通恢复、source-specific rollback、新工作保护；不写 Git history/远端 |
| D-MIG-495-FAMILY | 上述 inventory/core owners | 两系列 source predicate 与 exact manifest/core mapping；无 revision 白名单和 alias 分支 |

## 来源与 Public API

release tag、extension revision、实际 core 分开核对，分组沿用 prd 的 G1..G8。旧 manifest 的 source.commit/ref/tree_state 可能由旧 installer 记录为准备阶段 predecessor、mutable ref 或 dirty source，不能机械要求它等于最终 tag，也不能据此排除整组正式版本。优先使用真实 receipt 的逐资产 bytes/hash 与选定正式 source 的 canonical 资产核对；缺 receipts 时从已核验正式 tag/source 及对应旧 installer 确定完整 ownership 和旧字节。无法唯一确认的本地文件保留并列为定制/待处置，不用新来源 hash 冒充旧 hash，也不伪造 current manifest。

G1/G2 在一次性边界把 schema 1.0 安装事实投影到 current installer 所需的 provenance；G3 补齐缺失 expanded hashes；G4..G7 按已存在 receipts 和实际 core 做同一 managed update；G8 校验并保留 current task/control。旧 manifest 本身归档于私有备份，不先人工改成 schema 2.0 再绕过验证。早期 Guru 清单中的 upstream-owned skills/agents 交还 Fork updater，不按 Guru retired assets 批量删除。

用户定制处理统一：旧 canonical/receipt 与本地字节相同才自动替换或清退；不同则保留本地，输出目标 `.new` 和精确差异，由 AI 在具体安装计划中决定保留/合并/替换。业务 spec、规划、历史、journal、人员目录、未知文件及无关 dirty/untracked 原字节保留；配置有效设置保持，官方必需 additive keys 单列。升级后用新 canonical/receipt 检验实际目标语义，不因旧文件未触碰而误判已迁移。

初始 public `source_profile` 从唯一 `.41` selector 原位演进为 `guru0.6-family` 与 `guru0.7.0-family` 两个 selector；selector 只选择来源族，实际来源由目标 live facts 校验。`initial_upgrade`、`resume`、`rollback` profile、命令 id 和既有 typed exits 保留。同步 input/output schema、Interface、受控调用方、examples、README 和测试；旧 `.41` selector 的调用文档明确迁移到 family selector，不增 alias/fallback。已发布 tag 的包保持 immutable。rollback `installed_version` 改为当前恢复来源的真实 extension，不返回固定 `.41`。

目标源和实际安装的版本、schema、source OID由本步骤直接 consumer使用；完整 inventory/文件 hash/原 task/control/local paths 不进入 public handoff。initial/recovery inputs 与各 typed output保持独立简洁合同。新增字段必须指向执行、resume 或 rollback 的直接 consumer；不引入审计总 artifact。

## 写前预览与执行

1. 零写入读取 core/Guru manifests、template hashes、配置/platform selection、业务/spec/规划/历史、task/branch/session/control、Git dirty/untracked 与 registered worktrees。source family、exact来源映射、目标后继关系与 writer capability先校验。
2. 对旧和目标的完整 managed footprint 作 write/remove/preserve 投影。旧 receipt 拥有而目标已退役的路径逐项决策；manifest 缺 hash 时从 exact old source 取字节，不用新源字节补旧 hash。模式和本地修改也进入事实。
3. AI审查逐文件和逐任务投影；current task不列为 legacy conversion。显示真实命令和写入范围后获得具体安装副作用确认；授权只在对话，不进入计划或恢复文件。
4. 既有 backup/checkpoint记录实际 before core/Guru/source/schema、目标source、旧文件与新增路径、转换范围、会被修改的本地/shared control。已审查 current task与deferred旧记录均原字节保留；只备份确实会修改的control，不接管无关checkout工作。
5. 同一 Fork `migrate --from <实际core> --plan <reviewed-plan>`预览/执行路径复用 managed updater。计划显式区分旧转换、current保留、已诊断deferred；来源 `.6.x/.7.0-castbox.N`按实际来源合同处理，不全局放宽正常 task reader。未列处置的旧记录仍阻塞。
6. marketplace同provider `--create-new`读取 `.new`，核验字节、identity、用户修改后显式 `--force`；Guru旧provenance在升级边界转换后调用current preset。清理退役owned空目录，保留含未知内容的目录；逐项处理sidecar。
7. 从目标实际installed runtime验证安装/库存/当前task与平台投影。正式owner re-entry并分别报告安装、转换、接续与保留处置。失败返回原Skill恢复入口，不能把manifest/version单文件视为整体完成。

## Task 与 Control 转换

| 实际事实 | 明确动作 |
| --- | --- |
| current task满足目标schema | 保留原bytes/mode、id/generation/source/status/relations/meta；不初始化generation，不重建有效binding/session，不伪造gate |
| 旧task缺generation/source、有人员/旧branch/path字段 | id/ref不变；generation缺失初始化0；来源与Issue disposition由AI/live事实决定；只用已知字段投影退役人员/旧authority |
| 精简旧record | 采用prd的数据补全规则；不将迁移日期称创建日期；未知业务字段逐项诊断 |
| children/parent/subtasks | 有效关系保留；空subtasks退役；非空经AI确认同语义去重映射；不能无损表示则原地preserve并报告 |
| TAPD或其它非GitHub来源 | 结构化no_issue；原业务来源保留于既有description/meta/规划，不制造GitHub关闭意图 |
| 有效current control/session | 保留责任、generation、branch/ref/HEAD与sessionfocus；shared/local override保持各自owner，不能更新其它checkout的业务状态 |
| known retired control字段/格式 | 仅在版本差异审查证明真实legacy格式后，按该control的owner/schema确定性投影；preserve资源id/revision/状态/Finish事实。未知冲突或无法唯一解析具体报告，不改成新的current authority |
| 缺失/旧binding或stale旧路径 | 从真实refs/registeredcheckout/actualtask核实，由currentC4/C5/Bind建立；普通dirtyresume与新checkoutcleanacquisition分开 |
| PR/merge/旧Finalizer或Finish | 读取livefacts逐案处置，旧gate/receipt不转成当前pass，不重复外部副作用 |

旧记录只保留身份占用，不成为current candidate；Fork `deferred_tasks`与current installed inventory继续消费已审查旧字节投影。direct旧目标、占用/同身份冲突、坏current/JSON/id仍拒绝，不catch-all跳过。尚未提交到branchHEAD的task单列正式acquisition处置，不暗中commit或丢弃dirtywork。

planning与未发布in_progress实际接续均进入fresh当前语义owner；真实脱敏Architecture baseline、actualnormal-scenario/solution-mechanismqualification、wording、Planning gates构成证据。upgrade改变的gate依赖由当前owner重新审查；原generation0结果不绑定新generation。

## 部分写入、恢复与回退

沿用一个private checkpoint，不新增第二事务或全链digest。完成动作只以旧bytes/目标bytes和固定plan事实识别，ordinary drift停止并重新预览；不重复task转换或已发生的remote副作用。before实际sourceidentity在begin固定，resume不得重取当前task/control业务内容当可覆盖旧基线。

core/task已写而Guru阶段因普通本地受管冲突暂停时，立即固定rollback所需task/control与Git业务状态基线。native writer新增meta、newtask/delivery、业务文件或其它checkout合法工作必须阻止覆盖式回退，即使resume随后成功。没有新版业务工作时，仅恢复本迁移清单的旧bytes/modes/control，删除未被新工作修改的迁移新增文件，运行实际旧runtime smoke。输出恢复的真实core/Guru版本。保留无关dirty/untracked，不reset/rewind，不删除remotePR。

## Architecture Planning contribution

Identity：`architecture-contribution-495-upgrade-version-families-plan-v1`，locator为本文。expected current：`current-main-0.6.17-guru.73`；constitution/change contract分别为`guru-trellis-design-constitution-v1`、`guru-trellis-architecture-change-contract-v1`。impact为`architecture_impact`，唯一path为`legacy_boundary_convergence`。

| Required concern | 本轮判定 |
| --- | --- |
| authority-binding | applicable：live#495系列修正、Guru2.0、current.73与projectv1共同绑定 |
| constitution-binding | applicable：官方扩展面、实际来源语义完整、原writer隔离、最小恢复状态与迁移后current-only；无原则例外 |
| boundary-and-decision | applicable：D-MIG-495-FAMILY修改固定来源边界；继承ADR-017，形成系列来源的ADR候选；不恢复人员体系 |
| owner-and-single-writer | applicable：Fork写core/task，Guru写Guruassets，C4/C5/Bind写各自control，sharedknowledge只由promotion写 |
| compatibility-and-exit | applicable：旧格式只在一次性边界转换，current不转换；成功出口current-only；旧selector受控调用同步迁移，不长期双轨 |
| gap-and-deviation | applicable：补齐.73固定样本范围之外的真实升级缺口；原已验收范围仍为历史事实，不虚构其它GAP关闭 |
| parallel-scope | applicable：本task规划/isolatedcontribution/canonicalcandidate；Fork有独立Git副作用边界；禁止竞争sharedcurrent和业务文件 |
| evidence-and-freshness | applicable：before为实际系列拒绝；after为设计待验收；计划来源分组与 linked/current 任务验证，不称运行通过 |
| review-and-promotion | applicable：候选RDT/Architecture经Phase2/独立完整committedBranchReview，expectedcurrent晋升后再检查晋升diff |

项目检查`guru-trellis-architecture-convergence:repository:1`以当前Planning内容执行语义审查：来源族没有变成runtime双读，没有第二schema/controlwriter，没有无consumer状态。ADR候选在`docs/architecture/contributions/495-upgrade-version-families-adr.md`承接系列边界，独立review后通过promotion确定正式ADR；本轮不改sharedcurrent或历史ADR。

## Docs SSOT Plan

实施创建`docs/requirements-design-test-contributions/495-upgrade-version-families/`，以`MIG-495-01..12 → D-MIG-495-* → S-MIG-495-*`映射Requirements/Design/Test及双向trace。Architecture实施贡献位于`docs/architecture/contributions/495-upgrade-version-families.md`。操作入口文档、package合同与spec投影同步，fixed-only条款退役到历史；generation0贡献、tags和原验收不覆盖。

知识晋升严格expected-current串行；未reviewcandidate不提前写current.73。普通presetapply同步dogfood和所有声明平台投影，检查officialupdate/hash/sidecar机制；不单独patch生成副本。完整累计Release矩阵、真实业务安装和版本发布仍独立。
