# Issue #247: 移除 task-local Issue scope ledger

## Goal

在当前 Guru Team Trellis Extension 上独立退役 task-local
`issue-scope-ledger.json` 及其 Issue aggregate authority，使 task identity、
external work item reference、delivery object 和 mutation authority 按现有 owner
职责分离。#247 是当前版本上的小幅优化，不恢复 #305 Evolution 大规模重构，
不依赖或绑定其它 Issue。

## Current Authority

- Live Issue：`https://github.com/castbox/guru-trellis/issues/247`。
- Issue contract：`2026-09-13-r19`；该正文替代旧 body 与历史评论。
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
9. Finalizer 只绑定并执行已审查 Publication payload，并向 Merge 投影 exact PR body 的最小
   SHA-256 identity。Merge 保留独立 semantic review、expected-head 与本次 merge 确认，且必须在
   mutation 前验证 live PR body 与该 identity 一致；不一致时直接 fail closed，由调用方重新进入
   fresh Publication/Finalizer，Merge 不新增 reprepare typed exit，且不得按漂移后的 body 重新决定
   Issue 是否应关闭。Merge 后只以 live
   PR/Issue facts验证 GitHub 自动关闭结果，不根据历史 ledger 宣称成功。
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

## Compatibility Decision

本 Issue 明确不提供向后兼容。内部 Skill I/O、artifact schema、DTO、script 参数和
fixture 直接演进；不保留 alias、adapter、dual-read、dual-write、compatibility reader、
旧字段 nullable 壳或隐藏替代 aggregate。历史 archive、ADR、旧版本 RDT/release evidence
保持 immutable history，不回写删除。legacy ledger 文件只作为 inert history 原样保留，
不构成 current compatibility consumer。

## Out Of Scope

- 不实施或恢复 #305 Evolution 大规模重构。
- 不新建或重构 lifecycle owner、graph-entry router、全局 authority graph、每入口全图扫描
  或 `guru-validate-authority-free-graph` Skill。
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
- Architecture：本变更修改 current authority/owner integration、Issue closure 规则与
  distribution contract，按 `target_native` 由 task-owned Architecture contribution 承接；
  serialized promotion 已建立唯一 active `.50` 并接受 `ADR-009`，promotion-created diff
  仍须 fresh Task Commit 与独立完整 Branch Review。
- Historical boundary：不修改 archive、既有 accepted ADR、superseded/released RDT 版本或旧
  release evidence；这些历史对象也不是新 runtime 的兼容或迁移输入。
