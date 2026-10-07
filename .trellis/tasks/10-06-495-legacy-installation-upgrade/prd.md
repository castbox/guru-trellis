# #495 版本系列原地升级 — generation 1 需求

状态：Planning 已批准；本轮已进入实现。本文替换原 generation 0 的固定样本规划；原交付和验收由 Git 历史及 [原验收贡献](../../../docs/requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/test.md) 保留，不构成本轮通过证据。
Authority：[Issue 正文](https://github.com/castbox/guru-trellis/issues/495)、[版本系列修正](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6040798771)，以及正文引用的混合库存、候选发布顺序、隔离构造在途样本说明。TaskId 为 `495-legacy-installation-upgrade`，generation 为 1。

## 目标与事实

让 `v0.6.x-guru.*` 与 `v0.7.0-guru.*` 系列中的正式安装升级到选定的后继 Guru/Fork 来源，保留业务内容、合法任务身份和可接续的业务事实。原实现将最低代表样本固定成唯一来源，拒绝其它正常安装。完整范围已由当前用户请求及 GitHub 修正评论明确。

## 来源分组与覆盖归属

2026-10-07 直连远端 tag 盘点有 18 个 `v0.6.x-guru.*` 和 1 个 `v0.7.0-guru.*` 正式 tag。下表覆盖全部 19 个；未发布 `.2` 安装来源另列。tag 后缀与 extension revision 不等价，不能由 tag 名推算 installed version。

| 组 | 正式来源归属 | 安装清单与资产管理差异 | 代表验收来源 |
| --- | --- | --- | --- |
| G1 | `v0.6.5-guru.1/.2` | core 0.6.5；schema 1.0，无 skill_packages/overlays 和 expanded managed hashes；早期清单混含 upstream-owned 入口 | `.1` |
| G2 | `v0.6.5-guru.3` | core 0.6.5；schema 1.0，有 package/overlay receipts，尚无 expanded managed hashes；实际 extension 为 `.25` | `.3` |
| G3 | `v0.6.5-guru.4/.5` | core 0.6.5；schema 2.0，尚无 expanded managed hashes；actual extension `.25/.27` | `.4` |
| G4 | `v0.6.5-guru.7/.8/.9/.10` | core 0.6.5；schema 2.0，有 expanded managed hashes；actual extension `.31/.33/.34/.36` | `.7` |
| G5 | `v0.6.15-guru.1/.2/.3/.4/.5/.6` | core 0.6.15；schema 2.0；tag `.1` 实际 extension 仍是 `0.6.5-guru.37`，其余为 `.38/.39/.40` | `.1` |
| G6 | `v0.6.16-guru.1`；其后同 extension 的可核验 source 安装 | extension `0.6.16-guru.41`；实际 core 分别 0.6.16 与 0.6.17 | 正式 tag；后续 source `29954796d26dda59a57aede400bbcb1347e619df` 仅补 core 映射差异 |
| G7 | `v0.6.17-guru.1/.2` | core 0.6.17；extension `.42/.43`；`.2` 安装选择已退役 all_platforms | `.2`；`.1` 的配置投影差异定向验收 |
| G8 | `v0.7.0-guru.1`；本轮 base 的 `0.7.0-guru.2` source 安装 | core `0.7.0-castbox.1/.2`；schema 2.0；current task/control 保留路径与已知 legacy 转换路径分开 | 正式 `.1`；`.2` 仅补 target-relative/current control 差异 |

这些是安装迁移合同分组，不是支持白名单。所有正式版本均通过同一来源识别和资产投影检查，复用该组实际升级、恢复及回退的代表证据；只有出现新的实际迁移行为差异才拆组。任务格式独立于版本，legacy/current/deferred 和状态场景横向覆盖。历史 dogfood manifest 只用于发现差异，不冒充该 tag 的正式安装 before；正式 tag 的旧 installer 在干净隔离样本生成实际安装。


本轮 base 为 `main@11ef591ceb454041540721d44bcbb72e66b0f22e`；RDT/Architecture current 为 `current-main-0.6.17-guru.73`。现有 Fork lock 为 `8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1`；它仍只接受 `migrate --from 0.6.16`，普通 update 拒绝不同 installedVersion。Guru preview、旧 manifest、source hash 补齐和 rollback 返回版本也写死 `.41`。

## 支持合同

1. 系列判断涵盖 release tag 与实际 extension revision 两个轴，不能用 release 后缀推算 extension 后缀；每个来源核对正式 source 与真实安装 receipt、manifest/schema、实际 core 和 Fork 映射。不得再按 `.41` 或 `.1` 的 revision 白名单排除同系列来源。
2. 每次升级的目标必须是该来源的后继：Guru extension 与 Fork core 不降级，精确目标 source/lock 含所需实现。来源等于目标时走同候选 reapply，不能报告一次版本升级。未来不存在或未发布来源不冒充已验证；新来源符合相同合同后进入相同入口。
3. 本轮实施目标拟为 Guru `0.7.0-guru.3` / Fork `0.7.0-castbox.3`，覆盖现有 `.1`、`.2` 来源。这是待实现并固定的候选，不是已发布能力；repository tag、extension、core、knowledge identity 分别记录。
4. 安装版本与任务格式独立：当前格式任务保留原 TaskId、generation、source、关系、业务字段、绑定和会话事实；只有已知旧格式按明确投影转换。当前 runtime 保持 current-only，旧 parser 只位于一次性升级边界。
5. 原 MIG-495-01..09 继续适用，下面增量不削弱它们。真实业务 checkout/worktrees 只读；预演写入隔离脱敏样本。

## 行为与验收

| ID | 必须行为 | 可观察验收 |
| --- | --- | --- |
| MIG-495-01 | 写前读取安装、受管清单、配置、平台、task/archive、Git/control/session；AI 审查逐文件/逐任务计划后取得具体副作用确认 | public preview 不写目标；列出 source/target 映射、write/remove/preserve 和任务处置、实际命令 |
| MIG-495-02 | Fork、workflow marketplace、Guru preset 各按 ownership 更新；保留业务/spec/规划/历史、有效配置、本地定制和无关 dirty/untracked | bytes/modes/Git 状态对照；有效设置语义不变，官方必需 additive config 单列；逐项解决 `.new/.bak`；退役受管空目录清理，含用户内容的目录保留 |
| MIG-495-03 | 保留合法非 UUID TaskId；旧 task generation 初始化、source/关系/缺字段按设计转换；当前 task 原字节保留 | 完整旧记录和两种真实精简旧记录通过 current schema；当前任务不重置 generation/source/status/meta，不因升级变成 completed |
| MIG-495-04 | AI 明确需求来源及 Issue disposition；复用 current branch/checkout/session owners | exact_source/reference_only 明确；TAPD 保留业务来源且不虚构 GitHub source；有效当前绑定不重建，缺失/旧绑定由正式 owner 承接 |
| MIG-495-05 | planning 接续当前 Planning；未发布 in_progress 保留 commit 与未提交工作，重新审查受影响 gate 后接续 dev/check | 两条实际 owner re-entry；真实脱敏项目 Architecture、两类 qualification 与语义 gates；schema pass 不等于接续 pass |
| MIG-495-06 | PR、merge、旧 Finalizer/Finish 在途逐任务诊断；旧 gate 不成为 current pass | 真实 live PR/merge 各一项；旧正式 writer 生成的隔离非 terminal 快照明确标注构造边界；保留 bytes/modes/refs，不重复 commit/push/PR/merge；pinned-old/manual 处置 |
| MIG-495-07 | 写前备份；普通部分写入恢复；无新版业务工作时实际 post-write rollback | 每个受支持来源恢复自己的 core/Guru/task/control；暂停期间新增业务事实阻止覆盖回退，resume 不吸收新工作为旧基线；旧 runtime smoke 通过 |
| MIG-495-08 | 固定正式 Fork lock/CI、Guru source，验证 canonical/dogfood/installed/platform/inventory/runtime/reapply/drift/sidecar | 同一固定远端 Guru commit 的 public/source_locked/provider 实际运行；后继文档 HEAD 不冒充运行；完整多平台 Release matrix 单列未验证 |
| MIG-495-09 | current/已迁移任务与无关已诊断旧 active 共存 | current creator/ref/id/branch/checkout/session 成功；旧目标/身份占用/同身份冲突/坏 current/JSON/id 继续拒绝；遗漏旧记录阻塞，deferred 原字节保留且不成为 current authority |
| MIG-495-10 | 版本系列进入同一 public 升级入口，不按代表 revision 排除 | 全部现有正式 tag/source 映射有 disposition；上述每种不同安装清单/资产管理/任务控制合同运行代表性预演，无仅改版本文件的成功声明 |
| MIG-495-11 | 当前 task、合法 shared/local control 和 session 保留，升级不强制旧转换 | `.7.0-guru.1` 与 `.2` 的 planning/in_progress owner 接续；linked checkout 验证；普通旧私有格式在唯一 owner 边界按精确合同迁移，不手填 current gate/ledger |
| MIG-495-12 | 来源特定的备份、恢复、回退和报告 | legacy 与 current 来源分别 post-write rollback；输出实际恢复版本，非固定 `.41`；不覆盖其它 checkout 的合法工作 |

## 数据与处置边界

旧字段移除只作用于已审查 active 转换；退役人员字段原字节保存在 private backup，archives、`.developer`、journal/traces 不改写。精简记录补全空数组、空对象、nullable null、priority P2、description/notes 空字符串；createdAt 无可核验事实时用 current schema 的空字符串并报告 unknown。非空 subtasks 经 AI 核实同语义映射到 children；不能无损表示或真实未知字段时保留并给出具体处置，不静默丢弃。

旧 TaskId/TaskRef 继续占用身份，但不成为 current lifecycle candidate。缺失或 stale 路径只作为线索，事实唯一才能重建绑定；不能清空 dirty 业务工作来满足新 checkout 的 clean 要求。untracked-only task、来源/分支真实歧义与不兼容在途逐案报告，不自动 commit 或授予关闭意图。整仓安装成功、任务转换成功和实际接续成功分别报告。

已完成交付仍读取 live facts；gate 是否仍有效由当前 owner 按当前合同判定，不能沿用 generation 0 的通过结论。普通失败、stale/mismatch 属于范围；不引入攻击模型、故意伪造、额外锁、并发压力或 fault injection。

## 完成定义

MIG-495-01..12 的适用场景有实际执行证据，正式 Fork successor 与 Guru 固定来源可复现，文档入口真实可执行，RDT/Architecture contribution 经独立完整 committed Branch Review 后晋升，再检查晋升 diff。首个 Refs-only 候选 Delivery 只交付可用于远端验收的实现和合同；远端同源验收及最终 Completion 前不得关闭 #495。

不恢复人员体系、不维持长期双读、不批量迁移 archives、不自动完成/关闭任务、不改业务代码或生产配置、不 rewrite Git history。本轮规划不执行真实业务安装、版本发布、commit/push/PR/merge 或 Fork Git 副作用。
