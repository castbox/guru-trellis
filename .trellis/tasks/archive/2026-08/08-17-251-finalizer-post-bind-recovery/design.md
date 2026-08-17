# #251 技术设计：Finalizer post-bind recovery 与 legacy plan 退休

## 1. 核心状态顺序

Current preview 的阶段判断改为：

```text
rebuild current plan
  -> validate current transaction against exact plan
  -> if transaction mode=existing_pr_recovery and phase >= archive:
       recover bound PR/HEAD/payload/scope and preserve transaction stage
  -> otherwise evaluate genuine pre-PR provenance reprepare
  -> classify fresh existing-PR adoption only when no owning transaction exists
```

关键原则是“已绑定 owner transaction 的阶段 authority 高于 pre-PR 推断”。这不是放宽 provenance；它只是阻止一个较早阶段的判断覆盖已完成的后续阶段。

## 2. Post-bind recovery predicate

新增或收敛一个 package-private helper，判断 transaction 是否是可优先恢复的 post-bind current transaction。最小条件包括：

- `mode=existing_pr_recovery`；
- rebuilt plan 与 transaction 的 task/repo/base/branch/branch-review/publication/plan digest 完全匹配；
- `adopted_pr` 与 current bound `pr` 结构完整；
- `next_transition` 属于 `archive|push_archive|mark_ready`；
- live PR、remote HEAD 与当前 transition 所要求的阶段一致。

Helper 只做确定性阶段分类；PR/scope/HEAD 的现有严格校验继续由 current recovery preflight 承担。任何 mismatch 抛出当前稳定的 fail-closed error，不回退到普通首次发布。

## 3. Provenance 判断边界

`finalizer_pre_pr_provenance_tail_required` 保留给 `prepared/content_pushed` 且无 post-bind transaction 的路径。调用点在判断前加入 post-bind exclusion，而不是修改 manifest 的通用读取规则去兼容业务仓。

这样同时保持：

- #191 的真实 source-owned pre-PR reprepare；
- #205 的业务 Finalizer 永不进入 extension verifier；
- #208 的 fresh/adopted existing PR recovery；
- #251 的 post-push/archive same-plan resume。

## 4. Legacy closeout-plan 退休模型

选择 Issue 允许的“受控 projection 退休”，不重新 materialize current plan。

### 4.1 Current plan 构建

当 `current_finalizer=true` 且观察到历史 tracked `closeout-plan.json` 已在工作树删除时：

- 从 active `move_paths` 与 `tracked_move_paths` 排除该文件；
- 不把它加入 `required_artifacts`、retained archive paths 或 reviewed tracked bindings；
- 单独把 index 中的历史 entry 记录为 package-private plan projection 字段 `retired_tracked_paths`，唯一 consumer 是 archive transaction path validator/executor。

### 4.2 Archive transaction

Archive commit 的 expected path set 同时包含：

- active task 中正常 tracked move paths 的删除；
- archive core retained paths 的新增；
- `retired_tracked_paths` 的 active-side 删除。

退休路径不要求工作树文件存在，也不进入 archive。Continuity 校验绑定 transaction parent 中的历史 blob 与 current working-tree deletion，拒绝文件被重新 materialize、内容被替换或跨 task 路径混入。

### 4.3 Terminal recovery

Current archived/terminal context 以 transaction、finish summary、PR 与三方 HEAD 为 authority；规范 current archive 不含 `closeout-plan.json`。历史 legacy-only archived route 仍由旧 migration contract 处理，不把 current transaction 误判为 legacy-bound。

## 5. 数据与公共 API

- Public input/outputs、六个 typed exits、Finalizer-to-Merge DTO 均不变。
- 如 plan projection schema 增加 `retired_tracked_paths`，它只属于 Finalizer private plan/transaction implementation，不进入 public DTO。
- Owner-private transaction schema 3.0 只有在当前字段无法表达剩余 transition 时才版本迁移；优先复用现有 `next_transition` 和 adopted/bound PR facts。
- 不创建 tracked `closeout-plan.json`、migration artifact、handoff 或新 checkpoint。

## 6. 测试设计

### 6.1 Focused unit/contract

- post-bind `archive|push_archive|mark_ready` 跳过 provenance predicate；
- pre-PR 无 transaction 仍可返回 provenance reprepare；
- ordinary transaction 或 mismatched plan 不被当作 post-bind recovery；
- external source commit 与 reviewed HEAD 不同的业务 fixture；
- legacy tracked/deleted plan 进入退休删除集合，不进入 move/retained/required 集合；
- archive/terminal current context 接受规范缺失 plan，拒绝重新出现或 identity drift。

### 6.2 Focused installed-package smoke

在干净临时 fixture repo 中仅投影/安装 current canonical package 所需 runtime，运行真实 installed `guru-finalize-task` public wrapper 的 same-plan recovery。该 smoke 不运行 marketplace initial install、workflow preview/switch、official update、preset reapply 或 tag-pinned 验证。

### 6.3 Failure matrix

- PR number/url、Draft state、pre-push HEAD、publication HEAD、payload、close scope、plan digest 漂移；
- remote/PR/local HEAD 不一致；
- arbitrary equal-head Open PR 未由 transaction 绑定；
- retired plan 工作树重新出现或 transaction parent 不含预期历史 blob；
- unexpected archive path/sidecar。

## 7. Docs SSOT Plan

策略：`ssot_first`。

1. Canonical code/package contract：`trellis/skills/guru-team/packages/guru-finalize-task/**`。
2. Durable SSOT：`.trellis/spec/workflow/{workflow-contract,skill-package-contract,data-contracts,companion-scripts,quality-guidelines}.md` 中只更新受影响的 current Finalizer recovery/retirement 合同。
3. Preset/install SSOT：`.trellis/spec/preset/{installer,upstream-ownership}.md` 与必要 README 说明 focused smoke 和 #254 完整 Release Gate 分工。
4. 通过 canonical preset apply 同步 `.trellis/guru-team/skills`、`.agents/skills`、`.codex/skills`、`.claude/skills`、`.cursor/skills`；不手工维护语义分叉。
5. Task planning 只记录本次 delta；Phase 2 完成 durable reconciliation 后再进入 commit/review。

## 8. 回滚与风险

- 主要风险是过早把 transaction 视为 post-bind，或退休路径未进入 archive commit expected set。两者都通过 exact state/identity predicate 与 path-set equality fail closed。
- 若 private plan schema 调整影响历史 migration，保留旧 schema validator 并新增明确 current version；不得静默重解释旧 artifact。
- 回滚以本 task commit 为单位；不修改真实业务仓或历史任务数据。
