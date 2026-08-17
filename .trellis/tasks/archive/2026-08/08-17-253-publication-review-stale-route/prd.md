# #253 修复 planless publication_review_stale 路由校验

## 背景

Finalizer 在 Publication Review payload 绑定原 reviewed commit、而当前任务 HEAD 已前进时，能够正确识别 `publication_status=stale`，并在尚无 closeout plan、transaction 或发布副作用的情况下进入 `publication_review_stale`。

当前缺陷发生在 route recorder/checker 之前的确定性校验：`finalization_validate_route()` 先把所有含 `branch_review_commit` 的输出统一绑定到 closeout plan。planless stale 场景中 `plan is None`，因此合法的 Publication owner commit 被错误地与 `None` 比较，导致满足 public schema 的 stale route 无法进入 `guru-review-task-publication`。

## 目标

1. `publication_review_stale` 在无 closeout plan 时使用当前 Publication owner 已验证的原 reviewed commit。
2. stale route 同时绑定当前 stale status、stale reason、task ref 和 owner commit。
3. 合法 route 依次通过 production recorder、checker 与 public invocation，并只返回 Publication Review。
4. 保持所有 plan-backed exits 的 plan、commit、HEAD 与 freshness 校验强度不变。
5. 同步 canonical package、dogfood、安装态和平台 managed copies。

## 需求

### R1 Route 专属 authority

- `publication_review_stale.branch_review_commit` 必须与 `context["publication_branch_review_commit"]` 完全一致。
- `task_ref` 必须与当前 public input 的 task ref 完全一致。
- `stale_reason` 必须与当前 `context["publication_stale_reason"]` 完全一致。
- `publication_status` 必须为 `stale`，且当前 transaction state 必须与 stale re-entry 相容。
- route 只返回既有三个 seed fields，不创建 closeout plan、transaction 或 Git/GitHub 副作用。

### R2 相邻 route 不弱化

- `resume_finalization`、`reprepare_required`、`ready_for_merge` 继续使用现有 plan-bound commit、publication HEAD、plan ref、transaction state 和 executor-marker 校验。
- `base_reconciliation_required` 的 exact owner-facts equality 保持不变。
- `blocked` 仍可在不相容状态下 fail closed。

### R3 回归覆盖

- 增加 planless stale 原生 fixture：Publication payload 保留原 reviewed commit，task HEAD 已前进，preview 无副作用。
- 正例覆盖 preview、production recorder、checker、public invocation 的完整链路。
- 负例覆盖错误 task、非 owner commit、错误 stale reason、Publication 已 current。
- 增加相邻 plan-backed route 回归，证明本修复未放宽通用校验。

### R4 分发与安装态

- canonical `guru-finalize-task` package 是唯一代码源。
- preset apply 同步 `.trellis/guru-team/skills/packages/` 与 `.agents/.codex/.claude/.cursor` managed copies。
- 验证 canonical、dogfood 和平台 copies 字节一致，overlay drift 为零，且没有 `.new` / `.bak`。
- 运行一个聚焦的 clean installed-package smoke，只覆盖本 Issue 的 stale re-entry production wrappers。

## 验收标准

1. 无 closeout plan 的 preview 返回 `transaction_state=publication_review_stale`、`publication_status=stale`、`side_effects=false` 和空 actions。
2. 合法 stale output 保留 Publication owner 返回的 40 位 reviewed commit。
3. 合法 output 通过 production recorder、checker、public invocation，并投影至 `guru-review-task-publication:publication_review_stale`。
4. 错误 task、owner commit、stale reason 和 current Publication 四类负例全部 fail closed。
5. plan-backed exits 的原有强校验继续通过回归。
6. canonical、installed dogfood 与平台 managed copies 同步，overlay drift 和 sidecar 检查通过。
7. 聚焦 installed-package smoke 通过。
8. 不运行或声称通过完整 throwaway initial install、workflow preview/switch、official update、preset reapply、全平台矩阵或 tag-pinned smoke。

## 不在范围

- Issue #251 的 post-bind same-plan recovery 与 legacy closeout-plan migration。
- Issue #254 的累计候选发布、完整安装/升级矩阵和 tag 发布。
- 业务仓库 Issue #52 / PR #75 的任何修改。
- public schema、Interface、typed exit、consumer 或 seed fields 的迁移。
- 恶意伪造、对抗性绕过、锁、TOCTOU、并发压力、跨 OS 原子性或额外 fault injection。

## Docs SSOT Plan

- 状态：`stale_docs`。
- 策略：`ssot_first`。
- Durable authority：补充 `guru-finalize-task` package contract 与 companion-script contract，明确 planless stale route 使用 Publication owner facts，而其他 exits 保持 plan-bound。
- 公共 Interface/schema：语义和字节合同不变，仅作为 projection/equality 验证对象。
- Generated/installed copies：由 canonical package 与 preset spec 经 `apply.sh` 同步，不手工建立第二套实现。
- Task artifacts：三份规划文档只记录 #253 的交付方案，不成为长期 Finalizer authority。

## Issue Scope

- Close：#253。
- Related：#251。
- Follow-up：#254。
