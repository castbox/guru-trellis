# Issue #247: 移除 task-local Issue scope ledger

## Goal

在当前 Guru Team Trellis Extension 上独立退役 task-local
`issue-scope-ledger.json` 及其 Issue aggregate authority，使 task identity、
external work item reference、delivery object 和 mutation authority 按现有 owner
职责分离。#247 是当前版本上的小幅优化，不恢复 #305 Evolution 大规模重构，
不依赖或绑定其它 Issue。交付后的单独版本必须在不安装后续 lifecycle package 的
条件下继续运行修改前已支持的完整旧流程；新的 Task lifecycle 由后续 Issue 渐进实现。

## Current Authority

- Live Issue：`https://github.com/castbox/guru-trellis/issues/247`。
- Issue contract：`2026-09-13-r24`；该正文替代旧 body 与历史评论中的实施要求。
- Base：`origin/main` / `ec016827fac81d33faeacb307b0db76d5259dc28`。
- RDT / Architecture：`current-main-0.6.5-guru.50`，状态 `active`；由 reviewed #247
  contribution 和 accepted `ADR-009` 从 immutable `.49` serialized promotion 得到。
- 当前 public graph 仍为 23 Skills / 97 exits / 78 commands；本 Issue 不改变四阶段顺序或无关 owner。

## Requirements

1. 从 current active graph 中删除 `issue-scope-ledger.json`、
   `guru-issue-scope-ledger-*` 及具有相同 Issue 分类聚合语义的 writer、reader、
   precondition、schema registration 和 consumer。
2. Task/workspace creation 不再生成或登记 ledger；Clarification/Readiness 到
   workspace 不再投影 `primary_issue`、`close_issues`、`related_issues`、
   `followup_issues` 组成的 aggregate。
3. 删除所有仅为已废止 ledger 服务的 current Skill Markdown 描述、interface /
   consumer schema、eval/example JSON、DTO 字段、runtime/script、fixture/test、
   manifest/registry 和安装验证内容，而不是保留空字段或死代码。
4. Planning、qualification、Phase 2、Task Commit、Branch Review、Publication、
   Finalizer、Merge、Finish、restore/re-entry 和 Cleanup 均不得读取 ledger。
5. Commit message 与 Branch Review 中的 Issue reference 只能由当前 task、source
   reference 和 reviewed requirement authority fresh 判断；无 Issue、reference-only
   和明确 Issue-backed task 不得被一个 `primary_issue` 默认值混同。
6. Publication 是唯一的 Issue 关闭意图判断 owner：
   - issue-backed completed：task 已完整解决对应 Issue 时，默认判定应关闭；
   - reference-only：只有 live Issue 明确包含合并后仍待完成的验证、观测、发布或其它
     条件，或本次交付未完整覆盖 Issue 时，才保持 open，并记录具体 current-authority 原因；
   - no external work item：不生成 Issue 引用或关闭效果。
7. Publication 基于 current requirement authority、reviewed diff、目标 base/default branch
   与 live Git/GitHub facts形成 PR payload 和关闭决定；不得继续经 ledger、换名文件、隐藏
   aggregate、shared cache、journal、index 或 optional frame 传递 Issue 分类。
8. 执行关闭的 owner 是 GitHub closing-keyword 自动行为：
   - 目标为默认分支的 PR，由 Publication 在 PR body 写入已审查 closing keyword；
   - 目标为非默认分支的 PR 不宣称其 body 关键字会关闭 Issue，当前 PR 只引用 Issue；该
     base 分支后续进入默认分支时，由后续 Publication 基于届时 current authority fresh
     判断并在目标默认分支 PR 写入 closing keyword；
   - workflow 不调用 Issue close API 补偿自动关闭；只有用户显式要求手动关闭时才进入
     单独确认的 GitHub mutation。
