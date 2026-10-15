# #566 实施规划

## P1 状态与 Delivery Policy

Task566-single-checkout-upgrade/generation0 仍为 planning，branch codex/566-single-checkout-upgrade，base main；本文件是执行计划，不是实现或验证通过结果。需求见 PRD；唯一来源设计处置见 design.md D1。

Delivery Policy=full：本任务一次交付两个独立维护能力及原 owner 接口、runtime 隔离、文档和联合验证；下列是内部有序实施阶段，不把 tools-only 子集当作整个 Issue 完成。Completion 要求 R1-R14/A1-A9 在 Guru fixture/匹配公共候选边界都有实际证据；真实业务安装、外部验收、发布和 Release 全平台矩阵保持非目标。正式 source lock 缺能力的阻塞必须真实，local_candidate 的联合证明不宣称正式来源或 release。

## P2 顺序与边界

### S0 规划与实际依赖

- 完成 Author → Wording → final Architecture → Approval；之后展示实际实现写集与激活副作用。
- 回读 #40 actual matching CLI/Core candidate、public maintain contract、bin/SDK、类型/错误/恢复结果。独立 installed tar pair 作为隔离 local_candidate 输入，不能用 mock 或 deep import dist/commands 替代。source_locked 校验当前正式锁不具能力时应写前阻塞；本轮不更新 lock。
- 清点 target/source native runtime 与 pointer；R1/R3 的 shared/peer 保留成为实际 before/after 证据，不只检查文件名。

### S1 共用事实与独立 tools owner

- 新增 canonical `trellis/skills/guru-team/packages/guru-upgrade-tools/` complete semantic package、closed independent schemas/commands/exits及最薄 determinist executor。
- 复用/提取 Sync 只读 base selection；保留 Sync clean/fetch/fast-forward。覆盖显式目标、config/base、dev/develop/main/master/remote-default、选中分支无 checkout/歧义/prunable 和本地 asset conflict。
- 在原 managed Python owner 的 bootstrap/resolve/validate 中实现 tools-only checkout-local override（primary/linked 同样隔离），不改原 common-default activation。目标真实 interpreter 与所有 peers 的原解析结果分别验证。
- 委托公共 tools_install；Guru 当前 installer负责自身 assets/manifest/平台与 conflict/sidecar。仅新 source-loaded operation 处理旧 manifest，不放宽 ordinary apply/current validators。
- 整合准确 Guru asset/pointer preimages 与 upstream recovery refs，实际 target validation/native consumer 才能输出 tools_upgraded。

### S2 所选旧任务 owner 与原历史核验

- 新增 canonical `guru-maintain-legacy-task/` complete package；convert/history_closeout/resume/rollback 各自独立输入，不做通用 metadata bag 或新 lifecycle。
- 在原交付/合并 owner 新增明确只读历史核验 profile；不经 current parser/ready，保留普通 Publication/Merge前置和唯一写者。真实 PR/head/merge/target 与 owner必须核实；不产生当前通过结果。
- 使用公共 inspect/prepare/apply/recovery 做 Task2 projection、五 artifact 映射、raw source、session/binding/alias、归档屏障；不写第二套公共 parser/converter。
- 按design D5在Publish/Merge/Finish及真实inventory命中的其他原gate owner增加legacy_control_retirement；prepare先核实并固定private preimages，公共保存源可读后按Publish→Merge→Finish→其他选定owner退役，不依赖已移除active tree，外部未决事实保留note。原私有 state owner逐项处理选定Task/gen，组合tools operation独立审查。历史路径不升级目标工具、不造 Completion/Finish、不清理资源。实现实际目标 native no-selection／continuation＋下一 Guru owner，不以外部代执行替代。
- 兼容性与后续业务保护覆盖整个“安装→任务转换→请求tools回退”顺序；写前阻断不兼容组合，固定原ID/备份，不重导入交付。

### S3 成套发布面与原生联合证据

