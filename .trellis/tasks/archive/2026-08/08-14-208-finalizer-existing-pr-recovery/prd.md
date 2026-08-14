# Issue #208：Finalizer 安全接管既有 Ready PR

## 目标

为 `guru-finalize-task` 增加严格受控的 `existing_pr_recovery` 路径，使同一变更请求的后续修复 task 在完成新的 Phase 2、task commit、Branch Review 与 Publication Review 后，复用同一 repository、head branch、base branch 上唯一的既有 Open PR，并继续完成 Finalizer 归档与 `ready_for_merge` 输出。

## 已确认事实

- Live Issue #208 是需求 SSOT，当前为 Open，最后更新时间为 2026-08-13T03:51:37Z。
- 前置 Issue #218 已于 2026-08-13 通过 PR #226 合并；当前基线为 `main@c8c2409cbb79759dae8be8ce95ce03655d5cf518`。
- #218 只处理同一 Finalizer 计划的 terminal DTO、单 JSON stdout 与 Ready 幂等恢复，明确不处理跨 task 的 existing-PR adoption。
- 当前 `finalization_pre_mutation_remote_preflight` 在无当前 task 私有 transaction 时，只要发现既有 Open PR 就返回 `pre_finalizer_remote_state_exists`；这正是 #208 的实现缺口。
- 当前 `resolve_closeout_pull_request` 已具备 repo/head/base 唯一性、fork 排除、canonical URL、PR HEAD 与 Draft/Ready 字段读取能力，可作为 recovery 候选解析基础。
- 当前 transaction schema 2.0 只表达普通首次发布状态 `push_content -> bind_draft -> archive -> push_archive -> mark_ready`；existing-PR recovery 必须成为显式状态分支，不能放宽普通首次发布合同。
- #205 已固定业务 Finalizer 不得调用或路由到 `guru-verify-extension-installation`；本任务必须保持该边界。

## 需求

### R1 显式 preview 与语义门禁

- Preview 只能在当前 Publication `ready` DTO、task、repository、remote、base/head branch、`branch_review_commit` 与 `publication_head` 全部 current 时识别 `existing_pr_recovery`。
- Preview 必须返回唯一 PR number/URL、PR 当前 Draft/Ready 状态、remote PR HEAD、reviewed/publication HEAD 的祖先关系、计划执行的 push、PR metadata convergence、archive、Ready 保持/转换动作与 fail-closed 条件。
- 普通首次发布仍要求零 Open PR；recovery 是显式独立分支，不得成为自动兜底。

### R2 候选 PR 与远端 HEAD 校验

- 候选必须是目标 repository 内同 head/base 的唯一 Open PR，canonical URL/number 有效，且不是 fork、Closed 或 Merged PR。
- live PR HEAD 必须等于 `publication_head`，或是 `publication_head` 的严格 Git 祖先且 fast-forward 检查通过。
- 非祖先、未知对象、force-push 漂移、多个候选、repo/head/base 不一致或无法检查 ancestry 时 fail closed。
- 不把任意 out-of-order push 追认为合法 recovery；只有 preview 与 transaction 绑定的 pre-push HEAD 可进入恢复。

### R3 Issue Scope 与 Publication authority

- 当前 task 的 `issue-scope-ledger.json` 必须与 PR 当前 close/related/follow-up 语义兼容，不得扩大、缩小或重写未由当前 Branch/Publication Review 覆盖的范围。
- PR title/body 只取自当前 Publication `ready` DTO；旧 PR body、旧 task、archive、旧 plan 或删除的 checkpoint 不构成 authority。
- 当前 Publication payload 与 live PR payload 不一致时，收敛目标只能是当前 reviewed title/body。

### R4 owner-private transaction 与执行

- 用户确认后，在首次 mutation 前把 recovery mode、精确 PR identity、PR 原始 Draft/Ready 状态、pre-push remote HEAD、reviewed/publication HEAD 与合法 transition 写入 owner-private transaction。
- remote HEAD 为严格祖先时只 push exact `publication_head`；已等于 publication HEAD 时只能进行同一 recovery transaction 的幂等恢复。
- 复用同一 PR，不关闭、不重开、不新建第二个 PR；title/body 收敛到当前 Publication DTO。
- 原 PR 为 Ready 时保持 Ready；原 PR 为 Draft 时继续使用既有 Draft-to-Ready transition。
- 继续执行 final projection、官方 task archive、唯一 archive commit/push 与 local/remote/PR HEAD 三方校验，最终只输出 current `ready_for_merge` DTO。