9. Finalizer 保留当前 transaction 的 local preparation、push、PR create/update、official archive、
   Ready、handoff 与已声明 recovery；只移除 ledger 输入。它继续向 Merge 投影 exact PR body 的
   最小 SHA-256 identity。Merge 保留独立 semantic review、expected-head、本次 merge 确认、
   post-merge verification 与四个 declared exits；body identity 不一致时在 mutation 前 fail closed。
   `phase2_reentry_required` 继续携带 archived identity 进入 `guru-restore-archived-task`，
   `closure_mismatch` 继续报告 GitHub closing-keyword effect 不完整。
10. 现有项目 update/reapply 时，不主动删除或改写磁盘上的 legacy
   `issue-scope-ledger.json`；active runtime 不读取、不解析、不登记该文件。ledger absent、
   present-A、present-B 不得改变 current task/runtime 的结果。
11. 不迁移旧 task，不保证旧 task artifact、旧 DTO 或旧 schema 能在新 runtime 上继续
    运行，也不为其提供 re-entry、reader、adapter 或 compatibility fixture。current task 的
    authority 不足时仍由当前 lifecycle 的既有 semantic owner 处理，但该行为不是旧 task
    迁移路径，且不得回退读取 ledger 或猜测 closure intent。
12. canonical、dogfood、installed、Shared、Codex、Claude、Cursor 与 preset
    apply/reapply/update 投影保持一致；不修改 Trellis upstream、global npm、
    `node_modules` 或业务仓库。
13. 修改前后既有 producer/consumer、target/stop、成功与恢复语义保持一致；只安装本次 candidate
    即可从无 task/无 ledger 起步，经过真实 production wrappers 完成 Intake、Task creation、Planning、
    Phase 2、Commit、Branch Review、Publication、Finalizer、Merge 与 current terminal。
14. 声明 `guru-ledger-free-runtime@1.0.0`，canonical 与 installed manifest 只记录 capability id/version
    和 current projection identity；该 capability 不宣称新 lifecycle 已激活，也不依赖 #398。
15. 明确披露旧流程的提前归档、PR 冲突及同一 task 多次 Delivery 接续局限；这些是后续 Issue 范围，
    不是 #247 已解决能力，也不阻止本次兼容交付。

## Compatibility Decision

本 Issue 不提供 ledger reader、adapter、dual-read、dual-write、ledger conversion 或隐藏替代
aggregate，但必须保持当前生产调用链在同一版本内端到端完整。ledger 专属 public 字段按既有
API 版本约定收敛；仍有旧流程直接 consumer 的最小步骤局部 Issue identity、reviewed close set、
archive locator 和 recovery DTO 保留。历史 schema 可作为明确 inactive 的兼容验证资产保留，
但不得恢复 ledger reader。legacy ledger 仅作为 inert history 原样保留。

## Out Of Scope

- 不实施或恢复 #305 Evolution 大规模重构。
- 不新建或重构 lifecycle owner、graph-entry router、全局 authority graph、每入口全图扫描
  或 `guru-validate-authority-free-graph` Skill。
- 不强制所有 PR 改为 Refs-only，不禁止旧 Finalizer 归档，不替换现有 Merge/Restore route。
- 不实现同一 active task 多个顺序 PR、merge 后保持 active 或新的独立 Completion/Finish/Cleanup。
- 不等待、消费或修改 #249、#250、#292、#293、#261、#248、#252、#267 以及任何其它 Issue。
- 不迁移旧 task，不支持旧 task schema/DTO/runtime continuation，不增加 legacy task recovery。
- 不执行完整多平台 exact-candidate Release matrix、tag、GitHub Release 或生产业务仓验证。
- 不处理恶意伪造、对抗输入、TOCTOU、锁、压力竞态或未要求的跨 OS 加固。

## Acceptance Criteria

- [ ] current active graph 中 ledger 名称、ledger schema id 及 ledger aggregate 的
      writer、reader、precondition、registration、consumer 均为零。
