# #495 版本系列原地升级 — generation 1 实施计划

状态：in_progress；Planning 门禁与 activation 已完成。行为与机制分别由[prd.md](./prd.md)、[design.md](./design.md)拥有；Fork 本地实现与定向验证已完成，Guru 实现与分组预演进行中；不把原generation0结果当当前gate。

## 实施顺序

1. 完成本轮wording、normal-scenario与solution-mechanismqualification、ArchitecturePlanningimpact及PlanningApproval。展示正式方案和activation状态写入后停在reviewpause；确认具体方案后才进入实现。
2. 枚举两系列当前正式tag与完整manifesthistory，建立release/extension/core/exactsource/schema映射；检查指定下游安装和task/control真实格式。核实不足项用当前owner具体诊断，不缩回revision白名单。
3. 在用户指定Fork来源上实现单一migrate入口的实际source/core支持、coremanagedupdate和旧/current/deferredtask明确处置；保持普通runtimecurrent-only和唯一writer。Forkbranch/worktree/commit/push/PR/merge均另列精确副作用计划；不把GuruPlanning确认当ForkGit授权。
4. 直接修改现有Guruupgradepackage的sourceprofile/schema/sourcehash补齐/core调用/backup/recovery/rollback；同步Interface、controlledcallers、examples和source-specificoutputs。旧fixedselector原位演进到familyselector，不新建facade/alias/平行状态机；不会修改已发布tag。
5. 候选版本设Guru`0.7.0-guru.3`、Fork`0.7.0-castbox.3`；正式ForkmergedOID/tree/parents/成功CI后更新唯一sourcelock。没有正式固定依赖前只报告localcandidate，不称source_locked通过。
6. 同步canonicalworkflow/package/presetREADME/`MIGRATION-495.md`/workflow与preset specs；创建本轮isolatedRDT/Architecture/ADRcandidate。普通apply依旧current-only；source加载升级Skill。复用marketplace/create-new/force/preset，不patch全局npm/node_modules或旧目标副本。
7. 正式apply同步dogfood，逐项处理`.new/.bak`；运行drift、package/registry/schema/consumergraph/installedinventory/modes/声明平台投影与officialsource-repositorydogfoodprojection。改动非生成文件保持≤3000行；超过时先机械拆分。
8. 在隔离脱敏样本跑下表本地定向验证，分别证明安装更新、task/controls保留或转换、owner接续、恢复和真实post-writerollback。真实业务仓只读，不copysecret/.env/敏感trace或打印原业务正文。
9. 本地候选和Fork正式依赖通过后，freshPhase2/TaskCommit/独立完整`origin/main...HEAD`BranchReview；按expectedcurrent执行知识promotion，再检查晋升diff。展示后发布Refs-only验收候选PR，保持#495OPEN。
10. 使用固定远端可读Gurucommit，跑同源public/source_locked/marketplaceprovideractualinstalled验收；失败保留原样本与日志，同一task修复、重跑受影响gates。MIG-495-01..12完整后才能合并、Completion、Closure、Finish；每个Git/GitHub副作用分别确认。

## 改动位置

| 层 | 精确目标 |
| --- | --- |
| Fork | `packages/cli/src/commands/migrate.ts`、`update.ts`及其helper/tests；currenttask与generatedtemplates涉及的已知转换和schema；版本候选/官方生成同步 |
| Gurucanonical | `trellis/skills/guru-team/packages/guru-upgrade-installation/`的Markdown、Interface、schemas、runtime、tests、examples；受控调用和manifestcandidate |
| source/preset | `trellis/presets/guru-team/source/trellis-source.json`、现有installer调用边界与受管ownership；不复制旧读逻辑进普通apply |
| workflow/docs/spec | `trellis/workflows/guru-team/`、presetREADME/升级指南；当前migration/current-onlyspec投影；无新mandatoryworkflowphase |
| dogfood | 正式installer生成的`.trellis/guru-team/`、`.agents/skills/`和声明平台入口、workflow；不独立patch |
| task/knowledge | 本三份planning；isolated`495-upgrade-version-families`RDT/Architecture/ADRcandidate；sharedcurrent只正式promotion |

当前Gurucheckout为`codex/495-upgrade-version-families`，TaskId/generation1不变，base`11ef591c`。任务归档移动已经发生；未commit/push。本轮Planning只写本taskplanning，不写workspacejournal或授权字段。

## 最小可靠验证集

来源验收使用 prd 的 G1..G8 分组。全部现有正式 tag 执行来源映射与 managed footprint 投影检查；每组代表运行 public 零写入 preview、实际 managed 升级、安装/模式/资产 smoke、普通部分失败恢复和无新版工作时实际来源回退。G6 的 core 0.6.17 source、G7 的 all_platforms 差异及 G8 的 `.2` current control 只补不同路径，不重复整套等价测试。复用 generation 0 中实现未变化且固定来源仍匹配的有效证据；变更 consumer/runtime 或 freshness 依赖的部分重新运行。

每个 tag 有一条明确覆盖归属，实际 receipts、资产 ownership、配置或 task/control writer 差异若推翻同组等价，才增加该差异的代表验收。缺 source 对象先直连重试；未知本地定制作具体保留/处置，不能缩回版本白名单。未来同系列正式来源进入相同合同，但不声称不存在的版本已执行验证。

