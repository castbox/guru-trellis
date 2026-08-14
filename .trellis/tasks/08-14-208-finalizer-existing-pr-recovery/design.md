# 技术设计

## 1. 设计原则

现有普通首次发布合同保持不变：无 owner transaction 时，远端 branch 必须不存在，或停留在 reviewed HEAD 的历史基线；同时不得存在 Open PR。新增能力只在完整 current Publication authority 下，显式选择 `existing_pr_recovery`，并以新的 owner-private transaction 状态接管唯一 PR。

```text
Publication ready
  -> Finalizer preview
  -> ordinary first publication | existing_pr_recovery | blocked
  -> current-conversation confirmation
  -> bind exact PR + pre-push HEAD transaction
  -> optional exact fast-forward push
  -> converge current Publication title/body
  -> archive + archive push
  -> preserve Ready or Draft-to-Ready
  -> three-way HEAD verification
  -> ready_for_merge
```

## 2. 候选识别

复用并收紧 `resolve_closeout_pull_request`：

- 继续由 `gh pr list --repo --head --base --state open` 获取候选；
- 继续验证 repository/head/base、canonical URL、head repository、fork 标记、head SHA 与 Draft 状态；
- recovery 要求候选唯一且属于目标 repository；
- 额外读取/验证 PR 当前 title/body 和 close scope 所需 facts；
- PR 为 Closed/Merged 不会进入 Open 候选；若显式历史查询发现同 identity 已终止，返回稳定 blocked reason，而不是创建新 PR。

## 3. Recovery eligibility

在 `finalization_pre_mutation_remote_preflight` 上层增加语义明确的 recovery classification，避免把普通首次发布的失败分支改成宽松成功：

- `ordinary_unpublished`：零 PR，沿用现有逻辑；
- `existing_pr_recovery`：唯一同 repo/head/base PR，当前 task/Publication/scope/payload current，remote PR HEAD 等于 publication HEAD 或为其严格祖先；
- `blocked`：其它情况。

Ancestry 使用现有 Git `merge-base --is-ancestor` helper 判定。必须同时绑定 remote branch HEAD 与 PR `headRefOid`；二者不相等时阻断。

## 4. Transaction 设计

将 current transaction 升级为能区分普通发布与 recovery 的新版本，保留旧 schema 2.0 为显式 legacy：

- `mode`: `ordinary_publication | existing_pr_recovery`；
- recovery 专属 `adopted_pr`：number、canonical URL、initial draft state；
- `pre_push_remote_head`：首次 mutation 前的 exact PR/remote HEAD；
- `branch_review_commit`、`publication_head`、Publication title/body 与 close issues继续绑定；
- next transition 复用现有 mutation 序列，仅增加必要的 metadata convergence/Ready-preservation 表达，不新增 workflow external exit。

Transaction validator 必须按 mode 使用互斥 required fields。普通 transaction 不携带 adoption 字段；recovery transaction 缺少任一 adoption identity 时无效。

## 5. Mutation 顺序

### 5.1 Ready PR

1. 写入 recovery transaction；
2. 若 pre-push HEAD 是严格祖先，push exact publication HEAD；相等则跳过；
3. 重新读取 PR/remote HEAD 并验证 transaction identity；
4. 将 title/body 收敛为当前 Publication DTO；
5. 执行官方 archive、唯一 archive commit/push；
6. 保持 Ready，不调用 Draft-to-Ready；
7. 验证 local/remote/PR HEAD 一致并物化 `ready_for_merge`。

### 5.2 Draft PR

前五步相同，之后沿用现有 `mark_ready` transition；不得创建或绑定第二个 PR。

每一步完成后 transaction 只前进一个确定性 transition。恢复从 current transaction 与 live facts重建状态，不以旧 PR payload 或旧 task archive 作为 authority。

## 6. Issue Scope 与 PR payload

- 从当前 task ledger 与当前 Publication review projection得到 close/related/follow-up 集合；
- 从 live PR body解析 current close scope，并要求与 reviewed scope兼容；
- 不从旧 PR body继承 title/body authority，最终 body完全等于当前 Publication DTO；
- scope mismatch在任何 metadata mutation前阻断。

## 7. Preview 与 Gate

Preview 的 `expected_actions` 增加结构化 recovery 信息，但公共 typed exits不变。语义 gate 必须说明：

- recovery mode与唯一 PR；
- PR/remote/publication ancestry；
- initial Draft/Ready；
- 是否需要 push、metadata update、archive、mark-ready；
- transaction将绑定的 immutable facts；
- 未验证或阻断原因。

用户确认只存在于当前对话，不写入 transaction、gate或其它 artifact。

## 8. 测试与 fixture

- Package unit/integration fixture构造真实 Git ancestry：旧 PR head commit -> 新 reviewed/publication descendant；
- fake GitHub adapter记录 push、edit、ready、create PR mutation计数；
- recovery重放验证各已完成 transition的 mutation计数为零；
- 负向矩阵逐项绑定稳定 reason code；
- `verify_installed_closeout.py` 增加 installed wrapper真实拓扑回归；
- source/installed/platform copy identity由现有 preset测试验证。

## 9. Canonical 与投影

只修改 `trellis/skills/guru-team/packages/guru-finalize-task/` canonical package和必要的 `.trellis/spec/` SSOT。通过 preset `apply.sh --repo .` 生成 installed/shared/Codex/Claude/Cursor副本，处理所有 `.new/.bak`，再运行 dogfood drift检查。禁止直接把 generated copy作为源头。

## 10. 兼容与回滚

- Stable Skill id、external exit与 Merge consumer保持不变；
- transaction/gate schema如需升级，current无前缀资产指向新版本，旧版以显式版本文件保留；
- 回滚时恢复 canonical package与 spec，再重新 apply preset；不得只回退 installed副本；
- 旧 transaction不满足新 recovery字段时只能沿其原 ordinary/legacy恢复合同或 fail closed，不自动升级为 adoption。