- [ ] 新 task/workspace 创建不产生 ledger，也不在 task artifact/result/interface 中声明它。
- [ ] 所有仅服务 ledger 的 active Skill 文案、schema、eval/example JSON、DTO、script、
      fixture/test、manifest/registry 内容已删除；没有 alias、adapter、dual-read/write、
      compatibility reader 或替代 aggregate。
- [ ] ledger absent、present-A、present-B 不影响 current lifecycle；update/reapply 不主动
      删除或改写 present 文件，但不为旧 task 提供迁移、读取或兼容运行能力。
- [ ] Issue-backed completed、Issue-backed remain-open、no-Issue 三条 Publication 判断路径通过；
      completed 默认关闭，remain-open 必须有 live authority 中的具体未完成条件。
- [ ] 默认分支 PR 使用 Publication 已审查的 closing keyword；非默认分支 PR 不宣称其 body
      关键字会关闭 Issue，后续默认分支 Publication fresh 判断并编码关闭决定。
- [ ] Commit、Branch Review、Publication、Finalizer、Merge、Finish、restore/re-entry 和
      Cleanup 均不读取 ledger，source reference 不自动授权 closure、merge、Finish 或 Cleanup。
- [ ] Finalizer/Merge 不重新决定关闭范围、不调用 Issue close API；Finalizer-to-Merge handoff
      保留 Publication-reviewed PR body 的最小 identity，body-only metadata drift 在 merge mutation
      前 fail closed；Merge 后 closure result 与 live GitHub facts 一致。
- [ ] Finalizer 的 archive/Ready/handoff、Merge 的四个 exits、`phase2_reentry_required -> Restore`
      及现有 stale/reprepare/existing-PR/lost-result 路径在无 ledger 条件下保持可用。
- [ ] 代表性 installed Git fixture 通过真实 production wrappers 串联完整旧流程到 current terminal；
      remote provider 模拟与真实 GitHub evidence 边界明确。
- [ ] canonical/installed manifest 均声明同一 `guru-ledger-free-runtime@1.0.0` projection identity。
- [ ] current Skill id、owner、typed route 和四阶段 workflow 顺序除 ledger 必要字段删除外保持不变。
- [ ] canonical、dogfood、installed、Shared、Codex、Claude、Cursor 及 preset
      apply/reapply/update 投影一致，recursive sidecar 为零。
- [ ] 本变更涉及的 package/runtime/eval/integration tests、source/installed validation、dogfood
      overlay drift、managed byte/mode、schema/registry/consumer 检查及一个代表性 clean 或
      existing install/update 场景通过。
- [ ] fresh committed full-diff Branch Review 覆盖完整变更且无 open P0-P3 finding；未执行的
      Release matrix、tag、GitHub Release 和业务生产验证明确标记为 deferred。

## Docs SSOT Plan

- Requirements：创建 task-owned RDT contribution，定义 ledger current authority 退役、
  三种 external-work-item/closure 正常路径、legacy inert preservation 和无兼容层边界。
- Design：在同一 contribution 中记录 owner-by-owner 数据来源替换、public DTO 收敛、
  active asset 删除与 canonical/installed/platform 投影策略。
- Test：在同一 contribution 中定义 active-zero inventory、三路 closure、legacy
  absent/present-A/present-B 等价、安装更新保留和跨投影验证场景。
- Architecture：本变更替换 ledger authority 来源但保持旧 lifecycle owner、edge、时点和恢复语义；
  task-owned contribution 与 `ADR-009` 必须按 r24 修订为兼容交付边界，唯一 active `.50` 同步
  capability、已知局限和后续 Issue 边界；promotion-created diff 仍须 fresh Task Commit 与独立完整 Branch Review。
- Historical boundary：不修改 archive、既有 accepted ADR、superseded/released RDT 版本或旧
  release evidence；这些历史对象也不是新 runtime 的兼容或迁移输入。