| 场景 | 实际验证与预期结果 | 行为 |
| --- | --- | --- |
| S-MIG-495-FAMILY | G1..G8 代表 public 零写入 preview→实际 managed 升级；tag/extension/core/source匹配，无代表revision拒绝；同目标reapply单列 | 01、02、08、10 |
| S-MIG-495-TASK | 完整/两种精简旧record、非UUID/source/generation/relations转换；currenttask原bytes/modes保留 | 03、04、11 |
| S-MIG-495-PLAN | 旧转换与currentplanning各实际identity→branch→checkout→Bind→freshPlanning；真实脱敏Architecture与两qualifiers/语义gates | 04、05、11 |
| S-MIG-495-DEV | 旧和current未发布in_progress保留committed/dirty业务工作，fresh当前审查后dev/check；不把cleanacquisition误用于dirtyresume | 04、05、11 |
| S-MIG-495-LINKED | primary/linked实际checkout、common/localPythonoverride、当前session及资源责任保持；knowncontrol格式由正式owner承接，不改其它checkout业务工作 | 11、12 |
| S-MIG-495-DELIVERY | livePR/merge各一项；fixed旧`.41`canonical正式writer正常生成非terminal快照，observer只读保存后原路径完成；upgradepreserve旧task/事务/gate/refs并报告pinned-old/manual，无重复副作用 | 06 |
| S-MIG-495-PRESERVE | business/spec/规划/history/journal/.developer/tracebytes/modes；有效config/customsettings语义不变，officialadditiveconfig单列；dirty/untracked不覆盖 | 02、03、11 |
| S-MIG-495-PARTIAL | core/task已写而Guru因普通managed本地冲突停止；解决具体冲突后原入口resume成功，无重复转换 | 07、12 |
| S-MIG-495-ROLLBACK | G1..G8 代表分别实际 post-write rollback，恢复各自真实core/Guru/task/control/定制与旧runtimesmoke；输出不是固定`.41` | 07、12 |
| S-MIG-495-NEW-WORK | 部分写入暂停时nativewriter产生新meta/业务工作，resume后rollback仍阻止覆盖；完成后newtask/delivery亦保护 | 07、12 |
| S-MIG-495-MIXED | current+无关knownlegacy及revieweddeferred旧记录；currentcreator/ref/id/branch/checkout/session成功；旧目标/占用/同身份冲突/坏current/JSON/id拒绝；omitted旧任务阻塞 | 09 |
| S-MIG-495-REAPPLY | 同固定candidateupdate/reapply、source/installed/canonical/dogfood/平台projection/hash/modes/inventory/runtime与零sidecar；retiredownedemptydirs退出 | 02、08 |
| S-MIG-495-REMOTE | 同远端GuruOID与正式Forklock的public/source_locked、providercreate-new→字节审查→force→presetactualinstalled；原失败和恢复单列 | 08、10 |

旧在途构造继续固定`a32ffdca61f432bc6c3e0557fe68486c1422d08f`正式planbuilder/recorder/checker/writer/executor；testprovider只证明构造，不能代替liveGitHub或真实原始业务事务。原generation0证据按freshness/实现影响判断是否需重跑；changedpublic/source/runtime入口必须以本轮exactcandidate重跑，不移植旧pass。

Fork命令从当前package/scripts读取并运行相关CLIunit/integration/generated-template、build/typecheck。Guru运行upgradepackage、registry/schema/graph/source/installed和presetupgradecontract定向测试；nativeowner创建只在隔离sample执行。完整累计多平台clean/existing/update/reapply/workflow-switch/releasecandidate矩阵属于独立Releaseowner；本 task 覆盖全部来源的迁移合同分组和声明平台静态投影，不能泛称ReleaseGate。

## Docs SSOT 与交付边界

RDT新贡献：`docs/requirements-design-test-contributions/495-upgrade-version-families/`的manifest、requirements、design、test、traceability；Architecture新贡献及ADRcandidate位置见design。旧generation0贡献和.73知识作为immutablebefore，不直接覆盖。README、package、spec、平台入口同步公开familyselector迁移及source-specific回退说明。

完整task scope为MIG-495-01..12。首个slice是可执行且本地已验收、固定正式Fork依赖的系列升级候选及合同；remaining work是同一固定远端Guru的formalpublic/provider验收、最终证据晋升与Completion，owner仍是本TaskId/generation1。slice独立交付条件不依赖remaining work已完成；不关闭#495、不宣称系列完整验收通过。失败必须留在本task修复。

正式 Fork `.3` 已合并为 `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c`，main CI `37647767799` 成功，唯一来源锁及精确源码 build/identity 验证通过。469 CLI + 5 core 定向验证通过；Guru G1..G8 与差异代表实际升级/来源回退通过，SSH transport 和暂停期间新增定制编辑保护已修复。当前控制会话接续和最终 dogfood/apply/drift/官方投影已通过，Phase2 正在收敛；远端同源 Guru public/provider 验收尚待发布候选。原.41结果不能代替变更路径的验收。真实业务安装、tag/Release、生产操作和完整Release矩阵未授权。