### R5 中断恢复与 fail closed

- 中断后只接受 transaction 中绑定的同一 PR、pre-push HEAD、publication HEAD、原始 Draft/Ready 状态与合法 next transition。
- PR identity、payload、Issue Scope、transaction、archive、summary、HEAD 或 current Publication 任一漂移时阻断，不自动修复。
- 当前 task 已存在冲突 archive、ambiguous PR binding、未知 transaction 状态或未审核 tracked drift 时阻断。

### R6 公共合同、投影与兼容性

- 同步 canonical Finalizer package、package runtime、Interface、schemas、examples、evals/tests，以及 installed/shared/Codex/Claude/Cursor copies。
- 如 transaction、gate、preview 或公共 interface 需要破坏性语义变化，使用新 schema/interface identity，并将旧版明确保留为 legacy；不得静默改变已有公共 API。
- 同步 `.trellis/spec/workflow/` 中 Finalizer 数据、companion script、skill package 与质量门禁 SSOT。
- 如用户可见安装/升级行为或资产清单变化，同步 preset README、installer inventory 与 extension version SSOT。

## 验收标准

1. 真实拓扑 fixture 包含：旧 task 已归档、同一 Ready PR 存在、修复 task active、新 `publication_head` 是旧 PR HEAD 的严格后代。
2. Preview 明确输出 `existing_pr_recovery`、唯一 PR identity、ancestry、原始 Draft/Ready 状态、动作计划与 fail-closed 条件。
3. 首次 mutation 前 transaction 已绑定精确 PR 与 pre-push HEAD；push 仅执行 exact publication HEAD fast-forward。
4. Ready PR recovery 不创建第二个 PR、不切回 Draft、不重复 Ready mutation；Draft PR recovery 沿用既有 Draft-to-Ready 合同。
5. PR title/body 收敛到当前 Publication DTO，Issue Scope 保持兼容，archive 与三方 HEAD 校验完成，输出唯一 `ready_for_merge` DTO。
6. 已推送后的同 transaction 恢复不重复 push；metadata、archive 或 Ready transition 中已完成的步骤均不重复 mutation。
7. 覆盖多个 PR、fork PR、Closed/Merged、repo/head/base mismatch、非祖先/未知 ancestry、force-push、scope/payload drift、stale Publication、archive 冲突与未知 transaction 的负向矩阵。
8. Current business Finalizer graph、runtime、examples 与 tests 不出现 `verification_required` 或 verifier 调用。
9. Finalizer package/runtime/integration tests、source-installed byte identity、registry/workflow graph、ownership、targeted preset apply/reapply、dogfood drift与零未知 sidecar通过。
10. 按风险完成 clean throwaway install/update 验证；若完整矩阵受环境限制，最终报告明确未验证项，不声称开箱即用。

## 范围外

- 不修改 Afizzy Issue #51 / PR #59 的业务实现或远端状态。
- 不自动 merge、关闭 Issue、部署业务仓库或清理业务 worktree。
- 不扩展为通用 PR 搜索、跨 branch/repository adoption 或对任意手工 push 的追认。
- 不恢复业务 `verification_required` 路由。
- 不处理恶意伪造、对抗输入、并发竞态、锁、TOCTOU 或额外 crash-consistency 加固。

## Docs SSOT Plan

- `trellis/skills/guru-team/packages/guru-finalize-task/{SKILL.md,references/contract.md}`：拥有 existing-PR recovery 的语义门禁、确认、transaction、恢复与 typed exit 合同。
- `.trellis/spec/workflow/data-contracts.md`：拥有 recovery transaction、PR identity、ancestry、scope/payload binding 的持久数据定义。
- `.trellis/spec/workflow/companion-scripts.md`：拥有 preview/record/check/execute 的确定性边界与 mutation 顺序。
- `.trellis/spec/workflow/skill-package-contract.md`：拥有 Interface、schema/version、public/private I/O 与投影规则。
- `.trellis/spec/workflow/quality-guidelines.md`：拥有真实拓扑、负向矩阵、source-installed、preset/update/throwaway 验收要求。
- `trellis/presets/guru-team/README.md` 与 `trellis/guru-team-extension.json`：仅在安装资产、用户可见合同或 extension 版本发生变化时更新。
- Global workflow 的 Skill id、六个 Finalizer exits 与 `ready_for_merge -> guru-merge-task-pr` 路由保持不变。