- registry、Interfaces/command descriptors、必要 standalone discovery/workflow routes、MIGRATION-566、README/spec与source inventory同步。
- canonical workflow `.trellis/workflow.md`、Guru package安装树、声明平台overlay/discovery保持；改overlay后运行 apply.sh --repo . 和 check-dogfood-overlay-drift.sh，逐项处理.new/.bak。不手改安装副本作为唯一源头。
- 使用最多一个代表性旧安装拓扑运行真实公共CLI/Core＋Guru source-loaded wrapper＋目标原生入口。并行worktree只是该样本的保留对象，不扩张多平台Release矩阵。
- 完成Docs SSOTdelta协调后，再执行完整当前scope Architecture/Phase2/check；Commit、独立完整Branch Review、promotion及后续交付各走原owner，不在实现中自动push/PR/merge。

## P3 Docs SSOT Plan

strategy=delta_first。原 RDT writer `guru-maintain-requirements-design-test-ssot` 在 task-owned `docs/requirements-design-test-contributions/566-single-checkout-upgrade/` 写 requirement/design/test、双向trace与真实结果；原 Architecture writer消费 `.trellis/tasks/10-15-566-single-checkout-upgrade/architecture/contribution.md` 和必要 ADR candidate。只修改贡献，不竞争共享 CURRENT/README identity。最终 Phase2之前由原RDTowner完成delta reconciliation；独立 committed BranchReview之后才进行expected-current-bound promotion，再fresh gates。规划和task.py start不代表晋升。

## P4 验证与 Requirement 承接

| 场景 | 真实验证对象与结果 | PRD |
| --- | --- | --- |
| target/base选择 | 真实Git仓库、refs、registered checkout和只读resolver；explicitwins、有序选择、不可用不降级、不create/switch/fetch | A1/R1-R2 |
| 单checkout工具切换 | public candidate+Guru真实 wrapper；active/archive Task、planning、shared/public/privatecontrols、peerbytes/modes及runtime解析均保留 | A2/R3-R6 |
| 首次切换与诊断 | 不预写版本/declaration；required conflicts/skip/sidecar不能成功；合法新任务操作实际可用，旧状态maintenance_required包含可调用完整source入口 | A3-A4/R4-R8 |
| 旧任务启动循环 | 基线已更新、旧target正常入口格式拒绝、Git候选无冲突；从外部完整来源只读prepare，再精确转换/必要独立tools/原Reconcile语义，目标native＋下一owner可执行 | A6/R8-R10,R12,R14 |
| 仅历史保留 | oldtarget工具不变；archive rawtree/note先可读再精确退役公共及Guruprivatecarriers；旧正常current无选中；identity/外部责任/其他会话/peers保留 | A7/R9,R11 |
| 已交付待验收 | 原owner验证真实历史事实，Task/planning/history保留、当前gates不自动pass；目标Completion owner返回evidence_pending，无新Delivery | A8/R9-R11,R14 |
| 固定操作恢复 | 普通partialwrite与lostoutput使用原ID/原backup；后续owned-edit保护、unrelated业务保留；install→convert→toolsrollback不兼容写前阻断 | A9/R5,R13 |
| 分发兼容 | canonical/dogfood/installed、声明投影、reapply/drift/sidecar与原Plan2/current流程定向回归；普通Issue最多一个代表安装样本 | A5/R6-R7 |

测试使用现有包的unittest/schema/graph、实际Gitworktree与nativewrapper；具体新增test入口随实现模块就位后登记，不用计划中的不存在路径冒充已执行。公开marker/profile字符串的测试必须证明消费/路由效果，不能只比常量。超过3000行的触达非生成文件先做必要小拆分，不扩张历史债务。无恶意输入/锁/TOCTOU/压力/faultcampaign。

## P5 副作用与终态

规划写集仅本Taskplanning/docs与task-ownedArchitecture贡献/ADR、官方context JSONL。实现写集限定上述canonical packages/runtime/preset/workflow/schema/必要README/spec、受管dogfood投影及定向tests；不变更正式source lock、不操作实际业务安装或旧业务Task。

真实目标安装/迁移/历史收尾、基线Git整合、commit/push/PR/merge、发布与清理均须展示各自精确对象后走原owner。上游#40尚未提交不授权本会话替其提交。Task保持planning直到当前plan展示及activation边界完成；不在任何artifact中记录授权或授权过程。
